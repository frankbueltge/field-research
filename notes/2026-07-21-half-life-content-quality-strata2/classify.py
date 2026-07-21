#!/usr/bin/env python3
"""Structural content-quality classifier — Telegram + news/org strata (session 46).

CONTAINMENT (session-39 condition 7; the session-45 discipline unchanged): this reads ONLY
the structural envelope of an archived capture — content-bearing vs access wall vs
unavailable/deleted — and records NOTHING of the cited content's substance. It stores the
label, which structural markers fired, the *length* of the best description meta, and a
truncated HASH of the normalised description (a hash reveals no substance but lets
boilerplate-duplication be detected). Results are keyed by frozen sample INDEX + capture
timestamp, NOT by url/handle/channel; the index->URL join lives in sample.json for
reproducibility. No message text, media, author identity, or subject matter is assessed,
printed, or written to disk. The question is durability of the *copy*, not the content of
the evidence.

Skeptic pre-run conditions (session 46) applied BEFORE any sample fetch:
 C1. non-HTML binaries (PDF/JPEG/PNG magic bytes) get their own label `binary_document`,
     reported separately and excluded from p's denominator (pre-registered amendment) —
     never silently folded into `other`.
 C2. news/org `content_present` cannot rest on generic article markup or a generic
     description alone when the capture's own canonical/og:url points somewhere else:
     a clear path mismatch (cited path deep, canonical path root/shallow) downgrades to
     `redirected_off_target` (a structural, substance-free comparison of two URLs).
 C3. (pre-flight, preflight_telegram.py + preflight_results.json) the discriminating
     envelope on plain t.me/<channel>/<id> pages was determined empirically on known
     out-of-sample pages: a previewable post renders WITHOUT `tgme_page_description` and
     carries the message text in og:description (~37KB); a non-previewable post serves the
     CHANNEL-preview envelope WITH `tgme_page_description` and the channel bio as its
     description (~11KB, identical to the channel root). `tgme_widget_message` never
     appears on plain pages (dead code — removed). New Telegram label: `channel_fallback`.
 C4. the "please open telegram to view this post" banner did not appear on any pre-flight
     page (content-bearing or fallback); the wall-override risk for short genuine captions
     is therefore resolved by the envelope rule in C3, not by a banner string.
Session-45 conditions carried: attribute-order-robust description extraction (og +
twitter + name=description for news); walls outvote short boilerplate; Wilson 95%
intervals; per-stratum capture-day clustering caveat.

Outbound HTTPS transits a pre-configured proxy; full response bodies pass through the
process and that infrastructure — inherent to any fetch, named honestly.

Run AFTER the hardened-classifier commit. Input: sample.json. Output: results.json.
"""
import json, subprocess, os, time, re, html, hashlib, math, gzip
from collections import Counter
from urllib.parse import urlparse

here = os.path.dirname(os.path.abspath(__file__))
sample_doc = json.load(open(os.path.join(here, "sample.json")))

# ---- structural markers (lowercased HTML) — envelope only, never substance ----

TG_CHANNEL_FALLBACK = "tgme_page_description"     # channel-preview envelope (pre-flight C3)
TG_GONE = ["post not found", "channel with this name doesn", "page not found",
           "please open telegram to view this post"]

NEWS_CONTENT_MARKUP = ["<article", 'itemprop="articlebody"', 'property="article:',
                       'og:type" content="article', "og:type' content='article"]
NEWS_WALL  = ["cookie consent", "accept all cookies", "before you continue",
              "subscribe to continue", "subscription required", "register to continue",
              "sign in to continue", "paywall"]
NEWS_GONE  = ["404 not found", "page not found", "error 404", "seite nicht gefunden",
              "this page does not exist", "domain is for sale", "account suspended",
              "this domain has expired"]

