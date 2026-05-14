# resume-handoff

> Pick up where a previous session left off — loads the newest open handoff written by `/handoff`, runs an environment preflight, marks the file resumed, and **asks the user what to do next** before touching anything.

**Category:** Agent Behavior

## What It Does

Discovers the newest open handoff document in the current project, runs a preflight check (project root / cwd / branch / uncommitted-file count / staleness), summarises the goal and next moves, asks for confirmation, then on Y:

1. Updates frontmatter (`status: resumed`, `resumed_at: <now>`) and moves the file to `.claude/handoffs/resumed/`.
2. Bootstraps `using-superpowers` if that skill is available in the environment, so process discipline (brainstorming → plan → TDD → verification) is loaded **before** the next move is chosen.
3. Internalises the handoff body, then **stops and asks the user what to do next**. It does not pick up the first Next-moves item on its own — the user decides the direction.

**The user never has to remember or paste a file path.** The skill resolves the project root the same way `/handoff` does (`git rev-parse --show-toplevel` → ancestor with `.claude/` → `pwd`) and globs `<root>/.claude/handoffs/*.md` for the newest top-level file. The `resumed/` subdirectory is never recursed into.

### Why `resume-handoff`, not `resume`

Most agents (Claude Code, Codex, others) already ship a built-in `/resume` command that restores the prior conversation transcript. A skill named `resume` is shadowed in those environments — typing `/resume` triggers the agent's built-in, not the skill. `/resume-handoff` is unambiguous: it always means *load the handoff document written by `/handoff`*.

### Pair with `/handoff`

`/handoff` writes, `/resume-handoff` reads. Install both together:

```bash
npx skills@latest add amit-t/skills --skill handoff
npx skills@latest add amit-t/skills --skill resume-handoff
```

### When to Use

- Starting a fresh session after running `/handoff` previously
- Switching agents or machines and continuing from a left-off handoff
- After a break, when you don't remember where the last session stopped

### When NOT to Use

- The new work is unrelated to any prior handoff
- The handoff directory is empty
- You want to *write* a handoff — use `/handoff`
- You meant the agent's built-in `/resume` (restore the prior chat) — that's a different operation

## Usage

```text
/resume-handoff                    # load the newest open handoff
/resume-handoff list               # show all open handoffs, oldest first, indexed
/resume-handoff 2                  # load index 2 from the list
/resume-handoff migration          # substring match by filename
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
| `status` | Already `resumed` → refuses to load; suggests `/resume-handoff list` |

Drift never blocks — it just makes the difference visible so you can decide.

## What happens on confirm

1. If `using-superpowers` is listed as an available skill, the agent invokes it via the platform's skill mechanism (Claude Code `Skill`, Copilot CLI `skill`, Gemini CLI `activate_skill`). Skipped silently if not present.
2. Frontmatter is updated in place: `status: resumed`, `resumed_at: <ISO-8601 now>`.
3. The file is moved (atomic rename) to `.claude/handoffs/resumed/<resume-ts>--<orig-basename>` so the audit trail is sorted by *resume time*, not original create time.
4. The agent internalises the body and **stops**. It presents:
   - The Next-moves items, numbered.
   - The Suggested-skills list.
   - Free-form options ("walk me through your understanding", "re-scope", "show the full body", "hold").
   - **Then waits for the user to pick a direction.** No edits, no shell side-effects, no skill invocations until the user chooses.

If you decline, the file is left exactly where it was, still `status: open`, and the next `/resume-handoff` invocation will find it again.

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill resume-handoff
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r resume-handoff .cognition/skills/resume-handoff
# or
cp -r resume-handoff .windsurf/skills/resume-handoff

# Global
cp -r resume-handoff ~/.config/cognition/skills/resume-handoff
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r resume-handoff .claude/skills/resume-handoff

# Global
cp -r resume-handoff ~/.claude/skills/resume-handoff
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r resume-handoff .cursor/skills/resume-handoff
```

</details>

<details>
<summary>Codex</summary>

```bash
cat resume-handoff/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat resume-handoff/SKILL.md >> GEMINI.md
```

</details>

## Related Skills

- [`handoff`](../handoff) — the write side of this pair. `/handoff` produces the document `/resume-handoff` consumes. Install both together.
- [`compact-conversation`](../compact-conversation) — in-place conversation compaction for the *same* agent. Complementary, not a replacement.

## License

MIT
