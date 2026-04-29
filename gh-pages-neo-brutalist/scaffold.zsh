#!/usr/bin/env zsh
# scaffold.zsh — drop the neo-brutalist GH Pages templates into the current repo.
#
# Run from inside the target repo root:
#   zsh /path/to/at-skills/gh-pages-neo-brutalist/scaffold.zsh
#
# Flags:
#   --force   overwrite files that already exist
#   --title   "Repo Title"           (skip prompt)
#   --tagline "One-line description" (skip prompt)
#   --owner   "github-owner"         (skip prompt)
#   --repo    "repo-name"            (default: $(basename PWD))
#   --github  "https://github.com/owner/repo" (default: derive from --owner/--repo)

emulate -L zsh
setopt err_return pipe_fail no_unset
script_path=${0:A}
script_dir=${script_path:h}
templates_dir=${script_dir}/templates

if [[ ! -d $templates_dir ]]; then
  print -ru2 -- "scaffold.zsh: cannot locate templates dir at $templates_dir"
  exit 1
fi

force=0
title=""
tagline=""
owner=""
repo=""
github_url=""
date_today=$(date +%Y-%m-%d)

while (( $# )); do
  case $1 in
    --force)   force=1; shift ;;
    --title)   title=$2; shift 2 ;;
    --tagline) tagline=$2; shift 2 ;;
    --owner)   owner=$2; shift 2 ;;
    --repo)    repo=$2; shift 2 ;;
    --github)  github_url=$2; shift 2 ;;
    -h|--help)
      sed -n '2,15p' "$script_path"
      exit 0
      ;;
    *)
      print -ru2 -- "scaffold.zsh: unknown flag: $1"
      exit 2
      ;;
  esac
done

# Determine repo + owner.
[[ -z $repo ]] && repo=${PWD:t}

if [[ -z $owner ]]; then
  if (( $+commands[git] )) && git -C . rev-parse --git-dir >/dev/null 2>&1; then
    remote=$(git -C . remote get-url origin 2>/dev/null || true)
    if [[ $remote == *github.com* ]]; then
      owner=${${${remote#*github.com[:/]}%%/*}}
    fi
  fi
fi

prompt_for() {
  local var_name=$1 prompt_text=$2 default_value=$3 reply
  if [[ -n ${(P)var_name} ]]; then return; fi
  if [[ -t 0 ]]; then
    if [[ -n $default_value ]]; then
      print -n -- "$prompt_text [$default_value]: "
    else
      print -n -- "$prompt_text: "
    fi
    read -r reply
    [[ -z $reply ]] && reply=$default_value
  else
    reply=$default_value
  fi
  : ${(P)var_name::=$reply}
}

prompt_for title    "Site title"          "$repo"
prompt_for tagline  "One-line tagline"    "Polished landing page for $repo"
prompt_for owner    "GitHub owner"        "amit-t"

[[ -z $github_url ]] && github_url="https://github.com/${owner}/${repo}"

baseurl="/${repo}"
hero_eyebrow=$(print -- "$repo" | tr '[:lower:]' '[:upper:]')

print "──────────────────────────────────────────"
print "Scaffolding GH Pages site"
print "  title:     $title"
print "  tagline:   $tagline"
print "  owner:     $owner"
print "  repo:      $repo"
print "  baseurl:   $baseurl"
print "  github:    $github_url"
print "  date:      $date_today"
print "  force:     $force"
print "──────────────────────────────────────────"

# Walk templates and copy. Skip files that already exist unless --force.
copy_one() {
  local rel=$1 src=$templates_dir/$1 dst=$PWD/$1
  if [[ -e $dst && $force -eq 0 ]]; then
    print -- "  skip   $rel (exists)"
    return
  fi
  mkdir -p "${dst:h}"
  cp "$src" "$dst"
  print -- "  write  $rel"
}

# Files to copy verbatim.
verbatim_files=(
  Gemfile
  .gitignore
  assets/css/site.css
  assets/js/site.js
  _layouts/base.html
  _layouts/home.html
  _layouts/page.html
  .github/workflows/pages.yml
)
for f in $verbatim_files; do
  copy_one "$f"
done

# Files to template.
template_one() {
  local rel=$1 src=$templates_dir/$1 dst=$PWD/$1
  if [[ -e $dst && $force -eq 0 ]]; then
    print -- "  skip   $rel (exists)"
    return
  fi
  mkdir -p "${dst:h}"
  sed \
    -e "s|REPLACE_TITLE|${title}|g" \
    -e "s|REPLACE_DESCRIPTION|${tagline}|g" \
    -e "s|REPLACE_BASEURL|${baseurl}|g" \
    -e "s|REPLACE_OWNER|${owner}|g" \
    -e "s|REPLACE_EYEBROW|${hero_eyebrow}|g" \
    -e "s|REPLACE_HERO_TITLE|${title}|g" \
    -e "s|REPLACE_HERO_DESC|${tagline}|g" \
    -e "s|REPLACE_GITHUB_URL|${github_url}|g" \
    -e "s|REPLACE_DATE|${date_today}|g" \
    "$src" > "$dst"
  print -- "  write  $rel"
}

template_one _config.yml
template_one index.md

# Refuse to keep .nojekyll — it disables layout rendering.
if [[ -f $PWD/.nojekyll ]]; then
  print -- "  remove .nojekyll (Jekyll must run for layouts)"
  rm "$PWD/.nojekyll"
fi

print
print "Done."
print
print "Next steps:"
print "  1. Review _config.yml + index.md, fill in nav links + stats."
print "  2. git add . && git commit -m 'feat: scaffold GH Pages (neo-brutalist)'"
print "  3. GitHub Settings → Pages → Source: GitHub Actions"
print "  4. (optional) bundle install && bundle exec jekyll serve  # local preview"
