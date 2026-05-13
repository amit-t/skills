# wisdom-capture

> Capture a wisdom snippet into a personal corpus — categorize, write, commit

**Category:** Leadership

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill wisdom-capture
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
cp -r wisdom-capture .cognition/skills/wisdom-capture
# or
cp -r wisdom-capture .windsurf/skills/wisdom-capture

# Global
cp -r wisdom-capture ~/.config/cognition/skills/wisdom-capture
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r wisdom-capture .claude/skills/wisdom-capture

# Global
cp -r wisdom-capture ~/.claude/skills/wisdom-capture
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r wisdom-capture .cursor/skills/wisdom-capture
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat wisdom-capture/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat wisdom-capture/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/wisdom-capture
```

Or in Codex:

```
$wisdom-capture
```

This skill is designed for the [`wisdom`](https://github.com/amit-t/wisdom)
companion repository, which provides a CLI launcher (`wisdom "snippet"`),
storage layout (`wisdoms/<YYYY>/<MM>/<ulid>.md`), and a closed-category file
(`wisdoms/_categories.yml`). The skill can be installed standalone in any
project that adopts the same data shape — see `REFERENCE.md` for the
frontmatter contract.

## License

MIT
