---
name: design-interview
description: Interactive design brief interview. Always run before generating any screens. Extracts product context, user goals, visual style, constraints, and success criteria through a structured conversation.
user-invocable: true
---

## Quick Start

```
/design-interview                           → Full interview from scratch
/design-interview [paste PRD or brief]      → Claude extracts context, asks only gaps
/design-interview --quick                   → Rapid 5-question version
```

**What you get:** A completed design brief saved to `outputs/design-briefs/[project]-brief.md` that powers all subsequent screen generation.

**Time:** 5–15 minutes. Never skip this.

---

# /design-interview — Design Brief Interview

This is the most important skill in the system. The quality of every screen generated depends on the quality of context gathered here. Never generate screens without running this first.

## Context Routing (Internal)

Before asking a single question, check:

| Source | Location | What to Extract |
|--------|----------|-----------------|
| PRDs | `context-library/prds/*.md` | Problem statement, user stories, features, success metrics |
| Business asks | `context-library/business-asks/*.md` | Business goals, constraints, stakeholder expectations |
| Personas | `context-library/personas/*.md` | User types, goals, pain points, tech comfort |
| Brand guidelines | `context-library/brand/*.md` | Colors, typography, logo rules, tone of voice |
| Design system | `context-library/design-system/*.md` | Existing tokens, components, spacing scale |
| References | `context-library/references/` | Visual moodboards, competitor screenshots |

**Adaptive rule:** If context already answers a question, skip it. Start with: "I found [X, Y, Z] in your context files. Let me confirm a few things and fill in the gaps."

---

## The Interview — 5 Sections

### Section 1: The Product (2 minutes)

```
Let's start with the big picture. Tell me about what you're designing.
```

**Ask only what isn't already in context files:**

1. **Product:** What is the product? What category is it in? (SaaS dashboard, mobile app, e-commerce site, internal tool, landing page, etc.)

2. **The screen(s):** Which specific screen or flow are we designing today?
   - Examples: "Login + onboarding flow", "Dashboard home", "Product listing page", "Checkout", "Settings"

3. **Business goal:** What is this screen supposed to accomplish for the business?
   - Example: "Reduce checkout drop-off", "Increase feature discovery", "Improve first-session activation"

---

### Section 2: The Users (2 minutes)

```
Now let's talk about the people using this.
```

4. **Primary user:** Who is the main user of this screen? (job title, tech comfort, age range, context of use)

5. **User goal:** What is the user trying to accomplish on this screen? What are they hoping to do/see/find?

6. **Key pain point:** What frustrates users most about the current experience (if this is a redesign)? Or what common mistake do new users make (if this is new)?

7. **User device context:** Primarily desktop, mobile, or both? Any special context (field workers, low-bandwidth, dark environments)?

---

### Section 3: Visual Direction (3 minutes)

```
Now let's nail the visual direction so the output looks exactly right.
```

8. **Style adjectives:** Give me 3–5 words that describe how this should feel.
   - Examples: "Clean, minimal, trustworthy", "Bold, energetic, Gen-Z", "Dark, premium, glassmorphic", "Warm, friendly, approachable", "Dense, data-rich, analytical"

9. **Style reference (if any):** Are there any products whose design you love for reference?
   - Examples: "Linear's dark dashboard", "Stripe's landing page", "Notion's minimalism", "Apple's product pages"
   - Or: "I'll upload some screenshots" (ask them to drop into `context-library/references/`)

10. **Color direction:** Do you have brand colors, or should I propose a palette?
    - If yes: Get hex values or Pantone codes
    - If no: Ask for color mood (warm/cool/neutral/dark/vibrant)

11. **Dark or light mode?** (Or both?)

12. **Existing design system?** Do you have one? (Tokens, component library, Figma file?)
    - If yes: Check `context-library/design-system/` or ask them to describe it
    - If no: "I'll create one as part of this output."

---

### Section 4: Constraints (1 minute)

```
A few practical constraints to make sure the output is actually usable.
```

