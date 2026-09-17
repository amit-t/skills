import datetime
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from report_usage import append_usage
from retire_review import (
    build_report,
    compute_skill_stats,
    find_conflicts,
    load_usage_rows,
    propose_action,
    run_retire_review,
)

REPORT_USAGE = SCRIPTS_DIR / "report_usage.py"
RETIRE_REVIEW = SCRIPTS_DIR / "retire_review.py"

DEFAULT_CFG = {
    "feedback": {"review_window_days": 90, "validated_min_good_reports": 5},
    "library_size_warning": 20,
}


def make_skill_entry(status="provisional", trigger_description="does a thing", task_type="tt"):
    return {
        "path": "skills/x/SKILL.md",
        "status": status,
        "version": "1.0",
        "task_type": task_type,
        "trigger_description": trigger_description,
        "supporting_sessions": ["sess-001"],
        "created_at": "2026-01-01T00:00:00+00:00",
        "updated_at": "2026-01-01T00:00:00+00:00",
        "superseded_by": None,
        "human_edited": False,
    }


def make_registry(skills):
    return {
        "extractor_version": "1.0",
        "skills": skills,
        "suppressed_task_types": [],
        "runs": [],
    }


def iso(dt):
    return dt.isoformat()


def usage_row(skill, outcome, at, note=""):
    return {"skill": skill, "outcome": outcome, "note": note, "at": at}


def write_usage_log(feedback_dir, rows, extra_raw_lines=None):
    feedback_dir = Path(feedback_dir)
    feedback_dir.mkdir(parents=True, exist_ok=True)
    lines = [json.dumps(r) for r in rows] + list(extra_raw_lines or [])
    text = "\n".join(lines)
    if lines:
        text += "\n"
    (feedback_dir / "usage-log.jsonl").write_text(text, encoding="utf-8")


class FeedbackFixture:
    """Tempdir with registry.json + feedback dir + out dir."""

    def __enter__(self):
        self._tmp_ctx = tempfile.TemporaryDirectory()
        self.tmp = Path(self._tmp_ctx.name)
        self.registry = self.tmp / "registry.json"
        self.feedback_dir = self.tmp / "feedback"
        self.out_dir = self.tmp / "review-queue"
        return self

    def __exit__(self, *exc):
        self._tmp_ctx.cleanup()

    def write_registry(self, skills):
        self.registry.write_text(json.dumps(make_registry(skills)), encoding="utf-8")


class TestReportUsageAppendsJsonLine(unittest.TestCase):
    def test_append_writes_valid_json_line_with_four_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            feedback_dir = Path(tmp) / "feedback"
            row = append_usage("my-skill", "good", "worked great", feedback_dir)

            log_path = feedback_dir / "usage-log.jsonl"
            self.assertTrue(log_path.is_file())
            line = log_path.read_text(encoding="utf-8").strip()
            parsed = json.loads(line)

            self.assertEqual(set(parsed.keys()), {"skill", "outcome", "note", "at"})
            self.assertEqual(parsed["skill"], "my-skill")
            self.assertEqual(parsed["outcome"], "good")
            self.assertEqual(parsed["note"], "worked great")
            self.assertEqual(parsed, row)
            # "at" must be a parseable ISO-8601 timestamp
            datetime.datetime.fromisoformat(parsed["at"])

    def test_creates_dir_and_file_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            feedback_dir = Path(tmp) / "nested" / "feedback"
            self.assertFalse(feedback_dir.exists())
            append_usage("my-skill", "neutral", None, feedback_dir)
            self.assertTrue((feedback_dir / "usage-log.jsonl").is_file())

    def test_note_defaults_to_empty_string_when_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            row = append_usage("my-skill", "poor", None, Path(tmp) / "feedback")
            self.assertEqual(row["note"], "")

    def test_appends_multiple_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            feedback_dir = Path(tmp) / "feedback"
            append_usage("my-skill", "good", "one", feedback_dir)
            append_usage("my-skill", "poor", "two", feedback_dir)
            lines = (feedback_dir / "usage-log.jsonl").read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["note"], "one")
            self.assertEqual(json.loads(lines[1])["note"], "two")


