# The Floor

**Instrument on trial:** PUE (Power Usage Effectiveness) — the data-center industry's dominant
public efficiency metric, ISO/IEC 30134-2:2016.

**Thread:** material stakes (second work, after 012 "The Two Meters"). Cluster C1, material/planetary
AI cost.

**Status:** DRAFT — built session 16 (2026-07-09). Full gauntlet OWED before it can ship.

## The failure mode

PUE is a ratio: total facility energy ÷ IT-equipment energy. Because IT energy is a subset of
total facility energy, the ratio has a hard **floor of 1.0** — a perfect data center delivers all
the energy entering the building to its servers and loses none to cooling or conversion. A fleet
already reporting **1.09** therefore has, at most, **~8% of travel left — once, and forever.**

The metric was built by The Green Grid as a management tool for one facility over time. It says
nothing about the carbon of the electricity (renewable and coal count identically), nothing about
IT-equipment efficiency, and — the point of this instrument — **nothing about absolute scale.** A
facility can double its absolute energy draw at a constant, or even improving, PUE. The industry
has its own name for leaning on the number past its purpose: **"PUE Abuse."**

The trial: put a near-floor efficiency ratio next to the absolute it is presented as mitigating,
and show — from the subject's own disclosed numbers — that the ratio is structurally incapable of
the offsetting work the framing invites the reader to credit it with.

## The subject and why it was chosen

Google — examined **precisely because it discloses the most.** Its 2025 Environmental Report (fiscal
2024) publishes fleet-wide PUE, the year-over-year growth of total data-center electricity, and a
full six-year greenhouse-gas inventory, in one document. The instrument can only be built on a
company transparent enough to be audited this way. That is the first self-implication: the deepest
version of this problem is worst-hidden by whoever discloses least — and least auditable there.

## The claim under trial (the subject's own framing)

The 2025 report, at Figure 4:

> "For the first time in six years, the average annual power usage effectiveness (PUE) for our
> global fleet of data centers dropped below 1.10 to 1.09 ... this efficiency gain avoids
> significant electricity consumption. This means our global computing network **requires less
> electricity and produces fewer emissions than it otherwise would have, yielding meaningful
> savings even as our overall computing demands grow.**"

The same report itemizes "PUE improvements" as one of four wedges in its carbon-reduction bridge
graphic, and foregrounds "84% less overhead energy than the industry average" and "over six times
more computing power per unit of electricity than five years ago." In the same report:

> "our total data center electricity consumption grew by 27% in 2024, compared to 17% growth in
> the prior year."

And the disclosed absolute — location-based Scope 2, "what the grid saw" — rose from **5.12 million
tCO₂e (2019) to 11.28 million tCO₂e (2024): +120%.** Total ambition-based emissions: **+51% vs 2019.**

## The arithmetic (disclosed inputs + the definitional floor; no modeling)

- **PUE series, 2019→2024:** 1.10, 1.10, 1.10, 1.10, 1.10, **1.09.** Six years; the metric moved 0.01.
- **Remaining headroom:** (1.09 − 1.00) / 1.09 = **8.3%.** That is the entire future contribution
  PUE can ever make to energy-per-unit-of-IT — one time, permanently.
- **One year's growth:** total data-center electricity **+27%** in 2024 alone.
- **Verdict ratio:** the metric's whole remaining lifetime headroom (8.3%) is **less than a third**
  of a single year's absolute growth (27%).
- **Breakeven:** required PUE = 1.10 / (1 + growth). It crosses below the floor of 1.0 once growth
  exceeds **10%**. At 2024's **27%**, the required PUE is **≈0.87** (1.10/1.27) — below the floor,
  thermodynamically impossible. The efficiency lever could not have offset the growth even in
  principle. (Using implied IT-load growth of ~28% instead of total growth lands it at ≈0.86 — even
  lower; 0.87 is the conservative figure.)

## Why this is not a rerun of 012

**This is not a concealment claim.** 012 (The Two Meters) tried a discretion that hides a number in
an appendix. Here nothing is hidden: Google discloses the 27% openly. The failure is that a bounded,
near-exhausted ratio is **foregrounded** as if it mitigates an unbounded absolute it was never built
to measure. Different failure mode (a metric's structural ceiling, not a reporter's discretion),
different mechanism (a breakeven proof from disclosed numbers, not a pairing of two published
figures), different form (a floor-gauge with an impossible zone, not a twin-invoice register).

## Honesty / self-implication (carried on the work)

1. Not a concealment claim — the trial is of the metric's structure and the report's framing, not of
   Google's candor, which is comparatively high.
2. Google is audited because it discloses most; the problem is least visible where disclosure is least.
3. Fleet PUE covers owned-and-operated campuses only, not leased/colocation facilities — the reported
   ratio is not the overhead of the whole footprint.
4. The breakeven ≈0.86 infers IT-load growth (~28%) from disclosed total growth; stated as such. The
   headroom argument (8.3% vs 27%) needs no inference and is the primary, airtight claim.
5. PUE improvements are real efficiency gains. The critique is not that the number is fake — it is
   that a near-floor ratio is being asked to carry an argument about an absolute it cannot bound.

## The form

An interactive floor-gauge (see `work.astro`). A vertical PUE scale with the physical floor (1.00) as
a hard line and a hatched impossible band beneath it; Google's fleet PUE plotted hugging the floor;
the disclosed absolute (location-based emissions) rising beside it across the same years; and a
**breakeven slider** — set a year's growth, read the PUE that would be required to hold energy flat,
and watch it cross below the floor into the impossible band once growth exceeds 10%. Google's actual
27% lands at ≈0.87. The core exhibit (PUE flat vs absolute rising; 8.3% vs 27%) is legible without
JavaScript; the slider is the only scripted addition.

Sources: `SOURCES.md`. Data: `data.json`. Seed: 0 (no randomness — all figures disclosed or
deterministically derived).
