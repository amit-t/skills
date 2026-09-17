---
name: session-to-skill-extractor
description: Reviews completed agent sessions to find non-obvious, recurring, generalizable procedures and articulates them as reusable SKILL.md skills with trigger, prerequisites, steps, decision points, expected output, and edge cases; deduplicates against the existing library and routes candidates to human review. Use when asked to "extract skills from sessions", "mine my transcripts", "what procedures did we discover", "turn this session into a skill", or on a scheduled nightly/weekly skill-harvest run. Works in Claude Code, Codex, Devin, Copilot, or any agent (auto-detects host).
---

# Session-to-Skill Extractor

## What this is / is not

This is a filter, not a replacement for human judgment: it reviews completed agent sessions and answers exactly one question per session — *did this session contain a non-obvious, generalizable procedure that should be captured for future use?* It is **not** a transcript summarizer and **not** a logging tool; sessions that were merely long, or merely successful, are not automatically candidates. "Non-obvious" is load-bearing: it is not looking for things the agent already knows how to do, only for approaches that emerged through the session itself and are not codified anywhere. It surfaces candidates; a human (via `promote.py`) decides what actually enters the skill library. Keep its job narrow: filter → identify → articulate → dedup → queue. It never installs, deploys, auto-promotes, or edits another skill's body outside of a reviewed version bump.

## Step 0 — Detect host

Run `python3 scripts/detect_host.py`. It prints JSON, e.g. `{"host": "claude-code", "confidence": "high", "signals": ["env:CLAUDECODE=1"], "session_sources": [...]}`. Honor an explicit override with `python3 scripts/detect_host.py --override claude-code|codex|devin|copilot|generic`. State the detected host and confidence to the user before proceeding. `session_sources` lists every session store actually found on the machine independent of the cascade result, so a run under one host can still mine another host's local logs if asked. If `host` is `generic` (or confidence is `low` and no session source looks right), ask the user for a session file path, a glob pattern, or a pasted transcript — never refuse to run.

## Step 1 — Locate and filter sessions

Load sessions for the detected host:

```
python3 scripts/load_sessions.py --host <host> --out <work_dir>/sessions.json \
  [--paths "<glob>" ...] [--lookback-days N] [--max N] [--config config.json]
```

`<work_dir>` defaults to `./.session-to-skill` (see `config.example.json`). `--host` must be one of the adapters actually available (`claude-code`, `codex`, `copilot`, `devin`, `generic` — an unknown host exits 2 with the real list in the JSON error). Per-session load failures are collected into the output's `errors` array rather than aborting the run. `--paths` means explicit files: it skips store discovery entirely (all hosts) — each glob match is passed straight to the adapter's loader instead of the adapter scanning its own session store, so it works the same way for `claude-code`/`codex`/`copilot`/`devin` as it does for `generic`.

Then filter deterministically (no LLM call):

```
python3 scripts/filter_sessions.py --in <work_dir>/sessions.json --out <work_dir>/filtered_sessions.json [--config config.json]
```

This gates on `min_turns` / `min_tool_calls` (or `min_assistant_turns_if_no_tools`), excludes Q&A-only and single-tool-repetition sessions, ranks survivors by `priority_score` (length + complexity + outcome + novelty), and truncates to `max_sessions_per_run` (default 25). Show the user the ranked list, the counts admitted vs. dropped, and why (`admitted_by` / drop `reason` fields).

## Step 2 — Identify

Read `references/rubric.md` first — it has the five article questions verbatim, the 0–2 scoring anchors, and the flag rule. For each filtered session (one at a time, or in small batches if context allows), score all five questions 0–2 using the anchors, then apply the flag rule from the rubric: flag only if at least 3 of 5 questions score 2, total ≥ 7/10, **and** Q2 ≥ 1 (a session with Q2 = 0 never flags — the agent already knew this). For every flagged session, assign a short `task_type` label (noun phrase, e.g. `migrate-jest-to-vitest`) and a one-paragraph `procedure_sketch`.

## Step 3 — Cluster and gate

Group flagged sessions by `task_type` (exact match first, then judge semantic matches yourself). Before articulating a cluster, read `registry.json`'s `suppressed_task_types`: skip any cluster whose `task_type` has an entry with `until` in the future, unless the cluster's supporting evidence has at least doubled since the rejection (spec C5 Stage 5) — note the skip to the user rather than silently dropping it. Count `supporting_sessions` per cluster and apply the recurrence ladder from `config.example.json` (`recurrence.candidate_min_sessions: 3`, `provisional_min_sessions: 20`, `validated_min_sessions: 30` — see the Status ladder table in `README.md` for what each tier means downstream). A cluster with exactly 1 supporting session may still proceed to articulation **only if** Q2 = 2 **and** Q3 = 2 for that session, and it must always be marked `requires_human_review: true` — no other single-session cluster proceeds. Clusters below `candidate_min_sessions` (and not covered by the single-session exception) are not articulated yet; note them to the user as "seen once, watching for recurrence" rather than discarding them.

