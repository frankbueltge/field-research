"""Study 38: write data-38.js for the page from data/results38.json. No computation beyond selecting; the 'read'
column is my reading of each Storm Events narrative, in my words (the narratives are in results38.json).
Corrected 2026-10-23 (session 226): McLoud's class and reading come from data/correction38.json (the office's
official Storm Data); results38.json stays as study 38 wrote it."""
import json, pathlib
HERE = pathlib.Path(__file__).resolve().parent
R = json.loads((HERE / "data/results38.json").read_text())
READ = {315890: "says nothing of injuries; the office's own page: 1 injured, the driver of a semi truck",
        613772: "five injured among about 20 damaged homes",
        614660: "four injuries",
        616002: "four occupants of a flipped mobile home",
        134: "homes damaged by falling trees; says nothing of injuries",
        579261: "four minor injuries at an apartment complex (and: damage “indicative of an EF1”, rated EF0)",
        299112: "three in one flipped mobile home",
        368708: "six dead in mobile homes; no count of the injured",
        613656: "a mobile home park; “at least 3” injured",
        85: "three in a truck a tree fell on",
        613559: "about 75 injured at an RV park; the tornado came out of Assumption Parish, peak EF3 there"}
C = json.loads((HERE / "data/correction38.json").read_text())
READ[315890] = (f"says nothing of injuries; the office's event page: 1 injured, a truck driver; the office's official "
                f"Storm Data (printed {C['source']['printed']}): {C['mcloud_315890']['injured']} injured (corrected 2026-10-23)")
CLS = {315890: "two accounts; the official one agrees"}
rows = [{"om": x["om"], "date": x["date"], "st": x["st"], "ef": x["spc"]["ef"], "spc": x["spc"]["inj"], "se": x["se_inj"],
         "cls": CLS.get(x["om"], x["class"]), "read": READ[x["om"]]} for x in R["records"]]
F = R["fits"]
out = {"rows": rows, "fits": {k: {"irr": v["irr"], "lo": v["lo"], "hi": v["hi"], "mu_la": v.get("mu_louisiana", F["mu_full"]["louisiana"])}
                                    for k, v in F.items() if k != "mu_full"}, "predictions": R["predictions"]}
(HERE / "data-38.js").write_text("window.S38=" + json.dumps(out, separators=(",", ":"), ensure_ascii=False) + ";\n")
print("data-38.js written", len(rows))
