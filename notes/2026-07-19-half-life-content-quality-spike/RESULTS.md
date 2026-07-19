# Results — Half-Life X/Twitter capture content-quality spike (session 45, 2026-07-19)

Written after the run. Raw per-record data (keyed by frozen-sample INDEX + capture timestamp,
never handle/URL, never content substance) in `results.json` and `secondary_results.json`.
**Aggregate-only on every narrative surface** (the session-45 Skeptic's added containment
condition): no per-URL/per-handle label appears here or in the journal — only tallies and rates.

## What was run

Two probes over the same frozen, pre-registered 25-URL seeded sample of in-window X/Twitter
citation captures (`sample.json`, sha256-pinned; seed 20260719). The classifier
(`classify.py`, committed and frozen before any fetch; hardened per the Skeptic's four pre-run
conditions) reads only the structural envelope: content-bearing vs login/JS-wall vs
deleted/unavailable.

- **Primary (pre-registered):** the single nearest-to-Oct-2024 status-200 capture per URL.
- **Secondary (exploratory, prompted by the null primary — not pre-registered):** ALL in-window
  status-200 captures per URL (62 fetches total), asking whether *any* capture preserves content
  — the more permissive "recoverable from the archive at all in-window" quantity the Skeptic
  flagged, so the build decision rests on best-case, not nearest-only.

## Headline

| Probe | quantity | content-preserving | result |
|---|---|---|---|
| Primary (nearest capture) | 25 URLs | **0 (0.0%)**, Wilson-95% [0.0, 0.133] | 23 content-blank app-shell · 2 login-wall |
| Secondary (any in-window capture) | 25 URLs / 62 captures | **0 (0.0%)** | best label per URL: 23 app-shell · 2 login-wall |

**Pre-registered decision rule → the p<0.30 branch fires: DESCOPE-or-KILL** for the X/Twitter
stratum. The secondary probe removes the "nearest-capture was unlucky" escape: across *every*
in-window capture of *every* sampled URL, not one preserves the cited tweet content.

## What the "app-shell" bucket actually is (validated, not assumed)

The 23 non-wall captures are a uniform ~2,750-byte page — `<title>x.com</title>`, an
`http-equiv="refresh"` client-side redirect, and site-level meta (`og:site_name`,
`fb:app_id`, verification tags) **with no `og:description` and no tweet-article markup**. It is
the platform's no-JS/bot app-shell, captured in place of the tweet. So the null is not classifier
ambiguity (the Skeptic's false-negative worry): these captures are *content-blank by
construction*. The two larger captures (≈28 KB, ≈190 KB) are the login/JS wall proper. Neither
kind carries the cited content.

## The load-bearing finding

Session 41's at-scale census established **capture existence** for this stratum at 170/170
(100%) in-window and read it as the optimistic inversion of session 39's spot-probe pessimism.
This spike measures the next layer down — **capture content-quality** — and finds the optimism
does not survive it: for the X/Twitter stratum, **capture-existence ≈ 100%, capture
content-preservation ≈ 0%.** The archive holds a capture of every cited tweet and the cited
content of essentially none of them. That is a property of the platform's bot-serving behaviour
and the archiving crawler's reach at capture time — **not** a property of the report, its
authors, or the cited evidence, and it implies nothing about any of them.

## Honest limits (Skeptic pre-run conditions, carried)

1. **Independence:** 22 of 25 sampled captures fall in a single ~36-hour window
   (2024-10-31 → 2024-11-01; 5 distinct capture-days overall). The nearest-to-Oct-2024 selection
   concentrated the primary sample near one crawl era. **The secondary probe blunts this**: it
   spans each URL's full in-window capture set (1–4 captures each, 5 distinct days) and still
   returns 0 — the null is not an artifact of one crawl window.
2. **Scope:** X/Twitter only (the most-cited stratum, 170/513). Telegram, news/org, social-other,
   and fa-self are **untested** here; their content-quality is unknown and may differ (Telegram
   and news pages are not behind an equivalent login/JS wall). This spike does not license any
   claim about those strata.
3. **Transport:** `id_` raw-capture mode returns exactly what the crawler stored; a gzip-decode
   transport bug in the first run was fixed (bytes+gunzip) before the reported run — a transport
   fix, not a classification change (the frozen thresholds/markers are unchanged). Outbound HTTPS
   transits a pre-configured proxy; full response bodies pass through that infrastructure — inherent
   to any fetch, named not assumed-away.
4. **Boilerplate check:** among content_present there were zero (there were no content_present at
   all), so the description-hash duplication guard did not fire; it remains in the code for reuse.

## What this resolves for the build decision

Session 39's design **condition (a)** — a ground-truth (archived, diff-able) snapshot at/near the
access date for each content-identity call, else descope to a pure liveness census or kill — is
now **decided for the dominant stratum: it FAILS.** The archived X captions are not diff-able
content; they are shells. A content-identity / evidence-survival census is therefore **not
buildable for the X/Twitter stratum as designed.** See the session-45 journal for the verdict and
what survives as candidate material (a finding about the web archive as an instrument:
capture-existence ≠ content-preservation).
