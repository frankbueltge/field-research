# VERIFIER-120 — independent check of the session-120 bundle at commit `93855be`

**VERDICT: SOUND WITH QUALIFICATION** — every figure in the bundle reproduces exactly from the run
files under independent code, and no fabricated datum was found; but eighteen prose, provenance and
metadata defects are listed below, of which four (F1, F2, F3, F4) are factual errors in
receiver-facing text and one (F1) will silently mislead anyone who uses the shipped tool.

*Checked against the data and the sources, not against the argument. All recomputation was written
from scratch in `/tmp/.../scratchpad/v120/` (`recompute.py`, `checkjson.py`); nothing in the
repository was imported, and no repository file was modified. No request was made to the platform
endpoint from any tool in this review.*

---

## PART A — what reproduced, exactly

### F0-a. Every number in `deliverable/FIGURES.md` §§1–6

**Checked:** pooled and per-band absence rates and Wilson intervals for all four days; the
across-day spread; the crossed stratum×band table; the stratum table; the exclusion counts; the
changed-unit table; the transport-noise table; the six day-pair overlaps.

**Code:** `recompute.py` — own reader of `ledger/baseline-union.json` and the three complete
`run-*.json` files, own `band_of`, own Wilson score interval (`z = 1.959963984540054`), own
stratum map. Run as `python3 recompute.py` from the draft directory.

**Result: 0 mismatches.** Every one of the following reproduced to the printed precision:

| FIGURES.md states | I computed |
|---|---|
| baseline 3581 in rate, 437 absent, 12.20 %, [11.17 %, 13.32 %] | identical |
| 2026-08-12 3582 / 437 / 12.20 % / [11.17 %, 13.31 %] | identical |
| 2026-08-13 3576 / 439 / 12.28 % / [11.24 %, 13.39 %] | identical |
| 2026-08-14 3583 / 435 / 12.14 % / [11.11 %, 13.25 %] | identical |
| spread 12.14 %–12.28 %, 0.14 pp | 0.13562 pp → 0.14 pp |
| six age bands on 2026-08-14: n = 500/771/795/670/456/384, absent 24/59/96/109/74/68 | identical |
| band spreads 0.25 / 0.26 / 0.42 / 0.32 / 0.29 / 0.35 pp | identical |
| all 18 crossed stratum×band cells | identical |
| strata 446/64, 2375/259, 762/112 | identical |
| exclusions 249 / 37 / 7 | identical |
| 5 of 3620 raw changers, 3 after overlay, and all five identifiers with their four states | identical |
| INDETERMINATE 42 / 40 / 47 / 40 and shares 1.09 / 1.03 / 1.21 / 1.03 % | identical |
| day-pair overlaps 0, 1, 0, 0, 1, 1 | identical |

**Disposition: no action.**

### F0-b. `gradient-test.json` — two-sided Fisher exact

**Checked:** all four tests, recomputed with exact rational arithmetic (`fractions.Fraction` over
`math.comb`, summing every table whose hypergeometric probability is ≤ the observed one), so the
comparison is against exact values rather than against their float implementation.

| group | document | my exact recomputation |
|---|---|---|
| pooled 24/500 vs 68/384 | `6.446636838056336e-10` | `6.446637e-10` |
| F-forum 2/50 vs 8/54 | `0.0949480273148097` | `9.494803e-02` |
| W-article 16/308 vs 47/266 | `1.8035510480786782e-06` | `1.803551e-06` |
| W-other-ns 6/142 vs 13/64 | `0.0004942478835822774` | `4.942479e-04` |

Ratios 3.689 / 3.704 / 3.401 / 4.807 all reproduce. **Disposition: no action.** The prose reading —
significance in two strata and not in the third, whose cells hold 50 and 54 — is correct.

### F0-c. `expectation.json` and `reference-baseline.json`, cell by cell

**Checked:** a full recursive deep-diff of my independently built tables against every cell of
`per_day` (4 days × pooled + by_age_band + by_stratum + by_year + by_stratum_band + excluded),
`across_day_stability`, and the whole `corrected_arm` sub-tree; plus every cell of
`reference-baseline.json`.

**Code:** `checkjson.py`.

**Result: 0 structural or count differences.** The only numeric differences are in the Wilson
bounds, at ≤ 3.3 × 10⁻¹¹ relative — traced to their `z = 1.959963985` (`power_audit.wilson`) against
the exact 1.959963984540054. Immaterial at every printed precision. **Disposition: no action**
(optionally state the z constant in `LIMITS.md` §5).

### F0-d. Exclusion logic, verified by counting rather than by reading

