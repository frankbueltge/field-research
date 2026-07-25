import unittest

import _pathfix  # noqa: F401
from envelope import (
    classify,
    reverse_sublabel,
    metric_report,
    _classify_from_rows,
    evaluate_stratum,
    plurality_bucket,
    UNITS,
    REFERENCE_UNITS,
    EXTENSION_UNITS,
    T_CRIT_LINEAR,
    MARGIN_METRIC_DIRECTIONS,
)


class TestClassifyDirect(unittest.TestCase):
    def test_no_anomaly(self):
        self.assertEqual(classify(a_ref=False, a_ext=False, delta=-2.0), "NO-ANOMALY")
        self.assertEqual(classify(a_ref=False, a_ext=False, delta=None), "NO-ANOMALY")

    def test_no_anomaly_even_with_large_positive_delta(self):
        # A swing between two never-anomalous windows is NO-ANOMALY, not REVERSE
        # (§6: REVERSE is gated on (A_ref OR A_ext) -- an anomaly must have been
        # established somewhere before "recovery" can be claimed).
        self.assertEqual(classify(a_ref=False, a_ext=False, delta=5.0), "NO-ANOMALY")

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

    def test_reverse_requires_a_ref_or_a_ext(self):
        # Gated: without an anomaly in EITHER window, a positive delta is NOT REVERSE
        # (already covered by test_no_anomaly_even_with_large_positive_delta, since
        # a_ref=a_ext=False routes to NO-ANOMALY before the REVERSE check is ever
        # reached -- this test documents that the gate is real, not just unreachable).
        self.assertNotEqual(classify(a_ref=False, a_ext=False, delta=0.6), "REVERSE")

    def test_residual_boundary_noise(self):
        # A_ref only, delta inside (-0.5, 0.5): none of the labeled buckets apply.
        # RESIDUAL is now an explicit label, not an absence of one.
        self.assertEqual(classify(a_ref=True, a_ext=False, delta=0.1), "RESIDUAL")

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


def _rows_from_z(ref_zs, ext_zs, threshold=T_CRIT_LINEAR):
    """Build the minimal `rows` shape _classify_from_rows() needs, directly from
    prescribed reoriented z-values for the 4 reference + 3 extension units -- bypasses
    OLS entirely, exactly matching how the coordinator's cases (A)-(G) are specified
    ("ref = 4 units, ext = 3 units; threshold -2.1448; delta = Delta_ext - Delta_ref")."""
    assert len(ref_zs) == 4
    assert len(ext_zs) == 3
    rows = []
    for unit, z in zip(REFERENCE_UNITS, ref_zs):
        rows.append({"unit": unit, "value": z, "z": z, "out_of_band": z < -threshold})
    for unit, z in zip(EXTENSION_UNITS, ext_zs):
        rows.append({"unit": unit, "value": z, "z": z, "out_of_band": z < -threshold})
    return rows


