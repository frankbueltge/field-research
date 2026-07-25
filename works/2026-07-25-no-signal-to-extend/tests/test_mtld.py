import unittest

import _pathfix  # noqa: F401
from metrics import _mtld_factor_pass, mtld_bidirectional, MTLD_THRESHOLD


class TestMtldFactorPass(unittest.TestCase):
    def test_partial_factor_only_hand_computable(self):
        # tokens: a,b,c,d,a -- TTR never drops to <=0.72 until the very last token
        # (4 types / 5 tokens = 0.8 > 0.72), so no full factor completes; the whole
        # factor count comes from the trailing partial term.
        # partial = (1 - 0.8) / (1 - 0.72) = 0.2 / 0.28 = 5/7
        # MTLD_forward = 5 / (5/7) = 7.0 exactly.
        tokens = ["a", "b", "c", "d", "a"]
        result = _mtld_factor_pass(tokens, MTLD_THRESHOLD)
        self.assertAlmostEqual(result, 7.0, places=9)

    def test_bidirectional_symmetric_case(self):
        # Same 5-token sequence is a palindrome of repeats (only 'a' repeats, at
        # position 1 and 5), so forward and backward passes are identical by
        # symmetry, and MTLD == 7.0 exactly in both directions.
        tokens = ["a", "b", "c", "d", "a"]
        result = mtld_bidirectional(tokens)
        self.assertAlmostEqual(result, 7.0, places=9)

    def test_all_unique_tokens_is_undefined(self):
        # TTR == 1.0 throughout (every token is new) -> partial factor term is
        # (1 - 1.0) / (1 - 0.72) == 0, so factor_count == 0 -> undefined (None),
        # per PREREGISTRATION.md §3 ("factor_count is 0 ... MTLD undefined").
        tokens = [f"tok{i}" for i in range(10)]
        self.assertIsNone(_mtld_factor_pass(tokens, MTLD_THRESHOLD))
        self.assertIsNone(mtld_bidirectional(tokens))

    def test_empty_tokens_is_undefined(self):
        self.assertIsNone(_mtld_factor_pass([], MTLD_THRESHOLD))
        self.assertIsNone(mtld_bidirectional([]))

    def test_fully_repetitive_text_has_low_mtld(self):
        # Strongly repetitive text should complete many full factors quickly and
        # therefore yield a low MTLD relative to the partial-only case above.
        tokens = ["a", "b"] * 100
        result = mtld_bidirectional(tokens)
        self.assertIsNotNone(result)
        self.assertLess(result, 5.0)

    def test_one_full_factor_then_unique_tail(self):
        # a,b,a -> factor completes at index 3 (TTR = 2/3 = 0.667 <= 0.72).
        # Trailing c,d,e,f are all unique (TTR stays 1.0), contributing a 0 partial.
        # factor_count = 1 + 0 = 1; MTLD_forward = 7 / 1 = 7.0.
        tokens = ["a", "b", "a", "c", "d", "e", "f"]
        result = _mtld_factor_pass(tokens, MTLD_THRESHOLD)
        self.assertAlmostEqual(result, 7.0, places=9)

    def test_bidirectional_is_mean_of_forward_and_backward(self):
        tokens = ["a", "b", "a", "c", "d", "e", "f", "g", "a", "b"]
        forward = _mtld_factor_pass(tokens, MTLD_THRESHOLD)
        backward = _mtld_factor_pass(list(reversed(tokens)), MTLD_THRESHOLD)
        expected = (forward + backward) / 2.0
        self.assertAlmostEqual(mtld_bidirectional(tokens), expected, places=9)


if __name__ == "__main__":
    unittest.main()
