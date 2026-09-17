"""Normalized session model: Turn/Session dataclasses, stats, and outcome signals.

Shared by every host adapter (generic, claude-code, codex, copilot, devin).
"""
import re
from dataclasses import asdict, dataclass, field
from typing import List, Optional

_POSITIVE_RE = re.compile(
    r"\b(?:perfect|that worked|exactly|great,? thanks|lgtm|nice,? (?:that|it) works)\b",
    re.IGNORECASE,
)
_NEGATIVE_RE = re.compile(
    r"\b(?:didn'?t work|that'?s wrong|not what i asked|revert|still (?:broken|failing))\b",
    re.IGNORECASE,
)
_TASK_COMPLETED_RE = re.compile(
    r"git (?:commit|push)|create_pr|gh pr create",
    re.IGNORECASE,
)


@dataclass
class Turn:
    role: str  # "user" | "assistant" | "tool"
    text: str = ""
    tool_calls: list = field(default_factory=list)    # [{"name": str, "input_summary": str}]
    tool_results: list = field(default_factory=list)  # [{"name": str, "ok": bool, "output_summary": str}]
    timestamp: Optional[str] = None


@dataclass
class Session:
    session_id: str
    host: str
    source_path: Optional[str] = None
    started_at: Optional[str] = None
    ended_at: Optional[str] = None
    cwd: Optional[str] = None
    turns: list = field(default_factory=list)          # of Turn
    outcome_signals: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "session_id": self.session_id,
            "host": self.host,
            "source_path": self.source_path,
            "started_at": self.started_at,
            "ended_at": self.ended_at,
            "cwd": self.cwd,
            "turns": [asdict(t) for t in self.turns],
            "stats": compute_stats(self.turns),
            "outcome_signals": self.outcome_signals,
        }


def compute_stats(turns: List[Turn]) -> dict:
    """turn_count, assistant_turns, tool_call_count, distinct_tools, char_count, error_count, retry_count."""
    turn_count = len(turns)
    assistant_turns = sum(1 for t in turns if t.role == "assistant")
    tool_call_count = sum(len(t.tool_calls) for t in turns)

    tools = set()
    for t in turns:
        for call in t.tool_calls:
            name = call.get("name")
            if name:
                tools.add(name)
    distinct_tools = sorted(tools)

    char_count = sum(len(t.text or "") for t in turns)

    error_count = 0
    for t in turns:
        for result in t.tool_results:
            if result.get("ok") is False:
                error_count += 1

    # Strict adjacency: a retry only counts when the very next tool_call
    # after an error result is the same tool. Any intervening tool_call
    # (same tool or not) consumes the pending error and breaks the
    # sequence, so it can credit at most one retry per error.
    retry_count = 0
    pending_error_tool = None
    for t in turns:
        for call in t.tool_calls:
            if pending_error_tool is not None:
                if call.get("name") == pending_error_tool:
                    retry_count += 1
                pending_error_tool = None
        for result in t.tool_results:
            if result.get("ok") is False:
                pending_error_tool = result.get("name")
            elif result.get("name") == pending_error_tool:
                pending_error_tool = None

    return {
        "turn_count": turn_count,
        "assistant_turns": assistant_turns,
        "tool_call_count": tool_call_count,
        "distinct_tools": distinct_tools,
        "char_count": char_count,
        "error_count": error_count,
        "retry_count": retry_count,
    }


def detect_outcome_signals(turns: List[Turn]) -> dict:
    """Scan user turns for positive/negative acks; scan tool calls for a completion marker."""
    user_positive_ack = False
    user_negative_ack = False
    task_completed_marker = False

    for t in turns:
        if t.role == "user":
            text = t.text or ""
            if _POSITIVE_RE.search(text):
                user_positive_ack = True
            if _NEGATIVE_RE.search(text):
                user_negative_ack = True
        for call in t.tool_calls:
            name = call.get("name") or ""
            input_summary = call.get("input_summary") or ""
            if _TASK_COMPLETED_RE.search(name) or _TASK_COMPLETED_RE.search(input_summary):
                task_completed_marker = True

    return {
        "explicit_user_rating": None,
        "user_positive_ack": user_positive_ack,
        "user_negative_ack": user_negative_ack,
        "task_completed_marker": task_completed_marker,
        "notes": "",
    }


class Adapter:
    """Interface every host adapter implements."""

    host = "generic"

    def locate(self, config) -> list:
        """Return source refs (paths/ids), newest first."""
        raise NotImplementedError

    def load(self, ref, config) -> Session:
        """Load a single source ref into a Session."""
        raise NotImplementedError
