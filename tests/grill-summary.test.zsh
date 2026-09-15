#!/usr/bin/env zsh
# Packaging/catalog checks only. Agent behavior is tested separately in cases.md.
set -eu
script_path=${0:A}
repo_root=${script_path:h:h}
cd "$repo_root"

python3 - <<'PY'
import json
from pathlib import Path
import re

root = Path.cwd()
skill = root / "grill-summary"
required = [skill / name for name in ("SKILL.md", "README.md", "WAYFINDER.md")]
assert all(p.is_file() for p in required), "Missing grill-summary package files"
entrypoint = required[0].read_text()
frontmatter = entrypoint.split("---", 2)[1]
assert re.search(r"^name: grill-summary$", frontmatter, re.M)
description = re.search(r"^description: (.+)$", frontmatter, re.M).group(1)
assert len(description) <= 1024
assert "disable-model-invocation: true" not in frontmatter
assert len(entrypoint.splitlines()) < 100

for path in required:
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
        if "://" in target or target.startswith("#"):
            continue
        assert (path.parent / target.split("#", 1)[0]).exists(), (path, target)

catalog = json.loads((root / "skills.json").read_text())["skills"]
matches = [s for s in catalog if s["slug"] == "grill-summary"]
assert len(matches) == 1, "Expected one catalog entry"
entry = matches[0]
for key in ("slug", "name", "category", "tagline", "detail", "usage"):
    assert isinstance(entry[key], str) and entry[key].strip(), key
assert entry["category"] == "Engineering"
assert entry["name"] == "grill-summary"
assert "/grill-summary" in entry["usage"]
i = catalog.index(entry)
assert catalog[i - 1]["category"] == catalog[i + 1]["category"] == "Engineering"

readme = (root / "README.md").read_text()
section = readme.split("### Engineering\n", 1)[1].split("\n### ", 1)[0]
slugs = re.findall(r"\| \[`([^`]+)`\]", section)
assert slugs == sorted(slugs), "Engineering table must be alphabetical"
assert slugs.count("grill-summary") == 1
assert "[\u0060grill-summary\u0060](./grill-summary)" in section

changes = json.loads((root / "changelog.json").read_text())["changes"]
added = [c for c in changes if any("Added grill-summary skill" in t for t in c["items"])]
assert len(added) == 1
md = (root / "CHANGELOG.md").read_text()
dated = md.split("## " + added[0]["date"] + "\n", 1)[1].split("\n## ", 1)[0]
assert "Added the `grill-summary` skill" in dated
print("PASS: skill package, discovery metadata, relative links, catalog, sort order, changelogs")
PY
