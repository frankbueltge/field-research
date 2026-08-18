# Verifier report — session 126 gauntlet, 2026-08-18 (deliverable-v0.3, version 0.3.3 + repairs of 2026-08-18)

**VERDICT: FAIL**

*Independent check against sources and data, not against the argument. All commands were run
against the current, frozen state of `drafts/2026-08-11-the-arm-that-was-missing/deliverable-v0.3/`
(32 files) and its supporting files one directory up. All recomputation used my own code, written
against the raw CSV/JSON, not the bundle's own scripts, except where explicitly noted as a rerun of
a named script for cross-checking. This is the seventh gauntlet on this bundle.*

One blocking finding. It is a new instance of the same defect class that has killed six previous
gauntlets — a claim about the bundle's own contents that was true when written and is false as
shipped — arising specifically from the mechanics of this session's repair, not from anything a
prior review examined. Every load-bearing statistic I recomputed (headline rate, Wilson CI, the
pooled and per-stratum age-gradient Fisher tests, the panel-date bracket, and the new persistence
figures) matched the bundle's own numbers exactly, independent of the bundle's own guard scripts.

---

## Findings

### Finding 1 — BLOCKING. `MANIFEST.json`'s self-hash inventory is stale and incomplete for the frozen state under review

**File:** `deliverable-v0.3/MANIFEST.json`, fields `bundle_files_sha256` and `bundle_files_note`.

**The claim:** `bundle_files_note` states, in the present tense and without qualification:
*"every file in this directory except MANIFEST.json itself, which cannot hash itself. A file
present here and absent from disk, or vice versa, is a defect."* `bundle_files_sha256` is offered
as that inventory — the one self-contained integrity table a receiver finds without leaving the
directory.

**What I computed:** I re-hashed every file currently in `deliverable-v0.3/` and diffed the result
against `bundle_files_sha256`.

- **2 files on disk are absent from the inventory**: `panel-date-125.json` and
  `persistence-126.json` — both added by this session, both listed in the freeze manifest
  `FROZEN-126.sha256`, neither mentioned in `MANIFEST.json`.
- **7 files have a wrong hash recorded**, because they were edited by this session's repairs after
  `MANIFEST.json` was last written: `FIGURE-PROVENANCE.json`, `FIGURES-PROVENANCE.json`,
  `FIGURES.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md`, `confirmation-record.json`. Every one of
  these hashes matches an *earlier* state of the file (the one `MANIFEST.json` itself was built
  against, dated `2026-08-16T17:30:13Z` in its own `built_utc`/`built_by` fields) and none matches
  the file as it now sits in the same, currently-frozen bundle recorded in `FROZEN-126.sha256`.

Example (full list reproducible from the two JSON files directly):

| file | `MANIFEST.json` says | actual sha256 (= `FROZEN-126.sha256`) |
|---|---|---|
| `LETTER.md` | `d36fc71f8d32...326` | `f2999823ac18...b71` |
| `VERSIONS.md` | `dd2c405533be...519` | `a59a6df30753...69f` |
| `LIMITS.md` | `4be49be10c47...0a8` | `690e679e77d0...89c` |
| `confirmation-record.json` | `37b16cdd2734...cb3` | `b9bb3dbdfc59...76b` |

**Why this is not the same as anything a prior review dispositioned.** `VERIFIER-125.md` finding 5
(non-blocking, informational) flagged that `MANIFEST.json`'s *named source* for `tools/run_lock.py`
— a file one directory **up**, outside the frozen bundle — had drifted after the freeze; it
explicitly confirmed "every file inside `deliverable-v0.3/` matches `MANIFEST.json`'s own hash
table exactly" at that time. That was true on 2026-08-17. It stopped being true during this
session's own repair pass: `versions_provenance_126.py`'s own docstring records that
`CONDITIONS-125.md` binding item 1 required the repairs be made "as edits, not a rebuild," so
`build_v03.py` — the only script that regenerates `MANIFEST.json`'s `bundle_files_sha256` (confirmed
by reading `build_v03.py` lines 700–712) — was "deliberately not run." That session accounted for
the fallout of skipping the rebuild on `FIGURE-PROVENANCE.json` (via `versions_provenance_126.py`)
but not the identical fallout on `MANIFEST.json`'s self-hash table, which nothing in this arc
checks standalone (`guard_claims.py`, `session126_sections.py` and `errata_check.py` do not touch
it, and I confirmed this by reading all three and by rerunning them: none reports on `MANIFEST.json`
content).

