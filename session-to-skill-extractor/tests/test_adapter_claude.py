import json
import os
import sys
import tempfile
import time
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from adapters.claude_code import ClaudeCodeAdapter

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"
CLAUDE_FIXTURE = FIXTURES_DIR / "claude_code" / "sample.jsonl"

EXPECTED_SESSION_ID = "cc-sess-2026-09-15-abcd1234"
EXPECTED_CWD = "/Users/dev/projects/widget-app"


class TestClaudeCodeAdapterLoad(unittest.TestCase):
    def setUp(self):
        self.session = ClaudeCodeAdapter().load(str(CLAUDE_FIXTURE), {})

    def test_drops_meta_and_sidechain_lines_role_sequence(self):
        self.assertEqual(
            [t.role for t in self.session.turns],
            ["user", "assistant", "tool", "assistant", "tool", "assistant", "user"],
        )

    def test_host_is_claude_code(self):
        self.assertEqual(self.session.host, "claude-code")

    def test_error_count_from_tool_result_is_error(self):
        stats = self.session.to_dict()["stats"]
        self.assertEqual(stats["error_count"], 1)

    def test_user_positive_ack_detected(self):
        self.assertTrue(self.session.outcome_signals["user_positive_ack"])

    def test_session_id_from_first_kept_line(self):
        self.assertEqual(self.session.session_id, EXPECTED_SESSION_ID)

    def test_cwd_from_kept_line(self):
        self.assertEqual(self.session.cwd, EXPECTED_CWD)

    def test_started_and_ended_at_use_first_and_last_kept_timestamps(self):
        # The dropped meta/sidechain lines are earlier than 10:00:00 — started_at
        # must come from the first *kept* line, not the raw first line in the file.
        self.assertEqual(self.session.started_at, "2026-09-15T10:00:00Z")
        self.assertEqual(self.session.ended_at, "2026-09-15T10:01:20Z")

    def test_tool_only_turn_has_no_text(self):
        tool_turns = [t for t in self.session.turns if t.role == "tool"]
        self.assertEqual(len(tool_turns), 2)
        for turn in tool_turns:
            self.assertEqual(turn.text, "")
            self.assertEqual(len(turn.tool_results), 1)

    def test_tool_calls_captured_on_assistant_turns(self):
        assistant_turns = [t for t in self.session.turns if t.role == "assistant"]
        tool_call_names = [
            call["name"] for turn in assistant_turns for call in turn.tool_calls
        ]
        self.assertEqual(tool_call_names, ["Bash", "Edit"])

    def test_thinking_blocks_excluded_from_text(self):
        first_assistant = self.session.turns[1]
        self.assertNotIn("Check for a vitest config", first_assistant.text)
        self.assertIn("Let me check the current jest configuration first.", first_assistant.text)


class TestClaudeCodeAdapterLocate(unittest.TestCase):
    def test_locate_with_claude_projects_dir_override_finds_one_file(self):
        adapter = ClaudeCodeAdapter()
        refs = adapter.locate({"claude_projects_dir": str(FIXTURES_DIR)})
        self.assertEqual(len(refs), 1)
        self.assertTrue(refs[0].endswith("claude_code/sample.jsonl") or refs[0].endswith("claude_code\\sample.jsonl"))

    def test_locate_excludes_files_older_than_lookback(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            project_dir = root / "old-project"
            project_dir.mkdir()
            old_file = project_dir / "old-session.jsonl"
            old_file.write_text('{"type": "user", "sessionId": "x", "timestamp": "2020-01-01T00:00:00Z", "message": {"role": "user", "content": "hi"}}\n')
            old_time = time.time() - (10 * 86400)
            os.utime(old_file, (old_time, old_time))

            adapter = ClaudeCodeAdapter()
            refs = adapter.locate({
                "claude_projects_dir": str(root),
                "filter": {"lookback_days": 1},
            })
            self.assertEqual(refs, [])

    def test_locate_default_root_is_dot_claude_projects(self):
        # No override: locate() must not raise even if ~/.claude/projects doesn't exist.
        adapter = ClaudeCodeAdapter()
        refs = adapter.locate({})
        self.assertIsInstance(refs, list)


class TestClaudeCodeAdapterMalformedLines(unittest.TestCase):
    def test_malformed_line_is_skipped_not_fatal(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write('{not valid json at all\n')
            f.write(
                json.dumps({
                    "type": "user",
                    "sessionId": "malformed-test-session",
                    "timestamp": "2026-09-16T00:00:00Z",
                    "cwd": "/tmp/proj",
                    "message": {"role": "user", "content": "hello"},
                })
                + "\n"
            )
            path = f.name
        try:
            session = ClaudeCodeAdapter().load(path, {})
            self.assertEqual(len(session.turns), 1)
            self.assertEqual(session.turns[0].role, "user")
            self.assertEqual(session.session_id, "malformed-test-session")
        finally:
            Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
