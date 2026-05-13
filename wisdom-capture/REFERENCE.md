# Wisdom Capture — Reference

## Categorization output schema

When you propose a category, structure your internal reasoning as:

```json
{
  "primary": "<key from _categories.yml>",
  "confidence": "high | med | low",
  "tags": ["string", "string"],
  "reason": "<one sentence>",
  "new_bucket_proposal": null | {
    "key": "<snake_case>",
    "label": "<Human Readable>",
    "color": "<one of color_pool unused>",
    "reason": "<why existing buckets don't fit>"
  },
  "second_best": "<key from _categories.yml different from primary>"
}
```

## Frontmatter rendering rules

- YAML scalars: quote with double quotes only when value contains `:`, `#`,
  `>`, `|`, leading `-`, leading `?`, or newline.
- `created_at` / `updated_at`: ISO 8601 with `Z` suffix, second precision.
- `tags`: inline flow style — `tags: [a, b, c]` — not block style.
- Empty optional strings: `""` (do not omit the key).
- Null URL / author: literal `null`.

Example:

```yaml
---
id: 01jabcdefghjkmnpqrstvwxyz0
created_at: 2026-05-13T14:32:00Z
body_hash: a3f5c2e1b89...
category: engineering
tags: [debugging, systems]
source_url: https://hickeyhq.com/quote/123
source_author: Rich Hickey
note: ""
import_origin: manual
---

Programming is not about typing, it's about thinking.
```

## Commit message body limits

Subject line: max 72 chars after `wisdom: <category> — ` prefix. If the body
preview must be truncated, end with `…` (single U+2026, not three dots).

## Push policy state

`.wisdom-session` is a single line, one of: `y` | `n` | `always` | `never`. It
is gitignored and may be deleted between sessions. Treat its absence as "ask".

## Engine-specific notes

- **Claude:** The Skill tool loads this file directly. You see this content as
  in-session instruction.
- **Codex:** Read at session start via AGENTS.md or the `$wisdom` prefix
  trigger. Codex may not surface YAML files; in that case the user pastes the
  snippet, and Codex follows the same flow from instruction.
- **Devin:** Triggered via `/wisdom`. Devin's tool surface includes file write
  + shell, which is all this flow needs.
