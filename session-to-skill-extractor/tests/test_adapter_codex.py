import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from adapters.codex import CodexAdapter

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CODEX_FIXTURE = FIXTURES_DIR / "codex" / "rollout-sample.jsonl"

EXPECTED_SESSION_ID = "codex-sess-2026-09-17-xyz789"
EXPECTED_CWD = "/Users/dev/projects/widget-api"


class TestCodexAdapterLoad(unittest.TestCase):
    def setUp(self):
        self.session = CodexAdapter().load(str(CODEX_FIXTURE), {})

    def test_host_is_codex(self):
        self.assertEqual(self.session.host, "codex")

    def test_session_id_and_cwd_from_session_meta(self):
        self.assertEqual(self.session.session_id, EXPECTED_SESSION_ID)
        self.assertEqual(self.session.cwd, EXPECTED_CWD)

    def test_started_at_from_session_meta_timestamp(self):
        self.assertEqual(self.session.started_at, "2026-09-17T09:00:00Z")

    def test_ended_at_from_last_line_timestamp(self):
        self.assertEqual(self.session.ended_at, "2026-09-17T09:00:45Z")

    def test_developer_and_environment_context_lines_dropped(self):
        texts = [t.text for t in self.session.turns]
        self.assertFalse(any("sandbox" in t for t in texts))
        self.assertFalse(any("environment_context" in t for t in texts))

    def test_reasoning_and_event_msg_lines_skipped(self):
        # 13 raw lines minus: developer(1), environment_context(1), reasoning(1),
        # event_msg(1), session_meta(1) = 8 lines that become turns, but the two
        # function_call lines attach onto assistant turns rather than creating
        # their own, so the turn count is lower still. Assert role sequence
        # directly instead of a bare count, since that pins the real behavior.
        self.assertEqual(
            [t.role for t in self.session.turns],
            ["user", "assistant", "tool", "assistant", "tool", "assistant", "user"],
        )

    def test_tool_call_pairing_yields_error_count_one(self):
        stats = self.session.to_dict()["stats"]
        self.assertEqual(stats["error_count"], 1)

    def test_tool_calls_are_named_shell(self):
        assistant_turns = [t for t in self.session.turns if t.role == "assistant"]
        names = [c["name"] for t in assistant_turns for c in t.tool_calls]
        self.assertEqual(names, ["shell", "shell"])

    def test_tool_call_input_summary_from_arguments(self):
        first_assistant = self.session.turns[1]
        self.assertIn("npx", first_assistant.tool_calls[0]["input_summary"])
        self.assertIn("jest", first_assistant.tool_calls[0]["input_summary"])

    def test_tool_result_ok_flags(self):
        tool_turns = [t for t in self.session.turns if t.role == "tool"]
        self.assertEqual(len(tool_turns), 2)
        self.assertFalse(tool_turns[0].tool_results[0]["ok"])
        self.assertTrue(tool_turns[1].tool_results[0]["ok"])

    def test_user_positive_ack_detected(self):
        self.assertTrue(self.session.outcome_signals["user_positive_ack"])


class TestCodexAdapterLocate(unittest.TestCase):
    def test_locate_finds_fixture_nested_under_year_month_day(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = Path(tmp) / "2026" / "09" / "17"
            nested.mkdir(parents=True)
            dest = nested / "rollout-sample.jsonl"
            shutil.copy(str(CODEX_FIXTURE), str(dest))

            adapter = CodexAdapter()
            refs = adapter.locate({"codex_sessions_dir": tmp})
            self.assertEqual(len(refs), 1)
            self.assertTrue(refs[0].endswith("rollout-sample.jsonl"))

    def test_locate_excludes_files_older_than_lookback(self):
        with tempfile.TemporaryDirectory() as tmp:
            nested = Path(tmp) / "2020" / "01" / "01"
            nested.mkdir(parents=True)
            old_file = nested / "rollout-old.jsonl"
            old_file.write_text('{"ordinal": 1, "timestamp": "2020-01-01T00:00:00Z", "type": "session_meta", "payload": {"id": "x", "cwd": "/tmp", "timestamp": "2020-01-01T00:00:00Z"}}\n')
            old_time = time.time() - (10 * 86400)
            os.utime(old_file, (old_time, old_time))

            adapter = CodexAdapter()
            refs = adapter.locate({
                "codex_sessions_dir": tmp,
                "filter": {"lookback_days": 1},
            })
            self.assertEqual(refs, [])

    def test_locate_default_root_is_dot_codex_sessions(self):
        # No override: locate() must not raise even if ~/.codex/sessions doesn't exist.
        adapter = CodexAdapter()
        refs = adapter.locate({})
        self.assertIsInstance(refs, list)


class TestCodexAdapterMalformedLines(unittest.TestCase):
    def test_malformed_line_is_skipped_not_fatal(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write("{not valid json at all\n")
            f.write(
                json.dumps({
                    "ordinal": 1,
                    "timestamp": "2026-09-16T00:00:00Z",
                    "type": "session_meta",
                    "payload": {
                        "id": "malformed-test-session",
                        "cwd": "/tmp/proj",
                        "timestamp": "2026-09-16T00:00:00Z",
                    },
                })
                + "\n"
            )
            f.write(
                json.dumps({
                    "ordinal": 2,
                    "timestamp": "2026-09-16T00:00:05Z",
                    "type": "response_item",
                    "payload": {
                        "type": "message",
                        "role": "user",
                        "content": [{"type": "input_text", "text": "hello"}],
                    },
                })
                + "\n"
            )
            path = f.name
        try:
            session = CodexAdapter().load(path, {})
            self.assertEqual(len(session.turns), 1)
            self.assertEqual(session.turns[0].role, "user")
            self.assertEqual(session.session_id, "malformed-test-session")
        finally:
            Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
