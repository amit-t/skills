"""Codex adapter: loads local Codex CLI rollout JSONL files.

Each Codex session is one JSONL file under
`~/.codex/sessions/<YYYY>/<MM>/<DD>/rollout-<id>.jsonl`, one JSON object per
line. Every line has the shape `{"ordinal", "timestamp", "type", "payload"}`.

Line `type`s handled:
- `session_meta`: carries session_id/cwd/started_at in `payload`.
- `response_item`: the actual conversation content, itself tagged by
  `payload["type"]` -- `message`, `function_call`, `custom_tool_call`,
  `function_call_output`, `custom_tool_call_output`, `reasoning`,
  `agent_message`.
- everything else (`event_msg`, `turn_context`, `world_state`,
  `token_usage_record`, ...) is metadata/telemetry and is skipped.
"""
import glob
import json
import os
import re
import time
from pathlib import Path

from adapters.base import Adapter, Session, Turn, detect_outcome_signals

DEFAULT_SESSIONS_DIR = "~/.codex/sessions"
DEFAULT_LOOKBACK_DAYS = 1

_ENV_CONTEXT_PREFIXES = ("<environment_context>", "<user_instructions>")
_EXIT_CODE_RE = re.compile(r'"exit_code"\s*:\s*(-?\d+)')


def _extract_message_text(content):
    """Join input_text/output_text blocks from a message payload's content list."""
    if isinstance(content, str):
        return content
    if not isinstance(content, list):
        return ""
    parts = []
    for block in content:
        if isinstance(block, dict) and block.get("type") in ("input_text", "output_text"):
            parts.append(block.get("text", ""))
    return "".join(parts)


def _input_summary(payload):
    """arguments (function_call, a JSON string) or input (custom_tool_call), first 200 chars."""
    raw = payload.get("arguments")
    if raw is None:
        raw = payload.get("input")
    if raw is None:
        raw = ""
    if not isinstance(raw, str):
        raw = json.dumps(raw)
    return raw[:200]


def _output_ok(output):
    """Best-effort success heuristic: not a nonzero exit_code, not an ERROR-prefixed message."""
    if isinstance(output, dict):
        exit_code = output.get("exit_code")
        if isinstance(exit_code, (int, float)) and not isinstance(exit_code, bool) and exit_code != 0:
            return False
        text = output.get("output")
        text = text if isinstance(text, str) else ""
    else:
        text = output if isinstance(output, str) else ("" if output is None else str(output))
        match = _EXIT_CODE_RE.search(text)
        if match and int(match.group(1)) != 0:
            return False
    if text.startswith("ERROR") or text.startswith("error:"):
        return False
    return True


def _current_assistant_turn(turns):
    """The last turn if it's an assistant turn, so sequential tool calls with no
    intervening message accumulate on it; otherwise None (caller creates one)."""
    if turns and turns[-1].role == "assistant":
        return turns[-1]
    return None


class CodexAdapter(Adapter):
    host = "codex"

    def locate(self, config) -> list:
        config = config or {}
        root = config.get("codex_sessions_dir") or DEFAULT_SESSIONS_DIR
        root = str(Path(root).expanduser())
        lookback_days = (config.get("filter") or {}).get("lookback_days", DEFAULT_LOOKBACK_DAYS)
        cutoff = time.time() - (lookback_days * 86400)

        pattern = str(Path(root) / "*" / "*" / "*" / "rollout-*.jsonl")
        matches = [p for p in glob.glob(pattern) if os.path.getmtime(p) >= cutoff]
        return sorted(matches, key=lambda p: os.path.getmtime(p), reverse=True)

    def load(self, ref, config) -> Session:
        path = Path(ref)
        turns = []
        call_names = {}
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

                ended_at = obj.get("timestamp") or ended_at

                line_type = obj.get("type")
                payload = obj.get("payload")
                if not isinstance(payload, dict):
                    continue

                if line_type == "session_meta":
                    if session_id is None:
                        session_id = payload.get("id") or payload.get("session_id")
                        cwd = payload.get("cwd")
                        started_at = payload.get("timestamp")
                    continue

                if line_type != "response_item":
                    # event_msg, turn_context, world_state, token_usage_record, ...
                    continue

                item_type = payload.get("type")

                if item_type == "message":
                    role = payload.get("role")
                    if role not in ("user", "assistant"):
                        continue  # drops "developer" and anything unexpected
                    text = _extract_message_text(payload.get("content"))
                    if role == "user" and text.startswith(_ENV_CONTEXT_PREFIXES):
                        continue
                    turns.append(Turn(role=role, text=text, timestamp=obj.get("timestamp")))

                elif item_type in ("function_call", "custom_tool_call"):
                    name = payload.get("name")
                    call_id = payload.get("call_id")
                    if call_id:
                        call_names[call_id] = name
                    turn = _current_assistant_turn(turns)
                    if turn is None:
                        turn = Turn(role="assistant", timestamp=obj.get("timestamp"))
                        turns.append(turn)
                    turn.tool_calls.append({
                        "name": name,
                        "input_summary": _input_summary(payload),
                    })

                elif item_type in ("function_call_output", "custom_tool_call_output"):
                    call_id = payload.get("call_id")
                    output = payload.get("output")
                    turns.append(Turn(
                        role="tool",
                        tool_results=[{
                            "name": call_names.get(call_id, ""),
                            "ok": _output_ok(output),
                            "output_summary": str(output)[:200] if output is not None else "",
                        }],
                        timestamp=obj.get("timestamp"),
                    ))

                # else: reasoning, agent_message -- skipped (inter-agent chatter,
                # not user-facing content worth extracting).

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
