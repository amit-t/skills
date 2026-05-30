---
name: grill-me-auto
description: Batch-mode fork of grill-me. Asks for grill depth (quick / standard / deep, default deep), then dumps ALL questions, options, recommendations, and alt recommendations into a single hierarchical, collapsible markdown grill document at `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`. User reads the doc once, fills the answer key at the bottom (or pastes one of the three batch shortcuts), and replies in one shot — no back-and-forth Q&A. Use when the user wants the full grill in writing instead of an interactive interview, or types `/grill-me-auto`.
---

# grill-me-auto

Same coverage as [`grill-me`](../grill-me/SKILL.md), different delivery: produce every question, every option, every recommendation **as one written document**, then stop. The user reads it on their own time, picks answers, and pastes a single reply back. No turn-by-turn interview.

Use this when:

- The user explicitly invokes `/grill-me-auto` (or asks for "the grill but written down", "auto grill", "give me all the questions at once").
- The user wants to review the grill in a browser / preview tool with collapsible sections.
- The user wants to answer offline and reply once.

If the user just says "grill me" or "/grill-me", use the interactive [`grill-me`](../grill-me/SKILL.md) skill instead. This skill is the batch-mode fork.

---

## Step 0 — Ask for grill depth before generating

Before producing the document, ask the user which depth to run at. **Default is `deep`** (deepest). Offer the three options with a one-line description each, plus a pre-selection shortcut:

> Grill depth? (default: **deep**)
>
> - **deep** — every branch of the decision tree, critical + edge + corner cases, cross-references against code / docs / prior decisions, invented boundary scenarios. Unbounded (typically 20–40+ questions).
> - **standard** — critical assumptions + main edge cases + obvious cross-references. ~15–25 questions.
> - **quick** — top highest-leverage hard-hitters only. Deal-breaker assumptions and dead-on-arrival risks. ~5–10 questions.
>
> Reply with `deep` / `standard` / `quick` (or hit return for deep). Pre-select next time with `/grill-me-auto deep`, `/grill-me-auto standard`, or `/grill-me-auto quick` — aliases `3` / `2` / `1` and `deepest` / `medium` / `sharp` also work.

If the user invoked the skill with an argument that maps to a level (e.g. `/grill-me-auto quick`, `/grill-me-auto 2`, `/grill-me-auto deepest`), **skip the depth prompt** and proceed directly at that depth. Echo the chosen depth in one short line so the user knows what they got.

If the argument is ambiguous or unrecognised, fall back to asking.

---

## Step 1 — Silently explore the codebase

Before writing questions, gather the context an interactive grill would have gathered by asking. The whole point of auto mode is that the user shouldn't have to answer trivia the agent can read for itself.

- Inspect the files / dirs / artifacts the plan touches.
- Re-read relevant `CLAUDE.md`, `CONTEXT.md`, ADRs, `MEMORY.md` entries, recent commits / PRs in the affected area.
- Resolve anything the user already stated in this session — don't ask back.

Do **not** narrate this step in chat — the user is waiting for the document, not commentary. Mention only blockers (e.g. "couldn't find `CONTEXT.md` — questions about domain language will be answered as assumptions, flag them in 1.4 Alt").

---

## Step 2 — Generate questions according to depth

Apply the same rigor as `grill-me`. Depth changes *how many branches* you walk, not *how sharp* each question is.

- **deep** — every branch, every dependency. Push back on hedging language inside the recommendation itself ("we *might* batch writes" → ask which one and why). Cross-check claims against the code. Invent boundary scenarios. Unbounded; typically 20–40+ questions for non-trivial plans.
- **standard** — cover the spine plus the obvious edges. Probe each major assumption once. ~15–25 questions.
- **quick** — only questions whose wrong answer would kill or seriously bend the plan. Skip stylistic, naming, and second-order concerns. ~5–10 questions.

For each question:

- **Question text** — sharp, one sentence. No filler.
- **Why it matters** — one line. The cost of getting it wrong.
- **Options** — 2 to 4 mutually-exclusive choices, labelled `A`, `B`, `C`, `D`.
- **Recommendation** — pick one option as the agent recommendation. Lead with the letter (`Recommendation: A`) and one-line reason.
- **Alt recommendation** — pick a *different* option as a second-best (`Alt: B`) with the one-line reason it's a defensible alternative. If the question is binary and only one option is reasonable, set Alt to "n/a" — don't manufacture a fake second choice.

