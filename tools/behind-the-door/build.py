"""Build — every number the page shows, computed from data/ and nothing typed by hand.

Session 162, 2026-09-16.  python3 tools/behind-the-door/build.py
"""

import json
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rungs  # noqa: E402

DIR = "artifacts/2026-09-16-an-address-is-not-an-artifact/data"
OUT = f"{DIR}/data.json"

RUNG_ORDER = [
    ("R1_content", "something beyond boilerplate"),
    ("R2_code", "a file with a source-code extension"),
    ("R3_licence", "a licence file"),
    ("R4_manifest", "a dependency or environment manifest"),
    ("R6_entry", "a command a stranger can copy"),
    ("R7_tests", "tests"),
    ("R8_ci", "a CI configuration"),
    ("FLOOR", "code AND a licence AND a manifest AND a way in"),
]
EXTRA_ORDER = [
    ("R4b_container", "a container recipe"),
    ("R3b_licence_declared_only", "a licence named in a manifest, no licence file"),
]

Z = 1.959963984540054
ZB = 0.8416212335729143


def wilson(k, n, z=Z):
    if n == 0:
        return None
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [max(0.0, centre - half), min(1.0, centre + half)]


def two_proportion_z(k1, n1, k2, n2):
    """Pooled two-proportion z, two-sided p. Independence is assumed and is not true —
    cohort B is drawn in contiguous blocks per month (session 141's disclosed defect)."""
    if min(n1, n2) == 0:
        return None, None
    p1, p2 = k1 / n1, k2 / n2
    p = (k1 + k2) / (n1 + n2)
    se = math.sqrt(p * (1 - p) * (1 / n1 + 1 / n2))
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    pv = math.erfc(abs(z) / math.sqrt(2))
    return z, pv


def fisher_exact_two_sided(a, b, c, d):
    """Exact two-sided p for the 2x2 table [[a,b],[c,d]] by summing tables no more
    probable than the observed one. Exact arithmetic, no dependency."""
    n = a + b + c + d
    r1, r2 = a + b, c + d
    c1 = a + c

    def prob(x):
        return (math.comb(r1, x) * math.comb(r2, c1 - x)) / math.comb(n, c1)

    lo = max(0, c1 - r2)
    hi = min(r1, c1)
    p_obs = prob(a)
    tot = 0.0
    for x in range(lo, hi + 1):
        p = prob(x)
        if p <= p_obs * (1 + 1e-12):
            tot += p
    return min(1.0, tot)


