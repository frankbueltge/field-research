#!/usr/bin/env python3
"""The 2026-08-04 population correction, as a test rather than a note.

A note records that something was corrected. A test fails when it is uncorrected again.
This practice learned that on 2026-08-04 by finding a verdict it had declared void standing
unmarked fifty times inside another shipped work's data layer, a day after publishing the
prose that voided it.

These assertions run over the PUBLISHED files in this directory, not over fixtures, so they
fail if a future edit drops the marking, if the marking and the correction text disagree
about a count, or if a case appears whose population status nobody recorded.

    cd works/2026-08-03-where-the-reader-declines/tests && python3 -m unittest discover
"""

from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

WORK = Path(__file__).resolve().parent.parent
DATA = json.loads((WORK / "data.json").read_text(encoding="utf-8"))
SECOND = json.loads((WORK / "second-reader-2026-08-04.json").read_text(encoding="utf-8"))
CORRECTIONS = (WORK / "CORRECTIONS.md").read_text(encoding="utf-8")
ASTRO = (WORK / "work.astro").read_text(encoding="utf-8")
BUILDER = (WORK / "build_data.py").read_text(encoding="utf-8")


class TestTheMarkingReachesEveryCase(unittest.TestCase):
    def test_top_level_notice_present(self):
        c = DATA.get("_population_correction")
        self.assertIsNotNone(c, "data.json lost its top-level _population_correction")
        self.assertEqual(c["date"], "2026-08-04")
        self.assertIn("NOT REPRODUCED", c["notice"])
        self.assertEqual(c["published_n"], 39)
        self.assertEqual(c["independent_readers_n"], {"R1": 23, "R2": 23})

    def test_every_case_carries_both_readers_and_a_status(self):
        for case in DATA["cases"]:
            with self.subTest(case=case["case_id"]):
                v = case.get("in_population_second_readers")
                self.assertIsNotNone(v, "no second-reader record")
                self.assertEqual(set(v), {"R1", "R2"})
                for who in ("R1", "R2"):
                    self.assertIn(v[who], ("IN", "OUT", "UNDECIDABLE"))
                self.assertRegex(case.get("in_population_status", ""), r"^(CONFIRMED|DISPUTED)")

    def test_status_agrees_with_the_verdicts_it_summarises(self):
        """The status may not say CONFIRMED where a reader in fact disagreed."""
        for case in DATA["cases"]:
            published = "IN" if case["in_population"] else "OUT"
            v = case["in_population_second_readers"]
            agreed = v["R1"] == published and v["R2"] == published
            with self.subTest(case=case["case_id"]):
                self.assertEqual(
                    case["in_population_status"].startswith("CONFIRMED"), agreed,
                    f"status contradicts the verdicts: published {published}, {v}")

    def test_the_two_files_do_not_disagree_about_a_single_verdict(self):
        by_id = {c["case_id"]: c for c in SECOND["cases"]}
        self.assertEqual(len(by_id), len(DATA["cases"]))
        for case in DATA["cases"]:
            rec = by_id[case["case_id"]]
            with self.subTest(case=case["case_id"]):
                self.assertEqual(case["in_population_second_readers"]["R1"], rec["R1"])
                self.assertEqual(case["in_population_second_readers"]["R2"], rec["R2"])
                self.assertEqual(case["in_population"], rec["published_in_population"])


