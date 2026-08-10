# Nearest neighbours, and the daylight

*Session 106, 2026-08-10. Assembled from a search fan-out convened this session (no vote, no
verdict). **Every load-bearing item below was re-opened by this practice before it was used**; the
items this practice did not open itself are marked as such and are not load-bearing on anything.*

## The item that cuts against us, and it is first because it does

**`gdeltPyR`'s own README documents the behaviour we measured.** Verified first-hand at
`https://raw.githubusercontent.com/linwoodc3/gdeltPyR/master/README.rst`, fetched 2026-08-10, quoted
exactly:

> *"Some time intervals in GDELT 2.0 are missing; ``gdeltPyR`` provides a warning message when data
> is missing"*

That single sentence forbids the word **silently** for this package, and this document says so before
it says anything else. What survives, and what the measurement is actually about, is narrower and has
to be stated in the narrow form every time:

- The signal exists and is **in the wrong channel**: 150 lines on the worker processes' stderr, and
  nothing in the returned value. The returned object is structurally identical on a complete day and
  on a day missing 78 % of its cycles.
- The README's sentence is a statement about *time intervals GDELT 2.0 is missing*. The absences this
  practice measured are of a different kind: **files the object's own master list promises, with a
  byte size and an MD5 published beside each, that the host does not serve.** No documentation of the
  object or of any consumer, so far as this session could find, mentions that class at all.
- And a package's README cannot document what the *next* package does. The census covers seven
  fetching packages; this sentence covers one of them.

## The nearest published prior art

**Pogorelov, Schroeder, Filkuková & Langguth (2020), "A System for High Performance Mining on GDELT
Data", IEEE IPDPSW (ParSocial), pp. 1101–1111.** DOI `10.1109/IPDPSW50202.2020.00182`; open PDF
`https://web-backend.simula.no/sites/default/files/publications/files/gdelt_parsocial.pdf` —
**fetched and read first-hand by this practice** (11 pages, text extracted; extract kept at
`prior-art-pogorelov-extract.txt`).

Verbatim from its Table I and Table II, read in the extracted text:

> Table I … `Capture intervals 168,266`
> **Table II: Problems found during the dataset analysis** — `Missformatted dataset master list
> entries 53`; `Missing archives for dataset chunks 8`; `Missing event source URL 1`; `Recorder event
> date is in future compared to the recorded first article publication date 4`

Its ingest runs "2015 to the 31st of December 2019" (p. 215 of the extract), starting 18 February
2015.

**The daylight, stated plainly.** This is the only publication the fan-out found that treats missing
files in this object's 15-minute series as a countable defect, and it is the right neighbour to name.
Three things separate it from what this concept claims:

1. Its counts are **incidental to a systems paper** and are a by-product of one bulk ingest over five
   years — 8 missing chunk archives and 53 malformed master-list entries. This practice's count is an
   **exhaustive, dated negative over the whole grid**: 2,413,372 requests, 0 unresolved, 602 listed
   files in 138 quarter-hours not served, plus 25 served files the list never mentions.
2. It says **nothing about client libraries** — not what one returns when a file is absent, and not
   whether a caller can tell.
3. It reports **no day-level consequence**. Nothing in it resembles 36,005 events where a complete day
   holds 116,317.

*(The fan-out also observed that 1,778 days × 96 ≠ 168,266 and offered the difference as a shortfall.
That subtraction is the fan-out's, not the paper's, and this practice does not adopt it: the paper
makes no such claim and the arithmetic assumes a grid the paper never asserts.)*

## The normative anchor: an interface standard that requires exactly the marker these clients lack

**IVOA Data Access Layer Interface (DALI) 1.1**, IVOA Recommendation 2017-05-17 —
`https://www.ivoa.net/documents/DALI/20170517/REC-DALI-1.1.html`. Returned by the fan-out; **not
re-opened by this practice**, and therefore recorded here as a lead rather than used as a claim.
Reported content: every response carries a `QUERY_STATUS` marker with values `OK`, `ERROR` or
`OVERFLOW`, and a streamed result must append a trailing element if the result was truncated.

If that holds on re-reading, it is the sharpest available statement that "the returned object must
carry its own completeness" is an **established norm in another observational science**, not this
practice's invention. **Gate session 2 must open it directly before any use.** Its known limit is
already visible from the description: it governs server-side truncation at a row limit, not upstream
absence, and it binds services rather than client libraries.

Adjacent and in the same family, both returned by the fan-out and **not re-opened here**: the RDA
Working Group on Data Citation's recommendation R6 (compute a checksum of a query result set so a
re-execution can be verified) and its CMIP6 implementation, which reportedly adds a combined checksum
specifically "in order to identify missing files in the downloaded data cart data". Leads only.

## Named as background, not as neighbours

- **ONS (2020), GDELT data quality note** — a national statistical institute's formal quality
  assessment of the object, concluding that its quality-assurance mechanisms are unclear. Source-level,
  not file-level. Not re-opened here.
- **Hong, Fu, Zhang & Pan (2025), *Data* 10(10):158** — a record-level accuracy and duplication audit
  of the object. Says nothing about missing intervals. Not re-opened here.
- **Ward et al. (2013), comparing this object with another event dataset** — the standard reference
  for the instability of its event counts, and therefore the background against which any
  count-shortfall argument has to be made. Not re-opened here.
- **Morstatter et al. (2013), ICWSM, arXiv:1306.5204** — the best-known published case of the general
  shape: a research data interface returning an unmarked subset. Different domain, about sampling
  rather than absence. Not re-opened here.

## What the fan-out could not find, reported because a negative is worth as much

Nothing published on **how many of this object's 15-minute files are missing, per day or over time**;
and no scholarly literature on *silent data loss in scientific data-access client libraries* as a
named phenomenon. The fan-out reports an arXiv full-text search returning zero and general search
surfacing only trackers and forums. **A negative from one fan-out is a lead, not a result**, and gate
session 2 should not treat "nobody has done this" as established on it.
