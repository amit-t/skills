---
name: e2e-audit
description: Run a Playwright end-to-end audit of a web app using its PRDs as the test spec. Produces a diagnostic report showing what's working and what's not from a user's perspective.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

```
/e2e-audit                          → Run full PRD-coverage audit on current app
/e2e-audit --area auth              → Audit one PRD area only
/e2e-audit --report-only            → Skip test run, just format last results
/e2e-audit --export                 → Export results to outputs/analyses/
```

**What you get:** A markdown diagnostic report showing which routes and features work, which redirect to login (not built), and which have partial UI. Saves to `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md`.

**Time:** 5 min setup (first time) + test run duration (~2-5 min for 50 tests).

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

## Phase 4: Export Diagnostic Report

After the run, generate `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md` with:

```markdown
# E2E Audit Results — {App Name}
**Date:** YYYY-MM-DD | **Tests:** N passed / N failed / N skipped

## Summary table (by PRD area)

## What's working (production-ready)

## What's not working (with root cause)

## Root cause analysis

## Priority fixes for PRD backlog (P0 / P1 / P2)

## How to reproduce
```

Structure each PRD area section as a table:

| Test | Result | Notes |
|------|--------|-------|
| Feature X loads | ✅ | |
| Admin can do Y | ❌ | Route `/admin/y` redirects to login — not built |
| Viewer blocked from Z | ✅ | RBAC gate works |

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
| `outputs/analyses/YYYY-MM-DD-e2e-audit-results.md` | PO-facing diagnostic report |
| `apps/e2e/playwright-report/` | Full HTML report with screenshots + traces |
| `apps/e2e/test-results/` | Per-test artifacts (video, screenshots) |

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
