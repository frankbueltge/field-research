# Concept — "Who Actually Reads It"

> **DISPOSITION, 2026-08-10 (session 106): GATE NOT PASSED. THE CONCEPT IS DISCARDED as framed.**
> Interlocutor verdict **REFUTED** (`INTERLOCUTOR-1.md`, published unedited), reproduced by this
> practice before acceptance (`REFUTATION-REPRODUCED.md`). Two sentences of this document are false
> as written and are struck below in place, not deleted: the "31 %" and the "no sampling gets you"
> justification (`CORRECTIONS.md` C5, C6). One page: `FINDING.md`. The measurements stand.

*Third concept for the assigned investigation (PROTOCOL v3, "The first investigation"). Opened
2026-08-10, session 106. **Gate session 1 of at most 3.** The two concepts before this one failed at sessions
102 and 105; the ambition audit has this arc on the short leash.*

## The claim, in one page

A large public measurement infrastructure publishes, every fifteen minutes, three data files and a
master list that names every file it has ever produced, with a byte size and an MD5 beside each. This
practice measured that list exhaustively on 2026-08-09 — 2,413,372 requests, 0 unresolved — and found
**602 files, in 138 quarter-hours, that the list promises and the host does not serve**, plus 25 files
the host serves that the list never mentions.

That was a finding about the object. The claim this concept makes is about **what happens to it
downstream**:

> **The infrastructure's broken promises arrive in a researcher's analysis as ordinary data.** The
> two most reachable client libraries for this infrastructure return, for a day on which 75 of 96
> quarter-hours are absent, a result that is structurally identical to a complete day: no exception,
> no field marking incompleteness, no count of what was skipped. A researcher receives **21 of the
> day's 96 quarter-hours** and nothing in the value they are handed says so.

~~*(The neighbouring complete day returns 96 cycles and 116,317 rows against that day's 36,005. That
is a control, **not** a counterfactual: what 11 November 2022 would have held is unknowable, because
the files do not exist to be counted.)*~~ **WITHDRAWN AND REPLACED, `CORRECTIONS.md` C5.** What the
day would have held is **not** unknowable: the index declares a byte size for every absent file.
Summed and calibrated against 25 downloaded files of comparable declared size, the 75 absent files
held on the order of **4,260 events**, so the complete day held roughly **40,000** and the client
returns about **89 %** of it. Earlier drafts of this document said 31 %. That was false.

This is established, not conjectured: both libraries were installed unmodified from the registry and
run. They return the same 36,005 rows over the same 21 of 96 cycles, against 116,317 rows over 96
cycles on the control day — and the 21 cycles are exactly the 21 that this practice's own register
says are served. `RESULT-1.md`, `classification-v0.1.json`, `demonstration-*.json`.

The census also found a shape behind it — **and the adversary showed the shape does not hold outside
this census.** As written: *the packages that read the master list verify its checksums and stop; the
packages that skip quietly never read it.* Inside the Python and R registries that is true, but only
after correcting a cell that was wrong when the sentence was written (`CORRECTIONS.md` C7), so it was
true by accident. Outside them it is **false**: `gdelt-toolkit` on npm parses the published checksum
out of every line of the master list and verifies nothing (`CORRECTIONS.md` C8). So the
information the index carries (this file was promised; it is 618,971 bytes; here is its MD5) reaches
nobody who could act on it, and the consumers who fail quietly have no way to distinguish "the
instrument produced nothing here" from "the instrument produced something and it is gone."

~~**The reason this practice is the one that could find it:** the claim needs the object measured
exhaustively first — a negative over 2.4 million files that no sampling gets you…~~ **WITHDRAWN,
`CORRECTIONS.md` C6.** The demonstration day is the longest run in the index's own byte column by a
factor of fourteen and falls out of this practice's own screen, index-only, in **8.94 seconds**. The
exhaustive sweep is not free, but **this finding did not need it**. That withdrawal is what decides
the gate.

## The named receiver outside the house — **never named, and now never will be**

Nothing here names a receiver. That is not an oversight; it is the whole design of this gate session.

Three consecutive concepts of this arc died on a receiver argument that had not been checked against
the receiver's own source. Session 105's finding wrote the rule:

> *name a receiver only after establishing that a path through their code actually executes the
> defect — not that the defect is present in a file.*

So this session established the executing paths **first** and named nobody. The candidates are now
concrete — a small, enumerated set of maintainers whose code demonstrably produces a wrong answer,
and a research community that may or may not have consumed those answers — and gate session 2 decides
among them **on evidence about who is exposed**, not on plausibility. **The gate cannot pass until it
does.**

## The first checkable increment — **DONE this session**

`RESULT-1.md`. Population declared before the census; 867,935 project names screened exhaustively;
19 packages' source obtained from the registries themselves; 19 fetch paths classified with
file-and-line citations; **4** executed against a dated, measured outage. Pre-registered at `8e33d25`
before the first request; four predictions held, one part-failed, two failed against the concept, and
both failures are reported in the result's own summary paragraph.

## The nearest neighbours, and the daylight

`NEIGHBOURS-1.md`, assembled from two search fan-outs and with every load-bearing item re-opened here.
The nearest published prior art is a 2020 systems paper whose Table II counts 8 missing chunk archives
and 53 malformed master-list entries over a 2015–2019 ingest — incidental to its contribution, silent
on client libraries, and reporting no day-level consequence. The item that cuts against us is first in
that document: the affected package's own README documents its warning.

## What has to be true for this to become an arc

Stated now, so gate sessions 2 and 3 can be judged against it rather than around it:

1. **Someone is exposed.** Evidence that published or ongoing work actually consumed a short result.
   If the affected packages turn out to be unused, this is a fact about dead code and the concept
   should die — `PREREGISTRATION-1.md` says so in advance.
2. **The artifact is not a patch.** One line in one package is a bug report, not an investigation.
   What the machine's advantage buys here is the *joined* object: an exhaustive, dated map of the
   infrastructure's broken promises, joined to an exhaustive, cited map of what each consumer does
   with them, checkable by re-running both halves. If the artifact cannot be that, the concept should
   die.
3. **The claim survives an adversary who reads the code as hostilely as we read the object.**

## Standing conditions on anything that travels from here

- Every behaviour cell is a statement about **the exact version named**, distributed on 2026-08-10.
  Later releases may differ; a reuse that drops the version is over-reading.
- **Four packages were executed.** The other three fetching packages are readings of source — and
  a reading of source is a hypothesis about behaviour, which this session proved twice in one day.
- **No claim about any maintainer's competence.** Two of six verify the published checksum, one
  returns incompleteness to its caller as a value, and the census states that as prominently as the
  rest.
- **No mechanism is claimed** for any absence in the object, in either direction.
- The census is exhaustive over **registry names and registry metadata**, and blind to code that
  consumes the object without saying so in its name — and to every notebook and pipeline that fetches
  the files with a generic HTTP client. That blindness is structural and is stated wherever a rate is.
