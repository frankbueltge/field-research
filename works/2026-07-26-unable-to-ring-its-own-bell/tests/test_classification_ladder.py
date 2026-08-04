import unittest

import _pathfix  # noqa: F401
import envelope_units as eu


class TestClassificationLadder(unittest.TestCase):
    """PREREGISTRATION.md §6, fixed order, first match wins. Each branch reached by
    a synthetic (a_ref, a_ext, delta) triple."""

    def test_no_anomaly(self):
        self.assertEqual(eu.classify(False, False, 0.0), "NO-ANOMALY")
        # NO-ANOMALY wins even with an extreme delta, since it is checked first.
        self.assertEqual(eu.classify(False, False, -99.0), "NO-ANOMALY")

    def test_new_onset(self):
        self.assertEqual(eu.classify(False, True, -0.5), "NEW-ONSET")
        self.assertEqual(eu.classify(False, True, -1.2), "NEW-ONSET")

    def test_continue(self):
        # a_ref True distinguishes CONTINUE from NEW-ONSET (which requires not a_ref).
        self.assertEqual(eu.classify(True, True, -0.5), "CONTINUE")
        self.assertEqual(eu.classify(True, True, -2.0), "CONTINUE")

    def test_plateau(self):
        self.assertEqual(eu.classify(True, True, 0.0), "PLATEAU")
        self.assertEqual(eu.classify(False, True, 0.49), "PLATEAU")
        self.assertEqual(eu.classify(True, True, -0.49), "PLATEAU")

    def test_reverse(self):
        self.assertEqual(eu.classify(True, False, 0.5), "REVERSE")
        self.assertEqual(eu.classify(False, True, 0.5), "REVERSE")
        self.assertEqual(eu.classify(True, True, 2.0), "REVERSE")

    def test_residual_no_eligible_delta(self):
        self.assertEqual(eu.classify(True, False, 0.0), "RESIDUAL")
        self.assertEqual(eu.classify(True, False, 0.49), "RESIDUAL")

    def test_residual_when_delta_is_none(self):
        self.assertEqual(eu.classify(True, True, None), "RESIDUAL")
        self.assertEqual(eu.classify(False, False, None), "NO-ANOMALY")  # still checked first


class TestReverseSublabel(unittest.TestCase):
    def test_full_when_every_extension_unit_inside_band(self):
        rows = [{"index": i, "z": 0.1} for i in range(61, 74)]
        self.assertEqual(eu.reverse_sublabel(rows, 61, 73, t_crit=2.0), "FULL")

    def test_partial_when_one_extension_unit_outside_band(self):
        rows = [{"index": i, "z": 0.1} for i in range(61, 74)]
        rows[3]["z"] = 5.0  # index 64, |z| >= t_crit
        self.assertEqual(eu.reverse_sublabel(rows, 61, 73, t_crit=2.0), "PARTIAL")


class TestNonDecidable(unittest.TestCase):
    """A window with fewer than 2 computable units is undecidable for that metric,
    labelled NON-DECIDABLE and excluded from §7's counts."""

    def test_window_decidable_false_below_two_computable(self):
        rows = [{"index": i, "value": (1.0 if i == 61 else None)} for i in range(61, 74)]
        self.assertFalse(eu.window_decidable(rows, 61, 73))

    def test_window_decidable_true_at_exactly_two_computable(self):
        rows = [{"index": i, "value": (1.0 if i in (61, 62) else None)} for i in range(61, 74)]
        self.assertTrue(eu.window_decidable(rows, 61, 73))

    def test_metric_report_labels_non_decidable(self):
        # Only one computable value anywhere in the extension window.
        series = [(x, 3.0 + 2.0 * x) for x in range(1, 61)] + [(61, 999.0)] + \
                 [(x, None) for x in range(62, 74)]
        report = eu.metric_report("synthetic", "low", series, 1, 47, "two_consecutive")
        self.assertFalse(report["ext_decidable"])
        self.assertEqual(report["label"], "NON-DECIDABLE")


