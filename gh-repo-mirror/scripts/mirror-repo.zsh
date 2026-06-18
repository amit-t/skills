#!/usr/bin/env zsh
# gh-repo-mirror — scaffold a new GitHub repo whose settings, branch protection,
# security flags, and (optionally) GitHub Pages site mirror an existing reference repo.
#
# Idempotent: rerunning is safe; existing repos / Pages / protection rules are
# detected and skipped or PATCHed in place rather than errored.

set -euo pipefail

# Capture script path BEFORE any function defines $0 to itself.
script_path=${0:A}
script_dir=${script_path:h}
templates_dir=${script_dir:h}/templates

# ───────────────────────────── helpers ─────────────────────────────

print_err()    { print -u2 -r -- "✗ $*"; }
print_info()   { print -r -- "→ $*"; }
print_ok()     { print -r -- "✓ $*"; }
print_warn()   { print -u2 -r -- "! $*"; }
die()          { print_err "$*"; exit 1; }

require_cmd() {
  (( $+commands[$1] )) || die "$1 not found in PATH"
}

usage() {
  cat <<EOF
Usage: mirror-repo.zsh [flags]

Required:
  --ref-repo      <org>/<name>   reference repo to mirror
  --new-repo      <org>/<name>   new repo to create

Optional:
  --description   <text>         repo description
  --pages-path    /docs | /      Pages source path (default /docs)
  --custom-domain <fqdn>         custom domain for Pages (sets CNAME)
  --hero-eyebrow  <text>         hero eyebrow on the docs site (default: org name uppercased)
  --template                     set is_template=true on the new repo
  --no-port-docs                 skip the docs/ scaffold entirely (still creates a minimal
                                 README + .gitignore commit so 'main' exists for branch protection)
  --no-pages                     do not enable GitHub Pages on the new repo
  --from-repo     <org>/<name>   port Pages content from a different repo instead of bundled templates
  --visibility    private|public|internal   override (default: match reference)
  --mirror-rulesets              also mirror repo-level rulesets from the reference
  --no-mirror-access             skip mirroring teams + direct collaborators
                                 (by default, both are mirrored from the reference)
  --cname-provider <name>        create the DNS CNAME for --custom-domain. Supported: cloudflare, print
                                 cloudflare needs --cname-zone-id and \$CLOUDFLARE_API_TOKEN.
                                 print just emits the record the user must create manually.
  --cname-zone-id <id>           Cloudflare zone ID (when --cname-provider=cloudflare)
  --bootstrap-skill <slug>       drop a SKILL.md skeleton at <slug>/SKILL.md and add a docs/site.js entry
                                 so the initial commit contains real (placeholder) content
  --dry-run                      print plan, don't make changes
  --enforce-https-only <org>/<name>   skip everything; just poll cert + flip https_enforced=true
  -h, --help                     this help

The script interviews for any required flag that's missing.
EOF
}

# ───────────────────────────── arg parse ─────────────────────────────

ref_repo=""
new_repo=""
description=""
pages_path="/docs"
custom_domain=""
hero_eyebrow=""
template_flag="false"
port_docs="true"
enable_pages="true"
from_repo=""
visibility_override=""
dry_run="false"
enforce_https_only=""
mirror_rulesets="false"
mirror_access="true"
cname_provider=""
cname_zone_id=""
bootstrap_skill=""

while (( $# )); do
  case "$1" in
    --ref-repo)            ref_repo="$2"; shift 2;;
    --new-repo)            new_repo="$2"; shift 2;;
    --description)         description="$2"; shift 2;;
    --pages-path)          pages_path="$2"; shift 2;;
    --custom-domain)       custom_domain="$2"; shift 2;;
    --hero-eyebrow)        hero_eyebrow="$2"; shift 2;;
    --template)            template_flag="true"; shift;;
    --no-port-docs)        port_docs="false"; shift;;
    --no-pages)            enable_pages="false"; shift;;
    --from-repo)           from_repo="$2"; shift 2;;
    --visibility)          visibility_override="$2"; shift 2;;
    --mirror-rulesets)     mirror_rulesets="true"; shift;;
    --no-mirror-access)    mirror_access="false"; shift;;
    --cname-provider)      cname_provider="$2"; shift 2;;
    --cname-zone-id)       cname_zone_id="$2"; shift 2;;
    --bootstrap-skill)     bootstrap_skill="$2"; shift 2;;
    --dry-run)             dry_run="true"; shift;;
    --enforce-https-only)  enforce_https_only="$2"; shift 2;;
    -h|--help)             usage; exit 0;;
    *)                     die "Unknown flag: $1";;
  esac
done

# Validate cname-provider combinations.
case "$cname_provider" in
  ""|cloudflare|print) ;;
  *) die "--cname-provider must be one of: cloudflare, print";;
esac
if [[ "$cname_provider" == "cloudflare" && -z "$cname_zone_id" ]]; then
  die "--cname-provider=cloudflare requires --cname-zone-id"