def description(body, include_name_desc):
    """Attribute-order-robust extraction. Returns (length, hash12) of the longest
    normalised description text — never the text itself."""
    best = ""
    for tag in re.findall(r"<meta\b[^>]*>", body, re.I):
        low = tag.lower()
        is_desc = ('property="og:description"' in low or "property='og:description'" in low
                   or 'name="twitter:description"' in low or "name='twitter:description'" in low
                   or 'property=og:description' in low or 'name=twitter:description' in low)
        if include_name_desc:
            is_desc = is_desc or ('name="description"' in low or "name='description'" in low
                                  or 'name=description ' in low)
        if not is_desc:
            continue
        m = re.search(r'content=["\']([^"\']*)["\']', tag, re.I)
        if m:
            txt = html.unescape(m.group(1)).strip()
            if len(txt) > len(best):
                best = txt
    h = hashlib.sha256(best.encode()).hexdigest()[:12] if best else ""
    return len(best), h

def canonical_path(body):
    """Extract the capture's own canonical/og:url PATH (structural; substance-free)."""
    for pat in (r'<link\b[^>]*rel=["\']canonical["\'][^>]*href=["\']([^"\']+)["\']',
                r'<link\b[^>]*href=["\']([^"\']+)["\'][^>]*rel=["\']canonical["\']',
                r'<meta\b[^>]*property=["\']og:url["\'][^>]*content=["\']([^"\']+)["\']',
                r'<meta\b[^>]*content=["\']([^"\']+)["\'][^>]*property=["\']og:url["\']'):
        m = re.search(pat, body, re.I)
        if m:
            try:
                return urlparse(m.group(1)).path or "/"
            except ValueError:
                return None
    return None

def path_depth(path):
    return len([seg for seg in (path or "/").split("/") if seg])

def fetch(ts, url):
    # id_ suffix returns the archived ORIGINAL response bytes (no archive chrome);
    # bytes may be gzip-compressed (session-45 transport fix). Returns RAW BYTES (C1).
    wb = f"https://web.archive.org/web/{ts}id_/{url}"
    for attempt in range(4):
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "45",
                            "-A", "Mozilla/5.0 (durability-census; structural-only)", wb],
                           capture_output=True)
        if p.returncode == 0 and p.stdout:
            raw = p.stdout
            if raw[:2] == b"\x1f\x8b":
                try:
                    raw = gzip.decompress(raw)
                except OSError:
                    pass
            return raw
        time.sleep(2 * (attempt + 1))
    return b""

def classify(raw, stratum, cited_url):
    # C1: binary magic first — these can never carry HTML meta and are counted apart.
    if raw[:5] == b"%PDF-" or raw[:2] == b"\xff\xd8" or raw[:8] == b"\x89PNG\r\n\x1a\n":
        kind = "pdf" if raw[:5] == b"%PDF-" else "image"
        return {"label": "binary_document", "binary_kind": kind, "desc_len": 0,
                "desc_hash": "", "has_gone": False, "has_wall": False,
                "has_content_markup": False, "bytes": len(raw)}
    body = raw.decode("utf-8", errors="replace")
    low = body.lower()
    if stratum == "telegram":
        dlen, dhash = description(body, include_name_desc=False)
        has_gone = any(k in low for k in TG_GONE)
        is_fallback = TG_CHANNEL_FALLBACK in low       # C3 envelope rule
        if has_gone and dlen < 60:
            label = "unavailable"
        elif is_fallback:
            label = "channel_fallback"                  # channel bio served, not the post
        elif dlen >= 20:
            label = "content_present"                   # message-render envelope + real desc
        elif dlen > 0:
            label = "content_thin"
        else:
            label = "other"
        return {"label": label, "desc_len": dlen, "desc_hash": dhash,
                "has_gone": has_gone, "has_wall": is_fallback,
                "has_content_markup": (dlen > 0 and not is_fallback), "bytes": len(body)}
    # news/org
    dlen, dhash = description(body, include_name_desc=True)
    has_gone    = any(k in low for k in NEWS_GONE)
    has_wall    = any(k in low for k in NEWS_WALL)
    has_content = any(k in low for k in NEWS_CONTENT_MARKUP)
    if has_gone and not has_content and dlen < 60:
        label = "unavailable"
    elif has_wall and dlen < 60 and not has_content:
        label = "access_wall"
    elif dlen >= 20 or has_content:
        label = "content_present"
        # C2: canonical/og:url path check — a deep cited path resolved to a root/shallow
        # canonical is a homepage/soft-404 render, not the cited page.
        cpath = canonical_path(body)
        if cpath is not None:
            cited_depth = path_depth(urlparse(cited_url).path)
            if cited_depth >= 2 and path_depth(cpath) <= 1:
                label = "redirected_off_target"
    elif dlen > 0:
        label = "content_thin"
    elif has_wall:
        label = "access_wall"
    else:
        label = "other"
    return {"label": label, "desc_len": dlen, "desc_hash": dhash,
            "has_gone": has_gone, "has_wall": has_wall,
            "has_content_markup": has_content, "bytes": len(body)}