## Step 4 — Articulate

For each gated cluster, fill a `CandidateSkill` JSON per `schemas/candidate.schema.json` (D2): `candidate_id`, `name`, `description`, `task_type`, `trigger` (description + signals), `prerequisites`, `steps` (≥3, each an imperative sentence, no vague phrasing), `decision_points` (or `linear: true` if none), `expected_output` (checkable), `edge_cases` (≥1, or an explicit "none observed in N sessions"), `rubric`, `evidence`, `provenance`, `status`, `requires_human_review`, `version`. Then validate:

```
python3 scripts/validate_candidate.py --candidate <work_dir>/candidates/<candidate_id>.json [--registry <registry_path>] [--config config.json]
```

Pass `--registry` so a candidate whose `task_type` is still suppressed (see Step 3) fails validation deterministically instead of relying on the cluster-gate check alone. On failure (`{"ok": false, "errors": [...]}`), revise the candidate once using the returned error messages, then re-run. Before finalizing, self-check the article's own test: **could another agent follow this without interpretation?** If the honest answer is no, tighten the steps and re-validate — a description like "search the web and then summarize" is not a skill; "run `X`, extract field `Y`, then write `Z`" is.

## Step 5 — Dedup and conflict

Cheap pre-screen first (no LLM call):

```
python3 scripts/dedup_prescreen.py --candidate <work_dir>/candidates/<candidate_id>.json \
  --skill-dirs ".claude/skills,.agents/skills,.github/skills,./skills" \
  [--registry <registry_path>] [--threshold 0.3] [--config config.json]
```

This returns a `shortlist` of existing skills whose name/description/trigger tokens overlap the candidate above the Jaccard threshold (default 0.3). For every shortlisted pair, classify the relation yourself as `duplicate` (same trigger, same steps), `overlap` (same trigger, different steps — a real conflict), `superset`/`subset`, or `distinct`. Apply the resolution table:

- `duplicate` → do not create a new folder; note that the new session IDs should be appended to the existing skill's evidence in the registry, and propose a version bump only if the new articulation is measurably better (more decision points/edge cases, clearer steps).
- `overlap` (conflict) or `superset`/`subset` → never auto-write; route to review with both definitions side by side and a recommended merge.
- `distinct` → proceed to Step 6.

Record every finding under the candidate's `dedup.findings`.

## Step 6 — Queue for review

Render the candidate into the review queue:

```
python3 scripts/render_skill.py --candidate <work_dir>/candidates/<candidate_id>.json \
  --out-dir ./review-queue [--dedup-findings <work_dir>/dedup/<candidate_id>.json] [--config config.json]
```

This writes `review-queue/<candidate_id>/{candidate.json,SKILL.md,REVIEW.md}` and prints `{"ok": true, "dir": ...}`. `REVIEW.md` already carries the rubric table, quality-criteria checklist, evidence excerpts, dedup findings, and a `recommended_action` (`accept` only when no blocking dedup relation exists and the rubric total meets the flag threshold; otherwise `review dedup findings`). After rendering every candidate for the run, print your own summary table with columns: candidate, task type, evidence count, status, dedup finding, recommended action.

## Step 7 — Promote (on human instruction only)

Never call `promote.py` unless the human explicitly tells you to accept, edit, or reject a specific candidate — or `review.auto_promote` is `true` in config **and** the candidate is `validated`-tier with zero dedup findings (see Guardrails).

```
python3 scripts/promote.py <candidate_id> accept|edit|reject \
  --queue ./review-queue --skill-dir <output_skill_dir> --registry <registry_path> \
  [--reason "..."] [--config config.json]
```

`accept`/`edit` copy the rendered `SKILL.md` (status patched to the C6 ladder) and `.candidate.json` into `<skill-dir>/<name>/`, upsert `registry.json`, and move the queue folder to `review-queue/promoted/<candidate_id>`. `edit` additionally records `human_edited: true`. `reject` moves the folder to `review-queue/rejected/<candidate_id>`, writes `reason.txt`, and suppresses the `task_type` for `review.reject_suppress_days` (default 30).

## Feedback commands

After a promoted skill is used, log the outcome (best-effort — never blocks the skill that used it):

