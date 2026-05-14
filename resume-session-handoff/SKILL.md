---
name: resume-session-handoff
description: Pick up where a previous session left off by loading the newest open handoff document written by /session-handoff. Reads `.claude/handoffs/<timestamp>-<slug>.md` inside the project root, runs an environment preflight (branch, cwd, uncommitted state) against the handoff's frontmatter, then on user confirmation moves the file to `.claude/handoffs/resumed/`, internalises the content, and **asks the user what to do next** — never auto-executes. Triggers include "/resume-session-handoff", "resume the session handoff", "load the handoff", "continue from the last session", "pick up where we left off". Named `resume-session-handoff` (not `/resume` or `/resume-handoff`) because most agents already ship a built-in `/resume` that restores the prior conversation and Devin already ships a built-in `/handoff`; both would shadow shorter names.
argument-hint: "list | <slug-substring> | <number>  (optional: select a non-newest handoff)"
---

# Resume Session Handoff

Discover and load the newest open handoff in the current project so a fresh session can continue prior work. This is the read side of the `/session-handoff` pair — never requires the user to remember or paste a file path.

**Why the name is `resume-session-handoff`.** Two collisions to avoid: (1) most agents (Claude Code, Codex, others) reserve `/resume` for their built-in "restore the previous conversation" command; (2) Devin reserves `/handoff` for its own session-transfer flow. So neither `/resume` nor `/resume-handoff` is safe across environments. `/resume-session-handoff` is unambiguous: it always means *load the handoff document written by `/session-handoff`*.

## Workflow

1. **Bootstrap superpowers, if available.** If the platform exposes a skill named `using-superpowers` (or `superpowers:using-superpowers`), invoke it via the platform's skill mechanism (`Skill` in Claude Code, `skill` in Copilot CLI, `activate_skill` in Gemini CLI) **before** any other step. This ensures the process discipline (brainstorming, plan, TDD, verification) is loaded before the next move is chosen. If the skill is not listed in the environment, skip this step silently — do not guess at a path, do not error.
2. **Resolve the project root.** Use the exact same resolution order as `/session-handoff`:
   1. `git rev-parse --show-toplevel 2>/dev/null` — if non-empty, that is the root.
   2. Else walk upward from `pwd` looking for the first ancestor that contains a `.claude/` directory.
   3. Else fall back to `pwd` itself and warn the user about non-discoverable state.
3. **Find open handoffs.** List `<root>/.claude/handoffs/*.md` at the **top level only** — do not recurse into `resumed/`. Sort by filename descending (filenames are `YYYY-MM-DD-HHMM-<slug>.md`, so lexical sort equals chronological sort).
4. **Handle the empty case.** If no top-level `.md` files exist, print exactly `No open handoffs in <root>/.claude/handoffs/.` and exit. Do not error.
5. **Handle the argument.**
   - **No argument** → target the newest (index 0).
   - **`list`** → print a numbered, oldest-first table: index, filename, `focus` from frontmatter (truncated to 60 chars), `created` timestamp. Then exit. Do not load anything.
   - **A number** (`/resume-session-handoff 2`) → target index N from the same table (`list` indexes).
   - **Any other string** → case-insensitive substring match against filenames. If exactly one match, target it; if zero, print "No match" and the list; if multiple, print the matches and exit.
6. **Read the target file.** Parse YAML frontmatter (`focus`, `created`, `cwd`, `project_root`, `branch`, `worktree`, `uncommitted_files`, `status`, `resumed_at`). Read the markdown body.
7. **Preflight check** vs current state. Compute deltas and surface them as warnings (do not block):
   - **Project root drift** — current `<root>` vs frontmatter `project_root`. If different, warn.
   - **cwd drift** — current `pwd` vs frontmatter `cwd`. If different, note it (often fine, just informational).
   - **Branch drift** — current `git rev-parse --abbrev-ref HEAD` vs frontmatter `branch`. If different, warn explicitly: `handoff written on <X>, you're on <Y>`. Offer to `git switch <X>` (do not run automatically).
   - **Uncommitted-state drift** — current `git status --porcelain | wc -l` vs frontmatter `uncommitted_files`. If higher, note it; if lower, note it (something landed since the handoff was written).
   - **Stale handoff** — if `(now - created) > 14 days`, prepend a clear stale warning to the summary: `⚠ written N days ago — may be stale`.
   - **Status sanity** — if `status` is not `open`, refuse to resume that file and explain (it has already been resumed, or the field was hand-edited). Suggest `/resume-session-handoff list`.
