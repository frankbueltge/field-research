#!/usr/bin/env python3
"""Re-fetch the 156 licence-shaped files of session 163, at the commits it pinned.

Session 165, 2026-09-20. No file is committed: what is committed is, per blob, the
repository, the path, the head commit, the sha256 recorded on 2026-09-18 and the
sha256 read tonight. A blob whose digest moved is excluded from the scored set and
named.
"""
import concurrent.futures as cf
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

UA = "field-research/meridian (research measurement; contact via repository)"
SRC = "artifacts/2026-09-18-a-licence-file-is-not-a-licence/data/data.json"


def targets(root):
    d = json.load(open(os.path.join(root, SRC)))
    out = []
    for r in d["repos"]:
        for f in r.get("files", []):
            out.append({"repo": r["repo"], "head_sha": r["head_sha"], "path": f["path"],
                        "sha256_0918": f["sha256"], "bytes_0918": f["bytes"]})
    return out


def one(t):
    url = ("https://raw.githubusercontent.com/" + t["repo"] + "/" + t["head_sha"] + "/"
           + urllib.parse.quote(t["path"]))
    rec = dict(t, url=url)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            rec["http"] = r.status
    except urllib.error.HTTPError as exc:
        rec.update(http=exc.code, error=f"HTTPError: {exc.code}", sha256=None)
        return rec, None
    except Exception as exc:
        rec.update(http=None, error=f"{type(exc).__name__}: {exc}", sha256=None)
        return rec, None
    rec["sha256"] = hashlib.sha256(raw).hexdigest()
    rec["bytes"] = len(raw)
    rec["error"] = None
    rec["digest_matches"] = rec["sha256"] == t["sha256_0918"]
    return rec, raw


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    out = sys.argv[2] if len(sys.argv) > 2 else "/tmp/c2"
    os.makedirs(out, exist_ok=True)
    ts = targets(root)
    print(f"{len(ts)} blobs pinned on 2026-09-18", file=sys.stderr)
    recs, texts = [], {}
    with cf.ThreadPoolExecutor(max_workers=8) as ex:
        for rec, raw in ex.map(one, ts):
            key = rec["repo"] + "@" + rec["path"]
            recs.append(rec)
            if raw is not None:
                # decode exactly as session 163 did: utf-8 with replacement
                texts[key] = raw.decode("utf-8", "replace")
    man = {
        "note": "Session 165. The 156 licence-shaped files of 2026-09-18, re-fetched at "
                "the head commits that session pinned. No file text is committed.",
        "n_pinned": len(ts),
        "n_fetched": sum(1 for r in recs if r["sha256"]),
        "n_digest_matches": sum(1 for r in recs if r.get("digest_matches")),
        "excluded": [f'{r["repo"]}@{r["path"]}' for r in recs
                     if not r.get("digest_matches")],
        "entries": sorted(recs, key=lambda r: (r["repo"], r["path"])),
    }
    man["corpus_digest"] = hashlib.sha256("".join(
        f'{e["repo"]}@{e["path"]}:{e.get("sha256")}\n'
        for e in man["entries"]).encode()).hexdigest()
    json.dump(texts, open(os.path.join(out, "texts.json"), "w"))
    json.dump(man, open(os.path.join(out, "manifest.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in man.items() if k != "entries"}, indent=1))


if __name__ == "__main__":
    main()
