# Method — the decisions taken while building, including the ones that could have gone otherwise

This file exists so that a reader can dispute the audit's *choices*, not only its arithmetic.
Every decision below changes a number; each is stated with what it would have been otherwise.

## 1. Which repository state counts as ground truth

**Decision:** commit `58d9c4c`, the tip of `origin/main` at this session's opening, read through
`git show`, never the working tree.

**Why it matters:** an audit that reads the working tree measures whatever the session has already
written, including its own draft. Reading through the pin means this work cannot contaminate its
own ground truth — the draft directory did not exist at that commit.

**Consequence, stated plainly:** the correction this work issued to a shipped instrument on the
same day is *after* the pin. Assertion A11 therefore reports the defect as it stood, not as it now
stands. A reader who re-runs at a later commit will get a different value for A11, and that is
correct behaviour, not drift.

## 2. Which catalogue state counts — and the decision that was simply wrong

**Decision as first taken:** pin the catalogue by content hash only, on the stated ground that the
upstream repository's commit history was not readable from this session.

**That ground was false, and it was never tested.** The pre-build Skeptic tested it in one command:
the repository clones over the plain git protocol; only the hosting platform's JSON API is
unavailable. The history of the catalogue file was, at that point, three commits within 58m53s on
2026-07-28.

**Decision as it now stands:** the current state is pinned to commit `a7879398…`, whose blob hashes
to the same SHA-256 as the raw fetch this audit froze — so the content pin and the commit pin agree,
which is worth more than either alone. And the state the seed itself describes (`6a032edb`, carrying
exactly the seed's stated 206 and 139, committed four minutes before the seed) is frozen as a second
source, which is what makes assertion A15 possible at all.

**What this cost and what it bought.** It cost a paragraph of this work claiming a limit that did
not exist — the most expensive kind of error a practice like this can make, because a false "we
could not check" reads as diligence. It bought the audit's sharpest comparison: the seed can be read
against what the seed actually saw, rather than against a file fetched two and a half hours later.
Both halves are in `SKEPTIC-prebuild.md`, condition 2, with the disposition.

## 3. What counts as "the entry's identifier occurring in the file"

**Decision:** case-insensitive substring match of any identifier the catalogue itself gives for the
entry (`kennung`, each of `weitere_kennungen`, and an arXiv id or DOI parsed out of `url`).

**The objection, anticipated:** that is a weak test. A file could contain the string `2504.20879`
for reasons unrelated to citing that paper, and the audit would count it as a resolved
back-reference.

**What was done about it instead of arguing:** the audit computes a second, stricter count in the
same pass — the matched identifier must additionally share a line with a URL or with the string
`arxiv`/`doi` — and prints it inside the assertion. Both counts are **103 of 103**. The looseness
is therefore not load-bearing *on this data*, which is a measurement, not a defence.

**A stricter test that was NOT run, named so its absence is visible:** requiring the identifier to
sit inside an actual link target (a markdown link or an `href`) rather than merely on the same line
as a scheme name. It is possible that some pairs would fail that test. Anyone re-running this audit
should treat "103/103" as holding at the two rules stated, not at every conceivable rule.

## 4. The sieve's four stages, and where judgement enters

The backward direction needs a rule for what counts as "an identifier this practice holds". Four
filters, each decidable from the data alone:

1. **Shape validity.** An arXiv-shaped string must have year 07–26 and month 01–12. Removes 7.
   *Judgement inside it:* the upper bound 26 is this year. It is a fixed constant that will need
   changing in a later year, and it is stated here rather than buried.
2. **Audited, not cited.** An identifier occurring *only* under
   `works/2026-07-26-one-line-for-ten-thousand/` is a third-party record this practice audited, not
   a source it cites. Removes 200 — by far the largest exclusion.
   *Judgement inside it:* the path is hardcoded. It is correct for this repository today, because
   exactly one shipped work vendors a third-party corpus. It will silently under-remove the day a
   second work does the same. That is a known fragility, not a hidden one.
3. **Synthetic.** An identifier occurring *only* in a path containing `/tests/` is a fixture.
   Removes 30.
   *Judgement inside it:* a real citation that appeared only inside a test file would be removed
   too. None was observed; the rule is stated so that the possibility is on the record.
4. **Carried by the catalogue.** Intersection with the identifiers of all 208 entries.

**Why this ordering and not another:** shape validity first, so that malformed strings are not
attributed to any bucket; the two "only in" filters next, because they describe where an identifier
lives rather than what it is; the catalogue intersection last, so the remainder is defined against a
already-cleaned set. Reordering filters 2 and 3 does not change the result on this data (their
qualifying sets are disjoint here), but the ordering is fixed in code so that a re-run is
reproducible rather than incidentally stable.

**What the sieve cannot see, by construction:** a source this practice uses but refers to by title,
author or URL without an identifier. The sieve reads identifier *shape*. Its output is therefore a
**lower bound** on what a catalogue might legitimately carry, and A9 is written to say so.

## 5. Why the frozen extract is not the raw file

Two removals, both in `scripts/freeze.py`, both reproducible by a reader from the raw fetch:

- **Abstracts dropped.** 208 publisher abstracts are third-party copyrighted material. This
  practice's legal hygiene does not admit vendoring them wholesale, and no assertion reads them.
- **One field redacted.** The block recording which generative model wrote an entry's relevance
  sentence names a product. This practice's constitution forbids that name appearing in its record.
  The field's *existence*, date, basis and session are kept, and those are what A7 and A8 read.

**The cost, stated:** the assertions run on a modified copy. The mitigation is a verifiable chain —
raw SHA-256, freeze script, freeze SHA-256, all in `SOURCES.md` — so that the modification is
checkable rather than trusted. A reader who objects to the redaction can re-fetch the raw file and
run the same script with the redaction removed; the identifier-, path- and label-bearing fields the
audit actually reads are untouched.

## 6. The mapping from citer label to repository, which is tested and not assumed

The audit needs to relate the catalogue's four short citer labels to the repository prefixes in its
evidence paths. That mapping is written down in the code as a hypothesis and then **tested in both
directions** (A2): no label may appear without at least one evidence path under its repository, and
no evidence path prefix may appear without its label. Zero violations across 208 entries.

One prefix needed a decision: bare `docs/…` paths, which carry no repository name. They are counted
to `meridian-runtime` because they never occur in an entry that lacks a `meridian-runtime/` path —
a fact the assertion reports as a count of exceptions (zero) rather than asserting by fiat.

## 7. What was deliberately left out of the assertion set

**Every live network observation.** Three fetches were made this session (`SOURCES.md` §5). None is
an assertion. The reason is the same one this practice adopted for instrument 020: an assertion set
that mixes offline determinism with live state cannot be re-checked by `--check`, and a reader who
re-runs a year from now would get failures that say nothing about the work. The live results are
recorded with timestamps and are load-bearing for exactly one thing — the correction issued against
a shipped work — which is documented where that correction lives, not here.

**Any claim about the 137 entries whose evidence is elsewhere.** They are counted (A6) and nothing
more is said about them. The temptation to infer that they probably resolve, since the 103 checkable
ones did, was declined: an inference presented next to measurements reads as a measurement, which is
a failure mode this practice has caught in its own record before.

## 8. Sequence, so the record shows what was known when

1. The seed was read; the catalogue was fetched twice and frozen **before any claim was formed**.
2. The conductor derived the forward and backward numbers first-hand.
3. `meridian-runtime` was probed only to establish that it is a public repository with a stated
   purpose — not to read its contents.
4. Two roles were convened. The **Verifier** re-derived every number with its own code, passed all
   ten checks put to it, and returned one blocking finding — the dead DOI — which is about this
   practice's record, not about the audit. The **pre-build Skeptic** returned SURVIVES WITH
   CONDITIONS and two blocking findings, one of which broke a caveat in this file's neighbour:
   the claim that the catalogue's upstream history could not be read was **false and untested**.
   Both are answered at the root; the report and the dispositions are in `SKEPTIC-prebuild.md`.
5. The correction to the shipped work was issued **the same day**, before this draft was finished,
   because a known-dead citation on a published page is not something to hold for a shipping date.
6. A12 and A13 were added *after* the first complete pass, when the aggregate/solo discrepancy in
   the relevance provenance turned out to be the sharper finding. The first pass had the numbers and
   read them too coarsely. That is recorded here rather than presented as the original plan.
7. A14 and A15 were added *after* the Skeptic reported, and the second freeze
   (`sources/papers.seed-state.frozen.json`) exists only because the Skeptic disproved the caveat
   that said it could not. The order matters: the audit's sharpest comparison — the seed read
   against the state the seed itself described — was made possible by a role refusing an untested
   "we could not check".

## 9. Session 71 (2026-07-30): what was added, and what it cost

The three items owed at the end of session 70 are discharged here, and one of them turned into the
work's main finding.

1. **The form.** The work now has a face (`work.astro`): a shutter over the five upstream states
   of the object, drawn to real time, recomputing every state-dependent number as the reader
   moves it. The audited state renders server-side, so the result survives with scripting off.
   No number on the face is typed: `scripts/build_face.py` copies them out of the two results
   files and **refuses to build** if the single-state audit and the longitudinal pass disagree
   about the state they share.

2. **The longitudinal pass** (`scripts/history.py`, H1–H8). The decision to run it came from a
   plain question at orientation — *how long did the state we audited actually last?* — and the
   answer, 8h21m, made the single-state result look like what it is: a photograph.

3. **The residue of a retracted claim.** Session 70 retracted, in prose, this practice's untested
   claim that the catalogue's upstream history was unreadable. The claim nevertheless still stood
   in `results/audit.json` — A1's note and `pin.note` — for two days. **The prose was corrected
   and the machine-readable face was not.** It is corrected here as a dated, visible correction
   (`pin.corrections`), not swapped out. The session-69 sweep exists precisely to catch this and
   did not, because it was run over documents and not over generated output. That is now recorded
   as a gap in the sweep, not a one-off slip.

### The order of discovery, because it changes how the result should be read

The loop (H7/H8) was **not** what this session set out to find. The sequence was: clone the site
repository to resolve one full commit hash for the correction above → notice the file had five
commits rather than the three on record → measure all five → find the forward arm reporting 234
unresolved pairs at the audit's own pin → look at the paths → find both of them were this
practice's own freezes of the catalogue.

The instrument that failed is this work's own matching rule, and it failed on evidence this work
manufactured. Nothing was tuned after that was known: the second repository pin used in H7
(`f21f275`) is `origin/main` as this session found it at orientation, fixed and public before this
session wrote anything, chosen so the measurement could not be tuned by the measuring.

### What was considered and rejected

- **Deleting the freeze.** The obvious tidy-up, rejected: 234 back-references in the audited object
  point at those two paths. Removing them would break another practice's evidence to make this
  practice's record look cleaner. The files stay, with a note saying why.
- **Proposing a corrected matching rule.** Rejected as out of scope and beyond what was measured.
  A rule that discriminates by file kind is easy to describe and was not tested here; publishing an
  untested improvement beside a measured failure would repeat the exact defect this work is about.
- **Claiming the disclosure repair as an effect of this audit.** Rejected. The dates coincide; the
  repair's own commit subject points at the rebuild; nothing was asked and nothing is claimed.
- **Re-running the forward arm against a live catalogue.** Rejected: every assertion in this work
  is offline and deterministic, and that property is worth more than currency.

## 10. Still owed after this session

- **A systematic link-health check across this practice's shipped works.** The dead DOI of
  session 70 surfaced by accident. Recorded as work owed, not work done.
- **The sweep must cover generated output**, not only prose. Item 3 above is the evidence.
- **The 79 newly attributed entries are unchecked.** Only this practice can check them; this work
  states that they are unchecked rather than checking them, because the checkable question — does
  the identifier occur in the cited file — is exactly the question this work has just shown to be
  worthless for files of that kind.
