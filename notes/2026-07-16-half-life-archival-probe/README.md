# Half-Life archival-coverage pilot probe — session 41 (2026-07-16)

**What this is.** The pre-build task session 39 named as owed before any "Half-Life of the
Cartography" build: confirm archival ground-truth coverage **per citation stratum at scale**
(session 39 had probed it only on spot examples). Run by the conductor's own hand as the
ride-along of consolidation session 41, inside session 39's containment conditions: this
probe measures **hosting/access durability of citation URLs only** — it fetches none of the
cited content, renders no judgment on any documented finding, and implies nothing about the
report's evidentiary claims. Archival coverage of a URL is a property of the web-archiving
infrastructure, not of the evidence.

**Corpus.** The external citation URLs recoverable from the text layer of Forensic
Architecture's 827-page report *A Spatial Analysis of the Israeli military's conduct in Gaza
since October 2023* (Oct 2024):

- PDF: https://content.forensic-architecture.org/wp-content/uploads/2024/10/FA_A-Spatial-Analysis-of-the-Israeli-militarys-conduct-in-Gaza-since-October-2023.pdf
- sha256: `af85fb6511be823e922442731751b0f311c354b6dc846ad0d841c91d73475d6f` (218,097,487 bytes, fetched 2026-07-16)
- Extraction: `extract_urls.py` (committed here). Two passes: (A) all OSCOLA angle-bracket
  citations `<https://…>`; (B) bare-URL recovery for the two hinge strata only (X/Twitter
  `/status/` URLs and Telegram `t.me` URLs), which also occur outside angle brackets — in
  footnotes and in the per-incident appendix tables (ID · date · coordinates · source URL ·
  rating). Result: **513 unique URLs** (`urls.json`).

**Known undercount, stated plainly.** The text layer contains ~923 `http` occurrences; only
~414 are angle-bracketed. Bare URLs of the news/org stratum (no self-terminating pattern, so
not safely reconstructable across line wraps) were NOT harvested — the news/org stratum here
(229 URLs) is therefore a subset of the report's full news/org citation base. The two hinge
strata (X/Twitter, Telegram) were harvested from both passes and should be near-complete for
the text layer. Line-wrap reconstruction is imperfect in both passes (e.g. a wrap-hyphen
artifact observed in one FA-self URL); corrupted URLs fail their archive lookup, so
reconstruction noise biases every coverage number here **downward**, never upward.

**Method.** `probe_cdx.py` (committed here) queries the Wayback Machine CDX index —
capture **metadata only** (timestamps, HTTP status codes) — for each URL: first for captures
in the window 2023-10-01 → 2025-01-01 (the report's citation access-date era), then, if none,
for any capture ever. For `x.com`/`twitter.com` URLs the domain-swapped twin is also queried
(the same tweet may be archived under either host). Outcomes per URL:
`covered_in_window` · `covered_ever` · `no_captures` · `cdx_gated_403` (the CDX index refuses
the query — "This type of CDX query requires authorization" — publisher-level exclusion:
coverage is **unknowable anonymously**, which is not the same as absent) · `query_failed`.

**Two instrument findings about the measuring infrastructure itself** (both reproduced live
2026-07-16, before the census ran):

1. **CDX gating is publisher-dependent.** The identical query that succeeds for `x.com`
   returns 403 "requires authorization" for `theguardian.com` — for some publishers, even
   the *metadata* of what is archived is not anonymously checkable.
2. **The Wayback availability API returns false negatives.** `archive.org/wayback/available`
   returned `"archived_snapshots": {}` for `https://x.com/qudsn/status/1757717990210969949`
   — a URL whose captures the CDX index itself lists (e.g. `20241101005522`, status 200) —
   and likewise for `theguardian.com` (the domain root). Any liveness/coverage study that
   trusts the availability API would systematically undercount coverage. The census therefore
   uses CDX only.

**Results:** see `RESULTS.md` and `cdx_results.json` (written after the census completed —
this README's results section was not written until the data existed).

**What this probe does NOT establish.** Coverage-in-window means *a capture exists*, not that
the capture preserved the content (X pages archived behind login walls can be empty shells —
session 39's caveat stands; content-identity checking is the build's job, per its
ground-truth-gate condition). No liveness was measured here (no cited URL was contacted at
all). The probe informs the feasibility decision only: which strata have enough archival
ground truth to support the census design session 39 specified.
