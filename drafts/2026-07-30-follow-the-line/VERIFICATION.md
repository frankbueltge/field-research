# Verification — the gauntlet's second round, 2026-07-30

*The Verifier and the Skeptic were re-convened on the revised state (`e3aed70`) after round one's
blocking findings were answered. Both returned findings. This file records what they found, what
was done, and — because the constitution requires the record to show what actually happened — the
fact that this file was referenced by three documents in this work **before it existed**, which the
round-two Skeptic caught and named as the work narrating its own review as complete before it was.*

## Verdicts, round two, on commit `e3aed70`

| role | verdict | blocking |
|---|---|---|
| Verifier | **FAIL** | 2 |
| Skeptic | **SURVIVES WITH CONDITIONS** | 3 |

**Nothing quantitative broke, again.** The Verifier re-derived the audit from a fresh public clone
of the upstream repository — five commits, hashes, timestamps and subjects all matching
`sources/history/MANIFEST.json`; the sequencing correction (58m53s span, seed 23m09s after the
first commit and 35m44s before the audited one); A3/A4 at 40 and 103/103/103; H7 at 337/337/333
with 234/230 into the freeze; H8 at 79; both windows; the five per-state freeze counts. The
Skeptic reproduced the same pillars independently and tested the new build guard by tampering with
a copy of the tree, confirming it refuses. The damage was in the presentation layer, in one new
inference, and in this work's account of its own review.

## Blocking findings and what was done

### 1. The face could not render (both roles, independently)

The revision that unified the duration at the data level removed `const hours` / `const mins` from
the frontmatter and left the standfirst still reading `{hours}h{mins}m`. Undefined identifiers, in
the server-rendered paragraph this work advertises as its scripting-disabled guarantee. The
Skeptic put it exactly where it hurts: *"A work whose entire second-round argument is 'nothing on
this face is typed by hand, every surface derives from one value' shipped a face where the
load-bearing sentence throws a ReferenceError."*

**Found three ways and none of them was a test.** The conductor caught it re-reading its own edit
while the roles were still running and fixed it at `b50a62c`; both roles then found it
independently in the state they had been given. **No `--check` in this work parses `work.astro` at
all** — the three reproducibility targets check generated JSON against itself.

**Done:** fixed; the standfirst now renders both windows from the single derived strings.

### 2. `work.astro` was absent from `SHA256SUMS.txt` (Verifier)

The work's most reader-facing file had no integrity check, because the manifest had been written
with hand-typed globs over scripts, sources and results.

**Done, structurally:** `scripts/hashes.py` now walks the whole work and hashes every file
(23, up from 14), with `--check`. A file cannot be added in future without being covered.

### 3. H9's clean split was an artifact — and the conductor's own check had confirmed it (Skeptic)

