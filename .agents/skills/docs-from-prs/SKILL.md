---
name: docs-from-prs
description: Survey recent merged PRs/commits, find what is not yet documented in README.md / docs/index.html / docs/user-guide/, and update those docs with thoughtful section placement. Always re-checks the alias tables. Project-local skill for ai-ralph. Trigger when the user says "update docs from PRs", "doc the recent changes", "/docs-from-prs", or asks to bring README/landing page in sync with merged work.
---

# docs-from-prs

Survey merged PRs since the last docs update, decide which are user-facing, place each into the right doc section, and commit. Always re-check the aliases table.

## Inputs

Optional args (free-form, parse from the user's message):

- **since**: a date (`2026-04-01`), a PR number (`#24`), or a count (`last 15`). Default: PRs merged after the most recent commit that touched `README.md`, capped at 20.
- **remotes**: `origin`, `inv`, or `both`. Default: `origin` (`amit-t/ai-ralph`). When the user says "both remotes" follow `CLAUDE.md`'s 4-PR workflow.
- **dry-run**: just report the gap analysis, no edits. Use when the user says "what's missing" or "audit".

## Step 1 — Survey

Run these in parallel:

```bash
# Recent merged PRs (use the right account — amit-t for origin, amit-tiwari_vnt for inv)
gh pr list --repo amit-t/ai-ralph --state merged --limit 20 \
  --json number,title,mergedAt,body,files

# Last commit that meaningfully touched README
git log -1 --format='%H %ad' --date=short -- README.md

# Recent commits for context
git log --oneline --since="<derived date>" | head -40
```

If `gh pr list` 404s on the ICS remote, switch accounts: `gh auth switch --user amit-tiwari_vnt`.

## Step 2 — Classify each PR

For each PR, decide one of:

- **user-facing — flag/CLI/alias** → README CLI reference + alias table + landing page changelog + user guide
- **user-facing — config/env** → README `.ralphrc` examples + user guide config section
- **user-facing — behaviour/fix** → README "Recent Changes" + landing page changelog detail panel + (optional) How It Works subsection
- **internal chore** → skip (CI tweaks, refactors, dependency bumps, agent config moves)
- **already covered** → skip (verify with `grep` against current docs before skipping)

Read the actual source — don't trust PR titles alone:

- New flags: `ralph_plan.sh`, `ralph_loop.sh`, `ralph_enable.sh`
- New aliases: `ALIASES.sh`
- Workspace internals: `lib/workspace*.sh`
- Engine wiring: `lib/claude.sh`, `lib/codex.sh`, `lib/devin.sh`

## Step 3 — Aliases table audit (mandatory, every run)

The README has three engine alias tables (Claude / Codex / Devin) and a Common Loop Options block. **Every run** of this skill must:

1. `grep -nE '^(alias |[A-Za-z_]+\(\) \{$)' ALIASES.sh | head -80` to enumerate current aliases.
2. Cross-check each alias against the README tables. New aliases → add a row. Renamed/removed → fix or delete.
3. Spot-check `.qg`, `.p`, `.live`, `.b` variants — these tend to drift first.
4. If `ALIASES.sh` defines functions (not just aliases), check those are documented too.

Even if no PR touched aliases, do this audit. Drift accumulates from minor commits.

## Step 4 — Section placement

Don't dump everything into "Recent Changes". Place thoughtfully:

| Change type | README section | docs/index.html | docs/user-guide |
|---|---|---|---|
| New CLI flag | Options reference for that command + feature bullet | changelog `<li>` + detail panel | command page or advanced-features |
| New alias | engine alias table | (changelog if notable) | Quick Reference |
| Config var | `.ralphrc` example block + How It Works | changelog detail panel | config page |
| Bug fix (visible) | "Recent Changes" + How It Works subsection if it explains the model | changelog detail panel | brief mention |
| Bug fix (silent) | "Recent Changes" only | changelog `<li>` | skip |
| New mode/subcommand | feature bullets + dedicated section + Quick Start sample | changelog detail panel + landing-page feature card if prominent | new page or expanded section |

Existing pages to know about:
- `README.md` — main reference
- `docs/index.html` — landing page; changelog uses an `<li>` list with a JS `CHANGE_DETAILS['latest']` map for detail panels. **When inserting items at the top, all existing numeric keys in `CHANGE_DETAILS` must shift accordingly.** Re-verify the mapping after editing.
- `docs/user-guide/README.md` — index/quick reference
- `docs/user-guide/0[1-4]-*.md` — pages
- **Out of scope, never edit:** `docs/archive/`, `docs/code-review/`, `docs/generated/`, `docs/superpowers/`

## Step 5 — Edits

- Additive by default. Don't rewrite working prose.
- Match surrounding voice and emoji policy (the existing landing page uses some, the user guide is sparser).
- Read every file before editing; the README is ~56KB so use `grep -n` to find anchors instead of full reads.
- Verify HTML stays well-formed after editing `index.html` (tag balance + the JS `CHANGE_DETAILS` map).
- Do not regenerate `graphify-out/`.

## Step 6 — Copy-edit pass (mandatory, after content edits, before commit)

After all content additions are in place, do a grammar/style/alignment pass over **only the files you touched this run** (don't churn unrelated prose).

### Grammar and prose

- Subject-verb agreement, article use (a/an/the), pluralization, tense consistency.
- No double spaces, no trailing whitespace, no smart quotes mixed with straight quotes.
- Oxford comma when a list has three or more items, matching the rest of the doc.
- Active voice where the surrounding doc uses active voice; don't flip an existing passive section.
- Hyphenation: `command-line` (adj), `command line` (noun); `multi-repo`, `cross-repo`, `worktree` (one word), `fix_plan.md` (literal filename, never reflowed).
- Code identifiers, flags, env vars, file paths in backticks. Flags like `--workspace`, env vars like `WORKTREE_GATE_TIMEOUT`, paths like `lib/workspace_plan.sh`.

### Title casing

The repo's convention (sample: existing README headings):

- **H1 / H2 / H3 headings**: **sentence case** — capitalize only the first word and proper nouns. Examples: `## How it works`, `### Parallel-safe fix_plan.md merge`. Do NOT title-case (`## How It Works`) unless an entire neighbouring section already uses title case — match the surrounding style rather than enforcing a global rule.
- **Table column headers**: sentence case unless the column is a single proper-noun token (`Remote`, `Repo slug`, `gh account`).
- **Inline emphasis labels** (`**Why:**`, `**How to apply:**`): keep the exact casing already established in `CLAUDE.md`/`AGENTS.md` style.
- **Proper nouns always capitalized**: Claude, Codex, Devin, GitHub, Ralph, README, CLI.
- **`docs/index.html` titles**: match whatever casing the existing `<h1>`/`<h2>`/changelog `<li>` strings use — that page leans toward title case for major headings, sentence case for changelog entries. Don't unify; preserve.

When in doubt, run `grep -E '^#{1,4} ' README.md | head -30` and copy the dominant pattern.

### Alignment and layout

- **Markdown tables**: re-align pipes after edits. Every column's pipe must line up; pad with spaces. Header separator row matches column widths.
  ```
  | Remote   | URL                 | gh account |
  |----------|---------------------|------------|
  | origin   | github.com-at:...   | amit-t     |
  ```
- **Lists**: consistent bullet character (`-` not `*` if the file uses `-`); two-space indent for nested lists; blank line before and after a list block.
- **Code fences**: language tag on every fence (` ```bash `, ` ```html `, ` ```text ` for plain). No bare ` ``` ` if the rest of the file tags them.
- **Blank lines**: exactly one blank line between sections; no triple-blank gaps; file ends with a single trailing newline.
- **Line length**: don't hard-wrap prose paragraphs (this repo uses soft-wrap). Don't reflow existing paragraphs you didn't otherwise edit.

### HTML-specific (`docs/index.html`)

- Tag balance: every `<li>`, `<div>`, `<section>` you opened is closed. After editing, run `python3 -c "import html.parser as h, sys; ..."` or simpler: `grep -c '<li>' docs/index.html` and `grep -c '</li>' docs/index.html` should match.
- Indentation: match the surrounding 2-space or 4-space indent already in the file — don't introduce a new style.
- The `CHANGE_DETAILS['latest']` map: keys are sequential integers. After inserting items at top, **every** existing key must be incremented by the count of inserted items. Verify by counting `<li>` items vs object keys.

### Verification commands

Run these after the edit pass:

```bash
# Trailing whitespace / double spaces
grep -nE ' +$' README.md docs/index.html docs/user-guide/*.md
grep -nE '  +[^ ]' README.md docs/user-guide/*.md  # mid-line double space (excludes indents)

# Heading casing audit (skim output, don't blindly fix)
grep -nE '^#{1,4} ' README.md docs/user-guide/*.md

# HTML tag balance for changelog
grep -c '<li>' docs/index.html
grep -c '</li>' docs/index.html

# CHANGE_DETAILS key vs <li> count parity
```

If any check surfaces drift introduced by **this run**, fix it. If the drift predates this run, note it in the report but don't fix it (out of scope — separate cleanup PR).

## Step 7 — Commit, branch, PRs

Branch name pattern: `docs/update-recent-prs` (or `docs/update-<topic>` if the survey covers a single theme).

```bash
git checkout -b docs/update-recent-prs
git add README.md docs/index.html docs/user-guide/
git commit -m "docs: cover recent PRs (#X-#Y) in README, landing page, user guide"
```

PR creation follows `CLAUDE.md` rules:

- Default: one PR to `amit-t/ai-ralph:main`
- "Both remotes" / "main and dev on both": 4 PRs (`origin/main`, `origin/dev`, `inv/main`, `inv/dev`). Switch `gh` accounts between remotes.
- Use absolute paths with `git -C <worktree-path>` if running from a worktree.

## Step 8 — Report

Return a structured summary:

- Branch name, commit SHA
- Files changed (bulleted)
- One line per PR: gap-filled / already-covered / skipped (with reason)
- Aliases-table audit result: rows added / corrected / clean
- PR URLs if created
- Copy-edit pass: items fixed (grammar, casing, alignment) vs items flagged as pre-existing drift
- Any factual mismatches discovered between docs and source (these are bugs, flag them even if out of scope)

## Constraints

- Never push without confirming. Default is push branch + open PR(s); destructive force-push or rewriting history requires explicit user ask.
- Never edit `docs/archive/`, `docs/code-review/`, `docs/generated/`, `docs/superpowers/`.
- Never invent flags or aliases — read the code.
- If a PR's claimed feature can't be found in the source, surface it in the report rather than documenting a ghost feature.
