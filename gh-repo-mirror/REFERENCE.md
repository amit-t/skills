# gh-repo-mirror — Reference

Deep-dive notes, gotchas, and API payloads that don't belong in the lean `SKILL.md`.

## Multi-account gh CLI

If the user has more than one logged-in account (`gh auth status` lists several), the **active** account is used by every `gh api` call. A reference repo in a corporate org may 404 under a personal account.

```zsh
gh auth status                       # see all logged-in handles
gh api user --jq .login              # which one is active
gh auth switch --user <handle>       # switch
```

Switch before invoking the helper script.

## Finding the right org

The user's "org name" is often informal. Resolve the actual login:

```zsh
gh api user/orgs --jq '.[].login'    # all orgs the active account belongs to
gh repo list <org> --limit 100 | grep -i <fragment>
gh search repos <repo-name>          # global search fallback
```

## Reference-repo settings to capture

```zsh
gh api repos/<org>/<ref> | jq '{
  visibility, default_branch,
  has_issues, has_projects, has_wiki, has_discussions,
  is_template, allow_forking, web_commit_signoff_required,
  allow_squash_merge, allow_merge_commit, allow_rebase_merge,
  allow_auto_merge, delete_branch_on_merge, allow_update_branch,
  squash_merge_commit_message, squash_merge_commit_title,
  merge_commit_message, merge_commit_title,
  security_and_analysis
}'
```

Branch protection:

```zsh
gh api repos/<org>/<ref>/branches/main/protection
```

Pages:

```zsh
gh api repos/<org>/<ref>/pages
```

## Creating the new repo

```zsh
gh repo create <org>/<name> --private --description "<desc>"
```

`--public` / `--internal` if the reference uses those. `--template` flag on `gh repo create` does NOT set `is_template` on the new repo — it copies from a template source. To set `is_template=true` on the new repo, PATCH after creation.

## Settings PATCH

```zsh
gh api -X PATCH repos/<org>/<name> \
  -F has_issues=true -F has_projects=true -F has_wiki=true \
  -F has_discussions=false \
  -F is_template=false \
  -F allow_squash_merge=true -F allow_merge_commit=true -F allow_rebase_merge=true \
  -F allow_auto_merge=false \
  -F delete_branch_on_merge=false -F allow_update_branch=false \
  -F web_commit_signoff_required=false \
  -f squash_merge_commit_message=COMMIT_MESSAGES \
  -f squash_merge_commit_title=COMMIT_OR_PR_TITLE \
  -f merge_commit_message=PR_TITLE \
  -f merge_commit_title=MERGE_MESSAGE
```

**Gotcha**: orgs that prohibit private-repo forking reject any `allow_forking` field with HTTP 422 ("This organization does not allow private repository forking"), even when you pass `false`. The org default already enforces it. The script catches 422, strips `allow_forking`, retries.

## Security-and-analysis PATCH

Must go in its own PATCH (different shape — nested object):

```zsh
gh api -X PATCH repos/<org>/<name> --input - <<'JSON'
{
  "security_and_analysis": {
    "advanced_security":                  {"status": "enabled"},
    "secret_scanning":                    {"status": "enabled"},
    "secret_scanning_push_protection":    {"status": "enabled"},
    "secret_scanning_non_provider_patterns":{"status":"enabled"},
    "secret_scanning_ai_detection":       {"status": "enabled"},
    "secret_scanning_validity_checks":    {"status": "enabled"}
  }
}
JSON
```

`advanced_security` requires GitHub Advanced Security on the org plan; will 422 otherwise.

## Branch protection PUT

Pass the reference response payload through (after stripping read-only `url`s):

```zsh
gh api -X PUT repos/<org>/<name>/branches/main/protection --input - <<'JSON'
{
  "required_status_checks": null,
  "enforce_admins": false,
  "required_pull_request_reviews": null,
  "restrictions": null,
  "required_linear_history": false,
  "allow_force_pushes": false,
  "allow_deletions": false,
  "block_creations": false,
  "required_conversation_resolution": false,
  "lock_branch": false,
  "allow_fork_syncing": false,
  "required_signatures": false
}
JSON
```

