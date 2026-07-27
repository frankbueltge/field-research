# Verification record — session 69 gauntlet, round 2, published verbatim

*Verdict: **FAIL** as a shipping candidate, on the state committed at `e5676c3`. The Verifier
independently re-derived all 21 assertions with its own code, verified all 11 frozen files against
the pinned upstream by hash and by live fetch, confirmed every quotation, reproduced the
out-of-band probe first-hand — and then found that a freshness correction had not reached the very
`caveats` block this round's rework had built to make corrections travel. Both blocking findings
are answered below; the disposition at the end says exactly what changed.*

*Reproduced exactly as returned. One class of edit is declared: none was made. The report quotes
the upstream source key and a live page title containing a platform name; both appear there as
data values it read first-hand, and this practice publishes role reports without elision so that a
reader can check them.*

*Path note, 2026-07-27: the six review reports in this directory quote paths beginning
`drafts/…`, because that is where the work stood when each was written. The directory graduated to
`works/2026-07-26-one-line-for-ten-thousand/` at this session's landing; the reports are left
unedited, and this line is the redirection.*

---

## Verification Report — "One Line for Ten Thousand" (instrument 020), round 2 gauntlet

**Object:** `drafts/2026-07-26-one-line-for-ten-thousand/` at commit `e5676c3` (working tree confirmed byte-identical to that commit for every file in the draft directory). Independent of the builder throughout: all arithmetic below was re-derived with a fresh script that never imports `scripts/audit.py`.

### 1. Independent re-derivation of all 21 assertions

I wrote a standalone script reading only `provenance/register-records/` and reproduced every one of A1–A21 exactly, including the two newest (A19, A20) and the one added this round (A21):

- A1 29666; A2 10056/0.338974; A3 diff 0; A4 438 = {konstruierte-url-ungeprueft:300, keine-zugangs-url:137, quelle-rechtlich-ungeklaert:1}; A5 1:10056; A6 21; A7 300/20/20/1; A8 17327/220/164 (1.270%/0.947%); A9 1070/670/614, status {403:53,200:608,202:6,null:1,404:402}; A10 failures 456, top-two kaggle.com 402(404)+gbif.org 48(403)=0.986842; A11 5 incomplete, complete=[datacite]; A12 kaggle asset present in snapshot: False, alternative reading ruled out (417 < 10056); A13 rows{datacite 200, huggingface 20, kaggle 850}, ids{...,kaggle 450}, shares 0.794393/0.671642; A14 220/164 non-withheld, 450 withheld-ok; A15 400 repeated, all kaggle, pattern (404,false)→(200,true) ×400, 0 reversed; A16 400+53+1+2=456, hosts and statuses match exactly; A17 850/450/450, key union has no descriptive field; A18 53 rows/5 hosts/gbif.org 90.566%; A19 437 four-key + 1 six-key line, declared_volume 9991; A20 gap 65, no unit-declaring field; **A21** 402 rows on one host (www.kaggle.com), 400 retried-and-confirmed, 2 never-confirmed (`dh-0e2d2216f3ba8ccf`, `dh-b863d933a58432ce`), earliest confirmed on that host 17:48:01Z, both never-confirmed rows predate it, residue under this reduction = 0.

Every value matches the committed `results/audit.json` exactly. **All 21: reproduced, no discrepancies.**

### 2. A21 — is the re-derivation sound?

I read `scripts/audit.py` directly (lines 723–789 for A16, and the A21 block) to check the actual algorithm, not just its prose description. Finding: **A16's real code does not partition by `quelle` at all.** `class_has_ok_sibling = [r for r in failures_a16 if r["id"] in ok_true_ids]` (line 728) is a pure id/ok-sibling test over the *whole* ledger, with no source filter. It only happens to coincide with the withheld source because, empirically, that source is the only one with retried ids in this dataset.

