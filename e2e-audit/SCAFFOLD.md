# E2E Package Scaffold

Disclosed reference for `/e2e-audit` Phase 1. Use only when Phase 0 found no existing e2e suite; skip straight to Phase 2 if one already exists.

## 1.1 Create the package

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

## 1.2 Playwright config essentials

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

## 1.3 Seed user fixture pattern

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

## 1.4 Add pnpm shortcuts to root package.json

```json
"e2e":        "pnpm --filter @{project}/e2e test",
"e2e:report": "pnpm --filter @{project}/e2e run report",
"e2e:jira":   "pnpm --filter @{project}/e2e test -- --grep @jira"
```
