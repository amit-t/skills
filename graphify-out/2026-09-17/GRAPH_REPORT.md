# Graph Report - at-skills  (2026-09-15)

## Corpus Check
- 154 files · ~104,109 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 1195 nodes · 1160 edges · 103 communities (93 shown, 9 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 34 edges (avg confidence: 0.81)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `9e3e7db8`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- 7 Reviewer Sub-Agents (Eng/Design/Exec/Legal/UXR/Skeptic/Customer)
- TDD Skill (red-green-refactor)
- eng-spec Skill
- PRD Draft Skill
- site.js
- Changelog
- Skill Authoring Convention (SKILL.md + README.md per skill)
- Write-a-Skill Skill
- Multi-Job Workflow
- grill-me-auto
- 4. Components
- PMO Status Skill
- compact-conversation Skill
- request-refactor-plan Skill
- package-scout Skill
- /code-review-multi-axis — Principal-Engineer Review, Pre-PR and Post-PR
- concise-reporting Skill
- templates/site.js
- Part 2 — `skill-sync` utility
- gh-repo-mirror — Reference
- code-review-multi-axis — Reference
- The 10-step flow
- PRD template
- grill-summary
- docs-from-prs
- docs-from-prs
- docs-from-prs
- Process
- /resume-tailoring — Job-Specific Resume Workflow
- /session-feedback — Distill a session, and recall it deliberately
- Matching Strategies
- /resume-tailoring — Job-Specific Resume Workflow
- GitHub Pages — Neo-Brutalist
- Process
- resume-session-handoff
- /leadership-update — Outcome-First Status Updates
- resume-tailoring
- session-handoff
- Workflow
- Steps
- /skill-sync — Sync or Build at-skills Skills From a Source Path
- AI PRD Additional Sections
- Skills Catalog README
- Multi-Job Workflow
- /faq — Answer a Question and Record It in the Repo FAQ
- Step-by-Step Workflow
- Branching Questions
- domain-grill
- session-feedback
- Session Handoff
- setup-amit-skills
- Grill Summary Behavioral Cases
- docs-from-prs
- faq
- skill-sync
- Process
- ADR Format
- gh-repo-mirror
- leadership-update
- ADR Format
- repo-context-scan
- Research Prompts
- setup-pre-commit
- two-axis-review
- Wisdom Capture — Reference
- grill-me
- write-a-skill
- Grill Summary Design
- E2E Package Scaffold
- Document Templates
- gh-pages-neo-brutalist
- Resume Session Handoff
- CONTEXT.md
- wisdom-capture
- CONTEXT.md Format (read reference)
- Report & Fix-Plan Templates
- git-guardrails-claude-code Skill
- CONTEXT.md Format
- Context Map
- index.md
- ADR format
- amit-t/skills conventions
- amit-t/skills category vocabulary
- Fixture: ambiguous between writing + leadership
- Fixture: high-confidence engineering snippet
- Fixture: forces a new-bucket proposal
- Grill Summary Implementation Plan
- PANEL-PROMPTS.md
- UX-INTEGRATION.md
- block-dangerous-git.sh
- PROTOTYPE-TEMPLATES.md
- REVIEWER-PROMPTS.md
- SYNTHESIS-TEMPLATE.md
- Dependency Injection for Mockability
- SDK-style Interfaces over Generic Fetchers
- design-review Skill
- design-draft Skill (Full UXD Workflow)
- Map: A Calm Ordering Rollout
- write-a-prd Skill
- prd-to-plan Skill
- design-interview Skill
- Resume and Status

## God Nodes (most connected - your core abstractions)
1. `gh-repo-mirror — Reference` - 17 edges
2. `4. Components` - 15 edges
3. `design-draft Skill (Full UXD Workflow)` - 13 edges
4. `code-review-multi-axis — Reference` - 12 edges
5. `Rubric` - 12 edges
6. `docs-from-prs` - 11 edges
7. `docs-from-prs` - 11 edges
8. `/code-review-multi-axis — Principal-Engineer Review, Pre-PR and Post-PR` - 11 edges
9. `docs-from-prs` - 11 edges
10. `Process` - 11 edges

## Surprising Connections (you probably didn't know these)
- `Catalog Sync Rule (Mandatory)` --semantically_similar_to--> `CLAUDE Catalog Sync Rule (Mandatory)`  [INFERRED] [semantically similar]
  AGENTS.md → CLAUDE.md
- `write-a-prd Skill` --semantically_similar_to--> `5-Section Interview (Product/Users/Visual/Constraints/Success)`  [INFERRED] [semantically similar]
  write-a-prd/SKILL.md → design-interview/SKILL.md
- `5-Agent Engineering Panel Review` --semantically_similar_to--> `Review Panel Synthesis File`  [INFERRED] [semantically similar]
  eng-spec/SKILL.md → prd-approve/SKILL.md
- `Write-a-Skill Skill` --semantically_similar_to--> `PRD Draft Skill`  [INFERRED] [semantically similar]
  write-a-skill/SKILL.md → prd-draft/SKILL.md
- `Designer Reviewer Agent` --semantically_similar_to--> `Accessibility Auditor (WCAG 2.1 AA)`  [INFERRED] [semantically similar]
  prd-review-panel/SKILL.md → design-review/SKILL.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **PRD-to-Ralph Pipeline Flow** — prdapprove_skill, engspec_skill, engspec_hq_sync_context, engspec_rpc_plan [EXTRACTED 0.90]
- **PRD Draft Conversational Workflow** — prddraft_step0_context_check, prddraft_step1_clarifying_questions, prddraft_step2_first_draft, prddraft_step2_5_prototype, prddraft_step3_multi_agent_review [EXTRACTED 0.95]
- **QA Session End-to-End Flow** — qa_listen_clarify, qa_explore_codebase, qa_assess_scope, qa_file_github_issue, qa_continue_session [EXTRACTED 0.95]
- **TDD Red-Green-Refactor Loop Participants** — tdd_planning_step, tdd_tracer_bullet, tdd_red_green_refactor, tdd_refactor_step, tdd_cycle_checklist [EXTRACTED 0.95]
- **UXD Full Workflow Pipeline** — designdraft_skill, designinterview_skill, designreview_skill, designdraft_step9_approve [EXTRACTED 0.95]
- **Catalog Sync Required Artifacts** — readme_catalog, agents_site_js_skills_array, agents_site_js_changes_array, changelog_doc, concept_skill_authoring [EXTRACTED 1.00]
- **5-Agent Engineering Panel Review** — engspec_architect_reviewer, engspec_db_designer_reviewer, engspec_principal_swe_reviewer, engspec_sdet_reviewer, engspec_perf_engineer_reviewer [EXTRACTED 1.00]
- **Engineering Spec Artifact Trio (TDD/SPEC/ADR)** — engspec_tdd, engspec_spec, engspec_adr [EXTRACTED 1.00]
- **PRD Review 7-Agent Panel** — prdreviewpanel_engineer_agent, prdreviewpanel_designer_agent, prdreviewpanel_exec_agent, prdreviewpanel_legal_agent, prdreviewpanel_uxr_agent, prdreviewpanel_skeptic_agent, prdreviewpanel_customer_voice_agent [EXTRACTED 1.00]

## Communities (103 total, 9 thin omitted)

### Community 0 - "7 Reviewer Sub-Agents (Eng/Design/Exec/Legal/UXR/Skeptic/Customer)"
Cohesion: 0.16
Nodes (14): 5 Reviewers (UXR/A11y/Engineer/Brand/EndUser), Accessibility Auditor (WCAG 2.1 AA), Brand Guardian Reviewer, End User Voice Reviewer, Engineer Feasibility Reviewer, UX Researcher Reviewer, Customer Voice Agent, Designer Reviewer Agent (+6 more)

### Community 1 - "TDD Skill (red-green-refactor)"
Cohesion: 0.10
Nodes (24): Step 3: Assess Scope (single vs breakdown), Breakdown Template (parallel issues), Step 5: Continue Session, Durable Issues (no file paths or line numbers), Step 2: Explore Codebase via Subagent, Step 4: File GitHub Issues, Step 1: Listen and Lightly Clarify, qa Skill README (+16 more)

### Community 2 - "eng-spec Skill"
Cohesion: 0.06
Nodes (37): Auth Storage Discovery, Diagnostic Report (Markdown), False Positive Check (negative assertions), In-Memory Auth (Zustand) Strategy, Playwright Test Framework, PRD-Driven Tests, Rationale: Auth Storage Drives Fixture Strategy, e2e-audit README (+29 more)

### Community 3 - "PRD Draft Skill"
Cohesion: 0.09
Nodes (24): 10 Principles for AI Products, AI Behavior Contract, Part 3: AI Feature PRDs, AI Behavior Specification (Good/Bad/Reject), Context Routing Logic, $1-$10-$100 Prototype Rule, Part 2: Full PRD Workflow (7 steps), PRD Hypothesis Section (If/Then/Because) (+16 more)

### Community 4 - "site.js"
Cohesion: 0.10
Nodes (31): addCopyButtons(), catClass(), categories, categoryCountEl, changeList, changes, copyText(), drawer (+23 more)

### Community 5 - "Changelog"
Cohesion: 0.25
Nodes (8): Compact Conversation Skill Added (2026-04-08), Concise Reporting Added (2026-04-02), Changelog, E2E Audit Skill Added (2026-04-05), Eng-Spec, Git-Guardrails, TDD, Ubiquitous Language, Design Interview Added (2026-03-28), Flatten Skill Directories (2026-03-29), PRD-to-Plan, QA, Refactor-Plan Added (2026-03-31), Precision Mode + Package Scout Added (2026-04-03)

### Community 6 - "Skill Authoring Convention (SKILL.md + README.md per skill)"
Cohesion: 0.12
Nodes (17): Catalog Sync Rule (Mandatory), Category to CSS Class Mapping, AGENTS.md - Project Agent Instructions, Git Conventions (dev branch, conventional commits), site.js changes array requirement, site.js skills array requirement, Skill Authoring Reference (write-a-skill), CLAUDE Catalog Sync Rule (Mandatory) (+9 more)

### Community 7 - "Write-a-Skill Skill"
Cohesion: 0.06
Nodes (32): Description Requirements, Process, Review Checklist, SKILL.md Template, Skill Structure, When to Add Scripts, When to Split Files, Writing Skills (+24 more)

### Community 8 - "Multi-Job Workflow"
Cohesion: 0.05
Nodes (41): 1. JD Parsing, 2. Company Research, 3. Role Benchmarking, 4. Success Profile Synthesis, 5. Graceful Degradation, Adjacent (20%), Branching Questions, Capture Template (+33 more)

### Community 9 - "grill-me-auto"
Cohesion: 0.05
Nodes (34): Answering, Credits, Document naming convention, Grill depth, grill-me-auto, How it works, Install, License (+26 more)

### Community 10 - "4. Components"
Cohesion: 0.06
Nodes (35): 1. Design Tokens, 2. Typography, 3. Layout, 4.10 Drawer (slide-in from right), 4.11 Breadcrumbs, 4.12 Markdown body (for Jekyll-rendered content), 4.13 Copy button (auto-attached to `<pre>`), 4.14 Footer (+27 more)

### Community 11 - "PMO Status Skill"
Cohesion: 0.22
Nodes (11): Blockers & Risks Section, Engineering DOE Layer (doe-os), Feature Map, ralph fix_plan.md, Engineering Implementation (ralph / fix_plan), Next Actions (3-5 specific items), PRD-PIPELINE.md (source of truth), Product Layer (PM-OS) (+3 more)

### Community 12 - "compact-conversation Skill"
Cohesion: 0.18
Nodes (11): Native /compact Command, Rationale: Prefer Native Compaction, compact-conversation README, compact-conversation Skill, Conversation Summary Document, Domain-Driven Design (DDD), Example Dialogue Pattern, Flagged Ambiguities Section (+3 more)

### Community 13 - "request-refactor-plan Skill"
Cohesion: 0.22
Nodes (9): Decision Tree Walk, grill-me README, grill-me Skill, GitHub Issue (Refactor Plan), Martin Fowler (cited), request-refactor-plan README, request-refactor-plan Skill, Refactor Plan Template (+1 more)

### Community 14 - "package-scout Skill"
Cohesion: 0.22
Nodes (9): bundlephobia.com (cited), Package Comparison Table, Lockfile-Based Package Manager Detection, Quality Signals (stars, downloads, vulns), Rationale: Avoid Stale Training Data, package-scout README, package-scout Skill, Snyk / socket.dev (cited) (+1 more)

### Community 15 - "/code-review-multi-axis — Principal-Engineer Review, Pre-PR and Post-PR"
Cohesion: 0.07
Nodes (27): 1. Pin the fixed point, 2. Identify the spec source, 3. Identify the standards sources, 4. Spawn both sub-agents in parallel, 5. Aggregate, Pre-PR mode — two-axis local review, Process, Why two axes (+19 more)

### Community 16 - "concise-reporting Skill"
Cohesion: 0.50
Nodes (4): concise-reporting README, Reporting Mode (ultra-concise), concise-reporting Skill, Writing Mode (full verbosity)

### Community 17 - "templates/site.js"
Cohesion: 0.09
Nodes (28): addCopyButtons(), catClass(), categories, categoryCountEl, changeList, changes, copyText(), drawer (+20 more)

### Community 18 - "Part 2 — `skill-sync` utility"
Cohesion: 0.07
Nodes (26): Body outline, Build mode (skill-name omitted), Catalog entries added in this PR, Category, CLI, Cross-cutting concerns, Delivery order, Dependencies (+18 more)

### Community 19 - "gh-repo-mirror — Reference"
Cohesion: 0.07
Nodes (25): Bootstrapping a starter skill (--bootstrap-skill), Branch protection PUT, Creating the new repo, DNS CNAME (--cname-provider), Finding the right org, gh-repo-mirror — Reference, HTTPS enforcement — async cert, Mirroring access: teams + direct collaborators (default-on, `--no-mirror-access` to skip) (+17 more)

### Community 20 - "code-review-multi-axis — Reference"
Cohesion: 0.08
Nodes (26): 10. Scope discipline, 11. Data migration safety, 1. Correctness, 2. Design / architecture, 3. Security, 4. Reliability, 5. Performance, 6. Testing (+18 more)

### Community 21 - "The 10-step flow"
Cohesion: 0.08
Nodes (23): Dedup hit, Edge cases, Inputs, Length guard, No-categories.yml, Overview, Step 10 — Report + loop, Step 1 — Detect inputs (+15 more)

### Community 22 - "PRD template"
Cohesion: 0.25
Nodes (8): Further Notes, Implementation Decisions, Out of Scope, PRD template, Problem Statement, Solution, Testing Decisions, User Stories

### Community 23 - "grill-summary"
Cohesion: 0.11
Nodes (17): grill-summary, Install as Agent Skill, License, Manual Installation, Output and Verification, Usage, What It Does, 1. Find the right grill (+9 more)

### Community 24 - "docs-from-prs"
Cohesion: 0.12
Nodes (16): Alignment and layout, Constraints, docs-from-prs, Grammar and prose, HTML-specific (`docs/index.html`), Inputs, Step 1 — Survey, Step 2 — Classify each PR (+8 more)

### Community 25 - "docs-from-prs"
Cohesion: 0.12
Nodes (16): Alignment and layout, Constraints, docs-from-prs, Grammar and prose, HTML-specific (when editing landing pages), Inputs, Step 1 — Survey, Step 2 — Classify each PR (+8 more)

### Community 26 - "docs-from-prs"
Cohesion: 0.12
Nodes (16): Alignment and layout, Constraints, docs-from-prs, Grammar and prose, HTML-specific (when editing landing pages), Inputs, Step 1 — Survey, Step 2 — Classify each PR (+8 more)

### Community 27 - "Process"
Cohesion: 0.12
Nodes (16): 0. Ask for grill depth (before grilling, after loading context), 1. Load context, 2. Interview relentlessly, 3. Challenge against the glossary, 4. Sharpen fuzzy language, 5. Stress-test with concrete scenarios, 6. Cross-reference with code, 7. Flag new terms — do not write (+8 more)

### Community 28 - "/resume-tailoring — Job-Specific Resume Workflow"
Cohesion: 0.12
Nodes (16): Checkpoints & User Control, Edge Cases, Multi-Job Mode, Phase 0 — Library build (always first), Phase 1 — Research, Phase 2.5 — Experience discovery (optional, offered when gaps found), Phase 2 — Template, Phase 3 — Assembly (match + score) (+8 more)

### Community 29 - "/session-feedback — Distill a session, and recall it deliberately"
Cohesion: 0.12
Nodes (15): 1. Scan, 2. Classify into three buckets, 3. Emit the file, 4. Update memory index, Idempotency, Quality bar, Quick start, Recall mode workflow (+7 more)

### Community 30 - "Matching Strategies"
Cohesion: 0.12
Nodes (15): Adjacent (20%), Confidence Bands, Direct Match (40%), Gap Handling (<60% on a must-have), Impact (10%), Matching Strategies, Reframing Strategies, Role Consolidation (Phase 2) (+7 more)

### Community 31 - "/resume-tailoring — Job-Specific Resume Workflow"
Cohesion: 0.12
Nodes (16): Checkpoints & User Control, Edge Cases, Multi-Job Mode, Phase 0 — Library build (always first), Phase 1 — Research, Phase 2.5 — Experience discovery (optional, offered when gaps found), Phase 2 — Template, Phase 3 — Assembly (match + score) (+8 more)

### Community 32 - "GitHub Pages — Neo-Brutalist"
Cohesion: 0.13
Nodes (14): Common Mistakes, Core Pattern, Enable Pages, GitHub Pages — Neo-Brutalist, Implementation, Manual scaffold, One-shot scaffold, Overview (+6 more)

### Community 33 - "Process"
Cohesion: 0.14
Nodes (13): 1. Detect structure, 2. Extract domain language, 3. Extract relationships, 4. Seed ADRs, 5. Write files, 6. Output summary, Companion skills, Mode (+5 more)

### Community 34 - "resume-session-handoff"
Cohesion: 0.14
Nodes (13): Install as Agent Skill, License, Manual Installation, Pair with `/session-handoff`, Preflight checks, Related Skills, resume-session-handoff, Usage (+5 more)

### Community 35 - "/leadership-update — Outcome-First Status Updates"
Cohesion: 0.15
Nodes (12): 1. Verbal / standup version (default), 2. Slack/chat-ready short version, 3. Email version, 4. Written status doc section, Anti-patterns to refuse, Core principles (non-negotiable), Edge cases, Invocation behavior — auto-detect (+4 more)

### Community 36 - "resume-tailoring"
Cohesion: 0.15
Nodes (12): Canonical Trigger, Files, Flags, Install, License, Manual Installation, Outputs, Prerequisites (+4 more)

### Community 37 - "session-handoff"
Cohesion: 0.15
Nodes (12): Document layout, Install as Agent Skill, License, Lifecycle, Manual Installation, Pair with `/resume-session-handoff`, Related Skills, session-handoff (+4 more)

### Community 38 - "Workflow"
Cohesion: 0.15
Nodes (12): 1. Explore repo state, 2. Present findings and ask 3 decisions sequentially, 3. Confirm drafts before writing, 4. Write/update files, 5. Done message, Assumptions, Common mistakes, Decision 1 — Agent instruction surface (+4 more)

### Community 39 - "Steps"
Cohesion: 0.15
Nodes (12): 1. Detect package manager, 2. Install dependencies, 3. Initialize Husky, 4. Create `.husky/pre-commit`, 5. Create `.lintstagedrc`, 6. Create `.prettierrc` (only if missing), 7. Verify, 8. Commit (+4 more)

### Community 40 - "/skill-sync — Sync or Build at-skills Skills From a Source Path"
Cohesion: 0.17
Nodes (11): Build mode, Dispatch Logic, Examples, Failure Recovery, Output Files, Preconditions, Quick Start, /skill-sync — Sync or Build at-skills Skills From a Source Path (+3 more)

### Community 41 - "AI PRD Additional Sections"
Cohesion: 0.18
Nodes (10): 10 Principles for AI Products, AI Constraints, AI Evaluation Plan, AI Feature PRDs — Full Guide, AI PRD Additional Sections, AI PRD Template Addition, Behavior Specification (Required for AI), Edge Case Handling (+2 more)

### Community 42 - "Skills Catalog README"
Cohesion: 0.18
Nodes (11): Skills Catalog README, Category: Agent Behavior, Category: AI Agent, Category: Engineering, Category: Product Management, Category: Project Management, Category: UX Design, Compatible Agents List (+3 more)

### Community 43 - "Multi-Job Workflow"
Cohesion: 0.18
Nodes (10): Failure Modes, Incremental Additions, Multi-Job Workflow, Phase 0 — Intake & Batch Init, Phase 1 — Aggregate Gap Analysis, Phase 2 — Shared Discovery, Phase 3 — Per-Job Processing, Phase 4 — Batch Finalization (+2 more)

### Community 44 - "/faq — Answer a Question and Record It in the Repo FAQ"
Cohesion: 0.20
Nodes (9): Common mistakes, /faq — Answer a Question and Record It in the Repo FAQ, Inputs, Rules, Step 1 — Locate the FAQ document, Step 2 — Detect structure and check for an existing entry, Step 3 — Answer from source of truth, Step 4 — Write the entry (+1 more)

### Community 45 - "Step-by-Step Workflow"
Cohesion: 0.20
Nodes (9): Full PRD Workflow — 7-Step Process, Step-by-Step Workflow, Workflow Step 1: Gather Context (10 min), Workflow Step 2: Generate First Draft (5 min), Workflow Step 3: Enhance Each Section (30-60 min), Workflow Step 4: Multi-Perspective Review (15 min), Workflow Step 5: Human Review, Workflow Step 6: Refine & Ship (30 min) (+1 more)

### Community 46 - "Branching Questions"
Cohesion: 0.20
Nodes (9): Branching Questions, Capture Template, Example Flow, Handing Off, Multi-Job Leverage Prefix, Pattern A — Technical Skill Gap, Pattern B — Soft Skill / Experience Gap, Pattern C — Recent Work Probe (+1 more)

### Community 47 - "domain-grill"
Cohesion: 0.22
Nodes (8): Companion skills, domain-grill, Grill depth, Install, License, Manual Installation, Scope, Usage

### Community 48 - "session-feedback"
Cohesion: 0.22
Nodes (8): Install, License, Manual Installation, Output, session-feedback, Three buckets, Two modes, Usage

### Community 49 - "Session Handoff"
Cohesion: 0.22
Nodes (7): Handoff document template, Companion skill, Document structure, Rules, Session Handoff, When NOT to use, Workflow

### Community 50 - "setup-amit-skills"
Cohesion: 0.22
Nodes (8): Example triggers, Install, License, Manual Installation, setup-amit-skills, What it does, When to use, Workflow summary

### Community 51 - "Grill Summary Behavioral Cases"
Cohesion: 0.12
Nodes (14): A — Wayfinder and mixed answers, B — Automatic handoff, standalone, C — Missing map, conflicting source instruction, D — Ambiguous grill, E — No pending decisions, F — Grouping without dropping decisions, G — Conflicting map and ambiguous identity, Grill Summary Behavioral Cases (+6 more)

### Community 52 - "docs-from-prs"
Cohesion: 0.25
Nodes (7): docs-from-prs, Install as Agent Skill, License, Manual Installation, Usage, What It Does, When to Use

### Community 53 - "faq"
Cohesion: 0.25
Nodes (7): faq, Install as Agent Skill, License, Manual Installation, Usage, What It Does, When to Use

### Community 54 - "skill-sync"
Cohesion: 0.25
Nodes (7): Install, License, Manual Installation, skill-sync, Usage, What It Does, When to Use

### Community 55 - "Process"
Cohesion: 0.25
Nodes (7): 1. Pin the fixed point, 2. Identify the spec source, 3. Identify the standards sources, 4. Spawn both sub-agents in parallel, 5. Aggregate, Process, Why two axes

### Community 56 - "ADR Format"
Cohesion: 0.29
Nodes (6): ADR Format, Numbering, Optional sections, Template, What qualifies, When to create an ADR (during a domain-grill session)

### Community 57 - "gh-repo-mirror"
Cohesion: 0.29
Nodes (6): gh-repo-mirror, Install, License, Manual Installation, Source, Usage

### Community 58 - "leadership-update"
Cohesion: 0.29
Nodes (6): Install, leadership-update, License, Manual Installation, Source, Usage

### Community 59 - "ADR Format"
Cohesion: 0.29
Nodes (6): ADR Format, Numbering, Optional sections, Template, What qualifies, When to create an ADR

### Community 60 - "repo-context-scan"
Cohesion: 0.29
Nodes (6): Companion skill, Install, License, Manual Installation, repo-context-scan, Usage

### Community 61 - "Research Prompts"
Cohesion: 0.29
Nodes (6): 1. JD Parsing, 2. Company Research, 3. Role Benchmarking, 4. Success Profile Synthesis, 5. Graceful Degradation, Research Prompts

### Community 62 - "setup-pre-commit"
Cohesion: 0.29
Nodes (6): Install, License, Manual Installation, setup-pre-commit, Usage, When to use

### Community 63 - "two-axis-review"
Cohesion: 0.29
Nodes (6): Install, License, Manual Installation, two-axis-review, Usage, When to use

### Community 64 - "Wisdom Capture — Reference"
Cohesion: 0.29
Nodes (6): Categorization output schema, Commit message body limits, Engine-specific notes, Frontmatter rendering rules, Push policy state, Wisdom Capture — Reference

### Community 65 - "grill-me"
Cohesion: 0.33
Nodes (5): grill-me, Install, License, Manual Installation, Usage

### Community 66 - "write-a-skill"
Cohesion: 0.33
Nodes (5): Install, License, Manual Installation, Usage, write-a-skill

### Community 67 - "Grill Summary Design"
Cohesion: 0.33
Nodes (5): Alternatives considered, Approved scope, Design, Grill Summary Design, Verification

### Community 68 - "E2E Package Scaffold"
Cohesion: 0.33
Nodes (5): 1.1 Create the package, 1.2 Playwright config essentials, 1.3 Seed user fixture pattern, 1.4 Add pnpm shortcuts to root package.json, E2E Package Scaffold

### Community 69 - "Document Templates"
Cohesion: 0.33
Nodes (5): ADR skeleton (Step 5) — `outputs/decisions/ADR-NNN-{decision-slug}.md`, one per technology decision, Document Templates, Panel synthesis skeleton (Step 8) — `outputs/specs/{SPEC-ID}-panel-review.md`, SPEC skeleton (Step 4) — `outputs/specs/SPEC-{CODE}-NN-{feature-slug}.md`, TDD skeleton (Step 3) — `outputs/tdds/TDD-NNN-{feature-slug}.md`

### Community 70 - "gh-pages-neo-brutalist"
Cohesion: 0.33
Nodes (5): gh-pages-neo-brutalist, Install, See, Use, What it ships

### Community 71 - "Resume Session Handoff"
Cohesion: 0.33
Nodes (5): Companion skill, Resume Session Handoff, Rules, When NOT to use, Workflow

### Community 72 - "CONTEXT.md"
Cohesion: 0.33
Nodes (5): CONTEXT.md, Example dialogue, Flagged ambiguities, Language, Relationships

### Community 73 - "wisdom-capture"
Cohesion: 0.33
Nodes (5): Install, License, Manual Installation, Usage, wisdom-capture

### Community 74 - "CONTEXT.md Format (read reference)"
Cohesion: 0.40
Nodes (4): CONTEXT.md Format (read reference), Reading rules, Single vs multi-context repos, Structure

### Community 75 - "Report & Fix-Plan Templates"
Cohesion: 0.40
Nodes (4): Diagnostic report skeleton (Phase 5), Fix-plan epic header (Phase 6.1), Fix-plan task template, one per bug (Phase 6.2), Report & Fix-Plan Templates

### Community 76 - "git-guardrails-claude-code Skill"
Cohesion: 0.60
Nodes (5): block-dangerous-git.sh Script, Blocked Git Commands (push, reset --hard, clean -f, etc.), PreToolUse Hook Mechanism, .claude/settings.json Hooks Config, git-guardrails-claude-code Skill

### Community 77 - "CONTEXT.md Format"
Cohesion: 0.40
Nodes (4): CONTEXT.md Format, Rules, Single vs multi-context repos, Structure

### Community 78 - "Context Map"
Cohesion: 0.40
Nodes (4): Context Map, Contexts, Ownership notes, Relationships

### Community 80 - "index.md"
Cohesion: 0.50
Nodes (3): Quick paths, What this is, Why

### Community 81 - "ADR format"
Cohesion: 0.50
Nodes (3): ADR format, Create an ADR only when all three are true, Template

### Community 82 - "amit-t/skills conventions"
Cohesion: 0.50
Nodes (3): Agent instruction files, amit-t/skills conventions, Downstream skill expectations

### Community 83 - "amit-t/skills category vocabulary"
Cohesion: 0.50
Nodes (3): amit-t/skills category vocabulary, Catalog sync reminder, Skill file convention

### Community 84 - "Fixture: ambiguous between writing + leadership"
Cohesion: 0.50
Nodes (3): Expected categorization output, Fixture: ambiguous between writing + leadership, Input

### Community 85 - "Fixture: high-confidence engineering snippet"
Cohesion: 0.50
Nodes (3): Expected categorization output, Fixture: high-confidence engineering snippet, Input

### Community 86 - "Fixture: forces a new-bucket proposal"
Cohesion: 0.50
Nodes (3): Expected categorization output, Fixture: forces a new-bucket proposal, Input

### Community 96 - "design-review Skill"
Cohesion: 0.20
Nodes (10): Multi-Agent Review Pattern, design-review — Reference, Review Output Format, Step 7: Design Review, Design Review Output Markdown Template, design-review Skill, Parallel Task Execution (single-message), prd-review-panel Skill (+2 more)

### Community 97 - "design-draft Skill (Full UXD Workflow)"
Cohesion: 0.18
Nodes (11): Resume From Step (--from), design-draft Skill (Full UXD Workflow), Step 0: Find Approved PRD, Step 1: Load PRD Context, Step 3: User Flow, Step 4: Wireframes, Step 5: Design System, Step 6: Hi-Fidelity Screens (+3 more)

### Community 98 - "Map: A Calm Ordering Rollout"
Cohesion: 0.22
Nodes (7): Answer key template — not submitted, Auto-answered, Rollout Decision Grill, Destination, Map: A Calm Ordering Rollout, Relevant decisions and work, Unrelated branch

### Community 99 - "write-a-prd Skill"
Cohesion: 0.33
Nodes (6): 5-Section Interview (Product/Users/Visual/Constraints/Success), Deep Module Concept, PRD Submitted as GitHub Issue, PRD Template (Problem, Solution, User Stories, Decisions), write-a-prd Skill, User Story Format (As an actor, I want...)

### Community 100 - "prd-to-plan Skill"
Cohesion: 0.29
Nodes (6): Plan File Template, Durable Architectural Decisions, Rationale: Prefer many thin slices over few thick, prd-to-plan Skill, Plan Markdown Template, Tracer Bullet Vertical Slices Concept

### Community 101 - "design-interview Skill"
Cohesion: 0.33
Nodes (6): Step 2: Design Interview, Design Brief Output Template, Context Routing (PRDs, Personas, Brand), Quick Mode (--quick, 5 questions), Rationale: Screen quality depends on context gathering, design-interview Skill

### Community 102 - "Resume and Status"
Cohesion: 0.40
Nodes (4): design-draft — Reference, `--from` flag values, `--list` output, Resume and Status

## Knowledge Gaps
- **816 isolated node(s):** `skills`, `changes`, `state`, `searchInput`, `filtersEl` (+811 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 886 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `write-a-prd Skill` connect `write-a-prd Skill` to `design-review Skill`, `prd-to-plan Skill`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `design-review Skill` connect `design-review Skill` to `7 Reviewer Sub-Agents (Eng/Design/Exec/Legal/UXR/Skeptic/Customer)`, `design-interview Skill`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **Why does `code-review-multi-axis — Reference` connect `code-review-multi-axis — Reference` to `/code-review-multi-axis — Principal-Engineer Review, Pre-PR and Post-PR`?**
  _High betweenness centrality (0.002) - this node is a cross-community bridge._
- **What connects `skills`, `changes`, `state` to the rest of the system?**
  _816 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `TDD Skill (red-green-refactor)` be split into smaller, more focused modules?**
  _Cohesion score 0.09782608695652174 - nodes in this community are weakly interconnected._
- **Should `eng-spec Skill` be split into smaller, more focused modules?**
  _Cohesion score 0.05855855855855856 - nodes in this community are weakly interconnected._
- **Should `PRD Draft Skill` be split into smaller, more focused modules?**
  _Cohesion score 0.09420289855072464 - nodes in this community are weakly interconnected._