"""Increment 2 — executes PREREGISTRATION-2.md exactly. Writes frames.json and census.json.

A coverage measurement, not a content measurement: one capture-index (CDX) query per sampled
document page, no payloads fetched. Frame rules, sample size and seed are fixed in
PREREGISTRATION-2.md and are not read from anywhere else.

Decode note carried over from increment 1's defect D1: every response body is decoded through
`decode_body` and asserted to parse as JSON before it is used. An instrument that compares
fetched bytes owes a check that it decoded them.
"""
import json, os, re, sys, time, gzip, zlib, random, collections, datetime as dt
import urllib.request, urllib.parse, urllib.error
from concurrent.futures import ThreadPoolExecutor

# Fetch schedule only, not the measurement: a single index query costs 8-14 s, and 336 of them
# in sequence do not fit in a session. Four workers, one query each, no retry storm. The value
# computed per URL is identical either way; nothing about the sample or the window changes.
WORKERS = 4

BASE = "/home/user/field-research/drafts/2026-08-08-does-the-date-move"
UA = "field-research/1.0 (non-commercial research; polite, rate-limited)"
SEED = 20260808
SAMPLE = 80
W24 = ("20240801", "20260731")
W12 = ("20250801", "20260731")


def decode_body(raw: bytes, enc: str | None) -> bytes:
    if raw[:2] == b"\x1f\x8b":
        return gzip.decompress(raw)
    if enc and "deflate" in enc.lower():
        for wbits in (-15, 15):
            try:
                return zlib.decompress(raw, wbits)
            except Exception:  # noqa: BLE001
                continue
    return raw


def get(url, timeout=90, tries=3, sleep=3.0):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as r:
                hdr = {k.lower(): v for k, v in r.headers.items()}
                return r.status, decode_body(r.read(), hdr.get("content-encoding"))
        except Exception as e:  # noqa: BLE001 - recorded, never silently swallowed
            last = e
            time.sleep(sleep * (i + 1))
    raise last


# ---------------------------------------------------------------- frames

def sitemap_pages(index_url, max_pages=60):
    _, body = get(index_url)
    txt = body.decode("utf-8", "replace")
    pages = re.findall(r"<loc>([^<]+)</loc>", txt)
    # a sitemap index lists further sitemaps; a flat sitemap lists content directly
    if pages and all(".xml" in p for p in pages[:3]):
        return pages[:max_pages]
    return [index_url]


def collect_sitemap(index_url, pattern, want=3000, max_pages=60):
    out, seen = [], set()
    for p in sitemap_pages(index_url, max_pages):
        try:
            _, body = get(p)
        except Exception as e:  # noqa: BLE001
            print("  frame page failed:", p, e, flush=True)
            continue
        txt = body.decode("utf-8", "replace")
        for loc in re.findall(r"<loc>([^<]+)</loc>", txt):
            if pattern.match(loc) and loc not in seen:
                seen.add(loc)
                out.append(loc)
        print(f"  {p} -> {len(out)} matching so far", flush=True)
        if len(out) >= want:
            break
        time.sleep(0.5)
    return out


def collect_govuk(want=1000):
    out, seen, start = [], set(), 0
    while len(out) < want and start < 2000:
        q = urllib.parse.urlencode({
            "count": "100", "start": str(start), "fields": "link",
            "filter_content_store_document_type": "guidance",
        })
        st, body = get("https://www.gov.uk/api/search.json?" + q)
        j = json.loads(body)
        res = j.get("results", [])
        if not res:
            break
        for r in res:
            link = r.get("link", "")
            if link.startswith("/government/publications/") and link.count("/") >= 3:
                u = "https://www.gov.uk" + link
                if u not in seen:
                    seen.add(u)
                    out.append(u)
        start += 100
        print(f"  gov.uk start={start} -> {len(out)} matching", flush=True)
        time.sleep(0.5)
    return out


def build_frames():
    frames = {}
    print("NIST", flush=True)
    frames["nist"] = collect_sitemap(
        "https://www.nist.gov/sitemap.xml",
        re.compile(r"^https://www\.nist\.gov/publications/[^/?#]+$"))
    print("EPA", flush=True)
    frames["epa"] = collect_sitemap(
        "https://www.epa.gov/sitemap.xml",
        re.compile(r"^https://www\.epa\.gov/newsreleases/[^/?#]+$"))
    print("GOV.UK", flush=True)
    frames["govuk"] = collect_govuk()
    print("ENERGY (admitted only if >= 200)", flush=True)
    energy = collect_sitemap(
        "https://www.energy.gov/sitemap.xml",
        re.compile(r"^https://www\.energy\.gov/articles/[^/?#]+$"), want=1000, max_pages=25)
    frames["energy_candidate_n"] = len(energy)
    if len(energy) >= 200:
        frames["energy"] = energy
    print("RECEIVER standards.digital.gov (whole)", flush=True)
    frames["receiver"] = collect_sitemap(
        "https://standards.digital.gov/sitemap.xml", re.compile(r"^https://"), want=10000)
    return frames


