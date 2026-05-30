# Grill Me Auto reference

## Depth behavior

Depth changes how many branches are covered, not the sharpness of each question.

| Depth | Coverage | Typical count |
| --- | --- | --- |
| `deep` | Every branch, dependency, edge case, contradiction, code/doc cross-check, and invented boundary scenario. | 20–40+ |
| `standard` | Critical assumptions, main edge cases, and obvious cross-checks. | 15–25 |
| `quick` | Highest-leverage deal-breakers and dead-on-arrival risks only. | 5–10 |

## Document skeleton

````markdown
---
created_at: 2026-05-30T21:14:00+05:30
depth: deep
topic: <one-line topic>
status: open
total_questions: <N>
answer_key_marker: "## Answer key"
shortcuts:
  accept_all_recommendations: "accept all my recommendations"
  accept_all_recommendations_alias: "ACCEPT_ALL_RECOMMENDATIONS"
  accept_all_alt_recommendations: "accept all my alt recommendations"
  accept_all_alt_recommendations_alias: "ACCEPT_ALL_ALT_RECOMMENDATIONS"
  per_question_format: "<question_number>: <option_letter|rec|alt>"
---

# Grill: <topic>

> Depth: **deep** · Generated 2026-05-30 21:14 · <N> questions
>
> **How to use this doc:** Read each question, expand details as needed, then reply with one shortcut or the filled answer key.

## Questions

1. **<Q1>**
2. **<Q2>**

---

<details>
<summary><strong>1. &lt;Q1&gt;</strong></summary>

- **Why it matters:** <cost of getting this wrong>
- **Options:**
  - **1.A** — <option A>
  - **1.B** — <option B>
  - **1.C** — <option C>
- **Recommendation:** **A** — <reason>
- **Alt:** **B** — <reason>

</details>

<details>
<summary><strong>2. &lt;Q2&gt;</strong></summary>

- **Why it matters:** <cost of getting this wrong>
- **Options:**
  - **2.A** — <option A>
  - **2.B** — <option B>
- **Recommendation:** **B** — <reason>
- **Alt:** n/a — only one defensible answer; B is correct.

  <details>
  <summary><strong>2a. &lt;Conditional sub-question&gt;</strong></summary>

  - **Conditional on:** `2 = A`
  - **Why it matters:** <cost>
  - **Options:**
    - **2a.A** — <option A>
    - **2a.B** — <option B>
  - **Recommendation:** **A** — <reason>
  - **Alt:** **B** — <reason>

  </details>

</details>

---

## Answer key

Pick exactly one of three ways to reply. Paste the chosen block back into chat verbatim.

### Option 1 — Accept all my recommendations

```
accept all my recommendations
```

Alias:

```
ACCEPT_ALL_RECOMMENDATIONS
```

### Option 2 — Accept all my alt recommendations

```
accept all my alt recommendations
```

Alias:

```
ACCEPT_ALL_ALT_RECOMMENDATIONS
```

For any question where Alt is `n/a`, the agent falls back to the primary recommendation and flags it in the summary.

### Option 3 — Copy/paste this in the chat after reading it back to the agent

Replace each `?` with the option letter you want. Conditional sub-questions are only required if their parent answer triggers them.

```
1: ?
2: ?
```

You can mix and match: use `rec` for the recommendation or `alt` for the alt. Example: `5: rec`, `7: alt`, `12: B`.
````

## Answer parsing

Accepted shortcuts are case-insensitive after trimming whitespace:

- `accept all my recommendations`
- `ACCEPT_ALL_RECOMMENDATIONS`
- `accept all my alt recommendations`
- `ACCEPT_ALL_ALT_RECOMMENDATIONS`

Per-question lines use `<question_number>: <option_letter|rec|alt>`. Resolve `rec` and `alt` from the document's recommendation fields. If `alt` resolves to `n/a`, use the primary recommendation and report the fallback.

Malformed replies get one targeted repair question, for example: "Q4 is missing and is not conditional — reply with `4: A`, `4: B`, `4: rec`, or `4: alt`."

## Resolved answer section

Append this after parsing:

```markdown
## Resolved answers

Answered at: 2026-05-30T22:10:00+05:30

- **1:** **A** — <one-line restatement of chosen meaning>
- **2:** **rec → B** — <one-line restatement>
- **2a:** skipped — parent answer did not trigger this conditional question.
```
