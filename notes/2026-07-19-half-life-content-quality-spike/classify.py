#!/usr/bin/env python3
"""Structural content-quality classifier for archived X/Twitter captures.

CONTAINMENT (session-39 condition 7): this reads ONLY the structural envelope of an
archived capture — is it a content-bearing snapshot, a login/JS wall, or an unavailable/
deleted page — and records NOTHING of the cited content's substance. It stores the
classification label, which structural markers fired, and the *length* (not the text) of
any og:description. No tweet text, media, author claim, or subject matter is fetched for
assessment, printed, or written to disk. The question is durability of the *copy*, not the
content of the evidence.

Run AFTER the pre-registration commit. Input: sample.json. Output: results.json.
"""
import json, subprocess, os, time, re, html

here = os.path.dirname(os.path.abspath(__file__))
sample = json.load(open(os.path.join(here, "sample.json")))["sample"]

# structural markers (lowercased HTML) — envelope only, never substance
LOGIN = ["javascript is not available", "log in to x", "log in to twitter",
         "enable javascript", "something went wrong. try reloading",
         "x.com/i/flow/login", "twitter.com/i/flow/login"]
GONE  = ["this account doesn’t exist", "this account doesn't exist",
         "account has been suspended", "these posts are protected",
         "this post is unavailable", "hmm...this page doesn’t exist",
         "hmm...this page doesn't exist", "sorry, that page", "page doesn’t exist"]

def fetch(ts, url):
    # id_ suffix returns the archived ORIGINAL response bytes (no Wayback chrome)
    wb = f"https://web.archive.org/web/{ts}id_/{url}"
    for attempt in range(4):
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "40",
                            "-A", "Mozilla/5.0 (durability-census; structural-only)", wb],
                           capture_output=True, text=True)
        if p.returncode == 0 and p.stdout:
            return p.stdout
        time.sleep(2 * (attempt + 1))
    return ""

def classify(body):
    low = body.lower()
    # og:description presence + LENGTH only (never the text itself)
    m = re.search(r'<meta[^>]+property=["\']og:description["\'][^>]+content=["\']([^"\']*)', body, re.I)
    ogd_len = len(html.unescape(m.group(1)).strip()) if m else 0
    has_gone  = any(k in low for k in GONE)
    has_login = any(k in low for k in LOGIN)
    # tweet article markup (envelope marker, not content)
    has_article = ('data-testid="tweet"' in low) or ('<article' in low and 'tweet' in low)
    if has_gone:
        label = "unavailable"
    elif ogd_len >= 20 or has_article:
        # a real captured tweet page carries a non-trivial og:description
        label = "content_present"
    elif has_login:
        label = "login_shell"
    elif ogd_len > 0:
        label = "content_thin"
    else:
        label = "other"
    return {"label": label, "ogd_len": ogd_len, "has_gone": has_gone,
            "has_login": has_login, "has_article": has_article, "bytes": len(body)}

results = []
for s in sample:
    body = fetch(s["capture"], s["url"])
    c = classify(body) if body else {"label": "fetch_failed", "bytes": 0}
    results.append({"url": s["url"], "capture": s["capture"], **c})
    print(f'{c["label"]:16s} ogd={c.get("ogd_len",0):4d} {s["capture"]}  {s["url"]}')
    time.sleep(1.0)  # polite throttle (session-41 lesson)

from collections import Counter
tally = Counter(r["label"] for r in results)
out = {"n": len(results), "tally": dict(tally), "results": results}
json.dump(out, open(os.path.join(here, "results.json"), "w"), indent=1)
print("\nTALLY:", dict(tally))
