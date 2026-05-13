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
    detail: "Reads CONTEXT.md (and ADRs) to interview the user against an eng spec, TDD plan, refactor proposal, technical design, schema migration, or API contract. Surfaces conflicts, sharpens fuzzy terms, may add new ADRs for crystallized decisions. Refuses PRDs and non-technical artifacts and redirects to /grill-me. Read-only on CONTEXT.md — flags new terms and recommends re-running /repo-context-scan.",
    usage: "/domain-grill",
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
    detail: "Good when an idea sounds plausible but the team wants to expose weak assumptions before investing implementation time.",
    usage: "/grill-me",
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
    tagline: "Scaffold a new GitHub repo mirroring a reference repo's settings, branch protection, and Pages site.",
    detail: "Captures the reference repo's general settings, security-and-analysis flags, and classic branch protection, then creates the new repo and PATCHes everything to match. Optionally ports a neo-brutalist GitHub Pages docs site (rebranded), wires a custom domain via docs/CNAME, and background-polls for the Let's Encrypt cert before flipping https_enforced. Opt-ins: mirror repo-level rulesets, create the Cloudflare DNS record, and bootstrap a starter skill so the first commit isn't empty arrays.",
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
    slug: "handoff",
    name: "handoff",
    category: "Agent Behavior",
    tagline: "Write a transferable handoff document so another agent can continue the work.",
    detail: "Saves a focused handoff to a `mktemp -t handoff-XXXXXX.md` path — goal, current state, decisions, ruled-out approaches, open questions, next moves, and suggested skills for the next session. References existing artifacts (PRDs, plans, ADRs, issues, commits, diffs) by path or URL instead of duplicating them. Accepts an argument describing what the next session will focus on and prunes the doc to match.",
    usage: "/handoff",
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
    tagline: "Mine the current conversation for corrections, preferences, and do-differently lessons; write a dated feedback file the next session reloads.",
    detail: "Walks every user turn, classifies into three buckets (corrections the user made, preferences they stated, principles to apply differently next time), and emits a frontmatter-tagged feedback-<YYYY-MM-DD>.md into the project's Claude Code auto-memory directory, plus a one-line entry in MEMORY.md so the file resurfaces in future sessions. Idempotent — re-running on the same day appends a new section unless --overwrite is passed. Captures the user's actual words for corrections so future-you recognises the pattern, not just the conclusion.",
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
    date: "2026-05-13",
    items: [
      "Added session-feedback skill under Agent Behavior — mines the current conversation for corrections the user made, preferences they stated, and do-differently lessons, then writes a dated frontmatter-tagged feedback-<YYYY-MM-DD>.md into the project's Claude Code auto-memory directory and indexes it in MEMORY.md. Idempotent (append by default, --overwrite to replace). Captures the user's actual words for corrections so future sessions recognise the pattern, not just the conclusion.",
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
