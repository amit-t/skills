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
| [`code-review`](./code-review) | Principal-engineer review of a GitHub PR with two-phase approval — pre-checks PR description, size, single-concern scope, then walks 11-dimension findings one at a time before posting |
| [`docs-from-prs`](./docs-from-prs) | Survey merged PRs, fill doc gaps in README and other user-facing docs, audit drift hot spots, and run a grammar/casing/alignment pass |
| [`domain-grill`](./domain-grill) | Engineering-only stress-test of an eng spec / TDD / refactor / tech design against `CONTEXT.md` (use `/grill-me` for PRDs and non-technical plans) |
| [`e2e-audit`](./e2e-audit) | Playwright PRD audit + persona screenshot demo + auto-emit one ralph task per bug to `fix_plan.md` |
| [`eng-spec`](./eng-spec) | Convert approved PRD into TDD + Spec + ADRs with 5-agent review |
| [`gh-pages-neo-brutalist`](./gh-pages-neo-brutalist) | Drop-in Jekyll templates that scaffold a GitHub Pages site with a neo-brutalist design system (4 themes, IBM Plex Mono, hard borders, offset shadows) |
| [`gh-repo-mirror`](./gh-repo-mirror) | Scaffold a new GitHub repo that mirrors a reference repo's settings, branch protection, security flags, and (optional) GitHub Pages site |
| [`git-guardrails-claude-code`](./git-guardrails-claude-code) | Block dangerous git commands before they execute |
| [`grill-me`](./grill-me) | Stress-test a plan or design through relentless interview |
| [`package-scout`](./package-scout) | Research, compare, and select the best packages before installing any dependency |
| [`qa`](./qa) | Interactive QA session: report bugs conversationally, agent files GitHub issues |
| [`repo-context-scan`](./repo-context-scan) | Scan a codebase to build `CONTEXT.md` (or `CONTEXT-MAP.md` for multi-context repos) and seed ADRs for clearly-deliberate decisions |
| [`request-refactor-plan`](./request-refactor-plan) | Create a detailed refactor plan with tiny commits via interview, filed as GitHub issue |
| [`resume-tailoring`](./resume-tailoring) | Tailor a resume to a specific job — research, branching discovery, confidence-scored matching, MD+DOCX+PDF+report |
| [`tdd`](./tdd) | Test-driven development with red-green-refactor loop |
| [`ubiquitous-language`](./ubiquitous-language) | **Deprecated** — superseded by `/repo-context-scan` (build) and `/domain-grill` (stress-test) |
| [`wisdom-capture`](./wisdom-capture) | Capture a wisdom snippet into a personal corpus — categorize into a closed bucket, write `wisdoms/<YYYY>/<MM>/<ulid>.md` with frontmatter, commit |

### UX Design

| Skill | Description |
|-------|-------------|
| [`design-interview`](./design-interview) | Interactive design brief interview before generating screens |
| [`design-draft`](./design-draft) | Full UXD workflow from design interview to developer handoff |
| [`design-review`](./design-review) | Multi-agent design review from 5 perspectives |

### Leadership

| Skill | Description |
|-------|-------------|
| [`leadership-update`](./leadership-update) | Reformat raw notes into an outcome-first, three-sentence update with a clear ask |

### Agent Behavior

| Skill | Description |
|-------|-------------|
| [`compact-conversation`](./compact-conversation) | Compact the current conversation into a concise summary to reduce context window usage |
| [`concise-reporting`](./concise-reporting) | Ultra-concise status/progress reporting; full verbosity preserved for written artifacts |
| [`handoff`](./handoff) | Compact the current conversation into a discoverable handoff document at `.claude/handoffs/` so a fresh agent can pick it up with `/resume` |
| [`precision-mode`](./precision-mode) | Universal conciseness directive — makes every LLM response shorter, denser, and more precise |
| [`resume`](./resume) | Pick up where a previous session left off — loads the newest open handoff, runs an environment preflight, and marks the file resumed on confirm |
| [`session-feedback`](./session-feedback) | Mine the current conversation for every correction, preference, and do-differently lesson; write a dated feedback file the next session reloads as memory |
| [`skill-sync`](./skill-sync) | Sync an existing skill from a source path, or scaffold a new one via claude/codex/devin |

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
