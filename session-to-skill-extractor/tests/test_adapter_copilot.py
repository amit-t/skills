import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from adapters.copilot import CopilotAdapter

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "copilot"
LAYOUT1_DIR = FIXTURES_DIR / "session-state" / "sess-layout1"
LAYOUT2_STATE_JSON = FIXTURES_DIR / "history-session-state" / "abc" / "state.json"

NOTES_MARKER = "copilot db has no message bodies; use paste fallback for full text"


def _make_sessions_db(db_path, rows):
    """rows: list of (id, title, session_type, model, created_at) tuples."""
    conn = sqlite3.connect(str(db_path))
    try:
        conn.execute(
            "CREATE TABLE sessions (id TEXT, title TEXT, session_type TEXT, model TEXT, created_at TEXT)"
        )
        conn.executemany(
            "INSERT INTO sessions (id, title, session_type, model, created_at) VALUES (?, ?, ?, ?, ?)",
            rows,
        )
        conn.commit()
    finally:
        conn.close()


class TestCopilotAdapterLayout1SessionStateDir(unittest.TestCase):
    """~/.copilot/session-state/<id>/ per-session dir, file names UNVERIFIED (best-effort)."""

    def setUp(self):
        refs = CopilotAdapter().locate({"copilot_dir": str(FIXTURES_DIR)})
        self.assertEqual(len(refs), 1)
        self.session = CopilotAdapter().load(refs[0], {})

    def test_host_is_copilot(self):
        self.assertEqual(self.session.host, "copilot")

    def test_at_least_two_turns_parsed(self):
        self.assertGreaterEqual(len(self.session.turns), 2)

    def test_roles_in_order(self):
        self.assertEqual(
            [t.role for t in self.session.turns],
            ["user", "assistant", "user"],
        )

    def test_session_id_from_file(self):
        self.assertEqual(self.session.session_id, "copilot-sess-layout1")


class TestCopilotAdapterLayout2HistorySessionState(unittest.TestCase):
    """Legacy history-session-state/<id>/state.json shape (host-notes: schema unverified)."""

    def setUp(self):
        self.session = CopilotAdapter().load(str(LAYOUT2_STATE_JSON), {})

    def test_host_is_copilot(self):
        self.assertEqual(self.session.host, "copilot")

    def test_at_least_two_turns_parsed(self):
        self.assertGreaterEqual(len(self.session.turns), 2)

    def test_roles_in_order(self):
        self.assertEqual(
            [t.role for t in self.session.turns],
            ["user", "assistant", "user"],
        )

    def test_session_id_and_started_at(self):
        self.assertEqual(self.session.session_id, "copilot-sess-legacy-abc")
        self.assertEqual(self.session.started_at, "2026-08-01T09:00:00Z")


class TestCopilotAdapterDbMetadataOnly(unittest.TestCase):
    """sessions table in session-store.db/data.db is metadata-only -- no message bodies."""

    def test_data_db_only_yields_one_metadata_session_with_notes_marker(self):
        with tempfile.TemporaryDirectory() as tmp:
            db_path = Path(tmp) / "data.db"
            _make_sessions_db(
                db_path,
                [("sess-1", "Fix flaky CI", "chat", "gpt-4.1", "2026-09-01T00:00:00Z")],
            )

            adapter = CopilotAdapter()
            refs = adapter.locate({"copilot_dir": tmp})
            self.assertEqual(len(refs), 1)

            session = adapter.load(refs[0], {})
            self.assertEqual(session.host, "copilot")
            self.assertEqual(len(session.turns), 1)
            self.assertEqual(session.turns[0].role, "user")
            self.assertEqual(session.outcome_signals["notes"], NOTES_MARKER)

    def test_session_store_db_preferred_over_data_db(self):
        with tempfile.TemporaryDirectory() as tmp:
            _make_sessions_db(
                Path(tmp) / "session-store.db",
                [("sess-preferred", "Preferred db", "chat", "gpt-4.1", "2026-09-02T00:00:00Z")],
            )
            _make_sessions_db(
                Path(tmp) / "data.db",
                [("sess-other", "Other db", "chat", "gpt-4.1", "2026-09-01T00:00:00Z")],
            )

            adapter = CopilotAdapter()
            refs = adapter.locate({"copilot_dir": tmp})
            self.assertEqual(len(refs), 1)
            session = adapter.load(refs[0], {})
            self.assertEqual(session.session_id, "sess-preferred")

    def test_corrupt_session_store_db_falls_through_to_data_db(self):
        with tempfile.TemporaryDirectory() as tmp:
            (Path(tmp) / "session-store.db").write_text("not a sqlite database")
            _make_sessions_db(
                Path(tmp) / "data.db",
                [("sess-fallback", "Fallback db", "chat", "gpt-4.1", "2026-09-01T00:00:00Z")],
            )

            adapter = CopilotAdapter()
            refs = adapter.locate({"copilot_dir": tmp})
            self.assertEqual(len(refs), 1)
            session = adapter.load(refs[0], {})
            self.assertEqual(session.session_id, "sess-fallback")


class TestCopilotAdapterLocateProbeOrder(unittest.TestCase):
    def test_session_state_dirs_take_priority(self):
        refs = CopilotAdapter().locate({"copilot_dir": str(FIXTURES_DIR)})
        # FIXTURES_DIR has both session-state/ and history-session-state/ --
        # session-state/ must win.
        self.assertTrue(all(isinstance(r, dict) and r.get("kind") == "session_dir" for r in refs))

    def test_missing_copilot_dir_returns_empty_list(self):
        with tempfile.TemporaryDirectory() as tmp:
            refs = CopilotAdapter().locate({"copilot_dir": str(Path(tmp) / "does-not-exist")})
            self.assertEqual(refs, [])

    def test_default_root_does_not_crash(self):
        refs = CopilotAdapter().locate({})
        self.assertIsInstance(refs, list)


if __name__ == "__main__":
    unittest.main()
