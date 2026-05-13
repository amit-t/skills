---
name: resume
description: Pick up where a previous session left off by loading the newest open handoff document written by /handoff. Reads `.claude/handoffs/<timestamp>-<slug>.md` inside the project root, runs an environment preflight (branch, cwd, uncommitted state) against the handoff's frontmatter, then on user confirmation moves the file to `.claude/handoffs/resumed/` and proceeds with the first next-move. Triggers include "/resume", "resume the handoff", "continue from the last session", "pick up where we left off".
argument-hint: "list | <slug-substring> | <number>  (optional: select a non-newest handoff)"
---

# Resume

Discover and load the newest open handoff in the current project so a fresh session can continue prior work. This is the read side of the `/handoff` pair — never requires the user to remember or paste a file path.

## Workflow

1. **Resolve the project root.** Use the exact same resolution order as `/handoff`:
   1. `git rev-parse --show-toplevel 2>/dev/null` — if non-empty, that is the root.
   2. Else walk upward from `pwd` looking for the first ancestor that contains a `.claude/` directory.
   3. Else fall back to `pwd` itself and warn the user about non-discoverable state.
2. **Find open handoffs.** List `<root>/.claude/handoffs/*.md` at the **top level only** — do not recurse into `resumed/`. Sort by filename descending (filenames are `YYYY-MM-DD-HHMM-<slug>.md`, so lexical sort equals chronological sort).
3. **Handle the empty case.** If no top-level `.md` files exist, print exactly `No open handoffs in <root>/.claude/handoffs/.` and exit. Do not error.
4. **Handle the argument.**
   - **No argument** → target the newest (index 0).
   - **`list`** → print a numbered, oldest-first table: index, filename, `focus` from frontmatter (truncated to 60 chars), `created` timestamp. Then exit. Do not load anything.
   - **A number** (`/resume 2`) → target index N from the same table (`list` indexes).
   - **Any other string** → case-insensitive substring match against filenames. If exactly one match, target it; if zero, print "No match" and the list; if multiple, print the matches and exit.
5. **Read the target file.** Parse YAML frontmatter (`focus`, `created`, `cwd`, `project_root`, `branch`, `worktree`, `uncommitted_files`, `status`, `resumed_at`). Read the markdown body.
6. **Preflight check** vs current state. Compute deltas and surface them as warnings (do not block):
   - **Project root drift** — current `<root>` vs frontmatter `project_root`. If different, warn.
   - **cwd drift** — current `pwd` vs frontmatter `cwd`. If different, note it (often fine, just informational).
   - **Branch drift** — current `git rev-parse --abbrev-ref HEAD` vs frontmatter `branch`. If different, warn explicitly: `handoff written on <X>, you're on <Y>`. Offer to `git switch <X>` (do not run automatically).
   - **Uncommitted-state drift** — current `git status --porcelain | wc -l` vs frontmatter `uncommitted_files`. If higher, note it; if lower, note it (something landed since the handoff was written).
   - **Stale handoff** — if `(now - created) > 14 days`, prepend a clear stale warning to the summary: `⚠ written N days ago — may be stale`.
   - **Status sanity** — if `status` is not `open`, refuse to resume that file and explain (it has already been resumed, or the field was hand-edited). Suggest `/resume list`.
7. **Summarise.** Print:
   - Title and one-line goal from the body.
   - Preflight warnings, if any.
   - The full **Next moves** section verbatim.
   - The **Suggested skills for next session** list.
   - Count of other unresumed handoffs at top level (e.g. `2 older unresumed handoffs — /resume list to see them`). Skip the line if count is zero.
8. **Confirm with the user.** Ask exactly: `Resume this handoff? [Y/n]`. Treat empty input as Y.
9. **On Y:**
   - Ensure `<root>/.claude/handoffs/resumed/` exists (`mkdir -p`).
   - Generate the resumed-side filename: `<resume-ts>--<orig-basename>`, where `<resume-ts>` is `YYYY-MM-DD-HHMM` of *now*. Example: `2026-05-14-0902--2026-05-13-1830-land-migration-218.md`.
   - **Update frontmatter in place first**: set `status: resumed` and `resumed_at: <ISO-8601 now>`. Leave the rest unchanged.
   - **Then move** the file to `<root>/.claude/handoffs/resumed/<resumed-filename>` using `mv` (or rename) so the operation is atomic.
   - Print the new path on its own line.
   - Internalise the handoff content. Proceed with the first **Next moves** item. If the handoff names skills under **Suggested skills**, offer to invoke them; do not auto-invoke.
10. **On n:** leave the file in place with `status: open`. Print `Left as open. Run /resume list to see all handoffs.` and exit.

## Rules

- **Never auto-execute next-moves without user confirmation.** Preflight + summarise + confirm is the contract.
- **Never auto-switch branches, stash, or modify the working tree.** Surface the drift, let the user decide.
- **Never move a file before the user confirms.** A user who reads the summary and bails should find the handoff exactly where it was.
- **Never recurse into `resumed/`.** That directory is a history audit, not a queue.
- **Never write the resumed-side file before mutating the source.** Update frontmatter, then move. One file, one rename — no `cp`.
- **No emojis, no filler.** Operational tone only.

## Companion skill

`/handoff` is the write side. They share the project-root resolution rules and the `.claude/handoffs/` location convention. Install both:

```bash
npx skills@latest add amit-t/skills --skill handoff
npx skills@latest add amit-t/skills --skill resume
```

## When NOT to use

- The user is starting genuinely new work unrelated to any prior handoff.
- The handoff directory does not exist — there is nothing to resume.
- The user wants to *write* a handoff, not *read* one. Use `/handoff` instead.
