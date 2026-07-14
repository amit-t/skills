# code-review — Reference

Detail behind `SKILL.md`: rubric dimensions, principles, exact gh commands, state format, dedupe, identity ack, config schema.

---

## Rubric

11 dimensions. Every finding is tagged with exactly one. Principle references are optional — add them when the finding maps directly to a named idea.

### 1. Correctness
Does the code do what the PR description says? Off-by-one, null/empty, concurrency, lost updates, race conditions, edge cases at boundaries (0, 1, MAX, exact equality on inequality checks), error paths that swallow errors.

### 2. Design / architecture
Right abstraction layer? Wrong coupling? Leaking abstractions across modules? Premature flexibility (interface for one impl)? Single-responsibility violations? Ousterhout: **information leakage**, **shallow modules**, **change amplification**. DDD: bounded-context leak, anemic domain model, aggregate root bypass.

### 3. Security
AuthN/AuthZ checks present where needed. Injection (SQL, command, header, log). Secrets in code or logs. Unsafe deserialization. SSRF / open redirect. Path traversal. CSRF where applicable. Crypto misuse (weak algos, IV reuse, no constant-time compare).

### 4. Reliability
Error handling complete (not just `if err != nil { return err }` everywhere). Timeouts on external calls. Retries with backoff + jitter where appropriate. Idempotency on write paths. Partial-failure handling. Graceful degradation. Resource cleanup (defer / using / finally).

### 5. Performance
N+1 queries. Hot-path allocations. Blocking I/O on event loop. Wrong complexity class (quadratic when linear suffices). Unbounded growth (lists, caches, goroutines). Synchronous what should be async.

### 6. Testing
New behavior has tests. Tests test behavior, not implementation. Mocks don't hide real bugs (watch for mock/prod divergence). Edge cases covered. No flaky patterns (sleep-based, network-dependent, time-of-day). Test names describe expected behavior, not the method called.

### 7. API / contract
Backward compat preserved (or breakage clearly documented). Semver respected. Deprecation present before removal. Wire-format compatibility (proto field numbers, JSON field names). Client SDK changes synchronized. Error codes documented and stable.

### 8. Observability
Logs at right level (no INFO floods, ERROR for actionable only). Structured logging where applicable. Metrics on new paths (counter for new errors, latency histogram for new ops). Trace span coverage. Failure modes are debuggable from log/trace alone.

### 9. Readability / maintainability
Names express intent. Functions do one thing (Ousterhout deep modules: simple interface, not necessarily small). Dead code removed. No premature abstraction (one caller ≠ helper). Comments explain *why*, not *what*. No lying comments. Pragmatic Programmer: **DRY** (knowledge, not lines) and **ETC** (easier to change).

### 10. Scope discipline
Drive-by changes flagged separately. Unrelated refactors mixed in flagged for split. Reformatting noise inflates diff. PR title/body matches actual scope. (Pre-check handles size + single-concern; this dimension catches in-scope cleanup that should still be a separate PR.)

### 11. Data migration safety
Forward + backward compat between code and schema. Migration is online (no long lock). Backfill strategy is safe under concurrent writes. Rollback path exists. Default values handle NULL legacy rows. Index creation is non-blocking (`CREATE INDEX CONCURRENTLY` etc).

---

## Principles (book-grounded)

Used in finding rationale and the review summary. Each principle has a short tag for cross-reference.

### The Pragmatic Programmer (Hunt & Thomas)
- **DRY** — every piece of knowledge has a single authoritative representation. Watch for duplicated knowledge across code/docs/data, not just duplicated lines.
- **Orthogonality** — independent components; change in one doesn't ripple. Coupled tests, hidden cross-deps, and god-objects break this.
- **Tracer bullets** — end-to-end skeleton before fleshing out. Big-bang PRs that wire everything at once fail orthogonality.
- **ETC (Easier To Change)** — name decisions whose change cost is high. Premature commitments to wire formats, table names, public APIs.
- **Reversibility** — prefer choices that can be undone. Flagged for irreversible deploys without rollback.

