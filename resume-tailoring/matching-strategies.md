# Matching Strategies

How Phase 3 scores candidate bullets against template slots, and how Phase 2 handles title reframing and role consolidation.

## Scoring Formula

```
Overall = 0.4·Direct + 0.3·Transferable + 0.2·Adjacent + 0.1·Impact
```

### Direct Match (40%)
Same skill, domain, technology, or outcome type as the requirement.

| Score | Meaning |
|------|---------|
| 90–100 | Exact match — same skill, same domain, same context |
| 70–89  | Strong match — same skill, different domain |
| 50–69  | Keyword/outcome overlap only |
| <50    | Weak direct match |

### Transferable (30%)
Same capability, different context (stack, industry, scale).

| Score | Meaning |
|------|---------|
| 90–100 | Process/skill is generic — transfers cleanly |
| 70–89  | Mostly transferable — needs light translation |
| 50–69  | Partially transferable — analogy required |
| <50    | Stretch |

### Adjacent (20%)
Touched the skill as a secondary responsibility, used related tools, worked in related problem space.

| Score | Meaning |
|------|---------|
| 90–100 | Same thing under a different name |
| 70–89  | Clearly related, distinct |
| 50–69  | Requires explanation |
| <50    | Loose |

### Impact (10%)
Achievement type aligns with what the target role values (metrics, scale, innovation, collaboration, revenue…).

| Score | Meaning |
|------|---------|
| 90–100 | Perfect alignment with role's impact lens |
| 70–89  | Strong alignment |
| 50–69  | Moderate |
| <50    | Weak |

### Confidence Bands

| Overall | Band | Action |
|------|------|--------|
| 90–100 | DIRECT | Use with confidence |
| 75–89  | TRANSFERABLE | Strong candidate |
| 60–74  | ADJACENT | Use with reframing |
| 45–59  | WEAK | Only if nothing better |
| <45    | GAP | Flag — do not force |

## Reframing Strategies

Apply **only** when overall ≥ 60 but terminology or emphasis is off. Every reframing must preserve factual accuracy and be disclosed in the generation report.

### Strategy 1 — Keyword alignment
Preserve meaning, adjust vocabulary to match the target.
```
Before: "Led experimental design and data analysis programs"
After:  "Led data science programs combining experimental design and statistical analysis"
Why truthful: same activities, domain-standard phrasing for the target role
```

### Strategy 2 — Emphasis shift
Same facts, different focus.
```
Before: "Designed statistical experiments... saving millions in recall costs"
After:  "Prevented millions in potential recall costs through predictive risk detection using statistical modeling"
Why truthful: outcome and method unchanged; lead with the outcome
```

### Strategy 3 — Abstraction level
Up or down on technical specificity depending on target.
```
Before: "Built MATLAB-based automated evaluation system"
After:  "Developed automated evaluation system" (language-agnostic target)
  or:   "Built automated evaluation system (MATLAB, Python)" (stack-heavy target)
```

### Strategy 4 — Scale emphasis
Highlight the scale dimension the target role cares about (people, $, traffic, org units, geographies).
```
Before: "Managed project with 3 stakeholders"
After:  "Led cross-functional initiative coordinating 3 organizational units"
```

## Title Reframing (Phase 2)

**Core rule:** Stay truthful to what you did; emphasize the aspect most relevant to the target.

Strategies:
- **Emphasize a different aspect:** "Graduate Researcher" → "Research Software Engineer" (if coding-heavy).
- **Industry-standard terminology:** "Scientist III" → "Senior Research Scientist".
- **Truthful specialization:** "Engineer" → "ML Engineer" (if ML was substantial).
- **Seniority indicator:** "Lead" vs "Senior" vs "Staff" based on defensible scope.

**Constraints:**
- Company name and dates must be exact.
- Core responsibilities must match what you actually did.
- Never claim seniority the scope can't defend.

Present 2 options with rationale; let the user pick.

## Role Consolidation (Phase 2)

**Consolidate same-company roles only when:**
- Responsibilities overlap heavily.
- Target role values continuity over granular progression.
- The combined narrative is stronger.
- Page space is tight.

**Keep separate when:**
- Different companies (always separate).
- Dramatically different responsibilities that both matter.
- Target role values the progression story.
- One position has much more relevant experience.

Template:
```
For {Company} with {N} positions:

OPTION A (Consolidated): "{combined_title}" ({first_start}–{last_end})
  Rationale: {why}

OPTION B (Separate): {position_1} / {position_2}
  Rationale: {why}

RECOMMENDED: Option {A/B} because {reasoning}
```

## Gap Handling (<60% on a must-have)

Present the user four options, in order:

1. **Reframe** — take the best available adjacent bullet and reframe (show before/after + truthfulness note). Use only if the reframe is honest.
2. **Run Phase 2.5 discovery** — the gap might be fillable from undocumented experience.
3. **Omit the slot** — drop the bullet, reallocate space, disclose in the report.
4. **Acknowledge in cover letter** — emphasize learning velocity / related strengths.

Never fabricate. If all four options are weak, proceed with the gap flagged and recommend cover-letter framing + interview prep in the report.
