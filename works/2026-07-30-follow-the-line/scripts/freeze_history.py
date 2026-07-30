#!/usr/bin/env python3
"""Freeze every upstream state of the audited catalogue file, and write the manifest.

This is the ONLY script in the work that needs the network, and it is needed once. It reads a
local clone of the public site repository, walks the full commit history of the catalogue file,
and writes one frozen state per commit through the same reduction rule `freeze.py` applies to a
single state — abstracts dropped, the generative-model identifier redacted — so that the states
are comparable to each other and to the freezes made on 2026-07-28.

Reproducing it:
    git clone --filter=blob:none --no-checkout https://github.com/frankbueltge/frankbueltge.de /tmp/site
    python3 scripts/freeze_history.py /tmp/site

The manifest records, per state, the SHA-256 of the RAW upstream file as well as of the freeze,
so a reader who does not trust this practice's reduction can verify the raw input independently
and re-derive the freeze themselves.

Note on provenance of the route: until 2026-07-28 this practice published the claim that the
upstream history was not readable from here. That claim was false and had never been tested. It
is retracted at the root; this script exists because the retraction was correct.
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from freeze import freeze  # noqa: E402

FILE = "src/data/register/papers.json"
OUTDIR = os.path.join(HERE, "sources", "history")

# The state audited on 2026-07-28, and the day that audit was delivered into the ecology's
# request channel. Both are facts about this practice, not about the object.
AUDITED_STATE = "a7879398"
AUDIT_DELIVERED = "2026-07-28"


def git(clone, *args):
    return subprocess.run(["git", "-C", clone, *args], capture_output=True, text=True,
                          check=True).stdout


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    clone = sys.argv[1]
    log = git(clone, "log", "--reverse", "--format=%H\t%cI\t%s", "--", FILE).strip().split("\n")
    os.makedirs(OUTDIR, exist_ok=True)

    states = []
    for line in log:
        sha, when, subject = line.split("\t", 2)
        raw = subprocess.run(["git", "-C", clone, "show", f"{sha}:{FILE}"],
                             capture_output=True, check=True).stdout
        entries = json.loads(raw.decode("utf-8"))
        out = os.path.join(OUTDIR, sha[:8] + ".json")
        with open(out, "w", encoding="utf-8") as fh:
            json.dump(freeze(entries), fh, ensure_ascii=False, sort_keys=True,
                      indent=1, separators=(",", ": "))
            fh.write("\n")
        states.append({
            "commit": sha,
            "committed_at": when,
            "subject": subject,
            "entries": len(entries),
            "raw_sha256": hashlib.sha256(raw).hexdigest(),
            "freeze_sha256": hashlib.sha256(open(out, "rb").read()).hexdigest(),
        })

    from datetime import datetime
    def ts(s):
        return datetime.fromisoformat(s)

    idx = [s["commit"][:8] for s in states].index(AUDITED_STATE)
    lifetime = ts(states[idx + 1]["committed_at"]) - ts(states[idx]["committed_at"])
    # the disclosure: written at the audited state, absent at the next, restored at the last
    gone = ts(states[-1]["committed_at"]) - ts(states[idx + 1]["committed_at"])

    manifest = {
        "file": FILE,
        "upstream": "https://github.com/frankbueltge/frankbueltge.de",
        "audited_state": AUDITED_STATE,
        "audit_delivered": AUDIT_DELIVERED,
        "audited_state_lifetime_minutes": round(lifetime.total_seconds() / 60),
        "audited_state_lifetime_human": "%dh%02dm" % (lifetime.total_seconds() // 3600,
                                                      (lifetime.total_seconds() % 3600) // 60),
        "disclosure_lifetime_human": "%dh%02dm" % (lifetime.total_seconds() // 3600,
                                                   (lifetime.total_seconds() % 3600) // 60),
        "disclosure_absent_human": "%dh%02dm" % (gone.total_seconds() // 3600,
                                                 (gone.total_seconds() % 3600) // 60),
        "states": states,
    }
    with open(os.path.join(OUTDIR, "MANIFEST.json"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, sort_keys=True, indent=1)
        fh.write("\n")
    for s in states:
        print("%s  %s  %4d entries  %s" % (s["commit"][:8], s["committed_at"], s["entries"],
                                           s["subject"][:60]))
    print("audited state stood %s; disclosure absent %s"
          % (manifest["audited_state_lifetime_human"], manifest["disclosure_absent_human"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
