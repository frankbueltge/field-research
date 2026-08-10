# Who uses these, as far as public evidence goes

*Session 106, 2026-08-10. Assembled from a search fan-out (no vote, no verdict). The two
load-bearing items were re-opened by this practice; everything else is marked as the fan-out's,
unverified here. `PREREGISTRATION-1.md` names this as the question that decides whether a finding
about these packages matters or is a fact about dead code — and it is a **gate-session-2** question.
This document is evidence for that session, not a verdict by this one.*

## Re-opened first-hand by this practice

**1. Download volume of the most-used affected package.** `https://pypistats.org/api/packages/gdelt/recent`,
fetched 2026-08-10, HTTP 200: `last_day 73, last_week 475, last_month 2132` (mirror-excluded). This
matches the fan-out's figure exactly. The service names no absolute window boundaries, so the figures
are relative to the retrieval date. **The same endpoint returned HTTP 429 for every other package
when this practice re-asked**, so the fan-out's figures for `gdelt-client`, `gdeltdoc`, `gdelt-py`,
`gdelttools` and `gdeltforge` are recorded below as the fan-out's and are **not** re-verified.

**2. An independent, unanswered report of the same symptom, open for two years.**
`https://github.com/linwoodc3/gdeltPyR/issues/79`, read first-hand 2026-08-10. Title *"Not all
available data is downloaded!!!"*, opened by `p-dre` on **3 April 2024**, **open**, **zero comments**.
The reporter receives repeated `GDELT did not return data for date time …` warnings from
`gdelt/parallel.py:111` and states the data is manually downloadable from the source.

**And the distinction this practice must make against its own interest:** the timestamps in that
report are 2021-02-01 cycles. **2021-02-01 is not in `availability-register-v1.0.json`** — those files
are served. So #79 is the *same symptom from a different cause* (a request-time defect; compare the
closed issue #65, where a reporter diagnosed a timezone offset producing URLs an hour ahead). It is
strong evidence that **the failure mode is real, reaches users, and goes unanswered**, and it is
**not** evidence that the object's broken promises reached that user. Anyone reusing this row must
carry that sentence with it.

## The fan-out's figures, not re-verified here (service rate-limited on re-ask)

| package | last month, mirror-excluded | source given |
|---|---|---|
| `gdeltdoc` | 53,610 | `https://pypistats.org/api/packages/gdeltdoc/recent` |
| `gdelt` | 2,132 | re-verified above |
| `gdelt-client` | 208 | `https://pypistats.org/api/packages/gdelt-client/recent` |
| `gdelttools` | 194 | `https://pypistats.org/api/packages/gdelttools/recent` |
| `gdeltforge` | 123 | `https://pypistats.org/api/packages/gdeltforge/recent` |
| `gdelt-py` | 81 | `https://pypistats.org/api/packages/gdelt-py/recent` |

Also reported by the fan-out and not re-verified: a 180-day series (2026-02-10 → 2026-08-09) of
20,756 downloads for `gdelt` and 1,786 for `gdelt-client`; an all-time figure of 217,021 for `gdelt`
from a second service; 254 stars and 62 forks on the source repository; 101 public Python files
matching an import of it in a code search.

**The number that most constrains this concept** is the first row. The client that dominates the
family by download volume — `gdeltdoc`, roughly twenty-five times `gdelt` — **does not consume the
15-minute file series at all**; it reads the article-index API and is outside the measured defect
(`classification-v0.1.json`). So the affected population is the small end of the family, and any
future claim of the form "researchers are receiving short data" has to survive that ratio.

## Named users

The fan-out found, for the whole family: one bachelor thesis citing `gdeltPyR` in its reference list
(not in its body sentence); one working paper whose full text a scholarly index reports contains the
string, and which the fan-out **could not open** (HTTP 403) and therefore did not quote; several
theses naming the withdrawn R package; and for `gdelt-client`, **no named user at all** — no paper,
no tutorial, no repository, no issue tracker in its own package metadata.

The object's own project blog endorses `gdeltPyR` by name (fan-out; not re-opened here).

**This practice's reading, stated as a reading:** the evidence supports *"a real package with real
users and no maintainer answering"*, and does **not yet** support *"published research results are
wrong because of this"*. Nobody has been shown to have consumed a short result. That gap is exactly
what gate session 2 has to close or fail on.

## What the fan-out could not reach

The one paper whose full text is indexed as containing the package name (HTTP 403, twice); a
bibliographic full-text sweep (rate limit); a second scholarly index (HTTP 429); one indexed tutorial
now returning 404. No conda-forge figure exists (the registry returns 404 for the name). Recorded so
a later session does not mistake absence of evidence for evidence.