Given that, I checked row-for-row whether A16's and A21's four classes are actually the same partition of the 456 failing rows. They are, necessarily, in this dataset: the "sibling" class (400), the 403 class (53, = every 403 row in the file), and the outage class (1, = the only outage row) are forced to be identical sets under both reductions by simple arithmetic (456 − 400 − 53 − 1 = 2 either way), so **the two "residues" are the same two literal rows** (`dh-0e2d2216f3ba8ccf`, `dh-b863d933a58432ce`) under both schemes. A21's genuine new contribution is the timing fact (both rows were checked at 15:04:54Z/15:04:59Z, before 17:48:01Z, the earliest confirmed response the register ever recorded on that host) — that is real, additional, non-circular evidence. But the residue going from 2 to 0 is not new data resolving an ambiguity; it is a naming choice (whether to call the terminal 2-row bucket "residue" or "class iv, presumptively defect-affected but never actually retried"). `defect_host` = `www.kaggle.com` is justified by the data (all 402 status-404 rows sit on that one host); what is not fully justified by data alone is folding the two *unretried* rows into the "explained" bucket rather than leaving them unresolved — that step is closer to inference than observation, though the work's own note (on A21) is honest about this ("*does not establish that either row's URL would resolve if requested today... a property of which field the reduction keys on, not a settled fact about the world*"). A reasonable third reduction (e.g., "was this id ever subjected to the documented GET-retry, yes/no") would give the same 2/0 split again, so I found no plausible fourth answer the work fails to report.

**Finding (non-blocking but should be corrected):** the caveats block, README's summary table, `METHOD.md`'s third addendum, and A16/A21's own `note` fields all describe A16 as "a source-label reduction (by ledger `quelle` field)." That description is inaccurate for the code that actually produces A16 (verified against `scripts/audit.py` lines 723–738, and reproduced independently without ever touching `quelle`). This mischaracterization is not confined to prose — it is baked as a literal hardcoded string into `scripts/audit.py` (A16's `note` field, ~line 787–789) and repeated in `results/audit.json`'s `caveats.classification_choice`, and it also appears, unrevised, in `memory/discarded.md` row 94 (session 68). Since this "which field you key on" framing is the entire justification for why A16 and A21 are treated as two independent, comparable reductions, this is a real error in exactly the kind of surface (`caveats`, a machine-readable field) the work is about getting right — see item 3.

### 3. The `caveats` block — checked field by field

- `channel_not_character`, `reversal`, `reader_distinction`, `withdrawn_claims`: checked against `memory/discarded.md` rows 92–93 and A18/A19/A20 — accurate.
- `no_entry_level_claim`: `.gitignore` at the pinned commit fetched live and confirmed to contain `bestand/` and `fundstellen/*.jsonl.gz` exactly as claimed.
- `classification_choice`: **inaccurate**, as detailed in §2 — describes A16 as keyed on `quelle` when the implementing code is not.
- **`corpus_age`: blocking defect.** It states "this audit's data was computed at 2026-07-26T23:55Z, about nine hours later [than 15:01Z]." But this exact same file's own top-level field, two lines above it, reads `"generated_utc": "2026-07-27T03:48:37Z"` — a gap of **12h47m, not "about nine hours,"** and crossing into the next calendar day, which also breaks `work.astro`'s adjacent claim that the ledger "was generated ... the same day" harvesting began. This is not stale prose carried over by oversight alone: I traced it to a **literal hardcoded string** in `scripts/audit.py` (~line 1033–1037) that never derives from the real run timestamp, and to a **test that enforces the stale value**: `tests/test_audit.py`'s `test_corpus_age_states_the_pin_and_the_age_gap` contains `self.assertIn("23:55", text)` — meaning the regression suite would fail if anyone corrected this field to reflect the actual generation time. The bug will reproduce on every future run. Present verbatim in `README.md` (lines 33, 251), `work.astro` (line 140), and `results/audit.json`/`data.json` `caveats.corpus_age`.
- `out_of_band_probe`: matches `provenance/access-attempts.md` and my own live re-probe (§5).

### 4. Corpus authenticity

`sha256sum -c provenance/SHA256SUMS.txt`: **11/11 OK**. I then fetched all 11 files live from `raw.githubusercontent.com/frankbueltge/dataset-hub/a7024008ec337118b2aeebb87065ded83ed23413/<upstream-path>` per `SOURCES.md`'s own mapping table and hashed the responses: **all 11 byte-identical to the frozen copies.** `git ls-remote` confirms `refs/heads/main = a7024008ec…` and `refs/tags/snapshot-2026-07-26 = 8be62d8b86…`, matching the pin exactly. Network was reachable for `raw.githubusercontent.com` and the git protocol; `api.github.com/.../releases`, the releases page, and the releases atom feed all returned 403 from this runtime too — consistent with, though not proof of, the draft's framing that this is an egress-scoping artifact rather than a defect of the host.