class TestClassificationLadderCases(unittest.TestCase):
    """The reconciliation round's seeded cases (A)-(G), verified against
    _classify_from_rows() directly on prescribed ref/ext z-series."""

    def test_case_a_continue(self):
        rows = _rows_from_z([-2.5, -2.3, -1.0, -0.9], [-3.0, -3.2, -3.1])
        result = _classify_from_rows(rows)
        self.assertTrue(result["a_ref"])
        self.assertTrue(result["a_ext"])
        self.assertLessEqual(result["delta"], -0.5)
        self.assertEqual(result["label"], "CONTINUE")

    def test_case_b_new_onset(self):
        rows = _rows_from_z([-1.0, -0.9, -1.0, -0.8], [-2.5, -2.6, -1.0])
        result = _classify_from_rows(rows)
        self.assertFalse(result["a_ref"])
        self.assertTrue(result["a_ext"])
        self.assertLessEqual(result["delta"], -0.5)
        self.assertEqual(result["label"], "NEW-ONSET")

    def test_case_c_plateau(self):
        rows = _rows_from_z([-2.5, -2.3, -1.0, -0.9], [-2.3, -2.4, -1.0])
        result = _classify_from_rows(rows)
        self.assertTrue(result["a_ref"])
        self.assertTrue(result["a_ext"])
        self.assertLess(abs(result["delta"]), 0.5)
        self.assertEqual(result["label"], "PLATEAU")

    def test_case_d_reverse_full(self):
        rows = _rows_from_z([-2.5, -2.4, -2.6, -2.5], [-0.2, 0.1, -0.1])
        result = _classify_from_rows(rows)
        self.assertTrue(result["a_ref"])
        self.assertFalse(result["a_ext"])
        self.assertGreaterEqual(result["delta"], 0.5)
        self.assertEqual(result["label"], "REVERSE")
        self.assertEqual(result["sub_label"], "FULL")

    def test_case_e_no_anomaly_not_reverse(self):
        rows = _rows_from_z([-1.5, -1.5, -1.0, -1.0], [0.0, -0.2, 0.0])
        result = _classify_from_rows(rows)
        self.assertFalse(result["a_ref"])
        self.assertFalse(result["a_ext"])
        # delta is large and positive here, which would satisfy REVERSE's delta
        # condition on its own -- the point of this case is that the (A_ref OR A_ext)
        # gate must still block it.
        self.assertGreaterEqual(result["delta"], 0.5)
        self.assertEqual(result["label"], "NO-ANOMALY")
        self.assertNotEqual(result["label"], "REVERSE")

    def test_case_f_stratum_headline_reverse_via_step3(self):
        # 2 metrics behave like case D (REVERSE, a_ref True / a_ext False), 2 behave
        # like case E (NO-ANOMALY). Step 1 (directional finding) needs >=2 EXT-
        # anomalous metrics -- both case-D and case-E metrics have a_ext False, so
        # step 1 cannot fire. Step 2 (kill) needs <=1 metric with any anomaly
        # (A_ref or A_ext) -- the 2 case-D metrics both have A_ref True, so kill
        # (<=1) doesn't fire either (2 > 1). It falls to step 3: plurality over all
        # four labels -- REVERSE has 2 votes, NO-ANOMALY (non-eligible) has 2 -> REVERSE.
        case_d_rows = _rows_from_z([-2.5, -2.4, -2.6, -2.5], [-0.2, 0.1, -0.1])
        case_e_rows = _rows_from_z([-1.5, -1.5, -1.0, -1.0], [0.0, -0.2, 0.0])
        case_d = _classify_from_rows(case_d_rows)
        case_e = _classify_from_rows(case_e_rows)
        self.assertEqual(case_d["label"], "REVERSE")
        self.assertEqual(case_e["label"], "NO-ANOMALY")

        metric_names = list(MARGIN_METRIC_DIRECTIONS)
        metrics_dict = {
            metric_names[0]: case_d,
            metric_names[1]: case_d,
            metric_names[2]: case_e,
            metric_names[3]: case_e,
        }
        math_info = {"marker_valid": True, "control_clear": True}
        result = evaluate_stratum(metrics_dict, math_info)

        self.assertEqual(result["step"], 3)
        self.assertFalse(result["kill_condition_met"])
        self.assertEqual(result["headline_state"], "REVERSE")

    def test_case_g_residual(self):
        rows = _rows_from_z([-2.5, -2.5, -1.0, -1.0], [-1.5, -1.5, -1.5])
        result = _classify_from_rows(rows)
        self.assertTrue(result["a_ref"])
        self.assertFalse(result["a_ext"])
        self.assertLess(result["delta"], 0.5)
        self.assertGreaterEqual(result["delta"], -0.5)
        self.assertEqual(result["label"], "RESIDUAL")


class TestPluralityBucket(unittest.TestCase):
    def test_tie_returns_tie_label(self):
        winner, bucket_counts, all_counts = plurality_bucket(
            ["CONTINUE", "REVERSE"], eligible_buckets=("DECLINE", "PLATEAU", "REVERSE"), tie_label="MIXED"
        )
        self.assertEqual(winner, "MIXED")

    def test_non_eligible_labels_excluded_from_winning_but_counted(self):
        winner, bucket_counts, all_counts = plurality_bucket(
            ["CONTINUE", "NO-ANOMALY", "NO-ANOMALY", "NO-ANOMALY"],
            eligible_buckets=("DECLINE", "PLATEAU", "REVERSE"),
            tie_label="MIXED",
        )
        # 3 NO-ANOMALY votes still can't win -- only 1 eligible (DECLINE) vote exists,
        # and it wins by default since it's the only nonzero eligible bucket.
        self.assertEqual(winner, "DECLINE")
        self.assertEqual(all_counts["NO-ANOMALY"], 3)

    def test_no_eligible_votes_at_all_is_tie_label(self):
        winner, bucket_counts, all_counts = plurality_bucket(
            ["NO-ANOMALY", "RESIDUAL", "NON-DECIDABLE"],
            eligible_buckets=("DECLINE", "PLATEAU", "REVERSE"),
            tie_label="MIXED",
        )
        self.assertEqual(winner, "MIXED")


if __name__ == "__main__":
    unittest.main()
