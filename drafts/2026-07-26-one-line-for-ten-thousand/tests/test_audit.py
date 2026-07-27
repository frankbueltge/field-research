"""Unit tests for scripts/audit.py.

Run from the repository root with:
    python3 -m unittest discover -s drafts/2026-07-26-one-line-for-ten-thousand/tests -t .

or directly:
    python3 drafts/2026-07-26-one-line-for-ten-thousand/tests/test_audit.py

Standard library only, offline. The import path is made robust by inserting
the sibling `scripts/` directory onto sys.path relative to this file's own
location, so the tests run regardless of the caller's working directory.
"""

import os
import sys
import tempfile
import unittest

TESTS_DIR = os.path.dirname(os.path.abspath(__file__))
DRAFT_DIR = os.path.dirname(TESTS_DIR)
SCRIPTS_DIR = os.path.join(DRAFT_DIR, "scripts")
if SCRIPTS_DIR not in sys.path:
    sys.path.insert(0, SCRIPTS_DIR)

import audit  # noqa: E402  (import after sys.path fixup, by design)


class TestHostOf(unittest.TestCase):
    def test_extracts_netloc(self):
        self.assertEqual(audit.host_of("https://www.kaggle.com/foo/bar"), "www.kaggle.com")

    def test_different_hosts_distinguished(self):
        self.assertEqual(audit.host_of("https://www.gbif.org/occurrence/1"), "www.gbif.org")
        self.assertNotEqual(
            audit.host_of("https://www.gbif.org/x"),
            audit.host_of("https://www.kaggle.com/x"),
        )

    def test_empty_or_none_url(self):
        self.assertEqual(audit.host_of(""), "")
        self.assertEqual(audit.host_of(None), "")

    def test_ignores_path_and_query(self):
        self.assertEqual(
            audit.host_of("https://example.org/a/b?c=1#frag"),
            "example.org",
        )


class TestShare(unittest.TestCase):
    def test_basic_ratio(self):
        self.assertAlmostEqual(audit.share(1, 4), 0.25)

    def test_zero_denominator_is_none(self):
        self.assertIsNone(audit.share(5, 0))

    def test_matches_known_withheld_share(self):
        # Same ratio as the withheld-source share fixed in the method (A2).
        self.assertAlmostEqual(round(audit.share(10056, 29666), 6), 0.338974)


class TestRound6(unittest.TestCase):
    def test_rounds_floats(self):
        self.assertEqual(audit.round6(1 / 3), 0.333333)

    def test_passes_through_non_floats(self):
        self.assertEqual(audit.round6(5), 5)
        self.assertEqual(audit.round6("x"), "x")
        self.assertIsNone(audit.round6(None))


class TestCountBy(unittest.TestCase):
    def test_counts_a_field_across_dicts(self):
        rows = [
            {"grund": "a"},
            {"grund": "b"},
            {"grund": "a"},
            {"grund": "a"},
        ]
        self.assertEqual(audit.count_by(rows, "grund"), {"a": 3, "b": 1})

    def test_missing_key_counts_as_none(self):
        rows = [{"x": 1}, {"y": 2}]
        result = audit.count_by(rows, "x")
        self.assertEqual(result, {1: 1, None: 1})

    def test_empty_rows(self):
        self.assertEqual(audit.count_by([], "anything"), {})


class TestSumField(unittest.TestCase):
    def test_sums_integers(self):
        rows = [{"records": 3}, {"records": 5}, {"records": 2}]
        self.assertEqual(audit.sum_field(rows, "records"), 10)

    def test_single_row(self):
        self.assertEqual(audit.sum_field([{"records": 7}], "records"), 7)


class TestLastWinsById(unittest.TestCase):
    def test_last_occurrence_wins(self):
        rows = [
            {"id": "a", "v": 1},
            {"id": "b", "v": 1},
            {"id": "a", "v": 2},
        ]
        result = audit.last_wins_by_id(rows)
        self.assertEqual(result, {"a": {"id": "a", "v": 2}, "b": {"id": "b", "v": 1}})

    def test_single_row_per_id(self):
        rows = [{"id": "x", "v": 1}, {"id": "y", "v": 2}]
        result = audit.last_wins_by_id(rows)
        self.assertEqual(len(result), 2)
        self.assertEqual(result["x"]["v"], 1)

    def test_empty_input(self):
        self.assertEqual(audit.last_wins_by_id([]), {})


class TestGroupById(unittest.TestCase):
    def test_groups_preserve_encounter_order(self):
        rows = [
            {"id": "a", "v": 1},
            {"id": "a", "v": 2},
            {"id": "b", "v": 3},
        ]
        groups = audit.group_by_id(rows)
        self.assertEqual(list(groups.keys()), ["a", "b"])
        self.assertEqual(groups["a"], [{"id": "a", "v": 1}, {"id": "a", "v": 2}])
        self.assertEqual(groups["b"], [{"id": "b", "v": 3}])

    def test_singletons_have_length_one(self):
        rows = [{"id": "a", "v": 1}, {"id": "b", "v": 2}]
        groups = audit.group_by_id(rows)
        self.assertTrue(all(len(v) == 1 for v in groups.values()))

    def test_empty_input(self):
        self.assertEqual(audit.group_by_id([]), {})


