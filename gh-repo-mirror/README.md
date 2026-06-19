# gh-repo-mirror

> Scaffold a new GitHub repo that mirrors an existing reference repo's settings, branch protection, security flags, and (optionally) its GitHub Pages site

**Category:** Engineering

Given a reference repo and a new repo name, this skill produces a new repo with identical general settings, security-and-analysis, classic branch protection on `main` (mirroring `required_status_checks` and `required_pull_request_reviews` faithfully where the reference sets them, not just force-push/deletion toggles), mirrored team access and direct collaborators, and an optional neo-brutalist GitHub Pages site under `docs/` (or `/`) — rebranded to the caller's slug and hero eyebrow. Custom domain is wired via `docs/CNAME` and HTTPS is enforced automatically once the Let's Encrypt cert lands. Optional extras: copy repo-level rulesets, create the CNAME DNS record via Cloudflare, and bootstrap a starter skill so the initial commit isn't empty.

## Install

Install using the [`skills`](https://github.com/vercel-labs/skills) CLI:

```bash
npx skills@latest add amit-t/skills --skill gh-repo-mirror
```

Install all skills from this repository:

```bash
npx skills@latest add amit-t/skills
```

### Manual Installation

<details>
<summary>Devin / Windsurf</summary>

```bash
# Project-level
cp -r gh-repo-mirror .cognition/skills/gh-repo-mirror
# or
cp -r gh-repo-mirror .windsurf/skills/gh-repo-mirror

# Global
cp -r gh-repo-mirror ~/.config/cognition/skills/gh-repo-mirror
```

</details>

<details>
<summary>Claude Code</summary>

```bash
# Project-level
cp -r gh-repo-mirror .claude/skills/gh-repo-mirror

# Global
cp -r gh-repo-mirror ~/.claude/skills/gh-repo-mirror
```

</details>

<details>
<summary>Cursor</summary>

```bash
# Project-level
cp -r gh-repo-mirror .cursor/skills/gh-repo-mirror
```

</details>

<details>
<summary>Codex</summary>

```bash
# Copy SKILL.md content into your codex instructions
cat gh-repo-mirror/SKILL.md >> AGENTS.md
```

</details>

<details>
<summary>Gemini CLI</summary>

```bash
# Copy SKILL.md content into your Gemini instructions
cat gh-repo-mirror/SKILL.md >> GEMINI.md
```

</details>

## Usage

Once installed, invoke in your agent session:

```
/gh-repo-mirror
```

Or run the helper script directly:

```bash
.claude/skills/gh-repo-mirror/scripts/mirror-repo.zsh \
  --ref-repo <org>/<reference-repo> \
  --new-repo <org>/<new-repo> \
  --description "<one-line description>" \
  --pages-path /docs \
  --custom-domain <optional-custom-domain>
```

Useful flags:

- `--template` — set `is_template=true` on the new repo
- `--no-port-docs` — skip the docs/Pages scaffold (a minimal `README` + `.gitignore` commit is still created so `main` exists for branch protection, Pages, and access steps)
- `--no-pages` — do not enable GitHub Pages on the new repo (also skips the HTTPS-enforce watcher); pair with `--no-port-docs` to mirror only settings, security, branch protection, and access with no site
- `--no-mirror-access` — skip mirroring teams + direct collaborators (both are mirrored by default)
- `--mirror-rulesets` — also copy repo-level rulesets
- `--cname-provider cloudflare --cname-zone-id <id>` — create the DNS record via Cloudflare (needs `CLOUDFLARE_API_TOKEN`)
- `--cname-provider print` — emit the DNS record for manual creation
- `--bootstrap-skill <slug>` — drop a placeholder skill + site entry so the first commit isn't empty
- `--dry-run` — print the plan without changing anything
- `--enforce-https-only <org>/<name>` — re-run only the HTTPS enforcement step (for when the cert was still pending at end of a prior run)

Requires `gh` CLI authenticated against an account with access to both the reference org and create-repo rights in the target org.

## Source

Bundled scripts and templates ship inside the skill directory — see `SKILL.md` and `REFERENCE.md` for the full workflow, API payloads, and gotchas (multi-account `gh` auth, `allow_forking=false` 422, async HTTPS cert provisioning, Pages-path tradeoff, `.nojekyll` requirement, ruleset payload trimming, Cloudflare DNS API).

## License

MIT
