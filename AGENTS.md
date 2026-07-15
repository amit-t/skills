# Project Agent Instructions

## Repository Overview

This is the `amit-t/skills` repository — a catalog of reusable agent skills for AI coding agents. Each skill lives in its own top-level directory with a `SKILL.md` and `README.md`.

## Catalog Sync Rule (MANDATORY)

Whenever you add, remove, rename, or meaningfully modify a skill, you **must** update all of the following before committing:

### 1. `README.md` (root)

- Add/remove the skill row in the correct category table under **Available Skills**
- Format: `| [\`skill-name\`](./skill-name) | One-line description |`
- Keep rows sorted alphabetically within each category table

### 2. `skills.json` — skills array

- Add/remove the skill object in the `skills` array (`site.js` fetches this file at runtime)
- Required fields: `slug`, `name`, `category`, `tagline`, `detail`, `usage`
- Place the entry with others in the same category
- Valid categories: `Product Management`, `Project Management`, `Engineering`, `UX Design`, `Agent Behavior`, `AI Agent`, `Leadership`

### 3. `changelog.json` — changes array

- Add a new entry or append to today's date entry in the `changes` array at the top (`site.js` fetches this file at runtime)
- Format: `"Added <skill-name> skill — <short description>."`

### 4. `CHANGELOG.md`

- Add a bullet under today's date heading (create the heading if it doesn't exist)
- Format: `- Added the \`skill-name\` skill — short description.`

### 5. Per-skill files

- `skill-name/SKILL.md` — the skill instructions (required)
- `skill-name/README.md` — install guide following the existing template (required)

## Category → CSS Class Mapping (for reference)

If you ever touch `site.js` rendering logic, these are the category-to-class mappings:

| Category | CSS Class |
|---|---|
| Product Management | `cat-product-management` |
| Project Management | `cat-project-management` |
| Engineering | `cat-engineering` |
| UX Design | `cat-ux-design` |
| Agent Behavior | `cat-agent-behavior` |
| AI Agent | `cat-ai-agent` |
| Leadership | `cat-leadership` |

## Git Conventions

- Branch: `main` is the only long-lived branch. Work on short-lived feature branches (`feat/...`, `fix/...`, `docs/...`), merge to `main` via PR, then delete the feature branch. No long-lived `dev`/`develop` branch.
- Commit style: `feat:`, `fix:`, `docs:`, `refactor:` with scope
- Push regularly; never leave work uncommitted

## Skill Authoring

See the installed `write-a-skill` skill (`.agents/skills/write-a-skill/SKILL.md`) for SKILL.md structure, description requirements, and review checklist.

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `graphify update .` to keep the graph current (AST-only, no API cost)
