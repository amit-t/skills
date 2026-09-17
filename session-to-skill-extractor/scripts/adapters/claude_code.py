"""Claude Code adapter: loads local Claude Code transcript JSONL files.

Each Claude Code session is one JSONL file under `~/.claude/projects/<project>/`,
one JSON object per line. Lines carry a top-level `type` ("user" | "assistant"
plus meta types like "file-history-snapshot", "attachment", "mode"), optional
`isMeta` / `isSidechain` flags, and (for "user"/"assistant" lines) a `message`
with a `content` field that is either a plain string or a list of blocks
(`text`, `thinking`, `tool_use`, `tool_result`).
"""
import glob
import json
import os
import time
from pathlib import Path

from adapters.base import Adapter, Session, Turn, detect_outcome_signals

DEFAULT_PROJECTS_DIR = "~/.claude/projects"
DEFAULT_LOOKBACK_DAYS = 1


def _extract_content(content):
    """Split message.content into (text, tool_calls, tool_results).

    content is either a plain string (-> text, no calls/results) or a list of
    blocks. `text` blocks are concatenated; `thinking` blocks are dropped;
    `tool_use` blocks become tool_calls; `tool_result` blocks (which arrive on
    user-type lines) become tool_results.
    """
    if isinstance(content, str):
        return content, [], []

    text_parts = []
    tool_calls = []
    tool_results = []

    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            block_type = block.get("type")
            if block_type == "text":
                text_parts.append(block.get("text", ""))
            elif block_type == "thinking":
                continue
            elif block_type == "tool_use":
                tool_calls.append({
                    "name": block.get("name"),
                    "input_summary": json.dumps(block.get("input", {}))[:200],
                })
            elif block_type == "tool_result":
                tool_results.append({
                    "name": "",
                    "ok": not block.get("is_error", False),
                    "output_summary": str(block.get("content", ""))[:200],
                })

    return "".join(text_parts), tool_calls, tool_results


def _should_keep(obj):
    """Keep only user/assistant lines that are neither meta nor sidechain."""
    if obj.get("type") not in ("user", "assistant"):
        return False
    if obj.get("isMeta"):
        return False
    if obj.get("isSidechain"):
        return False
    return True


def _line_to_turn(obj):
    """Convert one kept line into a Turn.

    A "user"-type line whose only content is tool_results (no text, no tool
    calls) is re-labelled role "tool" — it represents tool output being fed
    back in, not a human message.
    """
    message = obj.get("message") or {}
    content = message.get("content", "")
    text, tool_calls, tool_results = _extract_content(content)

    role = obj.get("type")
    if role == "user" and not text and tool_results and not tool_calls:
        role = "tool"

    return Turn(
        role=role,
        text=text,
        tool_calls=tool_calls,
        tool_results=tool_results,
        timestamp=obj.get("timestamp"),
    )


class ClaudeCodeAdapter(Adapter):
    host = "claude-code"

    def locate(self, config) -> list:
        config = config or {}
        root = config.get("claude_projects_dir") or DEFAULT_PROJECTS_DIR
        root = str(Path(root).expanduser())
        lookback_days = (config.get("filter") or {}).get("lookback_days", DEFAULT_LOOKBACK_DAYS)
        cutoff = time.time() - (lookback_days * 86400)

        pattern = str(Path(root) / "*" / "*.jsonl")
        matches = [p for p in glob.glob(pattern) if os.path.getmtime(p) >= cutoff]
        return sorted(matches, key=lambda p: os.path.getmtime(p), reverse=True)

    def load(self, ref, config) -> Session:
        path = Path(ref)
        turns = []
        session_id = None
        cwd = None
        started_at = None
        ended_at = None

        with path.open("r", encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except ValueError:
                    continue
                if not isinstance(obj, dict):
                    continue
                if not _should_keep(obj):
                    continue

                if session_id is None:
                    session_id = obj.get("sessionId")
                    cwd = obj.get("cwd")
                    started_at = obj.get("timestamp")
                ended_at = obj.get("timestamp") or ended_at

                turns.append(_line_to_turn(obj))

        session = Session(
            session_id=session_id or path.stem,
            host=self.host,
            source_path=str(path),
            started_at=started_at,
            ended_at=ended_at,
            cwd=cwd,
        )
        session.turns = turns
        session.outcome_signals = detect_outcome_signals(turns)
        return session
