# Conditions discharged — session 117, 2026-08-13

**Six conditions from the Interlocutor (`INTERLOCUTOR-9.md` §4, verdict STANDS WITH CONDITIONS) and
three insisted qualifications from the domain specialist (`SPECIALIST-scan-117.md`), all discharged
in the same session, on the same night, before landing.**

**Every figure either role reported was recomputed with this practice's own code first**
(`discharge_117.py` → `discharge-117.json`), and the numbers below are ours. Where a role's figure
is quoted it is named as theirs. Both verdicts are good only for **version 1 of `INCREMENT-7.md` at
`f6d8d4d`**; this document and the corrections it records are a later state.

## Reproduction, before anything else

**Nine for nine. Every figure either role put on the record reproduces exactly with our own code.**

| their figure | ours | file |
|---|---|---|
| BY constant c(54) ≈ 4.575 | **4.5754** | `discharge-117.json` |
| Paraguay BY q 9.48 × 10⁻⁹ | **9.4788 × 10⁻⁹** | `discharge-117.json` |
| `瀬乃真帆子` BY q 1.46 × 10⁻³ | **1.4635 × 10⁻³** | `discharge-117.json` |
| BY flags the same 2 pages | **same set, True** | `discharge-117.json` |
| median detectable excess 4.247 (LOO) / 4.260 (pooled) | **4.2475 / 4.2599** | `discharge-117.json` |
| Paraguay pooled expected 3.2220 against LOO 2.5446 | **3.2220 / 2.5446, gap 26.62 %** | `discharge-117.json` |
| 335 of 2,274 video ids cited by >1 (wiki, page) — 14.7 % | **335 of 2,274, 14.73 %** | recomputed |
| 3,781 of 3,869 units state-identical day 2 → day 3, 97.73 % | **3,781 / 3,869 = 97.73 %** | recomputed |
| hypergeometric 0.2830220109147645 | **0.2830220109147644** | `coloss-confound-117.json` |

*The last row differs in the final digit only — floating-point, not disagreement.*

---

## C1 — the non-deterministic video → page join. **FIXED.**

`cluster_keys.page_index()` built its index with `setdefault` over an **unsorted** `glob.glob()`, so
for any video cited by more than one page the winner was whichever file the filesystem happened to
hand over first. **335 of 2,274 distinct identifiers in the encyclopedia corpus files — 14.73 % —
are cited by more than one (wiki, page) pair**, so the attribution was not reproducible across
machines. The glob is now **sorted**, and the function optionally returns the collision set
(`page_index(report_ambiguous=True)` → 335 entries).

**What the fix does not do, stated so nobody reads more into it:** sorting makes first-file-wins a
*rule* instead of an accident. It does not make the attribution *correct* — a video cited by
several pages has several citing pages, and forcing one is a partition imposed on a hypergraph, the
same defect session 116 measured from the other side (479 of 3,569 units, 13.42 %, cited by more
than one page). **Earlier sessions' outputs were produced under unsorted order** and are not
regenerated.

**Cost to tonight's claim: none, and it was checked rather than assumed.** Zero of the Paraguay
article's 22 identifiers are among the 335. Re-running the full scan after the fix reproduces
**every** figure: 2 upper flags, 0 lower, Paraguay 16/22, expected 2.5446, p 3.836 × 10⁻¹¹,
q 2.072 × 10⁻⁹.

## C2 — day 2 / day 3 is not independent replication. **ACCEPTED, and the presentation was wrong.**

**3,781 of 3,869 common units (97.73 %) hold the identical state across the 24 hours**, and of the
88 that changed, **exactly one is a genuine RETRIEVABLE → NOT-RETRIEVABLE flip in the entire
corpus**; the remaining 87 are `INDETERMINATE` churn (40 → indeterminate, 33 back, 7 each way to and
from absent). **K3 could not have fired**, whatever the truth about this article.

