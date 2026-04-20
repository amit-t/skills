# skill-sync utility + companion skill — Design

**Date:** 2026-04-20
**Status:** Approved (pending user spec review)
**Scope:** Two deliverables

1. Refresh `e2e-audit` skill in at-skills from the updated source in `refinery-app`, then open a PR to `main`.
2. Build a reusable `skill-sync` utility (at `ai-utils/skill-sync/`) plus a companion at-skills skill (category `Agent Behavior`) that syncs or scaffolds skills from an arbitrary source path.

## Part 1 — Refresh `e2e-audit`

**Source of truth:** `/Users/amittiwari/Projects/Refinery/engineering/refinery-app/.agents/skills/e2e-audit/`
**Destination:** `/Users/amittiwari/Projects/Tools-Utilities/at-skills/e2e-audit/`

### Steps

1. Branch off `dev` → `feat/e2e-audit-refresh`.
2. Diff source vs destination (`SKILL.md`, `README.md`). Note: source `SKILL.md` is ~17.5 KB, destination is ~9.9 KB — meaningful rewrite expected.
3. Copy source files over destination files verbatim.
4. Catalog sync per `CLAUDE.md`:
   - `CHANGELOG.md` — bullet under `## 2026-04-20`.
   - `site.js` `changes` array — entry dated 2026-04-20.
   - `site.js` `skills` array — update `detail` / `tagline` if SKILL.md description changed.
   - `README.md` — update row under correct category table if tagline changed.
   - `skills-lock.json` — refresh `computedHash` if already tracked (otherwise skip).
5. Commit: `feat(e2e-audit): sync from refinery-app`.
6. Push branch, open PR to `main`, include diff summary in body.

### Non-goals

- No restructuring of e2e-audit beyond the source. This is a one-way pull.

## Part 2 — `skill-sync` utility

### Location

`/Users/amittiwari/Projects/Tools-Utilities/ai-utils/skill-sync/`

### File layout

| File | Purpose |
|------|---------|
| `skill-sync.zsh` | Main script. Runs from any cwd; assumes cwd = target skills repo. |
| `skill-sync.prompt.md` | Prompt consumed by `claude` / `codex` / `devin` when building a new skill. |
| `install.zsh` | One-shot installer that symlinks `skill-sync.zsh` into `~/.local/bin/skill-sync` and makes it executable. |
| `README.md` | Human-facing usage and examples. |

### CLI

```
skill-sync <source-path> [skill-name] [--agent claude|codex|devin] [--yolo]
```

**Positional args:**

- `source-path` (required). Direct path to a skill directory (must contain `SKILL.md`).
- `skill-name` (optional). When provided, utility runs in **sync mode** — copies source over `<cwd>/<skill-name>/`. When omitted, utility runs in **build mode** — invokes an agent to scaffold a new skill from the source.

**Flags:**

- `--agent` — one of `claude` (default), `codex`, `devin`. Selects the CLI used in build mode. Ignored in sync mode.
- `--yolo` — pass through dangerous-permission flag to the agent (e.g. `devin --permission-mode dangerous`, `claude --dangerously-skip-permissions`).

### Validation

Before any work:

1. Verify cwd is a skills repo. Marker: both `site.js` and `AGENTS.md` present at cwd root. Otherwise abort with actionable error.
2. Verify `source-path` exists and contains `SKILL.md`. Otherwise abort.
3. In build mode, verify the chosen agent CLI is on `PATH`.

### Sync mode (skill-name passed)

1. `rsync -a --delete <source>/ <cwd>/<skill-name>/` (mirrors source into destination, removes files no longer in source).
2. Parse SKILL.md frontmatter from the destination: `name`, `description`, `category`.
   - If `category` is missing, interactively prompt the user (numbered multiple choice from the fixed list: `Product Management`, `Project Management`, `Engineering`, `UX Design`, `Agent Behavior`, `AI Agent`).
3. Update catalog files:
   - `README.md` — upsert a row in the table under the resolved category. Row format matches the existing README convention (name linked to skill dir, tagline from `description`).
   - `site.js` `skills` array — upsert an object with `slug`, `name`, `category`, `tagline`, `detail`, `usage`. `tagline` comes from `description`; `detail` from the first paragraph of SKILL.md body; `usage` defaults to `/<slug>`.
   - `site.js` `changes` array — prepend a new entry under today's date (`2026-04-20` convention) describing the sync.
   - `CHANGELOG.md` — insert a bullet under today's date heading (create the heading if missing).
   - `skills-lock.json` — upsert entry with `source` (user-provided or derived), `sourceType`, and a freshly computed SHA-256 of the destination SKILL.md.
4. Print a summary of files touched.

### Build mode (skill-name omitted)

