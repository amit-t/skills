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

### Grill depth

The skill asks how deep to grill after loading `CONTEXT.md` and before the first question. **Default is `deep`** (deepest):

| Depth | Aliases | What you get |
| --- | --- | --- |
| `deep` | `3`, `deepest` | Every branch, every dependency. Full glossary challenge + fuzzy-language sharpening + invented edge-case scenarios + code cross-checks + ADR contradiction surfacing + new-term flagging. Unbounded until shared understanding. |
| `standard` | `2`, `medium` | Architectural spine plus obvious edges. Full glossary + fuzzy-language + spine scenarios. Code / ADR cross-checks on the main path only. ~15–25 questions. |
| `quick` | `1`, `sharp` | Top 5 highest-leverage hard-hitters only. Glossary conflicts that would mislead implementers, ADR contradictions, and the 1–2 most dangerous boundary scenarios. ~5–10 questions. Triage, not full coverage. |

Pre-select to skip the prompt:

```
/domain-grill deep        # default
/domain-grill standard
/domain-grill quick
```

Depth never lowers rigor on the questions asked — it changes how many branches the skill walks, not how sharp each question is. ADR-recording criteria and the end-of-session summary apply at every depth.

## Scope

**Use for:** eng specs, TDD plans, refactor proposals, architecture sketches, technical design docs, API contracts, schema migrations, IaC plans.

**Do not use for:** PRDs, marketing plans, business strategy, resume drafts, product-level RFCs, anything not anchored in code or schema. The skill will refuse and redirect you to `/grill-me`.

## Companion skills

- `/repo-context-scan` — owns `CONTEXT.md`; run it to build or refresh the context this skill grills against.
- `/grill-me` — non-code-grounded interview for PRDs and general plans.

## License

MIT
