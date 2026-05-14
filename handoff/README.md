# handoff

> Compact the current conversation into a discoverable handoff document so a fresh agent can pick it up with `/resume-handoff`

**Category:** Agent Behavior

## What It Does

Writes a focused handoff document so a fresh agent — or a teammate — can continue the work without re-reading the whole transcript.

Captures goal, current state, decisions, ruled-out approaches, open questions, suggested next moves, and skills the next session should invoke. References existing artifacts (PRDs, plans, ADRs, issues, commits) by path or URL instead of duplicating them.

The document is saved to a predictable, discoverable path inside the project:

```
<project-root>/.claude/handoffs/<YYYY-MM-DD-HHMM>-<slug>.md
```

Project root is resolved as `git rev-parse --show-toplevel` → first ancestor with a `.claude/` dir → `pwd` (with a warning). The directory is auto-added to `.gitignore` on first write, so handoffs stay local and never ride into commits by accident.

The companion `/resume-handoff` skill globs that directory for the newest open handoff and resumes from it — **the next session never needs to be told the file path**. (The skill is named `resume-handoff` rather than `resume` because most agents already ship a built-in `/resume` command for restoring the previous conversation, which would otherwise shadow the skill.)

### Pair with `/resume-handoff`

`/handoff` writes, `/resume-handoff` reads. Install both together:

```bash
npx skills@latest add amit-t/skills --skill handoff
npx skills@latest add amit-t/skills --skill resume-handoff
```

### When to Use

- Conversation is wrapping up and someone else (or a fresh session) will continue
- Context window is full enough that handing off is cheaper than continuing
- Switching machines, switching agents, or pausing work for the day
- You want a deliverable that survives the session, not an in-memory summary

### When NOT to Use

- Conversation is short and the next agent can just read the transcript
- A PRD, plan, or issue already captures everything — link to it instead
- Mid-debugging where transferring context costs more than just finishing

## Usage

```text
/handoff
/handoff "next session will land the migration in #218"
```

The optional argument describes what the next session will focus on; the doc is pruned to what that session needs and the argument is recorded in the handoff's `focus` frontmatter field.

## Document layout

YAML frontmatter on top for machine-readable fields (`created`, `cwd`, `project_root`, `branch`, `uncommitted_files`, `focus`, `status`, `resumed_at`), markdown body below for human-readable prose (Goal, State, Decisions, Ruled out, Open questions, Artifacts, Next moves, Suggested skills, Environment notes). `/resume-handoff` parses only the frontmatter for its preflight checks; the body is for you and the next agent.

## Lifecycle

1. `/handoff` writes `.claude/handoffs/<ts>-<slug>.md` with `status: open` and `resumed_at: null`.
2. `/resume-handoff` in a future session reads the newest open file, runs preflight (cwd / branch / uncommitted-count drift), and on user confirmation **moves** it to `.claude/handoffs/resumed/<resume-ts>--<orig-name>.md`, flips `status: resumed` + sets `resumed_at`, internalises the body, and **asks the user what to do next** instead of auto-executing the first listed move.
3. The `resumed/` directory is an audit trail. The skill never prunes it; remove old entries manually whenever you like.

If the user invokes `/handoff` multiple times before resuming any of them, `/resume-handoff` picks the newest by default and surfaces a one-line notice that older unresumed handoffs exist.

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill handoff
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r handoff .cognition/skills/handoff
# or
cp -r handoff .windsurf/skills/handoff

# Global
cp -r handoff ~/.config/cognition/skills/handoff
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r handoff .claude/skills/handoff

# Global
cp -r handoff ~/.claude/skills/handoff
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r handoff .cursor/skills/handoff
```

</details>

<details>
<summary>Codex</summary>

```bash
cat handoff/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat handoff/SKILL.md >> GEMINI.md
```

</details>

## Related Skills

- [`resume-handoff`](../resume-handoff) — the read side of this pair. `/resume-handoff` discovers and loads the newest open handoff written by `/handoff`, then asks you what to do next. Install both together.
- [`compact-conversation`](../compact-conversation) — summarises conversation state in-place; use when the *same* agent will continue in a new session. `handoff` produces a transferable doc aimed at a *different* agent or a fresh session.
- [`concise-reporting`](../concise-reporting) — keeps in-session reports terse; complements the handoff doc which is always terse by construction.

## License

MIT
