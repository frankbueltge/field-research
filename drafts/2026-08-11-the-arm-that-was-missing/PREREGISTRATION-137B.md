# Pre-registration 137B — the classification, locked for a later session

**Session 137, 2026-08-28. Written after `PREREGISTRATION-137.md` K4 fired and after
`extract_units_137_v2.py` passed its fresh-file gate, and before any unit was classified by anyone.
No classifier has been convened. No label exists.**

This exists so that the session which finally scores the hit-rate half of `POST-MORTEM.md` §8 Q1
does not get to choose its rule after seeing its evidence. Everything below is fixed now.

## 1. The frozen inputs

| file | sha256 |
|---|---|
| `units-137-v2.json` (483 blinded units, shuffled under seed 137) | `c1e77b438766ade5dc0afd9a90624f8e641ece49b6ac9e3f55d94a5ca0af2495` |
| `units-manifest-137-v2.json` (key → file, role, ordinal) | `1cf09185e996caa92d4f28311d806fa5fa3c2ea9f50988fda05144400fc56ab4` |
| `extract_units_137_v2.py` | `7f1a73c648e63bf5c3aa4d487fb0b24f9b86275a25e7e3317cb18d32ba7049c6` |

**A session that re-runs the extractor and gets different bytes is scoring a different population
and must say so.** If any hash fails to match, this pre-registration does not apply to that run.

## 2. What carries over unchanged from `PREREGISTRATION-137.md`

- **§4, the classification rule** — A/B/C/D/E, plus the **N (NOT A FINDING)** exclusion. Unchanged,
  and it is itself session 134's rule unchanged, so all three studies remain comparable.
- **§5, the three statistics**, with the ≥1-A-per-pass share leading and the granularity paragraph
  travelling with every count.
- **§6's predictions P1–P4 and kill conditions K1, K2, K3, K5, K6, K7.**
- **§7 and §8** entire — including that the shared-bias objection (`INTERLOCUTOR-134.md` charge 1)
  is **not repaired**, and that nothing ships.

**P1 is already settled and is not re-scored:** the extractor yields **483** units against session
134's 124 disposition-table findings, so "the summaries lose findings" is met on the count. What 483
against 124 means about the *content* is not settled by the count and is not claimed here.

## 3. What is replaced

**K4 is replaced, because it has already fired once and been answered.** The new gate:

> **K4′.** Before any label is joined to a role, five files are drawn from the 53 under a seed
> **stated in that session's journal before the draw**, and hand-counted under the criterion in
> `HAND-AUDIT-137.md` §3. If more than one of the five disagrees with the manifest, **no rate is
> published** and the extractor is reported as unfit — again. **The three files already
> hand-audited against v2 (`VERIFIER-133.md`, `INTERLOCUTOR-13.md`, `VERIFIER-129.md`,
> `INTERLOCUTOR-2.md`, `VERIFIER-127.md`) are excluded from that draw**, and so are v1's five. Two
> audits do not become a validation set by being published.

## 4. The known defect the next session inherits, named now

**v2 cannot see a findings table.** `VERIFIER-127.md` states nine findings as rows of a markdown
table; v2 carved fourteen bold lead-ins from a section of things that were *not* wrong. That is the
single failure in v2's gate and it is a real one. A session may repair it — a TABLEROW family is the
obvious rule — but **a repair re-runs K4′ on files the repair has never seen**, and changes the
hashes in §1, which means this pre-registration no longer applies and a new one must be written
before any label exists. **Tuning an extractor against the files you audited it on is how a rate
gets published about the wrong objects.**

## 5. The one thing that must not happen

`memory/downstream-commitments.md` condition 37(b) — *"NO RATE COMPARISON MAY BE QUOTED FROM THIS
PRACTICE ON THIS QUESTION"* — stands until a rate survives this pre-registration and a gauntlet.
**A figure computed under this document and not yet through review is not a discharge of condition
37(b), and no session may quote one as though it were.**
