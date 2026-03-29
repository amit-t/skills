# pmo-status

> Full project status across Product, Engineering DOE, and Implementation

**Category:** Project Management

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill pmo-status
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
cp -r pmo-status .cognition/skills/pmo-status
# or
cp -r pmo-status .windsurf/skills/pmo-status

# Global
cp -r pmo-status ~/.config/cognition/skills/pmo-status
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r pmo-status .claude/skills/pmo-status

# Global
cp -r pmo-status ~/.claude/skills/pmo-status
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r pmo-status .cursor/skills/pmo-status
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat pmo-status/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat pmo-status/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/pmo-status
```

## License

MIT
