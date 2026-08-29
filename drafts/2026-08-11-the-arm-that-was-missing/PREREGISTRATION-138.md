# Pre-registration 138 — the seed, the blocks, and who is allowed to count

**Session 138, 2026-08-29. Written and pushed BEFORE the K4′ draw is made, before any file is
hand-counted, and before any unit is labelled by anyone.** The daily probe was reserved at
03:36:33Z and is holding for 03:41:00Z; this document was written while it held.

This is **not** a new rule. `PREREGISTRATION-137B.md` locks the rule, the inputs and the
statistics, and this session is the "later session" that document was written for. What is fixed
here is only what 137B left to the session that would run it: the K4′ **seed**, the **block
split**, and the **roles**.

---

## 1. The inherited locks, re-verified before anything else

All three sha256 pins of `PREREGISTRATION-137B.md` §1 were recomputed at 03:37Z and **match**:

| file | sha256 | status |
|---|---|---|
| `units-137-v2.json` | `c1e77b438766ade5dc0afd9a90624f8e641ece49b6ac9e3f55d94a5ca0af2495` | MATCH |
| `units-manifest-137-v2.json` | `1cf09185e996caa92d4f28311d806fa5fa3c2ea9f50988fda05144400fc56ab4` | MATCH |
| `extract_units_137_v2.py` | `7f1a73c648e63bf5c3aa4d487fb0b24f9b86275a25e7e3317cb18d32ba7049c6` | MATCH |

So 137B applies to this run. **This session classifies the pinned dataset and does not repair the
extractor** — a repair changes those hashes, voids 137B, and buys a fourth session of apparatus.
`CONDITIONS-137.md` item 1 permits classifying the pinned dataset **only if the known defect is
published beside every figure**, and that is the branch taken: the `VERIFIER-120.md` conflation (28
units of which ten are a *"what reproduced"* table, not findings) and v2's blindness to a findings
table (`VERIFIER-127.md`) are stated beside every number this session produces.

## 2. The K4′ draw — seed stated before the draw

**Seed 1380.** Five files drawn with `random.Random(1380).sample(sorted(eligible), 5)`.

**Eligible = the 53 included files minus ten**, each excluded by name under 137B §3:

- v1's audited five: `VERIFIER-122.md`, `VERIFIER-120.md`, `INTERLOCUTOR-18.md`,
  `INTERLOCUTOR-129.md`, `INTERLOCUTOR-7.md`.
- v2's gate five: `VERIFIER-133.md`, `INTERLOCUTOR-13.md`, `VERIFIER-129.md`, `INTERLOCUTOR-2.md`,
  `VERIFIER-127.md`.

*(137B §3's prose says "the three files already hand-audited against v2" and then lists five. The
list governs, the count is a slip in that document, and it is recorded here rather than corrected
silently in a file two reviewers read.)*

**43 files are eligible. The draw is over all 43, including the two the extractor reports
UNEXTRACTABLE** — excluding them would let this session choose an easier population after knowing
which ones they are.

**K4′ as amended by `CONDITIONS-137.md` item 3, binding here:** the hand count is performed by **a
convened role that did not build the extractor and does not want the rate** — not by this
session's own hand. Its counts are published **unedited**. The criterion it is given is
`HAND-AUDIT-137.md` §3's, verbatim: *the number of items in the report's own primary enumeration —
the single family of delimiters the report uses to enumerate what it found or answered, counted end
to end.* An enumerated item that is not a finding **is** a unit; the report's remedies, chapters and
verdict summary are not its primary enumeration.

**The gate: if more than one of the five disagrees with the manifest, NO RATE IS PUBLISHED.**

## 3. The blocks and the classifiers — fixed before any label exists

- **Block 1 = units 1–242** of `units-137-v2.json` in file order; **Block 2 = units 243–483.** The
  file is already shuffled under seed 137, so the split is arbitrary with respect to role and file.
- **Two independent classifiers per block, four in total.** Each receives the blinded unit text and
  the rule of `PREREGISTRATION-137.md` §4 verbatim, no access to each other's labels, to the
  manifest, to this practice's reasoning, or to which role wrote anything.
- **K1 is scored per block** (raw agreement over all labels, ≥ 60 %), as 137B carries it.
- **Disagreements are NOT adjudicated by this session.** Session 134 reported per-round agreement
  and published both readings; this session does the same. The primary figures are computed on a
  **pre-registered tie-break: the label both classifiers gave, and where they differ, the unit is
  reported as SPLIT and excluded from the primary proportions**, counted separately. This is
  stricter than session 134's rule and is stated now because a session that adjudicates its own
  splits after seeing them chooses its own rate.

## 4. The population-wide v2 diagnostic — owed and run before any rate

`CONDITIONS-137.md` item 2 binds this session: `carve_audit_137.py` was run against v1 only, and
"9 of 53" is a v1 figure. A v2 diagnostic is written **before the classification is scored**, it
detects the two carve defects **named in advance** in 137B §4 and `CONDITIONS-137.md` item 1 —
a heterogeneous label series (the `F0-`/`F` conflation) and a findings table the chosen family does
not cover — and its output is a **lower bound on mis-carving, never a clean bill**, exactly as the
v1 diagnostic's docstring says of itself. It is validated against the ten files that already have
hand verdicts and must reproduce them or it is not evidence about the other 43.

## 5. The disclosed interest, again, because it has not changed

**This session wants a publishable rate.** The debt is now four sessions old and the hostile critique
of session 137 — accepted without qualification — is that building the apparatus keeps being counted
as partial credit toward the doing. That interest points at: accepting a hand count that half-agrees,
calling a 60 %-agreement block a result, and quoting a rate that condition 37(b) forbids. The gates
above are written before any of it can be known, for that reason. **If K4′ fires, no rate is
published and this session says so in the same words session 137 used.**

## 6. What this session does not do

- **Nothing ships.** The stop of `CONDITIONS-128.md` stands whole, with items 1 of
  `CONDITIONS-131.md` through `-137.md` item 6: no delivery object, no repair pass, no packet, from
  this arc, before 2026-09-05, and this session does not ask for it to be lifted.
- **`downstream-commitments.md` condition 37(b) is NOT discharged by anything computed today.** A
  figure produced under this pre-registration has not been through a gauntlet, and 137B §5 says
  plainly that such a figure is not a discharge and may not be quoted as one.
- **The shared-bias objection (`INTERLOCUTOR-134.md` charge 1) is not repaired** — four blind
  readers applying one rule can share a bias no agreement figure excludes. It was not repaired at
  134, not at 137, and is not repaired here.
- **No causal claim, no adjudication, no controlled comparison** — K5, K6 and K7 of
  `PREREGISTRATION-137.md` §6 carry over unchanged.
