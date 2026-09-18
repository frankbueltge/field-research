#!/usr/bin/env python3
"""Kill conditions K1 and K3, run on the canon before any repository blob is scored.

K1 — every family's SPDX canonical text must be identified as that family, and as no
     other family whose text it does not contain. If not, the identifier is broken.
K3 — the SPDX canonical MIT text IS a template: it reads
     `Copyright (c) <year> <copyright holders>`. If the placeholder rule does not fire
     on it, the placeholder rule is broken.

Both inputs are published reference texts. No property of any studied repository can
reach either condition, which is the whole point after five sessions of kill
conditions firing on the phenomenon.

Run: python3 control.py out.json
"""
import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules
from fingerprints import SPDX_CONTROL

BASE = "https://raw.githubusercontent.com/spdx/license-list-data/main/text/"


def fetch(spdx_id):
    url = BASE + spdx_id + ".txt"
    p = subprocess.run(["curl", "-sS", "--max-time", "60", "-w", "\n%{http_code}", url],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None, None, f"curl exit {p.returncode}: {p.stderr.strip()[:200]}"
    body, _, code = p.stdout.rpartition("\n")
    if code.strip() != "200":
        return None, code.strip(), f"HTTP {code.strip()}"
    return body, "200", None


def main(out_path):
    rows, errors = [], []
    for family, spdx_id in SPDX_CONTROL.items():
        text, code, err = fetch(spdx_id)
        if err:
            errors.append({"family": family, "spdx_id": spdx_id, "error": err})
            rows.append({"family": family, "spdx_id": spdx_id, "fetched": False,
                         "http": code, "error": err})
            continue
        got = rules.l1_families(text)
        rows.append({
            "family": family, "spdx_id": spdx_id, "fetched": True, "http": code,
            "bytes": len(text.encode()), "sha256": hashlib.sha256(text.encode()).hexdigest(),
            "identified_as": got,
            "identifies_itself": family in got,
            "also_identified_as": [g for g in got if g != family],
            "copyright_lines": rules.copyright_lines(text)[:3],
            "placeholder_fires": any(rules.has_placeholder(l) for l in rules.copyright_lines(text)),
        })

    fetched = [r for r in rows if r.get("fetched")]
    k1_failures = [r["family"] for r in fetched if not r["identifies_itself"]]
    mit = next((r for r in fetched if r["family"] == "MIT"), None)
    k3_ok = bool(mit and mit["placeholder_fires"])

    out = {
        "note": "K1 and K3, run on published reference texts before any repository blob "
                "was scored. Neither condition can be reached by a property of a studied "
                "repository.",
        "source": BASE,
        "n_families_in_table": len(SPDX_CONTROL),
        "n_fetched": len(fetched),
        "fetch_errors": errors,
        "K1_identifier_identifies_the_canon": {
            "fired": bool(k1_failures),
            "failures": k1_failures,
            "verdict": "BROKEN — L1 and L2 suspended" if k1_failures else "passed",
        },
        "K3_placeholder_rule_fires_on_the_MIT_canon": {
            "fired": not k3_ok,
            "mit_copyright_line": (mit or {}).get("copyright_lines"),
            "verdict": "passed" if k3_ok else "BROKEN — L2 and P4 suspended",
        },
        "rows": rows,
    }
    open(out_path, "w").write(json.dumps(out, indent=1) + "\n")
    print(f"{len(fetched)}/{len(SPDX_CONTROL)} canonical texts fetched")
    print("K1 fired:", bool(k1_failures), k1_failures or "")
    print("K3 fired:", not k3_ok)
    for r in fetched:
        if r["also_identified_as"]:
            print("  also identified as:", r["family"], "->", r["also_identified_as"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
