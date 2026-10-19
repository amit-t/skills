# Skeletons for the two files

Fill these in; drop sections that have nothing in them. Write in the user's style rules.

## Project instructions (the rules)

```
[Project name]: project instructions
Updated: [YYYY-MM-DD]. Full detail lives in [path to context file].

Purpose
- What this project produces and for whom, in one or two lines.
- Who the user is, only if their role affects the work. Exclude other personal details.
- Read [context file] before any task.
- When asked to "do what you did for X", find the earlier output first: [where outputs live].

Writing rules (chat replies, docs and outputs)
- Sentence length, voice, person.
- Punctuation and formatting bans and what to use instead.
- Spelling variant, date format, title style.
- Banned words, as one line.

Accuracy rules
- How sources are read, cited and dated.
- How the user's own figures are labelled.
- How claims from sources are kept apart from your own analysis.
- What must be searched before stating it.
- Domain checks the user always wants (pricing, approvals, compliance, and so on).

How to run a task
- When to ask and when to start.
- How to handle scope that turns out larger.
- When to split work across subagents.
- What is read-only or private.
- How to finish: what was made, where, things to know.

Choosing the output
- [Kind of request]: [output type] ([Template letter]).
- Repeat per kind. Include length limits per audience.

Every output must
- The fixed elements every output carries.
```

## Project context (the facts)

```
[Project name]: project context
Updated: [YYYY-MM-DD]
Built from: [chats, docs, memory, outputs read, with counts and dates].
Read with: [instructions file].

1. Who this is for
- The user's role, only if it affects the work, and relevant work threads.
- People and teams who receive outputs.
- Constraints at their organisation that affect recommendations.

2. Sources
- Each source: who, how to find it (exact search queries, sender addresses, URLs), coverage so far, caveats about bias or staleness.
- Seen, not confirmed
- Assistant suggestions, inferred conventions, and other material not accepted by the user. Keep it out of rules and defaults. Do not invert an unaccepted suggestion into a ban.

3. Past outputs
- Every output: title, date, kind (Template letter), link or path.
- Outputs that moved or were replaced, and where their content now lives.

Known fixes still open
- Past outputs that break current rules or carry stale facts.

4. How past tasks were run
- The step order that worked, tool settings and queries that worked, checks run, what was confirmed at the end.

5. Templates
Shared rules for every output of this medium (theming, fonts source, breakpoints, icons, charts, footer).

Template A: [kind] ([source outputs])
- Use when:
- Fonts:
- Light tokens:
- Dark tokens:
- Layout and sizes:
- Section order:
- Components and label sets:
- Must-haves:

Template B: ...

6. Defaults when nothing is said
- Only defaults the user explicitly chose or consistently accepted, with their sources. Leave unknown defaults unspecified.
```
