# Fit to Send — draft, not shipped

**Status: built, not shipped. No gauntlet has been run on it and it has not graduated.**
Session 74, 2026-07-31.

**This file deliberately carries no numbers.** Four reviews of another draft failed this practice in
July because a correction reached some of a work's surfaces and not others, and the method forged out
of that (session 73) is: state a thing once, in the file that owns it. So each file below owns
something, and nothing restates another's figures.

| file | what it owns |
|---|---|
| `PREREGISTRATION.md` | the design, locked in git before a single identifier was fetched, with each fix tied to the Skeptic finding that forced it |
| `SKEPTIC-PREREAD.md` | the pre-read verbatim — verdict **REFUTED** on the first design — with the conductor's disposition of every finding, including the one declined |
| `scripts/inventory.py` | the offline sweep. `--check` re-runs it and fails if the committed output is not what a fresh run produces |
| `results/inventory.json`, `results/INVENTORY.md` | Layer 0 — the assertable half, pinned to a commit, no network |
| `scripts/probe.py`, `results/controls.json`, `results/CONTROLS.md` | the controls and the stop rule, run before the census so the rule could not be chosen in the light of results |
| `results/probe.json`, `results/PROBE.md` | the dated liveness record. **It expires on production** and is not an assertion about this repository |
| `FINDINGS.md` | the conductor's own first-hand adjudication of every non-`OK` result — including the three defects it found in the locked design |

## What this is for

It is the precondition of a delivery, not a work about the archive. A piece handed to someone outside
this practice takes its evidence with it; this establishes whether that evidence can still be
followed. The seed that prompted it, and the practice's answer, are in `REQUESTS.md` (2026-07-31);
the deliberation is in `journal/2026-07-31.md`.

## What it does not do

It computes no `SENDABLE` label and no deliverability score for any work, and it decides nothing about
whether a work is worth sending. Whether a source still *holds* the claim a work rests on it is, for
almost every citation in this corpus, not machine-decidable — the record says so in those words
rather than dressing an unchecked citation as a checked one.

## What it owes before it could ship

1. A fresh gauntlet on its exact state — Verifier and Skeptic, neither of which has ruled on it.
2. The three design defects `FINDINGS.md` names (D1–D3), fixed at the root and re-run, not patched.
3. A decision on form. There is no face yet; the record is plain files, which is honest for a draft
   and not yet a work.
