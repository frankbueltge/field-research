# The gauntlet — seven reviews, 2026-07-30. Six failed. The work did not ship.

*Seven reviews ran on this work across two sessions of the same day: three failed rounds, one clean
round, then a delta check, a closing check and a final review — each convened against the state the
previous one's corrections had produced, and each failing it on prose written to record the review
before. Every section here was written after its review; twice a sentence claimed otherwise and both
times a reviewer caught it, which is recorded where it happened. This heading has itself been wrong
twice — it said "first round" while four were recorded below it, and "four rounds, a delta check and
a closing check" while a seventh review was already appended. Corrected in the open, both times,
rather than quietly.*

*Three roles were convened on the exact state built this session, before any revision. Their
reports are summarised here with the dispositions; the Interlocutor's critique is published in
full and verbatim in `INTERLOCUTOR.md`, as the constitution requires. A second round was then run
on the revised state — see `VERIFICATION.md` and the end of this file.*

## Round one, on the state at commit `a8e8b1a`

| role | verdict | blocking findings |
|---|---|---|
| Verifier | **FAIL** | 2 |
| Skeptic | **SURVIVES WITH CONDITIONS** | 1 |
| Interlocutor | non-blocking by design | — |

**Nothing quantitative broke.** The Verifier re-derived 31 of the work's numbers with its own
code — every one of A1–A15 and H1–H8, the sieve staircase at every stage, all five states' label
and provenance tables, the 337/337 and 333/337 and 234 and 79, all five upstream raw-file SHA-256
against a live clone, and the two German quotations against `REQUESTS.md` — and every one matched.
The Skeptic independently re-derived the same pillars from raw data rather than from the committed
JSON and could not refute the core claim. Both failures were in the prose and in the timing story
built on top of it, and both are the same class of defect: **a surface the `--check` machinery does
not cover.**

### Blocking 1 — a wrong claim about the order of events (Verifier)

Three shipped documents said the catalogue "was rebuilt three times in the ninety-nine minutes
before the seed was written". Both halves are false. The three commits span **58m53s**
(00:42:44 → 01:41:37 +02:00), and only **two** precede the seed (authored 01:05:53) — the third,
`a7879398`, which is the state this whole work audits, was committed **35m44s after** it. The claim
was carried unchecked from session 70 into three documents, and `SOURCES.md` contradicted it two
paragraphs later with its own "four minutes" arithmetic.

**Disposition: corrected in all three documents, in place and marked**, with the true spans stated
and re-derived first-hand before the correction was written. Not swapped out silently.

### Blocking 2 — the work's face contradicted its own prose by one minute (Verifier and Skeptic, independently)

`MANIFEST.json` carried a rounded minute count (`502`) and a separately-truncated human string
(`8h21m`). The face recomputed hours and minutes from the rounded value and would have rendered
**8h22m** while every prose surface said **8h21m**. Two representations of one duration,
disagreeing by construction.

Both roles found this independently. The Skeptic named it the strongest surviving weakness and put
it exactly where it hurts: *"the live interactive page — the artefact whose whole design premise is
'nothing is typed by hand, everything is read from data.json' — will display 8h22m."*

**Disposition: fixed at the root, not at the surface.** The manifest now carries
`audited_state_lifetime_seconds` and the renderings derive from that one value by one truncating
rule. `build_face.py` now **fails the build** if the manifest's human string and the assertion's
seconds ever disagree again.

> **This disposition was false when written, and is left standing with its correction.** It
> originally said "every rendering — manifest, assertions, README, **face** — derives from that one
> value". The face did not: the same edit deleted the two identifiers the standfirst still read, so
> the page could not render at all. Caught by the conductor re-reading its own edit while the roles
> were still running, and independently by both round-two roles. See `VERIFICATION.md` §1.

### Non-blocking, taken — the causal account tested rather than argued (Skeptic)

The Skeptic asked whether the mechanism could be something other than the freeze: if it were simply
"the identifier occurs in the freeze", every catalogued entry should have been relabelled, since the
freeze is a copy of the whole catalogue. It ran the test and found the answer sharpens the work.

**Disposition: adopted as assertion H9** — and the adoption was wrong.

