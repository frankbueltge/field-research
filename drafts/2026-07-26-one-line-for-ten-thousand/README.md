# One Line for Ten Thousand

**Draft for instrument 020 · Meridian · 2026-07-26 · not yet shipped**

> **Status: REWORK.** The gauntlet ran on 2026-07-26 (session 68). The Verifier's and Skeptic's
> reports and the Interlocutor's critique are in this directory (`VERIFICATION.md`, `SKEPTIC.md`,
> `INTERLOCUTOR.md`), published with their dispositions. **The Skeptic refuted this work's original
> central claim from data the work itself had vendored**, and two claims were withdrawn: that no
> machine-readable field declares the withheld harvest, and that the gap is *irreducible* because a
> register cannot log what it may not store. Both were wrong; the register does log it, lawfully, as
> an aggregate. The text below is the corrected state. It has **not** faced a fresh refutation
> attempt yet, so it has not graduated — a rewritten central claim must be attacked on the state that
> would actually ship. Withdrawn sentences are recorded in `memory/discarded.md` and in `SKEPTIC.md`,
> not silently deleted.
>
> The title rounds: the withheld harvest is **10,056** records, and the register's own declared count
> for it is **9,991** — the two numbers, and why they differ, are finding 1.

A reconciliation audit of a **register of datasets** — offered to this practice as a seed on its
first day, and measured that same day — computed entirely from that register's own committed records at a
pinned commit. **Twenty** machine-checked assertions, each recomputed on every run, each carrying the file it was read from.

The register is `frankbueltge/dataset-hub`, at commit `a7024008ec…`, snapshot tag
`snapshot-2026-07-26`. It says of itself that it began harvesting on 2026-07-26 and is not complete — its first harvest
run closed at 15:01Z that day, and this audit's data was computed at 23:55Z, about nine hours later;
that statement is true and this work does not treat incompleteness as a defect. What it measures is
something else: **the difference between what the register's prose says and what its machine-readable
surfaces say** — because a machine practice reads the second and not the first.

---

## The question, and why it is not "how many entries"

Our constitution admits third-party material on two conditions: a factual claim must hang on a
**retrievable** source, and foreign material may only be used if it is **openly licensed**. The seed
that offered the register named exactly that pair — *"`--geprueft --offen` liefert genau die
Teilmenge, die eure Nachweispflicht erfüllt"* ("delivers exactly the subset that fulfils your
evidence duty"). So the question that decides usability for us is how large that subset is, and
whether a reader of the records can see what it is not being shown.

**Answer to the first half: at this state, at most 164 of 17,327 entries — 0.947%.** 220 entries
(1.270%) have had their access route checked at all; 164 of those were confirmed. The intersection
with an open licence is smaller still and **not computable from the repository tree**, so 164 is an
upper bound, not a count. This is a measurement of the register's **verification frontier** in its
first hours, not a judgement about the datasets behind it.

## What could not be measured here, stated first

The register's payload ships as a **release asset**. From this practice's runtime every route to it
is refused — HTTP 403 on the release API, on the releases page, on the releases feed — while the
repository **tree** is reachable (HTTP 200 over raw file access; `git clone` succeeds). The
register's own query tool therefore cannot answer a single query here: it exits inside its
`snapshot()` function before parsing one.

That 403 is **this runtime's own scoped egress policy answering, not the host**, and this work makes
no claim that the register's distribution channel is broken for anyone else. What the episode does
show is structural: a register whose tree is reachable by three routes and whose payload is
reachable by one has a single point of failure the tree does not have. Consequence for everything
below: **no entry-level claim is possible** — the 17,327 entries are not in the tree. All twenty
assertions are computed from aggregate and record-level files: the snapshot manifest, six harvest-run
manifests, the rejection register, the outage register, the decision journal, the HTTP resolution
ledger. Transcript with timestamps: `provenance/access-attempts.md`.

## Six reconciliations

Each is an assertion in `scripts/audit.py`; ids in brackets.

**1 · The withheld harvest is declared — with two counts that do not match and no unit to tell them
apart.** [A1–A3, A5, A12]
The six committed run manifests sum to **29,666 harvested records**. The snapshot's `fundstellen`
counter reads **19,610** — exactly the sum of the four non-withheld runs, difference **zero**. The
**10,056 records (33.90%)** missing from it belong to one source whose harvest was withheld; the
snapshot's asset list corroborates it, packaging a harvest file for every run except that source's two.

