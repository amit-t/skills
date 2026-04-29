---
name: gh-pages-neo-brutalist
description: Use when scaffolding a GitHub Pages site for a new (or existing) repo and you want it to match the amit-t neo-brutalist design system shared by ai-workbench, ai-devkit, ai-ralph, and amit-t/skills. Drops in Jekyll layouts, design tokens, four-theme switcher (light/dark/cyberpunk/solarized), copy buttons, and a hero/nav/markdown-body system in one shot.
---

# GitHub Pages — Neo-Brutalist (amit-t house style)

## Overview

Every repo amit-t publishes ships a GitHub Pages site that looks the same: hard 3px borders, 5/8 px offset solid shadows, IBM Plex Mono everywhere, eight saturated accents (hot-pink / lime-green / electric-blue / cyan / yellow / coral / orange / purple), four themes via `<select>` (light, dark, cyberpunk grid, solarized IDE).

This skill packages that system as drop-in Jekyll templates plus a scaffolder. Use it the moment a repo gets created so the page lands in style on day one.

## When to Use

- New repo created under amit-t (or any repo that needs to match house style)
- Existing repo has no Pages site yet, or has a generic minima/cayman theme to replace
- User asks for "GitHub page", "landing page", "docs site" for a repo
- User mentions "neo-brutalist", "amit-t style", "match ai-workbench look", "house design system"

**Skip when:** target repo already wires its own Pages build (Next.js, Astro, Docusaurus, MkDocs); the repo is a fork that must keep upstream docs.

## When NOT to Use

- Production marketing sites needing CMS / dynamic routing
- Sites that must avoid Google Fonts (privacy-first)
- Repos forbidden from running Jekyll (rare; Pages runs Jekyll by default)

## Core Pattern

```
repo-root/
  _config.yml              # baseurl = /<repo>, theme: null, plugins
  Gemfile                  # github-pages gem
  _layouts/
    base.html              # head, theme-switcher, site-nav, footer, scripts
    home.html              # base + .hero + .markdown-body
    page.html              # base + .doc-hero + .breadcrumbs + .markdown-body
  assets/
    css/site.css           # 39KB — copied verbatim, design tokens + 4 themes
    js/site.js             # theme switcher (localStorage) + copy buttons
  .github/workflows/
    pages.yml              # GitHub Actions Pages build
  index.md                 # front-matter: layout: home, hero_*: ...
```

Front-matter the page wants:

```yaml
---
layout: home          # or 'page' for docs
title: Repo Tagline
hero_eyebrow: BADGE TEXT
hero_title: Big Headline.
hero_desc: One-paragraph promise.
hero_actions:
  - { label: "Get Started", href: "./getting-started.html", primary: true }
  - { label: "GitHub", href: "https://github.com/...", external: true }
---
```

## Quick Reference (design tokens)

| Token | Value | Use |
|-------|-------|-----|
| `--border-w` | `3px` | every box outline |
| `--shadow-sm/md/lg` | `3/5/8 px Npx 0` | drop shadows (no blur) |
| `--radius` | `0px` | always square |
| `--hot-pink` | `#ff00f5` | primary CTA, brand |
| `--lime-green` | `#afff00` | hero eyebrow, active filter |
| `--electric-blue` | `#0052ff` | engineering eyebrow, links |
| `--cyan-accent` | `#00c1d4` | table header, agent eyebrow |
| `--yellow-accent` | `#ffef00` | hover highlight, AI eyebrow |
| `--vibrant-orange` | `#ff4911` | proj eyebrow, code text |
| `--warm-coral` | `#ff5f5f` | PM eyebrow |
| `--purple-accent` | `#5b2eff` | UX eyebrow |
| Font | IBM Plex Mono 400/500/600/700 | EVERYTHING — body, headings, code |
| `body` font-size | `15px`, line-height `1.6` | base |
| `h1` | `clamp(2.5rem, 6vw, 4.5rem)`, weight 700, tracking `-0.03em` | hero |

