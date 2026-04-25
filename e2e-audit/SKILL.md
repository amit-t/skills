---
name: e2e-audit
description: Run a Playwright end-to-end audit of a web app using its PRDs as the test spec. Produces a diagnostic report showing what's working and what's not from a user's perspective.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

```
/e2e-audit                          → Full PRD-coverage audit: regression + persona screenshot demo + fix_plan bug list
/e2e-audit --area auth              → Audit one PRD area only
/e2e-audit --report-only            → Skip test run, just format last results
/e2e-audit --export                 → Export results to outputs/analyses/
/e2e-audit --demo-only              → Skip regression; just capture persona screenshots + bug catalogue
/e2e-audit --no-fix-plan            → Skip appending bug list to `.ralph/fix_plan.md`
```

**What you get (three artifacts):**
1. `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md` — PO-facing diagnostic report with embedded persona screenshots + bug catalogue
2. `outputs/analyses/e2e-demo-screenshots/` — full-page PNGs, one per (persona × screen), named with an ordered prefix for easy scrolling
3. New `QA-DEMO` epic appended to `.ralph/fix_plan.md` — one ralph task per bug (file paths, root-cause hypothesis, exit criteria)

**Time:** 5 min setup (first time) + ~2 min regression + ~1.5 min screenshot demo + ~1 min inspection per 10 screens.

---

# /e2e-audit — Playwright UI Audit Workflow

When this skill is invoked, run a Playwright end-to-end audit of the app against its PRDs.

---

## Phase 0: Discover Context

Before writing a single test, read:
1. `context-library/prds/` — what features exist (PRD areas to test)
2. `engineering/refinery-app/apps/e2e/` (or equivalent) — whether an e2e suite already exists
3. The app's router file to understand real routes (e.g., `src/App.tsx`, `routes.ts`, or equivalent)
4. The auth store — **critical**: determine how auth tokens are stored (cookies vs memory vs localStorage)

**Auth storage discovery is the most important step.** It determines the entire fixture strategy:

| Auth storage | Strategy |
|---|---|
| Cookies / localStorage | Use `storageState` — log in once, reuse session file |
| In-memory only (Zustand, Redux, etc.) | Real UI login per fixture — no session cache possible |

---

## Phase 1: Scaffold (if no e2e package exists)

### 1.1 Create the package

```
apps/e2e/
  package.json          # @{project}/e2e, type: module
  tsconfig.json         # extends root tsconfig
  playwright.config.ts  # config with webServer auto-start
  global-setup.ts       # validates seed users can log in
  .env.example          # optional env vars (e.g. JIRA_PAT)
  .gitignore            # .auth/, .env, playwright-report/, test-results/
  utils/
    seed-users.ts       # known test user credentials
  fixtures/
    auth.fixture.ts     # login fixture (UI login or storageState)
    workspace.fixture.ts  # (optional) pre-navigates to a workspace
    index.ts            # re-exports test + expect
  tests/
    auth/               # @PLAT-auth
    workspace/          # @PLAT-workspace
    admin/              # @PLAT-admin
    ...                 # one folder per PRD area
```

### 1.2 Playwright config essentials

```ts
// playwright.config.ts
export default defineConfig({
  testDir: './tests',
  fullyParallel: true,
  retries: 1,
  globalSetup: './global-setup.ts',
  use: {
    baseURL: 'http://localhost:{WEB_PORT}',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
    trace: 'on',                // per-step screenshots in trace viewer
  },
  reporter: [
    ['html', { outputFolder: 'playwright-report', open: 'never' }],
    ['list'],
  ],
  webServer: [
    {
      command: 'pnpm --filter @{project}/api dev',
      url: 'http://localhost:{API_PORT}/health',
      reuseExistingServer: true,
      timeout: 30_000,
    },
    {
      command: 'pnpm --filter @{project}/web dev',
      url: 'http://localhost:{WEB_PORT}',
      reuseExistingServer: true,
      timeout: 30_000,
    },
  ],
})
```