Number questions sequentially (`1`, `2`, `3`, …). Options are letters within the question (`1.A`, `1.B`, etc) so the answer key is unambiguous.

If a sub-question only matters depending on an earlier answer, nest it (`2a`, `2b`) inside its parent's `<details>` block and mark it `[conditional on 2 = A]`. Do not produce conditional questions at the top level — that breaks the answer-key contract.

---

## Step 3 — Pick the document path

Document goes at `<project-root>/.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`.

- **Project root** — resolve via `git rev-parse --show-toplevel`; fall back to first ancestor with `.claude/` or `.git`; fall back to `pwd`.
- **Slug** — 2–3 word kebab-case derived from the topic being grilled (e.g. `auth-rewrite`, `prd-pricing`, `migration-rollback`). Pulled from the user's prompt or, if absent, from the conversation's stated goal.
- **Timestamp** — local time, `YYYY-MM-DD-HHMM`. Collisions in the same minute get a `-2`, `-3` suffix.
- **Depth suffix** — `deep` / `standard` / `quick` — so the filename announces what you got.

If `.grills/` does not exist, create it. If it is not already gitignored, append `/.grills/` to the project's `.gitignore` and stage that one-line change with a short note in chat (`Added /.grills/ to .gitignore so grill docs stay out of source control.`). Don't commit on the user's behalf.

Write the file atomically (`.tmp` then rename).

---

## Step 4 — Write the document

The document must render with **collapsible question blocks** in GitHub, GitLab, VS Code preview, Obsidian, and any standard markdown previewer. That means each question lives inside a `<details><summary>…</summary>…</details>` block, with a top-level numbered list outside the details for the table of contents.

Use this exact structure (see `templates/grill-doc.template.md` for a filled example):

````markdown
---
created_at: 2026-05-30T21:14:00-07:00
depth: deep
topic: <one-line description of what is being grilled>
status: open
total_questions: <N>
answer_key_marker: "## Answer key"
shortcuts:
  accept_all_recommendations: "ACCEPT_ALL_RECOMMENDATIONS"
  accept_all_alt_recommendations: "ACCEPT_ALL_ALT_RECOMMENDATIONS"
  per_question_format: "<question_number>: <option_letter>"
---

# Grill: <topic>

> Depth: **deep** · Generated 2026-05-30 21:14 · <N> questions
>
> **How to use this doc:** Read each question. Each has 2–4 options labelled `A` / `B` / `C` / `D`, an agent **Recommendation**, and an **Alt** recommendation. Pick an option per question in the **Answer key** at the bottom, or paste one of the three batch shortcuts and stop there. Reply in chat — the agent will apply your answers in one pass.

## Questions

1. **<Q1 sharp one-sentence question>**
2. **<Q2>**
3. **<Q3>**
   <!-- TOC — top-level only; conditional sub-questions live inside their parent's details block -->

---

<details>
<summary><strong>1. &lt;Q1 sharp one-sentence question&gt;</strong></summary>

- **Why it matters:** <one line; cost of getting this wrong>
- **Options:**
  - **1.A** — <option A text>
  - **1.B** — <option B text>
  - **1.C** — <option C text> *(omit if only 2 options)*
- **Recommendation:** **A** — <one-line reason>
- **Alt:** **B** — <one-line reason it's defensible>

</details>

<details>
<summary><strong>2. &lt;Q2&gt;</strong></summary>

- **Why it matters:** <…>
- **Options:**
  - **2.A** — …
  - **2.B** — …
- **Recommendation:** **B** — …
- **Alt:** n/a — only one defensible answer; B is correct, A is the strawman.

  <details>
  <summary><strong>2a. &lt;Sub-question, conditional on 2 = A&gt;</strong></summary>

  - **Conditional on:** `2 = A`
  - **Why it matters:** <…>
  - **Options:** **2a.A** — … / **2a.B** — …
  - **Recommendation:** **A** — …
  - **Alt:** **B** — …

  </details>

</details>

<!-- … one details block per question … -->

---

## Answer key

Pick exactly one of three ways to reply. Paste the chosen block back into chat verbatim.

### Option 1 — Accept all agent recommendations

```
ACCEPT_ALL_RECOMMENDATIONS
```

### Option 2 — Accept all alt recommendations

```
ACCEPT_ALL_ALT_RECOMMENDATIONS
```

For any question where Alt is `n/a`, the agent will fall back to the primary recommendation and flag it in the summary.

### Option 3 — Answer per question

