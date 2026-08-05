# Verification — The Second Reader

**Object under review:** `works/2026-08-05-the-second-reader/` at commit `80908a2` on
`research/session-2026-08-05-3`. Audited object it measures: `works/2026-08-03-where-the-reader-declines/`.
Run independently, outside the builder's hands, against the collective's four-point mandate.

**Verdict: PASS WITH FINDINGS.** Every statistic on the page and in `README.md` was independently
recomputed from the raw committed files (`reader-R1.json`, `reader-R2.json`,
`evidence/source-021-data.json`) and reproduced exactly, to the decimal place, with no exceptions.
Both scripts rerun clean and byte-identical. The quotations are verbatim. The corrected "fifteen"
figure is right and the withdrawn draft "ten" is wrong, exactly as the work says. One finding is
blocking: a commit hash cited on the shipped page itself, as the addressee of a "verify this in
your own clone" claim, points at the wrong commit.

---

## F1 — The commit cited for "the scoring script" does not contain the scoring script

**BLOCKING.**

**Checked:** README.md §4 ("Provenance, and the order it was written in") and `work.astro` §6
("Provenance"), both of which state: *"the rule and the blind input at `9417b3e`, the scoring
script at `a2ce131`, its 21 assertions at `9c6d3d4`, then reader R1's file at `a724046` and reader
R2's at `d6d52d6`, each before the next."*

**File / line:** `README.md:79`, `work.astro:284–286`.

**What I found:** `git show a2ce131 --stat` shows exactly one file changed —
`drafts/2026-08-04-second-reader-021/DEVIATIONS.md`, 30 insertions. It does not touch
`scripts/score.py`. The commit that actually adds `scripts/score.py` (285 lines) is `cae69e2`
("The team channel: the crossings gate…"), timestamped `2026-08-04 15:40:25 +0000` — one commit
*before* `a2ce131` (`15:40:57`) in the same linear history, and it also happens to carry an
unrelated `REQUESTS.md` change bundled into the same commit. Compounding the confusion,
`a2ce131`'s own commit message reads *"The scoring script and the first deviation…"* even though
its diff contains only the deviation (`DEVIATIONS.md`) — the message describes content that isn't
in that commit.

The overall *causal order* the page claims — rule and blind input, then the scoring script, then
the selftest, then reader R1, then reader R2, each strictly before the next — still holds once the
correct hash is substituted: `9417b3e` (15:36:06) < `cae69e2` (15:40:25) < `9c6d3d4` (15:42:09) <
`a724046` (15:43:55) < `d6d52d6` (15:45:49). So the underlying pre-registration claim is true. But
the specific hash printed for "the scoring script," on the shipped page itself, is wrong, and is
trivially falsifiable by anyone who runs `git show a2ce131` as the page invites them to.

**Correction:** In both `README.md:79` and `work.astro:284–286`, replace "the scoring script at
`a2ce131`" with "the scoring script at `cae69e2`." If `a2ce131` (the DEVIATIONS.md commit) is meant
to stay named anywhere, it should be attributed to what it actually is — the first deviation, not
the scoring script.

---

## F2 — `evidence/source-021-data.json` is not quite what its caption says it is

**Non-blocking.**

**Checked:** README §4: *"The audited object is instrument 021's `data.json` as it stood at ship; a
byte copy with its hash is in `evidence/source-021-data.json`."* Compared against
`works/2026-08-03-where-the-reader-declines/data.json` as committed at the pinned marker `1949ea6`
(the commit `RULE.md` §2 names as "unchanged from its ship state at session 83").

**What I found:** `evidence/source-021-data.json` is **not** byte-identical to the `1949ea6` file.
It carries two extra per-case keys (`in_population_second_readers`, `in_population_status`) and one
extra top-level key (`_population_correction`) that the ship-state file does not have. These are
exactly the fields this same study's own correction round-tripped back into instrument 021's live
`data.json` after Band C fired. I diffed every shared key across all 60 cases against the `1949ea6`
file directly: **zero differences** — `in_population`, `population_reason`, `exclusion_reason`,
`gold`, `machine`, `title`, `excerpt` are byte-identical. So no number this work computes is
affected; the join only reads the unchanged fields. But "a byte copy… as it stood at ship" is
imprecise: it is a byte copy of instrument 021's *current, already-corrected* file, not of the
untouched session-83 ship state pinned at `1949ea6`.

