---
name: design-review
description: Multi-agent design review from 5 perspectives — UX Researcher, Accessibility Auditor, Engineer, Brand Guardian, and End User Voice. Feed it any generated screen file or design description.
user-invocable: true
---

## Quick Start

```
/design-review                              → Review latest screen from outputs/screens/
/design-review [screen name or filename]    → Review a specific screen
/design-review --quick                      → UX + Accessibility only (fastest)
/design-review --full                       → All 5 agents (most thorough)
```

**What you get:** Structured feedback from 5 perspectives with prioritized action items.

---

# /design-review — Multi-Agent Design Review

## Context Check (Internal)

Before reviewing, load:
- The target screen file from `outputs/screens/`
- Design brief from `outputs/design-briefs/` (to validate against stated goals)
- Brand guidelines from `context-library/brand/`
- Personas from `context-library/personas/`

---

## The 5 Reviewers

### Reviewer 1: UX Researcher
**Agent file:** `sub-agents/ux-researcher.md`

Evaluates from the user's perspective:
- Does the flow match how users actually think?
- Are there cognitive load issues?
- What will first-time users struggle with?
- What research evidence supports or contradicts this design?

**Output structure:**
```
✅ What works
⚠️ UX concerns (numbered, prioritized by severity)
💡 Suggestions
❓ Questions to validate with users
```

---

### Reviewer 2: Accessibility Auditor
**Agent file:** `sub-agents/accessibility-auditor.md`

Evaluates WCAG 2.1 AA compliance:
- Color contrast ratios (text and UI elements)
- Keyboard navigability
- Screen reader support (semantic HTML, ARIA)
- Touch target sizes (44px minimum)
- Focus indicators visible
- Animation/motion safety (prefers-reduced-motion)
- Form accessibility (labels, errors, instructions)

**Output structure:**
```
✅ Passes
❌ Failures (WCAG criterion + severity: critical/major/minor)
💡 Fixes (specific code suggestions)
```

---

### Reviewer 3: Engineer
**Agent file:** `sub-agents/engineer-feasibility.md`

Evaluates technical implementation:
- Component reusability (can this be extracted cleanly?)
- CSS complexity (is this maintainable?)
- Performance concerns (heavy animations, large assets)
- Responsive implementation complexity
- Component library alignment (can shadcn/Tailwind handle this?)
- Animation/interaction feasibility

**Output structure:**
```
✅ Easy to implement
⚠️ Implementation concerns
💡 Technical suggestions
🔴 Blockers (things that would require significant engineering effort)
```

---

### Reviewer 4: Brand Guardian
**Agent file:** `sub-agents/brand-guardian.md`

Evaluates brand consistency:
- Color usage vs brand guidelines
- Typography matches brand voice
- Spacing and visual density feels consistent with brand
- Component style aligns with existing product
- Tone of copy matches brand voice

**Output structure:**
```
✅ On-brand
⚠️ Brand deviations
💡 Corrections
```

---

### Reviewer 5: End User Voice
**Agent file:** `sub-agents/end-user-voice.md`

Simulates the target user's first impression:
- "My first reaction when I see this screen is..."
- "I'm confused about..."
- "I'm not sure how to..."
- "I love that..."
- "I wish it..."

**Output structure:**
```
First impression (1-2 sentences as the user)
😍 Moments of delight
😕 Moments of confusion
🤔 Questions I have as a user
💬 What I'd tell a friend about this screen
```

---

## Review Output Format

Assemble the final review using the exact section structure and template in [REFERENCE.md](REFERENCE.md#review-output-format) — one numbered section per reviewer that ran, then Synthesis and Recommended Actions.

**Save to:** `outputs/design-reviews/[screen-name]-review.md`

---

## After Review

```
Review complete. [N] concerns found across [N] perspectives.

Critical issues: [N]
High priority: [N]
Nice to have: [N]

Want me to:
1. Apply all critical fixes to the screen file now
2. Generate a revised version with your feedback applied
3. Break the priority fixes into specific tasks
```
