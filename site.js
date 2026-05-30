const repoUrl = "https://github.com/amit-t/skills";

const skills = [
  {
    slug: "prd-draft",
    name: "prd-draft",
    category: "Product Management",
    tagline: "Create modern, AI-era PRDs through guided interview.",
    detail: "Best when a feature idea is still fuzzy and the agent needs to shape the problem before writing requirements.",
    usage: "/prd-draft",
  },
  {
    slug: "prd-review-panel",
    name: "prd-review-panel",
    category: "Product Management",
    tagline: "Run a 7-perspective review on a PRD before approval.",
    detail: "Useful for pressure-testing clarity, scope, edge cases, and stakeholder concerns before the document moves forward.",
    usage: "/prd-review-panel",
  },
  {
    slug: "prd-approve",
    name: "prd-approve",
    category: "Product Management",
    tagline: "Approve a reviewed PRD and advance the pipeline.",
    detail: "Use after review is complete and the PRD is ready to become the source document for downstream planning and engineering.",
    usage: "/prd-approve",
  },
  {
    slug: "prd-to-plan",
    name: "prd-to-plan",
    category: "Product Management",
    tagline: "Break a PRD into tracer-bullet implementation phases.",
    detail: "Helps teams turn product requirements into a staged execution plan with slices that can be built and validated incrementally.",
    usage: "/prd-to-plan",
  },
  {
    slug: "write-a-prd",
    name: "write-a-prd",
    category: "Product Management",
    tagline: "Write a PRD through interview, exploration, and module design.",
    detail: "Good when the task needs more system understanding than a lightweight PRD interview alone can provide.",
    usage: "/write-a-prd",
  },
  {
    slug: "pmo-status",
    name: "pmo-status",
    category: "Project Management",
    tagline: "Get product, engineering, and implementation status in one pass.",
    detail: "Use at session start or when project state is fragmented across PM, DoE, specs, ADRs, and implementation artifacts.",
    usage: "/pmo-status",
  },
  {
    slug: "code-review",
    name: "code-review",
    category: "Engineering",
    tagline: "Principal-engineer review of any GitHub PR with two-phase approval before posting.",
    detail: "11-dimension rubric grounded in Pragmatic Programmer, Domain-Driven Design, and A Philosophy of Software Design. Pre-checks PR description quality (what / why / test plan), size (LOC + file count), and single-concern scope before deep review. Walks every finding one at a time with approve / skip / edit / expand / defer / quit verbs. Only the approved subset is posted as one grouped GitHub Review. Never auto-APPROVEs. Re-review safe — dedupes against prior runs via hidden markers. Fully configurable thresholds, rubric dimensions, and verdict policy in config.yaml.",
    usage: "/code-review <pr-num|url>",
  },
  {
    slug: "e2e-audit",
    name: "e2e-audit",
    category: "Engineering",
    tagline: "Playwright PRD audit + persona screenshot demo + bug-to-fix_plan emitter.",
    detail: "Discovers routes and auth strategy, scaffolds a Playwright e2e package, writes PRD-driven tests, captures full-page screenshots per persona/route, exports a diagnostic report, and appends one ralph task per bug to .ralph/fix_plan.md with file paths, root-cause hypotheses, and exit criteria.",
    usage: "/e2e-audit",
  },
  {
    slug: "eng-spec",
    name: "eng-spec",
    category: "Engineering",
    tagline: "Turn an approved PRD into TDD, engineering spec, and ADRs.",
    detail: "Runs a review panel across architecture, database design, testing, and performance before approval.",
    usage: "/eng-spec",
  },
  {
    slug: "tdd",
    name: "tdd",
    category: "Engineering",
    tagline: "Use a disciplined red-green-refactor workflow.",
    detail: "Fits feature work and bug fixes where the user wants test-first implementation and tighter feedback loops.",
    usage: "/tdd",
  },
  {
    slug: "git-guardrails-claude-code",
    name: "git-guardrails-claude-code",
    category: "Engineering",
    tagline: "Block destructive git commands in Claude Code.",
    detail: "Sets up hooks to stop push, reset, clean, and similar actions before they can damage the working tree or remote state.",
    usage: "/git-guardrails-claude-code",
  },
  {
    slug: "ubiquitous-language",
    name: "ubiquitous-language",
    category: "Engineering",
    tagline: "[Deprecated] Superseded by /repo-context-scan and /domain-grill.",
    detail: "Kept as a redirect so existing references resolve. Use /repo-context-scan to build CONTEXT.md from the code itself, /domain-grill to stress-test engineering artifacts against it, and /grill-me for PRDs or non-technical plans.",
    usage: "/ubiquitous-language",
  },
  {
    slug: "repo-context-scan",
    name: "repo-context-scan",
    category: "Engineering",
    tagline: "Scan a codebase to build CONTEXT.md and seed ADRs for clearly-deliberate decisions.",
    detail: "Autonomous by default — reads code, infers domain language, and writes CONTEXT.md (or CONTEXT-MAP.md for multi-context repos) plus seeded ADRs. Asks only when ambiguity blocks resolution. Idempotent; safe to re-run as the codebase evolves. Run after cloning a repo or whenever code has drifted from docs. Companion to /domain-grill.",
    usage: "/repo-context-scan",
  },
  {
    slug: "domain-grill",
    name: "domain-grill",
    category: "Engineering",
    tagline: "Engineering-only stress-test of a code artifact against CONTEXT.md.",
    detail: "Reads CONTEXT.md (and ADRs) to interview the user against an eng spec, TDD plan, refactor proposal, technical design, schema migration, or API contract. Surfaces conflicts, sharpens fuzzy terms, may add new ADRs for crystallized decisions. Refuses PRDs and non-technical artifacts and redirects to /grill-me. Read-only on CONTEXT.md — flags new terms and recommends re-running /repo-context-scan. Asks for a grill depth (quick / standard / deep) before starting, defaulting to deep; pre-selectable via `/domain-grill quick|standard|deep`. Depth changes how many branches the skill walks, not how sharp each question is.",
    usage: "/domain-grill [quick|standard|deep]",
  },
  {
    slug: "qa",
    name: "qa",
    category: "Engineering",
    tagline: "Run an interactive QA session that files GitHub issues.",
    detail: "Designed for conversational bug reporting when the user wants the agent to absorb context and turn findings into issues.",
    usage: "/qa",
  },
  {
    slug: "request-refactor-plan",
    name: "request-refactor-plan",
    category: "Engineering",
    tagline: "Plan a refactor as tiny, safe commits.",
    detail: "Best for risky cleanup work that needs an interview, incremental sequencing, and issue tracking before changes begin.",
    usage: "/request-refactor-plan",
  },
  {
    slug: "grill-me",
    name: "grill-me",
    category: "Engineering",
    tagline: "Stress-test a plan or design through relentless interview.",
    detail: "Good when an idea sounds plausible but the team wants to expose weak assumptions before investing implementation time. Asks for a grill depth (quick / standard / deep) before the first question, defaulting to deep; pre-selectable via `/grill-me quick|standard|deep`. Depth changes how many branches the skill walks, not how sharp each question is.",
    usage: "/grill-me [quick|standard|deep]",
  },
  {
    slug: "grill-me-auto",
    name: "grill-me-auto",
    category: "Engineering",
    tagline: "Batch-mode grill: all questions in one collapsible markdown doc, answered in one reply.",
    detail: "Same rigor as /grill-me, but non-interactive. Asks for depth (quick / standard / deep, default deep), writes numbered collapsible questions to `.grills/<YYYY-MM-DD-HHMM>-<slug>-<depth>.md`, includes options, recommendations, alt recommendations, and three reply paths: `accept all my recommendations`, `accept all my alt recommendations`, or a filled per-question answer key.",
    usage: "/grill-me-auto [quick|standard|deep]",
  },
  {
    slug: "package-scout",
    name: "package-scout",
    category: "Engineering",
    tagline: "Research, compare, and select the best packages before installing.",
    detail: "Stops the agent from blindly installing packages. Searches the web for alternatives, compares stars, downloads, bundle size, vulnerabilities, and maintenance — then presents a comparison table so the user picks the right dependency.",
    usage: "/package-scout",
  },
  {
    slug: "docs-from-prs",
    name: "docs-from-prs",
    category: "Engineering",
    tagline: "Sync README and other user-facing docs with merged PRs.",
    detail: "Surveys recent merged PRs, classifies user-facing changes, places each into the right doc section using a placement matrix, re-audits the project's drift hot spots (alias tables, CLI flag references, config examples) every run, and finishes with a grammar/casing/alignment copy-edit pass. Project-agnostic.",
    usage: "/docs-from-prs",
  },
  {
    slug: "gh-repo-mirror",
    name: "gh-repo-mirror",
    category: "Engineering",
    tagline: "Scaffold a new GitHub repo mirroring a reference repo's settings, branch protection, access, and Pages site.",
    detail: "Captures the reference repo's general settings, security-and-analysis flags, classic branch protection, and (default-on) team + direct-collaborator access, then creates the new repo and PATCHes / PUTs everything to match. Optionally ports a neo-brutalist GitHub Pages docs site (rebranded), wires a custom domain via docs/CNAME, and background-polls for the Let's Encrypt cert before flipping https_enforced. Pass `--no-mirror-access` to skip the team + collaborator step. Other opt-ins: mirror repo-level rulesets (`--mirror-rulesets`), create the Cloudflare DNS record (`--cname-provider cloudflare`), and bootstrap a starter skill so the first commit isn't empty arrays.",
    usage: "/gh-repo-mirror",
  },
  {
    slug: "resume-tailoring",
    name: "resume-tailoring",
    category: "Engineering",
    tagline: "Tailor a resume to a specific job with research, discovery, and scored matching.",
    detail: "Takes a JD and your resume library, researches the company/role, surfaces undocumented experience via branching interview, matches content with confidence scores, and emits MD + DOCX + PDF + interview-prep report. Multi-job batch mode for applying to 3–5 roles at once. Includes a portable single-file .skill bundle for Codex and co-work.",
    usage: "/resume-tailoring",
  },
  {
    slug: "design-interview",
    name: "design-interview",
    category: "UX Design",
    tagline: "Run a structured design brief interview before any screens.",
    detail: "Captures context, user goals, style, constraints, and success metrics before visual work starts.",
    usage: "/design-interview",
  },
  {
    slug: "design-draft",
    name: "design-draft",
    category: "UX Design",
    tagline: "Go from design interview to developer handoff.",
    detail: "Covers user flows, wireframes, system decisions, hi-fi screens, review, and approval in one end-to-end UX workflow.",
    usage: "/design-draft",
  },
  {
    slug: "design-review",
    name: "design-review",
    category: "UX Design",
    tagline: "Review generated screens from 5 design perspectives.",
    detail: "Useful for checking UX, accessibility, engineering feasibility, brand alignment, and end-user clarity before handoff.",
    usage: "/design-review",
  },
  {
    slug: "compact-conversation",
    name: "compact-conversation",
    category: "Agent Behavior",
    tagline: "Compact the current conversation into a concise summary.",
    detail: "Creates a structured summary of completed work, key decisions, current state, and pending tasks so you can continue in a fresh session without losing context. Only use when the agent lacks a built-in /compact command.",
    usage: "/compact-conversation",
  },
  {
    slug: "session-handoff",
    name: "session-handoff",
    category: "Agent Behavior",
    tagline: "Write a discoverable handoff document so another agent can continue the work via /resume-session-handoff.",
    detail: "Saves a focused handoff to `<project-root>/.claude/handoffs/YYYY-MM-DD-HHMM-<slug>.md` — goal, current state, decisions, ruled-out approaches, open questions, next moves, and suggested skills for the next session. YAML frontmatter (cwd, branch, uncommitted-file count, focus, status) feeds the companion `/resume-session-handoff` skill's preflight. Auto-adds `/.claude/handoffs/` to `.gitignore`, references existing artifacts (PRDs, plans, ADRs, issues, commits, diffs) by path or URL, and tailors the body to the optional argument describing the next session's focus. Named `session-handoff` (not `/handoff`) to avoid colliding with Devin's built-in `/handoff` command, which would otherwise shadow the skill.",
    usage: "/session-handoff",
  },
  {
    slug: "resume-session-handoff",
    name: "resume-session-handoff",
    category: "Agent Behavior",
    tagline: "Load the newest open handoff with an environment preflight, then ask what to do next — never auto-executes.",
    detail: "Companion to `/session-handoff`. Named `resume-session-handoff` because (1) most agents (Claude Code, Codex, others) ship a built-in `/resume` that restores the prior conversation and would shadow a skill named `resume`; (2) Devin reserves `/handoff` for its own session-transfer flow, so `/resume-handoff` collides by association. `/resume-session-handoff` is unambiguous. Resolves the project root the same way as `/session-handoff` (`git rev-parse --show-toplevel` → ancestor with `.claude/` → `pwd`), globs `<root>/.claude/handoffs/*.md` for the newest open handoff, parses its frontmatter, and surfaces drift against the current environment (project root, cwd, branch, uncommitted-file count, staleness over 14 days). On user confirm, flips `status: resumed`, sets `resumed_at`, moves the file to `.claude/handoffs/resumed/<resume-ts>--<orig-name>`, internalises the body, and **stops to ask the user what to do next** — presenting the Next-moves items, Suggested skills, and free-form options instead of auto-running the first move. Implicitly bootstraps the `using-superpowers` skill before asking, if the environment lists it, so process discipline (brainstorming → plan → TDD → verify) is loaded before the direction is chosen. Supports `/resume-session-handoff list`, `/resume-session-handoff <n>`, and `/resume-session-handoff <slug-substring>` for non-newest selection.",
    usage: "/resume-session-handoff",
  },
  {
    slug: "concise-reporting",
    name: "concise-reporting",
    category: "Agent Behavior",
    tagline: "Make progress and status reporting brutally concise.",
    detail: "Keeps agent updates short and direct while preserving full detail for real deliverables like docs, plans, and specs.",
    usage: "/concise-reporting",
  },
  {
    slug: "precision-mode",
    name: "precision-mode",
    category: "Agent Behavior",
    tagline: "Universal conciseness directive for all LLM output.",
    detail: "A single prompt injector that eliminates verbosity from every response — answers, code, explanations, plans, emails, docs. Paste into any system prompt.",
    usage: "/precision-mode",
  },
  {
    slug: "session-feedback",
    name: "session-feedback",
    category: "Agent Behavior",
    tagline: "Mine the conversation for corrections, preferences, and do-differently lessons; write a dated feedback file; in future sessions, ask 'do I care about this at the moment?' before applying any remembered item.",
    detail: "Two modes. Write mode walks every user turn, classifies into three buckets (corrections the user made, preferences they stated, principles to apply differently next time), and emits a frontmatter-tagged feedback-<YYYY-MM-DD>.md with stable IDs (C1-Cn, P1-Pn, D1-Dn) into the project's Claude Code auto-memory directory, indexed in MEMORY.md. No per-item filtering at write time. Recall mode (auto-triggered in future sessions, plus explicit --recall for a bulk session-start walk) surfaces remembered items in a compact listing format and asks 'Do I care about this at the moment, or do I not?' before the agent applies anything. Just-in-time recall is mandatory whenever the agent is about to act on a past pattern; bulk recall is opt-in via --recall. Session-scoped decisions live in .active-feedback.json; 'always' or 'never' answers persist back to the feedback file's frontmatter. Nothing is ever silently applied. Captures the user's actual words for corrections so future-you recognises the pattern, not just the conclusion.",
    usage: "/session-feedback",
  },
  {
    slug: "skill-sync",
    name: "skill-sync",
    category: "Agent Behavior",
    tagline: "Sync an existing skill from a source path, or scaffold a new one via claude/codex/devin.",
    detail: "Wraps the skill-sync zsh utility (in ai-utils/skill-sync). Sync mode mirrors a source skill into the current repo and upserts catalog entries (README, site.js, CHANGELOG, skills-lock). Build mode hands a runtime prompt to claude/codex/devin to scaffold a new skill from raw source material. Idempotent on rerun.",
    usage: "/skill-sync",
  },
  {
    slug: "write-a-skill",
    name: "write-a-skill",
    category: "AI Agent",
    tagline: "Create new skills with the right structure and disclosure.",
    detail: "Fits skill authoring work where the user wants reusable instructions, bundled resources, and better invocation behavior.",
    usage: "/write-a-skill",
  },
  {
    slug: "gh-pages-neo-brutalist",
    name: "gh-pages-neo-brutalist",
    category: "Engineering",
    tagline: "Scaffold a GitHub Pages site in a neo-brutalist house style.",
    detail: "Drop-in Jekyll templates with a cohesive neo-brutalist design system — IBM Plex Mono everywhere, 3px borders, solid offset shadows, eight saturated accents, four themes (light / dark / cyberpunk grid / solarized IDE), copy buttons on <pre>, theme switcher in localStorage. Includes scaffold.zsh for one-shot stamping and a GitHub Actions Pages workflow.",
    usage: "/gh-pages-neo-brutalist",
  },
  {
    slug: "wisdom-capture",
    name: "wisdom-capture",
    category: "Leadership",
    tagline: "Capture a wisdom snippet into a personal corpus — categorize, write, commit.",
    detail: "11-step flow that records one snippet as one file under `wisdoms/<YYYY>/<MM>/<ulid>.md`. Reads `wisdoms/_categories.yml` (closed taxonomy), proposes a primary bucket + tags, optionally proposes a new bucket if no fit, takes a personal note, writes frontmatter (id, created_at, body_hash, category, tags, source_url, source_author, note, import_origin), and commits with `wisdom: <category> — <body>…`. Vision-capable when the user pastes images (slide-style reels, quote cards). Designed for the companion `wisdom` CLI but works in any project that adopts the same data shape.",
    usage: "/wisdom-capture",
  },
  {
    slug: "leadership-update",
    name: "leadership-update",
    category: "Leadership",
    tagline: "Turn raw notes into an outcome-first update leadership remembers.",
    detail: "Reformats messy status into three sentences — outcome, reasoning, next — ending with a clear ask. Auto-detects whether to reformat directly or run a 1–3 question interview. Verbal/standup script by default; offers Slack, email, and status-doc formats. Based on Yasar Ahmad's leadership-update framework.",
    usage: "/leadership-update",
  },
];

