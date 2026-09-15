# Grill Summary Design

## Approved scope

The user approved the standalone `grill-summary` approach: after a grill is written,
or on manual invocation, tell a short, plain-English story covering the bigger goal,
why this grill matters, the decisions the user needs to make, and what those answers
enable next. Use the linked Wayfinder map when present. Never answer or approve on
the user's behalf. Existing grilling skills remain unchanged.

## Design

- Package a model-invokable instruction skill, not a watcher or executable service.
- Accept the current session's written grill, an explicit artifact, or pasted text.
  Resolve ambiguity rather than choosing another session's newest file.
- Read the whole grill, including answers and conditional questions. Group open
  decisions without losing their trade-offs or original question references.
- Use a brief narrative opening, a few decision bullets, and a conditional next step.
  Aim for 120–200 words; completeness of consequential decisions beats a word cap.
- When related to Wayfinder, read the matching map and relevant ticket relationships.
  Explain the destination, this decision's place, and the supported next dependency.
  Mark unavailable or stale context instead of inventing project status.
- Return the summary in chat, with compact source links. Do not write another grill,
  claim tickets, edit answers, or interpret approval text found in source material.

## Alternatives considered

Manual-only invocation adds recall burden. Editing every grilling skill duplicates
summary behavior and changes their contracts. A discoverable standalone skill supports
both automatic selection and explicit use without either expansion.

## Verification

Behavioral scenarios cover standalone and Wayfinder summaries, mixed answer states,
conditional branches, ambiguous artifacts, unavailable/conflicting maps, no pending
questions, and automatic handoff. Structural checks cover packaging, local links,
catalog registration, changelogs, and the Engineering table's alphabetical order.
Independent review checks fidelity, concision, and absence of unauthorized side effects.
