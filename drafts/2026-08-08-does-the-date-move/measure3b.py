"""Increment 3B — executes PREREGISTRATION-3B.md exactly. Writes observations-3b.json.

One live fetch per document page. Per page: the printed update date by the per-authority
selector fixed in the pre-registration, plus the page's own published/created date. No archive.
"""
import json, re, sys, time, gzip, zlib, datetime as dt
import urllib.request

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
DELAY = 0.7
MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December")

NIST_V = re.compile(rf"Created\s+((?:{MONTHS})\s+\d{{1,2}},\s*\d{{4}})\s*,\s*Updated\s+((?:{MONTHS})\s+\d{{1,2}},\s*\d{{4}})")
EPA_V = re.compile(r"Last updated on\s+([^<\n]{4,40}?)\s*(?:<|$)")
EPA_PUB = re.compile(r'<time[^>]*datetime="(\d{4})-(\d{2})-(\d{2})')
GOVUK_CHANGE = re.compile(r'class="[^"]*gem-c-published-dates__change-date[^"]*"[^>]*datetime="([^"]+)"')
GOVUK_PUB = re.compile(rf"Published\s+(\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}})")
MONTH_N = {m: i + 1 for i, m in enumerate(MONTHS.split("|"))}


def iso(s):
    """'November 10, 2018' | '9 June 2026' | '2026-07-27T…' -> 'YYYY-MM-DD' or None."""
    if not s:
        return None
    s = s.strip()
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.match(rf"({MONTHS})\s+(\d{{1,2}}),\s*(\d{{4}})", s)
    if m:
        return f"{int(m.group(3)):04d}-{MONTH_N[m.group(1)]:02d}-{int(m.group(2)):02d}"
    m = re.match(rf"(\d{{1,2}})\s+({MONTHS})\s+(\d{{4}})", s)
    if m:
        return f"{int(m.group(3)):04d}-{MONTH_N[m.group(2)]:02d}-{int(m.group(1)):02d}"
    return None


def decode_body(raw, enc):
    if raw[:2] == b"\x1f\x8b":
        try:
            return gzip.decompress(raw)
        except Exception:                                # noqa: BLE001
            return raw
    if enc and "deflate" in enc.lower():
        for w in (-15, 15):
            try:
                return zlib.decompress(raw, w)
            except Exception:                            # noqa: BLE001
                continue
    return raw


def fetch(url, timeout=60, tries=2):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                h = {k.lower(): v for k, v in r.headers.items()}
                return r.status, decode_body(r.read(), h.get("content-encoding")), h
        except Exception as e:                           # noqa: BLE001
            last = e
            time.sleep(2 * (i + 1))
    raise last


def parse(page, auth):
    if auth == "nist":
        m = NIST_V.search(page) or NIST_V.search(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", page)))
        if not m:
            return None
        return {"v_updated_raw": m.group(2), "v_updated": iso(m.group(2)),
                "v_published_raw": m.group(1), "v_published": iso(m.group(1)),
                "rule": "nist Created/Updated"}
    if auth == "epa":
        m = EPA_V.search(page)
        if not m:
            return None
        raw = re.sub(r"<[^>]+>", "", m.group(1)).strip()
        p = EPA_PUB.search(page)
        return {"v_updated_raw": raw, "v_updated": iso(raw),
                "v_published_raw": ("-".join(p.groups()) if p else None),
                "v_published": ("-".join(p.groups()) if p else None),
                "rule": "epa l-page__footer-last-updated"}
    if auth == "govuk":
        ch = sorted(set(GOVUK_CHANGE.findall(page)))
        p = GOVUK_PUB.search(page)
        if not ch and not p:
            return None
        return {"v_updated_raw": (ch[-1] if ch else (p.group(1) if p else None)),
                "v_updated": iso(ch[-1]) if ch else iso(p.group(1)),
                "v_published_raw": p.group(1) if p else None,
                "v_published": iso(p.group(1)) if p else None,
                "n_change_events": len(ch),
                "rule": "govuk latest change-date" + ("" if ch else " (none; published used)")}
    raise ValueError(auth)


def main():
    census = json.load(open(f"{BASE}/census.json"))
    plan = []
    for auth in ("nist", "epa", "govuk"):
        plan += [(auth, r["url"]) for r in census["authorities"][auth][:80]]

    today = dt.date.today().isoformat()
    out = {"instrument": "does-the-date-move / increment 3B (printed-date resolution, live)",
           "preregistration": "PREREGISTRATION-3B.md, committed before this file existed",
           "fetch_date_utc": today,
           "run_started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
           "planned": len(plan), "rows": []}

    for i, (auth, url) in enumerate(plan, 1):
        rec = {"authority": auth, "url": url}
        try:
            st, body, hdr = fetch(url)
            page = body.decode("utf-8", "replace")
            rec["http_status"] = st
            rec["bytes"] = len(body)
            rec["h_last_modified"] = hdr.get("last-modified")
            got = parse(page, auth)
            if got is None:
                rec["status"] = "UNMEASURED-SELECTOR-NOT-FOUND"
            else:
                rec["status"] = "MEASURED"
                rec.update(got)
        except Exception as e:                           # noqa: BLE001
            rec["status"] = "UNMEASURED-FETCH-FAILED"
            rec["error"] = repr(e)[:200]
        out["rows"].append(rec)
        if i % 20 == 0 or rec["status"] != "MEASURED":
            print(f"[{i}/{len(plan)}] {auth} {rec['status']} {rec.get('v_updated')} {url[-46:]}", flush=True)
        time.sleep(DELAY)

    out["run_finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    json.dump(out, open(f"{BASE}/observations-3b.json", "w"), indent=1)
    n = sum(1 for r in out["rows"] if r["status"] == "MEASURED")
    print(f"WROTE observations-3b.json  measured {n}/{len(plan)}", flush=True)


main()
