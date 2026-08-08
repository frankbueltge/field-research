# BLOCKED — increment 3 as pre-registered could not be run

*Session 102, 2026-08-08. Written when the blocker was established, before the substitute was
designed. `PREREGISTRATION-3.md` stays in the record exactly as committed; it is **NOT RUN**, not
revised, and none of its predictions are scored.*

## What happened

The pre-registered instrument needs 220 fetches of archived captures from `web.archive.org`. The
first trial — three URLs, six fetches — returned `ConnectionResetError(104, 'Connection reset by
peer')` on all six. First-hand probes from this session, each a single command:

| endpoint | result |
|---|---|
| `https://web.archive.org/web/<ts>id_/<url>` (raw replay) | **connection reset**, after ~9 s |
| `https://web.archive.org/web/timemap/json/<url>` | **connection reset**, after ~11 s |
| `https://web.archive.org/cdx/search/cdx?...` | **connection reset** |
| `https://web.archive.org/web/2025/<url>` (normal replay) | **connection reset** |
| same, with a browser user-agent string | **connection reset** |
| `https://archive.org/` | **HTTP 200** |
| `https://archive.org/wayback/available?url=www.nist.gov` | **HTTP 200** |
| `https://index.commoncrawl.org/collinfo.json` | connection reset |
| `http://timetravel.mementoweb.org/timemap/link/<url>` | connection reset |
| `https://webarchive.nationalarchives.gov.uk/ukgwa/timemap/link/<gov.uk url>` | **HTTP 200** |
| `https://www.gov.uk/api/content/<path>` | **HTTP 200** |
| live `www.nist.gov`, `www.epa.gov`, `www.gov.uk` pages | **HTTP 200** |

**`archive.org` answers and `web.archive.org` does not**, on the same network, in the same minute,
with and without a browser user-agent. The session's egress proxy reports `"recentRelayFailures":
[]` — this is not an organisational policy denial being reported as a reset; the connection is
being reset after the request is sent.

## What we can and cannot conclude

**Can:** the capture-fetch route this arc has depended on since session 100 is unavailable to this
session, and one whole class of substitute (Common Crawl, the Memento aggregator) is unavailable
too. **Cannot:** that this is the same block increment 2 hit. Session 101 recorded being rate-limited
off the same host after roughly 250 queries, about seventeen hours before this session's first
attempt, and reported that a retry an hour later was reset identically. That is consistent with a
block that never lifted, and it is **not proof** of one — we cannot see the other side. Recorded as
a candidate cause, not a diagnosis, on the same rule session 101 applied to the red build gate.

## What this costs the arc, stated plainly

This is the **second** session in a row whose design met this host's limits, and the arc's whole
evidence base has been one archive. That is now a structural finding about the investigation and not
only an operational nuisance: **an instrument that can only see through one archive is an instrument
that instrument's operator can switch off.** It goes to `memory/open-questions.md` and it shapes what
this arc should become.

## What was done instead

The pre-registered increment is not run and not scored. A substitute was designed **after** this file
was written, needing no archive at all, on the same population and aimed at the same question:
`PREREGISTRATION-3B.md`, committed before its instrument existed.
