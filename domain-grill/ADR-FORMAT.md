# ADR Format

ADRs (Architecture Decision Records) live in `docs/adr/` and use sequential numbering: `0001-slug.md`, `0002-slug.md`, etc.

Create the `docs/adr/` directory lazily — only when the first ADR is needed.

## Template

```md
# {Short title of the decision}

{1-3 sentences: what's the context, what did we decide, and why.}
```

That's it. An ADR can be a single paragraph. The value is in recording **that** a decision was made and **why** — not in filling out sections.

## Optional sections

Only include these when they add genuine value. Most ADRs won't need them.

- **Status** frontmatter (`proposed | accepted | deprecated | superseded by ADR-NNNN`) — useful when decisions are revisited
- **Considered Options** — only when the rejected alternatives are worth remembering
- **Consequences** — only when non-obvious downstream effects need to be called out

## Numbering

Scan `docs/adr/` for the highest existing number and increment by one.

## When to create an ADR (during a domain-grill session)

All three must be true:

1. **Hard to reverse** — meaningful cost to change later
2. **Surprising without context** — a future reader will wonder why
3. **Result of a real trade-off** — genuine alternatives existed

If any criterion is missing, skip. Do not pad the ADR log.

### What qualifies

- **Architectural shape.** "We're using a monorepo." "The write model is event-sourced; the read model is projected into Postgres."
- **Integration patterns between contexts.** "Ordering and Billing communicate via domain events, not synchronous HTTP."
- **Technology choices that carry lock-in.** Database, message bus, auth provider, deployment target. Not every library — only the ones that would take a quarter to swap out.
- **Boundary and scope decisions.** "Customer data is owned by the Customer context; other contexts reference it by ID only."
- **Deliberate deviations from the obvious path.** "We're using manual SQL instead of an ORM because X."
- **Constraints not visible in the code.** "We can't use AWS because of compliance requirements."
- **Rejected alternatives when the rejection is non-obvious.**
