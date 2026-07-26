import unittest

import _pathfix  # noqa: F401
import envelope_units as eu


def _rows(oob_indices, lo, hi):
    """Synthetic rows covering [lo, hi], out-of-band exactly at oob_indices."""
    return [{"index": i, "value": 1.0, "out_of_band": (i in oob_indices)} for i in range(lo, hi + 1)]


class TestTwoConsecutiveRule(unittest.TestCase):
    def test_adjacent_pair_fires(self):
        rows = _rows({61, 62}, 61, 73)
        self.assertTrue(eu.anomaly_two_consecutive(rows, 61, 73))

    def test_non_adjacent_pair_does_not_fire(self):
        rows = _rows({61, 63}, 61, 73)
        self.assertFalse(eu.anomaly_two_consecutive(rows, 61, 73))

    def test_single_out_of_band_unit_does_not_fire(self):
        rows = _rows({65}, 61, 73)
        self.assertFalse(eu.anomaly_two_consecutive(rows, 61, 73))

    def test_no_out_of_band_units_does_not_fire(self):
        rows = _rows(set(), 61, 73)
        self.assertFalse(eu.anomaly_two_consecutive(rows, 61, 73))

    def test_adjacency_not_invented_across_a_gap(self):
        # 61 and 63 both out-of-band, with 62 in-band between them: true adjacency
        # is required, a gap must not be skipped over.
        rows = _rows({61, 63}, 61, 73)
        rows[1]["out_of_band"] = False  # index 62, explicit
        self.assertFalse(eu.anomaly_two_consecutive(rows, 61, 73))


class TestFiveApartRule(unittest.TestCase):
    """PREREGISTRATION.md §4 Skeptic condition 1: metric 4 (similarity) requires two
    out-of-band units >= 5 apart in index, anywhere in the window -- deliberately
    HARDER than the two-consecutive rule, not merely different."""

    def test_adjacent_pair_does_not_satisfy_five_apart(self):
        rows = _rows({61, 62}, 61, 73)
        self.assertFalse(eu.anomaly_five_apart(rows, 61, 73))

    def test_exactly_five_apart_fires(self):
        rows = _rows({61, 66}, 61, 73)
        self.assertTrue(eu.anomaly_five_apart(rows, 61, 73))

    def test_four_apart_does_not_fire(self):
        rows = _rows({61, 65}, 61, 73)
        self.assertFalse(eu.anomaly_five_apart(rows, 61, 73))

    def test_more_than_five_apart_fires(self):
        rows = _rows({61, 73}, 61, 73)
        self.assertTrue(eu.anomaly_five_apart(rows, 61, 73))

    def test_non_adjacent_but_less_than_five_apart_does_not_fire(self):
        rows = _rows({61, 63}, 61, 73)
        self.assertFalse(eu.anomaly_five_apart(rows, 61, 73))

    def test_single_out_of_band_unit_does_not_fire(self):
        rows = _rows({65}, 61, 73)
        self.assertFalse(eu.anomaly_five_apart(rows, 61, 73))


class TestTwoConsecutiveBlocksRule(unittest.TestCase):
    """sim_block companion series: the naive per-unit rule would trivially fire on
    ANY single out-of-band block (its <=5 constituent units are "two consecutive
    out-of-band units"). The block-granularity rule requires two ADJACENT blocks."""

    def test_single_out_of_band_block_does_not_fire(self):
        # block 12 = units 61-65, entirely out-of-band; block 13 = 66-70, in-band.
        rows = _rows(set(range(61, 66)), 61, 73)
        self.assertFalse(eu.anomaly_two_consecutive_blocks(rows, 61, 73))

    def test_two_adjacent_out_of_band_blocks_fire(self):
        # blocks 12 (61-65) and 13 (66-70) both entirely out-of-band.
        rows = _rows(set(range(61, 71)), 61, 73)
        self.assertTrue(eu.anomaly_two_consecutive_blocks(rows, 61, 73))

    def test_two_non_adjacent_out_of_band_blocks_do_not_fire(self):
        # block 12 (61-65) and block 14 (71-73) out-of-band, block 13 (66-70) is not.
        rows = _rows(set(range(61, 66)) | set(range(71, 74)), 61, 73)
        self.assertFalse(eu.anomaly_two_consecutive_blocks(rows, 61, 73))


if __name__ == "__main__":
    unittest.main()
