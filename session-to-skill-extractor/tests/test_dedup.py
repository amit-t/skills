import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from dedup_prescreen import tokenize, build_shortlist

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CANDIDATES_DIR = FIXTURES_DIR / "candidates"
SKILLDIR = FIXTURES_DIR / "skilldir"
DEDUP_PRESCREEN = SCRIPTS_DIR / "dedup_prescreen.py"


def load_fixture(name):
    with open(CANDIDATES_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


class TestTokenize(unittest.TestCase):
    def test_lowercases_and_splits_on_non_alnum(self):
        self.assertEqual(tokenize("Jest-To-Vitest Migration!"), {"jest", "vitest", "migration"})

    def test_drops_stopwords_and_empty_strings(self):
        self.assertEqual(tokenize("use the for a and or in on with when this that"), set())

    def test_empty_and_none_return_empty_set(self):
        self.assertEqual(tokenize(""), set())
        self.assertEqual(tokenize(None), set())


class TestDedupShortlistsNearDuplicate(unittest.TestCase):
    """E3-5: good.json vs a near-identical fixture SKILL.md scores >= 0.3 and is shortlisted."""

    def test_near_identical_skill_is_shortlisted(self):
        candidate = load_fixture("good.json")
        shortlist = build_shortlist(candidate, [str(SKILLDIR)], registry=None, threshold=0.3)
        self.assertTrue(shortlist)
        entry = shortlist[0]
        self.assertEqual(entry["skill"], "jest-to-vitest-migration")
        self.assertGreaterEqual(entry["score"], 0.3)
        self.assertIn("SKILL.md", entry["path"])

    def test_shortlist_sorted_desc_by_score(self):
        candidate = load_fixture("good.json")
        shortlist = build_shortlist(candidate, [str(SKILLDIR)], registry=None, threshold=0.0)
        scores = [e["score"] for e in shortlist]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestDedupUnrelatedSkillNotShortlisted(unittest.TestCase):
    """An unrelated SKILL.md (different domain entirely) produces an empty shortlist."""

    def test_unrelated_skill_not_shortlisted(self):
        candidate = load_fixture("good.json")
        with tempfile.TemporaryDirectory() as tmp:
            skill_dir = Path(tmp) / "deploy-terraform-infra"
            skill_dir.mkdir()
            (skill_dir / "SKILL.md").write_text(
                "---\n"
                "name: deploy-terraform-infra\n"
                "description: Applies a terraform plan to provision cloud infrastructure resources.\n"
                "---\n\n"
                "# Deploy Terraform Infra\n",
                encoding="utf-8",
            )
            shortlist = build_shortlist(candidate, [tmp], registry=None, threshold=0.3)
        self.assertEqual(shortlist, [])


class TestDedupMissingSkillDirAndRegistry(unittest.TestCase):
    """Nonexistent skill dirs and a missing registry are skipped silently, no crash."""

    def test_missing_dirs_and_registry_do_not_crash(self):
        candidate = load_fixture("good.json")
        shortlist = build_shortlist(
            candidate,
            ["/no/such/skill/dir", str(SKILLDIR)],
            registry=None,
            threshold=0.3,
        )
        self.assertTrue(shortlist)


class TestDedupRegistryMatch(unittest.TestCase):
    """A registry skill entry (name + trigger_description) participates in scoring too."""

    def test_registry_entry_shortlisted(self):
        candidate = load_fixture("good.json")
        registry = {
            "extractor_version": "1.0",
            "skills": {
                "jest-to-vitest-migration": {
                    "path": "skills/jest-to-vitest-migration/SKILL.md",
                    "status": "validated",
                    "version": "1.0",
                    "task_type": "migrate-jest-to-vitest",
                    "trigger_description": (
                        "User asks to migrate a Jest test suite to Vitest, translating "
                        "jest.config and mocks."
                    ),
                    "supporting_sessions": ["sess-001"],
                    "created_at": "2026-01-01T00:00:00+00:00",
                    "updated_at": "2026-01-01T00:00:00+00:00",
                    "superseded_by": None,
                    "human_edited": False,
                }
            },
            "suppressed_task_types": [],
            "runs": [],
        }
        shortlist = build_shortlist(candidate, [], registry=registry, threshold=0.3)
        self.assertTrue(any(e["skill"] == "jest-to-vitest-migration" for e in shortlist))


class TestDedupPrescreenCli(unittest.TestCase):
    def test_cli_outputs_shortlist_json(self):
        result = subprocess.run(
            [
                sys.executable, str(DEDUP_PRESCREEN),
                "--candidate", str(CANDIDATES_DIR / "good.json"),
                "--skill-dirs", str(SKILLDIR),
                "--registry", "/no/such/registry.json",
                "--threshold", "0.3",
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        payload = json.loads(result.stdout)
        self.assertIn("shortlist", payload)
        self.assertTrue(payload["shortlist"])
        self.assertEqual(payload["shortlist"][0]["skill"], "jest-to-vitest-migration")


if __name__ == "__main__":
    unittest.main()