**Why it is blocking under the mandate, not merely untidy.** `bundle_files_note` is a sentence
inside the frozen, shipped bundle that describes the bundle's own contents, in the present tense,
with an explicit correctness guarantee ("A file present here and absent from disk... is a defect").
It is false as shipped: 2 files are undocumented and 7 recorded hashes do not match the frozen
files sitting beside them. A receiver who takes `LETTER.md`'s own invitation — *"check any figure
against the tables here"* — and uses the one self-contained hash table in the directory to audit
the bundle's internal consistency will find seven contradictions and two omissions, in a document
whose entire purpose is to state that no such thing exists. The underlying data is not corrupted —
`FROZEN-126.sha256`, computed fresh by me from the same files, matches every one of them — but
`MANIFEST.json`'s claim about its own completeness and correctness does not, and that is exactly
the class of defect this practice has named as fatal to six prior gauntlets: a sentence about the
apparatus that was true when typed and false when read.

**How checked:** wrote a standalone script (not reusing any bundle script) that walks
`deliverable-v0.3/`, computes sha256 of every file except `MANIFEST.json`, and diffs the result
against `MANIFEST.json`'s own `bundle_files_sha256` dict. Cross-checked the "why" against
`build_v03.py` (confirmed it is the only writer of that field), `versions_provenance_126.py`'s
docstring (confirmed the rebuild was skipped deliberately), and `git show 10c79b5 --stat` (confirmed
`MANIFEST.json` is not among the files that commit touched, while `FIGURES.md`, `LETTER.md`,
`LIMITS.md`, `VERSIONS.md`, `confirmation-record.json`, `FIGURE-PROVENANCE.json` and
`FIGURES-PROVENANCE.json` all are).

---

## What I RECOMPUTED and found CORRECT

All of the following were computed from `series/presence-series.csv` (3,869 rows × 6 days) or the
named source JSON, with code I wrote for this review — a closed-form Wilson interval and a
from-scratch hypergeometric two-sided Fisher exact test, not `scipy` and not the bundle's own
`figures.py`/`figures_page.py`.

1. **Headline rate, 2026-08-16, non-control panel.** k=436, n=3580 → **12.18 %**, Wilson
   **[11.15 %–13.29 %]**. Exact match to `LETTER.md`, `README.md` §4, `FIGURES.md` §1.
2. **Age-band table, 2026-08-16**, all 6 bands (n, absent, rate) — exact match to `FIGURES.md` §2
   and `README.md` §4: 0-1y 24/494 (4.86 %), 1-2y 58/768 (7.55 %), 2-3y 97/791 (12.26 %), 3-4y
   109/674 (16.17 %), 4-5y 75/457 (16.41 %), 5y+ 68/389 (17.48 %).
3. **The age-gradient Fisher test, pooled**, 0-1y vs 5y+: ratio **3.5981×**, two-sided
   **p = 1.4736 × 10⁻⁹** — exact match to `LETTER.md` and `FIGURES.md` §3 to the printed precision.
4. **The age-gradient Fisher test, all three strata** (18 cells + 3 tests) — exact match to
   `FIGURES.md` §3: F-forum ratio 3.44×, p=1.027×10⁻¹; W-article ratio 3.25×, p=5.758×10⁻⁶;
   W-other-ns ratio 5.22×, p=1.739×10⁻⁴, and all 18 per-band-per-stratum n/absent/rate cells.
5. **Panel size and composition**: 3,869 total rows, 249 `B-truncated` control rows, 3,620
   non-control; baseline-day determinate non-control = **3,581**, matching every prose use of that
   figure.
