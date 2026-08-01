#!/usr/bin/env python3
"""
Layers 1, 2 and 3 — the dated, fenced live probe.

Nothing this script writes is an assertion about the world. It is a record of what one
vantage saw on one day. The vantage is a datacenter address behind a forward proxy, not a
reader's browser, and that shows up in the results as its own classes.

  L1  does the cited URL resolve, and where does it land
  L2  does a public web archive hold captures of it, and one at or before the date the
      register recorded downloading the document
  L3  for URLs that answer with a body: does the live page still contain the passage the
      register stored — scored against the one-way fingerprint, never against stored text

Usage:
    python3 probe.py --out probe-2026-08-01.json [--limit N] [--only L1,L2,L3]
"""

import argparse
import concurrent.futures as cf
import html.parser
import json
import os
import re
import sys
import time
import urllib.parse

import requests

HERE = os.path.dirname(os.path.abspath(__file__))
SHINGLE_N = 8
SHINGLE_HASH_HEX = 12

# Disclosed, not concealed: the census identifies as a current desktop browser, because the
# comparison literature does and because a self-identifying crawler string changes what
# servers return. Every non-200 is then retried once with the honest string below, so the
# difference is measured instead of assumed.
UA_BROWSER = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/126.0.0.0 Safari/537.36")
UA_HONEST = "MeridianCitationCensus/1.0 (research measurement of citation durability)"

TIMEOUT = 25
MAX_BYTES = 3_000_000
LIVE_WORKERS = 8
CDX_WORKERS = 3
CDX_DELAY = 0.6


