#!/bin/sh
# detect_host.sh — POSIX sh host-detection cascade (mirrors detect_host.py).
# Prints the host guess only (one word) and always exits 0.
#
# Cascade (first match wins):
#   1. env CLAUDECODE == "1"        -> claude-code
#   2. any env var name ~ ^CODEX_   -> codex
#   3. any env var name ~ ^COPILOT_ -> copilot
#   4. any env var name ~ ^DEVIN_   -> devin
#   5. else: guess from session source dirs under $HOME, else "generic"
#      ~/.claude/projects -> claude-code, ~/.codex/sessions -> codex, ~/.copilot -> copilot

if [ "$CLAUDECODE" = "1" ]; then
    echo claude-code
    exit 0
fi

if env | grep -q '^CODEX_'; then
    echo codex
    exit 0
fi

if env | grep -q '^COPILOT_'; then
    echo copilot
    exit 0
fi

if env | grep -q '^DEVIN_'; then
    echo devin
    exit 0
fi

if [ -n "$HOME" ] && [ -d "$HOME/.claude/projects" ]; then
    echo claude-code
    exit 0
fi

if [ -n "$HOME" ] && [ -d "$HOME/.codex/sessions" ]; then
    echo codex
    exit 0
fi

if [ -n "$HOME" ] && [ -d "$HOME/.copilot" ]; then
    echo copilot
    exit 0
fi

echo generic
exit 0
