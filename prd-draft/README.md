# prd-draft

> Create modern, AI-era PRDs through guided interview

**Category:** Product Management

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill prd-draft
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
cp -r prd-draft .cognition/skills/prd-draft
# or
cp -r prd-draft .windsurf/skills/prd-draft

# Global
cp -r prd-draft ~/.config/cognition/skills/prd-draft
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r prd-draft .claude/skills/prd-draft

# Global
cp -r prd-draft ~/.claude/skills/prd-draft
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r prd-draft .cursor/skills/prd-draft
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat prd-draft/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat prd-draft/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/prd-draft
```

## License

MIT