**Checked:** (i) `B-truncated` excluded from every rate; (ii) `INDETERMINATE` excluded and counted;
(iii) non-19-digit identifiers excluded from age-banded rates only, present in the series.

**Result:**
- 249 `B-truncated` units, present in all four runs, **none of them 19 digits** (length 5–18);
  excluded from every rate in all four days. Correct.
- INDETERMINATE excluded and counted every day. Correct (but see **F5** for how it is *reported*).
- Exactly **7** non-19-digit non-control identifiers, the same seven every day —
  `194951213564514304`, `677767122007582643`, `726459750741134635`, `740580884959830349` (arm A,
  matching the run file's own `malformed_kept`), `27191084`, `70`, `78647522683981824` (arm A2).
  All seven are present in `presence-series.csv`/`.json` and absent from every age band. Correct.
- No 19-digit identifier decodes to a non-positive age or to ≥ 99 y, so no unit is silently dropped
  by `band_of` returning `None` for any other reason.

**Disposition: no action.**

### F0-e. The corrections overlay is applied exactly where `corrections.json` says, and nowhere else

**Checked:** `diff presence-series.csv presence-series-corrected.csv`, plus a full-population
recomputation of the corrected arm from the run files and the overlay rule.

**Result:** exactly **two** differing cells in 15,476:
`7016669364938149122` in the `2026-08-14` column and `7368171405361351954` in the `2026-08-13`
column — precisely the (run_file, vid) pairs the overlay names, each applied only because the run
file actually carries `NOT-RETRIEVABLE`. `presence-series.json → corrections_overlay` reports
`rows_available: 2`, `rows_applied: 2`, both named with their authority. `LIMITS.md` §10's "the
overlay holds two rows, both named" is exact. **Disposition: no action** on the arithmetic; see
**F16** for the overlay's deviation record.

### F0-f. No archived run file was edited; `MANIFEST.json` hashes are correct

**Command:** own sha256 of each named file; `git log --diff-filter=AMD` and `--diff-filter=M` over
`ledger/`.

**Result:** all five sha256 values in `MANIFEST.json` match the files on disk exactly
(`baseline-union.json`, the three run files, `corrections.json`). In git history each complete run
file has exactly one commit with status **A** and **no M** anywhere. The only ledger files ever
modified are `*.partial` files and `dayN-std{out,err}.txt`. The bundle correctly ignores
`run-2026-08-15T0337Z.json.partial` (and the two older `.partial` files): my own discovery, which
requires `endswith(".json")`, excludes them independently. **Disposition: no action**; see **F14**
for what the manifest omits.

### F0-g. CSV ↔ JSON ↔ run files

**Checked:** a 65-identifier sample (60 drawn with my own seed 20260815, plus all five identifiers
the bundle names in prose in `FIGURES.md` §5 and both overlay rows), then the **whole population**.

**Result:** 0 mismatches on the sample across arm, stratum, `created_utc` (independently recomputed
as `int(vid) >> 32`), `age_y_at_baseline`, band, and all four day columns in both arms. Extended to
all 3,869 units × 4 days: **0 mismatches in 15,476 cells** for the raw arm and **0** for the
corrected arm. CSV row count 3,869, JSON `n_units` 3,869, both consistent with the run files.
**Disposition: no action.**

### F0-h. The bundle rebuilds byte-for-byte

**Command:** `python3 build_deliverable.py --out <scratch>` from the draft directory.

**Result:** `expectation.json`, `gradient-test.json`, `reference-baseline.json`, and all three
`series/` files are **byte-identical**. `FIGURES.md` and `MANIFEST.json` differ only in their own
build timestamp (`03:56:21Z` → `04:03:21Z`). README §5's reproducibility claim is true as stated —
but see **F11** for why the receiver cannot exercise it.

### F0-i. `receiver-eleven.md` against its two sources

**Checked:** every cell against `presence-check-receiver-113.json` and
`receiver-arm-2026-08-12.json`, and the three day-count columns against the per-identifier total.

**Result:** all eleven states, decoded creation times, bands and returned handles match
`presence-check-receiver-113.json` exactly. All eleven `receiver_own_dashboard` blocks match
`receiver-arm-2026-08-12.json` exactly. **The three day columns sum to the first column for all
eleven** (ten × 279, one × 238); the "totals here are 238, 279" note is exact; "between 14 and 20
days of error" is exact (min 14, max 20); "10 of the 11 never once recorded as available" is exact.
Cross-checked against `drafts/2026-08-10-one-receiver-to-the-floor/dashboard-derived-raw.txt`, whose
independently derived totals (3,028 video-days; Available 213; Error 181; NotAvailable 2,634;
"NEVER once returned: 10 of 11") all reconcile with the per-identifier table. The observed
expectation `0.1376986368862619 [0.1139, 0.1655]` reproduces exactly from
`run-2026-08-12T0341Z.json` under the age profile {2-3y:7, 3-4y:2, 4-5y:2} using the run's own start
as reference time, and the stated reference `n = 3575` equals 3582 in-rate minus the 7 undatable.
**Disposition: no action** on the arithmetic; see **F10**.

### F0-j. External sources

| Claim | Source I retrieved | Result |
|---|---|---|
| dashboard generated `2026-01-14 21:53:41` | `https://playground.tiktok-audit.com/api-na/`, fetched 2026-08-15 | **confirmed verbatim** |
| `11 Total Videos Tracked, 0 Available, 0 Unavailable, 11 Videos with Errors` | same | **confirmed** |
| `"Note: Error are problems on our end, not TikTok."` | same | **confirmed verbatim, punctuation included** |
| the eleven identifiers | same | **all eleven confirmed, in the same order as `receiver-eleven.md`** |
| `"should be available through the Research API but were not"` | `receiver-report-2506.09746v2-extracted.txt` (arXiv:2506.09746) | **found verbatim** |
| `"without an apparent reason"` | same | **found verbatim** — but see **F9** for its scope |
| arXiv:2601.12390, submitted 2026-01-18 | arXiv record | **confirmed**, 2026-01-18T12:59:11Z |
| "~50 % exclusion, ~83 % metadata loss, ~1,000 requests/day, two sockpuppet accounts, two election periods, TikTok Research API and Meta Content Library" | arXiv:2601.12390 abstract | **all six confirmed** |
| FAccT '26, 25 June 2026, pp. 8276–8299, title *Platforms' Research API Data Access…* | `api.crossref.org/works/10.1145/3805689.3812237` | **all confirmed independently** |
| `dl.acm.org/doi/10.1145/3805689.3812237` returns 403 | own `curl` | **confirmed, HTTP 403** |
| catalogue counts 1,116 / 505 / 59 | `frankbueltge.de/papers/index.json`, `/atlas/werke.json`, `/datasets/register.json`, fetched by me | **1116 / 505 / 59 — exact** |
| atlas returns nothing on the term list except ten unrelated "decay" hits | own re-run of the 15-term search over the full JSON of every entry | **exact: 0 on all 14 other terms, exactly 10 decay hits, all net-art works; both named examples confirmed** |
| register of 59 returns nothing on any term | same | **exact: 0 on all 15 terms** |
| `LIMITS.md` §1: no HTTP 404 was ever returned | own scan of every archived run file | **confirmed**: 14,900 × 200, 3,275 × 400, 205 transport failures, **zero 404** |
| `LIMITS.md` §2: vantage logged before the first request of each run | own check of `vantage.fetched_utc` vs `run_utc_start` | **confirmed for all three window runs and the 11:24 component** (the union carries no `fetched_utc`, correctly, since it is not a run) |

---

## PART B — findings requiring disposition

### F1. `reference-baseline.json → t_ref_utc` names a reference time the table was not built with, and the shipped tool ages a caller's list at *now* against a reference frozen at 2026-08-11 — MATERIAL, undisclosed

**What I checked.** `build_deliverable.py` computes every unit's age once, at
`t_ref = days[0]["utc_start"]` = **2026-08-11T11:24:06Z** (line 179). `reference-baseline.json` then
writes `"t_ref_utc": newest["utc_start"]` = **2026-08-14T03:43:47Z** (line 372). I rebuilt the
2026-08-14 `by_age_band` table under both reference times and compared with the shipped file.

**Document states:** `"t_ref_utc": "2026-08-14T03:43:47Z"`.
**I computed:** the shipped table is the one produced at t_ref = 2026-08-11T11:24:06Z, **2.680 days
earlier**. Under the declared t_ref the band sizes would be 499/766/793/673/457/388 instead of the
shipped **500/771/795/670/456/384**. **24 identifiers of that day's panel fall in a different age
band** under the declared reference time than under the one actually used.

**Why it is more than cosmetic.** `presence_check.py` line 191 sets `t_ref = now` and never reads
`t_ref_utc`. So a re-user's identifiers are aged at the moment they run the tool, then matched
against a reference table whose own ages are frozen at 2026-08-11. On 2026-08-15 that is a ~3.7-day
offset (29 of the day-4 panel would band differently). A year from now it is a **one-year** offset:
the caller's list is pushed a whole band older against a static reference whose rates rise
monotonically with band, so the returned expectation inflates without bound and without warning.
`README.md` §4, `LIMITS.md` §6 and `LIMITS.md` §7 say nothing about this.

**Disposition required.** (a) Correct `t_ref_utc` to `2026-08-11T11:24:06Z`, or rebuild the age
columns at the newest day's start so the field is true. (b) Add a present-tense limit to
`LIMITS.md`: *the reference table's ages are fixed at the date in `t_ref_utc`; the tool ages your
list at the moment you run it; the two drift apart at one year per year, and the expectation should
not be used once the drift is comparable to a band width.* (c) Either make the tool read
`t_ref_utc`, or state in `README.md` §4 that it does not.

### F2. "21 language editions" is wrong in three receiver-facing places; the real number is at least 37 and, across all collection rounds, 61

**What I checked.** I traced every panel identifier back to the collection file it came from —
the 45 `corpus-*.wikipedia.org.json` files (arms A and A-new, article space) and
`expansion-111/corpus-A2-namespaces.json`, `corpus-round2.json`, `corpus-round3.json` (arm A2 and
the round-2/3 additions, which carry an explicit `wiki` field) — intersected with the 3,869
identifiers in `ledger/manifest-2026-08-12.json`.

**Document states:** `README.md` §6 and `LIMITS.md` §4: "the article and non-article namespaces of
**21** language editions of one public encyclopedia". `FIGURES.md` §4: "article space of **21**
encyclopedia language editions".

**I computed:** **37** distinct language editions contribute identifiers to the panel through the
article-space corpus alone (`en, ja, es, he, id, de, pt, uk, ru, zh, tr, ms, pl, it, ar, ko, nl, vi,
fi, hy, th, fa, sv, cs, uz, ka, tl, gl, bn, mk, ur, sq, ta, te, fr, hi, ne`), and **61** across all
collection rounds — 3,166 of the panel's identifiers are traceable to a named edition. The run
file's own `arms` metadata says so directly: arm `A-new` is "language editions **not queried at
session 109**", round 2 is "18 wikis round 1 never reached + 29 editions round 1 lost to HTTP 429",
round 3 is "the 14 wikis round 2 did not reach". `EXPANSION-111.md` §2 states 45 editions attempted
for A-new alone. The number 21 describes only arm A's session-109 article-space collection (2,201 of
3,620 non-control units); it does not describe the panel.

