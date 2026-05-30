---
name: grill-me-auto
description: Use when the user wants a non-interactive Grill Me run written as one collapsible markdown document, asks for "Grill Me Auto", "auto grill", "all grill questions at once", or invokes /grill-me-auto, /Grill Me Auto, or /grill me auto.
---

# Grill Me Auto

Batch-mode fork of [`grill-me`](../grill-me/SKILL.md): same relentless stress test, but every question is written into one markdown grill document so the user can read, collapse/expand, and answer in one shot.

Use this skill for `/grill-me-auto`, `/Grill Me Auto`, `/grill me auto`, "auto grill", or requests for all grill questions at once. If the user wants a live one-question-at-a-time interview, redirect to `/grill-me`. If they want engineering-only grilling against `CONTEXT.md` / ADRs, redirect to `/domain-grill`.

## Step 0 — choose depth first

Ask before generating unless the invocation already includes a recognized depth.

> Grill depth? (default: **deep**)
>
> - **deep** — every branch, edge case, contradiction, code/doc cross-check, and invented boundary scenario. Typically 20–40+ questions.
> - **standard** — critical assumptions plus main edge cases and obvious cross-checks. Typically 15–25 questions.
> - **quick** — only highest-leverage deal-breakers and dead-on-arrival risks. Typically 5–10 questions.
>
> Reply with `deep` / `standard` / `quick` (or hit return for deep). You can pre-select with `/grill-me-auto deep`, `/grill-me-auto standard`, `/grill-me-auto quick`; aliases `3` / `2` / `1` and `deepest` / `medium` / `sharp` also work.

Echo pre-selected depth in one short line. If depth is ambiguous, ask this question and stop.

## Step 1 — gather context silently

Inspect the prompt, linked artifacts, touched files, repo instructions, `CONTEXT.md`, ADRs, docs, and recent commits before writing questions. Do not ask the user anything the agent can read. Mention blockers only if needed.

## Step 2 — write the grill document

Create the document at:

`.grills/<YYYY-MM-DD-HHMM>-<2-to-3-word-slug>-<depth>.md`

Rules:

- Resolve project root with `git rev-parse --show-toplevel`; fall back to an ancestor with `.git` / `.claude`, then `pwd`.
- Use local time for `YYYY-MM-DD-HHMM`; same-minute collisions get `-2`, `-3` suffixes.
- Derive the slug from the plan/topic being grilled.
- Create `.grills/` if missing. If it is not gitignored, append `/.grills/` to `.gitignore` and stage that one-line change; do not commit.
- Write atomically via temp file then rename.

Use the full format in [`REFERENCE.md`](./REFERENCE.md) and the filled example in [`templates/grill-doc.template.md`](./templates/grill-doc.template.md).

## Question format requirements

The document must preview cleanly in GitHub, GitLab, VS Code, Obsidian, and browser markdown renderers:

- Start with a numbered `## Questions` table of contents.
- Put each top-level question in its own `<details><summary><strong>N. Question?</strong></summary> ... </details>` block so users can collapse/expand by number.
- For every question include:
  - **Why it matters** — one line with the cost of getting it wrong.
  - **Options** — 2–4 mutually exclusive answers labelled `N.A`, `N.B`, `N.C`, `N.D`.
  - **Recommendation** — one option letter plus a reason.
  - **Alt** — a different second-best option plus reason, or `n/a` only when there is no defensible alternative.
- Nest conditional questions inside their parent details block as `2a`, `2b`, etc, with `Conditional on: <expr>`.
- Keep the answer key unambiguous: top-level questions use `1: A`; conditional questions use `2a: B` only when triggered.

## Required answer options at bottom

End every document with `## Answer key` and exactly these three user-friendly reply paths:

1. **Accept all my recommendations** — accept every primary recommendation. Canonical phrase: `accept all my recommendations`; alias: `ACCEPT_ALL_RECOMMENDATIONS`.
2. **Accept all my alt recommendations** — accept every alt recommendation; where Alt is `n/a`, fall back to the primary recommendation and flag it later. Canonical phrase: `accept all my alt recommendations`; alias: `ACCEPT_ALL_ALT_RECOMMENDATIONS`.
3. **Copy/paste this in the chat after reading it back to the agent** — a per-question block with one `N: ?` line per top-level question; users replace `?` with `A` / `B` / `C` / `D` / `rec` / `alt`.

## Step 3 — hand off and stop

After writing the file, reply only with:

> Grill written to `.grills/<filename>` — **<N>** questions at depth **<depth>**. Open it in a markdown previewer, then paste one of: `accept all my recommendations`, `accept all my alt recommendations`, or the filled answer-key block. I'll apply your answers in one pass when you reply.

Do not summarize the questions in chat. The document is the deliverable.

## Step 4 — when the user replies

Parse the shortcut or answer-key block in one pass. If malformed, ask one targeted fix-up question, not a new grill.

After parsing:

1. Update the grill document frontmatter to `status: answered`, append `answered_at`, and add `## Resolved answers` at the bottom.
2. Summarize the resolved plan in ≤10 bullets, flagging any answer that changed direction from the original prompt with `(changed:)`.
3. Ask before starting the next step; do not implement automatically.

---

_Forked from [`grill-me`](../grill-me/SKILL.md), itself a fork of Matt Pocock's [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md). Matt's relentless-interview core remains; this fork adds batch document delivery._
