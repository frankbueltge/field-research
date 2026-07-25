import unittest

import _pathfix  # noqa: F401
from envelope import (
    fit_envelope_linear,
    pred_se_linear,
    build_metric_table,
    anomaly_in_window,
    window_mean_z,
    T_CRIT_LINEAR,
    UNITS,
    ENVELOPE_UNITS,
    REFERENCE_UNITS,
    EXTENSION_UNITS,
)


def _synthetic_envelope_series(a=10.0, b=-0.1, extra_by_unit=None):
    """Build a 23-unit (unit, x, value) series where the first 16 (envelope) points
    lie on y = a + b*x with a small deterministic zig-zag perturbation (so residual
    variance is nonzero but tiny), and later units default to sitting on the fitted
    line unless overridden via extra_by_unit={unit: value}."""
    extra_by_unit = extra_by_unit or {}
    series = []
    for x, unit in enumerate(UNITS):
        if unit in extra_by_unit:
            series.append((unit, x, extra_by_unit[unit]))
            continue
        if x < 16:
            wiggle = 0.02 if x % 2 == 0 else -0.02
            series.append((unit, x, a + b * x + wiggle))
        else:
            series.append((unit, x, a + b * x))
    return series


class TestOlsFit(unittest.TestCase):
    def test_fit_recovers_known_slope_and_intercept(self):
        xs = list(range(16))
        ys = [10.0 - 0.1 * x for x in xs]  # exact line, no noise
        fit = fit_envelope_linear(xs, ys)
        self.assertAlmostEqual(fit["a"], 10.0, places=9)
        self.assertAlmostEqual(fit["b"], -0.1, places=9)
        self.assertEqual(fit["df"], 14)

    def test_pred_se_positive_with_noise(self):
        series = _synthetic_envelope_series()
        xs = [x for (_, x, v) in series[:16]]
        ys = [v for (_, x, v) in series[:16]]
        fit = fit_envelope_linear(xs, ys)
        se = pred_se_linear(fit, 20)
        self.assertGreater(se, 0.0)


class TestOutOfBand(unittest.TestCase):
    def test_point_far_below_line_is_out_of_band(self):
        # yhat at x=20 (2025H1) is a + b*20; push the observed value far below it.
        series = _synthetic_envelope_series()
        a, b = 10.0, -0.1
        yhat_20 = a + b * 20
        far_below_unit = UNITS[20]
        series = _synthetic_envelope_series(extra_by_unit={far_below_unit: yhat_20 - 10.0})
        fit, rows = build_metric_table(series, "low")
        row = next(r for r in rows if r["unit"] == far_below_unit)
        self.assertLess(row["z"], -T_CRIT_LINEAR)
        self.assertTrue(row["out_of_band"])

    def test_point_on_the_line_is_not_out_of_band(self):
        # Fit the envelope from the (wiggled) 16 points first, then set each
        # extension unit's value to that FITTED line's own prediction -- this is
        # the only way to get an exact z == 0, since the fitted line (from noisy
        # points) is not identical to the generator's true a,b.
        base_series = _synthetic_envelope_series()
        env_xs = [x for (_, x, v) in base_series[:16]]
        env_ys = [v for (_, x, v) in base_series[:16]]
        fit = fit_envelope_linear(env_xs, env_ys)

        overrides = {unit: fit["a"] + fit["b"] * x for (unit, x, v) in base_series if x >= 16}
        series = _synthetic_envelope_series(extra_by_unit=overrides)
        fit2, rows = build_metric_table(series, "low")
        for unit in EXTENSION_UNITS:
            row = next(r for r in rows if r["unit"] == unit)
            self.assertFalse(row["out_of_band"])
            self.assertAlmostEqual(row["z"], 0.0, delta=1e-9)

    def test_high_direction_flips_sign(self):
        # For 'high' (similarity) direction, a value ABOVE the line is collapse and
        # must produce a NEGATIVE reoriented z (out-of-band on the collapse side).
        a, b = 0.05, 0.0
        series = _synthetic_envelope_series(a=a, b=b)
        yhat_20 = a + b * 20
        above_unit = UNITS[20]
        series = _synthetic_envelope_series(a=a, b=b, extra_by_unit={above_unit: yhat_20 + 1.0})
        fit, rows = build_metric_table(series, "high")
        row = next(r for r in rows if r["unit"] == above_unit)
        self.assertLess(row["z"], 0.0)
        self.assertGreater(row["z_raw"], 0.0)  # raw z is positive (value above line)

    def test_missing_envelope_point_raises(self):
        series = _synthetic_envelope_series()
        series[3] = (series[3][0], series[3][1], None)  # knock out one envelope point
        with self.assertRaises(ValueError):
            build_metric_table(series, "low")


class TestAnomalyRule(unittest.TestCase):
    def test_two_consecutive_out_of_band_is_anomaly(self):
        a, b = 10.0, -0.1
        yhat = {x: a + b * x for x in (20, 21, 22)}
        series = _synthetic_envelope_series(extra_by_unit={
            UNITS[20]: yhat[20] - 10.0,
            UNITS[21]: yhat[21] - 10.0,
        })
        fit, rows = build_metric_table(series, "low")
        self.assertTrue(anomaly_in_window(rows, EXTENSION_UNITS))

    def test_single_out_of_band_unit_is_not_anomaly(self):
        a, b = 10.0, -0.1
        yhat20 = a + b * 20
        series = _synthetic_envelope_series(extra_by_unit={UNITS[20]: yhat20 - 10.0})
        fit, rows = build_metric_table(series, "low")
        self.assertFalse(anomaly_in_window(rows, EXTENSION_UNITS))


if __name__ == "__main__":
    unittest.main()
