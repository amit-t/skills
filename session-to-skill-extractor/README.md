# session-to-skill-extractor

> Reviews completed agent sessions to find non-obvious, recurring, generalizable procedures and turns them into reusable `SKILL.md` skills — with a rubric, deduplication, a human review queue, and a usage-feedback loop.

**Category:** AI Agent

## What It Does

Implements the article's five-stage extraction pipeline as an Agent Skill: **filter → identify → articulate → dedup → review queue**, plus a **registry** and a **feedback loop** that closes the "does this skill actually help" question over time.

- **Host adapters** normalize sessions from Claude Code, Codex, Devin, Copilot, or a generic paste/file source into one common `Session` shape, so the rest of the pipeline is host-independent.
- **Deterministic scripts** do the parts that don't need judgment: gating/ranking sessions (Stage 1), hard-rule validation of a drafted candidate (Stage 3), a cheap token-overlap dedup pre-screen (Stage 4), rendering the review-queue files, and promoting/rejecting.
- **The host LLM** does the parts that need judgment: scoring the five identification questions (Stage 2), articulating the six-field skill definition (Stage 3), and classifying dedup shortlist pairs as duplicate/overlap/superset/subset/distinct (Stage 4).
- **A registry** (`registry.json`) tracks every promoted skill's status, version, evidence, and suppression list; a **review queue** (`review-queue/`) holds candidates awaiting a human `accept | edit | reject`.
- **Feedback** (`feedback/usage-log.jsonl` + `retire_review.py`) tracks whether promoted skills actually help, and proposes promote/revise/retire on a quarterly cadence.

```
detect host
    │
    ▼
locate + filter sessions ──► ranked, admitted sessions
    │
    ▼
identify (5 questions, rubric)  ──► flagged sessions
    │
    ▼
cluster by task_type + gate on recurrence
    │
    ▼
articulate CandidateSkill JSON ──► validate ──► revise once on failure
    │
    ▼
dedup pre-screen + LLM classify ──► duplicate | overlap | superset/subset | distinct
    │
    ▼
render → review-queue/<id>/{candidate.json, SKILL.md, REVIEW.md}
    │
    ▼
promote (human instruction only) ──► skill dir + registry.json
    │
    ▼
feedback loop ──► report-usage / retire-review (separate, ongoing)
```

### When to Use

