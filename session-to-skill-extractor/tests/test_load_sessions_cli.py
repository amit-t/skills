import json
import subprocess
import sys
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS_DIR))
from adapters import ADAPTERS

LOAD_SESSIONS = SCRIPTS_DIR / "load_sessions.py"


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


if __name__ == "__main__":
    unittest.main()
