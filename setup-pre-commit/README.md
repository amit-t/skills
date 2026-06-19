# setup-pre-commit

> Set up Husky pre-commit hooks with lint-staged (Prettier), type checking, and tests in the current JS/TS repo

**Category:** Engineering

Detects the repo's package manager (npm / pnpm / yarn / bun), installs `husky`, `lint-staged`, and `prettier` as devDependencies, runs `npx husky init`, then writes `.husky/pre-commit` (lint-staged → typecheck → test), `.lintstagedrc`, and `.prettierrc` (only if no Prettier config exists). It verifies the chain with `npx lint-staged` and commits so the new hook runs as a smoke test. Typecheck/test lines are omitted automatically when those scripts are missing from `package.json`.

Ported from [`mattpocock/skills` → `misc/setup-pre-commit`](https://github.com/mattpocock/skills/blob/main/skills/misc/setup-pre-commit/SKILL.md) and adapted to this catalog's conventions.

## When to use

- "Add pre-commit hooks to this repo"
- "Set up Husky / lint-staged / Prettier"
- "Run Prettier (and typecheck/tests) on commit"
- Onboarding a JS/TS project that has no commit-time formatting or checks

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill setup-pre-commit
```

Install all skills from this repository:

```bash
npx skills@latest add amit-t/skills
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r setup-pre-commit .cognition/skills/setup-pre-commit
# or
cp -r setup-pre-commit .windsurf/skills/setup-pre-commit

# Global
cp -r setup-pre-commit ~/.config/cognition/skills/setup-pre-commit
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r setup-pre-commit .claude/skills/setup-pre-commit

# Global
cp -r setup-pre-commit ~/.claude/skills/setup-pre-commit
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r setup-pre-commit .cursor/skills/setup-pre-commit
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat setup-pre-commit/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat setup-pre-commit/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/setup-pre-commit
```

The skill detects the package manager, installs the tooling, writes the hook and configs, verifies, and commits. See `SKILL.md` for the full step-by-step workflow and the files it creates.

## License

MIT
