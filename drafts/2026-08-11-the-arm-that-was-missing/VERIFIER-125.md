# Verifier report — session 125 gauntlet, 2026-08-16 bundle (deliverable-v0.3, version 0.3.3)

*Independent check against sources and data, not against the argument. All commands were run
against the frozen bundle at `drafts/2026-08-11-the-arm-that-was-missing/deliverable-v0.3/` and
its supporting files one directory up. `python3` (with `scipy` installed for this session) was
used throughout for recomputation; exact code is described inline.*

**VERDICT: FAIL**

Two blocking findings, both in the same document (`VERSIONS.md`), both self-descriptive claims
about the bundle's own guards that are false in the state actually shipped — the sixth gauntlet in
a row to fail on the practice's own prose about itself, never on a measurement.

---

## Findings

### Finding 1 — BLOCKING. `VERSIONS.md` falsely claims the provenance guard never covered `FIGURES.md`

**File:** `deliverable-v0.3/VERSIONS.md`, section "What changed between 0.1 and 0.3", item 6.

**Quoted text:** *"**Its limits, found at the gauntlet that failed this version:** it reads
**digits**, so a figure written as a word passes it untouched, and it never covered `FIGURES.md`
at all. Neither is fixed here; both are stated."*

**What is wrong:** The second half ("it never covered `FIGURES.md` at all. Neither is fixed
here") is false as shipped. `FIGURES.md`'s own header states it is "Written by `figures_page.py`"
with every number "fetched from a named field ... and the field is recorded in
`FIGURE-PROVENANCE.json`" (the actual file is `FIGURES-PROVENANCE.json`, a second, separate
provenance table — see Finding 3). That table exists, has 236 entries, and
`figures-audit-124.json` (built in the same build run, timestamp identical to `VERSIONS.md`'s)
shows `"n_unmatched_total": 0` of 255 rendered tokens in `FIGURES.md`. `build_v03.py` lines
760–775 show the audit gate explicitly calling `F.audit_prose([P("FIGURES.md")],
P("FIGURES-PROVENANCE.json"))` and failing the build on any unmatched figure. The routing is also
independently attested in `routing-equivalence-124.json` and in
`memory/downstream-commitments.md` condition 14(b): *"`FIGURES.md` is now inside the guards —
this **reverses condition 12(d)**."*

**Self-contradiction inside the same document:** `VERSIONS.md`'s own version table, three lines
above item 6, describes version 0.3.2: *"Session 124 routed `FIGURES.md` through the provenance
guard, completed the errata accounting..."* Item 6 was not updated to match.

**True state:** `FIGURES.md` is covered by the guard (via `FIGURES-PROVENANCE.json`), 0 unmatched
figures, and has been since version 0.3.2. Only the first half of item 6 (the guard matches digits,
not number-words) remains accurate — confirmed by reading `figures.py`'s `NUM` regex
(`r"(?<![A-Za-z0-9])\d[\d,]*(?:\.\d+)?"`), which indeed only matches numerals.

**How checked:** read `FIGURES.md` header; read `FIGURES-PROVENANCE.json` (236 entries, disjoint
content from `FIGURE-PROVENANCE.json`'s 118); read `figures-audit-124.json`
(`n_unmatched_total: 0`); read `build_v03.py` lines 754–775; read
`routing-equivalence-124.json`; read `memory/downstream-commitments.md` lines 559–563; confirmed
`figures.py`'s `NUM` regex only matches digit runs.

---

### Finding 2 — BLOCKING. `VERSIONS.md` falsely claims the errata check leaves 17 published errata "unchecked"

**File:** `deliverable-v0.3/VERSIONS.md`, section "What changed between 0.1 and 0.3", item 7.

**Quoted text:** *"Its own coverage is printed rather than implied: **36 of 53** published errata
are registered in it, and the rest are unchecked."*

**What is wrong:** "The rest are unchecked" is false. Running `errata_check.coverage()` from
`errata_check.py` (one directory up, the actual code the frozen build ran) gives:

```
n_published_accounted: 53
n_registered_as_wording: 36
n_reasoned_as_unregistrable: 17
unaccounted_published_ids: []
broken_mappings: []
```

`errata-check.json` — written by this exact bundle's own build (`mtime` identical to
`VERSIONS.md`'s, `2026-08-17 03:35:55`) — contains this identical output. The 17 errata that are
not phrase-registered are not "unchecked": each has a stated reason it is the wrong instrument for
a phrase check, and `unaccounted_published_ids` is empty. This is exactly the accounting
`memory/downstream-commitments.md` condition 14(c) describes: *"Every one of the **53** errata
this arc has published is either registered as wording ... (36) or left out with a stated reason
(17); none is unaccounted."* It is also exactly what session 124's own `VERIFIER-124.md` already
confirmed independently ("errata mappings have no broken targets") and `INTERLOCUTOR-16.md`
confirmed ("errata accounting 53/53 with none unaccounted").

**Self-contradiction inside the same document:** the same version-table row for 0.3.2, three lines
above item 7, says session 124 "completed the errata accounting."

**True state:** 53 of 53 published errata are accounted for (36 registered as machine-checkable
wording + 17 reasoned as unregistrable), 0 unaccounted, 0 broken mappings.

**How checked:** ran `python3 -c "import errata_check; print(errata_check.coverage())"` from
`drafts/2026-08-11-the-arm-that-was-missing/`; cross-read the identical output already written to
`errata-check.json` (same build run); read `memory/downstream-commitments.md` condition 14(c);
read `VERIFIER-124.md` and `INTERLOCUTOR-16.md`.

*(Both findings match the two concerns the conductor's own `SEALED-125-preread.md` flagged before
dispatch, P1 and P2 — this Verifier reached them independently, against the frozen state and the
code, before reading that either report existed as more than a name.)*

---

### Finding 3 — NON-BLOCKING. `FIGURES.md` names the wrong provenance file for itself

**File:** `deliverable-v0.3/FIGURES.md`, line 3.

**Quoted text:** *"...and the field is recorded in `FIGURE-PROVENANCE.json`."*

**What is wrong:** `FIGURES.md`'s own figures are recorded in `FIGURES-PROVENANCE.json` (plural,
39,985 bytes, 236 entries) — a completely disjoint file from `FIGURE-PROVENANCE.json` (singular,
19,668 bytes, 118 entries, which covers `README.md`/`LETTER.md`/`LIMITS.md`/`VERSIONS.md`). The
two files share zero overlapping `note` fields. `build_v03.py` line 765 confirms `FIGURES.md` is
in fact audited against `P("FIGURES-PROVENANCE.json")`, not the singular file its own header
names.

**How checked:** loaded both JSON files, compared their `note` sets (0 overlap out of 118×236
possible pairs); read `build_v03.py` line 765.

---

### Finding 4 — NON-BLOCKING. `confirmation-record.json` carries a stale sha256 for `ledger/corrections.json`

**File:** `deliverable-v0.3/confirmation-record.json`, `sources.corrections_sha256`.

**What is wrong:** the field reads `b08e4c531e79cac24a91cac17c51e00ccaa7cac1e064a4282dbc7b89372a8e7a`.
The actual current `ledger/corrections.json` hashes to
`357cb2b332faa44fe605fc03882e3be5ba8699daa93fdc54e6128937a4a12ae6` — which is exactly the value
`MANIFEST.json`'s `corrections_file.sha256` correctly records. `git log -p` on
`ledger/corrections.json` shows the only change between the two revisions is the
`generated_utc` timestamp field (`2026-08-15T05:31:52Z` → `2026-08-16T05:27:19Z`); the two
correction rows themselves (`vid 7368171405361351954`, `vid 7016669364938149122`) are byte-identical
across revisions. Substantively harmless — the confirmation counts built from this file were
independently recomputed against the current `series/presence-series.json` overlay (`states` vs
`states_corrected`) and matched exactly (Finding list below) — but two documents in the same
bundle assert two different hashes for the same file, and only one is current.

**How checked:** recomputed sha256 of `ledger/corrections.json`, compared to both
`confirmation-record.json` and `MANIFEST.json`; `git log -p` on the file's two prior revisions.

---

### Finding 5 — NON-BLOCKING (informational). `MANIFEST.json`'s named source for `tools/run_lock.py` has since diverged

**File:** `deliverable-v0.3/MANIFEST.json`, `carried_files` entry for `tools/run_lock.py`
(`from: run_lock.py`, claimed sha256 `73f4ae47b18baa6c9b1b934e68980d43d27d6d68baa55903330e1d082f842e67`).

**What is wrong:** the bundled `deliverable-v0.3/tools/run_lock.py` matches that hash exactly
(confirmed — this is not a defect in the shipped bundle). But the top-level `run_lock.py` one
directory up, which `MANIFEST.json` names as the source it was carried from, now hashes to
`abb15cd0b0029ccaec948967e317a3082517a9489e7443a9ec07f261108f340d` — a different file, modified
after the freeze (`mtime` 03:38:21 vs. the bundle's build at 03:35:55). This is expected repo
churn after the freeze (the README states the instrument keeps running) and does not affect the
integrity of the shipped bundle itself — every file inside `deliverable-v0.3/` matches
`MANIFEST.json`'s own hash table exactly (see below) — but a reader tracing `carried_files` back
to "the source" today would not find the file that produced the bundled copy.

**How checked:** recomputed sha256 of `run_lock.py` one directory up; compared to
`MANIFEST.json`'s `carried_files` entry; compared `mtime`s.

---

## What I RECOMPUTED and found CORRECT

All of the following were recomputed from `series/presence-series.json` (the raw unit-level data,
3,869 rows × 6 days) or from the named JSON files, independently of the prose, using `python3`
(Wilson intervals by closed-form formula, Fisher exact tests via `scipy.stats.fisher_exact`).

1. **Per-day determinate/absent/rate for all 6 measurement days**, excluding the `B-truncated`
   control arm — exact match to `README.md` §2 and `FIGURES.md` §1, including all six 95% Wilson
   intervals recomputed independently (e.g. day 2026-08-16: n=3580, absent=436, 12.18%,
   [11.15%–13.29%]).
2. **Age-band table for 2026-08-16** (6 bands, n/absent/rate/Wilson CI) — exact match to
   `README.md` §4 and `FIGURES.md` §2, all 6 rows and all 6 CIs.
3. **Age-gradient Fisher exact test**, pooled and per-stratum (F-forum, W-article, W-other-ns) —
   all 4 ratios and all 4 two-sided p-values reproduced to the printed precision (pooled: ratio
   3.5981148…, p=1.47359894…×10⁻⁹).
4. **Source-stratum breakdown** (F-forum/W-article/W-other-ns, n/absent/rate on 2026-08-16) —
   exact match to `FIGURES.md` §4.
5. **18-cell per-stratum × per-age-band gradient table** — exact match to `FIGURES.md` §3.
6. **Transport-noise table**, INDETERMINATE all-units and non-control counts for all 6 days —
   exact match to `FIGURES.md` §6.
7. **Control-arm resolution**: 249 `B-truncated` identifiers on 2026-08-16 split as 244
   NOT-RETRIEVABLE + 4 INDETERMINATE + 1 RETRIEVABLE — matches the claimed "248 of 249 do not
   resolve, and one is a real video" (`LIMITS.md` §8) exactly under "does not resolve" =
   NOT-RETRIEVABLE ∪ INDETERMINATE.
8. **Undatable-identifier exclusion**: exactly 7 non-control identifiers carry no decodable
   creation time on 2026-08-16 — matches `FIGURES.md` §4.
9. **Non-control panel size**: 3,869 − 249 = 3,620 — matches `FIGURES.md` §5.
10. **Multi-state identifiers across 6 days**: 7 raw / 5 after the corrections overlay, with the
    exact same 7 video IDs, in the exact same arm and per-day state sequence, as the table in
    `FIGURES.md` §5 — recomputed directly from `states` vs `states_corrected`.
11. **`confirmation-record.json`'s own arithmetic**: recomputing "raw" and "genuine" tallies from
    its 9-entry `readings` array reproduces `all_readings` (6/6 confirmed NOT→RET, 1/3 confirmed
    RET→NOT) and `genuine_transitions_only` (4/4, 1/3) exactly, including which two readings are
    the "artefact echoes" excluded from the genuine count — these are the same two video IDs
    (`7016669364938149122`, `7368171405361351954`) marked "no — refuted reading, see overlay" in
    `FIGURES.md` §5.
12. **Balanced-panel spread**: 3,386 non-control units determinate on all 6 days; recomputed
    per-day rates give range 0.0886pp, raw range ≈0.14pp, ratio 1.53× — matches `FIGURES.md` §1
    and `figures-derived.json` exactly.
13. **Baseline-union component sum**: 2,904 + 635 + 304 + 26 = 3,869, matching the baseline day's
    `n_units` and confirming the four-component union.
14. **`LIMITS.md` §2's E2 exception wording** ("the vantage was carried from the producing runs")
    is a verbatim match of `ledger/baseline-union.json`'s actual `vantage.source` field.
15. **Population count**: 37 distinct encyclopedia language editions recomputed from
    `figures-derived.json`'s `population.editions` list (counted directly) — matches every
    reference to "37" across `README.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md`.
16. **Shelf-life drift figures** in `LIMITS.md` §5 (0.2264pp at 30 days, 2.4225pp at 365 days)
    match `reference-drift.json`'s `measured_drift_pp_by_days_after_t_ref` exactly; the "26 day"
    crossover matches `reference-drift.json`'s
    `when_the_design_half_overtakes_the_bookkeeping_half.days`.
17. **`MANIFEST.json`'s `bundle_files_sha256`**: recomputed sha256 for all 29 listed files against
    the actual bytes on disk — **0 mismatches**. Also confirmed the file set is exact: no file on
    disk is missing from the manifest and no file in the manifest is missing from disk.
18. **`FROZEN-033.sha256`** (an external 30-line snapshot one directory up, dated to the freeze):
    recomputed sha256 for all 30 lines against current disk state — **0 mismatches**, confirming
    the bundle is genuinely unmodified since the freeze this review is conducted against.
19. **`MANIFEST.json`'s `source_runs`, `corrections_file`, `replicate_runs` and `carried_files`
    hashes** against the actual files one directory up — all matched except the one noted in
    Finding 5 (external file changed after the freeze; the bundled copy itself is correct).
20. **`errata_check.coverage()`** run directly against the actual `errata_check.py`: 53/53
    published errata accounted for, 0 unaccounted, 0 broken mappings — reproduces
    `errata-check.json` exactly (see Finding 2).
21. **`figures-audit-124.json`**: `FIGURES.md` audited against `FIGURES-PROVENANCE.json` returns 0
    unmatched of 255 tokens (see Finding 1).
22. **Receiver's own eleven-identifier table** (`receiver-eleven.md`/`.json`): the per-identifier
    dashboard day-counts (observations, error days, not-available days) sum to each identifier's
    stated total (279 for ten of them, 238 for one) exactly as claimed.
23. **`receiver-dashboard-2026-08-16.html`** genuinely contains the strings
    `receiver-dashboard-read.json` claims were extracted from it — "11" / "Total Videos Tracked",
    "Error are problems on our end, not TikTok." — confirmed by direct string search of the saved
    HTML bytes.
24. **External source, arXiv 2506.09746** ("TikTok's Research API: Problems Without
    Explanations," AI Forensics / Carlos Entrena-Serrano, Martin Degeling, Salvatore Romano, Raziye
    Buse Çetin) — fetched and confirmed real and retrievable; content matches
    `receiver-report-2506.09746v2-extracted.txt` and the bundle's characterization of it (Research
    API problems, a public monitoring dashboard, a Taylor Swift video among the missing — which
    matches the `taylorswift`-handle identifier appearing in `receiver-eleven.json`).
25. **External source, `playground.tiktok-audit.com`** — fetched live; the dashboard currently
    reports the identical 11 tracked / 0 available / 0 unavailable / 11 errors and the identical
    "Error are problems on our end, not TikTok" note that `receiver-dashboard-read.json` and
    `LETTER.md` quote.
26. **`presence_check.py`**: confirmed `VERSION = "0.3.1"` and default `--confirm-what absent`
    behavior (re-requests every refusal by default) match the claims in `README.md` §6 and
    `LIMITS.md`.

## What I could NOT check, and why

- **The full "family of crossover values running from 1 day to 26" claim** in `LIMITS.md` §5. I
  confirmed the "26" endpoint exactly (`reference-drift.json`'s
  `when_the_design_half_overtakes_the_bookkeeping_half`) and confirmed the general mechanism
  (six per-band bookkeeping deltas of differing magnitude, each implying a different crossover day
  against the caller-side drift curve), but did not reconstruct all six per-band crossover days to
  confirm the low end is exactly "1." UNCHECKED — plausible from the data shape, not
  independently re-derived to the exact bound.
- **The E1 finding** (LIMITS.md §1: "nineteen of the twenty" synthetic identifiers returned HTTP
  400, one returned no code) — this was originally established and corrected across sessions
  120–123 (see `CONDITIONS-120.md` line 41) and repeated consistently since; I did not locate and
  re-run the original raw probe output for the twenty synthetic IDs to re-derive it from scratch.
  UNCHECKED against raw bytes, but corroborated by a consistent, multiply-audited paper trail.
  This is not the kind of measurement claim the task's history warns about, and no later gauntlet
  has disturbed it.
- **The legal-requirement framing** ("required by law to give vetted researchers access") in
  `README.md` §1 — this refers to the EU Digital Services Act's researcher-data-access provision
  (Article 40), a well-established real requirement for very large online platforms; not
  independently re-verified against the statutory text in this pass.
- **`by_year` table in `reference-baseline.json`** — spot-checked that `n` sums to 3,573 (=
  3,580 − 7 undatable, consistent) but did not verify each year's absent-count individually against
  the raw series; this table is not surfaced in the bundle's prose documents.
