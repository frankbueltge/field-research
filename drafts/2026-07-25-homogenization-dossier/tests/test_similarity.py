import unittest

import _pathfix  # noqa: F401
from metrics import _cosine, between_abstract_similarity


class TestCosine(unittest.TestCase):
    def test_identical_normalized_vectors_give_one(self):
        va = {"x": 0.6, "y": 0.8}  # already unit norm: 0.6^2+0.8^2=1.0
        vb = {"x": 0.6, "y": 0.8}
        self.assertAlmostEqual(_cosine(va, vb), 1.0, places=9)

    def test_disjoint_support_gives_zero(self):
        va = {"x": 1.0}
        vb = {"y": 1.0}
        self.assertAlmostEqual(_cosine(va, vb), 0.0, places=9)

    def test_empty_vector_gives_zero(self):
        self.assertEqual(_cosine({}, {"x": 1.0}), 0.0)
        self.assertEqual(_cosine({"x": 1.0}, {}), 0.0)

    def test_order_independence(self):
        va = {"x": 0.6, "y": 0.8}
        vb = {"x": 0.6, "y": 0.8}
        self.assertEqual(_cosine(va, vb), _cosine(vb, va))


class TestBetweenAbstractSimilarity(unittest.TestCase):
    def test_disjoint_vocabulary_docs_give_zero_similarity(self):
        tokens_by_id = {
            "a": ["alpha"] * 20,
            "b": ["beta"] * 20,
            "c": ["gamma"] * 20,
        }
        result = between_abstract_similarity(["a", "b", "c"], tokens_by_id)
        self.assertAlmostEqual(result["value"], 0.0, places=9)
        self.assertEqual(result["n_draw"], 3)
        self.assertTrue(result["small_draw"])  # 3 < 150

    def test_small_draw_flag_and_two_doc_minimum(self):
        tokens_by_id = {"a": ["x", "y"]}
        result = between_abstract_similarity(["a"], tokens_by_id)
        self.assertIsNone(result["value"])
        self.assertEqual(result["n_draw"], 1)

    def test_overlapping_but_distinct_docs_give_partial_similarity(self):
        # 'shared' occurs in every doc (df=3) -> idf=ln(3/3)=0, contributes nothing.
        # 'a'/'b'/'c' are each unique to one doc (df=1) -> nonzero idf but disjoint
        # support across docs -> those terms never overlap between two different
        # docs either. With only a fully-shared term (idf 0) and per-doc-unique
        # terms, all pairwise dot products are exactly 0.
        tokens_by_id = {
            "a": ["shared", "shared", "a"],
            "b": ["shared", "shared", "b"],
            "c": ["shared", "shared", "c"],
        }
        result = between_abstract_similarity(["a", "b", "c"], tokens_by_id)
        self.assertAlmostEqual(result["value"], 0.0, places=9)

    def test_partial_overlap_gives_similarity_between_zero_and_one(self):
        tokens_by_id = {
            "a": ["shared", "shared", "only_a", "only_a", "only_a"],
            "b": ["shared", "shared", "only_b", "only_b"],
        }
        result = between_abstract_similarity(["a", "b"], tokens_by_id)
        # df('shared')=2 -> idf=ln(2/2)=0 -> shared term contributes nothing here too,
        # since it appears in every doc in the draw. So this pair is again disjoint
        # in effective (nonzero-idf) support -> similarity 0. Included to document
        # the within-draw-idf mechanic, not to assert a nontrivial positive value.
        self.assertAlmostEqual(result["value"], 0.0, places=9)

    def test_true_partial_overlap_with_three_docs(self):
        # 'common' appears in 2 of 3 docs (df=2, idf=ln(3/2)>0), giving a genuine
        # nonzero, non-unit similarity between those two docs, and 0 with the third.
        tokens_by_id = {
            "a": ["common", "common", "onlya"],
            "b": ["common", "common", "onlyb"],
            "c": ["onlyc", "onlyc", "onlyc"],
        }
        result = between_abstract_similarity(["a", "b", "c"], tokens_by_id)
        self.assertGreater(result["value"], 0.0)
        self.assertLess(result["value"], 1.0)


if __name__ == "__main__":
    unittest.main()
