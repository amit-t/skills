import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT = Path(__file__).resolve().parents[2] / "distill-project/scripts/check_style.py"


class CheckStyleTest(unittest.TestCase):
    def test_flags_banned_words_em_dash_and_markdown_emphasis(self):
        with tempfile.TemporaryDirectory() as folder:
            text = Path(folder) / "input.md"
            text.write_text("Never use: synergy\nThis synergy claim — has **bold** text.\n")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(text), "--banned", "synergy", "--no-markdown"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 1)
            self.assertIn("3 issue(s)", result.stdout)
            self.assertIn("[em dash]", result.stdout)
            self.assertIn("[banned: synergy]", result.stdout)
            self.assertIn("[markdown emphasis]", result.stdout)

    def test_accepts_clean_text(self):
        with tempfile.TemporaryDirectory() as folder:
            text = Path(folder) / "input.md"
            text.write_text("Use dates as 16 Sep 2026.\n")
            result = subprocess.run(
                [sys.executable, str(SCRIPT), str(text), "--banned", "synergy", "--no-markdown"],
                text=True,
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0)
            self.assertIn("0 issue(s)", result.stdout)

    def test_checker_source_passes_its_own_rules(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(SCRIPT)],
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
