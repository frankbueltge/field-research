import unittest

import _pathfix  # noqa: F401
from tdist import t975, t_quantile, t_cdf


class TestPublishedTableAgreement(unittest.TestCase):
    """PREREGISTRATION.md §4: t(0.975, df) computed numerically must agree to 4
    decimal places with these published table values, blocking if not."""

    def test_df_10(self):
        self.assertAlmostEqual(t975(10), 2.2281, places=4)

    def test_df_13(self):
        self.assertAlmostEqual(t975(13), 2.1604, places=4)

    def test_df_14(self):
        self.assertAlmostEqual(t975(14), 2.1448, places=4)

    def test_df_30(self):
        self.assertAlmostEqual(t975(30), 2.0423, places=4)

    def test_df_60(self):
        self.assertAlmostEqual(t975(60), 2.0003, places=4)


class TestRoundTrip(unittest.TestCase):
    def test_cdf_at_quantile_recovers_target_probability(self):
        for df in (5, 10, 14, 22, 44, 50):
            t = t_quantile(0.975, df)
            self.assertAlmostEqual(t_cdf(t, df), 0.975, places=8)

    def test_monotonic_in_df_toward_normal_1_96(self):
        # As df grows, t(0.975, df) decreases monotonically toward ~1.96.
        vals = [t975(df) for df in (5, 10, 30, 100, 1000)]
        self.assertEqual(vals, sorted(vals, reverse=True))
        self.assertLess(abs(vals[-1] - 1.96), 0.01)


if __name__ == "__main__":
    unittest.main()
