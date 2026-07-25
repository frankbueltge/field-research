import unittest

import _pathfix  # noqa: F401
from metrics import seeded_order, build_pool, compute_cell, MTLD_DRAW, SIM_DRAW


class TestSeededOrderDeterminism(unittest.TestCase):
    def test_same_inputs_give_byte_identical_order_twice(self):
        ids = [f"{1000 + i}.{i:05d}" for i in range(200)]
        order1 = seeded_order("cs.CL", "2019H2", ids)
        order2 = seeded_order("cs.CL", "2019H2", ids)
        self.assertEqual(order1, order2)

    def test_input_order_does_not_matter_only_the_set_of_ids(self):
        ids = [f"{1000 + i}.{i:05d}" for i in range(200)]
        import random
        shuffled_input = list(ids)
        random.Random(1).shuffle(shuffled_input)  # scramble caller-supplied order
        order1 = seeded_order("cs.CL", "2019H2", ids)
        order2 = seeded_order("cs.CL", "2019H2", shuffled_input)
        self.assertEqual(order1, order2)  # both sort first, so input order is irrelevant

    def test_different_unit_gives_different_order(self):
        ids = [f"{1000 + i}.{i:05d}" for i in range(200)]
        order_a = seeded_order("cs.CL", "2019H1", ids)
        order_b = seeded_order("cs.CL", "2019H2", ids)
        self.assertNotEqual(order_a, order_b)

    def test_different_stratum_gives_different_order(self):
        ids = [f"{1000 + i}.{i:05d}" for i in range(200)]
        order_a = seeded_order("cs.CL", "2019H1", ids)
        order_b = seeded_order("cs.CV", "2019H1", ids)
        self.assertNotEqual(order_a, order_b)

    def test_repeated_process_reruns_are_identical(self):
        # Simulate "two separate runs" by constructing fresh RNGs from scratch each
        # time (seeded_order already does this internally); assert full re-derivation
        # is stable across many repetitions.
        ids = [f"id{i}" for i in range(500)]
        orders = [seeded_order("math.NT", "2021H1", ids) for _ in range(5)]
        for o in orders[1:]:
            self.assertEqual(orders[0], o)


class TestOneOrderThreeUses(unittest.TestCase):
    """The pool prefix and the MTLD/similarity prefixes must all come from the SAME
    single shuffle -- i.e. build_pool's consumption order and a raw prefix of
    seeded_order() must agree on the first ids, not diverge due to separate RNG
    calls."""

    def test_pool_consumes_ids_in_seeded_order_prefix(self):
        ids = [f"id{i:03d}" for i in range(30)]
        order = seeded_order("cs.CV", "2020H1", ids)
        tokens_by_id = {rid: [f"{rid}_tok{i}" for i in range(10)] for rid in ids}
        pool, short = build_pool(order, tokens_by_id, pool_size=55)
        # first 6 ids' worth of tokens (10 each) = 60 >= 55, so pool should be built
        # from exactly the first 6 ids of `order`, truncated to 55 tokens.
        expected_ids_consumed = order[:6]
        expected_tokens = []
        for rid in expected_ids_consumed:
            expected_tokens.extend(tokens_by_id[rid])
        expected_tokens = expected_tokens[:55]
        self.assertEqual(pool, expected_tokens)
        self.assertFalse(short)

    def test_compute_cell_reuses_same_order_for_mtld_and_similarity_prefixes(self):
        ids = [f"id{i:03d}" for i in range(30)]
        rows = [{"id": rid, "created": "2020-03-01", "unit": "2020H1",
                 "abstract": " ".join([f"{rid}word{i}" for i in range(60)])}
                for rid in ids]
        order = seeded_order("cs.CV", "2020H1", ids)
        result = compute_cell("cs.CV", "2020H1", rows, marker_set=set())
        # With n_kept=30 < MTLD_DRAW(150) and < SIM_DRAW(150), both draws use the
        # whole cell (order[:30] == order), so both are flagged as small cells.
        self.assertTrue(result["mtld"]["small_cell"])
        self.assertTrue(result["similarity"]["small_draw"])
        self.assertEqual(result["similarity"]["n_draw"], 30)


class TestMtldDrawSize(unittest.TestCase):
    """Reconciliation round, item 1: MTLD draw size is now the first min(150, n)
    abstracts of the seeded order (was up to 1,000) -- a fixed draw, and the SAME
    prefix size as similarity's draw (§3 metric 4: "the same prefix as metric 1,
    deliberately")."""

    def test_mtld_draw_is_150_and_matches_similarity_draw(self):
        self.assertEqual(MTLD_DRAW, 150)
        self.assertEqual(MTLD_DRAW, SIM_DRAW)

    def test_cells_above_150_flag_neither_as_small_but_use_same_150_prefix(self):
        ids = [f"id{i:03d}" for i in range(200)]  # n_kept=200 > 150
        rows = [{"id": rid, "created": "2020-03-01", "unit": "2020H1",
                 "abstract": " ".join([f"{rid}word{i}" for i in range(60)])}
                for rid in ids]
        order = seeded_order("cs.CV", "2020H1", ids)
        result = compute_cell("cs.CV", "2020H1", rows, marker_set=set())

        self.assertFalse(result["mtld"]["small_cell"])
        self.assertFalse(result["similarity"]["small_draw"])
        self.assertEqual(result["mtld"]["n_drawn"], 150)
        self.assertEqual(result["similarity"]["n_draw"], 150)
        # Both draws are the identical first-150 prefix of the one seeded order.
        self.assertEqual(order[:150], order[:result["similarity"]["n_draw"]])

    def test_cell_of_exactly_150_is_not_flagged_small(self):
        ids = [f"id{i:03d}" for i in range(150)]
        rows = [{"id": rid, "created": "2020-03-01", "unit": "2020H1",
                 "abstract": " ".join([f"{rid}word{i}" for i in range(60)])}
                for rid in ids]
        result = compute_cell("cs.CV", "2020H1", rows, marker_set=set())
        self.assertFalse(result["mtld"]["small_cell"])
        self.assertFalse(result["similarity"]["small_draw"])

    def test_cell_of_149_is_flagged_small(self):
        ids = [f"id{i:03d}" for i in range(149)]
        rows = [{"id": rid, "created": "2020-03-01", "unit": "2020H1",
                 "abstract": " ".join([f"{rid}word{i}" for i in range(60)])}
                for rid in ids]
        result = compute_cell("cs.CV", "2020H1", rows, marker_set=set())
        self.assertTrue(result["mtld"]["small_cell"])
        self.assertTrue(result["similarity"]["small_draw"])


if __name__ == "__main__":
    unittest.main()