6. **The persistence result (`FIGURES.md`'s new section, `persistence-126.json`)**, recomputed
   independently from `series/presence-series.csv`: 3,620 non-control identifiers; 446 ever read as
   absent on a determinate day; **412 (92.38 %)** absent on all six days (an `INDETERMINATE` day
   breaks it); **439 (98.43 %)** absent on every day actually measured; the gap of **27** is
   identifiers whose only non-absent readings are `INDETERMINATE`; exactly **7** genuinely show both
   states, and the 7 IDs I found are the same 7 IDs listed in both `persistence-126.json` and
   `FIGURES.md` §5's transition table. Exact match on every count.
7. **The panel-date bracket (`LIMITS.md` §11, `panel-date-125.json`)**: reran `panel_date_125.py`
   itself (a legitimate rerun for a deterministic recomputation script, distinct from checking a
   cached report) — it reproduced the file byte-for-byte, confirming 47 corpus files examined, 1
   carrying any timestamp, lower bound `2026-08-01T22:33:14+00:00` (from `corpus-merged.json`'s
   `max_created`), upper bound `2026-08-11T11:24:06Z` (the earliest ledger run), and independently
   recomputed the interval myself: **9.5353 days**, matching. I also independently verified "37
   encyclopedia language editions": of the 45 `corpus-*.wikipedia.org.json` files, exactly 37 carry
   a nonzero `distinct_ids`; the other 8 are empty pulls. This matches every prose use of "37."
8. **The freeze itself.** Re-hashed all 32 files in `deliverable-v0.3/` with `sha256sum` and diffed
   against `FROZEN-126.sha256` one directory up: **identical, 32 of 32.** (My rerun of
   `panel_date_125.py`, step 7 above, wrote into the *outer* copy of `panel-date-125.json`, not the
   one inside the frozen bundle; I re-verified the freeze afterward and it was still intact, and
   confirmed via `git status`/`git diff` that nothing under version control was left dirty.)
9. **`confirmation-record.json`'s corrected sha256 (item 7 of the change list).** The recorded
   current hash of `ledger/corrections.json`, `357cb2b332fa...ae6`, matches what I computed directly
   from the file on disk. The recorded superseded hash, `b08e4c531e79...a7a`, matches what
   `git show 49f6d6b:.../ledger/corrections.json | sha256sum` produces from that historical commit.
   I diffed the two versions of `corrections.json` byte-for-byte myself: the **only** line that
   differs is `generated_utc`. The stated reason ("only `generated_utc` differs... regenerated when
   a measurement day closes") is true, checked against the actual diff, not asserted.
10. **`LETTER.md` item 3's rewording.** Confirmed no run file exists anywhere under
    `deliverable-v0.3/`, and confirmed all 7 files named in `MANIFEST.json`'s `source_runs` (the
    baseline union, five daily runs, and the second-probe replicate) exist at the stated paths one
    directory up with matching sha256. The new wording ("The raw daily run files themselves are
    not in it... at the paths `MANIFEST.json` names") is true.
11. **`FIGURES.md`'s header cross-reference.** Confirmed `FIGURES.md` is governed by
    `FIGURES-PROVENANCE.json` (247 entries) and the prose files by the separate
    `FIGURE-PROVENANCE.json` (126 entries) — the header's description of "two different files" is
    correct and matches which file `figures.py`'s `audit_prose` is actually called against for each.
12. **The receiver-dashboard numbers in `LETTER.md`** (generated 2026-01-14 21:53:41; 11 tracked, 0
    available, 0 unavailable, 11 errors; the "Note: Error are problems on our end, not TikTok."
    quote): read directly out of the raw saved `receiver-dashboard-2026-08-16.html` (246,014 bytes,
    hash matches `FROZEN-126.sha256`) with my own tag-stripped text search — all six strings present
    verbatim. `receiver-dashboard-read.json`'s transcription is accurate.
13. **`VERSIONS.md`'s `<!-- GUARD-CLAIMS -->` block.** Ran `guard_claims.py --check` (passed) and
    `guard_claims.py --facts` (fresh computation, not a cached report): 53 published errata
    accounted for (36 registered as wording, 17 reasoned, 0 unaccounted, 0 broken mappings); 126
    provenance entries covering the four prose files with 0 unmatched; 247 provenance entries
    covering `FIGURES.md` with 265 rendered tokens and 0 unmatched; the digit/word-number probe
    correctly flags `91827` and correctly fails to flag the spelled-out form, demonstrating (not
    just asserting) the stated limitation. Every number in the block on disk matches this live
    output.
14. **`LIMITS.md`'s new §11 block.** Ran `session126_sections.py --check` (passed): the panel-date
    numbers and the persistence numbers in the two generated blocks match their source JSON exactly,
    confirmed both by the script's own check and by my independent recomputation in items 6–7 above.
15. **The errata-regression gate.** Ran `errata_check.py` directly: `files_scanned: 23,
    registry_size: 29, n_regressions: 0`. Cross-checked `errata-check.json`'s per-file breakdown
    (`GAUNTLET-2026-08-15.md` 18, `ERRATA-121.md` 8, `ERRATA-122.md` 10, `ERRATA-123.md` 15,
    `ERRATA-124.md` 2 = 53) against the actual files those tables name; all `ids_declared_here`
    equal `ids_found_in_the_file` with `file_present: true`. I did **not** independently re-derive
    the full 29-entry registry from first principles against all five `ERRATA-*.md` source files
    line by line — see NOT CHECKED below.

---

## What I checked

- The freeze: re-hashed all 32 files, byte-identical to `FROZEN-126.sha256`.
- The three named gates: `errata_check.py`, `session126_sections.py --check`,
  `guard_claims.py --check` — all ran and all reported clean, and I read the check logic in
  `errata_check.py`, `guard_claims.py` and `figures.py` well enough to know what each gate does and
  does not cover.
- The headline rate, its Wilson CI, and the pooled and per-stratum age-gradient Fisher exact tests
  — recomputed from `series/presence-series.csv` with code written for this review, not the
  bundle's own scripts.
- The new persistence figures in `FIGURES.md`/`persistence-126.json` — fully recomputed from the
  raw series CSV, including the identity of the 7 units that changed state.
- The new panel-date bracket in `LIMITS.md`/`panel-date-125.json` — reran the deterministic script
  and independently recomputed the day-count from the two timestamps; independently verified the
  "37 encyclopedia editions" figure from the raw corpus files.
- All seven items in the "what changed" list: the guard-claims block, the version-table's new rows
  (cross-checked against `CONDITIONS-125.md`, `VERIFIER-125.md`, `INTERLOCUTOR-17.md`), the
  `LIMITS.md` §11 addition, the `FIGURES.md` persistence section, `LETTER.md` item 3's rewording,
  the `FIGURES.md` header's file cross-reference, and the `confirmation-record.json` hash repair
  (verified against git history at the named commit).
- The receiver-dashboard figures in `LETTER.md`, against the raw saved HTML.
- That `deliverable-v0.3/` matches its own git history exactly (`git diff --stat HEAD` empty) and
  that `MANIFEST.json` was not among the files touched by the repair commit `10c79b5`, which is the
  root cause of Finding 1.

## What I did NOT check (say so rather than guess)

- **The full 29-entry errata registry against all five source `ERRATA-*.md` files, phrase by
  phrase.** I confirmed the aggregate counts (53/36/17/0/0) via a live rerun of `errata_check.py`
  and spot-checked that `E20` (the erratum missed at session 124) is present in the registry, but I
  did not re-derive all 29 registered phrases and 17 reasoned exclusions independently from the
  underlying `ERRATA-*.md` prose myself. This has been recomputed independently by two prior review
  roles (session 125) with the same clean result; I relied on a fresh rerun of the same check rather
  than a full from-scratch reconstruction. NOT FULLY INDEPENDENTLY CHECKED.
- **The confidence interval on `receiver-eleven.md`'s "expected for this age profile" figure**
  (0.1377 [0.1139, 0.1655]). I recomputed the point estimate independently from
  `expectation.json`'s 2026-08-12 per-age-band rates weighted by the 11 identifiers' age-band
  composition (7×2-3y, 2×3-4y, 2×4-5y) and got 13.77 %, matching. I did not re-derive the specific
  CI-pooling method behind `[0.1139, 0.1655]`. NOT FULLY CHECKED.
- **Every one of the 265 rendered tokens FIGURES.md's provenance guard checks, individually.** I
  relied on the guard's own live `--facts` output (0 unmatched) plus my own independent
  recomputation of the specific tables that matter most (headline rate, age bands, Fisher tests,
  persistence) rather than re-deriving all 265 tokens by hand.
- **The `receiver-eleven.json` per-identifier age decoding** (that each 19-digit ID decodes to the
  stated creation timestamp under the platform's scheme) — I did not re-implement the ID-decoding
  algorithm to check the 11 dates in `receiver-eleven.md`. NOT CHECKED.
- **Anything about the correctness of the underlying oEmbed measurements themselves** — i.e.,
  whether the raw `ledger/run-*.json` files accurately reflect what the endpoint actually returned
  at measurement time. That is outside what this review can check from stored data; it is a
  question about the instrument's operation, not about whether the bundle's numbers are traceable
  to its own files.
- **Whether `memory/downstream-commitments.md` or other files outside this bundle and its immediate
  supporting scripts are consistent with claims made about them** (e.g. `README.md` §7's pointer to
  standing conditions there) — not opened.

---

## Bottom line

The measurement is, again, sound everywhere I tested it: every headline statistic, every new
figure added this session, and the freeze itself all check out exactly. The one blocking finding is
not a numeric error and not a fabricated figure — it is a true statement (`MANIFEST.json`'s
self-inventory) that went false as a direct, traceable side effect of this session's own repair
method, undetected because none of the three build gates this arc has built actually reads
`MANIFEST.json`. That is the same species of defect this bundle has failed six gauntlets on, arriving
by a new mechanism.
