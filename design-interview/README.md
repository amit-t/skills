# design-interview

> Interactive design brief interview before generating screens

**Category:** UX Design

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill design-interview
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
cp -r design-interview .cognition/skills/design-interview
# or
cp -r design-interview .windsurf/skills/design-interview

# Global
cp -r design-interview ~/.config/cognition/skills/design-interview
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r design-interview .claude/skills/design-interview

# Global
cp -r design-interview ~/.claude/skills/design-interview
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r design-interview .cursor/skills/design-interview
```

</details>

<details>
<summary>Codex</summary>

```bash
# Project-level (Agent Skills standard dir; Codex discovers SKILL.md here)
cp -r design-interview .agents/skills/design-interview

# Global
cp -r design-interview ~/.agents/skills/design-interview
```

Model-invoked, or mention explicitly with `$design-interview`.

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat design-interview/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/design-interview
```

## License

MIT
