# gh-pages-neo-brutalist

Drop-in Jekyll templates that scaffold a GitHub Pages site matching the amit-t neo-brutalist house design system.

Used by:

- [`ai-workbench`](https://amit-t.github.io/ai-workbench/)
- [`ai-devkit`](https://amit-t.github.io/ai-devkit/)
- [`ai-ralph`](https://amit-t.github.io/ai-ralph/)
- [`amit-t/skills`](https://amit-t.github.io/skills/)

## What it ships

- `templates/_layouts/{base,home,page}.html` — Jekyll layouts with theme-switcher, site nav, hero, markdown-body, footer
- `templates/assets/css/site.css` — 39 KB of design tokens, components, four themes (light, dark, cyberpunk grid, solarized IDE)
- `templates/assets/js/site.js` — theme switcher (localStorage `wb-theme`) + `<pre>` copy buttons
- `templates/_config.yml`, `templates/Gemfile` — Jekyll on GitHub Pages, no Node toolchain
- `templates/index.md` — landing page with hero front-matter pre-filled
- `templates/.github/workflows/pages.yml` — Pages build via GitHub Actions
- `scaffold.zsh` — one-shot scaffolder, interactive prompts

## Install

```sh
npx skills@latest add amit-t/skills --skill gh-pages-neo-brutalist
```

Or manually:

```sh
git clone https://github.com/amit-t/skills /tmp/skills
cp -R /tmp/skills/gh-pages-neo-brutalist ~/.claude/skills/
```

## Use

From inside the target repo:

```sh
zsh ~/.claude/skills/gh-pages-neo-brutalist/scaffold.zsh
```

Then in GitHub: **Settings → Pages → Source: GitHub Actions**.

## See

- `SKILL.md` — when-to-use, core pattern, tokens table, common mistakes, red flags
- `REFERENCE.md` — every component with markup, full design-token table, theme palette breakdown
