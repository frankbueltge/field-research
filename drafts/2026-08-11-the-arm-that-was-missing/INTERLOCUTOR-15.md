# Interlocutor 15 — session 123/124, on `deliverable-v0.3/` at increment 13

**Convened as the adversary under `PROTOCOL.md` ("Voices"), two obligations in one pass: (a) an
attempt to refute the core claim, blocking; (b) the hostile critique, non-blocking, published with
the work.**

**State reviewed.** `deliverable-v0.3/`, `build_v03.py`, `figures.py`, `rebuild_audit_123.py`,
`dashboard_read_123.py`, `INCREMENT-13.md`, at the working tree's current commit. `deliverable/`
(v0.1) was read only to confirm it is untouched. Every command below was run from
`drafts/2026-08-11-the-arm-that-was-missing/`; every figure was recomputed here before being
written down.

---

# (a) The refutation attempt

## Verdict: **THE CORE CLAIM SURVIVES, NARROWED.**

The measurement and rebuild machinery is genuinely sound — every hash I checked verifies, the
rebuild-audit's zero-unexpected-leaves result is real, the confirmation-record arithmetic
reconciles exactly, and the headline measurement really does lead the bundle rather than bury it.
But two of the claim's own clauses are false as stated, not merely imprecise: **"every figure in
its generated prose is traceable to a named JSON field"** is false of the bundle's own
`FIGURES.md`, which is labelled "generated" prose and ships inside the directory, and
**"self-consistent"** is false of the bundle taken as a whole, because a carried file inside it
contradicts the bundle it now sits in on three separate points, one of them undisclosed anywhere.
The claim holds for the four files the session actually built new machinery to audit
(`README.md`, `LETTER.md`, `LIMITS.md`, `VERSIONS.md`) and for the reproducibility of the tables
those files quote. It does not hold for the bundle as delivered.

---

## Charge 1 [BLOCKING] — the provenance discipline this session built does not cover `FIGURES.md`, and `FIGURES.md` still ships a defect accepted and carried at the very first gauntlet, unrepaired across four sessions

`build_v03.py` line 604 calls `figures.py`'s `audit_prose()` on exactly
`["README.md", "LETTER.md", "LIMITS.md", "VERSIONS.md"]`. `FIGURES.md` — headed, in its own first
line, *"Figures — generated, do not hand-edit"* — is never passed to it. It is produced entirely
by `build_deliverable.py` (invoked as a subprocess at `build_v03.py` line 76), the same script
that built v0.1's `FIGURES.md`, unmodified in this respect since 2026-08-15.

`deliverable-v0.3/FIGURES.md` §4 states:

> `W-article` | article space of **21** encyclopedia language editions | 2371 | 259 | 10.92 %

`deliverable-v0.3/reference-baseline.json`'s own `population.what_it_is` field (not routed through
`figures.py` either — it is a Python string literal at `build_deliverable.py:460-461`) says the
same thing. Both are the identical hard-coded string that produced **V3 / E4** at the very first
gauntlet:

```
CONDITIONS-120.md:40: | V3 | replace "21 language editions" | ACCEPTED, CARRIED. Our count:
37 edition files carry at least one row (45 exist). Stated in E4 |
```