The practice already knows this: the shipped tool's own output text says "**21+** MediaWiki language
editions", and `presence-check-receiver-113.json` carries that "+". The bundle's prose drops it.

**Disposition required.** Replace "21" with the counted number in `README.md` §6, `LIMITS.md` §4 and
the `what` map in `build_deliverable.py` (which hard-codes these strings, so the correction must be
made in the generator, not in the output). Note that this also qualifies `INCREMENT-10.md` §3's
"No figure in the bundle is typed by a human" — this one is, and it is wrong.

### F3. `LIMITS.md` §1 states the synthetic control at 20/20; the data is 19/20

**What I checked.** `reverify-results.json → arm_c`, the three-arm control's synthetic arm.

**Document states:** "A three-arm control run on 2026-08-11 with **twenty synthetic identifiers that
never existed** returned exactly the same code as identifiers that certainly did exist".

**I computed:** arm_c holds 20 rows. **19** returned `http 400`, `code 400`, `message "Something went
wrong"`. The twentieth, `7512505100479546335`, returned **no code at all** —
`URLError: <urlopen error _ssl.c:999: The handshake operation timed out>`, i.e. an INDETERMINATE
transport failure. The arc's own `RESULT.md` line 66 states it correctly: "**19 of 20** synthetic
identifiers … returned the same 400 and the same body."

