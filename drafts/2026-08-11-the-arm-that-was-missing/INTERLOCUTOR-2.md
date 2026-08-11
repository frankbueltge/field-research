# Interlocutor pass 2 — session 110's increment ("The run, the transition scan, the arms, the predictions scored…")

*Adversary pass against commit `62bb6592a893f0bb72db0b449aed2bcc7bb27235`, branch
`research/session-2026-08-11-2`. Files re-derived from: `INCREMENT-1.md`, `PREREGISTRATION-110.md`,
`DEVIATIONS.md` (D8–D12), `GATE-DECISION.md`, `CONCEPT.md` §5a, `vantage-2026-08-11-run2.md`,
`ledger/run-2026-08-11T1124Z.json` (2,904 obs), `census-results.json` (run 1, 2,201 results),
`ledger/diff-run1-run2.json`, `corpus-hn.json`, `corpus-merged.json`, `sweep-completeness.json`,
`legacy-id-control.json`, `ledger.py`, `ledger_diff.py`, `collect_corpus_hn.py`, `build_manifest.py`,
`check_sweep_completeness.py`, `manifest-run2.json`, `probe-results.json`, `edition-stratified-check.txt`.

**What I ran.** Independent Python re-implementations of the classifier and the diff logic (not
imports of the shipped scripts), run directly against the raw JSON, for every headline figure below.
`git log` / `git show --stat` / `git show --name-status` on the relevant commits and files to check
ordering. Two live network re-fetches: `curl` against `https://hn.algolia.com/api/v1/items/28456840`
(the specific primary source the report cites) and against `https://hn.algolia.com/{,api/v1/}robots.txt`
and `https://news.ycombinator.com/robots.txt`, done today (2026-08-11) from this environment, which is
**not** the arc's own vantage (AS396982) — so these are independent confirmations of content, not
reproductions of the arc's own network path.

---

## §(a) REFUTATION ATTEMPT

For each claim: what I did, what I got, verdict.

### 1. Run 2 headline counts (2,904 / 5,127.8 s / no throttling / arm rates)

Loaded `ledger/run-2026-08-11T1124Z.json` cold, wrote my own counter over `observations`, grouped by
`arm` and `state` (`RETRIEVABLE`/`NOT-RETRIEVABLE`/`INDETERMINATE`), independent of `ledger.py`.

- **A: 1940/2175 = 89.1954% → 89.20%.** Matches.
- **B: 381/447 = 85.2349% → 85.23%.** Matches.
- **B-truncated: 1/246 = 0.4065% → 0.41%.** Matches.
- Total requested = 2201 + 454 + 249 = 2904, exactly the planned count; `stopped: null`. Matches.
- `run_utc_end − run_utc_start` = 5,128.0 s (from the string timestamps) against the reported 5,127.8 s
  (from `time.time()` deltas, more precise) — a 0.2 s rounding gap, not a discrepancy.
- Cross-checked against `ledger/run2-stdout.txt` and the progress lines in `ledger/run2-stderr.txt`:
  monotonic progress (142s → 5121s across 2900 requests, evenly spaced, no jumps or resets) — internal
  evidence this is one continuous real run, not stitched or edited after the fact.

**Verdict: holds, exactly.**

### 2. Zero transitions across 2,147 jointly-determinate identifiers, 54 touching-INDETERMINATE

Wrote a second, independent diff — not `ledger_diff.py` — applying the classifier by hand to both
`census-results.json` (run 1, old schema) and the run-2 file, joining on `vid`. Result: **observed in
both = 2201, determinate in both = 2147, touching-indeterminate = 54, transitions = 0, disagreement =
0.000%.** Identical to `ledger/diff-run1-run2.json`'s published numbers in every field.

