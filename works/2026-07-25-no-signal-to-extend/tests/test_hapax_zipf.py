import math
import unittest
from collections import Counter

import _pathfix  # noqa: F401
from metrics import hapax_share, zipf_tail_slope, _ranked_types, ZIPF_MIN_TYPES


class TestHapaxShare(unittest.TestCase):
    def test_constructed_pool(self):
        # freq: a:2, b:1, c:3, d:1 -> total_types=4, hapax_types=2 (b, d)
        pool = ["a", "a", "b", "c", "c", "c", "d"]
        self.assertAlmostEqual(hapax_share(pool), 2 / 4)

    def test_all_hapax(self):
        pool = ["a", "b", "c", "d"]
        self.assertAlmostEqual(hapax_share(pool), 1.0)

    def test_no_hapax(self):
        pool = ["a", "a", "b", "b"]
        self.assertAlmostEqual(hapax_share(pool), 0.0)

    def test_empty_pool(self):
        self.assertIsNone(hapax_share([]))


class TestRankedTypesTieBreak(unittest.TestCase):
    def test_alphabetical_tiebreak(self):
        freq = Counter({"banana": 3, "apple": 3, "cherry": 1})
        ranked = _ranked_types(freq)
        self.assertEqual(ranked, [("apple", 3), ("banana", 3), ("cherry", 1)])


class TestZipfTailSlope(unittest.TestCase):
    def test_below_min_types_is_non_computable(self):
        pool = []
        for i in range(ZIPF_MIN_TYPES - 1):
            pool.append(f"type{i}")
        result = zipf_tail_slope(pool)
        self.assertTrue(result["non_computable"])
        self.assertIsNone(result["slope"])

    def test_exact_power_law_recovers_slope(self):
        # Construct an exact-ish power law: freq(rank r) = round(C / r) for
        # r = 1..1000, using distinct 4-digit zero-padded ranks as token strings so
        # that alphabetical tie-breaking never conflicts with the intended frequency
        # order (no ties occur here: freq is strictly non-increasing and, for this
        # C, strictly decreasing across r=1..1000).
        pool = []
        C = 2000
        for r in range(1, 1001):
            freq = max(1, round(C / r))
            token = f"tok{r:04d}"
            pool.extend([token] * freq)
        result = zipf_tail_slope(pool)
        self.assertFalse(result["non_computable"])
        self.assertEqual(result["types"], 1000)
        self.assertFalse(result["partial_range"])
        # True slope is -1.0 (freq ~ C / rank); rounding to integer counts introduces
        # small deviation, tolerate it.
        self.assertAlmostEqual(result["slope"], -1.0, delta=0.1)

    def test_partial_range_flag_when_fewer_than_max_rank_types(self):
        # 350 distinct types (>= 300, < 1000): must compute over 101..350 and flag.
        pool = []
        for i in range(350):
            count = 350 - i  # strictly decreasing frequency, no ties
            pool.extend([f"w{i:04d}"] * count)
        result = zipf_tail_slope(pool)
        self.assertFalse(result["non_computable"])
        self.assertTrue(result["partial_range"])
        self.assertEqual(result["types"], 350)
        self.assertIsNotNone(result["slope"])

    def test_empty_pool_non_computable(self):
        result = zipf_tail_slope([])
        self.assertTrue(result["non_computable"])
        self.assertIsNone(result["slope"])


if __name__ == "__main__":
    unittest.main()
