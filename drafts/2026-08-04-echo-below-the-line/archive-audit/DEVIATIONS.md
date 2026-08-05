# Deviations from `PREREGISTRATION-ARCHIVE.md`

Dated diffs. Each one is written **at the moment it is taken**, with the state of knowledge at that
moment stated, so that a reader can see whether it was taken before or after the numbers it affects
existed.

---

## D1 — 2026-08-05, 13:02 UTC — the masthead lists are truncated at 40, and the pre-registration did
not foresee it

**State of knowledge when this was written:** Stage 0 (reading the snapshots) had run. **No
nameserver query had been made, no candidate unit computed, no U existed for any cluster.**

**What was found.** For 14 of the 86 published clusters the instrument's own `domain_count` is larger
than the length of its committed `mastheads` list, and in every one of those 14 the list is **exactly
40** entries long: `2026-06-21` headline 76/40, `06-27` 50/40, `07-10` 48/40, `07-12` 45/40, `07-13`
41/40, `07-14` 53/40, `07-16` headline 49/40 and runner-up 45/40, `07-17` 44/40, `07-20` 62/40,
`07-21` 59/40, `07-22` 57/40, `07-25` 52/40, `07-30` 41/40. Thirteen of the fourteen are headline
clusters.

**Why it matters, in the direction that hurts this practice.** U is counted over the domains visible
in the snapshot. On a truncated cluster the invisible domains can only *add* publisher units, so the
computed U is a **lower bound**, which makes `U < 3` easier to reach. That is the opposite of the
conservative direction the pre-registration chose everywhere else.

**The deviation, decided now rather than after seeing what it costs.** The primary figures for **Q1**
and **Q2** are computed over the **untruncated headline clusters only** — those whose `domain_count`
equals their masthead-list length (30 of 43). The 13 truncated headline clusters are reported
**separately**, with their U stated explicitly as a lower bound, and are never folded into the
primary number. The all-clusters figure is reported as secondary, labelled as such.

**Q3** is unaffected in kind — a cluster whose visible domains already fall below three units fails
the threshold whether or not more domains exist behind the cap — but it is reported on the same
untruncated set as Q1, and the truncated set separately.

---

## D2 — 2026-08-05, 13:18 UTC — the evidence gate is applied per member, and candidate units are never merged with each other

**State of knowledge when this was written:** Stage A had run — 233 candidate units over 596 domains,
33 of them multi-member, 22 of them touching an untruncated headline cluster. The ownership specialists
had just been convened and **had returned nothing**. **No U existed for any cluster under any rule.**

**Two things the pre-registration left open, decided now.**

1. **Confirmation is per member.** Stage A's mechanical relations produce at least one visibly mixed
   group: candidate unit 2 contains thirteen British local-newspaper domains and two American public
   radio domains (`ksut.org`, `mynspr.org`), which share nothing but a nameserver set. The
   pre-registration says an unconfirmed unit is split back into singletons; it does not say what
   happens when a source confirms *some* members. It is now fixed: **a member stays in a confirmed
   unit only if the ownership source names it; every member the source does not name is split off as
   a singleton.** Splitting is the conservative direction — it raises U and makes our own prediction
   harder.

2. **Candidate units are never merged with each other.** Several candidate units may turn out to carry
   the same operator's name, because the nameserver relation fragments a single owner across several
   hosting units. The pre-registered rule confirms or splits; it does not merge. **The primary figure
   keeps Stage A's partition**, so one owner appearing as several units counts as several units. An
   owner-merged variant will be computed and reported **as a clearly labelled secondary figure only**,
   never as the primary result.

Both decisions push the primary number away from this practice's own prediction. That is deliberate,
and it is the reason they are written before the number exists rather than after.

---

## Bookkeeping note — two commits carry the same message, and why

`5d27245` (13:06:11 UTC) and `bfe30e8` (13:06:23 UTC) have the identical message *"The evidence gate
applies per member, and units are never merged — both decided before any count."* Only the second
contains the D2 text. The first was an accidental commit: the shell heredoc that was meant to append
D2 wrote to a path that did not exist, the command failed, and the `git commit` that followed it in the
same line swept up the already-gathered nameserver and redirect data under D2's message. Nothing was
lost and nothing is concealed — but a reader diffing the two will find the second one is where the rule
actually lands, and this note exists so that discovery is not a surprise. Both precede the first unit
count (13:08:13) by two minutes.
