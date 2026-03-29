# git-guardrails-claude-code

> Block dangerous git commands before they execute

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill git-guardrails-claude-code
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
cp -r git-guardrails-claude-code .cognition/skills/git-guardrails-claude-code
# or
cp -r git-guardrails-claude-code .windsurf/skills/git-guardrails-claude-code

# Global
cp -r git-guardrails-claude-code ~/.config/cognition/skills/git-guardrails-claude-code
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r git-guardrails-claude-code .claude/skills/git-guardrails-claude-code

# Global
cp -r git-guardrails-claude-code ~/.claude/skills/git-guardrails-claude-code
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r git-guardrails-claude-code .cursor/skills/git-guardrails-claude-code
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat git-guardrails-claude-code/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat git-guardrails-claude-code/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/git-guardrails-claude-code
```

## License

MIT
