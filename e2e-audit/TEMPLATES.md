# Report & Fix-Plan Templates

Disclosed reference for `/e2e-audit` Phase 5 (diagnostic report) and Phase 6 (fix_plan epic). Fill in the placeholders; the surrounding structure is the contract.

## Diagnostic report skeleton (Phase 5)

```markdown
# {App} — End-to-End Demo & Gap Audit

**Date:** YYYY-MM-DD
**Run:** Playwright N.N · `tests/demo/full-demo.spec.ts` · N tests passed
**Personas:** {list}
**Screenshots:** `outputs/analyses/e2e-demo-screenshots/` (N PNGs)
**Regression run:** P passed · F failed · S skipped

## Summary
<2-3 sentence executive summary — route coverage %, top P0/P1 themes>

## Demo Walkthrough — by Persona

### Public / Unauthenticated
| # | Screen | Route | Screenshot |
### Super Admin
### Workspace Admin
### Product Owner
### Viewer

## Regression Run — Failures
| Test | Area | Failure |

## Bug Catalogue (→ fix_plan)
| ID | Severity | Screen | Summary |
| QA-DEMO-01 | P0/P1/P2 | … | one-line defect |

## How to Reproduce
```

## Fix-plan epic header (Phase 6.1)

```markdown
---

## Active Epic: QA-DEMO — E2E Demo Audit Findings

**Source:** `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md` (Playwright demo spec + regression run YYYY-MM-DD)
**Status:** N tasks pending
**Depends on:** {previous completed epic}
**Blocks:** {downstream release / launch readiness}
**Success metric:** All N tasks resolved; regression green; screenshot re-capture shows no regression.

### Summary of findings
| ID | Severity | Area | Defect (one line) |
```

## Fix-plan task template, one per bug (Phase 6.2)

```markdown
- [ ] **QA-DEMO-NN** — {one-line title}
  - **Screens:** {route(s) affected — multiple personas → list all}
  - **Evidence:** `outputs/analyses/e2e-demo-screenshots/NN-persona-screen.png`
  - **Symptom:** {what the user sees, with exact quoted strings where applicable}
  - **Likely cause:** {1-3 hypotheses — don't diagnose blind, read the code path first if obvious}
  - **Files to inspect/fix:**
    - `apps/web/src/features/.../page.tsx:LINE`
    - `apps/api/src/adapters/...`
  - **Fix plan:** {numbered steps a ralph agent can follow mechanically}
  - **Exit criteria:** {observable assertion — "Playwright `expect(...).toHaveCount(0)`" or "screenshot shows X"}
```