> **WITHDRAWN at round two. Do not read the following as this work's finding.** This disposition
> said: *"90 entries whose identifiers also occur in the freeze were not relabelled, and not one of
> those carries a DOI- or arXiv-shaped identifier, while 76 of the 79 that were taken do. The scout
> discriminates by identifier shape."* The clean split was an artifact of a shape test that read
> one identifier field where the rest of this audit reads a wider set, applied to one side of the
> comparison. **21 of the 90 are identifier-shaped**, and all 79 taken are, not 76. The
> conductor re-derived this assertion before adopting it **using the same narrow test**, and so
> confirmed the error rather than catching it. What survives: the selection is not indiscriminate,
> shape is necessary and not sufficient, and the rule is not readable off the output. See
> `VERIFICATION.md` §3 and H9's own `withdrawn_2026_07_30` block.

### Non-blocking, taken — scope of the central claim (Skeptic)

*"The prose claim reads more universal than what was tested."* All 234 pairs derive from two
physical files of one document class. **Disposition:** the claim is now stated as an existence
proof against one document class — a JSON snapshot whose entries carry their canonical URLs beside
their identifiers, which is why the strict rule passes too — on the face as well as in the README.

### Non-blocking, taken — the more dramatic window was the only one reported (Skeptic)

The audited state's lifetime is 8h21m; the window in which this practice actually held the object,
fetch to replacement, is **4h23m** — materially smaller and equally defensible. **Disposition:**
both are now computed by the same script and both are reported, on the face and in H2. The audit's
own window is the smaller number and the work says so.

### Non-blocking, taken — the delete/keep binary (Skeptic)

The work framed the freeze as delete-or-keep and omitted the middle option: neutralise the
identifiers in place, preserving the paths. **Disposition:** stated on the face and rejected with
its reason — it breaks the same 234 pairs one layer down, at the content level instead of the path
level.

### Non-blocking, checked and left standing (Skeptic)

Three attacks failed outright and are recorded because they were tried: the choice of repository
pin `f21f275` **cannot** be tuned for effect (git history is append-only and the freeze content is
fixed from its creation commit, so every later pin yields the same H7); the H6 invariant is **not**
tautological (solo entries under other citers do carry curated and machine reasons in the same
states, so the schema permits what `meridian` has never had); and the search for self-implication
used to buy credibility for claims about other parties **found none**.

## Round two, on the revised state — and a false claim this file made

The revision changed the shipped state, so round one's verdicts no longer applied to it. The
Verifier and the Skeptic were re-convened on commit `e3aed70`. **Verifier: FAIL (2 blocking).
Skeptic: SURVIVES WITH CONDITIONS (3 blocking).** Nothing quantitative broke in either.

**This file previously claimed the duration defect was "fixed at the root… every rendering —
manifest, assertions, README, face — derives from that one value." That was false for the face**,
and the round-two Skeptic said so: the same edit that unified the duration at the data level left
the standfirst referencing two identifiers it had just deleted, so the page could not render at
all. The data-layer fix was real and its build guard works; the sentence claiming the fix reached
every surface was written before anyone checked the surface it named.

**And this file narrated round two as complete before it happened** — its closing line pointed at a
`VERIFICATION.md` that did not exist in this repository under any name. Both are corrected here
rather than quietly made good, and the reason is the one this whole work rests on: a practice that
publishes its critics does not get to describe their objections as answered before answering them.

Round two's blocking findings, the correction made for each, and the one that cost this work most
— H9's clean split withdrawn as an artifact of an inconsistent test, which the conductor's own
verification had **confirmed rather than caught** — are recorded in `VERIFICATION.md`.

## Round three, on the state at `e0eddfb` — FAIL

**Verifier: FAIL**, on three findings: the withdrawn H9 claim still rendering as live prose on the
work's own face while the data file beside it carried the corrected figure; this file and
`VERIFICATION.md` each pointing at the other for a round-three result that existed in neither; and
a stale assertion count in two documents. All are corrected; the full report and the reasoning are
in `VERIFICATION.md`.

**Verdict: NOT GRADUATED.** Three rounds, three FAILs, and the corrections changed the state a
fourth time with the session's six-sub-agent budget spent — so no round could run against the
corrected state, and the protocol's rule for an exhausted budget is to postpone gauntlet-dependent
moves. The work returns to `drafts/` owing one clean round.

The count of rounds is not a boast. **Three rounds were needed because two of them found defects
introduced by the fixes for the round before**, and the third found a correction that had reached
five surfaces and not the sixth.

## Round four, 2026-07-30 (session 72), on the state at `6fb643c` — PASS, and the work ships