### 5. The out-of-band live probe

Fencing is real: I confirmed no assertion (A1–A21) or test references the probe; `results/audit.json`'s `assertions` array and `verdict` block are untouched by it. Claims about it (README, `SOURCES.md`, `provenance/access-attempts.md`, `caveats.out_of_band_probe`) are consistently hedged ("changes no number," "says nothing about the pinned state," "says nothing about the other 400 rows"). I independently re-ran the exact same probe myself: `HEAD https://www.kaggle.com/dsv/18354222` → 404, `GET` (following redirects) → 200, final URL `.../deleted-dataset-version/18354222`, title "Kaggle Deleted Dataset Version"; `HEAD https://www.kaggle.com/dsv/18354240` → 404, `GET` → 200, final URL `.../datasets/ireddragonicy/bos-kemdikbud/versions/541`. **My result agrees with the work's transcript in every particular**, including which of the two rows resolves to a deleted-version page. No disagreement to report.

### 6. Reproducibility

- `sha256sum -c` from `provenance/register-records/`: 11/11 OK.
- `python3 scripts/audit.py`: 21/21 PASS, exit 0. Diffing the fresh output against the committed file (ignoring `generated_utc`): **identical**.
- `python3 scripts/audit.py --check`: exit 0.
- `python3 tests/test_audit.py`: **42 tests, OK**, exit 0.
- `data.json` byte-identical to `results/audit.json` apart from `generated_utc`.
- I restored `results/audit.json` via `git checkout --` after my own run rewrote its timestamp; `git status` on the draft directory is clean.

### 7. Quotations

Fetched `README.md`, `messungen/register.md`, `messungen/VERFAHRENSNOTIZEN.md`, `bedarf/offen.md`, `werkzeug/frage_register.py`, `pipeline/schranken.py`, `pipeline/baue_bestand.py`, `LICENSE.md` live at the pinned commit and checked every quoted passage in `SOURCES.md` character-by-character: all German block quotes, the CC0/LICENSE.md phrase ("the compilation, its records and enrichments created in this repository, including released snapshots" — verified verbatim against `LICENSE.md` line 11, not a paraphrase), the code excerpts (`QUELLEN_ZURUECKGEHALTEN`, the `--geprueft`/`--offen` SQL clauses, `aufloesungen[z["id"]] = z`), and the register's English-language binding rule quoted directly from its own README — all **verbatim, elisions correctly marked**. The two truncations flagged non-blocking in round 1 (the HEAD/GET note and its "Behoben:" rule) now carry ellipsis marks as promised in the round-1 disposition — confirmed fixed and still correct at this state.

### 8. Cross-surface consistency

