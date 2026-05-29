---
name: grill-me
description: Interview the user relentlessly about a plan or design until reaching shared understanding, resolving each branch of the decision tree. Use when user wants to stress-test a plan, get grilled on their design, or mentions "grill me". Supports a depth selector (quick / standard / deep) — deep is the default.
---

Interview me relentlessly about every aspect of this plan until we reach a shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time.

If a question can be answered by exploring the codebase, explore the codebase instead.

## Step 0 — Ask for grill depth before grilling

Before the first real question, ask the user which depth to run at. **Default is `deep`** (deepest). Offer the three options with a one-line description each, plus a one-shot invocation shortcut for next time:

> Grill depth? (default: **deep**)
>
> - **deep** — walk every branch of the decision tree, critical + edge + corner cases, cross-reference assertions against code / docs / prior decisions, invent boundary scenarios, surface contradictions hard. Unbounded until shared understanding.
> - **standard** — critical assumptions + main edge cases + obvious cross-references. Skip exotic corner cases. ~15–25 questions or until major branches are resolved.
> - **quick** — top 5 highest-leverage hard-hitters only. Deal-breaker assumptions and dead-on-arrival risks. ~5–10 questions. Triage, not full coverage.
>
> Reply with `deep` / `standard` / `quick` (or just hit return for deep). You can also pre-select next time with `/grill-me deep`, `/grill-me standard`, or `/grill-me quick` — aliases `3` / `2` / `1` and `deepest` / `medium` / `sharp` also work.

If the user invoked the skill with an argument that maps to a level (e.g. `/grill-me quick`, `/grill-me 2`, `/grill-me deepest`), **skip Step 0** and proceed directly at that depth. Echo the chosen depth in one short line ("Running at **quick** depth — top hard-hitters only.") so the user knows what they're getting.

If the argument is ambiguous or unrecognised, fall back to asking.

## How depth shapes the grilling

- **deep** — every branch, every dependency. Stress with invented scenarios. Cross-check claims against the codebase. Push back on hedging language. Do not stop until you can summarise the plan back without holes.
- **standard** — cover the spine of the plan plus the obvious edges. Probe each major assumption once. Stop when the critical path is solid even if leafy decisions remain.
- **quick** — only the questions whose wrong answer would kill or seriously bend the plan. Skip stylistic, naming, and second-order concerns. One pass, no follow-up branches unless the answer reveals a critical gap.

Depth never lowers rigor on the questions you *do* ask — it changes how many branches you walk, not how sharp each question is.

---

_Forked from [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) by [Matt Pocock](https://github.com/mattpocock). This fork adds the depth selector; the relentless-interview core is Matt's original._
