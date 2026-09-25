#!/usr/bin/env zsh
# skills.json, the root README tables, and the skill directories must agree.
# Local entries need a directory with SKILL.md + README.md; third-party entries
# (`source` set) must have no local directory and must point at upstream.
set -eu
script_path=${0:A}
repo_root=${script_path:h:h}
cd "${1:-$repo_root}"

python3 - <<'PY'
from pathlib import Path
import json, re
import yaml

root = Path.cwd()
failures = []
categories = {"Product Management", "Project Management", "Engineering", "UX Design",
              "Agent Behavior", "AI Agent", "Leadership"}

skills = json.loads((root / "skills.json").read_text())["skills"]
readme = (root / "README.md").read_text()
section = readme.split("## Available Skills", 1)[1].split("\n## ", 1)[0]
rows = {m.group(1): (m.group(2), m.group(3))
        for m in re.finditer(r"^\| \[`([^`]+)`\]\(([^)]+)\) \| (.*) \|$", section, re.M)}

slugs = [s.get("slug") for s in skills]
dupes = {s for s in slugs if slugs.count(s) > 1}
if dupes:
    failures.append(f"skills.json: duplicate slugs {sorted(dupes)}")

local_dirs = {p.parent.name for p in root.glob("*/SKILL.md")}

for s in skills:
    slug = s.get("slug", "?")
    for key in ("slug", "name", "category", "tagline", "detail", "usage"):
        if not isinstance(s.get(key), str) or not s[key].strip():
            failures.append(f"{slug}: skills.json field {key!r} missing or empty")
    if s.get("category") not in categories:
        failures.append(f"{slug}: unknown category {s.get('category')!r}")
    row = rows.get(slug)
    if row is None:
        failures.append(f"{slug}: no row in README Available Skills")
    if "source" in s:
        source, url, path = s.get("source"), s.get("sourceUrl"), s.get("skillPath")
        if not (isinstance(source, str) and re.fullmatch(r"[\w.-]+/[\w.-]+", source)):
            failures.append(f"{slug}: source must be owner/repo, got {source!r}")
        if url != f"https://github.com/{source}":
            failures.append(f"{slug}: sourceUrl {url!r} != https://github.com/{source}")
        if not isinstance(path, str) or not path.strip():
            failures.append(f"{slug}: third-party entry needs skillPath")
        if (root / slug).exists():
            failures.append(f"{slug}: third-party entry must not have a local directory")
        if row and row[0] != url:
            failures.append(f"{slug}: README row must link {url}, got {row[0]}")
        if row and not row[1].startswith("Third-party (not vendored)."):
            failures.append(f"{slug}: README row must start 'Third-party (not vendored).'")
        if row and f"npx skills@latest add {source} --skill {slug}" not in row[1]:
            failures.append(f"{slug}: README row must include its npx install command")
    else:
        if slug not in local_dirs:
            failures.append(f"{slug}: no {slug}/SKILL.md")
        elif not (root / slug / "README.md").is_file():
            failures.append(f"{slug}: no {slug}/README.md")
        if row and row[0] != f"./{slug}":
            failures.append(f"{slug}: README row must link ./{slug}, got {row[0]}")
        if row and slug in local_dirs:
            meta = yaml.safe_load((root / slug / "SKILL.md").read_text().split("---", 2)[1])
            slash_only = meta.get("disable-model-invocation") is True
            if slash_only != row[1].startswith("Slash-only."):
                failures.append(f"{slug}: README 'Slash-only.' marker disagrees with disable-model-invocation")

for d in sorted(local_dirs - set(slugs)):
    failures.append(f"{d}: directory has SKILL.md but no skills.json entry")
for r in sorted(set(rows) - set(slugs)):
    failures.append(f"{r}: README row has no skills.json entry")

assert not failures, "\n".join(failures)
PY

print -r -- "catalog: ok"
