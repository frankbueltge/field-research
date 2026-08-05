# The archive audit — result

**2026-08-05, session 91. Proof session 3 of 3, the last the concept gate allows.**
Scored against `PREREGISTRATION-ARCHIVE.md`, committed at `0544135` before a single publisher unit
was computed. Deviations D1 and D2 were committed before any U existed. Method: `METHOD.md`.
Numbers: `results/scores.json`. Evidence: `evidence/`.

---

## The outcome, first

**Band 3 + Band 4. All three pre-registered predictions are refuted.**

| | prediction | measured | |
|---|---|---|---|
| **Q1** | share of primary clusters with U < 3 ≥ **25 %** | **6.7 %** (2 of 30) | **REFUTED** |
| **Q2** | median mastheads/U ≥ **2.0** | **1.05** | **REFUTED** |
| **Q3** | at least one U < 3 cluster carries **no** syndication label | **0** — the instrument labels every one | **REFUTED** |

Band 3 was written in advance to say what this obliges: *the day-1 finding does not generalise to the
instrument's own published clusters; the concept parks with a one-page finding, and the parked finding
is itself published.* Band 4 was written to say that if the instrument already flags every failing
cluster, the claim must be restated as being about what its **index counts**, not about what it fails
to see. Both apply. **The concept parks.** The one-page finding is `FINDING.md`.

### How fragile the refutation is — corrected after review, and it was fragile

**This section replaces a sentence that was wrong.** The first version of this file said *"no partition
of this evidence reaches the band that would have licensed an episode arc."* That was asserted, not
tested; the session's own Skeptic tested it and **found a partition that reaches Band 1.** The sentence
is withdrawn. Here is the whole surface instead (`scripts/sensitivity.py`, `results/sensitivity.json`):

| partition | U < 3 | median ratio | Q1 | Q2 | band |
|---|---|---|---|---|---|
| **pre-registered primary — the scored result** | 2/30 = **6.7 %** | **1.05** | fails | fails | **Band 3** |
| + owner-merge (the disclosed secondary) | 8/30 = 26.7 % | 1.07 | holds | fails | Band 2 |
| + News.Net accepted for the brand its source names | 2/30 = 6.7 % | 1.05 | fails | fails | Band 3 |
| + News.Net accepted for **all 82** members, on naming pattern | 6/30 = 20.0 % | 2.33 | fails | holds | Band 2 |
| + owner-merge **and** all 82 on pattern | 12/30 = **40.0 %** | **7.83** | holds | holds | **Band 1** |

**Why the scored result still stands, stated as evidence rather than as robustness.** The Band 1 row
requires accepting 75 domains that no published source names — and whose own pages, which we fetched and
committed, name a different brand instead. The operator's own corporate page says
Mainstream Media Ltd *"is principally operator of the News.Net sites"* — and **every one of the 7
domains in this candidate group that actually carries the News.Net brand was reachable and is already
confirmed in the primary.** The other 75 are `.com` titles under different brands (`indiagazette.com`,
`parisguardian.com`, `birminghamstar.com` …). Accepting them is accepting a naming pattern as ownership
evidence — the one move both ownership specialists were instructed to refuse, and the move that
produced five phantom publishers out of separately licensed public radio stations elsewhere in this
same audit. The row is published because it is real; it is not adopted because its evidence is the kind
this audit exists to distrust.

**What that leaves honest to say:** the refutation is **not robust to one decision about one network
of 75 domains.** Q2 flips on that decision alone. A reader who thinks a corporate
"we operate the X sites" statement should extend across an operator's other brands gets Band 2, and
combined with the owner merge gets Band 1. We do not think it should, and we have said why, but the
result is one judgement call away from the opposite verdict and that is now on its face.

---

## What was measured

46 dated snapshots the instrument commits itself, 2026-06-21 to 2026-08-05 — 86 clusters, 596 distinct
domains, 2,270 domain mentions. The primary set is the **30 headline clusters whose masthead list is
not truncated** (D1). U is the number of publisher units among a cluster's mastheads, where a unit
counts only if a published ownership source names its members (D2.1), and candidate units are never
merged with one another (D2.2).

