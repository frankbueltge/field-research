# Verifier 119 — published unedited

*Convened by session 119, 2026-08-14, on `INCREMENT-9.md` at commit `34eb25c`, independently of
the build, with its own code throughout. Its answers are in `CONDITIONS-DISCHARGED-119.md`; they
are not interleaved here.*

---

## VERIFICATION REPORT — INCREMENT-9.md, session 119, commit `34eb25c`

**VERDICT: SOUND WITH QUALIFICATION**

Every numeric claim I could independently recompute from the underlying data reproduced exactly — A1 through A9's headline figures, the byte-range separation, and all of "What the overlay moves" are correct, and I regenerated `instrument-audit-119.json`, `overlay-downstream-119.json`, and `ledger/corrections.json` byte-for-byte (modulo timestamps) from the committed scripts and source data. But I found four defects that the document does not disclose: one false precision claim, one incomplete internal search (A8) papered over by a separate, non-general mechanism, one broken "unchanged" claim about `ledger_diff.py`'s no-flag behavior, and — most seriously — the document's own closing self-check section reports numbers that do not match what running that exact tool against the exact committed document produces.

### Table of recomputed figures

| # | Claim | Claimed | My recomputation | Agree? |
|---|---|---|---|---|
| A1 | ledger observations, all four run files | 14,511 | 2904+3869+3869+3869 = 14,511 | ✅ |
| A1 | re-derivation mismatches | 0 | 0 | ✅ |
| A2 | records both classifiers agree on | 16,712 | 14,511 (runs) + 2,201 (census-results.json) = 16,712, 0 disagreements | ✅ |
| A2 | grid points | 21 | 7×3 = 21, 0 disagreements | ✅ |
| A3 | distinct raw signatures | 3 | 3 (http=200 n=11,755; http=400 n=2,593; URLError/SSL timeout n=163) | ✅ |
| A3 | fallthrough records / pct | 163 / 1.123% | 163 / 1.123% | ✅ |
| A4 | within-record ledger contradictions | 0 (CLEAN) | 0 | ✅ |
| A5 | account records, 4 files | 164 | 102+36+24+2 = 164 | ✅ |
| A5 | contradiction findings | 3 (buzz_award, jere.ronkko, worldpadeltour, all status_field=10222) | same 3, exact match on http, bytes, marker fields, handle==unique_id_returned | ✅ |
| A5 | byte range of the three 10222 records | 365,335–366,046 | 365,335 (worldpadeltour) – 366,046 (buzz_award) | ✅ |
| A6/A7 | run-file aggregates (counts/requested/planned) | CLEAN | CLEAN, all 4 files | ✅ |
| A7 | manifest units / duplicates / handle stability | 3,869 units; 0 dup; 0 unstable handles | same | ✅ |
| A8 | refuted readings still standing | 2 (arutz_7, ask__dani) | 2, confirmed via all 3 sidecars | ✅ |
| A8 | "1 later diff row is the reversal" | 1 | **Incomplete** — see finding 1 below | ⚠️ |
| A9 | served range / not-served range / gap | [364064,366285] (n=101) / [362007,363708] (n=37) / 356 bytes / 0 misclassified | identical, independently computed | ✅ |
| A9 | records with a readable status_field | 138 | 102+36 = 138, all non-null | ✅ |
| Overlay | diff-baseline-day3: 2→1, dropped 7368…54 | as stated | reproduced exactly (own re-run of `ledger_diff.py --corrections`) | ✅ |
| Overlay | diff-baseline-day4: 4→3, dropped 7016…22 | as stated | reproduced exactly | ✅ |
| Overlay | diff-day2-day3: 1→0, dropped 7368…54 | as stated | reproduced exactly | ✅ |
| Overlay | diff-day3-day4: 4→2, dropped both | as stated | reproduced exactly | ✅ |
| Overlay | absent_on_day3 433→432, present 3107→3108 | as stated | 433/432, 3107/3108 | ✅ |
| Overlay | return rate 0.46189%→0.46296% | as stated | 0.4618937644%→0.4629629630% | ✅ |
| Overlay | widened [0.0819,2.5607]%→[0.0821,2.5666]% | as stated | [0.081869,2.560738]→[0.082058,2.566559]% | ✅ |
| Overlay | "unchanged at [session-118's] precision [0.08%,2.56%]" | claimed unchanged | **FALSE for upper bound** — see finding 2 | ❌ |
| Overlay | absence-share deltas −0.0262pp / −0.0261pp | as stated | −0.026164 / −0.026116 pp | ✅ |
| Overlay | day-3/day-4 shares 17.8964→17.8702 / 17.7592→17.7331 | as stated | identical to 4 decimals | ✅ |
| Overlay | loss-rate upper bound stays 0.25% | as stated | raw 0.245437%, corrected 0.245359% — both round to 0.25% | ✅ |
| Population | neither handle in account probe's population | true | `arutz_7`, `ask__dani` absent from T∪C1∪C2 (20+41+41=102) | ✅ |
| Population | pool_sizes 20/41/312 untouched | true | `account-state-117b.json.pool_sizes` = {T:20, C1_pool:41, C2_pool:312}, unaffected by overlay | ✅ |
| Net | requests_made: 0, no socket opened by the 4 scripts | true | grep confirms no urllib/socket calls in the 4 scripts themselves; `ledger.py`/`day4_118.py` are imported but only define functions, `__main__`-guarded, never invoked | ✅ |
| ledger_diff | "without the flag, behaves exactly as it did through days 1–4" | true | **FALSE at the byte level** — see finding 3 | ❌ |
| corrections | "a correction is only what confirmation already ruled" | true | code matches: only rows where `all_passes_agree_with_new_state` is False, and only when all 5 re-requests agree with each other, become `corrected_state` | ✅ |
| Self-check | prose_vs_json.py: "27 numbers audited, 4 unmatched" | 27 / 4 | **actual run: 30 / 6** — see finding 4 | ❌ |
| Self-check | prose_vs_json.py: "12 extremal claims" | 12 | **actual run: 16** | ❌ |

