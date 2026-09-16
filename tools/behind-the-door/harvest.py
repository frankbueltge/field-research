"""Harvest — knock on each door, read each tree, read a fixed few files, code the rungs.

Session 162, 2026-09-16. Run AFTER the pre-registration commit and not before.

    python3 tools/behind-the-door/harvest.py

What leaves this machine: one ``git ls-remote`` per repository, one blobless partial clone,
and one lazy blob fetch per file on a fixed name list. What is recorded: path counts, a
digest of the path list, the rung outcomes, up to three matched paths per rung as evidence,
and the byte size and SHA-256 of each file read. **No third-party file content is stored or
committed** (protocol v4 §7).
"""

import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rungs  # noqa: E402

POP = "artifacts/2026-09-16-an-address-is-not-an-artifact/data/population.json"
OUT = "artifacts/2026-09-16-an-address-is-not-an-artifact/data/repos.json"
WORK = os.environ.get("BTD_WORK", "/tmp/btd-work")

BLOB_CAP = 256 * 1024
WORKERS = 6

# The only file names whose contents are read. Fixed in the pre-registration.
BLOB_NAMES = {
    "readme", "readme.md", "readme.rst", "readme.txt", "readme.markdown",
    "license", "license.md", "license.txt", "licence", "licence.md", "licence.txt",
    "copying", "requirements.txt", "pyproject.toml", "setup.py", "setup.cfg",
    "pipfile", "environment.yml", "environment.yaml", "package.json",
    "cargo.toml", "go.mod", "description", "makefile",
}


def run(cmd, cwd=None, timeout=180):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           timeout=timeout)
        return p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired:
        return 124, "", "timeout"


def wanted_blob(path):
    base = rungs.basename(path).lower()
    if base in BLOB_NAMES:
        return True
    if rungs.MANIFEST_PATTERNS[0].match(base):
        return True
    return False


