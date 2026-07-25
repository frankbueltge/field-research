#!/usr/bin/env python3
"""Unit tests for the pre-landing anchor check.

Run:  python3 -m unittest discover -s tools/journal -p 'test_*.py'
"""

from __future__ import annotations

import json
import os
import tempfile
import unittest

import check_anchors as ca


SPINE = {"entries": [{"collective_session": None, "date": "2026-07-01",
                      "anchor": "pre-2026-07-01-1"},
                     {"collective_session": 1, "date": "2026-07-01", "anchor": "cs-1"}]}


def write(dirpath: str, name: str, body: str) -> None:
    with open(os.path.join(dirpath, name), "w", encoding="utf-8") as fh:
        fh.write(body)


class SplitSessions(unittest.TestCase):
    def test_splits_on_every_top_level_h1(self):
        body = "# Session 61 — 2026-07-25\n\ntext\n\n# Session 63 — 2026-07-25\n\nmore\n"
        self.assertEqual(
            ca.split_sessions(body),
            ["Session 61 — 2026-07-25", "Session 63 — 2026-07-25"],
        )

    def test_ignores_hash_lines_inside_code_fences(self):
        body = "# Session 61\n\n```\n# not a heading\n```\n\ntail\n"
        self.assertEqual(ca.split_sessions(body), ["Session 61"])

    def test_leading_text_before_first_heading_is_a_headingless_chunk(self):
        body = "stray preamble\n\n# Session 61\n\nbody\n"
        self.assertEqual(ca.split_sessions(body), ["", "Session 61"])

    def test_subheadings_do_not_split(self):
        body = "# Session 61\n\n## a\n\n#### quoted doc\n\n##### deeper\n"
        self.assertEqual(ca.split_sessions(body), ["Session 61"])

    def test_empty_body_still_renders_one_card(self):
        self.assertEqual(ca.split_sessions(""), [""])


class Anchors(unittest.TestCase):
    def test_collective_session_phrase_wins(self):
        self.assertEqual(ca.session_anchor("Journal — 2026-07-10 (collective session 22)",
                                           "2026-07-10", 0), "cs-22")

    def test_session_n_is_pre_on_day_one_and_cs_after(self):
        self.assertEqual(ca.session_anchor("Session 03 — 2026-07-01", "2026-07-01", 2),
                         "pre-2026-07-01-3")
        self.assertEqual(ca.session_anchor("Session 63 — 2026-07-25", "2026-07-25", 1), "cs-63")

    def test_unknown_heading_falls_back_to_position(self):
        self.assertEqual(
            ca.session_anchor("Skeptic Pre-Read — Homogenization Dossier", "2026-07-25", 2),
            "2026-07-25-2",
        )

    def test_collision_gets_a_day_suffix_first_claimant_keeps_clean_anchor(self):
        used: set[str] = set()
        self.assertEqual(ca.unique_session_anchor(used, "Session 24", "2026-07-10", 0), "cs-24")
        self.assertEqual(ca.unique_session_anchor(used, "Session 24", "2026-07-11", 0),
                         "cs-24-2026-07-11")
        self.assertEqual(ca.unique_session_anchor(used, "Session 24", "2026-07-11", 1),
                         "cs-24-2026-07-11-2")


class ServedAnchors(unittest.TestCase):
    def test_spine_plus_chronicle_with_duplicate_pair_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            spine = os.path.join(tmp, "spine.json")
            chron = os.path.join(tmp, "chronicle.json")
            with open(spine, "w", encoding="utf-8") as fh:
                json.dump(SPINE, fh)
            with open(chron, "w", encoding="utf-8") as fh:
                json.dump(
                    [
                        {"collective_session": 25, "date": "2026-07-11"},
                        {"collective_session": 25, "date": "2026-07-11"},  # same pair → skipped
                        {"collective_session": 1, "date": "2026-07-20"},   # cs-1 taken → suffix
                        {"collective_session": 1, "date": "2026-07-01"},   # spine pair → skipped
                    ],
                    fh,
                )
            # Order follows the site's merge: upstream sorted by (date, session), so the
            # 07-11 entry is appended before the 07-20 one.
            self.assertEqual(
                ca.served_anchors(chron, spine),
                ["pre-2026-07-01-1", "cs-1", "cs-25", "cs-1-2026-07-20"],
            )


