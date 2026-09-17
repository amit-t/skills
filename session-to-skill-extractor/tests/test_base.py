import sys, unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from adapters.base import Turn, Session, compute_stats, detect_outcome_signals

def turns_with_error_recovery():
    return [
        Turn(role="user", text="please migrate the tests"),
        Turn(role="assistant", text="running", tool_calls=[{"name": "bash", "input_summary": "npx jest"}],
             tool_results=[{"name": "bash", "ok": False, "output_summary": "ERR"}]),
        Turn(role="assistant", text="trying vitest", tool_calls=[{"name": "bash", "input_summary": "npx vitest"}],
             tool_results=[{"name": "bash", "ok": True, "output_summary": "pass"}]),
        Turn(role="user", text="perfect, that worked"),
    ]

class TestStats(unittest.TestCase):
    def test_counts(self):
        s = compute_stats(turns_with_error_recovery())
        self.assertEqual(s["turn_count"], 4)
        self.assertEqual(s["assistant_turns"], 2)
        self.assertEqual(s["tool_call_count"], 2)
        self.assertEqual(s["distinct_tools"], ["bash"])
        self.assertEqual(s["error_count"], 1)
        self.assertEqual(s["retry_count"], 1)

class TestRetryStrictAdjacency(unittest.TestCase):
    def test_intervening_different_tool_breaks_retry(self):
        turns = [
            Turn(role="assistant", tool_calls=[{"name": "bash", "input_summary": "npx jest"}],
                 tool_results=[{"name": "bash", "ok": False, "output_summary": "ERR"}]),
            Turn(role="assistant", tool_calls=[{"name": "read", "input_summary": "cat foo"}],
                 tool_results=[{"name": "read", "ok": True, "output_summary": "ok"}]),
            Turn(role="assistant", tool_calls=[{"name": "bash", "input_summary": "npx jest"}],
                 tool_results=[{"name": "bash", "ok": True, "output_summary": "pass"}]),
        ]
        self.assertEqual(compute_stats(turns)["retry_count"], 0)

    def test_immediate_same_tool_retry_counts(self):
        turns = [
            Turn(role="assistant", tool_calls=[{"name": "bash", "input_summary": "npx jest"}],
                 tool_results=[{"name": "bash", "ok": False, "output_summary": "ERR"}]),
            Turn(role="assistant", tool_calls=[{"name": "bash", "input_summary": "npx jest"}],
                 tool_results=[{"name": "bash", "ok": True, "output_summary": "pass"}]),
        ]
        self.assertEqual(compute_stats(turns)["retry_count"], 1)


class TestOutcome(unittest.TestCase):
    def test_positive_ack(self):
        o = detect_outcome_signals(turns_with_error_recovery())
        self.assertTrue(o["user_positive_ack"]); self.assertFalse(o["user_negative_ack"])
    def test_negative_ack(self):
        o = detect_outcome_signals([Turn(role="user", text="that's wrong, revert")])
        self.assertTrue(o["user_negative_ack"])

class TestSessionDict(unittest.TestCase):
    def test_schema_shape(self):
        d = Session(session_id="s1", host="generic", turns=turns_with_error_recovery()).to_dict()
        for k in ("session_id","host","source_path","started_at","ended_at","cwd","turns","stats","outcome_signals"):
            self.assertIn(k, d)
        self.assertEqual(d["turns"][0]["role"], "user")

if __name__ == "__main__": unittest.main()