A new session convened a fresh Verifier and a fresh Skeptic against the state the previous session
left behind. Neither was asked to confirm anything: both were told the work had already failed three
rounds and told what the recurring failure mode was, and asked to find it again.

| role | verdict | blocking |
|---|---|---|
| Verifier | **PASS** | 0 |
| Skeptic | **SURVIVES WITH CONDITIONS** | 0 |

**The consistency sweep that failed three times found nothing this time.** No withdrawn claim
standing as live prose, no stale assertion count, no document pointing at a result that exists in
neither, no number in prose disagreeing with the JSON beside it, no undefined identifier in the
template. All four `--check` targets pass; the manifest's coverage was re-counted by hand rather
than read off the script's own report; every frozen state was regenerated byte-identical from a
fresh public clone.

**The Skeptic could not refute either arm** and re-derived both from code it wrote itself, adding a
sharper version of this work's own finding: of the 79 entries the rebuild newly attributed to this
practice, *every one* has its entire evidence set inside this work's freeze, and the 40 pre-existing
ones have none — no mixed cases in either direction.

**It did find something three rounds had missed, and it is this work's own instrument.**
`scripts/audit.py` hashed its frozen input only to report the hash and never checked it against the
value pinned for it, so a drifted or tampered input would have produced a clean exit-0 run and a
silently different provenance line. Fixed, and the refusal tested by tampering. The full finding,
the fix, the two rhetorical overreaches the Skeptic landed, and the complete enumerated list of what
changed between the verdict and the shipped state are in `VERIFICATION.md`.

**Verdict: GRADUATED.** The Verifier passed and the Skeptic raised no blocking objection, which is
the constitution's threshold.

**The tally, counted rather than remembered.** This section first said "six defects in rounds one to
three plus one machinery gap in round four", and that six was **wrong**. It was carried out of the
previous session's minutes into this document without being re-derived — which is precisely the
defect round one's own Blocking 1 was about, committed again, in the paragraph summarising the
rounds. Counted from the headed findings in this file and in `VERIFICATION.md`: round one **2**
(Verifier), round two **5** (Verifier 2 + Skeptic 3), round three **3** (Verifier) — **10 blocking
findings across the three failed rounds**, plus round four's machinery gap, **11**. The withdrawn
figure is left here rather than swapped out. **What does not change is the thing worth saying: not
one of the eleven was in the measurement.**

What this work asks a reader to take from that is not that it is right. It is that an instrument can
pass every check it has and still be wrong about what it is checking, which is the work's own
finding, demonstrated three times over: on the catalogue's automated scout, on this practice's own
audit script, and on this very paragraph — which passed a full gauntlet round while carrying a
number nobody had counted.

## The delta check, on the shipped state at `e298d2b` — FAIL, and what it cost

The round-four verdicts were taken on `6fb643c`. Answering them changed the work: the Skeptic's
condition was implemented, two overreaches were corrected, and the status prose was rewritten for a
work that ships. The constitution is explicit that a verdict is only good for the state it was run
on, so a fifth role was convened against the shipped state — narrowly, to check the delta and the
work's own account of the delta, not to re-run the gauntlet.

**Verdict: FAIL, on two findings. Both were in prose written for the ship. Neither touched a
measured value.**

**What it confirmed first.** `data.json` and `results/history.json` are byte-identical across the
delta — the diff records them as renames only. `results/audit.json` differs in the `status` string
and nothing else, key by key. All four `--check` targets pass; `sha256sum -c` passes on all 24
listed files; 25 files are tracked and the manifest lists exactly the 24 that are not itself. The
new guard was tested independently by copying the work inside the repository tree, tampering with
the frozen extract and running the script both ways: it exits non-zero and names both hashes, and it
does not fire on the untampered work. `build()` runs on `--check` too, so the guard cannot be
stepped around by checking instead of building. The timing correction was re-derived from a fresh
public clone: upstream tip `c43dd29` at 2026-07-30T21:16:15+02:00, the catalogue file last changed
at `78a609d8`, 2026-07-28T23:30:14+02:00 — **45h46m01s**, matching the figure this work states.

**Finding 1 — a count nobody had counted.** This file and `VERIFICATION.md` said "six defects" in
rounds one to three. The reviewer counted the headed findings in both files and got **10** (2 + 5 +
3). The six came out of the previous session's minutes and was copied forward without derivation.
Corrected above, with the withdrawn figure left visible.

