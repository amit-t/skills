# CONTEXT.md Format (read reference)

`/domain-grill` reads `CONTEXT.md` but does not write to it. This file describes the format the skill expects so it can parse term definitions, relationships, and flagged ambiguities correctly.

`/repo-context-scan` is the canonical writer of this format.

## Structure

```md
# {Context Name}

{One or two sentence description of what this context is and why it exists.}

## Language

**Order**:
A customer's request to purchase one or more items.
_Avoid_: Purchase, transaction

**Invoice**:
A request for payment sent to a customer after delivery.
_Avoid_: Bill, payment request

**Customer**:
A person or organization that places orders.
_Avoid_: Client, buyer, account

## Relationships

- An **Order** produces one or more **Invoices**
- An **Invoice** belongs to exactly one **Customer**

## Example dialogue

> **Dev:** "When a **Customer** places an **Order**, do we create the **Invoice** immediately?"
> **Domain expert:** "No — an **Invoice** is only generated once a **Fulfillment** is confirmed."

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — resolved: distinct concepts.
```

## Single vs multi-context repos

**Single context:** One `CONTEXT.md` at the repo root.

**Multiple contexts:** A `CONTEXT-MAP.md` at the repo root lists each context and its location:

```md
# Context Map

## Contexts

- [Ordering](./src/ordering/CONTEXT.md) — receives and tracks customer orders
- [Billing](./src/billing/CONTEXT.md) — generates invoices and processes payments
- [Fulfillment](./src/fulfillment/CONTEXT.md) — manages warehouse picking and shipping

## Relationships

- **Ordering → Fulfillment**: Ordering emits `OrderPlaced`; Fulfillment consumes
- **Fulfillment → Billing**: Fulfillment emits `ShipmentDispatched`; Billing consumes
```

When grilling against a multi-context repo:

- Identify which context(s) the artifact touches before challenging terminology.
- Cross-context contradictions are first-class targets — flag them aggressively.
- If a context boundary is unclear, ask the user before assuming.

## Reading rules

- Bold tokens (`**Order**`) inside the Language section define canonical terms.
- The `_Avoid_` line lists deprecated or aliased synonyms — flag the artifact if it uses any of these.
- The Relationships section is the source of truth for cardinality — challenge artifacts that contradict it.
- The Flagged ambiguities section records past resolutions — refuse to re-litigate unless the user explicitly opens the question.
