# Verifier ride-along audit + responses — session 46, 2026-07-20

The Verifier was convened as a ride-along (the finding enters `claims.md`; the full independent
gauntlet is still owed before ship). Verdict: **PASS WITH FINDINGS.** The headline arithmetic was
independently recomputed and verified, the pre-registration confirmed a git-ancestor of the run,
and the sample selection independently rebuilt from the frozen prior census with zero mismatches.
Two blocking-class findings were remediated the same session (below); the rest are recorded.

## Findings and what was done

1. **BLOCKING — containment breach via `run.log` (remediated).** The run's per-item stdout, once
   committed, printed one line per item *in `sample.json` iteration order* — so index *i* in the log
   joined positionally to `sample.json[stratum][i]`, reconstructing URL→outcome for named handles
   (the exact "handle → shell/gone" misread containment exists to prevent). **Remediation:** the
   per-item log is no longer committed (it is written to an out-of-repo scratch file); the git
   history was rebuilt from the pre-registration anchor so `run.log` never enters the pushed record.
   Committed artifacts are `sample.json` (public URLs, no outcomes) + `results.json` (aggregates).
   `results.json` itself was verified aggregate-only, no raw hashes.

2. **BLOCKING-adjacent — classifier contradicted its own pre-registration (remediated).** The
   tweet-article-markup promotion (`has_article`) was documented "X-only" but was un-gated in code,
   so it fired on news/org (embedded-tweet/`<article>` markup on liveblogs, and one clear false
   positive on a report page with no tweet). **Remediation:** `has_article` is now gated to the
   `x-twitter` stratum in `classify_census.py`; the news/org arm was re-run under the corrected
   rule (archived **29/40→26/40 = 65.0%**; live **10/20→9/20 = 45.0%**). The Verifier confirmed
   **zero** such leakage in X or Telegram, so those figures are unchanged (and independently
   reproduced). The correction *strengthens* the validity-boundary reading (a larger under-read).

3. **Moderate — causal language (remediated).** "The loss happened at capture time" was stated in
   the finding-1 headline while the hedge sat paragraphs later. The hedge ("consistent with a
   capture-time failure … the live arm proves bot-servable in 2026, not that X served the crawler in
   2023-24") is now folded into finding-1 itself in both README and RESULTS-ANALYSIS.

4. **Moderate — validity-boundary rigour (addressed, one item deferred).** The Verifier judged the
   news/org handling "defensible, not motivated reasoning" (the positive-control shape was
   pre-registered), and pointed to objective corroboration in `results.json`'s own byte quartiles
   (median archived X = 2,754 B shell vs median archived news/org = 147,536 B real body). That
   corroboration is now stated on the work. Two honest limits recorded, not hidden: "near-100%" was
   not a numeric pass/fail threshold, so reading 65% as under-read is an interpretive call (supported
   by byte-size, not asserted); and a **frozen body-content sub-test** for news/org is a named
   next-session item rather than done here.

5. **Verified, no change needed:** arithmetic + all six Wilson intervals (exact match);
   `run.log`→`results.json` tally agreement (before removal); classifier logic (a) X-precedence and
   (b) Telegram no-post-ID-gate as documented; pre-registration `744fc4d` a git-ancestor of the run;
   sample selection rebuilt from the frozen CDX census with zero mismatches.

6. **Minor — "most-cited platform" framing (fixed).** news/org (229) is larger by raw count than X
   (170) but bundles many domains; the work now says "most-cited *single platform*."

7. **Minor — self-referential sample hash (documented).** `sample_sha256` is computed over the
   object before the field is embedded, so a plain `sha256sum sample.json` differs; noted in README.

## Standing status

The X-vs-Telegram headline (archived 3.1% vs 98.3%, corroborated by the live arm 80% vs 100% and by
independent selection-reproduction) is arithmetically correct and safe to record as a High-confidence
*computed* finding, now that the two blocking-class items are remediated. This ride-along does **not**
substitute for the full gauntlet on the exact shipped state, which remains owed.
