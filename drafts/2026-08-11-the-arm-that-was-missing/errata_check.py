#!/usr/bin/env python3
"""errata_check - a published correction must not come back.

Session 123, 2026-08-16, written after the fourth gauntlet failed.

WHY THIS EXISTS
---------------
On 2026-08-15 the first gauntlet on this arc's receiver bundle published a table of **18 errata**,
each with the false statement and its true value. On 2026-08-16 this practice rebuilt that bundle
from scratch, wrote its prose by hand from the old prose, and shipped **at least six of those
eighteen corrections back into it, unchanged**. Both reviewers found them independently. Every one
of the blocking ones is a sentence containing **no digit**, so the prose auditor this session
built - which extracts digits and compares them to a provenance table - could not have caught a
single one of them by construction.

`memory/downstream-commitments.md` and this practice's own legal-hygiene rule 6 both say a
correction stays in the record and a discarded claim must never read as live. Nothing enforced it.
This does.

WHAT IT IS
----------
A registry of corrections this practice has published, each as:

  * `false_phrase`   - a regex matching the wording that was found false
  * `true_value`     - what is actually the case, in one sentence
  * `source`         - the dated document that published the correction
  * `corrected_when` - OPTIONAL regex. A correction is often made IN PLACE: the old wording stays
    because the sentence now says what was wrong with it. This names the phrase that must appear
    in the same file for a match to count as corrected rather than as a regression. Without it a
    corrected-in-place sentence would be reported forever, and a check that cries wolf trains its
    readers to ignore it. It is also the obvious way to defeat this check by accident: a file that
    happens to contain the corrected_when phrase for an unrelated reason suppresses the finding
    for that whole file.

and a check that scans a directory for any of those phrases. A hit is a **regression**: a
correction the practice published and then un-published by rewriting around it.

WHAT IT CANNOT DO, STATED PLAINLY
----------------------------------
It matches wording, not meaning. A false claim restated in different words passes it, and a true
claim that happens to quote the old wording - as an erratum document does, on purpose - trips it.
So the errata documents themselves are excluded by path, and that exclusion is the obvious hole:
a bundle file could evade this check by paraphrasing. It catches the failure that actually
happened four times, which is verbatim reproduction of prose that was already corrected, and it
makes no claim beyond that.

The registry is also **incomplete by construction**: it holds the corrections a session took the
trouble to enter. `python3 errata_check.py --coverage` reports how many errata the published
tables contain against how many are registered here, so the gap is visible rather than implied.

Usage:
    python3 errata_check.py deliverable-v0.3          # check a bundle; exit 1 on any regression
    python3 errata_check.py --coverage                # how much of the published errata is covered
"""
import argparse
import json
import os
import re
import sys

# Paths whose whole purpose is to quote the false wording. Excluded, by design and by name.
EXCLUDE_SUBSTRINGS = ("ERRATA-", "GAUNTLET-", "INTERLOCUTOR-", "VERIFIER-", "CONDITIONS-",
                      "discharge-", "errata_check.py")