const changes = [
  {
    date: "2026-05-30",
    items: [
      "Added grill-me-auto skill — batch-mode `/grill-me` fork that writes every question, option, recommendation, alt recommendation, and one-shot answer shortcut into a collapsible markdown grill document.",
    ],
  },
  {
    date: "2026-05-29",
    items: [
      "Added upstream attribution to `grill-me`. The skill is a fork of [`grill-me`](https://github.com/mattpocock/skills/blob/main/skills/productivity/grill-me/SKILL.md) by [Matt Pocock](https://github.com/mattpocock) (`mattpocock/skills`); this fork adds the `quick` / `standard` / `deep` depth selector while the relentless-interview core is Matt's original. Credit now lives where anyone installing the skill will see it — a Credits section in `grill-me/README.md` and a footer line in `grill-me/SKILL.md` so the attribution travels with the installed copy.",
    ],
  },
  {
    date: "2026-05-21",
    items: [
      "`gh-repo-mirror` now mirrors **repository access by default** — every team that has access to the reference repo is added to the new repo at the same permission level (pull / triage / push / maintain / admin), and direct collaborators are invited at the same permission. Driven by two read APIs (`GET repos/<ref>/teams` and `GET repos/<ref>/collaborators?affiliation=direct`) and two write APIs (`PUT /orgs/{org}/teams/{slug}/repos/{owner}/{repo}` and `PUT /repos/{owner}/{repo}/collaborators/{login}`). The collaborator PUT expects the *API* permission vocabulary (`pull`/`triage`/`push`/`maintain`/`admin`) but GET returns the *display* vocabulary (`read`/`triage`/`write`/`maintain`/`admin`); a `role_to_permission` helper translates `read→pull` and `write→push`. Skip with the new `--no-mirror-access` flag. Cross-org caveat: team slugs are scoped to the target org, so teams from a different reference org will 404 on the PUT and log a warning per team — only teams that already exist in the new org resolve. Pending invites also show up as drift in the end-of-run diff until the invitee accepts; that's expected, not a failure. End-of-run verification now diffs teams and direct collaborators in addition to settings and branch protection (`gh-repo-mirror/SKILL.md`, `gh-repo-mirror/README.md`, `gh-repo-mirror/REFERENCE.md`, and `gh-repo-mirror/scripts/mirror-repo.zsh`).",
    ],
  },
  {
    date: "2026-05-14",
    items: [
      "Added a grill-depth selector to both `grill-me` and `domain-grill`. Each skill now asks the user how deep to grill before the first question, defaulting to `deep` (deepest) — and accepts `quick` / `standard` / `deep` (aliases `1` / `2` / `3` and `sharp` / `medium` / `deepest`) either as the answer to that prompt or as a pre-selected invocation argument: `/grill-me quick`, `/domain-grill standard`, etc. `deep` walks every branch of the decision tree, surfaces contradictions hard, invents boundary scenarios, and cross-references against code / CONTEXT.md / ADRs until shared understanding (unbounded). `standard` covers the spine plus the obvious edges in ~15–25 questions. `quick` runs only the top ~5–10 highest-leverage hard-hitters — deal-breaker assumptions, glossary conflicts that would mislead implementers, ADR contradictions — as triage rather than full coverage. Depth changes *how many branches* the skill walks, not *how sharp* each question is; for `domain-grill`, the ADR-recording criteria and end-of-session summary still apply at every depth. SKILL.md, README.md, the site.js skills array entries, and this changes feed are all updated; `usage:` strings updated to `/grill-me [quick|standard|deep]` and `/domain-grill [quick|standard|deep]`.",
      "Renamed the handoff pair again to dodge a *second* shadow: `handoff` → `session-handoff` and `resume-handoff` → `resume-session-handoff`. New triggers are `/session-handoff` and `/resume-session-handoff`. The earlier rename (resume → resume-handoff) only resolved the `/resume` shadow on Claude Code / Codex; but Devin already ships a built-in `/handoff` command for its own session-transfer flow, which shadowed the write side and made `resume-handoff` collide by association too. The pair is now unambiguous everywhere. Behaviour is unchanged: same `.claude/handoffs/` document path, same preflight, same no-auto-execute resume that asks the user what to do next and implicitly bootstraps `using-superpowers` when available. Catalog updated end-to-end: `git mv handoff session-handoff` and `git mv resume-handoff resume-session-handoff` to preserve history, both `name:` frontmatter fields, all internal cross-refs in both SKILL.md and README.md files, root README catalog table, site.js skills entries, install-command lines in both READMEs, and `design-draft/SKILL.md`'s developer-handoff step (`Skill: /session-handoff`). Re-install with `npx skills@latest add amit-t/skills --skill session-handoff` and `npx skills@latest add amit-t/skills --skill resume-session-handoff`; remove any old `~/.agents/skills/handoff/`, `~/.agents/skills/resume-handoff/`, `~/.claude/skills/handoff`, `~/.claude/skills/resume-handoff` install directories or symlinks — skill managers don't auto-prune renamed sources.",
      "Renamed the `resume` skill to `resume-handoff` and reworked its post-confirm behavior. Two reasons. (1) The trigger `/resume` collides with most agents' built-in conversation-restore command (Claude Code, Codex, others), which shadows the skill — the new name `/resume-handoff` is unambiguous. (2) After preflight + confirm, the skill now updates frontmatter (`status: resumed`, `resumed_at`), moves the file to `.claude/handoffs/resumed/`, internalises the body, and **stops to ask the user what to do next**, presenting the Next-moves items, Suggested skills, and free-form options. It no longer auto-executes the first Next-moves item — the user picks the direction. The skill also implicitly invokes `using-superpowers` (if listed in the environment's available skills) before asking, so process discipline (brainstorming → plan → TDD → verify) is loaded before any decision is made. Catalog updated end-to-end: directory renamed (`resume/` → `resume-handoff/`), top-level README row, `/handoff` SKILL.md and README.md cross-references, site.js skills array entry, and this changelog feed all flipped to the new name. (Superseded same-day by the rename to `resume-session-handoff` once the Devin `/handoff` shadow was identified.)",
    ],
  },
  {
    date: "2026-05-13",
    items: [
      "Moved wisdom-capture from Engineering to Leadership in the catalog (README table + site.js skills array + site.js changes feed + per-skill README header). The skill itself is unchanged — the recategorization reflects that wisdom capture serves leadership reflection more than engineering practice.",
      "Added wisdom-capture skill under Engineering — records a personal wisdom snippet as one Markdown file under `wisdoms/<YYYY>/<MM>/<ulid>.md` with strict frontmatter (id/created_at/body_hash/category/tags/source_url/source_author/note/import_origin). Reads `wisdoms/_categories.yml` for the closed taxonomy, proposes a primary bucket + 2–5 tags (with confidence), can propose a new bucket if none fits and fall back to a second-best existing bucket on user rejection, asks for a personal gloss, computes a normalized-body sha256 hash for dedup, and commits with `wisdom: <category> — <body first 60>…`. Honors per-session push policy (.wisdom-session) and `WISDOM_NO_PUSH`. Vision-capable for image-trapped wisdom (slide-style reels, quote cards). Built as the agent half of the companion `wisdom` CLI repo (https://github.com/amit-t/wisdom).",
      "Reworked the handoff skill and added a companion resume skill under Agent Behavior — handoffs now live at a predictable, discoverable path (`<project-root>/.claude/handoffs/YYYY-MM-DD-HHMM-<slug>.md`) instead of an opaque `mktemp` location, so the next session never has to be told the file path. `/handoff` resolves project root via git → `.claude/` ancestor → cwd, auto-adds `/.claude/handoffs/` to `.gitignore`, slugifies the `$ARGUMENTS` focus (or picks a 2–3 word slug from the goal), writes YAML frontmatter (cwd, branch, uncommitted_files, focus, status, resumed_at) on top of the markdown body, and writes atomically via a `.tmp` rename. `/resume` globs the same directory for the newest open file, runs an environment preflight (project_root / cwd / branch / uncommitted-count drift, plus a >14-day staleness warning), confirms with the user, and on Y flips `status: resumed` + `resumed_at` and moves the file to `.claude/handoffs/resumed/<resume-ts>--<orig-name>` so it can't be re-picked. Supports `/resume list`, `/resume <n>`, and `/resume <slug-substring>` for non-newest selection.",
      "Added session-feedback skill under Agent Behavior — mines the current conversation for corrections the user made, preferences they stated, and do-differently lessons, then writes a dated frontmatter-tagged feedback-<YYYY-MM-DD>.md (stable IDs: C1-Cn, P1-Pn, D1-Dn) into the project's Claude Code auto-memory directory and indexes it in MEMORY.md. Idempotent (append by default, --overwrite to replace). Captures the user's actual words for corrections so future sessions recognise the pattern, not just the conclusion.",
      "Added recall mode to session-feedback — in future sessions the skill surfaces each remembered item in a compact listing format and asks 'Do I care about this at the moment, or do I not care about it at the moment?' before applying anything. Just-in-time recall is mandatory whenever the agent is about to act on a past pattern; bulk recall is available at session start via /session-feedback --recall. Session-scoped decisions live in .active-feedback.json; 'always' / 'never' answers persist back to the feedback file's frontmatter for that item. Nothing is ever silently applied.",
    ],
  },
  {
    date: "2026-05-12",
    items: [
      "Added code-review skill — principal-engineer review of a GitHub PR with two-phase approval. Pre-checks PR description quality, size, and single-concern scope; deep-reviews against an 11-dimension rubric grounded in Pragmatic Programmer / DDD / A Philosophy of Software Design; walks the user through every finding one at a time with approve / skip / edit / expand / defer / quit; posts only the approved subset as one grouped GitHub Review. Never auto-APPROVEs. Re-review safe via hidden markers. Thresholds, rubric, and verdict policy are configurable in code-review/config.yaml.",
      "Added handoff skill under Agent Behavior — writes a transferable handoff document to a `mktemp -t handoff-XXXXXX.md` path so a fresh agent can continue the work. Captures goal, state, decisions, ruled-out approaches, open questions, next moves, and suggested skills; references existing artifacts (PRDs, plans, ADRs, issues, commits) by path or URL instead of duplicating them.",
      "Added gh-repo-mirror skill under Engineering — scaffold a new GitHub repo that mirrors a reference repo's general settings, security flags, classic branch protection, and (optionally) its GitHub Pages docs site, with opt-ins for ruleset mirroring, Cloudflare DNS, and a bootstrap starter skill.",
    ],
  },
  {
    date: "2026-05-08",
    items: [
      "Added leadership-update skill under a new Leadership category — reformats raw notes into an outcome-first, three-sentence update with a clear ask, based on Yasar Ahmad's framework.",
      "Added repo-context-scan skill — autonomous codebase scan that produces CONTEXT.md (or CONTEXT-MAP.md for multi-context repos) and seeds ADRs for visibly-deliberate decisions. Idempotent re-runs preserve user-authored prose.",
      "Added domain-grill skill — engineering-only relentless interview that stress-tests eng specs, TDD plans, refactor proposals, technical designs, schema migrations, and API contracts against CONTEXT.md and existing ADRs. Refuses PRDs and non-technical artifacts and redirects to /grill-me. Reads CONTEXT.md read-only; flags new terms and recommends re-running /repo-context-scan.",
      "Deprecated ubiquitous-language skill — split into /repo-context-scan (build) and /domain-grill (stress-test). Stub remains as a redirect; original implementation preserved in git history.",
    ],
  },
  {
    date: "2026-04-29",
    items: [
      "Added gh-pages-neo-brutalist skill — drop-in Jekyll templates that scaffold a GitHub Pages site in a neo-brutalist house style (IBM Plex Mono, 3px borders, solid offset shadows, eight accents, four themes). Ships scaffold.zsh, site.css and site.js for design tokens and the theme switcher, and a GitHub Actions Pages workflow.",
    ],
  },
  {
    date: "2026-04-25",
    items: [
      "Added docs-from-prs skill — survey merged PRs, fill README/landing-page/user-guide gaps with thoughtful section placement, audit alias tables every run, and finish with a grammar/casing/alignment copy-edit pass.",
      "Generalized docs-from-prs to be project-agnostic — replaced ai-ralph-specific paths and remote workflow with a generic drift-hot-spot audit, `gh repo view`-resolved survey, and a layout-aware placement matrix (single-file / README+site / README+guide / full).",
    ],
  },
  {
    date: "2026-04-20",
    items: [
      "Refreshed e2e-audit — added persona screenshot demo (Phase 4), expanded diagnostic report (Phase 5), and fix_plan bug-list emitter (Phase 6) with re-audit workflow.",
      "Added skill-sync skill under Agent Behavior — wraps the skill-sync zsh utility (ai-utils/skill-sync) for syncing or scaffolding skills via claude/codex/devin.",
    ],
  },
  {
    date: "2026-04-16",
    items: [
      "Added resume-tailoring skill — research-driven resume tailoring with branching discovery, scored matching, multi-job batch mode, and a portable .skill bundle for Codex / co-work.",
    ],
  },
  {
    date: "2026-04-08",
    items: [
      "Added compact-conversation skill — compact conversations into concise summaries to reduce context window usage.",
    ],
  },
  {
    date: "2026-04-05",
    items: [
      "Added e2e-audit skill — Playwright end-to-end audit driven by PRDs.",
    ],
  },
  {
    date: "2026-04-03",
    items: [
      "Added precision-mode skill — universal conciseness directive for all LLM output.",
      "Added package-scout skill — research and compare packages before installing any dependency.",
    ],
  },
  {
    date: "2026-04-02",
    items: [
      "Added the concise-reporting skill under Agent Behavior.",
    ],
  },
  {
    date: "2026-03-31",
    items: [
      "Added prd-to-plan for phased tracer-bullet planning.",
      "Added qa for conversational QA reporting and issue filing.",
      "Added request-refactor-plan for safe incremental refactor planning.",
    ],
  },
  {
    date: "2026-03-29",
    items: [
      "Flattened skill directories across the repository.",
      "Added per-skill README files to standardize install guidance.",
      "Removed character-distiller and older workflow entries.",
    ],
  },
  {
    date: "2026-03-28",
    items: [
      "Added eng-spec for TDD, spec, and ADR generation with review.",
      "Added git-guardrails-claude-code, tdd, ubiquitous-language, and design-interview.",
    ],
  },
];

