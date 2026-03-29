# design-draft

> Full UXD workflow from design interview to developer handoff

**Category:** UX Design

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill design-draft
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
cp -r design-draft .cognition/skills/design-draft
# or
cp -r design-draft .windsurf/skills/design-draft

# Global
cp -r design-draft ~/.config/cognition/skills/design-draft
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r design-draft .claude/skills/design-draft

# Global
cp -r design-draft ~/.claude/skills/design-draft
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r design-draft .cursor/skills/design-draft
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat design-draft/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat design-draft/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/design-draft
```

## License

MIT
