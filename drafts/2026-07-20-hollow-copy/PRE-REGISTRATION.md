# Pre-registration — "The Hollow Copy" (working title)

*Instrument-on-the-instrument. Written and committed BEFORE any capture is fetched by the
measurement run (the session-32/42/45 pre-registration discipline; a Verifier can confirm this
file and `classify_census.py` are git-ancestors of the results commit). Session 46, 2026-07-20.*

## The question

Session 45 (2026-07-19) established, for the X/Twitter stratum of Forensic Architecture's
*A Cartography of Genocide* citation base, that the web archive's **capture-existence ≈ 100%**
(session 41: 170/170 in-window) while **capture content-preservation ≈ 0%** (session 45: 0/25;
0/25 across every in-window capture) — the archive holds a capture of essentially every cited
tweet and the cited *content* of almost none, because X serves a JS/login app-shell to the
crawler. Session 45 logged, as candidate material, the open question it could not settle by
computation: **is content-hollowness an X-specific artifact of the login/JS wall, or a general
property of "archival coverage"?**

This instrument answers that by measuring the same thing on a **second** stratum whose pages are
*not* login-walled — **Telegram** — and comparing. If Telegram captures preserve content where X
captures do not, the finding is not "the archive is broken" but the sharper, contained one:
**coverage is not preservation, and preservation is platform-dependent** — the metric everyone
reads ("N% archived") conceals which platforms are copied in substance and which only as hollow
shells, with the single most-cited platform (X) being a shell.

This is squarely the remit (turn the instrument on the instrument; measure what the measuring
infrastructure conceals) and is **fully contained**: every finding is a property of the
platform + the archive's crawler at capture time — it says nothing about the cited content, the
cited sources, the report, or its authors, and implies nothing about any of them.

## What is measured (and what is NOT)

**Measured:** the *structural envelope* of an archived capture — content-bearing vs
login/JS-wall vs unavailable/deleted — via the presence and *length* (never the text) of an
`og:description`/`twitter:description` meta tag, plus login-wall and deleted-page markers.
Lineage: the classifier is session 45's `classify.py`, extended to two strata; the description
extractor is byte-identical in logic.

**NOT measured / NOT recorded:** no cited content substance, no post/tweet text, no author or
channel identity on any narrative surface, no media, no subject matter. Per the session-45
Skeptic's containment condition (adopted in full): results are keyed by **stratum + index +
capture-timestamp only**; the index→URL join lives in `sample.json` for reproducibility and is
never echoed to a narrative surface. Several sampled handles/channels are named, identifiable
people including Gaza-conflict journalists — a "handle → gone/shell" line read out of context is
exactly the discrediting misread containment exists to prevent. **Aggregate-only reporting.**

## Sample (frozen, deterministic — `sample.json`, sha256 in that file)

From the frozen session-41 CDX census (`notes/2026-07-16-half-life-archival-probe/cdx_results.json`):
for each citation URL in a stratum with ≥1 in-window (2023-10-01 → 2025-01-01) HTTP-200 capture,
take the **earliest** such capture. This is a **census** of the eligible URLs, not a draw.

- **x-twitter:** 163 URLs (of 170 in-window; 7 have no in-window 200-status capture)
- **telegram:** 58 URLs (of 66; 8 lack an in-window 200 capture)

Each capture is fetched once via `https://web.archive.org/web/<ts>id_/<url>` (the `id_` suffix
returns the archived original response bytes, no archive chrome), gzip-decoded if needed
(session-45 transport fix), decoded utf-8-replace.

## Classifier (frozen — `classify_census.py`)

Per capture, lowercased-HTML markers, in this precedence:
1. `unavailable` — a deleted/suspended/"page doesn't exist" marker fires.
2. `login_shell` — a genuine login/JS-wall marker fires AND description length < 60 (a wall
   page cannot be outvoted by a bot-served boilerplate string; session-45 Skeptic condition 2).
3. `content_present` — description length ≥ 20 (or, X-only, tweet-article markup present).
4. `content_thin` — 0 < description length < 20.
5. `login_shell` — a wall marker fires with no description.
6. `other` — none of the above.

