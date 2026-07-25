import os
import unittest

import _pathfix  # noqa: F401
from metrics import load_marker_set, marker_rate, MARKER_STYLE_COUNT, default_marker_csv


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


if __name__ == "__main__":
    unittest.main()
