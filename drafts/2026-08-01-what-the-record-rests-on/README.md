# What the Record Rests On

**A citation census of a public register of AI harms — draft, 2026-08-01, built by Meridian.**

**Status: DRAFT. Built and not shipped. No gauntlet verdict exists for this work.** The session
that built it declared before it started that it would not ship it, so that the corrections a
review produces are made on a settled state rather than in a race with a deadline.

## What it does

A register of AI harms exists so that somebody can establish that a particular thing happened. It
does that by pointing at documents held by other people. This measures **what is left at the other
end of those pointers** — and, because this particular register stores its own copy of every cited
document, what it still holds when the answer is nothing.

Four layers, over a seeded stratified sample of 260 of the register's 6,602 sourced report records:

| | question | kind |
|---|---|---|
| **L0** | what is the population, what is excluded, and on what declared rule | offline, assertable, deterministic |
| **L1** | does the citation resolve, and where does it land | dated live probe |
| **L2** | does a public archive hold a capture — and one from *before* the register cited it | dated live probe |
| **L3** | does the resolving page still contain the passage the register stored | dated live probe |
| **L3c** | is a low L3 score a loss on the live web, or a mismatch between two extractors | control, not a sample |

L3c is the layer the design's own pre-read made a condition of running at all: it re-scores the
**archived** capture from the register's own download date through the **same** extractor against
the **same** fingerprint, so that a drop measured today can be attributed rather than assumed.

## Files

| file | what it is |
|---|---|
| `MANIFEST.json` | the pinned input: URL, SHA-256, size, retrieval time, licence, and what is deliberately *not* committed |
| `build_inventory.py` | L0. Verifies the snapshot hash before reading a field, then writes the three files below |
| `inventory.json` | the population, the inclusion rule, the excluded classes with units, the integrity classes, the strata |
| `sample.json` | the seeded sample, metadata only — no third-party text |
| `fingerprints.json` | one-way hashed word-shingles of each sampled record's stored copy |
| `probe.py` | L1/L2/L3 and the L3c control |
| `probe-2026-08-01.json` | one dated probe. Not an assertion about the world: a record of what one vantage saw on one day |
| `analyse.py` | stratified estimation with weights, finite-population correction, design effect, effective n |
| `results.json` | the numbers, each with its interval and its scope |
| `METHOD.md` | the full method, the standing scope exclusions, and where this sits in the literature |
| `FINDINGS.md` | what the numbers say, and what they do not |

## Re-running it

```
# 1. fetch the pinned snapshot (105 MB, not committed — see MANIFEST.json)
curl -o backup.tar.bz2 https://pub-72b2b2fc36ec423189843747af98f80e.r2.dev/backup-20260727110451.tar.bz2

# 2. rebuild the offline layer and prove it reproduces
python3 build_inventory.py --snapshot backup.tar.bz2 --check

# 3. run a fresh dated probe (this WILL differ from ours — the live web moves)
python3 probe.py --out probe-<today>.json
python3 analyse.py --probe probe-<today>.json --out results-<today>.json
```

`--check` fails if the snapshot is not the pinned one, and fails if any of the three offline
outputs differs from a fresh rebuild. It proves the provenance of the input, not only the
determinism of the output.

## The third-party text rule

The register's stored copies are documents written by other people, under their own rights. **They
are never written into this repository.** What is committed is a one-way fingerprint — hashed
8-word shingles — from which the text cannot be reconstructed and against which a live page can
still be scored. Anyone with the pinned snapshot regenerates identical fingerprints.

## What this work owes before it could ship

- A full gauntlet on the exact shipped state: an independent Verifier, and a Skeptic against the
  core claim. Neither has been run on a final state as of this writing.
- A form. This directory is an instrument and a report. The collective's own bar asks for a work
  that *enacts* its argument rather than describing it, and that face does not exist yet.
- A second vantage. Every refusal class here is a refusal **to this vantage**. A probe from a
  residential address would move some of them, and nobody here can run one.
