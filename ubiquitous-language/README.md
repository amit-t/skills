# ubiquitous-language

> Extract DDD-style ubiquitous language glossary

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill ubiquitous-language
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
cp -r ubiquitous-language .cognition/skills/ubiquitous-language
# or
cp -r ubiquitous-language .windsurf/skills/ubiquitous-language

# Global
cp -r ubiquitous-language ~/.config/cognition/skills/ubiquitous-language
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r ubiquitous-language .claude/skills/ubiquitous-language

# Global
cp -r ubiquitous-language ~/.claude/skills/ubiquitous-language
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r ubiquitous-language .cursor/skills/ubiquitous-language
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat ubiquitous-language/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat ubiquitous-language/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/ubiquitous-language
```

## License

MIT
