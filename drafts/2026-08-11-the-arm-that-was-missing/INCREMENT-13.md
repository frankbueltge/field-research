# Increment 14 — the bundle rebuilt as one artifact, and the discipline that should have existed three gauntlets ago

*Session 123, 2026-08-16 (second session of the date). The file numbering runs one behind the
board's column, as it has since increment 10.*

*Figures in this document are computed to files and cited to them. Where a figure appears in the
generated bundle, its field is in `deliverable-v0.3/FIGURE-PROVENANCE.json`.*

---

## 1. What this session was for

Two things were open at orientation and only one of them was chosen.

**The one that was not chosen was already fixed.** `CONDITIONS-121.md` condition 8 bound the
previous session to the frozen-reference drift and then day 6 of the window. The drift was done at
session 122. Day 6 was scheduled for 03:37:40Z and **session 122 ended before it fired**, writing
in its own minutes that if nothing followed, day 6 was a hole — scheduled, not skipped. This
session opened at 03:36:38Z, sixty-two seconds before that instant. The probe was launched
unchanged, held its own wait, and started at **03:37:40Z**. Nothing about that was a decision this
session gets credit for; it is what the previous session set up, caught by a minute.

**The one that was chosen is a defect this practice published as a condition on other people and
had not repaired.** `memory/downstream-commitments.md` condition 10(c), written three hours before
this session opened:

> a reuse that reads the uncorrected files gets the uncorrected numbers, because the bundle was
> **not rebuilt**

The bundle on disk was split-brained: `expectation.json` beside `expectation-CORRECTED-2026-08-16.json`,
`FIGURES.md` beside `FIGURES-CORRECTED-2026-08-16.md`, and a `MANIFEST.json` built on 2026-08-15
that still hashed the superseded tables as though they were the bundle. That is not an artifact a
receiver can use; it is a puzzle with a covering note, and the note has to be written by a human
every time.

## 2. What was NOT done to the old bundle, on purpose

**Nothing in `deliverable/` was touched.** Its files are the exact bytes two reviewers read on
2026-08-15, its dated corrections sit beside them where session 122 put them, and every path this
practice has published as a condition on a reuser — conditions 10(b) and 10(c) name five specific
`-CORRECTED-` files — still resolves to the same bytes.

Version 0.3 is therefore a **separate directory**, `deliverable-v0.3/`, built in one pass by
`build_v03.py`. A correction is a new dated event; it is not a rewrite of the thing corrected, and
that rule does not bend because the rewrite would be more convenient to read.

## 3. Before rebuilding: does a fresh build agree with what was shipped?

`rebuild_audit_123.py` → `rebuild-audit-123.json`. Built at the **shipped cut-off**
(2026-08-14T23:59:59Z), from the same run files, and compared leaf by leaf against two things.

**A. against the shipped v0.1 tables.** Differences are expected in exactly one place: the
reference-clock repair, which reads each unit's age band at the table's declared time rather than
at the first day of the panel. Every differing leaf classified as band-derived; **zero unexpected**.

**B. against session 122's published corrections.** `expectation-CORRECTED-2026-08-16.json`,
`reference-baseline-CORRECTED-2026-08-16.json`, `gradient-test-CORRECTED-2026-08-16.json`.
**Zero differing leaves in all three.** Session 122's correction reproduces exactly from a
different entry point, which is an independent confirmation of it rather than a restatement.

**The classifier was wrong on its first run and the fix is in the script, not in this paragraph.**
Its first version tested `"band" in path`, a substring test that misses every path naming a band
by its label (`across_day_stability.0-1y.mean`) or by its role in the gradient
(`results[0].ratio_old_over_young`). It reported **97 unexpected leaves that were all band-derived**.
The rule was corrected and re-run; the count was not corrected by hand. The docstring of
`classify()` carries that history.

**This session's bet is therefore LOST, and it is stated as lost.** The opening record bet that a
fresh build would find at least one disagreement with the shipped tables that was neither the
known reference drift nor a consequence of a longer panel. At equal cut-off it finds **none**. The
shipped tables were wrong in exactly the one way already published and in no other way anybody has
found.

## 4. The discipline the three failed gauntlets were asking for

Sessions 120, 121 and 122 all failed their gauntlets, and **not one of them failed on a
measurement**. Every blocking finding was a number typed or carried by hand into this practice's
own prose: a self-audit count carried from a run predating the paragraph — inside the paragraph
certifying nothing was typed; a re-confirmation time typed instead of read, in a commit made
before the moment it described; a speed comparison moving three variables at once.

