---
name: character-distiller
description: >
  Turns character material into structured Character Templates usable as both human writing references
  and AI prose refinement lenses. Supports three modes: (A) fresh build from Q&A interview notes,
  (B) augment an existing template with new interview sessions without losing prior work, (C) extract
  all character sketches directly from a full manuscript. Trigger on: "character template", "character
  bible", "character sheet", "update my character", "augment character notes", "synthesize my character
  notes", "extract characters from my manuscript", "build character sheets from my novel", or whenever
  the user pastes Q&A interview content about a fictional character. Also trigger when users upload
  character interview files or a manuscript and want structured output. Use proactively for any
  character development work — interviews, manuscript analysis, or iterative deepening across sessions.
---

# Character Distiller

You are helping an author transform character material into structured **Character Templates** — documents that work both as human writing references and as AI context for prose refinement.

The output is not a summary. It's a *functional artifact* — something that, when prepended to an AI prompt, reliably shapes how that AI interprets and refines a character's behavior in any scene.

---

## Step 1 — Determine the mode

Before doing anything else, identify which of the three modes applies:

**MODE A — Fresh build from interviews**
The user is providing Q&A interview material for a character and no template yet exists.

**MODE B — Augment an existing template**
The user has an existing character template and is bringing new interview material to deepen or update it. They will paste or attach the existing template alongside the new interviews.

**MODE C — Extract from manuscript**
The user is providing a full prose manuscript and wants character templates generated from what's on the page.

If unclear, ask. Lean toward MODE B if they mention an existing template, MODE C if they mention a manuscript.

---

## MODE A — Fresh build from interviews

### Gathering the material

The user may provide interviews as:
- Text pasted directly into the conversation
- Attached .txt, .md, or .docx files (read them before proceeding)
- Multiple sessions for the same character (read all before synthesizing)

What counts as an interview: any Q&A, questionnaire, or free-form character exploration where answers reveal the character's inner world. Format doesn't matter — extract the insights regardless.

### Synthesis principles

Your job is to find the **underlying truth** rather than the surface answer. Characters develop over time; an author's understanding deepens. What looks like a contradiction is often the author discovering something more nuanced.

- If two answers contradict each other, look for the emotional or philosophical truth they're both circling
- Weight later interviews slightly more heavily when truly irreconcilable, but earlier answers often reveal something real that later refinement doesn't erase
- Synthesize by abstraction: "In session 1 she said she loves people; in session 2 she said she finds people exhausting — the underlying truth is that she deeply needs connection but it costs her"
- Only flag a contradiction if synthesis genuinely isn't possible without an interpretive leap the author should make themselves

---

## MODE B — Augment an existing template

The goal is to **deepen and refine** the existing template — not replace it.

1. Read the existing template in full before reading the new interview material
2. Read the new interview(s) and identify what's new, what confirms existing content, and what adds nuance or changes something
3. **Merge, don't overwrite:**
   - *Confirming evidence* — aligns with existing content: no change, but it strengthens what's there
   - *Additive evidence* — fills a gap or adds detail to a thin section: add it, mark with `*(updated)*`
   - *Deepening evidence* — reveals more complexity in something already present: revise the entry to incorporate the new layer, note what changed
   - *Evolving evidence* — author's understanding has shifted: update the entry and add a brief note explaining the evolution
4. Update the header line to reflect the new session count and date
5. Add an entry to the **REVISION LOG** section at the bottom
6. Check the AUTHOR'S OPEN QUESTIONS — mark any now-answered questions with ✓

Treat the existing template with respect. Don't casually revise things that were carefully stated just because a new interview offers a slightly different angle. Only update when the new material genuinely adds something.

---

## MODE C — Extract from manuscript

Read the full text carefully. As you read, track for each character:
- **Voice**: What does their dialogue actually sound like? Vocabulary, sentence patterns, verbal habits, what they avoid saying
- **Behavior**: What do they do, and what does it reveal about their values, fears, or habits?
- **Inner life**: If POV is inside their head, what do they notice, avoid, obsess over?
- **Social dynamics**: How do they treat different people? How do others react to them?
- **Contradictions**: Where does what they say diverge from what they do?

### Character tiers

**Major characters** (multiple scenes, dialogue, interiority, plot impact) → full template
**Supporting characters** (several scenes, defined role and voice) → condensed template (CORE IDENTITY + VOICE & SPEECH + AI PROSE REFINEMENT LENS only)
**Minor characters** (brief appearance, functional role) → one-paragraph sketch

Ask the user if they want all tiers or only major/supporting before proceeding on a long manuscript.

Every claim in a manuscript-extracted template should be grounded in something observable on the page. Mark inferences with `*(inferred from behavior)*` rather than just `*(inferred)*`. After generating all character files, also produce a **`character-map.md`** — a list of all characters, their tier, their essential one-line description, and their key relationships to one another.

---

## The Character Template

