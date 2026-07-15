# code-review-multi-axis

> Principal-engineer code review in two modes. **Pre-PR:** local Standards + Spec axes via parallel sub-agents (Fowler smell baseline + repo standards vs originating issue/PRD), side-by-side report, nothing posted. **Post-PR:** 11-dimension rubric grounded in Pragmatic Programmer / DDD / Philosophy of Software Design, pre-checks (description quality, size, single-concern scope), per-comment approval loop, posts one grouped GitHub Review. Never auto-APPROVEs. Re-review safe (dedupes via hidden markers). Slash-invoked only — the model never fires it on its own.

**Category:** Engineering

Formerly `code-review`; renamed and extended with the pre-PR two-axis mode adapted from [`two-axis-review`](../two-axis-review). Mode is picked by the argument: a git ref → pre-PR ([PRE-PR.md](PRE-PR.md)), a PR number/URL → post-PR.

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill code-review-multi-axis
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
cp -r code-review-multi-axis .cognition/skills/code-review-multi-axis
# or
cp -r code-review-multi-axis .windsurf/skills/code-review-multi-axis

# Global
cp -r code-review-multi-axis ~/.config/cognition/skills/code-review-multi-axis
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r code-review-multi-axis .claude/skills/code-review-multi-axis

# Global
cp -r code-review-multi-axis ~/.claude/skills/code-review-multi-axis
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r code-review-multi-axis .cursor/skills/code-review-multi-axis
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat code-review-multi-axis/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat code-review-multi-axis/SKILL.md >> GEMINI.md
```

</details>

## Usage

```
/code-review-multi-axis <ref>            # pre-PR: two-axis pass vs fixed point (main, SHA, HEAD~5); posts nothing
/code-review-multi-axis <pr-num|url>     # post-PR review (current branch's PR if no arg and one exists)
/code-review-multi-axis <id> --force     # bypass pre-check
/code-review-multi-axis status           # show approval state
/code-review-multi-axis abort            # discard state file
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

Defaults ship at `code-review-multi-axis/config.yaml`. Edit in place to tune size thresholds, single-concern strictness, required PR description fields, rubric dimensions, verdict policy, or principles citations. Annotated reference is in `code-review-multi-axis/config.example.yaml`. Full schema: [REFERENCE.md](REFERENCE.md#config-schema).

## Scope (v1)

GitHub only. GitLab / Bitbucket / Gerrit not supported.

## License

MIT
