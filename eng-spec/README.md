# eng-spec

> Convert approved PRD into TDD + Spec + ADRs with 5-agent review

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill eng-spec
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
cp -r eng-spec .cognition/skills/eng-spec
# or
cp -r eng-spec .windsurf/skills/eng-spec

# Global
cp -r eng-spec ~/.config/cognition/skills/eng-spec
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r eng-spec .claude/skills/eng-spec

# Global
cp -r eng-spec ~/.claude/skills/eng-spec
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r eng-spec .cursor/skills/eng-spec
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat eng-spec/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat eng-spec/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/eng-spec
```

## License

MIT
