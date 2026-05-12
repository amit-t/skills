# handoff

> Compact the current conversation into a handoff document for another agent to pick up

**Category:** Agent Behavior

## What It Does

Writes a focused handoff document so a fresh agent — or a teammate — can continue the work without re-reading the whole transcript.

Captures goal, current state, decisions, ruled-out approaches, open questions, suggested next moves, and skills the next session should invoke. References existing artifacts (PRDs, plans, ADRs, issues, commits) by path or URL instead of duplicating them.

The document is written to a temp path produced by `mktemp -t handoff-XXXXXX.md` — never committed by default.

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

The optional argument describes what the next session will focus on; the doc is pruned to what that session needs.

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

- [`compact-conversation`](../compact-conversation) — summarises conversation state in-place (`.windsurf/conversation-summary.md`); use when the same agent will continue in a new session. `handoff` produces a transferable doc aimed at a *different* agent.
- [`concise-reporting`](../concise-reporting) — keeps in-session reports terse; complements the handoff doc which is always terse by construction.

## License

MIT
