# Grill Summary Implementation Plan

> **For agentic workers:** Use independent subagents for behavioral testing and review;
> the primary agent owns the skill and shared catalog edits.

**Goal:** Deliver the approved standalone, concise, story-shaped grill summary skill.

**Architecture:** Markdown instructions with a conditional Wayfinder reference. No
runtime scripts or changes to existing grilling skills. Repository checks and test
fixtures live outside the installed skill.

**Tech Stack:** Markdown, JSON catalogs, zsh structural tests, agent behavioral tests.

## Tasks

- [x] Inspect repository conventions, clean baseline, and current grilling contract.
- [x] Obtain approval for standalone automatic/manual behavior and read-only scope.
- [x] Run baseline summaries without the skill; record missing question traceability.
- [x] Add `tests/grill-summary.test.zsh`; run before implementation and confirm missing
  package failure. Add reusable behavioral inputs under `tests/grill-summary/`.
- [x] Write `grill-summary/SKILL.md`, conditional `WAYFINDER.md`, and install/usage README.
- [x] Register the skill in root README and `skills.json`; add matching dated entries
  to `CHANGELOG.md` and `changelog.json`. Keep Engineering rows alphabetized.
- [x] Run independent behavioral tests and review; correct demonstrated gaps.
- [x] Run `zsh -n tests/grill-summary.test.zsh`, `zsh tests/grill-summary.test.zsh`,
  skill-creator's `quick_validate.py grill-summary`, and `git diff --check`.
- [x] Run `graphify update .` because the test script is new code; inspect scope of
  generated changes. Record any tool limitation without overstating verification.
- [x] Record actual behavioral outcomes and audit requirements.
- [ ] Commit only scoped files and push the short-lived feature branch. Do not merge
  or deploy without permission.
