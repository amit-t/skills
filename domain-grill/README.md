# domain-grill

> Engineering-only. Stress-test an engineering artifact (eng spec, TDD, refactor plan, technical design, schema migration, API contract) against the project's `CONTEXT.md`. For PRDs and non-technical artifacts, use `/grill-me` instead.

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill domain-grill
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
cp -r domain-grill .cognition/skills/domain-grill
# or
cp -r domain-grill .windsurf/skills/domain-grill

# Global
cp -r domain-grill ~/.config/cognition/skills/domain-grill
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r domain-grill .claude/skills/domain-grill

# Global
cp -r domain-grill ~/.claude/skills/domain-grill
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r domain-grill .cursor/skills/domain-grill
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat domain-grill/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat domain-grill/SKILL.md >> GEMINI.md
```

</details>

## Usage

Prerequisite: a `CONTEXT.md` (or `CONTEXT-MAP.md`) at the repo root or in the relevant module. If absent, run `/repo-context-scan` first.

Invoke in your agent session:

```
/domain-grill
```

## Scope

**Use for:** eng specs, TDD plans, refactor proposals, architecture sketches, technical design docs, API contracts, schema migrations, IaC plans.

**Do not use for:** PRDs, marketing plans, business strategy, resume drafts, product-level RFCs, anything not anchored in code or schema. The skill will refuse and redirect you to `/grill-me`.

## Companion skills

- `/repo-context-scan` — owns `CONTEXT.md`; run it to build or refresh the context this skill grills against.
- `/grill-me` — non-code-grounded interview for PRDs and general plans.

## License

MIT
