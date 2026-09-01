#!/usr/bin/env python3
"""The response clock: how long a public expression of concern stands before it
is resolved into a retraction.

Two independent corpora, the same question asked of each:

  A. The Retraction Watch database as distributed by Crossref (one CSV of
     notices; `RetractionNature` gives the notice type).
  B. The Crossref REST API's own notice records, harvested by
     `harvest_crossref.py` (each notice's `update-to` list names the works it
     acts on and the date the publisher assigned).

A paper enters the cohort on the date of its first expression of concern. It
leaves on the date of its first subsequent retraction notice. Papers whose
concern is younger than the follow-up window are excluded from the headline
rather than censored, so the headline needs no survival model to be read; a
Kaplan-Meier estimate over the whole cohort is reported beside it.

Uncertainty is a bootstrap resampled over *issuance days*, not papers:
expressions of concern arrive in batches — one day in the record carries 434 of
them — so papers are not independent units and a paper-level interval would be
far too narrow.

Usage: python3 ledger.py <rw.csv> <crossref-dir> <out-dir>
"""
import collections
import csv
import datetime as dt
import json
import random
import statistics
import sys

csv.field_size_limit(10 ** 9)

FOLLOW_UP_DAYS = int(365.25 * 5)   # the headline window
BOOTSTRAP_DRAWS = 2000
SEED = 20260901


# ---------------------------------------------------------------- corpus A

def parse_rw_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return dt.datetime.strptime(s.split(" ")[0], "%m/%d/%Y").date()
    except ValueError:
        return None


def load_retraction_watch(path):
    """-> (papers, cutoff, raw_row_count). One entry per original paper DOI."""
    rows = list(csv.DictReader(open(path, newline="", encoding="utf-8",
                                    errors="replace")))
    all_dates = [d for d in (parse_rw_date(r["RetractionDate"]) for r in rows) if d]
    cutoff = max(all_dates)

    by_doi = collections.defaultdict(list)
    for r in rows:
        doi = (r["OriginalPaperDOI"] or "").strip().lower()
        if doi and doi != "unavailable":
            by_doi[doi].append(r)

    papers = []
    for doi, group in by_doi.items():
        eocs = [(parse_rw_date(r["RetractionDate"]), r) for r in group
                if r["RetractionNature"] == "Expression of concern"]
        eocs = [(d, r) for d, r in eocs if d]
        if not eocs:
            continue
        flag_date, flag_row = min(eocs, key=lambda p: p[0])
        if flag_date > cutoff or flag_date.year < 1990:
            continue          # implausible or out-of-range dates, reported
        retractions = [parse_rw_date(r["RetractionDate"]) for r in group
                       if r["RetractionNature"] == "Retraction"]
        retractions = [d for d in retractions if d and d >= flag_date]
        later = [(parse_rw_date(r["RetractionDate"]), r["RetractionNature"])
                 for r in group]
        later = [(d, n) for d, n in later
                 if d and d > flag_date and n != "Expression of concern"]
        papers.append({
            "doi": doi,
            "flag": flag_date,
            "notice_doi": (flag_row["RetractionDOI"] or "").strip().lower(),
            "publisher": (flag_row["Publisher"] or "").strip(),
            "days": (min(retractions) - flag_date).days if retractions else None,
            "next_notice": sorted(later)[0][1] if later else None,
        })
    return papers, cutoff, len(rows)


# ---------------------------------------------------------------- corpus B

def load_crossref(directory, cutoff):
    """-> papers, from the Crossref API's own notice records."""
    def read(name, want):
        first = {}
        with open(f"{directory}/{name}", encoding="utf-8") as fh:
            for line in fh:
                notice = json.loads(line)
                for upd in notice.get("update-to") or []:
                    if upd.get("type") != want:
                        continue
                    target = (upd.get("DOI") or "").strip().lower()
                    stamp = (upd.get("updated") or {}).get("date-time")
                    if not target or not stamp:
                        continue
                    try:
                        d = dt.date.fromisoformat(stamp[:10])
                    except ValueError:
                        continue
                    if d.year < 1990 or d > cutoff:
                        continue
                    if target not in first or d < first[target][0]:
                        first[target] = (d, (notice.get("DOI") or "").lower())
        return first

    eoc = read("crossref-eoc.jsonl", "expression_of_concern")
    retr = read("crossref-retraction.jsonl", "retraction")
    papers = []
    for doi, (flag_date, notice_doi) in eoc.items():
        r = retr.get(doi)
        days = (r[0] - flag_date).days if r and r[0] >= flag_date else None
        papers.append({"doi": doi, "flag": flag_date, "notice_doi": notice_doi,
                       "publisher": "", "days": days, "next_notice": None})
    return papers


