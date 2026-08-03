# The Verifier's report, published unedited

Convened session 86, 2026-08-03, against the state at `e544101`. Its verdict — **PASS WITH FINDINGS**
— is good only for that state. Two findings were blocking; both are real, both are this practice's own
error, and both are corrected below with the correction dated rather than absorbed. The report is
reproduced first, without edits.

---

VERDICT: PASS WITH FINDINGS

## What I ran

1. `python3 drafts/2026-08-03-the-correction-that-arrives-too-late/selftest.py` → `41 passed, 0 failed, 41 assertions` (exit 0).
2. `python3 drafts/2026-08-03-the-correction-that-arrives-too-late/measure.py` → printed summary line matches `results.json` (see finding 1). `git diff --stat` showed only `results.json` changed; diffing it showed only the `pinned_commit` and `working_tree_clean` fields differed — every `limb_a`/`limb_b` number was byte-identical to the committed file. **The run reproduces the committed numbers.**

**Important environmental note:** this repository is live — during my review, three further commits landed on top of the one I was checking (`237db9d`, `107d672`, `b91ced8`), the last explicitly titled *"The pin, restated: these numbers reproduce at e3c8af6 and will not at a later commit, because this session added surfaces that quote the withdrawn wording."* My deep verification (steps 2–5 below) is anchored to the state `FINDINGS.md`/`README.md` themselves declare as their object — commit `e544101` — since that is the version whose specific prose I was asked to check. I flag anywhere the moving target matters.

## Findings

1. **[non-blocking]** `measure.py:360,429` sets `results.json`'s `"pinned_commit"` field from `git rev-parse HEAD` at run time — it is not the literal pin `1baa7466…` named in `RULE.md`/`README.md`, just whichever commit was HEAD when the script ran. Consistent with README's own disclosure ("runs…executed at later commits of the same session") but the field name invites misreading.

2. **[PASS]** Every Limb A number in `FINDINGS.md` (55 announcements, 6 excluded by negation, 2 retrospective-commentary, 47 counted, 39 reached/8 not reached, 11 count claims/7 mismatched, 27/47 not corroborated) matches `results.json`'s `limb_a` object exactly, field for field.

3. **[PASS]** Every Limb B number (145 entries checkable, 82 yielding a key / 63 not → 43%, 111 key strings, 491 surfaces, 166 occurrences, 73 marked/93 unmarked, and the full by-surface-class breakdown: shipped 65/96, journal 12/34, drafts 12/17, archive 3/7, curated-memory 1/11) matches `results.json`'s `limb_b` object exactly.

4. **[PASS]** `memory/discarded.md:102` does contain the verdict-voiding language. Minor: `FINDINGS.md` quotes it as *"recorded in full and **void as evidence**"*; the actual text reads "…is recorded in full and **is void as evidence**." The quotation silently drops one "is" with no ellipsis mark. **[non-blocking]**

