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

---

## D2 — the dispatched prompt gave the readers an example the locked rule does not contain

**Found:** 2026-08-07, by round 3's Skeptic, two days after the run and after two prior gauntlet
rounds missed it. This file exists to catch exactly this and did not.

**The gap.** `RULE.md` §5 offers `UNDECIDABLE` and argues why, but gives no example of when it
applies. Both dispatched prompts do: *"for instance when a source is a general framework or
benchmark whose stated domain neither clearly is nor clearly is not a research cycle"*
(`prompts/reader-R1.txt:335`, identically in `reader-R2.txt`). That sentence is in neither the
locked rule nor any prior deviation entry.

**Why it matters, checked rather than asserted.** It names a category and steers toward one verdict
for it, and that category is over-represented in the movements the study reports. Recomputed from the
committed files on 2026-08-07: of the 39 published-IN cases **13** carry a
bench/benchmark/evaluat/audit/suite word in the title; of the **14** unique cases either reader moved
to OUT, **8** do — ~57 % of the movements against a ~33 % base rate. It does not overturn the result:
the readers' stated exclusion reasons are about the system described, not the title word, and the
movements run one way whether or not those eight are counted. But the prompt is not neutral with
respect to the finding, and the record should have said so from the first day.

**Resolution.** Not rewritten, not re-run — the returns are what they are, and editing a prompt after
the fact would be worse than the defect. It is logged, the arithmetic published, and `README.md` §6
carries the correlated-reader limit this sits inside. Any reuse of `prompts/` should know it carries
an example the rule does not.
