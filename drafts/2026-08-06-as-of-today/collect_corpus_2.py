#!/usr/bin/env python3
"""collect_corpus_2.py — build the proof-session-2 corpora under C2-RULE-1..5.

Reads nothing but the pre-registration's rules and the network. Writes corpus-2.json.
Run BEFORE any date signal is collected; the output is committed before collect_signals_2.py
exists, so the selection cannot be tuned to the result.

C2-RULE-2  links come from the seed's main content region: first "<main" .. last "</main>",
           whole document if no <main> exists.
C2-RULE-3  same-host hrefs; drop query+fragment+trailing slash; drop the seed, /search*, and
           the listed non-HTML extensions; document order, first occurrence wins.
C2-RULE-4  cap 40; fewer than 15 -> that authority is reported inconclusive, never re-scoped.
C2-RULE-5  the same extractor is run once on the EC seed and the overlap with the locked
           session-94 corpus is reported. The EC corpus itself is NOT altered.
"""

from __future__ import annotations

import datetime as dt
import html as htmllib
import json
import re
import subprocess
from urllib.parse import urljoin, urlsplit, urlunsplit

UA = "Mozilla/5.0 (compatible; field-research/1.0; public-interest measurement)"
CAP = 40
FLOOR = 15
DROP_EXT = (".pdf", ".xml", ".csv", ".json", ".zip", ".jpg", ".jpeg", ".png", ".svg", ".gif")

SEEDS = {
    "GOVUK": "https://www.gov.uk/government/organisations/ai-security-institute",  # amendment 1
    "NIST": "https://www.nist.gov/artificial-intelligence",
    # amendment 2: first candidate of five passing (a) 200 (b) XML sitemap (c) no interstitial
    "IE": "https://enterprise.gov.ie/en/what-we-do/innovation-research-development/artificial-intelligence/",
}
EC_SEED = "https://digital-strategy.ec.europa.eu/en/policies/regulatory-framework-ai"

HREF_RE = re.compile(r"""<a\b[^>]*?\bhref\s*=\s*["']([^"']+)["']""", re.I | re.S)
MAIN_OPEN_RE = re.compile(r"<main\b", re.I)


def get(url: str, timeout: int = 60) -> dict:
    proc = subprocess.run(
        ["curl", "-sS", "-L", "-A", UA, "--max-time", str(timeout), "-w", "\n%{http_code}", url],
        capture_output=True, text=True, errors="replace",
    )
    if proc.returncode != 0:
        return {"ok": False, "error": f"curl exit {proc.returncode}: {proc.stderr.strip()[:200]}"}
    body, _, code = proc.stdout.rpartition("\n")
    return {"ok": True, "status": int(code or 0), "body": body}


def main_region(page: str) -> tuple[str, str]:
    """C2-RULE-2. Returns (region, which) where which is 'main' or 'document'."""
    m = MAIN_OPEN_RE.search(page)
    if not m:
        return page, "document"
    end = page.rfind("</main")
    if end == -1 or end <= m.start():
        return page, "document"
    return page[m.start():end], "main"


def normalise(url: str) -> str:
    s = urlsplit(url)
    path = s.path.rstrip("/") or "/"
    return urlunsplit((s.scheme or "https", s.netloc, path, "", ""))


def extract(seed: str, page: str) -> dict:
    region, which = main_region(page)
    host = urlsplit(seed).netloc
    seed_key = normalise(seed)
    kept: list[str] = []
    seen: set[str] = set()
    rejected: dict[str, int] = {}

    def reject(reason: str) -> None:
        rejected[reason] = rejected.get(reason, 0) + 1

    for raw in HREF_RE.findall(region):
        href = htmllib.unescape(raw.strip())
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            reject("non-http-scheme")
            continue
        absolute = urljoin(seed, href)
        s = urlsplit(absolute)
        if s.scheme not in ("http", "https"):
            reject("non-http-scheme")
            continue
        if s.netloc != host:
            reject("other-host")
            continue
        key = normalise(absolute)
        if key == seed_key:
            reject("seed-itself")
            continue
        if s.path.startswith("/search"):
            reject("search-path")
            continue
        if s.path.lower().endswith(DROP_EXT):
            reject("non-html-extension")
            continue
        if key in seen:
            reject("duplicate")
            continue
        seen.add(key)
        kept.append(key)
    return {"region": which, "candidates": len(kept), "urls": kept, "rejected": rejected}


def main() -> int:
    run = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    out = {
        "instrument": "as-of-today",
        "stage": "corpus, proof session 2",
        "preregistration": "PREREGISTRATION-2.md",
        "extracted_utc": run,
        "cap": CAP,
        "floor": FLOOR,
        "authorities": {},
    }

    # amendment 4: chrome (links also on https://<host>/) is filtered at selection, before the cap
    for key, seed in SEEDS.items():
        r = get(seed)
        if not r.get("ok") or r["status"] != 200:
            out["authorities"][key] = {
                "seed": seed, "fetch": "FAILED",
                "status": r.get("status", 0), "error": r.get("error"),
            }
            continue
        ex = extract(seed, r["body"])
        host = urlsplit(seed).netloc
        hr = get(f"https://{host}/")
        chrome: set[str] = set()
        if hr.get("ok") and hr["status"] == 200:
            chrome = set(extract(f"https://{host}/", hr["body"])["urls"])
        chrome.add(normalise(f"https://{host}/"))
        arm_a = ex["urls"][:CAP]
        corpus = [u for u in ex["urls"] if u not in chrome][:CAP]
        out["authorities"][key] = {
            "seed": seed,
            "fetch": "OK",
            "seed_bytes": len(r["body"]),
            "link_region": ex["region"],
            "candidates_after_rules": ex["candidates"],
            "rejected_counts": ex["rejected"],
            "home_page_links": len(chrome),
            "arm_a_corpus_size": len(arm_a),
            "arm_a_corpus": arm_a,
            "chrome_in_arm_a": sum(1 for u in arm_a if u in chrome),
            "corpus_size": len(corpus),
            "inconclusive_by_c2_rule_4": len(corpus) < FLOOR,
            "corpus": corpus,
        }

    # C2-RULE-5 — the control on the rule change. Measures, does not alter.
    r = get(EC_SEED)
    control: dict = {"seed": EC_SEED, "purpose": "C2-RULE-5: cost of the link-region rule change"}
    if r.get("ok") and r["status"] == 200:
        ex = extract(EC_SEED, r["body"])
        c2_ec = ex["urls"][:CAP]
        locked = [normalise(u) for u in json.load(open("corpus.json"))["corpus"]]
        inter = [u for u in c2_ec if u in set(locked)]
        control.update({
            "fetch": "OK",
            "link_region": ex["region"],
            "c2_corpus_size": len(c2_ec),
            "locked_corpus_size": len(locked),
            "overlap": len(inter),
            "overlap_share_of_locked": round(len(inter) / len(locked), 4) if locked else None,
            "c2_only": [u for u in c2_ec if u not in set(locked)],
            "locked_only": [u for u in locked if u not in set(c2_ec)],
        })
    else:
        control.update({"fetch": "FAILED", "status": r.get("status", 0), "error": r.get("error")})
    out["ec_rule_change_control"] = control

    with open("corpus-2.json", "w") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    for key, a in out["authorities"].items():
        print(f"{key}: {a.get('corpus_size', 0)} urls (region={a.get('link_region')}, "
              f"candidates={a.get('candidates_after_rules')})")
    c = out["ec_rule_change_control"]
    print(f"EC control: overlap {c.get('overlap')} of {c.get('locked_corpus_size')} locked")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
