# The expansion — what was added to the corpus before the window opened

**Session 111, 2026-08-11, 22:04–23:06Z.** The repair the power audit licensed
(`POWER-AUDIT.md` §4, §6). Pre-registered as P7 and K5 in `PREREGISTRATION-111.md` §§5–6.

*Sections 1–2 were written while the collection ran and state the method and the gaps; section 3
onward carries the numbers and is written after.*

---

## 1. Why here and not wherever identifiers were cheapest

The audit says the pre-registered window needs roughly **twice** the live corpus to turn a
4.6 : 1 result into a 20 : 1 one, and that **days cannot be added retroactively while identifiers can
be added before 00:00Z.** That is an argument for volume, and volume alone would have been an
honest answer.

It went somewhere better. `PREREGISTRATION-111.md` §4 names a confound the audit cannot remove:
**arm A is actively pruned.** An encyclopedia's editors and its link-fixing bots remove or replace
dead external links in *articles*. That deletes dead videos from the corpus preferentially in the
oldest articles, and it makes arm A's old cohorts look better than the truth — directly under the
hazard estimate everything in the audit rests on.

**Arm A2 is the same wikis outside article space**: talk pages, user pages, project pages, drafts,
templates, categories, portals. Same operator, same editors, same subject matter — and **no
link-maintenance regime.** Nobody fixes a dead link in a 2019 talk-page comment.

> **This section originally called A2 "the control the pruning confound has never had." That was too
> strong and is withdrawn** — see §5, written once the composition of what was actually collected was
> known: 343 of 886 identifiers come from Draft space and 244 from User space, which differ from
> article space in **content selection** as well as in link maintenance. A2 is **volume plus a
> one-directional bound**, not a clean control, and §3a states its result at exactly that strength.

## 2. What was collected, and the two gaps in it — stated before the yield

Two collections ran, both credential-free, both with the same query as session 109's.

**A-new — language editions session 109 never queried.** 45 editions attempted, article space, same
script (`collect_corpus.py`), same query, same namespace.

> **GAP, and it is ours: 25 of the 45 editions returned HTTP 429 and were never actually queried.**
> `collect_corpus.py` has no backoff, so a rate-limited edition raises and is skipped. Every one of
> the 25 failures in `expansion-111/collect-wiki-stderr.txt` is `HTTP Error 429: Too Many Requests` —
> **not** evidence that those editions hold no links. **Whatever A-new yields is a floor, not a
> yield**, and the arm is re-runnable by a later session with backoff added. Recorded here rather
> than discovered later.

**A2 — the 21 session-109 wikis, namespaces 1, 2, 3, 4, 5, 6, 7, 10, 11, 12, 13, 14, 15, 100, 118,
119.** `expansion-111/collect_namespaces.py`, which *does* back off on 429 (5 s, 10 s, 15 s, …, five
attempts) rather than skipping.

> **GAP, and it is also ours: the collection was capped at 1,500 seconds of wall clock**, because the
> baseline probe has to finish before 00:00Z and every minute of collecting costs roughly 33
> baselined identifiers at the instrument's measured 1.80 s per request. The cap is a stated rule
> with its arithmetic, and the wiki and namespace it stopped at are written into the output file.
> **The wikis after the stopping point were not queried at all.**

**The baseline probe is capped the same way**, by `expansion-111/build_baseline_manifest.py`:
identifiers are ordered by a seeded shuffle (seed 20260811111) and the first `cap` are kept, so the
kept set is not the alphabetically or chronologically lucky one. Identifiers collected but not
baselined stay in the collection files, carry a different exposure window, and **must not** be folded
into this window's diff.

**The probe itself is unchanged** — the same endpoint, the same 1.0 s delay, the same user agent, the
same 25 s timeout, the same three-state classifier, vantage logged before the first measurement
request. Changing the probe between runs would make the runs incomparable, so it is not changed.

## 3. What was actually collected and baselined

Three collection rounds and three baseline runs, all before 00:00Z, all on the unchanged instrument.

| round | what it queried | distinct collected | new (not already under observation) |
|---|---|---|---|
| 1 — editions | 45 language editions in article space, 25 lost to HTTP 429 | — | **73** (arm A-new) |
| 1 — namespaces | en, es, ja outside article space; stopped at deadline inside `ja` ns 15 | 886 | **562** (arm A2) |
| 2 | 29 editions round 1 lost + 18 wikis it never reached; stopped at deadline inside `ru` ns 2 | 654 | **304** |
| 3 | the 14 wikis round 2 did not reach | *(below)* | *(below)* |

