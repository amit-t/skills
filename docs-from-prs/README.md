# docs-from-prs

> Survey recent merged PRs, find what is undocumented, and update README and other user-facing docs with thoughtful section placement. Always re-checks the project's drift hot spots (alias tables, CLI flag references, config examples). Includes a grammar/casing/alignment copy-edit pass.

**Category:** Engineering

## What It Does

Closes the drift between merged code and the docs that describe it. The skill:

1. Surveys recent merged PRs (via `gh pr list`, repo resolved with `gh repo view`) and recent commits.
2. Classifies each PR as user-facing (flag / config / behaviour) or internal chore.
3. Cross-checks against current docs and **only edits what is actually missing or stale**.
4. Re-audits the project's drift hot spots every run — alias tables, CLI flag matrices, env-var lists, supported-version tables. Drift accumulates from minor commits even when no PR explicitly touches them.
5. Places each gap into the right doc section using a layout-aware placement matrix (single-file / README + landing page / README + user guide / full). CLI flag → Options reference, alias → alias table, fix → Recent Changes, etc.
6. Runs a copy-edit pass: grammar, sentence-case headings, table-pipe alignment, code-fence language tags, HTML tag balance, JS-driven changelog key shifting.
7. Reports filled gaps, skipped PRs (with reason), drift-hot-spot changes, and any source/doc factual mismatches.

Project-agnostic. Reads the project's `CLAUDE.md` / `AGENTS.md` for `gh` account names, "never edit" directories, drift hot spots, and PR workflow (single-remote vs multi-remote mirror).

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
- `both remotes` / `all remotes` — for projects mirrored to multiple GitHub orgs, open PRs against each (follows the project's `CLAUDE.md` / `AGENTS.md` workflow)

## When to Use

- After a sprint of merges, before a release.
- When the landing-page changelog is visibly behind `git log`.
- When you've shipped a new flag or alias and the README still shows the old surface.
- As a periodic cron (weekly) to keep docs from drifting more than a handful of PRs.

## License

MIT
