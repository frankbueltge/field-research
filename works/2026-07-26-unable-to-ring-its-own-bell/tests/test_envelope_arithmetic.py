import unittest

import _pathfix  # noqa: F401
import envelope_units as eu


class TestPerfectlyLinearSeriesGivesZeroZ(unittest.TestCase):
    """PREREGISTRATION.md §4: a hand-computable fixture where the whole series lies
    exactly on a line must give z = 0 at every envelope point (residual = 0 at the
    fitted points; se and the residual both vanish together, not a division blow-up:
    see the degenerate-fit guard in envelope_units.build_rows)."""

    def test_z_zero_at_every_point_low_direction(self):
        series = [(x, 3.0 + 2.0 * x) for x in range(1, 74)]
        fit_points = [(x, v) for x, v in series if 1 <= x <= 47]
        fit = eu.fit_linear([p[0] for p in fit_points], [p[1] for p in fit_points])
        self.assertAlmostEqual(fit["s"], 0.0, places=12)
        rows = eu.build_rows(series, fit, "low")
        for r in rows:
            self.assertAlmostEqual(r["z"], 0.0, places=12)
            self.assertFalse(r["out_of_band"])

    def test_z_zero_at_every_point_high_direction(self):
        series = [(x, 10.0 - 0.5 * x) for x in range(1, 74)]
        fit_points = [(x, v) for x, v in series if 1 <= x <= 47]
        fit = eu.fit_linear([p[0] for p in fit_points], [p[1] for p in fit_points])
        rows = eu.build_rows(series, fit, "high")
        for r in rows:
            self.assertAlmostEqual(r["z"], 0.0, places=12)
            self.assertFalse(r["out_of_band"])


class TestKnownDeviationGivesKnownZ(unittest.TestCase):
    """A single, deliberately displaced extension-window point must reproduce the
    §4 formula z = (y - yhat) / SE_pred exactly (hand-computed SE, not re-derived
    from the module under test)."""

    def test_hand_computed_z_at_one_displaced_point(self):
        import math
        xs = list(range(1, 48))
        ys = [3.0 + 2.0 * x for x in xs]
        # displace unit 30 slightly so the fit is not perfectly degenerate.
        ys[29 - 1] += 1.0
        fit = eu.fit_linear(xs, ys)

        x_star = 65
        yhat = fit["a"] + fit["b"] * x_star
        se_expected = fit["s"] * math.sqrt(1 + 1.0 / fit["n"] + (x_star - fit["xbar"]) ** 2 / fit["sxx"])
        se_got = eu.pred_se(fit, x_star)
        self.assertAlmostEqual(se_got, se_expected, places=12)

        y_star = yhat - 5 * se_expected  # deliberately 5 SE below trend
        series = [(x, ys[x - 1]) for x in xs] + [(x_star, y_star)]
        rows = eu.build_rows(series, fit, "low")
        row = next(r for r in rows if r["index"] == x_star)
        self.assertAlmostEqual(row["z"], -5.0, places=6)
        self.assertTrue(row["out_of_band"])  # -5 < -t_crit


if __name__ == "__main__":
    unittest.main()
