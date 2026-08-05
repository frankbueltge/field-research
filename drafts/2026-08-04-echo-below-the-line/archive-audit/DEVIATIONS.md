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
