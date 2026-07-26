import math
import unittest

import _pathfix  # noqa: F401
from metrics_units import window_similarity, content_filtered, top_contributors


class TestFiveIdenticalDocuments(unittest.TestCase):
    def test_idf_zeroing_gives_zero(self):
        # Every token present in all 5 documents gets idf = ln(5/5) = 0, so every
        # weight is zero, every vector is empty, and cosine on empty vectors is 0 —
        # the disclosed idf-zeroing property (PREREGISTRATION.md §3(a)), not an
        # accident of a degenerate all-ones fixture.
        doc = ["alpha", "beta", "gamma", "alpha", "beta"]
        docs = {i: list(doc) for i in range(1, 6)}
        value, contributions, total = window_similarity([1, 2, 3, 4, 5], docs)
        self.assertAlmostEqual(value, 0.0, places=12)
        self.assertEqual(total, 0.0)
        self.assertEqual(len(contributions), 0)


class TestTokenInTwoOfFiveDocuments(unittest.TestCase):
    def test_hand_computable_partial_overlap(self):
        docs = {
            1: ["shared", "uniq1"],
            2: ["shared", "uniq2"],
            3: ["uniq3"],
            4: ["uniq4"],
            5: ["uniq5"],
        }
        value, contributions, total = window_similarity([1, 2, 3, 4, 5], docs)

        idf_shared = math.log(5 / 2)  # df('shared') = 2
        idf_uniq = math.log(5 / 1)    # df(each uniqN) = 1
        norm1 = math.sqrt(idf_shared ** 2 + idf_uniq ** 2)
        w_shared = idf_shared / norm1
        expected_pair_12 = w_shared * w_shared  # only 'shared' overlaps between docs 1,2
        expected_total = expected_pair_12       # all other 9 pairs are disjoint -> 0
        expected_mean = expected_total / 10     # 10 pairs total

        self.assertAlmostEqual(value, expected_mean, places=12)
        self.assertAlmostEqual(total, expected_total, places=12)
        self.assertAlmostEqual(contributions["shared"], expected_total, places=12)
        self.assertEqual(set(contributions.keys()), {"shared"})

    def test_top_contributors_reports_the_single_contributing_token(self):
        docs = {
            1: ["shared", "uniq1"],
            2: ["shared", "uniq2"],
            3: ["uniq3"],
            4: ["uniq4"],
            5: ["uniq5"],
        }
        _value, contributions, total = window_similarity([1, 2, 3, 4, 5], docs)
        top5 = top_contributors(contributions, total, k=5)
        self.assertEqual(len(top5), 1)
        tok, contrib, share = top5[0]
        self.assertEqual(tok, "shared")
        self.assertAlmostEqual(contrib, total, places=12)
        self.assertAlmostEqual(share, 1.0, places=12)


class TestContentFiltering(unittest.TestCase):
    def test_content_filtered_removes_stopset_tokens(self):
        tokens = ["a", "b", "c", "a", "d"]
        self.assertEqual(content_filtered(tokens, {"a"}), ["b", "c", "d"])
        self.assertEqual(content_filtered(tokens, set()), tokens)
        self.assertEqual(content_filtered(tokens, {"a", "b", "c", "d"}), [])

    def test_removing_a_contributing_token_zeroes_the_similarity_it_carried(self):
        # Reuses the "token in 2 of 5" fixture: 'shared' is the ONLY contributor to
        # the window's similarity. If it is in the removed set (as it would be if it
        # were one of the envelope pool's 200 most frequent types), sim_content must
        # drop to exactly 0 even though sim_trailing on the same documents is not 0.
        docs = {
            1: ["shared", "uniq1"],
            2: ["shared", "uniq2"],
            3: ["uniq3"],
            4: ["uniq4"],
            5: ["uniq5"],
        }
        raw_value, _c, _t = window_similarity([1, 2, 3, 4, 5], docs)
        self.assertGreater(raw_value, 0.0)

        stopset = {"shared"}
        filtered_docs = {idx: content_filtered(toks, stopset) for idx, toks in docs.items()}
        filtered_value, filtered_contrib, filtered_total = window_similarity(
            [1, 2, 3, 4, 5], filtered_docs
        )
        self.assertAlmostEqual(filtered_value, 0.0, places=12)
        self.assertEqual(len(filtered_contrib), 0)


class TestGeneralizedWindowSizeForBlocks(unittest.TestCase):
    def test_three_document_block_uses_ln_three_over_df(self):
        # sim_block's final block can be shorter than 5 (this corpus's last block is
        # units 71-73, size 3); window_similarity must use the ACTUAL window size in
        # its idf denominator, not a hardcoded 5.
        docs = {1: ["shared", "u1"], 2: ["shared", "u2"], 3: ["u3"]}
        value, contributions, total = window_similarity([1, 2, 3], docs)
        idf_shared = math.log(3 / 2)
        idf_uniq = math.log(3 / 1)
        norm = math.sqrt(idf_shared ** 2 + idf_uniq ** 2)
        w_shared = idf_shared / norm
        expected_total = w_shared * w_shared
        expected_mean = expected_total / 3  # C(3,2) = 3 pairs
        self.assertAlmostEqual(value, expected_mean, places=12)
        self.assertAlmostEqual(total, expected_total, places=12)


if __name__ == "__main__":
    unittest.main()
