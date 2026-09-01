#!/usr/bin/env python3
"""Merge the door-census probes into one dataset, and compute every figure the page states.

Inputs (all committed beside the artifact):
  data/population.json      the draw, fixed before probing
  data/probes/group-*.json  the probe records, one file per probe group
  data/verification.json    the conductor's own re-checks, run after the probes

Outputs:
  data/census.csv           one row per publisher, the whole census, human-readable
  data/data.json            every figure the page states, and nothing the page does not

The evidence grade is assigned here, explicitly and by hand, from the fetch and evidence
notes each probe recorded. It is a judgment and it is auditable: the reason is in the table.
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/cycle-001/2026-09-01-a-door-to-knock-on"
DATA = ART / "data"

# Probe label -> population label. The probes were given working names; the population is
# the publisher exactly as the source record names it.
ALIAS = {
    "Elsevier": "Elsevier",
    "Oxford University Press": "Oxford University Press",
    "Cureus": "Cureus (Part of Springer Nature as of December 2022)",
    "American Heart Association": "American Heart Association",
    "Royal Society Publishing": "Royal Society Publishing",
    "American Chemical Society (ACS)": "American Chemical Society (ACS)",
    "Cell Press": "Elsevier - Cell Press",
    "American Speech-Language-Hearing Association": "American Speech-Language-Hearing Association",
    "Springer": "Springer",
    "Portland Press": "Portland Press",
    "Spandidos Publications": "Spandidos",
    "American Association for the Advancement of Science (AAAS)": "American Association for the Advancement of Science (AAAS)",
    "American Society for Microbiology": "American Society for Microbiology",
    "American Diabetes Association": "American Diabetes Association",
    "European Centre for Disease Prevention and Control": "European Centre for Disease Prevention and Control",
    "Association for Computing Machinery (ACM)": "Association for Computing Machinery (ACM)",
    "SAGE Publications": "SAGE Publications",
    "Wiley": "Wiley",
    "Dove Press": "Taylor and Francis - Dove Press",
    "American Society for Biochemistry and Molecular Biology (ASBMB)": "American Society for Biochemistry and Molecular Biology (ASBMB)",
    "Hindawi": "Hindawi",
    "BMJ Publishing Group": "BMJ Publishing",
    "IEEE: Institute of Electrical and Electronics Engineers": "IEEE: Institute of Electrical and Electronics Engineers",
    "Federation of American Societies for Experimental Biology": "Federation of American Societies for Experimental Biology",
    "PLoS": "PLoS",
    "Nature Portfolio": "Springer - Nature Publishing Group",
    "BMC (BioMed Central)": "Springer - Biomed Central (BMC)",
    "The Company of Biologists": "The Company of Biologists",
    "MDPI": "MDPI",
    "Cambridge University Press": "Cambridge University Press",
    "BioMed Central (BMC)": "BioMed Central (BMC)",
    "International Scientific Information, Inc": "International Scientific Information, Inc",
    "Taylor and Francis": "Taylor and Francis",
    "Royal Society of Chemistry (RSC)": "Royal Society of Chemistry (RSC)",
    "American Association for Cancer Research": "American Association for Cancer Research",
    "Frontiers": "Frontiers",
    "Cellular Physiology and Biochemistry Press": "Cellular Physiol Biochem Press",
    "American Medical Association": "American Medical Association",
    "American Society of Gene and Cell Therapy": "American Society of Gene & Cell Therapy",
    "Radiological Society of North America": "Radiological Society of North America",
}

# Evidence grade, assigned by hand from what each probe recorded about how it got the page.
#   verified_here — the conductor fetched the page in this session and read the quotation in it
#   source_read   — the probe returned text from the publisher's own page
#   snippet_only  — the classification rests on a search-engine snippet, the page never rendered
#   unresolved    — the check could not be completed
# machine_blocked — the load-bearing page refused an ordinary automated request at least once
GRADE = {
    "Elsevier": ("verified_here", False),
    "Oxford University Press": ("snippet_only", True),
    "Cureus (Part of Springer Nature as of December 2022)": ("source_read", True),
    "American Heart Association": ("source_read", True),
    "Royal Society Publishing": ("verified_here", False),
    "American Chemical Society (ACS)": ("source_read", True),
    "Elsevier - Cell Press": ("source_read", True),
    "American Speech-Language-Hearing Association": ("source_read", False),
    "Springer": ("verified_here", False),
    "Portland Press": ("snippet_only", True),
    "Spandidos": ("source_read", False),
    "American Association for the Advancement of Science (AAAS)": ("snippet_only", True),
    "American Society for Microbiology": ("source_read", True),
    "American Diabetes Association": ("snippet_only", True),
    "European Centre for Disease Prevention and Control": ("source_read", False),
    "Association for Computing Machinery (ACM)": ("snippet_only", True),
    "SAGE Publications": ("verified_here", False),
    "Wiley": ("source_read", False),
    "Taylor and Francis - Dove Press": ("source_read", False),
    "American Society for Biochemistry and Molecular Biology (ASBMB)": ("source_read", False),
    "Hindawi": ("source_read", True),
    "BMJ Publishing": ("source_read", False),
    "IEEE: Institute of Electrical and Electronics Engineers": ("snippet_only", True),
    "Federation of American Societies for Experimental Biology": ("source_read", False),
    "PLoS": ("verified_here", False),
    "Springer - Nature Publishing Group": ("source_read", False),
    "Springer - Biomed Central (BMC)": ("source_read", False),
    "The Company of Biologists": ("source_read", False),
    "MDPI": ("source_read", True),
    "Cambridge University Press": ("source_read", False),
    "BioMed Central (BMC)": ("source_read", False),
    "International Scientific Information, Inc": ("source_read", False),
    "Taylor and Francis": ("verified_here", True),
    "Royal Society of Chemistry (RSC)": ("source_read", False),
    "American Association for Cancer Research": ("unresolved", True),
    "Frontiers": ("source_read", False),
    "Cellular Physiol Biochem Press": ("source_read", False),
    "American Medical Association": ("source_read", True),
    "American Society of Gene & Cell Therapy": ("snippet_only", True),
    "Radiological Society of North America": ("source_read", True),
}


def load():
    pop = json.loads((DATA / "population.json").read_text())
    concerns = {r["publisher"]: r["concerns"] for r in pop["census"] + pop["tail_sample"]}
    stratum = {r["publisher"]: r["stratum"] for r in pop["census"] + pop["tail_sample"]}
    probes = []
    for f in sorted((DATA / "probes").glob("group-*.json")):
        probes += json.loads(f.read_text())
    ver = {c["publisher"]: c for c in json.loads((DATA / "verification.json").read_text())["checks"]}

    rows = []
    for p in probes:
        key = None
        for probe_label, pop_label in ALIAS.items():
            if p["publisher"].startswith(probe_label):
                if key is None or len(probe_label) > len(key[0]):
                    key = (probe_label, pop_label)
        if key is None:
            raise SystemExit("unmapped probe label: %r" % p["publisher"])
        name = key[1]
        grade, blocked = GRADE[name]
        v = ver.get(name) or ver.get(p["publisher"])
        rows.append({
            "publisher": name,
            "concerns": concerns[name],
            "stratum": stratum[name],
            "class": p["class"],
            "route_kind": p["route_kind"],
            "route_value": p["route_value"],
            "evidence_url": p["evidence_url"],
            "quote": p["quote"],
            "http_status": p["http_status"],
            "evidence_grade": grade,
            "machine_blocked": blocked,
            "verified_here": bool(v),
            "note": p.get("evidence_note", ""),
        })
    rows.sort(key=lambda r: (-r["concerns"], r["publisher"]))
    if len(rows) != 40:
        raise SystemExit("expected 40 census rows, got %d" % len(rows))
    return pop, rows


def figures(pop, rows):
    n = len(rows)
    total_concerns = sum(r["concerns"] for r in rows)
    A = [r for r in rows if r["class"] == "A"]
    B = [r for r in rows if r["class"] == "B"]
    U = [r for r in rows if r["class"] == "unresolved"]
    cw = lambda rs: sum(r["concerns"] for r in rs)

    census = [r for r in rows if r["stratum"] == "census"]
    tail = [r for r in rows if r["stratum"] == "tail"]

    # Sensitivity: every classification resting only on a search snippet is treated as unknown,
    # and every unknown is counted against class A. A floor, not an estimate.
    firm_A = [r for r in A if r["evidence_grade"] != "snippet_only"]

    return {
        "date": "2026-09-01",
        "n_publishers": n,
        "n_census": len(census),
        "n_tail": len(tail),
        "cohort_concerns_total": pop["cohort_rows"],
        "concerns_covered": total_concerns,
        "concerns_covered_pct": round(100 * total_concerns / pop["cohort_rows"], 1),
        "class_A": len(A),
        "class_B": len(B),
        "class_C": len([r for r in rows if r["class"] == "C"]),
        "class_D": len([r for r in rows if r["class"] == "D"]),
        "unresolved": len(U),
        "A_pct_of_publishers": round(100 * len(A) / n, 1),
        "A_concern_weighted_pct": round(100 * cw(A) / total_concerns, 1),
        "B_concern_weighted_pct": round(100 * cw(B) / total_concerns, 1),
        "unresolved_concern_weighted_pct": round(100 * cw(U) / total_concerns, 1),
        "A_concerns": cw(A),
        "B_concerns": cw(B),
        "census_A": len([r for r in census if r["class"] == "A"]),
        "tail_A": len([r for r in tail if r["class"] == "A"]),
        "A_floor_concern_weighted_pct": round(100 * cw(firm_A) / total_concerns, 1),
        "A_floor_publishers": len(firm_A),
        "machine_blocked": len([r for r in rows if r["machine_blocked"]]),
        "machine_blocked_pct": round(100 * len([r for r in rows if r["machine_blocked"]]) / n, 1),
        "machine_blocked_concern_weighted_pct": round(
            100 * cw([r for r in rows if r["machine_blocked"]]) / total_concerns, 1),
        "grade_verified_here": len([r for r in rows if r["evidence_grade"] == "verified_here"]),
        "grade_source_read": len([r for r in rows if r["evidence_grade"] == "source_read"]),
        "grade_snippet_only": len([r for r in rows if r["evidence_grade"] == "snippet_only"]),
        "verified_here_concern_weighted_pct": round(
            100 * cw([r for r in rows if r["verified_here"]]) / total_concerns, 1),
        "dedicated_email": len([r for r in rows if r["route_kind"] == "dedicated_email"]),
        "dedicated_form": len([r for r in rows if r["route_kind"] == "dedicated_form"]),
        "b_editor_no_address": len([r for r in B if r["route_kind"] == "editor_no_address"]),
        "b_generic_channel": len([r for r in B if r["route_kind"].startswith("generic")]),
        "largest_publisher": rows[0]["publisher"],
        "largest_publisher_class": rows[0]["class"],
        "largest_publisher_concerns": rows[0]["concerns"],
        "largest_publisher_share_pct": round(100 * rows[0]["concerns"] / pop["cohort_rows"], 1),
        "top5_concerns": sum(r["concerns"] for r in rows[:5]),
        "top5_share_pct": round(100 * sum(r["concerns"] for r in rows[:5]) / pop["cohort_rows"], 1),
        "seed": pop["seed"],
        "rows": rows,
    }


if __name__ == "__main__":
    pop, rows = load()
    fig = figures(pop, rows)
    if "--check" in sys.argv:
        have = json.loads((DATA / "data.json").read_text())
        print("data.json: %s" % ("reproduces from the probes" if have == fig
                                 else "DOES NOT reproduce"))
        sys.exit(0 if have == fig else 1)
    (DATA / "data.json").write_text(json.dumps(fig, indent=2, ensure_ascii=False) + "\n")
    with (DATA / "census.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    for k, v in fig.items():
        if k != "rows":
            print("%-42s %s" % (k, v))
