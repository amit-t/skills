# concise-reporting

> Ultra-concise status/progress reporting; full verbosity preserved for written artifacts

**Category:** Agent Behavior

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill concise-reporting
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
cp -r concise-reporting .cognition/skills/concise-reporting
# or
cp -r concise-reporting .windsurf/skills/concise-reporting

# Global
cp -r concise-reporting ~/.config/cognition/skills/concise-reporting
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r concise-reporting .claude/skills/concise-reporting

# Global
cp -r concise-reporting ~/.claude/skills/concise-reporting
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r concise-reporting .cursor/skills/concise-reporting
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat concise-reporting/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat concise-reporting/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```text
/concise-reporting
```

## License

MIT