/* ===== STATE ===== */
const state = { search: "", category: "All" };

/* ===== DOM REFS ===== */
const $ = (sel) => document.querySelector(sel);
const searchInput = $("#search-input");
const filtersEl = $("#category-filters");
const skillsGrid = $("#skills-grid");
const changeList = $("#change-list");
const skillCountEl = $("#skill-count");
const categoryCountEl = $("#category-count");
const drawer = $("#skill-drawer");
const drawerBackdrop = $("#drawer-backdrop");
const drawerCloseBtn = $("#drawer-close");
const drawerContent = $("#drawer-content");
const themeToggle = $("#theme-toggle");

/* ===== CATEGORIES ===== */
const categories = ["All", ...new Set(skills.map((s) => s.category))];

/* ===== INIT ===== */
skillCountEl.textContent = String(skills.length);
categoryCountEl.textContent = String(categories.length - 1);

/* ===== THEME ===== */
function initTheme() {
  const stored = localStorage.getItem("theme");
  if (stored === "dark" || (!stored && window.matchMedia("(prefers-color-scheme: dark)").matches)) {
    document.body.classList.add("dark");
  }
  updateThemeIcon();
}

function toggleTheme() {
  document.body.classList.toggle("dark");
  localStorage.setItem("theme", document.body.classList.contains("dark") ? "dark" : "light");
  updateThemeIcon();
}

