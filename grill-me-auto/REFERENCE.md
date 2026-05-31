# Grill Me Auto reference

This file is the canonical format contract. The filled example lives in [`templates/grill-doc.template.md`](./templates/grill-doc.template.md); do not duplicate the example elsewhere.

## Invocation and depth

Recognize `/grill-me-auto`, `/Grill Me Auto`, `/grill me auto`, "auto grill", and "all grill questions at once".

| Depth | Aliases | Coverage | Typical count |
| --- | --- | --- | --- |
| `deep` | `3`, `deepest` | every branch, dependency, edge case, contradiction, code/doc cross-check, and invented boundary scenario | 20–40+ |
| `standard` | `2`, `medium` | critical assumptions, main edge cases, and obvious cross-checks | 15–25 |
| `quick` | `1`, `sharp` | highest-leverage deal-breakers and dead-on-arrival risks only | 5–10 |

Depth changes how many branches are covered, not how sharp each question is.

## File contract

- Path: `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`.
- Timestamp: local time; same-minute collisions get `-2`, `-3`, etc.
- Slug: 2–3 word kebab-case topic slug.
- Write atomically through a temporary file and rename.
- If `.grills/` is not ignored, append `/.grills/` to `.gitignore` and stage that line only.

## Frontmatter contract

Each grill document starts with YAML frontmatter:

```yaml
created_at: 2026-05-30T21:14:00+05:30
depth: deep
topic: Rewrite the auth middleware to remove session-token storage
status: open
total_questions: 6
answer_key_marker: "## Answer key"
shortcuts:
  accept_all_recommendations: "accept all my recommendations"
  accept_all_recommendations_alias: "ACCEPT_ALL_RECOMMENDATIONS"
  accept_all_alt_recommendations: "accept all my alt recommendations"
  accept_all_alt_recommendations_alias: "ACCEPT_ALL_ALT_RECOMMENDATIONS"
  per_question_format: "<question_number>: <option_letter|rec|alt>"
```

When answered, change `status` to `answered` and add `answered_at`.

## Precision contract

The grill document is the deliverable, so authored prose inside it must pass [`precision-mode`](../precision-mode/SKILL.md) before serialization. Apply only to authored content (question text, *Why it matters*, option labels, recommendation reasons, alt reasons). Do not strip the markdown scaffolding (`<details>`, `<summary>`, bold field labels, TOC heading, answer-key heading, frontmatter keys, reply-path code blocks) — those are contract.

Word caps that bound the precision pass:

| Field | Cap |
| --- | --- |
| Question text | ≤1 sentence, ≤20 words |
| *Why it matters* | ≤1 sentence, ≤20 words |
| Option label | ≤15 words per option |
| Recommendation reason | ≤25 words |
| Alt reason | ≤25 words, or the literal token `n/a` |

If a reason genuinely needs more, split into two sentences — never drop the *why* to hit the cap. Precision must not strip security warnings, breaking-change flags, data-loss risks, or specific code/ADR references that ground the recommendation. The dual recommendation + alt structure is contract; precision cannot collapse it to a single answer.

## Question block contract

The document must render with collapsible numbered items in common markdown previews:

```markdown
<details>
<summary><strong>1. Sharp one-sentence question?</strong></summary>

- **Why it matters:** One line naming the cost of getting it wrong.
- **Options:**
  - **1.A** — First mutually exclusive answer.
  - **1.B** — Second mutually exclusive answer.
- **Recommendation:** **A** — one-line reason.
- **Alt:** **B** — one-line reason, or `n/a` only when there is no defensible alternative.

</details>
```

Rules:

- Include a top-level `## Questions` table of contents before the details blocks.
- Use one `<details>` block per top-level question.
- Use `<summary><strong>...</strong></summary>`; markdown inside `<summary>` is less portable.
- Label options as `N.A`, `N.B`, `N.C`, `N.D`.
- Nested conditionals stay inside the parent details block and use `2a`, `2b`, etc with `Conditional on: <expr>`.
- Do not put conditional questions in the top-level table unless always relevant.

## Answer key contract

End with exactly three reply paths, in this order:

1. **Accept all my recommendations**

   ```text
   accept all my recommendations
   ```

   Alias: `ACCEPT_ALL_RECOMMENDATIONS`

2. **Accept all my alt recommendations**

   ```text
   accept all my alt recommendations
   ```

   Alias: `ACCEPT_ALL_ALT_RECOMMENDATIONS`

   If Alt is `n/a`, fall back to the primary recommendation and flag the fallback in the summary.

3. **Copy/paste this in the chat after reading it back to the agent**

   ```text
   1: ?
   2: ?
   3: ?
   ```

   Users may answer with an option letter, `rec`, or `alt` per line.

## Reply parsing contract

- Shortcuts are case-insensitive after trimming whitespace.
- Per-question lines use `<question_number>: <option_letter|rec|alt>`.
- `rec` resolves to the documented recommendation.
- `alt` resolves to the documented alt, or the primary recommendation when Alt is `n/a`.
- Malformed replies get one targeted repair question, not a new grill.

Append resolved answers after parsing:

```markdown
## Resolved answers

Answered at: 2026-05-30T22:10:00+05:30

- **1:** **A** — one-line restatement of the selected meaning.
- **2:** **rec → B** — one-line restatement of the selected meaning.
- **2a:** skipped — parent answer did not trigger this conditional question.
```
