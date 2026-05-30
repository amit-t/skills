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

Use [`REFERENCE.md`](./REFERENCE.md) as the canonical contract and [`templates/grill-doc.template.md`](./templates/grill-doc.template.md) as the only filled example.

## Document contract

The generated file must include:

- A numbered `## Questions` table of contents.
- One collapsible `<details><summary><strong>N. Question?</strong></summary>` block per top-level question.
- For every question: **Why it matters**, 2–4 labelled options (`N.A`, `N.B`, ...), **Recommendation**, and **Alt**.
- Nested conditional questions inside their parent block (`2a`, `2b`, ...), never as stray top-level questions.
- `## Answer key` with exactly the three reply paths: **Accept all my recommendations**, **Accept all my alt recommendations**, and **Copy/paste this in the chat after reading it back to the agent**.

Do not duplicate the filled example in this file; use the reference/template links above.

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
