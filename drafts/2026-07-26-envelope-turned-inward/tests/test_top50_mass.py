import unittest

import _pathfix  # noqa: F401
from metrics_units import top50_frequency_mass
from pools import ranked_types


class TestTop50FrequencyMassHandComputed(unittest.TestCase):
    def test_known_answer(self):
        # 50 "high" types at count 2 each (top 50 = 100 tokens), 10 "low" types at
        # count 1 each (10 tokens, excluded from the top 50). total = 110 tokens.
        tokens = []
        for i in range(50):
            tokens.extend([f"high{i:02d}"] * 2)
        for i in range(10):
            tokens.append(f"low{i:02d}")
        result = top50_frequency_mass(tokens)
        self.assertAlmostEqual(result["mass"], 100 / 110, places=12)
        self.assertFalse(result["partial"])

    def test_fewer_than_50_types_uses_all_and_flags_partial(self):
        tokens = ["a", "a", "b", "b", "b", "c"]  # 3 types only
        result = top50_frequency_mass(tokens)
        self.assertAlmostEqual(result["mass"], 1.0, places=12)  # all types included
        self.assertTrue(result["partial"])

    def test_empty_tokens(self):
        result = top50_frequency_mass([])
        self.assertIsNone(result["mass"])
        self.assertIsNone(result["partial"])


class TestAlphabeticalTieBreak(unittest.TestCase):
    def test_ties_at_the_boundary_broken_alphabetically_ascending(self):
        # 45 "high" types at count 2 (clearly in the top 50), plus 10 "tied" types
        # all at count 1 -- only 5 of those 10 fit in the top-50 cut, and the tie
        # must be broken by ascending alphabetical token order, i.e. the 5
        # lexicographically smallest of the 10 tied tokens.
        tokens = []
        for i in range(45):
            tokens.extend([f"high{i:02d}"] * 2)
        tied_tokens = [f"t{i:02d}" for i in range(10)]  # t00..t09
        tokens.extend(tied_tokens)  # each appears exactly once

        freq = {}
        for tok in tokens:
            freq[tok] = freq.get(tok, 0) + 1
        ranked = ranked_types(freq)

        top50 = ranked[:50]
        top50_tokens = {tok for tok, _c in top50}
        expected_tied_included = {f"t{i:02d}" for i in range(5)}   # t00..t04
        expected_tied_excluded = {f"t{i:02d}" for i in range(5, 10)}  # t05..t09

        self.assertTrue(expected_tied_included.issubset(top50_tokens))
        self.assertFalse(expected_tied_excluded & top50_tokens)

        # And the mass computed via top50_frequency_mass must match this selection.
        from metrics_units import top50_frequency_mass
        result = top50_frequency_mass(tokens)
        expected_mass_tokens = 45 * 2 + 5 * 1
        expected_total = 45 * 2 + 10 * 1
        self.assertAlmostEqual(result["mass"], expected_mass_tokens / expected_total, places=12)


if __name__ == "__main__":
    unittest.main()
