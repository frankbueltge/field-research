# Verification — the 2026-08-04 second-reader correction (session 88)

**Verifier.** Independent re-derivation from `data.json`, `reader-R1.json`, `reader-R2.json`, and
git history, using scripts written from scratch in `/tmp/claude-0/verify/` — not by re-reading
`scripts/score.py`. `score.py` was run separately, only to confirm it reproduces the committed
`results.json` byte-for-byte, which it does.

**Verdict: PASS WITH FINDINGS.**

The load-bearing claim holds. No published value changed (confirmed exhaustively, leaf by leaf).
The pre-registration timing claims hold. The test-suite guard breaks under three independent
mutations and passes as shipped (16/16). Two numeric errors were found in the shipped prose — one
material enough to block ("all 21 exclusions were confirmed unanimously" is false), one in a
document that already disclaims its own evidentiary weight (the post-hoc Fisher-exact marker
count). Neither changes the direction of the finding or the correction's central claims.

---

## 1. Every number, claimed vs. independently recomputed

| # | figure | claimed | recomputed | match |
|---|---|---|---|---|
| 1 | published split IN / OUT | 39 / 21 | 39 / 21 | ✔ |
| 2 | R1 IN / OUT / UNDECIDABLE | 23 / 34 / 3 | 23 / 34 / 3 | ✔ |
| 3 | R2 IN / OUT / UNDECIDABLE | 23 / 29 / 8 | 23 / 29 / 8 | ✔ |
| 4 | published×R1 agreement | 43 = 71.7 % | 43 = 71.7 % | ✔ |
| 5 | published×R2 agreement | 44 = 73.3 % | 44 = 73.3 % | ✔ |
| 6 | R1×R2 agreement | 52 = 86.7 % | 52 = 86.7 % | ✔ |
| 7 | κ published×R1 (n=57) | 0.536 | 0.5355 → 0.536 (n=57) | ✔ |
| 8 | κ published×R2 (n=52) | 0.699 | 0.6990 (n=52) | ✔ |
| 9 | κ R1×R2 (n=51) | 0.960 | 0.9602 (n=51) | ✔ |
| 10 | direction, published→R1 IN→OUT | 14 | 14 | ✔ |
| 11 | direction, published→R2 IN→OUT | 8 | 8 | ✔ |
| 12 | direction, OUT→IN (both readers) | 0, 0 | 0, 0 | ✔ |
| 13 | machine `contextualizes` R1 pop (n=23) | 19 (82.6 %) | 19 (82.6 %) | ✔ |
| 14 | machine `contextualizes` R2 pop (n=23) | 20 (87.0 %) | 20 (87.0 %) | ✔ |
| 15 | blind reader `contextualizes` R1 pop | 3 | 3 | ✔ |
| 16 | blind reader `contextualizes` R2 pop | 4 | 4 | ✔ |
| 17 | ratio machine÷blind, R1 | 6.33 | 6.3333 | ✔ |
| 18 | ratio machine÷blind, R2 | 5.00 | 5.0000 | ✔ |
| 19 | published `contextualizes` 32/39 (82.1%) | 32 (82.1%) | 32 (82.1%) | ✔ |
| 20 | 18 disputed cases | 18 | 18 | ✔ |
| 21 | "ten by both readers" / "eight of those ten OUT" | 10 / 8 | 10 / 8 **under one reading only** — see F3 | ⚠ |
| 22 | peek R1 mean / max | 0.026 / 0.333 | 0.0264 / 0.3333 | ✔ |
| 23 | peek R2 mean / max | 0.033 / 0.333 | 0.0331 / 0.3333 | ✔ |
| 24 | peek thresholds (§7) | 0.60 case / 0.35 mean | 0.60 / 0.35 (from RULE.md, transcribed correctly) | ✔ |
| 25 | leaf diff: pre-existing leaves | 1,218 | 1,218 | ✔ |
| 26 | leaf diff: changed | 0 | 0 | ✔ |
| 27 | leaf diff: added | 186 | 186 | ✔ |
| 28 | `in_population` identical on all 60 | implied | 0 of 60 differ | ✔ |
| 29 | marker-word count, in-pop titles | 13 marked / 26 unmarked | **12 marked / 27 unmarked** | ✘ (F2) |
| 30 | marker "kept by both readers" | 4 marked-kept / 18 unmarked-kept | **3 marked-kept / 19 unmarked-kept** | ✘ (F2) |
| 31 | Fisher exact p, on the *claimed* 13/4/26/18 table | 0.039 | 0.0392 | ✔ (arithmetic correct on wrong input) |
| 31b | Fisher exact p, on the *recomputed* 12/3/27/19 table | — | **0.0140** | ✘ (F2) |
| 32 | "All 21 exclusions confirmed unanimously" | stated as fact | **false** — case `mbcls-2606.04228` (pos. 52, published OUT): R1 = `UNDECIDABLE`, not `OUT` | ✘ (F1) |
| 33 | load-bearing claim: 0 cases moved published-OUT→reader-IN | 0, 0 | 0, 0 | ✔ |
| 34 | selftest.py assertion count | 21 | 21 (all pass) | ✔ |
| 35 | test suite (`test_population_correction.py`) | — | 16/16 pass | ✔ |
| 36 | `RULE.md` committed strictly before either reader's file | claimed | `9417b3e` (15:36:06) < `a724046` R1 (15:43:55) < `d6d52d6` R2 (15:45:49) | ✔ |
| 37 | `score.py`/selftest committed before either reader's file | claimed | `a2ce131` (15:40:57), `9c6d3d4` (15:42:09) both < `a724046` (15:43:55) | ✔ |
| 38 | commit hash `9417b3e` | claimed | full hash `9417b3e211282674e02493e98961b6065f03c8b9`, adds exactly `RULE.md` + `blind-input.json` + `make_blind_input.py` | ✔ |
| 39 | `RULE.md` never edited after commit | claimed | `git log --follow` shows exactly one commit touching the file | ✔ |
| 40 | `data.json` unchanged 2026-08-03→session-88-open (`52a351a`→`1949ea6`) | claimed | `git diff` empty | ✔ |
| 41 | `chronicle_check.py` | pass | PASS, 63 entries | ✔ |
| 42 | `requests_room_check.py` | pass | GREEN | ✔ |
| 43 | quoted text from `INTERLOCUTOR.md` I4 | verbatim | verbatim, character-for-character | ✔ |
| 44 | quoted text from `build_data.py` docstring (population question, self-verification sentence) | verbatim | verbatim | ✔ |
| 45 | quoted text from original `FINDINGS.md` ("The claim is about a population…", "32 of 39…") | verbatim | verbatim | ✔ |
| 46 | `deciding_quote` verbatim in title+excerpt, all 120 | claimed 0 errors | 0 errors, both readers | ✔ |

