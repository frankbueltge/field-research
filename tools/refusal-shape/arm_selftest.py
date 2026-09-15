#!/usr/bin/env python3
"""Do the three arms send what the pre-registration says they send?

An arm is only evidence if the header it is named for is the header that leaves the machine.
This starts a throwaway HTTP server on localhost, sends each arm at it, and records the exact
User-Agent line the server received. No outside network, no third party.

    python3 tools/refusal-shape/arm_selftest.py    # write data/arm-selftest.json
"""
import json
import pathlib
import sys
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import probe  # noqa: E402

DATA = pathlib.Path(__file__).resolve().parents[2] / "artifacts/2026-09-15-whose-refusal-is-it/data"
seen = []


class H(BaseHTTPRequestHandler):
    def do_GET(self):
        seen.append({"path": self.path, "user_agent": self.headers.get("User-Agent"),
                     "accept": self.headers.get("Accept")})
        body = b"ok"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


ECHO = "https://httpbin.org/headers"


def network_leg():
    """The local leg proves what leaves this process. This proves what ARRIVES at a third
    party — this container's egress is a proxy, and a proxy that rewrote the User-Agent would
    turn every arm into the same arm and every number in this study into nothing."""
    probe.MIN_SPACING = 1.0
    out = {}
    for arm in ("bare", "urllib", "named"):
        r = probe.request(ECHO, arm, keep=3000)
        body = r["body_head"] or ""
        try:
            hdrs = json.loads(body).get("headers", {}) if body.strip().startswith("{") else {}
        except Exception:
            hdrs = {}
        out[arm] = {"status": r["status"], "user_agent_seen_by_third_party": hdrs.get("User-Agent"),
                    "body_head": body[:300], "error": r["error"]}
    ok = (
        out["bare"]["user_agent_seen_by_third_party"] is None
        and (out["urllib"]["user_agent_seen_by_third_party"] or "").startswith("Python-urllib/")
        and out["named"]["user_agent_seen_by_third_party"] == probe.NAMED_UA
    )
    return {"echo_service": ECHO, "arms": out, "arms_survive_this_egress": ok,
            "note": "The echoed headers are parsed from the full response body; the body_head "
                    "field here is a 300-byte excerpt for the reader. An earlier version of this "
                    "check parsed the 200-byte excerpt and reported a failure that was its own "
                    "truncation, not the proxy's doing."}


def main():
    srv = HTTPServer(("127.0.0.1", 0), H)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{srv.server_port}/probe-target"
    probe.MIN_SPACING = 0.0
    out = {}
    for arm in ("bare", "urllib", "named"):
        r = probe.request(url, arm)
        rec = seen[-1]
        out[arm] = {"status": r["status"], "user_agent_received": rec["user_agent"],
                    "accept_received": rec["accept"]}
    srv.shutdown()

    ua = {k: v["user_agent_received"] for k, v in out.items()}
    checks = [
        ("bare sends no User-Agent at all", ua["bare"] is None),
        ("urllib sends the library default", bool(ua["urllib"]) and ua["urllib"].startswith("Python-urllib/")),
        ("named sends this practice's string", ua["named"] == probe.NAMED_UA),
        ("named names a contact address", "frankbueltge.de" in (ua["named"] or "")),
        ("no arm claims to be a browser",
         not any(w in (v or "").lower() for v in ua.values()
                 for w in ("mozilla", "chrome", "safari", "firefox", "webkit"))),
        ("the three arms are distinguishable", len({str(v) for v in ua.values()}) == 3),
        ("every arm reached the server", all(v["status"] == 200 for v in out.values())),
    ]
    net = network_leg() if "--network" in sys.argv else None
    if net is not None:
        checks.append(("the arms survive this container's egress proxy intact",
                       net["arms_survive_this_egress"]))
    failed = [c for c, ok in checks if not ok]
    (DATA / "arm-selftest.json").write_text(json.dumps({
        "_note": "The arms of PREREGISTRATION.md §2.1, verified against a throwaway server on "
        "localhost. What the arm is named for is what leaves the machine.",
        "arms": out,
        "network_leg": net,
        "checks": [{"check": c, "pass": ok} for c, ok in checks],
        "failures": failed,
    }, indent=1, ensure_ascii=False) + "\n")
    for c, ok in checks:
        print(("  ok   " if ok else "  FAIL ") + c)
    print(f"user-agents: {json.dumps(ua)}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
