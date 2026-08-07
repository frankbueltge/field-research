# VERIFICATION — round 5, on the shipped state

**Object under review:** `works/2026-08-05-the-second-reader/` at commit `691a9de` — the exact bytes
that ship. Round 4 graded `515e404` and returned PASS WITH FINDINGS, two blocking findings (both
executed since); round 4's Skeptic returned SURVIVES WITH CONDITIONS. This round checks the two
blocking fixes, the new correlated-reader disclosure moved onto the page itself, the restored
caveats, `DEVIATIONS.md` D2's new paragraph, the core numbers from raw data rather than any prior
report, and the work's self-description against `git log` and, where reachable, the receiving
repository's own history.

**Verdict: PASS WITH FINDINGS. One blocking finding.**

---

## F1 — The rewritten word-ceiling paragraph is still not runnable exactly as it names its
exemptions, in a different place than round 4 found it

**BLOCKING.**

**Checked:** ran `tools/record_ceiling_check.py works/2026-08-05-the-second-reader/` with exactly the
exemptions the header paragraph now names: `VERIFICATION.md`, `VERIFICATION-round2.md`,
`VERIFICATION-round3.md`, `VERIFICATION-round4.md`, `SKEPTIC.md`, `SKEPTIC-round2.md`,
`SKEPTIC-round3.md`, `SKEPTIC-round4.md`, `INTERLOCUTOR.md`, `prompts/`, `evidence/`, `RULE.md`,
`DEVIATIONS.md` — passed one `--exempt` per name, nothing added or expanded.

**What I found.** The script's `--exempt` matching is an exact match against each file's path
relative to the directory root (`row[0] in exempt`, where `row[0]` is
`str(path.relative_to(root))`) — its own usage text only ever shows a filename
(`--exempt PREREGISTRATION.md`). `prompts/` and `evidence/` never equal the relative path of any
actual file (`prompts/reader-R1.txt`, `prompts/reader-R2.txt`,
`evidence/FINDINGS-draft-2026-08-04.md`, `evidence/INTERLOCUTOR-2026-08-04.md`), so the run prints:

```
WARNING: --exempt evidence/ matched no file in works/2026-08-05-the-second-reader
WARNING: --exempt prompts/ matched no file in works/2026-08-05-the-second-reader
```

and all four of those files stay in the counted pool. Run exactly as the paragraph specifies, the
counted total is **16,753 words — 13,753 words OVER the 3,000-word ceiling** (`.txt` is a prose
suffix the script counts, and the two `prompts/reader-R{1,2}.txt` files alone are 4,578 words each).
This directly contradicts "this file was cut by a third to get under it."

Only if `prompts/` and `evidence/` are read as shorthand for their four member files, and those
literal filenames are substituted for the two directory names, does the script report what the
paragraph implies: **2,996 words — 4 words of headroom** (`READER-PROVENANCE.md` 671 +
`README.md` 2,325). Both runs are reproducible; I ran both and show the exact commands and output
below.

```
$ python3 tools/record_ceiling_check.py works/2026-08-05-the-second-reader/ \
    --exempt VERIFICATION.md --exempt VERIFICATION-round2.md --exempt VERIFICATION-round3.md \
    --exempt VERIFICATION-round4.md --exempt SKEPTIC.md --exempt SKEPTIC-round2.md \
    --exempt SKEPTIC-round3.md --exempt SKEPTIC-round4.md --exempt INTERLOCUTOR.md \
    --exempt "prompts/" --exempt "evidence/" --exempt RULE.md --exempt DEVIATIONS.md
...
  COUNTED TOTAL                        16753     16811
...
  WARNING: --exempt evidence/ matched no file in works/2026-08-05-the-second-reader
  WARNING: --exempt prompts/ matched no file in works/2026-08-05-the-second-reader
  OVER    the counted record is 13753 words over the ceiling
[exit 1]

$ python3 tools/record_ceiling_check.py works/2026-08-05-the-second-reader/ \
    --exempt VERIFICATION.md --exempt VERIFICATION-round2.md --exempt VERIFICATION-round3.md \
    --exempt VERIFICATION-round4.md --exempt SKEPTIC.md --exempt SKEPTIC-round2.md \
    --exempt SKEPTIC-round3.md --exempt SKEPTIC-round4.md --exempt INTERLOCUTOR.md \
    --exempt "prompts/reader-R1.txt" --exempt "prompts/reader-R2.txt" \
    --exempt "evidence/FINDINGS-draft-2026-08-04.md" --exempt "evidence/INTERLOCUTOR-2026-08-04.md" \
    --exempt RULE.md --exempt DEVIATIONS.md
...
  COUNTED TOTAL                         2996      2972
...
  UNDER   4 words of headroom on the counted record
[exit 0]
```