**Always use `--filter @{project}/api` (full package name), not bare `api`.**

### 1.3 Seed user fixture pattern

**For in-memory auth (no storageState):**

```ts
// fixtures/auth.fixture.ts
async function loginPage(browser: Browser, email: string, password: string): Promise<Page> {
  const ctx = await browser.newContext()
  const page = await ctx.newPage()
  await page.goto(`${BASE_URL}/login`)
  await page.getByLabel('Email').fill(email)
  await page.getByLabel('Password').fill(password)
  await page.getByRole('button', { name: /sign in/i, exact: true }).click()
  // Adjust URL pattern to match your app's post-login redirect
  await page.waitForURL(/\/(home|dashboard|workspaces|ws\/)/, { timeout: 15_000 })
  return page
}
```

**For cookie/localStorage auth:**

```ts
// fixtures/auth.fixture.ts
// Run once in global-setup.ts:
await page.context().storageState({ path: '.auth/admin.json' })

// In fixture:
adminPage: async ({}, use) => {
  const ctx = await browser.newContext({ storageState: '.auth/admin.json' })
  const page = await ctx.newPage()
  await use(page)
  await ctx.close()
}
```

### 1.4 Add pnpm shortcuts to root package.json

```json
"e2e":        "pnpm --filter @{project}/e2e test",
"e2e:report": "pnpm --filter @{project}/e2e run report",
"e2e:jira":   "pnpm --filter @{project}/e2e test -- --grep @jira"
```

---

## Phase 2: Write Tests (PRD-Driven)

### Structure

- One folder per PRD/PLAT area under `tests/`
- Tag each `describe` block: `@PLAT-01`, `@PRD-001`, etc.
- For optional integrations (Jira, Slack, etc.): guard with `test.skip(!process.env.TOKEN, '...')`

### Test types to write per area

| Type | Example | Pass condition |
|------|---------|---------------|
| **Page loads** | dashboard loads | heading or key landmark visible |
| **Core action** | can fill story form | textarea accepts input |
| **Permission gate** | viewer blocked from admin | URL matches `forbidden\|login` or element not visible |
| **Data renders** | user list shows seed users | table rows visible |
| **Error state** | wrong password shows error | error text visible |

### The most informative test pattern

```ts
test('feature page loads for {role}', async ({ adminPage }) => {
  await adminPage.goto('/ws/{slug}/feature')
  // If page redirects to login → feature not built / route missing
  // If page renders but element missing → UI incomplete
  await expect(adminPage.getByRole('heading', { name: /feature/i })).toBeVisible()
})
```

### Conditional/optional tests

```ts
test.describe('@jira Jira tests', () => {
  test.beforeEach(() => {
    test.skip(!process.env.JIRA_PAT, 'Set JIRA_PAT in .env to run')
  })
  // biome-ignore lint/style/noNonNullAssertion: guarded by test.skip above
  test('can connect with PAT', async ({ adminPage }) => {
    await adminPage.getByLabel(/token|PAT/i).fill(process.env.JIRA_PAT!)
  })
})
```

---

## Phase 3: Run and Interpret

### Run command

```bash
pnpm e2e             # full suite
pnpm e2e:report      # open HTML report at localhost:9323
pnpm e2e:jira        # optional integration tests
```

### Interpreting failures

| What you see | What it means |
|---|---|
| Page snapshot shows **login page** | Route doesn't exist OR user lacks workspace access |
| Element not found on real page | Feature exists but UI selector is wrong / heading text differs |
| Timeout (30s) | Slow API call, missing seed data, or infinite redirect loop |
| Test passes but shouldn't | Check for false positives — login page has `<input>` fields, which trips `count > 0` checks |

### False positive check

Negative-assertion tests (`not.toBeVisible`, `toHaveURL(/login/)`) can pass for the wrong reason if the route doesn't exist at all. Always pair with a positive check or page title assertion for critical permission tests.

---

