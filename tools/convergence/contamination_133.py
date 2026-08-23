#!/usr/bin/env python3
"""contamination_133.py — does this audit's own report change the checks it audits?

WHY THIS EXISTS (2026-08-23, session 133)
-----------------------------------------
`audit_checks.py` counts checks whose output lands inside their own search space. It
writes its own report to `tools/convergence/convergence-audit-133.json`, inside a
repository that several of the checks it audits enumerate whole — `e34_sweep.py` reads
1,581 files across 157 directories, `record_ceiling_check.py` 719 files across 16.

So the audit is a candidate instance of the defect it counts, and saying so in a caveat
would be the cheap way out: the whole point of `ERRATA-132.md` E36 is that this class of
defect is invisible to review and obvious to a second run. **This script takes the second
run.**

METHOD
------
1. Run the population once against a copy of the repository as this session found it —
   with **no** audit report in the tree. Record each check's report hash. (BASELINE)
2. Run the identical population against a copy in which the audit's own report **has**
   been placed at the path it will be committed to. (CONTAMINATED)
3. Any check whose report hash differs between (1) and (2) was measuring the record plus
   this audit. The difference is the contamination, measured rather than assumed.

A check that differs is not thereby broken and this script does not say it is. It says
that this audit's own output is inside that check's search space, which is a fact about
where the report is filed, and it is stated so a later session reading a moved number
knows what moved it.

USAGE
    python3 tools/convergence/contamination_133.py       # writes contamination-133.json
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AUDIT = os.path.join(HERE, "audit_checks.py")
OUT = os.path.join(HERE, "contamination-133.json")


def run_audit(inject=None):
    argv = [sys.executable, AUDIT, "--report"]
    if inject:
        argv += ["--inject", inject]
    proc = subprocess.run(argv, cwd=REPO, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", "replace")[-2000:])
        raise SystemExit("audit run failed")
    return json.loads(proc.stdout.decode("utf-8"))


def main():
    sys.stderr.write("baseline: the tree with no audit report in it ...\n")
    base = run_audit()

    # The report that will be committed. Written to a scratch path, never into the tree,
    # so this script cannot contaminate the baseline it just took.
    fd, tmp = tempfile.mkstemp(prefix="audit-report-", suffix=".json")
    with os.fdopen(fd, "w") as fh:
        json.dump(base, fh, indent=1, sort_keys=True)

    sys.stderr.write("contaminated: the same tree with the audit's own report filed in it ...\n")
    cont = run_audit(inject=tmp)
    os.unlink(tmp)

    b = {c["id"]: c for c in base["checks"]}
    c2 = {c["id"]: c for c in cont["checks"]}
    rows = []
    for cid in sorted(set(b) | set(c2)):
        x, y = b.get(cid, {}), c2.get(cid, {})
        moved = (x.get("stdout_shas") != y.get("stdout_shas")
                 or x.get("exit_codes") != y.get("exit_codes")
                 or x.get("stderr_shas") != y.get("stderr_shas"))
        rows.append({
            "id": cid,
            "reads_the_whole_tree": len(x.get("repo_dirs_listed") or []) > 4,
            "baseline_stdout_shas": x.get("stdout_shas"),
            "contaminated_stdout_shas": y.get("stdout_shas"),
            "baseline_exit_codes": x.get("exit_codes"),
            "contaminated_exit_codes": y.get("exit_codes"),
            "report_moved_because_of_this_audit": moved,
        })

    moved = [r["id"] for r in rows if r["report_moved_because_of_this_audit"]]
    summary = {
        "generated_by": "tools/convergence/contamination_133.py",
        "session": 133,
        "question": "does filing this audit's own report in the repository change the "
                    "report of any check the audit measures?",
        "population": len(rows),
        "checks_whose_report_moved": moved,
        "count_moved": len(moved),
        "verdict": ("THIS AUDIT CONTAMINATES ITS OWN POPULATION" if moved
                    else "NO CHECK IN THIS POPULATION MOVED WHEN THE AUDIT'S REPORT WAS FILED"),
        "rows": rows,
    }
    with open(OUT, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps({k: summary[k] for k in
                      ("count_moved", "checks_whose_report_moved", "verdict")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
