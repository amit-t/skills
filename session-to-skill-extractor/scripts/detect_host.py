#!/usr/bin/env python3
"""Detect which agent host is running (or produced session logs on this machine).

Standalone module: deliberately imports nothing from `adapters` or any other
project module, so it can be invoked cheaply and independently of session
loading.

Cascade (first match wins for `host`):
    1. env CLAUDECODE == "1"        -> claude-code, confidence high
    2. any env key starting CODEX_  -> codex,       confidence medium
    3. any env key starting COPILOT_-> copilot,     confidence medium
    4. any env key starting DEVIN_  -> devin,       confidence medium
    5. else                         -> generic,     confidence low

`session_sources` always lists every session store found under `home`,
independent of the cascade result above: a run under Claude Code can still
mine local Codex/Copilot logs, so the run-host only controls defaults, not
what gets enumerated.
"""
import argparse
import json
import os
import sys
from pathlib import Path

# host -> path (relative to home) of that host's session store.
SESSION_SOURCE_DIRS = [
    ("claude-code", ".claude/projects"),
    ("codex", ".codex/sessions"),
    ("copilot", ".copilot"),
]

# env-key prefix -> host, checked in cascade order (steps 2-4).
ENV_PREFIX_HOSTS = [
    ("CODEX_", "codex"),
    ("COPILOT_", "copilot"),
    ("DEVIN_", "devin"),
]


def _enumerate_session_sources(home):
    """Return every known session store that exists under `home`."""
    sources = []
    for host, rel in SESSION_SOURCE_DIRS:
        path = Path(home) / rel
        if path.is_dir():
            sources.append({"host": host, "path": str(path), "exists": True})
    return sources


def detect(env=None, home=None, override=None):
    """Detect the host agent runtime.

    env: mapping to read env vars from (defaults to os.environ).
    home: base dir to look for session source dirs under (defaults to Path.home()).
    override: if given, short-circuits the cascade; host=override, confidence="high".

    Returns: {"host": str, "confidence": "high|medium|low",
              "signals": [str, ...], "session_sources": [{"host","path","exists"}, ...]}
    """
    if env is None:
        env = os.environ
    if home is None:
        home = Path.home()

    session_sources = _enumerate_session_sources(home)

    if override:
        return {
            "host": override,
            "confidence": "high",
            "signals": ["override:{}".format(override)],
            "session_sources": session_sources,
        }

    if env.get("CLAUDECODE") == "1":
        return {
            "host": "claude-code",
            "confidence": "high",
            "signals": ["env:CLAUDECODE=1"],
            "session_sources": session_sources,
        }

    for prefix, host in ENV_PREFIX_HOSTS:
        if any(key.startswith(prefix) for key in env):
            return {
                "host": host,
                "confidence": "medium",
                "signals": ["env-prefix:{}".format(prefix)],
                "session_sources": session_sources,
            }

    return {
        "host": "generic",
        "confidence": "low",
        "signals": ["no-cascade-signal"],
        "session_sources": session_sources,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Detect the host agent runtime.")
    parser.add_argument("--override", default=None, help="Force the host guess (confidence=high).")
    parser.add_argument("--json", action="store_true", help="No-op: output is always JSON.")
    args = parser.parse_args(argv)

    result = detect(override=args.override)
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