The bundle rounds 19/20 to 20/20 in the single limit that `README.md` §7 and `LETTER.md` require to
travel with every re-use of every number. The conclusion is unaffected — 19/19 of the determinate
synthetic requests returned the identical refusal — but the sentence as written claims a datum that
does not exist.

**Disposition required.** Restate as "nineteen of twenty synthetic identifiers … the twentieth ended
in a transport failure and returned no code", matching `RESULT.md`.

### F4. `README.md` §6 misstates the platform's `robots.txt`

**What I checked.** `tiktok-robots-2026-08-11.txt` (the file the practice itself fetched and saved,
1,288 bytes) line by line.

**Document states:** "the platform's `robots.txt` disallows the major public web crawlers, and the
largest free public crawl holds, for this domain, only `/robots.txt` entries and no video pages."

**I found:** the `Disallow: /` block covers 25 named agents — five regional search crawlers
(Baiduspider, 360Spider, Sogouspider, Yisouspider, PetalBot), Bytespider, **CCBot**, and eighteen
LLM/assistant agents. **Googlebot is not restricted at all. Bingbot is disallowed only `/discover`.**
The `User-agent: *` block explicitly *Allows* `/foryou`, `/tag`, `/share`, `/music` and others, and
does **not** disallow `/@handle/video/<id>`. So "the major public web crawlers" is false; what is
true, and what the argument actually needs, is that the crawler of the **largest free public crawl**
(CCBot) is disallowed.

