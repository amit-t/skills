# Branching Questions

Phase 2.5 discovery is a **conversation, not a questionnaire**. Each answer informs the next question. The goal is to surface genuine undocumented experience, not to generate claims the user can't defend.

## Principles

1. **Start broad, go narrow.** Open question first; follow-ups drill in on what the user shared.
2. **Branch on the answer.** Promising → deeper. No → pivot or move on.
3. **Time-box.** 10–15 min total. After 2–3 dry attempts per gap, move on.
4. **Cross-reference.** "Earlier you mentioned X — does it relate here too?"
5. **Capture in structure.** Context, scope, addressed-gap, bullet draft, truthfulness note.
6. **Truth bar stays high.** Help the user articulate what's real. Never lead them into invention.

## Multi-Job Leverage Prefix

When running inside a batch (multi-job mode), prefix each gap probe with leverage context:

```
"{SKILL} appears in {N} of your target jobs ({Company1}, {Company2}).
This is a {HIGH/MEDIUM/LOW}-LEVERAGE gap — addressing it helps {all / some / one} application(s).
Current best match: {X}% ('{best_match_text}').

{Standard probe below}"
```

- HIGH (3+ jobs), MEDIUM (2), LOW (1).

## Pattern A — Technical Skill Gap

```
PROBE: "The role requires {SKILL}. Have you worked with {SKILL} or {ADJACENT}?"

BRANCH A1 — YES / direct experience
  → "What did you use it for?"
  → "Scale? {metric relevant to the tech}"
  → "Production or dev/test?"
  → "What specific challenges did you solve?"
  → "Any metrics — performance / reliability / cost?"
  → CAPTURE: detailed bullet

BRANCH A2 — INDIRECT
  → "What was your role in the {SKILL} work?"
  → "Did you {action1} / {action2} / {action3}?"
  → "What did you learn?"
  → CAPTURE: frame as support/enabling role if substantial

BRANCH A3 — ADJACENT TECH
  → "Tell me about your {ADJACENT_TECH} experience."
  → "Did you do {relevant_activity}?"
  → CAPTURE: frame as related expertise; note the gap honestly

BRANCH A4 — PERSONAL / LEARNING
  → "Personal projects, courses, self-learning?"
  → "What did you build or deploy?"
  → "How recent?"
  → CAPTURE: include if recent and substantive; otherwise note

BRANCH A5 — COMPLETE NO
  → "Any {broader_category} work?"
  → If yes, explore; if no, move on
```

## Pattern B — Soft Skill / Experience Gap

```
PROBE: "The role emphasizes {SOFT_SKILL}. Tell me about times you've {demonstrated_skill}."

BRANCH B1 — STRONG EXAMPLE
  → "What {entities/stakeholders} were involved?"
  → "What was the challenge?"
  → "How did you drive the outcome?"
  → "Result? Metrics?"
  → "Obstacles navigated?"
  → CAPTURE: bullet with impact

BRANCH B2 — VAGUE / UNCERTAIN
  → "Let me reframe — have you ever {alternative_phrasing}?"
  → "What was the situation?"
  → "How many stakeholders / what scope?"
  → "What made it challenging?"
  → CAPTURE: help articulate clearly

BRANCH B3 — PROJECT-SPECIFIC
  → "Tell me more about that project."
  → "Your role vs others?"
  → "How did you ensure alignment?"
  → CAPTURE: frame as leadership if substantial

BRANCH B4 — VOLUNTEER / SIDE WORK
  → "Tell me more — scope, timeline?"
  → "What skills relate to this job?"
  → "Measurable outcomes?"
  → CAPTURE: include if demonstrates the capability
```

## Pattern C — Recent Work Probe

```
PROBE: "What have you worked on in the last 6 months that isn't on your resume yet?"

BRANCH C1 — DESCRIBES PROJECT
  → "Your role? Tech/methods? Problem? Impact?"
  → "Does this address {gap_area}?"
  → CAPTURE if substantive

BRANCH C2 — MULTIPLE THINGS
  → "Let's walk through each. Start with {first}."
  → Prioritize by gap relevance
  → CAPTURE multiple bullets

BRANCH C3 — "NOTHING NEW"
  → "Small improvements? Process changes? Learning?"
  → "Mentoring, teaching, knowledge sharing?"
  → "Anything that seems too small to mention?"
  → Often surfaces content; capture if relevant
```

## Capture Template

```markdown
### Discovery {n}: {Brief description}
- Context: {where / when}
- Scope: {scale, duration, impact}
- Addresses: {gap name(s)}, leverage: HIGH/MEDIUM/LOW
- Bullet draft: "{Achievement-focused bullet}"
- Confidence: {% the gap is filled}
- Truthfulness note: {why the bullet is defensible}
- Integration: ADD-TO-RESUME / ADD-TO-LIBRARY / REFINE / DISCARD
```

## Handing Off

After discovery, ask per-experience:

```
Captured {N} new experiences. For each:
1. ADD TO CURRENT RESUME — integrate into matching
2. ADD TO LIBRARY ONLY — save for future jobs
3. REFINE FURTHER — need to think more
4. DISCARD — not relevant enough

How should I handle each?
```

## Example Flow

```
SKILL → "JD requires CI/CD. Have you worked with CI/CD pipelines?"
USER  → "Yeah, set up GitHub Actions for my side project."
SKILL → "What does the pipeline do?" [A1 — depth]
USER  → "Runs tests and deploys to cloud on push."
SKILL → "What testing framework?" [technical detail]
USER  → "pytest."
SKILL → "Is this a production app?" [impact/scale]
USER  → "Yeah — three nonprofits use it."
SKILL → "Flaky tests or reliability issues you've dealt with?" [real-world depth]
USER  → "Had to add retries for API-dependent tests."
SKILL → "Nice — troubleshooting signal. Build time / deploy frequency?"
USER  → "Deploys in ~3 min, several times a week."

CAPTURED: hands-on CI/CD + pytest + flaky-test handling + production deploys
         for 3 real users. Gap filled with concrete, defensible detail.
```
