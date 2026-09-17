"""Generic adapter: loads plain-text or JSONL session transcripts from file paths.

No host-specific assumptions; used for manually-collected or ad hoc transcripts,
and as the fallback host when no other adapter applies.
"""
import glob
import json
import os
import re
from pathlib import Path

from adapters.base import Adapter, Session, Turn, detect_outcome_signals
from s2s_common import slugify

_BLOCK_RE = re.compile(r"^(User|Assistant):\s*(.*)$", re.DOTALL)


def _try_jsonl(text):
    """One JSON object per non-blank line, each with a 'role' key. None if not JSONL."""
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return None
    turns = []
    for line in lines:
        try:
            obj = json.loads(line)
        except ValueError:
            return None
        if not isinstance(obj, dict) or "role" not in obj:
            return None
        turns.append(Turn(role=obj.get("role"), text=obj.get("text", "")))
    return turns


def _try_plain_text(text):
    """Blank-line-separated blocks, each prefixed 'User:' or 'Assistant:'. None if not this shape."""
    blocks = re.split(r"\n\s*\n", text.strip())
    turns = []
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        m = _BLOCK_RE.match(block)
        if not m:
            return None
        role = "user" if m.group(1) == "User" else "assistant"
        turns.append(Turn(role=role, text=m.group(2).strip()))
    if not turns:
        return None
    return turns


def parse_transcript(text):
    """Parse text as JSONL, else blank-line User:/Assistant: blocks, else one user turn."""
    turns = _try_jsonl(text)
    if turns:
        return turns
    turns = _try_plain_text(text)
    if turns:
        return turns
    return [Turn(role="user", text=text)]


class GenericAdapter(Adapter):
    host = "generic"

    def locate(self, config) -> list:
        config = config or {}
        patterns = config.get("paths") or []
        matches = set()
        for pattern in patterns:
            matches.update(glob.glob(pattern))
        return sorted(matches, key=lambda p: os.path.getmtime(p), reverse=True)

    def load(self, ref, config) -> Session:
        path = Path(ref)
        text = path.read_text(encoding="utf-8", errors="replace")
        turns = parse_transcript(text)
        session = Session(
            session_id=slugify(path.stem) or path.stem,
            host=self.host,
            source_path=str(path),
        )
        session.turns = turns
        session.outcome_signals = detect_outcome_signals(turns)
        return session
