#!/usr/bin/env python3
"""Coverage-is-not-custody census: content-preservation of archived vs live captures,
three strata (X/Twitter, Telegram, news/org positive control).

Lineage: session 45's structural classifier (notes/2026-07-19-.../classify.py). The
description extractor and the content/login/gone precedence are logic-identical except for the
two Skeptic-mandated fixes recorded in DIAGNOSTIC-NOTE.md: (C3.1) tweet-article markup promotes
to content_present BEFORE the login-wall rule; (Telegram) the deleted-post→channel-bio guard is a
within-channel description-duplication statistic, not a hard post-ID gate (the pre-run diagnostic
showed valid post pages carry neither post-ID-in-og:url nor tgme markup).

CONTAINMENT (session-39 cond. 7; session-45 + this-session Skeptic C4): the committed results.json
is AGGREGATE-ONLY — no per-item URL, handle, or capture-timestamp→bucket row (a per-item capture
timestamp is joinable to the citation URL via the public session-41 CDX census). Description text
is never stored; description hashes are computed with a RUN-SCOPED random salt used only for the
within-run distinct/duplicate counts and then discarded — no raw hash is published. Handles/
channels are parsed only transiently for distinct-source counts. Capture-date histograms are
month-binned with small bins suppressed. sample.json lists the citation URLs (already public) for
reproducibility; a re-runner reproduces the AGGREGATES, not any URL→outcome mapping.

Run AFTER the pre-registration + this-file + sample.json commit. Output: results.json.
"""
import json, subprocess, os, time, re, html, hashlib, math, gzip, secrets
from collections import Counter, defaultdict

here = os.path.dirname(os.path.abspath(__file__))
sample = json.load(open(os.path.join(here, "sample.json")))
SALT = secrets.token_hex(8)  # run-scoped, discarded — hashes never published raw

LOGIN = ["javascript is not available", "log in to x", "log in to twitter",
         "enable javascript to", "something went wrong. try reloading",
         "x.com/i/flow/login", "twitter.com/i/flow/login", "/i/flow/login"]
GONE  = ["this account doesn’t exist", "this account doesn't exist",
         "account has been suspended", "these posts are protected",
         "this post is unavailable", "hmm...this page doesn’t exist",
         "hmm...this page doesn't exist", "sorry, that page", "page doesn’t exist",
         "nothing to see here", "post not found", "channel is not accessible"]

def description(body):
    best = ""
    for tag in re.findall(r"<meta\b[^>]*>", body, re.I):
        low = tag.lower()
        if ('og:description' in low or 'twitter:description' in low):
            m = re.search(r'content=["\']([^"\']*)["\']', tag, re.I)
            if m:
                txt = html.unescape(m.group(1)).strip()
                if len(txt) > len(best):
                    best = txt
    dlen = len(best)
    dhash = hashlib.sha256((SALT + best).encode()).hexdigest()[:16] if best else ""
    return dlen, dhash

def fetch(url, ts=None):
    u = f"https://web.archive.org/web/{ts}id_/{url}" if ts else url
    for attempt in range(4):
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "45", "-A",
                            "Mozilla/5.0 (durability-census; structural-only)", u],
                           capture_output=True, env={**os.environ})
        if p.returncode == 0 and p.stdout:
            raw = p.stdout
            if raw[:2] == b"\x1f\x8b":
                try: raw = gzip.decompress(raw)
                except OSError: pass
            return raw.decode("utf-8", errors="replace")
        time.sleep(2 * (attempt + 1))
    return ""

def classify(body, stratum):
    low = body.lower()
    dlen, dhash = description(body)
    has_gone = any(k in low for k in GONE)
    has_login = any(k in low for k in LOGIN)
    # tweet-article markup is an X-ONLY content signal (Verifier session-46 finding #2: an
    # un-gated has_article leaked embedded-tweet/<article> markup into news/org, contradicting
    # the pre-registered "X-only" documentation). Gated to the X stratum here.
    has_article = (stratum == "x-twitter") and (
        ('data-testid="tweet"' in low) or ('<article' in low and 'tweet' in low))
    if has_article:                         # C3.1: content markup wins outright (X only)
        label = "content_present"
    elif has_gone:
        label = "unavailable"
    elif has_login and dlen < 60:
        label = "login_shell"
    elif dlen >= 20:
        label = "content_present"
    elif dlen > 0:
        label = "content_thin"
    elif has_login:
        label = "login_shell"
    else:
        label = "other"
    return label, dlen, dhash

