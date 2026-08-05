#!/usr/bin/env python3
"""selftest.py — check the scoring code on cases whose answers are known by hand.

`score.py` produces the numbers this session will publish. Every function in it that does
arithmetic is exercised here against a fixture whose correct answer was worked out on paper
first, so that a mistake in the scoring shows up as a failing assertion rather than as a
finding. Offline, stdlib only, no network, no repository state.

Run:  python3 scripts/selftest.py
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import score  # noqa: E402


def cases_from(spec: dict) -> dict:
    """Minimal case records: id -> {in_population, gold, machine, title, excerpt, reasons}."""
    out = {}
    for cid, (inpop, gold, machine) in spec.items():
        out[cid] = {
            "case_id": cid,
            "title": "t",
            "excerpt": "e",
            "in_population": inpop,
            "population_reason": "" if not inpop else "reason",
            "exclusion_reason": "reason" if not inpop else "",
            "gold": {"relation": gold},
            "machine": {"relation": machine},
        }
    return out


class TestKappa(unittest.TestCase):
    def test_perfect_agreement_is_one(self):
        self.assertEqual(score.kappa([(True, True), (False, False)] * 5), 1.0)

    def test_total_disagreement_is_negative(self):
        k = score.kappa([(True, False), (False, True)] * 5)
        self.assertLess(k, 0)

    def test_known_2x2_by_hand(self):
        # a=20 both IN, b=5 left IN right OUT, c=10 left OUT right IN, d=15 both OUT.
        # po = 35/50 = .70 ; pa(left IN) = 25/50 = .5 ; pb(right IN) = 30/50 = .6
        # pe = .5*.6 + .5*.4 = .30 + .20 = .50 ; kappa = (.70-.50)/(1-.50) = .40
        pairs = ([(True, True)] * 20 + [(True, False)] * 5
                 + [(False, True)] * 10 + [(False, False)] * 15)
        self.assertEqual(score.kappa(pairs), 0.4)

    def test_degenerate_all_same_class_returns_none(self):
        # Both raters say IN to everything: pe == 1, kappa undefined, must not divide by zero.
        self.assertIsNone(score.kappa([(True, True)] * 10))

    def test_empty_returns_none(self):
        self.assertIsNone(score.kappa([]))


class TestCompare(unittest.TestCase):
    def setUp(self):
        self.cases = cases_from({
            "a": (True, "supports", "supports"),
            "b": (True, "qualifies", "contextualizes"),
            "c": (False, "contradicts", "contextualizes"),
            "d": (False, "qualifies", "qualifies"),
        })

    def test_undecidable_counts_as_disagreement_and_is_reported(self):
        left = {"a": "IN", "b": "IN", "c": "OUT", "d": "OUT"}
        right = {"a": "IN", "b": "UNDECIDABLE", "c": "OUT", "d": "OUT"}
        r = score.compare(self.cases, left, right, "L", "R")
        self.assertEqual(r["agree"], 3)                  # b differs
        self.assertEqual(r["undecidable_involved"], 1)
        self.assertEqual(r["kappa_n"], 3)                # b excluded from kappa
        self.assertEqual(len(r["disputes"]), 1)
        self.assertEqual(r["disputes"][0]["case_id"], "b")

    def test_direction_counts_are_not_symmetric(self):
        left = {"a": "IN", "b": "IN", "c": "OUT", "d": "OUT"}
        right = {"a": "OUT", "b": "IN", "c": "IN", "d": "OUT"}
        r = score.compare(self.cases, left, right, "L", "R")
        self.assertEqual(r["L_IN_to_R_OUT"], 1)          # a
        self.assertEqual(r["L_OUT_to_R_IN"], 1)          # c
        self.assertEqual(r["agreement_pct"], 50.0)


class TestTableAndMembership(unittest.TestCase):
    def setUp(self):
        self.cases = cases_from({
            "a": (True, "supports", "contextualizes"),
            "b": (True, "qualifies", "contextualizes"),
            "c": (True, "undecidable", "contextualizes"),
            "d": (False, "contradicts", "qualifies"),
        })

    def test_table_counts_and_ratio(self):
        t = score.table(self.cases, {"a", "b", "c"})
        self.assertEqual(t["n"], 3)
        self.assertEqual(t["machine"]["contextualizes"], 3)
        self.assertEqual(t["gold"]["contextualizes"], 0)
        self.assertIsNone(t["ratio_machine_over_gold_contextualizes"])  # no divide by zero

    def test_none_relation_is_read_as_undecidable(self):
        cases = cases_from({"a": (True, None, "contextualizes")})
        t = score.table(cases, {"a"})
        self.assertEqual(t["gold"]["undecidable"], 1)

    def test_membership_respects_the_undecidable_branch(self):
        v = {"a": "IN", "b": "UNDECIDABLE", "c": "OUT"}
        self.assertEqual(score.membership(v, False), {"a"})
        self.assertEqual(score.membership(v, True), {"a", "b"})


class TestPeekCheck(unittest.TestCase):
    """The check must not fire on shared source vocabulary and must fire on borrowed wording."""

    def test_quoting_the_same_excerpt_is_not_contamination(self):
        cases = {
            "a": {"title": "Automated peer review", "excerpt": "We automate peer review.",
                  "population_reason": "automating peer review", "exclusion_reason": ""},
        }
        reader = {"a": {"reason": "This automates peer review, a research activity."}}
        r = score.peek(cases, reader, "R")
        self.assertEqual(r["max"], 0.0)          # every shared word came from the excerpt
        self.assertFalse(r["compromised"])

    def test_borrowed_wording_absent_from_the_source_fires(self):
        cases = {
            "a": {"title": "LogiGAN", "excerpt": "adversarial pretraining.",
                  "population_reason": "",
                  "exclusion_reason": "reasoning capability, no research cycle"},
        }
        reader = {"a": {"reason": "reasoning capability, no research cycle"}}
        r = score.peek(cases, reader, "R")
        self.assertEqual(r["max"], 1.0)
        self.assertTrue(r["compromised"])

    def test_threshold_is_the_one_the_rule_fixed(self):
        self.assertEqual(score.PEEK_CASE_MAX, 0.60)
        self.assertEqual(score.PEEK_MEAN_MAX, 0.35)


class TestValidate(unittest.TestCase):
    def setUp(self):
        self.cases = cases_from({"a": (True, "supports", "supports")})
        self.cases["a"]["title"] = "A Title"
        self.cases["a"]["excerpt"] = "Some body text here."

    def test_non_verbatim_quote_is_caught(self):
        reader = {"a": {"case_id": "a", "verdict": "IN",
                        "deciding_quote": "text that is not there", "reason": "r"}}
        errs = score.validate(self.cases, reader, "R")
        self.assertTrue(any("not verbatim" in e for e in errs))

    def test_verbatim_quote_passes(self):
        reader = {"a": {"case_id": "a", "verdict": "IN",
                        "deciding_quote": "Some body text", "reason": "r"}}
        errs = [e for e in score.validate(self.cases, reader, "R") if "not verbatim" in e]
        self.assertEqual(errs, [])

    def test_bad_verdict_and_empty_reason_are_caught(self):
        reader = {"a": {"case_id": "a", "verdict": "MAYBE",
                        "deciding_quote": "A Title", "reason": "  "}}
        errs = score.validate(self.cases, reader, "R")
        self.assertTrue(any("verdict" in e for e in errs))
        self.assertTrue(any("empty reason" in e for e in errs))


class TestBands(unittest.TestCase):
    """RULE.md §8, exercised on splits whose band was worked out by hand."""

    def build(self, n_ctx_machine: int, n_ctx_gold: int, extra_out: int = 0):
        spec = {}
        for i in range(n_ctx_machine):
            spec[f"m{i}"] = (True, "qualifies", "contextualizes")
        for i in range(n_ctx_gold):
            spec[f"g{i}"] = (True, "contextualizes", "qualifies")
        spec["s"] = (True, "supports", "supports")
        spec["u"] = (True, "undecidable", "qualifies")     # blind reader's in-pop undecidable
        for i in range(extra_out):
            spec[f"o{i}"] = (False, "qualifies", "qualifies")
        return cases_from(spec)

    def test_band_a_when_both_reproduce_the_split(self):
        cases = self.build(10, 4, extra_out=3)
        orig = {c: ("IN" if cases[c]["in_population"] else "OUT") for c in cases}
        r = score.band(cases, orig, {"R1": {c for c in cases if cases[c]["in_population"]},
                                     "R2": {c for c in cases if cases[c]["in_population"]}})
        self.assertEqual(r["band"], "A")

    def test_band_c_when_the_supports_case_leaves(self):
        cases = self.build(10, 4, extra_out=3)
        orig = {c: ("IN" if cases[c]["in_population"] else "OUT") for c in cases}
        pop = {c for c in cases if cases[c]["in_population"]}
        r = score.band(cases, orig, {"R1": pop, "R2": pop - {"s"}})
        self.assertEqual(r["band"], "C")
        self.assertTrue(any("supports" in x for x in r["reasons"]))

    def test_band_c_when_n_moves_by_more_than_five(self):
        cases = self.build(10, 4, extra_out=8)
        orig = {c: ("IN" if cases[c]["in_population"] else "OUT") for c in cases}
        pop = {c for c in cases if cases[c]["in_population"]}
        wide = pop | {f"o{i}" for i in range(6)}
        r = score.band(cases, orig, {"R1": pop, "R2": wide})
        self.assertEqual(r["band"], "C")
        self.assertTrue(any("moves by more than" in x for x in r["reasons"]))

    def test_band_c_when_the_ratio_falls_below_the_threshold(self):
        # machine ctx 10, gold ctx 8 -> ratio 1.25 < 1.5
        cases = self.build(10, 8, extra_out=2)
        orig = {c: ("IN" if cases[c]["in_population"] else "OUT") for c in cases}
        pop = {c for c in cases if cases[c]["in_population"]}
        r = score.band(cases, orig, {"R1": pop, "R2": pop - {"g0"}})
        self.assertEqual(r["band"], "C")

    def test_band_b_when_cases_move_but_the_headline_conditions_hold(self):
        cases = self.build(10, 4, extra_out=3)
        orig = {c: ("IN" if cases[c]["in_population"] else "OUT") for c in cases}
        pop = {c for c in cases if cases[c]["in_population"]}
        moved = (pop - {"g0"}) | {"o0"}        # one swap: n unchanged, ratio 10/3, supports kept
        r = score.band(cases, orig, {"R1": moved, "R2": moved})
        self.assertEqual(r["band"], "B")


if __name__ == "__main__":
    unittest.main(verbosity=2)