Replace each `?` with the option letter you want. One question per line. Conditional sub-questions are only required if their parent answer triggers them.

```
1: ?
2: ?
3: ?
<!-- … one line per question … -->
```

You can mix and match: copy this block, fill the ones you have opinions on, and write `rec` (use the recommendation) or `alt` (use the alt) for the rest. Example: `5: rec`, `7: alt`, `12: B`.
````

A few authoring rules for the document body:

- Use `<details><summary><strong>…</strong></summary>…</details>` so the question stays visible when collapsed and the body hides cleanly. Plain GFM block-quotes don't collapse — `<details>` is the portable answer.
- Bold the question inside `<strong>` (not just `**`) — markdown inside `<summary>` is unreliable across renderers, HTML is not.
- Escape `<` and `>` inside `<summary>` as `&lt;` and `&gt;` only if the question literally contains them (rare).
- Conditional sub-questions nest inside their parent's `<details>` block and start with **`Conditional on: <expr>`**. Sub-question numbers are `<parent><letter>` (e.g. `2a`, `2b`) so the answer key stays flat for top-level entries.
- The answer-key block lives at the bottom under `## Answer key`. Three options. Always in this order.
- `created_at` in the frontmatter uses the local timezone offset (e.g. `-07:00`) — don't normalise to UTC.

---

## Step 5 — Hand the document off and stop

Print one short message in chat:

> Grill written to `.grills/<filename>` — **<N>** questions at depth **<depth>**. Open it in a markdown previewer, then paste **one of**:
>
> 1. `ACCEPT_ALL_RECOMMENDATIONS`
> 2. `ACCEPT_ALL_ALT_RECOMMENDATIONS`
> 3. The filled answer-key block from the bottom of the doc
>
> I'll apply your answers in one pass when you reply.

Then **stop**. Do not start summarising. Do not start implementing. Do not preview the doc back to the user. The whole value of this skill is the user gets to read on their own time.

---

## Step 6 — When the user replies, apply in one pass

Parse the user's reply against the shortcuts and per-question key:

- `ACCEPT_ALL_RECOMMENDATIONS` — apply the agent recommendation for every top-level question. For conditional sub-questions, walk them only if the parent answer triggers them.
- `ACCEPT_ALL_ALT_RECOMMENDATIONS` — apply the alt recommendation. For any question where Alt is `n/a`, fall back to the recommendation and call this out in the summary so the user can see where it happened.
- **Per-question key** — read each line `<question_number>: <option_letter|rec|alt>`. `rec` resolves to the recommendation letter; `alt` resolves to the alt letter (or recommendation if alt is `n/a`).

If the reply is malformed (missing questions, illegal letters, no shortcut and no key) — ask one targeted question, not a re-grill. Example: "Q4 has no answer and isn't conditional — `A`, `B`, or `rec`?"

After parsing:

1. Update the grill doc's frontmatter: `status: answered`, append `answered_at`, and add a `## Resolved answers` section at the very bottom showing `<question>: <chosen option> — <one-line restatement of what that means>`.
2. In chat, summarise the resolved plan in ≤10 bullets. Anything where the answer changed direction from the user's original prompt gets called out with `(changed:)`.
3. Hand off to the next obvious step (implementation, plan write-up, etc) — but do not start it without the user's go-ahead.

---

## When to refuse / redirect

- User asks for an interactive grill → redirect to `/grill-me`.
- User asks for an engineering-only domain stress-test → redirect to `/domain-grill` (still interactive).
- User invokes `/grill-me-auto` with no plan / prompt / artifact to grill → ask once for the topic; don't generate a generic grill.
- Plan or artifact lives in another repo / external doc → ask for a path or paste; don't fabricate questions against unseen material.

---

## Why this fork exists

`grill-me` is interactive — one question at a time, user answers, branch resolves, next question. That's the right tool when the agent + user want to discover the plan *together*.

`grill-me-auto` is for when the user already knows roughly what they think, wants to see the full surface in writing, wants to review it offline (or in a browser preview, on mobile, away from the agent), and reply in one batch. The collapsibility matters because deep grills produce a lot of branches and the user wants to scan the table of contents first, then drill into specific questions.

Same coverage, same recommendations, different cadence.

---

_Forked from [`grill-me`](../grill-me/SKILL.md) (which is itself a fork of [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) by [Matt Pocock](https://github.com/mattpocock)). The relentless-interview core is Matt's. The depth selector is the upstream `amit-t/skills` fork. This fork adds the batch-document delivery mode._