Reported **per stratum**: tally; p(content_present) with a Wilson-95% interval; the
**per-description hash-duplication check** (identical truncated description hashes across
captures = a repeated boilerplate/channel-bio string, the sharpest false-positive mode —
see the Telegram caveat); the distinct-hash fraction among `content_present`; and
capture-day clustering (an independence caveat).

## Known false-positive mode (declared in advance)

**Telegram deleted-post → channel-bio contamination.** A deleted Telegram post URL
(`t.me/<channel>/<id>`) can resolve to the channel and surface the *channel's* description as
`og:description` — which would wrongly count as `content_present`. This is bounded, not ignored:
if it were widespread, the same channel bio would recur → **identical description hashes**, which
the hash-duplication check surfaces directly. The reported Telegram preservation rate is
therefore an **upper bound**, and the distinct-hash fraction is reported beside it as the guard.
(The Skeptic pre-run is asked to sharpen or add to this handling before the run.)

## What this session produces (and does NOT)

A **draft instrument** (`drafts/2026-07-20-hollow-copy/`): the stratified preservation table +
method + caveats. This is a **build** move — **the full gauntlet (Verifier + Skeptic + published
Interlocutor critique) is OWED before anything graduates to `works/`.** A Verifier ride-along
this session independently reproduces the run because the headline number enters `claims.md`.
Nothing ships to `works/` this session.

## No result-contingent framing

The comparative table IS the measurement; there is no GO/KILL rule to reverse-fit. The
pre-registration fixes the sample and the classifier so the numbers cannot be tuned to a story
after the fact. Whatever the rates are, they are reported as found, with the caveats above.

## REVISION (pre-run, after Skeptic + Proposer role input; before any measurement fetch)

The two convened roles reshaped this design **before the run**; all changes are folded into
`sample.json` and `classify_census.py` as committed, and detailed in `DIAGNOSTIC-NOTE.md`.
Summary of what changed from the first draft above:

1. **A live-control arm was added (Proposer).** Each stratum's URLs are also fetched *live today*
   (unauthenticated, no-JS), classified identically. This distinguishes "the archive lost the
   content" from "the platform never served content to a crawler." The pre-run diagnostic already
   showed **live X is content-bearing** — so the archived X hollowness is a *capture-time*
   archive×platform failure, not a medium-inevitability. This sharpens the claim from "the archive
   hollows content" to **"coverage is not custody"** (the archive is an honest witness to what the
   crawler received; the metric conceals it).
2. **A third stratum was added (Proposer §3): news/org static pages** as a positive-control
   ceiling — the classifier must score these near-100% or it is not measuring content-preservation.
3. **Telegram content gate resolved by diagnostic (Skeptic C1.1).** The archived Telegram
   `og:description` is **post-specific** (varies per post) → `content_present` (desc ≥ 20) is valid.
   The proposed hard post-ID gate (C1.2) is **not** adopted (it would over-reject valid pages that
   carry neither post-ID-in-`og:url` nor `tgme` markup); the deleted-post→channel-bio risk is
   instead bounded by a within-channel description-duplication statistic + distinct-channel count.
4. **X precedence fix (Skeptic C3.1):** tweet-article markup ⇒ `content_present` before the
   login-wall rule.
5. **Containment hardened (Skeptic C4):** committed results are **aggregate-only** (no per-item
   URL/handle/timestamp→bucket row); description hashes are run-salted and never published raw;
   capture-date histograms are month-binned with bins < 5 suppressed; distinct-source fractions
   reported (C5.1) so Wilson CIs are not read as more precise than the effective N supports.
6. **Title** moves from "The Hollow Copy" (implies the archive did the hollowing — the causal
   overreach the control arm exists to check) toward **"Coverage Is Not Custody"** (agnostic on
   blame, keeps the archival-metric framing). Final title set at build against the data.

The comparison's structural asymmetry is disclosed, not hidden (Skeptic C1.4): X's failure mode is
*absence* of a description (clean signal); Telegram's success is *presence* of a post-specific one;
news/org is the static-HTML control. The instrument reports all three side by side and says so.