I specifically attacked the 54 touching-INDETERMINATE rows the task flagged. Breakdown by direction:
22 RETRIEVABLE→INDETERMINATE, 21 INDETERMINATE→RETRIEVABLE, 7 INDETERMINATE→NOT-RETRIEVABLE, 4
NOT-RETRIEVABLE→INDETERMINATE (sum 54, matches). None of these can be classified as a transition
because one side's true state is genuinely unknown — this is not a bug hiding a real event, it is the
correct, conservative behavior the pre-registration specified (§2.5: "transitions into or out of
INDETERMINATE are not transitions"). I additionally checked whether the 36 run-2 TLS timeouts are a
persistent property of particular identifiers (which would suggest something other than random noise
masking real transitions): **zero overlap** between run 1's 28 indeterminate vids and run 2's 26
indeterminate vids in arm A. The failures look like independent noise, not a systematic pattern tied
to specific videos.

I could not find a hidden transition. The only honest caveat — which the document does not state and
should — is structural, not a flaw in this run: **a real transition that happens to coincide with a
transport failure on either side is invisible to this instrument by construction**, and 54/2201 (2.5%)
of jointly-observed identifiers fall into that blind spot this round. That doesn't change the "0" — it
bounds how much confidence "0" can carry.

**Verdict: the classifier is genuinely identical across schemas (I reimplemented it separately and hit
the same numbers), nothing is silently dropped, and I could not find a transition hiding in the
touching-indeterminate rows. Holds.**

### 3. 36/2904 = 1.24% transport failures, one TLS class

All 36 INDETERMINATE records have `transport_error` == the literal string `"URLError: <urlopen error
_ssl.c:999: The handshake operation timed out>"` — I checked every one, zero exceptions. Distribution
across arms: A 26/2201 (1.18%), B 7/454 (1.54%), B-truncated 3/249 (1.20%) — roughly proportional to
arm size, not concentrated in one arm. Distribution across the request sequence: indices 113 through
2884 (out of 2904), spread over the entire run, not bunched in one time window. **36/2904 = 1.2397% →
1.24%.** Matches; correctly scored as failing the pre-registered P7 ≤1% ceiling.

**Verdict: holds, and not concentrated in a way that would bias any reported rate.**

### 4. The truncation artefact — mechanism, count, and the specific worked example

- **249/706 = 35.27% → 35.3%** not 19 digits: recomputed from `corpus-hn.json`'s raw `rows` (890 raw
  matches, 706 distinct ids) independently of `meta`. Matches.
- **248/249 = 99.6%** are strict prefixes of a well-formed id: recomputed with my own prefix-matching
  loop. Matches.
- **The "from the same comment" qualifier**, which is the load-bearing part of the causal claim (not
  just coincidence): my first pass, matching truncated-id → its *first* occurrence's `hn_object_id`
  only, found 2 apparent exceptions (`706572491190134711`, `75915920529540252`) that looked like
  prefixes of unrelated identifiers from different comments. On inspection this was **my own
  methodological error**: both ids recur across multiple raw rows under different `hn_object_id`s
  (duplicate hits from the sweep), and one of those recurrences does share a comment with the matching
  full id. Redone correctly — checking the *full set* of comments each truncated id appears in against
  the full set its full-id candidate appears in — gives **248/249 same-comment matches, 0 exceptions,
  1 no-candidate (`12345`)**, exactly as claimed.
- **Live re-fetch of the specific worked example**, `hn.algolia.com/api/v1/items/28456840`, run today
  independently of the arc's own tooling:
  ```
  "text":"Check out the author&#x27;s Arnold Schwarzenegger video call example: <a
  href=\"https:&#x2F;&#x2F;www.tiktok.com&#x2F;@arnoldschwarzneggar&#x2F;video&#x2F;6995538782204300545\"
  rel=\"nofollow\">https:&#x2F;&#x2F;www.tiktok.com&#x2F;@arnoldschwarzneggar&#x2F;video&#x2F;6995538782...</a>"
  ```
  This independently confirms the mechanism byte-for-byte: `href` carries the full 19-digit id
  `6995538782204300545`, the rendered text is cut to `6995538782...`, and both strings are exactly what
  `corpus-hn.json` recorded for that item. This is not the report's own harness reproducing its own
  claim — it is a fresh fetch of the primary source from outside the arc's environment.

**Verdict: the mechanism, the count, and the specific example all hold under independent re-derivation
and a live primary-source re-fetch.**

### 5. The counterfactual: naive harvest 382/693 = 55.12% vs true 89.20% (34.07pp vs 3.96pp)

Recomputed by merging arm B's determinate counts (381 RET, 66 NOT-RET) with arm B-truncated's (1 RET,
245 NOT-RET): 382/693 = 55.1227% → 55.12%. No double-counting — B and B-truncated are disjoint id sets
by construction (19-digit vs not), so the merge is a clean simulation of "what if the filter hadn't
run." Gap: 89.1954 − 55.1227 = 34.07pp; true gap 89.1954 − 85.2349 = 3.96pp. Both match. The "confirmed
P6 by a factor of about nine" line: 34.07/3.96 = 8.60×, which rounds more naturally to "about 8.6" than
"about nine" — a small rhetorical inflation, not a computational error.

