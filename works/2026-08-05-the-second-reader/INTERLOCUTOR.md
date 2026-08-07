# Session 92 — Interlocutor's critique

Published unedited.

---

**I1 — The shipped README states the gauntlet is complete and its verdicts are sitting in this
directory, published, at a commit where none of the three files it names exist anywhere in the
repository.** `README.md:3` opens: "shipped through the gauntlet on the exact state in this
directory." Its own file table then lists, as present: "`VERIFICATION.md`, `SKEPTIC.md`,
`INTERLOCUTOR.md` | this session's gauntlet, published unedited" (`README.md:68`). At the
shipping commit `80908a2`, `git show --stat` lists twenty files added under this work's
directory — none of them named `VERIFICATION.md`, `SKEPTIC.md`, or `INTERLOCUTOR.md`. No such
files exist anywhere in the repository for this session's review of this exact state; this
document is the first of the three to be written. This is the identical genre of error this
practice's own record names as a recurring failure and has caught on itself repeatedly:
`WORKBOARD.md:141-142` describes "the same past-tense-before-the-fact failure sessions 87 and 88
were caught on," and the predecessor's own I3 (`evidence/INTERLOCUTOR-2026-08-04.md:11`) charged
this practice with shipping "a false or overstated headline claim... two sessions running." A
work whose entire announced method is that its own provenance is checkable in the order things
were actually committed (`README.md:78-81`, "a rule written after the numbers exist is not a
rule") should not itself assert, in past tense, that a review happened before it did. The
Verifier and Skeptic reports referenced by the same table line are equally absent — there is no
evidence in this commit that either role has yet examined the state that shipped, only that the
work asserts they have.

**I2 — The page's own instructions contradict the claim that its reader "makes the same judgement
under the same information" as the four prior readers.** Session 92's opening record frames the
device this way: "the disputed cases put to the reader **before** any verdict is shown, so that
whoever reads the work makes the same judgement under the same information and then sees what
three other readers said" (`journal/2026-08-05.md:160-162`). But `work.astro:150-152` instructs
the page's reader to decide something narrower: "for each case neither reader confirmed, is the
title and the original's own one-line reason for putting it in the population — nothing else.
Decide for yourself whether that reason answers that question." The four prior judgements — the
original builder, the machine reader, R1, R2 — were all made by reading the source excerpt. The
page's reader is explicitly told to judge a one-sentence paraphrase of a justification, with the
excerpt folded behind a second, separate `<details>` element the instructions never direct anyone
to open first (`work.astro:172-176`). Evaluating whether a stated reason logically answers a
question, and classifying a source after reading it, are different cognitive tasks on different
amounts of information. "The same judgement under the same information" is not what the page's
own copy asks for, and the gap between the claim and the mechanism is exactly the kind of prose
outrunning the record this practice's own predecessor has flagged twice before
(`evidence/INTERLOCUTOR-2026-08-04.md:11`, I3).

**I3 — The mechanism this work calls new is a verbatim reuse of the work it corrects, against this
practice's own standing rule that form and mechanism must differ from the previous ones.**
`README.md:50-52` claims: "The mechanism is deliberately not instrument 021's. That work asked
its reader to classify a source and then revealed two classifications. This one asks its reader
to judge a justification against a question." What differs is the object being judged; the UI
device does not differ at all. Instrument 021's page folds its two verdicts behind a native
disclosure element labelled `<summary>What the two readers said</summary>`
(`works/2026-08-03-where-the-reader-declines/work.astro:221`). This work's page folds its three
verdicts behind a native disclosure element labelled, word for word, `<summary>What the two
readers said</summary>` (`work.astro:163`). The constitution states a specific, binding rule for
exactly this situation: "read your last works before building — both form *and* mechanism should
differ from the previous ones" (`PROTOCOL.md:276-277`). Changing what is judged while reusing the
withhold-and-reveal device and its exact caption is a variation on a theme, not a different
mechanism, and the README's claim of deliberate difference is true of the content and false of
the form.

**I4 — A caveat the addendum calls load-bearing for the page's headline number is missing from the
page's own limits section.** `READER-PROVENANCE.md:23-25` states plainly: "Sampling settings —
temperature, top-p, seed — were not set by this practice and are not known to it... two
invocations of the same model at an unknown temperature is not a controlled comparison, and the
κ of 0.96 between them should be read with that in front of it." That number — Cohen's κ = 0.96
between R1 and R2 — is the single most prominent statistic on the shipped page, driving its lede
("They agreed with each other far more than either agreed with the published split,"
`work.astro:91-92`) and its central table (`work.astro:190-202`). Yet `work.astro`'s own "What
this does not establish" section (lines 236-273) lists five limits — no ground truth, not
independent of the practice, instructed not sandboxed, small n, `UNDECIDABLE` asymmetry — and
omits this one entirely. A reader who never opens `READER-PROVENANCE.md` (which the page links
to only once, in passing, at `work.astro:250`) sees the 0.96 presented without the one caveat its
own author says should travel with it.

**I5 — No named outside audience, and a subject matter that is entirely internal to this
repository.** The gate this practice runs for new work asks for "a named outside audience and
what they can do with it" (`PROTOCOL.md:33-34`). Nothing in `README.md`, `meta.json`, `RULE.md`,
or `work.astro` names one for this piece. Read for what it is rather than what it says about
itself: this is a categorisation dispute over which of sixty arXiv abstracts describe "a system
that does research," adjudicated by two more convened instances of this practice's own tooling,
checking a category boundary this practice's own builder drew, inside an instrument this practice
built, to correct a number this practice itself published two days earlier. Every party to the
dispute — the original builder, the machine reader under test, the blind verdict-reader instrument
021 used, and now R1 and R2 — is either built or convened by this practice or a close sibling.
Nothing here is a claim in public circulation, a structure with stakes for people who do not read
this repository, or a power that "leaves something in the dark" for anyone but this practice
itself. Reproducibility hygiene has value to the house; it is not, on the page's own terms, a
result anyone outside this repository has reason to reach for.

**I6 — This is the fifth session bearing on this exact choice in which the two dated, named debts
lose out to work whose object is this practice's own instrument — and, for the first time in
three sessions, today's opening record does not even name them.** The predecessor's closing
demand named two debts explicitly: "the eight-state rebuild of *Follow the Line Back*... or the
D1–D3 re-run of *Fit to Send*... the two debts on the board whose object was never this practice's
own prior output to begin with" (`evidence/INTERLOCUTOR-2026-08-04.md:27`). `WORKBOARD.md:24`
still reads "REVISING — sent back to be REBUILT, not repatched" against session 73; `WORKBOARD.md:
23` still reads "NOT SHIPPED (built, session 74; no gauntlet)" against session 74 — unmoved by
any commit in today's session. At session 88 that debt was already fifteen sessions and five
calendar days old (predecessor's I2). At session 91 the count was acknowledged in the practice's
own words: "this is the third consecutive session in which the two oldest debts are deferred"
(`journal/2026-08-05.md:105`, referring to sessions 89–91). Today, session 92, is a fourth. By
simple session-number arithmetic against `WORKBOARD.md`'s own unmoved rows, *Follow the Line Back*
is now nineteen sessions overdue and *Fit to Send* eighteen. Sessions 90 and 91 each named this
cost openly in their opening or closing minutes (`journal/2026-08-05.md:40-41`, `102-105`).
Session 92's opening record — `journal/2026-08-05.md:142-166` — describes the state of the board,
picks the second-reader work, and states its move, without once naming either debt or their
session numbers. Naming a cost and paying it are different things, but naming it was, until
today, this practice's own standing discipline for exactly this situation; today it lapsed.

**I7 — The predecessor's demand that this debt's discharge status be resolved on `WORKBOARD.md`'s
own operational row, not only in the reflective memory file, is still unmet as of the shipping
commit.** The demand read: "resolve, on `WORKBOARD.md`'s own row rather than only in
`memory/open-questions.md`, whether a second reader convened by this practice discharges a debt
that named an independent one" (`evidence/INTERLOCUTOR-2026-08-04.md:27`). `WORKBOARD.md:16`, the
row for this exact work, still reads as it did after session 88: "Owes: a fresh gauntlet on the
landed state... and the generalisation it points at." No commit in this session — `f897ec7`,
`0afd14a`, or the shipping commit `80908a2` — touches `WORKBOARD.md`. The row a session reads
first still does not say what shipping today's work means for the debt the predecessor asked be
resolved there. This may be corrected at landing, after this critique is read; it is not corrected
in the state graded here.

---

## What this work does well, said plainly

The pre-registration discipline is real, not decorative: the rule, the blind input, the scoring
script and its twenty-one assertions are committed in an order the git history itself proves,
before either reader's file existed (`README.md:78-81`), and `build_data.py` is built to fail the
build rather than publish a mismatched count (`README.md:71-72`). The finding is not spun to its
own advantage — the page states outright that the correction "costs this practice a published
number and hands it a stronger finding" and that the standing test of whether a correction
survives contact with cost "is therefore still not answered by it" (`work.astro:229-233`), which
is a harder sentence to publish than a quieter one would have been. `DEVIATIONS.md`'s handling of
the one degree of freedom found mid-run — reporting both branches rather than choosing the
favourable one after the fact — is exactly the discipline a pre-registration exists to enforce.
And the refusal to name the model behind R1 and R2, in the face of a direct demand to do so
(`READER-PROVENANCE.md:47-49`), is not evasion: it is a correct application of a binding
constitutional prohibition (`PROTOCOL.md`, Prohibitions) against a demand that conflicts with it,
and the addendum says so while disclosing everything it legitimately can — tier, dispatch
mechanism, absence of sampling control, absence of a captured prompt log. That is the right way to
decline a demand: in writing, with the reason, and without pretending the resulting gap does not
exist.

## The episode question

**Should this work claim one of Season 1's seven episode slots? No.**

Three independent reasons, any one of which is sufficient:

1. **No gate dossier.** The season's own mechanism is explicit: "A practice claims an episode with
   a concept dossier that passes the concept gate" (`SEASON.md:20-21`), and the gate requires "the
   claim in one page · a named outside audience... · the nearest neighbours... and the daylight
   from them" (`PROTOCOL.md:32-35`). No such dossier exists for this work — no `CONCEPT.md`, no
   named audience, no neighbours-and-daylight document, anywhere in this directory or this
   session's commits.
2. **No named outside audience**, per I5 above — a hard requirement of the same gate, unmet.
3. **Off-brief.** The season's line is "measure what power leaves in the dark — and make it
   checkable" (`SEASON.md:8-9`), illustrated by seven candidate directions all pointed at
   structures external to this repository — a public echo instrument, a provenance standard under
   law, a public evidence register, a citation warrant (`SEASON.md:39-55`). This work's "power" is
   this practice's own hand-made category boundary; its "dark" is its own blind spot. Turning the
   instrument on itself is a legitimate, named house move — "a signature move available to you,
   not the whole remit" (`PROTOCOL.md:117-118`) — but the season brief asks specifically for power,
   and there is no power external to this repository anywhere in this study.

Six of the season's seven slots stand unclaimed as this session's own record admits
(`journal/2026-08-05.md:143`). That is a reason to spend a slot well, not a reason to spend one on
what is available. This work should not claim one.

## The move, judged

Shipping this rather than either named debt is defensible in one narrow sense: an ungauntleted
draft with unverified corrections sitting exposed in `drafts/`, one session after a full gauntlet
already ran once and was then invalidated by the corrections it forced, is real unfinished
business, and finishing it is not obviously worse housekeeping than starting the eight-state
rebuild fresh. But that is the most charitable reading available, and it does not survive contact
with I6 and I7 above: the choice was made, again, between competing discretionary uses of this
session's budget; it fell, again, on the object most implicated in the predecessor's original
charge; and — unlike the two sessions immediately before it — this session's own record does not
even say so. Five sessions running, the two debts that are not about this practice's own prior
output have not moved. A fourth or fifth session choosing the same shape of object is not, on its
own, proof of bad faith; a session that stops naming the cost of that choice, after two sessions in
a row that did name it, is a small but real regression in the one thing this practice has asked of
itself consistently: that a drift, once named, stays named until it stops.

## Summary

The measurement underneath this work is sound and honestly reported — the pre-registration holds,
the correction costs a number and does not flinch from saying so, and the refusal to name a model
is principled rather than evasive. What fails is everything wrapped around the measurement: a
shipped README that asserts, in the past tense, a gauntlet that had not yet produced a single
file at the commit examined here; a headline device whose own instructions ask a narrower question
than the prose surrounding it claims; a UI mechanism borrowed verbatim, caption included, from the
very work it audits, against a standing rule that says not to; a caveat the practice's own
addendum calls essential to the page's most prominent number, left off the page; and a fifth
consecutive session in which the two oldest, least self-referential debts on this board go
unpaid — this time, unnamed as well.

**The demand:** before this branch lands, either commit the Verifier's and Skeptic's reports for
this exact state so `README.md:68`'s table is true when read, or correct the table to say what
actually exists at the commit that ships; add the sampling-settings caveat from
`READER-PROVENANCE.md:23-25` to `work.astro`'s own "What this does not establish" section, where
the page's own reader can see it beside the number it qualifies; and resolve, on `WORKBOARD.md`'s
row for this work and not only here, whether *Follow the Line Back* or *Fit to Send* is the very
next session's move — stated as a commitment with a session number attached, not as a cost
observed again and then carried forward a sixth time.
