#!/usr/bin/env python3
"""Stage 3 dedup pre-screen: cheap Jaccard token-overlap check before any LLM call
(spec E3-5 prescreen). Compares a D2 candidate's name+description+trigger.description
tokens against every existing skill's SKILL.md frontmatter and every registry entry.

`tokenize` is a clean module-level function: Task 10's retire_review.py imports it
from this module (same scripts/ dir).
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from s2s_common import load_config, read_json

_STOPWORDS = {
    "a", "an", "the", "to", "of", "for", "and", "or", "in", "on", "with",
    "use", "when", "this", "that",
}
_TOKEN_SPLIT_RE = re.compile(r"[^a-z0-9]+")
_FRONTMATTER_LINE_RE = re.compile(r"^([A-Za-z0-9_]+):\s*(.*)$")


def tokenize(text):
    """Lowercase, split on non-alnum, drop stopwords and empty strings. Returns a set."""
    text = (text or "").lower()
    parts = _TOKEN_SPLIT_RE.split(text)
    return {p for p in parts if p and p not in _STOPWORDS}


def _jaccard(a, b):
    """|a & b| / |a | b|; 0.0 if either set is empty."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _candidate_tokens(candidate):
    candidate = candidate or {}
    trigger_description = (candidate.get("trigger") or {}).get("description") or ""
    combined = " ".join([
        candidate.get("name") or "",
        candidate.get("description") or "",
        trigger_description,
    ])
    return tokenize(combined)


def _parse_frontmatter(text):
    """YAML-lite frontmatter between the first two '---' lines: plain 'key: value' pairs,
    quotes stripped. Returns {} if there is no well-formed frontmatter block."""
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    body = []
    closed = False
    for line in lines[1:]:
        if line.strip() == "---":
            closed = True
            break
        body.append(line)
    if not closed:
        return {}

    result = {}
    for line in body:
        m = _FRONTMATTER_LINE_RE.match(line)
        if not m:
            continue
        key, value = m.group(1), m.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in ("'", '"'):
            value = value[1:-1]
        result[key] = value
    return result


def _skilldir_entries(skill_dirs):
    """Yield (skill_name, path, tokens) for every */SKILL.md under each skill dir.
    Missing directories are skipped silently."""
    for d in skill_dirs or []:
        d = Path(d)
        if not d.is_dir():
            continue
        for skill_md in sorted(d.glob("*/SKILL.md")):
            try:
                text = skill_md.read_text(encoding="utf-8")
            except OSError:
                continue
            fm = _parse_frontmatter(text)
            name = fm.get("name") or skill_md.parent.name
            description = fm.get("description") or ""
            tokens = tokenize(" ".join([name, description]))
            yield name, str(skill_md), tokens


def _registry_entries(registry):
    """Yield (skill_name, path, tokens) for every registry skills{} entry.
    A missing/empty registry yields nothing (skip silently)."""
    if not registry:
        return
    for name, entry in (registry.get("skills") or {}).items():
        entry = entry or {}
        trigger_description = entry.get("trigger_description") or ""
        tokens = tokenize(" ".join([name, trigger_description]))
        yield name, entry.get("path"), tokens


def build_shortlist(candidate, skill_dirs, registry, threshold):
    """Score candidate vs every existing SKILL.md + registry entry; return entries
    with score >= threshold as [{"skill", "path", "score"}, ...], sorted desc by score."""
    cand_tokens = _candidate_tokens(candidate)

    shortlist = []
    for name, path, tokens in _skilldir_entries(skill_dirs):
        score = _jaccard(cand_tokens, tokens)
        if score >= threshold:
            shortlist.append({"skill": name, "path": path, "score": score})

    for name, path, tokens in _registry_entries(registry):
        score = _jaccard(cand_tokens, tokens)
        if score >= threshold:
            shortlist.append({"skill": name, "path": path, "score": score})

    shortlist.sort(key=lambda e: (-e["score"], e["skill"]))
    return shortlist


def parse_args(argv=None):
    parser = argparse.ArgumentParser(
        description="Dedup pre-screen: Jaccard token-overlap vs existing skills + registry."
    )
    parser.add_argument("--candidate", required=True, help="path to a candidate JSON file")
    parser.add_argument("--skill-dirs", default="", help="comma-separated skill directories")
    parser.add_argument("--registry", default=None, help="path to registry.json (optional)")
    parser.add_argument("--threshold", type=float, default=None,
                         help="Jaccard threshold; defaults to config dedup.prescreen_overlap_threshold")
    parser.add_argument("--config", default=None, help="path to a user config.json")
    return parser.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)
    candidate = read_json(args.candidate)
    cfg = load_config(args.config)

    threshold = args.threshold
    if threshold is None:
        threshold = (cfg.get("dedup") or {}).get("prescreen_overlap_threshold", 0.3)

    skill_dirs = [d for d in (args.skill_dirs or "").split(",") if d]

    registry = None
    if args.registry and Path(args.registry).exists():
        registry = read_json(args.registry)

    shortlist = build_shortlist(candidate, skill_dirs, registry, threshold)
    print(json.dumps({"shortlist": shortlist}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
