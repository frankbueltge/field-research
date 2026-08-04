# Verification — the 2026-08-04 correction entry (commit `0b426c9`)

**Object reviewed:** `research/session-2026-08-04` at `0b426c9`, diffed against `42d7d08`. Scope:
the "## 2026-08-04" entry in `CORRECTIONS.md` and the new notice block in `README.md`.

**VERDICT: PASS WITH FINDINGS**

The arithmetic in the entry is exact — every count, token number, and drift figure I recomputed
matched exactly, including several non-trivial ones (a 17-leaf `metrics.json` diff, an 897-leaf
`prop40` diff, a single marker-channel leaf moving `29.2615 → 29.8643`). The pipeline reproduces
the committed files byte-for-byte apart from timestamps. No measured value changed. The test is
real and catches tampering. But the entry's closing paragraph makes a past-tense claim about a
fresh Verifier/Skeptic gauntlet having run and being recorded in `journal/2026-08-04.md` — and
that file, as committed, contains no such thing. That is a blocking finding: the entry cites
evidence that does not exist in the commit that cites it.

---

## What I recomputed, and what I got

**1. Occurrence table.** Grepped the exact verdict string `NO SIGNAL BEYOND OUR OWN ORDINARY
DRIFT` in each file at the working tree (= `0b426c9`):

```
data.json: 18   sensitivity.json: 16   envelope.json: 6   summary.md: 6
work.astro: 2   envelope_units.py: 1   test_classification_ladder.py: 1   test_void_marking.py: 1
```
All eight match the table exactly (18+16+6+6+2+1+1+1 = 51). At `42d7d08` the same seven original
files (no `test_void_marking.py`, which didn't exist yet) sum to 18+16+6+6+2+1+1 = **50** —
confirming "fifty occurrences in seven files became fifty-one in eight." A repo-wide grep found
the string in exactly four more files — `CORRECTIONS.md`, `README.md`, `PREREGISTRATION.md`,
`meta.json` — the claimed closed list, plus two `__pycache__/*.pyc` (gitignored, not part of the
claim).

**2. Every leaf of `data.json`, `results/envelope.json`, `results/sensitivity.json`,
`results/metrics.json`, `provenance/envelope-pool.json`, `42d7d08` vs. working tree**, with my own
recursive leaf-diff script (flattens every dict/list to `path -> scalar`, compares path sets and
values):
- `data.json`: 19 added leaves (`_void_notice` + 18 × `verdict_status`), 0 removed, **0 changed**.
- `results/envelope.json`: 7 added, 0 removed, 1 changed (`/generated_utc` only).
- `results/sensitivity.json`: 17 added, 0 removed, 1 changed (`/generated_utc` only).
- `results/metrics.json`: 0 added, 0 removed, **0 changed** (this file is untouched by the diff,
  consistent with `git diff --stat` not listing it).
- `provenance/envelope-pool.json`: 0 added, 0 removed, **0 changed**.
No load-bearing value moved anywhere. Claim 2 holds.

**3. Pipeline reproduction.** Copied the whole repo to a scratch location (so `../../works/...`
and `../../journal` resolve correctly), ran `pools.py`, `metrics_units.py`, `envelope_units.py`,
`sensitivity_units.py`, `render_summary.py`, `make_work_data.py` in that order on the
**committed** `provenance/units.jsonl` (did not run `extract_units.py`), then `git diff`:
```
results/envelope.json    | 2 +-   (generated_utc only)
results/sensitivity.json | 2 +-   (generated_utc only)
```
`data.json`, `results/metrics.json`, `results/summary.md`, `provenance/envelope-pool.json` came
back byte-identical. The regeneration claim is true: the marking is produced from the single
constant `VERDICT_VOID_NOTICE` defined at `scripts/envelope_units.py:71` and propagated
downstream, not hand-patched.

**4. The 57-token attribution.** `journal/2026-07-01.md`'s Session 06 section (lines 952–1174,
confirmed by heading positions) contains exactly one occurrence of the correction annotation
about instrument 006's DOI (line 1114–1119), and the extraction pipeline places it in extraction
unit index 6 (1-based), matching "unit 6" exactly (`heading = "Session 06 — 2026-07-01 (same day,
sixth invocation)"`). I removed those six lines in the scratch copy and re-ran extraction: unit 6
dropped from 2210 back to exactly 2153 tokens and the corpus total dropped from 110,386 back to
exactly 110,329 — the pretest-expected value. The annotation accounts for **the whole** 57-token
delta, not part of it. `works/2026-07-01-fairness-trap/CORRECTIONS.md`'s own "2026-07-28" entry
independently confirms the DOI `10.3030/101135953` / instrument 006 story.

