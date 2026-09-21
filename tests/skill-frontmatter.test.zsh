#!/usr/bin/env zsh
# Every SKILL.md frontmatter must parse as strict YAML, or `npx skills add` skips the skill.
set -eu
script_path=${0:A}
repo_root=${script_path:h:h}
cd "$repo_root"

python3 - <<'PY'
from pathlib import Path
import yaml

failures = []
for path in sorted(Path.cwd().glob("*/SKILL.md")):
    text = path.read_text()
    if not text.startswith("---\n"):
        failures.append(f"{path}: missing frontmatter")
        continue
    try:
        meta = yaml.safe_load(text.split("---", 2)[1])
    except yaml.YAMLError as err:
        failures.append(f"{path}: {str(err).splitlines()[0]}")
        continue
    if not isinstance(meta, dict):
        failures.append(f"{path}: frontmatter is not a mapping")
        continue
    if meta.get("name") != path.parent.name:
        failures.append(f"{path}: name {meta.get('name')!r} != directory {path.parent.name!r}")
    description = meta.get("description")
    if not isinstance(description, str) or not description.strip():
        failures.append(f"{path}: description missing or not a string")
    elif len(description) > 1024:
        failures.append(f"{path}: description longer than 1024 chars")

assert not failures, "\n".join(failures)
PY

print -r -- "skill-frontmatter: ok"
