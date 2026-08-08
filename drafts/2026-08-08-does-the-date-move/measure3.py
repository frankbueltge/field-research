"""Increment 3 — executes PREREGISTRATION-3.md exactly. Writes observations-3.json.

Two archived captures per document page (the census's first/last 200-status capture in the
24-month window, span >= 30 days). Per capture: the printed date V by an explicit per-authority
selector, and the content text of the authority's content container with every date-shaped string
removed. The date removal is the anti-circularity rule of the pre-registration: a page whose only
change is its date must not be scorable as a content change.

The gzip/deflate handling is increment 1's defect-D1 fix, by magic bytes, not by header trust.
"""
import json, re, sys, time, gzip, zlib, hashlib, difflib, datetime as dt
import urllib.request, urllib.error
from html.parser import HTMLParser

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
DELAY = 1.5

MONTHS = ("January|February|March|April|May|June|July|August|September|October|November|December")
DATE_PATTERNS = [
    re.compile(rf"\b(?:{MONTHS})\s+\d{{1,2}},\s*\d{{4}}\b"),
    re.compile(rf"\b\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}}\b"),
    re.compile(r"\b\d{4}-\d{2}-\d{2}\b"),
]
HEXTOK = re.compile(r"\b[0-9a-fA-F]{16,}\b")
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "area", "base",
        "col", "embed", "param", "track", "wbr"}

# ---- per-authority selectors, fixed in PREREGISTRATION-3.md -------------------------------

def container_nist(tag, at):
    c = at.get("class", "")
    return tag == "div" and "nist-page__region--content" in c and "content-top" not in c and "content-bottom" not in c

def container_epa(tag, at):
    return tag == "main" and at.get("id") == "main"

def container_govuk(tag, at):
    return tag == "main" and at.get("id") == "content"

def drop_common(tag, at):
    return tag in ("script", "style", "nav", "form")

def drop_nist(tag, at):
    return drop_common(tag, at) or "font-sans-2xs" in at.get("class", "")

def drop_epa(tag, at):
    return drop_common(tag, at) or "l-page__footer-last-updated" in at.get("class", "")

def drop_govuk(tag, at):
    c = at.get("class", "")
    return drop_common(tag, at) or any(k in c for k in
        ("gem-c-metadata", "gem-c-published-dates", "full-publication-update-history"))

NIST_V = re.compile(rf"Created\s+((?:{MONTHS})\s+\d{{1,2}},\s*\d{{4}})\s*,\s*Updated\s+((?:{MONTHS})\s+\d{{1,2}},\s*\d{{4}})")
EPA_V = re.compile(r"Last updated on\s+([^<\n]{4,40}?)\s*(?:<|$)")
GOVUK_CHANGE = re.compile(r'class="[^"]*gem-c-published-dates__change-date[^"]*"[^>]*datetime="([^"]+)"')
GOVUK_NOTE = re.compile(r'class="[^"]*gem-c-published-dates__change-note[^"]*"[^>]*>(.*?)</p>', re.S)
GOVUK_PUB = re.compile(rf"Published\s+(\d{{1,2}}\s+(?:{MONTHS})\s+\d{{4}})")

AUTH = {
    "nist": {"container": container_nist, "drop": drop_nist},
    "epa": {"container": container_epa, "drop": drop_epa},
    "govuk": {"container": container_govuk, "drop": drop_govuk},
}

# ---- html -> text of one container, with drops -------------------------------------------


class Collector(HTMLParser):
    def __init__(self, want, drop):
        super().__init__(convert_charrefs=True)
        self.want, self.drop = want, drop
        self.stack, self.out = [], []
        self.in_target = False
        self.found = False
        self.drop_depth = 0

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        at = {k: (v or "") for k, v in attrs}
        is_t = (not self.found) and self.want(tag, at)
        is_d = self.drop(tag, at)
        self.stack.append((tag, is_t, is_d))
        if is_t:
            self.in_target, self.found = True, True
        if is_d:
            self.drop_depth += 1

    def handle_startendtag(self, tag, attrs):
        return

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, is_t, is_d in self.stack[i:]:
                    if is_d:
                        self.drop_depth -= 1
                    if is_t:
                        self.in_target = False
                del self.stack[i:]
                return

    def handle_data(self, data):
        if self.in_target and self.drop_depth == 0:
            self.out.append(data)


def content_text(page, auth):
    c = Collector(AUTH[auth]["container"], AUTH[auth]["drop"])
    try:
        c.feed(page)
    except Exception:                                   # noqa: BLE001 - malformed markup is data
        pass
    if not c.found:
        return None
    t = " ".join(c.out)
    t = HEXTOK.sub(" ", t)
    for p in DATE_PATTERNS:
        t = p.sub(" ", t)
    return re.sub(r"\s+", " ", t).strip()


def norm_date(s):
    if not s:
        return None
    return re.sub(r"\s+", " ", s.strip().rstrip(".")).strip()


