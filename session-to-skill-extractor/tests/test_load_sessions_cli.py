import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from adapters import ADAPTERS

LOAD_SESSIONS = SCRIPTS_DIR / "load_sessions.py"
FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures"


class TestAdaptersRegistry(unittest.TestCase):
    def test_generic_is_registered(self):
        self.assertIn("generic", ADAPTERS)


class TestLoadSessionsCliUnknownHost(unittest.TestCase):
    def test_unknown_host_exits_2_with_json_error_no_traceback(self):
        result = subprocess.run(
            [sys.executable, str(LOAD_SESSIONS), "--host", "nosuchhost", "--paths", "x", "--out", "/dev/stdout"],
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 2)
        self.assertNotIn("Traceback", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

        error = json.loads(result.stderr)
        self.assertEqual(error["error"], "unknown_host")
        self.assertEqual(error["host"], "nosuchhost")
        self.assertIn("generic", error["available_hosts"])


class TestLoadSessionsPathsBypassesLocate(unittest.TestCase):
    """Fix A: --paths must work for every adapter, not just generic -- it bypasses
    adapter.locate() entirely and loads each glob match directly via adapter.load()."""

    def test_paths_with_devin_host_loads_one_session(self):
        fixture = FIXTURES_DIR / "devin" / "session_detail.json"
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "out.json"
            result = subprocess.run(
                [
                    sys.executable, str(LOAD_SESSIONS),
                    "--host", "devin",
                    "--paths", str(fixture),
                    "--out", str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["errors"], [])
            self.assertEqual(len(data["sessions"]), 1)
            self.assertEqual(data["sessions"][0]["host"], "devin")

    def test_paths_with_claude_code_host_skips_store_discovery(self):
        fixture = FIXTURES_DIR / "claude_code" / "sample.jsonl"
        with tempfile.TemporaryDirectory() as tmp:
            empty_store = Path(tmp) / "empty-claude-store"
            empty_store.mkdir()
            config_path = Path(tmp) / "config.json"
            config_path.write_text(
                json.dumps({"claude_projects_dir": str(empty_store)}), encoding="utf-8"
            )
            out = Path(tmp) / "out.json"
            result = subprocess.run(
                [
                    sys.executable, str(LOAD_SESSIONS),
                    "--host", "claude-code",
                    "--paths", str(fixture),
                    "--config", str(config_path),
                    "--out", str(out),
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(data["errors"], [])
            # Proves the store was never scanned: claude_projects_dir points at an
            # empty dir, yet the explicit --paths file still loaded.
            self.assertEqual(len(data["sessions"]), 1)
            self.assertEqual(data["sessions"][0]["host"], "claude-code")


if __name__ == "__main__":
    unittest.main()
