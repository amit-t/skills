# Changelog

Recent project updates, summarized from repository history.

## 2026-04-20

- Refreshed the `e2e-audit` skill — added persona screenshot demo phase, expanded diagnostic report format, and a fix_plan bug-list emitter that turns each defect into a ralph task with file paths, root-cause hypotheses, and exit criteria.

## 2026-04-16

- Added the `resume-tailoring` skill — tailor a resume to a specific job by researching company/role, branching interview for undocumented experience, confidence-scored content matching, and generating MD + DOCX + PDF + interview-prep report. Includes multi-job batch mode and a portable `.skill` bundle for Codex / co-work.

## 2026-04-08

- Added the `compact-conversation` skill — compact conversations into concise summaries to reduce context window usage.

## 2026-04-05

- Added the `e2e-audit` skill — run a Playwright end-to-end audit of a web app using its PRDs as the test spec.

## 2026-04-03

- Added the `precision-mode` skill — universal conciseness directive for all LLM output.
- Added the `package-scout` skill — research, compare, and select the best packages before installing any dependency.

## 2026-04-02

- Added the `concise-reporting` skill to the catalog under the `Agent Behavior` category.

## 2026-03-31

- Added the `prd-to-plan`, `qa`, and `request-refactor-plan` skills.

## 2026-03-29

- Flattened skill directories to simplify the repository layout.
- Added per-skill `README.md` files for installation and usage guidance.
- Removed the `character-distiller` skill from the catalog.
- Removed older workflow skills for architecture improvement, PRD breakdown, and QA sessions.

## 2026-03-28

- Added the `eng-spec` skill for TDD, engineering spec, and ADR generation with review.
- Added the `git-guardrails-claude-code`, `tdd`, `ubiquitous-language`, and `design-interview` skills.

For older changes, use `git log` in the repository root.
