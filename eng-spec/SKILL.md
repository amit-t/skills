---
name: eng-spec
description: Convert an approved PRD into TDD + Engineering Spec + ADRs, run a 5-agent engineering panel review (Architect, DB Designer, Principal SWE, SDET, Performance Engineer), fix blockers, approve, and sync to ralph.
---

## Purpose

Bridge the gap between an approved PRD and a ralph-ready engineering spec. Given an approved PRD, this skill produces:

1. **TDD** — Technical Design Document (problem, scope, approach, architecture)
2. **SPEC** — Implementation-ready engineering spec (data models, port interfaces, API contracts, sequence diagrams)
3. **ADRs** — One per technology decision that emerges from the spec work

Then runs a 5-agent panel review, fixes blockers, gets DoE approval, and syncs to the app's AI context.

## Usage

- `/eng-spec` — picks the most recent approved PRD without a spec
- `/eng-spec PLAT-02` — targets a specific PRD by code

---

## Context Routing

**Path resolution — read first:**
Read `project.conf` at the project root and source the following variables:
- `PM_OS_DIR` — path to the pm-os repo (e.g., `product/refinery-pm-os`)
- `UXD_OS_DIR` — path to the uxd-os repo (e.g., `product/refinery-uxd-os`)

Use these variables for all repo-relative paths in this skill.

**Load before starting:**
1. `PRD-PIPELINE.md` — current pipeline status, what's queued
2. Target approved PRD from `$PM_OS_DIR/outputs/prds/approved/`
3. `outputs/decisions/ADR-001-hexagonal-architecture.md` — architecture constraints
4. `outputs/decisions/ADR-002-three-database-strategy.md` — DB assignment rules
5. All existing ADRs in `outputs/decisions/` — to avoid duplicate decisions
6. `context-library/business-info-template.md` — tech stack, engineering org context
7. `outputs/tdds/` — scan for highest TDD number (for next TDD-NNN)
8. `outputs/specs/` — scan for existing specs (for SPEC numbering)

**UX/UI Design Assets (load by PRD code match):**
Search `$UXD_OS_DIR/outputs/` for files matching the PRD code (e.g., for `PLAT-02` look for files containing `PLAT-02` in their name or path):
- `screens/` — HTML prototype screens (user-facing flows, form fields, UI states)
- `wireframes/` — Low-fidelity wireframes (layout, information hierarchy)
- `user-flows/` — User journey flows (step-by-step interaction paths)
- `handoffs/` — Design handoff notes (component specs, interaction details)
- `design-reviews/` — Design review feedback (accepted/rejected patterns)
- `design-briefs/` — Design briefs (constraints, goals, context)

If no UX assets exist for the PRD code: note it and proceed. The spec will be API-driven rather than UI-driven.

**Sub-agents available (5):**
- `sub-agents/architect-reviewer.md`
- `sub-agents/db-designer-reviewer.md`
- `sub-agents/principal-engineer-reviewer.md`
- `sub-agents/sdet-reviewer.md`
- `sub-agents/performance-engineer-reviewer.md`

---

## Workflow

### Step 1: PRD Selection

**If user specified a PRD code (e.g., `PLAT-02`):**
- Search `$PM_OS_DIR/outputs/prds/approved/` for a file matching that code
- If found: load it
- If not found: list all approved PRDs, ask user to confirm

**If no PRD specified:**
- Read `PRD-PIPELINE.md` — find all rows where Spec column is `—` (not started)
- List them with: file name, title, PI allocation, dependencies
- Default to the first unspecced approved PRD
- Confirm with user: "Found [PRD-ID] — [title]. Proceeding with this one?"

**Always load before drafting:**
- ADR-001 (hexagonal architecture — folder layout and boundary rules)
- ADR-002 (three-database strategy — what goes in PG vs Mongo vs Redis)
- All existing ADRs (to avoid duplicating decisions already recorded)
- The full PRD text
- All UX/UI design assets found for this PRD code (screens, wireframes, user flows, handoffs)

**Report UX asset inventory to DoE before drafting:**
```
UX/UI assets found for {PRD-CODE}:
  Screens:      {N files — list names}
  Wireframes:   {N files — list names}
  User flows:   {N files — list names}
  Handoffs:     {N files — list names}
  Design reviews: {N files — list names}

These will inform: data model fields, API request/response shapes,
error state definitions, and UI-driven sequence flows.
```
If no assets found: "No UX/UI assets found for {PRD-CODE} in the uxd-os repo. Proceeding with API-first spec."

---

### Step 2: Determine Artifact Numbers

