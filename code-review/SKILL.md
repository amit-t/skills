---
name: code-review
description: Principal-engineer review of a GitHub PR via two-phase approval. Pre-checks PR description quality, size, and single-concern scope. Generates findings across an 11-dimension rubric grounded in Pragmatic Programmer, Domain-Driven Design, and A Philosophy of Software Design. Walks the user through every comment one at a time with approve / skip / edit / expand / defer / quit verbs. Only the approved subset is posted as one grouped GitHub Review. Never auto-APPROVEs. Use when user says `/code-review`, `code review this PR`, `review pull request`, or passes a PR number / URL.
user-invocable: true
---

# /code-review — Principal-Engineer PR Review

Two-phase workflow:
1. **Phase 1 (local):** generate findings → walk user through each → build approved pool.
2. **Phase 2 (remote):** on `submit review`, POST one grouped GitHub Review with the approved subset.

## Quick start

```
/code-review <pr-num|url>     → start review (current branch's PR if no arg)
/code-review <id> --force     → bypass pre-check
/code-review status           → show approval state for current PR
/code-review abort            → discard state file

a / s / e / x / d / q         → per-comment verbs (approve / skip / edit / expand / defer / quit)
show deferred / review deferred
submit review                 → POST grouped review
submit review --approve       → only if zero blocker/major in approved pool
submit review --lgtm          → clean APPROVE for empty-findings PR
```

## Preflight (fail-fast)

Verify, in order: `gh --version`, `gh auth status`, `gh repo view`, PR id resolves. Bail with install/auth hint on any failure.

## One-time identity ack

On first use per skill install, print the safety banner and require `I understand`. Persist to `state/.acknowledged`. See [REFERENCE.md](REFERENCE.md#identity-ack).

## Phase 1 — Pre-check (3 arms, all gated by `--force`)

For each violation, show the proposed bail comment via the verb loop. User can `approve` (post + stop), `edit`, `skip` (proceed to deep review), or say `review anyway` mid-prompt to override.

1. **Description quality.** Body must contain `what`, `why`, `test_plan` (configurable). Missing 2+ → bail with "Define what this PR does (what / why / test plan) before review."
2. **Size.** Hard reject above `size.hard_reject_loc` (default 500) **or** `size.hard_reject_files` (default 20), counting only source/tests/config (exclusions in config). Soft warn above the soft thresholds. Bail with "PR exceeds size threshold (N LOC / M files). Split into smaller, single-concern PRs."
3. **Single concern.** More than `scope.max_subsystems` (default 3) distinct top-level dirs touched without a cross-cutting note in title → bail with "PR spans N subsystems — split into one PR per concern, or restate the cross-cutting goal in the title."

If all pass (or `--force`), continue to deep review.

## Phase 1 — Deep review

Fetch the PR head into a worktree: `git worktree add <skill-dir>/state/worktree-pr-<num> <head_sha>`. Read every changed file in full + grep top-3 callers for each new/changed public symbol + read schema files if migrations touched. Skip files matching `size.exclude_globs`.

Generate findings across the 11-dimension rubric: correctness, design, security, reliability, performance, testing, api_contract, observability, readability, scope_discipline, data_migration. See [REFERENCE.md](REFERENCE.md#rubric) for what each dimension catches and the principles that ground each (Pragmatic Programmer / DDD / Ousterhout). Each finding has: severity (`blocker` / `major` / `minor` / `nit`), dimension, file, line, suggested comment text, optional principle reference.

Order findings by severity desc, then file. Persist state (see [REFERENCE.md](REFERENCE.md#state-file)).

## Phase 1 — Approval loop

For each non-deferred, non-decided finding, render the per-comment layout (header + ±4 line code window + finding + suggested comment + verb prompt). See [REFERENCE.md](REFERENCE.md#comment-layout) for the exact format.

Verbs: `a` approve (as-is) · `s` skip (drop) · `e <text>` edit (rewrite then approve) · `x` expand (more context, re-ask) · `d` defer (manual resurface) · `q` quit (keep approvals, exit loop). Deferred items only resurface on `review deferred`. `submit review` soft-warns if deferred is non-empty.

## Phase 2 — Submit

On `submit review` print confirmation (target URL, comment counts, verdict, posting identity). User types `confirm` / `preview` / `cancel`.

Verdict per `verdict.policy` (config): `comment` always COMMENT; `request_changes_on_blocker` REQUEST_CHANGES if any approved finding is blocker, else COMMENT; `never_approve` same but APPROVE always blocked. `--approve` only succeeds on zero approved blocker/major. `--lgtm` only succeeds when zero findings were generated.

POST one grouped Review via `gh api -X POST /repos/{owner}/{repo}/pulls/{num}/reviews` with `event` and `comments[]` (each with `path`, `line`, `body` + hidden marker `<!-- code-review-skill:<finding-hash> -->`). Description-quality bail uses `gh pr comment` (issue-level, no line anchor). Summary body format in [REFERENCE.md](REFERENCE.md#summary-body).

Archive state to `state/archive/pr-<num>-<timestamp>.json`. Remove worktree.

## Re-review (PR head moved)

On re-invocation when `head_sha` mismatches: archive stale state, fetch existing posted comments, generate fresh findings on new head, **dedupe** any whose `(file, line, marker-hash)` matches an already-posted comment. If stale state has approved-but-not-submitted findings, prompt `submit anyway` / `discard`.

## Config

Defaults ship at `<skill-dir>/config.yaml`. Reference + comments at `config.example.yaml`. Schema and every knob in [REFERENCE.md](REFERENCE.md#config-schema).

## Scope

GitHub only (v1). GitLab / Bitbucket / Gerrit out of scope.
