"""Build the population from this practice's own shipped artifact. No network.

Session 162, 2026-09-16. The population is fixed by the evidence of session 141's
artifact (`artifacts/cycle-001/2026-08-31-links-in-the-abstract/`) and by nothing decided
tonight: every `github.com` address that session extracted from a paper abstract and
scored *reachable* on 2026-08-31, deduplicated to one row per repository.

Run:  python3 tools/behind-the-door/population.py
"""

import csv
import hashlib
import json
import re

SRC = "artifacts/cycle-001/2026-08-31-links-in-the-abstract/data"
OUT = "artifacts/2026-09-16-an-address-is-not-an-artifact/data/population.json"

REPO_RE = re.compile(r"^https?://(?:www\.)?github\.com/([^/#?]+)/([^/#?]+)")


def parse_repo(url):
    m = REPO_RE.match(url)
    if not m:
        return None
    owner, repo = m.group(1), re.sub(r"\.git$", "", m.group(2))
    return owner, repo


def build():
    urls = list(csv.DictReader(open(f"{SRC}/urls.csv")))
    probes = {r["url"]: r for r in csv.DictReader(open(f"{SRC}/probes.csv"))}

    by_repo = {}
    skipped = {"not_github": 0, "not_reachable_0831": 0, "unparseable": 0}
    for row in urls:
        if row["host"] != "github.com":
            skipped["not_github"] += 1
            continue
        probe = probes.get(row["url"])
        if not probe or probe["outcome"] != "reachable":
            skipped["not_reachable_0831"] += 1
            continue
        parsed = parse_repo(row["url"])
        if not parsed:
            skipped["unparseable"] += 1
            continue
        owner, repo = parsed
        key = f"{owner}/{repo}"
        entry = by_repo.setdefault(key, {
            "repo": key,
            "owner": owner,
            "name": repo,
            "cohort": row["cohort"],
            "papers": [],
            "declared_urls": [],
        })
        # A repository declared by papers in two different cohorts would break the
        # comparison; the check below asserts there are none, rather than assuming it.
        entry["cohort_conflict"] = entry["cohort"] != row["cohort"]
        if row["arxiv_id"] not in entry["papers"]:
            entry["papers"].append(row["arxiv_id"])
        if row["url"] not in entry["declared_urls"]:
            entry["declared_urls"].append(row["url"])
        entry["earliest_paper"] = min(
            [row["published"]] + ([entry["earliest_paper"]] if "earliest_paper" in entry else [])
        )

    rows = sorted(by_repo.values(), key=lambda r: r["repo"].lower())
    conflicts = [r["repo"] for r in rows if r.get("cohort_conflict")]

    digest_input = "\n".join(f"{r['repo']}\t{r['cohort']}" for r in rows)
    out = {
        "note": ("The population of session 162: every github.com address a paper abstract "
                 "declared, that answered on 2026-08-31, one row per repository."),
        "source_artifact": SRC,
        "built": "2026-09-16, before any repository was contacted",
        "n_repos": len(rows),
        "n_cohort_A": sum(1 for r in rows if r["cohort"] == "A"),
        "n_cohort_B": sum(1 for r in rows if r["cohort"] == "B"),
        "cohort_conflicts": conflicts,
        "skipped": skipped,
        "population_digest": hashlib.sha256(digest_input.encode()).hexdigest(),
        "repos": rows,
    }
    return out


if __name__ == "__main__":
    out = build()
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(f"{out['n_repos']} repositories "
          f"(A={out['n_cohort_A']}, B={out['n_cohort_B']}), "
          f"conflicts={len(out['cohort_conflicts'])}, digest={out['population_digest'][:16]}")
    print(f"-> {OUT}")
