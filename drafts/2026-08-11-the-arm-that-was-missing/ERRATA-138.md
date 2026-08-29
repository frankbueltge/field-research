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
