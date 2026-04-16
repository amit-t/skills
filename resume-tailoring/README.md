# resume-tailoring

> Tailor a resume to a specific job: research the company, surface undocumented experience via branching interview, match content with confidence scores, and emit MD + DOCX + PDF + interview-prep report — all while keeping every bullet factually defensible.

**Category:** Engineering

## What It Does

The skill takes a job description and your existing resume library, and produces a job-specific resume plus a generation report. It goes beyond keyword matching:

1. **Library build** — scans a `resumes/` directory of your existing resumes in markdown and tags bullets with themes, metrics, keywords.
2. **Research** — parses the JD, researches the company (WebSearch), benchmarks the role (LinkedIn/GitHub profiles), and synthesizes a success profile.
3. **Template** — proposes role consolidation and title reframing with 2 options and a recommendation, with you approving before anything is written.
4. **Discovery (optional)** — offers a 10–15 min branching interview to surface undocumented experience when any requirement scores <60% confidence.
5. **Matching** — scores every candidate bullet on Direct / Transferable / Adjacent / Impact and shows you the top 3 per slot with reframing proposals.
6. **Generation** — writes MD + DOCX + PDF plus a report with coverage metrics, every before/after reframing with a truthfulness note, remaining gaps with recommendations, and interview prep.
7. **Save + learn** — optionally adds the approved resume back to your library so future runs start from a richer candidate pool.

**Multi-job batch mode** kicks in automatically when you paste multiple JDs: it runs one shared discovery session across all jobs (prioritizing gaps that appear in 3+ jobs), then processes each job with its own research and matching. 11–33% faster than sequential single-job runs, depending on overlap.

**Truthfulness contract (non-negotiable):**
- Never invents roles, companies, dates, metrics, or skills.
- Never inflates seniority beyond what scope defends.
- Every reframing has a before/after + "why this is still accurate" line in the report.
- Gaps are disclosed honestly with cover-letter recommendations, not padded.

### Canonical Trigger

```
I want to apply for [Role] at [Company]. Here's the JD: [paste JD or URL]
```

Or pass multiple JDs to trigger batch mode:

```
I want to apply for these 3 roles:
1. Microsoft 1ES — Principal PM: [JD or URL]
2. Google Cloud — Senior TPM: [JD or URL]
3. AWS Containers — Senior PM: [JD or URL]
```

### When It Triggers

- User pastes a job description or URL and asks for a tailored resume.
- User says "tailor my resume to X", "apply for Y at Z", "resume for this role".
- User provides multiple JDs (auto-detects batch mode).

## Prerequisites

- A `resumes/` directory (default) or any path you pass via `--library` containing at least 1 resume in markdown. 10+ is ideal.
- Optional: `document-skills:docx` sub-skill for DOCX output (skill falls back to markdown-only if missing).
- Optional: WebSearch / WebFetch for company and role research (falls back to JD-only analysis gracefully).

## Install

```bash
npx skills@latest add amit-t/skills --skill resume-tailoring
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r resume-tailoring .cognition/skills/resume-tailoring
# or
cp -r resume-tailoring .windsurf/skills/resume-tailoring

# Global
cp -r resume-tailoring ~/.config/cognition/skills/resume-tailoring
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r resume-tailoring .claude/skills/resume-tailoring

# Global
cp -r resume-tailoring ~/.claude/skills/resume-tailoring
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r resume-tailoring .cursor/skills/resume-tailoring
```

</details>

<details>
<summary>Codex</summary>

Codex uses `AGENTS.md` for skills. Append the skill's main file and reference files:

```bash
cat resume-tailoring/SKILL.md >> AGENTS.md
# Optional: make companion files discoverable by keeping them next to AGENTS.md
mkdir -p .codex/resume-tailoring
cp resume-tailoring/*.md .codex/resume-tailoring/
```

Or use the portable bundle:

```bash
cat resume-tailoring/resume-tailoring.skill >> AGENTS.md
```

The `.skill` bundle inlines SKILL.md and all companion references in a single file, so you only need to append once.

</details>

<details>
<summary>Gemini CLI</summary>

```bash
cat resume-tailoring/SKILL.md >> GEMINI.md
# or the bundled single-file version
cat resume-tailoring/resume-tailoring.skill >> GEMINI.md
```

</details>

<details>
<summary>Co-Work (single-file <code>.skill</code> bundle)</summary>

Some agent runtimes (co-work, plain prompt pipelines, slim IDE plugins) accept a single-file skill manifest. Use the bundled `.skill` file:

```bash
# Add to a co-work project
cp resume-tailoring/resume-tailoring.skill .cowork/skills/

# Or paste its contents into the agent's system prompt / skills panel
cat resume-tailoring/resume-tailoring.skill
```

The `.skill` file is self-contained — SKILL.md + research-prompts + matching-strategies + branching-questions + multi-job-workflow all inlined, with YAML frontmatter at the top.

</details>

## Usage

Once installed, invoke it:

```text
/resume-tailoring
```

…or simply ask the agent to tailor a resume using the canonical trigger prompt. The skill will activate automatically when it sees a JD-plus-role intent.

### Flags

| Flag | Effect |
|------|--------|
| `--library <path>` | Point at a resume library other than `./resumes/` |
| `--batch` | Force multi-job mode even for a single JD |
| `--no-docx` | Emit markdown only (skip DOCX/PDF) |
| `--express` | Skip checkpoints — use only after an initial interactive run |

### Outputs

Written to `resumes/tailored/{Company}_{Role}/`:

- `{Name}_{Company}_{Role}_Resume.md`
- `{Name}_{Company}_{Role}_Resume.docx` (when DOCX sub-skill available)
- `{Name}_{Company}_{Role}_Resume.pdf` (optional)
- `{Name}_{Company}_{Role}_Report.md` — coverage %, matches with scores, reframings with before/after + truthfulness notes, remaining gaps, interview prep

Multi-job runs also write a batch directory at `resumes/batches/batch-{date}-{slug}/` with state, aggregate gap analysis, and shared discovery transcript.

## Files

- `SKILL.md` — main workflow (all 5 phases + multi-job overview).
- `research-prompts.md` — JD parsing, company research, role benchmarking, success profile templates.
- `matching-strategies.md` — scoring formula, reframing strategies, title reframing, role consolidation, gap handling.
- `branching-questions.md` — discovery interview branches (technical, soft-skill, recent-work).
- `multi-job-workflow.md` — full batch workflow with state schema.
- `resume-tailoring.skill` — portable single-file bundle for co-work / Codex / plain prompt pipelines.

## License

MIT
