# Results — archival-coverage census, 513 citation URLs (run 2026-07-16, session 41)

Written after the census completed; raw per-URL records in `cdx_results.json`.

## Headline table

Coverage = at least one Wayback capture of the exact URL (or, for X, its
`x.com`/`twitter.com` twin) **in the window 2023-10-01 → 2025-01-01**, by CDX metadata.

| Stratum | n | in-window | ever-only | no captures | CDX-gated | failed |
|---|---|---|---|---|---|---|
| x-twitter | 170 | **170 (100%)** | 0 | 0 | 0 | 0 |
| telegram | 66 | 58 (88%) | 2 | 6 | 0 | 0 |
| news-org-other | 229 | 186 (81%) | 0 | 25 | 18 | 0 |
| social-other | 30 | 25 (83%) | 1 | 4 | 0 | 0 |
| fa-self | 18 | 16 (89%) | 0 | 2 | 0 | 0 |
| **total** | **513** | **455 (88.7%)** | 3 | 37 | 18 | 0 |

## Findings

1. **The session-39 hinge inverts at the capture-metadata level: the X/Twitter stratum is
   FULLY covered.** All 170 X/Twitter citation URLs have at least one capture inside the
   window — the most-cited platform stratum is the *best*-covered, not the worst. Session
   39's spot probing (which found X/`t.co` "unreliable for both live-checking and archival")
   was about a different layer: whether a capture of an X page *preserves the content*
   behind the login wall, and whether `t.co` shortlinks resolve. That caveat now becomes the
   single load-bearing question for the build: **capture existence is established at scale;
   capture content-quality for X is the open gate.** (Note also: `t.co` barely exists in the
   citation base — 1 URL of 513. The report cites canonical tweet URLs; the `t.co` links that
   appear in the PDF text are *inside quoted tweet bodies*, not citations.)
2. **Telegram: 88% in-window.** Of its 6 no-capture URLs, 4 carry implausibly long post IDs
   (10 digits — visible line-wrap reconstruction artifacts of the extractor, e.g.
   `t.me/ShehabTelegram/4005713101`), so true Telegram no-coverage is likely 2–6 of 66. Two
   further URLs are archived only *outside* the window (Sept 2025 captures — archived later,
   not diff-able against the report's Oct-2024 access dates).
3. **News/org: 81% in-window, plus an unknowability class.** All 18 CDX-gated URLs are
   `theguardian.com` — the Guardian's captures are anonymously unqueryable even at the
   metadata level ("This type of CDX query requires authorization"), so for this publisher
   coverage is **unknowable, not absent**. The 25 genuine no-capture URLs spread across 19
   domains (5× `ochaopt.org`, 3× `haaretz.com`, 2× `nytimes.com`, …; at least 1 is a visible
   reconstruction artifact).
4. **Overall: ~89% of the recoverable citation base has in-window archival ground truth** —
   and every no-capture count above is an upper bound on true absence, since extraction
   noise (imperfect line-wrap reconstruction) only ever produces lookup misses.

## Methods notes, honestly

- The first parallel run (5 workers) suffered a burst of TLS connection resets
  (`curl: (35) Recv failure`) concentrated in the contiguous Telegram block — transient
  server/proxy load behavior, not URL-specific: a serial retry at ~1 s spacing resolved all
  40 failures, most to `covered_in_window`. A re-runner should throttle politely.
- The Wayback **availability API** (`archive.org/wayback/available`) was tested and
  discarded as an instrument: it returned "no snapshot" for URLs whose captures the CDX
  index itself lists (details in `README.md`). Coverage numbers derived from that API would
  be systematically wrong in the undercounting direction.
- This census measured **archival coverage only**. No cited URL was contacted; no liveness
  was measured; no cited content was fetched or assessed (containment conditions, session
  39). "Covered" means the archive holds *a* capture — not that the capture is a faithful
  copy of what the citation saw.

## What this means for the "Half-Life" build decision

Session 39's condition (a) — "archival coverage confirmed per stratum at scale before any
build" — is now **met at the capture-existence level for all strata** (weakest: news/org 81%
plus the Guardian unknowability class). The census design's ground-truth gate remains
necessary per URL (content-identity, not existence), and the X stratum's gate now hinges
entirely on capture content-quality (login-shell risk). The Guardian gating adds a category
the design must carry: `coverage-unknowable (publisher-gated)` alongside
`content-comparison-unavailable`. The reframe decision (field-wide OSINT durability with FA
as one case among named peers) and the possible FA right-of-reply remain the open steer
questions — unchanged by this probe.