Second, the Common Crawl finding in `DERIVED.md` §1 is scoped to one collection —
`CC-MAIN-2026-30`, one 258 kB CDX block, 339 entries for the domain, 339/339 `/robots.txt`, 0 video
pages. `README.md` states it as an undated property of "the largest free public crawl".

**Disposition required.** Rewrite the sentence to what the saved file supports, and date the crawl
finding to its collection.

### F5. `FIGURES.md` gives two different INDETERMINATE counts for the same day without saying why

**What I checked.** Both figures, recomputed.

**Document states:** §4, for 2026-08-14: "**37** observations that ended in a transport failure".
§6, for 2026-08-14: "INDETERMINATE **40**", share 1.03 %.

**I computed:** both are right under different definitions. §4 counts INDETERMINATE **after**
`B-truncated` has already been dropped (37 = 40 − 3 control-arm transport failures); §6 counts all
units, control arm included, over a denominator of 3,869. The same is true on every day
(39/42, 38/40, 44/47, 37/40). Nothing on the page tells the reader this, and the two numbers sit
twenty-five lines apart on a page headed "generated, do not hand-edit".

**Disposition required.** Label the §6 column "including the `B-truncated` control arm", or report
both series. This is a generator change in `build_deliverable.py`.

### F6. The session's own novelty narrowing did not reach the two documents a receiver will actually read

**What I checked.** `grep -ri "bekavac|mayer|2601.12390|FAccT|sockpuppet|Content Library"` over the
whole of `deliverable/`.

**Result: zero hits.** `NEIGHBOURS-120.md` §1 and `INCREMENT-10.md` §2 both find that
`CONCEPT.md`'s "no one is running" is **too strong**, and both name the work that runs a version of
the public-side half. That work is named nowhere in the bundle. Meanwhile:

- `LETTER.md`: "**The control arm is free, and as far as we could find, nobody was running it.**" —
  un-narrowed, and it is the sentence the letter is built around.
- `LIMITS.md` §3: "this is the half that is free, **and it was not being run**." — un-narrowed, in
  the file the README declares load-bearing.
- `README.md` §1: "it was not being run **as a continuous, published series**" — this one *is* the
  narrowed form and is correct.

The practice found the neighbour, wrote the narrowing down twice, and then shipped two of three
statements in the unnarrowed form, in the documents most likely to travel alone.

**Disposition required.** Bring `LETTER.md` and `LIMITS.md` §3 to the `README.md` §1 wording, and
cite arXiv:2601.12390 / 10.1145/3805689.3812237 once in the bundle — the letter is addressed to
people who work in this exact area and will know the paper.

### F7. `LETTER.md` attributes "eleven videos" to the receiver's own words; their report says ten

**Document states:** "a public dashboard doing a daily availability check on **eleven** videos that,
in your own words, *'should be available through the Research API but were not'*."

**Source says** (arXiv:2506.09746, verbatim): "we publish a dashboard with a daily check of the
availability of **10 videos** that were not retrievable in the last month."

The dashboard itself tracks eleven (I confirmed eleven identifiers live). Both facts are true; the
sentence fuses them so that "eleven" reads as the receiver's own count inside a quotation frame.
The quoted clause itself is verbatim and correctly in context.

**Disposition required.** Reword: "a public dashboard that your report describes as a daily check of
ten videos and that today tracks eleven".

### F8. `LETTER.md` attributes to the report a statement the report does not make

**Document states:** "Your report states the limit of that instrument plainly, and so does the
dashboard page itself: > *'Note: Error are problems on our end, not TikTok.'*"

**I checked:** whitespace-normalised full-text search of the extracted report for `our end`, `our own
error`, `on our side`. **No match.** The report discusses limitations of the *Research API*
throughout; it contains no statement about the dashboard monitor's own error mode. That limit is
stated only on the dashboard page.

**Disposition required.** Drop "Your report states the limit of that instrument plainly, and so
does" — the dashboard quotation alone carries the point, and it is verified.

### F9. "without an apparent reason" is used at a scope the source does not give it

**Document states** (both `LETTER.md` and `receiver-eleven.md`): "your words for the interface's
behaviour **on these videos** are *'without an apparent reason'*, which presumes the videos are
there."

**Source, in full context:** "the API fails to provide metadata for **one in eight videos provided
through data donations**, including official TikTok videos, advertisements, and content from
specific accounts, without an apparent reason."