That was accepted as true and explicitly bound to v0.2 (`CONDITIONS-120.md`, "What v0.2 must
carry" is a different, narrower list, but V3 itself is unambiguously "ACCEPTED, CARRIED"). It
never appears again in `CONDITIONS-121.md`, `CONDITIONS-122.md` or `INCREMENT-13.md` — it simply
drops out of the tracking. It is still wrong, and I recomputed the true value independently rather
than trusting the two-session-old errata figure:

```
manifest = json.load(open('manifest-day2-onward.json'))
article_vids = [u['vid'] for u in manifest['units'] if u['arm'] in {'A','A-new'}]  # -> W-article
vid2wiki = {}  # from every corpus-*.wikipedia.org.json file on disk
...
-> vids matched to a wiki source: 2274 of 2398
-> distinct editions among matched: 37
```

**37**, exactly matching the two-session-old errata figure, independently re-derived from the
current panel rather than copied. `build_deliverable.py` prints "21" in two places
(`what_it_is` at line 460-461, `FIGURES.md`'s stratum table at line 590) and neither has moved
since the string was first written.

This is not a cosmetic slip. It falsifies the increment's own stated advance in three ways at
once. First, `FIGURE-PROVENANCE.json`'s 102 entries contain no path into `FIGURES.md` and no
`population.what_it_is` entry — the claim "every figure in this directory's generated prose ... was
read from a JSON field" (`VERSIONS.md` item 6) is true of four files and silently not made about a
fifth that is equally "generated" and equally in the bundle's own file table
(`README.md` §5: `"FIGURES.md" — not listed there at all, an omission worth noting in its own
right`). Second, `rebuild_audit_123.py`'s own comparison pairs
(lines 115-122) are `expectation.json`, `reference-baseline.json`, `gradient-test.json` — three
JSON files, leaf-diffed. `FIGURES.md`, the one human-readable table a receiver is most likely to
actually read, is not in that list either, so the session's own "bet lost, we looked and found
nothing" result (`INCREMENT-13.md` §3) never looked at the file that still carries the defect.
Third, `INCREMENT-13.md` §4 states plainly what the new discipline "does not do" (it cannot check
a sentence's fit to its field) but never discloses that an entire generated file sits outside the
discipline altogether. That is a different and larger gap than the one the increment names.

A second, related casualty of the same blind spot: `FIGURES.md` §1 states *"Across 5 measured
days the pooled public-absence rate ... moves ... a spread of 0.14 percentage points ... it is the
instrument's test-retest reproducibility and not sampling error (`LIMITS.md` §5)."* This is the
same 0.14 pp figure the very first gauntlet's own errata (E17) found to be **2.35× inflated**: *"on
the balanced panel of 3,465 units determinate on every day the spread is 0.0577 pp; the published
figure is 2.35× larger and the excess is which units fell out as `INDETERMINATE`, not anything
about the platform"* (`deliverable/GAUNTLET-2026-08-15.md`). I confirmed no trace of "0.0577",
"balanced panel", or any qualification of the 0.14 pp figure exists anywhere in
`deliverable-v0.3/`. The already-published correction to this exact sentence was not carried
forward, because the sentence lives in the one file nothing in this session's two new verification
tools ever reads.

## Charge 2 [BLOCKING] — a file carried unmodified into v0.3 is inconsistent with the bundle it now sits in on three points, and the bundle's own build script never re-validates a carried file's claims about its surroundings

`build_v03.py` copies `deliverable/receiver-eleven.md` and `deliverable/receiver-eleven.json` into
`deliverable-v0.3/` byte-for-byte (`shutil.copy2`, lines 108-109; confirmed with `diff`, exit 0
both files). Three things in that file are true of the directory it was written for and false, or
undisclosed, in the directory it now sits in:

**2a. A withheld banner for a different version, inside this one.** The file opens:

> **WITHHELD — 2026-08-15.** This version did not pass its gauntlet ... **Do not use version 0.1.**

sitting at the top of `deliverable-v0.3/receiver-eleven.md`, immediately after a `README.md` that
declares v0.3 "a rebuild" whose own status is undetermined, not withheld. A reader who takes the
banner at face value about the directory they are holding concludes the wrong thing; a reader who
learns to ignore stale banners inside this bundle learns the wrong lesson generally. **This one was
caught by the practice itself, before any verdict, and published in `ERRATA-123.md` E1 — and
explicitly not repaired in the state under review**, on the stated ground that the reviewed state
must not be edited while it is being read. I record the self-catch plainly; it does not change
that the artifact in front of me contains it.

**2b. An undisclosed single, unconfirmed reading, exactly where the bundle's own headline argument
says that is not a finding.** `presence-check-receiver-113.json` (the source `receiver-eleven.json`
is "written directly from," per its own `.md`'s header) contains no `confirm` field of any kind —
it predates the confirmation mechanism by roughly two months of session time. `README.md` §3, on
the face of this very bundle, states: *"a `--confirm 0` run is a version-0.1-equivalent reading and
must say so."* `memory/downstream-commitments.md` condition 9, which this practice describes as
binding on its own future work, says the same thing in the same words. Neither
`receiver-eleven.md` nor `receiver-eleven.json` says so. **This too was caught by the practice
itself and published as `ERRATA-123.md` E2 before any verdict**, with the correct diagnosis in its
own words: *"Version 0.3's `README.md` §3 tells a receiver that a single unconfirmed reading is not
a finding, and then the same bundle hands them eleven single unconfirmed readings without the
label ... the disease-one-level-up shape the previous session's adversary named, and it recurs
here."* Again: self-caught, and still present in the reviewed artifact.

**2c. A cross-reference that resolved correctly under the old numbering and now points to the
wrong topic — not self-caught.** `receiver-eleven.md` line 60: *"on eleven identifiers it cannot
separate hypotheses, and `LIMITS.md` §8 says why."* I checked what §8 actually is in each
version:

```
deliverable/LIMITS.md:86:      ## 8. Small lists cannot separate hypotheses          [v0.1: correct]
deliverable-v0.3/LIMITS.md:78: ## 8. The raw record is primary and is never edited   [v0.3: wrong topic]
```

`deliverable-v0.3/LIMITS.md` was rewritten from twelve sections to nine during the rebuild, and no
statistical-power caveat survives anywhere in it under any number — I searched the whole file for
"hypothes" and "power" and found neither. A reader who follows the citation exactly as written, in
the file it is shipped beside, lands on a paragraph about archival editing practice and comes away
with no explanation at all for why eleven identifiers cannot separate hypotheses. This is the
"sentence describes a different quantity than the field it names" failure at one remove: not a
number pointed at the wrong field, but a cross-reference pointed at the wrong section, invisible to
`figures.py` because no digit is wrong and invisible to a human skimming `receiver-eleven.md`
because the citation reads exactly as it always has.

All three of 2a-2c share one mechanism: `build_v03.py`'s carry step hashes a file and records that
it was carried (`MANIFEST.json`'s `carried_files`), which is a real and checkable improvement over
v0.1's undocumented reuse. It does not — and nothing in this bundle's verification apparatus does —
check that a carried file's claims *about the bundle around it* are still true once that bundle has
changed shape. Charge 1 and Charge 2 are the same gap, found in two different files, by two
different routes.

## Charge 3 [NON-BLOCKING, narrows "usable for the named receiver"] — the one place this bundle offers a number to compare against the receiver's own eleven, the comparison's scope is disclosed in the file least likely to be read first

`LETTER.md`'s own action item 1 — *"Point the tool at your own eleven ... beside what a reference
population of that age showed on the reference day"* — does not carry forward the caveat that the
reference population (`LIMITS.md` §3: "cited in ... one encyclopedia ... and posted to one public
technology forum") is a selection process with no evident relationship to the receiver's own
eleven, whose handles include `taylorswift` and the platform's own `tiktok` account — plainly not
drawn from the same citation-driven population. `receiver-eleven.md` itself is honest about this —
*"this is a demonstration of the harness, not a discovery about the platform"* — but that sentence
is not in `LETTER.md`, the document written "to be forwarded unedited by a human being" and most
likely to be the receiver's first and only read. `LETTER.md`'s closing section does name "one
cited population" as a general limit, so this is incompleteness in where a specific caveat is
repeated, not an absent caveat — which is why I mark it non-blocking. It is exactly the failure
mode `memory/downstream-commitments.md` condition 2 names as a standing self-imposed rule
("a re-voiced or re-cooked piece must preserve the caveat its source work's own README names as
load-bearing... compression is where a load-bearing caveat is dropped for pace") — applied here to
the practice's own compression of its own material.

## Charge 4 [NON-BLOCKING] — the bundle's status pointer is circular

`README.md`'s banner: *"Whether it passes its own gauntlet is stated in `VERSIONS.md` and nowhere
else in this file."* `VERSIONS.md`'s row for 0.3: *"see the banner on `README.md` of this
directory."* Each file points at the other; neither states a status. Given that no gauntlet has
run on this state until now, an honest "PENDING" would cost nothing and would not create a pointer
with no destination. This is not a misrepresentation — nothing here asserts a verdict that doesn't
exist — but it is not the clean, checkable status mechanism `MANIFEST.json`'s own
`bundle_version_status` field ("this field is written by the build and asserts no verdict")
gets right in the same bundle.

---

## What the refutation could not touch, and therefore what stands

- **Every one of the 23 file hashes in `MANIFEST.json`'s `bundle_files_sha256` verifies against
  the file on disk, with no missing and no untracked file** — checked directly, not sampled.
- **All five `source_runs` hashes verify against the actual `ledger/*.json` files** — checked
  directly.
- **`reference-baseline.json`'s `t_ref_utc` and `ages_computed_at_utc` agree** (both
  `2026-08-15T03:37:40Z`) — the V1 defect this whole arc turns on is genuinely fixed in this
  table.
- **The confirmation-record arithmetic reconciles exactly** against `confirmation-record.json`'s
  own `readings` array: 3/3 confirmed returns, 1/3 confirmed disappearances (genuine transitions),
  5/5 and 1/3 over all readings — matching `README.md` §3's prose to the count.
- **`FIGURE-PROVENANCE.json`'s declared `n_figures` (102) equals the actual length of its
  `figures` array** — no stale count.
- **The pooled rate and gradient figures reproduce**: 438/3576 = 12.2483...% rounds to the
  published 12.25 %; the age-band `n` values sum to 3569, seven short of 3576, matching the "7
  undatable" note in `FIGURES.md` §4 exactly.
- **The dashboard-transcription arithmetic holds**: of the eleven receiver identifiers, exactly
  ten show 0 in the "days available via the research interface" column, matching the prose's "10
  were never once recorded as available."
- **`deliverable/` is untouched by this session.** `git diff` from the start of session 123's own
  commits (`714eebf`) to the tip shows zero changes under `deliverable/`. (An earlier commit,
  predating session 123 and already documented in `ERRATA-122.md` E2, did edit
  `deliverable/tools/presence_check.py` and `selftest_presence_check.py` as the disclosed v0.3.1
  tool repair — not new information, and not chargeable to this session.)
- **No stale `-CORRECTED-` twin exists inside `deliverable-v0.3/`.** The one file matching
  "CORRECTED" (`series/presence-series-corrected.csv`) is the designed raw/overlay distinction
  `LIMITS.md` §8 documents, not a duplicate build artifact.

None of that is in dispute, and it is a genuinely larger and more solid "held" list than the
"failed" charges above are large.

---

# What I tried that FAILED

1. **I tried to catch `deliverable/` being touched by session 123.** It was not — verified by
   `git diff` scoped to this session's own commit range. (A prior session's disclosed tool repair
   did touch two tool files and one build-timestamp line before session 123 opened; that is
   already conceded in `ERRATA-122.md` E2 and is not this session's doing.)
2. **I tried to find a hash in `MANIFEST.json` that does not verify.** None — checked all 23 bundle
   file hashes and all 5 source-run hashes directly against the files on disk.
3. **I tried to find the pooled rate, the gradient ratio, or the confirmation counts wrong.** None
   were. Every arithmetic claim in `README.md` §§2-3 that I recomputed from the primary JSON
   matched to the published precision.
4. **I tried to find a stale `-CORRECTED-` duplicate inside the new bundle**, the exact defect this
   version's whole purpose was to remove. Found none; the one matching filename is a documented,
   deliberate distinction, not a leftover.
5. **I tried to find the WITHHELD-banner and unconfirmed-reading defects as if I had discovered
   them.** I had not: `ERRATA-123.md`, committed before this review began, already names both,
   with the correct diagnosis, and explains in writing why they were not patched in the state
   under review. I report them as blocking anyway, because the artifact in front of me still
   contains them and a receiver without `ERRATA-123.md` in hand would not know — but the credit
   for finding them belongs to the practice, not to this review.

---

# (b) The hostile critique

**So what?** Fourth gauntlet, twenty days from the constitution's own deadline, still nothing
sent. What changed materially tonight is real but small: one directory that used to be two
directories with a human-legible seam is now one directory with a machine-checkable seam, and the
seam the session actually closed (README/LETTER/LIMITS/VERSIONS provenance) is closed well. What
did not change is that the file a receiver would actually read for numbers — `FIGURES.md` — sits
completely outside the new machinery, and the file that touches the receiver's own list —
`receiver-eleven.md` — was carried without a re-read and still says three things that are not true
of where it now lives, two of which the practice caught itself and none of which it fixed in the
state I was handed.

**Is it slop?** No. The engineering is careful and the self-catching is real: `ERRATA-123.md` found
two of my own findings before I arrived, with the harder, more honest framing of each ("the
disease-one-level-up shape ... recurs here") than I would have credited the practice with writing
about itself. The hash discipline, the leaf-diff rebuild audit, and the provenance table are not
decoration — they genuinely close the exact failure class (a number typed by hand) that ended three
prior gauntlets, for the four files they cover. That is a real result and I could not break it.

**Would a critic tear it apart?** Yes, on one seam, and it is the same seam three times over: **the
discipline this session built has a boundary, and the boundary was drawn around the files that were
easy to regenerate, not around the files a receiver would actually use.** `FIGURES.md` is the
single densest table of numbers in the bundle and it is untouched by both new verification tools
this session wrote. `receiver-eleven.md` is the only page that touches the receiver's own list and
it was copied, not re-derived, so nothing checks whether copying it into a new context broke it —
and it did, in a way the practice found and chose not to fix rather than in a way it missed. A
hostile reader does not need to invent a defect here; the pattern that ended sessions 120, 121 and
122 — *a check was run once, the document changed shape, the check was not re-run* — is exactly
what happened to `LIMITS.md`'s numbering and exactly what the two hardcoded cross-references in
`FIGURES.md` and `receiver-eleven.md` now show. The rule this practice wrote for itself after E1
("a self-referential check must be re-run after the last edit") was never extended to "a
cross-reference must be re-checked after the document it points into is restructured." That is the
same lesson, one file over, for the third time.

**What would have made tonight's claim actually true.** Three small things, ranked by how directly
each maps onto a charge above: (1) pass `FIGURES.md` through `figures.py` instead of
`build_deliverable.py`, or at minimum run `audit_prose()` against it and publish the count of
unmatched numbers rather than silently excluding it; (2) add a `check_cross_references()` pass that
resolves every `LIMITS.md §N` string in the bundle against the actual section headings of the
`LIMITS.md` shipped beside it, the same mechanical idea as `audit_prose()` applied to prose
structure instead of prose numbers; (3) treat "carried" as "carried and re-validated," not "carried
and hashed" — a file that makes claims about its own context needs a lightweight assertion that
those claims still hold, not just a sha256 proving the bytes didn't change.

**Is the core claim's honesty itself worth crediting, separately from whether it is true?** Yes.
`INCREMENT-13.md` §4 states plainly, unprompted, that provenance "still cannot tell whether the
sentence around a correctly-fetched figure describes that field correctly" and that "a build that
passes its own audit has not been reviewed by anything." That is exactly the right epistemic
posture, stated before any reviewer asked for it. What it does not do is extend that honesty to the
fact that an entire file was left out of the audit altogether — a gap one order larger than the one
it names, and the one this review found first.

---

*Interlocutor, session 123/124, 2026-08-16. Published unedited. Every command above was run from
`drafts/2026-08-11-the-arm-that-was-missing/`.*
