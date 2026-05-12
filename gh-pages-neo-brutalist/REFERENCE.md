# Neo-Brutalist GH Pages — Full Design Reference

Every token, every component, every theme.

## 1. Design Tokens

```css
:root {
  /* surfaces */
  --bg-light: #fafaf9;
  --bg-dark: #0a0a0a;
  --text-light: #1a1a1a;
  --text-dark: #e5e5e5;
  --surface-light: #ffffff;
  --surface-dark: #141414;
  --border-light: #1a1a1a;
  --border-dark: #333333;
  --muted-light: #737373;
  --muted-dark: #a3a3a3;

  /* accents (8) */
  --hot-pink:        #ff00f5;
  --warm-coral:      #ff5f5f;
  --electric-blue:   #0052ff;
  --lime-green:      #afff00;
  --vibrant-orange:  #ff4911;
  --cyan-accent:     #00c1d4;
  --yellow-accent:   #ffef00;
  --purple-accent:   #5b2eff;

  /* shadows — solid offset only, no blur */
  --shadow-sm: 3px 3px 0;
  --shadow-md: 5px 5px 0;
  --shadow-lg: 8px 8px 0;

  /* geometry */
  --border-w: 3px;
  --radius:    0px;
  --radius-sm: 0px;
  --radius-pill: 0px;
}
```

### Dark-mode accent dampers

When `body.dark` is set, accents shift to ~30% lightness equivalents to keep contrast:

| Light accent | Dark equivalent |
|--------------|-----------------|
| `--hot-pink #ff00f5` | `#b3004b` |
| `--warm-coral #ff5f5f` | `#b2432e` |
| `--electric-blue #0052ff` | `#1e3a5c` |
| `--lime-green #afff00` | `#3d6600` |
| `--vibrant-orange #ff4911` | `#b25a00` |
| `--cyan-accent #00c1d4` | `#007a8a` |
| `--yellow-accent #ffef00` | `#bba701` |
| `--purple-accent #5b2eff` | `#341797` |

## 2. Typography

| Element | Family | Size | Weight | Tracking | Line-height |
|---------|--------|------|--------|----------|-------------|
| `body` | `"IBM Plex Mono", ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace` | `15px` | 400 | normal | 1.6 |
| `h1` | inherit | `clamp(2.5rem, 6vw, 4.5rem)` | 700 | `-0.03em` | 1.1 |
| `h2` | inherit | `clamp(1.75rem, 4vw, 2.75rem)` | 700 | `-0.03em` | 1.1 |
| `h3` | inherit | `clamp(1.1rem, 2.5vw, 1.5rem)` | 700 | `-0.03em` | 1.1 |
| `h4` | inherit | `1rem` | 700 | `-0.03em` | 1.1 |
| eyebrow text | inherit | `0.72-0.75rem` | 700 | `0.06-0.08em` | uppercase |
| code | inherit | `0.82-0.85rem` | 600 | normal | 1.5 |

