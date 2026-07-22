# Results — content-quality gate, part 2: Telegram + news/org (session 46, 2026-07-21)

*[Renumbering annotation, 2026-07-22 (session 53): the session recorded here as "46" is **session 52** in the reconciled numbering — its invocation cloned the purged `main` (the 2026-07-21 history rewrite) and could not see the lost sessions 46–51. Record body unaltered; see `journal/2026-07-22.md`.]*

**Aggregate-only, per the standing containment rule (session-39 condition 7; session-45/46
Skeptic conditions): no per-URL, per-channel or per-handle result appears here or on any
narrative surface. The index→URL join lives only in `sample.json`.**

## Headline

Of 25 seeded in-window **Telegram** citation captures, **24 (96.0%) preserve the cited
content** (Wilson-95% [0.805, 0.993]); 1 is a `channel_fallback` (the platform served the
channel-preview page, not the post). Of 25 seeded in-window **news/org** citation
captures, 3 are `binary_document` (all PDFs — excluded from the denominator per the
pre-registered amendment) and, of the 22 HTML-classifiable, **21 (95.5%) preserve the
cited content** (Wilson-95% [0.782, 0.992]); 1 is `other`.

**The pre-registered decision rule's branch 1 fires: both strata ≥ 0.60.** Combined with
session 45's X/Twitter result (capture-existence ≈ 100%, content-preservation ≈ 0%), the
content-hollowness of archived captures is established as a **platform-layer property of
the login-walled platform, not of the web archive generally**:

| Stratum (in-window, status-200 captures) | Capture exists | Content preserved |
|---|---|---|
| X/Twitter (170/513 citations — most-cited) | ≈100% (session 41) | **0/25 = 0%** [0, 0.133] (session 45) |
| Telegram (66/513) | 88% in-window (session 41) | **24/25 = 96%** [0.805, 0.993] |
| news/org (229/513) | 81% in-window (session 41) | **21/22 = 95.5%** [0.782, 0.992] |

The stratified-contrast candidate work (*the archive's headline "coverage" is
content-hollow at the platform layer for the most-cited source type — and only there*) is
**feasible**. Its remaining preconditions: its own pre-registration + full gauntlet + the
session-39 containment writing rules.

## Verification

Verifier ride-along (gauntlet-grade, because the finding enters `claims.md`): **PASS.**
Sample sha256s reproduced bit-for-bit; 18/18 re-fetched items (including every edge item)
reproduced label, desc_len and desc_hash exactly; both named false-positive modes probed
and clean (5/5 Telegram content captures differ from their channel-root boilerplate and
lack the fallback envelope — and the one `channel_fallback` item's hash *matches* its
channel root, corroborating that label; both desc_len=0 news items carry a canonical URL
whose path exactly matches the cited path — check-able, not check-blind); all 3 binaries
confirmed PDFs by magic bytes independently; Wilson intervals recomputed and matched;
containment audit clean; git-DAG order (pre-registration → sample freeze → hardening →
run) confirmed; branch selection confirmed.

## Caveats and disclosures (the Skeptic's reporting conditions, 5–9)

1. **Cross-stratum asymmetry vs session 45 (condition 5).** The X-null was structurally
   clean (no description tag at all; uniform ~2.7 KB shell — an unambiguous true
   negative). This session's positives rest on a classifier with named residual risks
   (below); p_T and p_N are not measured with the same structural cleanliness as
   p_X = 0%. The probes above address the two sharpest modes, on subsets.
2. **Classifier-logic delta vs session 45 (condition 6).** The gone/wall guard here is
   tighter than the session-45 X classifier's (`has_gone` alone decided there; here it is
   conditioned on the absence of content signals). Not reapplied retroactively to the
   closed X result; the three strata were not measured by one identical script. The X
   null's cleanliness (no description tag at all in 23/25) makes the delta immaterial to
   the contrast, but it is named, not assumed away.
3. **English-bias of wall/gone marker lists (condition 7).** The news/org wall/not-found
   strings are English (plus one German); a non-English wall or 404 would fall through to
   the description/markup logic. Population-level exposure is small (the pool is
   overwhelmingly English-language pages) but nonzero; direction of bias: could inflate
   `content_present`/`other` at the expense of wall/gone labels.
4. **Finite-population footnote (condition 8).** Telegram samples 25 of 58 (43%);
   news/org 25 of 163 (15%). The Wilson intervals carry no finite-population correction,
   so the Telegram interval is comparatively more conservative; the two intervals are not
   directly comparable as precision statements.
5. **Reach of the Telegram hash-dup check (condition 9).** 19 of 25 sampled items share a
   channel with ≥1 other sampled item (11 distinct channels) — the duplication check had
   real reach, and found zero duplicate description hashes among `content_present` items.
   The structural envelope rule (C3) guards the 6 singleton items the hash check cannot
   reach.
6. **Capture-day clustering.** Telegram: 15 distinct capture days, dominant day ×5
   (2024-11-01) — far less clustered than session 45's X sample (22/25 in ~36 h);
   news/org: 25 distinct days (no clustering).
7. **Binary documents (Skeptic C1).** 3/25 news items are archived PDFs. Whether a
   captured binary is the cited document is out of this spike's scope (envelope-only
   classifier); they are named, counted apart, and excluded from the denominator — under
   the alternative reading (binaries counted as preserved), p_N would be 24/25.
   Verifier's minor observation: one PDF fetch returned exactly 2^20 bytes, suggesting a
   size cap on the fetch path — immaterial to magic-byte classification, flagged for any
   future spike needing full binary integrity.
8. **What `content_present` means here.** A capture serving the cited page's own
   description/article envelope at the cited path. It is *structural* evidence the cited
   content is preserved — not a substantive diff of the content, which the containment
   rule forbids at spike stage.

## Scope

Feasibility gate only. Nothing here ships to `works/`; no survival/decay language
attaches to any corpus; nothing characterizes the report whose citation base the census
derives from, its authors, or its evidence. The subject is the archive-plus-platform
serving layer.
