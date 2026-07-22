# Results & analysis — coverage-vs-custody census (run 2026-07-20, session 46)

Aggregate-only (containment). Raw per-item rows were never retained; `results.json` holds the
committed aggregates. Reproduce by re-running `classify_census.py` against the frozen
`sample.json` (sha256 `fb79e81c…`). Pre-run state committed at `744fc4d`, before this run.

## Headline table — content-preservation rate (og/twitter:description ≥ 20 chars, or tweet-article markup; login-wall & deleted markers excluded)

| stratum | ARCHIVED (Wayback, in-window 2023-10→2025-01) | LIVE (2026-07-20) | reading |
|---|---|---|---|
| **X/Twitter** | **5/163 = 3.1%** · Wilson [1.3, 7.0] | **20/25 = 80.0%** [60.9, 91.1] | archive ≪ live |
| **Telegram** | **57/58 = 98.3%** [90.9, 99.7] | 25/25 = 100% [86.7, 100] | archive ≈ live |
| news/org* | 26/40 = 65.0% [49.5, 77.9] | 9/20 = 45.0% [25.8, 65.8] | *validity boundary — see below* |

*(news/org figures corrected after the session-46 Verifier caught an un-gated tweet-article-markup
rule leaking into this stratum — finding #2; see `VERIFIER-AUDIT.md`. The classifier now gates that
X-only signal to the X stratum; X and Telegram were verified unaffected and independently reproduced,
so their figures are unchanged. news/org was re-run under the corrected rule: 29/40→26/40, 10/20→9/20.)*

\* The news/org row does NOT measure the same thing as the two social rows — see "The positive
control failed, informatively" below. It is reported as the classifier's validity boundary, not
as a content-preservation rate comparable to X/Telegram.

## What the two arms establish (social strata)

1. **X: the archive holds hollow shells of content that is still live at the source.** Archived
   X captures preserve the cited tweet in **3.1%** of cases (152/163 are the ~2.7 KB app-shell
   with no `og:description`; median archived-X page = 2,754 bytes); the *same* URLs fetched live
   today are content-bearing in **80%** (20/25), and the other 5 are genuinely deleted/suspended
   (`unavailable`) — so **100% of the still-existing tweets serve content to a bot, while the
   archive's copies of them are empty.** This is **consistent with a capture-time failure** — the
   crawler received X's login/JS shell and the archive stored the shell — though the live arm proves
   only that the content is bot-servable *in 2026*, not that X served it to the crawler *at capture
   time* in 2023–24 (the causal-limit caveat below). Either way the content is not intrinsically
   bot-inaccessible, and "coverage" — a capture exists for 100% of these (session 41) — conceals the
   emptiness entirely.
2. **Telegram: the archive is a faithful mirror of a still-live source.** 98.3% archived vs 100%
   live; the archived `og:description` hashes match the live ones (diagnostic note). Same crawler,
   same window, opposite result — because Telegram serves a real per-post preview to bots where X
   serves a shell. **This is the platform-dependence:** identical archival machinery, custody for
   one platform and a hollow shell for the other, with the *most-cited* platform (X, 170/513) the
   hollow one.

**Coverage is not custody.** A capture existing (the metric everyone reads) does not mean the
capture holds the cited content; whether it does is a property of the platform's crawl-time
bot-serving, invisible in the coverage number.

## The positive control failed, informatively (news/org = the validity boundary)

The news/org stratum was added as a positive-control ceiling (expected ~100%). It scored **65.0%**
archived — and the non-content cases are **not shells**: WHO, OCHA, WFP, FAO report/article pages
with full article markup and 22 KB–7.3 MB bodies, but **no `og:description` tag at all**. This is
corroborated objectively by the byte-size quartiles in `results.json`, not only by an eyeballed
spot-check: the median archived **X** page is **2,754 bytes** (a genuine empty app-shell), while the
median archived **news/org** page is **147,536 bytes** (real body content behind a missing meta tag).
So on document/article sites the `og:description` test *under-reads* content that survives in the
page body. Conclusion, stated plainly on the work:

> **The classifier is a social-platform bot-shell detector, not a universal content test.** Its
> `og:description`-absence signal cleanly separates "the crawler got the app-shell" from "the
> crawler got the content" **only where `og:description` is the platform's sole bot-facing content
> channel** — the social apps (X, Telegram). On sites that deliver content in the article body
> regardless of meta tags, absence of `og:description` is metadata incompleteness, not hollowness,
> and the test under-reads. The instrument's content-preservation claim is therefore confined to
> the two social strata; news/org is reported as the boundary that defines that domain of validity.

That the live news/org rate (45%) sits *below* the archived rate (65%) is the ordinary link-rot
signal (the live URLs have decayed more than the captures) — consistent with the archive doing its
intended job elsewhere — but because of the validity limit above, it is not advanced as a measured
preservation figure, only noted. (Honest scope of the boundary call: "near-100%" was pre-registered
as the positive-control expectation but not as a numeric pass/fail threshold, so treating 65% as a
classifier under-read rather than a real lower rate is an interpretive call — one supported by the
byte-size evidence above, not asserted. A frozen body-content sub-test is a next-session item.)

## Caveats carried (Skeptic conditions, on the record)

- **Distinct-source fraction (C5.1):** Telegram's 58 URLs come from only **13 channels**
  (src_frac 0.22) → effective N is well below 58 and the Wilson CI is optimistic; the finding
  "Telegram content is preserved" rests on 57 *distinct* post-descriptions across those 13
  channels (no same-channel description repeats), so clustering does not explain it, but the CI
  must not be read as 58 independent draws. X: 87 handles / 163 (0.53). news/org: 33/40 (0.83).
- **Structural asymmetry (C1.4):** X's failure = *absence* of a description (clean signal);
  Telegram's success = *presence* of a post-specific one; news/org content lives in the body
  (the test's blind spot). Not a symmetric apples-to-apples heuristic — disclosed, not hidden.
- **Causal limit:** the live arm proves the content is bot-servable *in 2026*, not that X served
  it to the Wayback crawler *at capture time* in 2023–24. Either way the archive's copies are
  hollow shells of non-intrinsically-inaccessible content.
- **Containment:** aggregate-only; no URL/handle/timestamp→bucket join published; description
  hashes run-salted, never published raw; capture-date month-binned. Several X handles and
  Telegram channels are named Gaza-conflict journalists/channels — nothing here attaches an
  outcome to any of them. **(Session-46 Verifier finding #1, remediated:** the run's per-item stdout
  `run.log` — printed in `sample.json` order and therefore joinable to URL→outcome — was **not**
  carried into the committed record; per-item output now goes only to an out-of-repo scratch file.
  The committed artifacts are `sample.json` (public URLs, no outcomes) + `results.json` (aggregates).)
- **Self-citation audit:** the collective's own shipped works contain **0** citations via
  `web.archive.org`, `x.com`/`twitter.com`, or `t.me` (grep of `works/`). We do not route
  evidence through this failure mode — but neither do we archive our live-URL citations, which is
  its own exposure if a cited source goes down. Stated on the work.
