# docs-from-prs

> Survey recent merged PRs, find what is undocumented, and update README + landing page + user guide with thoughtful section placement. Always re-checks alias tables. Includes a grammar/casing/alignment copy-edit pass.

**Category:** Engineering

## What It Does

Closes the drift between merged code and the docs that describe it. The skill:

1. Surveys recent merged PRs (via `gh pr list`) and recent commits.
2. Classifies each PR as user-facing (flag / config / behaviour) or internal chore.
3. Cross-checks against current docs and **only edits what is actually missing or stale**.
4. Re-audits the project's alias tables every run — drift accumulates from minor commits even when no PR explicitly touches aliases.
5. Places each gap into the right doc section using a placement matrix (CLI flag → Options reference, alias → alias table, fix → Recent Changes, etc.).
6. Runs a copy-edit pass: grammar, sentence-case headings, table-pipe alignment, code-fence language tags, HTML tag balance.
7. Reports filled gaps, skipped PRs (with reason), aliases changed, and any source/doc factual mismatches.

The reference implementation in this catalog assumes a multi-doc layout (`README.md`, `docs/index.html` landing page with a JS `CHANGE_DETAILS` map, `docs/user-guide/*.md`) and a dual-remote PR workflow. Adapt the file paths and PR rules to your project before using.

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill docs-from-prs
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r docs-from-prs .cognition/skills/docs-from-prs
# or
cp -r docs-from-prs .windsurf/skills/docs-from-prs

# Global
cp -r docs-from-prs ~/.config/cognition/skills/docs-from-prs
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r docs-from-prs .claude/skills/docs-from-prs

# Global
cp -r docs-from-prs ~/.claude/skills/docs-from-prs
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r docs-from-prs .cursor/skills/docs-from-prs
```

</details>

<details>
<summary>Codex</summary>

```bash
cat docs-from-prs/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat docs-from-prs/SKILL.md >> GEMINI.md
```

</details>

## Usage

```text
/docs-from-prs
```

Optional inline args (free-form):

- `since 2026-04-01` — survey PRs merged after a date
- `since #24` — survey PRs after a number
- `last 15` — last N merged PRs
- `dry-run` — gap report only, no edits
- `both remotes` — open PRs against both configured remotes (project-specific)

## When to Use

- After a sprint of merges, before a release.
- When the landing-page changelog is visibly behind `git log`.
- When you've shipped a new flag or alias and the README still shows the old surface.
- As a periodic cron (weekly) to keep docs from drifting more than a handful of PRs.

## License

MIT
