"""Unit tests for scripts/audit.py.

Run from the repository root with:
    python3 -m unittest discover -s drafts/2026-07-26-one-line-for-ten-thousand/tests -t .

or directly:
    python3 drafts/2026-07-26-one-line-for-ten-thousand/tests/test_audit.py

Standard library only, offline. The import path is made robust by inserting
the sibling `scripts/` directory onto sys.path relative to this file's own
location, so the tests run regardless of the caller's working directory.
"""

import json
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


class TestComputeResidueByHostAndMechanism(unittest.TestCase):
    """R2: pin A21's pure computation against a small synthetic ledger exercising each
    of its classes, and separately against the real frozen resolution ledger."""

    def _synthetic_rows(self):
        # A retried 404: first row 404/false, later row (same id) 200/true.
        retried_404 = [
            {"id": "x-retried", "quelle": "kaggle", "quell_id": "k1",
             "url": "https://www.kaggle.com/dsv/1", "datum": "2026-07-26T17:42:45Z",
             "http_status": 404, "finale_url": "https://www.kaggle.com/dsv/1", "ok": False},
            {"id": "x-retried", "quelle": "kaggle", "quell_id": "k1",
             "url": "https://www.kaggle.com/dsv/1", "datum": "2026-07-26T17:48:01Z",
             "http_status": 200, "finale_url": "https://www.kaggle.com/dsv/1", "ok": True},
        ]
        # An unretried 404 on the defect host, checked before the earliest confirmed
        # row on that host (2026-07-26T17:48:01Z above) — the case A21 exists for.
        unretried_defect_host_404 = [
            {"id": "x-unretried", "quelle": "datacite", "quell_id": "10.x/dsv/2",
             "url": "https://www.kaggle.com/dsv/2", "datum": "2026-07-26T15:04:54Z",
             "http_status": 404, "finale_url": "https://www.kaggle.com/dsv/2", "ok": False},
        ]
        # A 403 (access-policy refusal), never confirmed.
        refusal_403 = [
            {"id": "x-403", "quelle": "datacite", "quell_id": "10.x/gbif/1",
             "url": "https://www.gbif.org/occurrence/1", "datum": "2026-07-26T18:00:00Z",
             "http_status": 403, "finale_url": "https://www.gbif.org/occurrence/1", "ok": False},
        ]
        # A transport outage: no http_status key at all, carries `ausfall` instead.
        outage = [
            {"id": "x-outage", "quelle": "datacite", "quell_id": "10.x/osti/1",
             "url": "https://www.osti.gov/x/1", "datum": "2026-07-26T18:05:00Z",
             "ausfall": "connection-reset", "finale_url": None, "ok": False},
        ]
        return retried_404 + unretried_defect_host_404 + refusal_403 + outage

    def test_synthetic_ledger_classifies_each_row_correctly(self):
        rows = self._synthetic_rows()
        result = audit.compute_residue_by_host_and_mechanism(rows, defect_host="www.kaggle.com")
        self.assertEqual(result["status_404_total"], 2)
        self.assertEqual(result["status_404_host_distribution"], {"www.kaggle.com": 2})
        self.assertEqual(result["retried_404_count"], 1)
        self.assertEqual(result["never_confirmed_404_count"], 1)
        self.assertEqual(
            result["never_confirmed_404_detail"],
            [{"id": "x-unretried", "quelle": "datacite", "datum": "2026-07-26T15:04:54Z"}],
        )
        self.assertEqual(result["earliest_ok_datum_on_defect_host"], "2026-07-26T17:48:01Z")
        self.assertTrue(result["never_confirmed_404_all_predate_earliest_ok"])
        self.assertEqual(result["failures_total"], 4)  # every row but the retried id's ok=true row
        self.assertEqual(result["class_retried_and_confirmed"], 1)
        self.assertEqual(result["class_403"], 1)
        self.assertEqual(result["class_outage"], 1)
        self.assertEqual(result["class_defect_host_404_unretried"], 1)
        self.assertEqual(result["residue_host_mechanism"], 0)
        self.assertEqual(result["classes_sum"], result["failures_total"])

    def test_synthetic_ledger_residue_is_nonzero_for_a_row_matching_no_class(self):
        # An unexplained failure that is on neither the defect host nor 403 nor outage
        # nor retried must show up in the residue, not silently disappear.
        rows = self._synthetic_rows() + [
            {"id": "x-mystery", "quelle": "datacite", "quell_id": "10.x/mystery/1",
             "url": "https://example.org/x/1", "datum": "2026-07-26T19:00:00Z",
             "http_status": 500, "finale_url": "https://example.org/x/1", "ok": False},
        ]
        result = audit.compute_residue_by_host_and_mechanism(rows, defect_host="www.kaggle.com")
        self.assertEqual(result["residue_host_mechanism"], 1)
        self.assertEqual(result["classes_sum"], result["failures_total"])

    def test_matches_real_frozen_resolution_ledger(self):
        report = audit.build_report()
        by_id = {a["id"]: a for a in report["assertions"]}
        computed = by_id["A21"]["computed"]
        expected = by_id["A21"]["expected"]
        self.assertEqual(computed, expected)
        self.assertEqual(computed["status_404_total"], 402)
        self.assertEqual(computed["retried_404_count"], 400)
        self.assertEqual(computed["never_confirmed_404_count"], 2)
        self.assertEqual(computed["residue_host_mechanism"], 0)
        self.assertEqual(computed["classes_sum"], computed["failures_total"])


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

    def test_all_assertions_pass_and_ids_are_exactly_a1_to_a21(self):
        report = audit.build_report()
        self.assertTrue(report["verdict"]["all_pass"], msg=report["verdict"])
        ids = [a["id"] for a in report["assertions"]]
        expected_ids = [f"A{i}" for i in range(1, 22)]
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