8. **Summarise.** Print:
   - Title and one-line goal from the body.
   - Preflight warnings, if any.
   - The full **Next moves** section verbatim.
   - The **Suggested skills for next session** list.
   - Count of other unresumed handoffs at top level (e.g. `2 older unresumed handoffs — /resume-session-handoff list to see them`). Skip the line if count is zero.
9. **Confirm resume.** Ask exactly: `Resume this handoff? [Y/n]`. Treat empty input as Y.
10. **On Y — create state, then stop.**
    - Ensure `<root>/.claude/handoffs/resumed/` exists (`mkdir -p`).
    - Generate the resumed-side filename: `<resume-ts>--<orig-basename>`, where `<resume-ts>` is `YYYY-MM-DD-HHMM` of *now*. Example: `2026-05-14-0902--2026-05-13-1830-land-migration-218.md`.
    - **Update frontmatter in place first**: set `status: resumed` and `resumed_at: <ISO-8601 now>`. Leave the rest unchanged.
    - **Then move** the file to `<root>/.claude/handoffs/resumed/<resumed-filename>` using `mv` (or rename) so the operation is atomic.
    - Print the new path on its own line.
    - **Internalise the handoff content.** Read the body fully into working memory — you'll need every section (goal, state, decisions, ruled-out, blockers, artifacts, next moves, suggested skills, environment notes) to answer the user's next question. Do **not** start any tool calls beyond reads.
    - **Ask what to do next. Do not auto-execute.** Present a short menu derived from the handoff and wait for the user to choose. Format:
      ```
      State loaded from <orig-basename>. Where would you like to start?

      Next moves from the handoff:
        1. <first Next moves item>
        2. <second Next moves item>
        3. <…>

      Suggested skills:
        - /<skill-a> — <why it fits>
        - /<skill-b> — <why it fits>

      Other options:
        - Walk me through your understanding of the state before we pick.
        - Re-scope or replace the next moves with something different.
        - Show me the full handoff body.
        - Hold here — I'll tell you what to do.
      ```
      Then stop and wait. Do not invoke any tool that mutates state (no edits, no shell side-effects, no skill invocations beyond `using-superpowers` from step 1) until the user picks a direction. Read-only inspections requested by the user (e.g. "show me the full handoff body") are fine.
11. **On n:** leave the file in place with `status: open`. Print `Left as open. Run /resume-session-handoff list to see all handoffs.` and exit.

## Rules

- **Never auto-execute next moves.** Loading the handoff and updating state is the contract; choosing a direction is the user's call. Even an "obvious" first step is not invoked without explicit instruction.
- **Never auto-switch branches, stash, or modify the working tree** during preflight. Surface the drift, let the user decide.
- **Never move the handoff file before the user confirms.** A user who reads the summary and bails should find the handoff exactly where it was.
- **Never recurse into `resumed/`.** That directory is a history audit, not a queue.
- **Never write the resumed-side file before mutating the source.** Update frontmatter, then move. One file, one rename — no `cp`.
- **Superpowers is opt-in by availability.** Invoke `using-superpowers` only if the environment lists it as an available skill. Never fabricate a skill path; never fall back to "remembering" what superpowers said.
- **No emojis, no filler.** Operational tone only.

## Companion skill

`/session-handoff` is the write side. They share the project-root resolution rules and the `.claude/handoffs/` location convention. Install both:

```bash
npx skills@latest add amit-t/skills --skill session-handoff
npx skills@latest add amit-t/skills --skill resume-session-handoff
```

## When NOT to use

- The user is starting genuinely new work unrelated to any prior handoff.
- The handoff directory does not exist — there is nothing to resume.
- The user wants to *write* a handoff, not *read* one. Use `/session-handoff` instead.
- The user invoked the agent's built-in `/resume` (restore previous conversation). That is a different operation; this skill loads the handoff *document*, not the prior chat transcript.
