#!/usr/bin/env python3
"""contamination_133.py — does this audit's own report change the checks it audits?

WHY THIS EXISTS (2026-08-23, session 133)
-----------------------------------------
`audit_checks.py` counts checks whose output lands inside their own search space. It
writes its own report to `tools/convergence/convergence-audit-133.json`, inside a
repository that several of the checks it audits enumerate whole — `e34_sweep.py` and
`record_ceiling_check.py` between them read well over a thousand files across more than a
hundred directories.

**No file count is written here on purpose.** The two that used to be
(1,581 and 719) were typed from one run of the audit and were stale against the next: the
independent recomputation found them wrong in this docstring and in the increment that
copied them. The live figures are in `convergence-audit-133.json` and are printed by
`table_133.py`; a number about a moving record does not belong in a docstring.

So the audit is a candidate instance of the defect it counts, and saying so in a caveat
would be the cheap way out: the whole point of `ERRATA-132.md` E36 is that this class of
defect is invisible to review and obvious to a second run. **This script takes the second
run.**

METHOD
------
0. **Freeze the record once.** One copy of the repository is made, hashed, used by all
   three passes below, and hashed again at the end. The live tree is never read after
   that. This step was added after the first replicated run was invalidated by the
   session writing a file into the tree between two of its passes — see `--master` in
   `audit_checks.py`. A test whose whole premise is *an unchanged record* now proves the
   record was unchanged instead of assuming it.
1. Run the population against a copy of the repository as this session found it, with
   **no** audit report in the tree. (BASELINE 1)
2. Run it again, identically. (BASELINE 2)
3. Run it against a copy in which the audit's own report **has** been placed at the path
   it will be committed to. (CONTAMINATED)
4. A check that already differs between BASELINE 1 and BASELINE 2 is **unstable on its
   own** and is excluded from the attribution, by name and with its hashes printed. Of
   the rest, any check differing between BASELINE 1 and CONTAMINATED was measuring the
   record plus this audit.

**Step 2 is not symmetry for its own sake, and the first version of this script did not
have it.** Run without a replicate baseline it returned *"THIS AUDIT CONTAMINATES ITS OWN
POPULATION"* on one mover: `validate_timestamps.py`, the one check in the population that
fetches a live service instead of reading the record. Its stdout was empty on all three
baseline runs and non-empty on one contaminated run, because the service answered
differently, not because a file had been added to a tree it never reads. **A test for
contamination that cannot tell contamination from a flaky third party is a test that will
report contamination sooner or later whatever is true**, which is the failure this whole
audit exists to name in other instruments. The replicate is the fix.

A check that differs is not thereby broken and this script does not say it is. It says
that this audit's own output is inside that check's search space, which is a fact about
where the report is filed, and it is stated so a later session reading a moved number
knows what moved it.

USAGE
    python3 tools/convergence/contamination_133.py       # writes contamination-133.json
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
AUDIT = os.path.join(HERE, "audit_checks.py")
OUT = os.path.join(HERE, "contamination-133.json")


def tree_hash(root):
    """One hash over every regular file under root, .git excluded. Used to PROVE the
    record did not change across the three passes, rather than assume it."""
    import hashlib
    h = hashlib.sha256()
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = sorted(d for d in dirnames if d != ".git")
        for fn in sorted(filenames):
            p = os.path.join(dirpath, fn)
            h.update(os.path.relpath(p, root).encode())
            try:
                with open(p, "rb") as fh:
                    h.update(hashlib.sha256(fh.read()).digest())
            except OSError:
                h.update(b"<unreadable>")
    return h.hexdigest()


def run_audit(master, inject=None):
    argv = [sys.executable, AUDIT, "--report", "--master", master]
    if inject:
        argv += ["--inject", inject]
    proc = subprocess.run(argv, cwd=REPO, capture_output=True)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr.decode("utf-8", "replace")[-2000:])
        raise SystemExit("audit run failed")
    return json.loads(proc.stdout.decode("utf-8"))


def sig(c):
    return (c.get("stdout_shas"), c.get("stderr_shas"), c.get("exit_codes"))


def main():
    # ONE frozen copy of the record, made once, used by all three passes. The live tree
    # is never read again after this line — see the note in `audit_checks.py --master`.
    scratch = tempfile.mkdtemp(prefix="contamination-133-")
    frozen = os.path.join(scratch, "frozen")
    sys.stderr.write("freezing the record ...\n")
    shutil.copytree(REPO, frozen, symlinks=True)
    h_before = tree_hash(frozen)

    sys.stderr.write("baseline 1: the frozen tree with no audit report in it ...\n")
    base1 = run_audit(frozen)
    sys.stderr.write("baseline 2: the same frozen tree again, to find what moves on its own ...\n")
    base2 = run_audit(frozen)

    # The report that will be committed. Written to a scratch path, never into the tree,
    # so this script cannot contaminate the baselines it just took.
    fd, tmp = tempfile.mkstemp(prefix="audit-report-", suffix=".json")
    with os.fdopen(fd, "w") as fh:
        json.dump(base1, fh, indent=1, sort_keys=True)

    sys.stderr.write("contaminated: the same frozen tree with the audit's own report filed in it ...\n")
    cont = run_audit(frozen, inject=tmp)
    os.unlink(tmp)

    h_after = tree_hash(frozen)
    shutil.rmtree(scratch, ignore_errors=True)

    b1 = {c["id"]: c for c in base1["checks"]}
    b2 = {c["id"]: c for c in base2["checks"]}
    c3 = {c["id"]: c for c in cont["checks"]}

    rows = []
    for cid in sorted(set(b1) | set(b2) | set(c3)):
        x, y, z = b1.get(cid, {}), b2.get(cid, {}), c3.get(cid, {})
        unstable = sig(x) != sig(y)
        differs = sig(x) != sig(z)
        rows.append({
            "id": cid,
            "reads_the_whole_tree": len(x.get("repo_dirs_listed") or []) > 4,
            "containment_verdict": x.get("verdict_containment"),
            "baseline1_stdout_shas": x.get("stdout_shas"),
            "baseline2_stdout_shas": y.get("stdout_shas"),
            "contaminated_stdout_shas": z.get("stdout_shas"),
            "baseline1_exit_codes": x.get("exit_codes"),
            "baseline2_exit_codes": y.get("exit_codes"),
            "contaminated_exit_codes": z.get("exit_codes"),
            "unstable_between_two_identical_baselines": unstable,
            "differs_from_baseline1": differs,
            "report_moved_because_of_this_audit": bool(differs and not unstable),
        })

    moved = [r["id"] for r in rows if r["report_moved_because_of_this_audit"]]
    excluded = [r["id"] for r in rows if r["unstable_between_two_identical_baselines"]]
    summary = {
        "generated_by": "tools/convergence/contamination_133.py",
        "session": 133,
        "question": "does filing this audit's own report in the repository change the "
                    "report of any check the audit measures?",
        "population": len(rows),
        "frozen_record_sha256_before": h_before,
        "frozen_record_sha256_after": h_after,
        "record_provably_unchanged_across_all_three_passes": h_before == h_after,
        "excluded_as_unstable_on_their_own": excluded,
        "checks_whose_report_moved": moved,
        "count_moved": len(moved),
        "verdict": ("THIS AUDIT CONTAMINATES ITS OWN POPULATION" if moved
                    else "NO CHECK IN THIS POPULATION MOVED WHEN THE AUDIT'S REPORT WAS FILED"),
        "verdict_scope": ("The verdict covers only the checks not excluded above. An "
                          "excluded check is not cleared: it is a check this test cannot "
                          "attribute anything to, because it moves on its own."),
        "rows": rows,
    }
    with open(OUT, "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps({k: summary[k] for k in
                      ("count_moved", "checks_whose_report_moved",
                       "excluded_as_unstable_on_their_own", "verdict")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
