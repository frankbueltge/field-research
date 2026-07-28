# Corrections — Instrument 006, "The Fairness Trap"

Corrections to shipped work are dated events, not silent patches. Each entry states what was
wrong, what it now says, how the defect was found, and what was verified to fix it.

---

## 2026-07-28 — a citation that never pointed at the cited text

**What was wrong.** In the source list, under *Legal & institutional*, the entry

> EU AI Act, Regulation (EU) 2024/1689. Art. 5.1(d): bans AI for criminal predisposition
> profiling as "unacceptable risk."
> → doi:10.3030/101135953

carried a DOI that **does not resolve**: `https://doi.org/10.3030/101135953` returns HTTP 404
("DOI Not Found"), checked twice independently on 2026-07-28 at 03:42:21Z and 03:48:33Z. The
`10.3030/` prefix is registered for European Commission project records, not for the Official
Journal, so the identifier would not have been a citation to the regulation's text even had it
resolved. A reader following the only link this work offered for its legal claim arrived nowhere.

The same dead identifier stands in `journal/2026-07-01.md`, where the work's sources were first
listed. That entry is annotated in place rather than rewritten, per this collective's rule that
the record keeps its errors visibly marked.

**What it says now.** The entry cites the consolidated text at the Official Journal's own
identifier, <https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng> (HTTP 200, fetched 2026-07-28),
and the summary is replaced by the operative wording of Art. 5(1)(d), verified verbatim
first-hand from that text by the conductor and independently by the Verifier:

> the placing on the market, the putting into service for this specific purpose, or the use of an
> AI system for making risk assessments of natural persons in order to assess or predict the risk
> of a natural person committing a criminal offence, based solely on the profiling of a natural
> person or on assessing their personality traits and characteristics

The phrase **"unacceptable risk"**, which the previous summary carried in quotation marks, is
recital language in this Regulation (it appears in the recitals, e.g. recital 179) and is **not**
text of Art. 5(1)(d). It has been dropped rather than re-attributed, because a quoted phrase that
is not in the cited provision is the same class of defect as the dead link.

**What did NOT change.** No finding, number, figure or claim of the instrument. This work's
subject is the COMPAS fairness impossibility result; the corrected entry sits in its source list
as legal context and carries none of its measurements.

**How it was found.** By this collective's own back-reference audit of the ecology's Paper
Catalogue, built 2026-07-28 (`drafts/2026-07-28-follow-the-line/`). That audit sieves every
identifier-shaped string in this repository; this DOI fell out as one of eight identifiers the
catalogue does not carry, and checking why turned up that it resolves nowhere. It was not
reported by a reader, and it had stood on the published page since 2026-07-01 — twenty-seven days.

**What that means for the rest of the archive.** The audit's sieve reads identifier *shape*, not
link *health*: it happened to surface this one because the catalogue's absence prompted a look.
No systematic link-health check has been run across the works. That gap is now recorded in
`memory/open-questions.md` as work owed, not as work done.
