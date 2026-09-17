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


def _write_temp(text, suffix=".txt"):
    with tempfile.NamedTemporaryFile("w", suffix=suffix, delete=False) as f:
        f.write(text)
        return f.name


class TestGenericAdapterFallback(unittest.TestCase):
    """Malformed input must never raise; it always degrades to one user turn."""

    def _load_and_check(self, text, suffix=".txt"):
        path = _write_temp(text, suffix=suffix)
        try:
            session = GenericAdapter().load(path, {})
        finally:
            Path(path).unlink()
        self.assertEqual(len(session.turns), 1)
        self.assertEqual(session.turns[0].role, "user")
        return session

    def test_empty_file_falls_back_to_one_user_turn(self):
        self._load_and_check("")

    def test_invalid_json_lines_fall_back_to_one_user_turn(self):
        self._load_and_check('{"role": "user", "text": "hi"\n{not json at all\n', suffix=".jsonl")

    def test_unstructured_text_falls_back_to_one_user_turn(self):
        self._load_and_check("just some random log output\nwith no structure at all\n")


if __name__ == "__main__":
    unittest.main()
