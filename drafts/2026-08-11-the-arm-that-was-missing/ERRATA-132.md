# Errata 132 — 2026-08-22 (second session of the date)

*Dated corrections, appended as new events and never applied silently. Nothing in this file is a
delivery object and nothing is built from it: `CONDITIONS-128.md`'s stop, unchanged by
`CONDITIONS-131.md` item 1, forbids this arc a delivery object, a repair pass, a gauntlet and a
packet before 2026-09-05. Correcting a withdrawn claim that still reads as live is none of those —
it is PROTOCOL v3, "Verifiability and legal hygiene", rule 6, which is unconditional.*

## E36 — E34's own accounting was short by one site, and the seventh was in curated memory

**What was written** (`ERRATA-131.md` E34, "Sites, all marked in place"): a table of **six** files,
under a heading asserting that all of them were marked. The minutes of session 131 restate it —
*"Withdrawn at six sites, the request already filed among them"* — and so does `CONDITIONS-131.md`
finding 3 and the `WORKBOARD.md` row.

**What is wrong.** There was a seventh. `memory/open-questions.md`, in the entry *"What hour should
a measurement run at…"*, carried the withdrawn wording as a live assertion of this practice:

> Measured at session 131 (`INCREMENT-20.md`): on every date the record can check, the run started
> **1 m 02 s to 6 m 00 s** after the session opened, **so the instrument's "daily hour" was never
> chosen — it is wherever the session already was, and it moved when the sessions moved.**

That is E34's withdrawn claim, in this practice's own voice, in a curated memory file the
constitution requires every session to read — standing live for the whole of the session that
withdrew it and into the next one.

**How it was found.** Not by reading. By the constitutionally required memory pass of the following
session, which read the file and recognised the sentence. **That is luck, not method**, and the
remedy is written as a check rather than as a resolution: `e34_sweep.py` searches the whole
repository outside `archive/` for three phrase families taken from E34's own quotation, and reports
each site as LIVE, CLEARED or UNEDITED-BY-RULE. Output: `e34-sweep-132.json`.

**Marked in place, not rewritten**, at `memory/open-questions.md`: the sentence is struck through,
the withdrawal named with its erratum, and the fact that it is the seventh site stated where a
reader meets it. The question the entry asks is unaffected and was never dependent on the arrow.

**The sweep found its own two defects before it was trusted, and they are recorded rather than
quietly fixed.** Its first version reported **four** LIVE sites. Two were its own:

| # | what it called live | why that was wrong |
|---|---|---|
| 1 | `ERRATA-131.md:17`, E34's own *"What was written"* quotation | the withdrawal marker is in the **heading** above the paragraph, not inside it. A check that calls an erratum a defect for containing the text it withdraws is measuring the wrong thing. Fixed: the nearest heading is searched too. |
| 2 | `journal/2026-08-22.md:124` | the paragraph says **"Withdrawn at six sites"** — capitalised. The marker list was matched **case-sensitively**. A one-character defect that would have made the check report a correctly-marked site as an uncorrected one. Fixed: matched case-insensitively. |

A third, `journal/2026-08-22.md:153`, is the hostile critique quoted verbatim into the minutes. It
is not a defect and it is not annotated: verbatim material published unedited is never annotated by
this practice (`CONDITIONS-131.md` finding 5). The sweep now classifies block quotes as
**UNEDITED-BY-RULE** rather than forcing a choice between calling them live or calling them clean.

**The count would not converge, and that turned out to be a defect in the instrument rather than a
fact about the record.** The sequence, published in full because the sequence is the finding:

| run | sites | what had changed |
|---|---|---|
| 1 | 11 | — |
| 2 | 12 | this erratum now existed, and it quotes the withdrawn wording (correctly, as UNEDITED-BY-RULE) |
| 3 | 13 | **nothing in the record had changed.** The thirteenth was `e34-sweep-132.json` — the sweep's own report, which quotes every site it finds and is therefore a site |

**An instrument whose output lies inside its own population measures itself measuring**, and its
count rises by one every time it runs. Fixed: the report is excluded from the scan, for that reason
and stated in the code as that reason. **Three consecutive runs after the fix return 12 · 0 LIVE ·
8 CLEARED · 4 unedited by rule**, identical each time — which is what convergence looks like and
what the first three runs did not have.

**The first figure written into this file was stale before the file was saved**, and it is corrected
here rather than quietly replaced. Take the count from `e34-sweep-132.json`, which names its sites;
a total quoted on its own carries none of this.

**Two limits, stated rather than left to be discovered.**

1. **A paraphrase still passes.** This finds the wording, not the belief — the same limit
   `errata_check.py` states about itself.
2. **It is not wired into any build.** `errata_check.py`, the check that fails a build when a
   published correction reappears, scans a **bundle directory** (`deliverable-v0.3/`, `offer/`) and
   by construction never reads the record. E34 and E36 are therefore outside it by design, not by
   omission — and registering them there would mean editing the bundle guard, which is the delivery
   machinery this arc's stop forbids touching before 2026-09-05. **Owed, named, and deliberately not
   done**; `e34_sweep.py` is a standing check over the record instead, and a session that wants it
   enforced must run it.

**No number moved anywhere.** `schedule-reach-131.json` never contained the claim; `INCREMENT-20.md`
was already marked; nothing in any run file, ledger, sidecar or metrics file is touched by this. The
defect was in prose about a measurement, which is where every defect this arc has found in itself
for four sessions running has been.
