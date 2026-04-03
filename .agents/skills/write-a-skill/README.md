# write-a-skill

> Create new agent skills with proper structure

**Category:** AI Agent

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill write-a-skill
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
cp -r write-a-skill .cognition/skills/write-a-skill
# or
cp -r write-a-skill .windsurf/skills/write-a-skill

# Global
cp -r write-a-skill ~/.config/cognition/skills/write-a-skill
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r write-a-skill .claude/skills/write-a-skill

# Global
cp -r write-a-skill ~/.claude/skills/write-a-skill
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r write-a-skill .cursor/skills/write-a-skill
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat write-a-skill/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat write-a-skill/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/write-a-skill
```

## License

MIT