function updateThemeIcon() {
  const isDark = document.body.classList.contains("dark");
  themeToggle.textContent = isDark ? "\u2600" : "\u263E";
  themeToggle.setAttribute("aria-label", isDark ? "Switch to light mode" : "Switch to dark mode");
}

themeToggle.addEventListener("click", toggleTheme);
initTheme();

/* ===== EVENTS ===== */
searchInput.addEventListener("input", (e) => {
  state.search = e.target.value.trim().toLowerCase();
  renderSkills();
});

drawerBackdrop.addEventListener("click", closeDrawer);
drawerCloseBtn.addEventListener("click", closeDrawer);
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && drawer.classList.contains("open")) closeDrawer();
});

/* ===== CATEGORY -> CSS CLASS MAPPING ===== */
function catClass(category) {
  const map = {
    "Product Management": "cat-product-management",
    "Project Management": "cat-project-management",
    "Engineering": "cat-engineering",
    "UX Design": "cat-ux-design",
    "Agent Behavior": "cat-agent-behavior",
    "AI Agent": "cat-ai-agent",
    "Leadership": "cat-leadership",
  };
  return map[category] || "";
}

/* ===== RENDER ===== */
function renderFilters() {
  filtersEl.innerHTML = "";
  for (const cat of categories) {
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = `filter-btn${cat === state.category ? " active" : ""}`;
    btn.textContent = cat;
    btn.addEventListener("click", () => {
      state.category = cat;
      renderFilters();
      renderSkills();
    });
    filtersEl.appendChild(btn);
  }
}