The phrase describes the API's behaviour across the data-donation corpus (~260k posts), not a
statement made about these eleven. The generalisation is defensible — the report says the dashboard
videos were selected from "the lists of videos that were not available" in that same experiment —
but it is an inference, and the bundle presents it as their words about these videos.

**Disposition required.** Attribute the phrase to what it describes: "your words for the interface's
behaviour across the donated corpus these videos were drawn from".

### F10. `receiver-eleven.json` claims to hold "every dated reading" and does not

**Document states:** `what_this_is`: "**every dated reading** this practice has taken of the eleven
identifiers the receiver's own public dashboard tracks."

**I found:** two dated readings of the eleven exist on disk for 2026-08-12 —
`receiver-arm-2026-08-12.json`, started **05:31:17Z**, and `presence-check-receiver-113.json`,
started **18:35:26Z**. Only the second is in `readings`. `receiver_series.py` accepts only
`field-research/presence-check/1` inputs, so the arm-R run is structurally excluded. Both readings
agree exactly (10 RETRIEVABLE / 1 NOT-RETRIEVABLE, the same identifier absent), so nothing numeric
changes — but the claim is false as written, and the 05:31 file is the very file the page's other
three columns come from.

**Disposition required.** Either include the arm-R reading or soften to "every reading taken with
`presence_check.py`", and note in `receiver-eleven.md` that the eleven were measured twice on
2026-08-12 with identical results (which is a small piece of evidence for the bundle, not against
it).

### F11. `README.md` §5 tells the receiver to re-run a script the bundle does not contain

**Document states:** "`FIGURES.md` is generated. **Re-run `build_deliverable.py`** against the run
files and it must reproduce byte for byte."

**I found:** `deliverable/` contains `tools/{presence_check,ledger,power_audit}.py` and nothing else
executable. `build_deliverable.py` is not in the bundle, and neither are the run files. The claim is
true (I verified it — see F0-h) but is not a check the bundle's holder can perform.

**Disposition required.** Ship `build_deliverable.py` in `tools/`, or reword to say where it lives
and that the run files must be fetched from the public record first.

### F12. `README.md` §2 misdescribes `tools/power_audit.py`

**Document states:** "`tools/ledger.py` · `tools/power_audit.py` | the probe and the interval
arithmetic **the tool imports**".

**I found:** `presence_check.py` imports `ledger` only; `ledger.py` imports stdlib only.
`power_audit` is imported by `build_deliverable.py`, which is not in the bundle. As shipped,
`power_audit.py` is unreachable from anything in `deliverable/`.

**Disposition required.** Correct the description, or ship the script that actually imports it.

### F13. `MANIFEST.json` publishes an unfilled placeholder as a source run's identity

**Document states:** for `ledger/run-2026-08-13T0427Z.json`,
`"run_id": "TEMPLATE — the running session sets this"`; for the 2026-08-14 run,
`"run_id": "2026-08-14T03:43:47Z (manifest carried a placeholder)"`.

This is faithful to the archived files (which must not be edited), but it means the receiver-facing
provenance file names a source run "TEMPLATE". `DEVIATIONS.md` D22 records that `ledger.py` was
changed to *refuse* a placeholder `run_id` — the day-3 file predates that guard.

**Disposition required.** Add a `run_id_note` in the manifest pointing at D22, so the placeholder
reads as a disclosed instrument defect rather than an unfilled field.

### F14. The manifest's own claim to name "every source run file" is not met for the baseline

**Document states:** `README.md` §5: "`MANIFEST.json` names **every source run file** with its
sha256."

**I found:** the `baseline` row of `MANIFEST.json` names only `ledger/baseline-union.json`. That
file is not a run: its own `components` field lists **four** producing runs —
`ledger/run-2026-08-11T1124Z.json` (2,904 obs, 11:24:06Z), `expansion-111/baseline-run.json` (635),
`baseline-run2.json` (304), `baseline-run3.json` (26) — spanning **11 h 41 m**, to 23:05:18Z. None of
the four is named or hashed in the manifest, and three of them are outside `ledger/` entirely.

Related, and reader-facing: `FIGURES.md` §1 renders that union as a single row —
"baseline | 2026-08-11T11:24:06Z | 3869" — with one start time and no end time. A reader has no way
to see that the baseline "day" is four runs over half a day, or that 965 of the 3,869 units were
first measured 11 hours after the timestamp shown. Ages are computed against 11:24:06Z for all of
them.

**Disposition required.** List the four component files with their sha256 under the baseline row,
and add the union's `utc_end` (or a "measurement window" column) to `FIGURES.md` §1.

