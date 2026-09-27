#!/usr/bin/env zsh
# The legacy-state migration snippet in code-review-multi-axis/REFERENCE.md must
# move <skill-dir>/state out of the skill folder, keep PR worktrees attached to
# their repo, and refuse to overwrite an existing state dir.
set -eu
script_path=${0:A}
repo_root=${script_path:h:h}

snippet=$(python3 - "$repo_root/code-review-multi-axis/REFERENCE.md" <<'PY'
import re, sys
text = open(sys.argv[1]).read()
section = text.split("## State directory", 1)[1].split("\n## ", 1)[0]
print(re.search(r"```bash\n(.*?)```", section, re.S).group(1))
PY
)

tmp=${$(mktemp -d):A}   # resolve /var -> /private/var so paths match git's
trap 'rm -rf "$tmp"' EXIT
fail() { print -r -- "FAIL: $*" >&2; exit 1 }

# Fixture: a repo with one commit, and a skill dir whose legacy state holds a worktree.
make_fixture() {
  local root=$1
  git init -q "$root/repo"
  git -C "$root/repo" -c user.email=t@t -c user.name=t commit -q --allow-empty -m init
  mkdir -p "$root/skill/state/archive"
  print -r -- '{"pr": 1}' > "$root/skill/state/pr-1.json"
  touch "$root/skill/state/.acknowledged"
  git -C "$root/repo" worktree add -q --detach "$root/skill/state/worktree-pr-1"
}

run_snippet() {  # $1 fixture root, $2 shell
  local root=$1 sh=$2
  (cd "$root" && env -u XDG_STATE_HOME HOME="$root/home" CODE_REVIEW_MULTI_AXIS_STATE_DIR= \
    $sh -c "${snippet//<skill-dir>/$root/skill}")
}

for sh in bash zsh; do
  root="$tmp/$sh"; mkdir -p "$root/home"; make_fixture "$root"
  run_snippet "$root" $sh || fail "$sh: migration exited non-zero"
  new="$root/home/.local/state/code-review-multi-axis"
  [[ ! -e $root/skill/state ]] || fail "$sh: legacy dir still present"
  [[ -f $new/pr-1.json && -f $new/.acknowledged && -d $new/archive ]] || fail "$sh: state files not moved"
  git -C "$root/repo" worktree list --porcelain | grep -qx "worktree $new/worktree-pr-1" \
    || fail "$sh: repo does not list the moved worktree"
  git -C "$root/repo" worktree list --porcelain | grep -q prunable && fail "$sh: worktree left prunable"
  git -C "$new/worktree-pr-1" status >/dev/null || fail "$sh: moved worktree unusable"

  # Idempotent: second run with no legacy dir is a no-op.
  run_snippet "$root" $sh || fail "$sh: rerun exited non-zero"

  # Collision: legacy and new both exist -> refuse, touch nothing.
  mkdir -p "$root/skill/state"; print -r -- keep > "$root/skill/state/marker"
  if run_snippet "$root" $sh 2>/dev/null; then fail "$sh: collision did not abort"; fi
  [[ -f $root/skill/state/marker && -f $new/pr-1.json ]] || fail "$sh: collision modified files"
done

print -r -- "code-review-multi-axis-state: ok"