## Phase 4: Capture Persona Screenshot Demo

**Always produce a screenshot demo alongside the regression run.** Regression asserts behaviour; the demo asserts *what users actually see* — and is where most visual/copy/i18n bugs surface.

### 4.1 Write `tests/demo/full-demo.spec.ts`

One spec, one helper, one screenshot per (persona × screen). Structure:

```ts
import path from "node:path";
import { expect, test } from "../../fixtures/auth.fixture.js";

const SCREENSHOT_DIR = path.resolve("test-results/demo-screenshots");
const DEFAULT_SLUG = "{slug}";

async function snap(page, name) {
  await page.waitForLoadState("networkidle", { timeout: 10_000 }).catch(() => {});
  await page.screenshot({ path: path.join(SCREENSHOT_DIR, `${name}.png`), fullPage: true });
}

test.describe.configure({ mode: "serial" });

test.describe("@demo public screens", () => { /* 00-xx */ });
test.describe("@demo super_admin persona", () => { /* 10-xx */ });
test.describe("@demo workspace_admin persona", () => { /* 40-xx */ });
test.describe("@demo product_owner persona", () => { /* 50-xx */ });
test.describe("@demo viewer persona", () => { /* 60-xx */ });
```

**Naming convention:** `NN-persona-screen.png` where `NN` orders the narrative (00–09 public, 10–39 admin, 40–49 WA, 50–59 PO, 60–69 viewer). This makes the screenshot dir directly scrollable top-to-bottom as a slide deck.

**Cover every route** in the router file — one test per route per persona that can reach it. Include permission-gate routes (screenshot the "Access Denied" fallback).

### 4.2 Register a package script

Add to `apps/e2e/package.json`:

```json
"test:demo": "playwright test tests/demo"
```

And to root `package.json`:

```json
"e2e:demo": "pnpm --filter @{project}/e2e exec playwright test tests/demo"
```

### 4.3 Run + copy outputs

```bash
pnpm run e2e:demo
cp apps/e2e/test-results/demo-screenshots/*.png outputs/analyses/e2e-demo-screenshots/
```

**Gotcha:** Playwright clears `test-results/` between runs. If you run regression *after* the demo, screenshots vanish. Either re-run demo last, or copy to `outputs/analyses/` immediately.

### 4.4 Inspect every screenshot

Read them via the Read tool (they render as images). Log every defect — even minor ones. Categories to watch:

| Category | Example defects |
|----------|----------------|
| Data contradiction | Stat cards empty while list views show data; "No X yet" message when X exists |
| Missing chrome | Page missing sidebar/topnav used by sibling routes (check `RieLayout` wrapping) |
| Raw error codes | API codes like `NOT_FOUND`, `UNAUTHORIZED` shown as user copy |
| Stub screens | Only heading renders — no form/content |
| Rendering glue | Avatar initials concatenated with names, column fallbacks (`createdAt` shown in `scoredAt` column) |
| i18n escapes | Literal `\u2013`, `&amp;`, unescaped HTML |
| RBAC UI leaks | Buttons visible to roles that get 403 on click |
| Duplicate records | Role chips, membership rows repeated |

---

## Phase 5: Export Diagnostic Report

Generate `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md`:

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

Structure each persona section as a table with a screenshot path and observations column — do not inline the PNGs unless the report is intended for a slide deck.

---

## Phase 6: Emit fix_plan Bug List

**Every defect becomes a ralph task.** Append a new `QA-DEMO` epic to `.ralph/fix_plan.md`. One checkbox per bug, each with enough detail that a ralph agent can execute without re-inspecting screenshots.

### 6.1 Epic header

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

### 6.2 Task template (one per bug)

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

### 6.3 Severity rubric

| Level | Trigger |
|-------|---------|
| **P0** | Primary feature is an unbuilt stub (e.g. SSO page empty heading), blocks a launch-readiness requirement |
| **P1** | Core data view broken (stats empty, chart missing, table absent), raw API codes leaked to users, RBAC UI gate missing |
| **P2** | Copy/i18n/cosmetic (literal `\u2013`, column fallback, minor permission UI leaks) |

