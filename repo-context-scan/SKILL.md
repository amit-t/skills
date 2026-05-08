---
name: repo-context-scan
description: Scans a codebase to build CONTEXT.md (or CONTEXT-MAP.md for multi-context repos) and seed ADRs for clearly-deliberate decisions. Autonomous by default; asks only when ambiguity blocks resolution. Use after cloning a repo, joining a project mid-flight, or when docs have drifted from code. Triggers include "scan repo context", "build CONTEXT.md", "bootstrap domain context", and "/repo-context-scan".
---

# Repo Context Scan

Build domain awareness for an unfamiliar codebase in one shot. Produces:

- `CONTEXT.md` (single-context repo) **or** `CONTEXT-MAP.md` plus per-context `CONTEXT.md` files (multi-context repo)
- Seeded `docs/adr/NNNN-*.md` entries for visibly deliberate, hard-to-reverse decisions

This skill **owns** the writing of `CONTEXT.md` and ADR files. The companion skill `/domain-grill` consumes them read-only.

## When to use

- After cloning a repo for the first time and you need to ramp on its domain language
- When joining a project mid-flight
- When code has drifted from existing docs and you want a fresh snapshot
- As a recurring sync: idempotent, so safe to re-run

## When NOT to use

- For *interactive* domain refinement during feature design — use `/domain-grill`
- For non-code artifacts (PRDs, marketing copy, business plans) — context describes the code domain, not product narratives
- For pure conversational glossary extraction — that responsibility used to belong to the deprecated `ubiquitous-language` skill; this skill replaces it with code-grounded scanning

## Mode

**Autonomous by default.** Read code, infer terms, write files, output a summary. Ask the user only when one of these blockers shows up:

1. Two terms appear used interchangeably in the codebase with no clear canonical winner (e.g., both `Order` and `Purchase` exist as type names with overlapping usage). Ask which is canonical.
2. Bounded-context boundaries are unclear — multiple modules look like contexts but share substantial vocabulary. Ask whether to treat as single or multi-context.
3. A decision passes the ADR bar (hard-to-reverse, surprising, real trade-off) but the rationale is not visible in code or commit history. Ask the user for the *why*.

Outside those cases: scan, write, summarize. No back-and-forth.

## Process

### 1. Detect structure

- Check for existing `CONTEXT-MAP.md` or `CONTEXT.md` at repo root → enter re-run mode (update, never overwrite user prose).
- Look for module boundaries: top-level `src/<domain>/`, monorepo workspaces, separately-deployed packages with distinct vocabularies.
- 2+ clearly-bounded modules with distinct domain types → multi-context.
- Otherwise → single context.

### 2. Extract domain language

Sources, in priority order:

1. Type / class / struct / interface names in primary source dirs
2. Database schema (table and column names)
3. API routes, GraphQL types, gRPC service names
4. Domain event names (`*Event`, `*Created`, `*Updated`, `*Cancelled`)
5. Test descriptions (`describe("when a Customer places an Order...")`)
6. Existing README / docs

For each candidate term, ask:

- Is it **domain-meaningful** (a non-engineer would recognize it) or **purely technical** (Logger, Cache, Util, Repository)? Drop the technical-only ones.
- Does it appear under multiple names? Pick one canonical, list the rest under "Avoid".
- One-sentence definition: what it **is**, not what it **does**.

### 3. Extract relationships

Walk type signatures, foreign keys, event flows. Express cardinality where obvious:

- "An **Order** has many **LineItems**"
- "An **Invoice** belongs to exactly one **Customer**"
- "A **Shipment** is produced by exactly one **Fulfillment**"

### 4. Seed ADRs

Look for visibly deliberate decisions in code:

- Database choice (Postgres extensions, Mongo aggregation pipelines, etc.)
- Event-sourcing vs CRUD (presence of event store, projections, replays)
- Sync vs async integration (HTTP clients vs message-bus client libraries)
- Manual SQL vs ORM, monorepo vs polyrepo, deployment target
- Custom auth vs off-the-shelf
- Test pyramid shape (unit-heavy, integration-heavy, e2e-heavy)

For each candidate, gate against the three ADR criteria (see `ADR-FORMAT.md`):

1. **Hard to reverse** — meaningful cost to change later
2. **Surprising without context** — a future reader will wonder *why*
3. **Result of a real trade-off** — there were genuine alternatives

All three true → seed an ADR. If only one or two hold, **skip**. Do not pad the ADR log.

### 5. Write files

Write paths and formats:

- `CONTEXT.md` (single context) or `CONTEXT-MAP.md` + per-context `CONTEXT.md` (multi-context)
- `docs/adr/NNNN-slug.md` for each seeded ADR (numbered sequentially from existing max)

See `CONTEXT-FORMAT.md` and `ADR-FORMAT.md` for templates.

If files already exist (re-run mode):

- **Preserve** any prose the user has authored outside the generated tables and lists
- Update term tables in place
- Append new ADRs with the next sequential number; never edit existing ADRs
- Never delete user content

### 6. Output summary

In conversation, report:

- Files written / updated (with paths)
- Term count by group
- ADRs seeded (with titles)
- Open questions where ambiguity required user input, if any
- Suggested next step: *"Run `/domain-grill` next time you draft an engineering spec to stress-test it against this context."*

## Re-running

Idempotent. Each run:

- Re-scans current code state
- Updates term tables to match what's in code today
- Adds new ADRs for newly-visible deliberate decisions
- Preserves user-authored prose

Do not delete files or sections the user has manually edited.

## Companion skills

- `/domain-grill` — uses the output of this skill to interview the user against an engineering artifact (eng spec, TDD plan, refactor proposal). Engineering-only.
- `/grill-me` — non-code-grounded interview for PRDs and general plans. Does not depend on this skill's output.
