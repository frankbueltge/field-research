#!/usr/bin/env python3
"""Independent re-probe of the demonstration day, dated 2026-08-10.

The register the demonstration is scored against is dated 2026-08-09. This asks the host
again, today, about all 96 English export cycles of 2022-11-11 and of the control day, so
the executed result rests on a same-day measurement rather than on yesterday's.
"""
import json, http.client, urllib.parse, concurrent.futures as cf

HOST = "data.gdeltproject.org"
def probe(cycle, suffix=".export.CSV.zip"):
    path = f"/gdeltv2/{cycle}{suffix}"
    c = http.client.HTTPConnection(HOST, timeout=30)
    try:
        c.request("HEAD", path, headers={"User-Agent": "field-research-census/1"})
        r = c.getresponse(); r.read()
        return cycle, r.status, r.getheader("Content-Length")
    finally:
        c.close()

out = {}
for day in ("20221111", "20221109"):
    grid = [f"{day}{h:02d}{m:02d}00" for h in range(24) for m in (0, 15, 30, 45)]
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        res = list(ex.map(probe, grid))
    served = [c for c, s, _ in res if s == 200]
    absent = [c for c, s, _ in res if s == 404]
    other = [(c, s) for c, s, _ in res if s not in (200, 404)]
    out[day] = {"probed": len(res), "served": len(served), "absent": len(absent),
                "other": other, "served_cycles": served}
    print(day, "served", len(served), "absent", len(absent), "other", other, flush=True)

reg = json.load(open("/home/user/field-research/drafts/2026-08-08-the-hours-it-was-not-looking/availability-register-v1.0.json"))
absent_reg = {r["cycle"] for r in reg["rows"]
              if r["cycle"].startswith("20221111")
              and r["series"].get("English/export", {}).get("verdict") == "absent"}
grid11 = [f"20221111{h:02d}{m:02d}00" for h in range(24) for m in (0, 15, 30, 45)]
out["agreement_with_register_2026_08_09"] = {
    "register_absent": len(absent_reg),
    "today_absent": 96 - out["20221111"]["served"],
    "identical_sets": sorted(c for c in grid11 if c not in absent_reg) == sorted(out["20221111"]["served_cycles"]),
}
out["probed_utc_date"] = "2026-08-10"
json.dump(out, open("reprobe-2026-08-10.json", "w"), indent=1)
print(json.dumps(out["agreement_with_register_2026_08_09"], indent=1))
