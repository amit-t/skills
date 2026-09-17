import copy
import datetime
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from render_skill import render_candidate
from promote import cmd_promote, PromoteError

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CANDIDATES_DIR = FIXTURES_DIR / "candidates"
PROMOTE = SCRIPTS_DIR / "promote.py"

DEFAULT_CFG = {
    "recurrence": {"provisional_min_sessions": 20, "validated_min_sessions": 30},
    "review": {"reject_suppress_days": 30},
}


def load_fixture(name):
    with open(CANDIDATES_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


class PromoteFixture:
    """Sets up a tempdir with queue/skill-dir/registry and a rendered candidate."""

    def __enter__(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)
        self.queue = self.tmp / "review-queue"
        self.skill_dir = self.tmp / "skills"
        self.registry = self.tmp / "registry.json"
        self.queue.mkdir()
        self.skill_dir.mkdir()
        return self

    def __exit__(self, *exc):
        self._tmp_ctx.cleanup()

    def render(self, candidate):
        candidate_path = self.tmp / "candidate.json"
        candidate_path.write_text(json.dumps(candidate), encoding="utf-8")
        return render_candidate(str(candidate_path), str(self.queue))


class TestPromoteAcceptMovesFolderAndRegisters(unittest.TestCase):
    """3-session candidate + accept -> provisional (reviewer-accept, below 20)."""

    def test_accept_provisional_status(self):
        with PromoteFixture() as fx:
            candidate = load_fixture("good.json")
            fx.render(candidate)

            result = cmd_promote(
                "cs-20260917-jest-to-vitest", "accept",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
            )
            self.assertTrue(result["ok"])
            self.assertEqual(result["status"], "provisional")

            skill_md = (fx.skill_dir / "jest-to-vitest-migration" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("status: provisional", skill_md)
            self.assertTrue((fx.skill_dir / "jest-to-vitest-migration" / ".candidate.json").is_file())

            self.assertFalse((fx.queue / "cs-20260917-jest-to-vitest").exists())
            self.assertTrue((fx.queue / "promoted" / "cs-20260917-jest-to-vitest").is_dir())

            registry = json.loads(fx.registry.read_text(encoding="utf-8"))
            entry = registry["skills"]["jest-to-vitest-migration"]
            self.assertEqual(entry["status"], "provisional")
            self.assertEqual(entry["task_type"], "migrate-jest-to-vitest")
            self.assertEqual(entry["supporting_sessions"], ["sess-001", "sess-002", "sess-003"])
            self.assertIsNone(entry["superseded_by"])
            self.assertFalse(entry["human_edited"])
            self.assertEqual(registry["extractor_version"], "1.0")


class TestPromoteAcceptThirtySessionsValidated(unittest.TestCase):
    """30-session candidate + accept -> validated."""

    def test_thirty_sessions_validated_status(self):
        with PromoteFixture() as fx:
            candidate = copy.deepcopy(load_fixture("good.json"))
            candidate["evidence"]["supporting_sessions"] = 30
            fx.render(candidate)

            result = cmd_promote(
                "cs-20260917-jest-to-vitest", "accept",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
            )
            self.assertEqual(result["status"], "validated")

            skill_md = (fx.skill_dir / "jest-to-vitest-migration" / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("status: validated", skill_md)

            registry = json.loads(fx.registry.read_text(encoding="utf-8"))
            self.assertEqual(registry["skills"]["jest-to-vitest-migration"]["status"], "validated")


class TestPromoteEditSetsHumanEdited(unittest.TestCase):
    def test_edit_sets_human_edited_true(self):
        with PromoteFixture() as fx:
            candidate = load_fixture("good.json")
            fx.render(candidate)

            cmd_promote(
                "cs-20260917-jest-to-vitest", "edit",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
            )
            registry = json.loads(fx.registry.read_text(encoding="utf-8"))
            self.assertTrue(registry["skills"]["jest-to-vitest-migration"]["human_edited"])


class TestPromoteRegistryPathRelative(unittest.TestCase):
    def test_registry_path_is_relative_to_registry_dir(self):
        with PromoteFixture() as fx:
            candidate = load_fixture("good.json")
            fx.render(candidate)
            cmd_promote(
                "cs-20260917-jest-to-vitest", "accept",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
            )
            registry = json.loads(fx.registry.read_text(encoding="utf-8"))
            path = registry["skills"]["jest-to-vitest-migration"]["path"]
            self.assertFalse(Path(path).is_absolute())
            resolved = (fx.registry.parent / path).resolve()
            self.assertTrue(resolved.is_file())
            self.assertEqual(resolved.name, "SKILL.md")


class TestPromoteReject(unittest.TestCase):
    def test_reject_moves_and_writes_reason_and_suppression(self):
        with PromoteFixture() as fx:
            candidate = load_fixture("good.json")
            fx.render(candidate)

            result = cmd_promote(
                "cs-20260917-jest-to-vitest", "reject",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), "not generalizable enough", DEFAULT_CFG,
            )
            self.assertTrue(result["ok"])

            self.assertFalse((fx.queue / "cs-20260917-jest-to-vitest").exists())
            rejected_dir = fx.queue / "rejected" / "cs-20260917-jest-to-vitest"
            self.assertTrue(rejected_dir.is_dir())
            reason_text = (rejected_dir / "reason.txt").read_text(encoding="utf-8")
            self.assertIn("not generalizable enough", reason_text)

            registry = json.loads(fx.registry.read_text(encoding="utf-8"))
            self.assertEqual(len(registry["suppressed_task_types"]), 1)
            suppression = registry["suppressed_task_types"][0]
            self.assertEqual(suppression["task_type"], "migrate-jest-to-vitest")
            self.assertEqual(suppression["reason"], "not generalizable enough")

            until = datetime.datetime.fromisoformat(suppression["until"])
            now = datetime.datetime.now(datetime.timezone.utc)
            self.assertGreater(until, now)

    def test_reject_without_reason_uses_unspecified(self):
        with PromoteFixture() as fx:
            candidate = load_fixture("good.json")
            fx.render(candidate)
            cmd_promote(
                "cs-20260917-jest-to-vitest", "reject",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
            )
            rejected_dir = fx.queue / "rejected" / "cs-20260917-jest-to-vitest"
            reason_text = (rejected_dir / "reason.txt").read_text(encoding="utf-8")
            self.assertIn("unspecified", reason_text)


class TestPromoteRegistryCreatedOnFirstUse(unittest.TestCase):
    def test_registry_created_with_skeleton(self):
        with PromoteFixture() as fx:
            self.assertFalse(fx.registry.exists())
            candidate = load_fixture("good.json")
            fx.render(candidate)
            cmd_promote(
                "cs-20260917-jest-to-vitest", "accept",
                str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
            )
            registry = json.loads(fx.registry.read_text(encoding="utf-8"))
            self.assertEqual(registry["extractor_version"], "1.0")
            self.assertIn("jest-to-vitest-migration", registry["skills"])
            self.assertEqual(registry["suppressed_task_types"], [])
            self.assertEqual(registry["runs"], [])


class TestPromoteMissingCandidateRaises(unittest.TestCase):
    def test_missing_candidate_id_raises_promote_error(self):
        with PromoteFixture() as fx:
            with self.assertRaises(PromoteError):
                cmd_promote(
                    "no-such-candidate", "accept",
                    str(fx.queue), str(fx.skill_dir), str(fx.registry), None, DEFAULT_CFG,
                )


class TestPromoteCli(unittest.TestCase):
    def test_cli_missing_candidate_exits_1_one_line_stderr_no_traceback(self):
        with PromoteFixture() as fx:
            result = subprocess.run(
                [
                    sys.executable, str(PROMOTE),
                    "no-such-candidate", "accept",
                    "--queue", str(fx.queue),
                    "--skill-dir", str(fx.skill_dir),
                    "--registry", str(fx.registry),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            stderr_lines = [l for l in result.stderr.splitlines() if l.strip()]
            self.assertEqual(len(stderr_lines), 1)

    def test_cli_accept_success_exits_0(self):
        with PromoteFixture() as fx:
            candidate = load_fixture("good.json")
            fx.render(candidate)
            result = subprocess.run(
                [
                    sys.executable, str(PROMOTE),
                    "cs-20260917-jest-to-vitest", "accept",
                    "--queue", str(fx.queue),
                    "--skill-dir", str(fx.skill_dir),
                    "--registry", str(fx.registry),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(payload["status"], "provisional")


if __name__ == "__main__":
    unittest.main()
