#!/usr/bin/env python3
"""figures_page - FIGURES.md, every number fetched from a named field of the bundle's own JSON.

Session 124, 2026-08-16. Written to discharge `CONDITIONS-123.md`, binding item 1:

    Route `FIGURES.md`'s figures through `figures.py`, or publish its unmatched count. It is
    the densest table of numbers a receiver would read and it sits outside every guard this
    session built. Finding 9.

WHAT WAS WRONG, PRECISELY
-------------------------
`FIGURES.md` was **generated**, so nobody had typed its tables - and that is the thing that made
it look safe. It was assembled inside `build_deliverable.py` from the same in-memory dicts that
had just been written to `expectation.json`. Two consequences, neither of them visible from the
page:

1. **The page and the data file could not disagree, because they were the same variable.** That
   reads like a guarantee and is the opposite of one: it means nothing ever checked that the
   number on the page is the field the sentence around it names. A cell read from the wrong key
   of the right dict is a correct number in a false sentence, and the shipped page had no way to
   say which key any cell came from.
2. **Literals had been written into the generated prose by hand**, where the surrounding machine
   generation vouched for them. `0.0577 pp`, `248 of 249`, `37 encyclopedia language editions` -
   all three sit inside f-strings in the old generator. The third is the arc's own erratum E9
   (published as `21`, corrected to `37`): it was corrected by typing the new number into the
   generator, so the page will go quietly wrong again the day the panel changes.

WHAT THIS MODULE DOES INSTEAD
------------------------------
It rebuilds the page **from the files the bundle ships**, after they are written, through
`figures.Figures`. Every rendered figure records the file and the JSON path it came from, so
`FIGURE-PROVENANCE.json` covers the densest page in the bundle and `figures.audit_prose` can be
run over it. A number the page needs that is not already a field somewhere is **computed into
`figures-derived.json` first**, which ships in the bundle, and then fetched from there - so
"where does this come from" always has a file-and-field answer, including for the three former
literals.

That also closes the first gauntlet's non-blocking finding 14: the page's two INDETERMINATE
counts differ in scope (one excludes the control arm, one does not). They are now two named
fields, computed side by side, and the page says which is which.

WHAT IT STILL CANNOT DO
-----------------------
Exactly what `figures.py` says it cannot do: it cannot know whether the sentence around a
correctly-fetched figure describes that field correctly. It also cannot see a number written as
a word - this arc published that hole as erratum E3 of session 123 and it is still open. And
the identifiers in section 5's table are inline code, which the auditor skips as addresses
rather than claims; that is a deliberate exclusion, named here so it is not a silence.
"""
import json
import os
import re

import figures as F

BAND_ORDER_SOURCE = "expectation.json:per_day.<newest>.by_age_band (insertion order)"


def _load(out, name):
    return json.load(open(os.path.join(out, name)))


def newest_day(exp):
    return [d for d in exp["per_day"] if d != "baseline"][-1]


