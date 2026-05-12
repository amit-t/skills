---
name: handoff
description: Compact the current conversation into a handoff document for another agent to pick up. Use when the user wants to pass work to a fresh session, hand off to a teammate, or stop here and resume later. Triggers include "/handoff", "write a handoff", "hand this off to another agent", "summarise so someone else can continue".
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a handoff document summarising the current conversation so a fresh agent can continue the work. Save it to a path produced by `mktemp -t handoff-XXXXXX.md` (read the file before you write to it).

Suggest the skills to be used, if any, by the next session.

Do not duplicate content already captured in other artifacts (PRDs, plans, ADRs, issues, commits, diffs). Reference them by path or URL instead.

If the user passed arguments, treat them as a description of what the next session will focus on and tailor the doc accordingly.

## Workflow

1. **Locate the file.** Run `mktemp -t handoff-XXXXXX.md` to get an absolute path. Read the file (it will be empty) before writing — required by the Write tool contract.
2. **Scan the conversation.** Pull out: the user's goal, decisions made, blockers hit, what's been tried, what's been *ruled out*, files touched, commands run, and any uncommitted state.
3. **Find the artifacts.** Note every PRD / plan / ADR / issue / commit / PR / diff / log produced this session. Reference them by absolute path or URL — never paste their content.
4. **Tailor to the focus.** If `$ARGUMENTS` describes what the next session will do, prune the doc to what *that* session needs. Drop history irrelevant to the next move.
5. **Suggest skills.** Recommend specific skills the next agent should invoke (e.g. `/tdd`, `/eng-spec`, `/repo-context-scan`). Only suggest skills you actually know exist in the user's environment.
6. **Write and print the path.** Save to the `mktemp` path. Print the path on its own line so the user can copy it.

## Document structure

Use these sections. Skip any that don't apply — empty sections are noise.

```markdown
# Handoff — <one-line title>

**Next session focus:** <from $ARGUMENTS, or "open">
**Created:** <YYYY-MM-DD HH:MM TZ>
**Working dir:** <cwd>
**Branch / worktree:** <branch> (clean | N uncommitted)

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
- **Don't commit the file.** `mktemp -t` puts it in the system temp dir on purpose. The user moves it if they want to keep it.

## When NOT to use

- Conversation is short and the next agent can read the transcript directly.
- A plan, PRD, or issue already captures the state — point at it instead.
- Mid-debugging on a single bug where transferring context costs more than just finishing it.
