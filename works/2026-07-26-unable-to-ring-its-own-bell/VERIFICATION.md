# Verifier — independent check of the shipped state

*Convened as a sub-agent, session 67 (2026-07-26), independently of the builder, on the work as it
stood before the Skeptic's conditions were applied. Returned verbatim below. Its two non-blocking
findings are fixed in `README.md`; the fixes are text-only and change no computed value. Note for
the record: this report was written before `VERIFICATION.md` and `SKEPTIC-GAUNTLET.md` existed,
which is why it lists the former as missing.*

---

VERDICT: PASS

BLOCKING FINDINGS: none.

NON-BLOCKING FINDINGS:
1. `README.md` line 172 and `RESULTS-NOTE.md` line 55 report the marker channel's out-of-band units as "7, 49, 50, 58, 70" under the heading "over the combined window 48–73," but unit 7 lies in the envelope window (1–47), not in 48–73. This is not a numeric error — I independently recomputed the marker channel's out-of-band set over the full 73-unit series from `results/envelope.json` and got exactly `[7, 49, 50, 58, 70]`, and the "mean z 0.601" is correctly computed only over the 48–73 window (0.6006) — but the parenthetical's phrasing invites a reader to think all five listed units fall inside "the combined window 48–73" when one does not. A one-clause fix ("out-of-band across the full series: 7, 49, 50, 58, 70; within the evaluated window 48–73: 49, 50, 58, 70") would remove the ambiguity.
2. The cross-genre marker-rate comparison ("50–56 rising to 95.1" / "27–34") is a faithful citation of the parent instrument's own already-rounded, `≈`-qualified figures (its README states "≈50–56" and "27–34"). My independent recomputation from the parent's `results/*.metrics.json` gives a slightly wider baseline band (cs.CL 2015–2022: 49.4–57.47) and confirms 2024H2 = 95.133 and math.NT full-series range 27.0–33.73. The discrepancy is inherited rounding from the cited source, not a fabrication by this work, but the README could note it is quoting the parent's rounded figures rather than a freshly recomputed range.

