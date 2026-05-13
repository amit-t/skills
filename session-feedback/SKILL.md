---
name: session-feedback
description: Mine the current conversation for every correction the user made, every preference they stated, and every "do-differently" lesson, then write a dated feedback file into the project's auto-memory directory so future sessions can reload the patterns. In future sessions, before applying any item from a past feedback file the agent must ask the user "Do I care about this at the moment, or do I not?" using the compact recall-listing format. Use when user says `/session-feedback` (write mode), `/session-feedback --recall` (bulk recall at session start), or whenever the agent is about to apply a remembered pattern (just-in-time recall).
user-invocable: true
---

# /session-feedback — Distill a session, and recall it deliberately

Two modes.

**Write mode** (default): read the live conversation, classify into three buckets, emit a dated `feedback-<YYYY-MM-DD>.md` to the project auto-memory directory, index it in `MEMORY.md`. No per-item filtering at write time — every extracted item is preserved as a durable candidate.

**Recall mode** (auto-triggered in future sessions; explicit `--recall` invocation also supported): before applying any item from a past `feedback_*.md` file, surface it to the user in the compact listing format and ask *"Do I care about this at the moment, or do I not care about it at the moment?"* User's answers are session-scoped — "yes" items are applied for the rest of the session; "no" items are suppressed.

## Quick start

```
/session-feedback                 → WRITE: emit feedback-<today>.md
/session-feedback <path>          → WRITE: write to a specific path
/session-feedback --overwrite     → WRITE: replace existing same-day file
/session-feedback --since "topic" → WRITE: only mine turns about a specific topic

/session-feedback --recall        → RECALL: walk all past feedback files at session start
```

Default write path resolution:
1. If `~/.claude/projects/<encoded-cwd>/memory/` exists → write `feedback-<YYYY-MM-DD>.md` there.
2. Else if `.claude/memory/` exists in cwd → write there.
3. Else create the auto-memory dir at #1.

## Write mode workflow

### 1. Scan
Walk every user turn. Drop pure acks, typos, and clarifying questions with no preference signal. For each surviving turn, recall the preceding assistant turn — the correction's meaning lives in the contrast.

### 2. Classify into three buckets
- **Corrections** — user pushed back on or changed your proposal (negations, accept-with-modification, reframings).
- **Preferences** — explicit "always" / "never" / "I want" / cited authorities / process beliefs.
- **Do differently** — *synthesised* general principles, not local fixes. Each entry should apply to multiple future situations.

### 3. Emit the file
Use the structure in [TEMPLATE.md](TEMPLATE.md). Stable IDs (`C1`–`Cn`, `P1`–`Pn`, `D1`–`Dn`). No checkboxes — items are durable candidates. Cite the user's actual words for corrections; phrasing encodes the principle better than a summary.

### 4. Update memory index
Add a line to `<memory-dir>/MEMORY.md`:
```
- [Session feedback YYYY-MM-DD (topic)](feedback-YYYY-MM-DD.md) — N items: <one-line hook on the session topic>
```

## Recall mode workflow

Fires in two situations:

**A. Just-in-time (per-reference).** Whenever the agent is about to apply a pattern that traces back to an item in a `feedback_*.md` memory file, the agent must first surface that item and ask the user. Present the item in this exact compact form:

```
**<ID>** *(<bucket>)* — <bolded title> — <one-line lesson hook>

Do I care about this at the moment, or do I not?
```

Wait for the answer. If `yes` / `still applies` / `keep` → apply the pattern, record decision. If `no` / `not now` / `skip` → suppress for the rest of this session, record decision. If `always` / `never ask again` → persist the decision durably (write back to the feedback file as a frontmatter `applies: always` / `applies: never` field on that specific item). Decisions for the session live in `<memory-dir>/.active-feedback.json` so they aren't re-asked within the same conversation.

**B. Bulk at session start (`/session-feedback --recall`).** Walk every `feedback_*.md` file in the memory directory. Present **every item** in the compact listing format, grouped by bucket and source file. Ask the user, in one consolidated prompt, which currently apply. Capture answers into `.active-feedback.json` for the session. Items the user does not address remain candidates for just-in-time recall later.

In both flavours: never apply a remembered item silently. The user must always have a chance to say "not now".

## Idempotency

| Target state | Behavior |
|---|---|
| File does not exist | Create it with frontmatter + content. |
| Exists, no `--overwrite` | Append `## <YYYY-MM-DD HH:MM> — <topic>` section; continue ID sequence. |
| Exists, `--overwrite` | Replace the entire file (keep frontmatter, refresh content). |

Never silently overwrite. Never apply a recalled item without asking.

## Quality bar

- Cite the user's actual words for at least the corrections bucket — phrasing encodes the principle.
- Each "do differently" entry must be a general principle. *"Don't suggest `--dry-run`"* is too narrow; *"don't bolt safety flags onto a workflow that already provides the guarantee structurally"* is reusable.
- Don't pad. Two corrections + one preference → file has two corrections and one preference.
- Don't pretend lessons you didn't learn.

## When to invoke

- **Write:** end of any non-trivial design / grilling / review / debug session, or before closing a project for the day.
- **Recall (bulk):** start of a new session where past feedback files exist and might apply broadly to the upcoming work.
- **Recall (just-in-time):** mandatory whenever the agent recognises a past pattern is about to influence its action.
