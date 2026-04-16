# Project Instructions for Claude Code

## Repository Overview

This is the `amit-t/skills` repository — a catalog of reusable agent skills for AI coding agents. Each skill lives in its own top-level directory with a `SKILL.md` and `README.md`.

## Catalog Sync Rule (MANDATORY)

Whenever you add, remove, rename, or meaningfully modify a skill, you **must** update all of the following before committing:

1. **`README.md`** — add/remove the skill row in the correct category table under "Available Skills"
2. **`site.js` skills array** — add/remove the skill object (`slug`, `name`, `category`, `tagline`, `detail`, `usage`)
3. **`site.js` changes array** — add a changelog entry under today's date
4. **`CHANGELOG.md`** — add a bullet under today's date heading
5. **Per-skill files** — `skill-name/SKILL.md` (required) and `skill-name/README.md` (required)

Valid categories: `Product Management`, `Project Management`, `Engineering`, `UX Design`, `Agent Behavior`, `AI Agent`.

## Git Conventions

- Branch: work on `dev`, merge to `main` via PR
- Commit style: conventional commits (`feat:`, `fix:`, `docs:`, `refactor:`)

## Skill Authoring

See `AGENTS.md` for full details on catalog structure, CSS class mappings, and the `write-a-skill` reference.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current
