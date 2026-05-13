# session-feedback

> Mine the current conversation for every correction the user made, every preference they stated, and every "do-differently" lesson. Write a dated feedback file into the project's auto-memory directory so future sessions reload the patterns.

**Category:** Agent Behavior

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill session-feedback
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
cp -r session-feedback .cognition/skills/session-feedback
# or
cp -r session-feedback .windsurf/skills/session-feedback

# Global
cp -r session-feedback ~/.config/cognition/skills/session-feedback
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r session-feedback .claude/skills/session-feedback

# Global
cp -r session-feedback ~/.claude/skills/session-feedback
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r session-feedback .cursor/skills/session-feedback
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat session-feedback/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat session-feedback/SKILL.md >> GEMINI.md
```

</details>

## Usage

```
/session-feedback                  # write feedback-<today>.md to project memory dir
/session-feedback <path>           # write to a specific path
/session-feedback --overwrite      # replace an existing same-day file
/session-feedback --since "topic"  # only mine turns about a specific topic
```

## Three buckets

- **Corrections** — places the user pushed back on or changed your proposal
- **Preferences** — explicit statements of how the user wants things done (with cited authorities preserved)
- **Do differently** — synthesised general principles that would have led to the right answer first time

## Output

A dated, frontmatter-tagged markdown file under the project's Claude Code auto-memory directory, plus a one-line entry in `MEMORY.md` so the file is surfaced in future sessions.

## License

MIT