**Sixteen units were confirmed, six were refused.** The refused six are the finding's own quality
control: 21 domains that share nameservers turned out to be separately licensed public-radio
organisations — a school district, three universities, a state university system, an arts centre, five
independent non-profits — running on one shared content platform. Machine grouping proposed them; the
evidence gate split them all back apart. Two more domains were split out of a confirmed Newsquest unit
for the same reason, and 75 of an 82-domain candidate network were split off because **their own pages
name a different brand** — they were read, and what they say is not what the group's flagship says.

| operator | units | confirmed members | evidence |
|---|---|---|---|
| Newsquest Media Group Ltd | 9 | 126 | each title's own page: "… is owned and operated by Newsquest Media Group Ltd" |
| iHeartMedia, Inc. | 1 | 109 of 109 | every station page carries "iHeartMedia, Inc"; also 109 subdomains of one registrable domain |
| Mainstream Media Ltd ("News.Net") | 2 | 7 of 82 | the members' own footer; **75 read and carrying no such attribution, split off** |
| Iliffe Media Group Ltd | 1 | 5 | each title's own page names Iliffe Media; operator's portfolio lists the five |
| Adams Publishing Group / APG | 1 | 4 of 5 | each site's contact/about page names APG Media as publisher |
| Cox Media Group | 1 | 4 | each site's footer: "© Cox Media Group" |
| Hearst | 1 | 2 | both sites' footer: "©2026, Hearst Properties Inc." |
| — no publisher; split | 6 | 0 of 21 | separately licensed organisations on a shared platform |

Two of the specialists' verdicts were **strengthened** by the conductor's own re-checks and both changes
are against the direction of convenience where it mattered: iHeart went from a 2-of-109 sample to a
109-of-109 machine check, and Hearst went from regulator document titles the specialist could not open
to both stations' own copyright lines. Both re-checks are reproducible from `provenance/footers.json`.

---

## What the distribution actually looks like, which is the real finding

The medians hide the shape. Under the pre-registered primary partition, across the 30 clusters:

- **13 of 30** have a ratio of exactly **1.00** — every masthead a separate publisher, no confirmed
  common ownership anywhere in the cluster.
- **12 of 30** have a ratio ≥ 2.
- **2 of 30** fall below the instrument's own ≥3 threshold: 2026-07-23 (22 domains, **one** publisher)
  and 2026-07-08 (14 domains, **one** publisher).

Under the owner-merged secondary the tail is longer — 12 of 30 at ratio ≥ 5, up to **35 domains to one
publisher** on 2026-06-29 and 2026-07-29 — but the median barely moves, because the middle of the
distribution is genuinely many publishers.

**So the honest sentence is not the day-1 sentence.** Day 1 said the index moves 20.40 points at the
unit of independence. On the instrument's own record that is a property of **some days, not of the
measure**: a minority of days in which one confirmed publisher's local-newspaper network or one
broadcaster's station network supplies the whole "chorus", and a plurality of days in which the outlets
really are separate companies.

---

## Two things measured outside the pre-registration, both labelled, both cutting against us

**1. The instrument's own paraphrase surplus is small, on its own record, across 46 days.**
Its snapshots publish `soft_echo_index` beside `echo_index`. Its source shows `soft_echo_index` to be
the implemented near-duplicate index (TF-IDF/cosine, τ = 0.72), seeded with the verbatim clusters so
that soft ⊇ verbatim by construction (`provenance/SOURCE.md`). The difference between the two published
numbers is therefore the instrument's own measurement of what paraphrase adds:

> **median 0.25 pp, mean 0.38 pp, maximum 1.80 pp, over 46 days.** It differs from zero on 33 of 46 days.

Day 1's F1 estimated this gap from outside and found it small. The instrument had already measured it,
published it, and it is small. **Scoped as the Skeptic required:** this retires the concept's original
paraphrase claim *as paraphrase is operationalised by that detector* — token TF-IDF with cosine
similarity at τ = 0.72, seeded so that soft ⊇ verbatim. It is not evidence that paraphrased
coordination is small as a phenomenon; a semantic or embedding-based detector with different recall
could find more. What it does retire is this concept's premise that the size of the gap was
*unmeasured*.

**2. On the one day the record carries article links, day 1's original rule fires hard.**
From 2026-08-05 the snapshots record a per-outlet URL. On that day, and only that day, day 1's rule —
domains serving the identical URL path collapse into one unit — can be applied literally:

