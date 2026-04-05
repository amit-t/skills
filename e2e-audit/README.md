# e2e-audit

> Run a Playwright end-to-end audit of a web app using its PRDs as the test spec

**Category:** Engineering

## What It Does

Runs a Playwright end-to-end audit of your web app against its PRDs and produces a diagnostic report showing what's working and what's not from a user's perspective. The skill:

1. Discovers PRDs, existing e2e infrastructure, routes, and auth strategy
2. Scaffolds a Playwright e2e package if none exists (config, fixtures, seed users)
3. Writes PRD-driven tests — page loads, core actions, permission gates, data renders, error states
4. Runs the suite and interprets failures (missing routes, incomplete UI, timeouts)
5. Exports a markdown diagnostic report to `outputs/analyses/`

### When to Use

- Before a release to verify PRD coverage end-to-end
- After a large feature lands to check what's actually working
- When onboarding to a codebase and you want a quick health check
- Any time you need a user-perspective audit of route and feature status

## Install

```bash
npx skills@latest add amit-t/skills --skill e2e-audit
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r e2e-audit .cognition/skills/e2e-audit
# or
cp -r e2e-audit .windsurf/skills/e2e-audit

# Global
cp -r e2e-audit ~/.config/cognition/skills/e2e-audit
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r e2e-audit .claude/skills/e2e-audit

# Global
cp -r e2e-audit ~/.claude/skills/e2e-audit
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r e2e-audit .cursor/skills/e2e-audit
```

</details>

<details>
<summary>Codex</summary>

```bash
cat e2e-audit/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat e2e-audit/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```text
/e2e-audit
```

Options:

```text
/e2e-audit --area auth        # Audit one PRD area only
/e2e-audit --report-only      # Skip test run, just format last results
/e2e-audit --export           # Export results to outputs/analyses/
```

## License

MIT
