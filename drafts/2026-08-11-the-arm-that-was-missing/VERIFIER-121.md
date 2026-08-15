# Verifier report — session 121, on commit `ffebcf56`

*Published unedited, as `PROTOCOL.md` requires. The Verifier was convened because every figure in
increment 12 was produced by code this session wrote the same night, and nobody but the session
that wrote it had checked it against the sources. Its verdict is **FAIL**, on two blocking
findings. The disposition of every finding is in `ERRATA-121.md`; the reports are not edited to
match it.*

---

VERIFIER: FAIL

## 1. Selftest actually runs and passes — 65 assertions confirmed independently
Ran `cd deliverable/tools && python3 selftest_presence_check.py` myself: exit 0, "65 assertion(s) passed / 0 failed." Independently recounted via AST parsing of `selftest_presence_check.py` (55 static `check`/`check_true` call sites; the parse_line loop over 4 lines and the I7 "drops personal field" loop over 5 fields expand the count to exactly 65, matching the runtime total). Not vacuous: assertions on confirmation logic (`UNCONFIRMED-ABSENT`, `INDETERMINATE` asymmetry), vantage-mode field dropping, and expectation/baseline-currency arithmetic all recompute independent expected values rather than restating tool output. Two minor completeness gaps, not blocking: the "accepts a full URL" tests only check `(vid, handle)`, never asserting `reason is None`; and no assertion covers a non-TikTok domain URL that contains `/video/<digits>` (see Finding 6). NOT BLOCKING.

## 2. v0.1 sha256 and behaviour verified by actually checking out and running v0.1
`git show 9157f731:.../presence_check.py | sha256sum` → `ae8fc947e6b7e7a12d646c282e49991cc6433640a0256acefdd0fa1eff6caa1d`, exact match to the value quoted in both `CHANGELOG-v0.2.md` and `INCREMENT-11.md`. Checked out that exact file and ran its real `parse_line()`: `'2026-08-15'→('2026','x')`, `'tiktok 2024 roundup'→('2024','x')`, `'https://www.youtube.com/watch?v=4'→('4','x')`, `'https://vm.tiktok.com/ZMabcdef/'→(None,None)`. All four match the claims exactly. PASS.

## 3. Confirmation-record arithmetic recomputed byte-for-byte
Re-ran `confirmation_record_121.py` against the committed `ledger/transition-confirm-*.json` and `ledger/corrections.json`: output is byte-identical (`diff` exit 0) to the committed `confirmation-record-121.json`. Independently re-verified sha256 of all five source files matches what the record claims it read. Manually cross-checked all 8 raw readings against the 4 sidecars and hand-verified `all_passes_agree_with_new_state` against the raw 5-state `reconfirmation_states` arrays in every case — all correct. All published tables check out exactly: all-readings 5/5 confirmed (NOT-RETRIEVABLE→RETRIEVABLE) and 1/3 confirmed (RETRIEVABLE→NOT-RETRIEVABLE); genuine-transitions 3/3 and 1/3. These numbers appear identically in `presence_check.py`'s docstring, `CHANGELOG-v0.2.md`, and `INCREMENT-11.md`. The "artefact echo" rule matches vids by identity only (not by run-file), which happens to be correct here because each corrected vid has exactly one correction, but it is a latent fragility if a vid were ever corrected twice. NOT BLOCKING (design note only).

