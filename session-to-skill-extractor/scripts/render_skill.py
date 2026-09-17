#!/usr/bin/env python3
"""Stage 6 renderer (spec D3): a D2 CandidateSkill JSON -> review-queue folder
containing a copy of the candidate, the rendered SKILL.md, and a REVIEW.md for
the human reviewer.

Templates (templates/*.tmpl) are plain `string.Template` files with no logic:
every composite string -- joined signal lists, numbered steps, decision-point
lines, bullet lists, evidence ids, the rubric line -- is built here in Python
and substituted into the template as a single value.
"""
import argparse
import json
import shutil
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, read_json

_TEMPLATES_DIR = Path(__file__).resolve().parent.parent / "templates"
_SKILL_TEMPLATE_PATH = _TEMPLATES_DIR / "extracted-skill.SKILL.md.tmpl"
_REVIEW_TEMPLATE_PATH = _TEMPLATES_DIR / "REVIEW.md.tmpl"

EXTRACTOR_VERSION = "1.0"

_QUALITY_CRITERIA_ORDER = (
    "recurrence", "non_obvious", "replicable", "measurable_quality", "clearly_articulable",
)


def title_case_name(name):
    """kebab-case skill name -> Title Case with hyphens rendered as spaces."""
    return (name or "").replace("-", " ").title()


def _bullets(items):
    """Bullet-list block, one '- item' per line; 'none' placeholder if empty."""
    items = [i for i in (items or []) if i]
    if not items:
        return "- none"
    return "\n".join("- %s" % item for item in items)


def _numbered_steps(steps):
    """'1. Action — why' when why is present, else '1. Action'; one per line."""
    lines = []
    for step in steps or []:
        step = step or {}
        n = step.get("n")
        action = step.get("action", "")
        why = step.get("why")
        if why:
            lines.append("%s. %s — %s" % (n, action, why))
        else:
            lines.append("%s. %s" % (n, action))
    return "\n".join(lines)


def _decision_points_block(candidate):
    """Decision-point lines, or the linear-procedure note when there are none."""
    decision_points = candidate.get("decision_points") or []
    if not decision_points:
        return "Linear procedure — no branches observed."
    lines = []
    for dp in decision_points:
        dp = dp or {}
        lines.append(
            "- After step %s: if %s → %s; otherwise → %s"
            % (dp.get("after_step"), dp.get("condition"), dp.get("if_true"), dp.get("if_false"))
        )
    return "\n".join(lines)


def _rubric_line(rubric):
    rubric = rubric or {}
    return "Q1 %s · Q2 %s · Q3 %s · Q4 %s · Q5 %s (total %s/10)." % (
        rubric.get("q1"), rubric.get("q2"), rubric.get("q3"),
        rubric.get("q4"), rubric.get("q5"), rubric.get("total"),
    )


def _yaml_bool(value):
    return "true" if value else "false"


def render_skill_md(candidate, extractor_version=EXTRACTOR_VERSION):
    """Build the rendered SKILL.md text (spec D3) for a D2 candidate dict."""
    candidate = candidate or {}
    template = string.Template(_SKILL_TEMPLATE_PATH.read_text(encoding="utf-8"))

    trigger = candidate.get("trigger") or {}
    evidence = candidate.get("evidence") or {}
    provenance = candidate.get("provenance") or {}
    rubric = candidate.get("rubric") or {}
    sessions = evidence.get("sessions") or []

    mapping = {
        "name": candidate.get("name", ""),
        "description": candidate.get("description", ""),
        "status": candidate.get("status", "candidate"),
        "version": candidate.get("version", "1.0"),
        "task_type": candidate.get("task_type", ""),
        "extracted_by": "session-to-skill-extractor/%s" % extractor_version,
        "extracted_from_host": provenance.get("extracted_by_host", ""),
        "supporting_sessions": evidence.get("supporting_sessions", 0),
        "extracted_at": provenance.get("extracted_at", ""),
        "requires_human_review": _yaml_bool(candidate.get("requires_human_review", True)),
        "title": title_case_name(candidate.get("name", "")),
        "trigger_description": trigger.get("description", ""),
        "signals_line": ", ".join(trigger.get("signals") or []),
        "prerequisites_block": _bullets(candidate.get("prerequisites")),
        "steps_block": _numbered_steps(candidate.get("steps")),
        "decision_points_block": _decision_points_block(candidate),
        "expected_output": candidate.get("expected_output", ""),
        "edge_cases_block": _bullets(candidate.get("edge_cases")),
        "evidence_ids": ", ".join(s.get("session_id", "") for s in sessions),
        "rubric_line": _rubric_line(rubric),
    }
    return template.substitute(mapping)


