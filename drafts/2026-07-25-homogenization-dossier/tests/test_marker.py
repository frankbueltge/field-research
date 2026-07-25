import os
import unittest

import _pathfix  # noqa: F401
from metrics import load_marker_set, marker_rate, MARKER_STYLE_COUNT, default_marker_csv, compute_cell, POOL_TOKENS


class TestMarkerSetLoading(unittest.TestCase):
    def test_real_csv_yields_exactly_407_style_words(self):
        csv_path = default_marker_csv()
        self.assertTrue(os.path.exists(csv_path), f"expected provenance csv at {csv_path}")
        marker_set = load_marker_set(csv_path)
        self.assertEqual(len(marker_set), MARKER_STYLE_COUNT)
        self.assertEqual(len(marker_set), 407)

    def test_assertion_fires_on_wrong_count(self):
        import csv
        import tempfile
        with tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False, newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["", "word", "type", "part_of_speech", "comment"])
            writer.writeheader()
            writer.writerow({"": "0", "word": "onlyone", "type": "style", "part_of_speech": "noun", "comment": ""})
            path = f.name
        try:
            with self.assertRaises(AssertionError):
                load_marker_set(path)
        finally:
            os.unlink(path)


class TestMarkerRate(unittest.TestCase):
    def test_rate_per_1000_tokens(self):
        marker_set = {"achieving", "acknowledges"}
        tokens = ["the", "model", "achieving"] + ["filler"] * 997  # 1000 tokens, 1 marker
        result = marker_rate(tokens, marker_set)
        self.assertAlmostEqual(result["value"], 1.0, places=9)
        self.assertEqual(result["total_tokens"], 1000)
        self.assertEqual(result["marker_tokens"], 1)

    def test_no_markers_present(self):
        marker_set = {"achieving"}
        tokens = ["nothing", "here", "matches"] * 10
        result = marker_rate(tokens, marker_set)
        self.assertAlmostEqual(result["value"], 0.0, places=9)

    def test_empty_tokens(self):
        result = marker_rate([], {"achieving"})
        self.assertIsNone(result["value"])
        self.assertEqual(result["total_tokens"], 0)


class TestMarkerChannelDecisionalVsContextSplit(unittest.TestCase):
    """The marker channel now has two statistics per cell (reconciliation round,
    item 2): DECISIONAL = rate over the SAME fixed 15,000-token seeded pool as
    hapax/Zipf; CONTEXT = rate over the whole cell (never fed to an envelope)."""

    def test_decisional_uses_pool_context_uses_whole_cell(self):
        marker_set = {"markerword"}
        # One abstract entirely made of the marker word (small, so the 15,000-token
        # pool is short and equals the whole cell here); a second, much larger
        # abstract with NO marker words. The whole-cell rate is diluted by the large
        # marker-free abstract; if the pool were built only from the seeded order's
        # FIRST id and were short of 15,000 tokens, pool == whole cell too in this
        # tiny fixture -- so to actually distinguish decisional vs context we need
        # the pool to be short (fewer than 15,000 tokens) OR to differ in composition
        # from the whole cell. We force a difference by making the cell bigger than
        # the pool can hold.
        rows = []
        # abstract A: 100 marker-word tokens (id chosen so it sorts predictably)
        rows.append({"id": "a", "created": "2020-01-01", "unit": "2020H1",
                     "abstract": " ".join(["markerword"] * 100)})
        # abstract B: 20,000 filler tokens, no markers -- pushes the pool to include
        # only part of the cell (pool_size=15000), while the whole-cell rate must
        # divide by all ~20,100 tokens.
        rows.append({"id": "b", "created": "2020-01-01", "unit": "2020H1",
                     "abstract": " ".join([f"filler{i}" for i in range(20000)])})
        result = compute_cell("cs.CL", "2020H1", rows, marker_set)

        pool_stat = result["marker_rate_pool"]
        whole_stat = result["marker_rate_whole_cell_context"]

        self.assertEqual(whole_stat["total_tokens"], 100 + 20000)
        self.assertEqual(whole_stat["marker_tokens"], 100)

        # The pool is capped at POOL_TOKENS; its total_tokens must reflect that cap
        # (not the whole cell), demonstrating the decisional statistic is computed
        # over a DIFFERENT (smaller, fixed-size) token set than the context one.
        self.assertLessEqual(pool_stat["total_tokens"], POOL_TOKENS)
        self.assertIn("pool_short", pool_stat)

        # Rates differ because the denominators differ (pool vs whole cell).
        self.assertNotAlmostEqual(pool_stat["value"], whole_stat["value"], places=6)

    def test_pool_short_flag_matches_hapax_zipf_pool(self):
        marker_set = {"markerword"}
        rows = [{"id": "a", "created": "2020-01-01", "unit": "2020H1",
                 "abstract": " ".join(["markerword"] * 60)}]
        result = compute_cell("cs.CL", "2020H1", rows, marker_set)
        self.assertTrue(result["marker_rate_pool"]["pool_short"])
        self.assertTrue(result["hapax_share"]["pool_short"])
        self.assertEqual(result["marker_rate_pool"]["pool_short"], result["hapax_share"]["pool_short"])


if __name__ == "__main__":
    unittest.main()