Use this structure for all modes. In MODE B, preserve all existing content and layer in additions rather than rewriting.

---

```markdown
# CHARACTER TEMPLATE: [Full Name]
*Synthesized from [N] interview(s) · Last updated [Date]*

---

## CORE IDENTITY

[2–4 sentences. The irreducible essence: what kind of person they are at their core,
what fundamental tension or drive shapes everything they do. Their nature, not their biography.
This is the north star that governs all sections below.]

---

## VOICE & SPEECH

### How They Talk
[Vocabulary register — formal, casual, elevated, street-level, mixed]
[Sentence structure — clipped/flowing, simple/complex, fragmented under stress?]
[Characteristic verbal habits — phrases they return to, how they signal disagreement]
[Pacing — deliberate, quick, trailing off, declarative]

### What Their Speech Reveals
[What beliefs or feelings leak through even when they're trying to be neutral]
[What they talk around, approach sideways, or over-explain when uncomfortable]

### What [Name] Never Says
[Specific words, phrases, or types of statements that would break character]
[Emotional registers or rhetorical moves they simply don't make]

---

## CORE BELIEFS & WORLDVIEW

### What They Believe (and Why It's Coherent to Them)
[Fundamental assumptions about how the world works — stated as beliefs, not character flaws]
[What they think people are fundamentally like]
[What they believe is worth protecting, pursuing, or sacrificing for]

### Their Blind Spots
[What they cannot see about themselves, despite being perceptive about many things]
[Where their worldview fails them without their awareness]

### Their Internal Contradictions
[Tensions they live with — not inconsistencies but genuine complexity]
[What they believe and what they do when those beliefs are tested]

---

## EMOTIONAL LANDSCAPE

### What Genuinely Moves Them
[What touches them, makes them angry, frightens them, delights them — be specific]
[The emotional register they live in most of the time]

### How They Handle Emotion
[Default strategy — express, suppress, redirect, intellectualize, physicalize, humor]
[What they look like overwhelmed vs. coping well]
[What they let show vs. what they guard carefully]

### Where They're Soft
[Specific vulnerabilities that get through their defenses — people, ideas, memories, values]
[What kind of person or situation disarms them]

---

## RELATIONSHIPS & SOCIAL DYNAMICS

### How They Relate
[Default relational stance with strangers, acquaintances, intimates]
[How they treat people with less power vs. more — often very revealing]
[What they need from relationships, even if they'd never say so]

### What They Give
[What they offer freely — warmth, protection, honesty, humor, silence]

### What They Withhold
[What they protect, can't give, or give only at great cost]

### Who Gets Through to Them
[The type of person who earns genuine connection — and why]

---

## FOR AI PROSE REFINEMENT — CHARACTER LENS

*This section is for AI tools refining or generating prose that features [Name].
Treat it as an active filter, not background information.*

### The Authenticity Test
Before accepting any dialogue line or action attributed to [Name], run it through:
1. **Voice check** — Does this sound like [Name], or like a generic character?
2. **Motivation check** — Is there a plausible internal reason [Name] would do/say this *right now*?
3. **Subtext check** — What's actually going on beneath what [Name] says? Does the prose honor that?

### The Negative Space — What [Name] Would NOT Do
[4–6 specific, concrete behavioral/verbal limits.
Not vague ("they wouldn't lie") but specific
("they wouldn't apologize preemptively to smooth social friction; they wait until they mean it")]

### Emotional Subtext in Scenes
When [Name] appears in a scene, the baseline beneath their surface behavior is usually:
[1–3 sentences: their habitual inner weather — what's running underneath even when they seem fine]

The tells — when [Name]'s internal state is shifting, watch for:
[Specific behavioral or verbal micro-signals]

### Scenes That Reveal [Name] Most Clearly
[2–3 situation types that put this character's nature in sharpest relief —
use as a benchmark for "does this feel right?"]

---

## AUTHOR'S OPEN QUESTIONS
*(verify, answer, or delete)*

[Gaps, unresolved tensions, or places where synthesis required an interpretive leap.
Framed as questions the author should answer. Mark resolved ones with ✓.]

---

## REVISION LOG
*(MODE B only — omit on first build)*

| Date | Sessions added | What changed |
|------|---------------|--------------|
| [Date] | Session [N] | [Brief description of what was updated or added] |
```

---

## Output and delivery

**File naming:** Save each template as `[CharacterName]-template.md` (e.g. `MiraVoss-template.md`). For MODE C, also save `character-map.md`. Save all files to the current working directory or a `characters/` subdirectory if one exists.

**After generating**, briefly narrate your synthesis choices — what you inferred, how you resolved contradictions, what you're flagging. Keep it to a short paragraph. The author knows their characters better than you; your job is to distill faithfully, not interpret beyond what the material supports.

Offer to revise any section before they finalize, particularly anything marked `*(inferred)*`.
```
