"""
test_digit_tests.py -- unit tests for digit_tests.py

Run with: python3 test_digit_tests.py

Validates the self-written chi-squared p-value implementation (built on a
hand-rolled regularized incomplete gamma function) against textbook
chi-squared critical values, and runs a few sanity checks on the digit
tests themselves.
"""

import math
import random
import unittest

import digit_tests as dt


class TestChi2CriticalValues(unittest.TestCase):
    """
    Known critical values (upper-tail p = 0.05 / 0.01) for the chi-squared
    distribution, from standard chi-squared tables:
      df=8,  x=15.507 -> p ~ 0.05
      df=9,  x=16.919 -> p ~ 0.05
      df=9,  x=21.666 -> p ~ 0.01
    """

    TOL = 1e-3

    def test_df8_p05(self):
        p = dt.chi2_sf(15.507, 8)
        self.assertAlmostEqual(p, 0.05, delta=self.TOL)

    def test_df9_p05(self):
        p = dt.chi2_sf(16.919, 9)
        self.assertAlmostEqual(p, 0.05, delta=self.TOL)

    def test_df9_p01(self):
        p = dt.chi2_sf(21.666, 9)
        self.assertAlmostEqual(p, 0.01, delta=self.TOL)

    def test_zero_stat_gives_p_one(self):
        self.assertAlmostEqual(dt.chi2_sf(0.0, 5), 1.0, delta=1e-9)

    def test_large_stat_gives_small_p(self):
        self.assertLess(dt.chi2_sf(1000.0, 8), 1e-10)

    def test_monotonic_decreasing(self):
        # p-value must strictly decrease as the statistic grows, for fixed df
        xs = [1, 5, 10, 15, 20, 30, 50]
        ps = [dt.chi2_sf(x, 9) for x in xs]
        for i in range(len(ps) - 1):
            self.assertGreater(ps[i], ps[i + 1])


class TestGammaSanity(unittest.TestCase):
    def test_gammp_plus_gammq_is_one(self):
        for a, x in [(0.5, 1.0), (2.0, 3.0), (5.0, 4.5), (9.0, 20.0), (4.5, 4.5)]:
            self.assertAlmostEqual(dt.gammp(a, x) + dt.gammq(a, x), 1.0, delta=1e-9)

    def test_gammp_bounds(self):
        for a, x in [(0.5, 1.0), (2.0, 3.0), (9.0, 20.0)]:
            p = dt.gammp(a, x)
            self.assertGreaterEqual(p, 0.0)
            self.assertLessEqual(p, 1.0)


class TestBenfordPerfectCounts(unittest.TestCase):
    def test_perfect_benford_first_digit_p_near_one(self):
        # Build counts that exactly match the Benford first-digit expectation.
        n = 100000
        expected = dt.benford_first_digit_expected()
        counts = [round(p * n) for p in expected]
        # fix rounding drift on the last bucket so counts sum exactly to n
        counts[-1] += n - sum(counts)
        stat, df, p = dt.chi_square_gof(counts, expected, n)
        self.assertGreater(p, 0.9)
        mad = dt.mean_absolute_deviation(counts, expected, n)
        self.assertLess(mad, 0.001)

    def test_perfect_benford_via_generated_values(self):
        # Values whose leading digits follow Benford by construction:
        # v = 10**t for t uniform over a wide multiplicative span.
        rng = random.Random(1234)
        values = [10 ** rng.uniform(0, 6) for _ in range(20000)]
        n, chi2_result, mad_result = dt.run_first_digit_test(values)
        # Randomly generated, so use a loose bound rather than a strict 0.05 cutoff.
        self.assertGreater(chi2_result["p"], 0.001)
        self.assertFalse(mad_result["flagged"])


class TestUniformLastDigit(unittest.TestCase):
    def test_uniform_last_digits_pass(self):
        rng = random.Random(7)
        values = [rng.randint(1000, 9999999) for _ in range(5000)]
        result = dt.run_last_digit_test(values)
        self.assertGreater(result["p"], 0.01)
        self.assertFalse(result["flagged"])

    def test_last_digit_excludes_small_values(self):
        values = [1, 2, 3, 999, 1000, 1001]
        result = dt.run_last_digit_test(values)
        self.assertEqual(result["n"], 2)  # only 1000 and 1001 qualify
        self.assertEqual(result["n_excluded_below_1000"], 4)


class TestDigitsAllNineFail(unittest.TestCase):
    def test_all_nines_first_digit_flagged(self):
        values = [9 * (10 ** k) for k in range(0, 6)] * 40  # all leading digit 9, n=240
        n, chi2_result, mad_result = dt.run_first_digit_test(values)
        self.assertTrue(chi2_result["flagged"])
        self.assertLess(chi2_result["p"], 0.05)
        self.assertTrue(mad_result["flagged"])
        self.assertGreater(mad_result["stat"], dt.MAD_FIRST_DIGIT_CUTOFF)

    def test_all_last_digit_nine_flagged(self):
        values = [1230 + 10 * k + 9 for k in range(300)]  # all end in 9, all >= 1000
        result = dt.run_last_digit_test(values)
        self.assertTrue(result["flagged"])
        self.assertLess(result["p"], 0.05)


class TestNGate(unittest.TestCase):
    def test_in_spec(self):
        self.assertEqual(dt.n_gate_status(217), "IN-SPEC")
        self.assertEqual(dt.n_gate_status(100), "IN-SPEC")
        self.assertEqual(dt.n_gate_status(10000), "IN-SPEC")

    def test_out_of_spec(self):
        self.assertEqual(dt.n_gate_status(99), "OUT-OF-SPEC")
        self.assertEqual(dt.n_gate_status(10001), "OUT-OF-SPEC")
        self.assertEqual(dt.n_gate_status(5), "OUT-OF-SPEC")


class TestDigitExtraction(unittest.TestCase):
    def test_leading_digit(self):
        self.assertEqual(dt.leading_digit(12345), 1)
        self.assertEqual(dt.leading_digit(987), 9)
        self.assertEqual(dt.leading_digit(0.00456), 4)
        self.assertIsNone(dt.leading_digit(0))

    def test_second_digit(self):
        self.assertEqual(dt.second_digit(12345), 2)
        self.assertEqual(dt.second_digit(987), 8)

    def test_last_digit(self):
        self.assertEqual(dt.last_digit(12345), 5)
        self.assertEqual(dt.last_digit(12340.9), 0)
        self.assertEqual(dt.last_digit(-12347), 7)


if __name__ == "__main__":
    unittest.main(verbosity=2)
