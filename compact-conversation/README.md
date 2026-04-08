# compact-conversation

> Compact the current conversation into a concise summary, reducing context window usage while preserving critical information

**Category:** Agent Behavior

## What It Does

Creates a structured summary of the current conversation — completed work, key decisions, current state, and pending tasks — so you can continue in a fresh session without losing context.

Useful when a conversation grows long and the agent starts hitting context limits or losing earlier details. The summary is written to a file and can be referenced in a new session.

### When to Use

- Conversation has grown very long and context is being lost
- You want to hand off to a new session with full context
- The agent's context window is nearing its limit

### When NOT to Use

- **The agent has a built-in `/compact` command** (e.g., Claude Code, Aider) — always prefer native compaction
- Conversation is short (< 10 messages)
- You are actively debugging and need full context
- You are in the middle of a complex multi-step task

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill compact-conversation
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r compact-conversation .cognition/skills/compact-conversation
# or
cp -r compact-conversation .windsurf/skills/compact-conversation

# Global
cp -r compact-conversation ~/.config/cognition/skills/compact-conversation
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r compact-conversation .claude/skills/compact-conversation

# Global
cp -r compact-conversation ~/.claude/skills/compact-conversation
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r compact-conversation .cursor/skills/compact-conversation
```

</details>

<details>
<summary>Codex</summary>

```bash
cat compact-conversation/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat compact-conversation/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed as an agent skill, invoke in your session:

```text
/compact-conversation
```

Or use one of the trigger phrases:

- "compact this conversation"
- "compact the context"
- "reduce context window"
- "summarize our progress"

## License

MIT
