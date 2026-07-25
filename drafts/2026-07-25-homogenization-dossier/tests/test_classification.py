import unittest

import _pathfix  # noqa: F401
from envelope import classify, reverse_sublabel, metric_report, UNITS, EXTENSION_UNITS


class TestClassifyDirect(unittest.TestCase):
    def test_no_anomaly(self):
        self.assertEqual(classify(a_ref=False, a_ext=False, delta=-2.0), "NO-ANOMALY")
        self.assertEqual(classify(a_ref=False, a_ext=False, delta=None), "NO-ANOMALY")

    def test_continue(self):
        self.assertEqual(classify(a_ref=True, a_ext=True, delta=-0.6), "CONTINUE")

    def test_new_onset(self):
        self.assertEqual(classify(a_ref=False, a_ext=True, delta=-0.7), "NEW-ONSET")

    def test_plateau(self):
        self.assertEqual(classify(a_ref=True, a_ext=True, delta=-0.2), "PLATEAU")
        self.assertEqual(classify(a_ref=True, a_ext=True, delta=0.0), "PLATEAU")

    def test_reverse(self):
        self.assertEqual(classify(a_ref=True, a_ext=False, delta=0.6), "REVERSE")
        self.assertEqual(classify(a_ref=True, a_ext=True, delta=0.5), "REVERSE")

    def test_residual_boundary_noise(self):
        # A_ref only, delta inside (-0.5, 0.5): none of the labeled buckets apply.
        self.assertIsNone(classify(a_ref=True, a_ext=False, delta=0.1))

    def test_boundary_delta_exactly_minus_half_is_continue(self):
        self.assertEqual(classify(a_ref=True, a_ext=True, delta=-0.5), "CONTINUE")

    def test_boundary_delta_exactly_half_is_reverse_not_plateau(self):
        # |delta| < 0.5 is PLATEAU's condition; delta == 0.5 fails that (not < 0.5)
        # and satisfies REVERSE's delta >= 0.5.
        self.assertEqual(classify(a_ref=True, a_ext=True, delta=0.5), "REVERSE")


class TestIntegrationScenarios(unittest.TestCase):
    """Build full 23-unit series (via metric_report) that exercise each labeled
    outcome end-to-end, through the actual envelope fit + anomaly rule."""

    def _flat_series(self, value=10.0):
        return [(unit, x, value) for x, unit in enumerate(UNITS)]

    def _with_overrides(self, base_value, overrides):
        series = self._flat_series(base_value)
        out = []
        for unit, x, v in series:
            out.append((unit, x, overrides.get(unit, v)))
        return out

    def test_continue_scenario(self):
        # Flat envelope at 10.0 with tiny zig-zag noise for a nonzero SE. Reference
        # window dips moderately (mild out-of-band); extension window dips much
        # deeper (12x the deviation) -> both windows anomalous, and the extension
        # deviation is deeper than the reference one by well over the 0.5 delta
        # threshold -> CONTINUE (or its NEW-ONSET sub-label; A_ref is True here, so
        # plain CONTINUE is expected).
        series = []
        for x, unit in enumerate(UNITS):
            if x < 16:
                wiggle = 0.01 if x % 2 == 0 else -0.01
                series.append((unit, x, 10.0 + wiggle))
            else:
                series.append((unit, x, 10.0))
        overrides = {
            "2023H1": 5.0, "2023H2": 5.0,     # reference window: mild, 2 consecutive out-of-band
            "2025H1": -50.0, "2025H2": -50.0,  # extension window: deep, 2 consecutive out-of-band
        }
        series = [(u, x, overrides.get(u, v)) for (u, x, v) in series]
        report = metric_report("test_metric", "low", series)
        self.assertTrue(report["a_ref"])
        self.assertTrue(report["a_ext"])
        self.assertLessEqual(report["delta"], -0.5)
        self.assertEqual(report["label"], "CONTINUE")

    def test_new_onset_scenario(self):
        series = []
        for x, unit in enumerate(UNITS):
            if x < 16:
                wiggle = 0.01 if x % 2 == 0 else -0.01
                series.append((unit, x, 10.0 + wiggle))
            else:
                series.append((unit, x, 10.0))
        overrides = {
            "2025H2": 0.0, "2026H1": 0.0,   # only extension window out-of-band
        }
        series = [(u, x, overrides.get(u, v)) for (u, x, v) in series]
        report = metric_report("test_metric", "low", series)
        self.assertFalse(report["a_ref"])
        self.assertTrue(report["a_ext"])
        self.assertLessEqual(report["delta"], -0.5)
        self.assertEqual(report["label"], "NEW-ONSET")

    def test_no_anomaly_scenario(self):
        series = []
        for x, unit in enumerate(UNITS):
            wiggle = 0.01 if x % 2 == 0 else -0.01
            series.append((unit, x, 10.0 + (wiggle if x < 16 else 0.0)))
        report = metric_report("test_metric", "low", series)
        self.assertFalse(report["a_ref"])
        self.assertFalse(report["a_ext"])
        self.assertEqual(report["label"], "NO-ANOMALY")


class TestReverseSublabel(unittest.TestCase):
    def test_full_when_all_extension_units_inside_interval(self):
        rows = [{"unit": u, "z": 0.1} for u in EXTENSION_UNITS]
        self.assertEqual(reverse_sublabel(rows, EXTENSION_UNITS), "FULL")

    def test_partial_when_one_unit_outside_interval(self):
        rows = [{"unit": u, "z": 0.1} for u in EXTENSION_UNITS]
        rows[0]["z"] = 5.0
        self.assertEqual(reverse_sublabel(rows, EXTENSION_UNITS), "PARTIAL")


if __name__ == "__main__":
    unittest.main()
