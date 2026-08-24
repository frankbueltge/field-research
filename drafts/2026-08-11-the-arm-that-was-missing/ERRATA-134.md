# Errata 134 — 2026-08-24

*Continuing the arc's numbering; `ERRATA-133.md` ended at E43. Every entry below is a **new dated
event**, not a silent patch. E44 corrects a document this practice published four days ago and five
sessions have read since. E45 through E48 are this session correcting itself within the hour, on
findings its own two roles handed it, and **three of the four make this session's result weaker
rather than stronger.***

---

## E44 — `POST-MORTEM.md` §8's exclusivity claim is REFUTED on this arc's own record

**The sentence, published 2026-08-20 and live since:**

> *"The severed-reader panel is the only instrument here that has ever found that class of defect,
> and it found one in each of the three times it ran."*

**The class**, in the post-mortem's own words: *"whether anyone read to the end of what was already
in hand."*

**Refuted.** 124 findings from this arc's own disposition tables, classified blind by four
classifiers in two rounds under a rule locked before any of them saw a case
(`PREREGISTRATION-134.md` §4): **25 findings are of that class, and 22 of them are attributed to
roles that are not the panel.** Six of the twenty-two were then put to this session's own adversary,
which reported it could find no reading under which they are not of the class
(`INTERLOCUTOR-134.md` charge 9). Computed by `score_findings_134b.py` → `score-134b.json`.

**What is NOT withdrawn.** The post-mortem's §4 stands unchanged; so does its account of why nine
gauntlets failed; so does *"a panel is cheap"*. **Only the word "only" fails**, and it fails against
the record §4 of the same document is drawn from. This practice notes against itself that
`POST-MORTEM.md` §4 already listed three findings of this class and credited the panel with **one**
of them — the contradiction was internal, four sections apart, and stood for four days.

**Marked in place** at `POST-MORTEM.md` §8, dated, in the form legal-hygiene rule 6 requires and the
same form this arc used at `POST-MORTEM.md:98`. **The post-mortem is not rewritten.**

## E45 — the extraction instrument dropped a whole file of twenty-two findings, in silence

**Found by:** `VERIFIER-134.md`, blocking 2 — an independent recomputation that went and read the
`CONDITIONS-*.md` files by hand rather than trusting the extractor's own file list.

`extract_findings_134.py` selected finding rows with `^\**\d+\**$`, a digit-only row id.
`CONDITIONS-122.md` numbers its rows `V1..V9` and `I1..I13`. **Every one of them was dropped, and
nothing reported a skip** — the file simply never appeared in `files_with_finding_tables`. The
file's own title is *"Disposition of all twenty-two findings of the session-122 gauntlet."*

The pre-registration promised *"every numbered row of every finding-disposition table"*
(`PREREGISTRATION-134.md` §3). **The population delivered 102 of 124: it was 17.7 % short of what
this session had written down that it would measure.** Repaired: alphanumeric ids are accepted, and
where a table carries no source column the role is read from the nearest preceding `## … findings`
heading — never from the row id's prefix letter, which would be this practice guessing from one
file's convention.

**The repair changed ten further attributions**, all `CONDITIONS-121.md` rows that were
`UNATTRIBUTED` and sit under that file's own `## Verifier findings` heading at line 20.

**This is a defect of the same shape as the one this session set out to measure:** an instrument that
read part of what it held and reported on the whole.

## E46 — role attribution had an undisclosed, order-dependent tie-break, and it moved a headline count

**Found by:** `INTERLOCUTOR-134.md`, charge 2.

`normalise_role` was a first-match-wins chain testing `interlocutor` before `verifier`. **Seven cells
in the population name more than one role.** `CONDITIONS-123.md:49` reads *"Verifier 9,
Interlocutor"* — on the convention every other row in these tables follows, the Verifier's ninth
numbered finding, seconded by the Interlocutor. It was recoded to **Interlocutor** and sat inside a
count this practice published.

**Nothing in `PREREGISTRATION-134.md` disclosed any role tie-break.** §4's only stated tie-break is
for the A–D label.

Repaired: every role name is tested, none wins by position, and a cell naming two roles is **JOINT**
and counted as neither. **Six such cells exist in the repaired population.**

## E47 — the rate comparison this session published in its own favour is WITHDRAWN

**The withdrawn sentences,** from the first version of `INCREMENT-22.md` at `8b89e9d`:

> *"the adversary finds this class more often than the panel does — 28.9 % against 22.2 %"*

> *"the roles that read the material do — all of them, at rates between one finding in five and two
> in seven, with no instrument distinguishing itself."*

**Both are withdrawn, and the reason is a demonstration, not an argument.** `INTERLOCUTOR-134.md`
charge 3 produced an instance: `READERS-127.md:110-115` records a severed reader finding — that the
printed command discloses the reader's own IP, read out of the tool's own output — **which the
disposition table files under an Interlocutor-only row** (`CONDITIONS-127.md` finding 8). The
population is this practice's summaries of its reviewers, and those summaries lose panel findings.

**And the repair made the panel look worse, which is the point.** Fixing E46 moved
`CONDITIONS-128.md#12` — one of the panel's two class-A findings — into a JOINT cell, dropping the
panel from 2/9 to **1/7**. A population that gets worse for the panel every time this practice
repairs its own bookkeeping is measuring the bookkeeping.

**Recorded against the adversary's arithmetic as well as this practice's:** charge 4 computed that
pruning contested rows would drop the Interlocutor below the panel. On the repaired population it
does not — the Interlocutor is top under the base, half-pruned and fully-pruned passes alike
(`score-134b.json`). **The withdrawal is not conceded to that arithmetic; it is made on charge 3,
which the repair confirmed rather than weakened.** No ranking is reported and none may be quoted.

## E48 — this session's own count of its classifiers' disagreements was wrong, in a document about counting

**Found by:** `VERIFIER-134.md`, blocking 1, by summing the label matrix the increment itself
published.

The first version of `INCREMENT-22.md` §6 said *"twelve findings were labelled differently by the two
classifiers … five of them A-against-B."* **The true figures are 20 and 8**, and they are derivable
from the increment's own correctly-stated agreement figure: 0.8039 × 102 = 82 agreed, therefore 20
disagreed. **The document contradicted itself two sections apart and neither number was recomputed
before it was written down.**

**This is the third session running** in which a hand-carried figure in this practice's own prose was
found wrong against a machine-written artifact standing beside it (`ERRATA-133.md` E39 was the
second).

**And it happened a fourth time, inside this entry, forty minutes later.** The first draft of this
erratum said the rewritten increment states *"19 of 124"* for the repaired population. **The figure
is 26 of 124** — 20 disagreements in round 1 and 6 in round 2, both derivable from the agreement
figures already published in `score-134b.json`. Nineteen was typed, not computed, in the paragraph
recording that this practice types figures rather than computing them. Caught here by running the
arithmetic rather than by any check; the increment and this entry both now carry **26**, taken from
the artifact.
