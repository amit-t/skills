# Failure Modes — Diagnosing a Skill

Disclosed reference for [write-a-skill](SKILL.md): use it when a drafted skill misbehaves, or on the final checklist sweep. Each entry gives the mechanism and the cure; the positive practices themselves live in SKILL.md. Adapted from [writing-great-skills in mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/productivity/writing-great-skills).

## Premature completion

Ending a step before it is genuinely done, because the agent's attention slips to *being done* rather than to the work. A tug-of-war between visible **post-completion steps** (the later steps pull the agent forward) and the completion criterion's clarity (a sharp, checkable bar resists; a vague one — "until understanding is reached" — gives way). Defence, in order: **sharpen the completion criterion first** (cheap, local); only if it is irreducibly fuzzy *and* you actually observe the rush, hide the later steps by splitting the sequence across a real context boundary (a hand-off or subagent dispatch — an inline call leaves the later steps in context and clears nothing).

## Duplication

The same meaning given more than one home. Costs maintenance (change one place, you must change the others), costs tokens, and inflates the meaning's prominence past its real rank. It is the accidental inverse of a leading word, which raises attention on purpose by repeating a *token*, never the meaning. Cure: keep the sharper statement, replace the other with a pointer.

## Sediment

Stale layers that settle because adding feels safe and removing feels risky — references to removed files, outdated tool names, obsolete steps. The default fate of any skill without a pruning discipline. Cure: check every line for relevance — does it still bear on what the skill does? — and delete what fails.

## Sprawl

A skill simply too long, even when every line is live and unique. The agent wades through more before it can act, and attention thins across the excess. Cure: the information hierarchy — disclose reference behind context pointers, and split by branch or sequence so each path carries only what it needs. Do not fragment a short skill: each split spends context load (another always-loaded description) or cognitive load (another name the human must remember).

## No-op

An instruction the model already obeys by default, so you pay load to say nothing. The test: does this sentence change behaviour versus the default? Run it sentence by sentence, and when one fails, delete the whole sentence rather than trim words from it. The test also grades leading words: a word too weak to beat the default (*be thorough* when the agent is already thorough-ish) is a no-op, and the fix is a stronger word (*relentless*), not a different technique.

## Negation

Steering by prohibition backfires: *don't think of an elephant* names the elephant and makes it more available, not less — the ban half-reads as an instruction to do the thing. Cure: prompt the positive — state the target behaviour so the banned one is never spoken. A prohibition earns its place only as a hard guardrail you cannot phrase positively (security and data-loss caveats stay), and even then pair it with the positive target.

## Supporting vocabulary

- **Branch** — a distinct way a skill can be invoked, so different runs take different paths through it. One trigger per branch in the description; disclosure is licensed by what only some branches reach.
- **Context pointer** — an in-context reference that names out-of-context material and encodes the condition for reaching it. A must-have target behind a weakly worded pointer is a variance bug: fix the wording first; inline the material only if sharpening fails.
- **Legwork** — the digging an agent does within a step (reading files, exploring, changing code) rather than offloading to the user. Raised by a demanding completion criterion or a strong leading word; "every rule applied" binds flat reference just as "every step done" binds a sequence.
- **Router skill** — one user-invoked skill that names your other user-invoked skills and when to reach for each, so the human remembers one name instead of many. The cure when cognitive load piles up.