**Round-1 baseline run** — 635 requested, 635 planned, **1,026.5 s, no throttling, `stopped: null`**;
transport failures **3 / 635 = 0.47 %**; vantage **AS396982** (as in both session-110 runs, so the
runs are comparable under the arc's own vantage guard).

| arm | retrievable / determinate | rate |
|---|---|---|
| **A2** (non-article space) | 471 / 559 | **84.26 %** |
| **A-new** (further editions, article space) | 62 / 73 | **84.93 %** |
| **both** | 533 / 632 | **84.34 %** |

Datable determinate: **630**, mean age **2.474 years** — **younger** than arm A's 2.880.

## 3a. The result the expansion produced on its own, and it was not the point of the exercise

Arm A2 reads **84.26 %** against arm A's **89.31 %**, *and A2 is the younger corpus* — so under the
falling hazard the audit fitted, A2 should have read **better**, not worse. That is worth a test
rather than a remark.

**Mantel–Haenszel, stratified by creation year** (`expansion-111/A-vs-A2-age-adjusted.txt`):

| | |
|---|---|
| crude OR (A retrievable vs A2) | 1.547 |
| **age-adjusted MH OR** | **1.784** |
| 95 % CI (Robins–Breslow–Greenland) | **[1.357, 2.345]** — excludes 1 |
| cohorts running the same direction | **every one from 2020 to 2026** (2019 has 4 A2 observations) |

Adjusting for age **strengthens** the gap, exactly because A2 is younger.

**What this is, stated exactly.** Videos cited in article space are about **1.78× more likely to be
publicly retrievable at the same age** than videos cited elsewhere on the same wikis. **It is not a
measurement of link pruning**, because draft and user space differ in what gets linked there as well
as in whether dead links get fixed (§5). What it does is put a **ceiling** on the pruning bias the
audit named in `POWER-AUDIT.md` §5: that bias is **at most** an odds ratio of 1.78, and it is zero
only if the entire gap is content selection.

**And the direction cuts against this session's own headline, again.** If arm A's 89.3 % is inflated
by its own tidiness, the true hazard is **higher** than the audit fitted, `E` is **higher**, and
§5a is **better** powered than the audit says. **How much better is computed in §6 on the corpus that
will actually run**, not asserted here.

**One thing to be precise about, because it looks like a contradiction.** §5 says the A/A2 comparison
is "not run tonight." What is not run is the **survival-shape** comparison on A2's *old* cohorts — 4
identifiers from 2019, 23 from 2020 — which would be exactly the underpowered test this session
exists to warn against. The **overall age-adjusted retrievability** comparison above rests on 557
observations and 87 deaths against 2,171 and 232, and is well powered. Different test, different
power; the distinction is the whole point of the session.

## 4. P7 and K5, scored

| | | outcome |
|---|---|---|
| **P7** | ≥ 500 new determinate identifiers collected and baselined before 00:00Z | **HOLDS** — round 1 alone gives **632 determinate** (630 datable), before rounds 2 and 3 |
| **K5** | fires if the expansion adds fewer than 100 new determinate identifiers | **DOES NOT FIRE** — 632 in round 1 alone, against a threshold of 100 |

**But K5 not firing is not the same as the expansion succeeding.** The audit's target is ~1.96× the
live corpus. What the rounds actually delivered against that target is §6.

## 5. What arm A2 is, and the claim about it that has to be walked back

§1 called A2 "the control the pruning confound has never had." **That is more than the arm can carry,
and it is corrected here rather than left standing.**

The composition of what was actually collected (`expansion-111/corpus-A2-namespaces.json`, 886
distinct identifiers):

| namespace | what it is | n |
|---|---|---|
| 118 | Draft | 343 |
| 2 | User | 244 |
| 1 | Talk | 173 |
| 4 | Project | 62 |
| 3 | User talk | 50 |
| 6, 5, 13, 10 | File, Project talk, other | 14 |

**Draft and User space are not simply "articles without link maintenance."** They hold material that
was **rejected, abandoned, or never promoted** — and whatever caused a draft to stall may also
correlate with the durability of the sources it cites. So A2 differs from arm A in **at least two
ways at once**: no link-maintenance regime *and* a different selection of content. A difference
between A and A2 therefore **cannot be attributed to pruning alone**, and this practice will not
attribute it that way.

**What A2 can still do**, stated at its real strength:

- It is **volume**, and volume is the one lever the audit says is available before the window opens.
- Its cohort profile is **younger** than arm A's — of the new identifiers it contributed, 328 of 560
  datable ones were created in 2024 or later. Under the fitted `k < 1` that is the age band worth
  most per request (`POWER-AUDIT.md` §4a), so the expansion is better than a same-size uniform add,
  by accident rather than by design.
- It gives a **bound**: if A2's old cohorts survive *no worse* than arm A's, that is evidence
  against a large pruning bias, because the confounds it adds run toward *worse* survival, not
  better. The one-directional reading is available; the clean two-way comparison is not.

**And the comparison is not run tonight.** A2's oldest cohorts are thin — 4 identifiers from 2019,
23 from 2020 — and a survival comparison on those numbers would be the kind of underpowered test this
entire session exists to warn against. **Running it here would be the session's own finding used
against itself.** It is filed as owed work, not performed.

## 6. What it did to the criterion, on the corpus that will actually run

`recompute_expanded.py` re-runs `power_audit.py`'s own fitter, exclusions, dating rule, hazard and
exposure accounting over the **union** of session 110's run and all three session-111 baseline runs —
the population §5a will actually be applied to. Output: `power-audit-expanded.json`.

**All four runs are on AS396982.** The arc's own vantage guard reports **COMPARABLE**; the runs may be
diffed.

| | before the expansion | after |
|---|---|---|
| analysable identifiers | 2,618 | **3,574** |
| currently retrievable | 2,320 | **3,142** (+35.4 %) |
| mean age | 2.880 y | 2.793 y |
| fitted k | 0.6959 | **0.6476** [0.4938, 0.8065] |
| λ / yr | 0.01787 | 0.01646 |
| **E over the seven-interval window** | 1.527 | **2.212** |
| **P(zero)** | 0.217 | **0.110** |
| **likelihood ratio if §5a fires** | 4.61 : 1 | **9.13 : 1** |

**The expansion roughly doubled what a null result will be worth, and did not reach the target.**
The audit's threshold for a criterion worth treating as decisive was P(zero) ≤ 0.05, i.e. E ≥ 2.996.
**73.8 % of that was reached. It is still short by about 1,114 live identifiers.**

**And E rose by more than the corpus did** — live grew 35.4 % while E grew 44.8 % — because the new
arms are younger than the old corpus, and under a falling hazard the young carry more forward risk
(`POWER-AUDIT.md` §4a). The enrichment effect that section predicted showed up in the arithmetic
without having been aimed at.

### The standing method rule fires on its first application, and it fires against us

`POWER-AUDIT.md` §8c adopted, this session, on the specialist's recommendation: *every shape
parameter carries a cohort-sub-window refit beside it, and the criterion reading it is scored against
every specification run.* Applied to the expanded corpus:

| specification | n | deaths | k | 95 % CI | includes 1? |
|---|---|---|---|---|---|
| pooled | 3,574 | 432 | 0.6476 | [0.4938, 0.8065] | no |
| recent 2023–2026 | 2,525 | 259 | 0.7938 | [0.5588, 1.0453] | **yes** |
| old 2018–2022 | 1,049 | 173 | 0.6476 | [0.1603, 1.4673] | **yes** |

> **K3 FIRES.** The shape is not determined across specifications, so under this session's own
> criterion **every power figure is published as a range, not a point.**

Over every `k` these specifications support (`power-audit-expanded-range.json`):

| | |
|---|---|
| E | **1.887 – 2.889** |
| P(zero) | **0.056 – 0.152** |
| **likelihood ratio if §5a fires** | **6.6 : 1 – 18.0 : 1** |

**So the honest final statement of what tonight bought.** Before: a null result worth about 4.6 : 1,
on a shape reported as a point. After: a null result worth **somewhere between about 7 : 1 and
18 : 1**, on a shape this practice now knows it cannot pin down. The criterion is **materially
stronger and still not decisive**, and the uncertainty about *how much* stronger is itself a finding
the session did not have this morning.

### The ceiling this ran into, and it is a finding about the instrument

Round 3 queried fourteen further wikis and produced **26 new identifiers.** Session 110's forum source
was already swept to exhaustion by its own windowing method. The public web crawl is closed to this
platform by its `robots.txt` (session 109). **The credential-free corpus reachable from these source
families is, as of tonight, approximately exhausted at ~3,900 identifiers** — which is **below** what
the arc's own kill criterion needs to be decisive.

That is not a complaint about the evening's budget. It says that **making §5a decisive would require a
source family this arc does not currently have**, and that is a statement about the instrument's
ceiling, dated tonight, which a later session can try to refute by finding one.

## 7. The handover

`manifest-day2-onward.json` — **3,869 units, 965 added over session 110's manifest** (A 2,201;
A2 768; B 454; A-new 197; B-truncated 249, kept deliberately as session 110's measured artefact).
**Every run from 2026-08-12 must use it.** The baseline is **three** run files, not one
(`DEVIATIONS.md` D13). See `NEXT-SESSION.md`.
