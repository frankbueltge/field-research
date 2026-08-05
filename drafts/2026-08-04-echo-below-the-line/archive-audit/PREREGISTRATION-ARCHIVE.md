# The archive audit — pre-registered

**Written and committed on 2026-08-05, session 91, BEFORE any collapse was computed and before any
number in this test existed.** Nothing below may be edited once a result exists; deviations go in
`DEVIATIONS.md` as dated diffs.

Proof phase session **3 of at most 3** (Production Amendment, rule 1). The concept is `../CONCEPT.md`;
the day-1 increment is `../INCREMENT.md`; the unscored day-2 pre-registration is
`../day2/PREREGISTRATION-DAY2.md` and stays open.

## Why this test, and why not the one that was planned

The planned move was proof session 3 on a fresh out-of-sample day from the same public news API.
That API refused every request across session 90 (eight refusals, three passes, 03:37–04:06 UTC,
`../day2/provenance/fetch.log`) and refused again this morning — one request at **12:53:52 UTC on
2026-08-05, HTTP 429**, a first request in a fresh session nine hours after the last attempt. The
refusal is not a pacing artifact.

So the test moves onto ground no provider can rate-limit: **the audited instrument's own committed
archive.** *The Consensus* commits a dated snapshot per day (`src/data/consensus/YYYY-MM-DD.json` in
the site repository, public; the human-readable archive is at
https://frankbueltge.de/consensus/archive). Each snapshot carries, for the day's headline cluster and
its runner-up, the **masthead list** — the domains behind the sentence the instrument publishes as
run "word-for-word across N separate outlets".

**The day-2 predictions P1–P3 are not scored by this test and are not retro-fitted to it.** Different
pool, different material, no URL paths available, so the day-1 collapse rule cannot be applied
literally. This is a separate test with its own predictions, scored on its own terms.

## What was already seen before these predictions were written

Reproduced verbatim rather than suppressed, because it visibly hints at the answer and a
pre-registration that hides its author's prior glance is a decoration:

- 46 dated snapshot files carrying clusters; **86 clusters** (headline + runner-up) with masthead
  lists; **596 distinct domains**; 2,270 domain mentions.
- The fifteen most frequent domains, as printed at 12:56 UTC before this file was opened:
  `echo-news.co.uk` (15 clusters), `kilburntimes.co.uk` (15), `harrowtimes.co.uk` (14),
  `hillingdontimes.co.uk` (14), `salisburyjournal.co.uk` (14), `guardian-series.co.uk` (13),
  `chesterstandard.co.uk` (13), `andoveradvertiser.co.uk` (12), `countypress.co.uk` (12),
  `gazette-news.co.uk` (12), `leaderlive.co.uk` (12), `dumbartonreporter.co.uk` (12),
  `gazetteherald.co.uk` (12), `redditchadvertiser.co.uk` (12), `impartialreporter.com` (12).
- One day's rendered page (2026-08-04) was read in full: 23 mastheads, and the instrument's own
  label for that day is `wire/chain syndication`.

**Nothing else.** No grouping was computed, no ownership was looked up, no unit count exists.

## The question

The instrument's published rule counts a title as echo when the identical 6-gram runs on **≥ 3
distinct domains**. This test asks the same question the day-1 increment asked, of the instrument's
own published output over its whole published life:

> When independence is counted at the **publisher** rather than at the **domain**, how many of the
> instrument's own published headline clusters still clear its own ≥ 3 threshold?

## The collapse rule, fixed now, in two stages

### Stage A — mechanical candidates, no judgement

Computed by a committed script, over the domains appearing in any cluster. Two domains are
**candidates** for the same publisher unit if any of:

- **A1 — same registrable domain.** eTLD+1 identity, using an explicit suffix list committed in the
  script (two-label public suffixes such as `co.uk`, `org.uk`, `com.au`, `co.nz`, `co.za`, `com.br`
  and the like are handled; everything else takes two labels).
- **A2 — identical authoritative nameserver set.** The sorted, lowercased, dot-stripped NS tuple,
  queried over DNS-over-HTTPS and written to `provenance/dns-ns.json` with the query timestamp and
  the resolver used.
- **A3 — identical final host after redirects.** `https://<domain>/` followed to its terminus; the
  final hostname recorded in `provenance/http-final.json` with timestamps. Failures are recorded as
  failures and never imputed.

Union-find over A1 ∪ A2 ∪ A3 gives **candidate units**.

### Stage B — the evidence gate, deliberately conservative

A candidate unit of size ≥ 2 counts as a **confirmed publisher unit** only if a **published ownership
source** names its members as belonging to one operator:

- **Primary evidence:** the operator's own published brand / title / station directory, or a member
  site's own imprint or about page naming its parent. A real, retrievable URL, retrieved and
  recorded with a timestamp and the member names it lists.
- **Secondary evidence:** a regulator filing or an equivalently checkable public record. Units
  resting on secondary evidence only are marked `SECONDARY` and reported **separately**, never
  folded silently into the primary figure.
- **No evidence:** the candidate unit is **split back into singletons** for the primary figure.

This direction is chosen deliberately: an unconfirmed merge helps our own finding, so unconfirmed
merges are discarded. The primary number is therefore a **lower bound on collapse** — it can only
understate the effect, never overstate it.

## The predictions, stated before the data

Let, for each headline cluster of a dated snapshot: **N** = the published `domain_count`, **U** = the
number of confirmed publisher units among its mastheads.

- **Q1 — the threshold prediction.** The share of headline clusters with **U < 3** — clusters that
  fail the instrument's own three-outlet rule once ownership is counted — is **≥ 25 %**.
  *Refuted if < 25 %.*
- **Q2 — the magnitude prediction.** The **median N/U** across headline clusters is **≥ 2.0**.
  *Refuted if < 2.0.*
- **Q3 — the prediction against ourselves.** Among the clusters with U < 3, **at least one** is not
  already labelled `wire/chain syndication` (or any other syndication label) by the instrument's own
  `syndication.label`. *Refuted if the instrument already flags every single one* — in which case the
  instrument is not blind to what we are measuring, and the audit's claim shrinks accordingly.

## What each outcome obliges — the bands, fixed now

- **Band 1 — Q1 and Q2 both hold.** The concept has a checkable multi-day result on the audited
  instrument's own record. It may be argued as a Season 1 episode claim in a later session, with the
  wording bounded to these dated snapshots — never "in general", never beyond the days measured.
- **Band 2 — exactly one of Q1, Q2 holds.** The collapse is real and smaller than the day-1 figure
  suggested. Reported at full weight; the day-1 `23.60 % → 3.20 %` is restated in the dossier as
  specific to that day and that pool, not a property of the instrument.
- **Band 3 — Q1 and Q2 both fail.** The day-1 finding does not generalise to the instrument's own
  published clusters. **The concept parks with a one-page finding** under amendment rule 1, and the
  parked finding is itself published: a collapse that does not reproduce on the instrument's own
  archive is a fact about measuring echo.
- **Band 4 — Q3 refuted.** Whatever Q1 and Q2 do, the dossier states at the top, in the same size
  type as the result, that the instrument already labels every failing cluster as syndication, and
  the claim is restated as being about what its **index** counts, not about what it fails to see.
- **Band 0 — the evidence cannot be gathered.** If DNS-over-HTTPS and the ownership sources are both
  unreachable, **nothing is scored**, exactly as day 2 scored nothing. An unverified merge is not a
  result.

## What this test cannot do, said now rather than when it is inconvenient

- It measures the instrument's **published clusters**, not its whole scanned stream. The published
  `echo_index` is computed over all clustered titles; this test can bound what happens to the two
  clusters each day that the instrument publishes with mastheads, and **cannot** recompute the index
  itself, because the archive does not commit the full title list. Any sentence about the index will
  say so.
- Ownership is not independence. Two titles under one owner may still report independently; one title
  may run a wire story with no owner involved at all. What is measured is whether the **count of
  distinct domains** overstates the count of distinct **publishing operations**, which is the
  instrument's own stated subject ("How much of the 'independent' news consensus is really one
  source, copied").
- DNS and redirect evidence describe **today's** infrastructure, not the infrastructure on the day
  the cluster was published. Where that matters — a domain sold between then and now — the ownership
  source's own date is what the confirmation rests on, and the gap is a disclosed limitation.