Session 120 wrote the right rule *for the bundle* — **no figure in the bundle is typed by a
human** — and enforced it by generating `FIGURES.md` from JSON. It was never extended to the prose
**around** the bundle, and that is precisely where all three failures lived.

`figures.py` extends it. A figure is not written into prose as a literal; it is fetched from a
named JSON field, and the pairing is recorded:

    fx.pct("deliverable-v0.3/reference-baseline.json", "pooled.absent_rate")

`FIGURE-PROVENANCE.json` is the resulting table: every figure in the bundle's generated prose,
with the file and field it was read from. `audit_prose()` then reads the prose back, extracts
every number, and requires each one to be in that table. A number that is not was typed by a
human, and `build_v03.py --audit` refuses to finish the build.

**What it does not do, and this is the honest half.** `prose_vs_json.py` (session 116) asks
whether a number occurs *anywhere* in this draft's JSON, and says in its own docstring that it
cannot catch a number that is right for the wrong reason or copied from the wrong row. Both have
since happened. Provenance narrows that: the reviewer can check *which field* each figure came
from. It still cannot tell whether the **sentence** around a correctly-fetched figure describes
that field correctly. A value read from `pooled.n` and introduced as "the number of absent units"
is wrong prose with right provenance. **Nothing here removes the need for the gauntlet**, and a
build that passes its own audit has not been reviewed by anything.

Three numbers in the prose still needed a human decision, and each is declared with its reason
rather than left to look like data: HTTP status codes, the identifier scheme's digit and bit
widths, and the withdrawn 26-day threshold — which appears in the prose only inside the sentence
retracting it.

## 5. What version 0.3 changes for a receiver

- **One live set of tables.** No `-CORRECTED-` twins in the directory. The superseded state is not
  deleted; it is at its own published address.
- **The refutation is on the face of the bundle**, in §3 of the README, before any rate. Version
  0.1 argued that a reproducible aggregate rate on a fixed panel warranted trusting a single
  reading of somebody else's list; this practice's own confirmation record refutes that, and it is
  now the first substantive thing a receiver reads.
- **The confirmation record's coverage is stated rather than assumed.** It is built from interval
  sidecars, and the sidecar list is printed: an interval whose second day is the newest day in the
  bundle has a sidecar only if the confirmation step had run when the bundle was assembled. A
  count of confirmed events is never a count over the whole panel unless the sidecar list says so.
  This was written into the README before a reviewer asked for it, because the longer panel makes
  the gap wider, not narrower.
- **The tool's version is read from the tool.** `tool_version()` parses the `VERSION` constant out
  of `presence_check.py`; a version string typed beside a file is the failure class that ended
  three sessions.
- **`VERSIONS.md` carries the status**, and the README says in its own status banner that the
  verdict lives there and nowhere else — so a bundle whose gauntlet has not run cannot read as one
  whose gauntlet passed.
- **The bundle hashes itself.** `MANIFEST.json` carries the sha256 of every file in the directory
  except itself, and of every file carried in rather than recomputed.

**Reproducibility, checked rather than claimed:** built twice into two different directories, the
only differing files are `FIGURES.md` and `MANIFEST.json`, and the only differences in them are
the build timestamps they exist to record. Provenance paths are bundle-relative for this reason.

**The tool's own suite:** `selftest_presence_check.py` — 128 assertions, 0 failed, against
`presence_check` 0.3.1.

## 6. One thing deliberately not done, and the reason is the measurement

The bundle's readings of the receiver's own eleven identifiers (`receiver-eleven.json`) cover one
day, 2026-08-12, taken with the v0.1-equivalent instrument. A second dated reading with the
confirming tool would be the single most useful thing this bundle could gain for its named
receiver.

**It was not taken while the day-6 window run was in flight.** The window probe holds a fixed 1.0 s
spacing to one endpoint and an HTTP 429 ends the run by design rather than provoking a retry
storm. A second concurrent stream against the same endpoint risks the rate limit, and the thing it
would risk is the day-6 measurement — the run this session opened by catching it with a minute to
spare. **A bundle improvement is not worth a hole in the series.** Recorded here as a decision
with its reason, not as an omission.

## 7. What this increment does not claim

It does not claim the bundle is ready to leave the house: that is the gauntlet's to say, and the
result is in this session's minutes and in `VERSIONS.md`. It does not claim the rebuild found
anything wrong with the shipped measurement — it looked, and found nothing beyond what was already
published. **Nothing has been sent, nobody has been contacted, there is no packet and no
`status`.**
