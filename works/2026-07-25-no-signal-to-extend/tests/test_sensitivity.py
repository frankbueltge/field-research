import unittest

import _pathfix  # noqa: F401
from envelope import UNITS, EXTENSION_UNITS, build_metric_table, anomaly_in_window
from sensitivity import (
    inject_unit_values,
    fires_at,
    power_curve_for_metric,
    power_curve_for_stratum,
    injection_grid,
    INJECTION_GRID_STEP,
)


def _synthetic_series(a=10.0, b=-0.1, wiggle=0.02):
    """A 23-unit (unit, x, value) series whose first 16 (envelope) points lie on
    y = a + b*x with a small deterministic zig-zag (nonzero but tiny residual
    variance, so se > 0); the three extension units sit exactly on that same
    line (baseline z ~ 0), giving a clean starting point to inject a
    collapse-direction shift away from."""
    series = []
    for x, unit in enumerate(UNITS):
        if x < 16:
            w = wiggle if x % 2 == 0 else -wiggle
            series.append((unit, x, a + b * x + w))
        else:
            series.append((unit, x, a + b * x))
    return series


class TestInjectionDirection(unittest.TestCase):
    """The shift must move each metric in ITS OWN collapse direction -- an
    additive, sign-aware shift off |yhat|, never a multiplicative rescale that
    would move a negative-valued trend (zipf_slope, ~-0.9) or a 'high'-direction
    metric (similarity) the wrong way."""

    def test_low_direction_always_decreases_value_regardless_of_yhat_sign(self):
        unit_values = [(u, x, 10.0) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS]
        # one positive yhat, two negative yhats -- direction of the shift must not
        # depend on the sign of yhat, only on its magnitude
        yhat_by_unit = {"2025H1": 5.0, "2025H2": -5.0, "2026H1": -5.0}
        injected = inject_unit_values(unit_values, "low", 0.1, yhat_by_unit)
        for (unit, x, v_new), (_, _, v_old) in zip(injected, unit_values):
            self.assertLess(v_new, v_old, f"{unit}: 'low' injection must decrease value")
            self.assertAlmostEqual(v_new, v_old - 0.1 * abs(yhat_by_unit[unit]), places=9)

    def test_high_direction_always_increases_value_regardless_of_yhat_sign(self):
        unit_values = [(u, x, 10.0) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS]
        yhat_by_unit = {"2025H1": 5.0, "2025H2": -5.0, "2026H1": -5.0}
        injected = inject_unit_values(unit_values, "high", 0.1, yhat_by_unit)
        for (unit, x, v_new), (_, _, v_old) in zip(injected, unit_values):
            self.assertGreater(v_new, v_old, f"{unit}: 'high' injection must increase value")
            self.assertAlmostEqual(v_new, v_old + 0.1 * abs(yhat_by_unit[unit]), places=9)

    def test_negative_valued_trend_still_moves_collapse_direction(self):
        # zipf_slope-shaped case: yhat itself is negative (~-0.9); a 'low'
        # (collapse=down) injection must still make the value MORE negative, not
        # less -- this is exactly the case a naive value*(1-d) rescale gets
        # backwards (multiplying a negative number by (1-d) < 1 makes it less
        # negative, which reads as an IMPROVEMENT, not a collapse).
        unit_values = [(u, x, -0.9) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS]
        yhat_by_unit = {u: -0.9 for u in EXTENSION_UNITS}
        injected = inject_unit_values(unit_values, "low", 0.2, yhat_by_unit)
        for (unit, x, v_new) in injected:
            self.assertLess(v_new, -0.9, f"{unit}: collapse-direction shift must be MORE negative")

    def test_untouched_units_pass_through_unchanged(self):
        series = _synthetic_series()
        injected = inject_unit_values(series, "low", 0.5, {u: 8.0 for u in EXTENSION_UNITS})
        for (unit, x, v_new), (_, _, v_old) in zip(injected, series):
            if unit in EXTENSION_UNITS:
                continue
            self.assertEqual(v_new, v_old, f"{unit}: non-extension unit must be untouched")