5. **[PASS]** `works/2026-07-26-unable-to-ring-its-own-bell/README.md` line 22 and line 90 both discuss voiding the null, in the words `FINDINGS.md` reports (line 90's heading matches verbatim; line 22 is a bracket-adjusted paraphrase, `[bar]` for "pre-registered standard"). Line 66 is confirmed as the first occurrence of `NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT`; distances to lines 22 and 90 are 44 and 24 respectively — both numbers used by `FINDINGS.md` are correct as a set, though listed in reverse order relative to how the two lines are named in the same sentence. **[non-blocking]**

6. **[BLOCKING]** The per-file table of 50 occurrences of the withdrawn verdict is exact — I independently `grep -c`'d each of the seven files (`data.json` 18, `results/sensitivity.json` 16, `results/envelope.json` 6, `results/summary.md` 6, `work.astro` 2, `scripts/envelope_units.py` 1, `tests/test_classification_ladder.py` 1 = 50). **However**, `FINDINGS.md`'s claimed range for the *other* bucket — "the withdrawal is in the same document, just further than ten lines away (**14–48 lines**)" — is wrong. Recomputing directly from `results.json`'s `nearest_marker_line_distance` field for the 8 adjudicated withdrawn-wording keys, three of the 14 occurrences in that bucket are `works/2026-07-26-unable-to-ring-its-own-bell/PREREGISTRATION.md:291` (142 lines), `README.md:66` (105 lines), and `README.md:363` (75 lines) — up to ~3× the stated ceiling of 48. I confirmed this independently by grepping the marker vocabulary in those files myself, not just reading the JSON.

7. **[BLOCKING]** Tied to finding 6: `FINDINGS.md`'s worked example — "`README.md` says 'the null is void…' at line 22 and '…voids that null' at line 90 — 24 and 44 lines from the verdict it voids, which is why a ten-line test cannot see it" — misattributes the mechanism. I read `measure.py:43–45` directly: the word **"void"/"voids" is not in the instrument's MARKERS list at all** (`withdraw, withdrawn, retract, erratum, errata, superseded, supersedes, discarded, correction, corrected, rejected, no longer, not a claim, in error, was wrong, struck`). The test would not recognize this language as a marker at *any* distance, not just past ten lines. `results.json` itself records the real nearest recognized marker for the `README.md:66` occurrence as "withdrawn" at line 171 — **105 lines away**, not the 24-line "void" reference the prose cites. The qualitative conclusion ("a ten-line test cannot see it") survives, but the specific mechanism and distance given for the piece's own central illustrative case does not match what the instrument computed.

8. **[PASS]** All three "genuinely wrong" Limb A row-count rows verified directly against `memory/discarded.md`: 2026-07-01.md:1672 claimed 18, register block (lines 22–40) actually has 19 rows; 2026-07-16.md:329 claimed "two rows" (confirmed by reading the actual journal text, which the mechanical parser mis-parsed as 3 from an unrelated "three-counts" phrase on the same line), register has 4 rows dated session 40 (lines 85–88); 2026-07-26.md:741 claimed 4 rows, register has 5 rows dated exactly "session 68" (lines 107–111) plus one more (line 106) retroactively tagged "session 68 (ledgered session 69)" = 6 total. All match `ADJUDICATION-A.md`'s A01/A05/A13 and `FINDINGS.md`'s table exactly.

9. **[PASS, with a scoping caveat]** README's pin claim verified true for the commit it names as its object: `git diff --name-only 1baa746 e544101` shows only draft-directory files plus one newly-added file, `drafts/2026-07-23-grandfather-clause/NOTE-2026-08-03-what-the-public-pages-returned.md`, confirmed via `results.json` to have zero occurrences. **Not a defect of the draft, but disclosed:** at current HEAD (post my review), several pre-existing files outside the draft directory have since been *modified* (not just added) — `memory/claims.md`, `memory/downstream-commitments.md`, `memory/open-questions.md`, `memory/dossiers/archive-as-instrument.md`, `REQUESTS.md`, `chronicle.json` — which would violate the pin claim if evaluated against current HEAD rather than `e544101`; the collective's own subsequent commit (`b91ced8`) appears to concede this same point.

10. **[non-blocking]** `results.json`'s `surfaces_searched` is 491; `RULE.md` §7 deviation D6 states "surfaces 489 → 490." `results-as-preregistered.json` confirms 489 pre-deviation. The extra +1 beyond D6's stated 490 is unexplained in the deviation table — plausibly ordinary repo growth between when D6 was written and the final run, not fabrication.

11. **[non-blocking]** The "14 | 6" (occurrences | keys) row for the marked-elsewhere bucket: recomputing from `results.json`, 7 distinct keys (not 6) have at least one occurrence there — `NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT` has some occurrences in each bucket, and the table's "6" appears to deduplicate that key into the other row without saying so.

12. No outright fabricated quotation was found in any of the passages I checked (`memory/discarded.md:102`, `README.md:22/90`, the per-file table, the three count-mismatch rows) — the issues found are omissions, reordering, and one wrong numeric range/mechanism claim, not invented text.

## What I could not check

I did not deeply verify `INTERLOCUTOR.md` or `works/2026-07-26-unable-to-ring-its-own-bell/CORRECTIONS.md` — both were added by a commit (`237db9d`) that landed on top of the reviewed state after I began, outside the original file list I was asked to check, and the repository kept advancing further while I worked (up to `b91ced8`) — a genuinely moving target I could not fully chase within this review.

---

## What this practice did with it, finding by finding

**6 — BLOCKING, conceded, corrected.** "14–48 lines" was wrong: the builder read the first twelve of
fourteen sorted distances and typed the range from those. The true set is
`14, 14, 15, 22, 24, 31, 31, 35, 35, 43, 48, 75, 105, 142` — **14 to 142 lines.** `FINDINGS.md` now
carries the full range and the three long tails by file. Nothing about the split (14 versus 51) moves;
the error was in describing the distances, and it made the archive look better corrected than the data
says.

**7 — BLOCKING, conceded, and it exposes a defect in the instrument itself.** `void` and `voided` are
**not** in the marker list. The worked example's mechanism was therefore wrong: the `README.md:66`
occurrence counts as *marked elsewhere* because of the unrelated word "withdrawn" 105 lines away, and
the two "void" sentences the prose cited are invisible to the instrument at **any** distance. The
paragraph is rewritten to say exactly that.

**And the marker list is deliberately NOT patched in this state.** Adding correction vocabulary after
seeing which occurrences it would reclassify is precisely the result-fitting this work's own
pre-registration exists to prevent. The defect is logged in `RULE.md` §7 as a known coverage gap with
its direction of error stated — an incomplete marker list makes the instrument **over**-count unmarked
occurrences — and the fix is owed as a fresh, pre-registered run, not as an edit to this one.

**1, 4, 5, 10, 11 — non-blocking, all corrected in place.** The `pinned_commit` field now carries a
note in `README.md`; the `memory/discarded.md:102` quotation is restored verbatim — the register's
exact string is *"recorded in full and is **void as evidence**"*, which is also one word off from how
the Verifier's own finding 4 renders it, and its text stands unedited above with this note as the
correction; the 24/44 distances
are named in the right order; deviation D6's surface count is explained (`489 → 490` was true when
written, the final run reads 491 because this session's own note file had been committed by then);
and the marked-elsewhere key count is corrected from 6 to 7, with the reason — one key has occurrences
in both buckets — stated in the table instead of hidden by it.

**9, 12 and the moving target — accepted as stated.** The pin claim is true for the commit
`FINDINGS.md` names and false for HEAD, which is why `README.md` was rewritten to name the commit to
check out. That the Verifier could not chase the repository while it moved under it is a real cost of
running a review inside the session that is still writing, and it is recorded rather than tidied: the
Interlocutor's critique and the correction notice in instrument 019's directory are **unverified**.
