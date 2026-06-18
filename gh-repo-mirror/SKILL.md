---
name: gh-repo-mirror
description: Scaffold a new GitHub repo that mirrors an existing reference repo's general settings, branch-protection rules, security flags, and (optionally) its GitHub Pages site — porting the static HTML/CSS/JS docs and rebranding them. Use when the user says "create a new repo like X", "mirror settings from Y", "new repo same as Z with Pages", or asks for a skills-library / Pages-site scaffold modelled on another repo.
---

# gh-repo-mirror

## What this does

Given a **reference repo** (e.g. `org/ai-workbench`), produces a **new repo** (e.g. `org/ai-skills`) with:

1. Identical general settings: visibility, has_issues/projects/wiki/discussions, is_template flag (caller decides), all merge methods + commit-message/title flags, delete-branch-on-merge, allow-update-branch, allow-forking, web-commit-signoff.
2. Identical security-and-analysis: advanced_security, secret_scanning, push_protection, non_provider_patterns, ai_detection, validity_checks, dependabot_security_updates.
3. Identical classic branch protection on `main`.
4. Identical access: every team that has access to the reference repo is added to the new repo with the same permission (pull/triage/push/maintain/admin); direct collaborators are invited at the same permission. Default-on; pass `--no-mirror-access` to skip.
5. A bundled neo-brutalist GitHub Pages docs site under `docs/` (or `/`, caller picks) with the caller's branding, empty `skills[]` and `changes[]` so content lands as you add it.
6. Custom domain wired via `docs/CNAME` (if provided) and HTTPS enforced once the cert is issued.

## Quick start

Run the helper script with the reference repo + new repo name. It interviews for anything you don't pass:

```bash
.claude/skills/gh-repo-mirror/scripts/mirror-repo.zsh \
  --ref-repo Invenco-Cloud-Systems-ICS/ai-workbench \
  --new-repo Invenco-Cloud-Systems-ICS/ai-skills \
  --description "AI agent skills library for Invenco" \
  --pages-path /docs \
  --custom-domain ai-skills.docs.invencocloud.com
```

Add `--template` to set `is_template=true`, `--no-port-docs` to skip the docs/Pages scaffold (a minimal README + `.gitignore` commit is still created so `main` exists for branch protection), `--no-pages` to skip enabling GitHub Pages entirely, `--dry-run` to print the plan without changing anything.

**Default-on capability** (suppress with a flag):

- Team + direct-collaborator access mirroring runs on every invocation. Pass `--no-mirror-access` to skip. Team slugs are scoped to the new repo's org — if the reference is in a different org, only teams that already exist in the target org will resolve; the rest log a warning.

**Extra capabilities** (all opt-in):

- `--mirror-rulesets` — also copy repo-level rulesets from the reference (in addition to classic branch protection).
- `--cname-provider cloudflare --cname-zone-id <id>` — create the DNS CNAME record for the custom domain via the Cloudflare API. Needs `CLOUDFLARE_API_TOKEN` in env. Use `--cname-provider print` to just emit the record the operator should create manually in any other provider.
- `--bootstrap-skill <slug>` — drop a placeholder skill at `<slug>/SKILL.md` and insert a matching entry into `docs/site.js` so the initial commit has real (template) content instead of empty arrays.

## Workflow

1. **Verify gh CLI auth.** `gh api user --jq .login` must match an account that can access **both** the reference org and create repos in the target org. Switch with `gh auth switch --user <handle>` if wrong. If the reference repo 404s, search orgs with `gh api user/orgs --jq '.[].login'` and `gh repo list <org>`.
2. **Run `scripts/mirror-repo.zsh`** with the flags above. The script:
   - Captures the reference repo's settings, branch protection, and Pages config.
   - Creates the new repo (`gh repo create`).
   - PATCHes general settings + security flags. If `allow_forking=false` PATCH returns HTTP 422 ("organization does not allow private repository forking"), drops that one flag and retries — the org default already enforces it.
   - Renders templates under `docs/` (or `/`) with the caller's `repoSlug`, `repoUrl`, hero eyebrow, and date stamps. Copies `.nojekyll`, optional `CNAME`.
   - Writes `README.md`, `CHANGELOG.md`, `.gitignore` at repo root.
   - `git init -b main`, commits, pushes.
   - PUTs classic branch protection mirroring the reference faithfully — including `required_status_checks` (strict + contexts) and `required_pull_request_reviews` (code-owner reviews, approval count, dismiss-stale) where the reference sets them, not just `allow_force_pushes`/`allow_deletions`. `restrictions`/`dismissal_restrictions`/bypass actors are intentionally omitted (org-scoped, may not resolve).
   - Mirrors team access (`PUT /orgs/{org}/teams/{slug}/repos/{owner}/{repo}`) and direct collaborators (`PUT /repos/{owner}/{repo}/collaborators/{login}`) at the same permission level as the reference. Skipped if `--no-mirror-access` is set.
   - POSTs Pages config with `source: {branch: main, path: /docs|/}` and `build_type: legacy`.
   - Background-polls for the Let's Encrypt cert (`https_certificate.state == "approved"`), then PUTs `https_enforced=true`.
3. **Verify by diff.** Script prints a side-by-side of settings, branch protection, teams, and direct collaborators between reference and new repo. Any drift is highlighted.

## Inputs the skill asks for if not passed

- Reference repo (`<org>/<name>`)
- New repo (`<org>/<name>`) — org defaults to reference org
- Description
- `is_template`: true / false
- Pages source path: `/docs` (recommended — keeps repo root clean for skill dirs) or `/` (matches some references like `amit-t/skills`)
- Custom domain (optional, e.g. `ai-skills.docs.invencocloud.com`)
- Port docs verbatim from bundled template, or skip docs scaffold entirely
- Hero eyebrow text for the Pages site (e.g. `INVENCO CLOUD SYSTEMS`)

## Templates bundled

Under `templates/`:

- `index.html` — neo-brutalist hero, README card, skill grid, changelog, drawer. Placeholders: `{{REPO_URL}}`, `{{REPO_SLUG}}`, `{{HERO_EYEBROW}}`, `{{LAST_UPDATE}}`.
- `site.css` — full design system (themes, IBM Plex Mono, hard borders, offset shadows). Verbatim copy.
- `site.js` — render logic with empty-state handling. Placeholders: `{{REPO_URL}}`, `{{REPO_SLUG}}`.
- `nojekyll` — empty file copied as `.nojekyll`.
- `README.md.tmpl`, `CHANGELOG.md.tmpl`, `gitignore.tmpl` — repo-root scaffolding with the same placeholders.

## Known gotchas

See [REFERENCE.md](REFERENCE.md) for: multi-account gh auth, the `allow_forking=false` 422, async HTTPS cert provisioning, Pages-path tradeoff, `.nojekyll` requirement, private-repo Pages requires GitHub Enterprise, ruleset mirror payload trimming, Cloudflare DNS API auth.

## After the skill runs

You should see:

- Repo URL printed.
- Pages URL printed (custom domain or `<org>.github.io/<name>`).
- A line stating whether HTTPS enforcement is **enforced** (cert was ready) or **pending** (background poll is armed; will flip when the cert lands — usually a few minutes).
- A diff block showing zero drift between reference and new repo (modulo intentional differences like `is_template`).

If HTTPS enforcement is pending and the session ends, re-run:

```bash
.claude/skills/gh-repo-mirror/scripts/mirror-repo.zsh --enforce-https-only <org>/<name>
```