### F15. `FIGURES.md` never says which arm its tables are

**What I checked.** The page carries no arm label on §§1–4 or §6. `gradient-test.json` correctly
declares `"arm": "raw run file (primary record)"`; `FIGURES.md` does not.

**I computed** the size of what is unlabelled: pooled 2026-08-14 raw 435/3583 = 12.141 %, corrected
434/3583 = 12.113 %; 2026-08-13 raw 439/3576 = 12.276 %, corrected 438/3576 = 12.248 %; band 4-5y on
2026-08-14 raw 74/456 = 16.23 %, corrected 73/456 = 16.01 %. Differences ≤ 0.22 pp — immaterial to
every conclusion, which is exactly why the label costs nothing.

**Disposition required.** One generated line under the §1 heading: "All tables on this page are the
raw arm — the run files as returned. The overlay-corrected arm is in `expectation.json →
corrected_arm` and `series/presence-series-corrected.csv`."

### F16. The overlay cites a deviation number that belongs to a different deviation, and has no record of its own

**What I checked.** `ledger/corrections.json` declares
`"deviation": "D23 — bookkeeping only; no probe and no archived run file changes"`.
`DEVIATIONS.md` **D23** is "session 118: post-hoc analyses beside a pre-registration, declared as
post-hoc" — an unrelated matter. `DEVIATIONS.md` ends at **D24**, and a grep for `overlay` or
`corrections.json` across the file returns **nothing**.

So the mechanism `LIMITS.md` §10 and `README.md` condition 3 make load-bearing has no deviation
record, and points at one that is already taken.

**Disposition required.** Open a new deviation (D25) for the overlay and correct the reference in
`corrections.json`. Note that `corrections.json` is hashed in the manifest, so the fix must be a
dated re-issue with a new hash, not a silent edit.

### F17. "Unmodified since it was written" is not what the file says about itself

**Document states:** `README.md` §2: "`tools/presence_check.py` | … **Unmodified since it was
written**."

**I found:** the bundle copy is byte-identical to the repository copy (sha256
`ae8fc947e6b7e7a12d646c282e49991cc6433640a0256acefdd0fa1eff6caa1d`), and in the retrievable git
history the file has exactly one commit, status A — so *whether it was modified before that commit
is* **UNCHECKABLE FROM HERE**: the history is squashed (see `notes/2026-07-12-history-rewrite-map.md`).
What is checkable is that the file's own lines 52–58 record a correction: "**CORRECTED session 113**,
condition 3 … The floor was `\d{6,25}`, which SILENTLY dropped `12345`". The intended claim is
plainly "not modified for this bundle", which is true and verified.

**Disposition required.** Reword to "unmodified for this bundle — it is the same file, byte for
byte, that measured every row of our own ledger", which is the claim that matters and is provable.

### F18. `NEIGHBOURS-120.md` sources the FAccT record to an unnamed "search index" when a retrievable source confirms it

**Document states:** "publisher page HTTP 403 from here, so the bibliographic detail is from **a
search index**".

**I checked:** `dl.acm.org/doi/10.1145/3805689.3812237` does return **HTTP 403** from this network —
confirmed, and the document is right to say so. But `api.crossref.org/works/10.1145/3805689.3812237`
answers HTTP 200 and confirms **every** disputed detail: title *Platforms' Research API Data Access:
What Users See vs. What Researchers can Retrieve*, authors Bekavac and Mayer, container *Proceedings
of the 2026 ACM Conference on Fairness, Accountability, and Transparency*, pages **8276-8299**,
issued **2026-06-25**, event FAccT '26 Montreal. The arXiv record independently carries the same
DOI and journal reference, which is what licenses the preprint↔publication identification.

So the claim is sound; the citation is not, because an unnamed search index is not a retrievable
source. (Related, and not the document's fault: the house paper register carries this one work
**twice** — once as `arXiv:2601.12390` under the preprint title, once as `10.1145/3805689.3812237`
under the published title — which is a catalogue duplicate worth reporting to the register.)

**Disposition required.** Name Crossref, with the URL, in place of "a search index".

### Minor observations, no disposition required

- `FIGURES.md` §3 calls 3-4y → 4-5y (16.27 % → 16.23 %) "one flat step". It is a 0.04 pp *decrease*.
  "Flat" is fair against the interval widths; "one step that does not rise" would be exact.
