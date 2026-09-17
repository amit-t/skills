"""Shared utilities for session-to-skill-extractor scripts.

Config loading (deep-merge over the bundled example), timestamps, slugs,
and small JSON I/O helpers used by adapters and CLIs.
"""
import copy
import datetime
import json
import re
from pathlib import Path

_BUNDLED_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.example.json"

_SLUG_RE = re.compile(r"[^a-z0-9]+")


def read_json(path):
    """Read and parse a JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    """Write obj as pretty-printed JSON to path."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)
        f.write("\n")


def _deep_merge(base, override):
    """Recursively merge override onto a copy of base; override wins."""
    result = copy.deepcopy(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = copy.deepcopy(value)
    return result


def load_config(path_or_none):
    """Load the bundled config.example.json, deep-merged with an optional user config."""
    bundled = read_json(_BUNDLED_CONFIG_PATH)
    if not path_or_none:
        return bundled
    user_config = read_json(path_or_none)
    return _deep_merge(bundled, user_config)


def now_iso():
    """Current UTC time as an ISO-8601 string."""
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def slugify(s):
    """Lowercase, alnum-and-hyphen slug of s."""
    s = (s or "").strip().lower()
    s = _SLUG_RE.sub("-", s)
    return s.strip("-")
