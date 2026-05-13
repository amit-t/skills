# resume

> Pick up where a previous session left off — loads the newest open handoff written by `/handoff`, with environment preflight and explicit user confirmation

**Category:** Agent Behavior

## What It Does

Discovers the newest open handoff document in the current project, runs a preflight check (project root / cwd / branch / uncommitted-file count / staleness), summarises the goal and next moves, asks for confirmation, and then moves the file to `.claude/handoffs/resumed/` while flipping its `status` frontmatter to `resumed` — so future invocations don't pick up an already-completed handoff.

**The user never has to remember or paste a file path.** The skill resolves the project root the same way `/handoff` does (`git rev-parse --show-toplevel` → ancestor with `.claude/` → `pwd`) and globs `<root>/.claude/handoffs/*.md` for the newest top-level file. The `resumed/` subdirectory is never recursed into.

### Pair with `/handoff`

`/handoff` writes, `/resume` reads. Install both together:

```bash
npx skills@latest add amit-t/skills --skill handoff
npx skills@latest add amit-t/skills --skill resume
```

### When to Use

- Starting a fresh session after running `/handoff` previously
- Switching agents or machines and continuing from a left-off handoff
- After a break, when you don't remember where the last session stopped

### When NOT to Use

- The new work is unrelated to any prior handoff
- The handoff directory is empty
- You want to *write* a handoff — use `/handoff`

## Usage

```text
/resume                    # load the newest open handoff
/resume list               # show all open handoffs, oldest first, indexed
/resume 2                  # load index 2 from the list
/resume migration          # substring match by filename
```

The default (no argument) targets the newest by filename — filenames are `YYYY-MM-DD-HHMM-<slug>.md`, so lexical sort equals chronological sort.

## Preflight checks

Before asking to resume, the skill compares the handoff's frontmatter against the current environment and surfaces drift:

| Field | Drift signal |
|---|---|
| `project_root` | Resumed in a different repo / worktree |
| `cwd` | You're in a different subdirectory |
| `branch` | Branch has changed since the handoff was written |
| `uncommitted_files` | Working tree differs from when the handoff was written |
| `created` | Older than 14 days → flagged as potentially stale |
| `status` | Already `resumed` → refuses to load; suggests `/resume list` |

Drift never blocks — it just makes the difference visible so you can decide.

## What happens on confirm

1. Frontmatter is updated in place: `status: resumed`, `resumed_at: <ISO-8601 now>`.
2. The file is moved (atomic rename) to `.claude/handoffs/resumed/<resume-ts>--<orig-basename>` so the audit trail is sorted by *resume time*, not original create time.
3. The skill proceeds with the first item from the handoff's **Next moves** section and offers to invoke any skills listed under **Suggested skills for next session** (does not auto-invoke).

If you decline, the file is left exactly where it was, still `status: open`, and the next `/resume` invocation will find it again.

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill resume
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r resume .cognition/skills/resume
# or
cp -r resume .windsurf/skills/resume

# Global
cp -r resume ~/.config/cognition/skills/resume
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r resume .claude/skills/resume

# Global
cp -r resume ~/.claude/skills/resume
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r resume .cursor/skills/resume
```

</details>

<details>
<summary>Codex</summary>

```bash
cat resume/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat resume/SKILL.md >> GEMINI.md
```

</details>

## Related Skills

- [`handoff`](../handoff) — the write side of this pair. `/handoff` produces the document `/resume` consumes. Install both together.
- [`compact-conversation`](../compact-conversation) — in-place conversation compaction for the *same* agent. Complementary, not a replacement.

## License

MIT
