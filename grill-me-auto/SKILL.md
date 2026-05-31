---
name: grill-me-auto
description: Use when the user wants a non-interactive Grill Me run written as one collapsible markdown document, asks for "Grill Me Auto", "auto grill", "all grill questions at once", or invokes /grill-me-auto, /Grill Me Auto, or /grill me auto.
---

# Grill Me Auto

Batch-mode fork of [`grill-me`](../grill-me/SKILL.md): same relentless stress test, but every question is written into one markdown grill document so the user can read, collapse/expand, and answer in one shot.

Use this skill for `/grill-me-auto`, `/Grill Me Auto`, `/grill me auto`, "auto grill", or requests for all grill questions at once. If the user wants a live one-question-at-a-time interview, redirect to `/grill-me`. If they want engineering-only grilling against `CONTEXT.md` / ADRs, redirect to `/domain-grill`.

## Step 0 — choose depth first

If the invocation includes a recognized depth (see the table in [`REFERENCE.md`](./REFERENCE.md#invocation-and-depth) for accepted values and aliases), echo it in one line and proceed. Otherwise, ask exactly this and stop:

> Grill depth? (default: **deep**)
>
> - **deep** — every branch, edge case, contradiction, code/doc cross-check, and invented boundary scenario. Typically 20–40+ questions.
> - **standard** — critical assumptions plus main edge cases and obvious cross-checks. Typically 15–25 questions.
> - **quick** — only highest-leverage deal-breakers and dead-on-arrival risks. Typically 5–10 questions.
>
> Reply with `deep` / `standard` / `quick` (or hit return for deep). Pre-select next time with `/grill-me-auto deep|standard|quick`.

## Step 1 — gather context silently

Inspect the prompt, linked artifacts, touched files, repo instructions, `CONTEXT.md`, ADRs, docs, and recent commits before writing questions. Do not ask the user anything the agent can read. Mention blockers only if needed.

## Step 2 — write the grill document

Resolve the project root with `git rev-parse --show-toplevel`, falling back to an ancestor with `.git` / `.claude`, then `pwd`. Create the document atomically (`.tmp` then rename) at the path defined in [`REFERENCE.md` § File contract](./REFERENCE.md#file-contract). Create `.grills/` if missing; if it is not gitignored, append `/.grills/` to `.gitignore` and stage that one-line change (do not commit).

Follow [`REFERENCE.md`](./REFERENCE.md) for every format contract — file path, frontmatter, question block, answer key, reply parsing. [`templates/grill-doc.template.md`](./templates/grill-doc.template.md) is the only filled example; do not inline another one here or in `README.md`.

### Precision pass — apply before writing

Before serializing the document to disk, internally apply [`precision-mode`](../precision-mode/SKILL.md) to every authored string: question text, *Why it matters* lines, option labels, recommendation reasons, and alt reasons. The grill doc is the only deliverable, so density of the prose inside it is the deliverable.

Implicit invocation rules:

- If `precision-mode` is listed in the environment's available skills, invoke it before drafting question prose; if not, apply the same rules inline from memory (lead with the answer, no filler, no echo, no trailing summary, fragments over sentences when unambiguous, quantify don't qualify, prefer structure over prose).
- Apply precision **only to the authored content** of questions, options, recommendations, and alt reasons. Do **not** strip the literal markdown scaffolding the format contract requires: `<details>` / `<summary>` tags, the `**Why it matters:**` / `**Options:**` / `**Recommendation:**` / `**Alt:**` labels, the `## Questions` TOC heading, the `## Answer key` heading, frontmatter keys, or the three reply-path code blocks. Those are contract, not prose.
- Caps that override the precision instinct to compress further: `Why it matters` stays ≤1 sentence (≤20 words); option labels stay ≤15 words; recommendation and alt reasons stay ≤25 words. If a reason genuinely needs more, split into two sentences — do not drop the *why* to hit the cap.
- Preserve correctness and critical caveats. Precision must not strip a security warning, breaking-change flag, data-loss risk, or a specific code/ADR reference that gives the recommendation its grip.
- Never let precision delete the alt recommendation to "lead with the answer". The dual recommendation + alt structure is contract.

Briefly mention in the hand-off message (Step 3) that the doc was written under precision mode, so the user knows scannability is intentional and reasons are not truncated by accident.

## Step 3 — hand off and stop

After writing the file, reply only with:

> Grill written to `.grills/<filename>` — **<N>** questions at depth **<depth>**, written under precision mode (terse on purpose; reasons capped, not truncated). Open it in a markdown previewer, then paste one of: `accept all my recommendations`, `accept all my alt recommendations`, or the filled answer-key block. I'll apply your answers in one pass when you reply.

Do not summarize the questions in chat. The document is the deliverable.

## Step 4 — when the user replies

Parse the shortcut or answer-key block in one pass. If malformed, ask one targeted fix-up question, not a new grill.

After parsing:

1. Update the grill document frontmatter to `status: answered`, append `answered_at`, and add `## Resolved answers` at the bottom.
2. Summarize the resolved plan in ≤10 bullets, flagging any answer that changed direction from the original prompt with `(changed:)`.
3. Ask before starting the next step; do not implement automatically.

---

_Forked from [`grill-me`](../grill-me/SKILL.md), itself a fork of Matt Pocock's [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md). Matt's relentless-interview core remains; this fork adds batch document delivery._
