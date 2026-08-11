#!/usr/bin/env python3
"""Independent check on the id->creation-time decoding.

The decoding (top 32 bits of the numeric video id = unix seconds) is a convention, not
something this practice can read off the platform. It is checked here against a source
the platform does not control: the date a human editor wrote into the citation template
that carries the link, in the wiki page's own wikitext.

Two checks:
  (1) ORDERING — the decoded creation time must not be after the cited date. A video
      cannot be cited before it exists. Violations are counted and listed.
  (2) TIGHTNESS — the distribution of (cited date - decoded creation). If the decoding
      were wrong, this would be scattered or negative.
"""
import json
import re
import time
import urllib.parse
import urllib.request
import datetime as dt

UA = "field-research/1.0 (independent research instrument; sequential)"
corpus = json.load(open("corpus-merged.json"))
rows = corpus["rows"]

# Only English Wikipedia rows, so one wiki's citation conventions are being read.
en = [r for r in rows.values() if r["wiki"] == "en.wikipedia.org"]
en.sort(key=lambda r: r["vid"])
pages = []
seen = set()
for r in en:
    if r["page"] not in seen:
        seen.add(r["page"])
        pages.append(r["page"])
pages = pages[:120]

DATE_KEYS = re.compile(r"\|\s*(date|access-date|accessdate)\s*=\s*([^|}\n]+)")


def parse_date(s):
    s = s.strip()
    for f in ("%d %B %Y", "%B %d, %Y", "%Y-%m-%d", "%d %b %Y", "%b %d, %Y"):
        try:
            return dt.datetime.strptime(s, f).replace(tzinfo=dt.timezone.utc)
        except ValueError:
            pass
    return None


out = []
for i in range(0, len(pages), 20):
    batch = pages[i:i + 20]
    p = {"action": "query", "prop": "revisions", "rvprop": "content", "rvslots": "main",
         "titles": "|".join(batch), "format": "json", "formatversion": "2"}
    url = "https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(p)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=90) as r:
        d = json.load(r)
    for pg in d.get("query", {}).get("pages", []):
        try:
            txt = pg["revisions"][0]["slots"]["main"]["content"]
        except Exception:
            continue
        # find each tiktok video url and the nearest citation dates in its template
        for m in re.finditer(r"tiktok\.com/@[^/\s|}\]]+/video/(\d+)", txt):
            vid = m.group(1)
            # Scope to the ENCLOSING template only: walk back to the nearest "{{" and
            # forward to the matching "}}". A ±N-character window picks up the dates of
            # neighbouring citations, which is how a first pass of this script produced
            # 47 spurious violations (recorded in DEVIATIONS.md D2).
            lo = txt.rfind("{{", 0, m.start())
            hi = txt.find("}}", m.end())
            if lo == -1 or hi == -1 or hi - lo > 1200:
                continue
            window = txt[lo:hi]
            if window.count("{{") != 1:      # nested/ambiguous template — skip, don't guess
                continue
            dates = [parse_date(v) for _k, v in DATE_KEYS.findall(window)]
            dates = [x for x in dates if x]
            if not dates:
                continue
            created = dt.datetime.fromtimestamp(int(vid) >> 32, dt.timezone.utc)
            out.append({"vid": vid, "page": pg.get("title"),
                        "created": created.isoformat(),
                        "cited_min": min(dates).isoformat(),
                        "delta_days": round((min(dates) - created).total_seconds() / 86400, 1)})
    time.sleep(1.0)

# ids whose decoded year is outside the platform's lifetime are reported separately:
# they are malformed/short ids, not evidence about the decoding.
bad_ids = [o for o in out if not (2016 <= int(o["created"][:4]) <= 2026)]
out = [o for o in out if 2016 <= int(o["created"][:4]) <= 2026]
viol = [o for o in out if o["delta_days"] < -1]
deltas = sorted(o["delta_days"] for o in out)
summary = {
    "pairs_checked": len(out),
    "violations_created_after_cited": len(viol),
    "delta_days_min": deltas[0] if deltas else None,
    "delta_days_median": deltas[len(deltas) // 2] if deltas else None,
    "delta_days_max": deltas[-1] if deltas else None,
    "within_2_years": sum(1 for d in deltas if 0 <= d <= 730),
    "delta_days_p10": deltas[len(deltas)//10] if deltas else None,
    "delta_days_p90": deltas[9*len(deltas)//10] if deltas else None,
    "out_of_lifetime_ids_excluded": len(bad_ids),
}
json.dump({"summary": summary, "violations": viol,
           "out_of_lifetime": bad_ids, "pairs": out},
          open("timestamp-validation.json", "w"), indent=1)
print(json.dumps(summary, indent=1))
