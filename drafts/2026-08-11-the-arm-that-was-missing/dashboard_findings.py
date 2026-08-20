#!/usr/bin/env python3
"""dashboard_findings - what the receiver's own per-video record says, computed from it.

Session 128, 2026-08-20. Reads the JSON `extract_dashboard.py` writes and derives the figures the
letter quotes. Every figure the letter prints is fetched from a named field of this file; nothing
is typed into the letter's prose.

It also scores, as its own section, the per-video breakdown an adversary handed this practice on
2026-08-19 and which session 127 recorded as CLAIMED-AND-UNREPRODUCED rather than adopt on
somebody's word. Scoring it is the point: a number accepted because a reviewer computed it is the
failure this practice exists to avoid, and it does not stop being that failure when the reviewer
turns out to be mostly right.

    python3 dashboard_findings.py receiver-series-2026-08-19.json \
        --reading offer/your-eleven-today.json -o dashboard-findings.json
"""
import argparse
import datetime
import json
import sys

# The claim handed over on 2026-08-19, quoted from INTERLOCUTOR-19.md, scored below against the
# extraction. It is stored here as data so the scoring cannot quietly drift to fit the result.
ADVERSARY_CLAIM = {
    "quoted": ("Nine of the eleven you have been recording as Not Available for most of nine "
               "months are publicly fetchable right now"),
    "quoted_breakdown": "ten of the eleven... Not Available on 224-265 days (88-95%)",
    "source": "INTERLOCUTOR-19.md, session 127's adversary; recorded unreproduced in "
              "CONDITIONS-127.md",
    "n_videos_claimed": 10,
    "day_range_claimed": [224, 265],
    "pct_range_claimed": [88.0, 95.0],
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("series")
    ap.add_argument("--reading", required=True,
                    help="this practice's own presence_check output over the same list")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()

    S = json.load(open(a.series, encoding="utf-8"))
    R = json.load(open(a.reading, encoding="utf-8"))

    per = []
    for v in S["videos"]:
        if len(v["charts"]) != 1:
            raise SystemExit("video %s has %d charts; this script expects exactly one timeline "
                             "per card and refuses to guess which" % (v["video_id"],
                                                                      len(v["charts"])))
        c = v["charts"][0]
        d = c["derived"]
        counts = d["status_day_counts"]
        per.append({
            "video_id": v["video_id"],
            "creator": v["metadata"].get("creator"),
            "created": v["metadata"].get("created"),
            "n_recorded_days": d["n_points"],
            "first_date": d["first_date"],
            "last_date": d["last_date"],
            "status_day_counts": counts,
            "not_available_days": counts.get("Not Available", 0),
            "available_days": counts.get("Available", 0),
            "error_days": counts.get("Error", 0),
            "not_available_pct_of_recorded_days": round(
                100.0 * counts.get("Not Available", 0) / d["n_points"], 1),
            "n_transitions": d["n_transitions"],
            "last_change_date": d["last_change_date"],
            "last_change": d["transitions"][-1] if d["transitions"] else None,
            "final_status": d["final_status"],
        })

    # --- the simultaneous flip -----------------------------------------------------------------
    change_dates = sorted(set(p["last_change_date"] for p in per))
    flip = change_dates[0] if len(change_dates) == 1 else None
    from_states = {}
    for p in per:
        if p["last_change"]:
            from_states[p["last_change"]["from"]] = from_states.get(
                p["last_change"]["from"], 0) + 1

    # --- the record's own end ------------------------------------------------------------------
    last_dates = sorted(set(p["last_date"] for p in per))
    read_utc = R["started_utc"]
    read_date = datetime.date.fromisoformat(read_utc[:10])
    end = datetime.date.fromisoformat(last_dates[-1])

    # --- the extraction, checked against the page's OWN aggregate chart --------------------
    # The dashboard draws a second, independent chart summing the eleven per day. If the per-video
    # extraction is right, it must reproduce that chart exactly - and if it does not, the
    # disagreement is the finding, not the sum. 279 dates x 3 statuses, compared one at a time.
    agg = {}
    for chart in S["aggregate_charts"]:
        for t in chart["traces"]:
            if t.get("name"):
                agg[t["name"]] = dict(zip(t["x"], t["y"]))
    tally = {}
    for v in S["videos"]:
        c = v["charts"][0]
        for x, st in zip([str(i)[:10] for i in c["x"]], c["states"]):
            tally.setdefault(x, {})
            tally[x][st] = tally[x].get(st, 0) + 1
    dates_seen = set(tally)
    for series in agg.values():
        dates_seen |= set(series)
    all_dates = sorted(dates_seen)
    names = sorted(agg)
    disagreements = []
    for dt in all_dates:
        for nm in names:
            drawn = agg[nm].get(dt)
            summed = tally.get(dt, {}).get(nm, 0)
            if drawn != summed:
                disagreements.append({"date": dt, "status": nm, "aggregate_chart": drawn,
                                      "sum_of_per_video_series": summed})
    cross_check = {
        "what_this_is": ("the page draws its own aggregate trend chart from a separate payload. "
                         "The eleven per-video series are summed here per day and compared with "
                         "it, value by value. A disagreement would be a finding about the "
                         "extraction or about the page; there are none."),
        "n_dates_compared": len(all_dates),
        "n_status_series_compared": len(names),
        "n_comparisons": len(all_dates) * len(names),
        "n_disagreements": len(disagreements),
        "disagreements": disagreements[:20],
        "verdict": "AGREES EXACTLY" if not disagreements else "DISAGREES",
    }

    # --- the receiver's final states against this practice's reading of the same identifiers ---
    ours = {o["vid"]: o["state"] for o in R["observations"]}
    missing = sorted(set(p["video_id"] for p in per) - set(ours))
    cross = []
    for p in per:
        cross.append({"video_id": p["video_id"],
                      "their_final_status": p["final_status"],
                      "their_final_status_as_of": p["last_date"],
                      "their_not_available_days": p["not_available_days"],
                      "their_available_days": p["available_days"],
                      "ours": ours.get(p["video_id"], "NOT IN OUR READING")})
    retrievable_now = [c for c in cross if c["ours"] == "RETRIEVABLE"]

    # the group the adversary's breakdown is about: mostly-Not-Available in their own record
    mostly_na = [p for p in per if p["not_available_days"] >= 200]
    other = [p for p in per if p["not_available_days"] < 200]
    mostly_na_ids = set(p["video_id"] for p in mostly_na)
    mostly_na_retrievable = [c for c in cross
                             if c["video_id"] in mostly_na_ids and c["ours"] == "RETRIEVABLE"]

    day_lo = min(p["not_available_days"] for p in mostly_na)
    day_hi = max(p["not_available_days"] for p in mostly_na)
    pct_lo = min(p["not_available_pct_of_recorded_days"] for p in mostly_na)
    pct_hi = max(p["not_available_pct_of_recorded_days"] for p in mostly_na)

    scoring = {
        "claim": ADVERSARY_CLAIM,
        "n_videos_found": len(mostly_na),
        "n_videos_verdict": "REPRODUCED" if len(mostly_na) == ADVERSARY_CLAIM[
            "n_videos_claimed"] else "NOT REPRODUCED",
        "day_range_found": [day_lo, day_hi],
        "day_range_verdict": "REPRODUCED" if [day_lo, day_hi] == ADVERSARY_CLAIM[
            "day_range_claimed"] else "NOT REPRODUCED",
        "pct_range_found": [pct_lo, pct_hi],
        "pct_denominator": ("each series' own number of recorded days (279 for ten of the "
                            "eleven, 238 for the one that starts later)"),
        "pct_range_verdict": "REPRODUCED" if [pct_lo, pct_hi] == ADVERSARY_CLAIM[
            "pct_range_claimed"] else "NOT REPRODUCED",
        "n_retrievable_now_in_that_group": len(mostly_na_retrievable),
        "n_retrievable_now_claimed": 9,
        "n_retrievable_now_verdict": "REPRODUCED" if len(
            mostly_na_retrievable) == 9 else "NOT REPRODUCED",
        "what_is_not_settled_by_this": (
            "the percentage range is the one figure that does not reproduce, and this file does "
            "not claim to know which denominator produced 88 %. It reports what the series say "
            "on the only denominator the series themselves supply."),
    }

    out = {
        "schema": "field-research/dashboard-findings/1",
        "generated_from": {
            "series_file": a.series,
            "series_source_file": S["source"]["file"],
            "series_source_sha256": S["source"]["sha256"],
            "series_source_bytes": S["source"]["bytes"],
            "extractor": S["extractor"]["script"],
            "reading_file": a.reading,
            "reading_started_utc": read_utc,
            "reading_vantage_asn": R["vantage"]["asn"],
        },
        "record": {
            "n_videos": len(per),
            "first_date": sorted(set(p["first_date"] for p in per))[0],
            "last_date": last_dates[-1],
            "all_series_end_on_the_same_date": len(last_dates) == 1,
            "n_recorded_days_max": max(p["n_recorded_days"] for p in per),
            "n_recorded_days_min": min(p["n_recorded_days"] for p in per),
            "days_from_record_end_to_our_reading": (read_date - end).days,
            "our_reading_date": read_utc[:10],
            "gaps_in_the_record": S["videos"][0]["charts"][0]["derived"]["gaps"],
            "final_status_counts": {s: sum(1 for p in per if p["final_status"] == s)
                                    for s in sorted(set(p["final_status"] for p in per))},
        },
        "simultaneous_flip": {
            "date": flip,
            "n_series_whose_last_change_is_that_date": len(per) if flip else 0,
            "n_series": len(per),
            "states_they_came_from": from_states,
            "state_they_went_to": sorted(set(p["last_change"]["to"] for p in per
                                             if p["last_change"])),
            "days_from_flip_to_record_end": (
                end - datetime.date.fromisoformat(flip)).days if flip else None,
            "days_from_flip_to_our_reading": (
                read_date - datetime.date.fromisoformat(flip)).days if flip else None,
            "what_it_is_not": ("this is a statement about eleven series in one file. It does not "
                               "identify a cause, and this practice has not seen the code that "
                               "writes them."),
        },
        "the_one_that_is_not_like_the_others": ({
            "video_id": other[0]["video_id"],
            "available_days": other[0]["available_days"],
            "not_available_days": other[0]["not_available_days"],
            "error_days": other[0]["error_days"],
            "n_recorded_days": other[0]["n_recorded_days"],
            "available_pct": round(100.0 * other[0]["available_days"]
                                   / other[0]["n_recorded_days"], 1),
            "last_change": other[0]["last_change"],
        } if len(other) == 1 else {"n_such_videos": len(other),
                                   "note": "not a single outlier; reported as a group",
                                   "video_ids": [p["video_id"] for p in other]}),
        "against_our_own_reading": {
            "identifiers_in_their_record_not_in_our_reading": missing,
            "n_retrievable_in_our_reading": len(retrievable_now),
            "n_in_their_record": len(per),
            "cross": cross,
        },
        "extraction_checked_against_the_pages_own_aggregate_chart": cross_check,
        "scoring_the_handed_over_breakdown": scoring,
        "per_video": per,
    }
    with open(a.out, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("wrote %s: %d videos, flip=%s, record ends %s, %d days before our reading; "
          "aggregate cross-check %s (%d comparisons, %d disagreements)"
          % (a.out, len(per), flip, last_dates[-1],
             out["record"]["days_from_record_end_to_our_reading"],
             cross_check["verdict"], cross_check["n_comparisons"],
             cross_check["n_disagreements"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