Eyebrow colour map: `eyebrow-pm` coral, `eyebrow-eng` blue, `eyebrow-ux` purple, `eyebrow-agent` cyan, `eyebrow-ai` yellow, `eyebrow-readme` lime, `eyebrow-changelog` pink, `eyebrow-proj` orange.

Components (full list + markup) → `REFERENCE.md`.

## Implementation

### One-shot scaffold

From the target repo root:

```sh
zsh /path/to/at-skills/gh-pages-neo-brutalist/scaffold.zsh
```

Prompts for repo name + tagline + GitHub URL, copies `templates/` into the repo, rewrites baseurl in `_config.yml`, swaps placeholders in `index.md`, ensures `.nojekyll` is **NOT** present (Pages must run Jekyll), commits nothing.

Re-run is safe: existing files are left alone unless `--force` is passed.

### Manual scaffold

```sh
SRC=/path/to/at-skills/gh-pages-neo-brutalist/templates
cp -R "$SRC"/. .
sed -i '' "s|REPLACE_BASEURL|/$(basename $PWD)|" _config.yml
```

### Enable Pages

GitHub repo → Settings → Pages → Source = **GitHub Actions**. The included `.github/workflows/pages.yml` does the build.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Adds `.nojekyll` at repo root | Delete it. The system needs Jekyll to render layouts. |
| Picks Inter / JetBrains Mono | Replace with IBM Plex Mono. The whole system is monospace. |
| Uses `border-radius` > 0 | Set to 0. Square corners are non-negotiable. |
| Adds blur to box-shadow | Use `Npx Npx 0 colour` — solid offset only. |
| Switches accent to single hue | Keep all eight. The colour map maps to skill / section taxonomy. |
| Single theme | Ship all four — light, dark, cyberpunk, solarized. Switcher is in `site.js`. |
| Hard-codes `/repo-name/` paths | Use `{{ '/path' \| relative_url }}` so baseurl works across forks. |
| Replaces neo-btn with default button | Keep `.neo-btn` — translate-on-hover + shadow-jump is the system's signature. |
| Kramdown `<pre>` inherits code styling | Already neutralised in CSS via `.markdown-body pre code *`. Don't re-skin. |

## Red Flags — STOP and Re-check

- About to install Tailwind / Bootstrap / Pico CSS → STOP. The system is plain CSS with custom properties.
- Adding a CSS framework "to make it nicer" → STOP. Boldness comes from tokens, not utilities.
- Reaching for `prefers-color-scheme` only → STOP. Use the four-theme `<select>` pattern.
- Templating with React / Vue → STOP. Pure Jekyll. No build toolchain beyond Pages.
- Replacing IBM Plex Mono "for legibility" → STOP. The mono is the brand.

## Verification Checklist

After scaffolding, before committing:

- [ ] `_config.yml` `baseurl: /<repo-name>` set
- [ ] `assets/css/site.css` byte-identical to `templates/assets/css/site.css`
- [ ] `assets/js/site.js` byte-identical to `templates/assets/js/site.js`
- [ ] `index.md` front-matter has `layout: home` + hero fields
- [ ] No `.nojekyll` at repo root
- [ ] `.github/workflows/pages.yml` present
- [ ] Pages source = GitHub Actions
- [ ] `bundle exec jekyll serve` (if Ruby installed) renders without errors
- [ ] Theme switcher cycles 4 themes; localStorage key `wb-theme` set
- [ ] `<pre>` blocks show **Copy** button on hover

## See Also

- `REFERENCE.md` — every CSS class, every token, every component with full markup
- `scaffold.zsh` — interactive scaffolder
- Sample sites (live):
  - https://amit-t.github.io/ai-workbench/
  - https://amit-t.github.io/ai-devkit/
  - https://amit-t.github.io/ai-ralph/
  - https://amit-t.github.io/skills/
