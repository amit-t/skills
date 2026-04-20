---
name: skill-sync
description: Sync an existing at-skills skill from a source path, or scaffold a new one via claude/codex/devin. Wraps the skill-sync zsh utility in ai-utils.
category: Agent Behavior
disable-model-invocation: false
user-invocable: true
---

# /skill-sync — Sync or Build at-skills Skills From a Source Path

When this skill is invoked, drive the `skill-sync` zsh utility (installed from `ai-utils/skill-sync/`) to either pull updates for an existing skill or scaffold a new one.

## Quick Start

```
/skill-sync <source-path>                              → Build new skill via claude (default agent)
/skill-sync <source-path> <skill-name>                 → Sync existing skill from path
/skill-sync <source-path> --agent codex                → Build new skill via codex
/skill-sync <source-path> --agent devin --yolo         → Build new skill via devin (dangerous perms)
```

**What you get:**
- **Sync mode**: Source skill mirrored into `<cwd>/<skill-name>/`, plus catalog entries upserted in `README.md`, `site.js` (skills + changes arrays), `CHANGELOG.md`, and `skills-lock.json`. Idempotent.
- **Build mode**: A new skill scaffold written by the chosen agent CLI, following the at-skills `write-a-skill` skill conventions and the catalog-sync rule in `CLAUDE.md`.

## Preconditions

1. `cwd` must be the root of an at-skills-style repo (must contain `site.js` and `AGENTS.md`). The utility validates this and aborts with a clear error otherwise.
2. `skill-sync` must be on `$PATH`. Install with:
   ```
   cd ~/Projects/Tools-Utilities/ai-utils/skill-sync && ./install.zsh
   ```
3. For build mode: the chosen agent CLI (`claude`, `codex`, or `devin`) must be on `$PATH`.

## Dispatch Logic

```
skill-name passed?
├── yes → SYNC MODE (rsync + catalog upsert; no agent invoked)
└── no  → BUILD MODE (invoke agent with skill-sync.prompt.md)
```

## Step-by-Step

### Sync mode

1. Confirm with the user: source path, target skill name (often the basename of the source), and that they understand the destination directory will be mirrored (`rsync --delete`).
2. Run:
   ```
   skill-sync <source-path> <skill-name>
   ```
3. Review the diff: `git status && git diff`.
4. Commit using conventional commits, e.g.:
   ```
   git add <skill-name>/ README.md site.js CHANGELOG.md skills-lock.json
   git commit -m "feat(<skill-name>): sync from <upstream>"
   ```
5. Push and open a PR to `main`:
   ```
   git push -u origin feat/<skill-name>-sync
   gh pr create --base main --title "feat(<skill-name>): sync from <upstream>" --body "..."
   ```

### Build mode

1. Confirm with the user: source path, agent (`claude` default), whether to use `--yolo`.
2. Run:
   ```
   skill-sync <source-path> [--agent codex|devin] [--yolo]
   ```
3. The utility hands control to the agent. The agent reads `$SKILL_SOURCE_PATH`, picks a slug + category, and writes:
   - `<slug>/SKILL.md`
   - `<slug>/README.md`
   - Updates to `README.md`, `site.js`, `CHANGELOG.md`, `skills-lock.json`
4. After the agent finishes, review and commit as in sync mode.

## Examples

Pull e2e-audit refresh from refinery-app:

```
cd ~/Projects/Tools-Utilities/at-skills
/skill-sync ~/Projects/Refinery/engineering/refinery-app/.agents/skills/e2e-audit e2e-audit
```

Build a new skill from a directory of source notes via codex:

```
cd ~/Projects/Tools-Utilities/at-skills
/skill-sync ~/Projects/Refinery/engineering/refinery-app/.agents/skills/new-thing --agent codex
```

Same, yolo with devin:

```
/skill-sync ~/path/to/source --agent devin --yolo
```

## Failure Recovery

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cwd does not look like a skills repo` | Wrong cwd | `cd` into the at-skills (or qr-skills) repo root |
| `no SKILL.md found at <path>/SKILL.md` | Source path wrong or not a skill dir | Pass the directory that contains `SKILL.md`, not its parent |
| `agent CLI not on PATH` | Agent not installed or not in `$PATH` | Install it, or pick a different `--agent` |
| Catalog has stale entries after build | Agent skipped a file | Re-run `skill-sync <source-path> <slug>` once the skill files exist — sync mode upserts the catalog |
| Sync touched files you did not expect | `rsync --delete` removed files in dest not in source | This is intentional; if undesired, run with a staging dir first |

## Output Files

| File | Effect |
|------|--------|
| `<cwd>/<skill-name>/SKILL.md`, `README.md` | Mirrored from source (sync) or written by agent (build) |
| `<cwd>/README.md` | Row upserted under correct category table |
| `<cwd>/site.js` | `skills` array entry upserted; `changes` array prepended under today's date |
| `<cwd>/CHANGELOG.md` | Bullet under today's date heading (creates heading if missing) |
| `<cwd>/skills-lock.json` | Entry refreshed with SHA-256 of `SKILL.md` |

## When Not To Use

- For a brand-new skill that has no source material — use `write-a-skill` directly.
- For one-off edits to an existing skill that don't change its `SKILL.md` description — just edit the file; no sync needed.
