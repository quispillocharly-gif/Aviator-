import importlib.util
import pathlib
import unittest

MODULE = pathlib.Path(__file__).resolve().parents[1] / "scripts" / "actualizar.py"
spec = importlib.util.spec_from_file_location("orbit", MODULE)
orbit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(orbit)


def summary(rounds, wins):
    return {"data": {
        "claim": {"rtp": .97},
        "measurement": {
            "rounds": rounds, "rtp": 2*wins/rounds, "ci95": [.95, .98],
            "asOf": "2026-10-17T19:00:00Z"
        }
    }}


class AuditTests(unittest.TestCase):
    def test_no_alert_at_claim_rate(self):
        s = [{"n": 10000, "winsAt2x": 4850},
             {"n": 11000, "winsAt2x": 5335}]
        a = orbit.audit(s, summary(11000, 5335), None)
        self.assertEqual(a["status"], "no_statistical_flag")
        self.assertEqual(a["window"]["rounds"], 1000)
        self.assertEqual(a["window"]["winsAt2x"], 485)
        self.assertFalse(a["canPredictNextRound"])

    def test_strong_deviation_is_only_exploratory_alert(self):
        s = [{"n": 10000, "winsAt2x": 4850},
             {"n": 11000, "winsAt2x": 5450}]
        a = orbit.audit(s, summary(11000, 5450), None)
        self.assertEqual(a["status"], "review_anomaly")
        self.assertLess(a["window"]["exploratoryPValue"], .001)
        self.assertFalse(a["hasFutureSeed"])

    def test_no_false_alarm_without_incremental_rounds(self):
        s = [{"n": 10000, "winsAt2x": 4850},
             {"n": 10350, "winsAt2x": 5030}]
        a = orbit.audit(s, summary(10350, 5030), None)
        self.assertEqual(a["status"], "insufficient_new_rounds")
        self.assertIsNone(a["window"])

    def test_sample_interval(self):
        ci=orbit.wilson(485, 1000)
        self.assertTrue(ci[0] < .485 < ci[1])
        self.assertEqual(len(ci), 2)


if __name__ == "__main__":
    unittest.main()
