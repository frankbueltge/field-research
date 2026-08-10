# Corrections — "Who Actually Reads It"

*Dated events, not silent patches (PROTOCOL v3, "Verifiability and legal hygiene", 6). Each entry
states what was believed, what is true, how it was caught, and where the wrong text still stands as
what was believed. Nothing above a correction is deleted.*

## C1 — 2026-08-10, session 106. "Zero warnings" was our harness, not the package. **Withdrawn.**

**Believed and written:** `demonstration-gdeltpyr.json` recorded `warnings_count: 0` for `gdelt`
0.1.14 on the outage day, and this practice was one step from calling the behaviour silent.

**True:** run with no warnings machinery at all, the package writes **150 warning lines to stderr** —
two per absent cycle (`demonstration-default-harness.json`, `demo3-stderr.txt`). The first harness
wrapped the call in `warnings.catch_warnings(record=True)`; the package downloads in forked worker
processes, which inherit the parent's warning recorder, so each child recorded into its own copy and
the parent saw nothing.

**Caught by:** us, same session, before publication, by re-running without the harness.

**Where the wrong figure stands:** `demonstration-gdeltpyr.json` is kept unedited beside the corrected
run, and `RESULT-1.md` reports both.

## C2 — 2026-08-10, session 106. `gdelt-py` was classified from its source as having no incompleteness marker. **Wrong; corrected by execution.**

**Believed and written:** the first pass of `classification-v0.1.json` grouped `gdelt-py` 0.1.11 with
the two packages that carry no field marking incompleteness.

**True:** it carries a result container built for exactly that purpose —
`FetchResult.data / .failed / .complete / .partial / .total_failed` (`py_gdelt/models/common.py`).
Publishing the first reading would have been a false statement about a third party's code.

**And what execution then found, which is sharper than the wrong reading:** on 2022-11-11 the
container reports `complete = true, total_failed = 0` with **0 records**, because for a whole-day
range the package requests **one** cycle per stream, both of which 404, and **neither reaches the
`failed` list** (`demonstration-gdelt-py.json`, `diagnose-gdelt-py.json`).

**Caught by:** us, same session, before publication, by executing the package instead of trusting the
read. Recorded because the arc's standing lesson has been paid for three times in the other direction.

## C3 — 2026-08-10, session 106. The word "silent". **Retired.**

**Believed:** that the behaviour could be described as silent.

**True:** `gdeltPyR`'s own README states *"Some time intervals in GDELT 2.0 are missing; ``gdeltPyR``
provides a warning message when data is missing"* — verified first-hand at
`https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/README.rst`, 2026-08-10. The claim is
retired and replaced by the narrow one this practice can defend: **the signal is in a channel the
returned value does not reach.**

**Caught by:** a search fan-out convened this session, then re-opened and confirmed by us.

## C4 — 2026-08-10, session 106. Guard against an over-read this arc has not yet made.

Stated as a correction in advance, because the sentence is easy to write and would be false: the
control day's 116,317 rows are **not** a counterfactual for 2022-11-11. What that day would have held
is unknowable; the files do not exist to be counted. **No figure of the form "N events were lost" may
appear anywhere in this arc**, and if one does, this entry withdraws it.

---

*The entries below were made after the adversary's verdict (`INTERLOCUTOR-1.md`, **REFUTED**) and
after this practice reproduced its decisive charges with its own code
(`REFUTATION-REPRODUCED.md`). They are dated events of 2026-08-10.*

## C5 — "a researcher receives 31 % of the day's events". **FALSE AS PUBLISHED. Withdrawn.**

**Written, twice in bold**, in `CONCEPT.md` and `RESULT-1.md`: 36,005 events against 116,317.

**True:** 116,317 is a *different day*. The index declares **178,909 bytes** for the 75 absent export
files; 25 calibration files of comparable declared size, downloaded and counted by us, give a median
of **42.0 declared bytes per event**; so the absent files held on the order of **4,260 events** and
the complete day held roughly **40,000**. The client returns about **89 %** of what the instrument
produced, not 31 %.

**Caught by:** the adversary. Reproduced by us before accepting. **This is the error the session's own
`C4` was written to prevent, four hours earlier, in this same file** — we wrote the guard and then let
the number stand in two documents anyway.

## C6 — "a negative over 2.4 million files that no sampling gets you". **Withdrawn as the justification for this finding.**

**Written** in `CONCEPT.md` as the reason this practice was the one that could find it.

**True:** the demonstration day is the **longest run by a factor of fourteen** in the index's own byte
column and falls out of this practice's own screen, index-only, in **8.94 seconds** on our run
(`reproduce-refutation.json`). The exhaustive sweep is genuinely not free — a naive size threshold does
not reproduce the 602-file register — but **the thing demonstrated needed one day, and that day was
free.** Fourth occurrence of this pattern in this arc.

## C7 — `gdelt-py`'s `C1_reads_master_list: true`. **Corrected to false**, and the D4 narrative withdrawn.

`get_master_file_list` is defined at `sources/files.py:128` and **called from no `.py` file in the
package**. The events path builds names arithmetically. And `RESULT-1.md` D4 claimed only execution
could have caught the earlier misreading; the source states it at `endpoints/events.py:218-219`, in the
maintainer's own comment. We read where the container is defined instead of where it is built. The
self-congratulation is withdrawn.

## C8 — "the reachable client libraries for this infrastructure". **Withdrawn; the population is renamed.**

The census screened the Python and R registries. One request each to two others, made by us after the
verdict: **npm returns nine** name matches, of which `gdelt-toolkit` 0.3.1 reads the master list and
passes its checksum on without verifying anything (`src/lib/get.js:101,106`); **crates.io** carries a
crate of the same name. The population is *"the Python and R registries"*, and the others are named as
out of scope rather than silently absent.

## C9 — "150 warning lines to stderr". **Corrected: 150 warnings across 300 lines.**

`demo3-stderr.txt` is 300 lines carrying 150 `UserWarning` occurrences — Python prints two lines per
warning. Small, and corrected because the document asks to be trusted on numbers.

## C10 — issue #79, "zero comments". **Withdrawn as unverified.**

Our page fetch shows no comments visible; the adversary's API query returned `comments: 2`. Neither of
us read a comment body. What survives is what both attempts support: **no maintainer response is
visible on the rendered page.** The inference "goes unanswered" is reduced accordingly.

## C11 — the graded commit no longer exists in this branch. **A defect of ours, recorded.**

The adversary graded `c18a8bf`. At landing the branch was rewritten back to `8e33d25` and recommitted,
to drop a 57 MB virtual environment this session had committed by mistake three commits earlier. The
graded content is the present state minus the four additions listed as D6 in `RESULT-1.md`; nothing it
graded was revised while it worked. But **a verdict whose commit hash cannot be checked out is a weaker
record than one whose hash can**, and the cause was our own carelessness with a `git add -A`.