function renderSkills() {
  const filtered = skills.filter((s) => {
    const matchCat = state.category === "All" || s.category === state.category;
    const hay = `${s.name} ${s.category} ${s.tagline} ${s.detail}`.toLowerCase();
    const matchSearch = !state.search || hay.includes(state.search);
    return matchCat && matchSearch;
  });

  skillsGrid.innerHTML = "";

  if (!filtered.length) {
    const p = document.createElement("p");
    p.className = "empty-state";
    p.textContent = "No skills match the current filter.";
    skillsGrid.appendChild(p);
    return;
  }

  for (const skill of filtered) {
    const card = document.createElement("button");
    card.type = "button";
    card.className = "skill-card";
    card.innerHTML = `
      <span class="skill-card-cat ${catClass(skill.category)}">${skill.category}</span>
      <h3 class="skill-card-title">${skill.name}</h3>
      <p class="skill-card-tagline">${skill.tagline}</p>
      <p class="skill-card-detail">${skill.detail}</p>
      <span class="skill-card-footer">&rarr; Install + Details</span>
    `;
    card.addEventListener("click", () => openDrawer(skill));
    skillsGrid.appendChild(card);
  }
}

function renderChanges() {
  changeList.innerHTML = "";
  for (const change of changes) {
    const card = document.createElement("article");
    card.className = "change-card";
    card.innerHTML = `
      <span class="change-date">${change.date}</span>
      <ul>${change.items.map((i) => `<li>${i}</li>`).join("")}</ul>
    `;
    changeList.appendChild(card);
  }
}

