#!/usr/bin/env python3
"""Apply the completeness conventions found in the census to one real catalogue.

Input: a JSON feed with an `entries` array (the house's Atlas of Data Art).
Output: the same catalogue scored under each convention the census actually
found in published measurements, so the spread attributable to the convention
alone can be read off. No model is called anywhere.
"""
import json, sys, hashlib, collections

def filled(v):
    if v is None:
        return False
    if isinstance(v, str):
        return v.strip() != ""
    if isinstance(v, (list, dict, tuple, set)):
        return len(v) > 0
    return True

def main(path, out):
    raw = open(path, "rb").read()
    feed = json.loads(raw)
    entries = feed["entries"]
    n = len(entries)

    # The schema, reconstructed as the union of keys observed across records.
    # The catalogue declares no application profile, which is itself a finding:
    # every schema-denominator convention needs a declared field list and this
    # catalogue has none, so the union of observed keys is the only stand-in.
    schema = sorted({k for e in entries for k in e.keys()})

    present_cells = sum(1 for e in entries for k in e.keys())
    filled_cells = sum(1 for e in entries for k, v in e.items() if filled(v))
    schema_cells = n * len(schema)

    per_field = {}
    for f in schema:
        have = sum(1 for e in entries if f in e and filled(e[f]))
        per_field[f] = {"records_with_value": have, "share": have / n}

    rates = sorted(v["share"] for v in per_field.values())
    mid = len(rates) // 2
    median = rates[mid] if len(rates) % 2 else (rates[mid - 1] + rates[mid]) / 2

    sparse = {f: v for f, v in per_field.items() if v["share"] < 0.05}

    result = {
        "feed": path,
        "feed_sha256": hashlib.sha256(raw).hexdigest(),
        "records": n,
        "schema_fields_observed": len(schema),
        "schema": schema,
        "conventions": {
            "A_present_key": {
                "description": "A cell counts only where the field is present on the record. The convention this practice used on 2026-09-08.",
                "numerator": filled_cells, "denominator": present_cells,
                "score": filled_cells / present_cells,
            },
            "B_schema_plain": {
                "description": "Every field in the schema is expected on every record, each counted equally. Ochoa & Duval eq. 1 as reproduced by Kiraly 2015; metadata-qa-api; Hillmann & Phipps obligation.",
                "numerator": filled_cells, "denominator": schema_cells,
                "score": filled_cells / schema_cells,
            },
            "C_per_field_over_records": {
                "description": "One rate per field, denominator the record count. Phillips, Zavalina & Tarver 2019; Tarver et al. 2015. Reported as a distribution, not one number.",
                "per_field": per_field,
                "min": rates[0], "median": median, "max": rates[-1],
            },
            "D_no_ratio": {
                "description": "Per-element occurrence counts, no denominator and no ratio at all. qa-catalogue.",
                "counts": {f: per_field[f]["records_with_value"] for f in schema},
            },
            "E_weighted_by_obligation": {
                "description": "Fields weighted by an obligation tier (mandatory/recommended/optional). Lorenzini et al. 2021; data.europa.eu MQA; F-UJI; Kiraly 2015 eq. 2.",
                "computable": False,
                "why_not": "The catalogue declares no application profile and no obligation tiers, so no weights exist to apply. The convention family cannot be run against it at all.",
            },
        },
        "sparse_fields_under_5pct": sparse,
        "gap_A_minus_B_points": (filled_cells / present_cells - filled_cells / schema_cells) * 100,
    }
    json.dump(result, open(out, "w"), indent=1)
    c = result["conventions"]
    print("records %d, schema fields observed %d" % (n, len(schema)))
    print("A present-key      %.4f %%" % (c["A_present_key"]["score"] * 100))
    print("B schema plain     %.4f %%" % (c["B_schema_plain"]["score"] * 100))
    print("C per-field  min %.4f  median %.4f  max %.4f"
          % (c["C_per_field_over_records"]["min"], c["C_per_field_over_records"]["median"],
             c["C_per_field_over_records"]["max"]))
    print("E weighted         not computable: no obligation tiers declared")
    print("gap A-B            %.2f points" % result["gap_A_minus_B_points"])
    print("sparse (<5%%):", list(sparse))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