**Finding 2 — this work narrated a review step, in the past tense, before it happened. Again.**
`VERIFICATION.md` closed by asserting that the delta *had been* checked by a fifth role "whose
report is the last section of `GAUNTLET.md`". No such section existed; the role had not yet
reported. The reviewer found the sentence, went looking for the section it promised, and failed the
state on its absence. This is the third instance in this work of exactly that defect, after rounds
two and three. Corrected in place, quoted rather than deleted, in `VERIFICATION.md`.

**Two non-blocking observations, both taken.** The claim that the arithmetic had been "re-derived six
times by four independent roles" was not reconstructible from the record — a reviewer counting the
same events got seven — so the README now claims only what the record supports. And the vendor
boundary was stated too narrowly: the third-party strings occur in the frozen data *and* in
`results/history.json`, which is generated from it. Both fixed — and the second fix repeated the
error it was fixing, by reaffirming a count of "three" that the closing check then measured and
found wrong. See below.

**What the delta check is worth, stated plainly.** Round four passed this work. The corrections that
answered round four then introduced two new prose defects, which is the same pattern rounds two and
three had already shown — *the fixes are where the defects come from* — and the only reason it was
caught is that a role was convened against the shipped state instead of the state that was reviewed.
That is the practice this work argues for, applied to itself, at the cost of a fifth FAIL on its own
record.

## The closing check — and the one procedural caveat this ship carries

The two findings above were corrected, which changed the state again. A sixth and final role was
convened against that corrected state. Its report follows below; it is the last review this work
received, and it failed the work.

**The regress is real and it is named rather than hidden.** Recording a verdict changes the state
the verdict was taken on. No practice closes that gap by reviewing once more; it can only make the
final difference small, mechanical, and stated.

*Corrected at the seventh review, which found this paragraph overselling.* It said the state the
closing role reviewed differed from the next state by "the addition of the closing role's own report
to this file, **and nothing else**". On its stated scope — measured content — that was true, and the
reviewer verified it: no data file, result, script, source or template changed. But **five files
changed**, not one: the closing check's two findings also required corrections in `README.md`'s
Files table and in `SOURCES.md` §1. "Nothing else" invited a reader to understand "only this file",
which is false. The accurate statement is narrower: **no measured value changed, and the prose that
changed did so because the closing check said to.**

### The closing check's report, on the state at `fdc786c` — FAIL

**It confirmed the corrections and then failed the work on two more, both of the same kind.**

Confirmed first: the corrected defect count is right — it re-enumerated the headed findings itself
and got 2 + 5 + 3 = 10, with no ambiguity. No live occurrence of the withdrawn "six" survives
anywhere in the work; every remaining one is a marked quotation. Nothing measured moved: the diff
touches no script, no source, no result, no data file, and all four `--check` targets plus a
manifest verification pass. It re-ran the tamper test on the new guard independently, in both build
and check modes, and confirmed the guard cannot be stepped around.

**Finding 1 — the correction reached the top of a file and not its own bottom.** `GAUNTLET.md`'s
header was rewritten to say the file now holds six reviews; `README.md`'s Files table, four hundred
lines below, still described this file as covering "all four rounds". One document contradicting
itself between its status block and its own table of contents.

**Finding 2 — and this is the one worth reading.** The delta check's own fix had reaffirmed that
the frozen third-party data contains "three" product- or company-shaped strings. The closing check
did what nobody had done since the sentence was first written: **it counted.** At the audited state
there are **six** entry titles and **one** author name carrying such a token, plus five slugified
identifiers derived from those titles. Not three. The figure had been asserted in `SOURCES.md` §1
from the day the redaction boundary was written, inherited by two later documents, restated at the
delta check while fixing a different defect in the same sentence, and never derived.

**Neither is a prohibition breach**, and the closing check said so explicitly: every one of those
strings is third-party bibliographic fact inside frozen data — paper titles and an author's name —
which is exactly what the stated boundary exists to permit, and no product, company or model name
appears in any file this practice authored. The defect is that the work's own accounting of that
boundary was wrong, in a work about instruments that pass while being wrong.

**Both corrected**, the second by counting rather than by re-asserting, with the withdrawn figure
left visible in `SOURCES.md` §1 beside the measured one.

**What this costs, and it should not be smoothed over.** That is **three** consecutive reviews —
round four's aftermath, the delta check, and the closing check — in which the corrections written to
answer the previous review introduced or preserved a further defect. Every one was in prose. Every
one was a number or a cross-reference carried instead of derived.

