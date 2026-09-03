#!/usr/bin/env python3
"""The sign and the door — re-probe the shipped door census under four arms.

Session 146, 2026-09-03. Design fixed in the artifact's PREREGISTRATION.md before
the measured probes were run.

Arms, per publisher (at most one request each, never concurrent, >= 2 s apart):

  R  the sign          GET https://<host>/robots.txt, honest identity
                       (repeated once with a browser identity only if refused)
  A  bare              GET <evidence_url>, honest identity, minimal headers
  B  complete          only if A refused: same identity, full browser header set
  U  unmarked          only if B refused: browser identity, full header set,
                       and only where the sign permits the path
  C  patient           only if A refused: exact repeat of A, after everything else

Usage:
  probe.py --run     write data/probes.json (network)
  probe.py --check   re-derive data/summary.json from data/probes.json and fail on drift
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CENSUS = ROOT / "artifacts/cycle-001/2026-09-01-a-door-to-knock-on/data/census.csv"
OUT = ROOT / "artifacts/cycle-001/2026-09-03-the-sign-and-the-door/data"

HONEST_UA = (
    "field-research-door-recheck/1.0 "
    "(+https://frankbueltge.de/field; research measurement; one request per page)"
)
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)
BROWSER_HEADERS = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language: en-US,en;q=0.9",
    "Accept-Encoding: gzip, deflate, br",
    "Upgrade-Insecure-Requests: 1",
    "Sec-Fetch-Dest: document",
    "Sec-Fetch-Mode: navigate",
    "Sec-Fetch-Site: none",
    "Sec-Fetch-User: ?1",
]
# Response headers kept, because they name the layer that refuses.
KEEP_HEADERS = (
    "server", "cf-ray", "cf-mitigated", "akamai-grn", "x-amzn-waf-action",
    "x-iinfo", "via", "retry-after", "x-cache", "content-type", "location",
    "x-served-by", "x-akamai-transformed",
)
GAP_SECONDS = 2.0
TIMEOUT = 25


def fetch(url, ua, full_headers, timeout=TIMEOUT, follow=False):
    """One GET. Returns a record; never raises for HTTP status."""
    cmd = [
        "curl", "-sS", "-D", "-", "-o", "/dev/null",
        "--max-time", str(timeout), "-A", ua, url,
    ]
    if follow:
        cmd[2:2] = ["-L"]
    if full_headers:
        for h in BROWSER_HEADERS:
            cmd[-1:-1] = ["-H", h]
    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True)
    elapsed = round((time.time() - t0) * 1000)
    rec = {"url": url, "elapsed_ms": elapsed, "status": None, "error": None, "headers": {}}
    if proc.returncode != 0:
        rec["error"] = (proc.stderr or "").strip()[:300] or f"curl exit {proc.returncode}"
    body = proc.stdout or ""
    # Skip the proxy's own CONNECT response block; the last status line is the origin's.
    statuses = re.findall(r"^HTTP/[\d.]+ (\d{3})", body, flags=re.M)
    if statuses:
        # With -L the last status line is the origin's final answer; the earlier ones are
        # the proxy's CONNECT and any redirects. Both are kept.
        rec["status"] = int(statuses[-1])
        rec["statuses"] = [int(s) for s in statuses]
    for line in body.splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            k = k.strip().lower()
            if k in KEEP_HEADERS and k not in rec["headers"]:
                rec["headers"][k] = v.strip()[:200]
    return rec


def fetch_body(url, ua, full_headers, timeout=TIMEOUT, limit=200000):
    cmd = ["curl", "-sS", "-L", "--compressed", "--max-time", str(timeout), "-A", ua, url]
    if full_headers:
        for h in BROWSER_HEADERS:
            cmd[-1:-1] = ["-H", h]
    proc = subprocess.run(cmd, capture_output=True)
    return (proc.stdout or b"").decode("utf-8", errors="replace")[:limit]


def parse_robots(text, path):
    """What the sign says. Returns (star_allows_path, named_allowed, named_disallowed)."""
    groups, current = [], None
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if not line or ":" not in line:
            continue
        field, _, value = line.partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if current is None or current["rules"]:
                current = {"agents": [], "rules": []}
                groups.append(current)
            current["agents"].append(value)
        elif field in ("allow", "disallow") and current is not None:
            current["rules"].append((field, value))
    named_allowed, named_disallowed = set(), set()
    star_allows = True
    for g in groups:
        blanket_block = any(f == "disallow" and v == "/" for f, v in g["rules"])
        any_allow = any(f == "allow" for f, v in g["rules"])
        for agent in g["agents"]:
            if agent == "*":
                star_allows = allows(g["rules"], path)
            elif blanket_block and not any_allow:
                named_disallowed.add(agent)
            else:
                named_allowed.add(agent)
    return star_allows, sorted(named_allowed), sorted(named_disallowed)


def rule_matches(pattern, path):
    """robots.txt path matching: * is any run of characters, a trailing $ anchors the end."""
    anchored = pattern.endswith("$")
    body = pattern[:-1] if anchored else pattern
    regex = "".join(".*" if ch == "*" else re.escape(ch) for ch in body)
    return re.match(regex + ("$" if anchored else ""), path) is not None


def allows(rules, path):
    """Longest matching rule wins; ties go to Allow (the common convention)."""
    best = None
    for field, value in rules:
        if value == "" or not rule_matches(value, path):
            continue
        length = len(value)
        if best is None or length > best[1] or (length == best[1] and field == "allow"):
            best = (field, length)
    return True if best is None else best[0] == "allow"


def refused(rec):
    """Refused = no 2xx, or a 2xx that is a bot challenge rather than the page."""
    h = rec.get("headers", {})
    if "x-amzn-waf-action" in h or h.get("cf-mitigated"):
        return True
    return rec["status"] is None or not (200 <= rec["status"] < 300)


def load_population():
    import csv
    rows = list(csv.DictReader(open(CENSUS)))
    pop = []
    for r in rows:
        url = r["evidence_url"].strip()
        parts = urllib.parse.urlsplit(url)
        pop.append({
            "publisher": r["publisher"],
            "concerns": int(r["concerns"]),
            "stratum": r["stratum"],
            "shipped_class": r["class"],
            "shipped_machine_blocked": r["machine_blocked"] == "True",
            "url": url,
            "host": parts.netloc,
            "path": parts.path or "/",
        })
    return pop


def run():
    OUT.mkdir(parents=True, exist_ok=True)
    pop = load_population()
    records = []

    def log(msg):
        print(msg, flush=True)

    # --- Arm R: the sign, one per distinct host ---
    signs = {}
    for host in sorted({p["host"] for p in pop}):
        robots_url = f"https://{host}/robots.txt"
        rec = fetch(robots_url, HONEST_UA, False, follow=True)
        rec.update(arm="R", host=host)
        records.append(rec)
        # 404 is not a refusal: a host that publishes no sign permits everything by convention.
        no_sign = rec["status"] == 404
        entry = {"host": host, "status": rec["status"], "error": rec["error"],
                 "no_sign": no_sign,
                 "readable": no_sign or not refused(rec),
                 "read_as": None if no_sign else ("honest" if not refused(rec) else None),
                 "text_bytes": 0, "star_allows": True if no_sign else None,
                 "named_allowed": [], "named_disallowed": []}
        if no_sign:
            pass
        elif not refused(rec):
            body = fetch_body(robots_url, HONEST_UA, False)
            entry["text_bytes"] = len(body)
            entry["raw"] = body[:8000]
        else:
            # robots.txt cannot itself be disallowed; establish name vs address.
            time.sleep(GAP_SECONDS)
            rec2 = fetch(robots_url, BROWSER_UA, True, follow=True)
            rec2.update(arm="R2", host=host)
            records.append(rec2)
            entry["browser_status"] = rec2["status"]
            if not refused(rec2):
                entry["readable"], entry["read_as"] = True, "browser"
                body = fetch_body(robots_url, BROWSER_UA, True)
                entry["text_bytes"] = len(body)
                entry["raw"] = body[:8000]
        signs[host] = entry
        log(f"R  {host:38s} {entry['status']} readable={entry['readable']}"
            f"{' (no sign)' if no_sign else ''}")
        time.sleep(GAP_SECONDS)

    # Parse each sign against every path used on that host.
    for p in pop:
        s = signs[p["host"]]
        if s.get("raw"):
            star, na, nd = parse_robots(s["raw"], p["path"])
            p["star_allows"] = star
            s["named_allowed"], s["named_disallowed"] = na, nd
            s["star_allows"] = star if s.get("star_allows") is None else s["star_allows"]
        else:
            # No sign published: everything permitted by convention. Sign unreadable:
            # undetermined — and never treated as a declared refusal.
            p["star_allows"] = True if s.get("no_sign") else None

    # --- Arm A: bare, honest, on every door the sign does not close ---
    for p in pop:
        if p["star_allows"] is False:
            p["A"] = {"skipped": "declared closed by robots.txt — not knocked on"}
            log(f"A  {p['publisher'][:34]:34s} SKIPPED (declared closed)")
            continue
        rec = fetch(p["url"], HONEST_UA, False, follow=True)
        rec.update(arm="A", publisher=p["publisher"], host=p["host"])
        records.append(rec)
        p["A"] = rec
        log(f"A  {p['publisher'][:34]:34s} {rec['status']} {rec['error'] or ''}")
        time.sleep(GAP_SECONDS)

    # --- Arm B: complete headers, same identity, only where A was refused ---
    for p in pop:
        a = p.get("A", {})
        if a.get("skipped") or not refused(a):
            continue
        rec = fetch(p["url"], HONEST_UA, True, follow=True)
        rec.update(arm="B", publisher=p["publisher"], host=p["host"])
        records.append(rec)
        p["B"] = rec
        log(f"B  {p['publisher'][:34]:34s} {rec['status']}")
        time.sleep(GAP_SECONDS)

    # --- Arm U: browser identity, only where B was also refused and the sign permits ---
    for p in pop:
        b = p.get("B")
        if b is None or not refused(b):
            continue
        if p["star_allows"] is not True:
            p["U"] = {"skipped": "sign not readable as permitting — browser identity not used"}
            log(f"U  {p['publisher'][:34]:34s} SKIPPED (sign not readable as permitting)")
            continue
        rec = fetch(p["url"], BROWSER_UA, True, follow=True)
        rec.update(arm="U", publisher=p["publisher"], host=p["host"])
        records.append(rec)
        p["U"] = rec
        log(f"U  {p['publisher'][:34]:34s} {rec['status']}")
        time.sleep(GAP_SECONDS)

    # --- Arm C: patience. Exact repeat of A, after everything else. ---
    wait = int(os.environ.get("DOOR_RECHECK_PATIENCE", "600"))
    pending = [p for p in pop if not p.get("A", {}).get("skipped") and refused(p.get("A", {}))]
    if pending:
        log(f"-- waiting {wait} s before the patient arm ({len(pending)} doors) --")
        time.sleep(wait)
    for p in pending:
        rec = fetch(p["url"], HONEST_UA, False, follow=True)
        rec.update(arm="C", publisher=p["publisher"], host=p["host"])
        records.append(rec)
        p["C"] = rec
        log(f"C  {p['publisher'][:34]:34s} {rec['status']}")
        time.sleep(GAP_SECONDS)

    payload = {
        "measured": time.strftime("%Y-%m-%d", time.gmtime()),
        "identity": {"honest": HONEST_UA, "browser": BROWSER_UA},
        "gap_seconds": GAP_SECONDS,
        "patience_seconds": wait if pending else None,
        "signs": signs,
        "doors": pop,
        "requests": records,
    }
    payload = redact(payload)
    (OUT / "probes.json").write_text(json.dumps(payload, indent=1, sort_keys=True))
    summary = summarise(payload)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True))
    print(json.dumps(summary["counts"], indent=1))


def opened(rec):
    """An arm counts as opened only if it was actually run and was not refused."""
    return isinstance(rec, dict) and not rec.get("skipped") and not refused(rec)


def classify(p):
    """The pre-registered verdict for one door. A function of the recorded statuses alone."""
    a = p.get("A", {})
    if a.get("skipped"):
        return "declared_closed"
    if opened(a):
        return "open"
    if opened(p.get("B")):
        return "shape"
    if opened(p.get("U")):
        return "name"
    if opened(p.get("C")):
        return "pace"
    return "impasse"


def redact(payload):
    """Constitution §7: no third-party source files are committed, and no tool-vendor names
    are carried in this record. Each sign is reduced to what the measurement uses — whether it
    permits the cited path, how many agents it names on each side, and a hash by which anyone
    who fetches the same file can check we read what they read."""
    import hashlib
    for rec in payload["requests"]:
        # A derived redirect counter was written by an earlier version of this tool and was
        # wrong: the proxy's CONNECT answers and 103 early hints interleave with the origin's
        # statuses, so it could not be separated. Removed rather than cited; the raw status
        # chain stays in every record.
        rec.pop("redirects", None)
    for door in payload["doors"]:
        for arm in ("A", "B", "U", "C"):
            if isinstance(door.get(arm), dict):
                door[arm].pop("redirects", None)
    for host, s in payload["signs"].items():
        raw = s.pop("raw", None)
        if raw is not None:
            s["sign_sha256"] = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            s["sign_bytes_read"] = len(raw)
        if "named_allowed" in s:
            s["named_allowed_n"] = len(s.pop("named_allowed"))
        if "named_disallowed" in s:
            s["named_disallowed_n"] = len(s.pop("named_disallowed"))
    return payload


def summarise(payload):
    doors = payload["doors"]
    for p in doors:
        p["verdict"] = classify(p)
    total_concerns = sum(p["concerns"] for p in doors)
    counts, weight = {}, {}
    for p in doors:
        counts[p["verdict"]] = counts.get(p["verdict"], 0) + 1
        weight[p["verdict"]] = weight.get(p["verdict"], 0) + p["concerns"]
    knocked = [p for p in doors if p["verdict"] != "declared_closed"]
    refused_a = [p for p in knocked if p["verdict"] != "open"]
    dissolved = [p for p in refused_a if p["verdict"] in ("shape", "name", "pace")]
    impasse = [p for p in refused_a if p["verdict"] == "impasse"]
    signs = payload["signs"]
    readable = [s for s in signs.values() if s["readable"]]
    undeclared = [p for p in impasse if p.get("star_allows") is True]
    shipped_blocked = [p for p in doors if p["shipped_machine_blocked"]]
    return {
        "counts": {
            "doors": len(doors),
            "distinct_hosts": len(signs),
            "signs_readable": len(readable),
            "signs_unreadable": len(signs) - len(readable),
            "signs_none_published": sum(1 for s in signs.values() if s.get("no_sign")),
            "signs_disallowing_star": sum(
                1 for s in signs.values() if s.get("star_allows") is False),
            "signs_read_with_browser_identity": sum(
                1 for s in signs.values() if s.get("read_as") == "browser"),
            "hosts_naming_agents": sum(
                1 for s in signs.values()
                if s.get("named_allowed_n") or s.get("named_disallowed_n")),
            "agents_named_allowed": sum(s.get("named_allowed_n", 0) for s in signs.values()),
            "agents_named_disallowed": sum(s.get("named_disallowed_n", 0) for s in signs.values()),
            "declared_closed": counts.get("declared_closed", 0),
            "knocked": len(knocked),
            "open_to_arm_A": counts.get("open", 0),
            "refused_arm_A": len(refused_a),
            "dissolved_total": len(dissolved),
            "verdict_shape": counts.get("shape", 0),
            "verdict_name": counts.get("name", 0),
            "verdict_pace": counts.get("pace", 0),
            "verdict_impasse": len(impasse),
            "undeclared_refusals": len(undeclared),
            "shipped_machine_blocked": len(shipped_blocked),
            "shipped_blocked_now_open": sum(
                1 for p in shipped_blocked if p["verdict"] == "open"),
            "shipped_open_now_refused": sum(
                1 for p in doors
                if not p["shipped_machine_blocked"] and p["verdict"] not in ("open", "declared_closed")),
        },
        "concerns": {
            "total": total_concerns,
            "by_verdict": weight,
            "impasse_share_pct": round(100 * sum(p["concerns"] for p in impasse) / total_concerns, 1),
            "refused_share_pct": round(100 * sum(p["concerns"] for p in refused_a) / total_concerns, 1),
        },
        "doors": [
            {
                "publisher": p["publisher"], "concerns": p["concerns"], "host": p["host"],
                "url": p["url"], "verdict": p["verdict"], "star_allows": p.get("star_allows"),
                "shipped_machine_blocked": p["shipped_machine_blocked"],
                "status": {
                    arm: (p[arm].get("status") if isinstance(p.get(arm), dict) and not p[arm].get("skipped")
                          else ("skipped" if isinstance(p.get(arm), dict) else None))
                    for arm in ("A", "B", "U", "C") if p.get(arm) is not None
                },
                "layer": refusing_layer(p),
            }
            for p in sorted(doors, key=lambda d: -d["concerns"])
        ],
        "signs": signs,
    }


def refusing_layer(p):
    """Which layer said no, from the response headers of the last refused arm."""
    for arm in ("C", "U", "B", "A"):
        rec = p.get(arm)
        if not isinstance(rec, dict) or rec.get("skipped") or not refused(rec):
            continue
        h = rec.get("headers", {})
        if "cf-ray" in h:
            return "Cloudflare"
        if "akamai-grn" in h or "x-akamai-transformed" in h:
            return "Akamai"
        if "x-amzn-waf-action" in h:
            return "AWS WAF"
        if "x-iinfo" in h:
            return "Imperva"
        if h.get("server"):
            return h["server"]
        if rec.get("error"):
            return "transport"
    return None


def check():
    payload = redact(json.loads((OUT / "probes.json").read_text()))
    fresh = summarise(payload)
    stored = json.loads((OUT / "summary.json").read_text())
    if json.dumps(fresh, sort_keys=True) != json.dumps(stored, sort_keys=True):
        print("DRIFT: summary.json does not match a re-derivation from probes.json", file=sys.stderr)
        for k, v in fresh["counts"].items():
            if stored["counts"].get(k) != v:
                print(f"  {k}: stored={stored['counts'].get(k)} derived={v}", file=sys.stderr)
        return 1
    print(f"OK — summary.json re-derived from {len(payload['requests'])} committed requests")
    return 0


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--summarise", action="store_true",
                    help="re-derive summary.json from the committed probes.json, no network")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    if args.run:
        run()
    elif args.summarise:
        payload = redact(json.loads((OUT / "probes.json").read_text()))
        (OUT / "probes.json").write_text(json.dumps(payload, indent=1, sort_keys=True))
        summary = summarise(payload)
        (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True))
        print(json.dumps(summary["counts"], indent=1))
    elif args.check:
        sys.exit(check())
    else:
        ap.print_help()