**Verdict: holds; the "about nine" phrasing is loose but not materially misleading.**

### 6. The structural prefix test predicted the measurement (245 NOT-RET + 3 IND + 1 RET)

Cross-tabulated the 249 B-truncated observations against the pre-run prefix classification. Of the 248
ids identified as prefixes (predicted phantom, before the run — see the ordering check below): **245
NOT-RETRIEVABLE, 3 INDETERMINATE, 0 RETRIEVABLE.** The one non-prefix id, `12345`, is exactly the one
RETRIEVABLE row. Exact match to the report.

**One precision objection.** The report says "the prediction and the measurement agree on every row."
For the 245 NOT-RETRIEVABLE rows that's true. For the 3 INDETERMINATE rows it overstates the case:
a transport timeout is not agreement with "this cannot resolve," it is a non-result — those 3 rows
neither confirm nor refute the prediction. The correct, still-strong claim is "no row contradicted the
prediction," not "every row agreed." This is a wording precision issue, not a numeric one — it doesn't
change the 0-false-positive result on the 245 that did resolve determinately.

### 7. `12345` is a genuine legacy video, not a false positive

`legacy-id-control.json`: 10/11 small integers return `http: 400`; only `12345` returns `http: 200`
with `author: "xksnkfkf"` and thumbnail path `res/2014/08/31/`. Matches the narrative exactly. Two
caveats worth recording:
- **No script produced this file** (unlike every other measurement in the arc, which has a paired
  `.py`), and the file itself carries only curated fields (`http`, `author`, `thumb`, `title_len`), not
  a raw response body — weaker provenance than the ledger's full-observation standard the rest of the
  arc holds itself to.
- `title_len: 0` for `12345` — the oEmbed payload has an empty title. Not inconsistent with "a genuine
  legacy video" (early-platform items plausibly lack a title), but the report's phrase "a complete
  oEmbed payload" isn't independently checkable from this file since the raw body wasn't kept.

**Verdict: the finding holds (I cannot verify title/completeness claims beyond what's in the file, and
say so rather than assume it), but the evidentiary standard for this one control is thinner than the
rest of the arc's own bar.**

### 8. Age effect does not replicate on corpus B: OR 1.334, χ²=1.147, CI [0.786, 2.264]

Recomputed the 2×2 table independently from raw vid-decoded years (`int(vid) >> 32` → Unix timestamp →
UTC year), not trusting the report's bucketing:
- Arm A: ≤2022 554/656 = 84.5%, ≥2023 1386/1519 = 91.2% — matches.
- Arm B: ≤2022 141/170 = 82.9%, ≥2023 240/277 = 86.6% — matches.
- OR (new-vs-old, i.e. "older is worse") = 1.3341, χ² (no continuity correction) = 1.1468, 95% CI
  [0.7863, 2.2637] → reported as 1.334 / 1.147 / [0.786, 2.264]. **Exact match to 3 decimal places.**