All seven required top-level keys must be present even if `null`. The API will reject partial payloads.

## Pages enable

```zsh
gh api -X POST repos/<org>/<name>/pages --input - <<'JSON'
{ "source": {"branch": "main", "path": "/docs"}, "build_type": "legacy" }
JSON
```

`/docs` keeps repo root clean for skill directories (`<slug>/SKILL.md`). `/` matches references like `amit-t/skills`. Custom domain is picked up automatically from `docs/CNAME` (or `CNAME` at root) on the next build.

`build_type: legacy` is Jekyll-or-static. `workflow` is GitHub-Actions-driven. Mirror the reference.

**Private-repo Pages requires GitHub Enterprise Cloud.** Free/Pro orgs can only host Pages from public repos. The skill should fail loudly if the target org plan doesn't allow it.

## HTTPS enforcement — async cert

Immediately after `POST /pages`, the cert isn't issued yet. Attempting `PUT /pages {"https_enforced": true}` returns:

```
{"message":"The certificate does not exist yet","status":"404"}
```

Solution: poll until issued, then PUT.

```zsh
until gh api repos/<org>/<name>/pages \
  | jq -e '.https_certificate.state == "approved"' >/dev/null 2>&1; do
  sleep 30
done
gh api -X PUT repos/<org>/<name>/pages --input - <<<'{"https_enforced": true}'
```

The script runs this poll in the background so the user gets a notification when it lands, rather than blocking on it. Typical wait: 2–10 minutes for a verified org domain.

## Templates

Placeholders use double curly braces. `scripts/mirror-repo.zsh` performs simple `sed` substitution:

| Placeholder | Example |
|-------------|---------|
| `{{REPO_URL}}` | `https://github.com/Invenco-Cloud-Systems-ICS/ai-skills` |
| `{{REPO_SLUG}}` | `Invenco-Cloud-Systems-ICS/ai-skills` |
| `{{HERO_EYEBROW}}` | `INVENCO CLOUD SYSTEMS` |
| `{{LAST_UPDATE}}` | `2026-05-12` (ISO date) |
| `{{DESCRIPTION}}` | one-line repo description |
| `{{CUSTOM_DOMAIN}}` | `ai-skills.docs.invencocloud.com` (omitted from CNAME if blank) |

## `.nojekyll`

GitHub Pages assumes Jekyll. A static HTML/CSS/JS site (no `_config.yml`) still gets a Jekyll pass that **drops files starting with `_` or `.`**. The empty `.nojekyll` marker disables Jekyll entirely. Put it next to `index.html` (in `docs/` when source is `/docs`, at repo root when source is `/`).

## Mirroring rulesets (--mirror-rulesets)

Classic branch protection (covered above) and repo-level **rulesets** are two parallel systems on GitHub. Modern orgs increasingly use rulesets because they're versioned, target multiple refs, and support bypass actors. The skill copies them via:

```zsh
gh api repos/<ref>/rulesets                       # list summaries
gh api repos/<ref>/rulesets/<id>                  # full definition
```

POST to the new repo after stripping server-managed fields:

```zsh
jq 'del(.id, .source, .source_type, .created_at, .updated_at, ._links, .node_id, .current_user_can_bypass)' <full>
```

Then POST to `repos/<new>/rulesets`. If a same-named ruleset already exists on the new repo (e.g. on a re-run), the script falls back to PUT against the existing id so the operation is idempotent.

**Caveat**: rulesets can reference org-level actor IDs (teams, custom roles). Those IDs are valid across repos in the same org but won't resolve if you mirror across orgs. Cross-org mirroring may need manual cleanup.

## Mirroring access: teams + direct collaborators (default-on, `--no-mirror-access` to skip)

Repo settings and branch protection don't carry **who** can access the repo. Two separate API surfaces govern that:

```zsh
gh api --paginate repos/<ref>/teams                              # teams with access + permission
gh api --paginate "repos/<ref>/collaborators?affiliation=direct"  # users granted directly (not via teams/org)
```

The skill copies both by default. Skip with `--no-mirror-access`.

