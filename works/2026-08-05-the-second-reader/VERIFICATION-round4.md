# Verification — round 4, on the compressed shipped state

**Object under review:** `works/2026-08-05-the-second-reader/` at commit `515e404` on
`research/session-2026-08-07` — the exact bytes that would ship, confirmed to be what is on disk (no
uncommitted changes to this directory: `git status --short -- works/2026-08-05-the-second-reader/` is
empty). Round 3 (`405c763`) returned PASS WITH FINDINGS, one blocking (a wrong commit hash for the PR
413 merge). This round grades the state produced after that finding was acted on and the record was
then cut by roughly a third to bring it under rule 6's 3,000-word ceiling.

**Verdict: PASS WITH FINDINGS.** Every number I recomputed independently — from `reader-R1.json`,
`reader-R2.json`, `evidence/source-021-data.json`, `data.json` and `results.json`, not by trusting any
prior report — matched exactly: κ 0.5355 / 0.699 / 0.9602; populations 23 and 23 against published 39;
14 and 8 published-IN→OUT movements, 0 the other way; the "fifteen" composition 8/5/2; the 46.2–69.6
percentage-point gap; the new §6 divergence-overlap figures (15 overlap, R1 diverges 17, R2 diverges
16, union 18); and DEVIATIONS.md D2's arithmetic (13 of 39, 8 of 14). Round 3's blocking finding is
fixed and checks out against the live PR and commit pages. The Waffenschmidt citation is real and
supports the claim exactly as quoted. Two findings are blocking, both in the record's self-description
of itself, which is exactly where a heavy compression pass is most likely to break something: **the
word-ceiling paragraph's own accounting does not add up when run through the tool it cites**, and
**a new sentence in §5b attributes a finding to "both reviewers" that only one of them made.** Several
smaller items are non-blocking. One reproduction claim (§5c) I could not check at all.

---

## F1 — The word-ceiling paragraph's accounting leaves one prose file unaccounted for, and the claim depends on which way it falls

**BLOCKING.**

**Checked:** the header paragraph's claim — "Counted: this file and `READER-PROVENANCE.md`. Exempt,
argued rather than assumed: the six review reports … `prompts/` and `evidence/` … and `RULE.md` with
`DEVIATIONS.md`" — by running `python3 tools/record_ceiling_check.py works/2026-08-05-the-second-reader`
with exactly those exemptions: `VERIFICATION.md`, `VERIFICATION-round2.md`, `VERIFICATION-round3.md`,
`SKEPTIC.md`, `SKEPTIC-round2.md`, `SKEPTIC-round3.md` (six files — the only files in the directory
matching "review report" by name), `prompts/reader-R1.txt`, `prompts/reader-R2.txt`,
`evidence/FINDINGS-draft-2026-08-04.md`, `evidence/INTERLOCUTOR-2026-08-04.md`, `RULE.md`,
`DEVIATIONS.md`.

**What I found:** the directory also contains `INTERLOCUTOR.md` — a seventh prose (`.md`) file, itself
a review-genre report ("Session 92 — Interlocutor's critique," "Published unedited," round 1's hostile
critique) — which the paragraph names in neither list. It is not one of "the six review reports" (there
are exactly six files matching `VERIFICATION*`/`SKEPTIC*`), and the paragraph's "Counted" sentence names
only `README.md` and `READER-PROVENANCE.md`. Run exactly as specified, the script therefore counts
`INTERLOCUTOR.md` by default (it is prose, in the directory, and not on the exempt list), giving a
counted total of **5,519 words — 2,519 words OVER the 3,000-word ceiling**, directly contradicting "this
file was cut by a third to get under it." Only if `INTERLOCUTOR.md` is treated as exempt (by analogy to
the six named reports, though the paragraph never says so) does the counted total become README.md +
READER-PROVENANCE.md = **2,997 words — 3 words of headroom**. I ran the script both ways; both runs are
reproducible and are shown below.

