#!/usr/bin/env python3
"""Feedback loop, part 1 (spec E3-9): record a single usage-outcome report for
a promoted skill. Appends one JSON line to F/usage-log.jsonl; retire_review.py
(Task 10, same directory) reads this log back to propose promote/revise/retire.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, now_iso

_OUTCOMES = ("good", "neutral", "poor")


def append_usage(skill, outcome, note, feedback_dir):
    """Append {"skill","outcome","note","at"} to F/usage-log.jsonl, creating the
    directory and file as needed. `note` defaults to "" when absent. Returns the
    written row."""
    feedback_dir = Path(feedback_dir)
    feedback_dir.mkdir(parents=True, exist_ok=True)
    row = {"skill": skill, "outcome": outcome, "note": note or "", "at": now_iso()}
    with open(feedback_dir / "usage-log.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps(row) + "\n")
    return row


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Record a usage-outcome report for a promoted skill."
    )
    parser.add_argument("skill", help="skill name")
    parser.add_argument("--outcome", required=True, choices=_OUTCOMES)
    parser.add_argument("--note", default=None)
    parser.add_argument("--feedback-dir", default=None, help="defaults to config feedback_dir")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    cfg = load_config(args.config)
    feedback_dir = args.feedback_dir or cfg.get("feedback_dir", "./feedback")
    row = append_usage(args.skill, args.outcome, args.note, feedback_dir)
    print(json.dumps(row))
    return 0


if __name__ == "__main__":
    sys.exit(main())
