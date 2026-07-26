#!/usr/bin/env python3
"""Cross-check: does the D1 route's stratum rule agree with the rule the pre-registration locked?

PREREGISTRATION.md §2 defines stratum membership by the OAI record's *first listed category*.
Deviation D1 switched the harvest route, and the substitute route's filter
(`filter_corpus_api.py`) uses the Atom entry's explicit `arxiv:primary_category` attribute
instead. The deviations log asserts the substitute is at least as strong and direction-neutral.
That assertion was never measured. This script measures it.

For every entry in a set of raw Atom chunks it extracts both:
  - `first_category`   : the term of the first <category> element in document order
                         (the substitute for the locked "first listed category" rule)
  - `primary_category` : the term of <arxiv:primary_category> (the rule actually applied)
and reports the agreement rate overall and per unit, plus the disagreement pairs.

No new fetch: it reads chunks already harvested. Usage:
  python3 scripts/crosscheck_primary_category.py --raw-dir <dir> --out results/crosscheck-primary-category.json
"""

import argparse
import collections
import glob
import gzip
import json
import os
import re

ENTRY_RE = re.compile(r"<entry>(.*?)</entry>", re.DOTALL)
CATEGORY_RE = re.compile(r"<category\b[^>]*\bterm=\"([^\"]+)\"")
PRIMARY_RE = re.compile(r"<arxiv:primary_category\b[^>]*\bterm=\"([^\"]+)\"")
ID_RE = re.compile(r"<id>\s*(?:https?://arxiv\.org/abs/)?([^<\s]+)\s*</id>")


def entries(xml_text):
    """Yield (arxiv_id, first_category, primary_category) for each entry in one chunk."""
    for body in ENTRY_RE.findall(xml_text):
        primary = PRIMARY_RE.search(body)
        # The primary_category element also matches the generic category pattern in some
        # serializations, so take the FIRST plain <category ...> occurrence explicitly.
        cats = [m for m in CATEGORY_RE.finditer(body)]
        first = cats[0].group(1) if cats else None
        ident = ID_RE.search(body)
        yield (
            ident.group(1) if ident else None,
            first,
            primary.group(1) if primary else None,
        )


def crosscheck(raw_dir):
    """Walk <raw_dir>/<stratum>/<unit>/*.xml.gz and compare the two conventions."""
    per_unit = collections.OrderedDict()
    disagreements = collections.Counter()
    examples = []
    for path in sorted(glob.glob(os.path.join(raw_dir, "*", "*", "*.xml.gz"))):
        parts = path.split(os.sep)
        stratum, unit = parts[-3], parts[-2]
        key = f"{stratum}/{unit}"
        bucket = per_unit.setdefault(key, {"n": 0, "agree": 0, "missing": 0})
        with gzip.open(path, "rt", encoding="utf-8", errors="replace") as handle:
            text = handle.read()
        for ident, first, primary in entries(text):
            bucket["n"] += 1
            if first is None or primary is None:
                bucket["missing"] += 1
                continue
            if first == primary:
                bucket["agree"] += 1
            else:
                disagreements[(first, primary)] += 1
                if len(examples) < 20:
                    examples.append({"id": ident, "first_category": first, "primary_category": primary})

    total = sum(b["n"] for b in per_unit.values())
    agree = sum(b["agree"] for b in per_unit.values())
    missing = sum(b["missing"] for b in per_unit.values())
    return {
        "n_entries": total,
        "n_agree": agree,
        "n_missing_a_field": missing,
        "agreement_rate": (agree / (total - missing)) if total - missing else None,
        "per_unit": {
            k: {**v, "agreement_rate": (v["agree"] / (v["n"] - v["missing"])) if v["n"] - v["missing"] else None}
            for k, v in per_unit.items()
        },
        "disagreement_pairs": [
            {"first_category": a, "primary_category": b, "count": n}
            for (a, b), n in disagreements.most_common(25)
        ],
        "disagreement_examples": examples,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description="Stratum-rule cross-check for deviation D1.")
    parser.add_argument("--raw-dir", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args(argv)

    report = crosscheck(args.raw_dir)
    report["note"] = (
        "Measures whether the D1 substitute stratum rule (arxiv:primary_category) selects the "
        "same records as the rule locked in PREREGISTRATION.md §2 (first listed category). "
        "Computed on raw chunks already harvested; no new fetch."
    )
    with open(args.out, "w", encoding="utf-8") as handle:
        json.dump(report, handle, indent=2, sort_keys=True)
    print(json.dumps({k: v for k, v in report.items() if k != "disagreement_examples"}, indent=2, sort_keys=True)[:2500])


if __name__ == "__main__":
    main()
