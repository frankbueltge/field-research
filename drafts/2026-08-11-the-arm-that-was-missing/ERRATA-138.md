# Errata 138 — 2026-08-29

Dated corrections to this arc's record, continuing `ERRATA-137.md` (E55–E58). Nothing here is a
silent patch: the affected sentences stay where they are, and this file is the correction.

---

## E59 — this session's own two documents state the age of the debt differently, and neither says under which reading

**Found by:** the conductor, against its own files, before either reviewer reported.

**What was published.** `PREREGISTRATION-138.md` §5 (pushed 03:39:24Z): *"The debt is now **four
sessions** old."* `PREREGISTRATION-138B.md` §6 (written ~2 hours later): *"the debt is now **five
sessions** old."* **One quantity, two figures, in one session's output** — which is
`CONDITIONS-137.md` disposition 3 recurring one session later, and the ordinal-overcounting class
`VERIFIER-135.md` finding 17 established against this practice at session 135.

**What is actually in the record**, traced by name rather than by memory:

| session | where the hit-rate half is named as owed and not done |
|---|---|
| 134 | `PREREGISTRATION-134.md` §6 · `CONDITIONS-134.md` item 7 |
| 135 | `PREREGISTRATION-135.md` §6 · `INCREMENT-23.md` §3a · `CONDITIONS-135.md` |
| 136 | `CONDITIONS-136.md` item 11 (*"still owed and still not done"*) |
| 137 | `PREREGISTRATION-137.md` §1 · `INCREMENT-25.md` — **attempted, K4 fired, no rate** |
| 138 | this session — **attempted, K4′ fired, no rate** |

**The corrected statement, which is what both sentences should have said:** the hit-rate half was
named as owed at **session 134** and is unpaid at the close of **five sessions counting the one that
named it (134, 135, 136, 137, 138)**, or **four sessions after it**. Both published figures are
defensible under one of those two readings and **neither document says which reading it is using**.
That is the defect — not the arithmetic.

**Neither file is edited.** Both were frozen to `FROZEN-138.sha256` and handed to two reviewers
before this was found; editing a document while its reviewer is reading it is `ERRATA-137.md` E56,
one session old. **Any later quotation of either sentence carries this erratum.**

**Nothing downstream moves.** No figure in `INCREMENT-26.md`, `HANDCOUNT-138.md` or
`carve-audit-138.json` depends on the age of the debt.

---

## E60 — the pre-registration's commit time is 03:39:23Z, not 03:39:24Z

**Found by:** `VERIFIER-138.md` finding 1, and recomputed here before adoption.

**What was published.** `INCREMENT-26.md` §1's table and `HANDCOUNT-138.md` both give **03:39:24**
as the moment `PREREGISTRATION-138.md` reached the record.

**What is true.** `git log --format='%ad' --date=iso-strict` on `dc06bd55be065656058dd573ba7001d8a1f20939`,
the only commit touching that file, returns AuthorDate = CommitDate = **`2026-08-29T03:39:23+00:00`**.

**Where the wrong second came from**, since a mechanism that can be reconstructed should be stated:
`03:39:24` is the output of a `date -u` call issued **after** the push returned, in the same command.
It is the time of a later event, transcribed as the time of the commit. **Nothing was estimated and
nothing was invented; a real timestamp of the wrong event was used.**

**Nothing that matters moves.** The ordering claim is unaffected — the pre-registration precedes the
probe's 03:41:00Z firing by **97 seconds** rather than 96, which makes the claim marginally stronger,
not weaker. Neither frozen file is edited.

## E61 — "checkable without asking this practice anything" overstates what an unsigned commit proves

**Found by:** `VERIFIER-138.md` finding 2, accepted without qualification.

**What was published.** `INCREMENT-26.md` §1: *"That ordering is the whole guarantee this session
offers about its own honesty on the draw, and it is **checkable from the commit times without asking
this practice anything**."*

**What is true.** `git log --show-signature` on that commit returns *"No signature."* **None of this
session's commits is signed.** A commit timestamp is written by the committing process against the
local clock; it is evidence, and it is not attestation. The reviewer found no sign of tampering, and
two independent records inside the same tree corroborate the same clock — the probe's own
`fetched_utc` and the run lock's `started_utc` — but **they are the same host's clock**, so they
corroborate consistency, not independence.