### Mismatches between the prose and the machine-written files

**Finding 1 — A8's search for contaminated diffs is one-directional and misses two of the three real cases.**
`audit_instrument.py`, lines 453–461, only follows the contaminated run file forward (`if dj.get("run1", {}).get("path") != run2: continue`). It never checks diffs where the contaminated file is the *second* run of the pair. I independently scanned all six raw `ledger/diff-*.json` files and found that besides the one reversal A8 reports (`diff-day3-day4.json`, `7368171405361351954` NOT-RETRIEVABLE→RETRIEVABLE), two more diffs also carry a refuted reading as a transition purely because A8 never looked backward:
```
FOUND in ledger/diff-baseline-day3.json: vid=7368171405361351954 RETRIEVABLE -> NOT-RETRIEVABLE
FOUND in ledger/diff-baseline-day4.json: vid=7016669364938149122 RETRIEVABLE -> NOT-RETRIEVABLE
```
`instrument-audit-119.json`'s A8 verdict ("2 refuted readings still stand in run files; **1** later diff rows are reversals…") therefore undercounts. In practice this doesn't corrupt the published document, because `downstream_119.py` independently checks a *hardcoded* tuple of four diff names (`"diff-baseline-day3", "diff-baseline-day4", "diff-day2-day3", "diff-day3-day4"`) that happens to include both diffs A8 missed — I confirmed by inspecting `diff-baseline-day2.json` and `diff-run1-run2.json` that no *other* diff file references the two contaminated run files, so the hardcoded list is currently complete. But that completeness was never verified programmatically by either script; it is a coincidence of the current file set, not a guarantee.

**Finding 2 — "unchanged at that precision" is false for the upper bound.**
INCREMENT-9.md, line 137: *"widened [0.0819 %, 2.5607 %] → **[0.0821 %, 2.5666 %]** — session 118 printed [0.08 %, 2.56 %] and it is unchanged at that precision."*
Recomputed corrected upper bound = 2.5665594702669717%. Rounded to 2 decimal places this is **2.57%**, not 2.56%. `round(2.5665594702669717, 2) == 2.57` in Python. The raw value (2.5607383…%) does round to 2.56%, so the *raw* figure is unchanged, but the *corrected* one crosses the rounding boundary the sentence claims it doesn't cross. This is exactly the kind of rounding-boundary error the audit is supposed to catch.

**Finding 3 — `ledger_diff.py` without `--corrections` is not byte-identical to its pre-session behavior.**
INCREMENT-9.md, line 118, and `ledger_diff.py`'s own docstring (lines 23–24): *"Without the flag the file behaves exactly as it did through days 1–4."* I ran the pre-session version (`git show 13f4bc8:…/ledger_diff.py`) and the current version on the same two run files with no `--corrections` flag. The current version's output always adds a `"corrections_applied": {"overlay": null, "n": 0, "rows": [], "note": "raw run files, no overlay applied"}` block that the old schema never had — confirmed against the actual committed `ledger/diff-day3-day4.json`, which lacks the key entirely. All substantive fields (transitions, counts, vantage_guard) are identical, so no number is affected, but "behaves exactly" is not literally true.