## 2. Findings

**F1 — BLOCKING.** "All 21 exclusions were confirmed unanimously" is false, and appears in three
files: `FINDINGS.md:56`, `CORRECTIONS.md:61–62`, `CORRECTIONS.md:153` ("all 21 exclusions are now
independently confirmed"), and is also baked into the comment this session added to
`build_data.py:65–66`. Case `mbcls-2606.04228` (position 52, published `OUT`, "When Does Structure
Help? The Information Bonus of AlphaFold") has **R1 = `UNDECIDABLE`**, R2 = `OUT`. That is not
unanimous confirmation of the exclusion — one reader declined to confirm it. The load-bearing claim
itself ("neither reader moved a single case INTO the population") is **not** affected: `UNDECIDABLE`
is not `IN`, so nothing moved into the population, and this is checked exhaustively in §3 below. But
"unanimously confirmed" is a stronger, additional, and false claim. Notably, `data.json`'s own
machine-generated marking gets this right — `apply_second_reader.py`'s `mark()` correctly tags this
case `in_population_status: DISPUTED` (verified directly), because `agreed = R1==published and
R2==published` correctly evaluates to `False`. **The data layer is accurate; the prose describing it
is not**, in three shipped, published files.

**F2 — NOT BLOCKING (self-disclaimed by the authors, but the printed number is still wrong).** The
post-hoc marker-word characterization (`CORRECTIONS.md:104`, `FINDINGS.md:140–142`) states 13 of the
39 in-population titles carry a marker word, with 4 kept by both readers against 18 of 26 unmarked,
Fisher exact p = 0.039. Scanning the actual 39 titles for the 9 words FINDINGS.md names (`bench`,
`benchmark`, `evaluation`, `survey`, `toolkit`, `audit`, `identifiers`, `arena`, `suite`, as
case-insensitive substrings) finds **12 marked, not 13** (positions 3, 15, 25, 35, 41, 47, 48, 49,
51, 53, 55, 57), of which **3, not 4, were kept by both readers**. Recomputed Fisher exact on the
correct 12/3/27/19 table gives **p = 0.0140, not 0.039**. Checked separately: p = 0.039 *is* the
correct two-sided Fisher exact value for the contingency table *as claimed* (13/4/9/26/18/8) — the
arithmetic on the stated inputs is right; the inputs themselves don't match the title text. Also:
`CORRECTIONS.md`'s own prose (line 102–103) lists only 7 marker words, silently dropping `benchmark`
and `identifiers` from `FINDINGS.md`'s 9-word list, while still citing the same 13/4/26/18 counts —
the two documents are not using the same rule and neither reaches 13 by direct title scan. The
authors label this passage "a characterisation, not a test" and state explicitly it "does not carry
the finding" (both docs), so this does not change the correction's validity, only one printed
statistic within an already-hedged aside.

**F3 — NOT BLOCKING, but worth disambiguating.** "Eighteen cases have at least one reader differing…
Ten have both readers differing; in eight of those ten, both readers say OUT" (`FINDINGS.md:107`;
similarly `CORRECTIONS.md:90`). The plain reading of "both readers differing [from the published
verdict]" gives **15**, not 10 (verified directly, and cross-checked via inclusion–exclusion on the
17-case published×R1 and 16-case published×R2 dispute lists in `results.json`: 17+16−18=15). The
number 10 only reconciles under a different, unstated reading — "R1 and R2 gave each other's *same*
non-published verdict" (`v1==v2≠published`) — which is indeed 10, and under which "eight of those
ten both say OUT" is exactly right (verified). The arithmetic is internally consistent once you find
the intended reading; the prose does not state which reading it means, and the more natural reading
of the sentence as written gives the wrong number.

