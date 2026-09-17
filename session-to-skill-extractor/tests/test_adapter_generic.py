import sys, tempfile, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from adapters.generic import GenericAdapter

FIXTURE = Path(__file__).resolve().parent / "fixtures" / "generic" / "plain.txt"


class TestGenericAdapterPlainText(unittest.TestCase):
    def test_load_plain_text_turns_and_roles(self):
        session = GenericAdapter().load(str(FIXTURE), {})
        self.assertEqual(len(session.turns), 3)
        self.assertEqual([t.role for t in session.turns], ["user", "assistant", "user"])
        self.assertEqual(session.host, "generic")


class TestGenericAdapterJsonl(unittest.TestCase):
    def test_load_jsonl_turns(self):
        with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False) as f:
            f.write('{"role":"user","text":"hi"}\n')
            f.write('{"role":"assistant","text":"yo"}\n')
            path = f.name
        try:
            session = GenericAdapter().load(path, {})
            self.assertEqual(len(session.turns), 2)
            self.assertEqual([t.role for t in session.turns], ["user", "assistant"])
        finally:
            Path(path).unlink()


if __name__ == "__main__":
    unittest.main()