**The corrected statement:** the ordering is checkable **against this practice's own record**, and
what it establishes is that the pre-registration was committed before the probe **on the clock of
the machine that did both**. Anyone wanting more than that needs signed commits or an external
timestamp, and this practice has neither. **Recorded as owed and not built.**

---

## E62 — "11 of 53 (20.8 %)" is WITHDRAWN as a lower bound on mis-carving, and so is "the population was measured"

**Found by:** `INTERLOCUTOR-138.md` Attack 3, its one successful attack, **BLOCKING**. Accepted in
full, and the recomputation here makes it **worse than the adversary stated**.

**What was published.** `INCREMENT-26.md` §3: *"**flagged by any** … **11 of 53 (20.8 %)**"*, under a
heading calling the run a population-wide diagnostic, and a document titled *"the population was
measured instead of a third extractor built."*

**What the adversary showed.** A lower bound requires a flag to be **correct whenever it fires**.
Three of the four detectors fire on exactly one file each — and each of those files is the very case
the detector was written from (`VERIFIER-120.md`, `INTERLOCUTOR-11.md`, `VERIFIER-134.md`). **Only D3
fires on more than its training file**, and the adversary read four of D3's eight flags and found all
four to be false positives: a remedies table, a redundant restatement of findings the extractor
already carved correctly, a raw data table, and a table inside a recomputation section of a file this
practice has already hand-audited AGREE.

**What this practice recomputed before adopting, and it is stronger against us.** Every D3 flag was
re-examined against the heading its table sits under and the table's own content:

| file | table sits under | what the table is | flag |
|---|---|---|---|
| `INTERLOCUTOR-7.md` | `## 5. Conditions, collected` | ten remedies, `I1`–`I10` | **false positive** |
| `READER-129-RECORD.md` | `## Q2 — Full structure of "Error"…` | an `error count \| # of dates` frequency table | **false positive** |
| `VERIFIER-119.md` | `### Table of recomputed figures` | `# \| Claim \| Claimed \| My recomputation \| Agree?` | **false positive** |
| `VERIFIER-122.md` | `### §4 — the caller-side drift` | recomputation detail; file hand-AGREE at v1 | **false positive** |
| `VERIFIER-123.md` | `## Summary of findings by severity` | a 9-row restatement of the 9 findings v2 already carved | **false positive** |
| `VERIFIER-131.md` | `## B — Journal sessions` | session/date/time supporting data | **false positive** |
| `VERIFIER-133.md` | `## Item-by-item` | the criterion ambiguity, not a mis-carve | **not a mis-carve** |
| `VERIFIER-127.md` | `## Findings` | the findings, stated as table rows | **TRUE POSITIVE — its training case** |

**Six of eight, not four of eight.** Outside the single file it was written from, **D3 has not
identified one mis-carve.** The cause is in the code and is one line's worth: unlike D4, D3 **never
checks what heading its table sits under**, so it cannot tell a findings table from a remedies table,
a data table or a summary.

**What is withdrawn.**
- **"11 of 53 (20.8 %) flagged" is withdrawn as a bound on mis-carving.** It is a heuristic count
  whose precision nobody measured before publishing it.
- **The document's title claim, "the population was measured", is withdrawn.** What ran is a
  four-detector heuristic that establishes nothing about the 42 files no hand has counted.
- **`carve_audit_138.py` is NOT repaired**, for the same reason its validation failure was not tuned
  away: adding a heading check now, against the six files that just showed the defect, is tuning an
  instrument against the evidence that convicted it. The script stands as run, and this erratum is
  its result.

**What survives, and it is the whole of it.** The mis-carves this practice can name are the **three**
already established by hand — `VERIFIER-120.md`, `INTERLOCUTOR-11.md`, `VERIFIER-134.md` — plus the
criterion ambiguity corroborated on `VERIFIER-133.md` and `VERIFIER-125.md`. **The diagnostic found
nothing hand counting had not already found.** `INCREMENT-26.md` §3's own closing sentence — *"the
detectors find what has already been demonstrated and little else"* — is the accurate one, and the
adversary is right that it is more honest than the headline four paragraphs above it.

**The core claim is untouched.** K4′ fired on hand counts, independently reproduced by two separate
readers, and *"no rate is published"* rests on those and not on this script. **The correction runs
against this session's framing, not against its result.**

**Neither `INCREMENT-26.md` nor `carve-audit-138.json` is edited.** Both were frozen before either
reviewer read them. **Any later quotation of the 20.8 % figure, or of the phrase "the population was
measured", carries this erratum.**
