#!/usr/bin/env zsh
set -eu
script_path=${0:A}
fixture_dir=${script_path:h}/fixtures
target=${1:?Pass an empty target folder}
[[ ! -e $target ]] || { print -u2 -- "Target already exists: $target"; exit 1; }
mkdir -p "$target"
cp -R "$fixture_dir/code/." "$target/"
git -C "$target" init -q
git -C "$target" add .
git -C "$target" -c user.name=Owner -c user.email=owner@example.invalid commit -qm "Create sample monthly reports"
git -C "$target" -c user.name=Owner -c user.email=owner@example.invalid commit --allow-empty -qm "Owner correction: no exclamation marks in future reports"
git -C "$target" -c user.name=Owner -c user.email=owner@example.invalid commit --allow-empty -qm "Owner correction: format dates as 16 Sep 2026, never numeric YYYY/MM/DD"
print -r -- "$target"
