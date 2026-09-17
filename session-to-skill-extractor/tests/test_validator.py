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

from validate_candidate import validate, load_blacklist, _anti_patterns_path

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "candidates"
VALIDATE_CANDIDATE = SCRIPTS_DIR / "validate_candidate.py"

DEFAULT_CFG = {
    "identify": {"flag_min_questions_at_2": 3, "flag_min_total": 7, "q2_min": 1},
}


def load_fixture(name):
    with open(FIXTURES_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def blacklist():
    return load_blacklist(_anti_patterns_path(DEFAULT_CFG))


class TestGoodCandidatePasses(unittest.TestCase):
    """E3-7: a realistic, well-formed D2 candidate produces no errors."""

    def test_good_json_has_no_errors(self):
        candidate = load_fixture("good.json")
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertEqual(errors, [])


class TestVagueCandidateFails(unittest.TestCase):
    """vague.json: a blacklisted step phrase + an uncheckable expected_output -> >=2 errors."""

    def test_vague_json_has_at_least_two_errors(self):
        candidate = load_fixture("vague.json")
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertGreaterEqual(len(errors), 2)

        joined = " | ".join(errors).lower()
        self.assertIn("blacklist", joined)
        self.assertIn("not checkable", joined)


class TestRubricTotalMismatch(unittest.TestCase):
    """rubric.total must equal q1+...+q5, else validation fails."""

    def test_total_mismatch_fails(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["rubric"]["total"] = candidate["rubric"]["total"] + 1
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(any("rubric total mismatch" in e.lower() for e in errors))


class TestSingleSessionRequiresHumanReview(unittest.TestCase):
    """evidence.supporting_sessions == 1 with requires_human_review false must fail."""

    def test_single_session_without_review_flag_fails(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["evidence"]["supporting_sessions"] = 1
        candidate["evidence"]["sessions"] = candidate["evidence"]["sessions"][:1]
        candidate["requires_human_review"] = False
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(any("requires_human_review" in e for e in errors))


class TestEmptyDecisionPointsWithoutLinear(unittest.TestCase):
    """decision_points empty and linear not true must fail (spec C5 Stage 3)."""

    def test_empty_decision_points_without_linear_fails(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["decision_points"] = []
        candidate.pop("linear", None)
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(any("decision_points" in e and "linear" in e for e in errors))

    def test_empty_decision_points_with_linear_true_passes_that_check(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["decision_points"] = []
        candidate["linear"] = True
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertFalse(any("decision_points" in e and "linear" in e for e in errors))


class TestRubricFlagRule(unittest.TestCase):
    """An unflaggable rubric (e.g. q2=0) must not pass validation."""

    def test_q2_zero_never_flags(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["rubric"] = {"q1": 2, "q2": 0, "q3": 2, "q4": 2, "q5": 2, "total": 8}
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(any("flag rule" in e.lower() for e in errors))


class TestMissingRequiredKeys(unittest.TestCase):
    def test_missing_key_reported(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        del candidate["expected_output"]
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(any("expected_output" in e for e in errors))


class TestSuppressedTaskType(unittest.TestCase):
    """Item B: validate() takes an optional registry dict and rejects a candidate
    whose task_type has an unexpired suppression entry (registry.json
    suppressed_task_types, written by promote.py's reject path but never
    previously enforced anywhere)."""

    def _registry_with_suppression(self, task_type, until, reason="not generalizable enough"):
        return {
            "suppressed_task_types": [
                {"task_type": task_type, "until": until, "reason": reason},
            ]
        }

    def test_unexpired_suppression_fails(self):
        candidate = load_fixture("good.json")
        future = (
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
        ).isoformat()
        registry = self._registry_with_suppression(candidate["task_type"], future)
        errors = validate(candidate, blacklist(), DEFAULT_CFG, registry)
        self.assertTrue(any("suppressed" in e.lower() for e in errors))
        self.assertTrue(any("not generalizable enough" in e for e in errors))

    def test_expired_suppression_passes(self):
        candidate = load_fixture("good.json")
        past = (
            datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(days=1)
        ).isoformat()
        registry = self._registry_with_suppression(candidate["task_type"], past)
        errors = validate(candidate, blacklist(), DEFAULT_CFG, registry)
        self.assertEqual(errors, [])

    def test_no_registry_does_not_suppress(self):
        candidate = load_fixture("good.json")
        errors = validate(candidate, blacklist(), DEFAULT_CFG, None)
        self.assertEqual(errors, [])

    def test_cli_registry_flag_suppressed_exits_1_with_error(self):
        candidate = load_fixture("good.json")
        future = (
            datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=10)
        ).isoformat()
        registry = self._registry_with_suppression(candidate["task_type"], future)
        with tempfile.TemporaryDirectory() as tmp:
            registry_path = Path(tmp) / "registry.json"
            registry_path.write_text(json.dumps(registry), encoding="utf-8")
            result = subprocess.run(
                [
                    sys.executable, str(VALIDATE_CANDIDATE),
                    "--candidate", str(FIXTURES_DIR / "good.json"),
                    "--registry", str(registry_path),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 1)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(any("suppressed" in e.lower() for e in payload["errors"]))


class TestMalformedCandidateNeverCrashes(unittest.TestCase):
    """Item F: every check must type-guard its inputs and collect an error string
    instead of raising -- a malformed candidate is a validation failure, not a
    crash."""

    def test_steps_as_string_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["steps"] = "do stuff"
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)
        self.assertTrue(any("steps" in e.lower() for e in errors))

    def test_rubric_null_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["rubric"] = None
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)

    def test_rubric_non_dict_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["rubric"] = "high"
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)
        self.assertTrue(any("rubric" in e.lower() for e in errors))

    def test_trigger_non_dict_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["trigger"] = "some trigger text"
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)
        self.assertTrue(any("trigger" in e.lower() for e in errors))

    def test_edge_cases_non_list_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["edge_cases"] = "none observed"
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)
        self.assertTrue(any("edge_cases" in e.lower() for e in errors))

    def test_decision_points_non_list_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["decision_points"] = {"not": "a list"}
        candidate.pop("linear", None)
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)
        self.assertTrue(any("decision_points" in e.lower() for e in errors))

    def test_step_entry_non_dict_reports_error_not_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["steps"] = [candidate["steps"][0], "not a step object", candidate["steps"][1]]
        errors = validate(candidate, blacklist(), DEFAULT_CFG)
        self.assertTrue(errors)
        self.assertTrue(any("step entry" in e.lower() for e in errors))

    def test_cli_steps_string_exits_1_no_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["steps"] = "do stuff"
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATE_CANDIDATE), "--candidate", str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])

    def test_cli_rubric_null_exits_1_no_traceback(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["rubric"] = None
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.json"
            path.write_text(json.dumps(candidate), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATE_CANDIDATE), "--candidate", str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])

    def test_cli_malformed_json_file_exits_1_no_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "candidate.json"
            path.write_text("{not valid json", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(VALIDATE_CANDIDATE), "--candidate", str(path)],
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertNotIn("Traceback", result.stdout)
            self.assertNotIn("Traceback", result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["ok"])
            self.assertTrue(any("malformed" in e.lower() for e in payload["errors"]))


class TestValidateCandidateCli(unittest.TestCase):
    def test_cli_exits_0_ok_true_for_good_candidate(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATE_CANDIDATE), "--candidate", str(FIXTURES_DIR / "good.json")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout), {"ok": True})

    def test_cli_exits_1_ok_false_with_errors_for_vague_candidate(self):
        result = subprocess.run(
            [sys.executable, str(VALIDATE_CANDIDATE), "--candidate", str(FIXTURES_DIR / "vague.json")],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 1)
        payload = json.loads(result.stdout)
        self.assertFalse(payload["ok"])
        self.assertGreaterEqual(len(payload["errors"]), 2)


if __name__ == "__main__":
    unittest.main()
