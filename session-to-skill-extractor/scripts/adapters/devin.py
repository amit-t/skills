"""Devin adapter: paste/export-first, with an optional Devin API fallback.

`locate` probe order:

1. Config `devin_session_files` -- a list of glob patterns pointing at
   exported/pasted session-detail JSON files. This is the primary path:
   Devin sessions live on Devin's own servers, so a local export or a
   pasted transcript is the reliable source.
2. Environment `DEVIN_API_KEY` set -- list sessions via
   `GET https://api.devin.ai/v1/sessions` (`Authorization: Bearer <key>`),
   then `load()` fetches each session's detail lazily via
   `GET https://api.devin.ai/v1/sessions/{session_id}`.
   # unverified: the exact list-sessions response envelope (assumed to be
   # `{"sessions": [...]}` or a bare list of `{"session_id"/"id": ...}`).
3. Neither configured -- return `[]`. There is no error channel on
   `Adapter.locate() -> list`, so the "tell the user to export/paste"
   guidance lives here as documentation, not a runtime return value; the
   caller sees an empty session list to load, same as any other adapter
   with nothing to find.

Session-detail shape (`messages[]` of `{"type", "event_id", "message",
"timestamp", "origin", "username"}`) per the Devin API: `origin`/`type`
containing "user" map to role "user"; containing "devin" or "assistant" map
to role "assistant"; anything else defaults to "user". Message text comes
from the `message` field.

API errors (bad key, network failure, timeout, malformed JSON) are turned
into a single clear `ValueError` message -- never left as a raw
urllib/socket exception or a traceback -- so a caller collecting per-ref
errors (like `load_sessions.py`) gets one readable line.
"""
import glob
import json
import os
import socket
import urllib.error
import urllib.request
from pathlib import Path

from adapters.base import Adapter, Session, Turn, detect_outcome_signals

API_BASE = "https://api.devin.ai/v1"
_API_TIMEOUT_SECONDS = 15


def _devin_role(msg):
    """type/origin containing "user" -> user; "devin"/"assistant" -> assistant; else user."""
    origin = str(msg.get("origin") or "").lower()
    msg_type = str(msg.get("type") or "").lower()
    combined = f"{origin} {msg_type}"
    if "user" in combined:
        return "user"
    if "devin" in combined or "assistant" in combined:
        return "assistant"
    return "user"


def _session_from_detail(obj, source_path):
    if not isinstance(obj, dict):
        raise ValueError(f"devin: session detail is not a JSON object: {source_path}")

    raw_messages = obj.get("messages") or []
    turns = []
    for msg in raw_messages:
        if not isinstance(msg, dict):
            continue
        turns.append(Turn(
            role=_devin_role(msg),
            text=msg.get("message") or "",
            timestamp=msg.get("timestamp"),
        ))

    session_id = obj.get("session_id") or obj.get("id") or Path(str(source_path)).stem
    started_at = obj.get("created_at") or (turns[0].timestamp if turns else None)
    ended_at = obj.get("updated_at") or (turns[-1].timestamp if turns else None)

    session = Session(
        session_id=str(session_id),
        host="devin",
        source_path=str(source_path),
        started_at=started_at,
        ended_at=ended_at,
    )
    session.turns = turns
    session.outcome_signals = detect_outcome_signals(turns)
    return session


class DevinAdapter(Adapter):
    host = "devin"

    def locate(self, config) -> list:
        config = config or {}
        patterns = config.get("devin_session_files")
        if patterns:
            matches = set()
            for pattern in patterns:
                matches.update(glob.glob(str(Path(pattern).expanduser())))
            return sorted(matches)

        api_key = os.environ.get("DEVIN_API_KEY")
        if not api_key:
            # No local export and no API key: paste-first design means we
            # simply have nothing to load. See module docstring re: the
            # "tell the user to export/paste" guidance.
            return []

        try:
            session_ids = self._list_session_ids(api_key)
        except Exception:
            # Never crash the run over a listing failure (bad key, network
            # down, unexpected envelope shape, ...); degrade to "nothing
            # found", same as the no-key case.
            return []

        return [{"kind": "api", "session_id": sid, "api_key": api_key} for sid in session_ids]

    def _list_session_ids(self, api_key):
        req = urllib.request.Request(
            f"{API_BASE}/sessions",
            headers={"Authorization": f"Bearer {api_key}"},
        )
        with urllib.request.urlopen(req, timeout=_API_TIMEOUT_SECONDS) as resp:
            body = json.loads(resp.read().decode("utf-8"))

        # unverified: exact envelope shape for the list-sessions response.
        if isinstance(body, dict):
            items = body.get("sessions") or body.get("data") or []
        elif isinstance(body, list):
            items = body
        else:
            items = []

        ids = []
        for item in items:
            if isinstance(item, dict):
                sid = item.get("session_id") or item.get("id")
                if sid:
                    ids.append(sid)
        return ids

    def load(self, ref, config) -> Session:
        if isinstance(ref, dict) and ref.get("kind") == "api":
            return self._load_via_api(ref["session_id"], ref["api_key"])
        return self._load_from_file(Path(ref))

    def _load_from_file(self, path):
        obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        return _session_from_detail(obj, source_path=str(path))

    def _load_via_api(self, session_id, api_key):
        url = f"{API_BASE}/sessions/{session_id}"
        req = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
        try:
            with urllib.request.urlopen(req, timeout=_API_TIMEOUT_SECONDS) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            raise ValueError(f"devin API error loading session {session_id}: HTTP {exc.code}") from None
        except urllib.error.URLError as exc:
            raise ValueError(f"devin API error loading session {session_id}: {exc.reason}") from None
        except socket.timeout:
            raise ValueError(f"devin API error loading session {session_id}: request timed out") from None

        try:
            obj = json.loads(raw)
        except ValueError:
            raise ValueError(f"devin API returned invalid JSON for session {session_id}") from None

        return _session_from_detail(obj, source_path=url)
