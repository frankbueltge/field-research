# Coverage Is Not Custody

*A stratified census of what the web archive holds versus what it merely covers, with a live-control arm. Draft — session 46, 2026-07-20.*

**One-line claim.** An archived capture *existing* (coverage) is not the same as that capture *holding* the cited content (custody); whether the two coincide is platform- and crawl-time-dependent — and for the single most-cited platform in this citation base, the web archive holds hollow shells of content that is still live at the source.

---

## What was measured — and what was not

**Measured:** the *structural envelope* of an archived (or live) capture — content-bearing vs. login/JS-wall vs. unavailable/deleted — via the presence and *length* of an `og:description`/`twitter:description` meta tag (X: or tweet-article markup), plus login-wall and deleted-page text markers. This is a property of the platform and the archive's crawler at capture time, not of the cited content.

**Not measured, not recorded:** no cited content substance, no post or tweet text, no author or channel identity on any narrative surface, no media, no subject matter. The committed results (`results.json`) are **aggregate-only** — no per-item URL, handle, or capture-timestamp→outcome row (a per-item capture timestamp is joinable back to the citation URL via the public prior census, so none is published; the run's per-item stdout is written to an out-of-repo scratch file, never committed). `sample.json` lists the already-public citation URLs, kept for reproducibility, and carries no outcomes. Several sampled handles/channels are named, identifiable people, including Gaza-conflict journalists — nothing here attaches an outcome to any of them.

This is an instrument-on-the-instrument: it says nothing about the underlying 2026 counter-forensic report, its citations, its authors, or the events they document. It measures the archiving infrastructure only.

## Method

**Sample (frozen, deterministic — `sample.json`).** Built from the frozen session-41 CDX census (`notes/2026-07-16-half-life-archival-probe/`) of the report's citation URLs. For each stratum, an archived arm and a live-control arm:

- **X/Twitter — archived:** 163 URLs (of 170 in-window citations; a full census, not a draw), each resolved to its earliest in-window (2023-10-01 → 2025-01-01) HTTP-200 capture, fetched via the archive's raw-response endpoint (no archive chrome).
- **Telegram — archived:** 58 URLs (of 66 in-window), same rule — a full census.
- **news/org — archived:** a deterministic sample of 40 URLs, added as a positive-control ceiling.
- **Live control:** the same URLs, fetched unauthenticated and without JavaScript on 2026-07-20 — 25 X/Twitter, 25 Telegram, 20 news/org — classified with the identical classifier.

**Classifier (frozen — `classify_census.py`), precedence order per capture:**
1. `unavailable` — a deleted/suspended/page-not-found marker fires.
2. `login_shell` — a login/JS-wall marker fires and description length < 60 (a wall page cannot be outvoted by bot-served boilerplate).
3. `content_present` — description length ≥ 20, or (X only) tweet-article markup is present.
4. `content_thin` — 0 < description length < 20.
5. `login_shell` — a wall marker with no description.
6. `other` — none of the above.

Content-preservation rate = `content_present` / n, reported with Wilson 95% intervals.

**Two fixes made before the run, on Skeptic input:**
- **X precedence fix:** tweet-article markup promotes a capture to `content_present` *before* the login-wall rule fires — a public tweet shown alongside a login nag is content, not a shell.
- **Telegram guard:** rather than a hard post-ID gate (rejected — a pre-run diagnostic showed genuinely post-specific pages carry neither a post ID in `og:url` nor `tgme` markup, so a gate would over-reject valid content), the deleted-post-to-channel-bio risk is bounded by a within-channel description-duplication statistic and a reported distinct-channel count.

**Pre-registration.** The sample and classifier were committed at `744fc4d`, before any capture in this run was fetched — a Verifier can confirm both files are git-ancestors of the results commit. The comparative table is the measurement; there is no go/kill rule to reverse-fit, so the numbers stand as found.

## The three findings

| stratum | ARCHIVED (Wayback, in-window 2023-10 → 2025-01) | LIVE (2026-07-20) | reading |
|---|---|---|---|
| **X/Twitter** | **5/163 = 3.1%** [1.3, 7.0] | **20/25 = 80.0%** [60.9, 91.1] | archive ≪ live |
| **Telegram** | **57/58 = 98.3%** [90.9, 99.7] | **25/25 = 100%** [86.7, 100] | archive ≈ live |
| news/org* | 26/40 = 65.0% [49.5, 77.9] | 9/20 = 45.0% [25.8, 65.8] | *validity boundary — see below* |

\* The news/org row does not measure the same thing as the two social rows. It is reported as the classifier's validity boundary, not as a content-preservation rate comparable to X/Telegram — see the section below.

### 1. X: the archive holds hollow shells of content still live at the source

Archived X captures preserve the cited tweet in 3.1% of cases (152/163 are the app-shell with no `og:description`; the median archived-X page is 2,754 bytes). The same URLs fetched live today are content-bearing in 80.0% (20/25); the other 5 are genuinely deleted or suspended tweets (`unavailable`) — meaning **100% of the tweets that still exist serve content to a bot, while the archive's copies of them are empty.** This is **consistent with a capture-time failure**: the crawler received X's login/JS app-shell instead of the tweet, and the archive faithfully stored the shell. (The live arm proves the content is bot-servable *in 2026*; it does not prove X served it to the crawler *in 2023-24* — the causal-limit caveat below. Either way the content is not intrinsically bot-inaccessible.) "Coverage" — a capture exists for essentially all of these citations, per the prior census — conceals the emptiness entirely.

### 2. Telegram: the archive faithfully mirrors a still-live source

98.3% archived vs. 100% live, and the archived `og:description` hashes match the live ones. Identical archival machinery, same crawler, same window — the opposite result from X, because Telegram serves a real per-post preview to the crawler where X serves a shell. This is the **platform-dependence**: custody for one platform, a hollow shell for the other, with the *most-cited single platform* in this citation base being the hollow one. (X = 170 of 513 citations; the news/org category is larger in raw count at 229 but bundles many distinct publisher domains rather than one platform.)

### 3. news/org: the positive control "failed," informatively — it is the instrument's validity boundary

news/org was added expecting a preservation rate near 100% (static article pages, no login wall). It scored 65.0% archived instead. The non-content cases are **not shells**: WHO, OCHA, WFP, and FAO report and article pages with full article markup and bodies ranging 22 KB to 7.3 MB — but carrying no `og:description` tag at all. This is corroborated objectively by the byte-size quartiles, not only by inspection: the median archived **X** page is **2,754 bytes** (a genuine empty app-shell) while the median archived **news/org** page is **147,536 bytes** (real body content behind a missing meta tag). On document/article sites, the `og:description` test *under-reads* content that lives in the page body.

**Conclusion:** the classifier is a social-platform bot-shell detector, not a universal content test. Its `og:description`-absence signal cleanly separates "the crawler got the app-shell" from "the crawler got the content" *only* where `og:description` is the platform's sole bot-facing content channel — the social apps, X and Telegram. On sites that deliver content in the article body regardless of meta tags, absence of `og:description` is metadata incompleteness, not hollowness. The content-preservation claim above is therefore confined to the two social strata; news/org is reported as the boundary that defines that domain of validity, not folded into the headline claim.

(The live news/org rate, 45.0%, sitting *below* the archived rate, 65.0%, is ordinary link-rot — the archive doing its intended job elsewhere on this stratum — but is not advanced as a measured preservation figure here, because of the validity limit just stated.)

## The instrument's domain of validity

This is a strength of the design, not a limitation to bury. The instrument does not claim to measure "content preservation" in general; it measures a specific, falsifiable signal — the presence of a bot-facing preview field — and that signal is only valid where the platform routes its bot-facing content through that field. X and Telegram do; document/report sites like WHO, OCHA, WFP, and FAO pages do not (they route content through the body). The news/org stratum was run specifically to find this boundary, and it did: 65.0% is not "the archive two-thirds-preserves news," it is "the classifier detects content on two-thirds of pages where content isn't only in the meta tag." Reporting this boundary alongside the two valid strata is what makes the X and Telegram findings trustworthy rather than assumed. (One honest scope note: "near-100%" was pre-registered as the positive-control expectation but not as a numeric pass/fail line, so reading 65% as an under-read rather than a real lower rate is an interpretive call — supported by the byte-size evidence, not asserted; a frozen body-content sub-test is a next-session item.)

## Caveats

- **Distinct-source fraction.** Telegram's 58 archived URLs come from only 13 channels (distinct-source fraction 0.22) — the effective N is well below 58, so the Wilson CI is optimistic. That said, the 57 `content_present` cases carry 57 *distinct* post-descriptions across those 13 channels — no same-channel description repeats — so the finding does not rest on clustering. (X: 87 handles / 163, fraction 0.53. news/org: 33/40, fraction 0.83.)
- **Structural asymmetry.** The three strata are not a symmetric apples-to-apples test: X's failure mode is *absence* of a description (a clean signal); Telegram's success is *presence* of a post-specific one; news/org's content lives in the page body, which is the test's blind spot. This asymmetry is disclosed, not hidden.
- **The causal limit.** The live-control arm proves the content is bot-servable *in 2026*; it does not prove X served `og:description` to the archive's crawler at capture time in 2023-24 (X's bot-serving behavior may have changed since). Either way, the archive's X captures are hollow shells of content that is not intrinsically bot-inaccessible — that is the load-bearing point regardless of which side of the causal question is true.
- **Containment.** All results are aggregate-only; no per-item URL, handle, or timestamp-to-outcome row is published. Description hashes are run-salted and discarded, never published raw. Capture-date histograms are month-binned with small bins suppressed. Several named X handles and Telegram channels in the underlying sample are Gaza-conflict journalists and channels; nothing in this work attaches an outcome to any of them.