Scan existing files to assign the next sequential numbers:

**TDD number:**
- Glob `outputs/tdds/TDD-*.md`
- Take the highest TDD-NNN found, increment by 1
- Format: `TDD-NNN` (zero-padded to 3 digits, e.g., TDD-002)

**SPEC identifier:**
- Derive from the PRD code: if PRD is `PLAT-02`, spec is `SPEC-PLAT-02`
- If PRD uses a different code scheme, ask the user

**ADR numbers:**
- Glob `outputs/decisions/ADR-*.md`
- Take the highest ADR-NNN found, assign next sequential numbers for each new ADR

---

### Step 3: Draft the TDD

Write `outputs/tdds/TDD-NNN-{feature-slug}.md` using this structure:

```markdown
# TDD-NNN: {Feature Name}

| Field | Value |
|-------|-------|
| **System / Service / Initiative** | {scope} |
| **RFC Number** | TDD-NNN |
| **DRI (Tech Lead / Engineer)** | TBD |
| **Stage** | Solution Review |
| **Last Updated** | {today} |
| **Status** | Draft |
| **Source PRD** | {PRD file path} |
| **Related SPEC** | SPEC-{CODE}-NN |
| **Links** | Architecture Diagram (below) |

---

## 1) Problem and Hypothesis

**Problem:** {extracted from PRD problem statement}

**If we** {engineering hypothesis},
**then** {measurable outcome},
**because** {mechanism}.

**Strategy Fit:** {why this initiative matters in the PI context}

**Supporting Evidence:** {from PRD}

---

## 2) Scope and Non-Goals

**In Scope:**
- {from PRD scope, translated to engineering deliverables}

**Non-Goals:**
- {from PRD non-goals + engineering constraints}

---

## 3) Approach and Architecture

**Pattern:** Hexagonal Architecture (Ports & Adapters) per ADR-001

**Component Overview:**
{High-level component diagram in ASCII or Mermaid}

**Key Design Decisions:**
- {each major decision, with brief rationale or reference to ADR}

**Technology Choices:**
- {list with ADR references where applicable}

---

## 4) Open Questions

| Question | Owner | Due |
|----------|-------|-----|
| {question} | DoE | {date} |

---

## 5) Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| {risk} | L/M/H | L/M/H | {mitigation} |

---

## Appendix: Related ADRs

- ADR-001: Hexagonal Architecture
- ADR-002: Three-Database Strategy
- {any new ADRs created for this feature}
```

---

### Step 4: Draft the SPEC

**Before writing: cross-reference all loaded UX/UI assets.**

Use UX assets to inform these sections of the SPEC:

| UX Asset | Informs SPEC Section |
|----------|---------------------|
| **Screens** (HTML) | Section 2 (data model fields visible in forms/displays), Section 5 (API endpoints the UI calls), Section 8 (error states shown in UI) |
| **Wireframes** | Section 5 (API shape — what data the UI needs, in what structure), Section 7 (sequence flows matching interaction steps) |
| **User flows** | Section 7 (sequence diagrams — map each UI step to an API call), Section 8 (error paths shown in flow) |
| **Handoffs** | Section 3 (port interfaces — what the frontend contract requires), Section 5 (request/response shape — form fields = request body fields) |
| **Design reviews** | Section 8 (edge cases flagged in design review), Section 9 (security considerations flagged by design) |

**Specific rules when UX assets are present:**
- Every form field visible in a screen must appear as a field in the request body schema (Section 5)
- Every data element displayed in a screen must appear in the response body schema (Section 5)
- Every error message shown in a screen must appear in Section 8 with its HTTP code and error code string
- Every step in a user flow must map to at least one API call in Section 5 or a client-side operation noted as such
- If a screen shows data that spans multiple entities, the API response shape must reflect that join/aggregation

**Note screen-driven decisions in the SPEC:**
When a UX screen drives a data model or API decision, annotate it:
```
// Field required by auth-login.html — email input
email: varchar(255) NOT NULL
```

Write `outputs/specs/SPEC-{CODE}-NN-{feature-slug}.md` using this structure:

