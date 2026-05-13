---
name: session-feedback
description: Mine the current conversation for every correction the user made, every preference they stated, and every "do-differently" lesson, then write a dated feedback file into the project's auto-memory directory so future sessions reload the patterns. Use when user says `/session-feedback`, "extract feedback from this session", "what did I correct you on", "lessons from this session", "summarise what I'd want you to do differently", or at the natural end of a non-trivial design / grilling / review session.
user-invocable: true
---

# /session-feedback — Distill a session into reusable feedback

Reads the live conversation, classifies user turns into three buckets, emits a dated `feedback-<YYYY-MM-DD>.md` to the project auto-memory directory, and indexes it in `MEMORY.md`. Idempotent: re-running on the same day appends a new section unless `--overwrite` is passed.

## Quick start

```
/session-feedback                  → write feedback-<today>.md to project memory dir
/session-feedback <path>           → write to a specific path
/session-feedback --overwrite      → replace an existing same-day file
/session-feedback --since "topic"  → only mine turns about a specific topic
```

Default path resolution:
1. If `~/.claude/projects/<encoded-cwd>/memory/` exists → write `feedback-<YYYY-MM-DD>.md` there.
2. Else if `.claude/memory/` exists in the cwd → write there.
3. Else create the auto-memory dir at #1 and write there.

`<encoded-cwd>` follows Claude Code's scheme: leading slash dropped, remaining slashes replaced with `-`, prefixed with `-`. Confirm in the `~/.claude/projects/` listing if unsure.

## Workflow

### 1. Scan the conversation
Walk every user turn. Drop pure acks ("yes", "thanks"), pure typos, and clarifying questions with no preference signal. For each surviving turn, also recall the assistant turn that *preceded* it — the correction's meaning lives in the contrast.

### 2. Classify into three buckets

**Corrections** — user pushed back on or changed your proposal. Signals:
- Negation / redirect: "no", "instead", "drop X", "change Y to Z", "is X needed?"
- Accept-with-modification: "accept all but...", "yes, also add..."
- Reframing a decision tree: a single sentence that promotes one branch over another or invalidates a sub-tree

**Preferences** — user stated how they want things done. Signals:
- Absolutes: "always", "never", "I want", "I prefer", "we don't do that here"
- External authority cited: books, frameworks, prior projects, conferences, named experts
- Domain or process beliefs: "PRs should be tiny", "deploys never on Fridays"

**Do differently** — *synthesise*, do not extract. For each correction, ask: *what general principle would have led me to the right answer first time?* Write the principle, not the local fix.

### 3. Emit the feedback file
Use the structure in [TEMPLATE.md](TEMPLATE.md). Group by bucket. Each entry: short bolded title + 1–3 lines (what you proposed, what user said, lesson). Keep every entry self-contained — a future-you should be able to read one bullet cold and apply it.

### 4. Update memory index
Add a line to `<memory-dir>/MEMORY.md`:
```
- [Session feedback YYYY-MM-DD (topic)](feedback-YYYY-MM-DD.md) — one-line hook
```
If `MEMORY.md` doesn't exist, create it with this line.

## Idempotency

| Target state | Behavior |
|---|---|
| File does not exist | Create it with frontmatter + content. |
| Exists, no `--overwrite` | Append `## <YYYY-MM-DD HH:MM> — <topic>` section. |
| Exists, `--overwrite` | Replace the entire file. |

Never silently overwrite. Never skip the MEMORY.md update on append.

## Quality bar

- Cite the user's actual words for at least the corrections bucket — phrasing encodes the principle better than your summary.
- Each "do differently" entry must be a general principle. *"Don't suggest `--dry-run`"* is too narrow; *"don't bolt safety flags onto a workflow that already provides the guarantee structurally"* is reusable.
- Don't pad. Two corrections and one preference → file has two corrections and one preference.
- Don't pretend lessons you didn't learn. If the user accepted every recommendation, say so.

## When to invoke

- End of a multi-turn design or grilling session
- After a review or debugging session where the user corrected the agent multiple times
- Before closing a project for the day if novel patterns emerged
- Any time the user wants future sessions to remember a hard-won lesson
