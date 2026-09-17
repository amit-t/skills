import json
import os
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from adapters.devin import DevinAdapter

FIXTURES_DIR = Path(__file__).resolve().parent / "fixtures" / "devin"
SESSION_DETAIL = FIXTURES_DIR / "session_detail.json"


class TestDevinAdapterLoadFromFile(unittest.TestCase):
    """Paste/export-first: devin_session_files config points straight at JSON files."""

    def setUp(self):
        self.session = DevinAdapter().load(str(SESSION_DETAIL), {})

    def test_host_is_devin(self):
        self.assertEqual(self.session.host, "devin")

    def test_session_id_from_detail(self):
        self.assertEqual(self.session.session_id, "devin-fixture-001")

    def test_roles_mapped_correctly(self):
        self.assertEqual(
            [t.role for t in self.session.turns],
            ["user", "assistant", "assistant", "user"],
        )

    def test_text_from_message_field(self):
        self.assertIn("flaky test", self.session.turns[0].text)

    def test_timestamps_carried_through(self):
        self.assertEqual(self.session.started_at, "2026-09-10T12:00:00Z")
        self.assertEqual(self.session.ended_at, "2026-09-10T12:45:00Z")

    def test_user_positive_ack_detected(self):
        self.assertTrue(self.session.outcome_signals["user_positive_ack"])


class TestDevinAdapterLocateViaConfigFiles(unittest.TestCase):
    def test_locate_returns_configured_glob_matches(self):
        refs = DevinAdapter().locate({"devin_session_files": [str(SESSION_DETAIL)]})
        self.assertEqual(refs, [str(SESSION_DETAIL)])

    def test_locate_config_files_take_priority_over_api_key(self):
        with mock.patch.dict(os.environ, {"DEVIN_API_KEY": "fake-key"}):
            refs = DevinAdapter().locate({"devin_session_files": [str(SESSION_DETAIL)]})
        self.assertEqual(refs, [str(SESSION_DETAIL)])


class TestDevinAdapterLocateNoSource(unittest.TestCase):
    def test_locate_returns_empty_list_when_no_files_and_no_key(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("DEVIN_API_KEY", None)
            refs = DevinAdapter().locate({})
        self.assertEqual(refs, [])

    def test_locate_never_raises_when_nothing_configured(self):
        with mock.patch.dict(os.environ, {}, clear=False):
            os.environ.pop("DEVIN_API_KEY", None)
            try:
                refs = DevinAdapter().locate({"devin_session_files": []})
            except Exception as exc:  # pragma: no cover - failure path
                self.fail(f"locate() raised unexpectedly: {exc}")
        self.assertEqual(refs, [])


class TestDevinAdapterLocateViaApi(unittest.TestCase):
    """API path is mocked -- no real network calls in tests."""

    def _fake_response(self, payload):
        body = json.dumps(payload).encode("utf-8")

        class _Resp:
            def __enter__(self_inner):
                return self_inner

            def __exit__(self_inner, *exc_info):
                return False

            def read(self_inner):
                return body

        return _Resp()

    def test_locate_lists_sessions_via_api_when_key_set(self):
        with mock.patch.dict(os.environ, {"DEVIN_API_KEY": "fake-key"}):
            with mock.patch("adapters.devin.urllib.request.urlopen") as mock_urlopen:
                mock_urlopen.return_value = self._fake_response(
                    {"sessions": [{"session_id": "sess-a"}, {"session_id": "sess-b"}]}
                )
                refs = DevinAdapter().locate({})

        self.assertEqual(len(refs), 2)
        self.assertEqual(refs[0]["session_id"], "sess-a")
        self.assertEqual(refs[0]["api_key"], "fake-key")

        request = mock_urlopen.call_args[0][0]
        self.assertEqual(request.get_header("Authorization"), "Bearer fake-key")

    def test_locate_api_failure_returns_empty_list_not_raise(self):
        with mock.patch.dict(os.environ, {"DEVIN_API_KEY": "fake-key"}):
            with mock.patch(
                "adapters.devin.urllib.request.urlopen",
                side_effect=urllib.error.URLError("boom"),
            ):
                try:
                    refs = DevinAdapter().locate({})
                except Exception as exc:  # pragma: no cover - failure path
                    self.fail(f"locate() raised unexpectedly: {exc}")
        self.assertEqual(refs, [])

    def test_load_via_api_ref_fetches_session_detail(self):
        detail = json.loads(SESSION_DETAIL.read_text())
        with mock.patch("adapters.devin.urllib.request.urlopen") as mock_urlopen:
            mock_urlopen.return_value = self._fake_response(detail)
            session = DevinAdapter().load({"kind": "api", "session_id": "devin-fixture-001", "api_key": "fake-key"}, {})

        self.assertEqual(session.session_id, "devin-fixture-001")
        self.assertEqual(len(session.turns), 4)

    def test_load_via_api_http_error_raises_clean_message_no_traceback(self):
        with mock.patch(
            "adapters.devin.urllib.request.urlopen",
            side_effect=urllib.error.HTTPError("url", 401, "Unauthorized", {}, None),
        ):
            with self.assertRaises(ValueError) as ctx:
                DevinAdapter().load({"kind": "api", "session_id": "sess-x", "api_key": "bad-key"}, {})
        message = str(ctx.exception)
        self.assertNotIn("Traceback", message)
        self.assertIn("sess-x", message)


if __name__ == "__main__":
    unittest.main()
