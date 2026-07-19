#!/usr/bin/env python3
"""Structural content-quality classifier for archived X/Twitter captures.

CONTAINMENT (session-39 condition 7, hardened by the session-45 Skeptic pre-run review):
this reads ONLY the structural envelope of an archived capture — content-bearing vs
login/JS wall vs unavailable/deleted — and records NOTHING of the cited content's substance.
It stores the label, which structural markers fired, the *length* of any description meta,
and a truncated HASH of the normalised description (a hash reveals no substance but lets
boilerplate-duplication be detected — the Skeptic's sharpest false-positive mode). Per the
Skeptic's added containment condition, results are keyed by the frozen sample INDEX + capture
timestamp, NOT by handle/URL, so no human-readable "handle -> gone/shell" line exists on any
surface; the index->URL join lives in sample.json for full reproducibility. No tweet text,
media, author identity, or subject matter is assessed, printed, or written to disk. The
question is durability of the *copy*, not the content of the evidence.

Skeptic pre-run conditions applied here (all before any fetch):
 1. description meta matched attribute-order-robustly, and BOTH og:description and
    twitter:description are checked (not og only).
 2. a boilerplate/login page cannot outvote a genuine wall: a login/JS-wall marker classifies
    login_shell even when a (generic, bot-served) description string is present.
 3. a binomial confidence interval is reported alongside the point estimate p.
 4. capture-timestamp clustering is reported as an explicit independence caveat.

Outbound HTTPS transits a pre-configured proxy; full response bodies pass through the process
and that infrastructure. That is inherent to any fetch and named honestly, not closed here.

Run AFTER the pre-registration + this-file commit. Input: sample.json. Output: results.json.
"""
import json, subprocess, os, time, re, html, hashlib, math

here = os.path.dirname(os.path.abspath(__file__))
sample = json.load(open(os.path.join(here, "sample.json")))["sample"]

# structural markers (lowercased HTML) — envelope only, never substance
LOGIN = ["javascript is not available", "log in to x", "log in to twitter",
         "enable javascript to", "something went wrong. try reloading",
         "x.com/i/flow/login", "twitter.com/i/flow/login", "/i/flow/login"]
GONE  = ["this account doesn’t exist", "this account doesn't exist",
         "account has been suspended", "these posts are protected",
         "this post is unavailable", "hmm...this page doesn’t exist",
         "hmm...this page doesn't exist", "sorry, that page", "page doesn’t exist",
         "nothing to see here"]

def description(body):
    """Attribute-order-robust extraction of og:description OR twitter:description.
    Returns (length, hash12) of the normalised text — never the text itself."""
    best = ""
    for tag in re.findall(r"<meta\b[^>]*>", body, re.I):
        low = tag.lower()
        is_desc = ('property="og:description"' in low or "property='og:description'" in low
                   or 'name="twitter:description"' in low or "name='twitter:description'" in low
                   or 'property=og:description' in low or 'name=twitter:description' in low)
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
    # id_ suffix returns the archived ORIGINAL response bytes (no archive chrome)
    wb = f"https://web.archive.org/web/{ts}id_/{url}"
    for attempt in range(4):
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "45",
                            "-A", "Mozilla/5.0 (durability-census; structural-only)", wb],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout:
            return p.stdout
        time.sleep(2 * (attempt + 1))
    return ""

def classify(body):
    low = body.lower()
    dlen, dhash = description(body)
    has_gone  = any(k in low for k in GONE)
    has_login = any(k in low for k in LOGIN)
    has_article = ('data-testid="tweet"' in low) or ('<article' in low and 'tweet' in low)
    # ordering: a deleted page first; a genuine login/JS wall outvotes a bot-served
    # boilerplate description (Skeptic false-positive mode); only then trust content.
    if has_gone:
        label = "unavailable"
    elif has_login and dlen < 60:
        # a wall page with at most a short/boilerplate description = shell
        label = "login_shell"
    elif dlen >= 20 or has_article:
        label = "content_present"
    elif dlen > 0:
        label = "content_thin"
    elif has_login:
        label = "login_shell"
    else:
        label = "other"
    return {"label": label, "ogd_len": dlen, "ogd_hash": dhash,
            "has_gone": has_gone, "has_login": has_login,
            "has_article": has_article, "bytes": len(body)}

results = []
for i, s in enumerate(sample):
    body = fetch(s["capture"], s["url"])
    c = classify(body) if body else {"label": "fetch_failed", "ogd_len": 0, "ogd_hash": "",
                                      "has_gone": False, "has_login": False,
                                      "has_article": False, "bytes": 0}
    # keyed by index + timestamp only — NO url/handle (containment)
    results.append({"i": i, "capture": s["capture"], **c})
    print(f'[{i:2d}] {c["label"]:16s} ogd={c.get("ogd_len",0):4d} h={c.get("ogd_hash",""):12s} {s["capture"]}')
    time.sleep(1.0)  # polite throttle (session-41 lesson)

from collections import Counter
tally = Counter(r["label"] for r in results)
n = len(results)
cp = tally.get("content_present", 0)
p = cp / n if n else 0.0
# Wilson 95% interval (better than normal approx at small n / extreme p)
z = 1.96
denom = 1 + z*z/n
centre = (p + z*z/(2*n)) / denom
half = (z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
ci = [round(centre-half, 3), round(centre+half, 3)]
# boilerplate-duplication check among content_present (identical desc hash => bot boilerplate)
cp_hashes = [r["ogd_hash"] for r in results if r["label"] == "content_present" and r["ogd_hash"]]
dup = {h: c for h, c in Counter(cp_hashes).items() if c > 1}
# capture-window clustering (independence caveat, Skeptic condition 4)
days = Counter(r["capture"][:8] for r in results)
top_day, top_n = days.most_common(1)[0] if days else ("", 0)
win = sum(c for d, c in days.items() if "20241031" <= d <= "20241101")

out = {"n": n, "tally": dict(tally), "p_content_present": round(p, 3),
       "wilson95": ci,
       "content_present_hash_dupes": dup,
       "capture_clustering": {"n_in_2024-10-31_to_11-01": win,
                              "dominant_day": top_day, "dominant_day_n": top_n,
                              "distinct_days": len(days)},
       "results": results}
json.dump(out, open(os.path.join(here, "results.json"), "w"), indent=1)
print("\nTALLY:", dict(tally))
print(f"p(content_present) = {p:.3f}  Wilson95 = {ci}")
print("content_present hash-dupes (boilerplate check):", dup or "none")
print(f"capture clustering: {win}/{n} in 2024-10-31..11-01; {len(days)} distinct days")
