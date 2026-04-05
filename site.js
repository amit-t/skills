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
    slug: "e2e-audit",
    name: "e2e-audit",
    category: "Engineering",
    tagline: "Run a Playwright end-to-end audit against your PRDs.",
    detail: "Discovers routes and auth strategy, scaffolds a Playwright e2e package, writes PRD-driven tests, runs the suite, and exports a diagnostic report showing what's working and what's not from a user's perspective.",
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
    tagline: "Extract a DDD-style glossary from the current conversation.",
    detail: "Useful when terms are drifting, requirements sound ambiguous, or the team needs canonical vocabulary before building.",
    usage: "/ubiquitous-language",
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
    slug: "write-a-skill",
    name: "write-a-skill",
    category: "AI Agent",
    tagline: "Create new skills with the right structure and disclosure.",
    detail: "Fits skill authoring work where the user wants reusable instructions, bundled resources, and better invocation behavior.",
    usage: "/write-a-skill",
  },
];

const changes = [
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
