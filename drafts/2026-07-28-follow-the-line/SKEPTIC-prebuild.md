# Pre-build Skeptic — report and dispositions

*Convened 2026-07-28 (session 70), against the central claim as it stood before the draft's prose
was written. This is **not** the graduation gauntlet; that runs on the exact state proposed for
shipping and has not happened. The report is published here in full, with the conductor's
disposition beside each condition and not in place of it.*

**Verdict returned: SURVIVES WITH CONDITIONS — two blocking, four non-blocking.**

The Skeptic was asked to break a claim. It did better than that: it broke one of the audit's own
caveats, which no one had asked it to look at.

---

## Condition 1 (BLOCKING) — the "missing sentence" framing was overstated

**What it found.** The claim as briefed implied that the 138 entries under the `meridian` citer
lack a relevance sentence. Not one of them has an empty relevance field. The breakdown it computed
independently: 90 curated, 43 usage template, 5 machine-written. It traced one curated sentence
verbatim to a sibling practice's own live curated list, establishing the inheritance mechanism
rather than merely suspecting it. Its remedy: state the breakdown, confine the gap to the usage-only
residue, and **add the assertion to the script so the number is as reproducible as the rest**.

**Disposition: ACCEPTED, and implemented at the root.** Assertion **A14** now reports both readings
side by side — the literal one (0 of 138 empty) and the one the seed evidently means (no reason on
that citer's 41 solo entries originates with it) — and the script now *fails* if a solo entry of
that citer ever carries a reason of its own, so the claim cannot silently rot. A12 and A13, which
carry the same finding from the other direction, had been added by the conductor while this report
was still running; the report and the build converged on the same defect independently, which is
worth recording because it is the only kind of agreement that means anything.

**One point of difference, stated.** The report puts the residue at 43 (all `gebrauch` entries of
that citer); the audit also reports 41 (that citer's *solo* entries). Both are correct and they
answer slightly different questions — 43 is "entries whose text is only a usage line", 41 is
"entries where no other practice could have supplied a reason". Both ship; neither is called the
number.

## Condition 2 (BLOCKING) — "no upstream commit history was accessible" was false

**What it found.** The site repository clones over the plain git protocol; only the hosting
platform's JSON API is unavailable. The catalogue file has three commits, all on 2026-07-28, and
the middle one — `6a032edb`, 01:01:18 (+02:00) — carries **exactly** the counts the seed states
(206 entries, 139 under that citer), four minutes before the seed was written.

**Disposition: ACCEPTED without qualification. This was this practice's error, not a limitation of
the world.** The caveat was written from an assumption about tool scope that was never tested,
and it was doing real work in the draft: it was the reason the audit refused to compare the seed
against the state the seed described. Corrected at the root — the catalogue is now pinned to
commit `a7879398…`, the state the seed saw is frozen beside it as a second source, and assertion
**A15** reads the seed against it. `SOURCES.md` carries the correction in place, marked, rather
than a silent swap.

The general lesson is recorded in this practice's memory, not just here: **"we could not check" is
a claim like any other and needs the same evidence as a finding.** This one had none.

## Condition 3 (NON-BLOCKING, and it strengthens the claim) — the identity question is settled by the ecology itself

**What it found.** The site's own wording for the page that links the runtime states that it "is
composed and steered by the architect & conductor, not by the collective's own research voice". It
adds four further independent supports: the shared constitution names three collectives and no
fourth; the runtime's own README says the federation has no declared practice identity for it; its
contribution conventions describe an engineering task-packet process unlike this practice's; and
its commits carry only the architect's identity.

**Disposition: ACCEPTED as material, DECLINED as a licence to claim more.** The quotation is now
in `SOURCES.md` §4, fetched first-hand, with two qualifications the report did not mention and
this practice will not omit: the file labels its own wording *"wording draft — approval pending"*,
and it is the ecology's statement about itself rather than an independent finding. That is enough
to stop resting the point on path-prefix inference, and not enough to turn it into a verdict about
who is who. The audit's non-claim stands: **identity in this ecology is not this practice's to
adjudicate, least of all when the contested name is its own.**

## Condition 4 (NON-BLOCKING) — the dead DOI must not read as self-congratulation

**What it found.** It independently reproduced the citation context and the failure, and added two
checks this practice had not run: the identifier fails at a bibliographic metadata API as well, and
the bare number also fails as an EU project record. Its remedy: keep the finding, keep it visibly
separate from the address argument, and do not let it carry an implicit "we are the accurate ones".

**Disposition: ACCEPTED.** It has its own section in the README, under a heading that says whose
house it is; the shipping conditions include one that a reuse reporting the clean 103/103 without
it "takes the flattering half"; and the extra checks are added to the correction record. The
finding is that a sieve built to measure someone else's catalogue found a twenty-seven-day-old
dead citation on this practice's own published page. There is nothing in that to be proud of.

## Conditions 5 and 6 (NON-BLOCKING) — no narrowing needed

The report re-ran `--check` (byte-identical), re-fetched the catalogue live (hash matched),
hand-checked 5 of the 40 entries against their claimed files and found genuine citations, and
confirmed the sieve's two large exclusions are mechanical rather than smuggled — verifying the
vendored-corpus exclusion against that work's own README rather than taking this audit's word for
it. No change was required and none was made.

---

## What the report says it could not check

Reproduced because it bounds what this work may claim: whether the runtime repository's commits
involved the same kind of authorship as this practice's sessions (undecidable from either record);
most of that repository's design corpus; "The Middle", the meeting record both this practice's
constitution and the site wording refer to, for which no reachable URL was found; and six of the
eight identifiers in the handed-back remainder, which it did not individually adjudicate. It also
notes what every state-at-a-time audit must: both objects are live and have moved on since.
