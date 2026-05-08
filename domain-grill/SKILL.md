---
name: domain-grill
description: Engineering-only. Stress-tests an engineering artifact (eng spec, TDD plan, refactor proposal, architecture sketch, technical design, schema migration, API contract) against the project's CONTEXT.md. Reads CONTEXT.md read-only, interviews the user against existing terminology and decisions, surfaces conflicts, may add ADRs for new hard-to-reverse decisions. For PRDs, marketing plans, or any non-code artifact, refuse and redirect to /grill-me. Triggers include "grill this spec", "domain grill", "stress-test against CONTEXT", and "/domain-grill".
---

# Domain Grill

Interview-driven stress-test of an **engineering** artifact against the project's existing domain context.

## Scope guard (read first)

This skill is for **code and engineering artifacts only**. Acceptable inputs:

- Engineering specs
- TDD / test plans
- Refactor proposals
- Architecture sketches
- Technical design documents
- API contract proposals
- Schema migrations / data-model changes
- Infrastructure-as-code plans

**Refuse and redirect** if invoked for:

- Product Requirements Documents (PRDs)
- Marketing / business / strategy plans
- General-purpose plan reviews not anchored in code or schema
- Resume drafts, blog posts, product-level RFCs
- Anything that doesn't define or modify code, schema, infrastructure, or technical interfaces

The decision rule: *does this artifact define or modify code, schema, infrastructure, or technical interfaces?* If yes → proceed. If no → redirect.

Suggested redirect message:

> `/domain-grill` is engineering-only — it grills against `CONTEXT.md` and assumes a code-grounded artifact. For PRDs and non-technical artifacts, use `/grill-me` (same relentless interview, no code/CONTEXT coupling).

If the user insists despite the redirect, still refuse. The skill is intentionally narrow; broadening it dilutes its value.

## Prerequisites

- A `CONTEXT.md` (or `CONTEXT-MAP.md` for multi-context repos) must exist at the repo root or in the relevant module.
- If absent, run `/repo-context-scan` first, then return.

This skill is **read-only** for `CONTEXT.md`. It does not edit the file. If new domain terms surface during grilling, flag them at the end and recommend re-running `/repo-context-scan`. Ownership of `CONTEXT.md` belongs to that skill.

## Process

### 1. Load context

- Read `CONTEXT.md` (or `CONTEXT-MAP.md` plus the relevant per-context `CONTEXT.md` files).
- If multi-context, identify which context(s) the artifact touches. Ask the user if unclear.
- Read existing `docs/adr/*.md` so you can flag artifacts that contradict prior decisions.

### 2. Interview relentlessly

Walk every branch of the artifact's decision tree until you reach shared understanding. Rules:

- Ask **one question at a time**.
- For each question, provide your **recommended answer** alongside the question.
- Wait for the user's response before moving to the next.
- If a question can be answered by reading code, **read the code instead** of asking.

### 3. Challenge against the glossary

When the artifact uses a term that conflicts with `CONTEXT.md`, surface immediately:

> Your spec calls this a "cancellation", but `CONTEXT.md` defines cancellation as X. You seem to mean Y here — which is it?

### 4. Sharpen fuzzy language

When the artifact uses vague or overloaded terms, propose precise canonical alternatives:

> You say "account" — do you mean Customer or User? `CONTEXT.md` treats those as distinct concepts.

### 5. Stress-test with concrete scenarios

Invent edge-case scenarios that probe the boundaries of relationships defined in `CONTEXT.md`:

> If a Shipment is cancelled mid-flight after one of its LineItems has already been picked, what happens to the Invoice? Your spec doesn't address this.

### 6. Cross-reference with code

When the user states how something works, verify against the implementation. Surface contradictions:

> Your spec assumes Orders are atomic, but the existing fulfillment code processes them line-by-line — which model is canonical?

Cross-reference against existing ADRs:

> ADR-0007 says we use synchronous HTTP between Ordering and Billing. Your spec introduces an event bus. Is this a deliberate departure (in which case we need a new ADR) or an oversight?

### 7. Flag new terms — do not write

If new domain terms emerge during the session, **flag them at the end** of the interview:

> The following terms came up during this session but aren't in `CONTEXT.md` yet:
> - **{Term}** — {one-sentence working definition}
>
> Run `/repo-context-scan` to incorporate them into the canonical context.

Do **not** write to `CONTEXT.md` yourself. That responsibility belongs to `/repo-context-scan`.

### 8. Offer ADRs sparingly

During grilling, decisions may crystallize that meet the ADR bar. Offer to record an ADR only when **all three** are true (see `ADR-FORMAT.md`):

1. **Hard to reverse** — meaningful cost to change later
2. **Surprising without context** — a future reader will wonder why
3. **Result of a real trade-off** — there were genuine alternatives

If yes → write to `docs/adr/NNNN-slug.md`, incrementing from the highest existing number. If any criterion is missing → skip. Do not pad the ADR log.

## End of session

Summarize:

- Conflicts surfaced (artifact vs `CONTEXT.md` or vs existing ADRs)
- New terms flagged, with a `/repo-context-scan` re-run suggestion
- ADRs added during the session, if any
- Open questions still unresolved
- Recommended changes to the artifact before it is finalized

## Companion skills

- `/repo-context-scan` — owns `CONTEXT.md` and seeds ADRs from a codebase scan. Run it before this skill if no `CONTEXT.md` exists, or after this skill if new terms emerged.
- `/grill-me` — non-code-grounded interview for PRDs and general plans. Use whenever the artifact is not engineering.