# The registry. Every entry cites the dated document that published the correction.
#
# SESSION 124 completed it. `CONDITIONS-123.md`, binding item 2: "Register the remaining 43
# published errata, or state a reason for each one left out." Both halves are below: REGISTRY
# holds every correction that can be expressed as WORDING that must not come back, and
# NOT_REGISTERED holds, by id, every one that cannot - each with the reason, because a guard
# whose coverage gap is a silence is a guard that flatters itself. 8 were registered before
# tonight; the coverage report prints the arithmetic.
REGISTRY = [
    {
        "id": "E1/2026-08-15",
        "false_phrase": r"twenty synthetic identifiers[^.]{0,120}same code",
        "true_value": ("nineteen of the twenty returned the refusal code; the twentieth returned "
                       "no code at all - a transport failure, which is the absence of a code, not "
                       "the same one"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E1; re-confirmed session 123 "
                  "(discharge-123b.json)",
        "corrected_when": r"nineteen of the twenty|no code at all",
    },
    {
        "id": "E2/2026-08-15",
        "false_phrase": r"logged in(?:to)? every run file before the first",
        "true_value": ("false for the baseline union, which the bundle lists as one of its source "
                       "runs: its own vantage field says it was carried from the producing runs, "
                       "not logged before a first request"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E2; re-confirmed session 123",
        "corrected_when": r"carried from the producing runs",
    },
    {
        "id": "E3/2026-08-15",
        "false_phrase": r"checked against the endpoint's own returned metadata",
        "true_value": ("no such check exists in this arc: the probe stores no creation time "
                       "returned by the endpoint, so there is nothing to check a decoded age "
                       "against"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E3; re-confirmed session 123",
        "corrected_when": r"no such check exists|not checked against anything",
    },
    {
        "id": "E5/2026-08-15",
        "false_phrase": r"disallows the major public (?:web )?crawlers",
        "true_value": ("the saved robots.txt names 27 user-agent groups: CCBot is disallowed, "
                       "Googlebot appears nowhere in it, and Bingbot is restricted only on one "
                       "path. The true statement is about the crawler whose corpus was checked, "
                       "not about major crawlers generally"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E5",
        "corrected_when": r"27 user-agent groups|appears nowhere|the crawler whose corpus",
    },
    {
        "id": "E7/2026-08-15",
        "false_phrase": r"(?:that are\s*\*{0,2}\s*not\s*\*{0,2}\s*|and not\s+)videos",
        "true_value": ("248 of the 249 display-truncated control identifiers do not resolve; one "
                       "is a real video predating the platform's current identifier scheme"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E7; re-confirmed session 123",
        "corrected_when": r"248 of|one is a real video|is a real video|real video predating",
    },
    {
        "id": "E9/2026-08-15",
        "false_phrase": r"names every source run file with its sha256",
        "true_value": ("the manifest named four runs; the baseline union's own four component "
                       "run files were neither named nor hashed"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E9",
        "corrected_when": r"component run|baseline_union_components",
    },
    {
        "id": "E10/2026-08-15",
        "false_phrase": r"re-?run [`\s]*build_deliverable\.py",
        "true_value": ("the bundle does not ship that script, so the instruction cannot be "
                       "followed from inside the bundle"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E10",
        "corrected_when": r"is not shipped|not part of this bundle|does not ship that script",
    },
    {
        "id": "E11/2026-08-15",
        "false_phrase": r"TEMPLATE\s*[-\u2014]\s*the running session sets this",
        "true_value": ("an unfilled placeholder, not a run identifier; the manifest entry it sits "
                       "in must carry the real run id or say plainly that it is unknown"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E11",
    },
    {
        "id": "E14/2026-08-15",
        "false_phrase": r"same instrument, so your reading and ours are comparable",
        "true_value": ("true of the probe and false of the record: this arc's rows are "
                       "re-requested five times before a transition is written down, and the "
                       "shipped tool's default single pass writes one"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E14; ERRATA-121.md E7 - the same sentence, "
                  "found twice, by two different reviewers a day apart",
        "corrected_when": r"not the same instrument|are not the same instrument",
    },
    {
        "id": "E15/2026-08-15",
        "false_phrase": r"point it at any list",
        "true_value": ("the tool coerced junk into identifiers and measured it - a date became a "
                       "year, a headline became a year, a foreign video URL became a single "
                       "digit. Repaired in v0.2.1; the unqualified invitation is still false of "
                       "any version, because a list it refuses is a list it cannot be pointed at"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E15",
        "corrected_when": r"refuses|rejects lines it cannot",
    },
    {
        "id": "E17/2026-08-15",
        "false_phrase": r"0\.14 (?:percentage points|pp)",
        "true_value": ("the raw across-day spread must travel with the balanced-panel spread "
                       "computed ON THE SAME PANEL; the excess is which units fell out as "
                       "INDETERMINATE, not anything about the platform"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E17; re-confirmed session 123",
        # Session 124: this used to name the VALUE (0.0577) as the evidence that the correction
        # was present. On the six-day panel the balanced spread is a different number, and a
        # `corrected_when` pinned to one panel's value would have reported a correctly corrected
        # page as a regression forever. What makes the correction present is the balanced panel
        # being STATED beside the raw figure, not any particular value of it.
        "corrected_when": r"balanced[-\s]*\n?panel",
    },
    {
        "id": "E18/2026-08-15",
        "false_phrase": r"(?:retrievability|it) falls with the age of the video",
        "true_value": ("a single cross-section cannot separate age from creation cohort; on the "
                       "forum arm, holding first-citation year fixed reverses the sign "
                       "(underpowered, p = 0.69)"),
        "source": "deliverable/GAUNTLET-2026-08-15.md, E18",
        "corrected_when": r"cannot separate age from|creation cohort",
    },
    {
        "id": "V3-E4/2026-08-15",
        # `21+` reads "at least 21" and is true of 37, so it is not the false claim; the false
        # claim is a bare 21 asserted as the count. The `(?!\+)` is the whole difference and it
        # was added after this check reported a true sentence as a regression.
        "false_phrase": r"\b21\b(?!\+)[^|\n]{0,60}language editions",
        "true_value": ("37 encyclopedia language editions contribute at least one article-arm unit "
                       "to this panel, re-derived independently three times"),
        "source": "CONDITIONS-120.md V3 (ACCEPTED, CARRIED); re-derived session 123 "
                  "(discharge-123.json); computed at build time since session 124",
        "corrected_when": r"\b37\b",
    },
    # ---- session 121 -------------------------------------------------------------------
    {
        "id": "121-E1/2026-08-15",
        "false_phrase": r"20:29 UTC|14\s*h\s*58\s*m",
        "true_value": ("there was no run at 20:29 UTC. The only run started 20:00:33Z and "
                       "finished 20:00:44Z; the gap from the day-5 run's close is 14 h 29 m 17 s"),
        "source": "ERRATA-121.md, E1",
        "corrected_when": r"20:00:33|14 h 29 m",
    },
    {
        "id": "121-E2/2026-08-15",
        "false_phrase": r"0\.7 s against 10\.7 s",
        "true_value": ("three variables differed between those two runs. Measured directly, the "
                       "geolocation call costs 0.451 s; presenting ~10 s as its cost overstates "
                       "it more than twentyfold. What is true is that --vantage none makes no "
                       "call at all - a disclosure property, not a speed property"),
        "source": "ERRATA-121.md, E2",
        "corrected_when": r"0\.451|makes no call at all",
    },
    {
        "id": "121-E3/2026-08-15",
        "false_phrase": r"agreed\s*=\s*all\(s\s*==\s*first_pass_state",
        "true_value": ("that line treated a confirmation pass that TIMED OUT exactly like one "
                       "that came back with the opposite state, discarding roughly one genuinely "
                       "absent unit in seventeen. Repaired in v0.2.1: only a reversing pass "
                       "refutes; an all-noise burst reports INDETERMINATE"),
        "source": "ERRATA-121.md, E3",
    },
    {
        "id": "121-E5/2026-08-15",
        "false_phrase": r"a short link or a link from another platform",
        "true_value": ("that reason was false on both counts for `m.tiktok.com/v/<id>.html`: same "
                       "platform, and the identifier is a plain substring, not a redirect target. "
                       "The refusal now names the real reason - an unresolved vm./vt. link, which "
                       "this tool does not follow"),
        "source": "ERRATA-121.md, E5",
        "corrected_when": r"unresolved|does not follow redirects",
    },
    # ---- session 122 -------------------------------------------------------------------
    {
        "id": "122-E1/2026-08-16",
        "false_phrase": r"audited 60 numbers|left 11 unmatched|flagged 13 statements",
        "true_value": ("65 numbers audited, 16 not found in any JSON of the draft, 15 claims "
                       "flagged. The published figures came from a run that predated the "
                       "paragraph certifying them"),
        "source": "ERRATA-122.md, E1",
        "corrected_when": r"65 numbers|16 not found",
    },
    {
        "id": "122-E2/2026-08-16",
        "false_phrase": r"no file either reviewer read has been rewritten",
        "true_value": ("false as a categorical claim: three files the reviewers demonstrably read "
                       "were rewritten. The true statement is that no DATA ARTIFACT of the bundle "
                       "was rewritten"),
        "source": "ERRATA-122.md, E2",
        "corrected_when": r"no data artifact|no .{0,12}data artifact",
    },
    {
        "id": "122-E3/2026-08-16",
        "false_phrase": r"three days apart",
        "true_value": ("the session-120 errata say 'three days earlier'; 'three days apart' is "
                       "CONDITIONS-120.md's wording. The substance is unaffected - only the "
                       "attribution was wrong"),
        "source": "ERRATA-122.md, E3",
        "corrected_when": r"three days earlier",
    },
    {
        "id": "122-E5/2026-08-16",
        "false_phrase": r"puts BOTH figures in front of the caller|puts both figures in front of "
                        r"the caller",
        "true_value": ("false in two ordinary cases: a list whose identifiers all postdate the "
                       "table fell through to the unlabelled today-aged figure, and a mixed list "
                       "produced two figures over different subsets and called the difference "
                       "drift"),
        "source": "ERRATA-122.md, E5",
        "corrected_when": r"all postdate|different subsets",
    },
    {
        "id": "122-E6/2026-08-16",
        "false_phrase": r"staleness outweighs the worst bookkeeping error",
        "true_value": ("wrong for the one real external list this arc has, in both magnitude and "
                       "sign: the drift there is negative and vanishingly small "
                       "(-0.00032514 pp by our recomputation, -0.0037 pp by the reviewer's)"),
        "source": "ERRATA-122.md, E6",
        "corrected_when": r"negative and vanishingly small|-0\.000325",
    },
    {
        "id": "122-E7/2026-08-16",
        "false_phrase": r"changes no conclusion",
        "true_value": ("narrowed: the by-band across-day spread column DID move (5y+ by +51.5 %), "
                       "by cohort migration under per-day banding. Under per-day banding that "
                       "column is no longer a test-retest measure of the same units, and any "
                       "across-day stability claim from this arc must say which banding it used"),
        "source": "ERRATA-122.md, E7",
        "corrected_when": r"cohort migration|which banding",
    },
    {
        "id": "122-E9/2026-08-16",
        "false_phrase": r"the staleness threshold is the measured one, not a round number",
        "true_value": ("that assertion compares a module constant to a literal and passes "
                       "identically whether the constant was computed or typed; nothing in the "
                       "suite read the measurement"),
        "source": "ERRATA-122.md, E9",
    },
    {
        "id": "I-26day/2026-08-16",
        "false_phrase": r"threshold is measured rather than picked",
        "true_value": ("withdrawn: the crossover is a family running from 1 day to 26 on a "
                       "comparand chosen after the fact, and 26 was its most forgiving member"),
        "source": "INTERLOCUTOR-14.md, session 122; ERRATA-122.md, E4",
    },
    # ---- session 123 -------------------------------------------------------------------
    {
        "id": "123-E1/2026-08-16",
        "false_phrase": r"\*\*WITHHELD\s*[-\u2014]\s*2026-08-15",
        "true_value": ("that banner is true of version 0.1 and was carried verbatim into version "
                       "0.3's directory, where it reads as though it describes this bundle. The "
                       "withheld status of any version belongs in VERSIONS.md"),
        "source": "ERRATA-123.md, E1 (found by us, while the reviewers were reading)",
        "corrected_when": r"transformed|the withheld status of version 0\.1 is in",
    },
    {
        "id": "123-E11/2026-08-16",
        "false_phrase": r"`?LIMITS\.md`?\s*\u00a7\s*8 says why",
        "true_value": ("the cross-reference still resolves to an existing section and lands on a "
                       "different topic; no statistical-power caveat survives anywhere in version "
                       "0.3's LIMITS.md under any number. Cross-references between renumbered "
                       "documents are made by TITLE"),
        "source": "ERRATA-123.md, E11",
        "corrected_when": r"Small lists cannot separate hypotheses",
    },
    {
        "id": "123-E13/2026-08-16",
        "false_phrase": r"/tmp/[A-Za-z0-9_./-]*(?:trial|scratch)",
        "true_value": ("a committed artifact recorded a scratch directory from a trial build as "
                       "its provenance path instead of the bundle's own"),
        "source": "ERRATA-123.md, E13",
    },
    # ---- session 124 -------------------------------------------------------------------
    {
        "id": "124-E19/2026-08-16",
        "false_phrase": r"0\.0577",
        "true_value": ("0.0577 pp is the balanced-panel spread of the FOUR-day panel of version "
                       "0.1 (3,465 units). It was typed into the generator and reprinted beside "
                       "the FIVE-day raw spread in version 0.3, where the true balanced figure is "
                       "0.0584 pp on 3,423 units and the ratio is 2.32x, not 2.35x. The balanced "
                       "spread is now computed on whatever panel the bundle covers"),
        "source": "ERRATA-124.md, E19; routing-equivalence-124.json",
        "corrected_when": r"figures-derived|balanced_panel\.range",
    },
]

# Every published erratum that CANNOT be expressed as wording a bundle must not repeat, with the
# reason. `CONDITIONS-123.md` item 2 asked for exactly this: "or state a reason for each one left
# out." An id here is not unchecked by accident; it is unchecked by a stated argument, and several
# of them name a guard that does cover them.
NOT_REGISTERED = [
    {"id": "E6/2026-08-15",
     "why": "a RELATION between two fields (a declared reference time against the time the age "
            "columns were actually computed), not a form of words. It is checked where a "
            "relation can be checked: build_deliverable.py asserts, unit by unit, that every "
            "banded unit was banded at the time the table declares, and refuses to write the "
            "table otherwise."},
    {"id": "E8/2026-08-15",
     "why": "an OMISSION - two INDETERMINATE counts of different scope printed with nothing "
            "saying so. This check finds wording that is present; it cannot find wording that is "
            "missing. Structurally prevented instead: figures_page.py computes both scopes into "
            "named fields and the page prints them side by side under a heading that says they "
            "are different questions."},
    {"id": "E12/2026-08-15",
     "why": "an OMISSION - the neighbouring paper that narrowed the novelty claim is named "
            "nowhere a receiver reads. Still owed (CONDITIONS-123.md, finding 16), and a "
            "presence check is the wrong instrument for it."},
    {"id": "E13/2026-08-15",
     "why": "REGISTERED FIRST, THEN WITHDRAWN THE SAME SESSION, and the reason is a fact about "
            "this guard rather than an opinion about the erratum. The correction is about the "
            "SCOPE AT WHICH A QUOTATION IS USED, not about a form of words: the same five words "
            "are false as this practice's own description of the phenomenon and correct as an "
            "attributed quotation of the receiver's report. Registered as wording, it fired on "
            "`receiver-eleven.md`, where the phrase appears as *their words for the interface's "
            "behaviour on these videos* - the scoped, attributed use the erratum asks for. That "
            "is the false-positive half of the hole this file's own docstring names, met in "
            "practice on the first night the registry was completed, and a check that reports a "
            "correctly-corrected sentence as a regression trains its readers to ignore it. The "
            "other two halves of the same erratum (a count fused with the dashboard's, and a "
            "statement attributed to the report that the report does not make) are single "
            "occurrences already repaired in LETTER.md and are not recurrences a phrase match "
            "would catch either."},
    {"id": "E16/2026-08-15",
     "why": "an OMISSION - the tool contacted a geolocation service and wrote the caller's own IP "
            "and location into the output with nothing in the bundle saying so. There is no false "
            "sentence to match; what is owed is a disclosure, which LIMITS.md now carries."},
    {"id": "121-E4/2026-08-15",
     "why": "a defect in a REGULAR EXPRESSION (a URL path rule with no host check), not in prose. "
            "The correct guard is the tool's own selftest, which now asserts that a video path on "
            "a foreign host is refused; a phrase match would report the repaired pattern."},
    {"id": "121-E6/2026-08-15",
     "why": "the statement was TRUE. The erratum is that its arithmetic was never shown, so there "
            "is no false wording that could return - only a standard of exposition."},
    {"id": "121-E7/2026-08-15",
     "why": "the same sentence as E14/2026-08-15, which is registered. Two reviewers a day apart "
            "found one sentence; it is one entry."},
    {"id": "121-E8/2026-08-15",
     "why": "a defect in a one-off discharge script (a check that returned empty while the verdict "
            "beside it already read CONFIRMED), corrected before publication. It cannot reappear "
            "in a bundle, which is what this check scans."},
    {"id": "122-E8/2026-08-16",
     "why": "the statement was TRUE and merely uncited; the correction supplied the basis. There "
            "is no false wording to guard against."},
    {"id": "122-E10/2026-08-16",
     "why": "an OMISSION in a one-off functional-test artifact (it recorded no baseline path). "
            "Not a bundle file and not a form of words."},
    {"id": "123-E2/2026-08-16",
     "why": "an OMISSION - a carried reading that did not name the instrument version that "
            "produced it. Prevented structurally instead: build_v03.py TRANSFORMS that file "
            "rather than carrying it, and records the transformation in the manifest."},
    {"id": "123-E3/2026-08-16",
     "why": "a defect in this practice's own prose auditor - it extracts digits and is blind to "
            "numbers written as words. STILL OPEN. It is not a claim in a bundle and this check "
            "cannot see it either; it is named here so the hole is counted rather than implied."},
    {"id": "123-E12/2026-08-16",
     "why": "a defect in the rebuild audit's classifier (file-wide where it reads as field-wide). "
            "Owed, and not a form of words."},
    {"id": "123-E14/2026-08-16",
     "why": "the same finding as E8/2026-08-15, one gauntlet later. One correction, one reason."},
    {"id": "123-E15/2026-08-16",
     "why": "a circular STATUS POINTER (README pointed at VERSIONS, VERSIONS at README) - a "
            "structural defect with no false sentence. Repaired: both state the verdict outright."},
    {"id": "124-E20/2026-08-16",
     "why": "a defect in the bundle BUILDER (build_deliverable.py discovered two runs of the same "
            "UTC day as two measurement days with one label), not a form of words in any bundle "
            "file. This check scans bundle files; a builder defect is invisible to it. Prevented "
            "structurally instead: the builder now records a `-second-probe` run as a replicate "
            "and refuses any surviving duplicate day-label as a hard error. Reported by the "
            "Verifier of session 124 as unaccounted - correctly, because it was published in "
            "ERRATA-124.md and not brought into this file until the repair; that is the same "
            "reading-your-own-output failure this arc keeps making, caught this time by this "
            "file's own coverage check."},
]


# ---- the accounting, published id by published id ---------------------------------------
# `CONDITIONS-123.md` item 2 asked for the remaining 43 to be registered "or a reason for each
# one left out". That is only answerable if every published id is named, so every one is, and
# the coverage report derives its arithmetic from this table rather than from a count anyone
# typed. A published id maps to a REGISTRY entry, or to a NOT_REGISTERED reason, or the coverage
# report fails - there is no third state and no silent remainder.
COVERS = {
    "deliverable/GAUNTLET-2026-08-15.md": {
        "E1": "E1/2026-08-15", "E2": "E2/2026-08-15", "E3": "E3/2026-08-15",
        "E4": "V3-E4/2026-08-15", "E5": "E5/2026-08-15", "E6": "!E6/2026-08-15",
        "E7": "E7/2026-08-15", "E8": "!E8/2026-08-15", "E9": "E9/2026-08-15",
        "E10": "E10/2026-08-15", "E11": "E11/2026-08-15", "E12": "!E12/2026-08-15",
        "E13": "!E13/2026-08-15", "E14": "E14/2026-08-15", "E15": "E15/2026-08-15",
        "E16": "!E16/2026-08-15", "E17": "E17/2026-08-15", "E18": "E18/2026-08-15",
    },
    "ERRATA-121.md": {
        "E1": "121-E1/2026-08-15", "E2": "121-E2/2026-08-15", "E3": "121-E3/2026-08-15",
        "E4": "!121-E4/2026-08-15", "E5": "121-E5/2026-08-15", "E6": "!121-E6/2026-08-15",
        "E7": "!121-E7/2026-08-15", "E8": "!121-E8/2026-08-15",
    },
    "ERRATA-122.md": {
        "E1": "122-E1/2026-08-16", "E2": "122-E2/2026-08-16", "E3": "122-E3/2026-08-16",
        "E4": "I-26day/2026-08-16", "E5": "122-E5/2026-08-16", "E6": "122-E6/2026-08-16",
        "E7": "122-E7/2026-08-16", "E8": "!122-E8/2026-08-16", "E9": "122-E9/2026-08-16",
        "E10": "!122-E10/2026-08-16",
    },
    "ERRATA-123.md": {
        # E4-E10 are the six corrections version 0.3 shipped back unchanged plus the spread
        # qualification - the SAME corrections the first gauntlet published, found again a day
        # later. They map to the same registry entries; counting them twice would inflate this
        # guard's coverage with its own repetitions.
        "E1": "123-E1/2026-08-16", "E2": "!123-E2/2026-08-16", "E3": "!123-E3/2026-08-16",
        "E4": "E1/2026-08-15", "E5": "E2/2026-08-15", "E6": "E3/2026-08-15",
        "E7": "E7/2026-08-15", "E8": "E11/2026-08-15", "E9": "V3-E4/2026-08-15",
        "E10": "E17/2026-08-15", "E11": "123-E11/2026-08-16", "E12": "!123-E12/2026-08-16",
        "E13": "123-E13/2026-08-16", "E14": "!123-E14/2026-08-16", "E15": "!123-E15/2026-08-16",
    },
    "ERRATA-124.md": {
        "E19": "124-E19/2026-08-16",
        "E20": "!124-E20/2026-08-16",
    },
}


def scan(root):
    hits = []
    files = 0
    for dirpath, _, names in os.walk(root):
        for n in sorted(names):
            p = os.path.join(dirpath, n)
            if any(s in p for s in EXCLUDE_SUBSTRINGS):
                continue
            if not n.endswith((".md", ".json", ".txt", ".csv")):
                continue
            try:
                text = open(p, errors="replace").read()
            except OSError:
                continue
            files += 1
            for e in REGISTRY:
                if e.get("corrected_when") and re.search(e["corrected_when"], text):
                    continue        # corrected in place, in this file
                for m in re.finditer(e["false_phrase"], text):
                    hits.append({
                        "erratum": e["id"],
                        "file": os.path.relpath(p, root),
                        "matched": m.group(0)[:120],
                        "true_value": e["true_value"],
                        "source": e["source"],
                    })
    return files, hits


def coverage():
    """Published erratum by published erratum: registered as wording, or reasoned as unregistrable.

    Session 124 replaced a count with an accounting. The old version counted ids in the published
    tables and compared the total to `len(REGISTRY)`, which said "8 of 51" and could not say WHICH
    43 were missing - and would have kept saying a number even if the registry had drifted onto
    errata nobody published. This walks `COVERS`, checks every target actually exists, and reports
    any published id that maps to nothing as an `unaccounted` entry. An unaccounted id is a defect
    in this file, not a rounding error.
    """
    reg_ids = {e["id"] for e in REGISTRY}
    reason_ids = {e["id"]: e["why"] for e in NOT_REGISTERED}
    published, registered, reasoned, unaccounted, broken = {}, set(), set(), [], []
    for table, ids in COVERS.items():
        found = set()
        if os.path.exists(table):
            text = open(table, errors="replace").read()
            found = set(re.findall(r"^\|\s*(E\d+)\s*\|", text, re.M)) or \
                set(re.findall(r"^#{2,3}\s*(E\d+)\b", text, re.M))
        published[table] = {"ids_declared_here": sorted(ids, key=lambda s: int(s[1:])),
                            "ids_found_in_the_file": sorted(found, key=lambda s: int(s[1:])),
                            "file_present": os.path.exists(table)}
        for pid, target in ids.items():
            key = f"{table}:{pid}"
            if target.startswith("!"):
                if target[1:] in reason_ids:
                    reasoned.add(key)
                else:
                    broken.append({"published": key, "maps_to": target,
                                   "problem": "no NOT_REGISTERED entry with that id"})
            elif target in reg_ids:
                registered.add(key)
            else:
                broken.append({"published": key, "maps_to": target,
                               "problem": "no REGISTRY entry with that id"})
        # An id in the file that this table does not map is the failure mode that matters.
        for f in found - set(ids):
            unaccounted.append(f"{table}:{f}")

    total = len(registered) + len(reasoned)
    return {
        "published_tables": published,
        "n_published_accounted": total,
        "n_registered_as_wording": len(registered),
        "n_reasoned_as_unregistrable": len(reasoned),
        "unaccounted_published_ids": sorted(unaccounted),
        "broken_mappings": broken,
        "registry_entries": len(REGISTRY),
        "reason_entries": len(NOT_REGISTERED),
        "note": ("every published erratum is either a phrase this check will catch coming back, "
                 "or a stated reason why a phrase check is the wrong instrument for it. "
                 "`unaccounted_published_ids` must be empty; if it is not, an erratum was "
                 "published and never brought into this file."),
    }


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("root", nargs="?", default="deliverable-v0.3")
    ap.add_argument("--coverage", action="store_true")
    ap.add_argument("--out", default="errata-check.json")
    a = ap.parse_args(argv)

    if a.coverage:
        print(json.dumps(coverage(), indent=1))
        return 0

    files, hits = scan(a.root)
    report = {"schema": "field-research/errata-regression-check/1",
              "root": a.root, "files_scanned": files,
              "registry_size": len(REGISTRY),
              "coverage": coverage(),
              "n_regressions": len(hits), "regressions": hits}
    json.dump(report, open(a.out, "w"), indent=1)
    for h in hits:
        print(f'REGRESSION {h["erratum"]:16s} {h["file"]:34s} "{h["matched"]}"')
    print(json.dumps({"files_scanned": files, "registry_size": len(REGISTRY),
                      "n_regressions": len(hits)}, indent=1))
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
