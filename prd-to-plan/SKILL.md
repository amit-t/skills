---
name: prd-to-plan
description: Turn a PRD into a multi-phase implementation plan using tracer-bullet vertical slices, saved as a local Markdown file in ./plans/. Use when the user wants to break a PRD into an implementation plan, or mentions "tracer bullets".
---

# PRD to Plan

Break a PRD into a phased implementation plan using vertical slices (tracer bullets). Output is a Markdown file in `./plans/`.

## Process

### 1. Confirm the PRD is in context

The PRD should already be in the conversation. If it isn't, ask the user to paste it or point you to the file.

### 2. Explore the codebase

If you have not already explored the codebase, do so to understand the current architecture, existing patterns, and integration layers.

### 3. Identify durable architectural decisions

Before slicing, identify high-level decisions that are unlikely to change throughout implementation:

- Route structures / URL patterns
- Database schema shape
- Key data models
- Authentication / authorization approach
- Third-party service boundaries

These go in the plan header so every phase can reference them.

### 4. Draft vertical slices

Break the PRD into **tracer bullet** phases: each phase is a thin vertical slice that cuts through every integration layer end-to-end, never a single horizontal layer.

<vertical-slice-rules>
- Each slice delivers a narrow but complete path through every layer (schema, API, UI, tests)
- A completed slice is demoable or verifiable on its own
- Prefer many thin slices over few thick ones
- Include durable decisions only — route paths, schema shapes, data model names — and omit file names, function names, or other implementation details likely to change as later phases are built
</vertical-slice-rules>

### 5. Quiz the user

Present the proposed breakdown as a numbered list. For each phase show:

- **Title**: short descriptive name
- **User stories covered**: which user stories from the PRD this addresses

Ask the user:

- Does the granularity feel right? (too coarse / too fine)
- Should any phases be merged or split further?

Iterate until the user approves the breakdown.

### 6. Write the plan file

Create `./plans/` if it doesn't exist. Write the plan as a Markdown file named after the feature (e.g. `./plans/user-onboarding.md`), using the template in [`PLAN-TEMPLATE.md`](PLAN-TEMPLATE.md).