/* ===== PERMALINK ===== */
const SHARE_ICON = `<svg viewBox="0 0 24 24"><circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42" y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/></svg>`;

function getSkillPermalink(slug) {
  const url = new URL(window.location.href);
  url.hash = `skill=${slug}`;
  return url.toString();
}

function openSkillFromHash() {
  const hash = window.location.hash;
  if (!hash.startsWith("#skill=")) return;
  const slug = decodeURIComponent(hash.slice(7));
  const skill = skills.find((s) => s.slug === slug);
  if (skill) openDrawer(skill, true);
}

/* ===== DRAWER ===== */
function openDrawer(skill, fromHash) {
  if (!fromHash) {
    history.replaceState(null, "", `#skill=${skill.slug}`);
  }
  drawerContent.innerHTML = `
    <span class="section-eyebrow ${catClass(skill.category)}">Skill Detail</span>
    <h2>${skill.name}</h2>

    <div class="drawer-meta">
      <span class="meta-pill meta-category">${skill.category}</span>
      <span class="meta-pill meta-usage">Invoke: ${skill.usage}</span>
    </div>

    <section class="drawer-section">
      <h3>What it does</h3>
      <p><strong>${skill.tagline}</strong></p>
      <p>${skill.detail}</p>
    </section>

    <section class="drawer-section">
      <h3>Install with CLI</h3>
      <pre><code>npx skills@latest add amit-t/skills --skill ${skill.slug}</code></pre>
      <p style="margin-top:0.5rem;font-size:0.82rem;color:var(--muted-light)">Or install all skills at once:</p>
      <pre><code>npx skills@latest add amit-t/skills</code></pre>
    </section>

    <section class="drawer-section">
      <h3>Install for specific agents</h3>
      <pre><code>npx skills@latest add amit-t/skills --skill ${skill.slug} --agent claude-code cursor</code></pre>
      <pre style="margin-top:0.5rem"><code>npx skills@latest add amit-t/skills --skill ${skill.slug} -g</code></pre>
    </section>

    <section class="drawer-section">
      <h3>Manual installation</h3>
      ${renderManualInstalls(skill.slug)}
    </section>

    <section class="drawer-section">
      <h3>Source files</h3>
      <div class="drawer-links">
        <a class="neo-btn" href="${repoUrl}/blob/main/${skill.slug}/README.md" target="_blank" rel="noreferrer">README</a>
        <a class="neo-btn" href="${repoUrl}/blob/main/${skill.slug}/SKILL.md" target="_blank" rel="noreferrer">SKILL.md</a>
        <a class="neo-btn" href="${repoUrl}/tree/main/${skill.slug}" target="_blank" rel="noreferrer">Directory</a>
      </div>
    </section>

    <section class="drawer-section">
      <h3>Share this skill</h3>
      <div class="drawer-links">
        <button class="neo-btn share-btn" type="button" data-slug="${skill.slug}">
          ${SHARE_ICON}<span>Copy link</span>
        </button>
      </div>
    </section>
  `;

  drawerContent.querySelector(".share-btn").addEventListener("click", (e) => {
    e.stopPropagation();
    const btn = e.currentTarget;
    const link = getSkillPermalink(btn.dataset.slug);
    copyText(link).then(() => {
      btn.innerHTML = `${CHECK_ICON}<span>Copied!</span>`;
      btn.classList.add("copied");
      setTimeout(() => {
        btn.innerHTML = `${SHARE_ICON}<span>Copy link</span>`;
        btn.classList.remove("copied");
      }, 1500);
    });
  });

  addCopyButtons(drawerContent);
  drawer.classList.add("open");
  document.body.classList.add("drawer-open");
  drawerCloseBtn.focus();
}

