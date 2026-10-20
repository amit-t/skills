#!/usr/bin/env python3
"""Check the three distill-project agent evaluations against fixture evidence."""
import argparse
import re
from pathlib import Path


def require(condition, reason, failures):
    if not condition:
        failures.append(reason)


def load_pair(folder):
    rules = folder / "CLAUDE.md"
    if not rules.exists():
        rules = folder / "AGENTS.md"
    context = folder / "docs/project-context.md"
    return rules, context


def check_one(folder, failures):
    rules, context = load_pair(folder)
    require(rules.is_file(), "missing root instructions", failures)
    require(context.is_file(), "missing docs/project-context.md", failures)
    if not rules.is_file() or not context.is_file():
        return
    r, c = rules.read_text(), context.read_text()
    require(re.search(r"no exclamation|avoid exclamation|do not use exclamation", r, re.I), "missing exclamation rule", failures)
    require("16 Sep 2026" in r, "missing owner date-format example", failures)
    for value in ("#14263D", "#F2E9D8", "#1F6E75", "Inter", "Source Serif 4"):
        require(value in c, f"missing exact template value {value}", failures)
    for value in ("Summary", "Evidence", "Next steps"):
        require(value in c, f"missing template section {value}", failures)
    require("720px" in c and "32px" in c, "missing exact layout sizes", failures)
    require("monthly ledger" in c, "missing source attribution", failures)
    require("animation" not in r.lower(), "invented animation rule", failures)


def check_two(folder, failures):
    rules, context = load_pair(folder)
    require(rules.is_file(), "missing root instructions", failures)
    require(context.is_file(), "missing docs/project-context.md", failures)
    if not rules.is_file() or not context.is_file():
        return
    r, c = rules.read_text(), context.read_text()
    require("option B" in r or re.search(r"title.{0,60}evidence.{0,60}decision.{0,60}sources", r, re.I | re.S), "option B is not a rule or default", failures)
    require("sentence case" in r.lower(), "correction missing from rules", failures)
    require("animat" not in r.lower(), "ignored suggestion promoted to a rule", failures)
    require(re.search(r"seen, not confirmed", c, re.I) and "animat" in c.lower(), "ignored suggestion not recorded as seen, not confirmed", failures)
    require(len(r) < 6000, f"instructions too long: {len(r)} characters", failures)


def check_three(folder, previous, failures):
    rules, context = load_pair(folder)
    require(rules.is_file(), "instructions deleted on update", failures)
    require(context.is_file(), "context deleted on update", failures)
    if not rules.is_file() or not context.is_file():
        return
    r, c = rules.read_text(), context.read_text()
    old_r, old_c = load_pair(previous)
    if old_r.is_file() and old_c.is_file():
        old_rules, old_context = old_r.read_text(), old_c.read_text()
        require(bool(re.search(r"(?:no|avoid|do not use) exclamation", r, re.I)) and "16 Sep 2026" in r, "old corrections lost on update", failures)
        require("September report" in c and "October report" in c, "past output index lost on update", failures)
        old_date = re.search(r"Updated:\s*(\d{4}-\d{2}-\d{2})", old_context)
        new_date = re.search(r"Updated:\s*(\d{4}-\d{2}-\d{2})", c)
        require(bool(old_date and new_date and old_date.group(1) != new_date.group(1)), "Updated date did not change", failures)
        require("monthly ledger" in c and "Source Serif 4" in c, "existing template evidence lost", failures)
        require(bool(old_rules.strip()), "old rules were empty", failures)
    require("Methods" in c, "new section absent", failures)
    require("rule-break.html" in c and re.search(r"known fixes", c, re.I), "rule-break page absent from known fixes", failures)
    template = c.split("## 5. Templates", 1)[-1].split("\n## 6.", 1)[0]
    require("2026/10/19" not in template and "Draft report!" not in template, "broken style copied into template", failures)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("case", choices=("1", "2", "3"))
    parser.add_argument("folder", type=Path)
    parser.add_argument("--previous", type=Path)
    args = parser.parse_args()
    failures = []
    if args.case == "1":
        check_one(args.folder, failures)
    elif args.case == "2":
        check_two(args.folder, failures)
    else:
        if args.previous is None:
            parser.error("--previous required for case 3")
        check_three(args.folder, args.previous, failures)
    if failures:
        print("\n".join(f"FAIL: {reason}" for reason in failures))
        raise SystemExit(1)
    print(f"Test {args.case}: PASS")


if __name__ == "__main__":
    main()
