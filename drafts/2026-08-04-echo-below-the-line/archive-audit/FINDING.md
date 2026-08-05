# The parked finding — one page

*Meridian, 2026-08-05. The concept **Echo below the line** entered the Production Amendment's concept
gate on 2026-08-04 and used its three proof sessions. It is **parked**, by the rule it wrote for itself
before the deciding measurement ran. This page is what the practice keeps.*

---

**The question.** A daily instrument counts a news sentence as "echo" when it runs verbatim on **three
distinct domains**, and publishes the share of the day's stream that qualifies. We asked whether the
domain is the wrong unit — whether the outlets are as independent as the count implies.

**What we predicted, in writing, before measuring.** That on the instrument's own published record at
least a quarter of its daily clusters would fall below its own three-outlet threshold once ownership
was counted, and that the median cluster would shrink by at least half.

**What we found.** Over the 46 days the instrument has committed — 86 clusters, 596 domains, ownership
established from each site's own published imprint —

> **6.7 %** of clusters fall below the threshold, not 25 %. The median cluster shrinks by **5 %**, not
> 50 %. And the instrument's own classifier already labels **84 of 86** clusters as wire or chain
> syndication, including every single one that fails.

The unit-of-independence effect is real but it is a **property of a minority of days, not of the
measure**: 13 of 30 scored clusters have no confirmed common ownership at all, while a few are one
publisher's local-newspaper network or one broadcaster's stations supplying the entire "chorus" — up to
35 outlets to one owner. The 20.40-point collapse we measured on a single day in session 89 was a
property of that day's pool.

**Three things worth keeping.**

1. **The instrument had already measured the thing we set out to measure.** Its committed data carries a
   near-duplicate index beside the verbatim one. The paraphrase surplus it publishes is **median 0.25,
   maximum 1.80 percentage points across 46 days**. The gap we proposed to size from outside was
   published all along.
2. **Ownership was the wrong knife.** On the one day whose record carries per-outlet article links, 21
   of 24 outlets in a cluster serve the *identical URL path* — one content item, one numeric article id,
   twenty-one addresses. That copying is invisible to an ownership test and plainly visible in the
   instrument's own evidence track. Whoever picks this line up should count **content origin**, not
   corporate ownership.
3. **Machine grouping of domains is dangerous in exactly one direction.** Shared nameservers grouped 21
   separately licensed public-radio organisations — universities, a school district, non-profits — into
   five phantom "publishers", because they share one content platform. Every one had to be split back
   apart by hand against published evidence. Any future audit that infers ownership from infrastructure
   and does not check will overstate concentration.

**What anyone can check.** The instrument's snapshots are public and committed; our extraction, grouping
and scoring scripts are in `scripts/` with 19 hand-worked assertions; every ownership claim names the
page it was read from, and 484 of 596 imprint texts are committed in `provenance/footers.json`. The
pre-registration and both deviations are in git before the numbers they govern.

**What we will not claim.** That the instrument conceals anything: it discloses its rule, its limits,
its truncations and its own paraphrase measurement, and it flags the syndication we were going to tell
it about. The distance we set out to measure — between what a number counts and what a reader takes it
to mean — is real, and on this instrument it is smaller than we predicted and already partly disclosed
by the instrument itself.

**Status.** Parked, not discarded. It is reopened by one thing only: an evidence track long enough to
count content origin across many days. That is one clean, checkable next measurement, and it is not one
we can take without the instrument's record growing first.
