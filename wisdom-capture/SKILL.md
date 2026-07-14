---
name: wisdom-capture
description: Record a wisdom snippet — quote, idea, or observation worth keeping — into the user's personal corpus. Categorizes into a closed bucket from wisdoms/_categories.yml, writes a frontmatter Markdown file, and commits. Captures from terminal CLI (`wisdom`) or in-session slash command (`/wisdom` / `$wisdom`).
---

# Wisdom Capture

## Overview

The corpus lives at `$WISDOM_REPO` (default `~/Projects/AmitTiwari/wisdom`).
Each snippet becomes one Markdown file under `wisdoms/<YYYY>/<MM>/<ulid>.md`
with strict frontmatter, then one git commit.

Follow the 10-step flow below in order, applying the schema exactly as
written. If you cannot proceed for any reason, surface the problem to the
user explicitly — never save partial data silently.

## Inputs

You receive the snippet via one of:
- A first user-turn message containing `Record this wisdom snippet: <body>`
- An interactive prompt where the user types `/wisdom` (Claude/Devin) or
  `$wisdom` (Codex) and then pastes the snippet
- Inside the URL-import flow (Phase 3), a pre-assembled preview with caption,
  transcript, and images

You MUST `cd` into the repo before any git operation:
`cd "$WISDOM_REPO"` (or the value from `wisdom_repo_path`).

## The 10-step flow

### Step 1 — Detect inputs

If the first turn already has a snippet, use it. Otherwise ask:
"Paste your wisdom snippet."

### Step 2 — Enrich (best-effort)

If the snippet contains a URL, attempt to fetch the page title and author
using your available web tools. Skip on failure. Ask the user explicitly for
`source_url` and `source_author` only if neither is derivable.

### Step 3 — Strip / clean

Trim leading and trailing whitespace. Preserve internal Markdown formatting
and the snippet's prose exactly as written.

### Step 4 — Propose category + tags

Read `wisdoms/_categories.yml`. Decide:

- **Primary bucket** — exactly one key from the file
- **Confidence** — `high` | `med` | `low`
- **Tags** — 2–5 lowercase hyphenated strings
- **If no bucket fits** — propose a new bucket with `key`, `label`, `color`
  (pick from `color_pool`), and a one-sentence reason. ALSO provide
  `second_best` — the closest existing bucket.

### Step 5 — Confirm with user

Show the proposal as a compact table. Options: `[y] accept`, `[n] reject`,
`[edit] adjust tags/note inline`.

### Step 6 — Ask for personal note (optional)

"Want to add your own gloss? (enter to skip)"

### Step 7 — Write file

- Compute `id = ulid` (lowercase 26-char Crockford base32)
- Compute `body_hash = sha256(normalize(body))`
- Set `created_at = now in ISO 8601 UTC`
- Choose path `wisdoms/<YYYY>/<MM>/<id>.md`
- Render frontmatter exactly per the rendering rules in REFERENCE.md.

### Step 8 — Commit

```bash
git status --porcelain
git add wisdoms/<YYYY>/<MM>/<id>.md
git commit -m "wisdom: <category> — <body first 60 chars>…

source: <url if present>
tags: <comma list>"
```

### Step 9 — Push (per session)

Read `.wisdom-session` if present. Honor `always` / `never`. Otherwise prompt.
Persist choice to `.wisdom-session` (gitignored).

### Step 10 — Report + loop

Print file path, category + tags, commit sha, Pages URL if push happened.

## Edge cases

### Dedup hit

Before Step 7, check `wisdom_find_dup "$body" "$WISDOM_REPO"`. If non-empty,
prompt the user with skip/add/merge/cancel options.

### Length guard

Body length < 20 chars → reject. Length > 5000 → warn but continue.

### URL import (Phase 3)

When invoked from `wisdom import-url`, the user's first turn is a preview
bundle assembled by the CLI from cached scrape artifacts — see
[`URL-IMPORT.md`](URL-IMPORT.md) for the bundle format, vision handling, and
the 7-step extraction + curation flow.

### No-categories.yml

If `wisdoms/_categories.yml` is missing or unparseable, halt with error. Do
not invent buckets.

## Verification before declaring done

- File written under `wisdoms/<YYYY>/<MM>/<id>.md`
- Frontmatter parses as valid YAML
- `id` matches filename
- `body_hash` matches `sha256(normalize(body))`
- Commit landed on local `main`

See REFERENCE.md for the categorization output schema, frontmatter rendering
rules, and engine-specific notes.
