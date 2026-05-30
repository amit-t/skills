# Graph Report - .  (2026-05-30)

## Corpus Check
- 3 files · ~76,176 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 271 nodes · 322 edges · 18 communities detected
- Extraction: 90% EXTRACTED · 10% INFERRED · 0% AMBIGUOUS · INFERRED: 33 edges (avg confidence: 0.8)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- [[_COMMUNITY_Community 0|Community 0]]
- [[_COMMUNITY_Community 1|Community 1]]
- [[_COMMUNITY_Community 2|Community 2]]
- [[_COMMUNITY_Community 3|Community 3]]
- [[_COMMUNITY_Community 4|Community 4]]
- [[_COMMUNITY_Community 5|Community 5]]
- [[_COMMUNITY_Community 6|Community 6]]
- [[_COMMUNITY_Community 7|Community 7]]
- [[_COMMUNITY_Community 8|Community 8]]
- [[_COMMUNITY_Community 9|Community 9]]
- [[_COMMUNITY_Community 10|Community 10]]
- [[_COMMUNITY_Community 11|Community 11]]
- [[_COMMUNITY_Community 12|Community 12]]
- [[_COMMUNITY_Community 13|Community 13]]
- [[_COMMUNITY_Community 14|Community 14]]
- [[_COMMUNITY_Community 15|Community 15]]
- [[_COMMUNITY_Community 16|Community 16]]
- [[_COMMUNITY_Community 17|Community 17]]

## God Nodes (most connected - your core abstractions)
1. `TDD Skill (red-green-refactor)` - 13 edges
2. `design-draft Skill (Full UXD Workflow)` - 13 edges
3. `PRD Draft Skill` - 11 edges
4. `Skills Catalog README` - 11 edges
5. `PMO Status Skill` - 10 edges
6. `eng-spec Skill` - 10 edges
7. `Write-a-Skill Skill` - 9 edges
8. `PRD Template (templates/prd-template.md)` - 9 edges
9. `design-interview Skill` - 9 edges
10. `Changelog` - 8 edges

## Surprising Connections (you probably didn't know these)
- `Write-a-Skill Skill` --semantically_similar_to--> `PRD Draft Skill`  [INFERRED] [semantically similar]
  write-a-skill/SKILL.md → prd-draft/SKILL.md
- `Catalog Sync Rule (Mandatory)` --semantically_similar_to--> `CLAUDE Catalog Sync Rule (Mandatory)`  [INFERRED] [semantically similar]
  AGENTS.md → CLAUDE.md
- `write-a-prd Skill` --semantically_similar_to--> `5-Section Interview (Product/Users/Visual/Constraints/Success)`  [INFERRED] [semantically similar]
  write-a-prd/SKILL.md → design-interview/SKILL.md
- `5-Agent Engineering Panel Review` --semantically_similar_to--> `Review Panel Synthesis File`  [INFERRED] [semantically similar]
  eng-spec/SKILL.md → prd-approve/SKILL.md
- `Verify Through Interface (not external means)` --semantically_similar_to--> `Durable Issues (no file paths or line numbers)`  [INFERRED] [semantically similar]
  tdd/tests.md → qa/SKILL.md

