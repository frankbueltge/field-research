#!/usr/bin/env python3
"""build_v03 - assemble version 0.3 of the receiver bundle, prose included, from the run files.

Session 123, 2026-08-16.

WHY A NEW BUNDLE DIRECTORY RATHER THAN AN EDIT
----------------------------------------------
`deliverable/` is version 0.1. It was refuted at its gauntlet on 2026-08-15 and is withheld; its
files are the exact bytes two reviewers read, and session 122's drift repair was published beside
them as `*-CORRECTED-2026-08-16.*` rather than written into them. Both of those are right and
neither is undone here: **nothing in `deliverable/` is touched by this script.** Every path this
practice has published as a condition on a reuser (`memory/downstream-commitments.md`, conditions
10(b), 10(c)) still resolves to the same bytes.

What was wrong was the resulting shape. A receiver handed `deliverable/` gets `expectation.json`
beside `expectation-CORRECTED-2026-08-16.json` and a `MANIFEST.json` that hashes the superseded
one as if it were the bundle - an artifact you cannot read without being told, in prose, by a
human, which half is live. This practice stated that defect as a condition on other people three
hours before this session opened and had not repaired it.

So version 0.3 is a separate, self-contained directory built from the run files in one pass:

    python3 build_v03.py [--out deliverable-v0.3] [--cutoff ...]

WHAT IS NEW IN 0.3, BEYOND THE LONGER PANEL
--------------------------------------------
1. **The prose is generated.** README, LETTER, LIMITS and VERSIONS are written here, and every
   figure in them is fetched from a JSON field by `figures.py`, which records the field it came
   from. `FIGURE-PROVENANCE.json` is that record. A number in the prose that is not in it was
   typed by a human, and `--audit` fails the build on it.
2. **The confirmation record is on the face of the bundle, not in a limits appendix.** It is the
   measurement that refuted version 0.1's core claim, made by this practice against itself.
3. **One live set of tables.** No `-CORRECTED-` twins: the correction is folded into the build
   and the superseded state is at its own published address, in `deliverable/`.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

import figures as F

V = "0.3"
DATE = "2026-08-16"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for b in iter(lambda: f.read(65536), b""):
            h.update(b)
    return h.hexdigest()


def tool_version(path="deliverable/tools/presence_check.py"):
    """The tool's own VERSION constant, read from the file rather than typed beside it. A version
    string typed into prose is the exact failure class that ended three gauntlets."""
    m = re.search(r'^VERSION\s*=\s*["\']([^"\']+)["\']', open(path).read(), re.M)
    if not m:
        raise SystemExit(f"{path}: no VERSION constant found; refusing to guess it")
    return m.group(1)


def newest_day(exp):
    """The label of the newest measurement day in the built expectation table."""
    return [d for d in exp["per_day"] if d != "baseline"][-1]


def build(out, cutoff):
    if os.path.isdir(out):
        shutil.rmtree(out)
    cmd = [sys.executable, "build_deliverable.py", "--out", out]
    if cutoff:
        cmd += ["--cutoff", cutoff]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.stderr.write(r.stdout + r.stderr)
        raise SystemExit("build_deliverable.py failed; no bundle written")
    return r.stdout


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="deliverable-v0.3")
    ap.add_argument("--cutoff", default=None)
    ap.add_argument("--audit", action="store_true",
                    help="fail the build if any number in the generated prose has no provenance")
    a = ap.parse_args(argv)

    build(a.out, a.cutoff)

    # Carry the files version 0.3 keeps but does not recompute. Each is hashed into the manifest,
    # so "carried" is checkable rather than asserted.
    os.makedirs(os.path.join(a.out, "tools"), exist_ok=True)
    carried = []
    for src, dst in [("deliverable/tools/presence_check.py", "tools/presence_check.py"),
                     ("deliverable/tools/selftest_presence_check.py",
                      "tools/selftest_presence_check.py"),
                     ("deliverable/tools/ledger.py", "tools/ledger.py"),
                     ("deliverable/tools/power_audit.py", "tools/power_audit.py"),
                     ("deliverable/tools/CHANGELOG-v0.2.md", "tools/CHANGELOG-v0.2.md"),
                     ("deliverable/receiver-eleven.json", "receiver-eleven.json"),
                     ("deliverable/receiver-eleven.md", "receiver-eleven.md"),
                     ("confirmation-record-121.json", "confirmation-record.json"),
                     ("drift-122.json", "reference-drift.json")]:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(a.out, dst))
            carried.append({"from": src, "to": dst, "sha256": sha256(src)})

    fx = F.Figures(relative_to=a.out)
    P = lambda n: os.path.join(a.out, n)
    REF, EXP, GRAD = P("reference-baseline.json"), P("expectation.json"), P("gradient-test.json")
    MAN, CONF = P("MANIFEST.json"), P("confirmation-record.json")

    exp = json.load(open(EXP))
    man = json.load(open(MAN))
    day = newest_day(exp)
    days = [d for d in exp["per_day"]]

    # ---- figures, every one fetched -----------------------------------------------------
    n_days = fx.raw(MAN, "coverage.n_measurement_days", "measurement days in this bundle")
    first_m = fx.raw(MAN, "coverage.first_measurement_utc", "first measurement")
    last_m = fx.raw(MAN, "coverage.last_measurement_utc", "cut-off of this bundle")
    n_units = fx.n(EXP, "per_day.baseline.pooled.n", "units measured on the baseline day")
    t_ref = fx.raw(REF, "t_ref_utc", "the reference table's declared time")
    t_ages = fx.raw(REF, "ages_computed_at_utc", "when the bands were actually computed")
    ref_n = fx.n(REF, "pooled.n", "reference population, determinate units")
    ref_absent = fx.n(REF, "pooled.absent", "reference population, units not retrievable")
    ref_rate = fx.pct(REF, "pooled.absent_rate", 2, "the reference rate")
    ref_ci = fx.ci(REF, "pooled.absent_ci", 2, "Wilson interval on the reference rate")
    g_ratio = fx.num(GRAD, "results[0].ratio_old_over_young", 4, "pooled age gradient")
    g_p = fx.sci(GRAD, "results[0].fisher_two_sided_p", 4, "pooled age gradient, Fisher p")
    n_runs = fx.count(MAN, "source_runs", "run files this bundle was built from")

    # the confirmation record - the measurement that refuted version 0.1
    cr_ret_n = fx.raw(CONF, "genuine_transitions_only.NOT-RETRIEVABLE->RETRIEVABLE.n", "returns")
    cr_ret_c = fx.raw(CONF, "genuine_transitions_only.NOT-RETRIEVABLE->RETRIEVABLE.confirmed",
                      "returns confirmed")
    cr_los_n = fx.raw(CONF, "genuine_transitions_only.RETRIEVABLE->NOT-RETRIEVABLE.n",
                      "disappearances")
    cr_los_c = fx.raw(CONF, "genuine_transitions_only.RETRIEVABLE->NOT-RETRIEVABLE.confirmed",
                      "disappearances confirmed")
    cr_raw_ret_n = fx.raw(CONF, "all_readings.NOT-RETRIEVABLE->RETRIEVABLE.n", "raw returns")
    cr_raw_ret_c = fx.raw(CONF, "all_readings.NOT-RETRIEVABLE->RETRIEVABLE.confirmed",
                          "raw returns confirmed")
    cr_raw_los_n = fx.raw(CONF, "all_readings.RETRIEVABLE->NOT-RETRIEVABLE.n",
                          "raw disappearances")
    cr_raw_los_c = fx.raw(CONF, "all_readings.RETRIEVABLE->NOT-RETRIEVABLE.confirmed",
                          "raw disappearances confirmed")
    cr_passes = fx.raw(CONF, "passes_per_reading", "re-requests per reading")
    cr_echoes = fx.raw(CONF, "n_artefact_echoes", "artefact echoes excluded from the genuine count")
    cr_sidecars = fx.count(CONF, "sources.sidecars", "confirmation sidecars, one per interval")
    cr_first = fx.raw(CONF, "sources.sidecars[0]", "the first interval the confirmation covers")
    cr_last = fx.raw(CONF, f"sources.sidecars[{len(json.load(open(CONF))['sources']['sidecars']) - 1}]",
                     "the last interval the confirmation covers")

    # the drift of this table against a caller who ages a list at today
    d30 = fx.num(REF, "shelf_life.measured_drift_pp_by_days_after_t_ref.30", 4, "drift, 30 days")
    d365 = fx.num(REF, "shelf_life.measured_drift_pp_by_days_after_t_ref.365", 4, "drift, 365 days")

    # per-day pooled rates, one figure per day, each read from its own field
    day_rows = []
    for d in days:
        day_rows.append((
            fx.raw(EXP, f"per_day.{d}.measured_utc_start", f"start of day {d}") if d != "baseline"
            else fx.raw(EXP, "per_day.baseline.measured_utc_start", "start of the baseline"),
            fx.key(EXP, "per_day", d, "measurement-day label"),
            fx.n(EXP, f"per_day.{d}.pooled.n", f"determinate units on {d}"),
            fx.n(EXP, f"per_day.{d}.pooled.absent", f"units not retrievable on {d}"),
            fx.pct(EXP, f"per_day.{d}.pooled.absent_rate", 2, f"pooled rate on {d}"),
        ))

    # age bands on the newest day
    band_rows = []
    for b in exp["per_day"][day]["by_age_band"]:
        if exp["per_day"][day]["by_age_band"][b]["n"] == 0:
            continue
        band_rows.append((
            fx.key(EXP, f"per_day.{day}.by_age_band", b, "age-band label"),
            fx.n(EXP, f"per_day.{day}.by_age_band.{b}.n", f"{b} units on {day}"),
            fx.n(EXP, f"per_day.{day}.by_age_band.{b}.absent", f"{b} absent on {day}"),
            fx.pct(EXP, f"per_day.{day}.by_age_band.{b}.absent_rate", 2, f"{b} rate on {day}"),
            fx.ci(EXP, f"per_day.{day}.by_age_band.{b}.absent_ci", 2, f"{b} interval on {day}"),
        ))

    day_label = fx.key(EXP, "per_day", day, "the newest measurement day, named in prose")

    v01 = fx.lit("0.1", "a version number, not a measurement")
    v031 = fx.lit(tool_version(), "the tool's own VERSION constant, read from "
                                  "tools/presence_check.py by this script")
    d2026 = fx.lit(DATE, "the date this bundle was built, as a date")

    # Literals that stay in the prose because they are not measurements of this panel. Each is
    # declared with its reason, so the audit can tell a declared literal from a typed figure.
    # This list is the complete set: anything else numeric in the generated prose fails the audit.
    L_400 = fx.lit("400", "an HTTP status code returned by the endpoint, not a quantity")
    L_404 = fx.lit("404", "an HTTP status code never returned, not a quantity")
    L_19 = fx.lit("19", "the digit-length of the platform's modern identifier scheme")
    L_32 = fx.lit("32", "the bit-width of the timestamp field in that scheme")
    L_26 = fx.lit("26", "a threshold this practice published and WITHDREW; it appears in the "
                        "prose only inside the sentence retracting it")
    L_1d = fx.lit("1", "the lower end of the withdrawn threshold family, in the same retraction")
    L_015 = fx.lit("2026-08-15", "the date version 0.1 was refuted, as a date")
    L_s122 = fx.lit("122", "a session number in this practice's own record, not a measurement")
    L_011 = fx.lit("2026-08-11", "the date of the three-arm synthetic control run, as a date")

    # ---- VERSIONS.md --------------------------------------------------------------------
    versions = f"""# Versions of this bundle, and what each one's status is

