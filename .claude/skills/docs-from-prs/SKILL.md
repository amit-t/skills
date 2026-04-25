---
name: docs-from-prs
description: Survey recent merged PRs/commits, find what is not yet documented in README and other user-facing docs, and update those docs with thoughtful section placement. Always re-checks the project's drift hot spots (alias tables, CLI flag references, config examples). Trigger when the user says "update docs from PRs", "doc the recent changes", "/docs-from-prs", or asks to bring docs in sync with merged work.
---

# docs-from-prs

Survey merged PRs since the last docs update, decide which are user-facing, place each into the right doc section, and commit. Always re-check the project's drift hot spots (e.g. CLI flag tables, alias lists, env-var examples).

## Inputs

Optional args (free-form, parse from the user's message):

- **since**: a date (`2026-04-01`), a PR number (`#24`), or a count (`last 15`). Default: PRs merged after the most recent commit that touched the primary doc (`README.md` by default), capped at 20.
- **remotes**: `origin` or a named remote, or `all` if the project mirrors to multiple GitHub orgs. Default: the current repo's `origin`. Multi-remote projects should follow their `CLAUDE.md` / `AGENTS.md` PR workflow.
- **dry-run**: report the gap analysis only, no edits. Use when the user says "what's missing" or "audit".

## Step 1 — Survey

Resolve the current repo first:

```bash
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
```

Then run these in parallel:

```bash
# Recent merged PRs
gh pr list --repo "$REPO" --state merged --limit 20 \
  --json number,title,mergedAt,body,files

# Last commit that meaningfully touched the primary docs
git log -1 --format='%H %ad' --date=short -- README.md

# Recent commits for context
git log --oneline --since="<derived date>" | head -40
```

If `gh pr list` 404s, the wrong `gh` account is active — switch with `gh auth switch --user <handle>`. The project's `CLAUDE.md` or `AGENTS.md` should name the handle for each remote.

## Step 2 — Classify each PR

For each PR, decide one of:

- **user-facing — flag/CLI/alias** → CLI reference + alias/command table + changelog + user guide
- **user-facing — config/env** → config example block + user guide config section
- **user-facing — behaviour/fix** → "Recent Changes" + changelog detail entry + (optional) "How it works" subsection
- **internal chore** → skip (CI tweaks, refactors, dependency bumps, agent config moves)
- **already covered** → skip (verify with `grep` against current docs before skipping)

Read the actual source — don't trust PR titles alone. Use `git show <sha> --stat` and inspect:

- New flags: command-entry scripts / CLI parser modules
- New aliases or shortcuts: any `aliases.sh`, shell wrappers, `package.json` scripts, `Justfile`, `Makefile`
- New config: `.<tool>rc` files, env-var loader modules, schema definitions
- New subcommands or modes: dispatcher / router / main entry point

## Step 3 — Drift hot spot audit (mandatory, every run)

Most projects have one or two surfaces that drift faster than the rest — alias tables, CLI flag matrices, env-var lists, supported-version tables. Identify these in the project's docs and audit them every run, even if no PR explicitly touches them.

A reasonable audit pass:

1. Enumerate the source of truth (`grep -nE '^(alias |[A-Za-z_]+\(\) \{$)' aliases.sh`, `--help` output, schema file, `package.json` scripts, etc.).
2. Cross-check each entry against the doc tables. New entries → add a row. Renamed/removed → fix or delete.
3. Spot-check the variants that historically drift first. If the project's `CLAUDE.md` / `AGENTS.md` names the hot spots, treat that list as authoritative; otherwise ask the user which surfaces tend to drift.

Drift accumulates from minor commits. Run this audit even when the survey returns zero PRs.

## Step 4 — Section placement

Don't dump everything into "Recent Changes". Place thoughtfully:

| Change type         | Primary reference (e.g. README)                                       | Landing page / site                                | User guide                        |
|---------------------|-----------------------------------------------------------------------|----------------------------------------------------|-----------------------------------|
| New CLI flag        | Options reference for that command + feature bullet                   | changelog entry + detail panel                     | command page or advanced features |
| New alias           | alias table                                                            | (changelog if notable)                             | quick reference                   |
| Config var          | config example block + "How it works"                                 | changelog detail panel                             | config page                       |
| Bug fix (visible)   | "Recent Changes" + "How it works" subsection if it explains the model | changelog detail panel                             | brief mention                     |
| Bug fix (silent)    | "Recent Changes" only                                                  | changelog entry                                    | skip                              |
| New mode/subcommand | feature bullets + dedicated section + Quick Start sample              | changelog detail panel + feature card if prominent | new page or expanded section      |

Identify the project's actual doc layout before placing. Common layouts:

- **Single-file** (`README.md` only) — collapse columns 2 and 3 into the README.
- **README + landing page** (`docs/index.html`, `index.html`, GitHub Pages site) — landing pages often carry a JS-driven changelog or detail panel; check for a `CHANGE_DETAILS` / `changelog` map and **shift numeric keys** when inserting items at the top.
- **README + user guide** (`docs/`, `wiki/`, `book/`) — multiple pages; put narrative explanation in the guide, terse reference in the README.
- **README + site + user guide** — apply the full matrix above.

Out-of-scope directories vary — check the project's `CLAUDE.md` / `AGENTS.md` for "never edit" lists (commonly `docs/archive/`, `docs/generated/`, `docs/code-review/`, vendored docs).

## Step 5 — Edits

- Additive by default. Don't rewrite working prose.
- Match surrounding voice and emoji policy (some pages use emojis, others don't — stay consistent within each file).
- Read every file before editing; for large reference files (>30KB) use `grep -n` to find anchors instead of full reads.
- Verify HTML stays well-formed after editing (tag balance + any JS-driven detail map).
- Do not regenerate generated artefacts (e.g. `graphify-out/`, autogenerated API docs, build outputs).

## Step 6 — Copy-edit pass (mandatory, after content edits, before commit)

After all content additions are in place, do a grammar/style/alignment pass over **only the files you touched this run** (don't churn unrelated prose).

### Grammar and prose

- Subject-verb agreement, article use (a/an/the), pluralization, tense consistency.
- No double spaces, no trailing whitespace, no smart quotes mixed with straight quotes.
- Oxford comma when a list has three or more items, matching the rest of the doc.
- Active voice where the surrounding doc uses active voice; don't flip an existing passive section.
- Hyphenation: `command-line` (adj), `command line` (noun); `multi-repo`, `cross-repo`, `worktree` (one word). Treat literal filenames as inviolable tokens — never reflow them across a line.
- Code identifiers, flags, env vars, file paths in backticks.

### Title casing

Match the dominant casing of the file you are editing:

- **Sentence case** (`## How it works`) — most modern READMEs and Markdown user guides.
- **Title case** (`## How It Works`) — many landing-page `<h1>`/`<h2>` headings, some legacy READMEs.

Do NOT normalize across the whole doc — match the immediate neighbourhood. When in doubt, run `grep -E '^#{1,4} ' <file> | head -30` and copy the dominant pattern.

Other casing rules:

- **Table column headers**: sentence case unless the column is a single proper-noun token.
- **Inline emphasis labels** (`**Why:**`, `**How to apply:**`): keep the exact casing already established.
- **Proper nouns always capitalized**: project names, language names, GitHub, CLI, README, etc.

### Alignment and layout

- **Markdown tables**: re-align pipes after edits. Every column's pipe must line up; pad with spaces. Header separator row matches column widths.
  ```
  | Column A | Column B     | Column C |
  |----------|--------------|----------|
  | value    | longer value | x        |
  ```
- **Lists**: consistent bullet character (`-` not `*` if the file uses `-`); two-space indent for nested lists; blank line before and after a list block.
- **Code fences**: language tag on every fence (` ```bash `, ` ```html `, ` ```text ` for plain). No bare ` ``` ` if the rest of the file tags them.
- **Blank lines**: exactly one blank line between sections; no triple-blank gaps; file ends with a single trailing newline.
- **Line length**: don't hard-wrap prose paragraphs unless the file already hard-wraps. Don't reflow existing paragraphs you didn't otherwise edit.

### HTML-specific (when editing landing pages)

- Tag balance: every `<li>`, `<div>`, `<section>` you opened is closed. Verify with `grep -c '<li>' <file>` vs `grep -c '</li>' <file>`.
- Indentation: match the surrounding 2-space or 4-space style — don't introduce a new style.
- JS-driven changelog maps (e.g. `CHANGE_DETAILS['latest']`): keys are sequential integers. After inserting items at top, **every** existing key must shift by the count of inserted items. Verify by counting `<li>` items vs object keys.

### Verification commands

Run these after the edit pass:

```bash
# Trailing whitespace / mid-line double spaces
grep -nE ' +$' <files-you-touched>
grep -nE '  +[^ ]' <files-you-touched>

# Heading casing audit (skim output, don't blindly fix)
grep -nE '^#{1,4} ' <files-you-touched>

# HTML tag balance for changelog
grep -c '<li>' <html-file>
grep -c '</li>' <html-file>
```

If any check surfaces drift introduced by **this run**, fix it. If the drift predates this run, note it in the report but don't fix it (out of scope — separate cleanup PR).

## Step 7 — Commit, branch, PRs

Branch name pattern: `docs/update-recent-prs` (or `docs/update-<topic>` if the survey covers a single theme).

```bash
git checkout -b docs/update-recent-prs
git add <doc-files>
git commit -m "docs: cover recent PRs (#X-#Y)"
```

PR creation:

- Default: one PR to the project's primary base branch (`main` or `dev`, per project convention).
- Multi-remote projects (mirrored to several GitHub orgs): follow the project's `CLAUDE.md` / `AGENTS.md` PR workflow. Switch `gh` accounts between remotes with `gh auth switch --user <handle>`.
- Use absolute paths with `git -C <worktree-path>` if running from a worktree.

## Step 8 — Report

Return a structured summary:

- Branch name, commit SHA
- Files changed (bulleted)
- One line per PR: gap-filled / already-covered / skipped (with reason)
- Drift hot spot audit result: rows added / corrected / clean
- PR URLs if created
- Copy-edit pass: items fixed (grammar, casing, alignment) vs items flagged as pre-existing drift
- Any factual mismatches discovered between docs and source (these are bugs, flag them even if out of scope)

## Constraints

- Never push without confirming. Default is push branch + open PR(s); destructive force-push or rewriting history requires explicit user ask.
- Never edit out-of-scope directories. Check `CLAUDE.md` / `AGENTS.md` for the project's "never edit" list — typical entries: `docs/archive/`, `docs/generated/`, `docs/code-review/`, vendored docs.
- Never invent flags or aliases — read the code.
- If a PR's claimed feature can't be found in the source, surface it in the report rather than documenting a ghost feature.