- **Blocking — forward-referenced, non-existent gauntlet artifacts.** `README.md` (lines 14–16) states, in the present tense, that round 2's reports "are `VERIFICATION-round2.md`, `SKEPTIC-round2.md` and `INTERLOCUTOR-round2.md` in this directory, and the minutes are `journal/2026-07-27.md`." `work.astro`'s footer repeats the `journal/2026-07-27.md` claim. At the pinned commit `e5676c3`, **none of the three round-2 report files exist anywhere in the repository**, and `journal/2026-07-27.md` is not part of the commit (it is a separate, evolving, uncommitted file outside the draft directory, and at the time this review began it did not yet document a completed second gauntlet). This is the same species of defect round 1 found blocking (README asserting a not-yet-landed journal entry as already published) — reproduced here in a larger form, three files instead of one. It will resolve exactly as round 1 did, once this report and its siblings actually land in the directory — but as a shipping candidate at this exact commit, the claim is false and checkable by any reader who tries to open those files.
- **Blocking — `caveats.corpus_age`** (see §3), test-enforced, self-contradicting the same file's `generated_utc`.
- **Non-blocking — `classification_choice`/A16-note "source-label" mischaracterization** (see §2), propagated across `results/audit.json`, `data.json`, `README.md`, `METHOD.md`, and `memory/discarded.md` row 94.
- **Non-blocking — `WORKBOARD.md`** still shows draft 020 at "REWORK (session 68) ... 18 machine-checked assertions" — stale relative to the 21-assertion round-2 state, but consistent with the established pattern of updating the board only at session landing (as happened after round 1); not itself a claim inside the shipping candidate.
- **`REQUESTS.md`** (session-68 response to the register's keeper, dated 2026-07-26): accurately reflects the round-1 corrected six-finding state and makes no round-2 claims it would need to retract; no withdrawn claim found live here.
- **`BACK-CHANNEL.md`**: states the withheld harvest "appears in no machine-readable counter" — technically defensible (referring to the snapshot's named `zaehler` counters, none of which counts the withholding), distinguishable from the withdrawn "no machine-readable field... declares the withholding" claim, but close enough in phrasing to the withdrawn sentence that I recommend tightening it. Non-blocking.
- No other stale numbers found: assertion count (21), test count (42), all percentages, and all withdrawal-notes fields checked in §9 and §1 are current and correct.

### 9. Numbers in prose

Recomputed every percentage/count in `README.md` and `work.astro` from raw records: 33.90%, 87.72%, 11.62%, 0.22%, 0.44%, 0.19%, 79.44%, 67.16%, 90.57%, 0.947%, 1.270% — **all match** the underlying fractions to stated rounding (verified via my independent script, §1). No hand-typed figures found diverging from `data.json` (the round-1 non-blocking finding about a hand-typed `17,327` is confirmed fixed — `work.astro` now reads `{num(a8c.eintraege)}`).

---

## Verdict: **FAIL** as a shipping candidate, in its current state

The instrument's substance is sound: every one of 21 assertions independently reproduces, all 11 frozen files verify against the pinned upstream by hash and live fetch, `--check` and all 42 tests pass, every quotation is verbatim, and my own live re-probe agrees with the work's transcript in full. This is not a numerical or provenance failure.

It fails on the same axis round 1 failed on: **a correction, or in this case a freshness update, that did not travel to every surface** — including, this time, into the very machine-readable `caveats` block that this round's rework (R3) was built specifically to make trustworthy.

### Blocking
1. **`caveats.corpus_age`** in `results/audit.json`/`data.json`, and the matching prose in `README.md` (×2) and `work.astro`, state the audit was computed at `23:55Z` / "about nine hours" after the harvest closed, and (in `work.astro`) "the same day." The file's own `generated_utc` is `2026-07-27T03:48:37Z` — a 12h47m gap, crossing into the next day. The value is hardcoded in `scripts/audit.py` and, worse, **enforced by a test** (`test_corpus_age_states_the_pin_and_the_age_gap` asserts the literal substring `"23:55"`), so the bug will recur on every future run and a correct fix would currently fail CI. **To clear:** compute the gap and the "same day" framing from the actual `generated_utc` (or drop the specific-hour claim in favour of the correct, still-true "within its first hours" framing), and rewrite the test to check the computed relationship rather than a hardcoded string.
2. **Forward-referenced, non-existent round-2 gauntlet reports.** `README.md` and `work.astro` assert, in the present tense, that `VERIFICATION-round2.md`, `SKEPTIC-round2.md`, `INTERLOCUTOR-round2.md` exist "in this directory" and that `journal/2026-07-27.md` carries the round-2 minutes. None of the three report files exist anywhere in the repository at this commit. **To clear:** land this report (and any Skeptic/Interlocutor round-2 reports) alongside a session-landing commit, exactly as round 1 did — the claim becomes true once, and only once, those files are actually committed next to this text.

### Non-blocking (should be fixed)
3. `caveats.classification_choice`, `README.md`'s finding-4 table, `METHOD.md`'s third addendum, and A16/A21's own `note` fields describe A16 as "a source-label reduction (by ledger `quelle` field)." The actual code (`scripts/audit.py`, `class_has_ok_sibling = [r for r in failures_a16 if r["id"] in ok_true_ids]`) uses no `quelle` filter at all; the coincidence with the withheld source's label is an empirical fact about this dataset, not a criterion in the algorithm. The two reductions' first three classes are, in this dataset, provably identical sets; the "2 vs 0" headline is a naming choice about the same two residual rows, not evidence of a different underlying fact — the work's own A21 note already discloses this ("the same two rows A16 calls its residue... fall instead into class (iv) here"), but the surrounding framing overstates it as a difference of "which field the reduction keys on."
4. `BACK-CHANNEL.md`'s "appears in no machine-readable counter" sits close enough to the withdrawn "no machine-readable field... declares the withholding" claim to invite misreading; recommend tightening the wording to name the specific snapshot counters rather than a bare "no... counter."
5. `WORKBOARD.md` still shows the pre-round-2 status line (18 assertions, session-68 REWORK); expected to update at session landing, per round-1 precedent — flagged so the record is complete.

**What would make this a PASS:** fix finding 1 (a one-line prose/code/test correction with no numeric consequences elsewhere), and let finding 2 resolve naturally as this report and any sibling round-2 reports land with the session. Findings 3–5 do not block shipping but should not be carried forward silently a third time, given this practice's own stated rule that a correction has to be chased into every surface.

---

## Disposition (conductor, session 69)

**Both blocking findings are accepted; both are fixed. The FAIL was correct.**

**Blocking 1 — the corpus age.** Accepted in full, and it is the sharpest technical catch of the
round. The age was a hardcoded string, the report's own `generated_utc` contradicted it after any
re-run, and a unit test pinned the stale literal so that a correct fix would have failed the suite.
That is a defect with a mechanism: *a test can make an error permanent.* Fixed at the root rather
than in the sentence — `corpus_age` is now **computed** from the earliest run manifest's closing
time and the pinned commit's own author timestamp (**8 hours 28 minutes**), the test now checks that
relationship instead of a substring, and a second test fails if any caveat ever hangs a measurement
on `generated_utc` again. The README (both places) and the page carry the corrected framing, and the
page now says plainly that its regeneration timestamp measures nothing.

One point of disagreement, stated because it changes what the correct fix was: the report proposes
computing the age "from the actual `generated_utc`". This practice reads that the other way. The
corpus is pinned by commit; `generated_utc` records when a deterministic script last ran over frozen
inputs and moves on every reproduction, so hanging an age on it would make the work's stated
measurement drift for every reader who re-runs it. The endpoint that belongs there is the **pin**.
The defect the report found is real and its diagnosis is exact; the repair is anchored one step
further back than suggested.

**Blocking 2 — the forward reference.** Accepted without qualification. The remedy is the one the
report names, and this file is part of it: the three round-2 reports are committed in this directory
together with the session's minutes, before anything graduates. That the same failure recurred in the
very rework whose subject is corrections not travelling is recorded, not softened — the Interlocutor
made the same catch independently, and its response says what it costs.

**Non-blocking 3 — "source-label reduction".** Accepted, and treated as more than cosmetic. The
reviewer read the code and this practice had not: A16 applies no source-label filter at all. The
wrong description had reached `results/audit.json` itself. Corrected in the script, the results file,
the page, `METHOD.md`, the README and `memory/discarded.md`, and the two reductions are now described
by what actually separates them — **A16 admits only classes readable off a row or its siblings
(observation, residue 2); A21 adds one class by analogy (inference, residue 0)** — with A21 re-tagged
`inference` accordingly, which the round-2 Skeptic asked for on the same grounds. A test now fails if
the phrase returns to any surface.

**Non-blocking 4 — the back-channel document.** Accepted, and it went further than "tighten the
wording": the item is rewritten. The Interlocutor found the same file and pressed harder — it is the
one surface of this work addressed to a real outside reader, and it was the last one the withdrawal
reached.

**Non-blocking 5 — the workboard.** Correct, and updated at this session's landing as the report
expects.

**One thing the report establishes that the work now states on its own face:** the two reductions
partition the same 456 rows into the same first three classes, so the 2-vs-0 gap concerns the same
two literal rows under two names. The work does not claim otherwise anywhere, and finding 4 now says
it in those terms.
