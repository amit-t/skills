"""Copilot (GitHub Copilot CLI/chat) adapter.

Probe order under `~/.copilot` (overridable via config `copilot_dir`):

1. `session-state/<id>/` per-session directories. The exact file name(s)
   Copilot writes inside each directory are UNVERIFIED, so this is parsed
   best-effort: every `*.json` file in the directory is tried in turn, and
   the first one containing a message list under a common key
   (`chatMessages`, `messages`, `events`) with role/content-ish fields wins.
2. `history-session-state/<id>/state.json`, the legacy shape
   `{"sessionId", "startTime", "chatMessages": [{"role", "content"}, ...]}`.
   # unverified: this exact shape could not be confirmed against a real
   # Copilot install; it is the minimal shape implied by the directory name
   # and is used as a best-effort fallback.
3. SQLite `session-store.db`, then `data.db`. Their `sessions` table is
   METADATA ONLY (columns like id, title, session_type, model, created_at,
   updated_at -- no message bodies), so a DB-sourced Session is a single
   user turn summarizing the metadata, with `outcome_signals["notes"]`
   pointing at the paste fallback for full text.

Every layer degrades to "nothing found here" rather than raising: a host
whose local layout doesn't match any of the above should never crash the
run, only skip that source (the run-level location has no error channel per
`Adapter.locate() -> list`, see per-layer comments below).
"""
import glob
import json
import os
import sqlite3
from pathlib import Path

from adapters.base import Adapter, Session, Turn, detect_outcome_signals

DEFAULT_COPILOT_DIR = "~/.copilot"
_DB_NAMES = ("session-store.db", "data.db")
_METADATA_NOTE = "copilot db has no message bodies; use paste fallback for full text"


def _role_from_raw(raw):
    """Best-effort role normalization. # unverified: exact role vocabulary Copilot uses."""
    raw = (raw or "").strip().lower()
    if not raw:
        return "user"
    if "system" in raw:
        return None  # dropped, like "developer" lines in other adapters
    if "assistant" in raw or "copilot" in raw or raw in ("bot", "ai"):
        return "assistant"
    if "tool" in raw:
        return "tool"
    if "user" in raw or raw == "human":
        return "user"
    return "user"


def _text_from_message(msg):
    content = msg.get("content")
    if content is None:
        content = msg.get("text")
    if content is None:
        content = msg.get("message")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for block in content:
            if isinstance(block, dict):
                parts.append(block.get("text") or block.get("content") or "")
            elif isinstance(block, str):
                parts.append(block)
        return "".join(parts)
    return "" if content is None else str(content)


def _message_to_turn(msg):
    if not isinstance(msg, dict):
        return None
    raw_role = msg.get("role") or msg.get("type") or msg.get("author")
    role = _role_from_raw(raw_role)
    if role is None:
        return None
    timestamp = msg.get("timestamp") or msg.get("time") or msg.get("createdAt")
    return Turn(role=role, text=_text_from_message(msg), timestamp=timestamp)


def _find_message_list(obj):
    """First non-empty list under a common message-list key, in priority order."""
    if not isinstance(obj, dict):
        return None
    for key in ("chatMessages", "messages", "events"):
        val = obj.get(key)
        if isinstance(val, list) and val:
            return val
    return None


def _messages_to_turns(messages):
    turns = []
    for msg in messages:
        turn = _message_to_turn(msg)
        if turn is not None:
            turns.append(turn)
    return turns


def _session_from_message_obj(obj, session_id_fallback, source_path):
    messages = _find_message_list(obj)
    if messages is None:
        return None
    turns = _messages_to_turns(messages)
    session_id = obj.get("sessionId") or obj.get("session_id") or session_id_fallback
    started_at = obj.get("startTime") or obj.get("started_at")
    ended_at = None
    for turn in reversed(turns):
        if turn.timestamp:
            ended_at = turn.timestamp
            break
    session = Session(
        session_id=session_id,
        host="copilot",
        source_path=source_path,
        started_at=started_at,
        ended_at=ended_at or started_at,
    )
    session.turns = turns
    session.outcome_signals = detect_outcome_signals(turns)
    return session


