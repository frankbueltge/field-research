import unittest

import _pathfix  # noqa: F401
from extract_units import apply_exclusions, extract_all, EXCLUDED_FILES
from tokenizer import tokenize


class TestExclusionRule1FencedCodeBlocks(unittest.TestCase):
    def test_fenced_block_dropped_including_fence_markers(self):
        lines = [
            "# Heading",
            "prose before",
            "```python",
            "def f(): return dropped_code_tokens",
            "```",
            "prose after",
        ]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("prose before\nprose after"))

    def test_multiple_fenced_blocks(self):
        lines = [
            "# Heading",
            "one",
            "```",
            "code one",
            "```",
            "two",
            "```bash",
            "code two",
            "```",
            "three",
        ]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("one\ntwo\nthree"))


class TestExclusionRule2Blockquotes(unittest.TestCase):
    def test_blockquote_line_dropped(self):
        lines = [
            "# Heading",
            "normal text",
            "> quoted material dropped entirely",
            "more normal text",
        ]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("normal text\nmore normal text"))

    def test_indented_blockquote_dropped(self):
        lines = ["# Heading", "kept", "   > also dropped despite leading spaces"]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("kept"))


class TestExclusionRule3TableRows(unittest.TestCase):
    def test_table_row_dropped(self):
        lines = [
            "# Heading",
            "before table",
            "| col1 | col2 |",
            "|---|---|",
            "| a | b |",
            "after table",
        ]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("before table\nafter table"))


class TestExclusionRule4Headings(unittest.TestCase):
    def test_own_heading_and_subheadings_dropped(self):
        lines = [
            "# Top heading dropped",
            "## Sub heading also dropped",
            "### Sub sub heading dropped too",
            "prose stays",
        ]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("prose stays"))


class TestExclusionRule5InlineCodeSpans(unittest.TestCase):
    def test_inline_code_span_replaced_by_space(self):
        lines = ["# Heading", "before `some_identifier` after"]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("before   after"))

    def test_multiple_inline_spans_on_one_line(self):
        lines = ["# Heading", "`a.py` and `b.py` were touched"]
        got = apply_exclusions(lines)
        self.assertEqual(got, tokenize("  and   were touched"))


class TestExclusionRuleOrderCombined(unittest.TestCase):
    def test_all_rules_together(self):
        lines = [
            "# Session heading",
            "opening prose",
            "> a quoted verdict, dropped",
            "| ledger | row |",
            "```",
            "traceback dropped",
            "```",
            "## Sub heading dropped",
            "closing prose with `inline_code` inside",
        ]
        got = apply_exclusions(lines)
        expected = tokenize("opening prose\nclosing prose with   inside")
        self.assertEqual(got, expected)


class TestSessionOwnFileExclusion(unittest.TestCase):
    def test_2026_07_26_excluded_by_name(self):
        # This run's own journal entry — see extract_units module docstring and
        # DEVIATIONS-CANDIDATES.md item 1.
        self.assertIn("2026-07-26.md", EXCLUDED_FILES)


class TestExtractAllRegression(unittest.TestCase):
    """Cross-checked against provenance/feasibility-pretest.md, computed independently
    before this extractor was built."""

    @classmethod
    def setUpClass(cls):
        cls.units = extract_all()

    def test_n_equals_73(self):
        self.assertEqual(len(self.units), 73)

    def test_total_tokens_matches_pretest(self):
        self.assertEqual(sum(u["n_tokens"] for u in self.units), 110329)

    def test_min_max_tokens_match_pretest(self):
        ns = [u["n_tokens"] for u in self.units]
        self.assertEqual(min(ns), 349)
        self.assertEqual(max(ns), 3417)

    def test_units_below_600_match_pretest(self):
        below = [u["index"] for u in self.units if u["n_tokens"] < 600]
        self.assertEqual(below, [29, 33, 40])

    def test_unit_1_and_73_match_pretest(self):
        self.assertEqual(self.units[0]["n_tokens"], 2789)
        self.assertEqual(self.units[0]["date"], "2026-07-01")
        self.assertEqual(self.units[-1]["n_tokens"], 3093)
        self.assertEqual(self.units[-1]["date"], "2026-07-25")

    def test_indexing_is_contiguous_from_1(self):
        self.assertEqual([u["index"] for u in self.units], list(range(1, 74)))

    def test_ordering_is_filename_then_position(self):
        pairs = [(u["date"], u["position_in_file"]) for u in self.units]
        self.assertEqual(pairs, sorted(pairs))


if __name__ == "__main__":
    unittest.main()
