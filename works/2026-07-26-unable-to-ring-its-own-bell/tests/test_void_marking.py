"""tests/test_void_marking.py — the correction, made re-runnable.

WHY THIS EXISTS (2026-08-04, session 87)
----------------------------------------
This work's decisional verdict, `NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT`, was
voided as evidence at publication by this work's own pre-registered power check
(PREREGISTRATION.md §9.4), and the voiding is registered in `memory/discarded.md`
at the repository root. Until 2026-08-04 the voiding was stated in this work's
prose and in nothing a machine reads: the string stood, unmarked, fifty times
across the published data files, the page source, a script and a test. Anyone who
parsed `data.json` — which is the form in which this practice asks to be
replicated and disputed — met a verdict field whose own author had withdrawn it,
with nothing in the file they were reading to say so.

The repair added the notice at the one place the verdict string is produced
(`scripts/envelope_units.py`) so every downstream file inherits it. This file is
what stops the repair from decaying: it asserts, over the *published* files rather
than over fixtures, that the verdict and the notice never travel apart.

It is deliberately a test and not a checklist. A note in a corrections file
records that something was fixed; a test fails when it is unfixed again.

WHAT IT DOES NOT DO — written down because two reviewers had to find these
------------------------------------------------------------------------
1. **Nothing runs it automatically.** No hook, no gate, and no orientation ritual
   in this repository runs any `works/*/tests/` suite. This guard fires only when
   a human or a session runs it by hand. That is the same limit two earlier
   guards in this repository carry (`tools/chronicle_check.py`,
   `tools/requests_room_check.py`) and it was not written down until the session
   87 Interlocutor pointed out that it hadn't been.
2. **It is stricter on data than on prose.** For the three JSON files it checks
   that the notice sits *beside* the verdict (sibling key), and for the summary
   dump that it sits within four lines. For `work.astro`, `envelope_units.py`,
   `test_classification_ladder.py` and this file it checks only that the voiding
   is stated *somewhere* in the file. The pinned occurrence counts stop a new
   unmarked occurrence appearing unnoticed, but proximity is not enforced there.
3. **`verdict_status` is a sibling key, not a wrapper.** A reuser who selects the
   `verdict` field alone still receives the bare withdrawn wording. That is
   deliberate — the withdrawn wording must stay retrievable verbatim, because the
   repository's withdrawal register is matched against it — and it is the reason
   the notice is also at the head of every file. It is a real gap and it is
   stated on the work's face rather than closed.
4. **It checks the files this work publishes.** It cannot check a copy of
   `data.json` someone has already taken, or a third party's prose quoting the
   verdict. The marking is an offer to a future reader of this directory, not a
   recall.
"""
import json
import os
import pathlib
import unittest

import _pathfix  # noqa: F401
import envelope_units as eu

WORK_DIR = pathlib.Path(__file__).resolve().parent.parent
VERDICT = eu.VERDICT_NO_SIGNAL
NOTICE = eu.VERDICT_VOID_NOTICE

# Every published file in which the voided verdict string occurs, and how it is
# marked there. Counts are asserted so that a file gaining new occurrences fails
# this test rather than passing it silently.
JSON_FILES = {
    "data.json": 18,
    "results/envelope.json": 6,
    "results/sensitivity.json": 16,
}
TEXT_FILES = {
    "results/summary.md": 6,
    "work.astro": 2,
    "scripts/envelope_units.py": 1,
    "tests/test_classification_ladder.py": 1,
    # This file quotes the verdict once, in its own docstring. It is counted
    # here rather than exempted: a guard that excuses itself from its own rule
    # is the shape of the defect it was written to catch.
    "tests/test_void_marking.py": 1,
}


def _verdict_objects(node, path=""):
    """Every dict in the tree that carries the voided verdict as its `verdict`."""
    found = []
    if isinstance(node, dict):
        if node.get("verdict") == VERDICT:
            found.append((path, node))
        for k, v in node.items():
            found += _verdict_objects(v, f"{path}/{k}")
    elif isinstance(node, list):
        for i, v in enumerate(node):
            found += _verdict_objects(v, f"{path}[{i}]")
    return found


class TestTheNoticeIsSayingWhatItShould(unittest.TestCase):
    def test_notice_names_the_status_the_repository_register_uses(self):
        self.assertIn("VOID AS EVIDENCE", NOTICE)
        self.assertIn("memory/discarded.md", NOTICE)
        self.assertIn("CORRECTIONS.md", NOTICE)
        self.assertIn("2026-08-04", NOTICE)

    def test_the_notice_does_not_restate_the_verdict(self):
        # A marking that repeats the withdrawn wording adds an occurrence of the
        # very string it is marking. It must not.
        self.assertNotIn(VERDICT, NOTICE)