class TestReadJsonl(unittest.TestCase):
    def test_skips_blank_lines_and_parses_each_row(self):
        content = '{"a": 1}\n\n{"a": 2}\n   \n{"a": 3}\n'
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as fh:
            fh.write(content)
            path = fh.name
        try:
            rows = audit.read_jsonl(path)
            self.assertEqual(rows, [{"a": 1}, {"a": 2}, {"a": 3}])
        finally:
            os.remove(path)

    def test_empty_file_returns_empty_list(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as fh:
            path = fh.name
        try:
            self.assertEqual(audit.read_jsonl(path), [])
        finally:
            os.remove(path)


class TestSha256OfFile(unittest.TestCase):
    def test_matches_known_digest_of_empty_file(self):
        # SHA-256 of the empty string, a well-known constant.
        with tempfile.NamedTemporaryFile(mode="wb", delete=False) as fh:
            path = fh.name
        try:
            digest = audit.sha256_of_file(path)
            self.assertEqual(
                digest,
                "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
            )
        finally:
            os.remove(path)


class TestReportsEqualIgnoringTimestamp(unittest.TestCase):
    def test_equal_apart_from_timestamp(self):
        a = {"generated_utc": "2026-01-01T00:00:00Z", "x": 1}
        b = {"generated_utc": "2026-02-02T00:00:00Z", "x": 1}
        self.assertTrue(audit.reports_equal_ignoring_timestamp(a, b))

    def test_detects_real_difference(self):
        a = {"generated_utc": "2026-01-01T00:00:00Z", "x": 1}
        b = {"generated_utc": "2026-01-01T00:00:00Z", "x": 2}
        self.assertFalse(audit.reports_equal_ignoring_timestamp(a, b))


class TestFullAuditOverRealInputs(unittest.TestCase):
    """Runs the full audit over the real frozen inputs under provenance/register-records/."""

    def test_all_assertions_pass_and_ids_are_exactly_a1_to_a18(self):
        report = audit.build_report()
        self.assertTrue(report["verdict"]["all_pass"], msg=report["verdict"])
        ids = [a["id"] for a in report["assertions"]]
        expected_ids = [f"A{i}" for i in range(1, 21)]
        self.assertEqual(ids, expected_ids)

    def test_every_assertion_has_required_fields(self):
        report = audit.build_report()
        for a in report["assertions"]:
            for field in ("id", "question", "computed", "expected", "verdict", "evidence", "kind"):
                self.assertIn(field, a, msg=f"assertion {a.get('id')} missing {field}")
            self.assertIn(a["kind"], ("observed", "inference"))
            self.assertIn(a["verdict"], ("PASS", "FAIL"))
            self.assertTrue(len(a["evidence"]) > 0)

    def test_inputs_manifest_hashes_are_recomputed_correctly(self):
        report = audit.build_report()
        for entry in report["inputs"]:
            full_path = os.path.join(audit.DRAFT_DIR, entry["path"])
            self.assertEqual(audit.sha256_of_file(full_path), entry["sha256"])

    def test_prose_fields_never_name_the_two_withheld_companies(self):
        """The naming rule: question/note-style prose must say "the withheld source" and
        "the model-hosting source", never the two sources' corporate names. Data values
        (the `quelle` field and URL hosts, carried under computed/expected) are exempt,
        since those are the frozen record's own content reported verbatim."""
        report = audit.build_report()
        banned = ("kaggle", "huggingface", "hugging face")
        for a in report["assertions"]:
            for key, value in a.items():
                if key in ("computed", "expected"):
                    continue
                if isinstance(value, str):
                    lowered = value.lower()
                    for term in banned:
                        self.assertNotIn(
                            term, lowered,
                            msg=f"assertion {a['id']} field '{key}' names a withheld company: {value!r}",
                        )


class WithdrawalNotesTravel(unittest.TestCase):
    """The gauntlet's lesson, enforced: the corrections must live in the machine-readable
    output, not only in prose. A future edit that strips these notes fails here."""

    def test_a5_a19_a20_carry_interpretive_notes(self):
        report = audit.build_report()
        by_id = {a["id"]: a for a in report["assertions"]}
        for aid in ("A5", "A19", "A20"):
            self.assertIn(aid, by_id, f"{aid} missing from the report")
            note = str(by_id[aid].get("note", ""))
            self.assertTrue(note.strip(), f"{aid} ships without a note field")
        self.assertIn("WITHDRAWN", by_id["A19"]["note"])
        self.assertIn("unit", by_id["A20"]["note"].lower())


if __name__ == "__main__":
    unittest.main()
