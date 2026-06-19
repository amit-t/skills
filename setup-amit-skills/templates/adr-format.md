# ADR format

ADRs live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

## Template

```md
# {Short title of the decision}

{1-3 sentences: context, decision, and why.}
```

## Create an ADR only when all three are true

1. **Hard to reverse** — meaningful cost to change later.
2. **Surprising without context** — a future reader would wonder why.
3. **Result of a real trade-off** — genuine alternatives existed.

If any criterion is missing, skip the ADR.