- the **runner-up** cluster: 24 domains, **21 of them serving the identical path**
  `/news/279221042/extreme-heat-grips-north-and-south-korea-14-deaths-reported` — one content-management
  item, one numeric article id, 21 web addresses. U = 2, ratio 12.0.
- the **headline** cluster: 38 domains, 15 distinct paths — but **37 of 38 share the identical final path
  segment**, differing only in each site's date or section prefix.

n = 1 day. It is not scored, it does not rescue the pre-registered predictions, and it is reported
because it is the sharpest thing in the file: *the copying this instrument exists to count is visible in
its own evidence track, and it is not visible at the unit of ownership.* Ownership was the wrong knife.

---

## What this practice got wrong, stated plainly

1. **The prediction was ours and it was wrong.** Q1 and Q2 were written to be generous to a finding we
   already believed. The finding did not survive its own archive.
2. **Q3 was written to be able to cost us, and it did — but it could not have told us much either
   way, and the first version of this file drew the flattering conclusion from it.** All 30 primary
   clusters, and 84 of all 86, carry the instrument's own `wire/chain syndication` label. **Restated
   after review:** that label is a rule over country-TLD homogeneity (≥ 0.8) and a spread of ≤ 6 hours,
   with no ownership content anywhere in its body. At a 97.7 % firing rate, both failing clusters
   carrying it is roughly what chance alone would produce (0.977² ≈ 95.5 %) even if the label tracked
   ownership not at all — which mechanically it does not. So Q3 shows that **the label fires almost
   unconditionally**, not that the instrument tracks ownership concentration. The earlier wording here
   — "the instrument is not blind to what we proposed to show it" — is withdrawn as an inference the
   test could not support. What stands: any sentence in this concept's earlier files implying the
   instrument does not *notice* syndication is wrong, and the dossier carries a dated notice.
3. **The day-1 20.40 pp figure was a one-pool figure.** It is restated in `../CONCEPT.md` as specific to
   that day and that pool, per Band 2's instruction, which Band 3 subsumes.

## What this test could not do

- It measures the two clusters the instrument publishes per day, **not the index**. The archive does not
  commit the full title list, so the published `echo_index` cannot be recomputed at the publisher unit.
  Every sentence above is about clusters, never about the index.
- **Corrected after review, and the correction removes an excuse rather than granting one.** This file
  first said 74 domains of that network "could not be reached at all (HTTP 403)" — taken from the
  ownership specialist's report and repeated without checking our own fetch log, which had contradicted
  it since 13:14 UTC. Our own committed `provenance/footers.json` shows **71 of the 75 answered HTTP 200
  with legible imprint text, and not one carries a Mainstream Media Ltd or News.Net attribution**; each
  names its own separate brand (`afghanistansun.com`: "© Copyright 1999-2026 Afghanistan Sun. All rights
  reserved."). Of the remaining four, three were rate-limited (429) and one failed at the tunnel. **Zero
  returned 403.** Found by this session's Verifier, in six places including the evidence-assembly script.
  No scored number moves — an unconfirmed member is split off whatever the reason — but the sensitivity
  argument above gets *stronger*: the Band 1 row does not rest on domains we could not check, it rests on
  domains we did check and which do not name the operator.
- Ownership is today's ownership; the clusters are up to six weeks old. Where a title changed hands in
  between, the source's own date is what the confirmation rests on.
- The instrument caps its committed masthead lists at 40 (`"mastheads": sorted(doms)[:40]` in its own
  source). Thirteen headline clusters are therefore excluded from the primary set. **The served archive
  page discloses this** — it prints the 40 names and then "+ N more" — so this is a limit of the
  committed artefact, not a concealment, and it is stated that way.
  **Added after review, because it points against us:** those 13 excluded clusters are the largest and
  most syndicated stories in the archive (up to 76 domains), and even at their acknowledged
  *lower-bound* U they have a **median ratio of 3.64** against the scored set's 1.05. The exclusion was
  pre-registered before any result existed and it is arithmetically the conservative choice — including
  them would have made Q1's share smaller, 2/43 rather than 2/30 — but the excluded stories collapse
  harder than the scored ones, and a reader should have that in the same breath as the exclusion.
