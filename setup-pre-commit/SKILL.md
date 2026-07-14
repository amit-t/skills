---
name: setup-pre-commit
description: Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current JS/TS repo. Use when the user wants to add pre-commit hooks or set up Husky/lint-staged for commit-time formatting, typechecking, and tests.
---

# Setup Pre-Commit Hooks

Wire up a Husky pre-commit hook that runs lint-staged (Prettier on staged files), then a typecheck and test pass. Detects the package manager, installs the tooling as devDependencies, writes the hook + config files, verifies, and commits.

> Ported from [`mattpocock/skills` → `misc/setup-pre-commit`](https://github.com/mattpocock/skills/blob/main/skills/misc/setup-pre-commit/SKILL.md). Adapted to this catalog's conventions.

## What this sets up

- **Husky** — git pre-commit hook manager
- **lint-staged** — runs Prettier on staged files only (fast)
- **Prettier** — formatter + config (only written if no config exists)
- **typecheck** + **test** — full passes run from the hook, when those scripts exist

This is a JS/npm-based toolchain. The hook tooling is `npx`-driven — keep it JS, not shell. (Any operator helper commands below use zsh per repo preference, but the hook itself stays npm-based.)

## Steps

### 1. Detect package manager

Check for a lockfile, in this order — use whichever is present:

| Lockfile | Manager | Run-script prefix |
|---|---|---|
| `package-lock.json` | npm | `npm run` |
| `pnpm-lock.yaml` | pnpm | `pnpm run` |
| `yarn.lock` | yarn | `yarn` |
| `bun.lockb` / `bun.lock` | bun | `bun run` |

Default to **npm** if none is clear. Quick check:

```zsh
for f in package-lock.json pnpm-lock.yaml yarn.lock bun.lockb bun.lock; do
  [[ -f $f ]] && print -r -- "found: $f"
done
```

### 2. Install dependencies

Install as devDependencies (substitute the detected manager's install command):

```
husky lint-staged prettier
```

- npm: `npm install -D husky lint-staged prettier`
- pnpm: `pnpm add -D husky lint-staged prettier`
- yarn: `yarn add -D husky lint-staged prettier`
- bun: `bun add -d husky lint-staged prettier`

### 3. Initialize Husky

```bash
npx husky init
```

Creates the `.husky/` directory and adds `"prepare": "husky"` to `package.json` (so hooks install on fresh clones).

### 4. Create `.husky/pre-commit`

Write this file (Husky v9+ needs no shebang):

```
npx lint-staged
npm run typecheck
npm run test
```

**Adapt:**
- Replace `npm run` with the detected manager's prefix (see step 1 table).
- If `package.json` has no `typecheck` script, omit that line and tell the user.
- If `package.json` has no `test` script, omit that line and tell the user.

### 5. Create `.lintstagedrc`

```json
{
  "*": "prettier --ignore-unknown --write"
}
```

`--ignore-unknown` skips files Prettier can't parse (images, binaries, etc.).

### 6. Create `.prettierrc` (only if missing)

Skip if any Prettier config already exists (`.prettierrc`, `.prettierrc.json`, `.prettierrc.js`, `prettier.config.js`, or a `prettier` key in `package.json`). Otherwise write:

```json
{
  "useTabs": false,
  "tabWidth": 2,
  "printWidth": 80,
  "singleQuote": false,
  "trailingComma": "es5",
  "semi": true,
  "arrowParens": "always"
}
```

### 7. Verify

- [ ] `.husky/pre-commit` exists and is executable
- [ ] `.lintstagedrc` exists
- [ ] `package.json` `prepare` script is `"husky"`
- [ ] A Prettier config exists
- [ ] `npx lint-staged` runs clean

### 8. Commit

Stage everything created/changed and commit:

```
Add pre-commit hooks (husky + lint-staged + prettier)
```

This commit runs through the new hook — a built-in smoke test that the whole chain works.

## Notes

- The hook runs lint-staged first (fast, staged-only), then full typecheck and tests — so formatting failures surface fast, before the slower passes.
- If the hook is too slow on large repos, consider dropping `test` from the pre-commit and moving it to pre-push or CI; keep lint-staged + typecheck local.
