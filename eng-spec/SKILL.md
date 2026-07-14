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

Write `outputs/tdds/TDD-NNN-{feature-slug}.md` using the TDD skeleton (frontmatter table, problem/hypothesis, scope, architecture, open questions, risks, related ADRs) in `TEMPLATES.md`.

---

### Step 4: Draft the SPEC

**Before writing:** if UX/UI assets were found for this PRD, cross-reference them into the SPEC per `UX-INTEGRATION.md`. If none were found, go straight to the SPEC skeleton below.

Write `outputs/specs/SPEC-{CODE}-NN-{feature-slug}.md` using the SPEC skeleton (12 sections: overview through migration plan) in `TEMPLATES.md`.

---

### Step 5: Draft ADRs

**Identify technology decisions** that emerge from the SPEC work — any choice of:
- A library or framework (like jose, @node-saml in PLAT-01)
- An external service (like AWS SES)
- A pattern or approach that deviates from or extends existing ADRs

**For each decision, write `outputs/decisions/ADR-NNN-{decision-slug}.md`** using the ADR skeleton in `TEMPLATES.md`.

**Skip ADRs for:**
- Decisions already covered by existing ADRs (cite the existing one instead)
- Obvious choices with no real alternatives (e.g., "use Drizzle for PG" is already implied by ADR-002)

---

### Step 6: Panel Review — 5 Agents in Parallel

**Spawn all 5 agents in a single message with parallel Task tool calls.** The five prompts — each with its review-framework pointer, required inputs (full TDD, full SPEC, all new ADR texts, relevant existing ADRs, source PRD), and the required ✅/⚠️/❌/💡 output shape — live in `PANEL-PROMPTS.md`.

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

Write `outputs/specs/{SPEC-ID}-panel-review.md` using the panel synthesis skeleton (frontmatter, overall assessment, detailed feedback by reviewer) in `TEMPLATES.md`.

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