def sample(frame, n=SAMPLE):
    frame = sorted(set(frame))
    if len(frame) <= n:
        return frame
    return sorted(random.Random(SEED).sample(frame, n))


# ---------------------------------------------------------------- census

def cdx(url):
    q = urllib.parse.urlencode({
        "url": url, "output": "json", "fl": "timestamp,statuscode,digest",
        "from": W24[0], "to": W24[1], "filter": "statuscode:200", "limit": "1000",
    })
    st, body = get("https://web.archive.org/cdx/search/cdx?" + q)
    s = body.decode("utf-8", "replace").strip()
    if not s:
        return []
    rows = json.loads(s)
    return rows[1:] if rows else []


def measure(url):
    rec = {"url": url}
    try:
        rows = cdx(url)
    except Exception as e:  # noqa: BLE001
        rec["error"] = f"{type(e).__name__}: {e}"
        return rec
    ts = sorted(r[0] for r in rows)
    rec["n24"] = len(ts)
    rec["truncated"] = len(ts) >= 1000
    in12 = [t for t in ts if W12[0] <= t[:8] <= W12[1]]
    rec["n12"] = len(in12)
    rec["months24"] = len({t[:6] for t in ts})
    rec["months12"] = len({t[:6] for t in in12})
    rec["first"] = ts[0] if ts else None
    rec["last"] = ts[-1] if ts else None
    rec["pairable"] = False
    if len(ts) >= 2:
        a = dt.datetime.strptime(ts[0], "%Y%m%d%H%M%S")
        b = dt.datetime.strptime(ts[-1], "%Y%m%d%H%M%S")
        rec["pairable"] = (b - a).days >= 30
    rec["span_days"] = None
    if len(ts) >= 2:
        rec["span_days"] = (dt.datetime.strptime(ts[-1], "%Y%m%d%H%M%S")
                            - dt.datetime.strptime(ts[0], "%Y%m%d%H%M%S")).days
    return rec


def main():
    t0 = time.time()
    if os.path.exists(f"{BASE}/frames.json"):
        frames = json.load(open(f"{BASE}/frames.json"))
        print("frames reused from frames.json (built earlier this session)", flush=True)
    else:
        frames = build_frames()
        json.dump({k: v for k, v in frames.items()}, open(f"{BASE}/frames.json", "w"), indent=1)
    samples = {}
    # Order matters only for robustness, never for the measurement: the capture index is
    # idempotent and each URL's numbers are independent of every other. The receiver's own site
    # is measured first because P10 depends on it and it is the smallest; within an authority the
    # sampled URLs are processed in a seeded shuffle, so that if the run is cut short the
    # completed part is an unbiased subsample of the sample rather than its alphabetical head.
    for key in ("receiver", "nist", "epa", "govuk", "energy"):
        if key in frames and isinstance(frames[key], list):
            samples[key] = sample(frames[key], 10**9 if key == "receiver" else SAMPLE)
            print(f"{key}: frame {len(frames[key])} -> sample {len(samples[key])}", flush=True)
    out = {"generated_utc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
           "seed": SEED, "window24": W24, "window12": W12,
           "frame_sizes": {k: (len(v) if isinstance(v, list) else v) for k, v in frames.items()},
           "authorities": {}}
    cache = {}
    if os.path.exists(f"{BASE}/census-partial.json"):
        cache = json.load(open(f"{BASE}/census-partial.json"))
        print(f"resuming: {len(cache)} URLs already measured", flush=True)

    for key, urls in samples.items():
        urls = list(urls)
        random.Random(SEED).shuffle(urls)
        done = [0]

        def one(u, key=key):
            r = cache.get(u) or measure(u)
            cache[u] = r
            done[0] += 1
            if done[0] % 5 == 0:
                json.dump(cache, open(f"{BASE}/census-partial.json", "w"))
            print(f"[{key} {done[0]}/{len(urls)}] n12={r.get('n12')} m12={r.get('months12')} "
                  f"pairable={r.get('pairable')} {u}", flush=True)
            return r

        with ThreadPoolExecutor(max_workers=WORKERS) as ex:
            recs = list(ex.map(one, urls))
        json.dump(cache, open(f"{BASE}/census-partial.json", "w"))
        out["authorities"][key] = recs
        json.dump(out, open(f"{BASE}/census.json", "w"), indent=1)
    out["elapsed_s"] = round(time.time() - t0, 1)
    json.dump(out, open(f"{BASE}/census.json", "w"), indent=1)
    print("done in", out["elapsed_s"], "s", flush=True)


if __name__ == "__main__":
    main()