function closeDrawer() {
  drawer.classList.remove("open");
  document.body.classList.remove("drawer-open");
  if (window.location.hash.startsWith("#skill=")) {
    history.replaceState(null, "", window.location.pathname + window.location.search);
  }
}

function renderManualInstalls(slug) {
  return `
    <details class="install-expand">
      <summary>Devin / Windsurf</summary>
      <pre><code># Project-level
cp -r ${slug} .cognition/skills/${slug}
# or
cp -r ${slug} .windsurf/skills/${slug}

# Global
cp -r ${slug} ~/.config/cognition/skills/${slug}</code></pre>
    </details>

    <details class="install-expand">
      <summary>Claude Code</summary>
      <pre><code># Project-level
cp -r ${slug} .claude/skills/${slug}

# Global
cp -r ${slug} ~/.claude/skills/${slug}</code></pre>
    </details>

    <details class="install-expand">
      <summary>Cursor</summary>
      <pre><code># Project-level
cp -r ${slug} .cursor/skills/${slug}</code></pre>
    </details>

    <details class="install-expand">
      <summary>Codex</summary>
      <pre><code>cat ${slug}/SKILL.md >> AGENTS.md</code></pre>
    </details>

    <details class="install-expand">
      <summary>Gemini CLI</summary>
      <pre><code>cat ${slug}/SKILL.md >> GEMINI.md</code></pre>
    </details>
  `;
}

