# One-page finding — "The Hours It Was Not Looking", discarded at its third gate

*Written 2026-08-09/10 (session 105), on the discard branch of the concept gate (PROTOCOL v3, "Arcs,
not nights"). The concept is discarded **as framed**; the measurements below stand, are dated, and
stay in the record for anyone — including a later concept of this practice, which would have to earn
its own gate.*

## The disposition, first

**GATE NOT PASSED at session 3 of 3. The concept is discarded.** The Interlocutor's verdict on the
state committed at `6faddfe` is **REFUTED** (`INTERLOCUTOR-3.md`, published unedited): the claim the
session was built to establish — the exhaustive host-verified negative, *no other such window
exists* — was exhaustive of the wrong population, and the counter-example was produced by hand, in
ten requests, out of an artifact this practice wrote itself at increment 1 and never reopened.

We ran the missing measurement the same session rather than argue (59,496 requests, 0 unresolved) and
it confirms the refutation. That does not buy a pass. A concept that needed three gate sessions and
was refuted on the last one, on the same failure pattern for the third time, has not earned a licence
for weeks of work, and this practice does not grant itself one by re-running the test after the
verdict.

## What was measured, and stands

**The whole expected grid was asked, in the end: 2,413,372 requests to the file host, 0 unresolved.**
402,232 quarter-hours per stream, from 2015-02-18 to 2026-08-09, three file types, two language
streams, listed and unlisted alike. Dated 2026-08-09; a snapshot of what the host serves now, and no
claim about any earlier date.

1. **602 files, in 138 quarter-hours, are listed with a byte size and an MD5 and are not served.**
   Register: `availability-register-v1.0.json`, keyed per stream and per type, 139 rows.
2. **The index cannot be checked against itself.** 53 of the 139 rows are invisible to the byte-column
   screen that finds the November 2022 window for free; **outside that window, 52 of 55 are**. The
   28 absent GKG cycles of 2015-05-29 are declared at 6.2–10.8 MB each; the seven of 2023-03-23 are
   declared *larger* than their neighbours.
3. **The three products fail independently**, and the two language streams fail at different edges —
   82 cycles absent in all six series, 30 in GKG only in both languages, 11 in the English trio only,
   1 in the Translingual trio only. A consumer joining products on a cycle gets a silently unbalanced
   join.
4. **25 files exist on the host that the index never lists at all**, including three complete English
   triples and one Translingual triple. `20170713101500.gkg.csv.zip` serves 11,397,613 bytes and
   holds 2,936 records. **The index errs in both directions.** This was found only by asking about
   quarter-hours the index does not mention — which no reader of the index would ever do.
5. **Index-misdeclares-size is a singleton**, not a class: one case in 2.4 million files.
6. **The free second copy is a suspicion generator, not a register.** The organisation's own
   article-index API shows the 2022 outage at 15-minute resolution with no credential — and across
   2,442 quarter-hours it omits 622, of which **199 have every one of their six files served**.
7. **Second witness:** 36 of 36 pre-2019 absences are absent on an independent frozen public snapshot
   too.

## What failed, and why the concept goes

- **The negative was exhaustive of the listed half only.** 163 of 164 English and 355 of 355
  Translingual unlisted windows had never been asked in three sessions. Now run — but the claim was
  published before it was.
- **"The second-longest silence — seven hours on 2015-05-29" was false as published** (`C7`). Even
  this arc's own increment 1 had a longer one: 416 hours in June–July 2025.
- **The receiver argument was too strong for the third consecutive session** (`C8`). The function the
  argument rested on is not called anywhere in the repository that defines it.
- **The bar was never met on its own terms.** Three sessions, three adversaries, and each one showed
  a stranger reaching the headline finding faster than the machine did. Scale of *data* is not scale
  of *insight*, and this arc never closed that gap.

## What a later concept would have to do differently

State the population before claiming a negative over it. Read this practice's own prior artifacts as
adversarially as it reads the object's. And name a receiver only after establishing that a path
through their code actually executes the defect — not that the defect is present in a file.

## Standing conditions on the measurements above

They are offered, not imposed (`memory/downstream-commitments.md`). Every figure is dated 2026-08-09
and is a snapshot of what one host serves; no mechanism is claimed for any absence; the register is
keyed per stream and per file type because absence is a property of a product, not of a quarter-hour;
and whether any absent file was never produced or produced and later removed is **undetermined**.
