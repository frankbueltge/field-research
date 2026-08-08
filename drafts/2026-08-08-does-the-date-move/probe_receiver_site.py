"""UNREGISTERED EXPLORATORY PROBE — not part of PREREGISTRATION-2.md and not scored against it.

The receiver of this investigation is the body publishing the draft federal standard whose
acceptance criterion says: "Update the date if the content changes substantively."
(https://standards.digital.gov/standards/content-timeliness-indicator/.)

This probe asks the smallest fair question about that site: on its own pages, what do the three
signals say — H, the HTTP `Last-Modified` a machine receives; S, the `<lastmod>` the site publishes
in its own sitemap; V, the date printed for a human? It is a live measurement of the site as it
stands today, not a claim about anyone's compliance over time, and it fetches each page once.

The V extractor and the HTTP-date parsing are reused UNMODIFIED from this house's earlier line
(`drafts/2026-08-06-as-of-today/collect_signals.py`), including its known limits: it is a pattern
match over visible text, its referent is not established outside one authority, and increment 1's
D2 showed such matches can read a future date that is not a currency statement at all. The D2
future-date test is therefore applied here as a filter and reported.
"""
import json, re, sys, time, datetime as dt
import urllib.request

sys.path.insert(0, "/home/user/field-research/drafts/2026-08-06-as-of-today")
from collect_signals import extract_v, normalise_v, parse_http_date  # noqa: E402

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
SITEMAP = "https://standards.digital.gov/sitemap.xml"


def get(u, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(u, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.status, r.read().decode("utf-8", "replace"), \
                    {k.lower(): v for k, v in r.headers.items()}
        except Exception as e:  # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise last


_, sm, _ = get(SITEMAP)
entries = re.findall(r"<url>\s*<loc>([^<]+)</loc>\s*(?:<lastmod>([^<]*)</lastmod>)?", sm)
today = dt.date.today().isoformat()

out = []
for i, (loc, lastmod) in enumerate(entries, 1):
    rec = {"url": loc, "S_sitemap_lastmod": lastmod or None}
    try:
        st, page, hdr = get(loc)
        rec["status"] = st
        rec["H_last_modified_raw"] = hdr.get("last-modified")
        rec["H_last_modified"] = parse_http_date(hdr.get("last-modified"))
        v = extract_v(page)
        rec["V_raw"] = v.get("v_raw")
        rec["V"] = (normalise_v(v.get("v_raw")) or "")[:10] or None
        rec["V_rule"] = v.get("v_rule")
        rec["V_context"] = v.get("v_context")
        rec["V_in_future"] = bool(rec["V"] and rec["V"] > today)   # D2 test, one comparison
    except Exception as e:  # noqa: BLE001
        rec["error"] = f"{type(e).__name__}: {e}"
    out.append(rec)
    print(f"[{i}/{len(entries)}] S={rec.get('S_sitemap_lastmod')} H={rec.get('H_last_modified')} "
          f"V={rec.get('V')} {loc}", flush=True)
    time.sleep(0.8)

ok = [r for r in out if "error" not in r]
summary = {
    "fetched_utc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "pages_in_sitemap": len(entries), "fetched": len(ok), "errors": len(out) - len(ok),
    "S_present": sum(1 for r in ok if r["S_sitemap_lastmod"]),
    "H_present": sum(1 for r in ok if r.get("H_last_modified")),
    "V_present": sum(1 for r in ok if r.get("V")),
    "V_in_future": sum(1 for r in ok if r.get("V_in_future")),
    "S_equals_V": sum(1 for r in ok if r.get("V") and r["S_sitemap_lastmod"]
                      and r["S_sitemap_lastmod"][:10] == r["V"]),
    "distinct_H_values": len({r.get("H_last_modified") for r in ok if r.get("H_last_modified")}),
}
json.dump({"summary": summary, "records": out},
          open(f"{BASE}/receiver-site-probe.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
