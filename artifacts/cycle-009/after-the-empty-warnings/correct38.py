"""Study 38, a correction (session 226, 2026-10-23, answering the Atelier's handoffs ho-2026-10-22-atelier-6 and
ho-2026-10-23-atelier-1). Reads the Norman office's official Storm Data for May 2011 and asks which injured count it
gives McLoud (om 315890, Pottawatomie County, tornado D3) and Stillwater (om 315880, Payne County, B4). No refit: the
fits for 32 and 1 injured are already in data/results38.json.
Usage: python3 -I correct38.py <oun201105.pdf from weather.gov/media/oun/stormdata/>   (needs pdftotext; writes
data/correction38.json)"""
import json, sys, pathlib, hashlib, subprocess, re
HERE = pathlib.Path(__file__).resolve().parent
raw = open(sys.argv[1], "rb").read()
SHA = "bd5ef021a6f68ce079555cf38b79a4defe8faa48876c7d60856cddcb381d225f"   # as the Atelier's accounts.json names it
assert hashlib.sha256(raw).hexdigest() == SHA
txt = subprocess.run(["pdftotext", "-layout", sys.argv[1], "-"], capture_output=True, text=True, check=True).stdout
lines = txt.splitlines()
printed = sorted(set(re.findall(r"Printed on:\s+(\S+)", txt)))
assert printed == ["10/14/2011"], printed

def row(county_place, kind):
    """The injured count on the second line of the first tornado entry whose header names county_place."""
    i = next(k for k, l in enumerate(lines) if l.startswith(county_place) and "Tornado" in lines[k + 1])
    assert kind in lines[i + 1], lines[i + 1]
    m = re.search(r"CST\s+(\d+)\s+(\d+)\s+Source", lines[i + 2])   # injured, then crop damage
    return {"header": lines[i].strip(), "event": re.sub(r"\s+", " ", lines[i + 1]).strip(),
            "line": re.sub(r"\s+", " ", lines[i + 2]).strip(), "injured": int(m.group(1))}, i

mc, i = row("POTTAWATOMIE COUNTY --- 4.7 WSW DALE", "EF2, L: 2.00 mi")
assert lines[i + 4].startswith("Tornado D3 (McLoud tornado.)")
st, _ = row("PAYNE COUNTY --- 7.5 SSE LAKE CARL BLACKWELL DAM", "EF2, L: 10.40 mi")
narr = " ".join(l.strip() for l in lines[i + 4:i + 12] if l.strip())
narr = narr[:narr.index("Monetary damage estimates were not available.")]
R = json.loads((HERE / "data/results38.json").read_text())
rec = next(r for r in R["records"] if r["om"] == 315890)
same = re.sub(r"\s+", " ", rec["narrative"]).strip().startswith(narr.strip())
F = R["fits"]
out = {"date": "2026-10-23", "session": 226,
       "answers": ["ho-2026-10-22-atelier-6", "ho-2026-10-23-atelier-1"],
       "source": {"url": "https://www.weather.gov/media/oun/stormdata/oun201105.pdf", "sha256": SHA,
                  "fetched": "2026-10-23", "printed": printed[0], "not_committed": True},
       "mcloud_315890": mc, "stillwater_315880": st,
       "storm_data_narrative_same_as_storm_events": same,
       "verdict": "The office's official Storm Data gives McLoud 32 injured, as the database does; its event page's 1 is a "
                  "second account by the same office. Study 38's class 'contradicted' is corrected to 'two accounts; the "
                  "official one agrees'. The headline reading moves from both corrections (McLoud at 1, Louisiana as one "
                  "track) to Louisiana alone.",
       "headline_before": F["both"], "headline_after": F["louisiana_one_track"]}
assert mc["injured"] == 32 and st["injured"] == 18 and same
(HERE / "data/correction38.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
print("McLoud", mc["injured"], "| Stillwater", st["injured"], "| narrative same:", same,
      "| headline", F["both"]["irr"], "->", F["louisiana_one_track"]["irr"])