## Hyperedges (group relationships)
- **TDD Red-Green-Refactor Loop Participants** — tdd_planning_step, tdd_tracer_bullet, tdd_red_green_refactor, tdd_refactor_step, tdd_cycle_checklist [EXTRACTED 0.95]
- **PRD Draft Conversational Workflow** — prddraft_step0_context_check, prddraft_step1_clarifying_questions, prddraft_step2_first_draft, prddraft_step2_5_prototype, prddraft_step3_multi_agent_review [EXTRACTED 0.95]
- **QA Session End-to-End Flow** — qa_listen_clarify, qa_explore_codebase, qa_assess_scope, qa_file_github_issue, qa_continue_session [EXTRACTED 0.95]
- **UXD Full Workflow Pipeline** — designdraft_skill, designinterview_skill, designreview_skill, designdraft_step9_approve [EXTRACTED 0.95]
- **PRD Review 7-Agent Panel** — prdreviewpanel_engineer_agent, prdreviewpanel_designer_agent, prdreviewpanel_exec_agent, prdreviewpanel_legal_agent, prdreviewpanel_uxr_agent, prdreviewpanel_skeptic_agent, prdreviewpanel_customer_voice_agent [EXTRACTED 1.00]
- **Catalog Sync Required Artifacts** — readme_catalog, agents_site_js_skills_array, agents_site_js_changes_array, changelog_doc, concept_skill_authoring [EXTRACTED 1.00]
- **5-Agent Engineering Panel Review** — engspec_architect_reviewer, engspec_db_designer_reviewer, engspec_principal_swe_reviewer, engspec_sdet_reviewer, engspec_perf_engineer_reviewer [EXTRACTED 1.00]
- **PRD-to-Ralph Pipeline Flow** — prdapprove_skill, engspec_skill, engspec_hq_sync_context, engspec_rpc_plan [EXTRACTED 0.90]
- **Engineering Spec Artifact Trio (TDD/SPEC/ADR)** — engspec_tdd, engspec_spec, engspec_adr [EXTRACTED 1.00]

## Communities

### Community 0 - "Community 0"
Cohesion: 0.07
Nodes (31): Multi-Agent Review Pattern, Resume From Step (--from), design-draft Skill (Full UXD Workflow), Step 0: Find Approved PRD, Step 1: Load PRD Context, Step 2: Design Interview, Step 3: User Flow, Step 4: Wireframes (+23 more)

### Community 1 - "Community 1"
Cohesion: 0.09
Nodes (28): Catalog Sync Rule (Mandatory), Category to CSS Class Mapping, AGENTS.md - Project Agent Instructions, Git Conventions (dev branch, conventional commits), site.js changes array requirement, site.js skills array requirement, Skill Authoring Reference (write-a-skill), CLAUDE Catalog Sync Rule (Mandatory) (+20 more)

### Community 2 - "Community 2"
Cohesion: 0.1
Nodes (25): Deep Module (small interface, deep implementation), A Philosophy of Software Design (citation), Shallow Module (anti-pattern), Accept Dependencies, Don't Create Them, Small Surface Area Interfaces, Dependency Injection for Mockability, Do Not Mock Internal Collaborators, SDK-style Interfaces over Generic Fetchers (+17 more)

### Community 3 - "Community 3"
Cohesion: 0.09
Nodes (25): ADR (Architecture Decision Record), ADR-001 Hexagonal Architecture, ADR-002 Three-Database Strategy, Architect Reviewer Agent, DB Designer Reviewer Agent, DoE Approval Gate, hq.sync-context, 5-Agent Engineering Panel Review (+17 more)

### Community 4 - "Community 4"
Cohesion: 0.09
Nodes (24): 10 Principles for AI Products, AI Behavior Contract, Part 3: AI Feature PRDs, AI Behavior Specification (Good/Bad/Reject), Context Routing Logic, $1-$10-$100 Prototype Rule, Part 2: Full PRD Workflow (7 steps), PRD Hypothesis Section (If/Then/Because) (+16 more)

### Community 5 - "Community 5"
Cohesion: 0.25
Nodes (16): $(), addCopyButtons(), catClass(), closeDrawer(), copyText(), flashCopied(), getSkillPermalink(), initTheme() (+8 more)

### Community 6 - "Community 6"
Cohesion: 0.12
Nodes (18): Compact Conversation Skill Added (2026-04-08), Concise Reporting Added (2026-04-02), Changelog, E2E Audit Skill Added (2026-04-05), Eng-Spec, Git-Guardrails, TDD, Ubiquitous Language, Design Interview Added (2026-03-28), Flatten Skill Directories (2026-03-29), PRD-to-Plan, QA, Refactor-Plan Added (2026-03-31), Precision Mode + Package Scout Added (2026-04-03) (+10 more)

### Community 7 - "Community 7"
Cohesion: 0.13
Nodes (16): Calibration Examples, What Precision Mode Does NOT Mean, Derived from concise-reporting, 10 Output Rules (lead with answer, no filler, etc.), Prime Directive: Maximize Information Density, precision-mode README, Precision Mode Skill, Description Requirements (1024 chars, triggers) (+8 more)

