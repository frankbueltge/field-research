#!/usr/bin/env python3
"""Structural content-quality classifier — Telegram + news/org strata (session 46).

CONTAINMENT (session-39 condition 7; the session-45 discipline unchanged): this reads ONLY
the structural envelope of an archived capture — content-bearing vs access wall vs
unavailable/deleted — and records NOTHING of the cited content's substance. It stores the
label, which structural markers fired, the *length* of the best description meta, and a
truncated HASH of the normalised description (a hash reveals no substance but lets
boilerplate-duplication be detected — the channel-about-text false-positive mode on
Telegram). Results are keyed by frozen sample INDEX + capture timestamp, NOT by
url/handle/channel; the index->URL join lives in sample.json for reproducibility. No
message text, media, author identity, or subject matter is assessed, printed, or written
to disk. The question is durability of the *copy*, not the content of the evidence.

Session-45 Skeptic conditions carried forward (all applied before any fetch):
 1. description meta matched attribute-order-robustly; og:description,
    twitter:description AND name="description" all checked.
 2. a wall page cannot be outvoted by a short bot-served boilerplate description.
 3. Wilson 95% intervals reported alongside each point estimate.
 4. capture-timestamp clustering reported per stratum as an independence caveat.

Outbound HTTPS transits a pre-configured proxy; full response bodies pass through the
process and that infrastructure — inherent to any fetch, named honestly.

Run AFTER the pre-registration + this-file commit. Input: sample.json. Output: results.json.
"""
import json, subprocess, os, time, re, html, hashlib, math, gzip
from collections import Counter

here = os.path.dirname(os.path.abspath(__file__))
sample_doc = json.load(open(os.path.join(here, "sample.json")))

# ---- structural markers (lowercased HTML) — envelope only, never substance ----

# Telegram envelopes
TG_CONTENT = ["tgme_widget_message"]              # embed-page message markup
TG_WALL    = ["please open telegram to view this post", "tgme_page_context_link"]
TG_GONE    = ["post not found", "channel with this name doesn", "page not found"]

# News/org envelopes
NEWS_CONTENT_MARKUP = ["<article", 'itemprop="articlebody"', 'property="article:',
                       'og:type" content="article', "og:type' content='article"]
NEWS_WALL  = ["consent.", "cookie consent", "accept all cookies", "before you continue",
              "subscribe to continue", "subscription required", "register to continue",
              "sign in to continue", "paywall"]
NEWS_GONE  = ["404 not found", "page not found", "error 404", "seite nicht gefunden",
              "this page does not exist", "domain is for sale", "account suspended",
              "this domain has expired"]

def description(body):
    """Attribute-order-robust extraction of og:description OR twitter:description OR
    name=description. Returns (length, hash12) of the longest normalised text — never
    the text itself."""
    best = ""
    for tag in re.findall(r"<meta\b[^>]*>", body, re.I):
        low = tag.lower()
        is_desc = ('property="og:description"' in low or "property='og:description'" in low
                   or 'name="twitter:description"' in low or "name='twitter:description'" in low
                   or 'property=og:description' in low or 'name=twitter:description' in low
                   or 'name="description"' in low or "name='description'" in low
                   or 'name=description' in low)
        if not is_desc:
            continue
        m = re.search(r'content=["\']([^"\']*)["\']', tag, re.I)
        if m:
            txt = html.unescape(m.group(1)).strip()
            if len(txt) > len(best):
                best = txt
    h = hashlib.sha256(best.encode()).hexdigest()[:12] if best else ""
    return len(best), h

def fetch(ts, url):
    # id_ suffix returns the archived ORIGINAL response bytes (no archive chrome);
    # bytes may be gzip-compressed (session-45 transport fix).
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
            return raw.decode("utf-8", errors="replace")
        time.sleep(2 * (attempt + 1))
    return ""

def classify(body, stratum):
    low = body.lower()
    dlen, dhash = description(body)
    if stratum == "telegram":
        has_gone    = any(k in low for k in TG_GONE)
        has_wall    = any(k in low for k in TG_WALL)
        has_content = any(k in low for k in TG_CONTENT)
    else:
        has_gone    = any(k in low for k in NEWS_GONE)
        has_wall    = any(k in low for k in NEWS_WALL)
        has_content = any(k in low for k in NEWS_CONTENT_MARKUP)
    # ordering (session-45 rule): deleted first; a genuine wall outvotes a short
    # boilerplate description; only then trust content signals.
    if has_gone and not has_content and dlen < 60:
        label = "unavailable"
    elif has_wall and dlen < 60 and not has_content:
        label = "access_wall"
    elif dlen >= 20 or has_content:
        label = "content_present"
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

out = {"strata": {}}
for stratum, block in sample_doc["strata"].items():
    results = []
    for i, s in enumerate(block["sample"]):
        body = fetch(s["capture"], s["url"])
        c = classify(body, stratum) if body else {
            "label": "fetch_failed", "desc_len": 0, "desc_hash": "",
            "has_gone": False, "has_wall": False, "has_content_markup": False, "bytes": 0}
        # keyed by index + timestamp only — NO url/handle/channel (containment)
        results.append({"i": i, "capture": s["capture"], **c})
        print(f'[{stratum:14s} {i:2d}] {c["label"]:16s} desc={c["desc_len"]:4d} '
              f'h={c["desc_hash"]:12s} {s["capture"]}')
        time.sleep(1.0)  # polite throttle (session-41 lesson)
    tally = Counter(r["label"] for r in results)
    n = len(results)
    cp = tally.get("content_present", 0)
    # boilerplate-duplication check (identical desc hash across content_present items —
    # on Telegram this is the channel-about-text false-positive mode)
    cp_hashes = [r["desc_hash"] for r in results if r["label"] == "content_present" and r["desc_hash"]]
    dup = {h: c for h, c in Counter(cp_hashes).items() if c > 1}
    days = Counter(r["capture"][:8] for r in results)
    top_day, top_n = days.most_common(1)[0] if days else ("", 0)
    out["strata"][stratum] = {
        "n": n, "tally": dict(tally),
        "p_content_present": round(cp / n, 3) if n else 0.0,
        "wilson95": wilson(cp, n),
        "content_present_hash_dupes": dup,
        "capture_clustering": {"dominant_day": top_day, "dominant_day_n": top_n,
                               "distinct_days": len(days)},
        "results": results}
    print(f"\n{stratum} TALLY: {dict(tally)}")
    print(f"{stratum} p(content_present) = {cp/n:.3f}  Wilson95 = {wilson(cp, n)}")
    print(f"{stratum} hash-dupes: {dup or 'none'}")
    print(f"{stratum} clustering: dominant day {top_day} x{top_n}; {len(days)} distinct days\n")

json.dump(out, open(os.path.join(here, "results.json"), "w"), indent=1)
