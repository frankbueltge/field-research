"""Increment 1 — executes PREREGISTRATION.md exactly. Writes observations.json.

Monthly observations of archived captures; per observation: normalised text hash,
visible date V (extractor reused unmodified from the 'As of Today' line), and the
origin's own Last-Modified as preserved by the archive (x-archive-orig-last-modified).
"""
import json, re, sys, time, gzip, zlib, hashlib, difflib, datetime as dt
import urllib.request, urllib.parse, urllib.error

sys.path.insert(0, "/home/user/field-research/drafts/2026-08-06-as-of-today")
from collect_signals import extract_v, normalise_v, visible_text  # noqa: E402  (reused unmodified)

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
MONTHS = [(2025, m) for m in range(8, 13)] + [(2026, m) for m in range(1, 8)]  # 2025-08..2026-07
HEXTOK = re.compile(r"\b[0-9a-fA-F]{16,}\b")


def decode_body(raw: bytes, enc: str | None) -> tuple[bytes, str]:
    """D1 fix. The archive replays the ORIGINAL payload, so a capture the origin served
    gzipped arrives gzipped and no client library unpacks it for us. Run 1 hashed those
    compressed bytes as if they were text. Detect by magic bytes, not by trusting the header."""
    if raw[:2] == b"\x1f\x8b":
        try:
            return gzip.decompress(raw), "gzip"
        except Exception:                           # noqa: BLE001
            return raw, "gzip-FAILED"
    if enc and "deflate" in enc.lower():
        for wbits in (-15, 15):
            try:
                return zlib.decompress(raw, wbits), "deflate"
            except Exception:                       # noqa: BLE001
                continue
        return raw, "deflate-FAILED"
    if enc and "br" in enc.lower().split(","):
        return raw, "br-UNSUPPORTED"
    return raw, "identity"


def get(url, timeout=90, tries=3):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                hdr = {k.lower(): v for k, v in r.headers.items()}
                body, how = decode_body(r.read(), hdr.get("content-encoding"))
                hdr["_decoded_as"] = how
                return r.status, body, hdr
        except Exception as e:                      # noqa: BLE001 - recorded, never silently swallowed
            last = e
            time.sleep(4 * (i + 1))
    raise last


def cdx(url):
    q = urllib.parse.urlencode({
        "url": url, "output": "json", "fl": "timestamp,digest,statuscode",
        "from": "20250801", "to": "20260731", "filter": "statuscode:200", "limit": "5000",
    })
    st, body, _ = get("https://web.archive.org/cdx/search/cdx?" + q)
    rows = json.loads(body) if body.strip() else []
    return rows[1:] if rows else []


def pick(caps, year, month):
    """M: first 200-capture at or after the 15th; else the last before the 15th; else None."""
    pre = f"{year:04d}{month:02d}"
    inm = [c for c in caps if c[0].startswith(pre)]
    if not inm:
        return None
    at_or_after = [c for c in inm if int(c[0][6:8]) >= 15]
    return at_or_after[0] if at_or_after else inm[-1]


def norm_text(body: bytes) -> str:
    page = body.decode("utf-8", "replace")
    t = visible_text(page)
    t = HEXTOK.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()


def observe(url, cap):
    ts = cap[0]
    st, body, hdr = get(f"https://web.archive.org/web/{ts}id_/{url}")
    page = body.decode("utf-8", "replace")
    v = extract_v(page)
    t = norm_text(body)
    return {
        "timestamp": ts, "cdx_digest": cap[1], "http_status": st, "bytes": len(body),
        "h_raw": hdr.get("x-archive-orig-last-modified"),
        "v_raw": v["v_raw"], "v": normalise_v(v["v_raw"]), "v_rule": v["v_rule"],
        "text_sha256": hashlib.sha256(t.encode()).hexdigest(), "text_len": len(t),
        "decoded_as": hdr.get("_decoded_as"),
        "_text": t,
    }


