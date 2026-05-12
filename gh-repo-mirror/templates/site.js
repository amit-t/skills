const repoUrl = "{{REPO_URL}}";
const repoSlug = "{{REPO_SLUG}}";

const skills = [];

const changes = [];

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
categoryCountEl.textContent = String(Math.max(0, categories.length - 1));

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
  themeToggle.textContent = isDark ? "☀" : "☾";
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

  if (!skills.length) {
    const p = document.createElement("p");
    p.className = "empty-state";
    p.textContent = "No skills yet. Add a skill directory + entry in docs/site.js to populate this grid.";
    skillsGrid.appendChild(p);
    return;
  }

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
  if (!changes.length) {
    const p = document.createElement("p");
    p.className = "empty-state";
    p.textContent = "No changelog entries yet.";
    changeList.appendChild(p);
    return;
  }
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
      <pre><code>npx skills@latest add ${repoSlug} --skill ${skill.slug}</code></pre>
      <p style="margin-top:0.5rem;font-size:0.82rem;color:var(--muted-light)">Or install all skills at once:</p>
      <pre><code>npx skills@latest add ${repoSlug}</code></pre>
    </section>

    <section class="drawer-section">
      <h3>Install for specific agents</h3>
      <pre><code>npx skills@latest add ${repoSlug} --skill ${skill.slug} --agent claude-code cursor</code></pre>
      <pre style="margin-top:0.5rem"><code>npx skills@latest add ${repoSlug} --skill ${skill.slug} -g</code></pre>
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