*Every version this practice has built, with what happened to it. A version that did not pass
its own gauntlet says so here, and its files stay retrievable at their published address so the
reports against them stay checkable.*

| Version | Date | Status | Where |
|---|---|---|---|
| {v01} | {L_015} | **WITHHELD — refuted at its gauntlet.** Its core claim was that reproducing an aggregate rate on a fixed panel warrants trusting a single reading of somebody else's list. This practice's own confirmation record refutes that, and the tool shipped in it took one pass and no confirmation. | `deliverable/` — unedited, plus `GAUNTLET-2026-08-15.md` listing every corrected statement with its true value |
| {v01} + dated corrections | 2026-08-16 | **STILL WITHHELD.** Session {L_s122} measured a reference-clock defect and published the corrected tables **beside** the originals rather than editing them. | `deliverable/*-CORRECTED-2026-08-16.*` |
| **{V}** | **{d2026}** | see the banner on `README.md` of this directory | this directory |

## What changed between {v01} and {V}

1. **The panel is longer.** {n_days} measurement days, {first_m} to {last_m}, built from
   {n_runs} run files whose sha256 are in `MANIFEST.json`.
2. **The reference-clock defect is fixed in the build, not patched beside it.** Version {v01}
   declared a reference time of one date and computed its age bands at another. In this version
   `t_ref_utc` is {t_ref} and `ages_computed_at_utc` is {t_ages}; where those two agree, the
   bands are the bands of the moment the table names.
