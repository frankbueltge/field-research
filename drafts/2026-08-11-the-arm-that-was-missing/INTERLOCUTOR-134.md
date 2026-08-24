# Interlocutor 134 — against Increment 22's refutation of `POST-MORTEM.md` §8

**Session under review:** 134, 2026-08-24, commit `8b89e9d`, branch `research/session-2026-08-24`.
Reviewed: `PREREGISTRATION-134.md`, `INCREMENT-22.md`, `POST-MORTEM.md` §§4/8, `findings-134.json`,
`labels-134-A.json`, `labels-134-B.json`, `score-134.json`, `blinded-134.txt`,
`extract_findings_134.py`, `score_findings_134.py`, `READERS-126.md`, `READERS-127.md`,
`READERS-128.md`, `CONDITIONS-123.md`, `CONDITIONS-127.md`, `CONDITIONS-128.md`, `CONDITIONS-131.md`,
`CONDITIONS-133.md`, `ERRATA-131.md`, `INTERLOCUTOR-133.md`.

---

## VERDICT (a): **CORE CLAIM SURVIVES NARROWED**

**What survives:** the post-mortem's *exclusivity* sentence — "the severed-reader panel is the only
instrument here that has ever found that class of defect" — is refuted on this arc's own disposition
tables; at least half a dozen agreed-A findings attributed to the Interlocutor and the Verifier
withstand hostile scrutiny even after every attack below is granted. **What does not survive
unscathed:** the *comparative rate* half of the core claim — that the adversary role finds the class
at a *higher rate* (13/45) than the panel (2/9) — rests on an undisclosed claim of classifier
independence, a demonstrated and undisclosed tie-break bug in the role-attribution code, and a
population that provably under-samples the panel's own reading-based output relative to its own
source files. The direction of the rate comparison is not reversed by anything found below, but its
reliability is not established either.

Fourteen charges follow: **9 BLOCKING** (bear on the verdict), **5 NON-BLOCKING** (recorded because
they were tested and either failed to land or cut the other way).

---

## OBLIGATION (a) — REFUTATION

### Charge 1 (BLOCKING). The two classifiers' independence is asserted, never shown, and the record
does not permit checking it.

`PREREGISTRATION-134.md` §4 and `INCREMENT-22.md` §2 both say the population was "handed to two
independent classifiers who were told none of this." Neither document, nor `labels-134-A.json`, nor
`labels-134-B.json`, states **what a classifier is** — separate models, separate humans, two calls of
the same underlying process with different prompts, or two calls of the same process with no
variation at all beyond ordering. `labels-134-A.json` and `labels-134-B.json` each carry exactly two
keys — `classifier` (`"A"` / `"B"`) and `labels` — and nothing else. This is checkable: I read both
files in full (`wc -l` 107 and 104 lines) and there is no metadata field of any kind describing
provenance.

The whole of K1 ("raw agreement between the two classifiers... the rule was operational") is a
reliability claim, and reliability claims are meaningless without knowing what varies between the two
measurements. Two runs of a correlated process converging on the same latent reading of "what counts
as reading-held evidence" is not two classifiers; it is one classifier, asked twice, agreeing with
itself at whatever rate its own consistency happens to produce. **0.8039 is compatible with either
story and the record supplies no way to tell them apart.**

*Self-counter:* the 12 disagreements recorded in the label matrix (`score-134.json`
`label_matrix`), five of them A-against-B, are real disagreement, not zero — a single perfectly
self-consistent process would plausibly disagree less on the boundary-heavy cases and might not
produce an E-vs-A split on the post-mortem's own headline row (Charge 5, below). That some daylight
exists between the two label sets is evidence, if weak, against pure self-agreement. It does not
substitute for disclosure.

### Charge 2 (BLOCKING). The role-attribution code has an undisclosed, order-dependent tie-break that
demonstrably misattributes at least one of the 23 agreed-A findings.

`extract_findings_134.py:53-58`:

```
if "panel" in t or "reader" in t:
    return "READER_PANEL"
if "interlocutor" in t:
    return "INTERLOCUTOR"
if "verifier" in t:
    return "VERIFIER"
```

This is a first-match-wins chain, and nothing in `PREREGISTRATION-134.md` discloses that a
dual-attributed source cell resolves this way — §4's only stated tie-break rule is for the A–D
*label*, not for *role*. I found seven source cells in `findings-134.json` naming more than one role
(`role_raw` field), and one of them changes the headline numbers.

