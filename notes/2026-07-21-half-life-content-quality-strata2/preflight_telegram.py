#!/usr/bin/env python3
"""Skeptic condition 3 (session 46): pre-flight envelope check on KNOWN Telegram pages
OUTSIDE the frozen sample, run BEFORE the classifier is finalised and before any sample
fetch. Purpose: determine empirically, on plain t.me/<channel>/<id> pages, (a) what
structural marker (if any) distinguishes a message-body render from a channel-bio
fallback, and (b) whether Telegram's wall/nag text appears on content-bearing pages too.

Pages used are Telegram's own official public channels (t.me/telegram, t.me/durov) —
public infrastructure channels, not part of the citation base, so naming them here is
containment-safe. Recorded: marker booleans, description LENGTHS and truncated hashes,
byte sizes — plus, for these out-of-sample infrastructure pages only, whether the
description equals the channel root's description (the fallback test). No sample URL is
touched."""
import subprocess, re, html, hashlib, gzip, json, time, os

PAGES = [
    # (label, url) — live plain pages + channel roots for the fallback comparison
    ("root:telegram",   "https://t.me/telegram"),
    ("post:telegram/1", "https://t.me/telegram/1"),
    ("post:telegram/271","https://t.me/telegram/271"),
    ("root:durov",      "https://t.me/durov"),
    ("post:durov/1",    "https://t.me/durov/1"),
    ("post:durov/342",  "https://t.me/durov/342"),
    # one ARCHIVED capture of a plain post page, to compare the archive's render
    ("wb:post:telegram/271", "https://web.archive.org/web/20240101000000id_/https://t.me/telegram/271"),
]

MARKERS = ["tgme_widget_message", "tgme_page_description", "tgme_page_context_link",
           "please open telegram to view this post", "preview channel",
           "tgme_action_button", "og:description", "twitter:description",
           "tgme_page_extra", "tgme_page_title"]

def fetch(url):
    for attempt in range(3):
        p = subprocess.run(["curl", "-sS", "-L", "--max-time", "45",
                            "-A", "Mozilla/5.0 (durability-census; structural-only)", url],
                           capture_output=True)
        if p.returncode == 0 and p.stdout:
            raw = p.stdout
            if raw[:2] == b"\x1f\x8b":
                try: raw = gzip.decompress(raw)
                except OSError: pass
            return raw.decode("utf-8", errors="replace")
        time.sleep(2)
    return ""

def desc(body):
    best = ""
    for tag in re.findall(r"<meta\b[^>]*>", body, re.I):
        low = tag.lower()
        if ('og:description' in low or 'twitter:description' in low):
            m = re.search(r'content=["\']([^"\']*)["\']', tag, re.I)
            if m:
                t = html.unescape(m.group(1)).strip()
                if len(t) > len(best): best = t
    return best

out = []
descs = {}
for label, url in PAGES:
    body = fetch(url)
    low = body.lower()
    d = desc(body)
    descs[label] = d
    rec = {"page": label, "bytes": len(body),
           "desc_len": len(d),
           "desc_hash": hashlib.sha256(d.encode()).hexdigest()[:12] if d else "",
           "markers": {m: (m in low) for m in MARKERS}}
    out.append(rec)
    print(json.dumps(rec, indent=None))
    time.sleep(1.0)

# fallback test: does a post page's description equal its channel root's? (booleans only)
cmp = {
    "telegram/1_eq_root":   descs.get("post:telegram/1") == descs.get("root:telegram"),
    "telegram/271_eq_root": descs.get("post:telegram/271") == descs.get("root:telegram"),
    "durov/1_eq_root":      descs.get("post:durov/1") == descs.get("root:durov"),
    "durov/342_eq_root":    descs.get("post:durov/342") == descs.get("root:durov"),
    "wb271_eq_live271":     descs.get("wb:post:telegram/271") == descs.get("post:telegram/271"),
}
print("FALLBACK-EQUALITY:", json.dumps(cmp))
here = os.path.dirname(os.path.abspath(__file__))
json.dump({"pages": out, "fallback_equality": cmp},
          open(os.path.join(here, "preflight_results.json"), "w"), indent=1)
