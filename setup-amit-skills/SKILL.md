---
name: setup-amit-skills
description: Use when configuring a repository for amit-t/skills conventions, bootstrapping AGENTS.md or CLAUDE.md, docs/agents context docs, ADR layout, or skill catalog category vocabulary. Triggers include "setup amit skills", "configure amit skills", "/setup-amit-skills", and "make this repo work with amit-t/skills".
---

# Setup Amit Skills

Prompt-driven setup for a repo that will consume skills from the `amit-t/skills` catalog. Configure only what the repo needs; do not force catalog-authoring rules onto ordinary codebases.

## Assumptions

- This skill configures conventions and starter docs only. It does not install skills, open PRs, create issues, or run downstream skills.
- Prefer existing repo conventions when visible; ask before replacing or widening them.
- If the repo already has equivalent guidance, update in place with a clearly marked `amit-t/skills` section instead of duplicating whole files.

## Workflow

### 1. Explore repo state

Inspect before asking:

- Git remotes and default branch hints (`git remote -v`, current branch, recent status)
- Existing agent instruction files: `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, `.cursor/rules`, `.windsurf/`
- Existing context docs: `CONTEXT.md`, `CONTEXT-MAP.md`, `docs/agents/`, module-level context files
- Existing ADR layout: `docs/adr/`, `docs/adrs/`, `adr/`, numbered decision docs
- Skill-catalog signals: top-level skill dirs with `SKILL.md`, root `README.md` Available Skills tables, `site.js`, `CHANGELOG.md`, `skills.json`, `changelog.json`
- Project docs that may already define categories, labels, or working agreements

Summarize findings in bullets. Mark inferred facts as `Inference:`.

### 2. Present findings and ask 3 decisions sequentially

Ask one decision at a time. For each, show the recommended option first, 2-3 choices, and one short consequence per choice. Wait for the user's answer before the next decision.

#### Decision 1 — Agent instruction surface

Recommended: use the repo's existing canonical file; if none exists, create `AGENTS.md`.

Choices:

1. `AGENTS.md` only — best for Codex and cross-agent repo guidance.
2. `CLAUDE.md` only — best when the repo is Claude Code-first.
3. Both `AGENTS.md` and `CLAUDE.md` — best for mixed-agent teams; keep shared content identical or cross-linked.

Why it matters: downstream skills need stable instructions for zsh preference, docs ownership, ADR paths, and repo-specific rules.

#### Decision 2 — Domain context layout

Recommended: single `CONTEXT.md` unless multiple bounded contexts are visible.

Choices:

1. Single context — root `CONTEXT.md` plus `docs/agents/` notes for skill usage.
2. Multi-context — root `CONTEXT-MAP.md` plus per-context `CONTEXT.md` files.
3. Defer context docs — only write setup instructions telling the user to run `/repo-context-scan` later.

Why it matters: `/repo-context-scan` owns context generation and `/domain-grill` consumes it read-only.

#### Decision 3 — Catalog/category mode

Recommended: `consumer-only` unless this repo authors reusable skills.

Choices:

1. Consumer-only — include downstream skill usage conventions, ADR path, and context-doc layout; no catalog sync rules.
2. Skill-catalog authoring — include `SKILL.md` + `README.md` per skill, valid categories, and catalog sync checklist.
3. Hybrid — consumer guidance plus a short category vocabulary appendix for occasional internal skill authoring.

Why it matters: the amit-t catalog has a fixed category vocabulary: `Product Management`, `Project Management`, `Engineering`, `UX Design`, `Agent Behavior`, `AI Agent`, `Leadership`. Ordinary repos should not inherit catalog-maintenance burden unless they publish skills.

### 3. Confirm drafts before writing

Draft the exact file changes from the decisions. Show:

- Target paths to create/update
- Sections to add or modify
- Template sources to use:
  - `templates/agent-config-block.md`
  - `templates/context-layout-single.md`
  - `templates/context-layout-multi.md`
  - `templates/adr-format.md`
  - `templates/catalog-categories.md`
- Any assumptions or inferred mappings

Ask: `Write these changes?` Do not edit files until the user confirms.

### 4. Write/update files

After confirmation only:

- Update chosen agent instruction file(s) with an `amit-t/skills conventions` section.
- Create `docs/agents/` when the setup needs durable agent notes.
- If context layout is single and the user wants a starter file, write root `CONTEXT.md` from `templates/context-layout-single.md` only as a scaffold; otherwise leave `/repo-context-scan` to populate it.
- If context layout is multi, write root `CONTEXT-MAP.md` from `templates/context-layout-multi.md` only as a scaffold; ask before creating per-context files if contexts are inferred.
- Ensure ADR guidance points to `docs/adr/NNNN-slug.md` and copy the minimal format from `templates/adr-format.md` into `docs/agents/adr-format.md` if useful.
- If catalog/category mode is `skill-catalog authoring` or `hybrid`, include the category vocabulary from `templates/catalog-categories.md`.

Preserve user prose. Append marked sections rather than overwriting. If paths conflict, stop and ask.

### 5. Done message

Report:

- Files created/updated
- The 3 decisions selected
- Downstream skills now enabled:
  - `/repo-context-scan` once context docs are absent/stale or need generation
  - `/domain-grill` once `CONTEXT.md` or `CONTEXT-MAP.md` exists
  - `write-a-skill` when authoring new skills with the selected category vocabulary
  - `docs-from-prs` if the repo maintains README/docs from merged work
- Follow-up commands the user may run next
- Any assumptions still unresolved

Do not claim downstream skills ran unless you actually ran them.

## Common mistakes

- Writing files before the confirmation step.
- Copying catalog sync rules into a non-catalog repo.
- Creating both `CONTEXT.md` and `CONTEXT-MAP.md` without choosing single vs multi.
- Editing existing ADRs instead of appending new numbered ADRs.
- Treating templates as final truth; they are scaffolds to adapt after user confirmation.
