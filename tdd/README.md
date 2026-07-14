# tdd

> Test-driven development via the red → green loop — seams, anti-patterns, and vertical slices

**Category:** Engineering

The red → green loop, made to produce tests worth keeping. Defines what a good test is (verifies behavior through public interfaces, survives refactors), where tests go (**seams** — pre-agreed public boundaries, confirmed with the user before any test is written), and the anti-patterns to catch: implementation-coupled tests, tautological assertions, and horizontal slicing (writing all tests before any implementation). Work proceeds in **vertical slices** — one test → one minimal implementation → repeat — each test a tracer bullet informed by the last cycle. Refactoring is deliberately out of the loop; it belongs to the review stage, handled by this repo's [`two-axis-review`](../two-axis-review) skill.

Synced from [`mattpocock/skills` → `engineering/tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd).

## When to use

- "Build this feature test-first" / "fix this bug with TDD"
- "red-green-refactor"
- Adding integration tests for a new capability
- Any time seams and testing scope need to be agreed before code is written

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill tdd
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
cp -r tdd .cognition/skills/tdd
# or
cp -r tdd .windsurf/skills/tdd

# Global
cp -r tdd ~/.config/cognition/skills/tdd
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r tdd .claude/skills/tdd

# Global
cp -r tdd ~/.claude/skills/tdd
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r tdd .cursor/skills/tdd
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat tdd/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat tdd/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/tdd
```

## License

MIT
