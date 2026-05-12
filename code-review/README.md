# code-review

> Principal-engineer review of any GitHub PR with two-phase approval before posting. 11-dimension rubric grounded in Pragmatic Programmer / DDD / Philosophy of Software Design. Pre-checks PR description quality, size, single-concern scope. Per-comment approval loop. Never auto-APPROVEs. Re-review safe (dedupes via hidden markers).

**Category:** Engineering

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill code-review
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
cp -r code-review .cognition/skills/code-review
# or
cp -r code-review .windsurf/skills/code-review

# Global
cp -r code-review ~/.config/cognition/skills/code-review
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r code-review .claude/skills/code-review

# Global
cp -r code-review ~/.claude/skills/code-review
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r code-review .cursor/skills/code-review
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat code-review/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat code-review/SKILL.md >> GEMINI.md
```

</details>

## Usage

```
/code-review <pr-num|url>     # start review (current branch's PR if no arg)
/code-review <id> --force     # bypass pre-check
/code-review status           # show approval state
/code-review abort            # discard state file
```

In the per-comment approval loop:

```
a   approve as-is
s   skip (drop)
e <text>   edit comment text then approve
x   expand (more context, re-ask)
d   defer (manual resurface)
q   quit (keep approvals, exit loop)
```

Submit:

```
submit review              # POST grouped review with current verdict policy
submit review --approve    # only if zero approved blocker/major
submit review --lgtm       # clean APPROVE on a zero-findings PR
```

## Requirements

- `gh` CLI installed and authenticated (`gh auth status`)
- Working directory is a GitHub repo (`gh repo view` succeeds)
- For full-file context: ability to add a git worktree

## Configuration

Defaults ship at `code-review/config.yaml`. Edit in place to tune size thresholds, single-concern strictness, required PR description fields, rubric dimensions, verdict policy, or principles citations. Annotated reference is in `code-review/config.example.yaml`. Full schema: [REFERENCE.md](REFERENCE.md#config-schema).

## Scope (v1)

GitHub only. GitLab / Bitbucket / Gerrit not supported.

## License

MIT