**Teams** — `PUT /orgs/{org}/teams/{slug}/repos/{owner}/{repo}` with body `{"permission": "<pull|triage|push|maintain|admin>"}`. Permission values come back from the GET in the right form already.

**Direct collaborators** — `PUT /repos/{owner}/{repo}/collaborators/{login}` with body `{"permission": "..."}`. Caveat: GET returns `role_name` in the *display* vocabulary (`read`/`triage`/`write`/`maintain`/`admin`) but PUT expects the *API* vocabulary (`pull`/`triage`/`push`/`maintain`/`admin`). The script's `role_to_permission` helper maps `read→pull`, `write→push`, leaves the others alone.

**Cross-org caveat**: team slugs are scoped to the target org, not the reference org. If you mirror `acme-corp/foo` → `widgets-inc/bar`, the team `acme-corp/security-admins` does not auto-create in `widgets-inc`. The PUT will 404 and the script logs a warning per team. Only teams that already exist in the new org will resolve. For same-org mirrors this is a non-issue.

**Pending invites**: direct-collaborator PUTs create *invitations*. The diff at the end of the run may show drift on `collaborators` until the invitee accepts. That's expected — not a failure.

## DNS CNAME (--cname-provider)

GitHub Pages needs a `CNAME <custom-domain> -> <org-lowercased>.github.io` record before it can issue the Let's Encrypt cert. The skill handles two providers:

**`--cname-provider cloudflare --cname-zone-id <id>`** — POSTs to `https://api.cloudflare.com/client/v4/zones/<zone-id>/dns_records` with `Authorization: Bearer $CLOUDFLARE_API_TOKEN`. Token needs `Zone.DNS:Edit` permission on the zone. The script proxies-off by default (`"proxied": false`) since Pages requires DNS-only for cert issuance. If the record already exists Cloudflare returns an error containing "already exists" and the script treats that as a no-op.

**`--cname-provider print`** — just emits the record the operator must create in any other DNS provider (Route 53, GCP Cloud DNS, manual zone file, etc.). Default when no provider is given is to skip DNS entirely; the operator handles it out-of-band.

Both modes are paired with `--custom-domain`. Without a custom domain there's no record to make.

## Bootstrapping a starter skill (--bootstrap-skill)

When the new repo's first commit shouldn't be empty placeholder arrays, pass `--bootstrap-skill <slug>` to drop:

- `<slug>/SKILL.md` — frontmatter + sections to fill in (Quick start, Workflow, Inputs, Outputs, Gotchas).
- `<slug>/README.md` — quick install + usage snippet.
- An entry inside the `const skills = [];` literal in `docs/site.js`, splicing in slug/name/category/tagline/detail/usage placeholders so the Pages site renders a card.

Slug must be lowercase kebab-case (matches `^[a-z0-9][a-z0-9-]*$`). The agent should expect to fill in the placeholders before opening a PR — the bootstrap step makes a working scaffold, not finished content.

## Verification

After the script finishes, it runs:

```zsh
diff <(gh api repos/<org>/<ref>     | jq -S '<settings-projection>') \
     <(gh api repos/<org>/<new>     | jq -S '<settings-projection>')
diff <(gh api repos/<org>/<ref>/branches/main/protection | jq -S 'del(.url, .[].url)') \
     <(gh api repos/<org>/<new>/branches/main/protection | jq -S 'del(.url, .[].url)')
diff <(gh api --paginate repos/<org>/<ref>/teams | jq -S '[.[] | {slug, permission}] | sort_by(.slug)') \
     <(gh api --paginate repos/<org>/<new>/teams | jq -S '[.[] | {slug, permission}] | sort_by(.slug)')
diff <(gh api --paginate "repos/<org>/<ref>/collaborators?affiliation=direct" | jq -S '[.[] | {login, role_name}] | sort_by(.login)') \
     <(gh api --paginate "repos/<org>/<new>/collaborators?affiliation=direct" | jq -S '[.[] | {login, role_name}] | sort_by(.login)')
```

Empty diff = success. Any drift is printed for the operator to review. Expected non-empty diffs: `is_template` when the caller chose differently; collaborator entries while invitations are still pending acceptance; cross-org team mirroring when some teams don't exist in the target org.