fi
if [[ -n "$cname_provider" && -z "$custom_domain" ]]; then
  die "--cname-provider requires --custom-domain"
fi

require_cmd gh
require_cmd jq
require_cmd git
require_cmd sed

# ───────────── enforce-https-only fast path ─────────────

poll_and_enforce_https() {
  local repo=$1
  print_info "Polling for HTTPS cert on $repo (every 30s)…"
  until gh api "repos/$repo/pages" 2>/dev/null \
      | jq -e '.https_certificate.state == "approved"' >/dev/null 2>&1; do
    sleep 30
  done
  print_info "Cert approved; enforcing HTTPS"
  gh api -X PUT "repos/$repo/pages" --input - <<<'{"https_enforced": true}' >/dev/null
  print_ok  "HTTPS enforced on $repo"
}

if [[ -n "$enforce_https_only" ]]; then
  poll_and_enforce_https "$enforce_https_only"
  exit 0
fi

# ───────────────────────────── interview ─────────────────────────────

prompt_if_blank() {
  local var_name=$1 prompt_text=$2
  if [[ -z "${(P)var_name}" ]]; then
    print -n "$prompt_text "
    local answer
    read -r answer
    typeset -g "$var_name=$answer"
  fi
}

prompt_if_blank ref_repo "Reference repo (<org>/<name>):"
prompt_if_blank new_repo "New repo (<org>/<name>):"

[[ "$ref_repo" == */* ]] || die "ref-repo must be <org>/<name>"
[[ "$new_repo" == */* ]] || die "new-repo must be <org>/<name>"

new_org=${new_repo%/*}
new_name=${new_repo#*/}

# ───────────── auth + access sanity ─────────────

active_login=$(gh api user --jq .login 2>/dev/null) || die "gh not authenticated; run 'gh auth login'"
print_info "Active gh account: $active_login"

if ! gh api "repos/$ref_repo" >/dev/null 2>&1; then
  print_err "Cannot access reference repo $ref_repo as $active_login."
  print_warn "Try: gh auth status  (then gh auth switch --user <handle>)"
  print_warn "Or search orgs: gh api user/orgs --jq '.[].login'"
  exit 1
fi

# ───────────── capture reference state ─────────────

print_info "Fetching reference settings, branch protection, Pages config…"

ref_json=$(gh api "repos/$ref_repo")
ref_visibility=$(jq -r '.visibility' <<<"$ref_json")
ref_default_branch=$(jq -r '.default_branch' <<<"$ref_json")

# Override visibility if asked.
new_visibility=${visibility_override:-$ref_visibility}

ref_protection_json=""
gh api "repos/$ref_repo/branches/$ref_default_branch/protection" >/tmp/_ref_prot.$$.json 2>/dev/null \
  && ref_protection_json=$(< /tmp/_ref_prot.$$.json)
rm -f /tmp/_ref_prot.$$.json

ref_pages_json=""
gh api "repos/$ref_repo/pages" >/tmp/_ref_pages.$$.json 2>/dev/null \
  && ref_pages_json=$(< /tmp/_ref_pages.$$.json)
rm -f /tmp/_ref_pages.$$.json

ref_rulesets_json="[]"
if [[ "$mirror_rulesets" == "true" ]]; then
  gh api "repos/$ref_repo/rulesets" >/tmp/_ref_rs.$$.json 2>/dev/null \
    && ref_rulesets_json=$(< /tmp/_ref_rs.$$.json)
  rm -f /tmp/_ref_rs.$$.json
fi

ref_teams_json="[]"
ref_collabs_json="[]"
if [[ "$mirror_access" == "true" ]]; then
  gh api --paginate "repos/$ref_repo/teams" >/tmp/_ref_teams.$$.json 2>/dev/null \
    && ref_teams_json=$(< /tmp/_ref_teams.$$.json)
  rm -f /tmp/_ref_teams.$$.json
  gh api --paginate "repos/$ref_repo/collaborators?affiliation=direct" >/tmp/_ref_collabs.$$.json 2>/dev/null \
    && ref_collabs_json=$(< /tmp/_ref_collabs.$$.json)
  rm -f /tmp/_ref_collabs.$$.json
fi

# Default hero eyebrow = org name (uppercased, underscores→spaces).
if [[ -z "$hero_eyebrow" ]]; then
  hero_eyebrow=$(print -r -- "$new_org" | tr '[:lower:]' '[:upper:]' | tr '_-' '  ')
fi

# ───────────── dry-run summary ─────────────

cat <<EOF