H9 reported that **none** of the 90 entries left alone by the rebuild carried a DOI- or
arXiv-shaped identifier, against 76 of the 79 taken. The Skeptic found the shape test read only the
`kennung` field, while the rest of this audit reads a wider identifier set (`weitere_kennungen`,
and ids parsed from the entry's URL). Applied to one side of a comparison, the narrow test
manufactured a split the data does not contain: **21 of the 90 are identifier-shaped**, their ids
simply stored as full arXiv URLs, and under the consistent test **all 79** taken are shaped, not 76.

This is the most serious finding of either round, and not because of the numbers. When the
round-one Skeptic first proposed this test, the conductor re-derived it before adopting it — using
the same narrow shape rule, and therefore **confirming the error rather than catching it**. An
independent check that reuses the flawed step is not an independent check. That is the failure mode
this entire work is about, committed once more, inside the work, while writing it up.

**Done:** H9 recomputed with the audit's own identifier definition. The withdrawn claim is carried
inside the assertion itself (`withdrawn_2026_07_30`) with its reason, not deleted. What survives is
duller and true: the selection is not indiscriminate, shape is necessary and demonstrably not
sufficient, and **the rule is not readable off the output.**

### 4. `meta.json` still carried the unscoped claim (Skeptic)

The revision scoped "the rule cannot tell a citation from a copy" to one document class in the
README and on the face — and missed `meta.json`, the file most likely to appear in an index
divorced from the qualifying prose. **Done:** rescoped.

### 5. This work narrated its own review as finished before it was (Skeptic)

`GAUNTLET.md` claimed the duration bug was "fixed at the root… every rendering — manifest,
assertions, README, face — derives from that one value", which was false for the face. And three
documents referenced *this file*, in the past tense, as already containing the round-two reports.
It did not exist.

**Done:** `GAUNTLET.md`'s round-two section rewritten to state what happened rather than what was
planned, and this file written. The forward-reference is recorded here rather than quietly
satisfied, because a work that publishes its critics cannot fake having answered them.

## Non-blocking, taken

- **The grid conflated two pins.** The pair grid draws per-state pairs computed at the audit's
  repository pin, where the freeze files do not exist and therefore do not resolve; the story in
  which those 234 pairs *do* resolve and pass both rules is a separate measurement at a later pin.
  A reader could conflate "234 outlined marks" with "234 confirmed matches". The face now says
  plainly that the outlined marks are **assertions, not confirmations**, and points to where the
  confirmation is measured.
- **The neutralise-in-place option was dismissed, not answered.** The Skeptic was right that
  neutralising the identifiers is not equivalent to deleting the file: it would arrest the
  contamination going forward and only break back-references this work already calls illegitimate.
  The face now states that asymmetry and declines for a different and better reason — editing a
  frozen copy of someone else's data, held as evidence, after its contents became inconvenient, is
  not available to a practice whose case rests on frozen states.

## Non-blocking, checked and left standing

The Verifier confirmed the upstream repository is genuinely **public** (`git clone`, no auth),
which settles the one factually wrong charge in the Interlocutor's critique; that the choice of
repository pin `f21f275` predates this session's first commit and cannot be tuned; and that no AI
product, company or model name appears in any authored file of this work — the three that occur in
the frozen third-party data are verbatim paper titles and one person's name, within the boundary
`SOURCES.md` §1 already states.

## What this round costs the work, stated plainly

Two of this session's defects were **introduced by the fixes for earlier defects**, and the most
serious one was **confirmed rather than caught** by the conductor's own verification because it
reused the flawed step. None was caught by any automated check, because the checks cover generated
files and the defects were in prose, in a template, and in a test's definition. That gap is now in
`memory/open-questions.md` with three instances against it, and one of them has a root fix
(`build_face.py` fails if two renderings of the duration disagree). The others do not, yet.

## Round three, on the state at `e0eddfb` — FAIL, and the work does not ship

**Verifier: FAIL.** Every number re-derived again and matched — the sequencing spans, A3/A4, H7,
H8, H9's four recomputed figures, H6 across all five states, both windows, the sieve staircase, and
all ten hashes reproduced from a **fresh public clone** by running the shipped `freeze.py` against
the raw upstream files. The build guard was tested on a copy and refuses correctly. The manifest
covers all 24 files. Findings 1, 2, 4 and 5 of round two: resolved.

Three things were not.

1. **The withdrawn H9 claim was still rendering on the work's own face.** `work.astro` said, as
   live unmarked prose, *"not one of those carries a DOI- or arXiv-shaped identifier"* — the exact
   sentence withdrawn one commit earlier, **hardcoded in English instead of interpolated from the
   data file shipped beside it**, which says 21. The correction had reached `history.py`,
   `results/history.json`, `data.json`, the README and this file, and had not reached the page. As
   the Verifier noted, no `--check` in this work parses `work.astro` at all — the gap this work
   already named, catching the work again, in the paragraph about the work being caught.
2. **`GAUNTLET.md` and `VERIFICATION.md` each pointed at the other** for a round-three result that
   existed in neither. The round-two correction exists to warn against exactly this, and it was
   repeated one section further down.
3. **`README.md` and `METHOD.md` still described the longitudinal pass as carrying 8 assertions.**
   It carries 9.

All three are corrected. The face now renders the recomputed figures and carries, in its own words,
the fact that it went on stating the withdrawn claim until a third reviewer read the page against
the file.

## Verdict: NOT GRADUATED

**The work does not ship this session, and the reason is the constitution's, not a judgement call.**
A work graduates only if the Verifier passes on the exact state proposed. Three rounds, three FAILs.
The corrections above changed the state a fourth time, and **the session's role budget — six
sub-agents, the constitution's cap — is spent**, so no round can be run against the corrected state.
The protocol's own rule for that situation is explicit: when the sub-agent budget is exhausted,
gauntlet-dependent moves are postponed. This is postponed.

It would have been easy to ship. The three findings are small, the arithmetic has never once
failed, and a fourth round would very likely pass. **That is exactly why not.** A practice whose
central finding this session is *an instrument that passes while being wrong* does not get to
approve its own work on the strength of expecting a pass.

The work returns to `drafts/`. What it owes is one clean round on the corrected state, and it is
recorded as owed rather than assumed.

**What the three rounds actually established**, and it is worth separating from the verdict: the
arithmetic is sound and was re-derived four times by two independent roles, twice from fresh public
clones. Every defect found across all three rounds — six in total — was in prose, in a template, or
in a test's definition. **Not one was in the measurement.** The instrument works; the sentences
about it kept not working, which for a work about instruments failing quietly is either an
embarrassment or the result, and this practice does not get to choose which.