```
python3 scripts/report_usage.py <skill-name> --outcome good|neutral|poor [--note "..."] [--feedback-dir ./feedback] [--config config.json]
```

Run the quarterly review (default 90-day window) to get promote/revise/retire proposals plus a full-library trigger-conflict scan — read-only, it never mutates the registry or deletes anything:

```
python3 scripts/retire_review.py --registry <registry_path> --feedback-dir ./feedback \
  [--window-days 90] [--out ./review-queue] [--config config.json]
```

It writes `review-queue/retirement-<date>.md` and prints a JSON summary of proposals and conflicts. Treat this as an ongoing process, not a one-time cleanup.

## Guardrails

These are the article's five common mistakes, restated as do-not rules. Guard against all five on every run:

1. **Do not extract too broadly.** Apply every item in `references/quality-criteria.md` before articulating anything — a candidate that fails recurrence, non-obviousness, replicability, measurable quality, or clarity of articulation should not reach Step 4. Capturing everything potentially useful yields a cluttered library that confuses agents rather than helping them.
2. **Do not skip deduplication.** Always run Step 5 before Step 6, even for a candidate that looks obviously novel. Skipping it produces near-duplicate skills, and an agent presented with two ambiguous choices for the same trigger defaults to general behavior — defeating the entire point of extraction.
3. **Do not write vague skill definitions.** The validator rejects the phrases in `references/anti-patterns.md`'s blacklist ("be thorough", "as appropriate", "use best judgment", "handle accordingly", etc.) — do not work around this by rephrasing a vague instruction to dodge the exact string match; a skill describes specific actions, in sequence, with conditions, not general encouragement.
4. **Do not skip closing the feedback loop.** Every rendered skill ends with a `report_usage.py` instruction; do not omit it, and do run `retire_review.py` on the stated cadence rather than only when someone remembers to ask. Extraction without measurement is guesswork.
5. **Do not treat extraction as a one-time project.** Re-run Step 1 on new sessions on the configured schedule (see Scheduled use, below), not just once. Agent behavior improves incrementally as evidence accumulates, not in a single batch.

Scope and safety rules beyond the five pitfalls: never auto-promote unless `review.auto_promote` is `true` **and** the candidate is `validated`-tier with no dedup findings — the default is always human review, and this extractor never widens that default on its own. Never modify an existing skill's step body except through a version bump proposed in Step 5 and applied via `promote.py` — this extractor's scope is filter → identify → articulate → dedup → queue, not skill maintenance in general. Never copy more transcript content into a candidate JSON, a rendered `SKILL.md`, or a test fixture than the minimal excerpt needed as evidence — sessions may contain private material, and `evidence.sessions[].excerpt` should be a short quote, not a transcript dump.

## Scheduled use

Run this as a recurring job (the article's "scheduled batch at the end of each day") so recurrence evidence accumulates without a human remembering to trigger it. In every case, pass `--host <host>` explicitly to `detect_host.py`/`load_sessions.py` rather than relying on auto-detection, since a scheduled job's environment may not carry the same signals as an interactive session; see `references/host-notes.md` for per-host detection caveats.

- **Claude Code** — use a native scheduled task or a cloud-hosted Routine to run `/session-to-skill-extractor` (or the raw script pipeline) on a cron-like cadence, e.g. nightly with `--host claude-code --lookback-days 1`. This is the most direct mapping to the article's daily-batch recommendation since both the extractor and its session source live on the same machine.
- **Codex CLI** — configure a Codex app Automation to run the pipeline on a schedule, passing `--host codex` so the run reads `~/.codex/sessions/` directly instead of guessing from environment variables (which are only reliably set for sandboxed children, per `references/host-notes.md`).
- **Devin** — use a Scheduled Session / Automation. Because Devin has no local transcript store, the scheduled run should either supply `DEVIN_API_KEY` in the environment (the adapter then pulls sessions from the Devin API automatically) or, when no key is configured, fall back to a paste flow: have the automation post the exported session text somewhere a human (or a follow-up step) can hand it to `load_sessions.py --host devin --paths <pasted-file>` — `--paths` skips store discovery entirely and loads that file directly, which is exactly what a paste-first host needs.
- **GitHub Copilot** — use Copilot CLI scheduled prompts, or a cloud-agent Automation, with `--host copilot`. Local Copilot session stores were found to be metadata-only on the machine this skill was verified on (no message bodies in the SQLite tables — see `references/host-notes.md`), so a cloud-run Copilot automation should plan on the same paste fallback as Devin whenever the local/cloud session store doesn't expose full message text.