def main():
    sigs = json.load(open("/home/user/field-research/drafts/2026-08-06-as-of-today/signals.json"))
    sig2 = json.load(open("/home/user/field-research/drafts/2026-08-06-as-of-today/signals-2.json"))
    pop = [("EC", r["url"]) for r in sigs["rows"] if r.get("v")][:3]
    for a, n in (("NIST", 3), ("GOVUK", 3), ("IE", 2)):
        pop += [(a, r["url"]) for r in sig2["authorities"][a]["rows"] if r.get("v")][:n]

    out = {"instrument": "does-the-date-move / increment 1, run 2 (D1 fixed)",
           "preregistration": "PREREGISTRATION.md, committed before this file existed",
           "run_started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
           "months": [f"{y:04d}-{m:02d}" for y, m in MONTHS], "urls": []}

    for auth, url in pop:
        rec = {"authority": auth, "url": url, "observations": {}, "errors": [],
               "cdx_adjacent_pairs": 0, "cdx_adjacent_digest_differs": 0}
        try:
            caps = cdx(url)
        except Exception as e:                      # noqa: BLE001
            rec["errors"].append({"stage": "cdx", "error": repr(e)})
            out["urls"].append(rec)
            print("CDX-FAIL", auth, url[:60], flush=True)
            continue
        rec["captures_200_in_window"] = len(caps)
        digs = [c[1] for c in caps]
        rec["cdx_adjacent_pairs"] = max(0, len(digs) - 1)
        rec["cdx_adjacent_digest_differs"] = sum(1 for i in range(1, len(digs)) if digs[i] != digs[i - 1])
        time.sleep(1.5)
        for y, m in MONTHS:
            key = f"{y:04d}-{m:02d}"
            cap = pick(caps, y, m)
            if cap is None:
                rec["observations"][key] = {"status": "MISSING-NO-CAPTURE"}
                continue
            try:
                rec["observations"][key] = observe(url, cap)
            except Exception as e:                  # noqa: BLE001
                rec["observations"][key] = {"status": "MISSING-FETCH-FAILED", "timestamp": cap[0]}
                rec["errors"].append({"stage": "fetch", "month": key, "error": repr(e)})
            time.sleep(1.5)
        got = sum(1 for o in rec["observations"].values() if "text_sha256" in o)
        print(f"{auth} {got}/12 obs  {url[:62]}", flush=True)
        out["urls"].append(rec)

    # pairwise comparison of consecutive months
    for rec in out["urls"]:
        pairs = []
        keys = [f"{y:04d}-{m:02d}" for y, m in MONTHS]
        for i in range(1, len(keys)):
            a, b = rec["observations"].get(keys[i - 1], {}), rec["observations"].get(keys[i], {})
            if "text_sha256" not in a or "text_sha256" not in b:
                pairs.append({"from": keys[i - 1], "to": keys[i], "status": "DROPPED-MISSING"})
                continue
            ratio = difflib.SequenceMatcher(None, a["_text"], b["_text"]).ratio()
            cls = "IDENTICAL" if a["text_sha256"] == b["text_sha256"] else (
                "TRIVIAL" if ratio >= 0.98 else "SUBSTANTIVE")
            def moved(x, y_):
                if x is None or y_ is None:
                    return "UNSCORABLE"
                return "MOVED" if x != y_ else "STILL"
            pairs.append({"from": keys[i - 1], "to": keys[i], "status": "SCORED",
                          "ratio": round(ratio, 6), "content": cls,
                          "v_from": a["v"], "v_to": b["v"], "v": moved(a["v"], b["v"]),
                          "h_from": a["h_raw"], "h_to": b["h_raw"], "h": moved(a["h_raw"], b["h_raw"]),
                          "digest_differs": a["cdx_digest"] != b["cdx_digest"]})
        rec["pairs"] = pairs
        for o in rec["observations"].values():
            o.pop("_text", None)

    out["run_finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    json.dump(out, open(f"{BASE}/observations.json", "w"), indent=1)
    print("WROTE observations.json", flush=True)


main()