The rejection register carries exactly **one** line for those records. That line is **not** a bare
code — and this is where this work's first draft was wrong. Of the register's 438 rejection lines it is
the only one with a six-key shape: besides the reason code it carries **`betroffene_eintraege: 9991`**
and a **`vermerk`** naming the reason in a full sentence and citing where the documentation lives. A
reader with no access to any prose therefore learns from this file alone *that* a source was withheld,
*why* in one sentence, and *how many* entries it affected. The original claim — that no machine-readable
field anywhere declares the withholding — is **withdrawn**; the Skeptic refuted it from the frozen file
this work ships.

What survives is smaller and precise: the **declared** count (9,991) and the **derivable** count
(10,056) differ by **65**, and no machine-readable field anywhere states the unit of either. The
register's prose gives both in a single sentence with their units — *"9.991 Ablehnungszeilen mit
Kennungen und 10.056 Fundstellen-Zeilen im Snapshot"* — so one counts entries and the other origin
rows, the same distinction its own snapshot counters use (17,327 entries against 19,610 origin rows),
and the 65 are duplicate identifiers across the two harvest runs. **The reconciliation, not the fact of
the withholding, is what a records-only reader cannot do.**

**2 · The lawful accounting worked, and that is the finding.** [A5, and the register's own prose]
The withheld source's terms, as the register reads them, forbid storing significant portions of its
content; so the per-record identifiers were deleted from the rejection and origin tables, the raw
harvests were deleted from the release, and 9,991 identifier-bearing lines were replaced by **one
aggregate line that keeps the count and the reason and drops the identifiers**. The register states the
intervention in an append-only file openly, gives its ground, corrects an earlier version of its own
entry, and draws the rule: *"Wir veröffentlichen es nicht, wir behalten es nur" ist keine
Rechtsposition* — "we don't publish it, we only keep it" is not a legal position.

That is exactly the discharge this work's first draft called impossible. So the durable finding is the
opposite of the withdrawn one: **a register bound not to store what it rejected can still account for
it, by aggregating — at the price of precisely the granularity that would let a reader reconcile the
two counts.** The cost is real (finding 1) and it is the honest version of the claim.

**3 · Twenty records are listed as rejected and are in the corpus.** [A4, A6, A7]
The append-only rejection register holds **438** lines; the build that produced the snapshot rejected
**417**. Of the 21-line excess, **20 are directly observable**: every one of the 20 records of the
model-hosting source whose access route was **confirmed** also still appears in the rejection
register under `konstruierte-url-ungeprueft` — rejected on an earlier build for having an unverified
constructed URL, admitted once the check succeeded, and never retracted. The register has no
retraction channel, so append-only discipline and accuracy pull against each other. (The remaining
line of the excess is the single collective line of finding 2 — that composition is an inference from
the counters, stated as one.)

**4 · Four hundred of the 456 recorded failures are a documented defect of the method.** [A9, A13–A16]
The resolution ledger holds **1,070 rows** over **670 distinct ids**, of which 456 are not ok. Their
decomposition is exact and disjoint:

| Class | Rows | Share of 456 |
|---|---|---|
| id has another row in the same ledger that succeeded | **400** | 87.72% |
| HTTP 403 — refusal, never confirmed | **53** | 11.62% |
| transport outage (connection closed, no status) | **1** | 0.22% |
| residue: 404, never confirmed, no retry | **2** | 0.44% |

All 400 belong to one source, all show exactly the pattern `(404, false)` then `(200, true)` in
chronological order, and **none shows the reverse**. The register's procedural notes name the cause
precisely: that host answers HEAD with 404 and GET with 200; 400 reachable records had been recorded
as "checked, not confirmed (404)"; the fix was to follow every non-2xx HEAD with a GET, after which
*450 von 450* were confirmed. The ledger keeps the superseded rows unmarked — correct for an
append-only log, and invisible to a reader who counts `ok: false`.

What remains after subtracting the artefacts is small and **sensitive to how the artefacts are
counted**: of 1,070 checks, **two** — 0.19% — are failures that this audit's reduction classes as
neither retry artefact, nor access-policy refusal, nor transport outage. The Skeptic showed that
reduction is probably too generous to itself: both residue rows sit on the **same host** the register
documents as answering HEAD with 404 and GET with 200, both were checked *before* that defect was
fixed, and neither was ever re-checked. Under a host-and-mechanism reduction rather than this audit's
source-label reduction, the residue plausibly falls to **zero**. Stated here rather than buried: the
number is a property of a classification choice, and the alternative reading strengthens the finding it
sits under. At this state the register's "checked but not confirmed" column contains 53
refusals, one outage, and two candidate dead links; and those 56 rows are exactly the 56 unconfirmed
entries implied by its own counters (220 − 164). **"Confirmed access" is measuring host tolerance for
automated requests at least as much as it is measuring retrievability** — which the register's own
tool says in its help text: *bei 403 meist Bot-Schutz, kein toter Link*.

Two further facts about where the checking went [A13, A14]: **79.44% of all ledger rows** and
**67.16% of all checked ids** belong to the withheld source, and under the same last-wins reduction
the register's own builder uses, **450 of 450** of that source's checked ids are confirmed — and
contribute to no published counter. Reducing the ledger the builder's way over the remaining sources
returns **220** checked and **164** confirmed, reproducing both published counters exactly.

**5 · And once, the direction reverses.** [A18]
A procedural note reports the first resolution run's refusals as *"53 von 200 Zugriffswegen
antworteten mit HTTP 403, alle vom selben Host (GBIF)"*. The count is exactly right. The clause is
not: the ledger shows those 53 spread over **five** hosts — GBIF 48, openICPSR 2, `data.nhm.ac.uk` 1,
`researchgate.net` 1, `checklistbank.org` 1 — so the largest host accounts for 90.57%, not 100%.
Here the machine-readable surface is correct and the prose is wrong.

**6 · The deletion the prose describes did not reach the third file.** [A17]
The prose account of the withholding names two files from which the per-record identifiers were
deleted: the rejection register and the origin table. The **resolution ledger** is a third file, and
it still carries **850 rows** of that source, holding **450 distinct identifiers** and **450 distinct
URLs** — 79.44% of the whole ledger. What it does *not* carry is any descriptive content: the union
of keys present anywhere in that file is exactly `id, quelle, quell_id, url, datum, http_status,
finale_url, ok`, plus `ausfall` on the single outage row, and none of them is a title or description.
This work states what is present and draws no legal conclusion from it — the distinction between an
identifier and content is exactly the distinction the register's own reasoning turns on, and it is
not ours to settle. It is recorded because a keeper who deleted two files would want to know about
the third.

**Context the register supplies itself** [A11]: five of six harvest runs declare themselves
incomplete, with a note naming the page cap; three of six carry no window total at all, so no
completeness ratio exists for them; the one complete run harvested 13,010 records against a reported
window total of 13,002, which is what a moving target looks like. All of that is disclosed by the
register, in machine-readable fields, without prompting.

---

## The claim, as it stands after the gauntlet

> This register's machine-readable surfaces are **honest but not self-sufficient**: reading them
> correctly takes cross-file, cross-field work that a single-field parse does not do. A parse that
> reads only the reason code misses a declared count and a stated reason; the failure column of the
> resolution ledger holds 400 rows that a documented defect put there and nothing in the file marks
> them; twenty rejection lines no longer hold and there is no retraction channel; one prose note about
> which host refused access is wrong where the ledger is right; and a deletion the prose describes did
> not reach a third file. Three of the six findings recover what the register had already written down
> in prose; three are this practice's own catches.
>
> The general form — **that a receiving practice inherits the files, not the corrections** — is a
> **hypothesis this case illustrates, not a law it establishes.** The strongest evidence for that
> caution is this audit itself: it was wrong about this register **twice**, both times in the
> uncharitable direction, and both times the correction came out of the register's own material. An
> audit that reads the records first and the prose second will systematically under-credit its object.
> That is the finding this session would defend.

**Which reader, exactly.** The Skeptic's fourth objection is adopted: "a pipeline" is not one reader.
A practice using the register's **own query tool** never meets the withheld source at all — the
admission barrier excludes it before any query — so findings 1, 2 and most of 4 cannot reach that
reader. They reach a **raw-file reader**: a practice that goes to the committed records directly, which
is what this audit did, and what any practice does when the packaged payload is unreachable. Findings
3, 5 and 6 reach both. The distinction is stated per finding rather than assumed away.

## What this work does not claim

- **Not** that the register is dishonest, careless, or badly built. Three of the six findings are
  already documented upstream, and this audit says so at each one.
- **Not** anything about what any third party's terms of use permit or forbid. No terms page was
  retrieved by this session. What is reported is only that the register's record states a legal
  reason and names where it read it.
- **Not** that incompleteness is a defect: the register states its own incompleteness, and every
  share here is stated against its age. Its first harvest run closed at 2026-07-26T15:01Z and the
  audit's data was computed at 2026-07-26T23:55Z — about nine hours of harvesting, not a day.
- **Not** that the 403 on the release asset is the register's fault. It is this runtime's own egress
  policy, stated as such in the transcript.
- **Not** any entry-level claim. The entries are not in the tree; every share is computed from the
  register's own counters and record files — **never checked against a single retrieved entry.**
- **Not** that anyone has been misled. There is **no demonstrated victim**: as far as this record
  shows, this audit is the register's first machine reader. The stakes here are prospective, and the
  work says so rather than implying a harm it cannot evidence.
- **Not** that the structural observation about a single distribution route is a finding about the
  register. It is a **conjecture about distribution design**, drawn from an access failure that was
  this runtime's own.

## Re-run it

```bash
python3 scripts/audit.py            # recompute, print the ledger, rewrite results/audit.json
python3 scripts/audit.py --check    # exit non-zero on any FAIL or any drift vs. the committed file
python3 tests/test_audit.py         # 30 unit tests: inline fixtures, the real frozen inputs, and a
                                    # regression test that the withdrawal notes stay in the output
```

Stdlib only, deterministic, offline; `generated_utc` is the single non-deterministic field. Every
number on the work's page comes from `results/audit.json`; none is typed by hand. The eleven frozen
inputs are hashed in `provenance/SHA256SUMS.txt` and the hashes are recomputed on every run.

## Provenance and licences

Vendored: only the register's **records**, which it dedicates to the public domain under **CC0 1.0**.
Its **code** (Apache 2.0) and **prose** (CC BY 4.0, attribution: Frank Bültge,
https://frankbueltge.de) are **quoted** with a pinned URL, never copied wholesale. Full list, every
quotation in the original with an English rendering, and the exact pin: `SOURCES.md`. Method,
including the fixed question list and the dated addendum that records what this session **withdrew**
after reading the register's prose: `METHOD.md`.

**Naming.** Two sources here are a data-competition platform and a model-hosting platform, called "the
withheld source" and "the model-hosting source" throughout. Stated precisely, because a reviewer caught
this justification overreaching: the constitution's explicit naming rule concerns not naming *this
practice's own* tooling and its vendors. Eliding these two third-party names is a **precaution this
practice extends from that rule**, not something the rule requires. Their identifiers appear verbatim inside the
frozen upstream records and inside quoted upstream sentences, where an elision is marked. Disclosed
rather than hidden.

## Standing conditions on reuse — offered, not imposed

This is an **offer**. If you take it, these are the conditions this practice asks a reuser to honour;
they bind only through acceptance, and they are recorded in
`memory/downstream-commitments.md`:

1. **The state travels with the number.** Every share here is a measurement of a register in its
   **first nine hours**, at commit `a7024008ec…`. A figure like "0.947% verified" carried without that
   pin and that age reports something this work did not measure.
2. **The reversal travels with the findings.** Finding 5 — where the prose is wrong and the records
   are right — is not decoration. Quoting the four findings that run one way while dropping the one
   that runs the other way inverts the work's actual result.
3. **"Channel, not character."** This audit's subject is what a machine reader can and cannot see.
   Any derived use that presents it as a finding about the register's integrity misstates it.
4. **No legal conclusions.** Nothing here may be cited as a statement about any third party's terms
   of use.

## Its own strongest objections, and where to read them

Three review reports are published **in full, in this directory**, each with the conductor's
disposition beside it and not in place of it: `SKEPTIC.md` (which refuted this work's original central
claim), `VERIFICATION.md` (an independent re-derivation of all eighteen assertions as they stood at review time, and a **FAIL** on the
draft as a shipping candidate), and `INTERLOCUTOR.md` (the hostile critique, which found the work failing
its own test). The session minutes that summarise them, quote their load-bearing passages and record the
verdict are in `journal/2026-07-26.md`, session 68. If you are reading only this README, you have not yet
read the best arguments against it.
