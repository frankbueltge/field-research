"""Feasibility probe (NOT a scored run): is capture history usable for this question?
Writes probe-cdx.json. Declared as a probe in the journal before any pre-registration."""
import json, time, urllib.request, urllib.parse, sys

UA = "field-research-probe/1.0 (research; contact via repository)"
def get(url, timeout=60):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.status, r.read(), dict(r.headers)

def cdx(url, frm="20230101", to="20260808"):
    q = urllib.parse.urlencode({
        "url": url, "output": "json",
        "fl": "timestamp,digest,statuscode,mimetype,length",
        "from": frm, "to": to, "filter": "statuscode:200", "limit": "5000",
    })
    st, body, _ = get("https://web.archive.org/cdx/search/cdx?" + q)
    if st != 200 or not body.strip():
        return st, []
    rows = json.loads(body)
    return st, rows[1:] if rows else []

sigs = json.load(open("/home/user/field-research/drafts/2026-08-06-as-of-today/signals.json"))
sig2 = json.load(open("/home/user/field-research/drafts/2026-08-06-as-of-today/signals-2.json"))
pop = [("EC", r["url"]) for r in sigs["rows"] if r.get("v")][:3]
for a in ("NIST", "GOVUK", "IE"):
    pop += [(a, r["url"]) for r in sig2["authorities"][a]["rows"] if r.get("v")][:3]

out = []
for auth, url in pop:
    try:
        st, rows = cdx(url)
        digs = [r[1] for r in rows]
        distinct = len(set(digs))
        # count adjacent digest transitions in time order
        trans = sum(1 for i in range(1, len(digs)) if digs[i] != digs[i-1])
        out.append({"authority": auth, "url": url, "cdx_status": st,
                    "captures_200": len(rows), "distinct_digests": distinct,
                    "adjacent_transitions": trans,
                    "first": rows[0][0] if rows else None,
                    "last": rows[-1][0] if rows else None})
        print(auth, len(rows), distinct, trans, url[:70], flush=True)
    except Exception as e:
        out.append({"authority": auth, "url": url, "error": repr(e)})
        print("ERR", auth, url[:60], e, flush=True)
    time.sleep(2)

json.dump({"probe": "cdx-feasibility", "window": "20230101-20260808", "rows": out},
          open("/home/user/field-research/drafts/2026-08-08-does-the-date-move/probe-cdx.json", "w"), indent=1)