def _quality_criteria_block(quality_criteria):
    quality_criteria = quality_criteria or {}
    lines = []
    for key in _QUALITY_CRITERIA_ORDER:
        mark = "x" if quality_criteria.get(key) else " "
        lines.append("- [%s] %s" % (mark, key))
    return "\n".join(lines)


def _evidence_block(sessions):
    sessions = sessions or []
    if not sessions:
        return "- none"
    lines = []
    for s in sessions:
        s = s or {}
        lines.append(
            '- %s (%s): "%s" — %s'
            % (s.get("session_id", ""), s.get("host", ""), s.get("excerpt", ""), s.get("source_path", ""))
        )
    return "\n".join(lines)


def _load_extra_dedup_findings(path):
    """Load findings from an optional --dedup-findings file: a bare list, or a
    dict with a 'findings' key (wrapper-or-bare-list, matching Ruling 3)."""
    if not path:
        return []
    data = read_json(path)
    if isinstance(data, list):
        return data
    return (data or {}).get("findings") or []


def _dedup_findings_block(findings):
    if not findings:
        return "none"
    lines = []
    for f in findings:
        f = f or {}
        lines.append("- %s: %s — %s" % (f.get("skill", ""), f.get("relation", ""), f.get("note", "")))
    return "\n".join(lines)


def _recommended_action(findings, rubric, cfg):
    flag_min_total = ((cfg or {}).get("identify") or {}).get("flag_min_total", 7)
    total = (rubric or {}).get("total", 0)
    if not findings and total >= flag_min_total:
        return "accept"
    return "review dedup findings"


def render_review_md(candidate, cfg, dedup_findings_path=None):
    """Build the REVIEW.md text (rubric table, quality checklist, evidence,
    dedup findings, recommended action, status-ladder note) for a reviewer."""
    candidate = candidate or {}
    template = string.Template(_REVIEW_TEMPLATE_PATH.read_text(encoding="utf-8"))

    evidence = candidate.get("evidence") or {}
    rubric = candidate.get("rubric") or {}

    own_findings = (candidate.get("dedup") or {}).get("findings") or []
    extra_findings = _load_extra_dedup_findings(dedup_findings_path)
    all_findings = list(own_findings) + list(extra_findings)

    mapping = {
        "name": candidate.get("name", ""),
        "candidate_id": candidate.get("candidate_id", ""),
        "task_type": candidate.get("task_type", ""),
        "q1": rubric.get("q1"),
        "q2": rubric.get("q2"),
        "q3": rubric.get("q3"),
        "q4": rubric.get("q4"),
        "q5": rubric.get("q5"),
        "total": rubric.get("total"),
        "quality_criteria_block": _quality_criteria_block(candidate.get("quality_criteria")),
        "evidence_block": _evidence_block(evidence.get("sessions")),
        "dedup_findings_block": _dedup_findings_block(all_findings),
        "recommended_action": _recommended_action(all_findings, rubric, cfg),
    }
    return template.substitute(mapping)


def render_candidate(candidate_path, out_dir, dedup_findings_path=None, config_path=None):
    """Render one candidate into <out_dir>/<candidate_id>/{candidate.json,SKILL.md,REVIEW.md}.

    Returns the destination directory path.
    """
    candidate = read_json(candidate_path)
    cfg = load_config(config_path)

    candidate_id = candidate.get("candidate_id")
    dest_dir = Path(out_dir) / candidate_id
    dest_dir.mkdir(parents=True, exist_ok=True)

    shutil.copyfile(candidate_path, dest_dir / "candidate.json")
    (dest_dir / "SKILL.md").write_text(render_skill_md(candidate), encoding="utf-8")
    (dest_dir / "REVIEW.md").write_text(
        render_review_md(candidate, cfg, dedup_findings_path), encoding="utf-8"
    )
    return dest_dir


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Render a D2 candidate JSON into a review-queue SKILL.md + REVIEW.md."
    )
    parser.add_argument("--candidate", required=True, help="path to a candidate JSON file")
    parser.add_argument("--out-dir", required=True, help="review-queue directory to render into")
    parser.add_argument("--dedup-findings", default=None, help="optional dedup findings JSON file")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        dest_dir = render_candidate(args.candidate, args.out_dir, args.dedup_findings, args.config)
    except (OSError, KeyError, ValueError) as exc:
        print("render_skill: %s" % exc, file=sys.stderr)
        return 1
    print(json.dumps({"ok": True, "dir": str(dest_dir)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