class TestZeroInjectionReproducesFrozenLabels(unittest.TestCase):
    def test_d_zero_is_the_identity(self):
        series = _synthetic_series()
        yhat_by_unit = {u: (10.0 + -0.1 * x) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS}
        injected = inject_unit_values(series, "low", 0.0, yhat_by_unit)
        self.assertEqual(injected, series)

    def test_d_zero_reproduces_the_unmodified_anomaly_call(self):
        series = _synthetic_series()
        yhat_by_unit = {u: (10.0 + -0.1 * x) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS}
        baseline_fit, baseline_rows = build_metric_table(series, "low")
        baseline_a_ext = anomaly_in_window(baseline_rows, EXTENSION_UNITS)
        self.assertEqual(fires_at(series, "low", 0.0, yhat_by_unit), baseline_a_ext)
        # the synthetic fixture sits exactly on the fitted line at every
        # extension unit, so the unmodified frozen call must NOT fire
        self.assertFalse(baseline_a_ext)


class TestLargeInjectionFires(unittest.TestCase):
    def test_large_low_injection_fires(self):
        series = _synthetic_series(a=10.0, b=-0.1)
        yhat_by_unit = {u: (10.0 + -0.1 * x) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS}
        self.assertTrue(fires_at(series, "low", 0.3, yhat_by_unit))

    def test_large_high_injection_fires(self):
        series = _synthetic_series(a=0.05, b=0.0, wiggle=0.001)
        yhat_by_unit = {u: 0.05 for u in EXTENSION_UNITS}
        self.assertTrue(fires_at(series, "high", 0.3, yhat_by_unit))

    def test_tiny_injection_does_not_fire(self):
        series = _synthetic_series(a=10.0, b=-0.1)
        yhat_by_unit = {u: (10.0 + -0.1 * x) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS}
        self.assertFalse(fires_at(series, "low", INJECTION_GRID_STEP, yhat_by_unit))


class TestSmallestFiringDIsMonotone(unittest.TestCase):
    def test_grid_is_monotone_once_fired_stays_fired(self):
        series = _synthetic_series(a=10.0, b=-0.1)
        yhat_by_unit = {u: (10.0 + -0.1 * x) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS}
        grid = injection_grid()
        fires_by_d, smallest = power_curve_for_metric(series, "low", yhat_by_unit, grid)
        self.assertIsNotNone(smallest, "the constructed series must fire somewhere on the grid")
        seen_true = False
        for d, fires in zip(grid, fires_by_d):
            if fires:
                seen_true = True
            if seen_true:
                self.assertTrue(fires, f"d={d}: rule must stay fired once it has fired at a smaller d")

    def test_below_smallest_never_fires_at_or_above_always_does(self):
        series = _synthetic_series(a=10.0, b=-0.1)
        yhat_by_unit = {u: (10.0 + -0.1 * x) for x, u in enumerate(UNITS) if u in EXTENSION_UNITS}
        grid = injection_grid()
        _, smallest = power_curve_for_metric(series, "low", yhat_by_unit, grid)
        self.assertIsNotNone(smallest)
        idx = grid.index(smallest)
        # one grid step below the smallest firing d must not fire (guards
        # against an off-by-one in how "smallest" is picked out of the grid)
        if idx > 0:
            self.assertFalse(fires_at(series, "low", grid[idx - 1], yhat_by_unit))
        # the step at and just above the smallest firing d must both fire
        self.assertTrue(fires_at(series, "low", smallest, yhat_by_unit))
        if idx + 1 < len(grid):
            self.assertTrue(fires_at(series, "low", grid[idx + 1], yhat_by_unit))


class TestPowerCurveForStratum(unittest.TestCase):
    def test_two_of_four_uses_the_same_d_across_metrics(self):
        # Four metrics built from the IDENTICAL series (same envelope fit, same
        # baseline-on-the-line extension units): only "unit"/"x"/"value"/"yhat"
        # from each row are used downstream (power_curve_for_stratum recomputes
        # direction-aware z/out_of_band itself from envelope.MARGIN_METRIC_DIRECTIONS),
        # so all four metrics' smallest_firing_d must come out identical, and the
        # >=2-of-4 threshold must equal that same shared value.
        series = _synthetic_series(a=10.0, b=-0.1)
        _, rows = build_metric_table(series, "low")
        stratum_block = {
            "metrics": {
                m: {"rows": rows} for m in ("mtld", "hapax_share", "zipf_slope", "similarity")
            }
        }
        grid = injection_grid()
        result = power_curve_for_stratum(stratum_block, grid)
        individual = [result["metrics"][m]["smallest_firing_d"] for m in result["metrics"]]
        self.assertTrue(all(d == individual[0] for d in individual))
        self.assertEqual(result["smallest_d_two_of_four_metrics"], individual[0])


if __name__ == "__main__":
    unittest.main()
