---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when user wants to create, write, or build a new skill.
---

# Writing Skills

A skill exists to wrangle determinism out of a stochastic system. **Predictability** — the agent taking the same *process* every run, not producing the same output — is the root virtue; every rule below serves it. When a drafted skill misbehaves, diagnose it against the failure modes in [principles.md](principles.md).

*Principles adapted from [writing-great-skills in mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills).*

## Process

1. **Gather requirements** — done when each of these has an answer:
   - What task/domain does the skill cover, and which distinct use cases (**branches**) must it handle?
   - Model-invoked or user-invoked? (see Invocation)
   - Does it need executable scripts or just instructions?
   - Any reference materials to include?

2. **Draft the skill** — done when the draft passes every item on the Review Checklist:
   - SKILL.md with concise instructions
   - Disclosed reference files for material only some branches need
   - Utility scripts if deterministic operations are needed

3. **Review with user** — done when the user confirms every use case from step 1 is covered:
   - Does this cover your use cases?
   - Anything missing or unclear?
   - Should any section be more/less detailed?

## Invocation

Two modes, trading different costs:

- **Model-invoked** (the default): the skill keeps a trigger-rich description that sits in the agent's context every turn, so the agent — or another skill — can fire it autonomously. The price is permanent **context load**.
- **User-invoked** (`disable-model-invocation: true`): only the human typing its name can fire it. Zero context load, but it spends **cognitive load** — the human is the index that must remember it exists.

Pick model-invocation only when the agent (or another skill) must reach the skill on its own; otherwise make it user-invoked.

## Description

The `description` frontmatter field is the only thing the agent sees when deciding which skill to load, so every word pays context load:

- Max 1024 chars, third person. First sentence: what it does. Second: "Use when [specific triggers]".
- **Front-load the skill's leading word** — the description is where it does its invocation work.
- **One trigger per branch.** Synonyms that rename the same branch are duplication — collapse them; keep only genuinely distinct branches, plus one verbatim phrase users actually type.

**Good**: `Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, or document extraction.`

**Bad**: `Helps with documents.` — gives the agent no way to distinguish this from other document skills.

## Information hierarchy

Rank a skill's content by how immediately the agent needs it:

1. **Steps in SKILL.md** — what the agent does, in order. Each step ends on a **completion criterion** that is *checkable* (the agent can tell done from not-done) and *exhaustive* ("every modified model accounted for", not "produce a change list").
2. **Reference in SKILL.md** — definitions, rules, and facts consulted on demand.
3. **Disclosed reference** — a linked sibling `.md`, loaded only when its **context pointer** fires. The pointer's wording, not its target, decides how reliably the agent reaches the material.

**Progressive disclosure** is the move down this ladder, and branching licenses it: inline what every run needs; push behind a pointer what only some branches reach. Disclose when SKILL.md exceeds 100 lines, when content spans distinct domains (finance vs sales schemas), or when advanced features are rarely needed. Keep references one level deep.

```
skill-name/
├── SKILL.md           # Steps + always-needed reference (required)
├── REFERENCE.md       # Disclosed reference (if needed)
└── scripts/           # Utility scripts (if needed)
    └── helper.js
```

## Writing style

- **Leading words** — collapse restated qualities into one strong pretrained word the agent thinks with: "fast, deterministic, low-overhead" becomes *tight*. Fewer tokens, sharper hook.
- **Positive phrasing** — state the target behaviour ("write one-line comments") rather than banning the bad one. Keep a prohibition only as a hard guardrail you can't phrase positively, and pair it with what to do instead.
- **Single source of truth** — one meaning, one place; everywhere else, a pointer.
- **Every line must change behaviour** — a line the model already obeys by default ("be thorough") is a no-op: delete the sentence or strengthen the word (*relentless*).

## When to Add Scripts

Add utility scripts when the operation is deterministic (validation, formatting), the same code would be generated repeatedly, or errors need explicit handling. Scripts save tokens and improve reliability vs generated code.

## Review Checklist

After drafting, verify:

- [ ] Description: leading word front-loaded, one trigger per branch, "Use when..." present
- [ ] SKILL.md under 100 lines; overflow disclosed behind a sharply worded context pointer
- [ ] Every step ends on a checkable, exhaustive completion criterion
- [ ] Each meaning has one home; every relative link resolves
- [ ] Prohibitions rephrased as target behaviour wherever possible
- [ ] No time-sensitive info; consistent terminology; concrete examples included
- [ ] Swept for the failure modes in [principles.md](principles.md): premature completion, duplication, sediment, sprawl, no-ops, negation