**Power check** (the task's specific instruction — is this just underpowered?): I computed the power
of a two-proportion z-test at arm B's actual sample sizes (n=170 old, n=277 new) to detect an effect
the size of corpus A's own (84.5% vs 91.2%), α=0.05 two-sided: **power ≈ 58%.** A coin-flip-adjacent
chance of detecting the very effect corpus A shows, at this sample size. This substantiates — rather
than contradicts — the report's own "inconclusive, not refuted" framing; it is not dressing up a null
result, the null result really is close to what an underpowered honest test looks like.

**Verdict: holds, and the power argument for "inconclusive" is itself correct when checked.**

### 9. `194951213564514304` — HTTP 200 both runs, decodes to 1971

`census-results.json` row: `http: 200`, `created: "1971-06-10T08:30:16+00:00"`, `author_unique_id:
"ranzandniana1314"`, `title_len: 76`. `ledger` run-2 row for the same vid: `http: 200`,
`author_unique_id: "ranzandniana1314"`, `title_len: 76`. Independently decoding `int(vid)>>32` gives
`1971-06-10 08:30:16 UTC`. All match. The other three non-19-digit corpus-A ids (`726459750741134635`,
`677767122007582643`, `740580884959830349`) all return `http: 400` in run 2 — matches "the other three
return 400 and nothing more can be said."

**Verdict: holds.**

### 10. Corpus growth 2,201 → 2,655 (+20.6%)

454 new well-formed ids / 2201 = 20.63% → +20.6%. Matches (2201+454=2655).

### 11. P5 fails: corpus B older (61.7% vs 69.7% dating 2023+)

Recomputed independently: corpus B, 457 well-formed ids, 282 date ≥2023 → 61.71% → 61.7%. Matches.
Corpus A: I first got **69.87%** using the 2,197 well-formed ids as the denominator — 0.17pp off the
reported 69.7%. Traced it: the report's 69.7% uses **2,201** as the denominator (all of corpus A,
including its 4 non-19-digit "malformed" ids, which decode to junk pre-platform dates and are trivially
counted as "not ≥2023"): 1535/2201 = 69.74% → 69.7%. That reproduces the reported figure exactly, but
it is an **inconsistent denominator choice against corpus B's own figure**, which excludes corpus B's
249 phantom/malformed ids from its denominator (457, not 706). Using a like-for-like well-formed-only
denominator for both sides would report corpus A at 69.9%, not 69.7% — a bigger gap against corpus B,
if anything, so **P5 still fails and the direction is unaffected**, but the reported number is not
computed the same way on both sides of the comparison it's making.

**Verdict: P5's failure holds; the specific 69.7% figure rests on a denominator inconsistent with how
61.7% was computed. Non-fatal, but should be corrected or footnoted.**

### 12. P1–P7 scoring, K1–K5

- **P1** AS396982 both runs (`vantage-2026-08-11-run2.md`, `d['vantage']['asn']` in the run file) — holds.
- **P2** run 1: 1941/2173 = 89.3235% (recomputed from `census-results.json` directly); run 2: 89.1954%;
  Δ = 0.128pp — matches "0.128 pp," within the ±1.0pp band — holds.
- **P3** 0 transitions — holds (see §2 above).
- **P4** 454 new ids ≥ 100 — holds.
- **P6** see next paragraph.
- **P7** 36/2904=1.24% > 1% — correctly scored FAIL.
- **K1–K5**: recomputed each condition against its own stated threshold using the numbers above; all
  score exactly as the document says (K1 no, K2 no, K3 no [454≥50], K4 no [0.000%≤5%], K5 vacuous).

### 13. P6 "holds": is 3.96pp inside noise at n=447?

This is the sharpest test the task asked for. Two-proportion z-test, A (1940/2175) vs B (381/447):
**z = 2.194, two-sided p = 0.0282**, 95% CI on the 3.96pp gap = **[0.42pp, 7.50pp]**. The gap is real at
conventional α=0.05, but only just, and the CI's lower bound is a tenth of the point estimate. The
report states P6 as a flat "HOLDS" (§7, §9) without ever printing a p-value or a CI on the A-vs-B gap
itself (it does compute a CI for the *age* effect within B, just not for the *corpus* effect between A
and B). A reader taking "HOLDS" at face value would reasonably assume more daylight between the two
rates than a p=0.028, order-of-magnitude-uncertain CI actually gives.

**Verdict: the direction and point estimate are correct and reproduce exactly; the confidence with
which "HOLDS" is asserted outruns what the same document's own standards (it computes CIs elsewhere)
would show if applied here too. This is the single most defensible complaint in this whole pass.**

### 14. Independence of corpus B (Hacker News) from corpus A (Wikipedia)

`manifest-run2.json`: `overlap_with_A: 3` out of 457 well-formed HN ids (0.66%) — I confirmed this by
direct set intersection against `corpus-merged.json`'s 2,201 keys. Negligible direct overlap; no
evidence of a shared upstream feed or copy-paste between the two corpora. This supports "different
operator, different population" as stated. What I could **not** test computationally, and the document
doesn't claim to have tested either, is a subtler form of non-independence: both a technology forum
and an encyclopedia disproportionately surface *notable/viral* content, so the two corpora may still be
correlated in *what kind* of video survives even with near-zero direct id overlap. The document doesn't
overclaim on this axis — "independent" is qualified throughout as "different operator, different
population, no link-maintenance regime," never "statistically independent samples" — so this is a
conceptual limit worth naming for a reader, not a misrepresentation in the text as written.

### 15. Pre-registration ordering / is the prefix test circular?