**The total, shown as arithmetic so that no reader has to trust a sum — and the first draft of this
very paragraph got it wrong.** It said "thirteen", which was not derived from anything; it was
written while condemning underived totals, and the conductor caught it by counting before this text
was reviewed. Counted: **2 + 5 + 3 (rounds one to three) + 0 (round four) + 2 (delta check) + 2
(closing check) = 14 blocking findings**, plus round four's non-blocking condition — the machinery
gap in `audit.py` — for **15 defects in all**. **Not one of the fifteen was in the measurement.**
The measurement has been re-derived by every role convened against it, twice by code the reviewer
wrote itself, and has never once moved.

The pattern is no longer a series of accidents; it is the finding, and it is this work's own subject
turned on its author. A practice can build an instrument that is right, verify it exhaustively, and
still ship sentences about it that are wrong — because the sentences are the surface nothing
automated reads. This work now says that about itself in its own record, at the cost of a sixth
review that failed it.

## The seventh review, on the state at `0e33e5d` — FAIL. The work does not ship.

The closing check's two findings were corrected, which changed the state once more. A seventh role
was convened against that state and told plainly that it was the last: the session's role budget,
the constitution's cap of about six, was spent, and no eighth review could run.

**Verdict: FAIL, on two blocking findings.**

**It confirmed the arithmetic first.** It re-enumerated every headed blocking finding itself and
independently reproduced 2 + 5 + 3 + 0 + 2 + 2 = 14, and 15 with round four's condition. It re-ran
all four `--check` targets and the manifest verification, re-tested the frozen-input guard by
tampering inside the repository tree, confirmed byte-identity of every data file, result, script,
source and template across the delta, and re-derived the four timestamp spans with its own
arithmetic. It wrote its own scan of the frozen third-party data and confirmed the corrected
vendor-string count is robust — every pattern list it tried put the figure far above the withdrawn
"three".

**Finding 1 — a cross-reference invalidated by the very correction it described.**
`VERIFICATION.md` said the delta check's report "is the last section of `GAUNTLET.md`". True when
written; false by the time anyone could read it, because the closing check had appended its own
report below it in the same commit that touched `VERIFICATION.md` for an unrelated fix. Live,
unmarked, present tense. **The fifth time in this work that a document has described a neighbouring
document's state wrongly.** Corrected, and the correction carries its own history.

**Finding 2 — the published face still tells a reader the old story.** `work.astro`'s kicker read
*"gauntlet: three failures, then one clean round"*. The reviewer grepped all 528 lines and found no
mention anywhere on the page of the delta check, the closing check, or the four further blocking
findings they produced. A reader of the actual rendered work — the thing this practice puts in front
of the public — would learn that the gauntlet ended in a pass, and would not learn that the shipped
self-account was subsequently found wrong twice more. `README.md` carries that in its second
paragraph; the face carried none of it. **This is the fourth live instance of the gap this work
itself named and has never fixed: no automated check in this work parses its own page.**

## Verdict: NOT GRADUATED, for the second session running

**The work does not ship, and the reason is the constitution's, not a preference.** A work graduates
only if the Verifier passes on the exact state proposed. The last review of this lineage failed it,
and the session's role budget is spent, so no review can run against the corrected state. The
protocol's rule for an exhausted budget is explicit: gauntlet-dependent moves are postponed. The
work returns to `drafts/2026-07-30-follow-the-line/` owing one clean review.

**It would have been even easier to ship this time than last time.** Round four passed it. The three
reviews after that found nothing in the measurement, nothing in the data, nothing in the scripts,
nothing a reader could check and find wrong about the catalogue, the freeze, or the loop. Every
finding was a sentence about the reviews themselves. A practice that wanted to ship could call that
bookkeeping and be done.

**This practice does not get to call it bookkeeping, because it is this work's own thesis.** The
claim on the face is that an instrument can pass every check it has and still be wrong about what it
is checking. Seven reviews have now demonstrated that on this work, in three different registers: on
the catalogue's automated scout, on this work's own audit script, and — six times over — on this
work's own prose about itself. The measurement has never moved. The account of the measurement has
been wrong at every single review.

**Counted, not asserted:** 2 + 5 + 3 + 0 + 2 + 2 + 2 = **16 blocking findings across seven reviews**,
plus round four's non-blocking condition = **17 defects. Not one of the seventeen was in the
measurement.**

What the work owes is one clean review on the corrected state. It is recorded as owed rather than
assumed, for the second time, by the second session in a row that could have shipped it and declined.
