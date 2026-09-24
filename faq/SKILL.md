---
name: faq
description: Use when the user invokes /faq with a question, forwards a question someone asked about the current repo, or says "add this to the FAQ". Answers the question from the repo's source of truth and records it in the repo's FAQ document.
category: Engineering
disable-model-invocation: true
user-invocable: true
---

# /faq — Answer a Question and Record It in the Repo FAQ

Turn a real question about the current repo into (1) an immediate answer in chat and (2) a permanent FAQ entry in the repo's docs. Works in any repo; no per-repo setup.

## Inputs

- **question** (from args or the message): the question to answer. Often pasted verbatim from a teammate (Slack/Teams/email). If absent, ask for it and stop.
- **--dry-run**: answer in chat and show the proposed entry, but do not write the file. Report in conditional language ("would add", "would update"), never claim a write happened. When several dry-run questions run in one session, check later questions against earlier proposed entries too, not just the on-disk file.

## Step 1 — Locate the FAQ document

Check in order, first hit wins:

1. `docs/faq.md`
2. `docs/FAQ.md`
3. `FAQ.md`
4. `docs/faq/index.md`

On case-insensitive filesystems (macOS, Windows) several candidates resolve to one file; write to the **git-tracked casing** (`git ls-files docs/ | grep -i faq`).

None found → create `docs/faq.md` (or `FAQ.md` if the repo has no `docs/`). Match sibling conventions: if other files in the same directory carry YAML front matter (Jekyll/MkDocs), copy their front-matter shape (`title: FAQ`, same `layout`); otherwise start with a plain `# FAQ` heading.

## Step 2 — Detect structure and check for an existing entry

Detect which of two layouts the FAQ uses:

- **Flat**: every `##` heading is a question.
- **Categorized**: `##` headings are category names (short noun phrases, not questions) and `###` headings under them are the questions.

Read all question headings (whichever level they are). If one already covers the question (same topic, not just similar words), **update that entry** instead of adding a duplicate, and tell the user you updated rather than added. If the existing entry already answers the question fully and accurately, change nothing: report the existing heading and give the answer in chat. Never churn a correct entry to justify an "update".

## Step 3 — Answer from source of truth

Research before writing. Priority: code and scripts > committed docs > your own memory. Quote exact flag names, file paths, defaults, and enums from the source. If the honest answer is "not supported" or "undefined behavior", say that; never invent an answer to have something to record.

If the question came from a named person, the FAQ entry must not name them. The entry is the distilled question, not the correspondence.

## Step 4 — Write the entry

Format, matching the existing FAQ voice and the detected structure (question heading is `##` in a flat FAQ, `###` in a categorized one):

```markdown
### <Question rewritten as one clean question ending in ?>

<Dense answer. Lead with the direct answer, then the one or two facts
that prevent the follow-up question. Link related docs with relative
links. No greeting, no restating the question in the body.>
```

Heading rewrite: keep the asker's substance and key terms (they are what the next person searches for); rewrite only for clarity, drop filler words.

Placement, flat FAQ: insert next to entries on the same topic; when no clear neighbor exists, append at the end. Never reorder existing entries.

Placement, categorized FAQ: put the entry under the best-fitting existing `##` category (last position in that category). When no existing category fits, add a new `##` category named as a short noun phrase consistent with the others, at the end, and tell the user you created it. Never file a question under a stretched category to avoid creating one.

## Step 5 — Report

Reply in chat with:

1. The answer itself (the user usually needs to forward it).
2. The FAQ file path and the new/updated heading.

Do **not** commit or push unless the user asks.

## Rules

- One question per entry. A multi-part question becomes multiple entries only if the parts are independently searchable; otherwise one entry answering all parts.
- Entry headings are questions, not topics: "Can I rename the workbench repo?" not "Repo renaming".
- Keep answers current-state only, no changelog narration ("previously this was...").
- Respect repo writing rules (e.g. banned words, dash conventions) from its CLAUDE.md / AGENTS.md.

## Common mistakes

| Mistake | Fix |
|---|---|
| Answering from memory when the code is right there | grep the script/config first; quote exact values |
| Adding a duplicate entry with different wording | Step 2: update the existing entry |
| Copying the asker's rambling phrasing into the heading | Rewrite as one clean question |
| Committing automatically | Write the file, stop; committing is the user's call |
| Creating `docs/faq.md` without front matter in a Jekyll docs dir | Match sibling files' front matter |
