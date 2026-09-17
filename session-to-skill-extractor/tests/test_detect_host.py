import sys, unittest, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from detect_host import detect

class TestDetect(unittest.TestCase):
    def _home(self, dirs):
        h = Path(tempfile.mkdtemp())
        for d in dirs: (h / d).mkdir(parents=True)
        return h
    def test_claude_env(self):
        r = detect(env={"CLAUDECODE": "1"}, home=self._home([".claude/projects"]))
        self.assertEqual(r["host"], "claude-code"); self.assertEqual(r["confidence"], "high")
    def test_codex_env(self):
        self.assertEqual(detect(env={"CODEX_SANDBOX": "x"}, home=self._home([]))["host"], "codex")
    def test_bare_shell_is_generic_not_error(self):
        r = detect(env={}, home=self._home([]))
        self.assertEqual(r["host"], "generic"); self.assertEqual(r["session_sources"], [])
    def test_sources_enumerated_even_when_generic(self):
        r = detect(env={}, home=self._home([".claude/projects", ".codex/sessions"]))
        self.assertEqual({s["host"] for s in r["session_sources"]}, {"claude-code", "codex"})
    def test_override(self):
        self.assertEqual(detect(env={"CLAUDECODE": "1"}, home=self._home([]), override="devin")["host"], "devin")

if __name__ == "__main__": unittest.main()