### 6.4 Don't emit for

- Intentional permission gates that render the correct "Access Denied" fallback — those are passes, not bugs
- Known TODO routes labelled as such in the PRD (e.g. `Integrations (Soon)` chip in sidebar)
- Regression failures that are selector bugs in the test itself — fix the test directly, don't file against the app

---

## Re-audit Workflow (after ralph fixes)

When ralph marks tasks `[x]` in `.ralph/fix_plan.md`:

```bash
# bring up fresh infra if dev servers died
docker-compose up -d
pnpm --filter @{project}/api db:migrate
pnpm --filter @{project}/api seed
pnpm --filter @{project}/api seed:stories   # if separate demo seed

# regenerate screenshots + rerun regression
pnpm run e2e:demo
pnpm --filter @{project}/e2e exec playwright test --grep-invert "@demo"
```

Then for each `[x]`-marked task, read the corresponding screenshot and verify. Possible outcomes:

| Outcome | Action |
|---------|--------|
| Bug fixed | Leave `[x]`. Note in report under "Verified fixed". |
| Bug still reproduces | Revert to `[ ]` and add a comment to the task: `> Re-audit YYYY-MM-DD: still broken — {new evidence}`. |
| Partial fix (e.g. UI renders but regression test still red) | Leave `[x]` for the UI portion, add a follow-up `QA-DEMO-NN-B` task for the test-level gap. |
| New defect surfaced | File a new `QA-DEMO-NN` below the existing list. |

A single re-audit should also refresh the summary table at the top of the epic with verification status (`✅ fixed` / `⚠ partial` / `❌ still broken`).

---

## Common Pitfalls

### Auth
- **Don't assume storageState works** — check how the app stores auth before designing fixtures. In-memory Zustand requires real UI login per test.
- **Post-login URL pattern must match actual redirect** — if the app goes to `/dashboard` but your pattern only checks for `/home`, global setup will time out.

### Routes
- **Missing routes redirect to login** in most React SPAs — a "login page" in the failure screenshot means "route doesn't exist", not "user not authenticated".
- **Use the app's router file** to check real routes before writing test navigation.

### Selectors
- **Heading text must match exactly** — use flexible regex: `getByRole('heading', { name: /dashboard/i })`
- **SVG/canvas charts don't have semantic roles** — use `locator('svg, canvas').first()`

### Linting (Biome / ESLint)
- **No `console.log`** in test files — use Playwright's `test.info()` for logging
- **No `!` non-null assertions** — guard with `test.skip()` and add `biome-ignore` comment
- **Import order** — run `biome check --write` before committing

---

## Output Files

| File | Description |
|------|-------------|
| `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md` | PO-facing diagnostic report with persona tables + bug catalogue |
| `outputs/analyses/e2e-demo-screenshots/` | `NN-persona-screen.png` — one per (persona × route), ordered for slide-deck reading |
| `.ralph/fix_plan.md` | `QA-DEMO` epic appended with one ralph task per bug |
| `apps/e2e/tests/demo/full-demo.spec.ts` | Re-runnable screenshot demo spec |
| `apps/e2e/playwright-report/` | Full HTML report with traces |
| `apps/e2e/test-results/` | Per-test artifacts (video, screenshots) — cleared between runs |

---

## Adapting to Your Stack

| Variable | Replace with |
|----------|-------------|
| `{project}` | Your pnpm package name prefix (e.g., `refinery`) |
| `{WEB_PORT}` | Frontend dev server port (e.g., `5173`) |
| `{API_PORT}` | API server port (e.g., `3000`) |
| `{slug}` | Default workspace/tenant slug for test data |
| `@PLAT-xx` / `@PRD-xxx` | Your PRD/ticket tag system |
| `SEED_USERS` | Your test user credentials |
| `apps/e2e/` | Your monorepo path for the e2e package |