# ---------------------------------------------------------------- measures

def resolved(paper, window=FOLLOW_UP_DAYS):
    return paper["days"] is not None and paper["days"] <= window


def mature(papers, cutoff, window=FOLLOW_UP_DAYS):
    """Papers whose concern has had the full follow-up window to be resolved."""
    horizon = cutoff - dt.timedelta(days=window)
    return [p for p in papers if p["flag"] <= horizon]


def headline(cohort):
    hit = [p for p in cohort if resolved(p)]
    return {
        "n": len(cohort),
        "resolved": len(hit),
        "share": 100 * len(hit) / len(cohort) if cohort else None,
        "median_days": statistics.median([p["days"] for p in hit]) if hit else None,
        "issuance_days": len({p["flag"] for p in cohort}),
    }


def bootstrap(cohort, draws=BOOTSTRAP_DRAWS, seed=SEED):
    """Resampled over issuance days, because concerns arrive in batches."""
    by_day = collections.defaultdict(list)
    for p in cohort:
        by_day[p["flag"]].append(p)
    days = list(by_day)
    rng = random.Random(seed)
    shares, medians = [], []
    for _ in range(draws):
        sample = []
        for _ in range(len(days)):
            sample.extend(by_day[rng.choice(days)])
        hit = [p for p in sample if resolved(p)]
        if sample:
            shares.append(100 * len(hit) / len(sample))
        if hit:
            medians.append(statistics.median([p["days"] for p in hit]))
    shares.sort()
    medians.sort()
    lo, hi = int(0.025 * len(shares)), int(0.975 * len(shares)) - 1
    mlo, mhi = int(0.025 * len(medians)), int(0.975 * len(medians)) - 1
    return {"share_ci": [round(shares[lo], 1), round(shares[hi], 1)],
            "median_ci": [medians[mlo], medians[mhi]]}


def kaplan_meier(papers, cutoff):
    """Whole cohort, censoring unresolved papers at the file's own cutoff."""
    obs = []
    for p in papers:
        if p["days"] is not None:
            obs.append((p["days"], 1))
        else:
            obs.append(((cutoff - p["flag"]).days, 0))
    times = sorted({t for t, e in obs if e == 1})
    surv, curve = 1.0, [(0, 1.0)]
    for t in times:
        at_risk = sum(1 for tt, _ in obs if tt >= t)
        events = sum(1 for tt, e in obs if tt == t and e == 1)
        if at_risk:
            surv *= 1 - events / at_risk
            curve.append((t, surv))
    return curve


def at_day(curve, day):
    s = 1.0
    for t, v in curve:
        if t <= day:
            s = v
        else:
            break
    return s


def notice_level(cohort):
    by_notice = collections.defaultdict(list)
    for p in cohort:
        key = p["notice_doi"] or f"no-doi:{p['doi']}"
        by_notice[key].append(p)
    full = sum(1 for v in by_notice.values() if all(resolved(p) for p in v))
    part = sum(1 for v in by_notice.values()
               if any(resolved(p) for p in v) and not all(resolved(p) for p in v))
    return {"notices": len(by_notice), "fully_resolved": full,
            "partly_resolved": part, "unresolved": len(by_notice) - full - part,
            "share": round(100 * full / len(by_notice), 1) if by_notice else None,
            "largest_notice": max((len(v) for v in by_notice.values()), default=0)}


def by_publisher(cohort, minimum=25):
    out = []
    groups = collections.defaultdict(list)
    for p in cohort:
        if p["publisher"]:
            groups[p["publisher"]].append(p)
    for name, papers in groups.items():
        if len(papers) < minimum:
            continue
        hit = [p for p in papers if resolved(p)]
        out.append({
            "publisher": name,
            "n": len(papers),
            "resolved": len(hit),
            "share": round(100 * len(hit) / len(papers), 1),
            "median_days": statistics.median([p["days"] for p in hit]) if hit else None,
            "issuance_days": len({p["flag"] for p in papers}),
        })
    return sorted(out, key=lambda d: -d["n"])


# ---------------------------------------------------------------- report