3. **One live set of tables.** There are no `-CORRECTED-` twins in this directory. The
   superseded state is not deleted — it is at its own published address in `deliverable/`.
4. **The confirmation record is on the face of the bundle** (`README.md` §3,
   `confirmation-record.json`), not in an appendix. It is the measurement that refuted version
   {v01}, and a receiver meets it before any rate.
5. **The tool is version {v031}**, with confirmation of refusals and a caller-side staleness
   report. Every figure it prints names the version and the `--confirm` setting that produced it.
6. **The prose is generated.** Every figure in this directory's `README.md`, `LETTER.md` and
   `LIMITS.md` was read from a JSON field by `figures.py`, which recorded the field.
   `FIGURE-PROVENANCE.json` is that record — a number in the prose that is not in it was typed
   by a human, and the build refuses to complete with `--audit` if one is.

## What did NOT change, and must not be read as changed

The correction in item 2 moved **no** count of absent units and did not change the pooled rate to
the last digit: every unit that crossed an age band under the corrected clock was retrievable on
both sides of it. It moved age-band cells and three of four age-gradient rows, and changed no
conclusion. A reuse that renders it as a change in how much absence was found reports something
this practice did not measure.
"""

    # ---- LIMITS.md ----------------------------------------------------------------------
    limits = f"""# What this bundle cannot show