- You want to mine finished agent sessions (yours or a team's) for procedures worth turning into a reusable skill.
- You run the same kind of task repeatedly and suspect an undocumented approach has emerged.
- You maintain a skill library and want a quarterly prune/promote pass driven by actual usage outcomes, not guesswork.

### When NOT to Use

- You just want a transcript summary — use `session-handoff` instead; this skill only cares about extractable procedures, not narrative recap.
- You have fewer than 3 sessions of a given task type and no single session with a strong, non-obvious, well-executed result — there isn't enough evidence yet (see the recurrence ladder below).
- You want a skill installed immediately without review — auto-promotion is off by default on purpose; this is a filter, not an installer.

## Usage

```
/session-to-skill-extractor
```

Or invoke the scripts directly (all are stdlib-only Python 3.9+, no installs required):

| Script | Purpose | Example |
|---|---|---|
| `detect_host.py` | Detect the host agent runtime | `python3 scripts/detect_host.py --override codex` |
| `load_sessions.py` | Locate + normalize sessions via a host adapter. `--paths <glob>...` is explicit files: it skips store discovery entirely (all hosts), loading each glob match directly instead of scanning the adapter's session store | `python3 scripts/load_sessions.py --host claude-code --out sessions.json --max 25` |
| `filter_sessions.py` | Stage 1: gate + rank sessions, no LLM call | `python3 scripts/filter_sessions.py --in sessions.json --out filtered_sessions.json` |
| `validate_candidate.py` | Stage 3 hard rules: schema, vagueness lint, rubric arithmetic | `python3 scripts/validate_candidate.py --candidate candidate.json` |
| `dedup_prescreen.py` | Stage 4 pass 1: Jaccard token-overlap shortlist | `python3 scripts/dedup_prescreen.py --candidate candidate.json --skill-dirs "./skills,.claude/skills"` |
| `render_skill.py` | Render a candidate into `review-queue/<id>/` | `python3 scripts/render_skill.py --candidate candidate.json --out-dir ./review-queue` |
| `promote.py` | Accept/edit/reject a queued candidate; updates registry | `python3 scripts/promote.py cs-20260917-foo accept --queue ./review-queue --skill-dir ./skills --registry ./registry.json` |
| `report_usage.py` | Append a usage-outcome row for a promoted skill | `python3 scripts/report_usage.py foo-skill --outcome good --note "saved a rewrite"` |
| `retire_review.py` | Quarterly promote/revise/retire proposals + conflict scan (read-only) | `python3 scripts/retire_review.py --registry ./registry.json --feedback-dir ./feedback --out ./review-queue` |

## Configuration

Copy `config.example.json` to `config.json` and pass `--config config.json` to any script (each script deep-merges your file over the bundled defaults).

| Key | Default | Meaning |
|---|---|---|
| `host_override` | `null` | Force a host instead of auto-detecting |
| `skill_dirs` | `[".claude/skills", ".agents/skills", ".github/skills", "./skills"]` | Directories `dedup_prescreen.py` scans for existing `SKILL.md` files. Read automatically: this is the default when `--skill-dirs` is omitted; passing `--skill-dirs` explicitly still overrides it |
| `output_skill_dir` | `"./skills"` | Suggested destination for `promote.py --skill-dir`; **not read automatically** — every `promote.py` call must still pass `--skill-dir` explicitly (see Owner decisions defaulted, below) |
| `review_queue_dir` | `"./review-queue"` | Suggested review-queue location; `render_skill.py --out-dir` and `promote.py --queue` are always explicit args, not sourced from this key. `retire_review.py --out` also defaults to a hardcoded `./review-queue` of its own — the value matches this key by convention only, it is not read from config either |
| `feedback_dir` | `"./feedback"` | Where `report_usage.py` appends `usage-log.jsonl` when `--feedback-dir` is omitted (this one *is* read from config as a fallback) |
| `work_dir` *(DES)* | `"./.session-to-skill"` | Suggested scratch location for intermediate run artifacts (`sessions.json`, `filtered_sessions.json`, draft candidates) — a convention for the SKILL.md workflow, not consumed by any script |
| `registry_path` *(DES)* | `null` | Suggested path for `registry.json`; `promote.py --registry` and `retire_review.py --registry` are always required explicit args |
| `filter.min_turns` | `6` | Minimum combined user+assistant turns to pass Stage 1 |
| `filter.min_tool_calls` | `2` | Minimum tool calls (or see next key) to pass Stage 1 |
| `filter.min_assistant_turns_if_no_tools` | `4` | Alternate gate when the host has no tool-call data |
| `filter.max_sessions_per_run` | `25` | Cap on admitted sessions per run (keeps the LLM stage tractable) |
| `filter.lookback_days` | `1` | Default lookback window for adapters that support it |
| `identify.flag_min_questions_at_2` | `3` | Flag rule: at least this many of the 5 rubric questions must score 2 |
| `identify.flag_min_total` | `7` | Flag rule: rubric total must be at least this (out of 10) |
| `identify.q2_min` | `1` | Flag rule: Q2 (non-obviousness) must be at least this — Q2=0 never flags |
| `recurrence.candidate_min_sessions` | `3` | Sessions needed for `candidate` status |
| `recurrence.provisional_min_sessions` | `20` | Sessions needed for `provisional` status |
| `recurrence.validated_min_sessions` | `30` | Sessions needed for `validated` status |
| `recurrence.allow_single_session_if_q2_q3_max` | `true` | Enables the single-session exception (Q2=2 and Q3=2, always `requires_human_review`) |
| `dedup.prescreen_overlap_threshold` | `0.3` | Jaccard threshold for the dedup shortlist |
| `review.auto_promote` | `false` | Must be explicitly enabled; even then only `validated`-tier candidates with no dedup findings ever auto-promote |
| `review.reject_suppress_days` | `30` | How long a rejected `task_type` is suppressed from re-proposal |
| `feedback.review_window_days` | `90` | Trailing window `retire_review.py` uses for usage-outcome stats (the article's "quarterly review") |
| `feedback.validated_min_good_reports` | `5` | `good` reports (with zero `poor`) needed to propose promotion to `validated` |
| `library_size_warning` | `20` | Above this many registered skills, `retire_review.py`'s report warns the library favors dynamic (description-based) loading over always-loaded skills |

## Status ladder

| Status | Evidence | Behavior |
|---|---|---|
| `candidate` | 1–19 supporting sessions | Lives in `review-queue/` only. Single-session candidates always require human review. |
| `provisional` | 20–29 sessions, or any reviewer `accept`/`edit` below that | Installed; `metadata.status: provisional`. |
| `validated` | 30+ sessions, or ≥5 `good` usage reports with zero `poor` | Installed; eligible for auto-promotion of future version bumps. |
| `deprecated` | Superseded by a newer version, or a `retire-review` outcome | Folder kept with `metadata.status: deprecated` and `superseded_by`; not loaded. |

## Owner decisions defaulted

These were left to the build's judgment per the handoff spec (E4) rather than specified up front:

- **Output location for extracted skills.** Default intent is `./skills/extracted/` when the extractor runs inside this same skill project, to avoid colliding with the top-level skill catalog. The shipped `config.example.json` currently sets `output_skill_dir` to `"./skills"` and no script reads that key automatically — always pass `--skill-dir` explicitly to `promote.py` (e.g. `--skill-dir ./skills/extracted`) until the config wiring catches up.
- **Devin integration.** Paste-first: the primary path is a pasted/exported session-detail JSON. The Devin API (`DEVIN_API_KEY`) is optional and only used as a fallback when a key is present.
- **Reviewer model.** `REVIEW.md` is designed to be self-contained for a single reviewer (rubric, evidence, dedup findings, and a recommended action all in one file), though nothing prevents a second person from reading it.

## Install as Agent Skill

```bash
npx skills@latest add amit-t/skills --skill session-to-skill-extractor
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r session-to-skill-extractor .cognition/skills/session-to-skill-extractor
# or
cp -r session-to-skill-extractor .windsurf/skills/session-to-skill-extractor

# Global
cp -r session-to-skill-extractor ~/.config/cognition/skills/session-to-skill-extractor
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r session-to-skill-extractor .claude/skills/session-to-skill-extractor

# Global
cp -r session-to-skill-extractor ~/.claude/skills/session-to-skill-extractor
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r session-to-skill-extractor .cursor/skills/session-to-skill-extractor
```

</details>

<details>
<summary>Codex</summary>

```bash
# Project-level (Agent Skills standard dir; Codex discovers SKILL.md here)
cp -r session-to-skill-extractor .agents/skills/session-to-skill-extractor

# Global
cp -r session-to-skill-extractor ~/.agents/skills/session-to-skill-extractor
```

`~/.codex/skills` is the legacy location — prefer `.agents/skills` (see `references/host-notes.md`). Model-invoked, or mention explicitly with `$session-to-skill-extractor`.

</details>

<details>
<summary>GitHub Copilot</summary>

```bash
# Project-level
cp -r session-to-skill-extractor .github/skills/session-to-skill-extractor

# Global
cp -r session-to-skill-extractor ~/.copilot/skills/session-to-skill-extractor
```

`.claude/skills/` and `.agents/skills/` also work at the project level, and `~/.agents/skills/` works at the user level (see `references/host-notes.md`).

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat session-to-skill-extractor/SKILL.md >> GEMINI.md
```

</details>

## Scheduled use

- **Claude Code** — native scheduled task or a cloud Routine running the pipeline with `--host claude-code`.
- **Codex CLI** — a Codex app Automation running the pipeline with `--host codex`.
- **Devin** — a Scheduled Session / Automation; falls back to asking for a pasted transcript if `DEVIN_API_KEY` isn't configured for that run.
- **GitHub Copilot** — a Copilot CLI scheduled prompt or cloud-agent Automation with `--host copilot`; falls back to a pasted transcript when local session stores are metadata-only.

## Related Skills

- [`write-a-skill`](../write-a-skill) — the authoring guide this extractor's own `SKILL.md` and every rendered skill follow (progressive disclosure, description quality, review checklist).
- [`session-handoff`](../session-handoff) — compacts a single conversation into a discoverable handoff doc for a fresh agent; complementary but distinct from this skill's cross-session pattern mining.
- [`wisdom-capture`](../wisdom-capture) — captures point-in-time insights and lessons; this skill instead looks for recurring, generalizable *procedures* across multiple sessions before promoting anything.

## License

MIT