### Domain-Driven Design (Evans)
- **Ubiquitous language** — code names match domain language. Class/method/var names that drift from how the business talks are red flags.
- **Bounded context** — model boundaries are explicit. Cross-context calls without translation = leak.
- **Aggregates** — entities cluster with one root; external refs only to root. Direct access to inner entities breaks invariants.
- **Model-driven design** — structure of code mirrors domain. Generic "Manager" / "Helper" classes signal the model isn't speaking.

### A Philosophy of Software Design (Ousterhout)
- **Complexity** — anything that makes the system harder to understand or modify. Not a measure of LOC.
- **Deep modules** — simple interface, powerful implementation. Shallow modules (small interface, small impl) leak complexity to callers.
- **Information hiding** — encapsulate design decisions. Public state, exported globals, leaked config = breach.
- **Information leakage** — when a decision is spread across modules. Same constant duplicated, same enum re-defined.
- **Change amplification** — a small change requires edits in many places. Smell of bad encapsulation.
- **Cognitive load** — how much the reader has to know to follow the code.
- **Unknown unknowns** — code where it's unclear whether a change will work. Worst kind of complexity.
- **Make the common case simple** — interface optimized for typical caller.

---

## Pre-check thresholds (config-driven)

| Arm | Hard reject | Soft warn | Notes |
|---|---|---|---|
| Size LOC | `size.hard_reject_loc` (500) | `size.soft_warn_loc` (200) | counts additions + deletions in non-excluded files |
| Size files | `size.hard_reject_files` (20) | `size.soft_warn_files` (10) | non-excluded files only |
| Single concern | `scope.max_subsystems` (3) | — | distinct top-level dirs touched |
| Description | required: `[what, why, test_plan]` | — | missing 2+ → fail |

**Default exclusions** (in addition to `size.exclude_globs`): `*.lock`, `package-lock.json`, `yarn.lock`, `go.sum`, `Cargo.lock`, `**/__generated__/**`, `**/*.pb.go`, `**/*.gen.ts`, `vendor/**`, `node_modules/**`, snapshot files (`*.snap`), pure renames (detected via git).

---

## Comment layout (Phase 1 verb loop)

```
─────────────────────────────────────────────
[N/total]  <emoji> <SEVERITY>  ·  <dimension>
file: <path>:<line>

  <line-3> | <code>
  <line-2> | <code>
  <line-1> | <code>
  <line  > +<changed code>
  <line+1> | <code>

Finding:
  <1–3 sentences root cause>

Principle: <book> §<chapter> — <named idea>     (optional)

Suggested comment:
  > <verbatim text that will be posted>

Approve [a] · Skip [s] · Edit [e] · Expand [x] · Defer [d] · Quit [q] ›
```

Severity → emoji: `blocker` 🔴 · `major` 🟠 · `minor` 🟡 · `nit` ⚪. Honor `NO_COLOR=1` (drop ANSI + emoji, keep labels).

---

## Summary body (final grouped Review)

```markdown
## Review summary

**Verdict:** <Approve | Comment | Request changes> — N blockers, M major, K minor findings.

### What this PR does well
- <observation tied to dimension>
- <observation tied to a named principle>

### What needs to change before merge
- **<dimension> (<severity>):** <one-line>. See inline at <file>:<line>.
- ...

### Themes
- <cross-cutting observation that isn't anchored to one line>

### Principles invoked
- <book>: <named principles touched>

---
_Generated by code-review skill · 11-dimension rubric · PR head `<sha>`_
```

---

## gh commands

Read:
```bash
gh pr view <id> --json number,title,body,author,baseRefName,headRefName,headRefOid,additions,deletions,changedFiles,files,labels,url
gh pr diff <id>
gh api /repos/{owner}/{repo}/pulls/<num>/comments        # existing posted review comments
gh repo view --json owner,name                            # to resolve {owner}/{repo} for API calls
```

Worktree:
```bash
git fetch origin pull/<num>/head:code-review-pr-<num>
git worktree add <skill-dir>/state/worktree-pr-<num> code-review-pr-<num>
# tear down on submit/abort:
git worktree remove --force <skill-dir>/state/worktree-pr-<num>
git branch -D code-review-pr-<num>
```

Post grouped Review:
```bash
gh api -X POST /repos/{owner}/{repo}/pulls/<num>/reviews \
  -F event=COMMENT \
  -F body="<summary body>" \
  -F 'comments[][path]=<file>' \
  -F 'comments[][line]=<line>' \
  -F 'comments[][body]=<comment + hidden marker>' \
  ...
```

