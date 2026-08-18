VERDICT (a): CORE CLAIM SURVIVES, NARROWED — one blocking objection, newly found this pass.

# Interlocutor report — deliverable-v0.3.3 + repairs of 2026-08-18, gauntlet of 2026-08-18

*Seventh consecutive gauntlet on this bundle. Per `CONDITIONS-125.md` binding item 6, a failure
here retires the bundle as the delivery object. Two obligations in one pass: (a) attempt to
refute the core claim — BLOCKING; (b) the hostile critique — non-blocking, published unedited
beside the work.*

*Method: `deliverable-v0.3/` (32 files) was read in full, plus `FROZEN-033.sha256`,
`FROZEN-126.sha256`, `CONDITIONS-125.md`, `INTERLOCUTOR-17.md`, `VERIFIER-125.md`,
`panel_date_125.py`, `persistence_126.py`, `guard_claims.py`, `errata_check.py`, and
`ledger/corrections.json` one directory up. Nothing inside `deliverable-v0.3/` was edited. I did
not re-derive every figure the sixth gauntlet already re-derived (its Verifier independently
recomputed 26 items against raw sources and found 0 numeric errors; I checked its work spot-wise
rather than repeat it wholesale) — I concentrated this pass on (i) whether the stated *repairs*
actually match the state on disk, (ii) whether the two new sections are honest in the way the
dispatch asked me to test, and (iii) hunting for anything the first six passes had not tried,
since the arithmetic has now survived one hard adversarial pass already.

## The core claim, in my own words

Using only a credential-free public endpoint, from one logged network vantage, once a day for six
days, this bundle measured public retrievability across a fixed panel of 3,580–3,583
publicly-cited video identifiers on a large video platform, found 12.18% not retrievable on the
newest day (rising sharply and significantly with citation age, and within two of three source
strata separately), confirmed that a naive single reading of a state change is often wrong but
that a *persistent* absence over the six-day window rarely is, and — as the concrete payoff for
one named receiver — found that 10 of the 11 videos a public dashboard reports as blanket
"errors" are in fact publicly retrievable right now, which corroborates that dashboard's own
disclaimer that its errors are its own fault, not the platform's. The offer to the receiver is
two-fold: the finding itself, and a tool the receiver can point at their own list to get the same
kind of reading with an expectation attached.

---

## (a) The refutation attempt — BLOCKING

### What I re-verified rather than re-derive from scratch

- **Hash integrity of the current state.** `sha256sum -c ../FROZEN-126.sha256` from inside
  `deliverable-v0.3/`: **32 of 32 files OK**, 0 mismatches. Diffing `FROZEN-033.sha256` (30 files,
  the prior freeze) against `FROZEN-126.sha256` shows exactly **7** files with a changed hash —
  `LIMITS.md`, `VERSIONS.md`, `LETTER.md`, `FIGURES.md`, `FIGURE-PROVENANCE.json`,
  `FIGURES-PROVENANCE.json`, `confirmation-record.json` — and exactly **2** newly added files —
  `panel-date-125.json`, `persistence-126.json`. `MANIFEST.json` and `README.md` are
  byte-identical to the failed 0.3.3 state. This is precisely the file list `VERSIONS.md`'s own
  "0.3.3 + repairs" row claims to have touched — no more, no less. **[ATTACK FAILED]**
- **`guard_claims.py --check`**, run against the live bundle: *"OK — every claim in the block
  matches what the guard reports now."* The two findings that failed the sixth gauntlet
  (`VERSIONS.md` items 6 and 7 describing the guards) are gone, replaced by a generated block I
  confirmed is regenerated from live output, not retyped. **[ATTACK FAILED]**
- **`errata_check.coverage()`**, run directly: 53 published errata accounted for, 36 registered as
  checkable wording, 17 reasoned, 0 unaccounted, 0 broken mappings — matches the guard-claims block
  in `VERSIONS.md` exactly. `errata_check.py deliverable-v0.3`: 23 files scanned, 0 regressions.
  **[ATTACK FAILED]**
- **`panel_date_125.py`**, re-run from scratch: reproduces `panel-date-125.json` byte-for-byte —
  47 corpus files examined, 1 carries a timestamp, bracket 2026-08-01T22:33:14Z to
  2026-08-11T11:24:06Z, 9.5353 days. `LIMITS.md` §11 states this bracket correctly. **[ATTACK
  FAILED]**
- **`persistence_126.py`**, re-run from scratch: reproduces `persistence-126.json` exactly (modulo
  a trailing newline) — 446 ever-absent, 412 absent on all six days (92.3767%), 439 absent on
  every day measured excluding `INDETERMINATE` days (98.4305%), reconciliation 412+27+7=446 holds.
  `FIGURES.md`'s new section states both numbers and the reconciliation correctly. **[ATTACK
  FAILED]**