class TestEveryVerdictInThePublishedJsonCarriesTheNotice(unittest.TestCase):
    def test_each_file_carries_a_file_level_notice(self):
        for rel in JSON_FILES:
            with self.subTest(file=rel):
                data = json.loads((WORK_DIR / rel).read_text(encoding="utf-8"))
                self.assertEqual(data.get("_void_notice"), NOTICE)

    def test_each_verdict_object_carries_the_notice_beside_it(self):
        for rel, expected in JSON_FILES.items():
            with self.subTest(file=rel):
                data = json.loads((WORK_DIR / rel).read_text(encoding="utf-8"))
                objs = _verdict_objects(data)
                self.assertEqual(
                    len(objs), expected,
                    f"{rel}: expected {expected} verdict objects, found {len(objs)} — "
                    "if the file legitimately changed, change the count here deliberately",
                )
                unmarked = [p for p, o in objs if o.get("verdict_status") != NOTICE]
                self.assertEqual(unmarked, [], f"{rel}: verdict without the notice at {unmarked}")


class TestEveryOccurrenceInTheTextFilesIsAccountedFor(unittest.TestCase):
    def test_occurrence_counts_are_the_ones_the_correction_entry_states(self):
        for rel, expected in TEXT_FILES.items():
            with self.subTest(file=rel):
                text = (WORK_DIR / rel).read_text(encoding="utf-8")
                self.assertEqual(
                    text.count(VERDICT), expected,
                    f"{rel}: expected {expected} occurrences of the voided verdict, "
                    f"found {text.count(VERDICT)}",
                )

    def test_each_text_file_states_the_voiding_somewhere_in_itself(self):
        for rel in TEXT_FILES:
            with self.subTest(file=rel):
                text = (WORK_DIR / rel).read_text(encoding="utf-8")
                self.assertTrue(
                    "VOID AS EVIDENCE" in text or "VOIDED AS EVIDENCE" in text
                    or "void as evidence" in text,
                    f"{rel}: carries the voided verdict and says nothing about the voiding",
                )

    def test_in_the_summary_dump_the_notice_follows_every_verdict_line(self):
        # The dump is 2,000+ lines. A notice only at the top is not enough: a
        # reader who lands on the branch verdict at line 1780 must meet it there.
        lines = (WORK_DIR / "results/summary.md").read_text(encoding="utf-8").splitlines()
        verdict_lines = [i for i, l in enumerate(lines) if l == f"verdict text: {VERDICT}"]
        self.assertEqual(len(verdict_lines), TEXT_FILES["results/summary.md"])
        for i in verdict_lines:
            window = "\n".join(lines[i:i + 4])
            self.assertIn("VOID AS EVIDENCE", window, f"summary.md line {i + 1}: unmarked verdict")


class TestNoOtherPublishedFileCarriesItUnmarked(unittest.TestCase):
    """The counts above are a closed list. This test proves the list is closed."""

    SKIP_DIRS = {".git", "__pycache__"}
    # Prose documents whose occurrence is the correction record itself, or the
    # work's own description. Each must state the voiding in its own text, and
    # the test below asserts that rather than taking it on trust — the session 87
    # Verifier found that the entry claiming it had never been checked, and that
    # one of the four did not in fact do it.
    STATES_THE_VOIDING = {
        "CORRECTIONS.md", "README.md", "meta.json", "PREREGISTRATION.md",
        # The 2026-08-04 gauntlet's own reports, published unedited. They quote
        # the verdict because they are checking the marking of it, and each says
        # so in its own text. They are counted, not exempted, for the same reason
        # the guard counts its own docstring.
        "VERIFICATION-2026-08-04.md", "SKEPTIC-2026-08-04.md",
    }
    ALLOWED_ELSEWHERE = STATES_THE_VOIDING

    def test_every_occurrence_in_the_work_is_in_one_of_the_two_tables(self):
        known = set(JSON_FILES) | set(TEXT_FILES) | self.ALLOWED_ELSEWHERE
        stray = []
        for root, dirs, files in os.walk(WORK_DIR):
            dirs[:] = [d for d in dirs if d not in self.SKIP_DIRS]
            for name in files:
                path = pathlib.Path(root) / name
                rel = str(path.relative_to(WORK_DIR))
                if rel in known or path.name in known:
                    continue
                try:
                    text = path.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                if VERDICT in text:
                    stray.append(rel)
        self.assertEqual(stray, [], f"unaccounted occurrences of the voided verdict: {stray}")

    def test_each_exempted_prose_document_really_does_state_the_voiding(self):
        """The exemption is only legitimate if the file marks the occurrence itself.

        Added 2026-08-04 after the Verifier established that the correction entry
        asserted this of four files and it was true of only three.
        """
        for name in self.STATES_THE_VOIDING:
            with self.subTest(file=name):
                text = (WORK_DIR / name).read_text(encoding="utf-8")
                self.assertIn(VERDICT, text, f"{name}: no longer carries the verdict at all")
                self.assertRegex(
                    text, r"[Vv]oid(ed|s|ing)?\b",
                    f"{name}: carries the voided verdict and never says it was voided",
                )


if __name__ == "__main__":
    unittest.main()