Plan
────
  Reference:        $ref_repo  (visibility=$ref_visibility, default=$ref_default_branch)
  New repo:         $new_repo  (visibility=$new_visibility, is_template=$template_flag)
  Description:      ${description:-<none>}
  Port docs:        $port_docs  (pages path: $pages_path; minimal README+.gitignore commit always created)
  From-repo:        ${from_repo:-<bundled templates>}
  Custom domain:    ${custom_domain:-<none — github.io URL>}
  Hero eyebrow:     $hero_eyebrow
  Branch protect:   $([[ -n "$ref_protection_json" ]] && print -r -- "mirror reference" || print -r -- "<reference has none — skipping>")
  Pages config:     $([[ "$enable_pages" != "true" ]] && print -r -- "disabled (--no-pages)" || { [[ -n "$ref_pages_json" ]] && print -r -- "mirror reference (override path=$pages_path)" || print -r -- "enable fresh on $pages_path"; })
  Rulesets:         $([[ "$mirror_rulesets" == "true" ]] && print -r -- "mirror ($(jq 'length' <<<"$ref_rulesets_json") found on reference)" || print -r -- "skipped (pass --mirror-rulesets to enable)")
  Access:           $([[ "$mirror_access" == "true" ]] && print -r -- "mirror ($(jq 'length' <<<"$ref_teams_json") team(s), $(jq 'length' <<<"$ref_collabs_json") direct collaborator(s) on reference)" || print -r -- "skipped (--no-mirror-access)")
  DNS CNAME:        $([[ -n "$cname_provider" ]] && print -r -- "$cname_provider → ${custom_domain} -> ${new_org:l}.github.io" || print -r -- "skipped (pass --cname-provider to enable)")
  Bootstrap skill:  ${bootstrap_skill:-<none>}
EOF

if [[ "$dry_run" == "true" ]]; then
  print_info "Dry-run — exiting before changes."
  exit 0
fi

# ───────────── create repo (idempotent) ─────────────

if gh api "repos/$new_repo" >/dev/null 2>&1; then
  print_warn "Repo $new_repo already exists; skipping create"
else
  print_info "Creating $new_repo (visibility=$new_visibility)"
  vis_flag="--$new_visibility"
  if [[ -n "$description" ]]; then
    gh repo create "$new_repo" $vis_flag --description "$description" >/dev/null
  else
    gh repo create "$new_repo" $vis_flag >/dev/null
  fi
  print_ok "Created $new_repo"
fi

# ───────────── PATCH general settings ─────────────

