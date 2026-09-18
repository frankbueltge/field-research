#!/usr/bin/env python3
"""Knock on all 144 doors again, list every tree, read every licence-shaped blob.

Session 163, 2026-09-18. Population inherited unrepaired from session 162.
Nothing here decides anything: it fetches and records. The verdicts are computed by
build.py from what this file writes, so the measurement can be re-run without the
network.

Usage: python3 harvest.py <population.json> <out.json> [max_workers]
"""
import concurrent.futures as cf
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rules
from fingerprints import normalise

TIMEOUT = 180


def run(cmd, cwd=None, timeout=TIMEOUT, text=True):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=text, timeout=timeout)


def utc():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def harvest_one(row):
    url = f"https://github.com/{row['repo']}.git"
    out = {"repo": row["repo"], "cohort": row["cohort"], "url": (row.get("declared_urls") or [None])[0],
           "probed_utc": utc(), "door_ok": False, "door_refs": None,
           "clone_ok": False, "head_sha": None, "n_files": None,
           "tree_digest": None, "licence_paths": [], "blobs": [],
           "blob_errors": [], "error": None}
    # --- the door, again: 18 days after 2026-08-31, 2 after 2026-09-16
    try:
        p = run(["git", "ls-remote", "--heads", "--tags", url], timeout=90)
        out["door_ok"] = p.returncode == 0
        out["door_refs"] = len([l for l in p.stdout.splitlines() if l.strip()])
        if p.returncode != 0:
            out["error"] = f"ls-remote exit {p.returncode}: {p.stderr.strip()[:200]}"
    except subprocess.TimeoutExpired:
        out["error"] = "ls-remote timeout"
        return out
    if not out["door_ok"]:
        return out
    if out["door_refs"] == 0:
        out["error"] = "no refs — repository exists and holds no commit"
        return out

    tmp = tempfile.mkdtemp(prefix="lic-")
    try:
        p = run(["git", "clone", "--filter=blob:none", "--no-checkout", "--quiet",
                 url, os.path.join(tmp, "r")], timeout=TIMEOUT)
        if p.returncode != 0:
            out["error"] = f"clone exit {p.returncode}: {p.stderr.strip()[:200]}"
            return out
        repo = os.path.join(tmp, "r")
        out["clone_ok"] = True
        h = run(["git", "rev-parse", "HEAD"], cwd=repo)
        out["head_sha"] = h.stdout.strip() if h.returncode == 0 else None
        if out["head_sha"] is None:
            out["error"] = "no resolvable HEAD"
            return out
        t = run(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=repo)
        if t.returncode != 0:
            out["error"] = f"ls-tree exit {t.returncode}: {t.stderr.strip()[:200]}"
            return out
        files = [l for l in t.stdout.split("\n") if l]
        out["n_files"] = len(files)
        out["tree_digest"] = hashlib.sha256(
            "\n".join(sorted(files)).encode()).hexdigest()
        lic = sorted(p for p in files if rules.is_licence_shaped(p))
        out["licence_paths"] = lic
        for path in lic:
            try:
                b = subprocess.run(["git", "cat-file", "blob", f"HEAD:{path}"],
                                   cwd=repo, capture_output=True, timeout=120)
            except subprocess.TimeoutExpired:
                out["blob_errors"].append({"path": path, "error": "cat-file timeout"})
                continue
            if b.returncode != 0:
                out["blob_errors"].append(
                    {"path": path, "error": f"cat-file exit {b.returncode}: "
                                            f"{b.stderr.decode('utf-8','replace').strip()[:160]}"})
                continue
            raw = b.stdout
            text = raw.decode("utf-8", "replace")
            out["blobs"].append({
                "path": path,
                "bytes": len(raw),
                "sha256": hashlib.sha256(raw).hexdigest(),
                "text": text,
            })
    except subprocess.TimeoutExpired:
        out["error"] = "clone/tree timeout"
    except Exception as exc:                                  # noqa: BLE001
        out["error"] = f"{type(exc).__name__}: {exc}"
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    return out


def main(pop_path, out_path, workers=6):
    pop = json.load(open(pop_path))
    repos = pop["repos"]
    started = utc()
    t0 = time.time()
    results = []
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        futs = {ex.submit(harvest_one, r): r for r in repos}
        for i, f in enumerate(cf.as_completed(futs), 1):
            results.append(f.result())
            if i % 20 == 0:
                print(f"  {i}/{len(repos)}  {time.time()-t0:.0f}s", flush=True)
    results.sort(key=lambda r: r["repo"])
    out = {
        "note": "Session 163. All 144 doors of session 162's population re-knocked, every "
                "tree listed, every licence-shaped blob read. Fetch only: no verdicts here. "
                "Blob text is kept in this working file and is NOT committed — build.py "
                "derives the committed evidence from it.",
        "population_digest": pop["population_digest"],
        "started_utc": started, "finished_utc": utc(),
        "seconds": round(time.time() - t0, 1),
        "n": len(results),
        "repos": results,
    }
    json.dump(out, open(out_path, "w"), indent=1)
    doors = sum(1 for r in results if r["door_ok"])
    clones = sum(1 for r in results if r["clone_ok"])
    blobs = sum(len(r["blobs"]) for r in results)
    errs = sum(len(r["blob_errors"]) for r in results)
    print(f"doors {doors}/{len(results)} · clones {clones} · licence blobs {blobs} · "
          f"blob errors {errs} · {out['seconds']}s")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 6)
