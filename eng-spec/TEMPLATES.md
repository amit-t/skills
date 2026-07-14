# Document Templates

Disclosed reference for `/eng-spec`. Copy the skeleton for each artifact and fill in the placeholders — the surrounding structure (frontmatter table, section order) is the contract with downstream steps (panel review, DoE approval gate, ralph sync).

## TDD skeleton (Step 3) — `outputs/tdds/TDD-NNN-{feature-slug}.md`

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

## SPEC skeleton (Step 4) — `outputs/specs/SPEC-{CODE}-NN-{feature-slug}.md`

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

## ADR skeleton (Step 5) — `outputs/decisions/ADR-NNN-{decision-slug}.md`, one per technology decision

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

## Panel synthesis skeleton (Step 8) — `outputs/specs/{SPEC-ID}-panel-review.md`

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
