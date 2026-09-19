#!/usr/bin/env python3
"""Run every implementation over both arms. Session 164, 2026-09-19.

Usage: run.py <spdx-dir> <impl-dir> <out.json>

R-ship  this practice's 09-18 instrument as shipped, imported not copied.
R-def   the same with defect 1 of 09-18 restored: every line carrying the word
        'copyright' read as a copyright notice. Positive control (K4).
I*      the independent implementations, loaded by file path.
"""
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE)) if False else os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "is-it-a-licence"))

from inputs import fill                                     # noqa: E402
import fingerprints as fp                                   # noqa: E402
import rules                                                # noqa: E402


def r_ship(text):
    fams = rules.l1_families(text)
    return {"families": fams, "attribution": rules.l2_attribution(text, fams)}


def r_def(text):
    """Defect 1 restored, and restored ONLY for the duration of this call."""
    keep = fp.is_copyright_notice
    fp.is_copyright_notice = fp.mentions_copyright
    try:
        fams = rules.l1_families(text)
        return {"families": fams, "attribution": rules.l2_attribution(text, fams)}
    finally:
        fp.is_copyright_notice = keep


def load(path):
    name = "impl_" + os.path.basename(path).replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.score


VOCAB = {"MIT", "ISC", "BSD-4-Clause", "BSD-3-Clause", "BSD-2-Clause", "Zlib", "Apache-2.0",
         "GPL-3.0", "GPL-2.0", "LGPL-3.0", "LGPL-2.1", "AGPL-3.0", "MPL-2.0", "EPL-2.0",
         "BSL-1.0", "Unlicense", "CC0-1.0", "CC-BY-NC-SA-4.0", "CC-BY-NC-4.0", "CC-BY-SA-4.0",
         "CC-BY-4.0", "WTFPL", "OpenRAIL", "Llama-Community"}
ATTR = {"named", "placeholder", "no_holder", "no_copyright_line", None}


def shape_ok(v):
    if not isinstance(v, dict):
        return False, "not a dict"
    if set(v) != {"families", "attribution"}:
        return False, f"keys {sorted(v)}"
    f = v["families"]
    if not isinstance(f, (list, tuple)):
        return False, "families not a list"
    bad = [x for x in f if x not in VOCAB]
    if bad:
        return False, f"out-of-vocabulary {bad}"
    if v["attribution"] not in ATTR:
        return False, f"attribution {v['attribution']!r}"
    return True, None


def main():
    spdx_dir, impl_dir, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    texts = json.load(open(os.path.join(spdx_dir, "texts.json")))
    manifest = json.load(open(os.path.join(spdx_dir, "manifest.json")))
    ids = sorted(texts)

    impls = {"R-ship": r_ship, "R-def": r_def}
    delivery = {"R-ship": {"delivered": True, "note": "this practice's shipped instrument"},
                "R-def": {"delivered": True, "note": "positive control, defect 1 restored"}}
    for fn in sorted(os.listdir(impl_dir)):
        if not fn.endswith(".py"):
            continue
        label = "I-" + fn.replace("impl_", "").replace(".py", "")
        try:
            impls[label] = load(os.path.join(impl_dir, fn))
            delivery[label] = {"delivered": True, "note": "independent implementation"}
        except Exception as exc:
            delivery[label] = {"delivered": False, "note": f"import failed: {type(exc).__name__}: {exc}"}

    rows, errors = [], {k: [] for k in impls}
    for lid in ids:
        c = texts[lid]
        f = fill(c)
        for arm, text in (("C", c), ("F", f)):
            row = {"id": lid, "arm": arm, "same_as_C": (arm == "F" and f == c)}
            for label, fn in impls.items():
                try:
                    v = fn(text)
                    ok, why = shape_ok(v)
                    if not ok:
                        errors[label].append({"id": lid, "arm": arm, "shape": why})
                        row[label] = None
                    else:
                        row[label] = {"families": sorted(v["families"]),
                                      "attribution": v["attribution"]}
                except Exception as exc:
                    errors[label].append({"id": lid, "arm": arm,
                                          "raised": f"{type(exc).__name__}: {exc}"})
                    row[label] = None
            rows.append(row)

    for label in list(impls):
        n_bad = len(errors[label])
        if label.startswith("I-") and n_bad:
            delivery[label]["delivered"] = False
            delivery[label]["note"] = f"K3: failed on {n_bad} of {len(ids)*2} inputs"
        delivery[label]["n_failures"] = n_bad

    json.dump({"note": "Session 164. Every implementation, both arms, one row per input.",
               "license_list_version": manifest["license_list_version"],
               "corpus_digest": manifest["corpus_digest"],
               "n_ids": len(ids), "n_rows": len(rows),
               "implementations": sorted(impls),
               "delivery": delivery,
               "errors": {k: v[:50] for k, v in errors.items()},
               "rows": rows}, open(out_path, "w"), indent=1)
    print(json.dumps(delivery, indent=1))
    print(f"{len(rows)} rows over {len(ids)} identifiers -> {out_path}")


if __name__ == "__main__":
    main()
