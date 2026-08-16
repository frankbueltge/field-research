# Verifier — session 123, bundle version 0.3

**Verdict: FAIL**

Three of the eighteen factual errors this practice itself found and published against version 0.1
(`deliverable/GAUNTLET-2026-08-15.md`, findings E1, E2, E3) are still asserted, in substantially the
same words, in the "corrected" version 0.3 bundle this session shipped — plus a fourth (E7) and a
fifth defect (E11) from the same list. All five survive because they are plain prose sentences with
no digit in them, or a manifest field nobody re-checked; `figures.py`'s auditor only ever looks at
numbers, so none of these five ever had a chance of being caught by the discipline this session
built and is proudest of. The rebuild, the headline arithmetic, the Fisher test, the manifest hashes
and the dashboard extraction all check out exactly — the defect is not a measurement, it is
prose that was never re-verified against this repository's own already-published corrections.

---

## What was recomputed, and what agreed

**1. Independent rebuild.** `python3 build_v03.py --out /tmp/verify-v03 --cutoff
2026-08-15T23:59:59Z --audit` and a second build with no `--cutoff` (the two builds are identical
in coverage because the day-6 run is only a `.partial` — 600/3869 requests, per
`ledger/day6-stderr.txt` — and a `.partial` is never a run). Diffed byte-for-byte against the
committed `deliverable-v0.3/`: **21 of 23 files are byte-identical; the other 2 (`FIGURES.md`,
`MANIFEST.json`) differ only in the recorded `built_utc` / build timestamp.** This matches the
reproducibility claim in `INCREMENT-13.md` §5 exactly.

**2. Headline figures, recomputed from `ledger/*.json` directly**, with my own script (not
`build_deliverable.py`, not `figures.py`): per-day pooled determinate/absent counts for all 5 days
(baseline, 2026-08-12..15), the newest-day (2026-08-15) pooled rate, and its 6 age-band cells, using
my own Wilson-interval implementation. **All values agreed exactly** with `expectation.json` and
`reference-baseline.json`:

| day | n (mine) | absent (mine) | matches bundle |
|---|---|---|---|
| baseline | 3,581 | 437 | yes |
| 2026-08-12 | 3,582 | 437 | yes |
| 2026-08-13 | 3,576 | 439 | yes |
| 2026-08-14 | 3,583 | 435 | yes |
| 2026-08-15 | 3,576 | 438 | yes |

Age bands on 2026-08-15 (n/absent): 0-1y 493/23, 1-2y 773/60, 2-3y 787/94, 3-4y 672/111, 4-5y
457/76, 5y+ 387/69 — all exact matches, including CIs to displayed precision. Zero disagreements.

**3. Age-gradient Fisher test**, recomputed with `fractions.Fraction` and `math.comb` (exact
rational arithmetic, independent of `build_deliverable.py`): for `results[0]` (young 23/493, old
69/387), two-sided *p* = **3.082941987992075 × 10⁻¹⁰**, ratio = **3.8217054263565893**. Both match
`gradient-test.json` to full double precision (all 16 significant digits shown).

