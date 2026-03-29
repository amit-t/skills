---
name: prd-approve
description: Approve a reviewed PRD — updates status, copies to approved inbox, and updates PRD-PIPELINE.md. Run only after /prd-review-panel is complete and you are satisfied with the output.
disable-model-invocation: false
user-invocable: true
---

## Quick Start

Run this only after `/prd-review-panel` is done and you have reviewed the synthesis.

```
/prd-approve                        → List draft PRDs, pick one to approve
/prd-approve [prd-filename]         → Approve a specific PRD by name
```

**What you get:** Status updated to `Approved` in the PRD file, PRD copied to `outputs/prds/approved/`, and `PRD-PIPELINE.md` updated. Ready for `hq.sync-context` → `rpc.plan`.

---

## Context Routing Logic (Internal — for Claude)

Before doing anything, check:

| Source | What to look for |
|--------|-----------------|
| `outputs/prds/` | All `.md` files with `Status: Draft` (exclude the `approved/` subfolder) |
| `outputs/prds/*-review-synthesis.md` | Confirm a synthesis file exists for the PRD being approved |
| `PRD-PIPELINE.md` | Find the row matching this PRD to update it |

---

## Workflow

### Step 1: Identify the PRD to approve

**If user specified a filename:**
- Look for it in `outputs/prds/`
- If not found: list all draft PRDs and ask user to pick

**If no filename given:**
- Scan `outputs/prds/` for files with `Status: Draft` (ignore `approved/` subfolder and `*-review-synthesis.md` files)
- Present a numbered list:
  ```
  Draft PRDs available for approval:
  1. feature-name-team-kickoff.md (last modified: YYYY-MM-DD)
  2. another-feature-planning-review.md (last modified: YYYY-MM-DD)

  Which would you like to approve?
  ```

---

### Step 2: Review gate check

Read the PRD file. Verify:

1. `Status:` field is `Draft` (not already `Approved` or `In Review`)
2. A corresponding review synthesis file exists: `outputs/prds/[prd-name]-review-synthesis.md`

**If no synthesis file found:**
```
No review panel synthesis found for this PRD.

Run /prd-review-panel first, then come back here once you're satisfied with the output.
```
Stop — do not proceed.

**If synthesis exists**, read it and surface a brief summary:
```
Review synthesis found: [filename]
Overall assessment: [pull the "Overall Assessment" line from TL;DR]
Critical blockers: [X] | Important gaps: [Y]

Are you satisfied with the review panel output and ready to approve this PRD?
(yes / no)
```

Wait for explicit confirmation before proceeding.

---

### Step 3: Update PRD status

Read the PRD file. Find the `Status:` line in the frontmatter header block:

```markdown
**Status:** Draft
```

Replace with:

```markdown
**Status:** Approved
```

Also update `**Last Updated:**` to today's date (YYYY-MM-DD).

Save the file in place (`outputs/prds/[prd-name].md`).

---

### Step 4: Copy to approved inbox

Copy the updated file to `outputs/prds/approved/[prd-name].md`.

```
outputs/prds/[prd-name].md          ← source (keep this, it's the living file)
outputs/prds/approved/[prd-name].md ← approved snapshot (ralph reads from here)
```

If `outputs/prds/approved/` does not exist, create it.

If a file already exists at the approved path, overwrite it (the PM re-approved after changes).

---

### Step 5: Update PRD-PIPELINE.md

Read `PRD-PIPELINE.md` (at the repo root, one level up from `outputs/`).

Find the row in the Active Pipeline table that matches this PRD. It will have the PRD filename or feature name.

Update the `PRD` column value from whatever it currently shows (e.g., `~ PRD-00X`) to:

```
✓ PRD-00X (approved)
```

Keep the rest of the row intact. Save the file.

---

### Step 6: Confirm and show next steps

```
PRD approved!

Updated:  outputs/prds/[prd-name].md  →  Status: Approved
Copied:   outputs/prds/approved/[prd-name].md
Pipeline: PRD-PIPELINE.md row updated  ✓

Next steps to publish to ralph:
1. Run hq.sync-context   — syncs approved PRD + specs into the app's AI context
2. Run rpc.plan          — generates fix_plan.md from approved PRDs and specs
3. Update PRD-PIPELINE.md — fill in the fix_plan column once generated

Need an engineering spec first? Head to your doe-os repo and write the spec before running rpc.plan.
```

---

## Output Quality Self-Check

Before confirming to the user, verify:

- [ ] **Review synthesis confirmed:** Synthesis file exists and user gave explicit approval
- [ ] **Status field updated:** PRD file now shows `Status: Approved` (not Draft)
- [ ] **Last Updated refreshed:** Date reflects today
- [ ] **Approved copy created:** File exists at `outputs/prds/approved/[prd-name].md`
- [ ] **Pipeline updated:** Matching row in PRD-PIPELINE.md shows `✓` in the PRD column
- [ ] **Next steps shown:** User knows to run `hq.sync-context` → `rpc.plan`

---

## Related Skills

**Before this:**
- `/prd-draft` — write the initial PRD
- `/prd-review-panel` — run the 7-agent review (required gate)

**After this:**
- `hq.sync-context` — publish approved PRD into the app's AI context
- `rpc.plan` / `rpd.plan` / `rpx.plan` — generate fix_plan.md