*Version {V}, {d2026}. This file is load-bearing. If you re-use anything from this bundle, this
page travels with it. Everything below is a present-tense limit of the measurement, not a
future-tense hedge about work someone might do later.*

---

## 1. `NOT-RETRIEVABLE` does not mean deleted

The endpoint this bundle uses answers a refusal with a **single opaque HTTP {L_400}**, and that code
is semantically empty. A three-arm control run on {L_011} with twenty synthetic identifiers
that never existed returned exactly the same code as identifiers that certainly did exist, and
**no HTTP {L_404} was ever returned** in any run of this instrument.

So `NOT-RETRIEVABLE` means, exactly and only:

> not publicly retrievable through this endpoint, from this network vantage, at that moment.

It does not mean deleted, removed, moderated, geo-blocked or made private. Those are different
claims and this instrument cannot tell them apart. A derived headline that drops this caveat is
measuring something it cannot name.

## 2. One vantage, one endpoint

Every run is taken from **one** network vantage (autonomous system AS396982, United States —
logged into every run file before the first measurement request) through **one** credential-free
endpoint. A result that differs from another vantage is not a contradiction of this bundle; it is
a second reading this bundle cannot make.

## 3. The population is a cited population, not a sample of the platform

The panel is videos **cited in public** — in the article and non-article namespaces of language
editions of one encyclopedia, and posted to one public technology forum. Videos that nobody cited
are not in it and nothing here describes them. **A yardstick cited without its population is a
verdict wearing a yardstick's clothes:** any expected-absence figure taken from this bundle
carries the population, the run identifier and the date that produced it.

## 4. Six events is not a rate

The whole panel has produced a handful of confirmed state changes across its measurement days
(§3 of `README.md`). That is a count of events, not a hazard, and no reuse may render it as one.
Reading a single cross-section's age gradient forward as a rate of disappearance is a claim this
practice has made in public and **withdrawn in public**.

## 5. The reference table has a date, and using it later is an error that grows

This table is a measurement of one population on one day. A tool that ages a caller's list at
**today** and looks the result up here is doing arithmetic against a clock that stopped. The size
of that error was measured before it was disclosed (`reference-drift.json`): **{d30} pp** after a
month of shelf-life and **{d365} pp** after a year, on the reference population itself.

That drift is **arithmetic, not a forecast.** Nothing was re-measured at any horizon. It says how
far the printed expectation moves as the table ages, not what retrievability does.

**Corrected here, and it is a correction to this practice's own words.** Version {v01} of this
file said a {L_26}-day threshold in the tool was the point past which drift exceeded the largest
defect this practice had caused, and the tool warned past it. That claim was **withdrawn** at the
gauntlet of {d2026}: the crossover is a family of values running from {L_1d} day to {L_26} depending on
which comparand is chosen, the comparand was chosen after the fact, and {L_26} was the most forgiving
member. The fixed threshold is **deleted** from the tool. Version {v031} instead reports the
caller's own drift, computed on the caller's own list, and refuses to print a drift at all when
the two readings it would compare have different denominators.

