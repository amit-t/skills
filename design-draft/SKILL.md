---
name: design-draft
description: Run the full UXD workflow end-to-end for an approved PRD — design interview → user flow → wireframes → design system → hi-fi screens → design review → developer handoff → approve. Reads approved PRDs from pm-os automatically.
user-invocable: true
---

## Quick Start

```
/design-draft                     → List approved PRDs, pick one, run full workflow
/design-draft PLAT-01             → Run full workflow for a specific feature
/design-draft PLAT-01 --from step → Resume from a specific step (e.g. --from screens)
/design-draft --list              → Show approved PRDs and their design status
```

**What you get:** Complete design package — brief, user flow, wireframes, design system, hi-fi screens, design review, developer handoff — plus an offer to run `uxd-approve.zsh` to publish to doe-os.

---

# /design-draft — Full UXD Workflow

This command runs the complete UXD OS workflow for a feature, driven by its approved PRD. It sequences all individual skills in the correct order, skipping steps that are already complete.

---

## Step 0: Find the PRD

**Locate approved PRDs:**

```
../refinery-pm-os/outputs/prds/approved/
```

(Absolute path from HQ root: `product/refinery-pm-os/outputs/prds/approved/`)

Also check the local context library for any already-copied PRDs:
```
context-library/prds/
```

### If no feature argument was given

List all `.md` files in the approved folder and present a numbered menu:

```
Approved PRDs ready for design:

  1. PLAT-01 — Authentication & Identity
  2. PLAT-02 — [title from file]
  ...

Which feature would you like to design? (Enter number or feature ID)
```

### If feature argument was given

Find the matching file (`*{FEATURE}*.md`) in the approved folder. If not found, error:
```
No approved PRD found matching "{FEATURE}" in pm-os/outputs/prds/approved/
Run /prd-approve to approve a PRD first, or check the feature ID.
```

---

## Step 1: Load PRD Context

Copy the PRD to `context-library/prds/` if not already present.

Read the PRD and extract:
- Feature name and ID (e.g. PLAT-01)
- Problem statement and user stories
- User types / personas
- Screens or flows mentioned
- Success criteria and acceptance criteria
- Out-of-scope items

Print a summary:
```
PRD loaded: [FEATURE-ID] — [Feature Title]

Extracted context:
  - [N] user types: [list]
  - [N] screens/flows identified: [list]
  - Key constraints: [list]
  - Out of scope: [list]

Starting design workflow...
```

---

## Step 2: Design Interview Brief

**Skill:** `/design-interview`

Extract as much context as possible from the PRD (skip questions the PRD already answers). Ask only for gaps:

- Visual direction (style adjectives, references) — PRDs rarely specify this
- Mode preference (light/dark/both)
- Any hard technical constraints not in the PRD

Save the brief to:
```
outputs/design-briefs/[FEATURE-ID]-[feature-name]-brief.md
```

If a brief already exists for this feature, show it and ask: "Use existing brief or update it?"

---

## Step 3: User Flow

**Skill:** `/user-flow`

Map all user flows for the feature. Include:
- All happy paths
- Key error/edge paths (account disabled, SSO unavailable, rate limited, etc.)
- Decision nodes (MFA enforced? SSO-only workspace?)
- Screen-to-screen transitions

Save to:
```
outputs/user-flows/[FEATURE-ID]-[feature-name]-user-flow.md
```

Skip if the file already exists and user confirms it's current.

---

## Step 4: Wireframes

**Skill:** `/wireframe`

Create ASCII wireframes for all screens identified in the user flow. Focus on:
- Layout structure and information hierarchy
- Navigation placement
- Key UI regions (forms, CTAs, empty states)

Save to:
```
outputs/wireframes/[FEATURE-ID]-[feature-name]-wireframes.md
```

Skip if already exists and user confirms.

---

## Step 5: Design System

**Skill:** `/design-system`

Check if `outputs/design-systems/refinery-design-system.html` already exists.

- **If yes:** Review it and note any components needed for this feature that are missing. Add them if needed.
- **If no:** Create the full design system for the project.

The design system must cover all components needed by this feature's screens.

---

## Step 6: Hi-Fidelity Screens

**Skill:** `/generate-screens`

Generate all screens identified in the user flow. For each screen:

1. Announce: `Generating: [Screen Name] ([N] of [Total])`
2. Build the screen (all states: default, empty, loading, error)
3. Save to `outputs/screens/[FEATURE-ID]-[screen-name].html`
4. Confirm before proceeding to the next screen

**Required screens minimum:** Every distinct step in the user flow that a user sees. Include:
- All happy path screens
- Error state reference sheet (grouped, if >3 error states)
- Admin/settings screens if the PRD includes admin configuration

After all screens:
```
All [N] screens generated.

outputs/screens/
  [FEATURE-ID]-[screen-1].html
  [FEATURE-ID]-[screen-2].html
  ...

Next: running design review across all screens.
```

---

## Step 7: Design Review

**Skill:** `/design-review`

Run the 5-agent multi-perspective review across all generated screens:

