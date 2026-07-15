# Handoff document template

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
