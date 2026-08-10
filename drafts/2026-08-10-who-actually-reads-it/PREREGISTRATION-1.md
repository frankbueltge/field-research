# Pre-registration 1 — "Who Actually Reads It"

*Third concept for the assigned investigation (PROTOCOL v3, "The first investigation"), gate session
1 of at most 3. Written and committed **before the first request of this session left this machine**,
as at sessions 100–105. Nothing below may be edited after that commit; scoring happens in
`RESULT-1.md`, and every deviation is recorded there under its own number.*

## Why this pre-registration is shaped differently from the last three

The previous two concepts each measured something real about an object and then went looking for
someone the measurement would help. Both died on the second half. Session 105's own one-page finding
states the rule this concept is built to obey:

> …name a receiver only after establishing that a path through their code actually executes the
> defect — not that the defect is present in a file.

So the order is inverted. **This session measures the consumers, not the object.** The object's
defects are already measured, dated and banked (session 105, `availability-register-v1.0.json` and
the unlisted-but-served list: 2,413,372 requests, 0 unresolved, dated 2026-08-09). The question this
concept opens is whether any code that a person can actually install and run produces a **wrong
answer a caller cannot detect** when it meets one of them.

If nothing does, the concept dies at this gate or the next, and it dies cheaply. That outcome is
named as the kill criterion below and is not a failure of the session.

## The object under test, stated precisely

Not the news-measurement instrument this time — **its consumer software**: publicly distributed
packages whose own code fetches that instrument's published files or its master file lists.

## The population, declared before the census

Session 105 was refuted for claiming a negative over a population it had not stated. So:

- **P-A (Python index).** The full name list of the public Python package index, fetched from the
  index's own simple endpoint, screened case-insensitively for the object's project token in the
  **package name**. Exhaustive over names; **blind to any package that consumes the object without
  saying so in its name** — stated here as a known and unfixable limit of this screen.
- **P-B (R archive network).** The archive network's own complete package metadata database, screened
  case-insensitively over **name, title and description** — a full-text screen over the registry's own
  fields, exhaustive over that database.
- **P-C (named additions).** Any consumer named first-hand in this practice's own prior record
  (sessions 103–105) or surfaced by open web search, added explicitly and marked as **not** part of
  the exhaustive screens.

Anything found in P-C is reported separately from P-A/P-B and never folded into a rate.

## The classification, fixed before any source is read

For each candidate package whose source can be obtained from the registry itself, read the fetch path
first-hand and record, with a file-and-line citation into the fetched source:

- **C1** — does it read the object's master file list, or construct file names arithmetically from the
  15-minute grid, or both?
- **C2** — does it verify the checksum the master list publishes beside each file against the bytes it
  downloads?
- **C3** — on a listed file the host does not serve, what does the caller receive: an exception, a
  logged skip, or a value indistinguishable from success?
- **C4** — does it offer a joined or merged view across the three file products, and if so does it
  require all three for a cycle?
- **C5** — last release date, and whether the fetch path is reachable from the package's documented
  public entry points.

**C3 is the load-bearing cell.** Everything this concept could become depends on whether the answer
"indistinguishable from success" occurs at all.

## Predictions, written before the first fetch

Scored in `RESULT-1.md` as HELD / FAILED, with the failures reported as prominently as the holds.

1. **N1.** The name screen (P-A) returns **between 1 and 25** packages; the metadata screen (P-B)
   returns **between 1 and 15**.
2. **N2.** At least **two** candidates across P-A + P-B have source obtainable from the registry and a
   readable fetch path. *(If fewer than two: the population is too thin to carry a concept — park.)*
3. **N3 (no expected direction; written so it can go against us).** Of the candidates that download
   files, the number that verify the published checksum is **0**. If any candidate verifies it, that
   candidate is immune to the misdeclared-bytes half of the object's defect and must be reported as
   immune, in the same sentence as any claim about the others.
4. **N4 — THE KILL CRITERION.** At least **one** candidate returns, for a cycle listed in
   `availability-register-v1.0.json`, a result its caller **cannot distinguish** from a legitimate
   result. **If zero candidates do this — if every reachable consumer either raises loudly or verifies
   — the measured defect has no executing victim in the population we can reach, and this concept is
   DISCARDED at gate session 1 with a one-page finding.**
5. **N5.** At least one candidate offers a joined view across products (C4) that does not require all
   three products to be present for a cycle.
6. **N6.** At least one candidate has a release within the last 24 months. *(Aliveness is not a
   receiver argument. Sessions 103 and 104 each named a receiver that was alive and still could not
   use what was offered; this prediction exists only so the census records the pulse, and it is
   explicitly **not** admissible as evidence that anyone is a receiver.)*
7. **N7.** At least one candidate constructs file names arithmetically rather than from the master
   list, and can therefore reach files the master list never mentions.

## The check that has cost this arc two claims, run first this time

Before any of the above is written up as a finding:

> **Ask what the object already publishes about itself, and try to derive the finding from that
> first. If you can, the finding is not yours to supply.** *(dossier, session 104)*

Applied here as a fetch, not a recollection: the object's own published documentation and its own
data-format notes are fetched this session and read for any statement that its master lists may
promise files the host does not serve, or that consumers should verify checksums. **If the object
already documents this, the finding is that its consumers ignore documented guidance — a different and
weaker claim — and the write-up says so in its first paragraph.**

The companion, from the same dossier and paid for three times:

> **A receiver argument is not an argument until you have read the receiver's own source and
> established that their code can consume the artifact.**

This session may not name any receiver. Naming one is explicitly **out of scope for gate session 1**;
the census establishes whether a receiver could exist, and gate session 2 decides.

## What would make this concept worthless even if N4 holds

Stated in advance so it cannot be argued away afterwards:

- If the only affected consumers are unmaintained and unused, "somebody's code is wrong" is a fact
  about dead code. The census records last-release dates and download counts where the registry
  publishes them, and a concept that survives on a dead package is not a concept.
- If the failure is one line in one package, it is a bug report, not an investigation. The bar
  (PROTOCOL v3, "The bar") requires the machine's advantage — scale, repetition, verification, the
  temporal — to be experienceable in the artifact. A single patch is none of those.

Both are gate-session-2 questions. They are written down now so that session cannot pretend they were
not foreseen.

## Deviations

Recorded in `RESULT-1.md` §Deviations, numbered D1…, with the reason, as at every session since 100.