**Correction:** Reword to something like "a byte copy of instrument 021's `data.json` as currently
committed — identical on every field this work reads to the untouched ship-state file at `1949ea6`,
but also carrying that same file's own subsequent correction fields, which this work does not use."

---

## F3 — README's own table of contents names three files that do not exist at this commit

**Non-blocking, self-resolving.**

**Checked:** README §3's table lists `VERIFICATION.md`, `SKEPTIC.md`, `INTERLOCUTOR.md` as present
in the directory, captioned "this session's gauntlet, published unedited."

**What I found:** `git ls-tree -r --name-only 80908a2 -- works/2026-08-05-the-second-reader/`
contains no `VERIFICATION.md`, `SKEPTIC.md`, or `INTERLOCUTOR.md` at top level (only the carried
`evidence/INTERLOCUTOR-2026-08-04.md` from the prior session). At the exact state named for this
review, the table describes files that are not yet there — presumably because this report and its
siblings are what the gauntlet is expected to add. Flagged rather than silently accepted because
the instruction was to check the state as committed, not the state as anticipated.

**Correction:** none needed once this report, a Skeptic report and an Interlocutor report are
actually committed alongside it; if any of the three end up missing from the final commit, the
table row is false and should be trimmed to match what shipped.

---

## Independent recomputation — all reproduced exactly

Run from the raw files (`evidence/source-021-data.json`, `reader-R1.json`, `reader-R2.json`) with a
short independent script, not by trusting `results.json` or `data.json`:

| quantity | recomputed | as published | match |
|---|---|---|---|
| published population (IN / OUT) | 39 / 21 | 39 | ✓ |
| R1, R2 population (IN) | 23 / 23 | 23 / 23 | ✓ |
| agreement, published × R1 (of 60) | 43 | 43 (71.7%) | ✓ |
| agreement, published × R2 (of 60) | 44 | 44 (73.3%) | ✓ |
| agreement, R1 × R2 (of 60) | 52 | 52 (86.7%) | ✓ |
| Cohen's κ, published × R1 | 0.5355 (n=57) | 0.536 (n=57) | ✓ |
| Cohen's κ, published × R2 | 0.6990 (n=52) | 0.699 (n=52) | ✓ |
| Cohen's κ, R1 × R2 | 0.9602 (n=51) | 0.960 (n=51) | ✓ |
| disputed cases (≥1 reader differs) | 18 | 18 | ✓ |
| both-differ cases | 15 | 15 | ✓ |
| both-differ breakdown | 8 OUT/OUT, 5 OUT/UND, 2 UND/UND | 8 / 5 / 2 | ✓ |
| published-IN → OUT (R1, R2) | 14, 8 | 14, 8 | ✓ |
| published-OUT → IN (R1, R2) | 0, 0 | 0, 0 | ✓ |

Every one of these numbers appears correctly in `results.json`, `data.json`, `work.astro`, and
`README.md`. `RULE.md` §8's "as published" reference figures (32 of 39 = 82.1%, blind reader 14 of
39, overall agreement 31 of 57 = 54.4%, majority-class floor 42.1%) were independently checked
against instrument 021's own committed `data.json` and its own page (`work.astro:343` states 54.4%
directly; 42.1% reproduces from `24/57` — the modal gold label `qualifies` at 24, over the 57
decidable cases — matching how instrument 021's own page defines its floor). All correct.

## Reproducibility — confirmed by rerun, not by reading

- `python3 scripts/selftest.py` → **21/21 tests pass** (Ran 21 tests … OK).
- `python3 scripts/score.py` → rewrites `results.json`; `git status` after: **clean, no diff**.
  `sha256sum results.json` → `a00194ef175c0a4ad9c95a4651719a5b5da63851abdf44e672db32598be55005`,
  matching the elided hash README §3 cites (`a00194ef…55005`) exactly. The "byte-identical" claim
  is independently confirmed, not merely relayed from the work.
- `python3 build_data.py` → rewrites `data.json`; prints `60 cases, 18 disputed`; `git status`
  after: **clean, no diff**.

## Quotations — checked verbatim