class TestSingleChannelDowngrade(unittest.TestCase):
    """PREREGISTRATION.md §7: if the only two anomalous metrics are hapax_share and
    top50_mass, the finding is labelled SINGLE-CHANNEL, not ordinary >=2-of-4
    corroboration."""

    @staticmethod
    def _metric(ext_decidable, a_ext, label, ref_decidable=True, a_ref=False):
        return {"ext_decidable": ext_decidable, "a_ext": a_ext, "label": label,
                "ref_decidable": ref_decidable, "a_ref": a_ref}

    def test_hapax_and_top50_alone_triggers_single_channel(self):
        metrics_dict = {
            "mtld": self._metric(True, False, "NO-ANOMALY"),
            "hapax_share": self._metric(True, True, "CONTINUE"),
            "top50_mass": self._metric(True, True, "CONTINUE"),
            "similarity": self._metric(True, False, "NO-ANOMALY"),
        }
        result = eu.evaluate_verdict(metrics_dict, list(eu.MARGIN_METRIC_DIRECTIONS.keys()))
        self.assertEqual(result["step"], 1)
        self.assertTrue(result["single_channel"])
        self.assertEqual(result["headline_state"], "SINGLE-CHANNEL")
        self.assertIn("SINGLE-CHANNEL", result["verdict"])

    def test_other_pairs_do_not_trigger_single_channel(self):
        metrics_dict = {
            "mtld": self._metric(True, True, "CONTINUE"),
            "hapax_share": self._metric(True, True, "CONTINUE"),
            "top50_mass": self._metric(True, False, "NO-ANOMALY"),
            "similarity": self._metric(True, False, "NO-ANOMALY"),
        }
        result = eu.evaluate_verdict(metrics_dict, list(eu.MARGIN_METRIC_DIRECTIONS.keys()))
        self.assertEqual(result["step"], 1)
        self.assertFalse(result["single_channel"])
        self.assertNotEqual(result["headline_state"], "SINGLE-CHANNEL")

    def test_three_anomalous_including_the_pair_does_not_trigger(self):
        # hapax_share + top50_mass + mtld anomalous -- not "the only two".
        metrics_dict = {
            "mtld": self._metric(True, True, "CONTINUE"),
            "hapax_share": self._metric(True, True, "CONTINUE"),
            "top50_mass": self._metric(True, True, "CONTINUE"),
            "similarity": self._metric(True, False, "NO-ANOMALY"),
        }
        result = eu.evaluate_verdict(metrics_dict, list(eu.MARGIN_METRIC_DIRECTIONS.keys()))
        self.assertFalse(result["single_channel"])

    def test_kill_condition_at_most_one_anomalous(self):
        metrics_dict = {
            "mtld": self._metric(True, False, "NO-ANOMALY"),
            "hapax_share": self._metric(True, False, "NO-ANOMALY"),
            "top50_mass": self._metric(True, False, "NO-ANOMALY"),
            "similarity": self._metric(True, False, "NO-ANOMALY", a_ref=True),
        }
        result = eu.evaluate_verdict(metrics_dict, list(eu.MARGIN_METRIC_DIRECTIONS.keys()))
        self.assertEqual(result["step"], 2)
        self.assertEqual(result["headline_state"], "NO SIGNAL")
        self.assertEqual(result["verdict"], "NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT")
        # Dated correction, 2026-08-04 (session 87). This verdict is void as
        # evidence and may never be produced without the notice beside it. If a
        # later edit drops the marking at the source, this assertion fails here,
        # in the module that produces the string. See ../CORRECTIONS.md.
        self.assertEqual(result["verdict_status"], eu.VERDICT_VOID_NOTICE)
        self.assertIn("VOID AS EVIDENCE", result["verdict_status"])


if __name__ == "__main__":
    unittest.main()