**4. Provenance table.** All **102** entries in `FIGURE-PROVENANCE.json` checked independently
(file exists, JSON path resolves, value renders to the recorded string, under renderers I
reimplemented myself rather than importing `figures.py`'s). **0 mismatches.** But see Findings 1–5
below: this table cannot cover claims that were never routed through it, and several were not.

**6. Manifest.** `MANIFEST.json → bundle_files_sha256` lists exactly the 23 files on disk (besides
itself); I recomputed all 23 hashes myself — 0 mismatches, 0 extra, 0 missing. `source_runs` (5
entries) hashes match the actual `ledger/*.json` files — 0 mismatches. `carried_files` (11 entries)
hashes match their declared sources, and the copies inside the bundle match those hashes too — 0
mismatches.

**7. Dashboard reading.** Re-extracted the four counters and the generation timestamp from
`receiver-dashboard-2026-08-16.html` by my own regex-free method (locating the label occurrences
directly and reading the immediately preceding number), and confirmed the pairing used by
`dashboard_read_123.py` is the correct one — "Available" occurs 25 times in the flattened page text,
and the code's `.find()` (first occurrence) happens to land on the real stat block at offset 8136,
immediately after "Total Videos Tracked" at 8113, not on any of the 24 decoy occurrences elsewhere
on the page. `source_sha256` matches the committed HTML file. I fetched
`https://playground.tiktok-audit.com/api-na/` live: it reports the same generation timestamp
(2026-01-14 21:53:41) and the same four counts (11 total, 0 available, 0 unavailable, 11 errors) as
the saved bytes. This is **not** a byte-for-byte comparison — the fetch tool available to me
converts HTML to text/markdown and summarizes it — so full byte-identity of the live page against
the saved HTML is **UNCHECKED**; only the reported figures were confirmed to agree.

**8. Rebuild audit.** Re-ran `rebuild_audit_123.py` against my own fresh build at the shipped
cut-off (2026-08-14T23:59:59Z) and reproduced the committed `rebuild-audit-123.json` exactly:
zero unexpected leaves in both comparison groups A and B. I also reconstructed the *old, buggy*
classifier (`"band" in path` substring test, as described in `classify()`'s docstring) and ran it
over the same diffs: it produces **97** unexpected leaves — the exact count `INCREMENT-13.md` and
`memory/discarded.md` report for that discarded run. I then inspected every one of the 497 leaves
the *current* classifier labels `band_derived` (dumped and grouped by normalized path): all are
genuinely `by_age_band.*`, `by_stratum_band.*`, `across_day_stability.<band>.*`, or
`gradient-test.json` `results[]` cells, and the `young`/`old` absent-counts inside those cells are
unchanged across the correction (only their band-membership `n` moved) — consistent with the
prose's claim that no absence was created or destroyed by the clock repair. **One design weakness,
not a false certification:** `classify()` marks *every* leaf of `gradient-test.json` as
`band_derived` unconditionally, by filename, rather than by field — so a future bug that changed,
say, the Fisher-test formula itself inside that file would also be silently waved through as
"band-derived" and would not appear in `n_unexpected`. In this run it did not hide anything (the
diffs I inspected are all genuinely band-membership effects, and I independently recomputed the
Fisher p-value in item 3 above and it matched), but the rule is broader than it needs to be.
**NON-BLOCKING.**

**9. `INCREMENT-13.md`'s specific claims, checked against the files it cites:**
- Probe start "**03:37:40Z**" — matches `ledger/day6-stderr.txt` line 2 ("start
  2026-08-16T03:37:40Z") exactly.
- "**128 assertions**" — ran `deliverable/tools/selftest_presence_check.py` myself: "128
  assertion(s) passed / 0 failed". Exact match.
- "Reproducible except for timestamps" — confirmed in item 1 above.
- "This session's bet is therefore LOST" — confirmed against `memory/discarded.md`'s session-123
  entry and against my own reproduction of `rebuild-audit-123.json` (item 8): zero unexpected
  disagreements, so the pre-registered bet (that a fresh rebuild would find at least one
  disagreement beyond the known drift) did lose, and the record says so.

All of item 9 checks out.

---

## Findings

### Finding 1 — BLOCKING: "twenty synthetic identifiers" is false, and the practice already knew it

`deliverable-v0.3/LIMITS.md` §1: *"A three-arm control run on 2026-08-11 with twenty synthetic
identifiers that never existed returned exactly the same code as identifiers that certainly did
exist."*

**True value:** nineteen of twenty did. The twentieth (`vid 7512505100479546335`) ended in an SSL
handshake timeout — `http: null`, no code at all — not "the same code." I confirmed this directly
in `reverify-results.json`'s `arm_c` (`Counter({(400, 400): 19, (None, None): 1})`), which is the
practice's own record of that exact run.

This is not a new discovery: it is **verbatim finding E1** of this same repository's
`deliverable/GAUNTLET-2026-08-15.md` ("the three-arm control used twenty synthetic identifiers | 
nineteen of twenty returned the refusal code; the twentieth ended in a transport failure. This
arc's own RESULT.md has it right and the bundle did not"), and it was even checked by
`discharge_120.py`, whose own output records `limits_md_says: "20"` beside `matches_in_RESULT_md:
["19"]`. Session 123 rewrote `LIMITS.md` from scratch through `build_v03.py` and reproduced the
same false sentence, unchanged in substance, because "twenty" is a spelled-out word, not a digit —
`figures.py`'s prose auditor (`NUM = re.compile(r"...\d[\d,]*...")`) cannot see it, and the sentence
was never routed through `fx.*` at all; it is a hardcoded literal in the f-string with no
provenance entry.

### Finding 2 — BLOCKING: the vantage-logging claim is false for the baseline file, and the practice already knew it

`deliverable-v0.3/LIMITS.md` §2: *"Every run is taken from one network vantage (...) logged into
every run file before the first measurement request."*

**True value:** false for `ledger/baseline-union.json`, which the bundle's own `MANIFEST.json`
lists as one of its 5 `source_runs` (label "baseline"). I read that file directly: its `vantage`
object says `"source": "carried from the producing runs; see components"` — it is a union of 4
component runs spanning 2026-08-11T11:24:06Z–23:05:18Z (confirmed from `components[]`), not a
single sweep with a vantage logged before its first request. This is **verbatim finding E2** of
`deliverable/GAUNTLET-2026-08-15.md`, carried into v0.3 with the same substantive claim (the wording
was lightly rephrased — "logged into every run file" vs. the original "logged in every run file...
of that run" — but the false assertion is unchanged and the baseline file still contradicts it).
No digit is involved; invisible to the auditor for the same reason as Finding 1.

### Finding 3 — BLOCKING: the metadata-check claim is false, and the practice already knew it

`deliverable-v0.3/LIMITS.md` §6: *"Creation times are decoded from the identifier itself (...),
checked against the endpoint's own returned metadata where that metadata exists."*

**True value:** no such check exists in this arc's code. I grepped
`deliverable/tools/presence_check.py` and `probe.py` for any comparison of decoded creation time
against endpoint-returned metadata; there is none — the probe records no creation-time field
from the endpoint at all. This is **verbatim finding E3** of `deliverable/GAUNTLET-2026-08-15.md`
("no such check exists in this arc. The probe records no creation-time field"), carried into v0.3
essentially unchanged. No digit; invisible to the auditor.

### Finding 4 — BLOCKING: "not videos" is false for the B-truncated control arm, and it appears twice

`deliverable-v0.3/LIMITS.md` §7: *"A control arm of display-truncated identifiers that are **not**
videos is excluded from every rate."* The same claim appears again in `deliverable-v0.3/FIGURES.md`
§4: *"249 identifiers of the `B-truncated` control arm, which are display-truncated strings and not
videos."*

**True value:** 248 of 249 do not resolve; one (`12345`) does — this arc's own legacy-identifier
control (`legacy-id-control.json`, cited in `memory/claims.md`) established it is a real video that
predates the platform's current identifier scheme, and it returns HTTP 200 with a full oEmbed
payload. This is **verbatim finding E7** of `deliverable/GAUNTLET-2026-08-15.md`. It is present in
two files of the shipped bundle, neither of which routes the phrase "not videos" through any JSON
field — `FIGURES.md` is not even one of the four files `build_v03.py --audit` checks (only
`README.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md` are audited; `FIGURES.md` is generated by the
older `build_deliverable.py` and is outside `figures.py`'s reach entirely).

### Finding 5 — BLOCKING: an unfilled `TEMPLATE` placeholder is still in the shipped manifest

`deliverable-v0.3/MANIFEST.json → source_runs`, the 2026-08-13 entry: `"run_id": "TEMPLATE — the
running session sets this"`.

I read the field directly; it is the literal placeholder string, not a real run identifier. This is
**verbatim finding E11** of `deliverable/GAUNTLET-2026-08-15.md` ("one carries the unfilled
placeholder ... inherited from a manifest at session 113"), unresolved in the manifest this session
built and hashed itself into `bundle_files_sha256`. The manifest's own job is to be the receiver's
record of what each source file *is*; one of its five identity fields is not a value, it is a bug
report about itself.

### Finding 6 — NON-BLOCKING: `gradient-test.json`'s rebuild-audit classification is file-wide, not field-wide

Documented under item 8 above. `rebuild_audit_123.py`'s `classify()` marks any differing leaf of a
file named `gradient-test*.json` as `band_derived` unconditionally, rather than checking that the
specific leaf name is a band-related field the way it does for `expectation.json` and
`reference-baseline.json`. In this run every actual diff in that file was independently confirmed
band-membership-driven (item 8, item 3), so nothing was hidden this time — but the rule as written
would not catch a future defect confined to that file's non-band fields (`day`, `test`, `arm`,
`caveat`, per-group `group` labels).

### Finding 7 — NON-BLOCKING: `FIGURES.md`'s two INDETERMINATE tables count different things, unexplained

`FIGURES.md` §4 excludes 44 `INDETERMINATE` observations from the newest day's rate; §6's "Transport
noise" table reports 49 for the same day. I traced the difference myself directly from
`ledger/baseline-union.json` and the day-15 run file: the larger figure includes `INDETERMINATE`
observations inside the `B-truncated` control arm (5 of them on 2026-08-15; 3 on baseline, matching
baseline's 39-vs-42 split the same way), the smaller figure excludes them. Both numbers are
internally correct — this reproduces **finding E8** of the original gauntlet almost exactly ("both
are right and the page never says why"), which was never a false-statement finding to begin with,
and it still isn't; it is an unexplained duplicate metric, present in a file outside the audit's
scope.

### Finding 8 — NON-BLOCKING: `prose-audit-123.json`'s recorded provenance path is a scratch directory, not the bundle

The committed `prose-audit-123.json` (written by `build_v03.py --audit` to the current working
directory, not into `--out`) has `"provenance": "/tmp/verify-v03-nocutoff/FIGURE-PROVENANCE.json"`
— a path outside the bundle and outside the repository, which by definition cannot be resolved by
anyone re-reading the shipped file. (I confirmed this is the actual committed content via `git
cat-file`, not an artifact of my own testing overwriting it — the sha256 of the file on disk before
I touched it matches the committed blob exactly.) This is a build-script wrinkle
(`build_v03.py` always writes `prose-audit-123.json` to the caller's CWD, using whatever `--out`
path was passed as the label inside it) rather than a data-correctness problem: the audit result
itself (0 unmatched) is reproducible from the bundle regardless of what directory produced it, and
I reproduced it myself (item 4). Worth fixing so the record is self-describing, not blocking.

### Finding 9 — Persisting, not newly introduced: the neighbouring paper is still unnamed on the receiver-facing page

`deliverable/GAUNTLET-2026-08-15.md` finding E12 noted that the neighbour study that narrowed this
arc's own novelty claim (`arXiv:2601.12390` / `10.1145/3805689.3812237`) is named nowhere in
`LETTER.md` or `LIMITS.md`. I grepped `deliverable-v0.3/LETTER.md`, `LIMITS.md` and `README.md` for
both identifiers: still absent from all three. This is an omission, not an assertion of something
false, so I record it as **NON-BLOCKING**, but it has now survived two bundle versions unaddressed.

---

## What I could not check

- **Full byte-identity of the live dashboard page against the saved HTML.** I fetched
  `https://playground.tiktok-audit.com/api-na/` and it returned the same generation timestamp and
  the same four counters as the saved bytes, but my fetch tool renders the page to text through an
  intermediate summarization step rather than returning raw bytes, so I cannot certify the two HTML
  documents are byte-identical — only that the figures a reader would extract from each agree.
  **UNCHECKED** beyond that.
- **`presence_check.py`'s junk-coercion behaviour (gauntlet finding E15)** — whether the shipped
  tool still silently coerces non-identifier strings (dates, search phrases, foreign-platform URLs)
  into spurious identifiers. I read the code for the metadata-check claim (Finding 3) but did not
  execute the tool against adversarial input myself. **UNCHECKED.**
- **The full text of every `INTERLOCUTOR-*.md` and `CONDITIONS-*.md` file** for context on prior
  sessions' bets and conditions — I read `memory/discarded.md` and `memory/claims.md` selectively
  for the specific claims `INCREMENT-13.md` makes, not exhaustively.
- I did not attempt to re-derive `drift-122.json`'s shelf-life arithmetic from first principles;
  I confirmed the two literal drift figures used in `LIMITS.md` (30-day and 365-day) are read
  correctly from `reference-baseline.json → shelf_life.measured_drift_pp_by_days_after_t_ref`
  (Finding-free, provenance table entry checked in item 4), but did not independently recompute the
  drift model itself.

---

## Summary of findings by severity

| # | Finding | Severity |
|---|---|---|
| 1 | "twenty synthetic identifiers ... returned exactly the same code" — false, repeats gauntlet E1 | BLOCKING |
| 2 | "logged into every run file before the first measurement request" — false for the baseline file, repeats E2 | BLOCKING |
| 3 | "checked against the endpoint's own returned metadata" — no such check exists, repeats E3 | BLOCKING |
| 4 | "display-truncated identifiers that are not videos" — false for 1 of 249, repeats E7, in two files | BLOCKING |
| 5 | Unfilled `TEMPLATE` placeholder in the shipped `MANIFEST.json`, repeats E11 | BLOCKING |
| 6 | `gradient-test.json`'s rebuild-audit classification is file-wide rather than field-wide | NON-BLOCKING |
| 7 | `FIGURES.md`'s two INDETERMINATE counts differ by scope, unexplained (repeats E8, itself non-blocking) | NON-BLOCKING |
| 8 | `prose-audit-123.json` records a scratch-directory provenance path, not the bundle's own | NON-BLOCKING |
| 9 | Neighbour paper still unnamed on the receiver-facing page (repeats E12) | NON-BLOCKING |

Every recomputed statistic — the per-day and per-band counts, the pooled rate, the Wilson
intervals, the Fisher exact test, the manifest hashes, the dashboard extraction, and the rebuild's
own zero-unexpected-leaves verdict — agreed exactly with the shipped bundle. The fourth session in
a row has not failed on a measurement. It has failed on prose: specifically, on five sentences that
this same practice already proved false against its own data before this session began, rewritten
by the session's own generator without being checked against that existing record. Four of the five
have no digit in them at all, so `figures.py`'s discipline — built explicitly to end this failure
class — could not have caught them by construction; it only ever looks at numbers. The fifth is a
manifest field that was hashed into the bundle's own integrity record without being read.

**Verdict: FAIL.**
