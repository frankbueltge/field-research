# Pre-registration — increment 3, 2026-08-09 (session 105)

*Committed before the first request of this session leaves this machine. The manifests fetched at
session 104 are on disk from that session; this session re-fetches them and states so. As at
increments 1 and 2, the outcome that kills the arc is named here, in advance, in its own section.*

## What increment 3 is for

Two conditions from the adversary's session-104 verdict are open, and the gate is not passable with
either of them unasked:

- **C-VII** — the exhaustive host-verified negative: *no other such window exists*. The adversary
  granted this as the one machine argument in the arc that a person with a weekend cannot reproduce,
  and recorded that we had not earned it: 15,290 probes, not 1.18 million.
- **C-IV** — whether the absence is already visible for free in another copy the object publishes.

## The one design decision, stated before the numbers

A HEAD request returns `Content-Length`. So the sweep that answers C-VII also measures, for **every
listed cycle**, the size the host actually serves against the size the index declares. That
comparison is the one measurement in this arc that **cannot** be derived from the index by
construction — the index cannot check itself. Increment 3 therefore has two products from one pass:

1. the **complete negative** (which listed cycles the host does not serve), and
2. the **complete index-vs-host disagreement** (which listed cycles the host serves at a size other
   than the one published).

The second exists in the record already as exactly one case, found by hand at session 104
(2016-05-08T14:00:00Z: declared 18,095 bytes, served 10,276,183). Whether it is a singleton or a
class is unknown to us as this file is committed.

## The universe

Every cycle listed in `http://data.gdeltproject.org/gdeltv2/masterfilelist.txt`, `.gkg.csv.zip`
type — the same type increments 1 and 2 measured, ~394,878 cycles as counted at session 104. The
other two types (`.export.CSV.zip`, `.mentions.CSV.zip`) and the Translingual stream are probed for
**every cycle the gkg sweep finds absent or misdeclared**, plus a seeded control sample; a complete
sweep of all six series is ~2.37 million requests and is not claimed unless it is run.

## Engineering calibration — run first, not scored

Before the sweep, at most 2,000 requests establish a rate the host tolerates and the error behaviour
of this environment. **No prediction below is scored on calibration data**, and the calibration
results are reported separately. Rules that bind the sweep:

- bounded concurrency; on any 429 or 5xx, back off and record it;
- every non-200/404 outcome is retried up to three times and, if it never resolves, recorded as
  **unresolved** — never inferred in either direction;
- a sweep that does not complete is reported as the fraction it covered, and the complete negative is
  **not** claimed. Partial is partial.

## Predictions, written before any of them can be checked

**P1 — positive control.** The full sweep returns all 83 known cycles
(2022-11-10T22:00:00Z → 2022-11-11T18:30:00Z) as absent on `.gkg.csv.zip`.

**P2 — the size of the phenomenon.** Outside that window, the number of listed English gkg cycles the
host does not serve is **fewer than 500**. Basis: session 104 probed 3,000 uniformly drawn unflagged
cycles and found 0 absent, and all 3,148 byte-column-flagged cycles and found the same 83 and no
others.

**P3 — the decisive prediction, written so it can fire against us.** Among the absent cycles found
outside the known window, **at least one is not flagged by the index's own byte-column screen** at
threshold 0.20 — that is, absence is *not* fully predictable from the published size column. **If
zero such cycles exist**, the index predicts absence perfectly across eleven years, the register's
remaining value is confirmation of something a consumer can already infer for free, and **the arc's
value claim is dead in the form it now has**. See the kill criterion below.

**P4 — C-IV, the second copy.** A free, unauthenticated second copy published by the same
organisation shows the November 2022 window as a gap at cycle resolution. We predict **it does** —
the same trap that has closed on this arc twice. If it does, the location of the hole is free from a
second direction as well, and only the per-file verified status survives.

**P5 — the shape of the negative.** The absent set across eleven years forms **at most 20 contiguous
runs of length ≥ 4 cycles**.

**P6 — index-vs-host disagreement.** The number of *served* English gkg cycles whose `Content-Length`
differs from the declared size by more than 1 % is **between 1 and 2,000** (0.0003 %–0.5 % of the
universe). We know of exactly one, found by hand.

**P7 — direction.** Among those disagreements, **more will be declared-too-small than
declared-too-large** — i.e. the index under-states more often than it over-states.

## The kill criterion, written so it can fire against us

**P3 failing kills the value claim.** If every absent cycle in eleven years is already flagged by a
screen anyone can run on the published index in eight seconds, then this practice has spent three
sessions verifying, at 1.18 million requests, something the object gives away — for the third time,
and after writing that lesson into its own dossier. In that case the honest outcome is not a rescue.
It is: **discard the concept with a one-page finding**, unless the index-vs-host disagreement (P6)
is itself a class large enough to carry an artifact on its own — which is a *different* claim, and
would have to be argued as one, from scratch, with its own receiver.

**P4 holding does not by itself kill the arc** — the window's location is already conceded as free
(C4) — but if the free second copy also distinguishes *served* from *not served* at cycle
resolution, then C-IV has fired in its strong form and the same paragraph above applies.

## What this session may not do

- No claim about what was served in 2022. Every probe result is dated 2026-08-09 and is a snapshot.
- No mechanism claimed for any absence or any disagreement, in either direction.
- Any register row before 2019-05 that is reported absent is checked against the frozen public
  snapshot host as a second witness (C-VIII), or reported unchecked.
