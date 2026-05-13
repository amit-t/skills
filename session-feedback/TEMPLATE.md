# session-feedback output template

The skill writes a file in this shape. Frontmatter is required (the auto-memory loader uses it). Items are recorded as durable candidates — they are not pre-filtered at write time. The carry-forward gate fires in **recall mode** (see `SKILL.md`) when a future session is about to reference an item.

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

1. **C1** **<Short title>** *(<context locator>)*
   - I proposed: <agent's recommendation>
   - You changed: <user's redirect, ideally a near-verbatim quote>
   - **Lesson:** <general principle, not local fix>

2. **C2** **<Short title>** ...

---

## Preferences you stated

- **P1** **<bold preference>** — <one-sentence context, citation if any>
- **P2** ...

---

## What I'd do differently next time

1. **D1** <Principle stated as an instruction to future-me>
2. **D2** ...

---

## Memory entries created/updated this session

- [<file>](<file>) — <what it captures>

---

## When to reload this file

- <Trigger condition 1>
- <Trigger condition 2>
```

## Conventions for this schema

- **Stable IDs.** `C` for corrections, `P` for preferences, `D` for do-differently. Numbered within bucket. Once assigned, the ID never changes — append-mode runs allocate fresh IDs (`C7`, `P12`, etc.).
- **No checkboxes at write time.** Items are durable candidates. A future session decides per-reference whether each one still applies (see `SKILL.md` → Recall mode).
- **One-line hook per entry.** The bolded title plus the lesson sentence must be readable cold — recall mode lists items in this exact compact form.
- **Frontmatter `type: feedback`** is mandatory — auto-memory loader treats this as reusable behavioural guidance.
- **`topic-slug`** in `name` is 2–4 words, kebab-case, durable enough to grep against in six months.

## Notes on the buckets

- **Corrections** are the highest-value bucket — preserve the user's actual words. The phrasing encodes the principle better than your summary will.
- **Preferences** capture absolutes ("always", "never", cited authorities, process beliefs).
- **Do differently** entries must be general principles. Each should apply to multiple future situations, not just the one that triggered it.

## Append mode (same-day re-run)

If the file already exists for today and `--overwrite` is not passed, append the new content under a sub-section heading:

```markdown
## <YYYY-MM-DD HH:MM> — <new-topic>

(same three buckets, with fresh IDs continuing the numbering — e.g. C7, P12, D5)
```

Do not re-emit the frontmatter on append; only the most recent invocation's content. IDs continue the existing sequence so recall mode can address every item unambiguously across runs.
