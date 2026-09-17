#!/usr/bin/env python3
"""Stage 1 filter: gate, score, and rank normalized sessions for the extraction pipeline.

Deterministic, no LLM calls (spec C5 Stage 1). Consumes Task-2 Session.to_dict()-shaped
session dicts and admits each session under up to four categories from the source
article: length, complexity, outcome, novelty. Adapters may leave stats/outcome_signals
fields null, so every read below tolerates missing/null values.

priority_score = 1*length + 2*complexity + 2*outcome + 3*novelty (each flag is 0 or 1).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, read_json, write_json

_DEFAULT_FILTER_CFG = {
    "min_turns": 6,
    "min_tool_calls": 2,
    "min_assistant_turns_if_no_tools": 4,
    "max_sessions_per_run": 25,
}

# Structured output: fenced code blocks, or a markdown table separator row like "|---|".
_CODE_BLOCK_RE = re.compile(r"```")
_TABLE_SEP_RE = re.compile(r"\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)*\|?")

ADMITTED_BY_ORDER = ("length", "complexity", "outcome", "novelty")


def _filter_cfg(cfg):
    """Merge config['filter'] over the module defaults; tolerates a missing/partial cfg."""
    merged = dict(_DEFAULT_FILTER_CFG)
    merged.update((cfg or {}).get("filter") or {})
    return merged


def _has_structured_output(turns):
    """Triple-backtick fenced blocks or markdown table separator rows in assistant text."""
    for t in turns or []:
        t = t or {}
        if t.get("role") != "assistant":
            continue
        text = t.get("text") or ""
        if _CODE_BLOCK_RE.search(text) or _TABLE_SEP_RE.search(text):
            return True
    return False


def _has_novelty(turns, error_count):
    """error_count >= 1 and a tool_call after the LAST error tool_result uses a different
    tool name than the one that errored (error -> recovery)."""
    if not error_count:
        return False
    turns = turns or []

    last_error_idx = None
    last_error_name = None
    for i, t in enumerate(turns):
        for result in (t or {}).get("tool_results") or []:
            if result.get("ok") is False:
                last_error_idx = i
                last_error_name = result.get("name")
    if last_error_idx is None:
        return False

    for i, t in enumerate(turns):
        if i <= last_error_idx:
            continue
        for call in (t or {}).get("tool_calls") or []:
            name = call.get("name")
            if name and name != last_error_name:
                return True
    return False


def _rating_is_positive(rating):
    """explicit_user_rating 'truthy positive': positive numbers, or any other truthy value."""
    if isinstance(rating, bool):
        return rating
    if isinstance(rating, (int, float)):
        return rating > 0
    return bool(rating)


def _evaluate(session, fcfg):
    """Return (entry, None) if admitted, or (None, drop_reason) if dropped."""
    stats = session.get("stats") or {}
    turns = session.get("turns") or []
    outcome_signals = session.get("outcome_signals") or {}

    turn_count = stats.get("turn_count") or 0
    tool_call_count = stats.get("tool_call_count") or 0
    assistant_turns = stats.get("assistant_turns") or 0
    distinct_tools = stats.get("distinct_tools") or []
    error_count = stats.get("error_count") or 0

    tool_gate = tool_call_count >= fcfg["min_tool_calls"]
    assistant_gate = assistant_turns >= fcfg["min_assistant_turns_if_no_tools"]
    if not (turn_count >= fcfg["min_turns"] and (tool_gate or assistant_gate)):
        return None, "gate_not_met"

    structured_output = _has_structured_output(turns)
    task_completed_marker = bool(outcome_signals.get("task_completed_marker"))

    # Exclusion (a): only Q&A, no actions.
    if tool_call_count == 0 and not task_completed_marker:
        if not (assistant_gate and structured_output):
            return None, "qa_only_no_actions"

    novelty = _has_novelty(turns, error_count)

    # Exclusion (b): single-tool domination, no adaptation.
    if len(distinct_tools) == 1 and tool_call_count >= 10 and not novelty:
        return None, "single-tool repetition"

    complexity = bool(tool_call_count > 0 or len(distinct_tools) >= 3 or structured_output)
    outcome = bool(
        outcome_signals.get("user_positive_ack")
        or task_completed_marker
        or _rating_is_positive(outcome_signals.get("explicit_user_rating"))
    )

    flags = {"length": True, "complexity": complexity, "outcome": outcome, "novelty": novelty}
    admitted_by = [name for name in ADMITTED_BY_ORDER if flags[name]]
    priority_score = (
        1 * flags["length"] + 2 * flags["complexity"] + 2 * flags["outcome"] + 3 * flags["novelty"]
    )

    entry = {
        "session_id": session.get("session_id"),
        "host": session.get("host"),
        "source_path": session.get("source_path"),
        "priority_score": priority_score,
        "admitted_by": admitted_by,
        "stats": stats,
        "excluded": False,
    }
    return entry, None


def filter_sessions(sessions, cfg):
    """Gate, score, and rank sessions.

    Returns (filtered, dropped):
      filtered: admitted entries, ranked desc by priority_score (ties stable),
                truncated to filter.max_sessions_per_run.
      dropped:  [{"session_id", "reason"}, ...] audit trail for the REVIEW stage,
                including sessions cut solely by the max_sessions_per_run cap.
    """
    fcfg = _filter_cfg(cfg)

    admitted = []
    dropped = []
    for session in sessions or []:
        session = session or {}
        entry, drop_reason = _evaluate(session, fcfg)
        if entry is None:
            dropped.append({"session_id": session.get("session_id"), "reason": drop_reason})
        else:
            admitted.append(entry)

    admitted.sort(key=lambda e: e["priority_score"], reverse=True)

    max_sessions = fcfg.get("max_sessions_per_run")
    if isinstance(max_sessions, int) and len(admitted) > max_sessions:
        overflow = admitted[max_sessions:]
        admitted = admitted[:max_sessions]
        for entry in overflow:
            dropped.append({"session_id": entry["session_id"], "reason": "exceeds max_sessions_per_run"})

    return admitted, dropped


def _load_sessions(path):
    """--in accepts a {"sessions": [...]} wrapper or a bare list (Ruling 3)."""
    data = read_json(path)
    if isinstance(data, dict):
        return data.get("sessions") or []
    return data or []


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description=(
            "Stage 1 filter: gate sessions (min_turns, min_tool_calls / "
            "min_assistant_turns_if_no_tools), then rank the admitted ones by "
            "priority_score = 1*length + 2*complexity + 2*outcome + 3*novelty "
            "(each flag is 0 or 1), truncated to max_sessions_per_run."
        )
    )
    parser.add_argument("--in", dest="in_path", required=True,
                         help="input sessions JSON: {'sessions': [...]} or a bare list")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    parser.add_argument("--out", required=True, help="output filtered_sessions.json path")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    try:
        sessions = _load_sessions(args.in_path)
    except (OSError, ValueError) as exc:
        print(json.dumps({"ok": False, "errors": ["malformed or missing --in file: %s" % exc]}), file=sys.stderr)
        return 1
    cfg = load_config(args.config)
    filtered, dropped = filter_sessions(sessions, cfg)
    write_json(args.out, {"filtered": filtered, "dropped": dropped})
    return 0


if __name__ == "__main__":
    sys.exit(main())