def wilson(cp, n):
    if not n:
        return [0.0, 0.0]
    p = cp / n
    z = 1.96
    denom = 1 + z*z/n
    centre = (p + z*z/(2*n)) / denom
    half = (z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
    return [round(centre-half, 3), round(centre+half, 3)]

def channel_key(url):
    # first path segment of a t.me URL — used ONLY to count duplicate-detection
    # opportunities in aggregate (Skeptic condition 9); never stored or printed.
    return urlparse(url).path.strip("/").split("/")[0].lower()

out = {"strata": {}}
for stratum, block in sample_doc["strata"].items():
    results = []
    for i, s in enumerate(block["sample"]):
        raw = fetch(s["capture"], s["url"])
        c = classify(raw, stratum, s["url"]) if raw else {
            "label": "fetch_failed", "desc_len": 0, "desc_hash": "",
            "has_gone": False, "has_wall": False, "has_content_markup": False, "bytes": 0}
        # keyed by index + timestamp only — NO url/handle/channel (containment)
        results.append({"i": i, "capture": s["capture"], **c})
        print(f'[{stratum:14s} {i:2d}] {c["label"]:20s} desc={c["desc_len"]:4d} '
              f'h={c["desc_hash"]:12s} {s["capture"]}')
        time.sleep(1.0)  # polite throttle (session-41 lesson)
    tally = Counter(r["label"] for r in results)
    n_total = len(results)
    n_binary = tally.get("binary_document", 0)
    n_denom = n_total - n_binary          # C1: pre-registered denominator amendment
    cp = tally.get("content_present", 0)
    cp_hashes = [r["desc_hash"] for r in results if r["label"] == "content_present" and r["desc_hash"]]
    dup = {h: c for h, c in Counter(cp_hashes).items() if c > 1}
    days = Counter(r["capture"][:8] for r in results)
    top_day, top_n = days.most_common(1)[0] if days else ("", 0)
    entry = {"n_total": n_total, "n_binary_document": n_binary,
             "n_denominator": n_denom, "tally": dict(tally),
             "p_content_present": round(cp / n_denom, 3) if n_denom else 0.0,
             "wilson95": wilson(cp, n_denom),
             "content_present_hash_dupes": dup,
             "capture_clustering": {"dominant_day": top_day, "dominant_day_n": top_n,
                                    "distinct_days": len(days)},
             "results": results}
    if stratum == "telegram":
        # Skeptic condition 9: how much of the sample the hash-dup check could even
        # reach — items sharing a channel with >=1 other sampled item (count only).
        ch = Counter(channel_key(s["url"]) for s in block["sample"])
        entry["dup_check_reachable_items"] = sum(c for c in ch.values() if c > 1)
        entry["distinct_channels"] = len(ch)
    out["strata"][stratum] = entry
    print(f"\n{stratum} TALLY: {dict(tally)}")
    print(f"{stratum} p(content_present) = {entry['p_content_present']}  "
          f"Wilson95 = {entry['wilson95']}  (denominator {n_denom}, binaries {n_binary})")
    print(f"{stratum} hash-dupes: {dup or 'none'}")
    print(f"{stratum} clustering: dominant day {top_day} x{top_n}; {len(days)} distinct days\n")

json.dump(out, open(os.path.join(here, "results.json"), "w"), indent=1)