`event` is `COMMENT`, `REQUEST_CHANGES`, or `APPROVE` per verdict policy.

Description-quality bail (issue-level, no line anchor):
```bash
gh pr comment <num> --body "<bail comment + hidden marker>"
```

Every posted comment body ends with `\n\n<!-- code-review-skill:<sha256(file+line+text)[:12]> -->` for dedupe.

---

## State file

Path: `<skill-dir>/state/pr-<num>.json`. Format:

```json
{
  "pr": 42,
  "url": "https://github.com/org/repo/pull/42",
  "head_sha": "abc123def456",
  "started_at": "2026-05-12T10:30:00Z",
  "updated_at": "2026-05-12T10:42:11Z",
  "pre_check": { "description": "pass", "size": "pass", "scope": "pass" },
  "findings": [
    {
      "id": 1,
      "status": "approved",
      "severity": "blocker",
      "dimension": "security",
      "file": "auth/session.go",
      "line": 142,
      "comment": "Use `<=` here. RFC 7519 requires rejecting tokens at exact expiry.",
      "edited": false,
      "principle": "ousterhout-information-hiding",
      "marker_hash": "a1b2c3d4e5f6"
    },
    { "id": 2, "status": "skipped", "...": "..." },
    { "id": 3, "status": "deferred", "...": "..." }
  ]
}
```

`status` ∈ `pending | approved | skipped | deferred | submitted`. Writes happen on every verb (atomic via tmp-file + rename).

Archive on submit: `<skill-dir>/state/archive/pr-<num>-<ISO8601>.json`.

---

## Re-review dedupe

On re-invocation:
1. Compare current `head_sha` with state's `head_sha`.
2. If different: archive old state, fetch existing posted comments via `gh api /pulls/<num>/comments`, extract every `<!-- code-review-skill:<hash> -->` marker into a posted-set.
3. Generate fresh findings on new head. For each, compute `marker_hash`. Drop any whose hash is in the posted-set.
4. Run normal approval loop on the remaining novel findings.

This lets you re-review after every push without ever posting the same comment twice, even if the agent re-discovers the same issue.

---

## Identity ack

First-ever use per skill install:

```
⚠ code-review skill posts comments as your GitHub identity (<gh-user>).
  Engineers receiving the review cannot tell the comments are AI-assisted.
  You are responsible for what gets posted. Type "I understand" to continue.
```

Store ack at `<skill-dir>/state/.acknowledged` (touch-file, no content). Skip if `safety.identity_ack_required: false`.

---

## Config schema

See `config.example.yaml` for the annotated reference. Schema:

```yaml
size:
  hard_reject_loc: int    # default 500
  hard_reject_files: int  # default 20
  soft_warn_loc: int      # default 200
  soft_warn_files: int    # default 10
  exclude_globs: [string] # added to built-in exclusions

scope:
  enabled: bool           # default true
  max_subsystems: int     # default 3

description:
  enabled: bool           # default true
  required: [string]      # subset of [what, why, test_plan]

rubric:
  <dimension>: bool       # default true for all 11

verdict:
  policy: string          # one of: comment | request_changes_on_blocker | never_approve

principles:
  pragmatic_programmer: bool
  ddd: bool
  philosophy_of_software_design: bool

safety:
  identity_ack_required: bool   # default true
```

Project config: `<skill-dir>/config.yaml`. Ships with defaults filled in. User edits in place. `config.example.yaml` is reference-only with comments.

---

## Error handling

| Failure | Behavior |
|---|---|
| `gh` not installed | Print `brew install gh` (or platform equiv) and bail. |
| `gh auth status` fails | Print `gh auth login` and bail. |
| PR not found | Print URL tried and bail. |
| Worktree path exists | Reuse if same `head_sha`, else remove and re-create. |
| API rate limit | Surface remaining quota from gh response, bail without partial post. |
| `submit review` partial failure | Atomic POST: gh API takes the whole review in one call — failures are all-or-none. Retain state for retry. |
| User Ctrl-C in verb loop | State is already persisted on each verb; safe to re-enter via `/code-review <id>`. |
