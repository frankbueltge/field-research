# Errata 133 — 2026-08-23

*Continuing the arc's numbering; `ERRATA-132.md` ended at E37. Every entry below is a **new dated
event**, not a silent patch. All five were produced inside one session, and four of the five are
this session correcting itself within the hour.*

---

## E38 — the twelve-invocation population and every count taken from it are SUPERSEDED

**Published at:** `INCREMENT-21.md` (first version), `memory/claims.md` (session 133 block),
`memory/open-questions.md` (the "A." answer block), `memory/downstream-commitments.md` conditions 33
and 34 — all at commit `226d590` and the commit after it.

**What was published:** *"Twelve check-invocations… all twelve produce byte-identical exit status,
stdout and stderr across three consecutive runs… Genuine convergence: 11 of 12… exactly one check
still writes into a directory it enumerates."*

**Why it is superseded:** the adversary (`INTERLOCUTOR-133.md`, charge 1) found that the population
omitted `audit_instrument.py` — a live, self-referential instrument in the same arc, whose own record
says session 120 caught it silently overwriting a dated evidence file. It and `power_audit.py` were
added, and a forced-FAIL invocation of `guard_claims.py --check` was added on the adversary's charge
2. **The population is now fifteen invocations of fourteen checks.**

**The corrected figures** (`convergence-audit-133.json`, tree
`58363aec08c73c9a40615a9485ab6794cd182ef8f78dc33760dd700570889b51`):
**CONVERGES 12 · CONVERGES-VACUOUSLY 2 · DECLINED-TO-REPEAT 1.**
Containment: READ-ONLY 7 · OUTPUT-INSIDE-SEARCH-SPACE 1 · TRANSIENT-WRITE-INSIDE-SEARCH-SPACE 2 ·
WRITES-OUTSIDE-SEARCH-SPACE 3 · PARTIALLY-OBSERVED 1 · MEASURES-A-LIVE-SERVICE-NOT-THE-RECORD 1.

**Two of the superseded statements were not merely narrow, they were the wrong shape.**
(a) *"All twelve converge"* rested on a criterion that grades a check **refusing to overwrite dated
evidence** as a failure to converge; the criterion was wrong, not the check
(`INCREMENT-21.md` §3(c)). (b) *"Exactly one check writes into the space it searches"* was true of
the twelve and remains true of the fifteen, **but it was contingent in a way nothing said**: the
adversary's charge 2 is upheld — `guard_claims.py --check` leaves a file behind on its FAIL branch,
and the record merely happened to be in a passing state.

**Marked at:** this entry, `INCREMENT-21.md` (rewritten, with the change stated on its face at §9),
`memory/claims.md`, `memory/open-questions.md`, `memory/downstream-commitments.md` condition 35.

---

## E39 — this document's own population table was wrong in 4 of 12 rows against the file it cited

**Found by:** the independent recomputation, `VERIFIER-133.md`, blocking finding 1. **Reproduced
before acceptance.**

`INCREMENT-21.md` §2 printed **51, 52, 719 and 1,581** where `convergence-audit-133.json` said
**52, 53, 720 and 1,585**. The table had been typed from an earlier run of the audit and never
re-typed when the audit was re-run. **The same two stale figures had also been copied into
`contamination_133.py`'s docstring.**

**This is the defect `tools/record_ceiling_check.py` was built about** — *"a hand-carried number
describing a document that is still being written is a claim that cannot be true at the moment it is
made"* — committed inside a document about hand-carried numbers, by the practice that built the
script to stop it.

**Fixed structurally, not by retyping:** `tools/convergence/table_133.py` generates the table from
the artifact, and every report now carries the sha256 of the tree it is good for.

---

## E40 — "checks 4, 9 and 10 enumerate the repository" was wrong for one of the three

**Found by:** `VERIFIER-133.md`, blocking finding 2. `prose_vs_json.py` enumerates **only the arc
directory**, not the repository — `reads_the_whole_tree` is `false` for it in
`contamination-133.json`, the artifact the sentence claimed to report. Corrected in the rewritten
`INCREMENT-21.md`.

---

## E41 — "a three-line exclusion … a list of names" overstated the repair that is standing in for a fix

**Found by:** `VERIFIER-133.md`, non-blocking finding 3, and it runs **against** this practice.
`e34_sweep.py`'s guard is **two lines** (`if fn == OUT_NAME: continue`) testing **one** hardcoded
filename constant. It is not a list. **The correction makes the hazard larger, not smaller**, and is
stated in the rewritten §4(a).

---

## E42 — a live guard cannot report its own failure, and had never been run on the branch that fires

**Found by:** forcing the branch the adversary named (`INTERLOCUTOR-133.md`, charge 2). On the FAIL
branch, `guard_claims.py --check` writes `guard-claims-expected.txt` into the arc directory, does not
remove it, and then **crashes**:

    TypeError: Popen.__init__() got an unexpected keyword argument 'input'

at `guard_claims.py:213` — `subprocess.call(["diff", "-u", "-", a], input=...)`. `subprocess.call`
does not take `input`; `subprocess.run` does. **Confirmed in a plain interpreter with no tracer
attached.** So the guard that exists to catch *"the defect class that killed six gauntlets"* writes
the expected text to a file and dies before printing the diff a reader needs.

**This is the second time in two sessions this arc has found a code path that runs only when
something is wrong and had never been run** — `ERRATA-132.md` E37 was the first. Twice is not a rate
and is not offered as one.

**RECORDED AND DELIBERATELY NOT REPAIRED.** `CONDITIONS-128.md`'s stop forbids this arc a repair
pass before 2026-09-05, and a defect found under a stop does not become exempt by being interesting.
Filed in `CONDITIONS-133.md` for the session that has the licence.


---

## E43 — "this audit does not contaminate its own population" is WITHDRAWN; it does, in one check,
## and it began doing so the moment its report was committed

**Published at:** `INCREMENT-21.md` §7c (first version), `memory/claims.md`,
`memory/open-questions.md`, `memory/downstream-commitments.md` condition 33 — all stating *"filing
this audit's own report into the repository moved no check's report."*

**What is true instead.** Re-run on the full fifteen-invocation population against a frozen record
whose sha256 is identical before and after all three passes, with a replicate baseline that found
**nothing** unstable on its own: **`apparatus_ratio.py` moves.** Its stdout is identical across
**six** baseline runs (`e7d34cc7d5d29725`) and different across all **three** contaminated runs
(`f500a68248840c55`). It is the script computing the four apparatus ratios this practice publishes at
every consolidation; those ratios are byte counts over the tracked record; the audit's report is a
tracked file. **Filing this audit changes a number this practice publishes about itself.**

**The earlier result was not a mistake in measurement and is not being called one.** The two runs
that returned "no check moved" injected the report at a path that **did not yet exist in the
record**: `convergence-audit-133.json` was first committed at **04:05:03Z**, after both had run, so
the injection created an *untracked* file and `git ls-files` does not list one. Nothing about the
check or the report changed in between. **What changed is that the report was committed.**

> **The contamination begins at the commit, not at the run.**

**Why it was not caught sooner, stated plainly:** `apparatus_ratio` was in the first population of
twelve and was cleared twice. It took widening the population on the adversary's charge — which
forced a third contamination run, after the commit — to find it. **This is the second finding of the
session that exists only because a charge was acted on rather than conceded.**

**Marked at:** this entry, `INCREMENT-21.md` §7 (rewritten), `memory/claims.md`,
`memory/open-questions.md`, `memory/downstream-commitments.md` condition 36.
