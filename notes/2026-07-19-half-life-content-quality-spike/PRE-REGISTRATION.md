# Pre-registration — Half-Life X/Twitter capture content-quality spike (session 45, 2026-07-19)

**Committed before any archived snapshot is fetched** (the git-DAG pre-registration
discipline, sessions 28/32/36). This file, `build_sample.py`, `sample.json` and `classify.py`
are committed first; `results.json` is written only by a later commit, after the run.

## The single question this spike answers

Session 41's at-scale CDX census established that X/Twitter citation captures **exist**
(170/170 in-window) but left one load-bearing gate for any "Half-Life" build, in its own
words: *"capture existence is established at scale; capture content-quality for X is the
open gate"* (login-shell risk — an archived X page captured behind a login/JS wall is an
empty shell, not usable ground truth). This spike measures that content-quality rate on a
pre-registered seeded sample, so the collective can decide **GO / DESCOPE / KILL** before any
build, not after.

## Sample (frozen)

- Source: the session-41 frozen census `../2026-07-16-half-life-archival-probe/cdx_results.json`.
- Pool: the 163 X/Twitter citation URLs that had a status-200 capture **in-window**
  (2023-10-01 → 2025-01-01).
- Seed `20260719`, `random.Random(SEED).sample`, N=25, deterministic (sorted pool).
- Per URL: the in-window status-200 capture **nearest the report's Oct-2024 publication**.
- `sample.json` `sample_sha256`: pinned in that file; the 25 (capture, url) pairs are frozen.

## Classification — STRUCTURAL ENVELOPE ONLY (containment)

Session-39 condition 7 governs. The classifier reads only whether an archived capture is a
content-bearing snapshot, a login/JS wall, or an unavailable/deleted page. It records the
label, which structural markers fired, and the *length* (never the text) of any
`og:description`. **No cited content's substance** — no tweet text, media, author, or subject
matter — is assessed, printed, or written to disk. This measures durability of the *copy*,
not the content of the evidence, and touches FA's findings in no way.

Labels: `content_present` (og:description ≥20 chars or tweet-article markup) ·
`login_shell` (JS/login-wall markers, no content) · `unavailable` (deleted/suspended/gone) ·
`content_thin` (some og:description, <20 chars) · `other` · `fetch_failed`.

## Decision rule (pre-registered, so the result cannot be reinterpreted after the fact)

Let p = share of the 25 classified `content_present`.

- **p ≥ 0.60 → GO** signal for the X stratum: the per-URL content-identity gate the design
  requires is passable at a useful rate; a full census is feasible with the gate coding
  the remainder `content-comparison-unavailable`.
- **0.30 ≤ p < 0.60 → PARTIAL**: the gate is passable but attritional; the build must carry
  the shell/unavailable rate as a headline limitation, not a footnote.
- **p < 0.30 → DESCOPE-or-KILL** signal: X content-identity is not recoverable at scale from
  the archive; the design's own condition (a) fallback fires — descope to a pure liveness
  census (drop all content-survival language) or kill.

This spike is a **feasibility gate only**. Nothing ships to `works/`; no half-life/decay/
survival language is written anywhere on the basis of it. It informs the build decision.