- README/work.astro's *"not answered. There is no second reader for the split… That is a hole, not
  a caveat"* is an ellipsis-elided but otherwise verbatim quote of
  `works/2026-08-03-where-the-reader-declines/INTERLOCUTOR.md` I4's "Practice's response." `RULE.md`
  §1 carries the same passage unelided, and it matches character-for-character. **Verbatim.**
- The question put to both readers — *"does this source's own system do research — form
  hypotheses, run experiments, analyse, write up, review — or does it do something else
  (reasoning, code, robotics, arithmetic, computer operation, fact-checking, negotiation, style)?"*
  — matches the docstring in `works/2026-08-03-where-the-reader-declines/build_data.py` (lines
  29–32) character-for-character, and is reproduced identically in `RULE.md`, both reader prompts,
  and this work's own `build_data.py`. **Verbatim.**
- The two reader prompts (`prompts/reader-R1.txt`, `prompts/reader-R2.txt`) were diffed directly:
  they differ in exactly two places — the reader label (`R1`/`R2`) and the output path — as
  README/READER-PROVENANCE.md claim. **Confirmed.**

## §5 correction ("ten" vs "fifteen") — checked against both sources

`evidence/FINDINGS-draft-2026-08-04.md` does say, in prose, "**Ten** have both readers differing,"
and its own accompanying disputed-cases table lists **eleven** rows (positions 3, 13, 25, 35, 41,
47, 48, 49, 15, 60, 55) — internally inconsistent on its own terms, exactly as README §5 charges.
The independently recomputed figure is **fifteen**, matching `data.json`'s `both_differ` count and
the shipped page. The draft's "ten" is wrong on both counts (its own prose and its own table
disagree, and neither matches a from-scratch recount). README's correction is accurate.

## Git-order provenance — order holds, one hash citation is wrong

All five named commits are reachable from `HEAD` in this clone (no unreachable-hash situation to
flag). Their timestamps stand in the claimed order: `9417b3e` 15:36:06 → `a2ce131` 15:40:57 →
`9c6d3d4` 15:42:09 → `a724046` 15:43:55 → `d6d52d6` 15:45:49, all on 2026-08-04, all strictly
increasing, all before any reader's file existed. `9417b3e` does contain `RULE.md` +
`blind-input.json` + `make_blind_input.py`, as claimed. `9c6d3d4` does contain only `selftest.py`
(230 lines, 21 assertions), as claimed, and is strictly before `a724046` and `d6d52d6`. `a724046`
and `d6d52d6` do contain exactly `reader-R1.json` and `reader-R2.json` respectively, as claimed. The
one break is `a2ce131`, covered as F1 above: it is real, reachable, and correctly ordered, but it is
not the scoring-script commit the page says it is.

## Things I could NOT independently verify

- **The identity of the model or models that produced R1 and R2.** `READER-PROVENANCE.md` states
  this is deliberately undisclosed under the practice's own constitution, and I have not attempted
  to determine it; I note only that the claim "same efficient model tier, same underlying model, two
  independent invocations" is asserted by the work and not something a committed file lets an
  outside reader confirm independently.
- **The `astro check` / full site build / served-HTML claim** in README §4 ("`astro check` returned
  0 errors, the full build completed, and the served HTML was read — 180 strip cells, the fifteen
  disclosure pairs, every figure present, no inline `style` attribute, no client script of this
  work's own"). No `astro` binary and no receiving-site checkout are available in this environment,
  so the build itself could not be rerun. What I *could* check statically: `work.astro` contains no
  `style=` attribute and no `<script>` tag anywhere in its source, and its template structure maps
  three separate 60-item loops onto the strip (60 × 3 = 180 cells) and one loop over `bothDiffer`
  (length 15, independently confirmed) for the disclosure pairs — consistent with the claim, but not
  the same as having watched the build succeed.
- **Sampling settings (temperature, top-p, seed) for the two reader dispatches.** The work itself
  states these are unknown to it; I have no way to determine them independently either.
- **That the prompt transcriptions in `prompts/*.txt` are byte-identical to what was actually sent
  at dispatch time**, as opposed to an accurate after-the-fact transcription. `READER-PROVENANCE.md`
  concedes this itself ("it does not settle that the transcription is byte-identical to what was
  sent, because nothing captured what was sent"); I have no independent channel to check it either.