/* ===== COPY TO CLIPBOARD ===== */
const COPY_ICON = `<svg viewBox="0 0 24 24"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>`;
const CHECK_ICON = `<svg viewBox="0 0 24 24"><polyline points="20 6 9 17 4 12"/></svg>`;

function copyText(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    return navigator.clipboard.writeText(text);
  }
  // Fallback for older browsers / restricted contexts
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.cssText = "position:fixed;left:-9999px;top:-9999px;opacity:0";
  document.body.appendChild(ta);
  ta.select();
  try { document.execCommand("copy"); } catch (_) { /* best-effort */ }
  document.body.removeChild(ta);
  return Promise.resolve();
}

function flashCopied(btn) {
  btn.innerHTML = `${CHECK_ICON}<span>Copied</span>`;
  btn.classList.add("copied");
  setTimeout(() => {
    btn.innerHTML = `${COPY_ICON}<span>Copy</span>`;
    btn.classList.remove("copied");
  }, 1500);
}

function addCopyButtons(root = document) {
  root.querySelectorAll("pre").forEach((pre) => {
    if (pre.querySelector(".copy-btn")) return;
    const btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.setAttribute("aria-label", "Copy to clipboard");
    btn.innerHTML = `${COPY_ICON}<span>Copy</span>`;
    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const code = pre.querySelector("code");
      const text = (code || pre).textContent;
      copyText(text).then(() => flashCopied(btn)).catch(() => flashCopied(btn));
    });
    pre.appendChild(btn);
  });
}

/* ===== BOOT ===== */
renderFilters();
renderSkills();
renderChanges();
addCopyButtons();
openSkillFromHash();
window.addEventListener("hashchange", openSkillFromHash);