`CONDITIONS-123.md:49`, row 16 (= `F026`, one of the Interlocutor's 13 agreed-A findings, quoted in
`score-134.json` `A_set.agreed_by_both.by_role.INTERLOCUTOR`):

> `| 16 | The neighbouring paper is still unnamed on the receiver-facing page, two versions running | Verifier 9, Interlocutor | — | ACCEPTED, NOT FIXED. Owed. |`

Every other row in every `CONDITIONS-*.md` table numbers a role's own findings sequentially
("Verifier 1", "Verifier 2" … "Interlocutor 1", "Interlocutor 2" …). Read against that convention,
"Verifier 9, Interlocutor" is naturally **Verifier's ninth numbered finding, with Interlocutor named
second and unnumbered** — i.e. Verifier's finding, seconded. The extraction code's priority order
(interlocutor checked before verifier) recodes it as INTERLOCUTOR regardless. Moving `F026` to
Verifier changes the headline rate comparison from **13/45 (28.9%) vs 6/29 (20.7%)** to **12/45
(26.7%) vs 7/29 (24.1%)** — the ranking survives this one correction, but the margin the increment's
prose leans on ("the adversary finds this class more often than the panel does — 28.9% against
22.2%") shrinks by more than a third from a single undisclosed line of code, on a finding the increment
never mentions checking.

### Charge 3 (BLOCKING). The population under-samples the panel's own reading-based output relative
to the panel's own source files, and at least one instance directly denies the panel credit for a
read-the-output finding its own file attributes to it by name.

The task instruction to check `READERS-126.md`, `READERS-127.md`, `READERS-128.md` against the 9
population rows pays off. `READERS-126.md` §"What all three said back, unprompted" lists **seven**
items; only four became numbered `CONDITIONS-126.md` rows (`F041`–`F043` plus the "provenance
filenames" half of a merged row). Three did not:

- item 3, "the vocabulary of this practice is undefined inside the bundle" (`READERS-126.md:106-108`)
- item 5, "why an unfinished thing is packaged like a finished one," which required reading
  `VERSIONS.md`'s own sentence *"carries no verdict until the gauntlet of this date reports"*
  (`READERS-126.md:117-122`)
- item 6, "the precision asymmetry, found cold" against `LIMITS.md` §11
  (`READERS-126.md:124-128`) — explicitly a case of a stranger reading a held document (`LIMITS.md`)
  and reaching, unaided, an inconsistency the practice had *already written down against itself hours
  earlier* — as clean an instance of the locked A rule as exists anywhere in this record, and it was
  never tabled as a numbered finding at all, so it never entered `findings-134.json`.

More consequential: `READERS-127.md` item 4 —

> *"The letter undersells what running the tool costs the reader. Reader 2, and only reader 2,
> because only reader 2 ran it and read the output: the tool's default vantage mode discloses the
> caller's IP…"* (`READERS-127.md:110-115`)

— is a textbook A finding (opened a program's own output, already held, unread by the practice) made
by a severed reader. `CONDITIONS-127.md` finding 8 records the *same defect* — but sources it solely
as `Interlocutor (a) 5` and does not mention the panel at all, even though the panel's own unedited
file, published the day before, says in as many words that reader 2 found it first by running the
tool and reading what it printed. The population — and therefore the classifiers, and therefore the
23-count and the 2/9 panel denominator — never sees this instance as a panel finding. **The
disposition table's own compiling session chose which of two independently-arriving discoverers to
credit, and the extraction script inherited that choice as if it were the whole truth.**

This directly answers the task's second suggested attack: the panel's real findings, read from its
own unedited source, are richer than the 9 rows the population gives it, and at least one of the
missing instances is exactly the class this measurement exists to count.

*Self-counter:* adding these back does not obviously move the panel's *rate* much — the panel's
denominator would also grow (its total-findings count, not just its A-count, since several of the
dropped items are D-type argument, not A), and a rough recount with the three `READERS-126` items and
the `READERS-127` item-4 instance added puts the panel near 3/13 (23%), barely different from 2/9
(22.2%). The undercount is real and the sourcing inconsistency is real; the size of its effect on the
final ranking is not.

### Charge 4 (BLOCKING). Applied one by one, a fair reader does not agree with all 23 agreed-A labels
— and the disagreement concentrates on the Interlocutor and Verifier rows the rate claim needs.

Working from `score-134.json` `A_set.agreed_by_both`, against the locked rule in
`PREREGISTRATION-134.md` §4:

**Solid — survives a hostile reading, no real argument against A:** `F022` (README/VERSIONS circular
pointer, `CONDITIONS-123.md:45`), `F025` (`prose-audit-123.json`'s own scratch path,
`CONDITIONS-123.md:48`), `F030` (uncommitted merge-conflict markers in `DAY6-2026-08-16.md`,
`CONDITIONS-124.md:38` — the cleanest single example in the whole population: literal `<<<<<<<`
markers nobody read before committing), `F074` (a correction that stopped at the least consequential
copy of its own error, `CONDITIONS-129.md:28`), `F083` (Day 10's silence, `CONDITIONS-129.md:37`),
`F095` (the population's omission of `audit_instrument.py`, `CONDITIONS-133.md:35`). Six findings,
spanning Interlocutor and Verifier, none needing the contested calls below.

**Contestable as D (argument from material already in front of the reviewer, not newly opened) rather
than A:**
- `F020` ("The prose auditor reads digits and is blind to number words") and `F023` ("the rebuild
  audit's classifier is file-wide … not field-wide") and `F028` ("the build `--audit` gate does not
  fail on `unaccounted_published_ids`") and `F096` ("`guard_claims.py --check` has a second,
  data-dependent write path") are all findings reached by tracing what a piece of code's *logic* does
  — not by opening a document nobody had read, but by reasoning about a script the reviewer already
  had open in front of them as part of the review. §4's rule text confines A to "a document, dataset
  or program **output**" already possessed; source-code logic-tracing is not obviously any of those
  three, and D's test — "requiring no material the finder did not already have in front of them" —
  reads as a closer fit for all four. Two of these four (`F020`, `F096`) are Interlocutor-attributed
  and count toward the 13.
- `F066` ("D26's refusal is blind during the reservation hold" — a timing gap read out of
  `window_status.py` and `run_window_day.py`'s logic) is the same shape and is Interlocutor.
- `F093` ("Roughly half of `INCREMENT-20.md` is this practice's own extraction defects and a
  scoreboard against its own checker") is a characterisation of a whole document's proportions, not
  the discovery that a specific unread passage was missed — closer to D than A. Interlocutor.

**Contestable as B (a statement the practice made, checked against the artifact it names) rather than
A**, on the rule's own worked examples:
- `F017` ("The 0.14 pp spread ships with no trace of the correction that found it 2.35× inflated") —
  checking a printed figure against the correction record that produced it.
- `F019` ("`FIGURES.md` is generated prose and was never passed to the prose audit") — checking the
  prose-audit's coverage claim against what it actually covers.
- `F027` ("`ERRATA-124.md:E20`… in neither the registry nor the reason table") — checking a
  completeness claim (the registry, the reason table) against a named erratum.

  All three are Interlocutor.

That is **seven of the Interlocutor's thirteen** agreed-A findings with a live, arguable case for
relabelling to D or B, against **six solid**. Even a moderate reader who accepts only half the
contested calls (say, four of seven) drops the Interlocutor's A-count from 13 to 9, its rate from
28.9% to **9/45 = 20.0%** — below the panel's own 2/9 = 22.2%, which is the exact reversal the
post-mortem's rate claim needs and which the increment reports it did not find. The Verifier's six
include two more of the same shape (`F023`, `F028`); pruning those drops Verifier to 4/29 = 13.8%.

*Self-counter, and it is the important one:* I am one hostile reader applying the same rule the
practice's two classifiers applied, and I agree with the practice's rule-writers that these are
**genuinely arguable**, not misapplications — nothing above is a slam-dunk reclassification, each is
a defensible alternative reading of a rule whose own text (§4) concedes the A/B line turns on "where
the finder had to look," which is exactly the fact a blinded classifier reading only `blinded-134.txt`
cannot always recover. What this charge establishes is not that the 23-count is wrong, but that it is
**far less stable than a single 0.8039-agreement number suggests**, because the agreement figure is
dominated by the unambiguous bulk of the 102 (arithmetic checks, citation checks, run-it checks) and
says little about reliability on the ~15-20 rows that decide the rate comparison.

### Charge 5 (NON-BLOCKING, disclosed already). The post-mortem's own headline example could not be
classified — but the population's own construction, not the rule, is why.

`F073` (`CONDITIONS-128.md:63`) bundles five heterogeneous handed-over items into one table row,
of which line 3833 ("We intend to keep the dashboard online…") is only item (iii). Classifier A
called the whole row **E** ("Bundles five heterogeneous items… no single determinable action");
classifier B called it **A**. `INCREMENT-22.md` §4 already discloses this honestly and does not
oversell it. I confirm the reason is structural: the source table itself collapsed five distinct
claims of different classes into one cell, so no classifier working from `blinded-134.txt` alone could
cleanly resolve it. This is a real limit of a mechanically-extracted population, but it is the
increment's own limit, already stated in `PREREGISTRATION-134.md` §6 before the result existed, and
does not by itself move the verdict. Recorded non-blocking because the increment does not hide it.

### Charge 6 (NON-BLOCKING — tested, and it fails; recorded against myself). "Instrument" is not being
read uncharitably.

The candidate defense that `POST-MORTEM.md` §8's "instrument" means only an automated, *built*
mechanism (in which case the panel, a convened human/agent procedure, would be exempt from needing to
be "the only" thing, and the whole refutation would be attacking a strawman) does not survive contact
with the sentence itself. §8 reads: *"Every mechanism this arc built checks a statement against an
artifact… The severed-reader panel is **the only instrument here** that has ever found that class of
defect."* The post-mortem's own words put the panel inside the category it is being measured against
— it explicitly calls the panel an "instrument," in the same breath as "mechanism… built." There is no
narrower, more charitable reading available in the text that exempts the panel from being an
"instrument" in whatever sense the sentence uses the word. **This defense of the post-mortem does not
work, and I record that against my own side.**

### Charge 7 (NON-BLOCKING — conceded to the increment). `F037`'s A-label survives scrutiny against
the rule's own "recomputation is B" example.

§4's B row lists "recomputation… arithmetic" as characteristic B activity, and `F037` ("only 7 [of
3,620 identifiers] ever show more than one determinate state… 412 of the 446 ever-absent identifiers
are absent on every day," `CONDITIONS-125.md:63`) is, on its face, a recomputation over the arc's own
series data. But B requires "a statement the practice made" that the recomputation checks — and no
prior statement named this specific cross-tabulation; the finder derived a wholly new statistic from
data nobody had queried, which is closer to A's "the defect is the absence of that reading" than to
B's "the statement itself says where to look." I tested this hardest of all seven Interlocutor
findings above and it is the one that holds up cleanly. Conceded.

### Charge 8 (BLOCKING). The rate table's fence (K4) is honoured in the letter and violated in the
prose that surrounds it.

`score_findings_134.py:93-94` writes the fence into the data structure itself ("no significance test
is run and none may be quoted; the panel denominator is single digits"), and `INCREMENT-22.md` §6
repeats it. But §3 and §7 of the same document say, respectively, "the adversary finds this class more
often than the panel does" and "the roles that read the material do — all of them, at rates between
one finding in five and two in seven, **with no instrument distinguishing itself**." Both are
directional, comparative readings of a 13/45-vs-2/9 gap that Charges 1-4 above show is not robust to
a single undisclosed code choice or to a defensible re-reading of seven contested rows. K4 forbids a
significance test; it does not by itself forbid confident directional prose, but the increment's own
practice elsewhere (disclosing its losing prior belief in §4, naming the F073 disagreement in §4) shows
it knows how to hedge harder than this when it wants to. It did not extend that same hedge to the
sentence doing the most interpretive work in the document.

### Charge 9 (BLOCKING — the strongest single attack, and where it stops). None of the above reverses
the exclusivity finding, which is the core claim's load-bearing half.

I looked, deliberately, for a reading under which zero non-panel A findings survive. I could not
produce one. `F030` (merge-conflict markers left in a committed file, discovered by opening a file
nobody had reason to think needed opening) has no plausible B, C, or D reading — the defect *is* the
unread state of the document, full stop. `F025` (own JSON output carrying a scratch path from a trial
build) and `F022` (a circular documentation pointer) are the same shape. Three unimpeachable
non-panel A findings, from two different roles, is already sufficient to refute "the panel is the only
instrument that has ever found that class of defect" as written, on the meaning of "instrument" the
post-mortem's own sentence uses (Charge 6). **The exclusivity clause of the core claim is refuted, and
none of Charges 1-8 puts it back.**

---

## OBLIGATION (b) — THE HOSTILE CRITIC

**Does the recurring charge apply again, and is this a fourth consecutive session of it?** Yes to
both, and the record makes this checkable rather than a matter of taste.

The charge — "half of each increment is the practice checking its own checker" — is not something I
am importing from outside. It is in the repository, named three times before this session:

- `CONDITIONS-131.md:33`: *"Roughly half of `INCREMENT-20.md` is this practice's own extraction
  defects and a scoreboard against its own checker — the same charge session 129 drew."* Disposition:
  **"ACCEPTED AS FAIR AND DELIBERATELY NOT ACTED ON."**
- `CONDITIONS-133.md:41`: *""Half this increment is the practice checking its own checker" — and this
  is the third session running, unacknowledged."* Disposition: **"ACCEPTED AND NAMED FOR THE FIRST
  TIME."**
- `INTERLOCUTOR-133.md:27`: *"The recurring… pattern is real and unacknowledged as a recurrence…
  nowhere does it note this is the third occurrence of the pattern."*

Session 134's own population — this session's own output — contains a fourth instance of exactly this
observation, made by a *previous* session about a *previous* increment: `F095`
(`CONDITIONS-133.md:35`, agreed A, Interlocutor): *"The population omits `audit_instrument.py` — a
live, self-referential instrument in this same arc… The increment's generic concession that the
population is hand-made does not cover the single most on-point omission available."* This session
classified that very observation as data and moved on. It did not apply the observation to itself.

**What session 134 actually is, stripped of its instrumentation:** a session that took one sentence
from a four-day-old public document, built an extraction script and a scoring script (both written by
this practice), handed the output to two classifiers whose relationship to "this practice" is
undisclosed (Charge 1), and used the result to grade the practice's own past reviewers' past findings
about the practice's own past work. This is not literally "half the document explains the build tool's
bytecode hygiene" — the form has moved on since session 129's version of the charge — but the
substance is the same recursion one layer up: instead of auditing the auditing instrument, this
session audits the *classification* of what the auditing instruments (Interlocutor, Verifier, panel)
already found. Blinding, pre-registration, and named kill-conditions are real methodological
improvements over the earlier, cruder self-audits — they are not nothing — but they do not answer the
actual question the recurring charge raises, which is not "was this measurement careful" but "is the
entity marking the exam the same entity that sat it." Given Charge 1, that question is still open
after this session, dressed more convincingly than before.

**Is this slop?** Not in the sense of being careless — the opposite defect is closer to the truth. It
is *elaborate* self-examination that reliably produces well-hedged, honestly-caveated findings
(§4's confession, §6's fences, K4's letter-of-the-law compliance) which the practice's own conditions
files then mark "ACCEPTED AND DELIBERATELY NOT ACTED ON." A practice that diagnoses its own besetting
failure mode with this much precision, three sessions running, and then produces a fourth instance of
it in the very session that also (via `F095`) restates the diagnosis as agreed data, is not obviously
in need of more sessions of diagnosis. An outside critic handed this file would not say "this is
lazy" — they would say "this practice has excellent internal critics and no mechanism that makes their
verdicts change what happens next," which is a harder charge to answer than sloppiness, because the
practice's own artifacts (`CONDITIONS-131.md`'s disposition, quoted above) already make the point for
them.

**The honest alternative, with twelve days left before 2026-09-05.** `POST-MORTEM.md` §5 already
named the one thing this arc produced that a receiver could actually use — a short, kind bug report
about a volunteer-run dashboard — and said in its own words: *"it should have been written by this
practice rather than for it."* Nine days of arc plus one more day of Increment 22 later, it still has
not been written. Section 8's Q2 ("what is the honest form of a finding about somebody else's broken
instrument") is still open. And the pre-registration for this very session explicitly declined to
score the half of the post-mortem's claim that would actually tell the architect whether to convene
another panel — the hit-rate half, named "owed" in `PREREGISTRATION-134.md` §6 and left unscored.
With twelve days before a review of whether this practice continues, the honest use of a session was
either of those two unfinished, decision-relevant, outward-facing pieces of work — not a second
internal grading pass, using an undisclosed pair of classifiers, over the results of the first one.

---

## Summary count

- **Charges under obligation (a):** 9 total. **BLOCKING: 1, 2, 3, 4, 8, 9 = 6.**
  **NON-BLOCKING: 5, 6, 7 = 3.**
- **Verdict:** CORE CLAIM SURVIVES NARROWED. Survives: the exclusivity refutation (findings meeting
  the locked rule exist outside the panel, from at least two roles, on solid unimpeachable examples).
  Does not survive as established: the comparative rate claim (adversary role higher than panel),
  which depends on undisclosed classifier independence, an undisclosed and demonstrated
  role-attribution tie-break bug, and a population shown to under-sample the panel's own recorded
  output.
