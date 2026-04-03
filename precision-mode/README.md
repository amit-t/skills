# precision-mode

> Universal conciseness directive — makes every LLM response shorter, denser, and more precise

**Category:** Agent Behavior

## What It Does

A single prompt injector that eliminates verbosity from **all** LLM output — not just reporting. Prepend it to any system prompt (ChatGPT, Claude, Gemini, Copilot, local models, API calls) to get tighter responses across the board.

Derived from [`concise-reporting`](../concise-reporting), but generalized: applies to answers, code, explanations, plans, emails, docs — everything.

### Key Rules It Enforces

- Lead with the answer, no preamble
- No filler phrases ("Sure!", "Certainly!", "Great question!")
- No echo of the user's request
- No trailing summaries
- Fragments over sentences when clear
- Tables/bullets over paragraphs
- Code over English for code questions
- Quantify, don't qualify

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill precision-mode
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r precision-mode .cognition/skills/precision-mode
# or
cp -r precision-mode .windsurf/skills/precision-mode

# Global
cp -r precision-mode ~/.config/cognition/skills/precision-mode
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r precision-mode .claude/skills/precision-mode

# Global
cp -r precision-mode ~/.claude/skills/precision-mode
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r precision-mode .cursor/skills/precision-mode
```

</details>

<details>
<summary>Codex</summary>

```bash
cat precision-mode/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat precision-mode/SKILL.md >> GEMINI.md
```

</details>

## Use as Standalone Prompt Injector

Copy the content between the `---` fences in [`SKILL.md`](./SKILL.md) and prepend it to any system prompt. Works with:

- **ChatGPT** — paste into Custom Instructions → "How would you like ChatGPT to respond?"
- **Claude** — paste into Project Instructions or system prompt via API
- **Gemini** — paste into system instruction field
- **API calls** — prepend to your `system` message
- **Local models** — add to your system prompt template

## Usage

Once installed as an agent skill, invoke in your session:

```text
/precision-mode
```

## License

MIT