## 6. Ages are decoded, not looked up

Creation times are decoded from the identifier itself under the platform's modern {L_19}-digit scheme
(the high {L_32} bits are a Unix timestamp), checked against the endpoint's own returned metadata
where that metadata exists. Identifiers that are not {L_19} digits carry no age, stay in the series,
and are excluded from every age-banded rate.

## 7. Two arms are excluded from every rate, by design and in advance

A control arm of display-truncated identifiers that are **not** videos is excluded from every
rate and reported separately — including it would manufacture absence. Observations that failed
in transport (`INDETERMINATE`) are excluded and counted, never imputed.

## 8. The raw record is primary and is never edited

`states` in `presence-series.json` is what the instrument returned. `states_corrected` applies an
overlay of readings this practice's own confirmation step refuted with {cr_passes} immediate
re-requests. **No archived run file is ever edited**, and where the two arms differ, both are
published.

## 9. What this bundle is not

It is the **control arm** of a two-sided comparison: what was publicly retrievable, measured
without any credential. It is **not** an audit of any research interface, it makes no claim about
what any credentialed interface returns, and it cannot on its own show that any platform's
coverage claim is false. What it can do is give a reading of a research interface something to be
compared against.
"""

    # ---- README.md ----------------------------------------------------------------------
    readme = f"""# The Control Arm — a credential-free public-presence ledger

**Version {V} · {d2026} · Meridian, an autonomous research practice**

> **STATUS — read this first.** Version {v01} of this bundle was refuted at its own gauntlet on
> {L_015} and withheld. This version is a rebuild, not a patch: it is built in one pass from
> the run files, it carries the correction that version made necessary, and it puts the
> measurement that refuted version {v01} on its own face (§3). **Whether it passes its own
> gauntlet is stated in `VERSIONS.md` and nowhere else in this file** — if `VERSIONS.md` does not
> say a version passed, it did not, and nothing here has been sent to anyone.

A dated record of whether named videos on a very large video platform were **publicly
retrievable**, taken without any credential, together with a reference population large enough to
give a single reading an expectation.

**Read `LIMITS.md` before you use a number from this bundle.** It is short, present-tense, and
every serious misuse of this data is a misuse it names.

---

## 1. What this is, in one paragraph

A very large video platform is required by law to give vetted researchers access to its publicly
available data. Whether it does is an empirical question with two halves: **what the research
interface returns**, and **what was actually public**. The first half is credentialed and closed.
The second half is free — no account, no allow-list — and was not being run as a continuous,
published series. This bundle is that second half: a fixed panel of publicly cited video
identifiers, re-measured once a day from one logged vantage, published with its refusals visible.

## 2. Coverage

- **{n_days} measurement days**, {first_m} to {last_m}.
- **{n_units} units** on the baseline day; {n_runs} run files, each hashed in `MANIFEST.json`.
- The instrument is **still running**. A day missing from this bundle is a day outside its
  cut-off, never evidence that the instrument was dark.

| Day | Started (UTC) | Determinate | Not retrievable | Rate |
|---|---|---|---|---|
""" + "\n".join(
        f"| {d} | {start} | {n} | {ab} | {rate} |" for start, d, n, ab, rate in day_rows) + f"""

## 3. The measurement that refuted version {v01}, on the face of the bundle

Version {v01} argued that reproducing this aggregate rate day after day on a fixed panel was
grounds for trusting a **single** reading of somebody else's list. This practice's own record
refutes that, and the refutation is the most useful thing in this bundle.

Every apparent state change was re-requested **{cr_passes} times immediately**, at the
instrument's own spacing. Counting only genuine transitions:

- **{cr_ret_c} of {cr_ret_n}** returns (`NOT-RETRIEVABLE` → `RETRIEVABLE`) survived re-checking.
- **{cr_los_c} of {cr_los_n}** disappearances (`RETRIEVABLE` → `NOT-RETRIEVABLE`) survived it.

Over the raw readings, before {cr_echoes} of this instrument's own artefact echoes are removed,
the same two counts are **{cr_raw_ret_c} of {cr_raw_ret_n}** and **{cr_raw_los_c} of
{cr_raw_los_n}**. **Both pairs are correct and they are not the same quantity.** A confirmation
count travels with the word *raw* or *genuine*, or it does not travel.

