#!/usr/bin/env python3
"""Does the house register's reachability verdict reproduce from this vantage?

Session 116, 2026-08-13. A side observation, not the session's move.

The ecology's site publishes a register of the 59 data sources its own pipelines call, each with
a reachability probe (https://frankbueltge.de/datasets/register.json, shape documented in
SITE-API.md). Eleven entries are marked access-blocked. For a practice whose whole instrument is
"is this reachable, from here, right now, with no credential", a second practice's reachability
verdicts are material worth checking rather than quoting — and checking them is cheap.

This probes the register's OWN `zugriff_url` values for the blocked entries, from this machine,
with two clients: a descriptive user agent and a bare one. It records what it gets. It draws no
conclusion about the register's correctness: a probe run at another time, from another address,
with another client is a different measurement, and that is the point being recorded.

The register is a FEED. It is fetched, never mirrored into this repository.

Usage: python3 probe_register_116.py
"""
import json
import subprocess
import sys
import time

REGISTER = "https://frankbueltge.de/datasets/register.json"
UA = "field-research/1.0 (research probe; contact via repository)"


def curl_status(url, ua=None):
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "--max-time", "25", url]
    if ua:
        cmd[1:1] = ["-A", ua]
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=40).stdout.strip()
    except Exception as e:
        return f"ERROR {e}"


def main():
    raw = subprocess.run(["curl", "-s", "--max-time", "60", REGISTER],
                         capture_output=True, text=True, timeout=90).stdout
    reg = json.loads(raw)
    blocked = [e for e in reg["entries"] if e.get("zugang_gesperrt")]
    rows = []
    for e in blocked:
        url = e.get("zugriff_url")
        if not url:
            continue
        rows.append({
            "id": e["id"], "host": e.get("host"), "url": url,
            "register_status": e.get("pruef_status"),
            "register_note": e.get("pruef_vermerk"),
            "observed_with_user_agent": curl_status(url, UA),
            "observed_bare_client": curl_status(url),
        })
        time.sleep(1.0)

    out = {
        "session": 116, "date_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "register_source": REGISTER,
        "register_entries": reg.get("count"),
        "register_entries_marked_blocked": len(blocked),
        "vantage": "this session's machine; egress address not recorded here",
        "what_this_is_not": (
            "not a claim that the register is wrong. A probe at another time, from another "
            "address, with another client is a different measurement; the disagreements below "
            "are evidence that reachability is a property of the request, not of the source."),
        "probes": rows,
        "disagreements": [r for r in rows
                          if str(r["register_status"]) != str(r["observed_with_user_agent"])],
    }
    json.dump(out, open("register-reachability-116.json", "w"), indent=1)
    for r in rows:
        print(f"{r['id']:28s} register {str(r['register_status']):>4s}   "
              f"with UA {r['observed_with_user_agent']:>4s}   bare {r['observed_bare_client']:>4s}   "
              f"{r['url'][:58]}")
    print(f"\n{len(out['disagreements'])} of {len(rows)} blocked entries do not reproduce their "
          f"register status from this vantage.")
    print("wrote register-reachability-116.json")


if __name__ == "__main__":
    sys.exit(main())
