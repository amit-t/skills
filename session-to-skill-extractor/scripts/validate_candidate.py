#!/usr/bin/env python3
"""Stage 3 hard-rule validator for a D2 candidate JSON (spec C5 Stage 3).

Deterministic, no LLM calls. Checks schema-lite shape, step/action quality,
blacklist-free prose, a checkable expected_output, trigger completeness,
decision_points/linear consistency, edge_cases coverage, rubric arithmetic +
flag rule, and the single-session human-review gate.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, read_json

_DEFAULT_ANTI_PATTERNS_PATH = Path(__file__).resolve().parent.parent / "references" / "anti-patterns.md"
_BLACKLIST_LINE_RE = re.compile(r'^- "(.+)"$')

_REQUIRED_KEYS = (
    "candidate_id", "name", "description", "task_type", "trigger", "steps",
    "expected_output", "rubric", "evidence", "provenance", "status",
    "requires_human_review", "version",
)
_NAME_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
_STEP_ACTION_RE = re.compile(r"^[A-Z][a-z]+ ")
_CHECKABLE_RE = re.compile(
    r"file|json|table|report|exit|commit|PR|list|folder|diff|log|output at",
    re.IGNORECASE,
)


def _anti_patterns_path(cfg):
    """Default anti-patterns.md path, overridable via config key 'anti_patterns_path'."""
    override = (cfg or {}).get("anti_patterns_path")
    return Path(override) if override else _DEFAULT_ANTI_PATTERNS_PATH


def load_blacklist(path):
    """Parse vague-phrase blacklist lines (`- "phrase"`) from anti-patterns.md."""
    phrases = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            m = _BLACKLIST_LINE_RE.match(line.strip())
            if m:
                phrases.append(m.group(1))
    return phrases


def _find_blacklisted(text, blacklist):
    """First blacklist phrase found as a case-insensitive substring of text, or None."""
    lowered = (text or "").lower()
    for phrase in blacklist or []:
        if phrase.lower() in lowered:
            return phrase
    return None


def _check_schema_lite(candidate, errors):
    """Check 1: required D2 keys present, name pattern, description length."""
    for key in _REQUIRED_KEYS:
        if key not in candidate:
            errors.append("missing required key: %s" % key)

    name = candidate.get("name")
    if isinstance(name, str) and not _NAME_RE.match(name):
        errors.append("name does not match pattern ^[a-z0-9][a-z0-9-]{0,63}$: %r" % name)

    description = candidate.get("description")
    if isinstance(description, str) and len(description) > 1024:
        errors.append("description exceeds 1024 chars")


def _check_steps(candidate, blacklist, errors):
    """Check 2: >=3 steps; each action >=15 chars, capitalized-verb-ish start, blacklist-free."""
    steps = candidate.get("steps") or []
    if len(steps) < 3:
        errors.append("steps: need at least 3, got %d" % len(steps))

    for step in steps:
        step = step or {}
        n = step.get("n")
        action = step.get("action") or ""

        if len(action) < 15:
            errors.append("step %s action too short (<15 chars): %r" % (n, action))
        if not _STEP_ACTION_RE.match(action):
            errors.append(
                "step %s action must start with a capitalized verb-ish token (^[A-Z][a-z]+ ): %r"
                % (n, action)
            )
        phrase = _find_blacklisted(action, blacklist)
        if phrase:
            errors.append("step %s action contains blacklisted phrase: %r" % (n, phrase))


def _check_prose_blacklist_and_checkable(candidate, blacklist, errors):
    """Check 3: description/expected_output/trigger.description blacklist-free;
    expected_output must name a checkable artifact."""
    description = candidate.get("description") or ""
    phrase = _find_blacklisted(description, blacklist)
    if phrase:
        errors.append("description contains blacklisted phrase: %r" % phrase)

    expected_output = candidate.get("expected_output") or ""
    phrase = _find_blacklisted(expected_output, blacklist)
    if phrase:
        errors.append("expected_output contains blacklisted phrase: %r" % phrase)
    if not _CHECKABLE_RE.search(expected_output):
        errors.append("expected_output not checkable")

    trigger_description = (candidate.get("trigger") or {}).get("description") or ""
    phrase = _find_blacklisted(trigger_description, blacklist)
    if phrase:
        errors.append("trigger.description contains blacklisted phrase: %r" % phrase)


def _check_trigger(candidate, errors):
    """Check 4: trigger.description non-empty AND trigger.signals >= 1."""
    trigger = candidate.get("trigger") or {}
    description = trigger.get("description") or ""
    signals = trigger.get("signals") or []
    if not description.strip():
        errors.append("trigger.description must be non-empty")
    if len(signals) < 1:
        errors.append("trigger.signals must have at least 1 signal")


def _check_decision_points(candidate, errors):
    """Check 5: decision_points empty => linear must be true."""
    decision_points = candidate.get("decision_points") or []
    if not decision_points and candidate.get("linear") is not True:
        errors.append("decision_points is empty but linear is not true")


def _check_edge_cases(candidate, errors):
    """Check 6: edge_cases >= 1 non-empty entry (a 'none observed in N sessions' string counts)."""
    edge_cases = candidate.get("edge_cases") or []
    non_empty = [e for e in edge_cases if isinstance(e, str) and e.strip()]
    if len(non_empty) < 1:
        errors.append("edge_cases must have at least 1 non-empty entry")


def _check_rubric(candidate, cfg, errors):
    """Check 7: rubric total == sum(q1..q5); flag rule holds (an unflaggable candidate must
    not reach articulation)."""
    rubric = candidate.get("rubric") or {}
    try:
        q = [rubric["q1"], rubric["q2"], rubric["q3"], rubric["q4"], rubric["q5"]]
        total = rubric["total"]
    except KeyError:
        errors.append("rubric missing one or more of q1, q2, q3, q4, q5, total")
        return

    if total != sum(q):
        errors.append("rubric total mismatch: total=%s, sum(q1..q5)=%s" % (total, sum(q)))

    identify_cfg = (cfg or {}).get("identify") or {}
    min_at_2 = identify_cfg.get("flag_min_questions_at_2", 3)
    flag_min_total = identify_cfg.get("flag_min_total", 7)
    q2_min = identify_cfg.get("q2_min", 1)

    count_twos = sum(1 for v in q if v == 2)
    flagged = count_twos >= min_at_2 and total >= flag_min_total and q[1] >= q2_min
    if not flagged:
        errors.append(
            "rubric does not meet the flag rule (>=%d questions scoring 2, total>=%d, q2>=%d): "
            "an unflaggable candidate must not reach articulation" % (min_at_2, flag_min_total, q2_min)
        )


def _check_single_session_review(candidate, errors):
    """Check 8: evidence.supporting_sessions == 1 => requires_human_review must be true."""
    evidence = candidate.get("evidence") or {}
    supporting_sessions = evidence.get("supporting_sessions")
    if supporting_sessions == 1 and candidate.get("requires_human_review") is not True:
        errors.append(
            "single-session candidate (evidence.supporting_sessions == 1) "
            "must have requires_human_review=true"
        )


def validate(candidate, blacklist, cfg):
    """Run all Stage-3 hard-rule checks against a D2 candidate dict.

    Returns a list of error strings; an empty list means the candidate is valid.
    Never raises on missing/malformed fields -- each check tolerates absence and
    reports it as an error instead.
    """
    candidate = candidate or {}
    errors = []
    _check_schema_lite(candidate, errors)
    _check_steps(candidate, blacklist, errors)
    _check_prose_blacklist_and_checkable(candidate, blacklist, errors)
    _check_trigger(candidate, errors)
    _check_decision_points(candidate, errors)
    _check_edge_cases(candidate, errors)
    _check_rubric(candidate, cfg, errors)
    _check_single_session_review(candidate, errors)
    return errors


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Validate a D2 candidate JSON against Stage 3 hard rules (spec C5)."
    )
    parser.add_argument("--candidate", required=True, help="path to a candidate JSON file")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    candidate = read_json(args.candidate)
    cfg = load_config(args.config)
    blacklist = load_blacklist(_anti_patterns_path(cfg))
    errors = validate(candidate, blacklist, cfg)
    if errors:
        print(json.dumps({"ok": False, "errors": errors}))
        return 1
    print(json.dumps({"ok": True}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