```markdown
# SPEC-{CODE}-NN: {Feature Name} — Engineering Spec

| Field | Value |
|-------|-------|
| **Status** | Draft |
| **Date** | {today} |
| **DRI** | TBD |
| **Source PRD** | {PRD path} |
| **Related TDD** | TDD-NNN |
| **ADRs** | {ADR-NNN list} |

---

## 1. Overview

{What ships in this feature — bulleted list of capabilities}

---

## 2. Data Models

### PostgreSQL (Drizzle ORM)
{Tables with full column definitions, types, constraints, indexes}

### MongoDB
{Collections with document shape, indexes}

### Redis
{Key patterns, TTL strategy, eviction policy}

---

## 3. Port Interfaces

### Input Ports (core/ports/in/)
{TypeScript interface definitions for each use case}

### Output Ports (core/ports/out/)
{TypeScript interface definitions for each repository/provider}

---

## 4. Service Layer (core/services/)

{Key service methods with signatures and behavior description}

---

## 5. HTTP Adapter (adapters/in/http/)

{API endpoint table: Method, Path, Auth, Request body, Response, Error codes}

---

## 6. Persistence Adapters (adapters/out/)

{Each adapter's implementation notes — which port it implements, key queries}

---

## 7. Sequence Diagrams

{Critical flows as Mermaid sequence diagrams}

---

## 8. Error States

{All error conditions, HTTP status codes, error response shape}

---

## 9. Security Considerations

{Auth requirements, rate limiting, data privacy, audit logging}

---

## 10. Non-Functional Requirements

| Requirement | Target |
|-------------|--------|
| P95 latency | {target} |
| Throughput | {target} |
| Availability | {target} |

---

## 11. Test Strategy

{Unit, integration, e2e scope; test data requirements; BDD scenario hooks}

---

## 12. Migration Plan

{DB migrations needed; rollout order; rollback procedure}
```

---

### Step 5: Draft ADRs

**Identify technology decisions** that emerge from the SPEC work — any choice of:
- A library or framework (like jose, @node-saml in PLAT-01)
- An external service (like AWS SES)
- A pattern or approach that deviates from or extends existing ADRs

**For each decision, write `outputs/decisions/ADR-NNN-{decision-slug}.md`:**

```markdown
# ADR-NNN: {Decision Title}

| Field | Value |
|-------|-------|
| **Status** | Proposed |
| **Date** | {today} |
| **Decision Maker** | DoE |
| **Related TDD** | TDD-NNN |
| **Supersedes** | None |

---

## Context

{Why this decision is needed — what the system requires}

---

## Decision

**We will use {X} for {purpose}.**

{Brief usage example if helpful}

---

## Alternatives Considered

### Option A: {name}
{Pros / Cons / Why rejected}

### Option B: {name}
{Pros / Cons / Why rejected}

---

## Rationale

{2-3 factors that decided it, specific to this tech stack}

---

## Consequences

### Positive
- {benefit}

### Negative
- {trade-off}

### Risks
- {risk or None significant}
```

**Skip ADRs for:**
- Decisions already covered by existing ADRs (cite the existing one instead)
- Obvious choices with no real alternatives (e.g., "use Drizzle for PG" is already implied by ADR-002)

---

### Step 6: Panel Review — 5 Agents in Parallel

**CRITICAL: Spawn all 5 agents in a single message with parallel Task tool calls.**

For each agent, provide:
- The full TDD text
- The full SPEC text
- All new ADR texts
- Relevant existing ADRs (ADR-001 and ADR-002 always; others as relevant)
- The source PRD for context

**Agent 1: Architect**
```
Prompt:
You are a senior software architect reviewing an engineering TDD and SPEC.

Read sub-agents/architect-reviewer.md for your review framework.

Source PRD: [PRD content]
TDD: [TDD content]
SPEC: [SPEC content]
ADRs: [all new ADRs + ADR-001 + ADR-002]

Review for: hexagonal boundary compliance, port/adapter correctness, domain isolation,
component coupling, dependency direction, architecture consistency with existing ADRs.

Provide:
- ✅ Architecture decisions that look correct
- ⚠️ Concerns (important but not blocking)
- ❌ Blockers (must fix — boundary violations, wrong adapter placement, dependency inversion broken)
- 💡 Suggestions
```

**Agent 2: DB Designer**
```
Prompt:
You are a database architect reviewing an engineering SPEC.

Read sub-agents/db-designer-reviewer.md for your review framework.

Source PRD: [PRD content]
SPEC: [SPEC content]
ADR-002 (three-database strategy): [ADR-002 content]

Review for: schema completeness, correct DB assignment (PG vs Mongo vs Redis per ADR-002),
normalization, indexes, constraints, query patterns, migration safety.

Provide:
- ✅ Strong data model decisions
- ⚠️ Schema gaps or concerns
- ❌ Blockers (wrong DB for data type, missing indexes for stated query patterns, unsafe migrations)
- 💡 Suggestions
```