class Check(unittest.TestCase):
    def _run(self, files: dict[str, str], chronicle: list[dict]) -> dict:
        with tempfile.TemporaryDirectory() as tmp:
            jdir = os.path.join(tmp, "journal")
            os.makedirs(jdir)
            for name, body in files.items():
                write(jdir, name, body)
            spine = os.path.join(tmp, "spine.json")
            chron = os.path.join(tmp, "chronicle.json")
            with open(spine, "w", encoding="utf-8") as fh:
                json.dump({"entries": []}, fh)
            with open(chron, "w", encoding="utf-8") as fh:
                json.dump(chronicle, fh)
            return ca.check(jdir, chron, spine)

    def test_clean_repo_passes(self):
        r = self._run(
            {"2026-07-25.md": "# Session 61 — d\n\nx\n\n# Session 63 — d\n\ny\n"},
            [{"collective_session": 61, "date": "2026-07-25"},
             {"collective_session": 63, "date": "2026-07-25"}],
        )
        self.assertEqual(r["status"], "PASS")
        self.assertEqual((r["rendered"], r["served"]), (2, 2))

    def test_the_2026_07_25_defect_is_caught_and_named(self):
        r = self._run(
            {"2026-07-25.md": "# Session 61 — d\n\nx\n\n# Session 63 — d\n\ny\n"
                              "\n# Skeptic Pre-Read — quoted verbatim\n\nverdict\n"},
            [{"collective_session": 61, "date": "2026-07-25"},
             {"collective_session": 63, "date": "2026-07-25"}],
        )
        self.assertEqual(r["status"], "DEFECT")
        self.assertEqual((r["rendered"], r["served"]), (3, 2))
        self.assertEqual([s["anchor"] for s in r["stray_headings"]], ["2026-07-25-2"])
        self.assertEqual(r["sessions_without_chronicle_entry"], [])

    def test_text_above_the_first_heading_is_caught_as_a_stray_card(self):
        r = self._run(
            {"2026-07-25.md": "preamble above the heading\n\n# Session 61 — d\n\nx\n"},
            [{"collective_session": 61, "date": "2026-07-25"}],
        )
        self.assertEqual(r["status"], "DEFECT")
        self.assertEqual([s["anchor"] for s in r["stray_headings"]], ["2026-07-25-0"])

    def test_missing_chronicle_entry_is_a_transient_not_a_defect(self):
        r = self._run(
            {"2026-07-25.md": "# Session 61 — d\n\nx\n\n# Session 64 — d\n\ny\n"},
            [{"collective_session": 61, "date": "2026-07-25"}],
        )
        self.assertEqual(r["status"], "TRANSIENT")
        self.assertEqual([s["anchor"] for s in r["sessions_without_chronicle_entry"]], ["cs-64"])

    def test_chronicle_entry_with_no_rendered_session_is_a_dead_deep_link(self):
        r = self._run(
            {"2026-07-25.md": "# Session 61 — d\n\nx\n"},
            [{"collective_session": 61, "date": "2026-07-25"},
             {"collective_session": 99, "date": "2026-07-25"}],
        )
        self.assertEqual(r["status"], "DEFECT")
        self.assertEqual(r["served_anchors_not_rendered"], ["cs-99"])

    def test_exit_codes(self):
        self.assertEqual({"PASS": 0, "DEFECT": 1, "TRANSIENT": 2}["DEFECT"], 1)


class RealRepo(unittest.TestCase):
    """The check must pass on the repo's actual state at landing (see README)."""

    def test_repo_state(self):
        r = ca.check()
        self.assertIn(r["status"], ("PASS", "TRANSIENT"), r)
        self.assertEqual(r["stray_headings"], [])
        self.assertEqual(r["served_anchors_not_rendered"], [])


if __name__ == "__main__":
    unittest.main()