class TestReportUsageCli(unittest.TestCase):
    def test_cli_appends_line_and_exits_0(self):
        with tempfile.TemporaryDirectory() as tmp:
            feedback_dir = Path(tmp) / "feedback"
            result = subprocess.run(
                [
                    sys.executable, str(REPORT_USAGE),
                    "skill-x", "--outcome", "good", "--note", "worked great",
                    "--feedback-dir", str(feedback_dir),
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            line = (feedback_dir / "usage-log.jsonl").read_text(encoding="utf-8").strip()
            parsed = json.loads(line)
            self.assertEqual(set(parsed.keys()), {"skill", "outcome", "note", "at"})
            self.assertEqual(parsed["skill"], "skill-x")
            self.assertEqual(parsed["outcome"], "good")
            self.assertEqual(parsed["note"], "worked great")

    def test_cli_invalid_outcome_exits_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            feedback_dir = Path(tmp) / "feedback"
            result = subprocess.run(
                [
                    sys.executable, str(REPORT_USAGE),
                    "skill-x", "--outcome", "bogus", "--feedback-dir", str(feedback_dir),
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertIn("invalid choice", result.stderr)
            self.assertFalse((feedback_dir / "usage-log.jsonl").exists())

    def test_cli_default_feedback_dir_from_config(self):
        with tempfile.TemporaryDirectory() as tmp:
            custom_feedback_dir = Path(tmp) / "custom-feedback"
            config_path = Path(tmp) / "config.json"
            config_path.write_text(
                json.dumps({"feedback_dir": str(custom_feedback_dir)}), encoding="utf-8"
            )
            result = subprocess.run(
                [
                    sys.executable, str(REPORT_USAGE),
                    "skill-x", "--outcome", "good", "--config", str(config_path),
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((custom_feedback_dir / "usage-log.jsonl").is_file())


class TestLoadUsageRowsTolerance(unittest.TestCase):
    """Malformed lines are skipped silently -- never fatal (contract requirement)."""

    def test_bad_json_and_missing_keys_are_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            feedback_dir = Path(tmp) / "feedback"
            good_row = usage_row("skill-a", "good", iso(datetime.datetime.now(datetime.timezone.utc)))
            write_usage_log(
                feedback_dir,
                [good_row],
                extra_raw_lines=[
                    "not valid json{{{",
                    json.dumps({"skill": "skill-a"}),  # missing outcome/at
                    "",
                    json.dumps(["not", "a", "dict"]),
                ],
            )
            rows = load_usage_rows(feedback_dir)
            self.assertEqual(rows, [good_row])

    def test_missing_file_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_usage_rows(Path(tmp) / "no-such-dir"), [])


class TestComputeSkillStatsAndProposeAction(unittest.TestCase):
    def test_promote_to_validated_on_five_good_zero_poor(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        rows = [usage_row("skill-a", "good", iso(now)) for _ in range(5)]
        usage_count, counts = compute_skill_stats("skill-a", rows, now, 90)
        self.assertEqual(usage_count, 5)
        self.assertEqual(counts, {"good": 5, "neutral": 0, "poor": 0})
        self.assertEqual(propose_action("provisional", usage_count, counts, DEFAULT_CFG), "promote_to_validated")

    def test_promote_not_proposed_if_already_validated(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        rows = [usage_row("skill-a", "good", iso(now)) for _ in range(5)]
        usage_count, counts = compute_skill_stats("skill-a", rows, now, 90)
        self.assertEqual(propose_action("validated", usage_count, counts, DEFAULT_CFG), "keep")

    def test_retire_on_zero_usage(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        usage_count, counts = compute_skill_stats("skill-b", [], now, 90)
        self.assertEqual(usage_count, 0)
        self.assertEqual(propose_action("provisional", usage_count, counts, DEFAULT_CFG), "retire")

    def test_revise_on_poor_heavy(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        rows = [
            usage_row("skill-c", "poor", iso(now)),
            usage_row("skill-c", "poor", iso(now)),
            usage_row("skill-c", "good", iso(now)),
            usage_row("skill-c", "neutral", iso(now)),
        ]
        usage_count, counts = compute_skill_stats("skill-c", rows, now, 90)
        self.assertEqual(usage_count, 4)
        self.assertEqual(propose_action("provisional", usage_count, counts, DEFAULT_CFG), "revise")

    def test_keep_when_neither_threshold_met(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        rows = [usage_row("skill-d", "good", iso(now)), usage_row("skill-d", "neutral", iso(now))]
        usage_count, counts = compute_skill_stats("skill-d", rows, now, 90)
        self.assertEqual(propose_action("provisional", usage_count, counts, DEFAULT_CFG), "keep")

    def test_rows_outside_window_are_excluded(self):
        now = datetime.datetime.now(datetime.timezone.utc)
        old = now - datetime.timedelta(days=100)
        rows = [usage_row("skill-e", "good", iso(old)) for _ in range(5)]
        usage_count, counts = compute_skill_stats("skill-e", rows, now, 90)
        self.assertEqual(usage_count, 0)
        self.assertEqual(propose_action("provisional", usage_count, counts, DEFAULT_CFG), "retire")


class TestFindConflicts(unittest.TestCase):
    def test_near_identical_trigger_descriptions_are_a_conflict_pair(self):
        skills = {
            "migrate-jest-a": make_skill_entry(trigger_description="migrate jest tests to vitest"),
            "migrate-jest-b": make_skill_entry(trigger_description="migrate jest tests into vitest"),
            "deploy-terraform": make_skill_entry(trigger_description="apply a terraform plan to provision cloud infra"),
        }
        conflicts = find_conflicts(skills)
        self.assertIn(["migrate-jest-a", "migrate-jest-b"], conflicts)
        self.assertEqual(len(conflicts), 1)


class TestBuildReportLibrarySizeWarning(unittest.TestCase):
    def test_twenty_one_skills_triggers_library_size_warning(self):
        skills = {"skill-%02d" % i: make_skill_entry() for i in range(21)}
        registry = make_registry(skills)
        report_text, summary = build_report(registry, [], 90, DEFAULT_CFG, "2026-09-17")
        self.assertTrue(summary["warning"])
        self.assertIn("library size", report_text.lower())

    def test_twenty_skills_does_not_trigger_warning(self):
        skills = {"skill-%02d" % i: make_skill_entry() for i in range(20)}
        registry = make_registry(skills)
        _report_text, summary = build_report(registry, [], 90, DEFAULT_CFG, "2026-09-17")
        self.assertFalse(summary["warning"])


class TestRunRetireReviewEndToEnd(unittest.TestCase):
    def test_writes_report_file_and_never_mutates_registry(self):
        with FeedbackFixture() as fx:
            skills = {
                "skill-a": make_skill_entry(status="provisional", trigger_description="migrate jest tests to vitest"),
                "skill-b": make_skill_entry(status="provisional", trigger_description="migrate jest tests into vitest"),
                "skill-c": make_skill_entry(status="provisional", trigger_description="deploy a terraform stack"),
            }
            fx.write_registry(skills)
            registry_bytes_before = fx.registry.read_bytes()

            now = datetime.datetime.now(datetime.timezone.utc)
            rows = [usage_row("skill-a", "good", iso(now)) for _ in range(5)]
            write_usage_log(fx.feedback_dir, rows)

            report_path, summary = run_retire_review(
                str(fx.registry), str(fx.feedback_dir), None, str(fx.out_dir), DEFAULT_CFG,
            )

            self.assertTrue(report_path.is_file())
            self.assertEqual(summary["proposals"]["skill-a"], "promote_to_validated")
            self.assertEqual(summary["proposals"]["skill-c"], "retire")
            self.assertIn(["skill-a", "skill-b"], summary["conflicts"])
            self.assertFalse(summary["warning"])

            # never mutates the registry
            self.assertEqual(fx.registry.read_bytes(), registry_bytes_before)
            # never deletes the feedback log
            self.assertTrue((fx.feedback_dir / "usage-log.jsonl").is_file())

    def test_missing_registry_defaults_to_no_skills(self):
        with FeedbackFixture() as fx:
            report_path, summary = run_retire_review(
                str(fx.registry), str(fx.feedback_dir), None, str(fx.out_dir), DEFAULT_CFG,
            )
            self.assertTrue(report_path.is_file())
            self.assertEqual(summary["proposals"], {})
            self.assertEqual(summary["conflicts"], [])
            self.assertFalse(summary["warning"])


class TestRetireReviewCli(unittest.TestCase):
    def test_cli_prints_json_summary_and_writes_report(self):
        with FeedbackFixture() as fx:
            skills = {"skill-a": make_skill_entry(status="provisional")}
            fx.write_registry(skills)
            write_usage_log(fx.feedback_dir, [])

            result = subprocess.run(
                [
                    sys.executable, str(RETIRE_REVIEW),
                    "--registry", str(fx.registry),
                    "--feedback-dir", str(fx.feedback_dir),
                    "--window-days", "90",
                    "--out", str(fx.out_dir),
                ],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertEqual(set(payload.keys()), {"proposals", "conflicts", "warning"})
            self.assertEqual(payload["proposals"]["skill-a"], "retire")

            today_str = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
            report_path = fx.out_dir / ("retirement-%s.md" % today_str)
            self.assertTrue(report_path.is_file())


if __name__ == "__main__":
    unittest.main()