def extract_v(page, auth):
    """Returns (v_scored, detail dict). Selectors are exactly those fixed in the pre-registration."""
    if auth == "nist":
        m = NIST_V.search(page)
        if not m:
            txt = re.sub(r"<[^>]+>", " ", page)
            m = NIST_V.search(re.sub(r"\s+", " ", txt))
        if m:
            return norm_date(m.group(2)), {"v_created": norm_date(m.group(1)), "rule": "nist Created/Updated"}
        return None, {"rule": "nist Created/Updated NOT FOUND"}
    if auth == "epa":
        m = EPA_V.search(page)
        if m:
            v = norm_date(re.sub(r"<[^>]+>", "", m.group(1)))
            return v, {"rule": "epa l-page__footer-last-updated"}
        return None, {"rule": "epa last-updated NOT FOUND"}
    if auth == "govuk":
        changes = sorted(set(GOVUK_CHANGE.findall(page)))
        pub = GOVUK_PUB.search(page)
        notes = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", n)).strip() for n in GOVUK_NOTE.findall(page)]
        det = {"rule": "govuk latest change-date else published",
               "changes": changes, "notes": notes[:40],
               "v_published": norm_date(pub.group(1)) if pub else None}
        if changes:
            return changes[-1][:10], det
        if pub:
            det["rule"] += " (no change dates; published used)"
            return norm_date(pub.group(1)), det
        return None, det
    raise ValueError(auth)


# ---- fetching ----------------------------------------------------------------------------

def decode_body(raw, enc):
    if raw[:2] == b"\x1f\x8b":
        try:
            return gzip.decompress(raw)
        except Exception:                               # noqa: BLE001
            return raw
    if enc and "deflate" in enc.lower():
        for wbits in (-15, 15):
            try:
                return zlib.decompress(raw, wbits)
            except Exception:                           # noqa: BLE001
                continue
    return raw


def fetch(url, timeout=90, tries=2):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                hdr = {k.lower(): v for k, v in r.headers.items()}
                return r.status, decode_body(r.read(), hdr.get("content-encoding"))
        except Exception as e:                          # noqa: BLE001
            last = e
            time.sleep(3 * (i + 1))
    raise last


def observe(url, ts, auth):
    st, body = fetch(f"https://web.archive.org/web/{ts}id_/{url}")
    page = body.decode("utf-8", "replace")
    v, det = extract_v(page, auth)
    txt = content_text(page, auth)
    return {
        "timestamp": ts, "http_status": st, "bytes": len(body),
        "v": v, "v_detail": det,
        "container_found": txt is not None,
        "text_sha256": hashlib.sha256(txt.encode()).hexdigest() if txt is not None else None,
        "text_len": len(txt) if txt is not None else None,
        "_text": txt,
    }


def main():
    census = json.load(open(f"{BASE}/census.json"))
    plan = []
    for auth, n in (("nist", 40), ("epa", 40), ("govuk", 30)):
        rows = [r for r in census["authorities"][auth] if r.get("pairable")][:n]
        plan += [(auth, r) for r in rows]

    out = {"instrument": "does-the-date-move / increment 3 (V arm)",
           "preregistration": "PREREGISTRATION-3.md, committed before this file existed",
           "run_started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
           "planned": len(plan), "urls": []}

    for i, (auth, row) in enumerate(plan, 1):
        rec = {"authority": auth, "url": row["url"], "from": row["first"], "to": row["last"],
               "span_days": row["span_days"], "status": None, "errors": []}
        obs = {}
        for side, ts in (("a", row["first"]), ("b", row["last"])):
            try:
                obs[side] = observe(row["url"], ts, auth)
            except Exception as e:                      # noqa: BLE001
                rec["errors"].append({"side": side, "ts": ts, "error": repr(e)})
            time.sleep(DELAY)
        if len(obs) < 2:
            rec["status"] = "UNMEASURED-FETCH-FAILED"
            print(f"[{i}/{len(plan)}] FAIL {auth} {row['url'][-52:]}", flush=True)
            out["urls"].append(rec)
            json.dump(out, open(f"{BASE}/observations-3-partial.json", "w"), indent=1)
            continue

        a, b = obs["a"], obs["b"]
        rec["status"] = "MEASURED"
        rec["a"] = {k: v for k, v in a.items() if k != "_text"}
        rec["b"] = {k: v for k, v in b.items() if k != "_text"}
        if a["_text"] is None or b["_text"] is None:
            rec["content"] = "UNSCORABLE-NO-CONTAINER"
            rec["ratio"] = None
        else:
            ratio = difflib.SequenceMatcher(None, a["_text"], b["_text"]).ratio()
            rec["ratio"] = round(ratio, 6)
            rec["content"] = ("IDENTICAL" if a["text_sha256"] == b["text_sha256"]
                              else "TRIVIAL" if ratio >= 0.98 else "SUBSTANTIVE")
        if a["v"] is None or b["v"] is None:
            rec["v"] = "UNSCORABLE"
        else:
            rec["v"] = "MOVED" if a["v"] != b["v"] else "STILL"
        rec["_text_a"], rec["_text_b"] = a["_text"], b["_text"]
        print(f"[{i}/{len(plan)}] {auth} {rec['content']:<22} V={rec['v']:<10} "
              f"{str(a['v'])[:12]:<12}->{str(b['v'])[:12]:<12} {row['url'][-40:]}", flush=True)
        out["urls"].append(rec)
        json.dump(out, open(f"{BASE}/observations-3-partial.json", "w"), indent=1)

    out["run_finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
    # texts kept in a separate file for the hand-check; scored file stays readable
    texts = {r["url"]: {"a": r.pop("_text_a", None), "b": r.pop("_text_b", None)}
             for r in out["urls"] if "_text_a" in r or "_text_b" in r}
    json.dump(out, open(f"{BASE}/observations-3.json", "w"), indent=1)
    json.dump(texts, open(f"{BASE}/texts-3.json", "w"), indent=1)
    print("WROTE observations-3.json", flush=True)


main()
