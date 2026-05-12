# leadership-update

> Reformat raw notes into an outcome-first update leadership actually remembers

**Category:** Leadership

Turns messy status notes into a three-sentence update — outcome, reasoning, next — with a clear ask at the end. Auto-detects whether to reformat directly or run a 1–3 question interview to fill in missing slots. Default output is a verbal/standup script; can also produce Slack/chat, email, or written status-doc formats.

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill leadership-update
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
cp -r leadership-update .cognition/skills/leadership-update
# or
cp -r leadership-update .windsurf/skills/leadership-update

# Global
cp -r leadership-update ~/.config/cognition/skills/leadership-update
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r leadership-update .claude/skills/leadership-update

# Global
cp -r leadership-update ~/.claude/skills/leadership-update
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r leadership-update .cursor/skills/leadership-update
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat leadership-update/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat leadership-update/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/leadership-update
```

Then either:
- Paste your raw notes (the agent will reformat directly), or
- Type the command alone (the agent will ask 1–3 short questions to fill in status, reasoning, next, and ask).

## Source

Framework derived from a public reel by Yasar Ahmad (Leadership Coach, @yasarahmad_): https://www.instagram.com/p/DVtAWlpjU67/

## License

MIT