## Self-implication

A grep of the collective's own shipped works (`works/`) for citations via `web.archive.org`, `x.com`/`twitter.com`, or `t.me` returns zero genuine matches. We do not route evidence through the failure mode this instrument measures. But the same grep shows we also do not archive our own live-URL citations — which is its own exposure if a source we cite goes down later. That gap is stated here honestly rather than left implicit.

## The argument, enacted

This work is an instrument built to measure the archive rather than the archived content. Turning the same classifier on a third stratum — news/org — measured the instrument's *own* validity limit, not a new fact about the world: the boundary at which "absence of a meta tag" stops meaning "absence of content." An instrument that measures the measuring infrastructure, and then uses the same test to find where its own measurement stops being valid, is the reflexive move this instrument was built to make.

## Status

**DRAFT.** This document has not passed the full gauntlet. A Skeptic and a Verifier were convened this session as pre-run design-hardening and a ride-along audit (their input is folded in and recorded in `VERIFIER-AUDIT.md`), but the **full gauntlet on the exact shipped state** — an independent Verifier, an independent Skeptic's refutation attempt, and a published Interlocutor critique — is **owed** before this graduates from `drafts/` to `works/`. Named next-session build items: a frozen body-content sub-test for the news/org validity boundary; a decision on the work's public form (an interactive/visual custody-vs-coverage exhibit). Data and method are committed and frozen:

- Prior census: `notes/2026-07-16-half-life-archival-probe/` (513-URL citation census, capture-existence)
- Prior content-quality spike: `notes/2026-07-19-half-life-content-quality-spike/` (X/Twitter-only content-preservation pilot)
- This draft: `PRE-REGISTRATION.md`, `DIAGNOSTIC-NOTE.md`, `RESULTS-ANALYSIS.md`, `VERIFIER-AUDIT.md`, `sample.json`, `classify_census.py`, `results.json` (`sample.json`'s embedded `sample_sha256` is computed over the object *before* the hash field is added, so a plain `sha256sum` of the file will differ — re-derive by hashing the sorted object without that key)
