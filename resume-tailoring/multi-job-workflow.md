# Multi-Job Workflow

Batch mode for 3–5 similar roles. Consolidates discovery while preserving per-job research depth.

**Architecture:** Shared library + shared discovery + per-job research/matching/generation.

## When It Triggers

Any of:
- User pastes multiple JDs or URLs.
- Phrases: "multiple jobs", "these roles", "batch", "3 jobs", "5 positions".
- Explicit flag `--batch`.

Offer the user a choice:
```
I see {N} job descriptions. Multi-job mode:
  - Shared discovery (ask once, apply to all)
  - Aggregate gap analysis across jobs
  - Per-job research/template/matching kept separate

Benefits: 10–30% faster than sequential; same quality.
Use multi-job mode? (Y/N)
```

If N, process sequentially using the single-job workflow.

## Phase 0 — Intake & Batch Init

For each job, collect:
- JD text or URL.
- Company (extract from JD if possible, else ask).
- Role title (ditto).
- Priority — high / medium / low (default medium).
- Notes — optional (referral, deadline, etc.).

Assign `job_id = job-1, job-2, …`, status `pending`.

Quick-parse each JD (no full research yet): must-have reqs, technical keywords, soft skills, domain areas. Just enough to identify gaps in Phase 1.

Create batch directory:
```
resumes/batches/batch-{YYYY-MM-DD}-{slug}/
├── _batch_state.json
├── _aggregate_gaps.md
├── _discovered_experiences.md
└── {job_id}_{Company}_{Role}/   # per-job outputs, created later
```

`_batch_state.json`:
```json
{
  "batch_id": "batch-2026-04-16-pm-search",
  "created": "2026-04-16T10:30:00Z",
  "current_phase": "intake",
  "processing_mode": "interactive",
  "jobs": [
    {
      "job_id": "job-1",
      "company": "Microsoft",
      "role": "Principal PM — 1ES",
      "jd_text": "...",
      "jd_url": "https://...",
      "priority": "high",
      "notes": "Internal referral",
      "status": "pending",
      "requirements": ["Kubernetes", "CI/CD", "Cross-functional leadership"],
      "gaps": []
    }
  ],
  "discoveries": [],
  "aggregate_gaps": {}
}
```

Run standard Phase 0 library init **once** for the whole batch.

**Checkpoint:** Confirm batch is complete before Phase 1.

## Phase 1 — Aggregate Gap Analysis

1. For every requirement in every JD, run first-pass match against library.
2. Flag as gap if confidence <60%.
3. Deduplicate across jobs by requirement name.
4. Classify leverage:
   - **HIGH** — appears in 3+ jobs
   - **MEDIUM** — appears in 2 jobs
   - **LOW** — appears in 1 job

Write `_aggregate_gaps.md`:
```markdown
# Aggregate Gap Analysis
Batch: {batch_id}
Jobs: {N}

## Summary
Total gaps: {X}   After dedup: {Y}
HIGH: {count}   MEDIUM: {count}   LOW: {count}

## Gaps Ranked by Leverage
### HIGH — {gap_name}
Appears in: {Company1}, {Company2}, {Company3}
Best match: {%} ('{best_match_text}')
Discovery strategy: {Pattern A/B/C + key probe}
```

**Checkpoint:** Show the gap map. Ask if user wants to attempt shared discovery now or defer.

## Phase 2 — Shared Discovery

Single branching interview that addresses HIGH then MEDIUM leverage gaps. LOW-leverage gaps are surfaced per-job later (often simpler to just reframe or cover-letter).

For each gap, use the appropriate pattern from `branching-questions.md`, prefixed with leverage context so the user understands what they're unlocking.

Write captured experiences to `_discovered_experiences.md`. Tag each experience with `applies_to_jobs: [job-1, job-3]` and merge into the in-memory library.

**Output:** Enriched library ready for per-job processing.

## Phase 3 — Per-Job Processing

For each job (sequential, in priority order):

1. **Research** — full Phase 1 from single-job workflow (JD parse, company research, role benchmarking, success profile).
2. **Template** — Phase 2 (consolidation, title reframing, bullet allocation).
3. **Matching** — Phase 3 (use enriched library; LOW-leverage gaps may still surface — offer a mini-discovery loop if critical).
4. **Generation** — Phase 4 (MD + DOCX + PDF + report).
5. **Set status** → `ready_for_review` in batch state.

Two modes:
- **Interactive** (default) — checkpoints per job (success profile, template, mapping).
- **Express** (`--express` after first job) — skip checkpoints; present everything at Phase 4 batch finalization.

## Phase 4 — Batch Finalization

Present all resumes together:
```
Batch summary — {N} resumes ready for review

| Job | Company | Role | Coverage | Direct | Gaps |
|----|--------|------|---------|--------|------|
| 1  | ...    | ...  | 85%     | 12     | 1    |

Actions:
- REVIEW ALL — walk through each
- REVIEW SPECIFIC — pick one
- APPROVE BATCH — save all to library
- REVISE {job_id} — re-run specific phase
```

On approve:
- Move all artifacts into library.
- Rebuild library with enriched content + new metadata.
- Preserve batch state for incremental additions.

## Incremental Additions

If the batch already exists and the user adds new jobs:
1. Load `_batch_state.json` and `_discovered_experiences.md`.
2. Quick-parse new JDs.
3. Run incremental gap analysis — only gaps not already addressed by existing discoveries.
4. Mini-discovery for new gaps only.
5. Process new jobs through Phase 3 per-job.

Typical benefit: a 2-job add after a 3-job batch takes ~20 min vs ~30 min fresh, because 70%+ of gaps are already filled.

## Time Model

| Jobs | Sequential | Batch | Savings |
|-----|-----------|-------|---------|
| 3   | ~45 min   | ~40   | 11%     |
| 5   | ~75 min   | ~55   | 27%     |
| 7   | ~105 min  | ~70   | 33%     |

Savings grow with job similarity. Diverse jobs (different domains) gain less — fall back to sequential if overlap <40%.

## Failure Modes

- **Low overlap detected** — if aggregate dedup reduces gaps by <20%, tell the user "these jobs are too different for shared discovery to help much" and offer sequential mode.
- **Discovery fatigue** — if user is running low energy mid-Phase 2, pause, save batch state, resume later.
- **Per-job research failure** — degrade gracefully for that job (JD-only), continue batch.
- **DOCX generation fails for one job** — emit MD + report, flag in batch summary.
