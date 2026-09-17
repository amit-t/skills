import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from filter_sessions import filter_sessions

DEFAULT_CFG = {
    "filter": {
        "min_turns": 6,
        "min_tool_calls": 2,
        "min_assistant_turns_if_no_tools": 4,
        "max_sessions_per_run": 25,
        "lookback_days": 1,
    }
}

VALID_ADMITTED_BY = {"length", "complexity", "outcome", "novelty"}


def turn(role, text="", tool_calls=None, tool_results=None):
    """A minimal Task-2 Turn dict."""
    return {
        "role": role,
        "text": text,
        "tool_calls": tool_calls or [],
        "tool_results": tool_results or [],
        "timestamp": None,
    }


def mk(session_id, turns=None, outcome_signals=None, stats_override=None,
       host="claude-code", source_path="s.jsonl"):
    """A minimal Task-2 Session.to_dict()-shaped session, with stats derived from turns
    (unless overridden)."""
    turns = turns or []
    stats = {
        "turn_count": len(turns),
        "assistant_turns": sum(1 for t in turns if t.get("role") == "assistant"),
        "tool_call_count": sum(len(t.get("tool_calls") or []) for t in turns),
        "distinct_tools": sorted({
            c.get("name") for t in turns for c in (t.get("tool_calls") or []) if c.get("name")
        }),
        "char_count": sum(len(t.get("text") or "") for t in turns),
        "error_count": sum(
            1 for t in turns for r in (t.get("tool_results") or []) if r.get("ok") is False
        ),
        "retry_count": 0,
    }
    if stats_override:
        stats.update(stats_override)
    return {
        "session_id": session_id,
        "host": host,
        "source_path": source_path,
        "started_at": None,
        "ended_at": None,
        "cwd": None,
        "turns": turns,
        "stats": stats,
        "outcome_signals": outcome_signals or {
            "explicit_user_rating": None,
            "user_positive_ack": False,
            "user_negative_ack": False,
            "task_completed_marker": False,
            "notes": "",
        },
    }


def error_recovery_session(session_id="recover1"):
    turns = [
        turn("user", "please fix the failing build"),
        turn("assistant", "let me look at the test output"),
        turn("assistant", "running tests",
             tool_calls=[{"name": "Bash", "input_summary": "npx jest"}],
             tool_results=[{"name": "Bash", "ok": False, "output_summary": "ERR: failed"}]),
        turn("assistant", "trying a different approach",
             tool_calls=[{"name": "Read", "input_summary": "cat config"}],
             tool_results=[{"name": "Read", "ok": True, "output_summary": "config contents"}]),
        turn("assistant", "fixed it, re-running",
             tool_calls=[{"name": "Bash", "input_summary": "npx jest"}],
             tool_results=[{"name": "Bash", "ok": True, "output_summary": "pass"}]),
        turn("user", "perfect, that worked"),
    ]
    return mk(session_id, turns=turns, outcome_signals={
        "explicit_user_rating": None,
        "user_positive_ack": True,
        "user_negative_ack": False,
        "task_completed_marker": False,
        "notes": "",
    })


def plain_pass_session(session_id):
    turns = [
        turn("user", "add a helper function"),
        turn("assistant", "adding",
             tool_calls=[{"name": "Write", "input_summary": "helper.py"}],
             tool_results=[{"name": "Write", "ok": True, "output_summary": "written"}]),
        turn("assistant", "done",
             tool_calls=[{"name": "Write", "input_summary": "helper2.py"}],
             tool_results=[{"name": "Write", "ok": True, "output_summary": "written"}]),
        turn("user", "ok"),
        turn("assistant", "anything else?"),
        turn("user", "no thanks"),
    ]
    return mk(session_id, turns=turns)