**Why this is the same defect as round 4's F1, relocated, not a new kind of problem.** Round 4's
blocking F1 found `INTERLOCUTOR.md` unaccounted for in the prior paragraph's exemption list — a name
the paragraph owed and did not give. That is fixed here: `INTERLOCUTOR.md` is now named explicitly.
But the paragraph still contains two entries, `prompts/` and `evidence/`, that are not names the
script's exemption mechanism can consume, for the same underlying reason round 4 objected to: the
claim "counted now by `tools/record_ceiling_check.py`" is not true of the paragraph's own exemption
list when that list is handed to the script unmodified. **This is not new to this round** — I checked
`git show 515e404:works/2026-08-05-the-second-reader/README.md`, and the identical shorthand
(`prompts/` and `evidence/` (committed data)) was already present at `515e404`. Round 4's own
Verifier did not catch it because, when testing "with exactly those exemptions," it silently expanded
`prompts/` and `evidence/` into the four literal filenames before invoking the script (visible in
`VERIFICATION-round4.md`'s own F1, which lists `prompts/reader-R1.txt`, `prompts/reader-R2.txt`,
`evidence/FINDINGS-draft-2026-08-04.md`, `evidence/INTERLOCUTOR-2026-08-04.md` as "exactly those
exemptions" rather than testing the paragraph's literal wording). Applying the same rigor round 4 used
to catch the `INTERLOCUTOR.md` gap to the rest of the same list surfaces this. The task's own
instruction — "run it with exactly the exemptions that paragraph now names… do not accept the claim;
execute it" — is what this finding follows.

**Secondary, non-blocking note on the same paragraph:** even under the generous reading, the true
headroom is a razor-thin 4 words (down from round 4's already-thin 3-word margin at the equivalent
check) — one more word anywhere in `README.md` or `READER-PROVENANCE.md` re-breaches the ceiling.

**Correction owed:** either name the four files individually in the paragraph (as it now does for the
eight review reports and `INTERLOCUTOR.md`), or extend `record_ceiling_check.py` to accept a directory
prefix for `--exempt`. Either fix makes the claim executable as written; neither is done in the bytes
graded here.

---

## Checked and correct

**§5b's attribution correction (Round 4's F2).** Read `VERIFICATION-round3.md` and
`SKEPTIC-round3.md` directly. `VERIFICATION-round3.md` F2 ("Reports the shipped text says are 'in this
directory' are not, at the graded commit") is exactly the claim-about-not-yet-existing-files issue
§5b now attributes to "round 3's Verifier." `SKEPTIC-round3.md` contains no mention of present-tense
claims, "in this directory," or files not yet existing — I grepped the full file for those phrases and
found nothing. The corrected sentence ("round 3's Verifier caught that... An earlier version said
'both reviewers'; round 4's Verifier read both reports and found only one raised it") is accurate.

**The two new `work.astro` §5 limit items, recomputed from `data.json` independently of the
frontmatter's own arithmetic.** Reimplemented the exact logic (`pubIn`, `r1OutOfPubIn`,
`r2OutOfPubIn`, `r2InsideR1`, `diverges`, `divergeOverlap`, `promptWord`, `pubInFlagged`,
`movedCases`, `movedFlagged`) in Python against `data.json`'s `cases` array and got: `pubIn.length` =
39, `r1OutOfPubIn` = 14, `r2OutOfPubIn` = 8, R2's set **is** a subset of R1's, `cases.length` = 60,
`d1.size` = 17, `d2.size` = 16, overlap = 15 (union = 18, matching `README.md`'s "union 18"),
`pubInFlagged` = 13, `movedCases.length` = 14, `movedFlagged` = 8 — every one matches what the page's
own frontmatter would render and what `README.md` §6 and `DEVIATIONS.md` D2 separately state in
prose. I also checked the *definitions*, not just the outputs: `r2InsideR1` is correctly scoped to
published-IN cases only; `movedCases` is correctly the union of strict published-IN→OUT movements
(not including UNDECIDABLE), matching D2's "14 unique cases either reader moved to OUT"; `diverges`
correctly spans all 60 cases and counts UNDECIDABLE as divergence, matching the `d1`/`d2` figures
elsewhere in the record. No definitional mismatch found — a correct number from a wrong definition is
not what shipped here.

**Restored caveats (round 4's non-blocking F3, F4).** `grep` confirms "a work of this practice's has
shipped compiling-but-dead before" is present in `README.md` §4, and "26 and 31 against 39" is
present in §6. Recomputed both figures directly from `data.json`'s
`carried.tables.undecidable_inside_population`: R1 n=26, R2 n=31, published n=39 — exact match.

**`DEVIATIONS.md` D2's new purge paragraph** ("6 of R1's 14 and 5 of R2's 8 strict-OUT movements
carry no such word at all, and zero reverse movements holds either way"), recomputed independently
from `data.json`: R1's 14 published-IN→OUT movements split 8 bench-worded / 6 not; R2's 8 split 3 /
5; deleting every bench/benchmark/evaluat/audit/suite-worded title from the population entirely still
gives zero published-OUT→reader-IN reversals for either reader. This also matches
`SKEPTIC-round4.md`'s own "Check 2" table exactly (14/8/6 and 8/3/5, zero reversals).

**Core numbers, recomputed from `data.json`/`results.json`, not from any prior report:**
- κ and agreement: published×R1 43/60=71.7%, κ=0.5355 (n=57); published×R2 44/60=73.3%, κ=0.699
  (n=52); R1×R2 52/60=86.7%, κ=0.9602 (n=51) — matches `README.md`'s table exactly.
- Populations: R1 IN = 23, R2 IN = 23, published IN = 39 — matches "Both readers return a population
  of 23" against "published 39 of 60."
- Movements: `original_IN_to_R1_OUT`=14, `original_OUT_to_R1_IN`=0; `original_IN_to_R2_OUT`=8,
  `original_OUT_to_R2_IN`=0 — 14+8=22 one-directional, 0 reverse, matches.
- Gap range: recomputed `100*m/n - 100*g/n` for all five rows in `carried.tables` — min 46.15, max
  69.57 — matches the claimed "46.2 to 69.6" to one decimal.
- "Fifteen" breakdown: `both_differ`=15, of which both-OUT=8, one-OUT-one-UNDECIDABLE=5, both
  UNDECIDABLE=2 — matches "eight both-OUT, five OUT/UNDECIDABLE, two undecided" exactly, and all 15
  are published-IN, matching the page's `bothDifferAllPublishedIn` claim.

**Reproducibility of `results.json`.** Reran `scripts/selftest.py` — 21/21 assertions pass. Reran
`scripts/score.py` and diffed the regenerated `results.json` against the committed one — byte-
identical (`sha256:a00194ef175c0a4ad9c95a4651719a5b5da63851abdf44e672db32598be55005`), matching the
"sha256:a00194ef…55005" citation in `README.md` §3.

**Commit-history self-description (README §4 / work.astro's frontmatter comment).** This repository's
clone was shallow; I unshallowed it (`git fetch --unshallow`) to check the cited hashes rather than
report them as unreachable. All six resolve, at exactly the claimed timestamps and in the claimed
order: `9417b3e` (2026-08-04 15:36:06, `RULE.md` + `blind-input.json`), `cae69e2` (15:40:25, contains
`scripts/score.py` — its own commit *message* is about an unrelated "team channel" matter),
`9c6d3d4` (15:42:09, `scripts/selftest.py`), `a724046` (15:43:55, `reader-R1.json`), `d6d52d6`
(15:45:49, `reader-R2.json`) — each strictly before the next. `a2ce131` (15:40:57) contains **only**
`DEVIATIONS.md`, despite a commit message that describes "the scoring script and the first
deviation" — this fully confirms the "crossed commit messages 32 seconds apart" story the record
tells about itself, including which commit is which.

**§5b's round-by-round table against the reports themselves.** `VERIFICATION-round4.md` has exactly
two findings marked `**BLOCKING.**` (F1, F2) and two marked non-blocking (F3, F4), matching "2
blocking (both in this record's description of itself)." `git cat-file -t` resolves `80908a2`,
`405c763`, `515e404`, `691a9de` as commits; `84f52b0` does not resolve in this repository even after
unshallowing — pre-existing and already disclosed inside `SKEPTIC-round3.md` itself, not a defect
introduced here.

**§0's account of the receiving-repository incident, checked against a fresh clone of
`frankbueltge/frankbueltge.de` (network-reachable from this environment).** The merge commit
`2be3529` exists, with parents `131fc56` and `f3f0b7a` exactly as cited; its date is 2026-08-06; its
committer is `GitHub <noreply@github.com>` and its author is `Frank Bültge <f.bueltge@gmail.com>` —
the repository's owner, matching "merged... by that repository's owner." At `131fc56` (the pre-fix
tip), `src/lib/field/dossier.test.ts` line 329 is `expect(real).toHaveLength(21)` and line 339 is
`expect(real[0].slug).toBe('2026-08-03-where-the-reader-declines')` — exactly the two pinned
assertions §0 describes. At `f3f0b7a` (the fix branch tip) both are gone, replaced by a comment
("Read off the mirror, not pinned to a number"). `field-feedback/2026-08-05.md`, cited in the same
paragraph, exists and contains the matching CI failure text almost verbatim ("expected... to have a
length of 21 but got 22"; "expected '2026-08-05-the-second-reader' to be
'2026-08-03-where-the-reader-declines'"). The commit `745965c`, cited in §5c, exists and is an
ancestor of that repository's current `main`, dated 2026-08-06 23:29:59 UTC — before the push this
session describes. I could not clone-and-build the whole receiving site to reproduce the "1,849 tests
in 109 files passing" / "astro check 0 errors" figures myself — same limitation
`VERIFICATION-round4.md` already recorded for this claim.

---

## Non-blocking observations

1. **§5b's "2 conditions" for round 4's Skeptic is a defensible but not obviously the only reading.**
   `SKEPTIC-round4.md`'s own "Summary — conditions, marked" section lists five numbered items; only
   two (1 and 2) carry an explicit "what must change" instruction, and the other three are
   self-labelled "informational, not a shipped defect" (3), "soft" (4), and "unresolved from round 3"
   (5). Counting only the two with explicit remediation gives "2," matching §5b — but this is the same
   kind of counting-convention ambiguity round 4's own Verifier flagged non-blocking for round 3's
   tally (its F5), so I am not treating it as a new problem, only noting it is still unsettled anywhere
   in the record.
2. **`WORKBOARD.md`** (outside `works/2026-08-05-the-second-reader/`) still reads "GAUNTLET PASSED
   TWICE, NOT SHIPPED," still names the retired `drafts/2026-08-05-the-second-reader/` path, and still
   describes PR 413 as "waiting on a human merge" — pre-existing, already flagged non-blocking by
   round 3's F3, still unresolved, outside this round's core remit.
3. **`prompts/reader-R{1,2}.txt`** still carry the duplicated preamble `SKEPTIC-round4.md` flagged as
   condition 5; untouched this round.

---

## What I could not check

- The exact test/build figures in §5c ("1,849 tests in 109 files passing," "astro check 0 errors,"
  "drift-check clean") at the receiving repository's `745965c` — I confirmed the commit exists and
  predates the push, but reproducing the full integration-and-test run this session describes was
  outside what I could do here (no local `astro`/site toolchain, and the described check integrates
  this work into that site rather than just checking it out).
- The exact minute of the GitHub merge. The object declines to state one ("repeated fetches returned
  different times... the API route... is closed to these sessions"). I could reach the repository via
  git's own protocol (its web UI returned 403 for me too, matching what round 3 found), and the merge
  commit's own committer timestamp is 18:58:53 UTC — consistent with, but not something I can use to
  either confirm or contradict, the object's decision not to state a time; its claim is about what
  those sessions could access, not a claim that no time exists.
- `READER-PROVENANCE.md`'s "one thing that cannot be disclosed" — not checkable by definition.
- Whether sampling settings for the two readers were truly never logged anywhere outside this
  directory — a negative claim about the dispatch process I have no way to verify from here.
- The precise 19:39:13 UTC timestamp for the original build-red event — not present in
  `field-feedback/2026-08-05.md` itself; I did not chase it further.
