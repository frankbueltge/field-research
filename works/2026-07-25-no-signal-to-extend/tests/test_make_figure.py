import unittest

import _pathfix  # noqa: F401
from make_figure import (
    linear_scale,
    value_domain,
    band_bounds,
    band_side,
    nice_step,
    nice_ticks,
    select_x_ticks,
    points_attr,
    band_polygon_points,
    declutter_positions,
)


class TestLinearScale(unittest.TestCase):
    def test_maps_domain_to_range_including_degenerate_and_inverted_cases(self):
        cases = [
            # (value, d0, d1, r0, r1, expected)
            (0, 0, 10, 100, 200, 100.0),   # domain start -> range start
            (10, 0, 10, 100, 200, 200.0),  # domain end -> range end
            (5, 0, 10, 100, 200, 150.0),   # midpoint
            (0, 0, 10, 300, 0, 300.0),     # inverted range (svg y-axis usage)
            (10, 0, 10, 300, 0, 0.0),
            (5, 3, 3, 0, 100, 50.0),       # degenerate domain -> range midpoint
        ]
        for value, d0, d1, r0, r1, expected in cases:
            with self.subTest(value=value, d0=d0, d1=d1, r0=r0, r1=r1):
                self.assertAlmostEqual(linear_scale(value, d0, d1, r0, r1), expected)


class TestValueDomain(unittest.TestCase):
    def test_padding_and_degenerate_spans(self):
        lo, hi = value_domain([10.0, 20.0], pad_frac=0.10)
        self.assertAlmostEqual(lo, 9.0)
        self.assertAlmostEqual(hi, 21.0)

        lo_flat, hi_flat = value_domain([5.0, 5.0], pad_frac=0.10)
        self.assertLess(lo_flat, 5.0)
        self.assertGreater(hi_flat, 5.0)

        lo_zero, hi_zero = value_domain([0.0, 0.0], pad_frac=0.10)
        self.assertAlmostEqual(lo_zero, -1.0)
        self.assertAlmostEqual(hi_zero, 1.0)


class TestBandBoundsAndSide(unittest.TestCase):
    def test_direction_sets_the_collapse_edge(self):
        low = band_bounds(yhat=10.0, se=2.0, t_crit=2.0, direction="low")
        self.assertAlmostEqual(low["lower"], 6.0)
        self.assertAlmostEqual(low["upper"], 14.0)
        self.assertEqual(low["collapse"], "lower")
        self.assertEqual(low["anti"], "upper")

        high = band_bounds(yhat=10.0, se=2.0, t_crit=2.0, direction="high")
        self.assertEqual(high["collapse"], "upper")
        self.assertEqual(high["anti"], "lower")

        with self.assertRaises(ValueError):
            band_bounds(yhat=1.0, se=1.0, t_crit=1.0, direction="sideways")

    def test_band_side_vocabulary_matches_band_bounds_collapse_label(self):
        # band_side must return values directly comparable to band_bounds()'s
        # 'collapse'/'anti' labels with no name-translation in between -- the
        # figure script decides "is this point on the collapse side?" via
        # `band_side(...) == band_bounds(...)["collapse"]", and an earlier
        # draft used mismatched vocabulary ('below'/'above' vs 'lower'/
        # 'upper') that silently made this comparison always false.
        self.assertEqual(band_side(5.0, 0.0, 10.0), "inside")
        b = band_bounds(yhat=10.0, se=2.0, t_crit=2.0, direction="low")
        self.assertEqual(band_side(5.0, b["lower"], b["upper"]), b["collapse"])
        self.assertEqual(band_side(15.0, b["lower"], b["upper"]), b["anti"])


class TestNiceStepAndTicks(unittest.TestCase):
    def test_nice_step_family_and_tick_generation(self):
        for raw, expected in [(0.4, 0.5), (1.5, 2.0), (3.0, 5.0), (7.0, 10.0), (0, 1.0)]:
            with self.subTest(raw=raw):
                self.assertAlmostEqual(nice_step(raw), expected)

        ticks = nice_ticks(0.0, 9.0, target_count=3)
        self.assertGreaterEqual(ticks[0], -1e-9)
        self.assertLessEqual(ticks[-1], 9.0 + 1e-9)
        self.assertEqual(ticks, sorted(ticks))
        self.assertEqual(nice_ticks(5.0, 5.0), [5.0])


class TestSelectXTicks(unittest.TestCase):
    def test_endpoints_stride_and_empty_input(self):
        units = [f"u{i}" for i in range(23)]
        idxs = [i for i, _label in select_x_ticks(units, stride=11)]
        self.assertIn(0, idxs)
        self.assertIn(22, idxs)

        self.assertEqual(select_x_ticks(["a", "b", "c"], stride=1),
                         [(0, "a"), (1, "b"), (2, "c")])
        self.assertEqual(select_x_ticks([], stride=4), [])


class TestSvgCoordinateFormatting(unittest.TestCase):
    def test_points_attr_and_band_polygon(self):
        self.assertEqual(points_attr([0, 1], [10, 20], decimals=1), "0.0,10.0 1.0,20.0")
        # polygon outline: forward along the upper edge, then backward along the lower edge
        pts = band_polygon_points([0, 1], [5, 6], [15, 16], decimals=0)
        self.assertEqual(pts, "0,15 1,16 1,6 0,5")


class TestDeclutterPositions(unittest.TestCase):
    def test_spacing_order_preservation_and_edge_cases(self):
        untouched = [0.0, 100.0, 200.0]
        self.assertEqual(declutter_positions(untouched, min_gap=10), untouched)

        ys = [50.0, 10.0, 30.0]  # given out of sorted order on purpose
        adjusted = declutter_positions(ys, min_gap=10)
        # index-for-index rank order must match the input's rank order
        self.assertEqual(
            sorted(range(len(ys)), key=lambda i: ys[i]),
            sorted(range(len(adjusted)), key=lambda i: adjusted[i]),
        )
        for a, b in zip(sorted(adjusted), sorted(adjusted)[1:]):
            self.assertGreaterEqual(b - a, 10 - 1e-9)

        self.assertEqual(declutter_positions([42.0], min_gap=10), [42.0])


if __name__ == "__main__":
    unittest.main()
