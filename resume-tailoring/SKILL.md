---
name: resume-tailoring
description: Tailor a resume to a specific job by researching the company/role, surfacing undocumented experience through branching interview, matching content with confidence scores, and emitting MD + DOCX + PDF + interview-prep report. Use when the user says "I want to apply for [Role] at [Company]. Here's the JD:", pastes a job description, provides multiple JDs/URLs, or asks to tailor/optimize a resume for a role. Never fabricates experience; reframes and emphasizes truthfully.
disable-model-invocation: false
user-invocable: true
---

# /resume-tailoring — Job-Specific Resume Workflow

Build a resume around the whole person, not just the documents on file. Maximize fit to the target role while keeping every bullet factually defensible.

**Core rule:** Never fabricate experience. Reframe, emphasize, and translate terminology — do not invent.

**Trigger prompt (canonical):**
```
I want to apply for [Role] at [Company]. Here's the JD: [paste JD or URL]
```

Multi-job mode triggers automatically when the user pastes multiple JDs, multiple URLs, or says "these roles"/"batch"/"multiple jobs".

---

## Quick Start

```
/resume-tailoring                              → run full workflow, single job
/resume-tailoring --library ~/resumes          → point at a specific library
/resume-tailoring --batch                      → force multi-job mode
/resume-tailoring --no-docx                    → skip DOCX/PDF, emit markdown only
/resume-tailoring --express                    → skip checkpoints (only use after first run)
```

**Inputs the skill needs:**
1. Job description (text or URL).
2. A resume library: markdown files under `resumes/` in the current dir (or a path the user provides). Works with 1 resume, but 10+ is ideal.

**Outputs written to `resumes/tailored/{Company}_{Role}/`:**
- `{Name}_{Company}_{Role}_Resume.md`
- `{Name}_{Company}_{Role}_Resume.docx` (requires `document-skills:docx`)
- `{Name}_{Company}_{Role}_Resume.pdf` (optional)
- `{Name}_{Company}_{Role}_Report.md` — coverage %, matches, reframings, interview prep

---

## Workflow

### Phase 0 — Library build (always first)

1. Resolve library dir: use `--library` flag, else `./resumes/`, else ask. Validate it exists.
2. Glob `*.md` in the library. Announce count: `Building library... found {N} resumes`.
3. For each resume, Read and parse: contact, roles (company/title/dates), bullets, skills, education.
4. Tag each bullet: `themes` (leadership, technical, analytics, strategy…), `metrics` (numbers, %, $), `keywords` (action verbs, domain terms), `source_resume`.
5. Detect user preferences: typical length (1 vs 2 page), section order, bullet style.
6. Hold the library in memory as the candidate pool for matching.

If library has <3 resumes, warn the user: coverage will be thinner; discovery (Phase 2.5) will be especially valuable.

### Phase 1 — Research

Build a **success profile** — what would make any candidate successful for this role, not just what the JD says.

Use `research-prompts.md` templates. Three sub-steps:
1. **Parse JD.** Extract must-haves, nice-to-haves, technical keywords, implicit preferences, red flags, role archetype (IC / manager / cross-functional).
2. **Company research.** WebSearch: mission/values/culture, engineering blog, recent news, team structure.
3. **Role benchmarking.** WebSearch `site:linkedin.com {title} {company}` → WebFetch top 3-5 profiles → extract common backgrounds, skills, terminology.

If research tools are unavailable or sparse, fall back to JD-only analysis and tell the user what you couldn't get.

**Checkpoint:** Present the success profile (core reqs, valued capabilities, cultural signals, narrative themes, terminology map, risk factors). Wait for the user to confirm or adjust before continuing.

### Phase 2 — Template

Build the resume structure optimized for this role. See `matching-strategies.md` for title reframing and consolidation rules.

1. **Role consolidation.** Combine same-company consecutive positions only when continuity serves the target role better than granularity. Never merge across companies.
2. **Title reframing.** Stay truthful; emphasize the aspect most relevant to the target. Company, dates, and core responsibilities must be exact.
3. **Section order.** Use the user's library preferences unless the target role dictates otherwise (e.g., Education top if fresh grad / required credential).
4. **Bullet allocation.** Weight by role relevance × recency. Front-load the most relevant role.

**Checkpoint:** Present template skeleton with consolidation decisions, title options (with rationale), and bullet counts per role. Wait for approval.

### Phase 2.5 — Experience discovery (optional, offered when gaps found)

When any requirement has <60% confidence after a first-pass match, offer a 10–15 min branching interview. Use `branching-questions.md` patterns:

- **Technical gap:** "Have you worked with {skill} or {adjacent}?" → branch on YES / INDIRECT / ADJACENT / PERSONAL / NO.
- **Soft skill gap:** "Tell me about times you've {demonstrated_skill}" → branch on STRONG / VAGUE / PROJECT-SPECIFIC / VOLUNTEER.
- **Recent-work probe:** "What have you worked on in the last 6 months not on your resume yet?"

