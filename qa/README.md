# qa

> Interactive QA session: report bugs conversationally, agent files GitHub issues

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill qa
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
cp -r qa .cognition/skills/qa
# or
cp -r qa .windsurf/skills/qa

# Global
cp -r qa ~/.config/cognition/skills/qa
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r qa .claude/skills/qa

# Global
cp -r qa ~/.claude/skills/qa
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r qa .cursor/skills/qa
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat qa/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat qa/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/qa
```

## License

MIT
