# Agent Skills

A collection of skills for AI coding agents. Skills are packaged instructions and workflows that extend agent capabilities across any tool that supports the [Agent Skills](https://github.com/vercel-labs/skills) format.

Compatible with **Devin**, **Claude Code**, **Cursor**, **Codex**, **Gemini CLI**, **Windsurf**, **GitHub Copilot**, **Cline**, **Roo**, and [many more](https://github.com/vercel-labs/skills).

## Quick Start

Install all skills:

```bash
npx skills@latest add amit-t/skills
```

Install a specific skill:

```bash
npx skills@latest add amit-t/skills --skill tdd
npx skills@latest add amit-t/skills --skill prd-draft
npx skills@latest add amit-t/skills --skill eng-spec
```

Install for a specific agent:

```bash
npx skills@latest add amit-t/skills --agent claude-code cursor
```

Install globally (available in all projects):

```bash
npx skills@latest add amit-t/skills -g
```

## Available Skills

### Product Management

| Skill | Description |
|-------|-------------|
| [`prd-draft`](./prd-draft) | Create modern, AI-era PRDs through guided interview |
| [`prd-review-panel`](./prd-review-panel) | Multi-agent PRD review from 7 perspectives |
| [`prd-approve`](./prd-approve) | Approve a reviewed PRD and update pipeline |
| [`prd-to-plan`](./prd-to-plan) | Turn a PRD into a phased implementation plan using tracer-bullet vertical slices |
| [`write-a-prd`](./write-a-prd) | Create a PRD through interview, codebase exploration, and module design |

### Project Management

| Skill | Description |
|-------|-------------|
| [`pmo-status`](./pmo-status) | Full project status across Product, Engineering DOE, and Implementation |

### Engineering

| Skill | Description |
|-------|-------------|
| [`eng-spec`](./eng-spec) | Convert approved PRD into TDD + Spec + ADRs with 5-agent review |
| [`tdd`](./tdd) | Test-driven development with red-green-refactor loop |
| [`git-guardrails-claude-code`](./git-guardrails-claude-code) | Block dangerous git commands before they execute |
| [`ubiquitous-language`](./ubiquitous-language) | Extract DDD-style ubiquitous language glossary |
| [`qa`](./qa) | Interactive QA session: report bugs conversationally, agent files GitHub issues |
| [`request-refactor-plan`](./request-refactor-plan) | Create a detailed refactor plan with tiny commits via interview, filed as GitHub issue |
| [`grill-me`](./grill-me) | Stress-test a plan or design through relentless interview |

### UX Design

| Skill | Description |
|-------|-------------|
| [`design-interview`](./design-interview) | Interactive design brief interview before generating screens |
| [`design-draft`](./design-draft) | Full UXD workflow from design interview to developer handoff |
| [`design-review`](./design-review) | Multi-agent design review from 5 perspectives |

### Agent Behavior

| Skill | Description |
|-------|-------------|
| [`concise-reporting`](./concise-reporting) | Ultra-concise status/progress reporting; full verbosity preserved for written artifacts |
| [`precision-mode`](./precision-mode) | Universal conciseness directive — makes every LLM response shorter, denser, and more precise |

### AI Agent

| Skill | Description |
|-------|-------------|
| [`write-a-skill`](./write-a-skill) | Create new agent skills with proper structure |

## What Are Skills?

Skills are self-contained units of functionality that teach AI coding agents how to perform specific tasks. Each skill is a `SKILL.md` file (with optional companion files) that gets loaded into the agent's context when invoked.

Skills can be invoked by name (e.g., `/tdd`, `/prd-draft`) or automatically triggered by the agent when relevant.

## Manual Installation

If you prefer not to use the CLI, copy skill directories into your agent's skills folder:

| Agent | Project Path | Global Path |
|-------|-------------|-------------|
| Devin / Windsurf | `.cognition/skills/` or `.windsurf/skills/` | `~/.config/cognition/skills/` |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` |
| Cursor | `.cursor/skills/` | — |
| Codex | Append to `AGENTS.md` | — |
| Gemini CLI | Append to `GEMINI.md` | — |

## License

MIT