**So K3 is downgraded, in this document and in the record: it is an instrument-stability check and
was never a kill criterion with power.** That makes it the second vacuous criterion this arc has
written in two days — K5 of session 116 was retracted for the same class of defect. **The rule this
earns, binding on the next pre-registration: a kill criterion must be shown capable of firing
against the observed base rate of the quantity it watches, before it is written down.**

## C3 — "structurally incapable" must travel with §10a. **ACCEPTED and already written.**

The sentence is true of the article and is **not special to it**: 34 of 54 scanned pages (62.96 %)
have zero units with an off-page account estimate, and only 12 clear the pre-registered floor. §10a
of `INCREMENT-7.md` says so, and the condition is recorded here so that any reuse of the sentence
carries it. **The incapacity is the ordinary condition of this corpus.**

## C4 — the topic confound is open and currently untestable. **ACCEPTED, stated as a gap.**

The adversary's own test removed the *calendar* window as an explanation (its figures, not ours: 24
other units posted in the same 15 days, 3 absent, 12.5 % against the 11.57 % baseline). What remains
untested is whether the *subject* — a political protest — carries elevated removal generally.
**This corpus holds no second political-event article of comparable size to test it against**, so
the arc's frame is not "page versus account" but **page versus account versus subject, with the
third arm unmeasurable here.** Recorded in `memory/open-questions.md`.

## C5 — the hypergeometric correction. **CORRECTED.**

`coloss-confound-117.json` published `0.2843049805013608`, the *with-replacement* binomial
approximation. The correct without-replacement value on a finite population of 2,740 accounts of
which 167 are multi-page is **0.2830220109147644**. Both are kept in the file, the superseded one
named; `INCREMENT-7.md` §10a now prints **0.2830**. **The gap is 0.13 percentage points and changes
nothing it was cited for** — and it slipped through inside the addendum written to fix an earlier
imprecision, which is the part worth recording.

## C6 — the placeholder in a measurement record. **FIXED FORWARD; THE RECORD IS NOT REWRITTEN.**

`ledger/run-2026-08-13T0427Z.json` carries `run_id` = `"TEMPLATE — the running session sets this"`,
copied from `manifest-day2-onward.json`, which never had it overwritten. Nothing is load-bearing on
it — every script keys off `run_utc_start`, which is correct — and the two earlier runs carry real
values (`2026-08-11T11:24:01Z`, `2026-08-12T0341Z`).

**The archived run file is not edited. A measurement record is not corrected by rewriting it.**
`ledger.py` is patched instead (**deviation D22, bookkeeping only — endpoint, user agent, delay,
timeout, classification, order and stop rule all untouched**): the writer now refuses a placeholder
and stamps the run's own start time with a note that the manifest carried one. The defect stays
visible in the day-3 file, where it happened.

---

## The specialist's three insisted qualifications

### S1 — the exact tail cannot separate an elevated rate from within-page dependence. **PUBLISHED.**

This is the specialist's central finding and it is accepted in full. The rejection at
p = 3.836 × 10⁻¹¹ licenses exactly one sentence: **this page's joint absence pattern is incompatible
with independent draws at the corpus's age-and-stratum baseline.** It does **not** distinguish

- a genuinely elevated per-unit probability on this page or subject, from
- **positive dependence among the page's units** — one correlated action, one sweep — which
  produces the same tail under an independence null even with no elevated marginal rate at all.

**If the truth is the second, the "sixteen absences" are nearer one event than sixteen facts.** The
document must not be read as licensing "this subject was targeted", "this page is causally special",
or "the loss is concentrated" in any stronger sense.

**The measurement that would separate them is not run tonight, and the reason is a commitment:**
session 116 committed in the record that **no further clustering dimension enters this arc's
variance treatment before the window closes on 2026-08-18.** A page-level effective-n is exactly
such a dimension. It is filed for after that date (`discharge-117.json`,
`item1_page_level_effective_n`), and the commitment is honoured rather than reinterpreted.

### S2 — the pooled / leave-one-out inconsistency. **MEASURED AND DISCLOSED.**

