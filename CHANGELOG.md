# Changelog

Recent project updates, summarized from repository history.

## 2026-05-30

- Added the `grill-me-auto` skill — batch-mode `/grill-me` fork that writes every question, option, recommendation, alt recommendation, and one-shot answer shortcut into a collapsible markdown grill document under `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`.

## 2026-05-29

- Added upstream attribution to `grill-me`. The skill is a fork of [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) by [Matt Pocock](https://github.com/mattpocock) (`mattpocock/skills`); this fork adds the `quick` / `standard` / `deep` depth selector while the relentless-interview core is Matt's original idea. Credit now appears where anyone downloading or installing the skill will see it: a **Credits** section in `grill-me/README.md` (above License) and a footer attribution line in `grill-me/SKILL.md` so the credit travels with the installed copy. No behavior change.

## 2026-05-21

- `gh-repo-mirror` now mirrors **repository access by default** — every team that has access to the reference repo is added to the new repo at the same permission level (pull / triage / push / maintain / admin), and direct collaborators are invited at the same permission. Driven by two read APIs (`GET repos/<ref>/teams` and `GET repos/<ref>/collaborators?affiliation=direct`) and two write APIs (`PUT /orgs/{org}/teams/{slug}/repos/{owner}/{repo}` and `PUT /repos/{owner}/{repo}/collaborators/{login}`). The collaborator PUT expects the *API* permission vocabulary (`pull` / `triage` / `push` / `maintain` / `admin`) but GET returns the *display* vocabulary (`read` / `triage` / `write` / `maintain` / `admin`); a `role_to_permission` helper translates `read → pull` and `write → push`, leaving the others alone. Skip with the new `--no-mirror-access` flag. Cross-org caveat: team slugs are scoped to the target org, so teams from a different reference org will 404 on the PUT and log a warning per team — only teams that already exist in the new org resolve. Pending invites also show up as drift in the end-of-run diff until the invitee accepts; that's expected, not a failure. End-of-run verification now diffs teams and direct collaborators in addition to settings and branch protection. Touches `gh-repo-mirror/SKILL.md`, `gh-repo-mirror/README.md`, `gh-repo-mirror/REFERENCE.md`, and `gh-repo-mirror/scripts/mirror-repo.zsh`. Catalog rows in root `README.md` and `site.js` updated to mention access in the tagline + detail.

## 2026-05-14

- Added a grill-depth selector to both `grill-me` and `domain-grill`. Each skill now asks the user how deep to grill before the first question, defaulting to **`deep`** (deepest), and accepts `quick` / `standard` / `deep` — aliases `1` / `2` / `3` and `sharp` / `medium` / `deepest` — either as the answer to that prompt or as a pre-selected invocation argument (e.g. `/grill-me quick`, `/domain-grill standard`). `deep` walks every branch of the decision tree, invents boundary scenarios, and cross-references claims against code / `CONTEXT.md` / existing ADRs until shared understanding (unbounded). `standard` covers the architectural spine plus the obvious edges in roughly 15–25 questions. `quick` runs only the top ~5–10 highest-leverage hard-hitters — deal-breaker assumptions, glossary conflicts that would mislead implementers, ADR contradictions — as triage rather than full coverage. Depth changes *how many branches* the skill walks, not *how sharp* each question is; for `domain-grill` the ADR-recording criteria (hard-to-reverse + surprising + real trade-off) and end-of-session summary still apply at every depth. Catalog updated end-to-end: `grill-me/SKILL.md`, `grill-me/README.md`, `domain-grill/SKILL.md`, `domain-grill/README.md`, both `site.js` skills-array entries (with new `usage:` strings `/grill-me [quick|standard|deep]` and `/domain-grill [quick|standard|deep]`), and the `site.js` changes feed.
- Renamed the handoff pair again to dodge a *second* shadow: `handoff` → **`session-handoff`** and `resume-handoff` → **`resume-session-handoff`**. New triggers are `/session-handoff` and `/resume-session-handoff`. The earlier same-day rename (`resume` → `resume-handoff`) only resolved the `/resume` shadow on Claude Code / Codex; but Devin already ships a built-in `/handoff` command for its own session-transfer flow, which shadowed the write side and made `resume-handoff` collide by association too. The pair is now unambiguous everywhere — Claude Code, Codex, Cursor, Gemini CLI, Devin, Windsurf. Behaviour is unchanged: same `.claude/handoffs/` document path, same preflight (project root / cwd / branch / uncommitted-count / 14-day staleness), same no-auto-execute resume that asks the user what to do next, same implicit `using-superpowers` bootstrap when available. Catalog updated end-to-end: `git mv handoff session-handoff` and `git mv resume-handoff resume-session-handoff` to preserve history, both `name:` frontmatter fields, every internal cross-reference in both SKILL.md and README.md files, the resume-hint line printed by `/session-handoff`, root README catalog table, `site.js` skills entries and changes feed, install-command lines, and the `Skill: /handoff` reference in `design-draft/SKILL.md` (step 8: Developer Handoff). Re-install with `npx skills@latest add amit-t/skills --skill session-handoff` and `npx skills@latest add amit-t/skills --skill resume-session-handoff`; remove any old `~/.agents/skills/handoff/`, `~/.agents/skills/resume-handoff/`, `~/.claude/skills/handoff`, and `~/.claude/skills/resume-handoff` install directories or symlinks — skill managers don't auto-prune renamed sources.
- Renamed the `resume` skill to **`resume-handoff`** and reworked its post-confirm behavior. Two reasons. **(1)** The trigger `/resume` collides with most agents' built-in conversation-restore command (Claude Code, Codex, others), which shadows the skill — typing `/resume` would fire the agent's "restore previous chat" command instead of loading the handoff document. The new name `/resume-handoff` is unambiguous: it always means *load the handoff doc written by `/handoff`*. **(2)** After preflight + confirm, the skill now updates frontmatter (`status: resumed`, `resumed_at`), moves the file to `.claude/handoffs/resumed/<resume-ts>--<orig-name>`, internalises the body, and **stops to ask the user what to do next** — presenting the Next-moves items, the Suggested-skills list, and a short menu of free-form options ("walk me through your understanding", "re-scope", "show the full body", "hold"). It no longer auto-executes the first Next-moves item; the user picks the direction. The skill also implicitly invokes `using-superpowers` *before* asking, if (and only if) that skill is listed in the environment's available skills, so process discipline (brainstorming → plan → TDD → verification) is loaded before the next step is chosen. If `using-superpowers` is not present, the bootstrap step is skipped silently — no path-guessing, no errors. Catalog updated end-to-end: directory renamed (`resume/` → `resume-handoff/`) via `git mv` to preserve history, top-level README row, `/handoff` SKILL.md + README.md cross-references and the resume-hint line it prints, `site.js` skills-array entry and changes feed all flipped to the new name. `/resume-handoff` retains `list` / `<n>` / `<slug-substring>` argument modes for non-newest selection and still refuses to re-resume any file already marked `status: resumed`. *Superseded same-day by the rename to `resume-session-handoff` once the Devin `/handoff` shadow was identified.*

## 2026-05-13

- Moved the `wisdom-capture` skill from `Engineering` to `Leadership` in the catalog (README table, `site.js` skills array, `site.js` changes feed, and the per-skill README header). The skill itself is unchanged — the recategorization reflects that wisdom capture serves leadership reflection more than engineering practice.
- Added the `wisdom-capture` skill under `Engineering` — records one wisdom snippet as one Markdown file under `wisdoms/<YYYY>/<MM>/<ulid>.md` with strict YAML frontmatter (`id`, `created_at`, `body_hash`, `category`, `tags`, `source_url`, `source_author`, `note`, `import_origin`). Reads `wisdoms/_categories.yml` as the closed taxonomy, proposes a primary bucket + 2–5 tags with a confidence label, can propose a *new* bucket when no existing one fits and fall back to a second-best existing pick when the user rejects the new bucket, asks for a personal gloss, computes a normalized-body sha256 hash for dedup, and commits with `wisdom: <category> — <body first 60>…`. Honors per-session push policy via `.wisdom-session` and the `WISDOM_NO_PUSH` env var. Vision-capable for image-trapped wisdom (slide-style reels, quote cards). Built as the agent half of the companion [`wisdom`](https://github.com/amit-t/wisdom) CLI repo, but works in any project that adopts the same data shape.
- Reworked the `handoff` skill and added a companion **`resume`** skill under `Agent Behavior` — handoffs now write to a predictable, discoverable `<project-root>/.claude/handoffs/YYYY-MM-DD-HHMM-<slug>.md` instead of an opaque `mktemp` path, so the next session never needs to be told the file path. `/handoff` resolves the project root via git toplevel → first `.claude/` ancestor → `pwd`, auto-adds `/.claude/handoffs/` to `.gitignore`, slugifies the `$ARGUMENTS` focus (falls back to a 2–3 word slug picked from the conversation goal), writes YAML frontmatter (`cwd`, `project_root`, `branch`, `uncommitted_files`, `focus`, `status`, `resumed_at`) above the markdown body, and writes atomically via `.tmp` rename. Filename collisions in the same minute get a `-2`, `-3` suffix. The companion `/resume` skill globs the same directory for the newest open handoff (top-level only — never recurses into `resumed/`), runs an environment preflight (project_root / cwd / branch / uncommitted-count drift, plus a >14-day staleness warning), summarises goal + Next moves + Suggested skills, and asks for confirmation. On confirm it mutates `status: resumed` + `resumed_at` in place and moves the file (atomic rename) to `.claude/handoffs/resumed/<resume-ts>--<orig-name>` so the audit trail is sorted by resume time. Supports `/resume list`, `/resume <n>`, and `/resume <slug-substring>` for non-newest selection; refuses to re-resume any file whose `status` is already `resumed`.
- Added the `session-feedback` skill under `Agent Behavior` — mines the current conversation for every correction the user made, every preference they stated, and every "do-differently" lesson, then writes a dated, frontmatter-tagged `feedback-<YYYY-MM-DD>.md` (stable IDs `C1`–`Cn`, `P1`–`Pn`, `D1`–`Dn`) into the project's Claude Code auto-memory directory and adds an entry to `MEMORY.md` so future sessions reload the patterns. Three explicit buckets (corrections / preferences / do differently); idempotent (append by default, `--overwrite` to replace); preserves the user's actual words for corrections so the pattern is recognisable, not just the conclusion.
- Added **recall mode** to `session-feedback` — in future sessions the skill surfaces each remembered item in a compact listing format and asks *"Do I care about this at the moment, or do I not care about it at the moment?"* before applying anything. Just-in-time recall is mandatory whenever the agent is about to act on a past pattern; bulk recall is available at session start via `/session-feedback --recall`. Session-scoped decisions live in `.active-feedback.json`; `always` / `never` answers persist back to the feedback file's frontmatter for that item. Nothing is ever silently applied — the carry-forward gate moved from write time to recall time so the user judges relevance in the moment, not in advance.

## 2026-05-12

- Added the `code-review` skill — principal-engineer review of a GitHub PR with two-phase approval. Pre-checks PR description quality (what / why / test plan), size (LOC + file count), and single-concern scope before deep review. Generates findings across an 11-dimension rubric (correctness, design, security, reliability, performance, testing, api_contract, observability, readability, scope_discipline, data_migration) grounded in Pragmatic Programmer, Domain-Driven Design, and A Philosophy of Software Design. Walks the user through every finding one at a time with approve / skip / edit / expand / defer / quit verbs. Only the approved subset is posted as one grouped GitHub Review. Never auto-APPROVEs. Re-review safe — dedupes against prior runs via hidden markers in comment bodies. Thresholds, rubric dimensions, and verdict policy are fully configurable in `code-review/config.yaml`.
- Added the `handoff` skill under `Agent Behavior` — writes a transferable handoff document to a `mktemp -t handoff-XXXXXX.md` path so a fresh agent can continue the work. Captures goal, current state, decisions, ruled-out approaches, open questions, concrete next moves, and suggested skills for the next session. References existing artifacts (PRDs, plans, ADRs, issues, commits, diffs) by path or URL instead of duplicating them. Accepts an argument describing the next session's focus and prunes the document to match.
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