- `README.md` §3(b) "roughly a quarter the rate": 4.80/17.71 = 0.271. Fair.
- `README.md` §3(a) "stable to a tenth of a percentage point": spread 0.1356 pp. Fair.
- `INCREMENT-10.md` is headed "Increment 11"; the file declares the offset itself.
- `expectation.json`'s `by_age_band` for 2026-08-12 (t_ref = baseline) and the expectation embedded
  in `presence-check-receiver-113.json` (t_ref = that run's own start) use different reference times
  and therefore different band sizes (e.g. 2-3y n = 795 vs 790). Both are internally correct; the
  bundle does not say they differ. Folded into **F1**.

---

## CONDITIONS

The collective must discharge these before this bundle ships. Each is falsifiable and each names the
file to change.

1. **Fix `reference-baseline.json → t_ref_utc`** to the reference time the age columns were actually
   computed with (`2026-08-11T11:24:06Z`), or rebuild those columns at the declared time. Verify by
   recomputing the six band sizes and showing they equal the shipped 500/771/795/670/456/384. (F1)
2. **Add a present-tense limit to `LIMITS.md`** stating that the reference table's ages are frozen at
   `t_ref_utc` while `presence_check.py` ages the caller's list at run time, that the two drift at
   one year per year, and at what drift the expectation should no longer be used. Cross-reference it
   from `README.md` §4. (F1)
3. **Replace "21 language editions"** with the counted figure in `README.md` §6, `LIMITS.md` §4 and
   the `what` map in `build_deliverable.py`; publish the per-edition count so the number is checkable
   rather than asserted. My count: 37 editions in article space, 61 across all rounds. (F2)
4. **Restate `LIMITS.md` §1 as 19 of 20**, matching `RESULT.md` and `reverify-results.json → arm_c`,
   and name the twentieth identifier's transport failure. (F3)
5. **Rewrite `README.md` §6's `robots.txt` sentence** to what the saved file supports (CCBot and 24
   other named agents disallowed; Googlebot unrestricted; Bingbot restricted only on `/discover`),
   and date the Common Crawl finding to collection `CC-MAIN-2026-30`. (F4)
6. **Disambiguate the two INDETERMINATE counts** in `FIGURES.md` §§4 and 6 in the generator, so the
   page cannot show 37 and 40 for the same day without saying why. (F5)
7. **Propagate the neighbour narrowing** into `LETTER.md` and `LIMITS.md` §3, and cite
   arXiv:2601.12390 / 10.1145/3805689.3812237 once in the bundle. The letter's central sentence
   currently claims more than the session's own neighbour check allows. (F6)
8. **Correct the three receiver-attribution defects in `LETTER.md` and `receiver-eleven.md`**: the
   "eleven videos" fusion (their report says ten), the claim that their report states the dashboard's
   own error limit (it does not), and the scope of "without an apparent reason". (F7, F8, F9)
9. **Make `receiver-eleven.json`'s "every dated reading" true**, either by including the
   2026-08-12T05:31:17Z arm-R reading or by narrowing the sentence; and record in the page that the
   eleven were measured twice that day with identical results. (F10)
10. **Ship `build_deliverable.py` in `tools/`** (or reword `README.md` §5), and correct §2's claim
    that the tool imports `power_audit.py`. (F11, F12)
11. **Name the baseline union's four component run files with their sha256** in `MANIFEST.json`, and
    show the baseline's measurement window (11:24:06Z–23:05:18Z) in `FIGURES.md` §1, so §5's "every
    source run file" is true and the baseline row is not read as a single instant. (F13, F14)
12. **Label the arm on `FIGURES.md`** — one generated line saying the tables are the raw run files and
    naming where the corrected arm lives. (F15)
13. **Open a deviation for the corrections overlay** and correct `corrections.json`'s reference away
    from D23; re-issue the file with a new dated hash and update `MANIFEST.json`. (F16)
14. **Reword "Unmodified since it was written"** to the provable claim ("unmodified for this bundle;
    byte-identical to the file that measured every row of our own ledger"), given the file's own
    record of a session-113 correction. (F17)
15. **Name Crossref as the source** of the FAccT bibliographic detail in `NEIGHBOURS-120.md`, and
    report the duplicate register entry for arXiv:2601.12390 / 10.1145/3805689.3812237 to the house
    catalogue. (F18)
16. **Re-run `build_deliverable.py` after every change above** and confirm the bundle still rebuilds
    byte-for-byte apart from its timestamps, and that the recomputed figures still match this report's
    Part A table. Any change to the `what` map or the exclusion reporting changes `FIGURES.md`.

---

*No fabricated data was found. Every rate, interval, count, p-value and cross-file cell in this
bundle survived independent recomputation from the primary run files; every external quotation and
every catalogue count survived first-hand retrieval. The defects above are defects of prose,
provenance labelling and one metadata field — none of them moves a number, and one of them (F1) will
quietly move somebody else's.*
