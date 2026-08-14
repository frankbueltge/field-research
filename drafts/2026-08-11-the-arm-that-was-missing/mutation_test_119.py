#!/usr/bin/env python3
"""Does the auditor catch an error it was not built around? — the mutation test.

Session 119. `audit_instrument.py` found the `10222` miscoding it was bet against. The obvious
objection, and the one this practice would make against anyone else: **a check written the day
after an error is known is not evidence that the check works.** It might be a rule shaped to fit
one answer.

So the auditor is run against errors it has never seen. Nine mutations, each a distinct failure
class, are injected into **copies** of this arc's files in a scratch directory built of symlinks
— **no file of this repository is modified, and no request is made**. The auditor runs there
unchanged, and the test asks one question per mutation: **did it notice?**

A mutation the auditor misses is the honest result and is reported as loudly as one it catches.

Usage: python3 mutation_test_119.py
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
RUN = "ledger/run-2026-08-14T0343Z.json"
ACC = "account-state-117b.json"


def scratch():
    """A working copy of the draft: symlinks to everything, so nothing here is touched."""
    d = tempfile.mkdtemp(prefix="mutation-119-")
    os.mkdir(os.path.join(d, "ledger"))
    for name in os.listdir(HERE):
        src = os.path.join(HERE, name)
        if name == "ledger":
            for f in os.listdir(src):
                if os.path.isfile(os.path.join(src, f)):
                    os.symlink(os.path.join(src, f), os.path.join(d, "ledger", f))
            continue
        if os.path.isfile(src):
            os.symlink(src, os.path.join(d, name))
    return d


def materialise(d, rel):
    """Replace a symlink with a real, writable copy, and return the loaded JSON."""
    p = os.path.join(d, rel)
    if os.path.islink(p):
        real = os.readlink(p)
        os.unlink(p)
        shutil.copy(real, p)
    return json.load(open(p)), p


def write(obj, p):
    json.dump(obj, open(p, "w"), indent=1)


# ---------------------------------------------------------------- the nine mutations
# Each returns a description and the check it OUGHT to be caught by. The auditor is never told.

def m_state_flip(d):
    j, p = materialise(d, RUN)
    j["observations"][7]["state"] = "NOT-RETRIEVABLE" \
        if j["observations"][7]["state"] == "RETRIEVABLE" else "RETRIEVABLE"
    # keep the aggregate consistent, so only the re-derivation can see it
    c = {}
    for r in j["observations"]:
        c.setdefault(r["arm"], {}).setdefault(r["state"], 0)
        c[r["arm"]][r["state"]] += 1
    j["counts"] = c
    write(j, p)
    return "a stored state flipped, with the file's own aggregate kept consistent", "A1"


def m_new_http_class(d):
    j, p = materialise(d, RUN)
    o = j["observations"][11]
    o["http"], o["state"] = 403, "INDETERMINATE"
    o.pop("author_unique_id", None)
    c = {}
    for r in j["observations"]:
        c.setdefault(r["arm"], {}).setdefault(r["state"], 0)
        c[r["arm"]][r["state"]] += 1
    j["counts"] = c
    write(j, p)
    return "a response class the classifier has no branch for (HTTP 403)", "A3"


def m_retrievable_without_evidence(d):
    j, p = materialise(d, RUN)
    for o in j["observations"]:
        if o["state"] == "RETRIEVABLE":
            o["author_unique_id"] = None
            break
    write(j, p)
    return "a RETRIEVABLE record with no returned handle in it", "A4"


def m_account_unknown_code(d):
    j, p = materialise(d, ACC)
    r = next(x for x in j["results"] if x.get("status_field") == 0)
    r["status_field"] = 99999                      # a code never seen, still serving the object
    j["by_group"], j["codes_by_group"] = recount(j["results"])
    write(j, p)
    return "an unseen non-zero account code that still returns the user object", "A5"


def m_account_marker_only(d):
    j, p = materialise(d, ACC)
    r = next(x for x in j["results"] if x.get("status_field") == 10221)
    r["markers"] = dict(r["markers"], userInfo=True, uniqueId=True)   # no handle parsed
    write(j, p)
    return "an account read as 'not served' whose page carries the user-object markers", "A5"


def m_duplicate_unit(d):
    j, p = materialise(d, RUN)
    j["observations"].append(dict(j["observations"][3]))
    j["requested"] = len(j["observations"])
    j["counts"], _ = None, None
    c = {}
    for r in j["observations"]:
        c.setdefault(r["arm"], {}).setdefault(r["state"], 0)
        c[r["arm"]][r["state"]] += 1
    j["counts"] = c
    write(j, p)
    return "the same identifier probed twice in one run", "A7"


def m_aggregate_drift(d):
    j, p = materialise(d, RUN)
    arm = next(iter(j["counts"]))
    st = next(iter(j["counts"][arm]))
    j["counts"][arm][st] += 3
    write(j, p)
    return "a summary block that no longer follows from the rows", "A6"


def m_alien_unit(d):
    j, p = materialise(d, RUN)
    o = dict(j["observations"][2], vid="1234567890123456789")
    j["observations"].append(o)
    j["requested"] = len(j["observations"])
    c = {}
    for r in j["observations"]:
        c.setdefault(r["arm"], {}).setdefault(r["state"], 0)
        c[r["arm"]][r["state"]] += 1
    j["counts"] = c
    write(j, p)
    return "an observation of a unit that is not in the manifest", "A7"


def m_handle_drift(d):
    j, p = materialise(d, RUN)
    j["observations"][5]["handle"] = "some_other_handle"
    write(j, p)
    return "the same identifier probed under a different handle than on other days", "A7"


def recount(rows):
    tab, codes = {}, {}
    for r in rows:
        g, s = r["group"], r.get("status_field")
        t = tab.setdefault(g, {"n": 0, "readable": 0, "nonzero": 0})
        t["n"] += 1
        if s is not None:
            t["readable"] += 1
            if s != 0:
                t["nonzero"] += 1
        codes.setdefault(g, {})
        codes[g][str(s)] = codes[g].get(str(s), 0) + 1
    for g, t in tab.items():
        t["nonzero_share"] = t["nonzero"] / t["readable"] if t["readable"] else None
    return tab, codes


MUTATIONS = [m_state_flip, m_new_http_class, m_retrievable_without_evidence,
             m_account_unknown_code, m_account_marker_only, m_duplicate_unit,
             m_aggregate_drift, m_alien_unit, m_handle_drift]


def baseline_findings(report):
    """The findings the clean record already has, so a mutation is judged on the difference."""
    n = {}
    for c in report["checks"]:
        k = c["check"][:2]
        n[k] = {"A1": len(c.get("mismatches", [])),
                "A3": c.get("n_distinct_classes"),
                "A4": len(c.get("findings", [])),
                "A5": len(c.get("findings", [])),
                "A6": len(c.get("findings", [])),
                "A7": len(c.get("findings", [])),
                }.get(k, None)
    return n


def run_audit(cwd):
    out = os.path.join(cwd, "audit.json")
    r = subprocess.run([sys.executable, "audit_instrument.py", out], cwd=cwd,
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None, r.stderr[-800:]
    return json.load(open(out)), None


def main():
    clean_dir = scratch()
    clean, err = run_audit(clean_dir)
    if clean is None:
        print("the auditor does not run on an unmutated copy:", err)
        sys.exit(1)
    base = baseline_findings(clean)

    results = []
    for fn in MUTATIONS:
        d = scratch()
        desc, expected = fn(d)
        rep, err = run_audit(d)
        if rep is None:
            results.append({"mutation": fn.__name__, "description": desc,
                            "expected_check": expected, "caught": None,
                            "auditor_error": err})
            shutil.rmtree(d, ignore_errors=True)
            continue
        now = baseline_findings(rep)
        moved = sorted(k for k in now
                       if now[k] is not None and base.get(k) is not None and now[k] != base[k])
        results.append({"mutation": fn.__name__, "description": desc,
                        "expected_check": expected,
                        "checks_that_moved": moved,
                        "caught": expected in moved,
                        "caught_by_something_else": bool(moved) and expected not in moved,
                        "counts": {k: {"clean": base[k], "mutated": now[k]} for k in moved}})
        shutil.rmtree(d, ignore_errors=True)
    shutil.rmtree(clean_dir, ignore_errors=True)

    caught = sum(1 for r in results if r.get("caught"))
    out = {"schema": "field-research/auditor-mutation-test/1", "session": 119,
           "generated_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "requests_made": 0,
           "method": ("Each mutation is injected into a symlinked scratch copy of this draft and "
                      "the auditor runs there unchanged. Nothing in the repository is modified."),
           "n_mutations": len(results), "caught_by_the_expected_check": caught,
           "missed": [r["mutation"] for r in results if r.get("caught") is False],
           "results": results}
    json.dump(out, open("mutation-test-119.json", "w"), indent=1)
    for r in results:
        mark = "CAUGHT " if r.get("caught") else ("MISSED " if r.get("caught") is False
                                                  else "ERROR  ")
        print(f'{mark} {r["expected_check"]}  {r["description"]}'
              + (f'   (moved: {",".join(r.get("checks_that_moved", []))})'
                 if r.get("checks_that_moved") else ""))
    print(f'{caught} of {len(results)} caught by the check that should catch them')
    print("wrote mutation-test-119.json")


if __name__ == "__main__":
    main()