def handle(url):
    m = re.search(r"(?:x\.com|twitter\.com)/([^/]+)/status", url) or \
        re.search(r"t\.me/([^/]+)/", url) or re.search(r"https?://([^/]+)/", url)
    return m.group(1) if m else url

def quartiles(xs):
    if not xs: return None
    xs = sorted(xs); n = len(xs)
    return {"min": xs[0], "med": xs[n//2], "max": xs[-1]}

def wilson(cp, n):
    if not n: return [0.0, 0.0]
    p = cp/n; z = 1.96; d = 1 + z*z/n
    c = (p + z*z/(2*n))/d
    h = (z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)))/d
    return [round(c-h, 3), round(c+h, 3)]

def aggregate(items):
    """items: list of dicts with label,dlen,dhash,bytes,handle,capday (capday None for live)."""
    n = len(items)
    tally = Counter(it["label"] for it in items)
    cp = tally.get("content_present", 0)
    # distinct-source (C5.1)
    handles = [it["handle"] for it in items]
    # within-channel description duplication among content_present (Telegram deleted-post guard)
    cp_items = [it for it in items if it["label"] == "content_present" and it["dhash"]]
    by_ch = defaultdict(list)
    for it in cp_items:
        by_ch[it["handle"]].append(it["dhash"])
    same_ch_repeat = sum(len(v) - len(set(v)) for v in by_ch.values())
    distinct_desc = len(set(it["dhash"] for it in cp_items))
    # month histogram of captures (archived only), suppress bins < 5 (C4.1)
    months = Counter(it["capday"][:6] for it in items if it.get("capday"))
    hist = {m: c for m, c in months.items() if c >= 5}
    suppressed = sum(c for m, c in months.items() if c < 5)
    capdays = sorted(it["capday"] for it in items if it.get("capday"))
    med_capday = capdays[len(capdays)//2] if capdays else None
    return {
        "n": n, "tally": dict(tally),
        "content_present": cp, "p_content_present": round(cp/n, 3) if n else 0.0,
        "wilson95": wilson(cp, n),
        "distinct_handles": len(set(handles)), "distinct_source_frac": round(len(set(handles))/n, 3) if n else 0.0,
        "content_present_distinct_desc": distinct_desc, "content_present_total": len(cp_items),
        "same_channel_desc_repeats": same_ch_repeat,
        "bytes_quartiles": quartiles([it["bytes"] for it in items]),
        "capture_month_hist_ge5": hist, "capture_months_suppressed_lt5": suppressed,
        "median_capture_day": med_capday,
    }

report = {"sample_sha256": sample.get("sample_sha256"), "archived": {}, "live_control": {}}

# ---- archived arm (census) ----
for stratum in sample["stratum_order"]:
    items = []
    rows = sample[stratum]
    for i, s in enumerate(rows):
        body = fetch(s["url"], s["capture"])
        if body:
            label, dlen, dhash = classify(body, stratum); nbytes = len(body)
        else:
            label, dlen, dhash, nbytes = "fetch_failed", 0, "", 0
        items.append({"label": label, "dlen": dlen, "dhash": dhash, "bytes": nbytes,
                      "handle": handle(s["url"]), "capday": s["capture"][:8]})
        print(f'A {stratum:10s}[{i:3d}] {label:16s} d={dlen:4d} {s["capture"][:8]}')
        time.sleep(0.8)
    report["archived"][stratum] = aggregate(items)

# ---- live-control arm (sample) ----
for stratum in sample["stratum_order"]:
    items = []
    for i, url in enumerate(sample["live_control"][stratum]):
        body = fetch(url)
        if body:
            label, dlen, dhash = classify(body, stratum); nbytes = len(body)
        else:
            label, dlen, dhash, nbytes = "fetch_failed", 0, "", 0
        items.append({"label": label, "dlen": dlen, "dhash": dhash, "bytes": nbytes,
                      "handle": handle(url), "capday": None})
        print(f'L {stratum:10s}[{i:3d}] {label:16s} d={dlen:4d}')
        time.sleep(0.8)
    report["live_control"][stratum] = aggregate(items)

json.dump(report, open(os.path.join(here, "results.json"), "w"), indent=1)
print("\n=== SUMMARY (content_present rate) ===")
for arm in ("archived", "live_control"):
    for st in sample["stratum_order"]:
        r = report[arm][st]
        print(f"  {arm:12s} {st:10s} {r['content_present']:3d}/{r['n']:3d} "
              f"= {r['p_content_present']:.3f}  Wilson {r['wilson95']}")
