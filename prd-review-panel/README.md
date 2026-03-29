# prd-review-panel

> Multi-agent PRD review from 7 perspectives

**Category:** Product Management

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill prd-review-panel
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
cp -r prd-review-panel .cognition/skills/prd-review-panel
# or
cp -r prd-review-panel .windsurf/skills/prd-review-panel

# Global
cp -r prd-review-panel ~/.config/cognition/skills/prd-review-panel
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r prd-review-panel .claude/skills/prd-review-panel

# Global
cp -r prd-review-panel ~/.claude/skills/prd-review-panel
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r prd-review-panel .cursor/skills/prd-review-panel
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat prd-review-panel/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat prd-review-panel/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/prd-review-panel
```

## License

MIT
