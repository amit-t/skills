---
name: pmo-status
description: Full project status across Product (PM-OS), Engineering DOE (specs/ADRs), and Engineering Implementation (fix_plan/ralph). Run this at the start of any session to orient yourself, or on demand.
---

# /pmo-status — Full Project Status

When this skill is invoked, read the following files in parallel, then produce the structured status report below.

## Files to Read

Read ALL of these before producing output.

**Compute the project root first:** The base directory for this skill is provided at the top of this prompt (e.g. `/path/to/project/.claude/skills/pmo-status`). The project root is 3 levels up: `{base_dir}/../../..`. Use this to construct all paths below — do NOT hardcode absolute paths.

Also read `{project_root}/project.conf` to resolve directory names (PM_OS_DIR, DOE_OS_DIR, APP_DIR).

1. `{project_root}/PRD-PIPELINE.md` — pipeline tracker (source of truth)
2. `{project_root}/{APP_DIR}/.ralph/fix_plan.md` — ralph task list
3. List of files in `{project_root}/{PM_OS_DIR}/outputs/prds/` — PRD inventory
4. List of files in `{project_root}/{PM_OS_DIR}/outputs/prds/approved/` — approved PRDs
5. List of files in `{project_root}/{DOE_OS_DIR}/outputs/specs/` — spec inventory

## Output Format

Produce the report in exactly this structure. Be concise — each row/line should be one line. No padding, no filler.

---

## PMO Status
_as of {today's date}_

---

### 1. Product Layer (PM-OS)

List every PRD with its current status. Pull from PRD-PIPELINE.md Active Pipeline + Completed sections, cross-checked against the actual files in pm-os/outputs/prds/.

| PRD | Status | Approved? | Notes |
|-----|--------|-----------|-------|

Then list Queued PRDs (from PRD-PIPELINE.md Queued section):

**Queued (not yet written, in priority order):**
- Priority N — Feature name — one-line rationale

---

### 2. Engineering DOE Layer (doe-os)

List every spec file found in doe-os/outputs/specs/ with its status (pull from PRD-PIPELINE.md where available, otherwise infer from the filename and pipeline).

| Spec | Status | Linked PRD | Notes |
|------|--------|------------|-------|

---

### 3. Engineering Implementation (ralph / fix_plan)

**fix_plan last run:** {date from fix_plan header}
**Sources analyzed:** {from fix_plan header}

#### In Progress / Active Sprint
List any tasks marked `[~]` or currently being executed.

#### High Priority — Pending
Summarise the high-priority task groups with task count and first unblocked task.

#### Medium Priority — Pending
Summarise medium-priority groups with task count.

#### Completed (this fix_plan)
Count of `[x]` tasks by group. One line per group.

#### Blocked
Any tasks with a BLOCKED flag, what they're waiting on.

---

### 4. Feature Map

List features from the fix_plan Completed section and pipeline tracker.

| # | Feature | Backend | Frontend | Tests | Notes |
|---|---------|---------|----------|-------|-------|

Use: ✓ Done / ~ Partial / ✗ None / — N/A / ✗ Blocked

---

### 5. Blockers & Risks

List anything that is explicitly blocked (external or internal), and any risks visible from the fix_plan notes or PRD pipeline.

---

### 6. Next Actions

The 3-5 most important next actions across all three layers. Be specific — name the exact command, file, or task.

1. **[Layer]** Action — why
2. ...

---

After producing the report, offer:
"Want me to dive into any section, or start a planning session for a specific feature?"
