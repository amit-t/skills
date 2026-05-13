# session-feedback output template

The skill writes a file in this shape. Frontmatter is required (the auto-memory loader uses it).

```markdown
---
name: feedback_session_<topic-slug>
description: <one-line on what this session was about and when to reload>
type: feedback
---

# Session feedback — <topic> (<YYYY-MM-DD>)

Distilled from <N-round> <grill | design | review | debug> session where <user-name> drove <short scope>.

---

## Corrections you made

1. **<Short title>** *(<context locator, e.g. Q3 / file X / round 2>)*
   - I proposed: <agent's recommendation>
   - You changed: <user's redirect, ideally a near-verbatim quote>
   - **Lesson:** <general principle, not local fix>

...

---

## Preferences you stated

- **<bold preference>** — <one-sentence context, citation if any>
- ...

---

## What I'd do differently next time

1. <Principle stated as an instruction to future-me>
2. ...

---

## Memory entries created/updated this session

- [<file>](<file>) — <what it captures>

---

## When to reload this file

- <Trigger condition 1>
- <Trigger condition 2>
```

## Notes on the template

- **Frontmatter `type: feedback`** is mandatory — it tells the auto-memory loader this is reusable behavioural guidance, not a one-shot session log.
- **Topic-slug** in `name` should be 2–4 words, kebab-case, durable enough to grep against in 6 months (e.g. `code_review_grill`, `db_migration_review`).
- **Corrections** are the highest-value bucket — preserve the user's actual words. The phrasing they used encodes the principle better than your summary will.
- **"Do differently"** entries must be general principles. Each one should be applicable to multiple future situations, not just the one that triggered it.
- **"When to reload this file"** is what makes the entry resurface usefully — be specific about trigger conditions so the auto-memory system can match.

## Append mode (same-day re-run)

If the file already exists for today and `--overwrite` is not passed, append the new content under a sub-section heading:

```markdown
## <YYYY-MM-DD HH:MM> — <new-topic>

(same three buckets, scoped to the most recent slice of the session)
```

Do not re-emit the frontmatter on append; only the most recent invocation's content.
