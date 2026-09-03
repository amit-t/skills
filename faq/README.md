# faq

> Answer a question about the current repo from its source of truth, then record the Q&A as a permanent entry in the repo's FAQ document. Dedupes against existing entries and matches the FAQ's format and voice.

**Category:** Engineering

## What It Does

Turns real questions (often pasted from a teammate) into durable documentation:

1. Locates the repo's FAQ (`docs/faq.md`, `FAQ.md`, variants) or creates one, matching sibling front-matter conventions (Jekyll/MkDocs aware).
2. Checks existing entries first; an entry covering the same topic gets updated, never duplicated.
3. Researches the answer from code and scripts before docs, quoting exact flags, paths, defaults, and enums.
4. Writes one dense entry per question: heading is the question, answer leads with the direct answer.
5. Replies in chat with the forwardable answer plus the FAQ path and heading. Never commits on its own.

Project-agnostic. Strips the asker's name from the recorded entry and respects the repo's writing rules from `CLAUDE.md` / `AGENTS.md`.

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill faq
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r faq .cognition/skills/faq
# or
cp -r faq .windsurf/skills/faq

# Global
cp -r faq ~/.config/cognition/skills/faq
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r faq .claude/skills/faq

# Global
cp -r faq ~/.claude/skills/faq
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r faq .cursor/skills/faq
```

</details>

<details>
<summary>Codex</summary>

```bash
cat faq/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat faq/SKILL.md >> GEMINI.md
```

</details>

## Usage

```text
/faq <question>
/faq --dry-run <question>   # answer + proposed entry, no file write
/faq                        # prompts for the question
```

## When to Use

- A teammate asks a question you had to dig through code to answer — capture it so the next person doesn't ask again.
- Piloting a tool and fielding recurring onboarding questions.
- Backfilling an FAQ from a support thread, one question at a time.

## License

MIT
