# prd-to-plan

> Turn a PRD into a phased implementation plan using tracer-bullet vertical slices

**Category:** Product Management

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill prd-to-plan
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
cp -r prd-to-plan .cognition/skills/prd-to-plan
# or
cp -r prd-to-plan .windsurf/skills/prd-to-plan

# Global
cp -r prd-to-plan ~/.config/cognition/skills/prd-to-plan
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r prd-to-plan .claude/skills/prd-to-plan

# Global
cp -r prd-to-plan ~/.claude/skills/prd-to-plan
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r prd-to-plan .cursor/skills/prd-to-plan
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat prd-to-plan/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat prd-to-plan/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/prd-to-plan
```

## License

MIT