`git log` shows: pre-registration `1575eed` (11:20:17Z) → corpus/manifest/ledger code `4fb626b`
(11:25:52Z) → deviations D8–D11 `e786186` (11:26:52Z) → the run itself + diff `62bb659` (12:54:44Z,
committed after the run finished at 12:49:34Z). Git commit time is not, by itself, proof of causal
order (a committer could in principle stage files out of execution order), so I checked internal file
timestamps instead: `manifest-run2.json`'s own `run_id` field (generated by `time.strftime` at the
moment `build_manifest.py` ran) reads **`2026-08-11T11:24:01Z`**, five seconds before the ledger run's
own recorded `run_utc_start` (**`11:24:06Z`**) and `vantage.fetched_utc` (also `11:24:06Z`, logged
"before the first measurement request" per `ledger.py`'s own code). That five-second gap is exactly
what you'd expect from "build the manifest, then immediately launch the run that reads it" — strong,
internally-generated (not just git-metadata) evidence that the prefix classification (which arm each
id lands in, computed inside `build_manifest.py`) was fixed before a single measurement request for
run 2 went out. I could not find evidence of backdating, and the alternative (the same actor forging
both the git history and the internal timestamps consistently) is not something any static audit of
this repository can rule out — noted as a general limit of pre-registration-by-commit, not specific
evidence against this session.

**Verdict: not circular, as far as it is possible to verify from the repository's own record.**

### 16. Robots.txt claim for the second source — could NOT verify

`collect_corpus_hn.py` and `INCREMENT-1.md` §3 both state: "Neither `hn.algolia.com` nor the API host
serves a `/robots.txt` (HTTP 404 and HTTP 400 respectively...)." I fetched, live, today:
`https://hn.algolia.com/robots.txt` → 404, `https://hn.algolia.com/api/v1/robots.txt` → 404,
`https://hn.algolia.com/api/robots.txt` → 404 (with and without the stated User-Agent string). I could
not find any host actually used in this pipeline (the only endpoint the code queries is
`hn.algolia.com/api/v1/search_by_date`) that returns 400 for `/robots.txt`. `news.ycombinator.com` —
never fetched by this pipeline, only used to construct permalink strings from data already in hand —
**does** serve a real `robots.txt` (HTTP 200) with a `Crawl-delay: 30` directive, which is not honoured
because it's never queried, so this doesn't create a compliance problem, but it does mean the "HTTP 404
and HTTP 400" sentence names two response codes I could not reproduce for any host this code actually
touches. This is the one claim in the document I could not confirm and could not identify what it
refers to.

**Verdict: unverified / likely imprecise. Does not affect data collection (no robots.txt anywhere
actually disallows anything relevant), but the specific sentence should be corrected or the intended
second host named.**

### 17. Honesty-framing carried through ("this is not day 2")

Grepped the whole document for "day"/"daily series" language: §0, §6, §11, and the P/K tables are
internally consistent — every place a "day" framing could leak in is qualified ("a same-day pair
contributes at most one day," "it is one day's second run, not day 2"). I did not find a sentence that
smuggles a daily-series claim past the guard the document sets up in §0.

### 18. Anything else claimed that the data doesn't support

Nothing beyond items 6, 8/11, 13, and 16 above. Every other headline number I attempted to re-derive —
including several the task didn't explicitly list, like the vantage IP/ASN table, the 7h18m22s gap,
the sweep-completeness 288/288 result, and `probe-results.json`'s 0.33% figure used as P7's baseline —
reproduced exactly.

---

## §(b) THE HOSTILE CRITIQUE

**So what?** Strip the machinery and the actual scientific yield of this increment is: (1) an
instrument that, when asked the same question twice 7h18m apart, gave the same answer 2,147/2,147
times — a real and useful reliability result, but a null result about the world; (2) one genuinely
valuable methodological catch — a second, independently-sourced corpus would have manufactured a false
"confirmation" of the arc's own prediction if a display-truncation artefact hadn't been caught and
measured rather than silently filtered, and the arc caught it before publishing the naive number; (3)
two pre-registered predictions that failed (P5, P7), honestly reported as failures; (4) a barely
significant (p=0.028) confirmation of a prediction (P6) reported with more confidence than its own
confidence interval supports; (5) an inconclusive replication attempt on the arc's one interesting
substantive finding (the age effect), which the document itself — correctly, as I verified with a power
calculation — declines to spin as either confirmation or refutation.

**Is this slop?** No. The document does something most research writing in this genre does not: it
goes looking for its own errors and finds them (D9's backward test on corpus A's own malformed ids;
D12's 12-request follow-up that could have gone either way and the practice paid for the answer instead
of guessing). Every number I tried to break, held — including a live re-fetch of a primary source that
independently reproduced a byte-level HTML detail (the exact `href`/display-text split in HN comment
28456840) the report used as its worked example. That is not the signature of fabricated or
carelessly-asserted data. The prose is dense and self-regarding in its constructed style, but the
underlying arithmetic is careful.

**Would a critic tear it apart?** A sharp critic has three real openings, in descending order of bite:

1. *"You've spent an entire increment proving your thermometer doesn't move when you look at it twice
   in one afternoon."* The document says this about itself, almost verbatim, in §6 — "the first
   evidence this arc has produced... supports the critic, not us." A critic cannot improve on a charge
   the target has already conceded in its own words. What the critic *can* still press is: conceding
   the charge is not the same as answering it, and the arc is now two full sessions into an
   eight-increment gate with its central research question (does content actually disappear over time,
   and at what rate) still completely unaddressed by any dated event. The seven-day kill is the arc's
   own admission that it may have nothing.
2. *"Your one significant finding is barely significant."* P6's 3.96pp gap is real at p=0.028, but a
   critic reading only "HOLDS" would not guess the CI reaches down to 0.42pp. A document this careful
   about hedging the age-effect non-replication should hold P6 to the same standard rather than state
   it flatly.
3. *A minor scavenger-hunt find*: one process claim (the HN robots.txt response codes) doesn't survive
   an independent check, and doesn't matter to anything downstream — but it's exactly the kind of loose
   thread a critic clips first to cast doubt on everything else, disproportionate to its actual weight.

None of these are fatal. All are fixable with a sentence or two, and none touch a headline number.

---

## Conditions this pass would attach

1. **P6's headline gap needs its own uncertainty stated**, not just the age-effect's. Report the
   two-proportion z-test / CI on 85.23% vs 89.20% (z=2.19, p=0.028, 95% CI on the gap [0.42pp, 7.50pp])
   alongside "HOLDS," the same way the age-effect section already reports its own CI.
2. **Correct "the prediction and the measurement agree on every row"** (§8) to something like "no row
   contradicted the prediction" — the 3 INDETERMINATE rows among the 248 predicted-phantom ids are
   non-results, not agreements.
3. **Resolve the P5 denominator inconsistency**: corpus A's 69.7% counts its 4 non-19-digit ids in the
   denominator; corpus B's 61.7% excludes its 249 phantom ids from its denominator. State which
   convention is used, or recompute both the same way (well-formed-only gives corpus A 69.9%, which
   doesn't change P5's outcome but changes the reported number).
4. **Verify or correct the robots.txt sentence** in `collect_corpus_hn.py` / `INCREMENT-1.md` §3 —
   every host actually queried by this pipeline returned 404, not 400, for `/robots.txt` when checked
   live today; identify what "the API host" (distinct from `hn.algolia.com`) was meant to refer to, or
   fix the sentence.
5. **`legacy-id-control.json` has no accompanying script and no raw response bodies** — bring D12's
   control up to the same reproducibility bar (script + raw JSON) the rest of the arc holds itself to,
   given it's the evidence for a real-vs-false-positive call that "would bound every retrievability
   figure this arc has published" if it went the other way.

None of these conditions change a conclusion in the document. All of them are about calibrating
confidence language to match the arithmetic underneath it, which — every time I checked it against the
raw files myself — was correct.

---

**VERDICT: STANDS WITH CONDITIONS**

1. State a confidence interval / significance level for the P6 corpus-A-vs-B gap (85.23% vs 89.20%),
   not just for the within-B age effect.
2. Correct "agree on every row" (§8) to reflect that the 3 INDETERMINATE prefix rows are inconclusive,
   not confirmatory.
3. Make the P5 percentages' denominators consistent between corpus A and corpus B, or state explicitly
   which convention each uses.
4. Verify or correct the Hacker News robots.txt claim ("HTTP 404 and HTTP 400 respectively") — not
   reproducible against any host this pipeline actually queries.
5. Bring `legacy-id-control.json` (D12) up to the arc's own reproducibility standard: a script and raw
   response bodies, not curated summary fields only.