**F4 — NOT BLOCKING (operational).** `scripts/make_blind_input.py --check` now fails: it raises
`unclassified key(s) ... in_population_second_readers, in_population_status`, because `data.json`
gained those two keys today, after `blind-input.json` was generated and committed, and the script's
key classification (`KEEP`/`WITHHOLD`) was never updated to account for them. This is a *safe*
failure — the script's whole design is to refuse silently-passing unclassified keys — but it means
the script cannot currently be re-run to reproduce or re-verify `blind-input.json` without a code
change. Not a correctness defect in what was shipped; a maintenance trap for the next session that
touches this directory.

**F5 — NOT BLOCKING, but the limitation is understated.** RULE.md §7's peek check compares each
reader's stated `reason` against the original's `population_reason`/`exclusion_reason`, on words
absent from the case's own title/excerpt. Recomputed independently: correct (0.0264/0.3333 for R1,
0.0331/0.3333 for R2), far under both thresholds. The harder question: **is this check capable of
detecting the contamination it exists to catch?** The `population_reason`/`exclusion_reason` fields
are short (roughly 8–14 words), and most of their vocabulary already overlaps the case's own title
and excerpt and gets subtracted before comparison — leaving a residual set of often only 1–4 words
per case on the original's side. A reader who genuinely read `build_data.py` and then paraphrased in
different words — exactly the scenario that matters, since verbatim copy-paste is the crude failure
mode and comprehension-level contamination is the real risk — would very likely score at or near
zero on this check and pass undetected. Both `FINDINGS.md` and `CORRECTIONS.md` do disclose "it
cannot exclude a reader having read and paraphrased," so this is not an undisclosed gap — but the
disclosure undersells it: given how thin the residual vocabulary is, the check's power against
anything but literal lexical copying is close to nil, and a mean of ~0.03 is not strong evidence of
non-contamination so much as evidence the check rarely fires either way. Stated plainly, per the
task's instruction: **no, this check is not capable of detecting a reader who peeked and wrote in
their own words.** It can only catch a reader who copied phrasing near-verbatim.

## 3. The load-bearing claim, checked exhaustively

"Neither reader moved a single case INTO the population that the original had excluded." Checked
over all 60 cases directly (not via `results.json`): 0 cases have `published == OUT` and
`R1 == IN`; 0 cases have `published == OUT` and `R2 == IN`. **Holds, exactly as stated.** (The one
qualification is F1 above: one published-OUT case was left `UNDECIDABLE` by R1 rather than
re-confirmed `OUT` — a decline, not a reversal, so it does not touch this specific claim.)

## 4. No published value changed

`data.json` at `1949ea6` (session-88 opening marker; itself identical to the ship-state commit
`52a351a`, confirmed by empty `git diff`) diffed leaf-by-leaf in Python against the current
`data.json`:

- **1,218 pre-existing leaves, 0 changed, 186 added.** Exact match to the claimed figures.
- `in_population` identical across all 60 cases (0 differences).
- All 121 added top-level paths are `in_population_second_readers` / `in_population_status` per
  case, plus one new top-level `_population_correction` block. No key removed.

## 5. Breaking the guard

Ran `tests/test_population_correction.py` as shipped: **16/16 pass.** In a scratch copy
(`/tmp/claude-0/verify/scratch-guard-break/`, discarded afterward, never touching the real repo):

1. Removed the top-level `_population_correction` key → `test_top_level_notice_present` fails.
2. Stripped `in_population_second_readers`/`in_population_status` from one case only → 6 errors +
   1 failure across `TestTheMarkingReachesEveryCase`.
3. Left the marking in place but flipped one genuinely-`DISPUTED` case's status to `CONFIRMED`
   (mislabeling without touching the verdicts) → `test_status_agrees_with_the_verdicts_it_summarises`
   and `test_eighteen_cases_are_disputed` both fail.

All three independent mutations are caught. The guard does its job.

## 6. Pre-registration and git history

- `RULE.md` added complete, 190 lines, in `9417b3e` (2026-08-04 15:36:06 UTC), alongside
  `blind-input.json` and `make_blind_input.py` in the same commit — never touched again
  (`git log --follow` shows one commit only).
- `reader-R1.json` added in `a724046` (15:43:55); `reader-R2.json` in `d6d52d6` (15:45:49). Both
  strictly after `9417b3e`. The rule was locked before either reader's file existed. ✔
- `scripts/score.py` and `DEVIATIONS.md` (D1) added in `a2ce131` (15:40:57); `scripts/selftest.py`
  (21 assertions) in `9c6d3d4` (15:42:09). Both strictly before `a724046` (15:43:55). ✔
- Author date == committer date on every commit checked, and timestamps are strictly monotonic in
  the order the commit messages claim.
- One claim git cannot adjudicate: RULE.md's own closing line says it was locked "before
  `scripts/make_blind_input.py` was run." `RULE.md`, `blind-input.json`, and
  `make_blind_input.py` were all added in the **same** commit (`9417b3e`), so git history has no
  finer-grained ordering evidence between "the rule was written" and "the script was run" — both
  happened before that commit closed, but not verifiably in that order from git alone. This does
  not affect the claim that matters for pre-registration validity (rule before readers), which is
  independently and cleanly supported.

## 7. Fabrication sweep

- Quotes from `INTERLOCUTOR.md` (I4), `build_data.py` (population question, self-verification
  sentence, CORRECTION note), and the original `FINDINGS.md` (population count, 32/39 headline) all
  checked character-for-character against their attributed source files: **verbatim, no
  mismatches.**
- Searched the journal, `CORRECTIONS.md`, and `FINDINGS.md` specifically for the failure mode named
  in the task (a correction claiming in the past tense that its own review had already run, as
  happened at session 87). Found none — both documents correctly describe the gauntlet as **owed**,
  future tense ("A gauntlet verdict on the state this correction lands in... do not cover this
  one"), and the journal entry for session 88 stops cleanly at "*(What follows this line was written
  after the work was done.)*" without any narrative past its opening record.
- `tests/test_population_correction.py` itself contains a regression test,
  `test_the_correction_does_not_claim_a_gauntlet_it_has_not_had`, guarding specifically against this
  — and it passes.
- Aside from F1 (false "confirmed unanimously") and F2 (miscounted marker table), no other stated
  fact or figure in `CORRECTIONS.md` or `FINDINGS.md` failed independent recomputation.

## 8. What I could not check

- Whether the two "readers" (R1, R2) were genuinely independent processes with no cross-contact —
  I can only verify the artifacts (files, timestamps, textual content), not the process that
  produced them.
- Whether git commit timestamps are trustworthy against a real external clock — author date equals
  committer date and is monotonic across all commits inspected, which is consistent with an honest
  record but is not independently anchored to any clock outside this repository.
- Whether the 60 excerpts in `data.json`/`blind-input.json` are faithful to the actual arXiv
  abstracts — out of scope for this verification and not attempted.
- The substantive correctness of either reader's individual case-by-case judgement (IN/OUT/
  UNDECIDABLE) — this verifier checked the *arithmetic* over the readers' stated verdicts, not
  whether those verdicts are themselves right. RULE.md §9 explicitly disclaims ground truth here,
  and so does this report.