Font load (in `<head>`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## 3. Layout

```css
.container {
  width: min(1140px, calc(100% - 2rem));
  margin: 0 auto;
  padding: 0 1rem;
}
```

Breakpoints: 860px (collapse hero stats / readme grid), 640px (single-column, full-width buttons).

## 4. Components

### 4.1 Theme switcher (top-right `<select>`)

```html
<div class="theme-switcher">
  <label class="sr-only" for="theme-select">Theme</label>
  <select id="theme-select" aria-label="Select theme">
    <option value="light">☀ Light</option>
    <option value="dark">☾ Dark</option>
    <option value="cyberpunk">⚡ Cyberpunk</option>
    <option value="solarized">◐ Solarized</option>
  </select>
  <span class="theme-switcher-chevron" aria-hidden="true">▾</span>
</div>
```

JS in `site.js` reads `localStorage['wb-theme']`, falls back to `prefers-color-scheme`, applies one of `dark|cyberpunk|solarized` body classes (light = no class).

### 4.2 Site nav

```html
<nav class="container site-nav" aria-label="Primary">
  <a class="site-nav-brand" href="/repo/">Repo Name</a>
  <a href="/repo/getting-started.html">Getting Started</a>
  <a href="/repo/architecture.html">Architecture</a>
  <a href="https://github.com/owner/repo" target="_blank" rel="noreferrer">GitHub</a>
</nav>
```

Brand cell: hot-pink background, 3px border, 3px shadow. Links: transparent until hover, then lime-green background + 2px border.

### 4.3 Hero (landing)

```html
<header class="container hero">
  <div>
    <span class="hero-eyebrow">EYEBROW LABEL</span>
    <h1>Big Headline.</h1>
    <p class="hero-desc">Promise paragraph, max 60ch.</p>
    <div class="hero-actions">
      <a class="neo-btn neo-btn-primary" href="/start">Start Here</a>
      <a class="neo-btn" href="/skills">Browse Skills</a>
      <a class="neo-btn" href="https://github.com/..." target="_blank" rel="noreferrer">GitHub</a>
    </div>
  </div>
  <div class="hero-stats">
    <div class="stat-card"><span class="stat-value">42</span><span class="stat-label">Skills</span></div>
    <div class="stat-card"><span class="stat-value">8</span><span class="stat-label">Categories</span></div>
    <div class="stat-card"><span class="stat-value">2026-04-29</span><span class="stat-label">Last Update</span></div>
  </div>
</header>
<hr class="divider container">
```

`hero-stats` is optional — drop it for plain hero.

### 4.4 Doc hero (per-page)

Lighter than landing hero. Used on `getting-started.html`, `architecture.html`, etc.

```html
<header class="container doc-hero">
  <span class="doc-hero-eyebrow">SECTION</span>
  <h1>Page Title</h1>
  <p class="doc-hero-desc">One-line lede.</p>
</header>
```

### 4.5 Buttons

```html
<a class="neo-btn">Plain</a>
<a class="neo-btn neo-btn-primary">Primary (hot pink)</a>
<a class="neo-btn neo-btn-accent">Accent (electric blue)</a>
```

Hover: `translate(-2px, -2px)` + larger shadow. Active: `translate(2px, 2px)` + tiny shadow.

### 4.6 Eyebrow / section label

```html
<span class="section-eyebrow eyebrow-readme">README</span>
<span class="section-eyebrow eyebrow-eng">ENGINEERING</span>
```

Map:

| Class | Background | Foreground | Use |
|-------|-----------|------------|-----|
| `eyebrow-pm` | warm-coral | `#000` | Product Management |
| `eyebrow-eng` | electric-blue | `#fff` | Engineering |
| `eyebrow-ux` | purple-accent | `#fff` | UX Design |
| `eyebrow-agent` | cyan-accent | `#000` | Agent Behaviour |
| `eyebrow-ai` | yellow-accent | `#000` | AI Agent |
| `eyebrow-readme` | lime-green | `#000` | README |
| `eyebrow-changelog` | hot-pink | `#000` | Changelog |
| `eyebrow-proj` | vibrant-orange | `#fff` | Project Management |

### 4.7 Section + section header

```html
<section class="container section" id="readme-section">
  <div class="section-header">
    <div>
      <span class="section-eyebrow eyebrow-readme">README</span>
      <h2>What the repository promises</h2>
    </div>
    <a class="section-link" href="...">Open full README</a>
  </div>
  <!-- section content -->
</section>
<hr class="divider container">
```

### 4.8 Cards

#### Stat card

```html
<div class="stat-card">
  <span class="stat-value">42</span>
  <span class="stat-label">Skills</span>
</div>
```

#### Readme card (compound)

```html
<div class="readme-card">
  <div class="readme-grid">
    <div class="readme-text">
      <p>...</p>
      <div class="chip-row">
        <span class="chip">Devin</span>
        <span class="chip">Claude Code</span>
      </div>
    </div>
    <div class="install-commands">
      <h3>Quick Install</h3>
      <pre><code>npx skills@latest add amit-t/skills</code></pre>
    </div>
  </div>
  <div style="overflow-x:auto"><table class="manual-table">...</table></div>
</div>
```

#### Skill card (clickable, used on index pages)

```html
<button class="skill-card" data-skill="tdd">
  <span class="skill-card-cat cat-engineering">Engineering</span>
  <h3 class="skill-card-title">tdd</h3>
  <p class="skill-card-tagline">Test-driven development with red/green/refactor</p>
  <p class="skill-card-detail">Three-phase loop: write a failing test, write minimal code, refactor.</p>
  <span class="skill-card-footer">View Install →</span>
</button>
```

Category classes: `cat-product-management`, `cat-project-management`, `cat-engineering`, `cat-ux-design`, `cat-agent-behavior`, `cat-ai-agent`.

#### Change card

```html
<article class="change-card">
  <span class="change-date">2026-04-29</span>
  <h3>v1.4.0</h3>
  <ul>
    <li>Added gh-pages-neo-brutalist skill</li>
  </ul>
</article>
```

### 4.9 Filter / search controls

```html
<div class="controls">
  <label>
    <span class="sr-only">Search</span>
    <input class="search-input" type="search" placeholder="Search...">
  </label>
  <div class="filters">
    <button class="filter-btn active">All</button>
    <button class="filter-btn">Engineering</button>
    <button class="filter-btn">Product</button>
  </div>
</div>
```

### 4.10 Drawer (slide-in from right)

```html
<aside class="drawer" id="skill-drawer">
  <div class="drawer-backdrop"></div>
  <div class="drawer-panel">
    <button class="drawer-close" aria-label="Close">&times;</button>
    <div class="drawer-content">
      <h2>Skill Title</h2>
      <div class="drawer-meta">
        <span class="meta-pill meta-category">Engineering</span>
        <span class="meta-pill meta-usage">/skill-name</span>
      </div>
      <div class="drawer-section">
        <h3>What it does</h3>
        <p>...</p>
      </div>
      <details class="install-expand">
        <summary>Install for Claude Code</summary>
        <pre><code>npx skills@latest add amit-t/skills --skill name --agent claude-code</code></pre>
      </details>
    </div>
  </div>
</aside>
```

JS toggles `body.drawer-open` (locks scroll) and `.drawer.open`.

### 4.11 Breadcrumbs

```html
<nav class="container breadcrumbs" aria-label="Breadcrumb">
  <ol>
    <li><a href="/repo/">Home</a></li>
    <li><a href="/repo/architecture.html">Architecture</a></li>
    <li aria-current="page">Component X</li>
  </ol>
</nav>
```

### 4.12 Markdown body (for Jekyll-rendered content)

Wrap rendered markdown in `<article class="markdown-body">{{ content }}</article>`. Provides:

- h1 with bottom border (3px solid)
- h2 with bottom border (2px solid)
- code in vibrant-orange with 2px border + light background tint
- `<pre>` with shadow + dark surface (`#0a0a0a`)
- tables with cyan header row, full-width borders
- blockquote with 6px hot-pink left border
- `<details>` rendered as collapsible card with rotating chevron

### 4.13 Copy button (auto-attached to `<pre>`)

`site.js` adds a copy button to every `.markdown-body pre`. No markup needed — the JS attaches it. Confirm with hover; turns lime-green when copied.

### 4.14 Footer

```html
<footer class="container footer">
  <p>
    <code>repo-name</code> — short tagline. Source on
    <a href="https://github.com/owner/repo">GitHub</a>.
  </p>
</footer>
```

## 5. Themes

### 5.1 Light (default — no class)

Background `#fafaf9`, text `#1a1a1a`, borders `#1a1a1a`, surfaces `#ffffff`. Accents at full saturation.

### 5.2 Dark (`body.dark`)

Background `#0a0a0a`, text `#e5e5e5`, borders `#333333`, surfaces `#141414`. Accents at ~30% lightness (see token table).

### 5.3 Cyberpunk (`body.cyberpunk`)

Background `#0b0016` with magenta/cyan grid backdrop:

```css
background-image:
  linear-gradient(rgba(255, 54, 192, 0.05) 1px, transparent 1px),
  linear-gradient(90deg, rgba(0, 247, 255, 0.05) 1px, transparent 1px);
background-size: 40px 40px, 40px 40px;
```

Borders `#ff36c0` (magenta), shadows `#00f7ff` (cyan), text `#eedcff`. h1/h2 gain neon `text-shadow`.

### 5.4 Solarized (`body.solarized`)

Solarized Light palette:

| Token | Hex | Solarized name |
|-------|-----|----------------|
| `--bg-light` | `#fdf6e3` | base3 |
| `--surface-light` | `#eee8d5` | base2 |
| `--text-light` | `#073642` | base02 |
| `--border-light` | `#586e75` | base01 |
| `--muted-light` | `#93a1a1` | base1 |
| brand | `#268bd2` | blue |
| primary CTA | `#cb4b16` | orange |
| eyebrow | `#859900` | green |
| current-page | `#b58900` | yellow |
| `<pre>` bg | `#002b36` | base03 (dark editor pane) |
| `<pre>` text | `#eee8d5` | base2 |
| code | `#d33682` | magenta |

Gives an IDE-feel that pairs well with code-heavy docs.

## 6. Jekyll integration

### 6.1 `_config.yml`

```yaml
title: Repo Name
description: One-line tagline.
baseurl: /repo-name
url: https://owner.github.io
theme: null

plugins:
  - jekyll-seo-tag
  - jekyll-relative-links

permalink: pretty
markdown: kramdown
kramdown:
  input: GFM
  syntax_highlighter: rouge

include:
  - .well-known
exclude:
  - Gemfile
  - Gemfile.lock
  - vendor
  - node_modules
```

### 6.2 `Gemfile`

```ruby
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
gem "webrick", "~> 1.8"
```

### 6.3 GitHub Actions build

`.github/workflows/pages.yml` uses `actions/jekyll-build-pages` + `actions/deploy-pages`. Repo Settings → Pages → Source = **GitHub Actions**.

## 7. Anti-patterns (collected from baseline tests)

| Default tendency | Why wrong | Replace with |
|------------------|-----------|--------------|
| Inter / JetBrains Mono | Not the brand | IBM Plex Mono everywhere |
| `border-radius: 8px` | Softens neo-brutalism | `--radius: 0` always |
| Tailwind / Bootstrap | Adds 200KB toolchain | 39KB hand-written CSS |
| `box-shadow: 0 4px 12px rgba(0,0,0,.1)` | Material-style blur | `Npx Npx 0 var(--border)` solid |
| Single accent | Loses category mapping | All 8 accents + eyebrow map |
| `[data-theme="dark"]` toggle | Two-theme assumption | Four themes via body class |
| `prefers-color-scheme` only | No user override | `<select>` + localStorage |
| Minima theme inheritance | Brings unwanted styles | `theme: null` + own layouts |
| `.nojekyll` at root | Disables layouts | Remove it |
| Hard-coded `/repo-name/` paths | Breaks on forks | `{{ '/' \| relative_url }}` |

## 8. Reference URLs

- ai-workbench landing (richest sample): https://amit-t.github.io/ai-workbench/
- ai-workbench raw CSS: https://amit-t.github.io/ai-workbench/assets/css/site.css
- ai-workbench raw JS: https://amit-t.github.io/ai-workbench/assets/js/site.js
- ai-devkit: https://amit-t.github.io/ai-devkit/
- ai-ralph: https://amit-t.github.io/ai-ralph/
- skills: https://amit-t.github.io/skills/