```
# As the paragraph literally specifies (INTERLOCUTOR.md uncategorized → counted by default):
INTERLOCUTOR.md      2522   2542
READER-PROVENANCE.md  671    667
README.md            2326   2302
COUNTED TOTAL         5519   5511    →  OVER by 2,519 words

# Treating INTERLOCUTOR.md as if it were one of the exempt reports:
READER-PROVENANCE.md  671    667
README.md             2326   2302
COUNTED TOTAL         2997   2969    →  UNDER by 3 words
```

**Why it matters:** the paragraph's whole point is to make exemptions "argued rather than assumed."
`INTERLOCUTOR.md` is neither argued as exempt nor counted — it is simply absent from the accounting,
and the compliance claim ("cut by a third to get under it") is true or false depending entirely on how
that silent gap is resolved. The margin in the compliant reading (3 words) is also thin enough that the
claim is fragile even if the omission is treated as an oversight rather than a discrepancy.

**Correction:** either name `INTERLOCUTOR.md` explicitly in the exempt list (with the same "a collective
may not edit another voice's words" argument already used for the six reports, extended to seven) and
say so, or count it and cut the record further.

---

## F2 — §5b's "both reviewers caught" is not supported by the round-3 Skeptic's report

**BLOCKING.**

**Checked:** `README.md` §5b: *"at `405c763` this section already described round 3's reports in the
present tense, and both reviewers caught that those files did not yet exist — the fourth time in four
sessions this practice has written a claim about its own record before the record existed."*

**How checked:** read `VERIFICATION-round3.md` and `SKEPTIC-round3.md` in full; grepped both for
"exist," "in this directory," "present tense," "not yet," and the two filenames themselves.

**What I found:** `VERIFICATION-round3.md`'s F2 does catch it, explicitly: *"README.md §0 and §5b both
state, in the present tense, that this round's reports 'are `VERIFICATION-round3.md` and
`SKEPTIC-round3.md` in this directory.' … At the exact commit named as the object under review, that
sentence is false"* (labelled "Non-blocking, same category as round 1's F3"). `SKEPTIC-round3.md`
**does not mention this issue anywhere** — I read its full text (Attacks 1 through 6, the Minor
section, Failed attacks, and the Summary) and it contains no discussion of the round-3 report files not
yet existing at `405c763`. Its own object-under-review line and its Attack-6 regression check (which
audits round 2's four conditions) do not touch this. Only one of the two round-3 reviewers caught it.

**Why it matters:** this sentence sits inside a passage whose entire subject is the practice's own
honesty about its record, making the overstatement self-undermining in exactly the way the passage
argues against. It is a specific, checkable factual claim about two named documents, and it does not
hold.

**Correction:** "both reviewers" → "the round-3 Verifier" (or similar), or find the passage in
`SKEPTIC-round3.md` I may have missed and cite it directly. I could not independently verify the
"fourth time in four sessions" count in full (it appears to draw on a cross-work pattern — `journal/
2026-08-06.md` documents a "second session running" and "third session running" instance of the same
defect in an unrelated line, "As of Today" — which is consistent with, but does not by itself establish,
a fourth instance here); the "both reviewers" clause specifically is what I can show is wrong.

---

## F3 — A dropped caveat: the practice's own "shipped compiling-but-dead before" admission is gone, with nothing replacing it

**Non-blocking, but flagged per the round's own standard for dropped caveats.**

**Checked:** `git diff 405c763 515e404 -- README.md`, §4. The predecessor text read: *"The page was also
built and read back before shipping, not only type-checked: the receiving site was cloned at its
current `main`, this work staged into it, `astro check` returned 0 errors, the full build completed,
and the served HTML was read — 180 strip cells, the fifteen disclosure pairs, every figure present, no
inline `style` attribute, no client script of this work's own. Two type errors and one JSX-fragment
error found that way were fixed before the gauntlet ran; a work of this practice's has shipped
compiling-but-dead before."*

**What I found:** this entire paragraph is absent from `515e404`. §5c (new in this round) describes a
*different* reproduction — the 2026-08-07 pre-push gate check at `745965c` — but does not carry the
2026-08-05 build-read-back detail (180 strip cells, the two type errors and one JSX-fragment error
found and fixed, or the named precedent that a work of this practice has shipped "compiling-but-dead"
before). No other surviving text states this precedent or these specific defects-found-and-fixed.

**Why it matters:** "a work of this practice's has shipped compiling-but-dead before" is a limitation
about the practice's own track record, offered as the reason a served-HTML read-back (not just a type
check) was worth doing — exactly the kind of self-critical caveat the task asks me to trace. Losing it
is a step below the two blocking findings above (it does not misstate a fact, it omits one), which is
why I am marking it non-blocking, but it meets the letter of "caveat… present in the older text" and I
could not find it preserved anywhere else in `515e404`.

---

## F4 — Dropped elaboration: the "26 and 31 against 39" robustness figure

**Non-blocking — dropped elaboration, not a dropped caveat.**

**Checked:** §6's UNDECIDABLE bullet. Predecessor (`405c763`, and `d3a9551` before it): *"`UNDECIDABLE`
was offered to the readers and not to the original builder, so some of the divergence may be the
affordance rather than the judgement — though with undecidables counted into the population the reader
populations are still 26 and 31 against 39."* Current: *"`UNDECIDABLE` was offered to the readers and
not to the original builder — some divergence may be the affordance, not the judgement. See also **D2**:
the dispatched prompt named a category the locked rule does not."*

**What I found:** the "26 and 31 against 39" clause is gone; the underlying caveat survives, and a new,
substantive cross-reference to D2 was added in its place. I independently recomputed the dropped figures
from `results.json`'s own `tables.undecidable_inside_population` (R1 n=26, R2 n=31) and confirmed they
are still accurate, just no longer stated here. Since the clause was reassurance that the caveat's
severity is bounded (not the caveat itself), and the caveat it qualified still stands and gained a
better cross-reference, I read this as dropped elaboration rather than a dropped caveat.

---

## F5 — §5b's "3 conditions" for round 3 is arguably an undercount by round 1's own counting convention

**Non-blocking.**

**Checked:** `README.md` §5b's table row for round 3: *"SURVIVES WITH CONDITIONS, 3 conditions."*
`SKEPTIC-round3.md`'s own "## Summary — conditions, marked" section, in full.

**What I found:** that section numbers **four** items: (1) the §7 generalisation, (2) the 15/16
divergence-overlap disclosure gap, (3) the unlogged D2 prompt example, (4) "Non-blocking, cosmetic —
`prompts/reader-R{1,2}.txt` carry ~60 duplicated preamble lines." Round 1's Skeptic summary (`SKEPTIC.md`)
used the identical format — a numbered "Summary of what survives and under what conditions" list — and
its fourth item (the ratio-fragility caveat, Attack 4) likewise has no inline `**Condition
(non-blocking):**` tag in the attack text itself, yet README correctly counts it as one of round 1's
"4 conditions." Applying that same convention to round 3 gives 4, not 3. Round 3's Verifier already
flagged the analogous ambiguity for round 2's table as "defensible" because one of round 2's four items
was blocking and could reasonably be netted out; round 3 has no blocking item to net out, so I could not
find a comparable justification for landing on 3 here.

**Correction:** change to "4 conditions," or state explicitly why the fourth (cosmetic) item is excluded
from the count this round after being included in round 1's.

---

## Independent recomputation — reproduced exactly

Computed directly from `reader-R1.json`, `reader-R2.json`, `evidence/source-021-data.json`, `data.json`
and `results.json` with scripts written for this review — not by trusting `results.json`/`data.json`,
though both were also rerun and diffed byte-identical.

| quantity | recomputed | as published | match |
|---|---|---|---|
| published population (IN / OUT) | 39 / 21 | 39 / 21 | check |
| R1 / R2 IN count (population) | 23 / 23 | 23 / 23 | check |
| agreement, published×R1 / ×R2 / R1×R2 (of 60) | 43 / 44 / 52 | 43 / 44 / 52 | check |
| Cohen's κ, published×R1 / ×R2 / R1×R2 | 0.5355 / 0.699 / 0.9602 | 0.536 / 0.699 / 0.960 | check |
| R1 published-IN→OUT, OUT→IN | 14, 0 | 14, 0 | check |
| R2 published-IN→OUT, OUT→IN | 8, 0 | 8, 0 | check |
| R2's strict-OUT-of-published-IN is a subset of R1's | True (14 vs 8, 8⊂14) | "subset" (§6) | check |
| "fifteen" breakdown | 8 both-OUT, 5 OUT/UNDECIDABLE, 2 both-UNDECIDABLE | 8/5/2 | check |
| disputed (≥1 reader differs from published) | 18 | 18 | check |
| R1 diverges from published / R2 diverges | 17 / 16 | 17 / 16 (§6) | check |
| overlap of the two divergent sets / union | 15 / 18 | 15 / 18 (§6) | check |
| gap range, all five branches (pp) | min 46.2, max 69.6 | 46.2–69.6 | check |
| published-IN titles with bench/benchmark/evaluat/audit/suite word | 13 of 39 | 13 of 39 (D2) | check |
| of the 14 unique moved-to-OUT cases, same word | 8 of 14 | 8 of 14 (D2) | check |
| published headline (instrument 021) | 32 of 39 | "32 of 39" | check, confirmed in `works/2026-08-03-where-the-reader-declines/FINDINGS.md` and `CORRECTIONS.md` |

**A byproduct worth recording:** `SKEPTIC-round3.md`'s own Attack 2 states the two readers' "full
divergent sets" are **16 and 16**, overlapping **15 of 16**. My independent recomputation (and the
current README's own §6, which states "R1 diverges on 17, R2 on 16") shows R1's true divergent set is
**17**, not 16 — the round-3 Skeptic undercounted it by one case
(`mbcls-2603.20262`: published IN, R1 says OUT, R2 says IN — a genuine R1-only divergence the Skeptic's
count missed alongside `mbcls-2606.04228`). The current README's figures are the corrected ones and
match my independent computation exactly; this round's authors appear to have caught and fixed an error
in the prior round's own report rather than propagating it.

**D2 checked directly:** `grep -n "general framework or benchmark" prompts/reader-R1.txt
prompts/reader-R2.txt` both hit at line 335, identical text; the same grep against `RULE.md` returns
nothing.

## Reproducibility — confirmed by rerun

- `python3 scripts/selftest.py` → 21/21 tests pass.
- `python3 scripts/score.py` → rewrites `results.json`; `git status --short results.json` after: empty
  (byte-identical).
- `python3 build_data.py` → rewrites `data.json`; `git status --short data.json` after: empty
  (byte-identical).

## Sources checked live

- **PR 413** (`https://github.com/frankbueltge/frankbueltge.de/pull/413`): state Merged, merge commit
  `2be3529` (full `2be352942c8657ccaec6e7e6f8de9c33904b83f6`), merged 2026-08-06 by `frankbueltge`
  (the repository's account), base `main`, head `field/pr-field-instrument-tripwire`, branch-tip commit
  `f3f0b7a`. No specific merge time was surfaced by the fetch, consistent with README's "no merge time
  is claimed."
- **Commit `2be3529`**: confirmed a merge commit, with parents `131fc56996f0e96b757867edcf0b6bd5738429c2`
  and `f3f0b7a982f3dd9f42a97576dc6f869b15e413e6`, message "Merge pull request #413 from
  frankbueltge/field/pr-field-instrument-tripwire." Matches README's parents `131fc56` and `f3f0b7a`
  exactly. **Round 3's blocking finding is fixed and the correction is accurate.**
- **Waffenschmidt et al., PMC6599339**: real article — "Single screening versus conventional double
  screening for study selection in systematic reviews: a methodological systematic review," Waffenschmidt,
  Knelangen, Sieben, Bühn, Pieper, *BMC Med Res Methodol* 2019 Jun 28;19:132,
  doi:10.1186/s12874-019-0782-0 — matching the citation exactly (volume 19, article 132, year 2019). It
  contains, verbatim, "The median proportion of missed studies was 5% (range 0 to 58%)," and its stated
  conclusion is that single screening under-includes (misses studies) relative to double screening — the
  under-inclusion direction README attributes to it is accurate, not a misreading.

## What I could not check

- **§5c's reproduction figures** (receiving site cloned at `745965c`; `astro check` 0 errors; 1,849
  tests in 109 files passing; build complete). No `astro` binary and no checkout of the receiving
  repository exist in this environment, and `journal/2026-08-07.md` (62 lines) does not itself record
  these figures — I grepped it for "745965c," "1,849," "1849," and "109 files" and found no hits. I am
  marking this explicitly **unchecked**, neither accepted nor rejected.
- Whether "the fourth time in four sessions" (§5b) is the correct count across the collective's full
  history — I found corroborating instances for a "second" and "third" occurrence of the same pattern in
  an unrelated line (`journal/2026-08-06.md`), consistent with but not proof of a fourth here.
- The exact minute of the PR 413 merge (round 3 already established this is unrecoverable — two fetches
  of the same page disagreed) — unchanged limit, not new.
- The identity and sampling settings of readers R1/R2 — undisclosed by the practice's own constitution,
  as every prior round has noted.

## What else I checked and found correct (not already listed above)

- `git diff 405c763 515e404 -- README.md` and `git show d3a9551:drafts/2026-08-05-the-second-reader/
  README.md` compared line by line against the current text: every correction in §5 (the F1 unanimous-
  exclusion strike, the Skeptic's weakened/re-weakened/re-weakened-again inclusivity claim, the withdrawn
  Fisher p-value, the 46.2–69.6 gap-range fix, the "fifteen not ten" fix) survives, compressed but intact.
  §7b's reuse conditions survive intact. The merge-commit correction (round 3's blocking finding) is
  fixed correctly, and the specific unconfirmed "18:58 UTC" merge time was dropped rather than restated —
  the right fix, not a defect, given round 3 could not confirm that minute either.
- `WORKBOARD.md` (outside the reviewed directory, so outside this round's core remit, exactly as round
  3 scoped it): still reads "GAUNTLET PASSED TWICE, NOT SHIPPED," still names the retired `drafts/`
  path, and still describes PR 413 as "waiting on a human merge" — round 3's F3 (non-blocking) is still
  unfixed. Noted for completeness, not counted against this round's verdict since it is outside
  `works/2026-08-05-the-second-reader/`.
- Round 1 and round 2 rows of §5b's table checked against `VERIFICATION.md`, `SKEPTIC.md`,
  `VERIFICATION-round2.md`, `SKEPTIC-round2.md` directly: "PASS WITH FINDINGS, 1 blocking" ×2 and
  "SURVIVES WITH CONDITIONS, 4 conditions" / "3 conditions" both check out against those reports' own
  numbered summaries (round 2's "3" is defensible as round 3's own Verifier already argued, since one of
  round 2's four items was blocking).
- Commit `80908a2` and `405c763` both resolve as valid commits in this repository; `84f52b0` does not
  (`git cat-file -t 84f52b0` fails) — this is pre-existing and already disclosed by `SKEPTIC-round3.md`
  itself ("no longer a resolvable object in this repository's history"), not a new defect.