class CaveatsBlockTravels(unittest.TestCase):
    """R3: the report's top-level `caveats` block is the surface a machine reader of
    audit.json/data.json alone actually sees. A regression guard of the same kind as
    WithdrawalNotesTravel: fails if the block goes missing, is emptied, or loses any
    of its required keys."""

    REQUIRED_KEYS = (
        "corpus_age",
        "channel_not_character",
        "reversal",
        "reader_distinction",
        "no_entry_level_claim",
        "withdrawn_claims",
        "classification_choice",
    )

    def test_caveats_present_after_upstream_and_nonempty(self):
        report = audit.build_report()
        self.assertIn("caveats", report, "top-level caveats block is missing")
        self.assertTrue(report["caveats"], "caveats block is empty")
        keys = list(report.keys())
        self.assertLess(
            keys.index("upstream"), keys.index("caveats"),
            "caveats must be placed after upstream in the report dict",
        )

    def test_caveats_carries_every_required_key_nonblank(self):
        report = audit.build_report()
        caveats = report["caveats"]
        for key in self.REQUIRED_KEYS:
            self.assertIn(key, caveats, f"caveats missing required key: {key}")
            value = caveats[key]
            self.assertTrue(value, f"caveats['{key}'] is empty")

    def test_corpus_age_states_the_pin_and_the_computed_age_gap(self):
        """The age must be DERIVED, not typed.

        The second gauntlet round found this field hardcoded to a generation time that
        the report's own `generated_utc` contradicted after a re-run — and found the
        earlier version of this very test pinning that stale literal, so a correction
        would have failed the suite. The test now checks the relationship instead of a
        string: both endpoints must come from the data/pin, and the stated interval must
        equal the one recomputed here independently of the sentence.
        """
        report = audit.build_report()
        text = report["caveats"]["corpus_age"]
        self.assertIn(audit.UPSTREAM_COMMIT, text)
        self.assertIn(audit.UPSTREAM_TAG, text)
        self.assertIn(audit.UPSTREAM_TAG_SHA, text)
        self.assertIn(audit.UPSTREAM_COMMIT_UTC, text)

        data = audit.load_inputs()
        first_close, age = audit.corpus_age_sentence(data["run_manifests"])
        self.assertIn(first_close, text)
        self.assertIn(age, text)

        # And the interval itself, recomputed here from the two endpoints.
        from datetime import datetime, timezone
        fmt = "%Y-%m-%dT%H:%M:%SZ"
        start = datetime.strptime(first_close, fmt).replace(tzinfo=timezone.utc)
        pin = datetime.strptime(audit.UPSTREAM_COMMIT_UTC, fmt).replace(tzinfo=timezone.utc)
        minutes = int((pin - start).total_seconds() // 60)
        self.assertEqual(age, f"{minutes // 60} hours {minutes % 60} minutes")

    def test_corpus_age_never_claims_generated_utc_is_the_measurement_time(self):
        """`generated_utc` drifts on every reproduction; no caveat may hang a measurement
        on it. Guards the exact defect the second round found."""
        report = audit.build_report()
        text = report["caveats"]["corpus_age"]
        self.assertNotIn(report["generated_utc"], text)
        self.assertIn("generated_utc", text)

    def test_reversal_points_at_a18(self):
        report = audit.build_report()
        self.assertIn("A18", report["caveats"]["reversal"])

    def test_channel_not_character_does_not_cite_a18_as_prose_being_right(self):
        """A18 is the reversal — the one place the register's prose is wrong. The second
        gauntlet round found it cited under `channel_not_character` as an example of the
        opposite. The corrected field may mention A18 only to say it is NOT such an
        example."""
        report = audit.build_report()
        text = report["caveats"]["channel_not_character"]
        self.assertIn("A19", text)
        self.assertIn("A20", text)
        if "A18" in text:
            self.assertIn("NOT an example", text)

    def test_the_two_reductions_are_tagged_differently(self):
        """A16 rests on facts observable in a row; A21 adds a class by analogy. They must
        not both be tagged `observed` — the second round's Skeptic and Verifier both caught
        this."""
        report = audit.build_report()
        kinds = {a["id"]: a["kind"] for a in report["assertions"]}
        self.assertEqual(kinds["A16"], "observed")
        self.assertEqual(kinds["A21"], "inference")

    def test_no_surface_calls_a16_a_source_label_reduction(self):
        """A16's code uses no `quelle` filter. The description that said otherwise was
        wrong in the results file itself, which is the surface this work says a machine
        reads; it may not come back."""
        report = audit.build_report()
        blob = json.dumps(report, ensure_ascii=False)
        # The phrase may appear only where it is explicitly marked as a correction.
        for bad in ["is a source-label reduction", "keys on (`quelle`"]:
            self.assertNotIn(bad, blob)

    def test_withdrawn_claims_is_a_two_entry_dict_of_strings(self):
        # Shape rule: plain string / list of strings / small dict of strings. A dict
        # mapping each withdrawn claim to its one-line replacement fits that rule and
        # is what work.astro's generic caveats renderer (asPairs) expects for a dict
        # value: a flat mapping of string to string.
        report = audit.build_report()
        withdrawn = report["caveats"]["withdrawn_claims"]
        self.assertIsInstance(withdrawn, dict)
        self.assertEqual(len(withdrawn), 2)
        for claim, replacement in withdrawn.items():
            self.assertIsInstance(claim, str)
            self.assertIsInstance(replacement, str)
            self.assertTrue(claim.strip())
            self.assertTrue(replacement.strip())

    def test_caveats_values_are_plain_strings_lists_or_dicts_of_strings(self):
        report = audit.build_report()
        for key, value in report["caveats"].items():
            if isinstance(value, str):
                continue
            elif isinstance(value, list):
                for item in value:
                    self.assertIsInstance(item, (str, dict), f"caveats['{key}'] has a non-string/dict item")
                    if isinstance(item, dict):
                        for sub_value in item.values():
                            self.assertIsInstance(sub_value, str)
            elif isinstance(value, dict):
                for sub_value in value.values():
                    self.assertIsInstance(sub_value, str)
            else:
                self.fail(f"caveats['{key}'] is neither a string, list nor dict: {type(value)}")

    def test_caveats_prose_never_names_the_two_withheld_companies(self):
        report = audit.build_report()
        banned = ("kaggle", "huggingface", "hugging face")

        def check(value, path):
            if isinstance(value, str):
                lowered = value.lower()
                for term in banned:
                    self.assertNotIn(term, lowered, msg=f"caveats field '{path}' names a withheld company: {value!r}")
            elif isinstance(value, list):
                for i, item in enumerate(value):
                    check(item, f"{path}[{i}]")
            elif isinstance(value, dict):
                for k, v in value.items():
                    check(v, f"{path}.{k}")

        for key, value in report["caveats"].items():
            check(value, key)


class ResidueReductionsStayDistinct(unittest.TestCase):
    """R2 regression guard: A16's source-label residue and A21's host-and-mechanism
    residue must not be silently collapsed into the same figure by an edit that drops
    one of the two reductions. On the real frozen ledger they are 2 and 0 respectively
    — different by construction, since A21 exists to show the choice matters."""

    def test_a16_and_a21_residue_counts_differ_on_real_input(self):
        report = audit.build_report()
        by_id = {a["id"]: a for a in report["assertions"]}
        a16_residue = by_id["A16"]["computed"]["class_residue"]
        a21_residue = by_id["A21"]["computed"]["residue_host_mechanism"]
        self.assertEqual(a16_residue, 2)
        self.assertEqual(a21_residue, 0)
        self.assertNotEqual(
            a16_residue, a21_residue,
            "A16's source-label residue and A21's host-and-mechanism residue must stay "
            "distinct: if an edit makes them equal, it has likely dropped one of the two "
            "reductions (the whole point of R2 is that the reduction choice matters).",
        )

    def test_a16_note_points_to_a21(self):
        report = audit.build_report()
        by_id = {a["id"]: a for a in report["assertions"]}
        self.assertIn("A21", by_id["A16"]["note"])


if __name__ == "__main__":
    unittest.main()
