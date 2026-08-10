#!/usr/bin/env python3
"""Reproducing the adversary's two decisive charges before accepting them (session 106).

C-I  — is 116,317 the wrong counterfactual? Sum the byte sizes the index itself declares
       for the 75 absent cycles, against the 21 served ones, and calibrate bytes->events
       on files of comparable declared size elsewhere in the series.
C-II — is the demonstration day free from the index alone? Run this practice's OWN screen
       (rolling median over +/-192 cycles, ratio < 0.20) and take run lengths.
"""
import urllib.request, json, re, statistics, io, zipfile, time

UA = {"User-Agent": "field-research-census/1"}
def get(u, timeout=600):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=timeout).read()

t0 = time.time()
raw = get("http://data.gdeltproject.org/gdeltv2/masterfilelist.txt")
print("master list", len(raw), "bytes in", round(time.time()-t0, 1), "s")

export = []          # (cycle, declared_bytes, url) in listed order, export only
for line in raw.decode("utf-8", "replace").splitlines():
    p = line.split()
    if len(p) != 3: continue
    m = re.search(r"/(\d{14})\.export\.CSV\.zip$", p[2])
    if m: export.append((m.group(1), int(p[0]), p[2]))
print("listed export cycles:", len(export))

reg = json.load(open("/home/user/field-research/drafts/2026-08-08-the-hours-it-was-not-looking/availability-register-v1.0.json"))
absent = {r["cycle"] for r in reg["rows"]
          if r["cycle"].startswith("20221111")
          and r["series"].get("English/export", {}).get("verdict") == "absent"}

day = [(c, b, u) for c, b, u in export if c.startswith("20221111")]
abs_rows = [(c, b) for c, b, _ in day if c in absent]
srv_rows = [(c, b) for c, b, _ in day if c not in absent]
sum_abs = sum(b for _, b in abs_rows); sum_srv = sum(b for _, b in srv_rows)
print(f"C-I: 2022-11-11 export — absent {len(abs_rows)} cycles, declared {sum_abs:,} bytes;"
      f" served {len(srv_rows)} cycles, declared {sum_srv:,} bytes")

# --- calibration: files elsewhere in the series with declared size in the absent band ---
lo, hi = min(b for _, b in abs_rows), max(b for _, b in abs_rows)
band = [(c, b, u) for c, b, u in export
        if lo <= b <= hi and not c.startswith("202211")]
step = max(1, len(band)//25)
sample = band[::step][:25]
cal = []
for c, b, u in sample:
    try:
        blob = get(u, timeout=120)
    except Exception as e:
        cal.append({"cycle": c, "declared": b, "error": str(e)}); continue
    with zipfile.ZipFile(io.BytesIO(blob)) as z:
        n = sum(1 for _ in z.open(z.namelist()[0]))
    cal.append({"cycle": c, "declared": b, "served": len(blob), "events": n,
                "bytes_per_event": round(b/n, 1) if n else None})
ok = [r for r in cal if r.get("events")]
bpe = sorted(r["bytes_per_event"] for r in ok)
med_bpe = statistics.median(bpe)
print(f"C-I calibration: {len(ok)} files in the {lo}-{hi} byte band, "
      f"median {med_bpe} declared bytes/event, range {bpe[0]}-{bpe[-1]}")
est_missing = sum_abs / med_bpe
print(f"C-I estimate: the 75 absent export files held on the order of {est_missing:,.0f} events")

# --- C-II: this practice's own screen, index only ---
t1 = time.time()
sizes = [b for _, b, _ in export]
W = 192
flagged = []
for i, (c, b, _) in enumerate(export):
    lo_i, hi_i = max(0, i-W), min(len(export), i+W+1)
    med = statistics.median(sizes[lo_i:hi_i])
    if med and b/med < 0.20:
        flagged.append(i)
runs, cur = [], []
for i in flagged:
    if cur and i == cur[-1] + 1: cur.append(i)
    else:
        if cur: runs.append(cur)
        cur = [i]
if cur: runs.append(cur)
runs.sort(key=len, reverse=True)
top = [{"length": len(r), "from": export[r[0]][0], "to": export[r[-1]][0]} for r in runs[:4]]
secs = round(time.time()-t1, 2)
print(f"C-II: {len(flagged)} flagged of {len(export)}; longest runs {json.dumps(top)}; screen took {secs}s")

json.dump({"checked_utc_date": "2026-08-10",
           "C_I": {"absent_cycles": len(abs_rows), "declared_bytes_absent": sum_abs,
                   "served_cycles": len(srv_rows), "declared_bytes_served": sum_srv,
                   "calibration_band": [lo, hi], "calibration_files": len(ok),
                   "median_declared_bytes_per_event": med_bpe,
                   "bytes_per_event_range": [bpe[0], bpe[-1]],
                   "estimated_events_in_the_absent_files": round(est_missing),
                   "calibration": cal},
           "C_II": {"flagged": len(flagged), "of": len(export), "longest_runs": top,
                    "screen_seconds": secs,
                    "note": "rolling median over +/-192 listed export cycles, ratio < 0.20 — this practice's own screen.py heuristic"}},
          open("reproduce-refutation.json", "w"), indent=1)