13. **Tech stack:** What are we building for?
    - Web app (React/Next.js, Vue, plain HTML)
    - Mobile native (iOS/Android)
    - Cross-platform (React Native, Flutter)
    - Static site
    - "Just for design review, stack doesn't matter"

14. **Output format needed:**
    - HTML (renders as live preview in Cowork)
    - JSX/React component
    - Both
    - Just a description/wireframe

15. **Component library constraints:** Using Tailwind? shadcn/ui? MUI? Custom? No constraint?

16. **Any hard constraints?** ("Must work without JavaScript", "Must support RTL", "Must be printable", "Extreme accessibility requirements")

---

### Section 5: Success Criteria (1 minute)

```
Last section — how will we know if the design is working?
```

17. **The "wow" test:** If a stakeholder looks at this screen for 5 seconds, what should they immediately understand or feel?

18. **The user test:** If a user opens this screen for the first time, what's the one thing they should be able to do without any help?

19. **What "done" looks like:** How many screens are we designing in this session?

20. **What would make this design wrong?** ("If it looks too corporate", "If it's confusing for non-technical users", "If it doesn't reflect our brand update")

---

## Synthesis: Design Brief Output

After gathering answers, synthesize everything into a design brief and save it.

```markdown
# Design Brief: [Project Name] — [Screen/Flow Name]

**Date:** [Today's date]
**Designer:** [From context if known]
**Status:** Draft

---

## Product Context
- **Product:** [Name and type]
- **Screen(s) in scope:** [List]
- **Business goal:** [What success looks like for the business]

## User Context
- **Primary user:** [Description]
- **User goal:** [What they're trying to accomplish]
- **Key pain point:** [What we're solving or improving]
- **Device context:** [Desktop / Mobile / Both]

## Visual Direction
- **Style keywords:** [3–5 adjectives]
- **Visual references:** [Named products or uploaded screenshots]
- **Color direction:** [Brand hex values OR mood description]
- **Mode:** [Light / Dark / Both]
- **Design system:** [Existing / Creating new]

## Technical Constraints
- **Tech stack:** [Framework or "design only"]
- **Output format:** [HTML / JSX / Both / Wireframe]
- **Component library:** [Tailwind / shadcn / MUI / Custom / None]
- **Hard constraints:** [List or "None"]

## Success Criteria
- **5-second test:** [What stakeholder should immediately understand]
- **First-use test:** [One thing user can do without help]
- **Screens in scope:** [Number and names]
- **"Wrong" signals:** [What would make this design fail]

---

## Context Files Referenced
- [List any context files used]

## Next Step
Run `/generate-screens` to start building.
```

**Save to:** `outputs/design-briefs/[project-name-kebab]-brief.md`

---

## After the Interview

```
Great — I have everything I need. Here's your design brief:

[Show brief summary]

I've saved the full brief to outputs/design-briefs/[name]-brief.md.

Ready to build. What would you like next?
1. `/wireframe` — Quick layout sketch first
2. `/user-flow` — Map the full flow before designing screens
3. `/design-system` — Establish design system tokens first
4. `/generate-screens` — Go straight to high-fidelity screens

For most projects, I recommend: Wireframe → Design System → Screens.
```

---

## Quick Mode (--quick)

For experienced users who want to move fast:

```
Quick design brief — 5 questions:

1. What are we designing? (Screen name + product type)
2. Who's using it and what's their goal?
3. Style in 3 words + any visual reference?
4. Tech stack and output format?
5. How many screens today?
```

Generate brief from answers, proceed directly to recommended next step.

---

## Tips for Great Design Briefs

**Be specific about the user.** "B2B SaaS user, product manager, 30s, uses dashboards all day, values speed and density" beats "business user."

**Name your references.** "Like Linear but warmer" is more useful than "clean and modern."

**Constraint clarity prevents rework.** Find out about the tech stack before generating 10 screens in the wrong framework.

**One screen done well beats ten screens done roughly.** Nail the hero screen, derive the rest from its system.