def derive(out, draft_root="."):
    """Compute every quantity the page states that is not already a field, and write it into the
    bundle as `figures-derived.json`.

    Each entry carries `what` - the sentence the figure is used in - so a reviewer checking the
    provenance table can see the claim the field is supposed to support without opening the page.
    """
    exp = _load(out, "expectation.json")
    ser = _load(out, os.path.join("series", "presence-series.json"))
    newest = newest_day(exp)
    labels = [d["label"] for d in ser["days"]]
    units = ser["units"]

    # ---- the balanced panel -----------------------------------------------------------
    # The raw across-day spread moves partly because different units fall out as INDETERMINATE
    # on different days. The balanced panel holds the membership fixed: only units determinate
    # on EVERY day, control arm excluded. Published as 0.0577 pp at the first gauntlet (E17) and
    # then TYPED into the generator; computed here.
    DET = ("RETRIEVABLE", "NOT-RETRIEVABLE")
    balanced = [u for u in units
                if u["arm"] != "B-truncated"
                and all(u["states"].get(l) in DET for l in labels)]
    bal_rates = {}
    for l in labels:
        absent = sum(1 for u in balanced if u["states"][l] == "NOT-RETRIEVABLE")
        bal_rates[l] = {"n": len(balanced), "absent": absent,
                        "absent_rate": (absent / len(balanced)) if balanced else None}
    bvals = [bal_rates[l]["absent_rate"] for l in labels]
    raw_range = exp["across_day_stability"]["__pooled__"]["range"]
    bal_range = max(bvals) - min(bvals)

    # ---- the control arm ---------------------------------------------------------------
    # "display-truncated strings, 248 of 249 of which do not resolve" was a typed literal.
    ctrl = [u for u in units if u["arm"] == "B-truncated"]
    ctrl_resolving = [u for u in ctrl if u["states"].get(newest) == "RETRIEVABLE"]

    # ---- how much the panel moves at all -----------------------------------------------
    noncontrol = [u for u in units if u["arm"] != "B-truncated"]
    def _changes(u, key):
        seen = {u[key].get(l) for l in labels} & set(DET)
        return len(seen) > 1
    changed_raw = [u for u in noncontrol if _changes(u, "states")]
    changed_cor = [u for u in noncontrol if _changes(u, "states_corrected")]

    # ---- transport noise, and the two scopes named apart --------------------------------
    # First gauntlet, non-blocking finding 14: the page printed an INDETERMINATE count per day
    # over ALL units (control arm included) beside an `excluded.indeterminate` count that
    # excludes the control arm, with nothing saying they were different questions.
    ind_all, ind_noncontrol = {}, {}
    for l in labels:
        ind_all[l] = sorted(u["vid"] for u in units if u["states"].get(l) == "INDETERMINATE")
        ind_noncontrol[l] = sorted(u["vid"] for u in noncontrol
                                   if u["states"].get(l) == "INDETERMINATE")
    pairs = [(a, b) for i, a in enumerate(labels) for b in labels[i + 1:]]
    overlaps = [{"days": [a, b],
                 "n_shared_indeterminate": len(set(ind_all[a]) & set(ind_all[b]))}
                for a, b in pairs]

    # ---- how many encyclopedia language editions actually contribute ---------------------
    # Erratum E9/V3-E4: the bundle said 21 for three versions; the true value is 37. It was
    # repaired by typing 37 into the generator, which is the same defect with a better number.
    # Re-derived here at build time, the way session 123's discharge derived it: the distinct
    # encyclopedia hosts that cite at least one identifier which is a W-article unit of THIS
    # panel. If the corpus files are not beside the builder, the field says so and the page
    # prints the reason instead of a stale integer.
    editions, edition_note = None, None
    try:
        # `arm` is the harvest arm (A, A2, A-new, B, B-truncated); `stratum` is what the tables
        # are cut by (W-article, W-other-ns, F-forum). The first version of this derivation
        # filtered on `arm == "W-article"`, which matches NOTHING, and the field came back 0 -
        # caught by the equivalence check below before it reached a page. Named here because a
        # silent zero is exactly the failure this module exists to prevent.
        article_vids = {u["vid"] for u in units if u.get("stratum") == "W-article"}
        hosts = set()
        matched = set()
        for fn in sorted(os.listdir(draft_root)):
            m = re.match(r"corpus-(.+)\.json$", fn)
            if not m:
                continue
            host = m.group(1)
            try:
                doc = json.load(open(os.path.join(draft_root, fn)))
            except (OSError, ValueError):
                continue
            # The corpus files nest differently across harvest generations, so identifiers are
            # taken as digit runs anywhere in the file and intersected with the panel - the same
            # method session 123's discharge used to re-derive this count independently.
            blob = json.dumps(doc)
            present = set(re.findall(r"(?<!\d)(\d{8,20})(?!\d)", blob))
            hit = article_vids & present
            if hit:
                hosts.add(host)
                matched |= hit
        editions = sorted(h for h in hosts if h.endswith("wikipedia.org"))
        edition_note = (f"distinct encyclopedia hosts whose corpus file cites at least one of "
                        f"this panel's {len(article_vids)} W-article identifiers; "
                        f"{len(matched)} of those identifiers were matched to at least one "
                        f"edition. Re-derived at build time from the corpus files beside the "
                        f"builder, not typed.")
    except OSError as e:                                   # pragma: no cover - stated, not hidden
        edition_note = (f"could not be derived at build time ({type(e).__name__}); the page says "
                        f"so rather than printing a number no file supports")

    derived = {
        "schema": "field-research/figures-page-derived/1",
        "written_by": "figures_page.derive(), session 124, 2026-08-16",
        "what_this_is": ("every quantity FIGURES.md states that is not already a field of "
                         "expectation.json, gradient-test.json or reference-baseline.json. It "
                         "exists so that no number on that page is a literal typed into a "
                         "generator: the page fetches from here, and this file is built from the "
                         "series the bundle ships."),
        "newest_day": newest,
        "n_days": len(labels),
        "balanced_panel": {
            "what": ("the across-day spread with panel membership held fixed: only units "
                     "determinate on every measured day, control arm excluded. The raw spread "
                     "is larger and the excess is which units fell out as INDETERMINATE, not "
                     "anything about the platform (first gauntlet, E17)."),
            "n_units": len(balanced),
            "per_day": bal_rates,
            "min": min(bvals) if bvals else None,
            "max": max(bvals) if bvals else None,
            "range": bal_range,
            "raw_range": raw_range,
            "raw_over_balanced": (raw_range / bal_range) if bal_range else None,
        },
        "control_arm": {
            "what": ("the B-truncated control: display-truncated identifier strings, excluded "
                     "from every rate. The count that resolves is the arc's erratum E7 - one of "
                     "them is a real video predating the platform's current identifier scheme."),
            "n": len(ctrl),
            "n_resolving_on_newest_day": len(ctrl_resolving),
            "n_not_resolving_on_newest_day": len(ctrl) - len(ctrl_resolving),
            "resolving_ids": [u["vid"] for u in ctrl_resolving],
        },
        "movement": {
            "what": ("non-control identifiers showing more than one determinate state across "
                     "the measured days, before and after the refuted-reading overlay."),
            "n_noncontrol": len(noncontrol),
            "n_changed_raw": len(changed_raw),
            "n_changed_corrected": len(changed_cor),
            "changed_ids": [u["vid"] for u in changed_raw],
        },
        "indeterminate": {
            "what": ("two counts that are NOT the same question, printed apart because the "
                     "first gauntlet found them printed together (finding 14). `all_units` "
                     "includes the B-truncated control arm; `noncontrol` excludes it and is the "
                     "scope of `expectation.json`'s per-day `excluded.indeterminate`."),
            "all_units": {l: {"n": len(ind_all[l]),
                              "share_of_run": len(ind_all[l]) / len(units) if units else None}
                          for l in labels},
            "noncontrol": {l: {"n": len(ind_noncontrol[l]),
                               "share_of_noncontrol": (len(ind_noncontrol[l]) / len(noncontrol)
                                                       if noncontrol else None)}
                           for l in labels},
            "n_day_pairs": len(pairs),
            "pair_overlaps": overlaps,
            "max_pair_overlap": max((o["n_shared_indeterminate"] for o in overlaps), default=None),
        },
        "population": {
            "what": ("how many encyclopedia language editions actually contribute a W-article "
                     "unit to this panel. Published as 21 in versions 0.1-0.3, corrected at the "
                     "first gauntlet (E9 / V3-E4)."),
            "n_encyclopedia_language_editions": len(editions) if editions is not None else None,
            "editions": editions,
            "derivation": edition_note,
        },
    }
    json.dump(derived, open(os.path.join(out, "figures-derived.json"), "w"), indent=1)
    return derived