def main():
    rw_path, cr_dir, out_dir = sys.argv[1], sys.argv[2], sys.argv[3].rstrip("/")

    papers, cutoff, raw_rows = load_retraction_watch(rw_path)
    cohort = mature(papers, cutoff)
    head = headline(cohort)
    head.update(bootstrap(cohort))
    curve = kaplan_meier(papers, cutoff)

    outcomes = collections.Counter(p["next_notice"] for p in papers)
    batches = collections.Counter(p["flag"] for p in papers)

    cr_papers = load_crossref(cr_dir, cutoff)
    cr_cohort = mature(cr_papers, cutoff)
    cr_head = headline(cr_cohort)
    cr_head.update(bootstrap(cr_cohort))

    # Where both corpora hold the same paper, do they agree about what happened?
    # Neither is a ground truth; the disagreement rate is the measurement.
    a_index = {p["doi"]: p for p in cohort}
    b_index = {p["doi"]: p for p in cr_cohort}
    overlap = set(a_index) & set(b_index)
    agree = collections.Counter()
    for doi in overlap:
        agree[(resolved(a_index[doi]), resolved(b_index[doi]))] += 1
    gap_days = [a_index[doi]["days"] - b_index[doi]["days"] for doi in overlap
                if resolved(a_index[doi]) and resolved(b_index[doi])]

    result = {
        "generated": dt.date.today().isoformat(),
        "follow_up_days": FOLLOW_UP_DAYS,
        "corpus_a": {
            "name": "Retraction Watch database, distributed by Crossref",
            "rows": raw_rows,
            "cutoff": cutoff.isoformat(),
            "papers_with_a_concern": len(papers),
            "headline": head,
            "notice_level": notice_level(cohort),
            "outcomes_whole_cohort": {
                (k or "nothing after the concern"): v for k, v in outcomes.most_common()
            },
            "largest_issuance_days": [[d.isoformat(), n] for d, n in batches.most_common(5)],
            "km": {
                "at_1y": round(100 * (1 - at_day(curve, 365)), 1),
                "at_2y": round(100 * (1 - at_day(curve, 731)), 1),
                "at_3y": round(100 * (1 - at_day(curve, 1096)), 1),
                "at_5y": round(100 * (1 - at_day(curve, 1826)), 1),
                "at_10y": round(100 * (1 - at_day(curve, 3653)), 1),
                "median_days": next((t for t, s in curve if s <= 0.5), None),
                "plateau": round(100 * (1 - curve[-1][1]), 1),
            },
            "by_publisher": by_publisher(cohort),
        },
        "corpus_b": {
            "name": "Crossref REST API notice records",
            "eoc_notices": sum(1 for _ in open(f"{cr_dir}/crossref-eoc.jsonl")),
            "retraction_notices": sum(1 for _ in open(f"{cr_dir}/crossref-retraction.jsonl")),
            "papers_with_a_concern": len(cr_papers),
            "headline": cr_head,
        },
        "agreement": {
            "papers_in_both_mature_cohorts": len(overlap),
            "both_say_resolved": agree[(True, True)],
            "both_say_unresolved": agree[(False, False)],
            "only_corpus_a_says_resolved": agree[(True, False)],
            "only_corpus_b_says_resolved": agree[(False, True)],
            "disagreement_share": round(
                100 * (agree[(True, False)] + agree[(False, True)]) / len(overlap), 1
            ) if overlap else None,
            "date_gap_days": {
                "n": len(gap_days),
                "identical": sum(1 for g in gap_days if g == 0),
                "within_31_days": sum(1 for g in gap_days if abs(g) <= 31),
                "median_abs": statistics.median([abs(g) for g in gap_days]) if gap_days else None,
                "max_abs": max((abs(g) for g in gap_days), default=None),
            },
        },
    }

    with open(f"{out_dir}/data.json", "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2, ensure_ascii=False)

    # the per-paper table the page's figure and any re-check are built from
    with open(f"{out_dir}/cohort.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["original_doi", "concern_date", "concern_notice_doi",
                    "publisher", "days_to_retraction", "resolved_within_5y",
                    "in_mature_cohort"])
        horizon = cutoff - dt.timedelta(days=FOLLOW_UP_DAYS)
        for p in sorted(papers, key=lambda p: p["flag"]):
            w.writerow([p["doi"], p["flag"].isoformat(), p["notice_doi"],
                        p["publisher"], p["days"] if p["days"] is not None else "",
                        int(resolved(p)), int(p["flag"] <= horizon)])

    with open(f"{out_dir}/survival.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["days", "share_still_under_concern"])
        for t, s in curve:
            w.writerow([t, round(s, 6)])

    print(json.dumps(result, indent=2)[:3000])


if __name__ == "__main__":
    main()