### Community 8 - "Community 8"
Cohesion: 0.16
Nodes (14): 5 Reviewers (UXR/A11y/Engineer/Brand/EndUser), Accessibility Auditor (WCAG 2.1 AA), Brand Guardian Reviewer, End User Voice Reviewer, Engineer Feasibility Reviewer, UX Researcher Reviewer, Customer Voice Agent, Designer Reviewer Agent (+6 more)

### Community 9 - "Community 9"
Cohesion: 0.17
Nodes (12): Auth Storage Discovery, Diagnostic Report (Markdown), False Positive Check (negative assertions), In-Memory Auth (Zustand) Strategy, Playwright Test Framework, PRD-Driven Tests, Rationale: Auth Storage Drives Fixture Strategy, e2e-audit README (+4 more)

### Community 10 - "Community 10"
Cohesion: 0.2
Nodes (11): Step 3: Assess Scope (single vs breakdown), Breakdown Template (parallel issues), Step 5: Continue Session, Durable Issues (no file paths or line numbers), Step 2: Explore Codebase via Subagent, Step 4: File GitHub Issues, Step 1: Listen and Lightly Clarify, qa Skill README (+3 more)

### Community 11 - "Community 11"
Cohesion: 0.22
Nodes (11): Blockers & Risks Section, Engineering DOE Layer (doe-os), Feature Map, ralph fix_plan.md, Engineering Implementation (ralph / fix_plan), Next Actions (3-5 specific items), PRD-PIPELINE.md (source of truth), Product Layer (PM-OS) (+3 more)

### Community 12 - "Community 12"
Cohesion: 0.18
Nodes (11): Native /compact Command, Rationale: Prefer Native Compaction, compact-conversation README, compact-conversation Skill, Conversation Summary Document, Domain-Driven Design (DDD), Example Dialogue Pattern, Flagged Ambiguities Section (+3 more)

### Community 13 - "Community 13"
Cohesion: 0.22
Nodes (9): Decision Tree Walk, grill-me README, grill-me Skill, GitHub Issue (Refactor Plan), Martin Fowler (cited), request-refactor-plan README, request-refactor-plan Skill, Refactor Plan Template (+1 more)

### Community 14 - "Community 14"
Cohesion: 0.22
Nodes (9): bundlephobia.com (cited), Package Comparison Table, Lockfile-Based Package Manager Detection, Quality Signals (stars, downloads, vulns), Rationale: Avoid Stale Training Data, package-scout README, package-scout Skill, Snyk / socket.dev (cited) (+1 more)

### Community 15 - "Community 15"
Cohesion: 0.5
Nodes (0):

### Community 16 - "Community 16"
Cohesion: 0.5
Nodes (4): concise-reporting README, Reporting Mode (ultra-concise), concise-reporting Skill, Writing Mode (full verbosity)

### Community 17 - "Community 17"
Cohesion: 1.0
Nodes (1): Return Results, Avoid Side Effects

## Knowledge Gaps
- **141 isolated node(s):** `Mock at System Boundaries`, `Dependency Injection for Mockability`, `SDK-style Interfaces over Generic Fetchers`, `Do Not Mock Internal Collaborators`, `A Philosophy of Software Design (citation)` (+136 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **Thin community `Community 17`** (1 nodes): `Return Results, Avoid Side Effects`
  Too small to be a meaningful cluster - may be noise or needs more connections extracted.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `prd-review-panel Skill` connect `Community 0` to `Community 8`, `Community 1`?**
  _High betweenness centrality (0.027) - this node is a cross-community bridge._
- **Why does `design-review Skill` connect `Community 0` to `Community 8`, `Community 1`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **What connects `Mock at System Boundaries`, `Dependency Injection for Mockability`, `SDK-style Interfaces over Generic Fetchers` to the rest of the system?**
  _141 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Community 0` be split into smaller, more focused modules?**
  _Cohesion score 0.07 - nodes in this community are weakly interconnected._
- **Should `Community 1` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
- **Should `Community 2` be split into smaller, more focused modules?**
  _Cohesion score 0.1 - nodes in this community are weakly interconnected._
- **Should `Community 3` be split into smaller, more focused modules?**
  _Cohesion score 0.09 - nodes in this community are weakly interconnected._