## 4. `presence_check.py` code-level checks (measure/tally/parse_line/read_vantage/baseline_currency)
- `tally()`: denominator `det = RETRIEVABLE+NOT-RETRIEVABLE` genuinely excludes `UNCONFIRMED-ABSENT`/`INDETERMINATE` — confirmed both by reading the code and by the selftest's stub run (`det=2`, `rate=0.5`).
- `--confirm 0`: confirmed by code reading (early-return path skips the confirmation loop and keeps first-pass state) and independently reproduced via the session's own leftover scratch run (`i6.out`/`i6.json`, `"confirmation":{"passes":0,"enabled":false}`, single reading reported as final state).
- `read_vantage`: `asn` mode genuinely strips `ip/city/region/loc/timezone` (checked by direct call with a fake vantage dict — confirmed dropped).
- `baseline_currency`: recomputed by hand against `functional-test-121.json`'s inputs (`2026-08-14T03:43:47Z` vs `2026-08-15T20:00:33Z`) → `1.678` days, exact match.
- **Real defect found by adversarial testing (not in the selftest):** `VIDEO_PATH_RE` matches `/video/<digits>` anywhere in the string with no host check at all. `parse_line("https://www.instagram.com/reel/video/9999999999")` → `('9999999999','x',None)` — **accepted**, not refused. This contradicts the docstring/changelog framing that "a URL from another platform" is refused; in fact only URLs *lacking* a `/video/<digits>` substring are refused, regardless of domain. Functionally low-impact (the probe always targets tiktok.com's oEmbed endpoint using only the extracted digits, so no request goes to the wrong host), but the documentation overstates what the refusal rule actually checks. NOT BLOCKING but should be corrected.

## 5. Default-baseline-path claim verified against actual bundle layout
`find . -iname presence-baseline.json` shows the file exists only at the top-level research directory, not inside `deliverable/`. The bundle's own file is `reference-baseline.json` (different name), confirmed by reading its schema. So `--baseline` defaulting to `presence-baseline.json` when run from `deliverable/tools/` genuinely fails, exactly as both changelog and README addendum claim. PASS.

## 6. Functional-test-121.json arithmetic independently recomputed — all correct
Recomputed by hand and via `presence_check.dated()`/`expectation()` logic against `deliverable/reference-baseline.json`: `age_y` for both live vids (4.852345837452785, 3.2481053058534237), `created_utc` timestamps, `expected_absent_rate` (0.16248363445928254) and its CI bounds, `baseline_currency.age_days_at_measurement` (1.678) — every one matches the committed JSON exactly. The leftover scratch file `livelist.txt` (session's own working file, still present in the shared scratchpad) matches the 7-line input described in `INCREMENT-11.md` exactly (3 valid ids + the 4 adversarial refused lines). PASS on all arithmetic in this file.

## 7. BLOCKING — the "20:29 UTC" re-confirmation and "14 h 58 m" claim is false and chronologically impossible
`INCREMENT-11.md` states: *"...was still `NOT-RETRIEVABLE` at 20:29 UTC, through five further re-requests. That is an independent re-confirmation 14 h 58 m later..."* — and `deliverable/README.md`'s addendum repeats: *"...which stopped being true at 20:29 UTC today."*

The only committed artifact of this re-confirmation, `functional-test-121.json`, shows `"started_utc": "2026-08-15T20:00:33Z"`, `"finished_utc": "2026-08-15T20:00:44Z"` — not 20:29. The gap from the "found at 05:31 UTC" disappearance to the actual run is **14h 29m**, not 14h 58m (computed: `20:00:44 − 05:31:27 = 14:29:17`). The value "14 h 58 m" is arithmetically consistent only with a 20:29 timestamp (`20:29:00 − 05:31:27 = 14:57:33`, rounds to "14 h 58 m"), which never happened.

Worse: the whole commit `ffebcf56` (containing `INCREMENT-11.md` and the README addendum making this claim) is timestamped **2026-08-15T20:02:47Z** (`git show -s --format=%cI ffebcf5`) — 26 minutes *before* the claimed 20:29 UTC event could have occurred. The claim describes, in the past tense, an event that had not yet happened at the moment it was committed. This is not a rounding error; it is a false, checkable, temporally-impossible claim stated as an observed fact in two files. BLOCKING.

## 8. BLOCKING — the "0.7 s against 10.7 s" vantage comparison is not what it is presented as
`INCREMENT-11.md`: *"`--vantage none` made no third-party call (0.7 s against 10.7 s)."* This reads as an apples-to-apples demonstration that disabling the geolocation call saves ~10 seconds.

Leftover scratch files from the session's own working directory (`i6.out`, `i6.err`, `i6.json`, `one.txt` — never committed, found by chance while sharing the scratchpad path) reveal the true source of "0.7 s": a **1-item** list (`one.txt` = `"12345"`) run with **`--confirm 0`** (confirmation disabled) and `--vantage none`, actually testing the I6 missing-baseline behaviour, not a vantage-isolation test. Meanwhile "10.7 s" is `functional-test-121.json`: a **3-item** list with the **default `--confirm 5`** (one item needing 5 re-request passes) and `--vantage asn`. The two runs differ in three variables at once (item count, confirm passes, vantage mode); the `measure()` loop's own sleeps alone (`ledger.DELAY=1.0`, confirmed in `deliverable/tools/ledger.py`) force ≥7 s for the 10.7 s run regardless of vantage mode, so the true isolated cost of the geolocation call is on the order of ~0.3–1 s, not ~10 s. The comparison as stated misattributes essentially the entire time difference to `--vantage none` when it is overwhelmingly due to `--confirm 0` and fewer items. This is a checkable, materially misleading quantitative claim. BLOCKING.

## 9. "26 of 31 conditions untouched" — arithmetically reconcilable but not self-evident
`CONDITIONS-120.md` lists 32 conditions (V1–V16, I1–I16); only I16 is marked "DISCHARGED TONIGHT" at session 120, leaving 31 "carried." `CHANGELOG-v0.2.md`/`INCREMENT-11.md` claim v0.2 leaves "26" or "twenty-six" of these untouched. The tool itself only closes I3, I4, I6, I7 (4 conditions) — 31−4=27, not 26. The number "26" only reconciles if the README addendum's correction of the "Unmodified since it was written" line (which the disposition table names as V14, "reword 'unmodified since it was written'... ACCEPTED, CARRIED") is also counted as touched, giving 31−5=26. This is a plausible but nowhere explicitly stated accounting; a reader cannot verify "26" without independently reconstructing this chain. NOT BLOCKING (the number is defensible once reconstructed) but under-explained.

## 10. K4 citation and other cross-references verified real
`PREREGISTRATION-112.md` §4 "Kill criteria" genuinely contains K4 ("an unreproduced transition is not an event," line 153) as cited throughout `presence_check.py`'s docstring and the changelog. `DAY5-2026-08-15.md` genuinely states the Day-5 close time "05:31:27Z" cited in `INCREMENT-11.md`. `deliverable/tools/ledger.py` and root `ledger.py` are byte-identical (`diff` exit 0), so the "imported, not re-implemented" claim holds. `GAUNTLET-2026-08-15.md` E14/E15/E16 map to I3/I4/I6/I7 exactly as `CONDITIONS-120.md` states. PASS.

## What I could not check and why
- The live-network behaviour of `presence_check.py` against the real TikTok oEmbed endpoint — no network calls attempted, per task scope ("no network needed"); relied on the committed run artifacts and the session's own leftover scratch files instead.
- Whether any *other* ephemeral test runs happened in the session that were not saved and are not present in the shared scratchpad (I only found what happened to survive: `i6.*`, `livelist.txt`, `v01.py`, `v01check/`). Absence of evidence for other undisclosed runs is not evidence of absence, but nothing found contradicts the two findings above — if anything the surviving files are what proved them.
- The 26 remaining Session-120 conditions in `CONDITIONS-120.md` (V1–V13, V15, V16, I1, I2, I5, I8–I15) were not re-verified against source data — out of scope, since this review covers only what v0.2/session 121 changed.