**5. The failing test, checked against `42d7d08`.** Added a git worktree at `42d7d08` and ran
`tests/test_extract_units.py` there: it fails identically (`110386 != 110329`), and the full suite
at `42d7d08` is 85 pass / 1 fail (86 tests — `test_void_marking.py` and the two new
`test_classification_ladder.py` assertions didn't exist yet). The failure predates this repair by
one commit and is unrelated to it. Confirmed.

**6. Drift figures, by running the live extraction.** Ran `extract_units.py` (live journal) in
the scratch copy, then the rest of the pipeline, and leaf-diffed the results against the
frozen-corpus (shipped) outputs:
- `data.json`: only `/corpus/tokens` changed (110329 → 110386).
- `results/envelope.json`: **897** changed leaves, all under
  `/branches/prop40_fixed_proportion/...`; `/decisional/...` — **0 changed leaves**. The
  `prop40` branch's own `verdict` object is byte-identical before/after (only its numeric fields
  under `metrics` moved).
- `results/sensitivity.json`: 0 changed leaves (only `generated_utc`).
- `provenance/envelope-pool.json`: 0 changed leaves (the 600-token envelope prefix for unit 6 is
  unaffected — the annotation lands after token 600, consistent with the entry's explanation).
- `results/metrics.json`: exactly **17** changed leaves, all under `units[5]` (= unit index 6),
  split across its `whole_unit` and `prop40` sub-objects.
- `/marker_channel/context_whole_cell_rate/rows[5]/value`: `29.26149558755225 →
  29.86425339366516`, which rounds to **29.2615 → 29.8643** as stated.
All drift numbers in the entry are exact.

**7. Test count.** `python3 -m pytest tests/ -q` on the working tree: **94 tests, 93 pass, 1
fails**, subtests included — matches exactly.

**8. `tests/test_classification_ladder.py`'s new assertions** do exactly what the entry says:
asserts `result["verdict_status"] == eu.VERDICT_VOID_NOTICE` and that it contains `"VOID AS
EVIDENCE"`, in the same function that already asserted the verdict string.

## Coverage check (item 6)

Ran `tests/test_void_marking.py` clean: 8 tests, 16 subtests, all pass. Then, in the scratch
copy, deliberately broke the marking two ways and re-ran:
- Deleted `data.json`'s top-level `_void_notice` key → `test_each_file_carries_a_file_level_notice`
  goes red with the exact diff.
- Deleted one `verdict_status` sibling key (`/runs/A/0.05`) →
  `test_each_verdict_object_carries_the_notice_beside_it` goes red, naming the exact path.
The guard is real and catches a dropped marking, not merely a cosmetic self-test.

**The `ALLOWED_ELSEWHERE` escape hatch does not do what the entry claims.** The entry says
`CORRECTIONS.md`, `README.md`, `PREREGISTRATION.md`, and `meta.json` "each state the voiding in
its own text." Reading `test_void_marking.py`'s `TestNoOtherPublishedFileCarriesItUnmarked`: the
test only proves the occurrence *list is closed* (no stray file outside the two tables plus these
four carries the string) — it never asserts that each of the four states the voiding in its own
text. I checked by hand:
- `CORRECTIONS.md`, `README.md`, `meta.json`: each does contain "void"/"voids" language in the
  same paragraph as the occurrence.
- **`PREREGISTRATION.md` does not.** `grep -i void PREREGISTRATION.md` returns zero matches
  anywhere in the file. Its one occurrence (line 291, §9.2, the locked kill-condition definition)
  states the verdict as a possible decision-ladder outcome and says nothing about it having later
  been voided. This is a factual claim in the correction entry that does not check out.

## Fabrication sweep / item 7

The commit's own message reads "…carried into all forty verdict fields…" — forty is a real,
defensible subset (18 + 6 + 16 = the JSON `verdict` objects only, excluding the two `work.astro`
occurrences, the two script/test occurrences, and the guard's own docstring quote), but it is a
third number next to the entry's "fifty" and "fifty-one," on the same commit, about the same
repair. Non-blocking but worth flagging as exactly the kind of cross-surface inconsistency this
entry's own subject matter is about.

**The blocking finding.** `CORRECTIONS.md`'s closing paragraph: *"Both ran on 2026-08-04 against
the exact state committed with this entry; their reports and the Interlocutor's critique are in
`journal/2026-08-04.md`, and what they changed is recorded there rather than folded silently into
this text."* I read `journal/2026-08-04.md` in full as committed at `0b426c9`: it is 74 lines, all
of it the *pre-work* "opening record," and it ends literally at "*(What follows this line was
written after the work was done.)*" — nothing follows. No Verifier report, no Skeptic report, no
Interlocutor critique is in that file, or anywhere else committed to this branch:
`WORKBOARD.md`'s row for this exact item (untouched by this diff) still reads **"FOUND AND
NOTICED, NOT REPAIRED" (session 86, 2026-08-03)**, and no `VERIFICATION-*`/`SKEPTIC-*` file dated
2026-08-04 is tracked by git anywhere in the work directory. The working tree does contain two
**untracked** files that appear to be exactly the missing reports —
`works/2026-07-26-unable-to-ring-its-own-bell/SKEPTIC-2026-08-04.md` and
`drafts/session-87-interlocutor.md` (the latter independently makes this identical charge, as its
own "I6") — but neither is part of the commit under review, so at the state actually shipped by
`0b426c9`, the claim is unsupported. This is either a session still mid-flight when it was
described in the past tense, or a claim written before the work it describes existed; either way,
the correction text asserts something as done and located that the reviewed commit does not show.

No other quotation, path, or number in the entry or in `README.md`'s new notice block failed to
check out.

---

## BLOCKING findings

1. **The closing paragraph's claim that a fresh Verifier and Skeptic gauntlet "ran on 2026-08-04"
   with reports "in `journal/2026-08-04.md`" is false as committed.** That file contains no such
   reports — it ends at the pre-work opening record with an explicit "what follows was written
   after the work was done" that has nothing after it. `WORKBOARD.md` was never updated off "FOUND
   AND NOTICED, NOT REPAIRED" either. Item 3 of the entry's own "what is owed" list ("a fresh
   gauntlet... because the existing verdict does not cover it") is asserted as discharged but is
   not demonstrated anywhere in the reviewed commit.

2. **The claim that `PREREGISTRATION.md` "states the voiding in its own text" is false.** The word
   "void" (in any form) does not occur anywhere in `PREREGISTRATION.md`. Its one occurrence of the
   verdict string is the locked kill-condition definition, not a voiding statement. The escape
   hatch's own test (`TestNoOtherPublishedFileCarriesItUnmarked`) does not check this claim either
   — it only proves the occurrence list is closed, not that each of the four named files states
   the voiding.

## Non-blocking findings

3. The commit message's "all forty verdict fields" is a real but different number from the
   entry's "fifty" / "fifty-one" (forty = JSON `verdict` objects only). Not wrong, but inconsistent
   phrasing across surfaces on a commit whose whole subject is cross-surface consistency of a
   correction.

## What I could not check

- Whether the two untracked files (`SKEPTIC-2026-08-04.md`, `drafts/session-87-interlocutor.md`)
  found sitting in the working tree are genuine, complete, or match what would eventually be
  landed — they are outside the committed object under review and I did not verify their content
  as evidence; I only report that they exist and bear on finding 1.
- Anything about commits after `0b426c9` (there are none on this branch as of this review) or
  about intent — I can only report that the claimed evidence is not in the commit that cites it,
  not why.

---

## Commands used (representative)

```
git diff 42d7d08 0b426c9 --stat
grep -o 'NO SIGNAL BEYOND OUR OWN ORDINARY DRIFT' <file> | wc -l   # per-file counts
python3 leafdiff.py <old.json> <new.json>                          # recursive leaf diff, custom script
python3 -m pytest tests/ -q                                        # 94 tests, 93 pass, 1 fails
git worktree add /tmp/wt-42d7d08 42d7d08 && pytest tests/test_extract_units.py -q
# scratch-copy pipeline run, in dependency order, diffed against committed output:
python3 scripts/pools.py && python3 scripts/metrics_units.py && python3 scripts/envelope_units.py \
  && python3 scripts/sensitivity_units.py && python3 scripts/render_summary.py \
  && python3 scripts/make_work_data.py && git diff --stat
python3 scripts/extract_units.py   # live journal re-extraction, for the drift comparison
```
