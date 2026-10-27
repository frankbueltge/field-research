"""Score PREDICTIONS.md H1-H4 from cases.json and readings.json. Usage: python3 -I score.py > results.json"""
import collections, json
cases = json.load(open("cases.json"))
read = json.load(open("readings.json"))["cases"]
conf = [c for c in read if c["status"].startswith("confirmed")]
others = [c for c in conf if (c["analysis"], c["country"]) != ("Sep 2025", "SDN")]
SUDAN = {"volatility": "A", "lack of data": "B"}
breaks = [dict(analysis=c["analysis"], country=c["country"], **a) for c in others for a in c["areas"]
          if a["reason"] in SUDAN and a["encoding"] != SUDAN[a["reason"]]]
exact = [c for c in others if {(a["reason"], a["encoding"]) for a in c["areas"]} >= {("volatility", "A"), ("lack of data", "B")}]
reasons = collections.Counter(a["reason"] for c in others for a in c["areas"])
by_reason = collections.defaultdict(set)
for c in conf:
    for a in c["areas"]:
        by_reason[a["reason"]].add(a["encoding"])
h1 = cases["single_encoding"] / cases["cases"]
out = dict(
    H1=dict(single=cases["single_encoding"], of=cases["cases"], share=round(h1, 3), bar=0.8, held=h1 >= 0.8),
    H2=dict(breaks=len(breaks), rows=breaks, held=len(breaks) >= 1),
    H3=dict(exact_reproductions=len(exact), held=len(exact) == 0),
    H4=dict(reasons=reasons.most_common(), held=reasons.most_common(1)[0][0] == "lack of data"
            and (len(reasons) == 1 or reasons.most_common(2)[1][1] < reasons.most_common(1)[0][1])),
    encodings_by_reason={k: sorted(v) for k, v in by_reason.items()},
    confirmed_analyses=len(conf), unconfirmed=[f'{c["analysis"]} {c["country"]}' for c in read if c not in conf])
json.dump(out, open("/dev/stdout", "w"), indent=1)
