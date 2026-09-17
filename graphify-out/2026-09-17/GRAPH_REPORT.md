# Graph Report - at-skills  (2026-09-17)

## Corpus Check
- 202 files · ~130,329 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 2206 nodes · 2763 edges · 191 communities (171 shown, 18 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 170 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `aaca29c5`
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
- Rubric
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
- PromoteFixture
- retire_review.py
- validate_candidate.py
- filter_sessions.py
- build_shortlist
- DevinAdapter
- CopilotAdapter
- properties
- properties
- properties
- Turn
- CodexAdapter
- render_skill.py
- type
- ClaudeCodeAdapter
- properties
- copilot.py
- render_skill_md
- properties
- properties
- properties
- properties
- detect
- session-to-skill-extractor
- properties
- codex.py
- GenericAdapter
- Session-to-Skill Extractor
- description
- properties
- provenance
- test_render.py
- _output_ok
- generic.py
- code-review-multi-axis — Reference
- Branching Questions
- evidence
- items
- promote.py
- render_candidate
- Writing Skills
- Process
- code-review-multi-axis
- PRD Template (templates/prd-template.md)
- Precision Mode Skill
- Workflow
- candidate.schema.json
- registry.schema.json
- items
- session.schema.json
- yaml_scalar
- Failure Modes — Diagnosing a Skill
- Host Notes — Detection, Session Sources, Skill Install Locations, Scheduling
- additionalProperties
- properties
- test_load_sessions_cli.py
- resume-tailoring.skill
- Research Prompts
- Scoring Formula
- Adapter
- Reframing Strategies
- Rubric — Stage 2: Procedure Identification
- TestRecommendedActionDistinctFindings
- Principles (book-grounded)
- Part 3: AI Feature PRDs
- name
- version
- version
- stats
- title_case_name
- Anti-Patterns — Spec A7
- until
- updated_at
- quality-criteria.md
- detect_host.sh script
- _bullets
- jest-to-vitest-migration/SKILL.md
- dedup_prescreen.py
- load_fixture
- test_validator.py
- load_config
- validate
- append_usage
- TestSuppressedTaskType
- _check_suppression
- .test_vague_json_has_at_least_two_errors
- .test_single_session_without_review_flag_fails

## God Nodes (most connected - your core abstractions)
1. `validate()` - 30 edges
2. `DevinAdapter` - 27 edges
3. `CopilotAdapter` - 26 edges
4. `Turn` - 24 edges
5. `Session` - 23 edges
6. `render_skill_md()` - 23 edges
7. `load_fixture()` - 22 edges
8. `load_fixture()` - 22 edges
9. `blacklist()` - 21 edges
10. `load_config()` - 20 edges

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

## Communities (191 total, 18 thin omitted)

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
Cohesion: 0.20
Nodes (12): Context Routing Logic, $1-$10-$100 Prototype Rule, Part 2: Full PRD Workflow (7 steps), Output Quality Self-Check, prd-draft README, PRD Draft Skill, Stage-Specific Length Guidance, Step 0: Feature Context Check (+4 more)

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
Cohesion: 0.20
Nodes (8): Skill Authoring Process (gather, draft, review), write-a-skill README, Review Checklist, Write-a-Skill Skill, Skill Folder Structure, SKILL.md Template, When to Add Scripts, When to Split Files

### Community 8 - "Multi-Job Workflow"
Cohesion: 0.20
Nodes (10): Failure Modes, Incremental Additions, Multi-Job Workflow, Phase 0 — Intake & Batch Init, Phase 1 — Aggregate Gap Analysis, Phase 2 — Shared Discovery, Phase 3 — Per-Job Processing, Phase 4 — Batch Finalization (+2 more)

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
Cohesion: 0.18
Nodes (11): /code-review-multi-axis — Principal-Engineer Review, Pre-PR and Post-PR, Config, One-time identity ack, Phase 1 — Approval loop, Phase 1 — Deep review, Phase 1 — Pre-check (3 arms, all gated by `--force`), Phase 2 — Submit, Preflight (fail-fast) (+3 more)

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

### Community 20 - "Rubric"
Cohesion: 0.17
Nodes (12): 10. Scope discipline, 11. Data migration safety, 1. Correctness, 2. Design / architecture, 3. Security, 4. Reliability, 5. Performance, 6. Testing (+4 more)

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
Cohesion: 0.25
Nodes (8): Checkpoints & User Control, Edge Cases, Multi-Job Mode, Quick Start, References, /resume-tailoring — Job-Specific Resume Workflow, Sub-Skills Used, Truthfulness Rules (non-negotiable)

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

### Community 103 - "PromoteFixture"
Cohesion: 0.12
Nodes (17): cmd_promote(), Dispatch accept/edit/reject. Raises PromoteError for any CLI-facing failure., load_fixture(), PromoteFixture, Fix round 1, item 2b: a malformed candidate.json in the queue folder must not…, Sets up a tempdir with queue/skill-dir/registry and a rendered candidate., 3-session candidate + accept -> provisional (reviewer-accept, below 20)., 30-session candidate + accept -> validated. (+9 more)

### Community 104 - "retire_review.py"
Cohesion: 0.07
Nodes (37): build_report(), compute_skill_stats(), _conflicts_block(), find_conflicts(), _jaccard(), _library_size_block(), load_usage_rows(), main() (+29 more)

### Community 105 - "validate_candidate.py"
Cohesion: 0.12
Nodes (23): _anti_patterns_path(), _as_dict(), _as_list(), _check_decision_points(), _check_edge_cases(), _check_prose_blacklist_and_checkable(), _check_steps(), _check_trigger() (+15 more)

### Community 106 - "filter_sessions.py"
Cohesion: 0.06
Nodes (39): _evaluate(), _filter_cfg(), filter_sessions(), _has_novelty(), _has_structured_output(), _load_sessions(), main(), parse_args() (+31 more)

### Community 107 - "build_shortlist"
Cohesion: 0.12
Nodes (14): build_shortlist(), Score candidate vs every existing SKILL.md + registry entry; return entries…, load_fixture(), Item G: --skill-dirs omitted must fall back to config skill_dirs (config flows…, E3-5: good.json vs a near-identical fixture SKILL.md scores >= 0.3 and is…, An unrelated SKILL.md (different domain entirely) produces an empty shortlist., Nonexistent skill dirs and a missing registry are skipped silently, no crash., A registry skill entry (name + trigger_description) participates in scoring too. (+6 more)

### Community 108 - "DevinAdapter"
Cohesion: 0.09
Nodes (9): DevinAdapter, Paste/export-first: devin_session_files config points straight at JSON files., Binding Task-2 contract: locate() returns refs newest first., API path is mocked -- no real network calls in tests., TestDevinAdapterLoadFromFile, TestDevinAdapterLocateNoSource, TestDevinAdapterLocateOrdering, TestDevinAdapterLocateViaApi (+1 more)

### Community 109 - "CopilotAdapter"
Cohesion: 0.09
Nodes (12): CopilotAdapter, _make_sessions_db(), Binding Task-2 contract: locate() returns refs newest first., rows: list of (id, title, session_type, model, created_at) tuples., ~/.copilot/session-state/<id>/ per-session dir, file names UNVERIFIED (best-…, Legacy history-session-state/<id>/state.json shape (host-notes: schema…, sessions table in session-store.db/data.db is metadata-only -- no message…, TestCopilotAdapterDbMetadataOnly (+4 more)

### Community 110 - "properties"
Cohesion: 0.07
Nodes (29): q1, q2, q3, q4, q5, rubric, total, maximum (+21 more)

### Community 111 - "properties"
Cohesion: 0.08
Nodes (26): description, type, type, type, type, type, properties, type (+18 more)

### Community 112 - "properties"
Cohesion: 0.08
Nodes (25): description, type, description, type, description, type, description, type (+17 more)

### Community 113 - "Turn"
Cohesion: 0.11
Nodes (23): compute_stats(), detect_outcome_signals(), Normalized session model: Turn/Session dataclasses, stats, and outcome signals.…, Scan user turns for positive/negative acks; scan tool calls for a completion…, turn_count, assistant_turns, tool_call_count, distinct_tools, char_count,…, Session, Turn, _extract_content() (+15 more)

### Community 114 - "CodexAdapter"
Cohesion: 0.12
Nodes (4): CodexAdapter, TestCodexAdapterLoad, TestCodexAdapterLocate, TestCodexAdapterMalformedLines

### Community 115 - "render_skill.py"
Cohesion: 0.12
Nodes (19): _decision_points_block(), _dedup_findings_block(), _evidence_block(), _load_extra_dedup_findings(), main(), _numbered_steps(), parse_args(), _quality_criteria_block() (+11 more)

### Community 116 - "type"
Cohesion: 0.12
Nodes (21): items, type, items, additionalProperties, properties, type, items, type (+13 more)

### Community 117 - "ClaudeCodeAdapter"
Cohesion: 0.10
Nodes (7): ClaudeCodeAdapter, Item E, discriminating case: retry_count only credits a retry when the tool…, Item E: tool_results[].name must be the real tool name (looked up via…, TestClaudeCodeAdapterLoad, TestClaudeCodeAdapterLocate, TestClaudeCodeAdapterMalformedLines, TestClaudeCodeAdapterRetryCountNeedsRealToolNames

### Community 118 - "properties"
Cohesion: 0.11
Nodes (18): description, type, type, type, type, properties, at, candidates (+10 more)

### Community 119 - "copilot.py"
Cohesion: 0.23
Nodes (9): _find_message_list(), _message_to_turn(), _messages_to_turns(), Copilot (GitHub Copilot CLI/chat) adapter. Probe order under `~/.copilot`…, Best-effort role normalization. # unverified: exact role vocabulary Copilot…, First non-empty list under a common message-list key, in priority order., _role_from_raw(), _session_from_message_obj() (+1 more)

### Community 120 - "render_skill_md"
Cohesion: 0.24
Nodes (6): Build the rendered SKILL.md text (spec D3) for a D2 candidate dict., render_skill_md(), load_fixture(), Fix round 1, item 1: a description containing ': ' must not corrupt the…, TestRenderSkillMdBodySections, TestRenderSkillMdFrontmatterYamlSafety

### Community 121 - "properties"
Cohesion: 0.12
Nodes (16): properties, description, type, type, description, type, created_at, human_edited (+8 more)

### Community 122 - "properties"
Cohesion: 0.12
Nodes (16): type, description, type, enum, type, properties, cwd, ended_at (+8 more)

### Community 123 - "properties"
Cohesion: 0.13
Nodes (15): type, type, type, type, assistant_turns, char_count, distinct_tools, error_count (+7 more)

### Community 124 - "properties"
Cohesion: 0.13
Nodes (15): type, type, additionalProperties, properties, required, type, explicit_user_rating, notes (+7 more)

### Community 125 - "detect"
Cohesion: 0.22
Nodes (7): detect(), _enumerate_session_sources(), main(), Detect which agent host is running (or produced session logs on this machine).…, Return every known session store that exists under `home`., Detect the host agent runtime. env: mapping to read env vars from (defaults to…, TestDetect

### Community 126 - "session-to-skill-extractor"
Cohesion: 0.14
Nodes (13): Configuration, Install as Agent Skill, License, Manual Installation, Owner decisions defaulted, Related Skills, Scheduled use, session-to-skill-extractor (+5 more)

### Community 127 - "properties"
Cohesion: 0.14
Nodes (14): type, type, type, clearly_articulable, measurable_quality, non_obvious, quality_criteria, recurrence (+6 more)

### Community 128 - "codex.py"
Cohesion: 0.20
Nodes (8): _current_assistant_turn(), _extract_message_text(), _input_summary(), Codex adapter: loads local Codex CLI rollout JSONL files. Each Codex session is…, The last turn if it's an assistant turn, so sequential tool calls with no…, Join input_text/output_text blocks from a message payload's content list., arguments (function_call, a JSON string) or input (custom_tool_call), first 200…, TestInputSummary

### Community 129 - "GenericAdapter"
Cohesion: 0.24
Nodes (6): GenericAdapter, Malformed input must never raise; it always degrades to one user turn., TestGenericAdapterFallback, TestGenericAdapterJsonl, TestGenericAdapterPlainText, _write_temp()

### Community 130 - "Session-to-Skill Extractor"
Cohesion: 0.14
Nodes (13): Feedback commands, Guardrails, Scheduled use, Session-to-Skill Extractor, Step 0 — Detect host, Step 1 — Locate and filter sessions, Step 2 — Identify, Step 3 — Cluster and gate (+5 more)

### Community 131 - "description"
Cohesion: 0.15
Nodes (13): description, maxLength, type, description, signals, trigger, description, items (+5 more)

### Community 132 - "properties"
Cohesion: 0.15
Nodes (13): properties, role, text, timestamp, tool_calls, tool_results, enum, type (+5 more)

### Community 133 - "provenance"
Cohesion: 0.17
Nodes (12): description, type, type, type, extracted_at, extracted_by_host, extractor_version, provenance (+4 more)

### Community 134 - "test_render.py"
Cohesion: 0.20
Nodes (8): h2_headings(), parse_frontmatter(), Minimal 'key: value' frontmatter parser (top-level keys only, quotes stripped)., Brief Step 1: the rendered SKILL.md's H2 headings appear in exact spec order., TestRenderSkillCli, TestRenderSkillMdFrontmatter, TestRenderSkillMdH2Sequence, TestRenderSkillMdNoDollarResidue

### Community 135 - "_output_ok"
Cohesion: 0.27
Nodes (5): _maybe_json_object(), _output_ok(), Parse text as JSON; return it only if the result is itself a dict, else None., Best-effort success heuristic: not a nonzero exit_code, not an ERROR-prefixed…, TestOutputOkHeuristic

### Community 136 - "generic.py"
Cohesion: 0.19
Nodes (10): parse_transcript(), Generic adapter: loads plain-text or JSONL session transcripts from file paths.…, One JSON object per non-blank line, each with a 'role' key. None if not JSONL., Blank-line-separated blocks, each prefixed 'User:' or 'Assistant:'. None if not…, Parse text as JSONL, else blank-line User:/Assistant: blocks, else one user…, _try_jsonl(), _try_plain_text(), Adapter registry: maps host name -> Adapter subclass. Each adapter module is… (+2 more)

### Community 137 - "code-review-multi-axis — Reference"
Cohesion: 0.20
Nodes (10): code-review-multi-axis — Reference, Comment layout (Phase 1 verb loop), Config schema, Error handling, gh commands, Identity ack, Pre-check thresholds (config-driven), Re-review dedupe (+2 more)

### Community 138 - "Branching Questions"
Cohesion: 0.22
Nodes (9): Branching Questions, Capture Template, Example Flow, Handing Off, Multi-Job Leverage Prefix, Pattern A — Technical Skill Gap, Pattern B — Soft Skill / Experience Gap, Pattern C — Recent Work Probe (+1 more)

### Community 139 - "evidence"
Cohesion: 0.22
Nodes (9): additionalProperties, properties, required, type, evidence, sessions, supporting_sessions, type (+1 more)

### Community 140 - "items"
Cohesion: 0.33
Nodes (9): items, additionalProperties, required, type, turns, items, items, items (+1 more)

### Community 141 - "promote.py"
Cohesion: 0.14
Nodes (24): Exception, _load_or_init_registry(), main(), parse_args(), _patch_status_line(), _promote_accept_or_edit(), _promote_reject(), PromoteError (+16 more)

### Community 142 - "render_candidate"
Cohesion: 0.22
Nodes (5): Render one candidate into…, render_candidate(), Fix round 1, item 2a: a candidate JSON missing candidate_id must not crash with…, TestRenderCandidateWritesFiles, TestRenderSkillCliMissingCandidateId

### Community 143 - "Writing Skills"
Cohesion: 0.25
Nodes (8): Description Requirements, Process, Review Checklist, SKILL.md Template, Skill Structure, When to Add Scripts, When to Split Files, Writing Skills

### Community 144 - "Process"
Cohesion: 0.25
Nodes (8): 1. Pin the fixed point, 2. Identify the spec source, 3. Identify the standards sources, 4. Spawn both sub-agents in parallel, 5. Aggregate, Pre-PR mode — two-axis local review, Process, Why two axes

### Community 145 - "code-review-multi-axis"
Cohesion: 0.25
Nodes (8): code-review-multi-axis, Configuration, Install, License, Manual Installation, Requirements, Scope (v1), Usage

### Community 146 - "PRD Template (templates/prd-template.md)"
Cohesion: 0.25
Nodes (8): PRD Hypothesis Section (If/Then/Because), PRD Non-Goals, PRD Template (templates/prd-template.md), Risks and Recovery Table, PRD Rollout Plan, Solution Overview (non-AI), PRD Strategic Fit + Impact Sizing, PRD Success Metrics + STEDII

### Community 147 - "Precision Mode Skill"
Cohesion: 0.29
Nodes (8): Calibration Examples, What Precision Mode Does NOT Mean, Derived from concise-reporting, 10 Output Rules (lead with answer, no filler, etc.), Prime Directive: Maximize Information Density, precision-mode README, Precision Mode Skill, Description Requirements (1024 chars, triggers)

### Community 148 - "Workflow"
Cohesion: 0.25
Nodes (8): Phase 0 — Library build (always first), Phase 1 — Research, Phase 2.5 — Experience discovery (optional, offered when gaps found), Phase 2 — Template, Phase 3 — Assembly (match + score), Phase 4 — Generation, Phase 5 — Save + learn (conditional), Workflow

### Community 149 - "candidate.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, description, $id, required, $schema, title, type

### Community 150 - "registry.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, description, $id, required, $schema, title, type

### Community 151 - "items"
Cohesion: 0.32
Nodes (8): additionalProperties, required, type, supporting_sessions, items, items, type, items

### Community 152 - "session.schema.json"
Cohesion: 0.25
Nodes (7): additionalProperties, description, $id, required, $schema, title, type

### Community 153 - "yaml_scalar"
Cohesion: 0.36
Nodes (4): Render value as a YAML frontmatter scalar. Returns the raw string unquoted only…, yaml_scalar(), Fix round 1, item 1: frontmatter scalars must be YAML-safe., TestYamlScalar

### Community 154 - "Failure Modes — Diagnosing a Skill"
Cohesion: 0.25
Nodes (8): Duplication, Failure Modes — Diagnosing a Skill, Negation, No-op, Premature completion, Sediment, Sprawl, Supporting vocabulary

### Community 155 - "Host Notes — Detection, Session Sources, Skill Install Locations, Scheduling"
Cohesion: 0.29
Nodes (6): claude-code, codex, copilot, devin, generic, Host Notes — Detection, Session Sources, Skill Install Locations, Scheduling

### Community 156 - "additionalProperties"
Cohesion: 0.29
Nodes (7): additionalProperties, required, type, skills, additionalProperties, description, type

### Community 157 - "properties"
Cohesion: 0.29
Nodes (7): type, properties, extractor_version, runs, suppressed_task_types, type, type

### Community 158 - "test_load_sessions_cli.py"
Cohesion: 0.22
Nodes (4): Fix A: --paths must work for every adapter, not just generic -- it bypasses…, TestAdaptersRegistry, TestLoadSessionsCliUnknownHost, TestLoadSessionsPathsBypassesLocate

### Community 159 - "resume-tailoring.skill"
Cohesion: 0.33
Nodes (5): Gap Handling (<60% on a must-have), Matching Strategies, resume-tailoring (portable bundle), Role Consolidation (Phase 2), Title Reframing (Phase 2)

### Community 160 - "Research Prompts"
Cohesion: 0.33
Nodes (6): 1. JD Parsing, 2. Company Research, 3. Role Benchmarking, 4. Success Profile Synthesis, 5. Graceful Degradation, Research Prompts

### Community 161 - "Scoring Formula"
Cohesion: 0.33
Nodes (6): Adjacent (20%), Confidence Bands, Direct Match (40%), Impact (10%), Scoring Formula, Transferable (30%)

### Community 162 - "Adapter"
Cohesion: 0.33
Nodes (4): Adapter, Interface every host adapter implements., Return source refs (paths/ids), newest first., Load a single source ref into a Session.

### Community 163 - "Reframing Strategies"
Cohesion: 0.40
Nodes (5): Reframing Strategies, Strategy 1 — Keyword alignment, Strategy 2 — Emphasis shift, Strategy 3 — Abstraction level, Strategy 4 — Scale emphasis

### Community 164 - "Rubric — Stage 2: Procedure Identification"
Cohesion: 0.40
Nodes (4): 0–2 anchor table (spec C5 Stage 2), Flag rule, Rubric — Stage 2: Procedure Identification, The five questions (verbatim, spec A4 Stage 2)

### Community 167 - "Principles (book-grounded)"
Cohesion: 0.50
Nodes (4): A Philosophy of Software Design (Ousterhout), Domain-Driven Design (Evans), Principles (book-grounded), The Pragmatic Programmer (Hunt & Thomas)

### Community 168 - "Part 3: AI Feature PRDs"
Cohesion: 0.50
Nodes (4): 10 Principles for AI Products, AI Behavior Contract, Part 3: AI Feature PRDs, AI Behavior Specification (Good/Bad/Reject)

### Community 169 - "name"
Cohesion: 0.50
Nodes (4): description, pattern, type, name

### Community 170 - "version"
Cohesion: 0.50
Nodes (4): version, description, pattern, type

### Community 171 - "version"
Cohesion: 0.50
Nodes (4): version, description, pattern, type

### Community 172 - "stats"
Cohesion: 0.50
Nodes (4): stats, additionalProperties, required, type

### Community 173 - "title_case_name"
Cohesion: 0.50
Nodes (3): kebab-case skill name -> Title Case with hyphens rendered as spaces., title_case_name(), TestTitleCaseName

### Community 175 - "until"
Cohesion: 0.67
Nodes (3): until, description, type

### Community 176 - "updated_at"
Cohesion: 0.67
Nodes (3): updated_at, description, type

### Community 181 - "dedup_prescreen.py"
Cohesion: 0.15
Nodes (15): _candidate_tokens(), _jaccard(), main(), parse_args(), _parse_frontmatter(), Yield (skill_name, path, tokens) for every registry skills{} entry. A…, Stage 3 dedup pre-screen: cheap Jaccard token-overlap check before any LLM call…, Lowercase, split on non-alnum, drop stopwords and empty strings. Returns a set. (+7 more)

### Community 182 - "load_fixture"
Cohesion: 0.21
Nodes (6): blacklist(), load_fixture(), Item F: every check must type-guard its inputs and collect an error string…, decision_points empty and linear not true must fail (spec C5 Stage 3)., TestEmptyDecisionPointsWithoutLinear, TestMalformedCandidateNeverCrashes

### Community 183 - "test_validator.py"
Cohesion: 0.13
Nodes (8): E3-7: a realistic, well-formed D2 candidate produces no errors., rubric.total must equal q1+...+q5, else validation fails., An unflaggable rubric (e.g. q2=0) must not pass validation., TestGoodCandidatePasses, TestMissingRequiredKeys, TestRubricFlagRule, TestRubricTotalMismatch, TestValidateCandidateCli

### Community 184 - "load_config"
Cohesion: 0.20
Nodes (12): _expand_paths(), main(), parse_args(), CLI: locate and load sessions for one host adapter, writing a sessions+errors…, Expand glob patterns into a deduplicated list of matches, newest first., main(), parse_args(), Feedback loop, part 1 (spec E3-9): record a single usage-outcome report for a… (+4 more)

### Community 185 - "validate"
Cohesion: 0.25
Nodes (8): _check_rubric(), _check_schema_lite(), _check_single_session_review(), Check 7: rubric total == sum(q1..q5); flag rule holds (an unflaggable candidate…, Check 8: evidence.supporting_sessions == 1 => requires_human_review must be…, Run all Stage-3 hard-rule checks against a D2 candidate dict. Returns a list of…, Check 1: required D2 keys present, name pattern, description length., validate()

### Community 186 - "append_usage"
Cohesion: 0.43
Nodes (3): append_usage(), Append {"skill","outcome","note","at"} to F/usage-log.jsonl, creating the…, TestReportUsageAppendsJsonLine

### Community 188 - "_check_suppression"
Cohesion: 0.50
Nodes (4): _check_suppression(), _parse_iso(), Parse an ISO-8601 timestamp, treating a naive datetime as UTC. None on failure., C5 Stage 5 / item B: reject a candidate whose task_type has an unexpired entry…

## Knowledge Gaps
- **1032 isolated node(s):** `skills`, `changes`, `state`, `searchInput`, `filtersEl` (+1027 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 1315 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `load_config()` connect `load_config` to `retire_review.py`, `validate_candidate.py`, `filter_sessions.py`, `promote.py`, `render_candidate`, `render_skill.py`, `dedup_prescreen.py`?**
  _High betweenness centrality (0.014) - this node is a cross-community bridge._
- **Why does `ClaudeCodeAdapter` connect `ClaudeCodeAdapter` to `generic.py`, `Turn`, `Adapter`, `filter_sessions.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Why does `Session` connect `Turn` to `codex.py`, `GenericAdapter`, `Adapter`, `generic.py`, `DevinAdapter`, `CopilotAdapter`, `CodexAdapter`, `ClaudeCodeAdapter`, `copilot.py`?**
  _High betweenness centrality (0.013) - this node is a cross-community bridge._
- **Are the 18 inferred relationships involving `validate()` (e.g. with `.test_empty_decision_points_with_linear_true_passes_that_check()` and `.test_empty_decision_points_without_linear_fails()`) actually correct?**
  _`validate()` has 18 INFERRED edges - model-reasoned connections that need verification._
- **Are the 6 inferred relationships involving `DevinAdapter` (e.g. with `Session` and `TestDevinAdapterLoadFromFile`) actually correct?**
  _`DevinAdapter` has 6 INFERRED edges - model-reasoned connections that need verification._
- **Are the 7 inferred relationships involving `CopilotAdapter` (e.g. with `Session` and `Turn`) actually correct?**
  _`CopilotAdapter` has 7 INFERRED edges - model-reasoned connections that need verification._
- **Are the 5 inferred relationships involving `Turn` (e.g. with `CodexAdapter` and `CopilotAdapter`) actually correct?**
  _`Turn` has 5 INFERRED edges - model-reasoned connections that need verification._