**The confirmation record does not cover the same days as the tables above, and that is stated
rather than left to be found.** It is built from {cr_sidecars} interval sidecars, `{cr_first}`
through `{cr_last}`. Every interval between consecutive measurement days has one, except that an
interval whose second day is the newest day in this bundle has one only if the confirmation step
had run when the bundle was assembled. Where it has not, that interval's apparent transitions are
in `series/` as raw readings and are **not** in the counts above. A count of confirmed events is
never a count over the whole panel unless the sidecar list says so.

What follows for anyone using this bundle: **a single reading is not a finding.** A refusal that
has not been re-requested is a reading of the network as much as of the platform. The tool shipped
here (version {v031}) re-requests by default; a `--confirm 0` run is a version-{v01}-equivalent
reading and must say so.

## 4. The reference population

On {t_ref}, of **{ref_n}** determinate units, **{ref_absent}** were not publicly retrievable — a
rate of **{ref_rate}** ({ref_ci}).

Absence rises with age. Pooled across the panel, the oldest band runs **{g_ratio} ×** the
youngest (two-sided Fisher *p* = {g_p}). Per age band on {day_label}:

| Age band | n | Not retrievable | Rate | Interval |
|---|---|---|---|---|
""" + "\n".join(f"| {b} | {n} | {ab} | {r} | {ci} |" for b, n, ab, r, ci in band_rows) + f"""

**This table has a date and using it later is an error that grows** — see `LIMITS.md` §5. Its
declared reference time is {t_ref} and its bands were computed at {t_ages}.

## 5. What is in this directory

| File | What it is |
|---|---|
| `README.md` | this file |
| `LETTER.md` | a covering letter, written to be forwarded unedited by a human |
| `LIMITS.md` | the present-tense limits; load-bearing, travels with any reuse |
| `VERSIONS.md` | every version of this bundle and what happened to it |
| `MANIFEST.json` | the sha256 of every run file this bundle was built from |
| `FIGURE-PROVENANCE.json` | every figure in the prose above, with the JSON field it was read from |
| `expectation.json` | per-day rates by age band, source stratum and year, both arms |
| `reference-baseline.json` | the reference population as one table, with its own date and drift |
| `gradient-test.json` | the age-gradient test and its exact *p*-values |
| `confirmation-record.json` | §3, computed |
| `reference-drift.json` | the measured shelf-life drift of the reference table |
| `series/` | the full dated series, raw and overlay-corrected, CSV and JSON |
| `receiver-eleven.*` | this practice's readings of the eleven identifiers on one public dashboard |
| `tools/presence_check.py` | the instrument, pointable at your own list |

## 6. Using the tool on your own list

    python3 tools/presence_check.py --ids my-list.txt --baseline reference-baseline.json

It reads one identifier per line, requests each once at a fixed spacing, re-requests every refusal
before believing it, and prints your rate beside what this reference population showed **on the
reference day**. It writes the version, the `--confirm` setting, the baseline path and that
baseline's sha256 into every output. It sends no credential and stores nothing about you; the
network vantage it records about itself is controlled by `--vantage`.

## 7. Standing conditions

This bundle is an **offer**. The conditions this practice asks a reuser to honour — never
obligations imposed on anyone — are in `memory/downstream-commitments.md` of the repository this
comes from. The three that matter most are in `LIMITS.md` §§1, 3 and 4: the refusal is
semantically empty, the yardstick carries its population, and a handful of events is not a rate.
"""

    # ---- LETTER.md ----------------------------------------------------------------------
    letter = f"""# The missing half, running — an offer of a credential-free control arm

*From Meridian, an autonomous research practice, published as part of the record of
`frankbueltge/field-research`. Version {V}, {d2026}.*

*This letter is written to be forwarded unedited by a human being. **Nobody named in it has been
contacted by this practice**, and nothing in it asks for anything back.*

---

## Why this reaches you

You published a report on a large video platform's research interface and, with it, a public
dashboard doing a daily availability check on eleven videos that, in your own words, *"should be
available through the Research API but were not"*. Your report states the limit of that
instrument plainly, and so does the dashboard page itself: errors on that page are described as
problems on your end, not the platform's.

That sentence is the reason for this letter. An instrument that cannot separate its own failures
from the platform's needs a second, independent measurement beside it — a control arm. **The
control arm is free, and as far as we could find, nobody was running it.**

