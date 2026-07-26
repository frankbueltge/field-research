import unittest

import _pathfix  # noqa: F401
from pools import EnvelopePool, ranked_types, load_pool, ENVELOPE_WINDOW, PREFIX_LEN


class TestEnvelopePoolConstruction(unittest.TestCase):
    def test_top_types_and_rank_slice_agree_and_are_deterministic(self):
        pool = EnvelopePool(["b", "a", "a", "c", "c", "c"])
        # c:3, a:2, b:1 -- no ties here, unambiguous order.
        self.assertEqual(pool.top_types(2), [("c", 3), ("a", 2)])
        self.assertEqual(pool.rank_slice(1, 2), pool.top_types(2))
        self.assertEqual(pool.rank_slice(2, 3), [("a", 2), ("b", 1)])

    def test_alphabetical_tie_break_matches_parent_convention(self):
        freq = {"zeta": 2, "alpha": 2, "mu": 1}
        ranked = ranked_types(freq)
        # both zeta and alpha have count 2 -- alpha sorts first ascending.
        self.assertEqual(ranked, [("alpha", 2), ("zeta", 2), ("mu", 1)])


class TestRealEnvelopePool(unittest.TestCase):
    def test_pool_size_matches_computable_envelope_units(self):
        pool = load_pool()
        # Envelope window is units 1-47; units 29, 33, 40 are below 600 tokens
        # (provenance/feasibility-pretest.md), so 44 computable units * 600 tokens.
        self.assertEqual(len(pool.tokens), 44 * PREFIX_LEN)
        self.assertEqual(ENVELOPE_WINDOW, (1, 47))


if __name__ == "__main__":
    unittest.main()