patch_general_settings() {
  local include_forking=$1
  local payload
  payload=$(jq -n \
    --argjson r "$ref_json" \
    --argjson tmpl "$([[ $template_flag == true ]] && echo true || echo false)" \
    --argjson inc_fork "$([[ $include_forking == true ]] && echo true || echo false)" '
    ({
      has_issues:                      $r.has_issues,
      has_projects:                    $r.has_projects,
      has_wiki:                        $r.has_wiki,
      has_discussions:                 $r.has_discussions,
      is_template:                     $tmpl,
      allow_squash_merge:              $r.allow_squash_merge,
      allow_merge_commit:              $r.allow_merge_commit,
      allow_rebase_merge:              $r.allow_rebase_merge,
      allow_auto_merge:                $r.allow_auto_merge,
      delete_branch_on_merge:          $r.delete_branch_on_merge,
      allow_update_branch:             $r.allow_update_branch,
      web_commit_signoff_required:     $r.web_commit_signoff_required,
      squash_merge_commit_message:     $r.squash_merge_commit_message,
      squash_merge_commit_title:       $r.squash_merge_commit_title,
      merge_commit_message:            $r.merge_commit_message,
      merge_commit_title:              $r.merge_commit_title
    })
    + (if $inc_fork then {allow_forking: $r.allow_forking} else {} end)
  ')
  print -r -- "$payload" | gh api -X PATCH "repos/$new_repo" --input - >/dev/null
}

print_info "Applying general settings (mirroring reference)"
if ! patch_general_settings true 2>/tmp/_patch.$$.err; then
  if grep -q "does not allow private repository forking" /tmp/_patch.$$.err 2>/dev/null; then
    print_warn "Org rejects allow_forking flag; retrying without it (default already enforced)"
    patch_general_settings false
  else
    cat /tmp/_patch.$$.err >&2
    rm -f /tmp/_patch.$$.err
    die "Settings PATCH failed"
  fi
fi
rm -f /tmp/_patch.$$.err
print_ok "General settings applied"

# ───────────── PATCH security flags ─────────────

if jq -e '.security_and_analysis' <<<"$ref_json" >/dev/null 2>&1; then
  print_info "Applying security_and_analysis flags"
  sec_payload=$(jq -n --argjson r "$ref_json" '
    {security_and_analysis:
      ($r.security_and_analysis
        | with_entries(select(.value.status != null))
        | with_entries(.value = {status: .value.status}))}
  ')
  if ! print -r -- "$sec_payload" | gh api -X PATCH "repos/$new_repo" --input - >/dev/null 2>/tmp/_sec.$$.err; then
    print_warn "Security PATCH failed (often: GitHub Advanced Security not on org plan):"
    cat /tmp/_sec.$$.err >&2
  fi
  rm -f /tmp/_sec.$$.err
  print_ok "Security flags applied (or attempted)"
fi

# ───────────── scaffold local repo + docs ─────────────

# Always scaffold a minimal initial commit so `main` exists — branch protection,
# Pages, and team access all require the branch to be present on the remote.
workdir=$(mktemp -d -t gh-repo-mirror.XXXXXX)
print_info "Staging initial commit in $workdir"
pushd "$workdir" >/dev/null

today=$(date -u +%Y-%m-%d)
repo_url="https://github.com/$new_repo"

if [[ "$port_docs" == "true" ]]; then
  # Pick source for HTML/CSS/JS: bundled templates by default, or --from-repo clone.
  if [[ -n "$from_repo" ]]; then
    print_info "Cloning $from_repo to port Pages content"
    git clone --depth=1 "https://github.com/$from_repo.git" /tmp/_pages-src.$$ >/dev/null 2>&1 \
      || die "Failed to clone $from_repo"
    src_dir=/tmp/_pages-src.$$
    # locate the Pages source: prefer docs/ then root
    if [[ -f $src_dir/docs/index.html ]]; then src_pages=$src_dir/docs
    elif [[ -f $src_dir/index.html ]]; then src_pages=$src_dir
    else die "No index.html in $from_repo at /docs or /"
    fi
  else
    src_pages=$templates_dir
  fi

  # Destination for docs: docs/ or repo root
  if [[ "$pages_path" == "/docs" ]]; then
    docs_dest="docs"
    mkdir -p docs
  else
    docs_dest="."
  fi

  # Copy HTML/CSS/JS (only files that exist in src_pages).
  for f in index.html site.css site.js; do
    [[ -f $src_pages/$f ]] && cp "$src_pages/$f" "$docs_dest/$f"
  done

  # .nojekyll — either copy template marker, or `touch` one.
  if [[ -f $src_pages/.nojekyll ]]; then
    cp "$src_pages/.nojekyll" "$docs_dest/.nojekyll"
  elif [[ -f $src_pages/nojekyll ]]; then
    cp "$src_pages/nojekyll" "$docs_dest/.nojekyll"
  else
    : >"$docs_dest/.nojekyll"
  fi

  # CNAME — only if user supplied a custom domain.
  if [[ -n "$custom_domain" ]]; then
    print -r -- "$custom_domain" >"$docs_dest/CNAME"
  fi

  # Render placeholders in the docs files.
  render_placeholders() {
    local file=$1
    [[ -f $file ]] || return 0
    local tmp; tmp=$(mktemp)
    sed \
      -e "s|{{REPO_URL}}|$repo_url|g" \
      -e "s|{{REPO_SLUG}}|$new_repo|g" \
      -e "s|{{HERO_EYEBROW}}|$hero_eyebrow|g" \
      -e "s|{{LAST_UPDATE}}|$today|g" \
      -e "s|{{DESCRIPTION}}|$description|g" \
      -e "s|{{CUSTOM_DOMAIN}}|$custom_domain|g" \
      "$file" >"$tmp"
    mv "$tmp" "$file"
  }
  for f in "$docs_dest/index.html" "$docs_dest/site.js" "$docs_dest/site.css"; do
    render_placeholders "$f"
  done

  # Root README / CHANGELOG / .gitignore from bundled templates.
  if [[ -f $templates_dir/README.md.tmpl ]]; then
    cp "$templates_dir/README.md.tmpl" README.md
    render_placeholders README.md
  fi
  if [[ -f $templates_dir/CHANGELOG.md.tmpl ]]; then
    cp "$templates_dir/CHANGELOG.md.tmpl" CHANGELOG.md
    render_placeholders CHANGELOG.md
  fi
  if [[ -f $templates_dir/gitignore.tmpl ]]; then
    cp "$templates_dir/gitignore.tmpl" .gitignore
  fi

  # ───── Bootstrap a starter skill, if requested ─────
  if [[ -n "$bootstrap_skill" ]]; then
    # Slug must be kebab-case-ish; reject anything obviously wrong.
    if [[ ! "$bootstrap_skill" =~ ^[a-z0-9][a-z0-9-]*$ ]]; then
      die "--bootstrap-skill slug must be lowercase kebab-case (got: $bootstrap_skill)"
    fi
    print_info "Bootstrapping skill directory: $bootstrap_skill/"
    mkdir -p "$bootstrap_skill"
    cat >"$bootstrap_skill/SKILL.md" <<EOF_SKILL
---
name: $bootstrap_skill
description: Brief description of what this skill does. Use when [specific trigger keywords or contexts that should activate this skill].
---

# $bootstrap_skill

## Quick start

[Minimal working example — the simplest invocation that demonstrates the skill.]

## Workflow

1. [First concrete step]
2. [Second concrete step]
3. [Verification — how the user confirms success]

## Inputs

- [What the user supplies, with examples]

## Outputs

- [What the skill produces, with file paths or behaviors]

## Gotchas

- [Known edge cases the agent should watch for]
EOF_SKILL

    cat >"$bootstrap_skill/README.md" <<EOF_README
# $bootstrap_skill

[One-paragraph description.]

## Install

\`\`\`bash
npx skills@latest add $new_repo --skill $bootstrap_skill
\`\`\`

## Usage

\`/$bootstrap_skill\`
EOF_README

    # Insert into docs/site.js skills array (between the [] brackets).
    if [[ -f "$docs_dest/site.js" ]]; then
      local entry
      entry=$(cat <<EOF_ENTRY
  {
    slug: "$bootstrap_skill",
    name: "$bootstrap_skill",
    category: "Engineering",
    tagline: "Replace with one-line tagline.",
    detail: "Replace with a longer description of when and why to use this skill.",
    usage: "/$bootstrap_skill",
  },
EOF_ENTRY
      )
      # Replace the empty-array literal with an array containing the entry.
      # Tolerate whitespace variants: `const skills = [];` / `[ ]` / `[]`.
      local tmp; tmp=$(mktemp)
      awk -v entry="$entry" '
        BEGIN { done=0 }
        /^const skills = \[\];/ && !done {
          print "const skills = ["
          print entry
          print "];"
          done=1
          next
        }
        { print }
      ' "$docs_dest/site.js" >"$tmp"
      if ! grep -q "slug: \"$bootstrap_skill\"" "$tmp"; then
        print_warn "Could not splice $bootstrap_skill into $docs_dest/site.js skills array — leaving site.js untouched. Add the entry manually."
      else
        mv "$tmp" "$docs_dest/site.js"
        print_ok "Added $bootstrap_skill entry to $docs_dest/site.js"
      fi
      rm -f "$tmp"
    fi
    print_ok "Skill skeleton at $bootstrap_skill/SKILL.md (placeholders inside — fill them in)"
  fi
fi  # end docs-content scaffold (port_docs)

# Guarantee a non-empty commit even when docs are skipped, so `main` is created
# on the remote — branch protection / Pages / team access all need it to exist.
if [[ ! -f README.md ]]; then
  cat >README.md <<EOF_README_MIN
# ${new_repo#*/}

${description:-AI agent skills and automation.}

> General settings, security flags, branch protection, and team access mirrored from
> [\`$ref_repo\`](https://github.com/$ref_repo) via gh-repo-mirror.
EOF_README_MIN
fi
if [[ ! -f .gitignore ]]; then
  if [[ -f $templates_dir/gitignore.tmpl ]]; then
    cp "$templates_dir/gitignore.tmpl" .gitignore
  else
    cat >.gitignore <<'EOF_GITIGNORE'
.DS_Store
*.log
.env
.env.*
!.env.example
node_modules/
dist/
build/
__pycache__/
*.py[cod]
.venv/
venv/
EOF_GITIGNORE
  fi
fi

if [[ "$port_docs" == "true" ]]; then
  commit_msg="chore: initial scaffold — README, CHANGELOG, $docs_dest Pages site"
else
  commit_msg="chore: initial scaffold — README + .gitignore"
fi

git init -b main >/dev/null
git add . >/dev/null
git -c commit.gpgsign=false commit -q -m "$commit_msg

Mirrored settings, security flags, branch protection, and team access
from $ref_repo via gh-repo-mirror."
git remote add origin "https://github.com/$new_repo.git"

if ! git push -u origin main 2>/tmp/_push.$$.err >/dev/null; then
  if grep -qE "rejected|already exists|fetch first|non-fast-forward" /tmp/_push.$$.err 2>/dev/null; then
    print_warn "Push rejected — repo likely already has commits. Skipping initial scaffold push."
  else
    cat /tmp/_push.$$.err >&2
    rm -f /tmp/_push.$$.err
    die "Push failed"
  fi
fi
rm -f /tmp/_push.$$.err

popd >/dev/null
[[ -n "$from_repo" ]] && rm -rf "/tmp/_pages-src.$$"
rm -rf "$workdir"
print_ok "Initial commit pushed"

# ───────────── branch protection ─────────────

if [[ -n "$ref_protection_json" ]]; then
  print_info "Mirroring branch protection on $new_repo/$ref_default_branch"
  # Mirror status-check and PR-review requirements faithfully — nulling them
  # would silently drop the reference's review/CI gates (a real protection gap).
  # dismissal_restrictions / bypass actors are intentionally omitted: their
  # users/teams/apps are org-scoped and may not resolve in the new repo's org.
  prot_payload=$(jq '{
    required_status_checks: (
      if .required_status_checks then
        { strict:   (.required_status_checks.strict   // false),
          contexts: (.required_status_checks.contexts // []) }
      else null end
    ),
    enforce_admins: (.enforce_admins.enabled // false),
    required_pull_request_reviews: (
      if .required_pull_request_reviews then
        { dismiss_stale_reviews:           (.required_pull_request_reviews.dismiss_stale_reviews           // false),
          require_code_owner_reviews:       (.required_pull_request_reviews.require_code_owner_reviews       // false),
          require_last_push_approval:       (.required_pull_request_reviews.require_last_push_approval       // false),
          required_approving_review_count:  (.required_pull_request_reviews.required_approving_review_count  // 0) }
      else null end
    ),
    restrictions: null,
    required_linear_history: (.required_linear_history.enabled // false),
    allow_force_pushes:     (.allow_force_pushes.enabled // false),
    allow_deletions:        (.allow_deletions.enabled // false),
    block_creations:        (.block_creations.enabled // false),
    required_conversation_resolution: (.required_conversation_resolution.enabled // false),
    lock_branch:            (.lock_branch.enabled // false),
    allow_fork_syncing:     (.allow_fork_syncing.enabled // false),
    required_signatures:    (.required_signatures.enabled // false)
  }' <<<"$ref_protection_json")
  print -r -- "$prot_payload" \
    | gh api -X PUT "repos/$new_repo/branches/$ref_default_branch/protection" --input - >/dev/null
  print_ok "Branch protection applied"
else
  print_warn "Reference has no classic branch protection on $ref_default_branch — skipping"
fi

# ───────────── Pages ─────────────

pages_state=""
if [[ "$enable_pages" != "true" ]]; then
  print_warn "Pages disabled (--no-pages) — skipping enable"
elif gh api "repos/$new_repo/pages" >/dev/null 2>&1; then
  print_warn "Pages already enabled on $new_repo — skipping enable"
  pages_state="existing"
else
  print_info "Enabling Pages from $ref_default_branch:$pages_path"
  pages_payload=$(jq -n --arg p "$pages_path" --arg b "$ref_default_branch" \
    '{source: {branch: $b, path: $p}, build_type: "legacy"}')
  if print -r -- "$pages_payload" | gh api -X POST "repos/$new_repo/pages" --input - >/dev/null 2>/tmp/_pages.$$.err; then
    pages_state="enabled"
  else
    print_err "Pages enable failed:"
    cat /tmp/_pages.$$.err >&2
    print_warn "Private-repo Pages requires GitHub Enterprise Cloud."
  fi
  rm -f /tmp/_pages.$$.err
fi

# Background-poll HTTPS enforcement if Pages is configured.
if [[ "$pages_state" == "enabled" || "$pages_state" == "existing" ]]; then
  print_info "Spawning background HTTPS-enforce watcher (poll every 30s)…"
  (
    until gh api "repos/$new_repo/pages" 2>/dev/null \
        | jq -e '.https_certificate.state == "approved"' >/dev/null 2>&1; do
      sleep 30
    done
    gh api -X PUT "repos/$new_repo/pages" --input - <<<'{"https_enforced": true}' >/dev/null 2>&1
  ) &!
  print_ok "HTTPS enforcement scheduled (will flip when cert lands)"
fi

# ───────────── Rulesets (optional) ─────────────

if [[ "$mirror_rulesets" == "true" ]]; then
  ruleset_count=$(jq 'length' <<<"$ref_rulesets_json")
  if (( ruleset_count == 0 )); then
    print_warn "Reference has no repo-level rulesets — nothing to mirror"
  else
    print_info "Mirroring $ruleset_count ruleset(s) from $ref_repo"
    # For each ruleset summary in the list, GET the full definition then POST to the new repo.
    jq -c '.[]' <<<"$ref_rulesets_json" | while IFS= read -r rs_summary; do
      rs_id=$(jq -r '.id' <<<"$rs_summary")
      rs_name=$(jq -r '.name' <<<"$rs_summary")
      # Pull full ruleset definition.
      rs_full=$(gh api "repos/$ref_repo/rulesets/$rs_id" 2>/dev/null) || {
        print_warn "  Skipped ruleset '$rs_name' (id=$rs_id): could not fetch full definition"
        continue
      }
      # Strip server-managed fields (id, source, source_type, *_at, _links, node_id) before POST.
      rs_payload=$(jq 'del(.id, .source, .source_type, .created_at, .updated_at, ._links, .node_id, .current_user_can_bypass)' <<<"$rs_full")
      if print -r -- "$rs_payload" | gh api -X POST "repos/$new_repo/rulesets" --input - >/dev/null 2>/tmp/_rs.$$.err; then
        print_ok "  Created ruleset '$rs_name'"
      else
        # Likely conflict (already exists) — try PUT against same-named ruleset on the new repo.
        existing_id=$(gh api "repos/$new_repo/rulesets" 2>/dev/null \
          | jq -r --arg n "$rs_name" '.[] | select(.name == $n) | .id' | head -1)
        if [[ -n "$existing_id" ]]; then
          if print -r -- "$rs_payload" | gh api -X PUT "repos/$new_repo/rulesets/$existing_id" --input - >/dev/null 2>/dev/null; then
            print_ok "  Updated existing ruleset '$rs_name' (id=$existing_id)"
          else
            print_warn "  Could not create or update ruleset '$rs_name':"
            cat /tmp/_rs.$$.err >&2
          fi
        else
          print_warn "  Could not create ruleset '$rs_name':"
          cat /tmp/_rs.$$.err >&2
        fi
      fi
      rm -f /tmp/_rs.$$.err
    done
  fi
fi

# ───────────── Access: teams + direct collaborators ─────────────

# Map collaborator role_name (read/triage/write/maintain/admin) to PUT permission
# value (pull/triage/push/maintain/admin).
role_to_permission() {
  case "$1" in
    read)     print -r -- "pull" ;;
    triage)   print -r -- "triage" ;;
    write)    print -r -- "push" ;;
    maintain) print -r -- "maintain" ;;
    admin)    print -r -- "admin" ;;
    # If we already got a permission-style value, pass through.
    pull|push) print -r -- "$1" ;;
    *)        print -r -- "$1" ;;
  esac
}

if [[ "$mirror_access" == "true" ]]; then
  team_count=$(jq 'length' <<<"$ref_teams_json")
  collab_count=$(jq 'length' <<<"$ref_collabs_json")

  if (( team_count == 0 && collab_count == 0 )); then
    print_warn "Reference has no teams or direct collaborators — nothing to mirror"
  else
    print_info "Mirroring access: $team_count team(s), $collab_count direct collaborator(s)"
  fi

  # Teams: PUT /orgs/{org}/teams/{slug}/repos/{owner}/{repo}
  if (( team_count > 0 )); then
    ref_org=${ref_repo%/*}
    new_org_for_teams=${new_repo%/*}
    if [[ "$ref_org" != "$new_org_for_teams" ]]; then
      print_warn "Reference org ($ref_org) differs from new org ($new_org_for_teams);"
      print_warn "team slugs are scoped to the new org — only teams that already exist there will resolve."
    fi
    jq -c '.[]' <<<"$ref_teams_json" | while IFS= read -r team; do
      slug=$(jq -r '.slug' <<<"$team")
      perm=$(jq -r '.permission' <<<"$team")
      payload=$(jq -n --arg p "$perm" '{permission: $p}')
      if print -r -- "$payload" \
          | gh api -X PUT "orgs/$new_org_for_teams/teams/$slug/repos/$new_repo" --input - >/dev/null 2>/tmp/_team.$$.err; then
        print_ok "  Team '$slug' → $perm"
      else
        print_warn "  Could not grant team '$slug' ($perm):"
        cat /tmp/_team.$$.err >&2
      fi
      rm -f /tmp/_team.$$.err
    done
  fi

  # Direct collaborators: PUT /repos/{owner}/{repo}/collaborators/{username}
  if (( collab_count > 0 )); then
    jq -c '.[]' <<<"$ref_collabs_json" | while IFS= read -r collab; do
      login=$(jq -r '.login' <<<"$collab")
      role=$(jq -r '.role_name // empty' <<<"$collab")
      [[ -z "$role" ]] && role="push"  # safe default if role_name missing
      perm=$(role_to_permission "$role")
      payload=$(jq -n --arg p "$perm" '{permission: $p}')
      if print -r -- "$payload" \
          | gh api -X PUT "repos/$new_repo/collaborators/$login" --input - >/dev/null 2>/tmp/_collab.$$.err; then
        print_ok "  Collaborator '$login' → $perm"
      else
        print_warn "  Could not invite collaborator '$login' ($perm):"
        cat /tmp/_collab.$$.err >&2
      fi
      rm -f /tmp/_collab.$$.err
    done
  fi
fi

# ───────────── DNS CNAME (optional) ─────────────

cname_target="${new_org:l}.github.io"

create_cname_cloudflare() {
  local domain=$1 target=$2 zone_id=$3
  if [[ -z "${CLOUDFLARE_API_TOKEN:-}" ]]; then
    print_err "CLOUDFLARE_API_TOKEN env var not set; cannot create DNS record"
    return 1
  fi
  require_cmd curl
  local body
  body=$(jq -n --arg name "$domain" --arg target "$target" \
    '{type: "CNAME", name: $name, content: $target, ttl: 1, proxied: false}')
  local resp
  resp=$(curl -fsS -X POST \
    "https://api.cloudflare.com/client/v4/zones/$zone_id/dns_records" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" \
    -d "$body" 2>/tmp/_cf.$$.err) || {
    if grep -q "An A, AAAA, or CNAME record with that host already exists" /tmp/_cf.$$.err 2>/dev/null \
       || grep -q "already exists" /tmp/_cf.$$.err 2>/dev/null; then
      print_warn "  CNAME $domain already exists on Cloudflare zone $zone_id — skipping"
      rm -f /tmp/_cf.$$.err
      return 0
    fi
    print_err "  Cloudflare API call failed:"
    cat /tmp/_cf.$$.err >&2
    rm -f /tmp/_cf.$$.err
    return 1
  }
  rm -f /tmp/_cf.$$.err
  if jq -e '.success == true' <<<"$resp" >/dev/null 2>&1; then
    print_ok "  Created CNAME $domain → $target on Cloudflare zone $zone_id"
  else
    print_err "  Cloudflare API responded with success=false:"
    print -r -- "$resp" >&2
    return 1
  fi
}

if [[ -n "$cname_provider" && -n "$custom_domain" ]]; then
  print_info "DNS CNAME ($cname_provider): $custom_domain → $cname_target"
  case "$cname_provider" in
    cloudflare) create_cname_cloudflare "$custom_domain" "$cname_target" "$cname_zone_id" || true ;;
    print)
      cat <<EOF
  Create this DNS record manually:
    Type:   CNAME
    Name:   $custom_domain
    Value:  $cname_target
    TTL:    auto / 300
    Proxy:  off (DNS-only)
EOF
      ;;
  esac
fi

# ───────────── verify by diff ─────────────

print_info "Verifying — diffing settings + branch protection between $ref_repo and $new_repo"

projection='{
  visibility, default_branch,
  has_issues, has_projects, has_wiki, has_discussions,
  allow_squash_merge, allow_merge_commit, allow_rebase_merge,
  allow_auto_merge, delete_branch_on_merge, allow_update_branch,
  web_commit_signoff_required,
  squash_merge_commit_message, squash_merge_commit_title,
  merge_commit_message, merge_commit_title,
  security_and_analysis: (.security_and_analysis // {})
}'

settings_diff=$(diff \
  <(gh api "repos/$ref_repo" | jq -S "$projection") \
  <(gh api "repos/$new_repo" | jq -S "$projection") || true)

if [[ -z "$settings_diff" ]]; then
  print_ok "Settings: zero drift"
else
  print_warn "Settings drift (expected if visibility/template overridden):"
  print -r -- "$settings_diff"
fi

if [[ -n "$ref_protection_json" ]]; then
  # Normalize both sides to the exact set of fields we mirror, so self-referential
  # *_url keys and empty dismissal_restrictions (intentionally omitted) don't read
  # as false drift. Compares semantics, not GitHub's response decoration.
  prot_norm='{
    required_status_checks: (if .required_status_checks then
      { strict: .required_status_checks.strict, contexts: (.required_status_checks.contexts // []) } else null end),
    enforce_admins: (.enforce_admins.enabled // false),
    required_pull_request_reviews: (if .required_pull_request_reviews then
      { dismiss_stale_reviews:          .required_pull_request_reviews.dismiss_stale_reviews,
        require_code_owner_reviews:      .required_pull_request_reviews.require_code_owner_reviews,
        require_last_push_approval:      .required_pull_request_reviews.require_last_push_approval,
        required_approving_review_count: .required_pull_request_reviews.required_approving_review_count } else null end),
    required_linear_history:          (.required_linear_history.enabled // false),
    allow_force_pushes:               (.allow_force_pushes.enabled // false),
    allow_deletions:                  (.allow_deletions.enabled // false),
    block_creations:                  (.block_creations.enabled // false),
    required_conversation_resolution: (.required_conversation_resolution.enabled // false),
    lock_branch:                      (.lock_branch.enabled // false),
    allow_fork_syncing:               (.allow_fork_syncing.enabled // false),
    required_signatures:              (.required_signatures.enabled // false)
  }'
  prot_diff=$(diff \
    <(gh api "repos/$ref_repo/branches/$ref_default_branch/protection" | jq -S "$prot_norm") \
    <(gh api "repos/$new_repo/branches/$ref_default_branch/protection" | jq -S "$prot_norm") || true)
  if [[ -z "$prot_diff" ]]; then
    print_ok "Branch protection: zero drift"
  else
    print_warn "Branch protection drift:"
    print -r -- "$prot_diff"
  fi
fi

if [[ "$mirror_access" == "true" ]]; then
  teams_diff=$(diff \
    <(gh api --paginate "repos/$ref_repo/teams" | jq -S '[.[] | {slug, permission}] | sort_by(.slug)') \
    <(gh api --paginate "repos/$new_repo/teams" | jq -S '[.[] | {slug, permission}] | sort_by(.slug)') || true)
  if [[ -z "$teams_diff" ]]; then
    print_ok "Teams: zero drift"
  else
    print_warn "Teams drift (expected if cross-org or some teams don't exist in new org):"
    print -r -- "$teams_diff"
  fi

  collabs_diff=$(diff \
    <(gh api --paginate "repos/$ref_repo/collaborators?affiliation=direct" \
        | jq -S '[.[] | {login, role_name}] | sort_by(.login)') \
    <(gh api --paginate "repos/$new_repo/collaborators?affiliation=direct" \
        | jq -S '[.[] | {login, role_name}] | sort_by(.login)') || true)
  if [[ -z "$collabs_diff" ]]; then
    print_ok "Direct collaborators: zero drift"
  else
    print_warn "Direct collaborators drift (invites may still be pending acceptance):"
    print -r -- "$collabs_diff"
  fi
fi

# ───────────── final summary ─────────────

cat <<EOF

Done.
─────
  Repo:     https://github.com/$new_repo
EOF

if [[ "$enable_pages" == "true" ]]; then
  cat <<EOF
  Pages:    ${custom_domain:+https://$custom_domain/}${custom_domain:-https://${new_org:l}.github.io/$new_name/}
  HTTPS:    pending — background watcher will flip https_enforced=true once cert lands.

Rerun if HTTPS hasn't flipped after a while:
  $script_path --enforce-https-only $new_repo
EOF
else
  print -r -- "  Pages:    disabled (--no-pages)"
fi
