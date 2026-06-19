# setup-amit-skills

> Configure a repository to work with `amit-t/skills` conventions: agent instructions, domain context docs, ADR layout, and optional skill-catalog category vocabulary.

**Category:** Engineering

## What it does

`setup-amit-skills` is a prompt-driven setup workflow. It explores a repo, presents findings, asks three sequential configuration decisions, confirms the draft changes, then writes the selected scaffolding.

It is designed for repos that will use skills such as `/repo-context-scan`, `/domain-grill`, `write-a-skill`, and `docs-from-prs`.

## When to use

Use this when you want to:

- Make a repo ready for `amit-t/skills` Engineering or Agent Behavior workflows
- Add or normalize `AGENTS.md` / `CLAUDE.md` agent guidance
- Decide between single-context and multi-context domain docs
- Standardize ADR docs under `docs/adr/`
- Add the amit-t skill catalog category vocabulary to a repo that authors skills

## Example triggers

```text
/setup-amit-skills
setup amit skills in this repo
configure this repo for amit-t/skills
make this repo work with repo-context-scan and domain-grill
add amit skill catalog conventions here
```

## Workflow summary

1. Explore repo state: remotes, agent files, context docs, ADR dirs, catalog signals.
2. Ask three decisions: agent instruction surface, domain context layout, catalog/category mode.
3. Confirm the exact draft before writing.
4. Write/update only the selected config files and docs.
5. Report which downstream skills can now operate.

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill setup-amit-skills
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
cp -r setup-amit-skills .cognition/skills/setup-amit-skills
# or
cp -r setup-amit-skills .windsurf/skills/setup-amit-skills

# Global
cp -r setup-amit-skills ~/.config/cognition/skills/setup-amit-skills
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r setup-amit-skills .claude/skills/setup-amit-skills

# Global
cp -r setup-amit-skills ~/.claude/skills/setup-amit-skills
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r setup-amit-skills .cursor/skills/setup-amit-skills
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat setup-amit-skills/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat setup-amit-skills/SKILL.md >> GEMINI.md
```

</details>

## License

MIT
