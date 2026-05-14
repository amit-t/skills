# grill-me

> Stress-test a plan or design through relentless interview

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill grill-me
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
cp -r grill-me .cognition/skills/grill-me
# or
cp -r grill-me .windsurf/skills/grill-me

# Global
cp -r grill-me ~/.config/cognition/skills/grill-me
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r grill-me .claude/skills/grill-me

# Global
cp -r grill-me ~/.claude/skills/grill-me
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r grill-me .cursor/skills/grill-me
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat grill-me/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat grill-me/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/grill-me
```

### Grill depth

The skill asks how deep to grill before starting. **Default is `deep`** (deepest):

| Depth | Aliases | What you get |
| --- | --- | --- |
| `deep` | `3`, `deepest` | Every branch of the decision tree, critical + edge + corner cases, cross-references to code, invented boundary scenarios. Unbounded until shared understanding. |
| `standard` | `2`, `medium` | Critical assumptions + main edge cases + obvious cross-references. Skip exotic corner cases. ~15–25 questions. |
| `quick` | `1`, `sharp` | Top 5 highest-leverage hard-hitters only. Deal-breaker assumptions and dead-on-arrival risks. ~5–10 questions. Triage, not full coverage. |

Pre-select to skip the prompt:

```
/grill-me deep        # default
/grill-me standard
/grill-me quick
```

Depth never lowers rigor on the questions asked — it changes how many branches the skill walks, not how sharp each question is.

## License

MIT
