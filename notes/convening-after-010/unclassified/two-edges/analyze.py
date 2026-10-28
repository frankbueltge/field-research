"""Two-edged absences in the IPC's national table (answers the Studio's case of 2026-10-28, bulletin s209).

Usage: python3 -I analyze.py ipc_global_area_long.csv ipc_global_national_long.csv > results.json
Definitions and predictions: PREDICTIONS.md (fixed before this script was written or run).
"""
import csv, collections, json, sys

area_csv, nat_csv = sys.argv[1], sys.argv[2]
CH = {"NGA", "GHA", "BEN", "BFA", "MLI", "NER", "TCD", "SEN", "MRT", "GIN", "SLE", "LBR", "TGO", "CIV",
      "GMB", "GNB", "CPV", "CMR"}
PH = ["1", "2", "3", "4", "5"]

def num(s):
    return int(round(float(s))) if s not in ("", None) else None

nat = collections.defaultdict(dict)
for r in csv.DictReader(open(nat_csv, newline="")):
    nat[(r["Date of analysis"], r["Country"], r["Validity period"])][r["Phase"]] = num(r["Number"])

area = collections.defaultdict(lambda: collections.defaultdict(dict))
for r in csv.DictReader(open(area_csv, newline="")):
    k = (r["Date of analysis"], r["Country"], r["Validity period"])
    area[k][(r["Level 1"], r["Area"])][r["Phase"]] = num(r["Number"])  # duplicates: last kept, as in s234

rows, gaps = [], []
for k, v in sorted(nat.items()):
    if v.get("all") is None or any(v.get(p) is None for p in PH):
        continue
    s = sum(v[p] for p in PH)
    gap = s - v["all"]
    counts = abs(gap) > max(1000, 0.005 * v["all"])
    rows.append(k)
    if not counts:
        continue
    areas = area.get(k, {})
    a_all = sum((a.get("all") or 0) for a in areas.values())
    a_ph = sum(sum((a.get(p) or 0) for p in PH) for a in areas.values())
    # E5 branch 1: areas with phase people but an `all` of 0 or missing
    hollow = [(l1, n, sum((a.get(p) or 0) for p in PH)) for (l1, n), a in areas.items()
              if sum((a.get(p) or 0) for p in PH) > 0 and not a.get("all")]
    hollow_sum = sum(x[2] for x in hollow)
    # PREDICTIONS.md says "within 1 % or 1,000 people". Read as the looser of the two (as first run), 1 % of
    # 47 million is 471,600, wider than the 330,000 under test: a vacuous bar. The strict reading (the tighter
    # of the two) is scored beside it and is the one reported (README.md, "A bad test").
    tol = lambda x, y: abs(x - y) <= max(1000, 0.01 * abs(y))
    tol_s = lambda x, y: abs(x - y) <= min(1000, 0.01 * abs(y))
    gaps.append(dict(date=k[0], country=k[1], period=k[2], ch=k[1] in CH,
                     national_all=v["all"], national_p5=v["5"], phase_sum=s, gap=gap,
                     kind="two-edged" if gap > 0 else "one-edged",
                     area_rows=len(areas), area_all_sum=a_all, area_phase_sum=a_ph,
                     hollow_areas=[f"{l1} / {n}" for l1, n, _ in hollow], hollow_sum=hollow_sum,
                     e5_hollow=bool(hollow) and tol(hollow_sum, gap),
                     e5_area_all=bool(areas) and tol(a_all, v["all"]),
                     e5_hollow_strict=bool(hollow) and tol_s(hollow_sum, gap),
                     e5_area_all_strict=bool(areas) and tol_s(a_all, v["all"]),
                     national_all_minus_area_all=v["all"] - a_all,
                     area_phases_match_national_phases=bool(areas) and tol(a_ph, s)))

def tally(sel):
    two = [g for g in sel if g["kind"] == "two-edged"]
    return dict(gaps=len(sel), two_edged=len(two), one_edged=len(sel) - len(two),
                two_edged_explained=sum(1 for g in two if g["e5_hollow"] or g["e5_area_all"]))

# The Studio's two areas, read from the area table: classified in the first projection, with phases, and
# the amount by which the national population falls short of the area table's population.
k = ("Sep 2025", "SDN", "first projection")
sudan_areas = [dict(level1=l1, area=n, all=a["all"], p5=a["5"], p4=a["4"]) for (l1, n), a in area[k].items()
               if n in ("Al Fasher Urban", "Kadugli Urban")]

sudan = [g for g in gaps if (g["date"], g["country"], g["period"]) == ("Sep 2025", "SDN", "first projection")]
out = dict(
    national_rows=len(rows),
    national_rows_non_ch=sum(1 for k in rows if k[1] not in CH),
    all=tally(gaps), non_ch=tally([g for g in gaps if not g["ch"]]), ch=tally([g for g in gaps if g["ch"]]),
    sudan_sep2025_first=sudan,
    scores=dict(
        E1=bool(sudan) and abs(sudan[0]["gap"] - 330000) <= 1000,
        E2=len(gaps) <= 0.05 * len(rows),
        E3=sum(1 for g in gaps if g["kind"] == "two-edged") < len(gaps) / 2,
        E4=sum(1 for g in gaps if g["kind"] == "two-edged" and g not in sudan) >= 1,
        E5=(lambda two: bool(two) and sum(1 for g in two if g["e5_hollow"] or g["e5_area_all"]) >= len(two) / 2)(
            [g for g in gaps if g["kind"] == "two-edged"]),
        E5_strict=(lambda two: bool(two) and sum(1 for g in two if g["e5_hollow_strict"] or g["e5_area_all_strict"]) >= len(two) / 2)(
            [g for g in gaps if g["kind"] == "two-edged"])),
    sudan_areas_outside=sudan_areas,
    strip=[[k[1], k[0], k[2], round((sum(nat[k][p] for p in PH) - nat[k]["all"]) / nat[k]["all"], 5) if nat[k]["all"] else None]
           for k in rows],
    gaps=gaps)
json.dump(out, sys.stdout, indent=1)
