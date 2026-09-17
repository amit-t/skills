#!/usr/bin/env python3
"""Feedback loop, part 2 (spec E3-9): retire/promote/revise proposals for every
registered skill, derived from usage-log outcomes, plus a full-library
trigger-conflict scan and a library-size warning.

Read-only by contract: NEVER mutates registry.json and NEVER deletes anything.
Writes a proposals-only markdown report (templates/retirement-report.md.tmpl,
plain string.Template, no logic) and prints a JSON summary to stdout.
"""
import argparse
import datetime
import json
import string
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, read_json
from dedup_prescreen import tokenize

_TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "templates" / "retirement-report.md.tmpl"

_CONFLICT_THRESHOLD = 0.5
_REVISE_POOR_RATIO = 0.5


def _jaccard(a, b):
    """|a & b| / |a | b|; 0.0 if either set is empty."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _parse_at(at_str):
    """Parse an ISO-8601 'at' timestamp; returns None (never raises) on any
    unparseable value -- part of the 'tolerate bad lines' contract."""
    try:
        dt = datetime.datetime.fromisoformat(at_str)
    except (TypeError, ValueError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=datetime.timezone.utc)
    return dt


def load_usage_rows(feedback_dir):
    """Read F/usage-log.jsonl. Malformed lines -- invalid JSON, a non-object, or
    missing skill/outcome/at -- are skipped silently, never fatal. A missing
    file yields []."""
    path = Path(feedback_dir) / "usage-log.jsonl"
    if not path.is_file():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except ValueError:
            continue
        if not isinstance(row, dict):
            continue
        if "skill" not in row or "outcome" not in row or "at" not in row:
            continue
        rows.append(row)
    return rows


def compute_skill_stats(skill_name, rows, now, window_days):
    """usage_count + good/neutral/poor counts for skill_name's rows whose `at`
    falls within the trailing window_days ending at `now`. Rows with an
    unparseable `at` are excluded (tolerated, not fatal)."""
    cutoff = now - datetime.timedelta(days=window_days)
    counts = {"good": 0, "neutral": 0, "poor": 0}
    usage_count = 0
    for row in rows:
        if row.get("skill") != skill_name:
            continue
        at = _parse_at(row.get("at"))
        if at is None or at < cutoff:
            continue
        usage_count += 1
        outcome = row.get("outcome")
        if outcome in counts:
            counts[outcome] += 1
    return usage_count, counts


def propose_action(status, usage_count, counts, cfg):
    """Precedence promote_to_validated > revise > retire > keep. Mutually
    exclusive by construction: revise/keep require usage_count > 0, retire
    requires usage_count == 0.

    - promote_to_validated: status != validated AND good >= validated_min_good_reports AND poor == 0
    - revise: usage_count > 0 AND poor / usage_count >= 0.5
    - retire: usage_count == 0
    - keep: otherwise
    """
    validated_min_good = ((cfg or {}).get("feedback") or {}).get("validated_min_good_reports", 5)
    good = counts.get("good", 0)
    poor = counts.get("poor", 0)

    if status != "validated" and good >= validated_min_good and poor == 0:
        return "promote_to_validated"
    if usage_count > 0 and (poor / usage_count) >= _REVISE_POOR_RATIO:
        return "revise"
    if usage_count == 0:
        return "retire"
    return "keep"


def find_conflicts(skills, threshold=_CONFLICT_THRESHOLD):
    """Pairwise Jaccard over trigger_description tokens (dedup_prescreen's
    tokenizer); pairs are [a, b] with a < b, sorted for determinism."""
    names = sorted(skills or {})
    tokens_by_name = {
        name: tokenize((skills[name] or {}).get("trigger_description") or "") for name in names
    }
    conflicts = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if _jaccard(tokens_by_name[a], tokens_by_name[b]) >= threshold:
                conflicts.append([a, b])
    return conflicts


def _proposals_table(rows):
    if not rows:
        return "- none"
    lines = ["| Skill | Status | Good | Neutral | Poor | Proposal |", "|---|---|---|---|---|---|"]
    for name, status, counts, action in rows:
        lines.append(
            "| %s | %s | %d | %d | %d | %s |"
            % (name, status, counts["good"], counts["neutral"], counts["poor"], action)
        )
    return "\n".join(lines)


def _conflicts_block(conflicts):
    if not conflicts:
        return "- none"
    return "\n".join("- %s <-> %s" % (a, b) for a, b in conflicts)


def _library_size_block(count, threshold, warning):
    if warning:
        return (
            "Warning: library size is %d registered skills, exceeding the configured "
            "threshold of %d. Consider retiring or merging underused skills before "
            "promoting new ones." % (count, threshold)
        )
    return "Library size is %d registered skills, within the configured threshold of %d." % (
        count, threshold,
    )


def build_report(registry, rows, window_days, cfg, today_str):
    """Compute proposals + conflicts + library-size warning and render the
    markdown report text plus the stdout JSON summary. Pure function -- never
    touches disk."""
    skills = (registry or {}).get("skills") or {}
    now = datetime.datetime.now(datetime.timezone.utc)

    proposals = {}
    table_rows = []
    for name in sorted(skills):
        entry = skills[name] or {}
        usage_count, counts = compute_skill_stats(name, rows, now, window_days)
        action = propose_action(entry.get("status"), usage_count, counts, cfg)
        proposals[name] = action
        table_rows.append((name, entry.get("status"), counts, action))

    conflicts = find_conflicts(skills)

    library_size_warning_threshold = (cfg or {}).get("library_size_warning", 20)
    warning = len(skills) > library_size_warning_threshold

    template = string.Template(_TEMPLATE_PATH.read_text(encoding="utf-8"))
    report_text = template.substitute({
        "date": today_str,
        "window_days": window_days,
        "skill_count": len(skills),
        "proposals_table": _proposals_table(table_rows),
        "conflicts_block": _conflicts_block(conflicts),
        "library_size_block": _library_size_block(
            len(skills), library_size_warning_threshold, warning
        ),
    })
    summary = {"proposals": proposals, "conflicts": conflicts, "warning": warning}
    return report_text, summary


def run_retire_review(registry_path, feedback_dir, window_days, out_dir, cfg):
    """Load registry + usage log, build the report, write it to
    <out_dir>/retirement-<YYYY-MM-DD>.md. Never writes to registry_path or
    feedback_dir. Returns (report_path, summary)."""
    registry = read_json(registry_path) if Path(registry_path).is_file() else {"skills": {}}
    rows = load_usage_rows(feedback_dir)
    if window_days is None:
        window_days = ((cfg or {}).get("feedback") or {}).get("review_window_days", 90)

    today_str = datetime.datetime.now(datetime.timezone.utc).date().isoformat()
    report_text, summary = build_report(registry, rows, window_days, cfg, today_str)

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    report_path = out_dir / ("retirement-%s.md" % today_str)
    report_path.write_text(report_text, encoding="utf-8")

    return report_path, summary


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Propose promote/revise/retire actions from usage feedback and scan for "
            "trigger conflicts. Read-only: never mutates the registry or deletes anything."
        )
    )
    parser.add_argument("--registry", required=True, help="path to registry.json")
    parser.add_argument(
        "--feedback-dir", required=True, help="feedback directory containing usage-log.jsonl"
    )
    parser.add_argument(
        "--window-days", type=int, default=None,
        help="defaults to config feedback.review_window_days",
    )
    parser.add_argument(
        "--out", default="./review-queue", help="directory to write the retirement report into"
    )
    parser.add_argument("--config", default=None, help="path to a user config.json")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    cfg = load_config(args.config)
    _report_path, summary = run_retire_review(
        args.registry, args.feedback_dir, args.window_days, args.out, cfg,
    )
    print(json.dumps(summary))
    return 0


if __name__ == "__main__":
    sys.exit(main())
