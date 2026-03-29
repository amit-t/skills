# design-review

> Multi-agent design review from 5 perspectives

**Category:** UX Design

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill design-review
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
cp -r design-review .cognition/skills/design-review
# or
cp -r design-review .windsurf/skills/design-review

# Global
cp -r design-review ~/.config/cognition/skills/design-review
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r design-review .claude/skills/design-review

# Global
cp -r design-review ~/.claude/skills/design-review
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r design-review .cursor/skills/design-review
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat design-review/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat design-review/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/design-review
```

## License

MIT