def harvest_one(entry):
    repo = entry["repo"]
    url = f"https://github.com/{repo}"
    rec = {
        "repo": repo,
        "cohort": entry["cohort"],
        "papers": entry["papers"],
        "url": url,
        "door_0831": "reachable",
        "probed_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    rc, out, err = run(["git", "ls-remote", "--heads", "--tags", url], timeout=120)
    rec["door_ok"] = rc == 0
    rec["door_refs"] = len([l for l in out.splitlines() if l.strip()]) if rc == 0 else 0
    if rc != 0:
        rec["door_error"] = (err or out).strip().splitlines()[-1][:300] if (err or out).strip() else f"exit {rc}"
        rec["clone_ok"] = False
        return rec

    dest = os.path.join(WORK, repo.replace("/", "__"))
    shutil.rmtree(dest, ignore_errors=True)
    rc, out, err = run(["git", "clone", "--filter=blob:none", "--no-checkout",
                        "--depth", "1", "-q", url, dest], timeout=300)
    rec["clone_ok"] = rc == 0
    if rc != 0:
        rec["clone_error"] = (err or out).strip().splitlines()[-1][:300] if (err or out).strip() else f"exit {rc}"
        shutil.rmtree(dest, ignore_errors=True)
        return rec

    rc, head, _ = run(["git", "rev-parse", "HEAD"], cwd=dest, timeout=60)
    if rc != 0:
        rec["clone_ok"] = False
        rec["clone_error"] = "no resolvable HEAD"
        shutil.rmtree(dest, ignore_errors=True)
        return rec
    rec["head_sha"] = head.strip()
    rc, branch, _ = run(["git", "rev-parse", "--abbrev-ref", "HEAD"], cwd=dest, timeout=60)
    rec["default_branch"] = branch.strip() if rc == 0 else None

    rc, tree, err = run(["git", "ls-tree", "-r", "HEAD", "--name-only"], cwd=dest, timeout=180)
    if rc != 0:
        rec["clone_ok"] = False
        rec["clone_error"] = f"ls-tree failed: {(err or '').strip()[:200]}"
        shutil.rmtree(dest, ignore_errors=True)
        return rec
    files = [l for l in tree.splitlines() if l.strip()]
    rec["n_files"] = len(files)
    rec["n_dirs"] = len({"/".join(p.split("/")[:-1]) for p in files if "/" in p})
    rec["tree_digest"] = hashlib.sha256("\n".join(sorted(files)).encode()).hexdigest()

    blobs = {}
    read = {}
    for path in files:
        if not wanted_blob(path):
            continue
        size_rc, size_out, _ = run(["git", "cat-file", "-s", f"HEAD:{path}"],
                                   cwd=dest, timeout=90)
        size = int(size_out.strip()) if size_rc == 0 and size_out.strip().isdigit() else -1
        entry_rec = {"bytes": size}
        if 0 <= size <= BLOB_CAP:
            b_rc, b_out, _ = run(["git", "cat-file", "blob", f"HEAD:{path}"],
                                 cwd=dest, timeout=120)
            if b_rc == 0:
                blobs[path] = b_out
                entry_rec["sha256"] = hashlib.sha256(b_out.encode(errors="replace")).hexdigest()
                entry_rec["read"] = True
            else:
                entry_rec["read"] = False
                entry_rec["why"] = "blob fetch failed"
        else:
            entry_rec["read"] = False
            entry_rec["why"] = "over the 256 KiB cap" if size > BLOB_CAP else "size unknown"
        read[path] = entry_rec
    rec["blobs_read"] = read

    coded = rungs.code_repo(files, blobs)
    rec["rungs"] = coded

    # Evidence: up to three paths per rung that made it fire, so a reader can check.
    ev = {}
    ev["R1_content"] = [p for p in files if not rungs.BOILERPLATE_RE.match(rungs.basename(p))][:3]
    ev["R2_code"] = [p for p in files if rungs.ext(p) in rungs.SOURCE_EXT][:3]
    lic = [p for p in files if rungs.LICENCE_BASENAME_RE.match(rungs.basename(p))]
    ev["R3_licence"] = lic[:3]
    ev["R4_manifest"] = [p for p in files if rungs._is_manifest(p)][:3]
    ev["R4b_container"] = [p for p in files if rungs.CONTAINER_BASENAMES_RE.match(rungs.basename(p))][:3]
    ev["R6_entry"] = ([p for p in files
                       if rungs.basename(p).lower() in ("makefile", "gnumakefile", "justfile")][:1]
                      + [p for p in files if "/" not in p and rungs.ROOT_RUNNER_RE.match(p)][:1]
                      + [p for p in blobs
                         if rungs.basename(p).lower().startswith("readme")
                         and any(rungs.COMMAND_RE.match(l) for l in rungs.code_block_lines(blobs[p]))][:1])
    ev["R7_tests"] = [p for p in files if rungs.r7_tests([p])][:3]
    ev["R8_ci"] = [p for p in files if rungs.CI_PATH_RE.match(p)][:3]
    ev["locks"] = [p for p in files if rungs.basename(p).lower() in rungs.LOCKFILES][:3]
    rec["evidence"] = ev

    # Descriptive sensitivity fields. Added before the full run, after a two-repository
    # smoke test showed that R3, R4 and R6 can fire on files nested deep in a tree. They
    # change no rung — the rules are frozen at the pre-registration commit — and exist so
    # the artifact can report how much of each rung rests on a file a visitor to the
    # repository's front page would never see.
    rec["licence_outside_root_only"] = bool(lic) and all("/" in p for p in lic)
    rec["boilerplate_only"] = not coded["R1_content"]
    manifests = ev["R4_manifest"] and [p for p in files if rungs._is_manifest(p)]
    rec["manifest_outside_root_only"] = bool(manifests) and all("/" in p for p in manifests)
    r6_root = (
        any("/" not in p and rungs.basename(p).lower() in ("makefile", "gnumakefile", "justfile")
            for p in files)
        or any("/" not in p and rungs.ROOT_RUNNER_RE.match(p) for p in files)
        or any("/" not in p and rungs.basename(p).lower().startswith("readme")
               and any(rungs.COMMAND_RE.match(l) for l in rungs.code_block_lines(t))
               for p, t in blobs.items())
    )
    rec["r6_via_root"] = bool(r6_root)
    rec["r6_via_nonroot_only"] = bool(coded["R6_entry"]) and not r6_root

    shutil.rmtree(dest, ignore_errors=True)
    return rec


def github_robots():
    """Recorded for the record, not because robots.txt governs the git protocol.

    Session 161's rule is to read a host's own rulebook before recording anything about
    its door. Nothing tonight crawls a github.com web path; the git transport is the
    documented interface and robots.txt does not speak to it. The answer is recorded so
    that the claim "we checked" is checkable.
    """
    rc, out, err = run(["curl", "-sS", "-o", "-", "-w", "\n__CODE__%{http_code}",
                        "--max-time", "45",
                        "-A", "Meridian research probe (field-research; contact meridian@field-research.invalid)",
                        "https://github.com/robots.txt"], timeout=60)
    code = None
    body = out
    if "__CODE__" in out:
        body, _, code = out.rpartition("__CODE__")
    return {
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": code.strip() if code else f"exit {rc}",
        "bytes": len(body),
        "sha256": hashlib.sha256(body.encode(errors="replace")).hexdigest(),
        "mentions_star_agent": "User-agent: *" in body,
        "note": ("Recorded for the record. Nothing in this session crawls a github.com web "
                 "path: the only requests are git ls-remote, a blobless partial clone and "
                 "lazy blob fetches over the git transport, which robots.txt does not "
                 "govern. No path this file disallows was requested."),
    }


def main():
    pop = json.load(open(POP))
    os.makedirs(WORK, exist_ok=True)
    started = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    robots = github_robots()

    records = []
    with cf.ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(harvest_one, e): e["repo"] for e in pop["repos"]}
        done = 0
        for fut in cf.as_completed(futures):
            try:
                records.append(fut.result())
            except Exception as exc:  # recorded, never swallowed
                records.append({"repo": futures[fut], "harvest_exception": repr(exc)[:300]})
            done += 1
            if done % 12 == 0:
                print(f"  {done}/{len(futures)}", flush=True)

    records.sort(key=lambda r: r["repo"].lower())
    out = {
        "note": "Per-repository harvest for session 162. No third-party file content is stored here.",
        "started_utc": started,
        "finished_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "population_digest": pop["population_digest"],
        "n": len(records),
        "github_robots": robots,
        "repos": records,
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=False)
        fh.write("\n")
    doors = sum(1 for r in records if r.get("door_ok"))
    clones = sum(1 for r in records if r.get("clone_ok"))
    print(f"{len(records)} repositories: {doors} doors answered, {clones} trees read -> {OUT}")
    shutil.rmtree(WORK, ignore_errors=True)


if __name__ == "__main__":
    main()