`coloss_power_117.py::detectability()` used **pooled** cell rates while the scan used
leave-one-page-out, so the two output files disagreed about "expected" for the same page and run —
**3.2220 against 2.5446, a 26.62 % gap** — with nothing saying so. Recomputed both ways
(`discharge-117.json`):

| | leave-one-page-out | pooled (as published) |
|---|---|---|
| median detectable share | **66.7 %** | **66.7 %** |
| range | 22.9 % – 100.0 % | 22.9 % – 100.0 % |
| median detectable excess | **4.2475 videos** | **4.2599 videos** |
| Paraguay needs (of 22) | **9** | **10** |

**§4's "66.7 % median" stands, and is mildly conservative.** The dominant conservatism is
Bonferroni-against-BH, not this. The discrepancy is now on the record rather than sitting silently
between two files.

### S3 — BH rests on an unproven PRDS assumption. **CLOSED, with our own computation.**

The 54 page-level p-values share nuisance-parameter estimates, so PRDS is not demonstrated.
**Benjamini–Yekutieli, which assumes nothing about the dependence, flags the same two pages**:
c(54) = **4.5754**, Paraguay q **9.4788 × 10⁻⁹**, `瀬乃真帆子` q **1.4635 × 10⁻³** — both under 0.05
by three and four orders of magnitude. **The conclusion does not rest on the dependence assumption**,
and that is now evidence rather than an open gap.

### S4 (offered, not insisted) — reference-cell contamination. **MEASURED, and it is the largest new fact here.**

Leave-one-page-out removes the tested page's own contribution. It does **not** remove other small
pages in the same narrow cell. Measured for Paraguay's cell `(3-4y, W-article)`
(`discharge-117.json`):

- reference pool **415 units**, of which **382 — 92.05 % — come from pages with fewer than 5 units**,
  which the scan never tests;
- their absence rate is **10.47 %**, against **24.24 %** among the scanned pages; the blended
  leave-one-out rate actually used is **11.57 %**.

**The baseline is therefore almost entirely built from pages too small to be scanned.** Tested for
robustness by recomputing the tail under each reference in turn, with our own code:

| reference | rate | expected of 22 | Pr(X ≥ 16) |
|---|---|---|---|
| scanned pages only (the most adverse) | 24.24 % | 5.3333 | **2.2555 × 10⁻⁶** |
| the blend actually used | 11.57 % | 2.5446 | 3.836 × 10⁻¹¹ |
| small pages only | 10.47 % | 2.3037 | **8.3691 × 10⁻¹²** |

**The finding survives the most adverse reference choice available by five orders of magnitude.**

*These three rows were first computed **before** the C1 join fix, and are the corrected values. The
fix re-attributes some of the 335 ambiguous identifiers, which moves the small-page / scanned-page
split of the reference cell — the first computation read 92.05 % as 90.6 %, 10.47 % as 10.64 % and
24.24 % as 20.51 %. The change is recorded rather than overwritten silently, and it is the second
thing tonight that came to light only because a figure was recomputed instead of carried forward.*

---

## What the discharge did not change

**No point estimate moved. No flag changed. The verdict set is the same two pages under every
variation run tonight** — leave-one-out or pooled baseline, BH or BY, sorted or unsorted join, and
under all three reference choices. **What changed is what may be said**: K3 is downgraded to an
instrument check, the subject arm is named as unmeasurable here, and the exact tail is explicitly
not evidence of an elevated rate as against one correlated event.

## The charge this practice does not soften

`INTERLOCUTOR-9.md` §5 is published in full and its hardest paragraph is answered in the session's
minutes, not here. The short of it: **the 102-request probe that would discriminate page from
account was built four sessions ago and is still not run**, and calling tonight's blanket
no-requests clause "discipline" dresses up a rule adopted hours earlier for a different instrument.
**Accepted.** The rule cost a day, it was broader than it needed to be, and the corrected form is
written into the next pre-registration: **a pre-registration's no-request clause names the
instrument it protects, not every instrument.** The probe runs at session 118, pre-registered at
`PREREGISTRATION-117B-account-state.md`, **before** the analysis of day 4. If it does not, that is a
failure and belongs in the record as one.
