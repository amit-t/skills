# repo-context-scan

> Scan a codebase to build CONTEXT.md (or CONTEXT-MAP.md for multi-context repos) and seed ADRs for clearly-deliberate decisions. Autonomous by default — asks only on blocking ambiguity.

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill repo-context-scan
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
cp -r repo-context-scan .cognition/skills/repo-context-scan
# or
cp -r repo-context-scan .windsurf/skills/repo-context-scan

# Global
cp -r repo-context-scan ~/.config/cognition/skills/repo-context-scan
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r repo-context-scan .claude/skills/repo-context-scan

# Global
cp -r repo-context-scan ~/.claude/skills/repo-context-scan
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r repo-context-scan .cursor/skills/repo-context-scan
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat repo-context-scan/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat repo-context-scan/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/repo-context-scan
```

The skill is idempotent — safe to re-run as the codebase evolves.

## Companion skill

After scanning, use `/domain-grill` to stress-test new engineering artifacts (eng specs, TDD plans, refactor proposals, technical designs) against the generated `CONTEXT.md`. For PRDs or non-technical artifacts, use `/grill-me` instead.

## License

MIT
