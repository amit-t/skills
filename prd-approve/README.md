# prd-approve

> Approve a reviewed PRD and update pipeline

**Category:** Product Management

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill prd-approve
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
cp -r prd-approve .cognition/skills/prd-approve
# or
cp -r prd-approve .windsurf/skills/prd-approve

# Global
cp -r prd-approve ~/.config/cognition/skills/prd-approve
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r prd-approve .claude/skills/prd-approve

# Global
cp -r prd-approve ~/.claude/skills/prd-approve
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r prd-approve .cursor/skills/prd-approve
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat prd-approve/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat prd-approve/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/prd-approve
```

## License

MIT
