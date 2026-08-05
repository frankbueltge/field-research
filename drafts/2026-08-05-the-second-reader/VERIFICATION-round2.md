# Verification, round 2 — The Second Reader

*Published unedited, as returned by the round-2 Verifier. The two HTML-escaped angle brackets in the
returned text are rendered here as the characters they encode; nothing else is changed.*

**Object under review:** `drafts/2026-08-05-the-second-reader/` at commit `84f52b0` on `research/session-2026-08-05-3`. This round checks the corrections made after round 1's PASS WITH FINDINGS (round-1 report: `VERIFICATION.md`; Skeptic: `SKEPTIC.md`; hostile critique: `INTERLOCUTOR.md`), independently, against the exact bytes at `84f52b0`. All checks below were run against that commit specifically (via `git show 84f52b0:<path>`), not against the branch tip, which moved forward by four further commits while this review was in progress — see the closing note.

**Verdict: PASS WITH FINDINGS.** Every one of round 1's corrections is real and independently reproduced: the commit-hash fix (F1), the `evidence/source-021-data.json` description fix (F2), the four Skeptic conditions, and the new sampling-settings limits entry are all present at `84f52b0` and all check out against the raw files, git history, and (where an environment permitted it) an actual rebuild of the receiving site. One finding is blocking: a hand-typed percentage-point range on the shipped page ("44 to 74 points") does not match the numbers in the work's own table (the true range is 46.2 to 69.6 points) — the same defect the page's own claim ("everything numeric is counted in this frontmatter") was supposed to rule out. Everything else recomputes exactly.

---

## F1 — `work.astro`'s hand-typed gap range ("44 to 74 points") does not match its own table

**BLOCKING.**

**Checked:** `work.astro:253–254` (at `84f52b0`): *"What carries the finding is the percentage-point distance between the two rows — 44 to 74 points in every branch above."* This sentence is hand-typed prose, not a value pulled from `data.json` — unlike every other figure on the page, which the work's own README and provenance section claim is counted, not hand-typed.

**What I found:** computing `machine_contextualizes_pct − gold_contextualizes_pct` for each of the five table rows from `data.json`'s own `carried.tables`:

| row | machine % | blind reader % | gap (points) |
|---|---|---|---|
| published | 82.1 | 35.9 | 46.2 |
| R1, undecidables outside | 82.6 | 13.0 | 69.6 |
| R2, undecidables outside | 87.0 | 17.4 | 69.6 |
| R1, undecidables inside | 80.8 | 19.2 | 61.6 |
| R2, undecidables inside | 83.9 | 32.3 | 51.6 |

The true range is **46.2 to 69.6 points**, not 44 to 74. The printed range is a loose superset that happens to contain the true one but is not what the sentence claims ("44 to 74 points in every branch"), off by ~2 points low and ~4–5 points high.

**Correction:** replace "44 to 74 points" with the differenced values, ideally computed in the frontmatter (as `minRatio` already is) — "46.2 to 69.6 points."

**Note on timing:** while this review was in progress, a further commit on the same branch (`6637776`, authored after `84f52b0`, outside the state graded here) independently found and fixed this exact defect, adding a frontmatter-computed `gapLow`/`gapHigh` resolving to 46.2–69.6, and a dated README correction crediting "the second review round" for surfacing it. That commit is not part of the state under review and does not change this finding at `84f52b0`; it is noted only because it independently corroborates this review's own recomputation.

---

## F2 — Round 1's commit-hash correction verified true

**Non-blocking — confirmed correct.**

Independently, with `git show`:

| commit | date/time (UTC) | contains | message topic |
|---|---|---|---|
| `9417b3e` | 2026-08-04 15:36:06 | `RULE.md`, `blind-input.json`, `make_blind_input.py` | matches |
| `cae69e2` | 2026-08-04 15:40:25 | `scripts/score.py` (285 lines) + unrelated `REQUESTS.md` | message is about "the team channel," not the scoring script |
| `a2ce131` | 2026-08-04 15:40:57 | `DEVIATIONS.md` only | message names "the scoring script," but the commit doesn't contain one |
| `9c6d3d4` | 2026-08-04 15:42:09 | `scripts/selftest.py` (230 lines, 21 assertions) | matches |
| `a724046` | 2026-08-04 15:43:55 | `reader-R1.json` | matches |
| `d6d52d6` | 2026-08-04 15:45:49 | `reader-R2.json` | matches |

`cae69e2` and `a2ce131` are exactly 32 seconds apart, matching the page's own description. The causal order holds using the corrected hash. **Accurate, and the printed times are exactly right.**

---

## F3 — Round 1's `evidence/source-021-data.json` description verified true

**Non-blocking — confirmed correct.**

The ship-state file at commit `1949ea6` exists (confirmed via `git cat-file -e` / `git show -s`). Diffing all five fields this work reads (`in_population`, `population_reason`, `exclusion_reason`, `gold`, `machine`) across all 60 cases programmatically returns **zero differences** between `1949ea6` and the current `evidence/source-021-data.json`. The current file carries exactly two extra per-case keys (`in_population_second_readers`, `in_population_status`) plus one extra top-level key (`_population_correction`) — precisely as the corrected README states.

---

## F4 — The four Skeptic conditions, verified executed on `work.astro`

**Non-blocking — confirmed correct.**

