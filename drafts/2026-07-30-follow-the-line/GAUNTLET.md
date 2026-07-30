# The gauntlet — first round, 2026-07-30

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