**Agent 3: Principal Software Engineer**
```
Prompt:
You are a principal software engineer reviewing an engineering TDD and SPEC.

Read sub-agents/principal-engineer-reviewer.md for your review framework.

Source PRD: [PRD content]
TDD: [TDD content]
SPEC: [SPEC content]

Tech stack: Elysia + Bun + TypeScript (strict), PNPM workspaces, Biome, Lefthook.

Review for: API contract completeness, error handling coverage, security (auth, rate limiting,
PII), TypeScript idioms, implementation feasibility, edge cases, missing port definitions.

Provide:
- ✅ Strong engineering decisions
- ⚠️ Implementation concerns
- ❌ Blockers (missing error states, security gaps, broken API contract)
- 💡 Suggestions
```

**Agent 4: SDET / SQA**
```
Prompt:
You are a senior SDET reviewing an engineering TDD and SPEC for testability and quality.

Read sub-agents/sdet-reviewer.md for your review framework.

Source PRD: [PRD content]
TDD: [TDD content]
SPEC: [SPEC content]
UX Screens: [list of screen files and their content — if available]
User Flows: [user flow content — if available]

Test runner: Bun built-in test runner. Stack: Elysia + Bun + TypeScript.

Review for: testability of components, unit/integration/e2e test strategy completeness,
acceptance criteria coverage, BDD scenario traceability, test data requirements,
mock/stub boundaries, quality gates.

When UX screens and flows are provided, cross-check:
- Every screen state (default, loading, error, empty, success) maps to a test scenario
- Every user flow step maps to an acceptance criterion
- Error messages shown in screens match error states defined in SPEC Section 8
- Form validation shown in screens matches validation rules in SPEC Section 5

Provide:
- ✅ Well-specified testable components
- ⚠️ Testing gaps or risks
- ❌ Blockers (untestable design, missing acceptance criteria, no rollback test plan)
- 💡 Suggestions for improving testability
```

**Agent 5: Performance Engineer**
```
Prompt:
You are a performance and reliability engineer reviewing an engineering SPEC.

Read sub-agents/performance-engineer-reviewer.md for your review framework.

Source PRD: [PRD content]
SPEC: [SPEC content]

Review for: latency targets, throughput requirements, N+1 query risks, caching strategy
(Redis), index coverage for stated query patterns, connection pool sizing, SLO definitions,
load/stress test strategy, bottleneck risks.

Provide:
- ✅ Good performance decisions
- ⚠️ Performance concerns
- ❌ Blockers (no SLO defined, N+1 with no mitigation, missing index for critical query)
- 💡 Optimizations to consider
```

---

### Step 7: Collect Reviews and Fix

Wait for all 5 agents. Then:

**Extract from each review:**
- ❌ Blockers
- ⚠️ Concerns
- 💡 Suggestions

**Categorize all feedback:**

**Auto-fix (silently update TDD/SPEC/ADR, no DoE input needed):**
- Missing error state definition in SPEC → add it
- Data model field missing for a stated requirement → add it
- Technology choice in SPEC without an ADR → create the ADR
- Missing index for a query pattern explicitly named in SPEC → add it
- Missing port interface definition for a named adapter → add it
- Incomplete test strategy section → fill it in
- Missing rollback procedure → add it
- Acceptance criteria gap for a stated feature → add it

**Surface to DoE (pause and ask for decision):**
- Architectural conflict (e.g., panel disagrees on PG vs Mongo for a specific entity)
- Scope change implied by a blocker (e.g., "this requires WebSocket infrastructure not in scope")
- Security trade-off requiring product judgment
- Conflicting opinions between agents (e.g., Architect says X, Principal SWE says Y)
- Any blocker where the fix requires changing the PRD's stated approach

**Present to DoE when surfacing:**
```
Panel raised [N] items requiring your decision:

1. [CONFLICT: DB Assignment]
   Architect says: {position}
   DB Designer says: {position}
   Options: A) {option} B) {option}
   Recommendation: {if any}

2. [SCOPE: WebSocket Infrastructure]
   Performance Engineer flagged: {issue}
   Options: A) Add to scope B) Descope requirement C) Defer to v2
```

Wait for DoE decisions, apply them, then re-run the panel (max 2 full iterations). After 2 iterations, if blockers remain, surface to DoE for final judgment — do not loop further.

---

### Step 8: Generate Panel Synthesis

Write `outputs/specs/{SPEC-ID}-panel-review.md`:

```markdown
---
spec: SPEC-{CODE}-NN
tdd: TDD-NNN
review_date: {today}
agents: [architect, db-designer, principal-swe, sdet, performance-engineer]
iteration: 1
---

# Panel Review Synthesis: {Feature Name}

**Reviewed:** {date}
**Panel:** Architect, DB Designer, Principal SWE, SDET/SQA, Performance Engineer
**Iteration:** 1 of max 2

---

## Overall Assessment

**Status:** [Approved / Approved with minor fixes / Requires iteration / Blocked]

**Auto-fixed:** [N items]
**Decisions needed from DoE:** [N items]
**Blockers remaining:** [N]

---

## Auto-Fixed Items

- [description of what was fixed] — flagged by [Agent]
...

## DoE Decisions Made

- [decision] — chosen option: [A/B/C]
...

## Approved By All Panels

- [what all 5 agents signed off on]
...

## Remaining Concerns (non-blocking)

- [concern] — flagged by [Agent] — deferred to [v2 / monitoring / backlog]
...

---

## Detailed Feedback by Reviewer

### Architect
[full review output]

### DB Designer
[full review output]

### Principal SWE
[full review output]

### SDET/SQA
[full review output]

### Performance Engineer
[full review output]

---

*Generated: {timestamp}*
*Next: DoE approval → hq.sync-context → rpc.plan*
```

---

### Step 9: DoE Approval Gate

Present summary to DoE:

```
Engineering panel review complete for {SPEC-ID}.

✅ Auto-fixed: N items
✅ DoE decisions applied: N items
⚠️ Non-blocking concerns noted in synthesis (deferred)
❌ Blockers remaining: 0

TDD:  outputs/tdds/TDD-NNN-{slug}.md
SPEC: outputs/specs/SPEC-{CODE}-NN-{slug}.md
ADRs: ADR-NNN, ADR-NNN+1 (if any)
Review: outputs/specs/SPEC-{CODE}-NN-panel-review.md

Approve to proceed? (yes / request changes)
```

**If DoE requests changes:** Apply them, re-run panel for affected sections only, return to this step.

**If DoE approves:** Proceed to Step 10.

---

### Step 10: Approve and Sync

**1. Mark spec as Approved:**
Update the Status field in both TDD and SPEC frontmatter:
```
| **Status** | Approved |
```

**2. Update PRD-PIPELINE.md:**
Find the row for this PRD. Update the Spec column:
```
✓ TDD-NNN + SPEC-{CODE}-NN (approved)
```
Update the `_Last updated:` line at the bottom.

**3. Run context sync:**
```bash
hq.sync-context
```

**4. Print handoff message:**
```
✓ Spec approved and synced.

Artifacts:
  TDD:  outputs/tdds/TDD-NNN-{slug}.md
  SPEC: outputs/specs/SPEC-{CODE}-NN-{slug}.md
  ADRs: {list}

PRD-PIPELINE.md updated ✓

Ready for ralph. Run:
  rpc.plan        (Claude)
  rpd.plan        (Devin)
  rpx.plan        (Codex)
```

---

## Output Quality Self-Check

Before presenting anything to DoE, verify:

- [ ] TDD references correct SPEC filename and all new ADR numbers
- [ ] SPEC references correct TDD number in frontmatter
- [ ] Every technology decision in SPEC has either an existing ADR cited or a new ADR created
- [ ] All 5 panel agents provided feedback with at least one concrete, specific item
- [ ] Auto-fixed items are reflected in the actual TDD/SPEC files (not just listed)
- [ ] PRD-PIPELINE.md update is accurate (correct row, correct status)
- [ ] SPEC includes all 12 sections (or explicit "N/A — {reason}" for any omitted)
- [ ] ADR-001 (hexagonal) compliance verified by Architect agent
- [ ] ADR-002 (three-database) compliance verified by DB Designer agent
- [ ] If UX screens were found: every form field in screens appears in SPEC Section 5 request schema
- [ ] If UX screens were found: every displayed data field in screens appears in SPEC Section 5 response schema
- [ ] If UX screens were found: every error state shown in screens appears in SPEC Section 8
- [ ] If user flows were found: every flow step maps to a SPEC Section 5 endpoint or is noted as client-side
- [ ] UX asset inventory reported to DoE at start (or "no assets found" noted)

---

## Integration with Other Skills

**Before `/eng-spec`:**
- `/prd-draft` — write the PRD (in pm-os)
- `/prd-review-panel` — PM-level review before approval

**After `/eng-spec`:**
- `rpc.plan` — generate fix_plan.md from the approved spec
- `/launch-checklist` — plan the release after implementation
- `/create-tickets` — break spec into engineering tickets

**Iterative use:**
- Run `/eng-spec` once per approved PRD
- If PRD scope changes post-approval, re-run for the affected PRD