1. **"Reproduces" qualified at first assertion.** `work.astro:224–229`: the first assertion of "reproduces" is immediately followed, same paragraph, by the technology-family/sampling-settings qualification. Confirmed at point of first use, not deferred.
2. **8/5/2 composition disclosed on the page.** `work.astro:166–173` states it inline. Recomputed directly from `data.json`: **8 OUT/OUT, 5 OUT/UNDECIDABLE, 2 UNDECIDABLE/UNDECIDABLE = 15.** Matches exactly.
3. **Reuse stated plainly.** `work.astro`'s provenance section: "the reader data is the run of 2026-08-04, reused, not a second execution… one measurement presented a second time." Confirmed present.
4. **Ratio fragility flagged.** "Read the gap, not the ratio" paragraph states denominators of "3, 4, 5 or 10." Recomputed from `data.json`: the four re-split branches' blind-reader `contextualizes` counts are exactly **3, 4, 5, 10**. Matches exactly.

## F5 — Sampling-settings limits entry, verified present and consistent

**Non-blocking — confirmed correct.** `work.astro` §5 now states settings were never set or logged and that κ=0.96 "has to be read with that in front of it, not after it," matching `READER-PROVENANCE.md`'s own account and satisfying the Interlocutor's I4 demand for this caveat to be on the page itself.

---

## Independent recomputation of the two new probabilities (README §5)

From `data.json`'s own counts (`r1_in_to_out=14`, `r2_in_to_out=8`, `published_IN=39`):

- R1 strict IN→OUT rate: 14/39 = 35.897…% → **35.9%** ✓
- R2 strict IN→OUT rate: 8/39 = 20.513…% → **20.5%** ✓
- P(0/21 | p=0.358974) = 0.641^21 = 0.0000880 = **0.0088%** → rounds to **0.009%** ✓
- P(0/21 | p=0.205128) = 0.795^21 = 0.008058 = **0.8058%** → rounds to **0.8%** ✓

**Both recomputed probabilities are correct.**

---

## Reproducibility — re-run, not read

At `84f52b0`: `python3 scripts/selftest.py` → **21/21 pass**. `python3 scripts/score.py` → rewrites `results.json`; sha256 `a00194ef175c0a4ad9c95a4651719a5b5da63851abdf44e672db32598be55005`, matching the elided hash the README cites exactly. `python3 build_data.py` → "60 cases, 18 disputed." `git status` after all three: **clean, no diff.**

---

## README §0 — the receiving site's own gate, reproduced independently

A clone of the receiving site (dependencies installed) was available and used to independently reproduce, not merely read, the claims:

- **Integrator: accepted, `kind: astro`, nothing rejected.** Ran `scripts/atelier/integrate.ts` against a scratch copy of this work's committed files. Output: `{"accepted":[{"slug":"2026-08-05-the-second-reader","kind":"astro","ignored":[…supporting files…]}],"rejected":[]}`. Confirmed exactly as claimed.
- **The two test failures, exact messages, exact count.** With the receiving repository's *original, unmodified* `dossier.test.ts` and this work integrated: `AssertionError: expected [ … ] to have a length of 21 but got 22` (line 329) and `AssertionError: expected '2026-08-05-the-second-reader' to be '2026-08-03-where-the-reader-declines'` (line 339). **1 test file failed | 104 passed. 2 tests failed | 1698 passed (1700).** Verbatim match, exact count.
- **The proposed fix (`site-prs/field-instrument-tripwire/PR.md`) resolves both, breaks nothing.** With the fixed test file (matching the PR's description) staged instead: **105 files passed, 1700/1700 tests passed.**
- **`astro check`: 0 errors.** Ran directly: `Result (605 files): 0 errors, 0 warnings, 46 hints.`
- **Build completes; served page carries every figure.** `astro build` completed; inside the work's own `<article class="tsr">` markup specifically: **180 `.cell` spans, 30 `<details>` elements (15 pairs), 0 inline `style=`, 0 `<script>` tags** of the work's own. All match.
- Staged component files (`data.json`, `meta.json`, `index.astro`) are byte-identical to this work's own source files, consistent with a mechanical integration.

**Not verified:** the identity of the model behind R1/R2 (deliberately undisclosed, not attempted); byte-identity of the transcribed prompts to what was actually dispatched (the work itself says this cannot be settled); the readers' sampling settings (stated as unknown to the practice).

---

## What this round could not independently verify

- That the site clone used for reproduction is an untampered checkout of the receiving repository's `main` prior to this session — I ran the files as found and confirmed `git remote`/`git log` looked ordinary, but did not audit its history against a separately-fetched copy of the remote.
- That the exact sequence/environment the work's own account describes matches this session's reproduction process — I reproduced the claimed *outcomes* (2/1700 failing pre-fix, 0/1700 post-fix, 0 `astro check` errors, successful build with correct output), not the original session's process.
- The model/vendor behind R1 and R2, by design (constitutional prohibition) and by this review's own instruction not to name AI vendors.

## Note on repository state during this review

The branch advanced by four commits (`83cf8a9`, `3280712`, `6637776`, `9766b16`) during this review, from concurrent activity not initiated by this review. Only `6637776` touched files under this work's directory, and it is exactly the fix for Finding 1, credited to "the second review round" mid-session. Every check above was anchored to `84f52b0` specifically, and a diff of `84f52b0` against the current tip confirmed no other file under this work's directory changed. This review made no commits, edits, or writes to `/home/user/field-research` — an earlier attempt to write this report as a file into the repository was identified as a mistake and reverted before finishing; the repository's working tree is clean.
