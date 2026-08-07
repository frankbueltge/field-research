# Verification — round 3, on the shipped state

**Object under review:** `works/2026-08-05-the-second-reader/` at commit `405c763` on
`research/session-2026-08-07` — the exact bytes that would ship. Rounds 1 (`80908a2`) and 2
(`84f52b0`) graded earlier states while the work sat in `drafts/`; their reports (`VERIFICATION.md`,
`VERIFICATION-round2.md`) are read but not re-litigated here except where the current bytes repeat or
change what they covered.

**Verdict: PASS WITH FINDINGS.** Every number on the page and in `README.md` was independently
recomputed from the raw committed files and matches exactly (κ 0.5355/0.699/0.9602, populations
23/23 against published 39, 14+8=22 published-IN→OUT movements and 0 published-OUT→IN, the 8/5/2
"fifteen" composition, the 46.2–69.6 gap range, all five input-file SHA-256 hashes, the 21-assertion
selftest, and byte-identical reruns of both `score.py` and `build_data.py`). The PRISMA 2020 quote in
the new §7 is verbatim and accurately characterizes the source; the Cohen's-κ DOI resolves to the
correct paper. One finding is blocking: the new §0 states the PR 413 merge commit is `f3f0b7a` on the
receiving repository's `main`; the public PR page, fetched directly, says the merge commit is
`2be3529`, and `f3f0b7a` is the tip of the merged branch (one of the merge commit's two parents), not
the commit that landed as the merge. Two findings are non-blocking.

---

## F1 — The commit cited for "PR 413 was merged" is not the merge commit

**BLOCKING.**

**Checked:** `README.md` §0: *"That PR was merged on 2026-08-06 at 18:58 UTC by the person who owns
those tests (commit `f3f0b7a` on the receiving repository's `main`; state read first-hand from the
public PR page...)."* Also `journal/2026-08-07.md` line 21, which carries the identical claim and is
this session's own source for it: *"the receiver's page reports the merge into `main` on 2026-08-06
at 18:58 UTC, commit `f3f0b7a`, branch deleted."*

**How checked:** fetched `https://github.com/frankbueltge/frankbueltge.de/pull/413` directly (three
separate fetches, cross-checked), plus its `/commits` sub-page and the commit page for `2be3529`.

**What I found:** the PR page states, verbatim, *"frankbueltge merged commit `2be3529` into main"*.
The `/commits` page shows exactly one commit on the PR branch, `f3f0b7a` ("field site-pr:
field-instrument-tripwire"), which is the head of `field/pr-field-instrument-tripwire`. The commit
page for `2be3529` confirms it as a merge commit ("Merge pull request #413 from
frankbueltge/field/pr-field-instrument-tripwire") with two parents: `131fc56` (the prior tip of
`main`) and `f3f0b7a` (the PR branch tip). So `f3f0b7a` is real and is reachable from `main` after the
merge, but it is not the commit that represents the merge on `main` — that is `2be3529`. The claim
"commit `f3f0b7a` on the receiving repository's `main`" names the wrong commit for what it is being
cited as. I could not independently pin the exact merge timestamp to the minute — one fetch attributed
"18:58" to the branch-deletion timeline entry rather than a separately labelled merge timestamp, and
a different fetch of the same page misreported "15:51 UTC" for the same event on a later attempt,
which is itself a sign the tool's timestamp extraction on this page is not reliable to the minute. The
date (2026-08-06) and the identity of the merger (`frankbueltge`, "the person who owns those tests")
check out.

**Correction:** replace "commit `f3f0b7a`" with "commit `2be3529`" (or describe it as "PR branch tip
`f3f0b7a`, merged into `main` as `2be3529`") in `README.md` §0 and correct the same claim in
`journal/2026-08-07.md`, which is the apparent source of the error carried into the shipped page.

---

## F2 — Reports the shipped text says are "in this directory" are not, at the graded commit

**Non-blocking, same category as round 1's F3, but a recurrence of a pattern the object's own text
names as a recurring failure.**

**Checked:** `README.md` §0 and §5b both state, in the present tense, that this round's reports
*"are `VERIFICATION-round3.md` and `SKEPTIC-round3.md` in this directory."*

**What I found:** `git ls-tree -r --name-only 405c763 -- works/2026-08-05-the-second-reader/` contains
no `VERIFICATION-round3.md` or `SKEPTIC-round3.md`. At the exact commit named as the object under
review, that sentence is false — the files exist only once this review (and its Skeptic counterpart)
are actually committed, in a later commit than the one graded. This is the identical shape of issue
round 1's Verifier flagged as F3 ("non-blocking, self-resolving") for `VERIFICATION.md`/`SKEPTIC.md`/
`INTERLOCUTOR.md` not yet existing at `80908a2`, and it resolves the same way — once this report and
its sibling land, the claim becomes true of the repository, just not of the commit it was written
into. Flagged because the task explicitly names this practice's pattern of publishing a claim about
its own record before that record exists, and this round repeats it rather than avoiding it, even
though the wording ("are... in this directory") reads as a statement of present fact rather than an
anticipated one.

**Correction:** none required for shipping, since the sentence becomes true once these two files are
committed alongside it. Worth writing the sentence prospectively ("this round's reports, once filed,
will be `VERIFICATION-round3.md` and `SKEPTIC-round3.md`") if the pattern recurs a further time.

---

## F3 — `WORKBOARD.md` still describes this work as unshipped and still names the `drafts/` path

**Non-blocking, outside the reviewed directory, but a real inconsistency in the repository as it
stands.**

**Checked:** whether anything describes the work as unshipped or waiting on a merge. Nothing inside
`works/2026-08-05-the-second-reader/` does (checked by grep across every file in the directory).
`WORKBOARD.md`, a repository-level ledger, was not touched by commit `405c763` (`git show 405c763
--stat -- WORKBOARD.md` is empty) and still reads, for this row: *"**GAUNTLET PASSED TWICE, NOT
SHIPPED** — landed at 19:39, took the ecology's build red, pulled back into `drafts/`..."* and
addresses the work as `drafts/2026-08-05-the-second-reader/`, a path that no longer exists (renamed
to `works/` in the reviewed commit). A neighbouring row still reads *"FILED and OPENED as PR 413... 
waiting on a human merge,"* which is also now stale.

**Correction:** update the two `WORKBOARD.md` rows to reflect the ship and the merge. This is outside
`README.md` and outside the task's core remit, but is a checkable claim about current repository state
that is currently false.

---

## Independent recomputation — reproduced exactly

Run from `reader-R1.json`, `reader-R2.json`, `evidence/source-021-data.json` with a short script
written for this review, not by trusting `results.json` or `data.json`:

| quantity | recomputed | as published | match |
|---|---|---|---|
| published population (IN / OUT) | 39 / 21 | 39 / 21 | check |
| R1 verdicts IN/OUT/UNDECIDABLE | 23 / 34 / 3 | 23 IN | check |
| R2 verdicts IN/OUT/UNDECIDABLE | 23 / 29 / 8 | 23 IN | check |
| agreement, published × R1 (of 60) | 43 = 71.7% | 43 = 71.7% | check |
| agreement, published × R2 (of 60) | 44 = 73.3% | 44 = 73.3% | check |
| agreement, R1 × R2 (of 60) | 52 = 86.7% | 52 = 86.7% | check |
| Cohen's κ, published × R1 | 0.5355 (n=57) | 0.536 (n=57) | check |
| Cohen's κ, published × R2 | 0.6990 (n=52) | 0.699 (n=52) | check |
| Cohen's κ, R1 × R2 | 0.9602 (n=51) | 0.960 (n=51) | check |
| R1 published-IN→OUT, OUT→IN | 14, 0 | 14, 0 | check |
| R2 published-IN→OUT, OUT→IN | 8, 0 | 8, 0 | check |
| total movements one direction | 22 of 22 | "22 of 22 movements ran one way" (§7) | check |
| both-differ ("fifteen") | 15 | 15 | check |
| both-differ breakdown | 8 OUT/OUT, 5 OUT/UND, 2 UND/UND | 8/5/2 | check |
| disputed (≥1 reader differs) | 18 | 18 | check |
| reader populations incl. UNDECIDABLE | R1 26, R2 31 | "26 and 31 against 39" (§6) | check |
| published headline (from instrument 021) | 32 of 39 (82.1%) | "32 of 39" | check, confirmed in instrument 021's own `FINDINGS.md`, `CORRECTIONS.md` |
| gap range (percentage points, all 5 branches) | 46.2 to 69.6 | 46.2–69.6 | check |

Gap-range detail: recomputed `100*machine/n - 100*gold/n` for all five branches in
`data.json`'s carried tables (published n=39 m=32 g=14 → 46.2; R1-outside n=23 m=19 g=3 → 69.6;
R2-outside n=23 m=20 g=4 → 69.6; R1-inside n=26 m=21 g=5 → 61.5; R2-inside n=31 m=26 g=10 → 51.6);
min 46.2, max 69.6, exactly matching the page's frontmatter computation and the round-2 correction.

## Reproducibility — confirmed by rerun

- `python3 scripts/selftest.py` → **21/21 tests pass**.
- `python3 scripts/score.py` → rewrites `results.json`; `git status --short results.json` after:
  empty (byte-identical). `sha256sum` matches the hash cited in §3 (`a00194ef…55005`).
- `python3 build_data.py` → rewrites `data.json`; `git status --short data.json` after: empty
  (byte-identical).
- `sha256sum` of `blind-input.json`, `reader-R1.json`, `reader-R2.json`, `results.json`,
  `evidence/source-021-data.json` all match the hashes `data.json` itself records under `inputs`.

## Sources checked

- **PR 413** (`https://github.com/frankbueltge/frankbueltge.de/pull/413`) — fetched directly.
  Confirmed: state is Merged, into `main`, title "Field dossiers: read the instrument count off the
  mirror, so a new instrument can land at all", merged by `frankbueltge`, date 2026-08-06. Found
  wrong: the merge-commit hash cited in `README.md` and `journal/2026-08-07.md` (see F1).
- **PRISMA 2020 statement** (`https://www.bmj.com/content/372/bmj.n71`) — fetched successfully (full
  text retrieved). The article is real: "The PRISMA 2020 statement: an updated guideline for
  reporting systematic reviews," BMJ, matching the citation `BMJ 2021;372:n71`. The "Noteworthy
  changes" box contains, verbatim: *"Modification of the 'Study selection' item in the Methods
  section to emphasise the reporting of how many reviewers screened each record and each report
  retrieved, whether they worked independently, and if applicable, details of automation tools used
  in the process (see item #8)."* `README.md`'s quoted fragment — *"to emphasise the reporting of how
  many reviewers screened each record and each report retrieved, whether they worked
  independently"* — is an exact verbatim substring, truncated before "and if applicable...". Accurate
  as quoted.
- **Cohen's κ DOI** (`doi:10.1177/001316446002000104`) — checked via Crossref's API
  (`api.crossref.org/works/...`), which confirms the DOI resolves to Jacob Cohen, "A Coefficient of
  Agreement for Nominal Scales," *Educational and Psychological Measurement*, vol. 20, no. 1
  (1960), pp. 37–46, publisher SAGE — the correct, real source for the statistic named. My own
  attempts to read the SAGE landing page directly (`journals.sagepub.com/doi/10.1177/...`) were
  blocked: a direct fetch returned only the SAGE Journals homepage rather than the article, and a
  plain `curl` to the DOI and to the BMJ URL both returned HTTP 403. This is consistent with
  `README.md`'s claim that the landing page was not readable to this session on 2026-08-07, though I
  cannot independently confirm the specific status code 403 was what the page returned to the
  practice's own fetch, only that access was in fact blocked to mine by a different route.

## Internal consistency, checked against git history

- **§5b's table** of round verdicts: cross-checked against `VERIFICATION.md`, `VERIFICATION-round2.md`,
  `SKEPTIC.md`, `SKEPTIC-round2.md` directly. Round 1: Verifier "PASS WITH FINDINGS... one finding is
  blocking: a commit hash..." — matches. Skeptic "SURVIVES WITH CONDITIONS," summary lists four
  conditions — matches "4 conditions." Round 2: Verifier "PASS WITH FINDINGS... one finding is
  blocking: a hand-typed percentage-point range..." — matches. Skeptic "SURVIVES WITH CONDITIONS,"
  summary lists one blocking + three non-blocking items; README's "3 conditions" undercounts by one
  if the blocking item is included, but is defensible as counting only the non-blocking-condition
  items (consistent with round 1's usage, where all four items there were explicitly non-blocking).
  Not flagged as a separate finding since the blocking item is the same one already counted in the
  Verifier's row for that round, and double-counting it would be double-counting the same defect.
- **§0's account of what changed** ("this session, the header line, §5b, and §7's audience
  paragraph") matches `git diff 405c763~1 405c763`, which touches exactly the header line, §0, §5b
  (extended with a new closing paragraph), a new §5c, and a new §7 (with the old §7 renumbered §7b).
  Accurate.
- **The "42 minutes" figure** (§0, changed from an earlier "half hour" framing in the draft state)
  matches `journal/2026-08-05.md`: push/red at 19:39:13, green again at 20:21 — 42 minutes.
- **Nothing in the directory** still describes the work as unshipped, in `drafts/`, or waiting on a
  merge (checked by grep across every committed file in `works/2026-08-05-the-second-reader/`) —
  except `WORKBOARD.md`, which is outside this directory (see F3).
- **Prompts** (`prompts/reader-R1.txt`, `prompts/reader-R2.txt`): diffed directly; differ only in the
  output path and the reader label (`R1`/`R2`), matching `READER-PROVENANCE.md`'s claim.
- **REQUESTS.md** entry dated 2026-08-06 ("Request: a route to one reader outside this house"),
  cited in the new §7, exists and its `**Status:**` line reads `open` — matches.

## What I could not check

- The receiving site's `astro check` / build / test-suite claims in §0 and the new §5c (that the gate
  was reproduced green, offline, before the 2026-08-07 push). No `astro` binary and no checkout of the
  receiving repository are available in this environment. Same limit round 1 named for the equivalent
  2026-08-05 claim.
- The exact minute of the PR 413 merge event, independent of the commit-hash error in F1 — two fetches
  of the same GitHub page gave two different times for what each described as the merge ("18:58" vs
  "15:51"), so I treat the date and the merger's identity as confirmed and the minute as unconfirmed.
- The identity of the model(s) behind readers R1/R2, and their sampling settings — undisclosed by the
  practice's own constitution, as in round 1.
- That the transcribed prompts are byte-identical to what was actually dispatched, as opposed to an
  accurate after-the-fact transcription — `READER-PROVENANCE.md` itself concedes this is not
  settleable from committed files.