1. Resolve agent CLI:
   - `claude` → `claude` (yolo: `claude --dangerously-skip-permissions`).
   - `codex` → `codex exec` (yolo: `codex exec --full-auto`). Non-yolo uses interactive `codex`.
   - `devin` → `devin` (yolo: `devin --permission-mode dangerous`).
2. Render `skill-sync.prompt.md`, passing context via environment variables (`SKILL_SOURCE_PATH`, `SKILLS_REPO_DIR`) plus appended instructions.
3. Exec the agent with `--prompt-file skill-sync.prompt.md` (or equivalent per CLI).
4. Agent is instructed to follow the at-skills `write-a-skill` skill and the Catalog Sync Rule in `CLAUDE.md`.

### Prompt content (`skill-sync.prompt.md`)

- Tells agent: "Build a new at-skills skill from `$SKILL_SOURCE_PATH`. Target repo root is `$SKILLS_REPO_DIR`."
- Requires: create `<slug>/SKILL.md` + `<slug>/README.md`, update `README.md` catalog table, update `site.js` skills + changes arrays, update `CHANGELOG.md`, update `skills-lock.json`.
- Requires: follow conventional commits and the repo's `AGENTS.md` / `CLAUDE.md` conventions.
- Defers category selection to user if ambiguous.

### Dependencies

- `jq` (JSON edits for `skills-lock.json`).
- `python3` — used for regex edits to `site.js` (robust array mutation is hard in pure zsh).
- `rsync` (pre-installed on macOS).
- Agent CLIs: `claude`, `codex`, `devin` (only the selected one must be installed).

### Error handling

- Any validation failure → non-zero exit, actionable message.
- Sync mode never edits catalog files if the rsync step fails.
- Build mode passes exit code from the agent through.

## Part 3 — Companion skill `skill-sync` in at-skills

### Location

`at-skills/skill-sync/`

### Category

`Agent Behavior`.

### Files

- `SKILL.md` — frontmatter (`name: skill-sync`, `description`, `category: Agent Behavior`, triggers), plus body.
- `README.md` — human-facing overview.

### Frontmatter + triggers

```yaml
---
name: skill-sync
description: Sync an existing at-skills skill from a source path, or scaffold a new one via claude/codex/devin.
category: Agent Behavior
---
```

Trigger phrases: `/skill-sync`, "sync this skill from path X", "pull updates for skill X from path Y", "build a new skill from path Z".

### Body outline

1. **Preconditions.** cwd is the target skills repo (`at-skills` or `qr-skills`). `skill-sync` on `PATH`.
2. **Dispatch.**
   - If user passes a skill name → sync mode.
   - Otherwise → build mode; ask which agent (`claude` default).
3. **Invocation examples.**
   - `skill-sync /path/to/source e2e-audit`
   - `skill-sync /path/to/new-source --agent codex`
   - `skill-sync /path/to/new-source --agent devin --yolo`
4. **Post-sync steps.** Review diff (`git status` / `git diff`), confirm catalog files updated, create conventional commit (`feat(skill-name): ...`), open PR to `main`.
5. **Failure recovery.** If validation fails, fix cwd or source path and retry. If the agent fails mid-build, inspect partial output, fix, resume.

### Catalog entries added in this PR

- `README.md` — row under `Agent Behavior` table.
- `site.js` `skills` array — entry for `skill-sync`.
- `site.js` `changes` array — entry dated 2026-04-20.
- `CHANGELOG.md` — bullet under `## 2026-04-20`.

## Cross-cutting concerns

### Testing

- Part 1: run `git diff` after sync to confirm e2e-audit files match source. Manual PR review.
- Part 2 (utility): dry-run sync mode against a scratch skill (e.g., clone a tmp dir from `at-skills/design-draft/`), verify catalog mutations are idempotent (running twice yields no extra entry). Build mode is exercised by invoking against the refinery `e2e-audit` source as a smoke test (but do not commit that output).
- Part 3 (companion skill): ensure `SKILL.md` frontmatter parses via the same rules the utility uses.

### Idempotency

Sync mode must be safe to re-run. Upserts (not appends) for `site.js skills`, `skills-lock.json`, and `README.md` rows. The `changes` array and `CHANGELOG.md` de-dupe by `(date, skill-name)` pair.

### Out of scope

- No automatic git commit or PR creation from the utility. User drives git manually.
- No support for syncing multiple skills in one invocation.
- No `qr-skills`-specific logic — the utility is repo-agnostic as long as the marker files exist.

## Delivery order

1. Part 1 (e2e-audit refresh) — PR to `main` in `at-skills`.
2. Part 2 (utility) — commit to `ai-utils` repo on a feature branch; user merges manually (no PR flow requested).
3. Part 3 (companion skill) — PR to `main` in `at-skills`, separate from Part 1.