Capture each discovered experience as a draft bullet with context, scope, addressed gaps, and truthfulness note. Never pressure the user into a claim they can't defend. Time-box and move on after 2–3 dry attempts per gap.

### Phase 3 — Assembly (match + score)

For each template slot, score every candidate bullet using `matching-strategies.md`:

```
Overall = 0.4·Direct + 0.3·Transferable + 0.2·Adjacent + 0.1·Impact
```

**Bands:** 90+ DIRECT · 75–89 TRANSFERABLE · 60–74 ADJACENT · 45–59 WEAK · <45 GAP.

For each slot, show top 3 candidates with scores and source resume, plus any reframing proposals (with a "why this is still truthful" line). For gaps: offer reframe, omit, cover-letter, or run another discovery loop.

**Checkpoint:** Present the full mapping plus coverage summary (% direct, % transferable, % gaps, JD coverage %). Wait for approval before generation.

### Phase 4 — Generation

Write outputs to `resumes/tailored/{Company}_{Role}/`.

1. **Markdown resume.** Clean, consistent with user's library style.
2. **DOCX.** Use `document-skills:docx` sub-skill. Calibri 11pt body / 12pt headers, 0.5–1in margins, proper bullet numbering config (never unicode bullets), bold for company/title/dates.
3. **PDF** (if requested or DOCX succeeds). Via `document-skills:pdf` or DOCX→PDF conversion.
4. **Generation report.** Target summary, success profile, coverage metrics, every reframing with before/after + reason, source resume breakdown, remaining gaps with recommendations, interview prep notes (stories to prepare, likely questions, how to address gaps).

If DOCX/PDF generation fails, fall back to markdown-only and note the failure in the report.

### Phase 5 — Save + learn (conditional)

Ask the user: (1) Save to library, (2) Revise, (3) Save locally only.

On save: move all artifacts into the library, re-parse to enrich the candidate pool, and persist a metadata file (`.meta.json`) with match scores, reframings, newly-discovered experiences, and jd_coverage. Future sessions start from a richer library.

---

## Multi-Job Mode

Triggers when the user pastes multiple JDs/URLs or asks for batch. Full workflow in `multi-job-workflow.md`.

High-level phases:
1. **Intake.** Collect 3–5 JDs, priorities, notes. Initialize batch state at `resumes/batches/batch-{date}-{slug}/`.
2. **Aggregate gap analysis.** Match each JD's requirements against the library. Deduplicate across jobs. Classify: HIGH-leverage (3+ jobs), MEDIUM (2), LOW (1).
3. **Shared discovery.** One branching interview that addresses high/medium leverage gaps first. Tag each discovered experience with job relevance.
4. **Per-job processing.** For each job: research → template → matching → generation (sequential, reusing enriched library).
5. **Batch finalization.** Review all resumes together, approve/revise individually or as a batch, update library once.

**Incremental adds.** If a batch already exists, the user can add jobs later; only new gaps trigger discovery.

Typical time savings: 11% for 3 jobs, 27% for 5 jobs vs sequential single-job runs.

---

## Checkpoints & User Control

Hard stops where the skill pauses for approval:
- End of Phase 1 — success profile
- End of Phase 2 — template skeleton
- End of Phase 3 — content mapping + coverage
- End of Phase 4 — file review before library save

Any checkpoint can request: go back, adjust, or accept. `--express` flag skips checkpoints 1–3 (use only for repeat applications in a trusted batch).

---

## Truthfulness Rules (non-negotiable)

- **Never invent** a role, company, date, metric, or skill.
- **Never inflate** seniority beyond what scope defends (e.g., "Lead" only if you led).
- **Reframe, don't fabricate.** Same facts, different emphasis and terminology — always.
- **Disclose gaps honestly** in the report; offer cover-letter recommendations rather than padding the resume.
- **Show before/after** for every reframing in the generation report, plus a one-line reason the reframing is still accurate.

---

## Edge Cases

- **Tiny library (<3 resumes):** Warn, lean heavily on Phase 2.5 discovery.
- **Critical gap (<60% on must-have):** Offer reframe, discovery, cover-letter, or omit — never force a match.
- **Research fails:** Fall back to JD-only; ask user for culture/team context; proceed best-effort.
- **Vague JD:** Extract what's possible, ask user for missing context, proceed.
- **>2 page overflow:** Rank bullets by match score, propose lowest-ranked for cut, let user decide.
- **Career gap:** Frame legitimately (startup, caregiving, study, etc.); surface skills gained during the gap via discovery.

---

## References

- `research-prompts.md` — JD parsing, company research, role benchmarking, success profile synthesis templates.
- `matching-strategies.md` — scoring weights, reframing strategies, title reframing, role consolidation rules, gap handling.
- `branching-questions.md` — discovery interview branches for technical, soft-skill, and recent-work gaps.
- `multi-job-workflow.md` — full batch workflow with state schema, aggregate gap analysis, shared discovery.

## Sub-Skills Used

- `document-skills:docx` — DOCX generation (required for .docx output).
- `document-skills:pdf` — PDF generation (optional).
- WebSearch / WebFetch — company and role research (falls back gracefully).
