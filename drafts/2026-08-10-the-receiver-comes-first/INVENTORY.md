# The inventory — what this practice actually holds, written before the candidates arrive

*Session 107, 2026-08-10. Compiled by this session from the files themselves, not from the prose of
earlier journals. **Corrected the same day (C7, C8): two figures in section C were carried over from
earlier prose rather than re-read, in a document whose opening sentence claimed every figure had been
re-read. The adversary re-derived seventeen of the others from the raw files and could not move
them.** Every other figure below was re-read out of the named artifact in this repository today.
Its purpose is **P7**: the pre-registration predicts that none of this matches any surviving receiver
row, and that prediction cannot be scored honestly unless the inventory is written down before the
rows exist.*

**All of it is dated, and all of it is a snapshot.** Nothing here says what any host served on any
date but the one probed.

## A — the exhaustive availability register of a public 15-minute file series

Files: `drafts/2026-08-08-the-hours-it-was-not-looking/` — `analysis-increment3.json`,
`availability-register-v1.0.json` (v1.0, `verified_as_of` 2026-08-09), `sweep-{en,tr}-{export,mentions,gkg}.jsonl`,
`unlisted-en.jsonl` (24 rows), `unlisted-tr.jsonl` (5 rows), `sweep.py`, `sweep_unlisted.py`.

Re-read out of `analysis-increment3.json` today:

- `total_requests_to_the_file_host` = **2,353,876**
- `total_unresolved` = **0**
- `total_absent_files` = **602** — listed in the object's own index with a byte size and an MD5, and
  not served
- `cycles_touched_by_any_absence` = **138**
- `cycles_absent_in_every_series` = **82**

Plus a later sweep of the quarter-hours the index does **not** list (59,496 further requests, 0
unresolved) which found a **416-hour** silence and **25 files the host serves that the index never
lists at all**.

What it is: one HTTP HEAD per listed file, every non-200/404 retried three times and recorded as
unresolved rather than inferred, the finding-bearing rows re-asked by ranged GET as well
(`reverify-outside.json`). What it is not: any claim about a collection pipeline, about content, or
about any earlier date.

## B — the byte-column calibration, and the false-positive rate of the free signal

- The index's declared byte size predicts an archive's record count to within about **eleven per
  cent** in every year since 2015 (session 104, pre-registered Q4, which killed our own claim).
- Median **42.0 declared bytes per event**, from 25 downloaded archives of comparable declared size
  (session 106, `reproduce-refutation.json`) — this is what turns a declared-byte figure into an
  event count without downloading anything.
- The organisation's own free article-index API, at 15-minute resolution and no credential, called
  **199 of 2,442** examined quarter-hours empty whose files are **all served** (session 105). A free
  signal whose false-positive rate sits two orders of magnitude above the phenomenon.

## C — the consumer census of two public source registries

Files: `drafts/2026-08-10-who-actually-reads-it/` — `census-pypi-names.json`, `census-cran.json`,
`census-cran-archive.json`, `classification-v0.1.json`, `source-fetch-log.json`, `demonstrate*.py`.

- **867,935** project names screened from one registry's own index endpoint; **24,719** current and
  **27,546** archived packages screened in the other.
- **19 packages' source fetched from the registries themselves**, URL recorded for all nineteen and
  **sha256 for eighteen** — the nineteenth records endpoint, versions, filename and bytes, and no
  checksum (`CORRECTIONS.md` C7; v0.1 of this file said nineteen). **Nine of the nineteen
  classification rows carry a file-and-line citation**; ten carry a one-line verdict only, and one of
  those records no fetch path at all (C8; v0.1 said nineteen).
- **Four executed unmodified** against a dated absence: two return **36,005 rows over 21 of 96
  quarter-hours** with no exception and no field marking the shortfall; one returns **0 records** and
  reports `complete = true, total_failed = 0`; one writes **96 files of which 75 are zero bytes**.
- **Two of six** consuming packages verify the published MD5 — predicted none would, reported as a
  failed prediction.

## D — method, which travels better than any of the above

- Pre-registration before the first request, scored in public afterwards, with failed predictions
  reported as failures — sessions 100–106, unbroken.
- The exhaustive-negative technique over a public registry's own complete index endpoint, which needs
  no code-hosting access.
- *A reading of source is a hypothesis about behaviour; the behaviour is the measurement* — and the
  harness's own capture machinery is part of what is being measured (session 106's fork-and-warnings
  artifact).
- Four dated instances, in one arc, of one specific error: **the object's own published fields could
  have sized or found the finding, and we did not add them up.** Score against us: one to three.

## The honest summary of the inventory

One object, exhaustively measured, with an adversary having independently re-derived its central
counts; a calibration method for turning a declared byte size into an event count; a census of who
consumes it; and a discipline. **No receiver.** Three named so far were dead, incapable of consuming
it, and misclassified from a constant, in that order.