- UX Researcher — usability, flow logic, user goals
- Accessibility Auditor — WCAG AA, keyboard nav, screen reader
- Engineer — implementation complexity, component reuse, feasibility
- Brand Guardian — visual consistency, design system adherence
- End User Voice — first impression, confusion points, delight moments

Format each agent's review as:
```
✅ What works
⚠️ Concerns
💡 Suggestions
```

Synthesise all perspectives at the end. Highlight P0 (must fix) vs P1/P2 issues.

Save to:
```
outputs/design-reviews/[FEATURE-ID]-design-review.md
```

Ask: "Would you like to fix any P0 issues before handoff?" If yes, regenerate the affected screens.

---

## Step 8: Developer Handoff

**Skill:** `/handoff`

Generate the complete developer handoff document:

- All CSS design tokens used
- Per-screen specs (spacing, states, accessibility requirements)
- Component library mapping (which HTML/CSS component maps to which React component)
- API → frontend data contract (response shapes, token storage, error handling)
- Suggested React file structure for the feature (`apps/web/src/features/[feature]/`)
- Open items table (items blocked on API, product decisions still open, etc.)

Save to:
```
outputs/handoffs/[FEATURE-ID]-[feature-name]-handoff.md
```

---

## Step 8b: Update Preview Manifest

**After all screens for the feature are generated**, update the screen manifest so they appear in the preview hub.

File: `outputs/screens/manifest.js`

1. Open `outputs/screens/manifest.js`
2. Add a new feature block (or update the existing one) following the exact structure already in the file
3. For each screen generated, add an entry with:
   - `name` — human-readable screen name
   - `file` — exact HTML filename (e.g. `PLAT-03-foo-bar.html`)
   - `route` — app URL route (e.g. `/ws/{slug}/dashboard`)
   - `group` — grouping label (e.g. `"Settings"`, `"Creation wizard"`)
   - `description` — one sentence describing the screen

4. Set `status: "draft"` for newly generated features; `status: "approved"` only after `uxd-approve.zsh` runs

**Also wire navigation** in the new screens:
- Any Next/Back/CTA buttons that navigate between screens → add `onclick="window.location.href='[filename].html'"`
- Sidebar nav links in settings screens → use relative filenames, not absolute `/ws/...` paths
- Tabs that switch between sub-screens (e.g. Active/Pending invite tabs) → use relative `href="[filename].html"`

After updating manifest, confirm: "Preview manifest updated — open `outputs/preview.html` to browse all screens."

---

## Step 9: Approve and Publish

```
Design package complete for [FEATURE-ID]:

  outputs/design-briefs/[FEATURE-ID]-*-brief.md       ✓
  outputs/user-flows/[FEATURE-ID]-*-user-flow.md       ✓
  outputs/wireframes/[FEATURE-ID]-*-wireframes.md      ✓
  outputs/screens/[FEATURE-ID]-*.html                  ✓ ([N] screens)
  outputs/design-reviews/[FEATURE-ID]-design-review.md ✓
  outputs/handoffs/[FEATURE-ID]-*-handoff.md           ✓
  outputs/screens/manifest.js                          ✓ (preview hub updated)

Ready to approve and publish to doe-os?

  This will:
  1. Copy screens, handoffs, and design reviews to outputs/*/approved/
  2. Copy those artifacts to doe-os/outputs/designs/ (so the engineer can
     update SPEC and TDD to include frontend implementation tasks)
  3. After this, run sync-all.zsh from the app dir and then rpc.plan

  Run now? [y/N]
```

If yes, run:
```bash
./scripts/uxd-approve.zsh [FEATURE-ID]
```

If the script is not executable or not found, print the command for the user to run manually.

After approval:
```
Published. Next steps:

  1. Update SPEC-[FEATURE-ID] in doe-os — add frontend implementation tasks
  2. Update TDD for [FEATURE-ID] — reference handoff at doe-os/outputs/designs/handoffs/
  3. cd engineering/refinery-app && ./ai/sync-all.zsh
  4. rpc.plan
```

---

## Resume From Step (`--from`)

| Flag | Starts at |
|------|-----------|
| `--from interview` | Step 2 — Design Interview |
| `--from flow` | Step 3 — User Flow |
| `--from wireframes` | Step 4 — Wireframes |
| `--from system` | Step 5 — Design System |
| `--from screens` | Step 6 — Hi-Fi Screens |
| `--from review` | Step 7 — Design Review |
| `--from handoff` | Step 8 — Developer Handoff |
| `--from approve` | Step 9 — Approve and Publish |

When resuming, always re-read existing outputs for that feature before starting the resumed step.

---

## Status Command (`--list`)

Show all approved PRDs and their design status:

```
Approved PRDs — Design Status

  PLAT-01  Authentication & Identity
           Brief ✓  Flow ✓  Wireframes ✓  Screens ✓ (8)  Review ✓  Handoff ✓
           Status: APPROVED — run uxd-approve.zsh to publish

  PLAT-02  Workspace & Team Management
           Brief ✗  Flow ✗  Wireframes ✗  Screens ✗  Review ✗  Handoff ✗
           Status: Not started — run /design-draft PLAT-02 to begin

  ...
```

Detection logic: check for files matching `*[FEATURE-ID]*` in each output folder.
