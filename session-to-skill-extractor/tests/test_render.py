import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from render_skill import render_skill_md, render_review_md, render_candidate, title_case_name

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CANDIDATES_DIR = FIXTURES_DIR / "candidates"
RENDER_SKILL = SCRIPTS_DIR / "render_skill.py"

EXPECTED_H2_SEQUENCE = [
    "Trigger", "Prerequisites", "Steps", "Decision points",
    "Expected output", "Edge cases", "Provenance", "Feedback",
]

DEFAULT_CFG = {
    "identify": {"flag_min_questions_at_2": 3, "flag_min_total": 7, "q2_min": 1},
}

_DOLLAR_RESIDUE_RE = re.compile(r"\$\{?[a-z_]+")
_FRONTMATTER_LINE_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


def load_fixture(name):
    with open(CANDIDATES_DIR / name, "r", encoding="utf-8") as f:
        return json.load(f)


def h2_headings(text):
    return re.findall(r"^## (.+)$", text, re.MULTILINE)


def parse_frontmatter(text):
    """Minimal 'key: value' frontmatter parser (top-level keys only, quotes stripped)."""
    lines = text.splitlines()
    assert lines[0].strip() == "---"
    body = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        body.append(line)
    result = {}
    for line in body:
        m = _FRONTMATTER_LINE_RE.match(line.strip())
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        result.setdefault(key, value)
    return result


class TestTitleCaseName(unittest.TestCase):
    def test_hyphens_become_spaces_and_title_cased(self):
        self.assertEqual(title_case_name("jest-to-vitest-migration"), "Jest To Vitest Migration")


class TestRenderSkillMdH2Sequence(unittest.TestCase):
    """Brief Step 1: the rendered SKILL.md's H2 headings appear in exact spec order."""

    def test_h2_sequence_matches_spec_exactly(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertEqual(h2_headings(text), EXPECTED_H2_SEQUENCE)


class TestRenderSkillMdFrontmatter(unittest.TestCase):
    def test_frontmatter_has_name_description_and_correct_status(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        fm = parse_frontmatter(text)
        self.assertEqual(fm.get("name"), "jest-to-vitest-migration")
        self.assertTrue(fm.get("description"))
        self.assertEqual(fm.get("status"), "candidate")

    def test_frontmatter_metadata_fields(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn("extracted_by: session-to-skill-extractor/1.0", text)
        self.assertIn("extracted_from_host: claude-code", text)
        self.assertIn("supporting_sessions: 3", text)
        self.assertIn("requires_human_review: true", text)
        self.assertIn("superseded_by: null", text)


class TestRenderSkillMdNoDollarResidue(unittest.TestCase):
    def test_no_unsubstituted_placeholders(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIsNone(_DOLLAR_RESIDUE_RE.search(text), text)


class TestRenderSkillMdBodySections(unittest.TestCase):
    def test_title_is_title_case_of_name(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn("\n# Jest To Vitest Migration\n", text)

    def test_signals_joined_with_comma(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn(
            'Signals: jest.config.js present alongside a vitest dependency, '
            'user says "migrate to vitest"',
            text,
        )

    def test_steps_numbered_with_why(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn(
            "1. Run the existing jest suite to capture a baseline of passing tests "
            "— Establishes a pass/fail baseline before touching any config.",
            text,
        )

    def test_decision_point_line_format(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn(
            "- After step 1: if Did the baseline jest run reveal any already-failing tests? "
            "→ Record the pre-existing failures separately so the migration diff is not "
            "blamed for them; otherwise → Proceed directly to creating the vitest config",
            text,
        )

    def test_linear_candidate_gets_no_branches_line(self):
        candidate = copy.deepcopy(load_fixture("good.json"))
        candidate["decision_points"] = []
        candidate["linear"] = True
        text = render_skill_md(candidate)
        self.assertIn("Linear procedure — no branches observed.", text)

    def test_provenance_lists_evidence_ids_and_rubric_line(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn("Evidence session IDs: sess-001, sess-002, sess-003.", text)
        self.assertIn("Rubric: Q1 2 · Q2 2 · Q3 1 · Q4 2 · Q5 2 (total 9/10).", text)

    def test_feedback_line_has_report_usage_command(self):
        candidate = load_fixture("good.json")
        text = render_skill_md(candidate)
        self.assertIn(
            "python <extractor-path>/scripts/report_usage.py jest-to-vitest-migration "
            "--outcome good|neutral|poor",
            text,
        )


class TestRenderReviewMd(unittest.TestCase):
    def test_review_md_has_rubric_and_none_dedup_and_accept(self):
        candidate = load_fixture("good.json")
        text = render_review_md(candidate, DEFAULT_CFG)
        self.assertIn("# Review: jest-to-vitest-migration", text)
        self.assertIn("cs-20260917-jest-to-vitest", text)
        self.assertIn("| Q1 | 2 |", text)
        self.assertIn("| Total | 9/10 |", text)
        self.assertIn("- [x] recurrence", text)
        self.assertIn("sess-001", text)
        self.assertIn("migrated jest suite to vitest, all tests passing", text)
        self.assertIn("## Dedup findings\n\nnone", text)
        self.assertIn("## Recommended action\n\naccept", text)

    def test_dedup_findings_file_forces_review_action(self):
        candidate = load_fixture("good.json")
        with tempfile.TemporaryDirectory() as tmp:
            findings_path = Path(tmp) / "findings.json"
            findings_path.write_text(
                json.dumps({"findings": [
                    {"skill": "existing-skill-a", "relation": "overlap", "note": "shares steps 1-2"}
                ]}),
                encoding="utf-8",
            )
            text = render_review_md(candidate, DEFAULT_CFG, dedup_findings_path=str(findings_path))
        self.assertIn("existing-skill-a", text)
        self.assertIn("overlap", text)
        self.assertIn("## Recommended action\n\nreview dedup findings", text)


class TestRenderCandidateWritesFiles(unittest.TestCase):
    def test_writes_candidate_json_skill_md_review_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest_dir = render_candidate(str(CANDIDATES_DIR / "good.json"), tmp)
            dest_dir = Path(dest_dir)
            self.assertEqual(dest_dir.name, "cs-20260917-jest-to-vitest")
            self.assertTrue((dest_dir / "candidate.json").is_file())
            self.assertTrue((dest_dir / "SKILL.md").is_file())
            self.assertTrue((dest_dir / "REVIEW.md").is_file())

            copied = json.loads((dest_dir / "candidate.json").read_text(encoding="utf-8"))
            original = load_fixture("good.json")
            self.assertEqual(copied, original)


class TestRenderSkillCli(unittest.TestCase):
    def test_cli_writes_review_queue_folder(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable, str(RENDER_SKILL),
                    "--candidate", str(CANDIDATES_DIR / "good.json"),
                    "--out-dir", tmp,
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            dest_dir = Path(tmp) / "cs-20260917-jest-to-vitest"
            self.assertTrue((dest_dir / "SKILL.md").is_file())
            self.assertTrue((dest_dir / "REVIEW.md").is_file())
            self.assertTrue((dest_dir / "candidate.json").is_file())


if __name__ == "__main__":
    unittest.main()