**Finding 4 — the document's own closing self-check numbers do not match reality.**
INCREMENT-9.md, lines 170–174: *"**Pass 1: 27 numbers audited, 4 unmatched, all four dispositioned.**"* and line 175: *"**Pass 2: 12 extremal claims**, each checked against its own file."*
Running `python3 prose_vs_json.py INCREMENT-9.md` against the exact committed file (working tree clean, verified with `git status --short`) gives:
```
INCREMENT-9.md: pass 1 — 30 numbers audited, 6 not found in any JSON of this draft
INCREMENT-9.md: pass 2 — 16 claims whose FORM is the form all three published failures took
```
Reproduced twice for determinism. The 6 unmatched are still only the same two video identifiers (`7368171405361351954` ×4 occurrences, `7016669364938149122` ×2 occurrences) — nothing new or alarming in *content* — but the document's stated counts (27/4/12) are stale relative to the text as committed, most likely because the "What the overlay moves" table (which repeats both identifiers) and other later paragraphs were added after the quoted `prose_vs_json.py` run and the summary sentence was never re-run. This is precisely the failure mode `prose_vs_json.py` exists to catch (a stale claim about the draft's own numbers), now present in the sentence that reports the tool's own output.

### What checked out cleanly with no qualification
A1, A2, A3, A4, A5 (including the completeness search I ran across `status_field=None` rows and both account-route files — no missed contradictions exist; the only status_field values present are 0, 10221, 10202, 10222, and only 10222 rows show serving evidence), A6, A7, A9, the four "What the overlay moves" diff counts and all associated statistics, the population-membership check, the network-isolation check, `corrections.py`'s rule (verified in code: only rows from `transition-confirm-*.json` where `all_passes_agree_with_new_state` is False, and only when the 5 re-requests are unanimous, become `corrected_state`; `ledger_diff.py`'s `apply_corrections` only ever reads that overlay dict, so there is no code path today by which an unrefuted state could be silently altered), and the run files themselves (confirmed still carry the uncorrected/refuted states, no `state_source` marker, no in-place edit — D22 is respected).

### Numbered conditions the document must discharge before it can be trusted as written

1. Correct or retract the sentence "session 118 printed [0.08 %, 2.56 %] and it is unchanged at that precision" (line 137) — the corrected widened upper bound rounds to 2.57%, not 2.56%.
2. Re-run `prose_vs_json.py` against the final committed text of INCREMENT-9.md and update the self-reported Pass 1/Pass 2 counts (currently 27/4/12 in prose; actual reproduction is 30/6/16), or explain in-document why the numbers differ.
3. Fix or qualify the claim that `ledger_diff.py` "behaves exactly as it did through days 1–4" without `--corrections` — it now always emits an additional `corrections_applied: null` block not present in the original schema.
4. Extend A8's search to check diffs where the contaminated run file is the *second* run (`run2`), not only the first, so the check's own verdict count is accurate rather than relying on `downstream_119.py`'s separately-hardcoded, unverified list of "the four diffs."
5. Make `downstream_119.py`'s diff enumeration derive from a scan of all `ledger/diff-*.json` files that reference either contaminated run file, rather than a fixed 4-name tuple, so a future fifth contaminated diff cannot be silently omitted.
6. Document the (currently unexercised) collision risk in `corrections.py`/`corrections_mod.load()`: if the same `(run_file, vid)` pair ever appeared more than once across sidecars, the dict comprehension keeps only the last entry silently.

### What I could not check
- I could not verify against the live platform whether `10222` truly means "account served" in any authoritative sense — the document itself disclaims this (A9's "what it does not show"), and I have no way to consult a source TikTok has not published; this is consistent with the document's own stated limits, not a gap I could close.
- I did not re-run the original probes (`ledger.py`, `confirm_transition.py`) against the network, per the task's constraints and the document's own "zero requests" rule — I verified their *code paths* are inert when imported, not that their historical outputs are faithful to whatever the platform actually returned in the past.
- `census-results.json`'s 2,201 records were taken on trust as to their *original* collection provenance (I only verified they parse and classify consistently, which is what A2 requires) — I did not re-derive session 109's census.