class TextExtractor(html.parser.HTMLParser):
    SKIP = {"script", "style", "noscript", "svg", "template", "head"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.depth = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.depth += 1

    def handle_endtag(self, tag):
        if tag in self.SKIP and self.depth:
            self.depth -= 1

    def handle_data(self, data):
        if not self.depth:
            self.parts.append(data)

    def text(self):
        return " ".join(self.parts)


# Strings that appear on interstitial challenge / refusal pages served with status 200.
# Used only in combination with a very short extracted text, so that an article ABOUT
# captchas is not mistaken for a captcha.
BOT_MARKERS = [
    "just a moment", "enable javascript and cookies", "checking your browser",
    "attention required", "access denied", "unusual traffic", "are you a robot",
    "verify you are a human", "please enable js", "ddos protection", "captcha",
    "request unsuccessful", "incident id", "reference #",
]

WORD_RE = re.compile(r"[a-z0-9]+")


def normalise_words(text):
    return WORD_RE.findall(text.lower())


def live_shingle_hashes(text):
    import hashlib
    w = normalise_words(text)
    if len(w) < SHINGLE_N:
        return set(), len(w)
    out = set()
    for i in range(len(w) - SHINGLE_N + 1):
        s = " ".join(w[i:i + SHINGLE_N])
        out.add(hashlib.sha1(s.encode("utf-8")).hexdigest()[:SHINGLE_HASH_HEX])
    return out, len(w)


def unpack(packed):
    n = SHINGLE_HASH_HEX
    return {packed[i:i + n] for i in range(0, len(packed), n)}


def path_of(u):
    try:
        p = urllib.parse.urlsplit(u)
        return p.path or "/"
    except ValueError:
        return "/"


def fetch(url, ua):
    """One live GET. Returns a record; never raises."""
    rec = {"ua": "browser" if ua == UA_BROWSER else "self_identifying"}
    t0 = time.time()
    try:
        r = requests.get(url, headers={"User-Agent": ua,
                                       "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
                                       "Accept-Language": "en;q=0.9"},
                         timeout=TIMEOUT, allow_redirects=True, stream=True)
        body = b""
        for chunk in r.iter_content(65536):
            body += chunk
            if len(body) >= MAX_BYTES:
                break
        rec.update({
            "outcome": "response",
            "status": r.status_code,
            "final_url": r.url,
            "redirects": len(r.history),
            "content_type": (r.headers.get("Content-Type") or "").split(";")[0].strip().lower(),
            "bytes_read": len(body),
            "elapsed_s": round(time.time() - t0, 2),
        })
        rec["_body"] = body
        try:
            r.close()
        except Exception:
            pass
    except requests.exceptions.SSLError as e:
        rec.update({"outcome": "tls_error", "error": str(e)[:300]})
    except requests.exceptions.ConnectTimeout:
        rec.update({"outcome": "connect_timeout"})
    except requests.exceptions.ReadTimeout:
        rec.update({"outcome": "read_timeout"})
    except requests.exceptions.TooManyRedirects:
        rec.update({"outcome": "too_many_redirects"})
    except requests.exceptions.ConnectionError as e:
        msg = str(e)
        kind = "dns_error" if ("Name or service not known" in msg or "nodename nor servname" in msg
                               or "Failed to resolve" in msg or "getaddrinfo" in msg) else "connection_error"
        rec.update({"outcome": kind, "error": msg[:300]})
    except Exception as e:
        rec.update({"outcome": "other_error", "error": f"{type(e).__name__}: {str(e)[:280]}"})
    rec.setdefault("elapsed_s", round(time.time() - t0, 2))
    return rec


def classify_l1(rec, original_url):
    """The L1 class. 'Resolves' is not the same as 'answers 200'."""
    if rec["outcome"] != "response":
        return {"tls_error": "TLS_ERROR", "connect_timeout": "TIMEOUT", "read_timeout": "TIMEOUT",
                "too_many_redirects": "REDIRECT_LOOP", "dns_error": "DNS_FAIL",
                "connection_error": "CONNECT_FAIL"}.get(rec["outcome"], "OTHER_ERROR")
    s = rec["status"]
    if s == 200:
        op, fp = path_of(original_url), path_of(rec["final_url"])
        if fp in ("", "/") and op not in ("", "/"):
            return "REDIRECT_TO_ROOT"
        return "HTTP_200"
    if s in (401, 402, 403, 451):
        return "HTTP_%d" % s          # withheld from this vantage, not necessarily gone
    if s == 404 or s == 410:
        return "HTTP_%d" % s
    if 400 <= s < 500:
        return "HTTP_4XX"
    if 500 <= s < 600:
        return "HTTP_5XX"
    return "HTTP_OTHER"


def probe_l1_l3(item, fps):
    url = item["url"]
    rec = fetch(url, UA_BROWSER)
    out = {"report_number": item["report_number"], "url": url,
           "primary": {k: v for k, v in rec.items() if k != "_body"}}
    out["l1_class"] = classify_l1(rec, url)

    # A non-200 gets one honest-string retry, so a bot wall can be told from a dead document.
    if out["l1_class"] not in ("HTTP_200", "REDIRECT_TO_ROOT"):
        time.sleep(0.2)
        rec2 = fetch(url, UA_HONEST)
        out["retry_self_identifying"] = {k: v for k, v in rec2.items() if k != "_body"}
        out["retry_l1_class"] = classify_l1(rec2, url)

    # L3 asks what a page that ANSWERS still says. A page that refused, errored or was
    # withheld from this vantage has nothing to compare, and scoring it would manufacture
    # a zero out of a refusal.
    body = rec.get("_body")
    if body is None or out["l1_class"] not in ("HTTP_200", "REDIRECT_TO_ROOT"):
        out["l3_class"] = "NOT_APPLICABLE"
        return out

    ctype = rec.get("content_type", "")
    if ctype and not (ctype.startswith("text/") or "html" in ctype or "xml" in ctype):
        out["l3_class"] = "NON_HTML"
        out["l3"] = {"content_type": ctype}
        return out

    try:
        text_raw = body.decode("utf-8", errors="replace")
    except Exception:
        out["l3_class"] = "UNDECODABLE"
        return out

    p = TextExtractor()
    try:
        p.feed(text_raw)
    except Exception:
        pass
    live_text = p.text()
    live_hashes, live_words = live_shingle_hashes(live_text)

    fp = fps.get(item["report_number"])
    held = unpack(fp["shingle_hashes_packed"]) if fp else set()
    overlap = (len(held & live_hashes) / len(held)) if held else None

    out["l3"] = {
        "live_words_extracted": live_words,
        "live_unique_shingles": len(live_hashes),
        "held_unique_shingles": len(held),
        "held_shingles_found_live": len(held & live_hashes),
        "overlap": round(overlap, 4) if overlap is not None else None,
    }
    lowered = live_text.lower()
    markers = [m for m in BOT_MARKERS if m in lowered]

    if item.get("flag_register_declares_stand_in"):
        # The register says itself that what it stores is not a copy of this document.
        out["l3_class"] = "REGISTER_STAND_IN"
    elif not held:
        out["l3_class"] = "NO_HELD_TEXT"
    elif live_words < 300 and markers:
        # A challenge or refusal page served with status 200. Not the document, and not
        # evidence the document is gone — evidence that this vantage was not admitted.
        out["l3_class"] = "BOT_WALL"
        out["l3"]["bot_markers"] = markers
    elif live_words < 100:
        out["l3_class"] = "SHELL"        # answered, but served almost no readable text here
    elif overlap >= 0.50:
        out["l3_class"] = "HOLDS"
    elif overlap >= 0.10:
        out["l3_class"] = "PARTIAL"
    else:
        out["l3_class"] = "ABSENT"
    return out


CDX = "https://web.archive.org/cdx/search/cdx"


def probe_l2(item):
    url = item["url"]
    params = {"url": url, "output": "json", "fl": "timestamp,statuscode",
              "collapse": "timestamp:6", "limit": "400"}
    rec = {"report_number": item["report_number"], "url": url}
    try:
        r, last = None, None
        for attempt in range(4):          # the capture index rate-limits; back off rather than
            try:                          # record a refusal as an absence of captures
                r = requests.get(CDX, params=params, headers={"User-Agent": UA_HONEST},
                                 timeout=TIMEOUT)
                if r.status_code == 200:
                    break
                last = "status %d" % r.status_code
            except Exception as e:
                last, r = f"{type(e).__name__}", None
            time.sleep(2 * (attempt + 1))
        rec["cdx_attempts"] = attempt + 1
        if r is None or r.status_code != 200:
            rec["cdx_status"] = r.status_code if r is not None else None
            rec["l2_class"] = "CDX_UNAVAILABLE"
            rec["error"] = last
            return rec
        rec["cdx_status"] = r.status_code
        rows = r.json() if r.text.strip() else []
        rows = rows[1:] if rows and rows[0] and rows[0][0] == "timestamp" else rows
        stamps = [row[0] for row in rows if row and row[0]]
        codes = [row[1] for row in rows if len(row) > 1]
        rec["capture_months"] = len(stamps)
        rec["capture_stamps"] = stamps
        rec["first_capture"] = min(stamps) if stamps else None
        rec["last_capture"] = max(stamps) if stamps else None
        rec["captures_with_status_200"] = sum(1 for c in codes if c == "200")
        dl = (item.get("date_downloaded") or "").replace("-", "").replace(":", "")[:8]
        if stamps and dl and len(dl) == 8:
            rec["capture_at_or_before_register_download"] = any(s[:8] <= dl for s in stamps)
        else:
            rec["capture_at_or_before_register_download"] = None
        rec["l2_class"] = "CAPTURED" if stamps else "NO_CAPTURE"
    except Exception as e:
        rec["l2_class"] = "CDX_ERROR"
        rec["error"] = f"{type(e).__name__}: {str(e)[:200]}"
    return rec


def probe_l3_calibration(item, fps, cdx_rec):
    """L3c — the control on our own extractor.

    The Skeptic's blocking objection: a low overlap between the register's stored copy and
    a page we extract today cannot, by itself, tell drift from a mismatch between two
    extraction pipelines. So take the page out of the equation. Fetch the archived capture
    closest to (and not after) the date the register recorded downloading the document, run
    it through the SAME extractor, and score it against the SAME fingerprint.

      archived copy scores high, live page scores low  -> the loss is on the live web
      archived copy also scores low                    -> the mismatch is ours or the
                                                          register's, and predates today
    """
    rec = {"report_number": item["report_number"]}
    stamps = cdx_rec.get("capture_stamps") or []
    dl = (item.get("date_downloaded") or "").replace("-", "")[:8]
    if not stamps:
        rec["l3c_class"] = "NO_CAPTURE"
        return rec
    before = [s for s in stamps if dl and s[:8] <= dl]
    chosen = max(before) if before else None
    if chosen is None:
        rec["l3c_class"] = "NO_CAPTURE_BEFORE_DOWNLOAD"
        rec["earliest_capture"] = min(stamps)
        return rec
    rec["capture_used"] = chosen
    # `id_` asks the archive for the stored bytes without its own banner injected.
    u = f"https://web.archive.org/web/{chosen}id_/{item['url']}"
    r = fetch(u, UA_HONEST)
    if r["outcome"] != "response" or r.get("status") != 200 or r.get("_body") is None:
        rec["l3c_class"] = "ARCHIVE_FETCH_FAILED"
        rec["detail"] = {k: v for k, v in r.items() if k != "_body"}
        return rec
    p = TextExtractor()
    try:
        p.feed(r["_body"].decode("utf-8", errors="replace"))
    except Exception:
        pass
    live_hashes, words = live_shingle_hashes(p.text())
    fp = fps.get(item["report_number"])
    held = unpack(fp["shingle_hashes_packed"]) if fp else set()
    ov = (len(held & live_hashes) / len(held)) if held else None
    rec["archived_words_extracted"] = words
    rec["overlap_archived_vs_held"] = round(ov, 4) if ov is not None else None
    if ov is None:
        rec["l3c_class"] = "NO_HELD_TEXT"
    elif ov >= 0.50:
        rec["l3c_class"] = "ARCHIVED_COPY_HOLDS"
    elif ov >= 0.10:
        rec["l3c_class"] = "ARCHIVED_COPY_PARTIAL"
    else:
        rec["l3c_class"] = "ARCHIVED_COPY_ABSENT"
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--only", default="L1,L2,L3")
    args = ap.parse_args()

    sample = json.load(open(os.path.join(HERE, "sample.json"), encoding="utf-8"))
    fps = json.load(open(os.path.join(HERE, "fingerprints.json"), encoding="utf-8"))["fingerprints"]
    items = sample["reports"][: args.limit] if args.limit else sample["reports"]
    want = set(args.only.split(","))

    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    live, arch = [], []

    if "L1" in want or "L3" in want:
        with cf.ThreadPoolExecutor(LIVE_WORKERS) as ex:
            futs = {ex.submit(probe_l1_l3, it, fps): it for it in items}
            for i, f in enumerate(cf.as_completed(futs), 1):
                live.append(f.result())
                if i % 25 == 0:
                    print(f"  live {i}/{len(items)}", flush=True)
    if "L2" in want:
        def one(it):
            time.sleep(CDX_DELAY)
            return probe_l2(it)
        with cf.ThreadPoolExecutor(CDX_WORKERS) as ex:
            for i, r in enumerate(ex.map(one, items), 1):
                arch.append(r)
                if i % 25 == 0:
                    print(f"  archive {i}/{len(items)}", flush=True)

    # L3c — the control, run only where it can decide something: every case where the live
    # page did not clearly still hold the stored passage.
    calib = []
    if "L3" in want and "L2" in want:
        by_num = {r["report_number"]: r for r in arch}
        need = [it for it in items
                if next((l for l in live if l["report_number"] == it["report_number"]), {})
                .get("l3_class") in ("ABSENT", "PARTIAL", "SHELL", "BOT_WALL", "NOT_APPLICABLE",
                                     "NON_HTML", "UNDECODABLE")]
        print(f"  calibration targets: {len(need)}", flush=True)

        def onec(it):
            time.sleep(CDX_DELAY)
            return probe_l3_calibration(it, fps, by_num.get(it["report_number"], {}))
        with cf.ThreadPoolExecutor(CDX_WORKERS) as ex:
            for i, r in enumerate(ex.map(onec, need), 1):
                calib.append(r)
                if i % 20 == 0:
                    print(f"  calibration {i}/{len(need)}", flush=True)

    live.sort(key=lambda r: int(r["report_number"]))
    arch.sort(key=lambda r: int(r["report_number"]))
    calib.sort(key=lambda r: int(r["report_number"]))
    doc = {
        "layer": "L1/L2/L3 — dated live probe, not an assertion about the world",
        "probe_started_utc": started,
        "probe_finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "vantage": "datacenter address behind a forward proxy; not a reader's browser",
        "user_agents": {"primary": UA_BROWSER, "retry_on_non_200": UA_HONEST},
        "timeout_s": TIMEOUT, "max_bytes_read": MAX_BYTES,
        "sample_seed": sample["seed"], "n": len(items),
        "l3_thresholds": {"HOLDS": ">=0.50", "PARTIAL": "0.10..0.50", "ABSENT": "<0.10",
                          "SHELL": "fewer than 100 words extractable from a 200 response",
                          "BOT_WALL": "fewer than 300 words plus a challenge-page marker",
                          "REGISTER_STAND_IN": "the register declares its stored text a placeholder"},
        "l3c": ("control layer: the archived capture nearest to and not after the register's "
                "recorded download date, run through the same extractor against the same "
                "fingerprint, to separate loss on the live web from a mismatch between "
                "extraction pipelines"),
        "live": live, "archive": arch, "calibration": calib,
    }
    with open(os.path.join(HERE, args.out), "w", encoding="utf-8") as fh:
        json.dump(doc, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    print("wrote", args.out, "live:", len(live), "archive:", len(arch))
    return 0


if __name__ == "__main__":
    sys.exit(main())