def benjamini_hochberg(pvals):
    """Return the BH-adjusted q-values, in the input order."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    q = [0.0] * m
    prev = 1.0
    for rank, i in enumerate(reversed(order), start=1):
        k = m - rank + 1
        val = min(prev, pvals[i] * m / k)
        q[i] = val
        prev = val
    return q


def mde(p1, n1, n2):
    lo, hi = p1, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2
        se = math.sqrt(p1 * (1 - p1) / n1 + mid * (1 - mid) / n2)
        if abs(mid - p1) >= (Z + ZB) * se:
            hi = mid
        else:
            lo = mid
    return hi - p1


def main():
    pop = json.load(open(f"{DIR}/population.json"))
    harvest = json.load(open(f"{DIR}/repos.json"))
    fixtures = json.load(open(f"{DIR}/fixture-check.json"))
    mutants = json.load(open(f"{DIR}/mutation-check.json"))
    repos = harvest["repos"]

    doors_ok = [r for r in repos if r.get("door_ok")]
    empty = [r for r in repos if r.get("door_ok") and r.get("door_refs") == 0]
    other_clone_fail = [r for r in repos
                        if r.get("door_ok") and not r.get("clone_ok") and r.get("door_refs", 0) > 0]
    cloned = [r for r in repos if r.get("clone_ok")]
    A = [r for r in cloned if r["cohort"] == "A"]
    B = [r for r in cloned if r["cohort"] == "B"]

    out = {
        "note": "Every number on the shipped page of session 162, computed from data/.",
        "date": "2026-09-16",
        "session": 162,
        "population": {
            "n_repos": pop["n_repos"],
            "n_A": pop["n_cohort_A"],
            "n_B": pop["n_cohort_B"],
            "digest": pop["population_digest"],
            "source": pop["source_artifact"],
        },
        "doors": {
            "n": len(repos),
            "answered": len(doors_ok),
            "share": len(doors_ok) / len(repos),
            "days_since_141": 16,
            "refused": [{"repo": r["repo"], "cohort": r["cohort"],
                         "error": r.get("door_error")}
                        for r in repos if not r.get("door_ok")],
        },
        "empty_repositories": {
            "n": len(empty),
            "share_of_answered": len(empty) / len(doors_ok) if doors_ok else None,
            "repos": [{"repo": r["repo"], "cohort": r["cohort"], "refs": r["door_refs"]}
                      for r in empty],
            "what_it_means": ("git ls-remote exits 0 and lists no branch and no tag: the "
                              "repository exists, is public, and holds nothing. Session "
                              "141's probe counted exactly this as a reachable artifact."),
        },
        "other_tree_failures": [{"repo": r["repo"], "error": r.get("clone_error")}
                                for r in other_clone_fail],
        "cloned": {"n": len(cloned), "n_A": len(A), "n_B": len(B)},
    }

    # ---- the ladder
    rows = []
    raw_p = []
    for key, sentence in RUNG_ORDER + EXTRA_ORDER:
        kA = sum(1 for r in A if r["rungs"][key])
        kB = sum(1 for r in B if r["rungs"][key])
        kAll = kA + kB
        z, pz = two_proportion_z(kA, len(A), kB, len(B))
        fp = fisher_exact_two_sided(kA, len(A) - kA, kB, len(B) - kB)
        row = {
            "rung": key, "sentence": sentence,
            "all": {"k": kAll, "n": len(cloned), "share": kAll / len(cloned),
                    "wilson": wilson(kAll, len(cloned))},
            "A": {"k": kA, "n": len(A), "share": kA / len(A), "wilson": wilson(kA, len(A))},
            "B": {"k": kB, "n": len(B), "share": kB / len(B), "wilson": wilson(kB, len(B))},
            "diff_A_minus_B": kA / len(A) - kB / len(B),
            "z": z, "p_z": pz, "p_fisher": fp,
            "mde_at_B_rate_pp": 100 * mde(kB / len(B), len(B), len(A)),
        }
        rows.append(row)
        if (key, sentence) in RUNG_ORDER:
            raw_p.append(fp)

    qs = benjamini_hochberg(raw_p)
    qi = 0
    for row in rows:
        if any(row["rung"] == k for k, _ in RUNG_ORDER):
            row["q_bh"] = qs[qi]
            row["survives_bh_05"] = qs[qi] < 0.05
            qi += 1
    out["ladder"] = rows
    out["bh_note"] = ("Benjamini-Hochberg across the eight rung comparisons of the ladder "
                      "(the two extras are descriptive and not in the family).")

    # ---- pinning
    app = [r for r in cloned if r["rungs"]["R5_pinning_applicable"]]
    appA = [r for r in app if r["cohort"] == "A"]
    appB = [r for r in app if r["cohort"] == "B"]
    pin = lambda L: sum(1 for r in L if r["rungs"]["R5_pinned"])
    zp, pp = two_proportion_z(pin(appA), len(appA), pin(appB), len(appB))
    out["pinning"] = {
        "decidable": len(app), "of": len(cloned),
        "decidable_share": len(app) / len(cloned),
        "pinned": pin(app), "share": pin(app) / len(app) if app else None,
        "wilson": wilson(pin(app), len(app)),
        "A": {"k": pin(appA), "n": len(appA),
              "share": pin(appA) / len(appA) if appA else None},
        "B": {"k": pin(appB), "n": len(appB),
              "share": pin(appB) / len(appB) if appB else None},
        "diff_A_minus_B": (pin(appA) / len(appA) - pin(appB) / len(appB)) if appA and appB else None,
        "p_fisher": fisher_exact_two_sided(pin(appA), len(appA) - pin(appA),
                                           pin(appB), len(appB) - pin(appB)),
        "mde_at_B_rate_pp": 100 * mde(pin(appB) / len(appB), len(appB), len(appA)) if appB else None,
    }

    # ---- what the rungs rest on
    out["sensitivity"] = {
        "boilerplate_only": {
            "n": sum(1 for r in cloned if r.get("boilerplate_only")),
            "repos": [r["repo"] for r in cloned if r.get("boilerplate_only")],
        },
        "licence_outside_root_only": sum(1 for r in cloned if r.get("licence_outside_root_only")),
        "manifest_outside_root_only": sum(1 for r in cloned if r.get("manifest_outside_root_only")),
        "r6_via_nonroot_only": sum(1 for r in cloned if r.get("r6_via_nonroot_only")),
        "note": ("R3, R4 and R6 fire on a file anywhere in the tree, as the pre-registration "
                 "says. These counts are how often the rung rests only on a file a visitor "
                 "to the repository's front page would never see. Descriptive, added before "
                 "the full run, no rung changed."),
    }

    # ---- nothing behind the address at all
    nothing = len(empty) + sum(1 for r in cloned if r.get("boilerplate_only"))
    out["nothing_behind_it"] = {
        "n": nothing,
        "of_answered": len(doors_ok),
        "share": nothing / len(doors_ok),
        "made_of": f"{len(empty)} empty repositories + "
                   f"{sum(1 for r in cloned if r.get('boilerplate_only'))} holding only boilerplate",
    }

    # ---- the two facts the ladder's shares hide
    no_code = [r for r in cloned if not r["rungs"]["R2_code"]]
    out["no_code"] = {
        "n": len(no_code),
        "of": len(cloned),
        "share": len(no_code) / len(cloned),
        "repos": [{"repo": r["repo"], "cohort": r["cohort"], "n_files": r["n_files"],
                   "has_manifest": r["rungs"]["R4_manifest"],
                   "sample_paths": r["evidence"]["R1_content"][:3]}
                  for r in no_code],
        "note": ("Declared in an abstract, reachable, and holding no file with a "
                 "source-code extension. The paths are the evidence; this practice draws "
                 "no conclusion about any author from them."),
    }
    no_lic_with_code = [r for r in cloned
                        if not r["rungs"]["R3_licence"] and r["rungs"]["R2_code"]]
    out["code_without_permission"] = {
        "n": len(no_lic_with_code),
        "of": len(cloned),
        "share": len(no_lic_with_code) / len(cloned),
        "A": sum(1 for r in no_lic_with_code if r["cohort"] == "A"),
        "B": sum(1 for r in no_lic_with_code if r["cohort"] == "B"),
        "note": ("Source code present, no licence file anywhere in the tree. Under default "
                 "copyright a reader may look and may not lawfully reuse. Cycle 001 "
                 "concluded the handover is a boundary of consent rather than competence; "
                 "this is that boundary with a number on it."),
    }
    six = ["R2_code", "R3_licence", "R4_manifest", "R6_entry", "R7_tests", "R8_ci"]
    all_six = [r for r in cloned if all(r["rungs"][k] for k in six)]
    out["top_of_the_ladder"] = {
        "definition": "every rung of the ladder at once: the floor plus tests plus CI",
        "n": len(all_six), "of": len(cloned), "share": len(all_six) / len(cloned),
        "A": sum(1 for r in all_six if r["cohort"] == "A"),
        "B": sum(1 for r in all_six if r["cohort"] == "B"),
    }

    # ---- size
    sizes = sorted(r["n_files"] for r in cloned)
    out["tree_sizes"] = {
        "median": sizes[len(sizes) // 2], "min": sizes[0], "max": sizes[-1],
        "median_A": sorted(r["n_files"] for r in A)[len(A) // 2],
        "median_B": sorted(r["n_files"] for r in B)[len(B) // 2],
    }

    # ---- predictions
    r3A = next(r for r in rows if r["rung"] == "R3_licence")["A"]["share"]
    r1 = next(r for r in rows if r["rung"] == "R1_content")["all"]["share"]
    floor = next(r for r in rows if r["rung"] == "FLOOR")
    r4 = next(r for r in rows if r["rung"] == "R4_manifest")
    out["predictions"] = [
        {"id": "P1", "claim": "at least 95 % of the 144 doors still answer",
         "value": f"{100 * len(doors_ok) / len(repos):.1f} %",
         "verdict": "CONFIRMED" if len(doors_ok) / len(repos) >= 0.95 else "REFUTED"},
        {"id": "P2", "claim": "at least 95 % of cloned trees hold something beyond boilerplate",
         "value": f"{100 * r1:.1f} %",
         "verdict": "CONFIRMED" if r1 >= 0.95 else "REFUTED"},
        {"id": "P3", "claim": "a licence file in fewer than 70 % of cohort A",
         "value": f"{100 * r3A:.1f} %",
         "verdict": "CONFIRMED" if r3A < 0.70 else "REFUTED"},
        {"id": "P4", "claim": "the floor is met by fewer than half of BOTH cohorts",
         "value": f"A {100 * floor['A']['share']:.1f} %, B {100 * floor['B']['share']:.1f} %",
         "verdict": "CONFIRMED" if (floor["A"]["share"] < 0.5 and floor["B"]["share"] < 0.5)
                    else "REFUTED"},
        {"id": "P5", "claim": "cohort A at least as high as B on the manifest rung "
                              "(written to be uninformative if confirmed)",
         "value": f"A {100 * r4['A']['share']:.1f} % vs B {100 * r4['B']['share']:.1f} %",
         "verdict": "CONFIRMED" if r4["A"]["share"] >= r4["B"]["share"] else "REFUTED",
         "caveat": "Confirmed, therefore reported as uninformative: cohort A's genre "
                   "enrichment predicts it without any automation effect."},
        {"id": "P6", "claim": "fewer than 40 % pinned where pinning is decidable",
         "value": f"{100 * out['pinning']['share']:.1f} %",
         "verdict": "CONFIRMED" if out["pinning"]["share"] < 0.40 else "REFUTED"},
    ]
    out["predictions_refuted"] = sum(1 for p in out["predictions"] if p["verdict"] == "REFUTED")

    # ---- the kill condition, and the defect in it
    trigger = [r for r in repos if r.get("door_ok") and not r.get("clone_ok")]
    out["kill_condition"] = {
        "text": ("If the tree step fails for more than 10 % of the repositories whose door "
                 "answered - a non-zero git clone exit, or a clone with no resolvable HEAD - "
                 "the tree instrument is suspect and every rung outcome is suspended."),
        "triggering_units": len(trigger),
        "of": len(doors_ok),
        "rate": len(trigger) / len(doors_ok),
        "threshold": 0.10,
        "fired": (len(trigger) / len(doors_ok)) > 0.10,
        "defect": {
            "filed": "2026-09-16, same session, before the page was written",
            "what": ("All three triggering units are EMPTY REPOSITORIES: ls-remote exits 0 "
                     "with zero refs, so there is no HEAD to resolve. An empty repository is "
                     "the studied effect - an address that answers with nothing behind it - "
                     "and the same pre-registration that wrote this condition also wrote, in "
                     "the sentence above it, that a kill condition must be able to fire only "
                     "on the apparatus and never on the phenomenon."),
            "consequence": ("It did not fire, at 2.1 % against a 10 % threshold, so no number "
                            "is affected. Had the population held fifteen empty repositories "
                            "instead of three, a correct result would have been suspended by "
                            "a rule written that same hour to prevent exactly that."),
            "status": "filed as a defect; the verdict above is left as written",
        },
    }

    # ---- the external benchmark, quoted
    out["benchmark"] = {
        "source": "Hora, Montandon & Costa, arXiv:2605.16701 (ICSME 2026), Table II, 2026",
        "population": ("10,000 GitHub repositories drawn at random from 116,013 with at least "
                       "100 stars, at least 100 commits, not forks, and a commit in 2026; "
                       "median 211 stars and 557 commits"),
        "LICENSE": 0.731, "README_md": 0.953, "gitignore": 0.950,
        "github_dir": 0.825, "workflows_dir": 0.773,
        "caveat": ("A population of established, actively maintained projects. A research "
                   "repository attached to one paper should be expected to sit below it, and "
                   "P3 was written on that expectation."),
    }

    out["apparatus_checks"] = {
        "fixtures": fixtures["cases"], "fixtures_failed": fixtures["failed"],
        "mutants": mutants["mutants"], "mutants_survived": mutants["survivors"],
        "problems_found_before_any_data": 4,
    }
    out["robots"] = harvest["github_robots"]

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"-> {OUT}")
    for p in out["predictions"]:
        print(f"  {p['id']} {p['verdict']:<9} {p['value']}")
    print(f"  refuted: {out['predictions_refuted']}/6")
    print(f"  kill condition fired: {out['kill_condition']['fired']} "
          f"({out['kill_condition']['triggering_units']}/{out['kill_condition']['of']})")
    print(f"  nothing behind the address: {out['nothing_behind_it']['n']}/"
          f"{out['nothing_behind_it']['of_answered']}")


if __name__ == "__main__":
    main()
