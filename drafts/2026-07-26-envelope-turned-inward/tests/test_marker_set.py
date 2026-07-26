import unittest

import _pathfix  # noqa: F401
import metrics_units as mu


class TestMarkerSetSize(unittest.TestCase):
    def test_csv_sha256_matches_pinned_value(self):
        digest = mu.verify_marker_csv()
        self.assertEqual(digest, mu.MARKER_CSV_SHA256)

    def test_marker_set_has_exactly_407_words(self):
        from metrics import load_marker_set
        marker_set = load_marker_set(mu.MARKER_CSV_PATH)
        self.assertEqual(len(marker_set), 407)


if __name__ == "__main__":
    unittest.main()
