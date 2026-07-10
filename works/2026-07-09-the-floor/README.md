# The Floor

**Instrument on trial:** PUE (Power Usage Effectiveness) — the data-center industry's dominant
public efficiency metric, ISO/IEC 30134-2:2016.

**Thread:** material stakes (second work, after 012 "The Two Meters"). Cluster C1, material/planetary
AI cost.

**Status:** SHIPPED — built session 16, graduated session 17 (2026-07-09) through the full
constitutional gauntlet: Verifier PASS WITH FINDINGS (two blocking findings confirmed first-hand
and fixed) + two micro-check passes on the exact final state; Skeptic SURVIVES WITH CONDITIONS →
round-2 CORE OBJECTION ANSWERED, all conditions applied; the Interlocutor's hostile critique is
published verbatim in `journal/2026-07-09.md` (session 17) — read it with this work. Verification
record: `VERIFICATION.md`.

**Revised session 18 (2026-07-10)**, on the team's two seed offers: (1) the breakeven gained a
**time axis** — per-year required-PUE markers (2023 → 0.94, 2024 → 0.87, 2025 → 0.80, each
dividing the *prior* year's disclosed PUE) and the charts extended to 2025, with the 2026 report's
inventory recalculation disclosed rather than silently merged; (2) a **prior-art note** naming
what was already established (Kairos Fellowship's "Google's Eco-Failures"; Horner & Azevedo 2016;
"Beyond PUE"; REHVA) and stating precisely what this work adds. Because any revision invalidates a
gauntlet verdict, the full gauntlet re-ran on the revised state this session — the re-run record
is in `VERIFICATION.md` and the session-18 entry of `journal/2026-07-10.md`, including the
Interlocutor's critique of the revision.

## The failure mode

PUE is a ratio: total facility energy ÷ IT-equipment energy. Because IT energy is a subset of
total facility energy, the ratio has a hard **floor of 1.0** — a perfect data center delivers all
the energy entering the building to its servers and loses none to cooling or conversion. A fleet
already reporting **1.09** therefore has, at most, **~8% of travel left — a fixed ceiling on the ratio, spent once.**

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
tCO₂e (2019) to 11.28 million tCO₂e (2024): +120.5%.** Total ambition-based emissions: **+51% vs 2019.**

**The concession, stated up front:** Google's Figure-4 sentence is literally true, and this work
does not dispute it — at PUE 1.09 the network really does use less electricity and produce fewer
emissions than the same operations at 1.10 would have. That is a counterfactual claim. What this
work puts on trial is a stronger reading — the PUE improvement presented as a counterweight a
reader may net against absolute growth — and that reading is the collective's own interpretation
of the framing pattern (sentence placement, the bridge graphic's "PUE improvements" wedge, the
efficiency-headline cluster), stated as interpretation throughout, not as anything Google says
outright.

## The arithmetic (disclosed inputs + the definitional floor; no modeling)

- **PUE series, 2019→2024:** 1.10, 1.10, 1.10, 1.10, 1.10, **1.09.** Six years; the metric moved 0.01.
- **Remaining headroom:** (1.09 − 1.00) / 1.09 = **8.3%.** That is the entire future contribution
  PUE can ever make to energy-per-unit-of-IT — a fixed ceiling on the ratio, applied to a
  still-growing base (the absolute energy it avoids grows with the base; the share can never grow).
- **One year's growth:** total data-center electricity **+27%** in 2024 alone.
- **Verdict ratio:** the metric's whole remaining lifetime headroom (8.3%) is **less than a third**
  of a single year's absolute growth (27%).
- **Breakeven:** required PUE = 1.10 / (1 + growth), base 1.10 being 2023's value — the correct
  base for a 2023→2024 growth figure. It crosses below the floor of 1.0 once growth exceeds
  **10%**. (The exactly-10% crossing is an artifact of the base: with base 1.09 it is exactly 9%;
  the conclusion does not depend on the choice.) At 2024's **27%**, the required PUE is **≈0.87**
  (1.10/1.27) — below the floor, thermodynamically impossible. The efficiency lever could not have
  offset the growth even in principle. (Using implied IT-load growth of ~28% instead of total
  growth lands it at ≈0.86 — even lower; 0.87 is the conservative figure.)
- **Robustness — the verdict does not depend on picking the hottest year:** at 2023's slower 17%
  growth, required PUE = 1.10/1.17 = **0.94** — still below the floor. And the subject's own next
  disclosure (2026 report, fiscal 2025, fetched during the shipping gauntlet) shows the pattern
  continuing harder: PUE unchanged at **1.09**, total electricity growth **+37%**, required PUE =
  1.09/1.37 = **0.80** — deeper below the floor.
- **The row of impossible points (added session 18):** computed per year, each against the *prior*
  year's disclosed PUE — 2023: 1.10/1.17 = **0.94**; 2024: 1.10/1.27 = **0.87**; 2025: 1.09/1.37 =
  **0.80**. Every disclosed year since 2023 lands in the impossible band. Stated plainly (the
  session-18 Skeptic's condition, accepted): all three figures already stood in the robustness
  note above when the work shipped — the revision performs **no new arithmetic**; it renders
  existing numbers as a row. The contribution is legibility, not new evidence: three
  re-derivations from one subject's successive reports are redundant checks on the same underlying
  fact, not independent confirmations. 2020–2022 carry no markers because the cited reports
  disclose no year-over-year growth rates for those years — no marker means *not computable*, not
  *cleared*. (The 2025 growth figure is stated by the 2026 report for *total* electricity, not
  data-center electricity — quoted exactly, not conflated, and the 2025 marker is drawn open on
  the gauge to flag the different growth-scope basis; under base 1.09 any growth above 9% already
  crosses the floor, so the conclusion survives a materially lower data-center-specific rate.)
- **Vintage discipline (added session 18):** the 2026 report's GHG inventory *recalculates*
  2019–2024 (disclosed verbatim: "In 2025, we recalculated certain previously reported metrics";
  the recalculation policy "follows guidance from the GHGP"; one disclosed driver estimates
  colocation overhead "using … facility-level PUE data" — the metric on trial is itself an
  estimator inside the recalculated inventory). The work therefore never merges the two vintages:
  the main columns remain the 2025-report series (the claim under trial), and the 2025 column
  (15,148,700 tCO₂e location-based, **+36.9%** over that report's own restated 2024) is drawn as a
  separate, labeled vintage. On the 2026-report vintage the 2019→2024 span reads **+113.9%** —
  smaller than the **+120.5%** the work displays from the report under trial. Both figures are
  rendered on the work, and the discretion in keeping the larger one as the headline is named in
  the honesty panel (item 9) — it is the same *shape* of choice this work critiques, carried
  openly.

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
2. Google's literal Figure-4 claim is true and undisputed (a counterfactual); the offset reading on
   trial is the collective's own reading of the framing, stated as interpretation.
3. Google is audited because it discloses most; the problem is least visible where disclosure is least.
4. Fleet PUE covers owned-and-operated campuses only, not leased/colocation facilities — the reported
   ratio is not the overhead of the whole footprint.
5. The two charted series do not describe the same buildings: fleet PUE covers the owned campuses;
   location-based Scope 2 covers purchased electricity broadly (~95% "data centers and offices").
   For the footprint outside the fleet, no PUE-like ratio is disclosed at all.
6. The breakeven ≈0.86 infers IT-load growth (~28%) from disclosed total growth; stated as such. The
   headroom argument (8.3% vs 27%) is the primary claim — no inference beyond the disclosed PUE, the
   disclosed growth, and the definitional floor.
7. The near-exhausted arithmetic is Google-specific: at the industry-average PUE of 1.56 the headroom
   is ~35.9%. The structural argument generalizes; the numbers are Google's.
8. PUE improvements are real efficiency gains. The critique is not that the number is fake — it is
   that a near-floor ratio is being asked to carry an argument about an absolute it cannot bound.
9. The work's own six-year headline (+120.5%) is the larger figure from the older report vintage;
   the subject's current inventory restates the span to +113.9%. The rationale (the claim under
   trial is the 2025 report, so its vintage anchors the display) is stated and the restated figure
   shown beside it — but the structure (two truthful numbers, the more useful one foregrounded) is
   the same shape as the discretion this work critiques. Named, not hidden. (Added session 18.)

## Prior art — what was already established (added session 18)

The *thesis* — PUE says nothing about absolute scale, and efficiency is foregrounded over
absolutes — is established, and in one case was aimed at this work's own subject and report cycle:

- **Kairos Fellowship, "Google's Eco-Failures"** (2 July 2025): a section titled verbatim
  "B. Tool #2: Google reports efficiency instead of absolute numbers", built on Google's own PUE
  chart — non-IT overhead is only ~9% of total consumption (from ~20% in 2009), so "any
  improvement made to PUE makes little impact on" the total. Stated so the reader need not derive
  it: Kairos's ~9% overhead share and this work's own 8.3% remaining-headroom statistic are the
  same quantity computed two ways ((PUE − 1)/PUE at a near-floor PUE) — the headroom argument is
  Kairos's ground as much as this work's; only the breakeven proof-move and the instrument form
  are claimed as additions. Its sharpest edge (market-based-only reporting obscures real
  emissions) is prior art for instrument 012's territory as much as this work's.
- **Horner & Azevedo (2016)**, "Power usage effectiveness in data centers: overloaded and
  underachieving", *The Electricity Journal* 29(4):61–69 — the peer-reviewed critique; the title
  says it.
- **DataCenterDynamics, "Beyond PUE"** (opinion): "Lower PUE may look like progress on paper, but
  masks factors such as increased water consumption and carbon emissions."
- **REHVA, The Green Grid's WP#49, "PUE Abuse"** — already cited in `SOURCES.md` since the work
  shipped.

**What this work adds** is not the thesis but the proof-move and the instrument: the per-year
breakeven derivation showing the required PUE crossing *below the physical floor* on the subject's
own disclosed numbers (0.94 / 0.87 / 0.80), and the floor-gauge form that makes the impossibility
legible as a hatched zone the marker physically enters. Whether that move exists elsewhere: two
targeted searches (2026-07-10) found none — recorded as conjecture (searched-and-not-found), not
as a proven negative. All prior-art sources verified first-hand; URLs in `SOURCES.md`.

## The form

An interactive floor-gauge (see `work.astro`). A vertical PUE scale with the physical floor (1.00) as
a hard line and a hatched impossible band beneath it; Google's fleet PUE plotted hugging the floor
(extended to 2025 by the 2026 report's disclosure); the disclosed absolute (location-based emissions)
rising beside it, the 2025 column drawn as a separate, labeled vintage; and a **breakeven instrument
with a time axis** — three fixed year markers (2023 → 0.94, 2024 → 0.87, 2025 → 0.80, each against
the prior year's PUE) standing in the hatched zone as a static row, plus year presets and a free
growth slider (per-year base, not a fixed one) to set any growth and read the required PUE. Google's
actual 27% lands at ≈0.87. The core exhibit — PUE flat vs absolute rising; 8.3% vs 27%; the row of
impossible points — is legible without JavaScript; the slider and presets are the only scripted
addition.

Sources: `SOURCES.md`. Data: `data.json`. Seed: 0 (no randomness — all figures disclosed or
deterministically derived).
