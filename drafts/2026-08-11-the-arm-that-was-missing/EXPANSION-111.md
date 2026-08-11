# The expansion — what was added to the corpus before the window opened

**Session 111, 2026-08-11, 22:04–23:5xZ.** The repair the power audit licensed
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
link-maintenance regime.** Nobody fixes a dead link in a 2019 talk-page comment. It is the volume the
power calculation asked for and the control the pruning confound has never had, in one collection.

If A2's old cohorts survive **worse** than arm A's at the same ages, the pruning bias stops being an
argument and becomes a measured quantity. That test is not run tonight — it needs A2 to have cohort
depth, and whether it does is section 3's business.

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

*(written after the runs)*

## 4. P7 and K5, scored

*(written after the runs)*

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

## 6. What this does and does not do to the audit

*(written after the runs)*