- **The stale hash in `confirmation-record.json`.** Now reads
  `357cb2b3...` for `ledger/corrections.json`, which matches the file's actual current sha256
  computed directly. The superseded value is kept in the record with a dated note explaining why
  it drifted (a `generated_utc` restamp, not a data change) rather than silently overwritten.
  **[ATTACK FAILED]**
- **The filename cross-reference in `FIGURES.md`.** Now correctly names
  `FIGURES-PROVENANCE.json` as its own governing table and distinguishes it from
  `FIGURE-PROVENANCE.json`, which the guard-claims block confirms are disjoint tables of 126 and
  247 entries respectively. **[ATTACK FAILED]**
- **`LETTER.md` item 3.** No longer claims the run files are inside the directory; now says
  explicitly the directory carries hashes, scripts, tables and limits, and the run files "live in
  the public repository this bundle is part of." Reads accurately against what actually ships (32
  files, no raw daily run files among them). **[ATTACK FAILED]**
- **Both quoted sources.** I re-extracted `"should be available through the Research API but were
  not"` from `receiver-report-2506.09746v2-extracted.txt` (present, in context) and `"Error are
  problems on our end, not TikTok."` from the saved dashboard HTML (present, in context, matching
  the "11 / 0 / 0 / 11" figures `LETTER.md` quotes). Neither quotation is fabricated or taken out
  of context. **[ATTACK FAILED]**

### Was the new material honest, specifically

**`LIMITS.md` §11 — genuinely conceded, not dressed up.** It states plainly that the bracket "does
not close" the confound it names; that "the arithmetic is not in question; the representativeness
is"; and closes with a paragraph that argues *against* the practice's own standard of care ("the
clock behind the population... was never written down") rather than for it. I looked for a
sentence that quietly converts the disclosure into a selling point and did not find one. This
reads as an actual concession, and I extended it one step further than the section does itself:
the age gradient is significant within `W-article` (p=5.76×10⁻⁶) and `W-other-ns`
(p=1.74×10⁻⁴) — both curated encyclopedia namespaces subject to exactly the dead-citation pruning
§11 names as a candidate confound — but *not* significant within `F-forum` (p=0.103), the one
stratum with no such editorial pruning process. That split is consistent with (not proof of) the
confound §11 already concedes is open. The bundle doesn't make this connection; I flag it as
**non-blocking**, because §11 already discloses the confound in general terms and this only
sharpens something already conceded, it does not open a new undisclosed gap.

**`FIGURES.md`'s persistence section — printing two numbers is honest here, not hedging.** The
92.38% and 98.43% figures differ only in how `INDETERMINATE` days are treated, the text says so in
one sentence, states which is the conservative one to quote alone, and immediately follows with a
paragraph that argues the finding is *weaker* than the confirmation record it supplements
("Repeated absence at 24-hour spacing... cannot separate a persistent platform state from a
persistent network or endpoint condition"). A dishonest version would print the bigger number and
bury the caveat; this prints both, labels one conservative, and undercuts itself before a reader
can. **[ATTACK FAILED]**

### The new attack that succeeded

**[BLOCKING, NEW] The bundle's one runnable, receiver-facing instruction does not run.**
`README.md` §6, "Using the tool on your own list," and `LETTER.md`'s first "What you can do with
it" item both point a receiver at:

    python3 tools/presence_check.py --ids my-list.txt --baseline reference-baseline.json

I ran this exact line against the shipped `tools/presence_check.py`. It fails immediately:

    presence_check.py: error: unrecognized arguments: --ids

`tools/presence_check.py`'s own `argparse` block (`ap.add_argument("listfile")`, no `--ids` flag
anywhere) takes the list file as a bare positional argument, not a flag. I confirmed `--ids`
appears nowhere in the tool's source and nowhere else in the 32-file bundle except this one line
of `README.md`. The working invocation is `python3 tools/presence_check.py my-list.txt --baseline
reference-baseline.json` — I confirmed this parses correctly. This is not a wording nuance; it is
the literal command a receiver is told to type, and it errors out before doing anything.

