# Changelog

Recent project updates, summarized from repository history.

## 2026-05-12

- Added the `gh-repo-mirror` skill under `Engineering` — scaffolds a new GitHub repo that mirrors a reference repo's general settings, security-and-analysis flags, and classic `main` branch protection, with an optional neo-brutalist GitHub Pages docs site under `docs/` (or `/`), custom domain via `docs/CNAME`, async HTTPS cert polling, and opt-ins for ruleset mirroring (`--mirror-rulesets`), Cloudflare DNS record creation (`--cname-provider cloudflare`), and a bootstrap starter skill (`--bootstrap-skill <slug>`).

## 2026-05-08

- Added the `leadership-update` skill under a new `Leadership` category — reformats raw notes into an outcome-first, three-sentence update (status / reasoning / next) ending with a clear ask. Auto-detects whether to reformat directly or run a 1–3 question interview. Verbal/standup script by default; offers Slack, email, and status-doc formats. Based on Yasar Ahmad's leadership-update framework.
- Added the `repo-context-scan` skill — autonomous codebase scan that writes `CONTEXT.md` (or `CONTEXT-MAP.md` for multi-context repos) and seeds `docs/adr/` entries for clearly-deliberate decisions. Asks only when ambiguity blocks resolution; idempotent re-runs preserve user-authored prose.
- Added the `domain-grill` skill — engineering-only relentless interview that stress-tests eng specs, TDD plans, refactor proposals, technical designs, schema migrations, and API contracts against `CONTEXT.md` and existing ADRs. Refuses PRDs and non-technical artifacts and redirects to `/grill-me`. Reads `CONTEXT.md` read-only; flags newly-surfaced terms and recommends re-running `/repo-context-scan` to incorporate them.
- Deprecated the `ubiquitous-language` skill — split into `/repo-context-scan` (build) and `/domain-grill` (stress-test) so the *write* and *read* responsibilities are owned by separate skills with different cadences. The old skill is kept in the catalog as a redirect; the prior `SKILL.md` is preserved in git history.

## 2026-04-29

- Added the `gh-pages-neo-brutalist` skill — drop-in Jekyll templates that scaffold a GitHub Pages site with a neo-brutalist design system (IBM Plex Mono, 3px borders, solid offset shadows, eight saturated accents, four themes: light / dark / cyberpunk grid / solarized IDE). Includes `scaffold.zsh` for one-shot stamping, `site.css` and `site.js` for design tokens and the theme switcher, and a GitHub Actions Pages workflow.

## 2026-04-25

- Added the `docs-from-prs` skill — surveys merged PRs, fills doc gaps in README + landing page + user guide with section-placement awareness, re-audits alias tables every run, and finishes with a grammar/casing/alignment copy-edit pass.
- Generalized `docs-from-prs` so it is project-agnostic — replaced ai-ralph-specific paths, remote workflow, and alias tables with a generic drift-hot-spot audit, repo-resolved `gh` survey, and layout-aware section placement (single-file / README+site / README+guide / full).

## 2026-04-20

- Refreshed the `e2e-audit` skill — added persona screenshot demo phase, expanded diagnostic report format, and a fix_plan bug-list emitter that turns each defect into a ralph task with file paths, root-cause hypotheses, and exit criteria.
- Added the `skill-sync` skill under `Agent Behavior` — wraps the `skill-sync` zsh utility in `ai-utils/skill-sync/` to sync existing skills from a source path or scaffold new ones via `claude` / `codex` / `devin`.

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
