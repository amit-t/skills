---
name: package-scout
description: Research, compare, and select the best npm/pnpm/yarn packages before installing. Use when scaffolding a project, adding a new dependency or devDependency, choosing between competing libraries, or when user says "find a package", "which library", "add dependency", or "install package".
---

# Package Scout

Before installing **any** external package (npm, pnpm, yarn, or other package managers), stop and run this workflow. Never blindly install a package without researching alternatives first.

## When This Applies

- Scaffolding a new project and choosing its dependency stack
- Adding a new dependency or devDependency during development
- Replacing an existing package with a better alternative
- User asks you to install, add, or pick a package

## Workflow

### 1. Clarify the Need

Before searching, confirm with the user:

- **What problem does this package need to solve?** (e.g., "HTTP client", "date formatting", "form validation")
- **Any constraints?** (e.g., "must support ESM", "no native bindings", "MIT license only", "< 50 KB bundle")
- **Package ecosystem?** Ask which registry or repository source to search (npmjs.com, GitHub, JSR, etc.) — default to npm if not specified

If the user already named a specific package, still research alternatives before installing.

### 2. Research Using Web Search

Use your web search tool to find candidates. Search for:

- `best <category> library npm 2025` (use current year)
- `<package-name> vs alternatives`
- `<package-name> npm` (for the specific package info)

For each candidate, look up:

| Signal               | Where to Find                          |
|----------------------|----------------------------------------|
| GitHub stars         | GitHub repo page                       |
| Weekly downloads     | npmjs.com package page                 |
| Last publish date    | npmjs.com "Last publish" field         |
| Open issues count    | GitHub Issues tab                      |
| Fork count           | GitHub repo page                       |
| Bundle size          | bundlephobia.com or pkg-size.dev       |
| Known vulnerabilities| Snyk or socket.dev advisories          |
| License              | package.json or repo LICENSE file      |
| TypeScript support   | Built-in types vs @types/* needed      |

Gather data for **3-5 viable candidates** that solve the same problem.

### 3. Filter and Rank

Apply these quality signals (in priority order):

1. **Actively maintained** — last publish within 6 months; no "deprecated" or "unmaintained" warnings
2. **Low vulnerability count** — check Snyk/socket.dev; prefer zero known vulnerabilities
3. **Community adoption** — stars, forks, weekly downloads as social proof
4. **Small bundle size** — matters for frontend; less critical for backend/CLI
5. **TypeScript support** — built-in types preferred over @types/*
6. **Open issue ratio** — high open issues relative to stars may signal maintenance debt
7. **License compatibility** — must be compatible with the project's license

Eliminate any candidate that is deprecated, unmaintained (>12 months since last publish), or has unpatched critical vulnerabilities.

### 4. Present Options to the User

Show a comparison table with your top 3 picks:

```
## Package Comparison: <category>

| | Package A | Package B | Package C |
|---|-----------|-----------|-----------|
| Stars | 45K | 12K | 8K |
| Weekly DLs | 20M | 5M | 1.2M |
| Last publish | 2 weeks ago | 3 months ago | 6 months ago |
| Bundle size | 12 KB | 45 KB | 3 KB |
| Open issues | 42 | 180 | 15 |
| Vulnerabilities | 0 | 1 (moderate) | 0 |
| TS support | Built-in | @types needed | Built-in |
| License | MIT | Apache-2.0 | MIT |

**Recommendation:** Package A — most actively maintained, zero
vulnerabilities, smallest adoption risk.

**Runner-up:** Package C — lightest bundle, good if size is critical.
```

Include a 1-2 sentence recommendation with reasoning. Let the user choose.

### 5. Resolve the Latest Stable Version

Once the user picks a package:

1. **Web search** `<package-name> latest version npm` to confirm the current stable release
2. Cross-check against the npmjs.com page — use the version tagged `latest`, NOT `next`, `beta`, `rc`, or `canary`
3. If the user needs a specific version range (e.g., for peer dependency compat), verify that version exists

### 6. Install

Install using the project's package manager (detect from lockfile):

| Lockfile             | Command                                |
|----------------------|----------------------------------------|
| `package-lock.json`  | `npm install <pkg>@<version>`          |
| `pnpm-lock.yaml`     | `pnpm add <pkg>@<version>`            |
| `yarn.lock`          | `yarn add <pkg>@<version>`            |
| `bun.lockb`          | `bun add <pkg>@<version>`             |
| None found           | Ask user which package manager to use  |

- Add `--save-dev` / `-D` flag if it's a devDependency (test frameworks, linters, build tools, type packages)
- Pin to exact version or caret range based on project conventions (check existing `package.json`)

## Rules

- **Never install without research.** Even if the user names a specific package, present at least one alternative.
- **Never install pre-release versions** unless the user explicitly asks for beta/canary/next.
- **Always use web search** for version info — do not rely on training data, which may be outdated.
- **Respect the project's existing package manager.** Do not mix npm/pnpm/yarn.
- **Ask before adding** — always get user confirmation on the final package + version before running the install command.