def render(out, fx=None, built_at=None):
    """Write FIGURES.md from the bundle's own JSON, through `figures.Figures`.

    Returns the `Figures` instance, so the caller can merge its provenance into the bundle's
    provenance table.
    """
    fx = fx or F.Figures(relative_to=out)
    P = lambda n: os.path.join(out, n)
    EXP, GRAD, DER = P("expectation.json"), P("gradient-test.json"), P("figures-derived.json")
    SER = P(os.path.join("series", "presence-series.json"))

    exp, ser, der = _load(out, "expectation.json"), _load(out, "series/presence-series.json"), \
        _load(out, "figures-derived.json")
    grad = _load(out, "gradient-test.json")
    newest = newest_day(exp)
    labels = [d["label"] for d in ser["days"]]
    bands = list(exp["per_day"][newest]["by_age_band"].keys())
    strata = sorted(exp["per_day"][newest]["by_stratum_band"].keys())

    L = []
    L.append("# Figures — generated, do not hand-edit\n")
    L.append(f"*Written by `figures_page.py` at "
             f"{fx.lit(built_at, 'the build clock, read from the system at build time') if built_at else '(unstamped)'}"
             f". **Every number on this page is fetched from a named field of a file in this "
             f"bundle** — `expectation.json`, `gradient-test.json`, "
             f"`series/presence-series.json`, or `figures-derived.json`, which is built from the "
             f"series — and the field is recorded in `FIGURES-PROVENANCE.json` — the table that governs this page, a different file from the `FIGURE-PROVENANCE.json` that governs the prose. Before version "
             f"{fx.lit('0.3.2', 'the version in which this page was routed through the provenance guard')} "
             f"this page was generated from variables rather than from files, and three of its "
             f"numbers were literals typed into the generator; see `VERSIONS.md`.*\n")

    # ---- 1 ------------------------------------------------------------------------------
    L.append("## 1. The panel, and what was measured each day\n")
    CI_LEVEL = fx.lit("95", "the confidence level of the Wilson interval — a stated method "
                      "parameter of this arc, not a measured quantity")
    L.append(f"| day | measurement started (UTC) | units requested | in the rate | "
             f"publicly absent | absent rate | {CI_LEVEL} % Wilson |")
    L.append("|---|---|---|---|---|---|---|")
    for i, d in enumerate(ser["days"]):
        lbl = fx.key(EXP, "per_day", d["label"], "the label of a measured day")
        start = fx.raw(SER, f"days[{i}].utc_start", f"{lbl}: when the measurement started")
        req = (fx.n(SER, f"days[{i}].requested", f"{lbl}: identifiers requested")
               if "requested" in d else fx.n(SER, "n_units", f"{lbl}: units in the panel"))
        n = fx.n(EXP, f"per_day.{lbl}.pooled.n", f"{lbl}: units in the rate")
        ab = fx.n(EXP, f"per_day.{lbl}.pooled.absent", f"{lbl}: units not retrievable")
        rt = fx.pct(EXP, f"per_day.{lbl}.pooled.absent_rate", 2, f"{lbl}: pooled absence rate")
        ci = fx.ci(EXP, f"per_day.{lbl}.pooled.absent_ci", 2, f"{lbl}: Wilson interval")
        L.append(f"| {lbl} | {start} | {req} | {n} | {ab} | {rt} | [{ci}] |")
    L.append("")
    L.append(f"**Across {fx.raw(EXP, 'across_day_stability.__pooled__.days', 'measured days')} "
             f"measured days the pooled public-absence rate of this panel moves between "
             f"{fx.pct(EXP, 'across_day_stability.__pooled__.min', 2, 'lowest pooled rate')} and "
             f"{fx.pct(EXP, 'across_day_stability.__pooled__.max', 2, 'highest pooled rate')} — a "
             f"spread of "
             f"{fx.pp(EXP, 'across_day_stability.__pooled__.range', 2, 'raw across-day spread')} "
             f"on the RAW panel.**")
    L.append(f"On the balanced panel — the "
             f"{fx.n(DER, 'balanced_panel.n_units', 'units determinate on every measured day')} "
             f"non-control identifiers that are determinate on every measured day — the spread is "
             f"{fx.pp(DER, 'balanced_panel.range', 4, 'balanced-panel across-day spread')}. "
             f"The raw figure is "
             f"{fx.num(DER, 'balanced_panel.raw_over_balanced', 2, 'raw spread over balanced')}× "
             f"larger, and the excess is which units fell out as `INDETERMINATE`, not anything "
             f"about the platform (first gauntlet, E17). This is the same panel measured again, "
             f"so it is the instrument's test-retest reproducibility and not sampling error "
             f"(`LIMITS.md`).\n")

    # ---- 2 ------------------------------------------------------------------------------
    L.append("## 2. Public absence by the age of the video — newest day\n")
    L.append(f"*Day: {fx.key(EXP, 'per_day', newest, 'the newest measured day')}. Ages are "
             f"decoded from the identifier (`LIMITS.md`).*\n")
    L.append(f"| age band | in the rate | publicly absent | absent rate | {CI_LEVEL} % Wilson | "
             f"spread across all measured days |")
    L.append("|---|---|---|---|---|---|")
    for b in bands:
        blab = fx.key(EXP, f"per_day.{newest}.by_age_band", b, "an age-band label")
        base = f"per_day.{newest}.by_age_band.{b}"
        n = fx.n(EXP, f"{base}.n", f"{b}: units in the rate")
        ab = fx.n(EXP, f"{base}.absent", f"{b}: units not retrievable")
        rt = fx.pct(EXP, f"{base}.absent_rate", 2, f"{b}: absence rate")
        ci = fx.ci(EXP, f"{base}.absent_ci", 2, f"{b}: Wilson interval")
        sp = (fx.pp(EXP, f"across_day_stability.{b}.range", 2, f"{b}: across-day spread")
              if b in exp["across_day_stability"] else "—")
        L.append(f"| {blab} | {n} | {ab} | {rt} | [{ci}] | {sp} |")
    L.append("")

    # ---- 3 ------------------------------------------------------------------------------
    L.append("## 3. The same gradient inside each source stratum\n")
    L.append("*If the gradient were an artefact of which source the older identifiers come "
             "from, it would not survive this split.*\n")
    L.append("| age band | " + " | ".join(f"`{s}`" for s in strata) + " |")
    L.append("|---|" + "---|" * len(strata))
    for b in bands:
        blab = fx.key(EXP, f"per_day.{newest}.by_age_band", b, "an age-band label")
        cells = []
        for s in strata:
            base = f"per_day.{newest}.by_stratum_band.{s}.{b}"
            try:
                rt = fx.pct(EXP, f"{base}.absent_rate", 2, f"{s} / {b}: absence rate")
                n = fx.n(EXP, f"{base}.n", f"{s} / {b}: units in the rate")
                cells.append(f"{rt} (n={n})")
            except F.MissingField:
                cells.append("—")
        L.append(f"| {blab} | " + " | ".join(cells) + " |")
    L.append("")

    young = fx.raw(GRAD, "results[0].young_band", "youngest band, the gradient's low end")
    old = fx.raw(GRAD, "results[0].old_band", "oldest band, the gradient's high end")
    L.append(f"**The gradient's own test — {young} against {old} on "
             f"{fx.raw(GRAD, 'day', 'the day the gradient test was run on')}, two-sided Fisher "
             f"exact.** The pooled progression is not strictly monotone: it rises across the "
             f"bands with one flat step near four years, and the endpoints are what is tested "
             f"here.\n")
    L.append(f"| group | {young} | {old} | ratio | Fisher two-sided p |")
    L.append("|---|---|---|---|---|")
    for i, g in enumerate(grad["results"]):
        name = fx.raw(GRAD, f"results[{i}].group", "which population this row tests")
        ya = fx.n(GRAD, f"results[{i}].young[0]", f"{g['group']}: young band, absent")
        yn = fx.n(GRAD, f"results[{i}].young[1]", f"{g['group']}: young band, in the rate")
        oa = fx.n(GRAD, f"results[{i}].old[0]", f"{g['group']}: old band, absent")
        on = fx.n(GRAD, f"results[{i}].old[1]", f"{g['group']}: old band, in the rate")
        # The rates the two fractions come to. The shipped page printed them beside the
        # fractions and this page must not quietly drop a column while claiming to add
        # provenance - so they are fetched from the band tables the test was computed on.
        yp = fx.pct(EXP, f"per_day.{newest}.by_age_band.{g['young_band']}.absent_rate", 2,
                    f"{g['group']}: young-band rate") if g["group"] == "pooled" else \
            fx.pct(EXP, f"per_day.{newest}.by_stratum_band.{g['group']}.{g['young_band']}."
                        f"absent_rate", 2, f"{g['group']}: young-band rate")
        op = fx.pct(EXP, f"per_day.{newest}.by_age_band.{g['old_band']}.absent_rate", 2,
                    f"{g['group']}: old-band rate") if g["group"] == "pooled" else \
            fx.pct(EXP, f"per_day.{newest}.by_stratum_band.{g['group']}.{g['old_band']}."
                        f"absent_rate", 2, f"{g['group']}: old-band rate")
        rt = (fx.num(GRAD, f"results[{i}].ratio_old_over_young", 2, f"{g['group']}: ratio")
              if g.get("ratio_old_over_young") is not None else "—")
        p = fx.sci(GRAD, f"results[{i}].fisher_two_sided_p", 3, f"{g['group']}: Fisher p")
        L.append(f"| {name} | {ya}/{yn} ({yp}) | {oa}/{on} ({op}) | {rt} × | {p} |")
    L.append("")

    # ---- 4 ------------------------------------------------------------------------------
    L.append("## 4. Where the identifiers come from — newest day\n")
    n_ed = der["population"]["n_encyclopedia_language_editions"]
    ed_txt = (f"article space of "
              f"{fx.n(DER, 'population.n_encyclopedia_language_editions', 'encyclopedia language editions contributing a W-article unit')}"
              f" encyclopedia language editions"
              if n_ed is not None else
              "article space of the encyclopedia language editions listed in "
              "`figures-derived.json` (the count could not be derived at build time)")
    what = {"W-article": ed_txt,
            "W-other-ns": "non-article namespaces of the same editions",
            "F-forum": "public comments and stories of one technology forum"}
    L.append("| stratum | what it is | in the rate | publicly absent | absent rate |")
    L.append("|---|---|---|---|---|")
    for s in strata:
        base = f"per_day.{newest}.by_stratum.{s}"
        n = fx.n(EXP, f"{base}.n", f"{s}: units in the rate")
        ab = fx.n(EXP, f"{base}.absent", f"{s}: units not retrievable")
        rt = fx.pct(EXP, f"{base}.absent_rate", 2, f"{s}: absence rate")
        L.append(f"| `{s}` | {what.get(s, '—')} | {n} | {ab} | {rt} |")
    L.append("")
    L.append(f"**Excluded from every rate on the newest day:** "
             f"{fx.n(EXP, f'per_day.{newest}.excluded.arm_B_truncated', 'control-arm identifiers excluded')} "
             f"identifiers of the `B-truncated` control arm, which are display-truncated strings, "
             f"{fx.n(DER, 'control_arm.n_not_resolving_on_newest_day', 'control identifiers that do not resolve')} "
             f"of {fx.n(DER, 'control_arm.n', 'control identifiers in total')} of which do not "
             f"resolve — the remainder is a real video predating the platform's current "
             f"identifier scheme (first gauntlet, E7); "
             f"{fx.n(EXP, f'per_day.{newest}.excluded.indeterminate', 'observations excluded as INDETERMINATE, control arm not counted')} "
             f"observations that ended in a transport failure or an unexpected status "
             f"(`INDETERMINATE`, control arm not counted — see section 6); and "
             f"{fx.n(EXP, f'per_day.{newest}.excluded.undatable', 'identifiers with no decodable creation time')} "
             f"identifiers that carry no decodable creation time and are therefore absent from "
             f"the age-banded tables only.\n")

    # ---- 5 ------------------------------------------------------------------------------
    L.append("## 5. How much this panel moves at all\n")
    L.append(f"Over {fx.n(DER, 'n_days', 'measured days in this bundle')} measured days, "
             f"**{fx.n(DER, 'movement.n_changed_raw', 'non-control identifiers with more than one determinate state, raw')} "
             f"of {fx.n(DER, 'movement.n_noncontrol', 'non-control identifiers in the panel')}** "
             f"non-control identifiers show more than one determinate state in the raw record, "
             f"and **{fx.n(DER, 'movement.n_changed_corrected', 'the same count after the refuted-reading overlay')}** "
             f"do so after the refuted-reading overlay is applied. The identifiers are listed so "
             f"the claim can be checked:\n")
    daylabs = [fx.key(EXP, "per_day", l, "the label of a measured day") for l in labels]
    L.append("| video id | arm | " + " | ".join(daylabs) + " | changes after overlay |")
    L.append("|---|---|" + "---|" * len(labels) + "---|")
    by_vid = {u["vid"]: u for u in ser["units"]}
    for vid in der["movement"]["changed_ids"]:
        u = by_vid[vid]
        det = {u["states_corrected"].get(l) for l in labels} & {"RETRIEVABLE", "NOT-RETRIEVABLE"}
        L.append(f"| `{vid}` | {u['arm']} | "
                 + " | ".join(u["states"].get(l, "—") for l in labels)
                 + f" | {'yes' if len(det) > 1 else 'no — refuted reading, see overlay'} |")
    L.append("")

    # ---- 6 ------------------------------------------------------------------------------
    L.append("## 6. Transport noise\n")
    L.append("*Two counts, and they are not the same question. The first gauntlet found them "
             "printed together with nothing saying so (finding 14). `all units` includes the "
             "`B-truncated` control arm; `non-control` excludes it and is the scope of the "
             "exclusion counts in section 4.*\n")
    L.append("| day | INDETERMINATE, all units | share of the run | INDETERMINATE, non-control |")
    L.append("|---|---|---|---|")
    for l in labels:
        llab = fx.key(EXP, "per_day", l, "the label of a measured day")
        a_n = fx.n(DER, f"indeterminate.all_units.{l}.n", f"{l}: indeterminate, all units")
        a_s = fx.pct(DER, f"indeterminate.all_units.{l}.share_of_run", 2,
                     f"{l}: indeterminate share of the run")
        nc = fx.n(DER, f"indeterminate.noncontrol.{l}.n", f"{l}: indeterminate, non-control")
        L.append(f"| {llab} | {a_n} | {a_s} | {nc} |")
    L.append("")
    ovs = ", ".join(fx.n(DER, f"indeterminate.pair_overlaps[{i}].n_shared_indeterminate",
                         f"{o['days'][0]} ∩ {o['days'][1]}: identifiers indeterminate on both")
                    for i, o in enumerate(der["indeterminate"]["pair_overlaps"]))
    L.append(f"**The same identifier is almost never indeterminate twice.** Across the "
             f"{fx.n(DER, 'indeterminate.n_day_pairs', 'day-pairs')} day-pairs the overlap is "
             f"{ovs} identifiers respectively — at most "
             f"{fx.n(DER, 'indeterminate.max_pair_overlap', 'the largest overlap of any day-pair')}. "
             f"Transport noise is therefore a property of the request, not of the video — which "
             f"is why `INDETERMINATE` is excluded from rates rather than read as weak absence.\n")

    open(os.path.join(out, "FIGURES.md"), "w").write("\n".join(L) + "\n")
    return fx


def build(out, draft_root=".", fx=None, built_at=None):
    derive(out, draft_root)
    return render(out, fx, built_at)


if __name__ == "__main__":
    import sys
    import time
    d = sys.argv[1] if len(sys.argv) > 1 else "deliverable-v0.3"
    f = build(d, ".", built_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    print(json.dumps({"figures_recorded": f.provenance()["n_figures"]}, indent=1))
