import copy
import json
import subprocess
import sys
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
