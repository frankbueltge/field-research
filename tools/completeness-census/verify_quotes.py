#!/usr/bin/env python3
"""Check every quote in the coding record against the material actually fetched.

Sources fetched directly to disk are verified verbatim. Sources reached only
through the research tool were never written to disk by us, so their quotes
cannot be re-verified offline: they are reported as UNVERIFIABLE rather than
passed. A checker that cannot tell the two apart is the defect this replaces.
"""
import json, sys, os, re, hashlib

EVIDENCE = {
    "kiraly-plan-2015":      ["plan.txt"],
    "metadata-qa-api":       ["bodies/metadata-qa-api-0.body", "basic.java"],
    "qa-catalogue":          ["bodies/qa-catalogue-0.body"],
    "fuji":                  ["bodies/fuji-0.body"],
    "hillmann-phipps-2007":  ["dcmi-952108665.txt"],
    "margaritopoulos-2008":  ["dcmi-952109222.txt"],
    "tarver-2015":           ["dcmi-952137007.txt"],
}
TOOL_ONLY = {"lorenzini-2021", "mqa-europa", "w3c-dqv", "phillips-2019"}

LIGATURES = {"\x02": "fi", "\x03": "fl"}

def norm(s):
    """Collapse whitespace, and resolve the two ligature slots this font uses.

    The PDFs from this font place the fi and fl ligatures at code points 0x02
    and 0x03. The mapping is read off the documents themselves ("\x02elds" is
    "fields", "Work\x03ow" is "workflow") and is applied to both sides of the
    comparison, so a quote is checked against the same normalisation it was
    written under. The substitution is disclosed in VERIFICATION.md.
    """
    for k, v in LIGATURES.items():
        s = s.replace(k, v)
    return re.sub(r"\s+", " ", s).strip()

def main(sources_path, base):
    doc = json.load(open(sources_path))
    ok = bad = unver = 0
    for s in doc["sources"]:
        if not s["quotes"]:
            continue
        sid = s["id"]
        if sid in TOOL_ONLY:
            for q in s["quotes"]:
                print("UNVERIFIABLE OFFLINE  %-22s %s" % (sid, q[:60]))
                unver += 1
            continue
        files = EVIDENCE.get(sid)
        if not files:
            print("NO EVIDENCE FILE      %-22s" % sid); bad += len(s["quotes"]); continue
        hay = ""
        for f in files:
            p = os.path.join(base, f)
            hay += norm(open(p, errors="replace").read()) + "\n"
        for q in s["quotes"]:
            if norm(q) in hay:
                print("ok                    %-22s %s" % (sid, q[:60])); ok += 1
            else:
                print("QUOTE NOT FOUND       %-22s %r" % (sid, q[:90])); bad += 1
    print("\n%d verified, %d not found, %d unverifiable offline" % (ok, bad, unver))
    return 1 if bad else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
