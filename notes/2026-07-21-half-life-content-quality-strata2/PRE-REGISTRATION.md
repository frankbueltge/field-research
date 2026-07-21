# Pre-registration — content-quality gate, part 2: Telegram + news/org strata (session 46, 2026-07-21)

**Committed before any archived snapshot is fetched** (the git-DAG pre-registration
discipline, sessions 28/32/36/45). This file, `build_sample.py` and `classify.py` are
committed first; `results.json` is written only by a later commit, after the run.

## The single question this spike answers

Session 45 decided the X/Twitter half of the content-identity gate: capture-existence
≈ 100% (session 41), capture content-preservation ≈ 0% (0/25 primary; 0/25 across all
in-window captures). The surviving candidate work — *the web archive's headline "coverage"
is content-hollow at the platform layer for the most-cited source type* — has a named
precondition (open-questions, session 45): the other strata's content-quality must be
tested, because Telegram and news/org pages are not behind the same login/JS wall and are
plausibly different. This spike measures the content-preservation rate for those two
strata on pre-registered seeded samples.

## Sample (frozen)

- Source: the session-41 frozen census `../2026-07-16-half-life-archival-probe/cdx_results.json`.
- Pools: per stratum, the citation URLs with outcome `covered_in_window`
  (Telegram: 58 of 66; news-org-other: 186 of 229). The 18 CDX-gated Guardian URLs are
  structurally excluded (coverage unknowable anonymously — session 41's category).
- Seed `20260721`, `random.Random(SEED).sample`, N=25 **per stratum**, deterministic
  (sorted pool, one RNG per stratum).
- Per URL: the in-window status-200 capture **nearest the report's Oct-2024 publication**
  (same TARGET/WINDOW as session 45).
- `sample.json` carries a `sample_sha256` per stratum; the (capture, url) pairs are frozen.

## Classification — STRUCTURAL ENVELOPE ONLY (containment)

Session-39 condition 7 governs, exactly as in session 45. The classifier reads only
whether an archived capture is a content-bearing snapshot, an access wall, or an
unavailable/deleted page. It records the label, which structural markers fired, the
*length* and a truncated *hash* of any description meta (never the text). No cited
content's substance — no message text, media, author, or subject matter — is assessed,
printed, or written to disk. Results are keyed by frozen sample index + capture timestamp,
**never** by URL/handle/channel, on any narrative surface; the index→URL join lives only in
`sample.json` for reproducibility. Several Telegram channels and some bylines belong to
named, identifiable people; the aggregate-only rule of session 45 applies unchanged.

Stratum-specific structure (the envelope differs; the labels are shared):

- **Telegram** (`t.me` single-post or `/s/` embed pages): a post-preview page carries the
  message text in `og:description` / `twitter:description` and (on embed pages)
  `tgme_widget_message` markup. Known failure envelopes: the channel-boilerplate preview
  (a description present, but it is the channel's about-text, identical across posts of the
  same channel — detected via the description-hash duplication check, never by reading the
  text), and the "Please open Telegram to view this post" / not-found envelopes.
- **News/org**: content pages carry `og:description` / `twitter:description` /
  `name="description"` and usually `<article`/headline markup. Known failure envelopes:
  404/not-found pages, consent/cookie walls, paywall interstitials, parked/suspended
  domains.

Labels (shared): `content_present` (description ≥20 chars or content markup) ·
`access_wall` (login/consent/paywall envelope, no content — the analogue of session 45's
`login_shell`) · `unavailable` (deleted/suspended/not-found/parked) · `content_thin`
(description present, <20 chars) · `other` · `fetch_failed`.

## Decision rule (pre-registered, so no outcome can be reinterpreted after the fact)

Let p_T and p_N be the share of each stratum's 25 classified `content_present`.
Per stratum, the session-45 thresholds apply unchanged:
**p ≥ 0.60 → content-bearing** at a usable rate · **0.30 ≤ p < 0.60 → attritional** ·
**p < 0.30 → content-hollow**.

Interpretation of the four headline combinations, fixed in advance:

1. **Both strata ≥ 0.60 (content-bearing):** the session-45 X-null is established as a
   **platform-layer property specific to the login-walled platform**, not of the archive
   generally. The stratified-contrast candidate work (X ≈ 0% vs others high) is
   **feasible**; its remaining preconditions are its own pre-registration + full gauntlet
   + the session-39 containment writing rules.
2. **Both strata < 0.30 (content-hollow):** the contrast collapses; content-hollowness is
   general across strata. The stratified-contrast work as scoped is **killed**; the
   surviving question would concern the archive layer as a whole — new scoping required,
   nothing built on this spike alone. (This outcome would also demand a classifier
   sanity-check against known content-bearing captures before being believed — the
   Verifier's live-extractor check, session-45 pattern.)
3. **Split (one ≥ 0.60, one < 0.30):** the contrast survives in reduced form (two-way,
   not three-way); feasible, with the hollow stratum joining X on the hollow side of the
   contrast and named as such.
4. **Any stratum attritional (0.30–0.60):** that stratum enters a future work only with
   its shell/unavailable rate carried as a headline limitation, not a footnote
   (session-45 PARTIAL rule).

This spike is a **feasibility gate only.** Nothing ships to `works/`; no survival/decay
language is written anywhere on the basis of it; nothing in it characterizes the report,
its authors, or its evidence — the subject is the archive-plus-platform serving layer.