class CopilotAdapter(Adapter):
    host = "copilot"

    def locate(self, config) -> list:
        config = config or {}
        root = Path(config.get("copilot_dir") or DEFAULT_COPILOT_DIR).expanduser()

        session_dirs = sorted(
            (p for p in glob.glob(str(root / "session-state" / "*")) if os.path.isdir(p)),
            key=os.path.getmtime,
            reverse=True,
        )
        if session_dirs:
            return [{"kind": "session_dir", "path": p} for p in session_dirs]

        state_files = sorted(
            glob.glob(str(root / "history-session-state" / "*" / "state.json")),
            key=os.path.getmtime,
            reverse=True,
        )
        if state_files:
            return [{"kind": "state_json", "path": p} for p in state_files]

        for db_name in _DB_NAMES:
            db_path = root / db_name
            if not db_path.exists():
                continue
            try:
                rows = self._read_sessions_table(str(db_path))
            except Exception:
                # unverified: real session-store.db/data.db schema and
                # availability. Any failure opening/querying it (locked,
                # missing table, corrupt file, unexpected columns) must
                # degrade to "no sessions found here", not crash -- and
                # locate()'s return type carries no error channel, so this
                # is the only signal we can give; the next db_name (or an
                # eventual empty list) is what the caller sees.
                continue
            if rows:
                return [{"kind": "db_row", "db_path": str(db_path), "row": row} for row in rows]

        return []

    def _read_sessions_table(self, db_path):
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            conn.row_factory = sqlite3.Row
            cur = conn.execute("SELECT * FROM sessions ORDER BY created_at DESC")
            return [dict(row) for row in cur.fetchall()]
        finally:
            conn.close()

    def load(self, ref, config) -> Session:
        if isinstance(ref, dict):
            kind = ref.get("kind")
            if kind == "db_row":
                return self._load_db_row(ref)
            if kind == "state_json":
                return self._load_state_json(Path(ref["path"]))
            if kind == "session_dir":
                return self._load_session_dir(Path(ref["path"]))
            raise ValueError(f"copilot: unrecognized ref kind: {kind!r}")

        # Back-compat: a bare path string, mirroring other adapters' contract.
        path = Path(ref)
        if path.is_dir():
            return self._load_session_dir(path)
        return self._load_state_json(path)

    def _load_state_json(self, path):
        obj = json.loads(path.read_text(encoding="utf-8", errors="replace"))
        if not isinstance(obj, dict):
            raise ValueError(f"copilot state file is not a JSON object: {path}")
        session = _session_from_message_obj(obj, session_id_fallback=path.stem, source_path=str(path))
        if session is None:
            raise ValueError(
                f"copilot: no chatMessages/messages/events list found in {path}"
            )
        return session

    def _load_session_dir(self, dir_path):
        candidates = sorted(glob.glob(str(dir_path / "*.json")))
        for candidate in candidates:
            try:
                obj = json.loads(Path(candidate).read_text(encoding="utf-8", errors="replace"))
            except ValueError:
                continue
            if not isinstance(obj, dict):
                continue
            session = _session_from_message_obj(
                obj, session_id_fallback=dir_path.name, source_path=candidate
            )
            if session is not None:
                return session
        raise ValueError(
            f"copilot: no message-bearing json found in session dir: {dir_path}"
        )

    def _load_db_row(self, ref):
        row = ref.get("row") or {}
        session_id = str(row.get("id") or row.get("session_id") or "unknown-copilot-session")
        title = row.get("title") or "(untitled)"
        model = row.get("model") or "unknown model"
        session_type = row.get("session_type") or "unknown"
        started_at = row.get("created_at")
        ended_at = row.get("updated_at") or started_at

        note_turn = Turn(
            role="user",
            text=f'Copilot session "{title}" (type={session_type}, model={model})',
            timestamp=started_at,
        )
        turns = [note_turn]
        outcome_signals = detect_outcome_signals(turns)
        outcome_signals["notes"] = _METADATA_NOTE

        session = Session(
            session_id=session_id,
            host=self.host,
            source_path=ref.get("db_path"),
            started_at=started_at,
            ended_at=ended_at,
        )
        session.turns = turns
        session.outcome_signals = outcome_signals
        return session
