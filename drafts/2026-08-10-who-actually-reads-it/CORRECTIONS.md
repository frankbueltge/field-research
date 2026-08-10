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