class TestGateDrops(unittest.TestCase):
    """E3-1: trivial 2-turn no-tool Q&A session is dropped at the gate."""

    def test_trivial_qa_session_dropped(self):
        s = mk("qa1", turns=[turn("user", "what is python?"), turn("assistant", "a language")])
        filtered, dropped = filter_sessions([s], DEFAULT_CFG)
        self.assertEqual(filtered, [])
        self.assertEqual(len(dropped), 1)
        self.assertEqual(dropped[0]["session_id"], "qa1")


class TestSingleToolRepetition(unittest.TestCase):
    """E3-2: 30 Read calls, one tool, no adaptation -> dropped as single-tool repetition."""

    def test_thirty_read_calls_dropped(self):
        turns = [turn("user", "read all the files")]
        for i in range(30):
            turns.append(turn(
                "assistant", "reading",
                tool_calls=[{"name": "Read", "input_summary": "file%d" % i}],
                tool_results=[{"name": "Read", "ok": True, "output_summary": "ok"}],
            ))
        s = mk("repeat1", turns=turns)
        filtered, dropped = filter_sessions([s], DEFAULT_CFG)
        self.assertFalse(any(f["session_id"] == "repeat1" for f in filtered))
        reasons = {d["session_id"]: d["reason"] for d in dropped}
        self.assertEqual(reasons["repeat1"], "single-tool repetition")


class TestErrorRecoveryAdmitted(unittest.TestCase):
    """error->recovery + positive ack is admitted with novelty+outcome and ranks first."""

    def test_admitted_with_novelty_and_outcome_ranked_first(self):
        sessions = [
            plain_pass_session("plain1"),
            error_recovery_session("recover1"),
            plain_pass_session("plain2"),
        ]
        filtered, dropped = filter_sessions(sessions, DEFAULT_CFG)
        self.assertEqual(dropped, [])
        self.assertEqual(filtered[0]["session_id"], "recover1")
        self.assertTrue({"novelty", "outcome"}.issubset(set(filtered[0]["admitted_by"])))


class TestMaxSessionsCap(unittest.TestCase):
    """d: 3 sessions pass, max_sessions_per_run=2 -> capped to 2, highest score first."""

    def test_capped_at_max_sessions_per_run(self):
        sessions = [
            plain_pass_session("plain1"),
            error_recovery_session("recover1"),
            plain_pass_session("plain2"),
        ]
        cfg = {"filter": dict(DEFAULT_CFG["filter"], max_sessions_per_run=2)}
        filtered, dropped = filter_sessions(sessions, cfg)
        self.assertEqual(len(filtered), 2)
        self.assertEqual(filtered[0]["session_id"], "recover1")


class TestAdmittedByShape(unittest.TestCase):
    """e: every admitted entry's admitted_by is non-empty and a subset of the four categories."""

    def test_every_admitted_entry_has_nonempty_valid_admitted_by(self):
        sessions = [
            plain_pass_session("plain1"),
            error_recovery_session("recover1"),
            plain_pass_session("plain2"),
        ]
        filtered, dropped = filter_sessions(sessions, DEFAULT_CFG)
        self.assertTrue(filtered)
        for entry in filtered:
            self.assertTrue(entry["admitted_by"])
            self.assertTrue(set(entry["admitted_by"]).issubset(VALID_ADMITTED_BY))
            self.assertFalse(entry["excluded"])
            for key in ("session_id", "host", "source_path", "priority_score", "stats"):
                self.assertIn(key, entry)


class TestNullTolerance(unittest.TestCase):
    """Adapters may leave stats/outcome_signals fields null; the filter must not crash."""

    def test_missing_stats_and_outcome_fields_do_not_crash(self):
        s = {
            "session_id": "nullish",
            "host": "generic",
            "source_path": None,
            "turns": [],
            "stats": {"turn_count": 8},
            "outcome_signals": None,
        }
        filtered, dropped = filter_sessions([s], DEFAULT_CFG)
        self.assertEqual(filtered, [])
        self.assertEqual(len(dropped), 1)
        self.assertEqual(dropped[0]["session_id"], "nullish")


if __name__ == "__main__":
    unittest.main()