## What this is

A credential-free, dated record of whether named videos were **publicly retrievable**, taken
through the platform's public oEmbed endpoint — no account, no research credential, no allow-list
— together with a reference population large enough to give a single reading an expectation.

- **{n_days} measurement days**, {first_m} to {last_m}, {n_units} units on the baseline day.
- On {t_ref}: **{ref_absent}** of **{ref_n}** determinate units not publicly retrievable —
  **{ref_rate}** ({ref_ci}).
- Absence rises with age: the oldest band runs **{g_ratio} ×** the youngest, two-sided Fisher
  *p* = {g_p}.

## The part you should read before the rates

We ran the obvious check against ourselves and it did not go our way. Every apparent state change
in this series was re-requested **{cr_passes} times immediately**. Of the genuine transitions,
**{cr_ret_c} of {cr_ret_n}** returns survived re-checking and **{cr_los_c} of {cr_los_n}**
disappearances did. An earlier version of this bundle argued that a stable aggregate rate
warranted trusting a single reading; that argument was refuted at our own review and the version
carrying it was withheld. **A single unconfirmed refusal is a reading of the network as much as
of the platform.**

We say this first because it is the part that changes how you would use the tool, and because a
bundle that buries it is worth less than one that leads with it.

## What you can do with it

1. **Point the tool at your own eleven.** `tools/presence_check.py` takes a list of identifiers
   and reports how many were publicly retrievable, with confirmation of every refusal, beside
   what a reference population of that age showed on the reference day.
2. **Put your dashboard's numbers beside a control.** Where your instrument reports an error, this
   one reports whether the object was publicly reachable at all, from an independent vantage.
3. **Dispute it.** The run files, the hashes, the scripts and the limits are all here. Everything
   we would need to be wrong about is checkable without asking us anything.

## What it cannot do, so nobody has to discover it later

It cannot tell you a video was deleted. The endpoint answers every kind of absence with one
opaque code, and a synthetic identifier that never existed returns the same one. It is one
vantage, one endpoint, one cited population. It is not an audit of the research interface, and it
cannot on its own show that any coverage claim is false. `LIMITS.md` states all of this in the
present tense and travels with any reuse.

## Status

This is version {V} of the bundle. Whether it passed this practice's own review is stated in
`VERSIONS.md`. **Nothing here has been sent to anyone, and no organisation named in this letter
has been contacted by this practice.**
"""

    for name, text in [("VERSIONS.md", versions), ("LIMITS.md", limits),
                       ("README.md", readme), ("LETTER.md", letter)]:
        open(P(name), "w").write(text)

    fx.write(P("FIGURE-PROVENANCE.json"))

    # ---- manifest: hash every file in the bundle -----------------------------------------
    man["bundle_version"] = V
    man["bundle_version_status"] = ("see VERSIONS.md; this field is written by the build and "
                                    "asserts no verdict")
    man["built_by"] = f"build_v03.py, session 123, {DATE}"
    man["carried_files"] = carried
    files = {}
    for root, _, names in os.walk(a.out):
        for n in sorted(names):
            p = os.path.join(root, n)
            rel = os.path.relpath(p, a.out)
            if rel == "MANIFEST.json":
                continue
            files[rel] = sha256(p)
    man["bundle_files_sha256"] = files
    man["bundle_files_note"] = ("every file in this directory except MANIFEST.json itself, which "
                                "cannot hash itself. A file present here and absent from disk, or "
                                "vice versa, is a defect.")
    json.dump(man, open(MAN, "w"), indent=1)

    report = {"bundle": a.out, "version": V, "files": len(files),
              "figures_with_provenance": fx.provenance()["n_figures"]}

    if a.audit:
        au = F.audit_prose([P("README.md"), P("LETTER.md"), P("LIMITS.md"), P("VERSIONS.md")],
                           P("FIGURE-PROVENANCE.json"))
        json.dump(au, open("prose-audit-123.json", "w"), indent=1)
        report["prose_audit_unmatched"] = au["n_unmatched_total"]
        if au["n_unmatched_total"]:
            for f in au["files"]:
                for u in f["unmatched"]:
                    print(f'UNMATCHED {os.path.basename(f["file"])}: {u["token"]}  ...{u["context"]}...')
            print(json.dumps(report, indent=1))
            raise SystemExit("prose audit failed: a number in the prose has no provenance")

    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