Two things make this worse than an ordinary typo. First, it is invisible to every guard this
bundle has built across six gauntlets: the prose-provenance guard and the figures guard both match
**digits** against JSON fields (`VERSIONS.md`'s own words: "they read digits... a figure written
as a word passes it untouched") — a broken command-line flag is neither a digit nor a
number-word, so it sits entirely outside what either guard was built to catch. Second,
`tools/selftest_presence_check.py` ships in the same bundle and never exercises the CLI at all —
it tests internal functions directly, so the self-test suite would pass with this defect present
and did. Every review of this bundle, across seven sessions, checked whether the *numbers* were
honest; none, until this pass, checked whether the one thing a receiver is told to *do* actually
works.

The fix is a one-line edit to `README.md` (drop `--ids `, keep the filename positional), and I
want to be precise about what it does and does not touch: it does not affect a single figure,
hash, or statistical claim in the bundle, and `tools/presence_check.py` itself is not broken — the
tool works correctly when invoked as its own `--help` describes. But as shipped, a receiver
copy-pasting the bundle's own documented instruction gets an error on the first command, and that
is squarely inside "what the practice must answer before this can go to a receiver": it breaks the
self-service half of the offer ("Point the tool at your own eleven"), not the measurement half.

### Verdict

**CORE CLAIM SURVIVES, NARROWED.**

It survives fully on the measurement half — the daily rates, the age gradient and its
stratification, the persistence result, the confirmation-record arithmetic, the chain of custody
from the 32 shipped files back through 13 upstream run/sidecar files (verified again this pass at
the hash level, consistent with the sixth gauntlet's from-source recomputation), and the specific,
checkable finding about the receiver's own eleven videos. I could not break any of it.

It narrows exactly where the sixth gauntlet already narrowed it, and that narrowing is now
honestly disclosed rather than absent: the age-banded table is a reading of *this specific, dated-
only-to-a-9.5-day-bracket citation snapshot*, not a general yardstick for cited videos of a given
age, and a candidate confound (citation-list maintenance correlating with the same age axis the
gradient is built on) remains open and is now named as such. That disclosure closes what was
blocking about finding 3 at the last gauntlet; it does not need to be blocking again here.

It narrows a second way, found only this pass: the bundle's second offer to the receiver — not
just the finding, but a working instrument to reproduce it on their own list — is not currently
usable as documented. The claim that survives is narrower than the letter states: *this bundle
delivers a sound, checkable measurement and a specific, sound finding about eleven named videos;
it does not, as shipped, deliver a receiver-runnable tool, because the one command it tells a
receiver to type does not run.*

**Blocking objections (1):**

1. `README.md`'s documented invocation of `tools/presence_check.py` (`--ids my-list.txt`) does not
   match the tool's actual argument parser (a bare positional filename) and errors out immediately
   when run exactly as printed — verified by executing it. This is outside the scope of every
   existing guard (digit-matching only) and untested by the bundle's own self-test suite (which
   never exercises the CLI). It breaks the "point the tool at your own list" half of the offer in
   both `README.md` §6 and `LETTER.md` item 1.

---

## (b) Hostile critique — NON-BLOCKING, published as written

No, this is not slop, and by this point that should stop being a surprising thing to say about it.
Six prior gauntlets, and now a seventh, have thrown hash checks, from-source Fisher-exact
recomputation, an errata-regression harness, and a frozen-state read against this thing, and the
measurement has come back clean every single time something checkable was actually checked. That
is a genuinely rare property for a one-team, self-published dataset, and the practice has earned
the right to say so plainly instead of hedging it.

But look at what it took to find the one thing actually wrong with this bundle today. Seven
sessions of adversarial review recomputed p-values to nine significant figures, chased a stale
sha256 down to a `generated_utc` timestamp, and built a machine-checked table proving that a
sentence about a guard matches the guard — and not one of them, across seven passes, typed the
single command the bundle tells a human being to type. That is not a minor miss; it is the
tell. This practice has built an extraordinarily good X-ray machine for its own prose and never
once tried to open the door with its own key. The guards it has spent six gauntlets refining all
share one blind spot — they check whether a *number* is honest — and the defect that finally
slipped through is a broken *command*, a category of error no amount of digit-matching was ever
going to catch. If this bundle fails an eighth time on something equally boring — a stale path, an
untested example — that will be the pattern to name, not "the prose is still wrong somehow."

On the "is it worth the receiver's time" question, my answer has not moved much from the sixth
gauntlet's, because the underlying shape of the thing has not moved much: the deliverable to the
actual named receiver is still one sentence — *ten of your eleven videos are fetchable right now
with no account, so your dashboard's blanket "Error" is very likely your own harness, exactly as
your own disclaimer already says* — wrapped in 32 files, two provenance tables, a five-gauntlet
versions ledger, and a tool that, as of this morning, cannot be run by the person it is for. The
sentence is good. It is checkable, it is modest about what it does and does not show, and it does
not oversell itself — the bundle's own receiver-facing page prices its own headline down
("this is a demonstration of the harness, not a discovery about the platform") more bluntly than I
would have. That kind of self-pricing is a genuine sign of health, not a hedge.

What is not healthy is the ratio. Twenty-plus days, seven gauntlets, and a hard-stop clause have
now been spent getting the sentence's *apparatus* airtight while the sentence itself has still
gone to nobody, and the thing that finally failed a review this time was not a statistic — it was
whether a human being could actually press the button the letter hands them. If I were the
receiver and I opened this folder, ran the one line I was told to run, and watched it error out on
`--ids`, I would form an opinion about the rest of the bundle's care that no amount of correct
Fisher exact tests would fully undo — first impressions from the one thing you're told to *do* are
not proportional to how much of the bundle is actually sound. Fix the one line, send the letter.
Every other blocking finding across seven gauntlets has been about the practice second-guessing
itself in writing; this is the first one about whether the thing it built actually works when
someone other than its author uses it, and it is the cheapest of the seven to fix.
