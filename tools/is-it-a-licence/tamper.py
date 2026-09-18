#!/usr/bin/env python3
"""Corrupt the artifact's own evidence on purpose and require the checker to notice.

Session 163. A checker that passes on false evidence checks nothing. Each corruption
below is applied to a COPY; nothing in the artifact is touched.

    python3 tamper.py <artifact-dir> [out.json]
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile


def corruptions():
    def c(name, target, fn):
        return {"name": name, "target": target, "fn": fn}

    def bump_headline(d):
        d["headline"]["k"] += 1
    def wrong_pct(d):
        d["headline"]["pct"] = 100.0
    def flip_repo(d):
        for r in d["repos"]:
            if r["R3_licence_0916"] and r["delivers_any"]:
                r["delivers_any"] = False
                return
    def flip_file(d):
        for r in d["repos"]:
            for f in r["files"]:
                if f["delivers"]:
                    f["delivers"] = False
                    return
    def hide_family(d):
        for r in d["repos"]:
            for f in r["files"]:
                if f["families"]:
                    f["families"] = []
                    return
    def flip_verdict(d):
        d["predictions"][0]["verdict"] = "REFUTED"
    def move_threshold(d):
        d["predictions"][3]["threshold"] = 99.0
    def wrong_d1(d):
        d["counts"]["n_D1"] = 104
    def drop_repo(d):
        d["repos"].pop()
    def wrong_digest(d):
        d["population_digest"] = "0" * 64
    def hide_k2(d):
        d["kill_conditions"]["K2_blob_fetch_failures"]["failed"] = 99
    def bad_attribution(d):
        for r in d["repos"]:
            for f in r["files"]:
                if f["attribution"] == "no_holder":
                    f["attribution"] = "named"
                    return
    def short_sha(d):
        for r in d["repos"]:
            if r["files"]:
                r["files"][0]["sha256"] = "abc"
                return
    def wrong_root(d):
        d["post_hoc"]["identified_licence_at_the_root"]["k"] += 3
    def rewrite_run1(d):
        d["post_hoc"]["run1_defective_L2"]["run1_headline_pct"] = 95.2
    def inject_text(d):
        d["repos"][0]["note_added"] = ("Permission is hereby granted, free of charge, "
                                       "to any person obtaining a copy")
    def wrong_empties(d):
        d["counts"]["empty_repositories"] = []
    def wrong_doors(d):
        d["retrievability"]["doors_0918"] = 143
    def wrong_voices(d):
        for r in d["repos"]:
            if len(r["voices"]) == 1:
                r["voices"] = r["voices"] + ["GPL-3.0"]
                return
    def wrong_cohort(d):
        for r in d["repos"]:
            if r["cohort"] == "A":
                r["cohort"] = "B"
                return
    def wrong_r3(d):
        for r in d["repos"]:
            if not r["R3_licence_0916"]:
                r["R3_licence_0916"] = True
                return

    def ctrl_self(d):
        d["rows"][0]["identifies_itself"] = False
    def ctrl_mit(d):
        for r in d["rows"]:
            if r["family"] == "MIT":
                r["placeholder_fires"] = False
    def ctrl_count(d):
        d["n_fetched"] = 21

    def hand_class(d):
        d["files"][0]["class"] = "invented_class"
    def hand_path(d):
        d["files"][0]["path"] = "NOT/A/REAL/PATH"
    def hand_count(d):
        d["counts"]["not_a_licence"] = 99

    return [
        c("headline numerator raised by one", "data.json", bump_headline),
        c("headline percentage set to 100", "data.json", wrong_pct),
        c("a delivering repository flipped to not delivering", "data.json", flip_repo),
        c("a delivering file flipped to not delivering", "data.json", flip_file),
        c("an identified file's families emptied", "data.json", hide_family),
        c("P1's verdict flipped", "data.json", flip_verdict),
        c("P4's threshold moved after the fact", "data.json", move_threshold),
        c("D1 size understated by one", "data.json", wrong_d1),
        c("one repository row deleted", "data.json", drop_repo),
        c("population digest replaced", "data.json", wrong_digest),
        c("K2 failures inflated while the verdict stays false", "data.json", hide_k2),
        c("a no-holder file relabelled as named", "data.json", bad_attribution),
        c("a blob digest truncated", "data.json", short_sha),
        c("post-hoc root count raised by three", "data.json", wrong_root),
        c("the defective first run's headline rewritten", "data.json", rewrite_run1),
        c("licence text injected into the committed evidence", "data.json", inject_text),
        c("the empty repositories hidden", "data.json", wrong_empties),
        c("a door removed from the retrievability count", "data.json", wrong_doors),
        c("a family added to a repository's voices", "data.json", wrong_voices),
        c("a cohort label flipped", "data.json", wrong_cohort),
        c("a repository promoted into D1", "data.json", wrong_r3),
        c("a canonical text made to fail its own identification", "control-check.json", ctrl_self),
        c("the MIT canon's placeholder result flipped", "control-check.json", ctrl_mit),
        c("the canon fetch count understated", "control-check.json", ctrl_count),
        c("a hand-reading class invented", "hand-reading.json", hand_class),
        c("a hand-reading path pointed at nothing", "hand-reading.json", hand_path),
        c("a hand-reading tally inflated", "hand-reading.json", hand_count),
    ]


def main(art_dir, out_path=None):
    art_dir = os.path.abspath(art_dir)
    check = os.path.join(art_dir, "check.py")
    src = os.path.join(art_dir, "data")
    rows = []
    for corr in corruptions():
        tmp = tempfile.mkdtemp(prefix="tamper-")
        dst = os.path.join(tmp, "data")
        shutil.copytree(src, dst)
        path = os.path.join(dst, corr["target"])
        d = json.load(open(path))
        corr["fn"](d)
        json.dump(d, open(path, "w"), indent=1)
        env = dict(os.environ, CHECK_DATA_DIR=dst)
        p = subprocess.run([sys.executable, check], capture_output=True, text=True, env=env)
        caught = p.returncode != 0
        first = next((l.strip()[5:].strip() for l in p.stdout.splitlines()
                      if l.strip().startswith("FAIL")), None)
        rows.append({"corruption": corr["name"], "file": corr["target"],
                     "caught": caught, "first_failure": first})
        shutil.rmtree(tmp, ignore_errors=True)
        print(("  caught  " if caught else "  MISSED  ") + corr["name"])
    missed = [r for r in rows if not r["caught"]]
    out = {"note": "Deliberate corruptions of this artifact's own evidence, each applied to a "
                   "copy and put to check.py. A corruption the checker does not catch is a hole "
                   "in the checker.",
           "n": len(rows), "n_caught": len(rows) - len(missed), "n_missed": len(missed),
           "corruptions": rows}
    if out_path:
        open(out_path, "w").write(json.dumps(out, indent=1) + "\n")
    print(f"{len(rows)} corruptions, {len(missed)} missed")
    return 1 if missed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