class TestTheCountsAreTheOnesPublished(unittest.TestCase):
    """Every number the correction states about itself, recomputed from the data."""

    def test_published_split_is_still_39(self):
        self.assertEqual(sum(1 for c in DATA["cases"] if c["in_population"]), 39)

    def test_both_readers_return_23(self):
        for who in ("R1", "R2"):
            n = sum(1 for c in DATA["cases"] if c["in_population_second_readers"][who] == "IN")
            self.assertEqual(n, 23, f"{who} in-population count moved")

    def test_no_reader_added_a_case_this_split_excludes(self):
        """The correction's sharpest claim. If this ever fails, the claim is false."""
        for who in ("R1", "R2"):
            added = [c["case_id"] for c in DATA["cases"]
                     if not c["in_population"] and c["in_population_second_readers"][who] == "IN"]
            self.assertEqual(added, [], f"{who} added excluded case(s): {added}")

    def test_the_exclusions_are_twenty_of_twenty_one_not_unanimous(self):
        """Withdrawn claim, locked so it cannot be restated.

        Session 88 published "all 21 exclusions were confirmed unanimously" in four files.
        Its own Verifier refuted it: position 52 drew UNDECIDABLE from R1. The zero that
        actually carries the finding is asserted separately above.
        """
        out_cases = [c for c in DATA["cases"] if not c["in_population"]]
        self.assertEqual(len(out_cases), 21)
        unanimous = [c for c in out_cases
                     if c["in_population_second_readers"] == {"R1": "OUT", "R2": "OUT"}]
        self.assertEqual(len(unanimous), 20, "the exclusions are 20 of 21 unanimous, not 21")
        odd = [c for c in out_cases if c not in unanimous]
        self.assertEqual(odd[0]["case_id"], "mbcls-2606.04228")
        self.assertEqual(odd[0]["in_population_second_readers"], {"R1": "UNDECIDABLE", "R2": "OUT"})
        # Rule 6: the withdrawn sentence STAYS, struck. What must not happen is that it
        # stands as a live assertion. So every occurrence must be inside a struck quotation.
        needle = "All 21 exclusions were confirmed unanimously"
        for path, text in (("CORRECTIONS.md", CORRECTIONS), ("build_data.py", BUILDER)):
            live = [ln for ln in text.splitlines()
                    if needle in ln and not (ln.lstrip().startswith(">") and "~~" in ln)]
            self.assertEqual(live, [], f"{path} states the withdrawn unanimity claim live")
        self.assertIn("~~All 21 exclusions were confirmed unanimously.~~", CORRECTIONS,
                      "the withdrawn sentence was deleted instead of struck")

    def test_the_withdrawn_fisher_figure_is_not_restated(self):
        """The post-hoc p-value was withdrawn entirely, not corrected to a new number."""
        self.assertIn("WITHDRAWN, same day, and not replaced", CORRECTIONS)
        live = CORRECTIONS.split("The whole quantification is WITHDRAWN")[1]
        self.assertNotIn("p = 0.039.)*", live, "the withdrawn figure reappears after its withdrawal")

    def test_eighteen_cases_are_disputed(self):
        n = sum(1 for c in DATA["cases"] if c["in_population_status"].startswith("DISPUTED"))
        self.assertEqual(n, 18)
        self.assertIn("Eighteen of sixty cases are disputed", CORRECTIONS)

    def test_recomputed_contextualizes_counts_match_the_correction_table(self):
        expected = {"R1": (19, 3), "R2": (20, 4)}      # (machine, blind reader)
        for who, (m_exp, g_exp) in expected.items():
            pop = [c for c in DATA["cases"]
                   if c["in_population_second_readers"][who] == "IN"]
            m = sum(1 for c in pop if c["machine"]["relation"] == "contextualizes")
            g = sum(1 for c in pop if c["gold"]["relation"] == "contextualizes")
            self.assertEqual((m, g), (m_exp, g_exp), f"{who} recomputed table moved")

    def test_the_single_supports_case_stays_inside_every_split(self):
        sup = [c for c in DATA["cases"]
               if c["in_population"] and c["gold"]["relation"] == "supports"]
        self.assertEqual(len(sup), 1)
        for who in ("R1", "R2"):
            self.assertEqual(sup[0]["in_population_second_readers"][who], "IN")


class TestTheCorrectionReachesTheOtherSurfaces(unittest.TestCase):
    """The failure this practice keeps repeating is a correction that stops at one surface."""

    def test_the_page_carries_a_dated_correction(self):
        self.assertIn("Correction, 2026-08-04", ASTRO)
        self.assertIn("population disputed 2026-08-04", ASTRO)

    def test_the_page_computes_the_corrected_figures_rather_than_hardcoding_them(self):
        """A number typed into the page can drift from the file; a counted one cannot."""
        self.assertIn("readerPop", ASTRO)
        self.assertIn("second-reader-2026-08-04.json", ASTRO)
        self.assertNotRegex(
            ASTRO, r"returned <strong>23</strong>",
            "the corrected n is hardcoded in the page instead of counted")

    def test_the_builder_warns_before_the_dict_it_would_regenerate(self):
        self.assertIn("CORRECTION 2026-08-04", BUILDER)
        self.assertLess(BUILDER.index("CORRECTION 2026-08-04"),
                        BUILDER.index("POPULATION: dict[int, str]"),
                        "the note must stand above the dict, not below it")

    def test_the_correction_states_its_own_sibling_key_limit(self):
        """Do not let the disclosure of the jq gap be quietly dropped in a later edit."""
        self.assertIn("sibling key, not a wrapper", CORRECTIONS)
        # The disclosure wraps across a line in the markdown; match across it rather than
        # letting a reflow of the paragraph look like the disclosure being removed.
        self.assertIsNotNone(
            re.search(r"jq[\s\S]{0,80}select\(\.in_population\)", CORRECTIONS),
            "the concrete query that misses the correction is no longer shown")

    def test_the_correction_does_not_claim_a_gauntlet_it_has_not_had(self):
        """Session 87 published a correction that claimed in the past tense that its own
        review had already run. Three reviewers caught it. Not twice."""
        m = re.search(r"^.*\bgauntlet\b.*$", CORRECTIONS, re.M | re.I)
        self.assertIsNotNone(m)
        # A gauntlet did run on this correction, and then the corrections it forced were
        # applied after its verdicts. Both facts must stay on the face of the entry.
        self.assertIn("no gauntlet verdict covers the exact bytes of this", CORRECTIONS)
        for report in ("VERIFICATION-2026-08-04.md", "SKEPTIC-2026-08-04.md"):
            self.assertTrue((WORK / report).exists(), f"{report} is cited and missing")
            self.assertIn(report, CORRECTIONS)


class TestNoPublishedValueWasChanged(unittest.TestCase):
    def test_in_population_is_untouched_by_the_marking(self):
        """Regenerating from build_data.py must still reproduce the published split."""
        marked = {c["position"]: c["in_population"] for c in DATA["cases"]}
        self.assertEqual(sum(marked.values()), 39)
        self.assertNotIn("in_population_second_readers", BUILDER,
                         "the marking must live in apply_second_reader.py, not in the builder")


if __name__ == "__main__":
    unittest.main(verbosity=2)
