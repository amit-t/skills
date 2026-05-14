---
name: session-handoff
description: Compact the current conversation into a discoverable handoff document so a fresh agent can pick it up with /resume-session-handoff. Writes to `.claude/handoffs/<timestamp>-<slug>.md` inside the project root, gitignored by default. Use when the user wants to pass work to a fresh session, hand off to a teammate, or stop here and resume later. Triggers include "/session-handoff", "write a session handoff", "hand this off to another agent", "summarise so someone else can continue". Named `session-handoff` (not `/handoff`) because Devin already ships a built-in `/handoff` command that would shadow this skill.
argument-hint: "What will the next session be used for?"
---

# Session Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work via the companion `/resume-session-handoff` skill. The file is saved to a predictable, discoverable location inside the project — the next session does **not** need to be told the path.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

If the user passed arguments, treat them as a description of what the next session will focus on, write them into the `focus` frontmatter field, and tailor the document body accordingly.

## Workflow

1. **Resolve the project root.** Try in order:
   1. `git rev-parse --show-toplevel 2>/dev/null` — if non-empty, that is the root.
   2. Else walk upward from `pwd` looking for the first ancestor that contains a `.claude/` directory; that ancestor is the root.
   3. Else fall back to `pwd` itself **and warn the user**: "not in a git repo and no `.claude/` ancestor found — writing to `./.claude/handoffs/`. Discovery from sibling dirs may be inconsistent."
2. **Ensure the handoff directory exists.** `mkdir -p <root>/.claude/handoffs`. The `resumed/` subdir is created lazily by `/resume-session-handoff`, not here.
3. **Auto-add gitignore entry** (only when step 1 resolved via git):
   - If `<root>/.gitignore` exists and does not already contain a line matching `/.claude/handoffs/` (or a broader pattern that covers it), append `/.claude/handoffs/` on its own line, preceded by a blank line if the file does not end with one.
   - If `<root>/.gitignore` does not exist, create it with the single line `/.claude/handoffs/`.
   - Skip this step entirely when not in a git repo.
4. **Pick a slug.**
   - If `$ARGUMENTS` is non-empty, slugify it: lowercase, replace any run of non-`[a-z0-9]` with `-`, trim leading/trailing `-`, collapse repeated `-`, cap at 40 characters (cut on a `-` boundary if possible).
   - Else pick a 2–3 word slug from the conversation goal, then slugify the same way.
   - Slug must be non-empty; if slugification yields the empty string, use `session-handoff`.
5. **Compose the filename.** `YYYY-MM-DD-HHMM-<slug>.md` using local time. If a file with that exact name already exists (same minute + same slug), append `-2`, `-3`, ... before `.md` until you find an unused name.
6. **Scan the conversation.** Pull out: the user's goal, decisions made, blockers hit, what's been tried, what's been *ruled out*, files touched, commands run, and any uncommitted state.
7. **Find the artifacts.** Note every PRD / plan / ADR / issue / commit / PR / diff / log produced this session. Reference them by absolute path or URL — never paste their content.
8. **Tailor to the focus.** If `$ARGUMENTS` describes what the next session will do, prune the body to what *that* session needs. Drop history irrelevant to the next move.
9. **Suggest skills.** Recommend specific skills the next agent should invoke (e.g. `/tdd`, `/eng-spec`, `/repo-context-scan`). Only suggest skills you actually know exist in the user's environment.
10. **Atomic write.** Write the document to `<filename>.tmp` first, then `mv` it to the final name. This avoids leaving a half-written file if anything dies mid-write. Read the temp file before writing it (required by the Write tool contract).
11. **Print the resume hint.** On its own line, print exactly:
    ```
    Next session: run /resume-session-handoff (or install with `npx skills@latest add amit-t/skills --skill resume-session-handoff`).
    ```
    Print the absolute path of the written file on a second line so the user can grep for it if needed, but make clear they do **not** need to remember the path — `/resume-session-handoff` discovers it automatically. (Note: the skill is `resume-session-handoff`, not `resume`, because most agents already ship a built-in `/resume` that restores the previous conversation transcript and would shadow this skill. The write side is named `session-handoff`, not `handoff`, because Devin already ships a built-in `/handoff` that would shadow it.)

## Document structure

YAML frontmatter for machine-readable fields (parsed by `/resume-session-handoff`'s preflight), markdown body for the human-readable prose. Skip body sections that don't apply — empty sections are noise.

```markdown
---
focus: "<from $ARGUMENTS, empty string if absent>"
created: <ISO-8601 local timestamp, e.g. 2026-05-13T14:30:00-07:00>
cwd: <absolute path of pwd at write time>
project_root: <absolute path resolved in step 1>
branch: <current git branch, or "" if not in git>
worktree: <git worktree path if different from project_root, else "">
uncommitted_files: <integer count of `git status --porcelain` lines, or 0>
status: open
resumed_at: null
---

# Handoff — <one-line title>

## Goal
<what the user is ultimately trying to do — 1–3 sentences>

## State right now
- Where execution stopped and why.
- What is committed vs. uncommitted vs. lost-if-not-resumed.

## Decisions made
- <decision> — <one-line rationale>

## Ruled out
- <approach> — <why it was rejected> (so next agent doesn't re-try it)

## Open questions / blockers
- <question> — <what would unblock it>

## Artifacts (do not re-derive)
- `path/to/prd.md` — <what it covers>
- `https://github.com/.../pull/123` — <status>
- commit `abc1234` — <what it landed>

## Next moves
1. <concrete first step>
2. <second step>
3. ...

## Suggested skills for next session
- `/skill-name` — <why it fits the next move>

## Environment notes
- Tools, env vars, secrets, services, running processes — anything the next agent must know that isn't obvious from the repo.
```

## Rules

- **Reference, don't duplicate.** If a PRD already says it, link the PRD. If a commit already does it, cite the SHA.
- **Be specific.** "Fix the bug" is useless; "rerun `pnpm test packages/api/auth.test.ts` after changing `verifyToken` to read `req.cookies.session`" is a handoff.
- **Capture failures.** What was tried and didn't work matters as much as what worked.
- **Cite paths absolutely.** Use absolute paths so the next agent doesn't have to guess `cwd`.
- **No emojis, no filler, no apologies.** This document is operational, not narrative.
- **Frontmatter is the source of truth for machine fields.** `/resume-session-handoff` only reads frontmatter for its preflight checks (branch, cwd, uncommitted count, status). Keep the body for humans.
- **Don't move the file yourself.** `/resume-session-handoff` moves it to `.claude/handoffs/resumed/` on user confirmation. `/session-handoff` only writes.

## Companion skill

`/resume-session-handoff` is the read side of this pair. Whenever a fresh session needs to pick up where this one left off, the user invokes `/resume-session-handoff` and the newest open handoff in `.claude/handoffs/` is loaded automatically. Install both skills together:

```bash
npx skills@latest add amit-t/skills --skill session-handoff
npx skills@latest add amit-t/skills --skill resume-session-handoff
```

## When NOT to use

- Conversation is short and the next agent can read the transcript directly.
- A plan, PRD, or issue already captures the state — point at it instead.
- Mid-debugging on a single bug where transferring context costs more than just finishing it.
