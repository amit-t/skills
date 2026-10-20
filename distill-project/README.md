# distill-project

> Distill project history into durable instructions and a context file with exact output templates.

**Category:** Agent Behavior

## What It Does

Reads reachable project conversations, files, docs, memories, and published outputs as evidence, then writes:

- A short rules file (`CLAUDE.md` or `AGENTS.md`) for future sessions.
- A growing context file such as `docs/project-context.md` containing sources, past outputs, process, exact templates, and known fixes.

The skill keeps accepted user decisions separate from unconfirmed assistant suggestions, preserves privacy boundaries, and updates existing files in place.

## Usage

```text
/distill-project
```

Use when asking an agent to learn from a project, capture house style, turn project chats into rules, update project context, or write `CLAUDE.md` or `AGENTS.md`.

## Install

```bash
npx skills@latest add amit-t/skills --skill distill-project
```

### Manual installation

Run these commands from the repository root. Links keep this folder as the source.

```bash
# Claude Code
mkdir -p ~/.claude/skills ~/.agents/skills
ln -s "$(pwd)/distill-project" ~/.claude/skills/distill-project

# Codex, Gemini CLI, GitHub Copilot CLI, Windsurf, or Devin CLI
ln -s "$(pwd)/distill-project" ~/.agents/skills/distill-project
```

Claude Code Cowork and claude.ai account skills are installed through the product's Skills interface. Upload `dist/distill-project.skill` as a ZIP with one top-level `distill-project/` folder. ChatGPT Skills uses Skills > Create > Upload from your computer on eligible workspaces; select `dist/distill-project.zip`, a link to the same archive. No upload happens during local installation. Do not upload project outputs or private source material.

The skill's source is `distill-project/`; `dist/distill-project.skill` is the portable package.

## License

MIT
