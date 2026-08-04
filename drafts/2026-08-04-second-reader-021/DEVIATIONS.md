# Deviations from RULE.md

Every departure from the locked rule, with the reason, in the order they were found. A rule
without a deviations file is a rule nobody tested.

---

## D1 — the rule does not say where an UNDECIDABLE case sits in that reader's population

**Found:** while writing `scripts/score.py`, **before either reader returned** — the readers were
already running, and neither reader's file existed yet. Timestamped by the git history: the
scoring script is committed before `reader-R1.json` and `reader-R2.json` are added.

**The gap.** `RULE.md` §6 fixes that an `UNDECIDABLE` verdict counts as *disagreement* with any
binary verdict in the agreement metrics. It does not say whether that case is inside or outside
that reader's **population** when §8's tables are recomputed. Both readings are defensible: a
reader who cannot decide has not put the case in the population (exclude), or the population is
the set the reader did not rule out (include).

**Why it matters.** It is a researcher degree of freedom, and it sits directly on the number under
audit — n, and therefore every share computed over n.

**Resolution.** Neither branch is chosen. `score.py` computes and `results.json` reports **both**,
and §8's band is evaluated **twice**, once under each. Where the two disagree, both are published
and the finding is stated at the weaker of them. This is the only honest resolution available for
a gap found after the rule is locked: picking one branch now, with the readers already running,
would be choosing a rule with partial sight of what it decides.

**Not a rewrite.** `RULE.md` is not edited. The gap is real, it stands in the locked text, and
this entry is the record of it.