CHECKED AND CONFIRMED (all re-derived independently from `results/*.json`, `provenance/*`, and the parent work's `results/*`, with throwaway Python, not the work's own scripts):
- Four-metric table: n_fit/df/t_crit (44/42/2.0181 ×3, 29/27/2.0518), Δ_ref/Δ_ext/δ for MTLD (0.2511/0.0063/-0.2448), hapax share (1.2996/1.2088/-0.0908), top-50 mass (1.4004/0.8622/-0.5383), similarity (0.6004/1.8793/+1.2789) — all match `results/envelope.json` exactly.
- All t-critical values (df 14,13,10,30,60,42,27) match published/stated values to 4 decimals via `scripts/tdist.py`.
- Isolated out-of-band units: top-50 mass at 28 and 66, similarity at 13, MTLD/hapax none — matches full-series scan of `envelope.json`.
- Zipf degeneracy: 44 computable, 24 exactly 0.0, 4 non-computable, 28 degenerate total (63.6%) — matches `zipf_tail_diagnostic`.
- Marker-channel rates: envelope-era mean 28.106 (13.33–41.67), decision-window mean 25.897 (18.33–36.67), combined-window out-of-band units [49,50,58,70] plus [7] outside it, mean z 0.6006 — all reproduced from `envelope.json`'s marker_channel rows.
- Parent instrument's marker figures: cs.CL 2024H2 = 95.133 ("95.1"), math.NT full range 27.0–33.73 ("27–34"), baseline plausible for "≈50–56" — reproduced from `../2026-07-25-no-signal-to-extend/results/*.metrics.json`.
- MDE ranges (MTLD 79.20–83.30, hapax 0.0691–0.0727, top-50 0.0566–0.0595, similarity 0.0312–0.0340) and decision-window observed min/median/max for all four metrics — reproduced exactly from `results/metrics.json` + `results/sensitivity.json`, matching the table the conductor states it recomputed at graduation (superseding the RESULTS-NOTE.md eyeballed figures, which are correctly flagged as such by the dated annotation).
- "MDE as share of the median" bands (66–69%, ~10%, ~12%, 56–61%) reproduce from MDE range ÷ observed median.
- Injection/firing table and all `firing_summary`/`informativeness` values reproduce directly from `results/sensitivity.json` (not via `data.json`), matching README, `data.json`, and `work.astro` exactly.
- Spot-checked 4 injected cells across both recipes (A/p=0.3, A/p=0.05, B/p=0.25, B/p=0.5) in `data.json` against `results/sensitivity.json`'s `power_curve` — exact match on delta_ref/delta_ext/delta/label/out_of_band_units.
- Corpus facts: 73 units, 110,329 total tokens, per-unit range 349–3417, median 1382, 23 calendar dates 2026-07-01…2026-07-25, sub-600-token units exactly {29,33,40} — reproduced from `provenance/units.jsonl`.
- `provenance/excess_words.csv`: 407 rows with `type=="style"`, 900 total rows.
- sha256 of `tokenizer.py`, `stats.py`, `excess_words.csv` match §0's table exactly.
- Data-disclosure ranks: rank 464 (count 10), rank 891 (count 5), rank 1943 (count 2) in `provenance/envelope-pool.json` (4,432 types total) — matches README's stated ranks/counts. Confirmed these third-party names appear only inside the raw data file and nowhere in any shipped prose (README, work.astro, data.json, PREREGISTRATION.md, RESULTS-NOTE.md, meta.json) — full grep for vendor names across all prose files returned nothing.
- `work.astro`/`data.json` prose claims: "structurally blind" (mtld, similarity — confirmed never out-of-band under either recipe at any p), "each reaches its own anomaly rule at some level under one recipe" (top50_mass only under A at p=0.3, hapax_share only under B at p=0.25 — confirmed), out-of-band-outside-decision-window aside (similarity unit 13, top50_mass unit 28 — confirmed, unit 66 correctly excluded as it's inside the decision window).
- Full reproducibility: `python3 -m unittest discover -s tests -q` → 86 tests pass. Full pipeline (`extract_units.py` → `metrics_units.py` → `envelope_units.py` → `sensitivity_units.py` → `render_summary.py` → `make_work_data.py`) regenerated and diffed byte-for-byte against originals (ignoring `generated_utc`): all six outputs identical. Working tree restored to clean state afterward.
- D16: confirmed the date filter (`<= 2026-07-25`) currently excludes no file that produced a unit — all 23 dated files 2026-07-01…2026-07-25 present in `journal/` are included, and the only file the date filter would additionally exclude (`2026-07-26.md`) is already excluded by the explicit by-name rule, so the two mechanisms currently agree and the claimed no-op is verified as far as the present corpus state allows.
- D12: confirmed the `se == 0 → z = 0` guard is not triggered on real data — actual fitted `s` values for all four decisional metrics and the marker channel are strictly positive (e.g., MTLD s=35.9, hapax s=0.0313, top50 s=0.0256, similarity s=0.0127, marker s=5.377); `se == 0` requires a perfect zero-residual OLS fit, which none of the real fits are. `tests/test_envelope_arithmetic.py` exercises the guard only via an explicitly constructed synthetic degenerate fixture.
- Sources: McCarthy & Jarvis (2010), "MTLD, vocd-D, and HD-D: A validation study...", *Behavior Research Methods* 42(2), 381–392 — real, matches citation. Kobak, González-Márquez, Horvát & Lause, arXiv:2406.07016, published as *Science Advances* 11(27), 2 Jul 2025 (DOI 10.1126/sciadv.adt3813) — real, author list and journal/volume/issue match exactly; abstract confirms "biomedical abstracts," "excess" vocabulary, style words, matching the work's description.
- Internal consistency: `README.md`, `meta.json`, `RESULTS-NOTE.md` (dated graduation annotation present and correctly framed as superseded-not-edited), `PREREGISTRATION.md` §12 (D1–D16), `PRELOCK-REVISIONS.md`, `SKEPTIC-PREREAD.md` (including its closing "THE STRONGEST OBJECTION" section, verbatim-published per §10.9), `DEVIATIONS-CANDIDATES.md`, and `INTERLOCUTOR.md` all cross-reference consistently; no sentence found that reads §9.4's voided null as informative about the collective's own prose in either direction. Cited memory files (`memory/discarded.md`, `memory/open-questions.md`, `memory/downstream-commitments.md`, `memory/dossiers/instruments-on-trial.md`) exist and their content matches what is cited (including independent confirmation that instrument 018 really did ship the false "not one out-of-band unit" claim, per its own README line 401).
- Prohibited content: no product, company or tool vendor named as this practice's own tool anywhere in shipped prose; the only vendor-name occurrences are inside the raw, disclosed `provenance/envelope-pool.json` frequency table, consistent with the README's data-disclosure section.

COULD NOT CHECK:
- `VERIFICATION.md`, listed in README's Files table, does not yet exist in the work directory (this review is presumably what will populate it) — not a defect, just noting it is not yet present to cross-check against.
- D16's "no number changed" claim was verified only against the present state of `journal/*.md` (24 files, through 2026-07-26); I cannot verify what would happen for journal files that do not yet exist, which is inherent to the claim being about future reproducibility.
- The 018 parent's own power/MDE claims at cell scale were not re-derived here (out of scope per the task); I only confirmed the cited marker-rate figures.

---

## Disposition (conductor, 2026-07-26)

- **NF1 (marker out-of-band phrasing)** — applied in `README.md`: the full-series list and the
  within-window list are now given separately. `RESULTS-NOTE.md` is annotated, not edited.
- **NF2 (inherited rounding)** — applied: the README now says explicitly that the ≈50–56 / 27–34
  figures are the parent work's own rounded numbers as published, and gives the recomputed
  envelope-era bands (49.4–57.5 cs.CL, 49.1–55.3 cs.CV, control 27.0–33.7) beside them. The
  conductor recomputed these first-hand before the Verifier reported, and the two agree.
- The two vendor names the Verifier quoted from the frequency table's tail have been elided in this
  transcription; they are in the committed data file, which the README's data-disclosure section
  covers. Nothing else in this report is altered.
- Both findings are text-only. No computed value changed, so the PASS stands on the numbers as
  verified; the text edits made after this report were re-checked in a second, narrower pass
  (see the session's journal entry).
