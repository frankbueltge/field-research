#!/usr/bin/env python3
"""Build the run manifest: the union of corpus A and corpus B, split into named arms.

Three arms, fixed here so the run file can be split back apart without re-deriving anything:

* **A** — the 2,201 identifiers from the MediaWiki `exturlusage` index (session 109). This arm
  is what run 2 compares against run 1.
* **B** — identifiers found only in the Hacker News corpus, well-formed (19 digits). Measured
  for the first time; no predecessor to compare against.
* **B-truncated** — the 249 malformed identifiers the Hacker News extraction produced. These
  are *not* videos. Hacker News renders a long URL with its display text cut short and an
  ellipsis appended, while the `href` carries the whole URL; a naive extraction captures both
  and 248 of the 249 turn out to be strict prefixes of a well-formed identifier from the same
  comment. They are measured **as a control arm**, deliberately, so that the effect of the
  artefact on a retrievability rate is an observation rather than an argument.

A note on well-formedness. 19 digits is the shape of every identifier this platform has issued
in the period covered (corpus A: 2,197 of 2,201). The other four in corpus A are 18 digits and
date, on the identifier's own clock, to 1971 and 1975 — they are malformed too, and are marked
here rather than quietly kept.
"""
import json
import time

a = json.load(open("corpus-merged.json"))
hn = json.load(open("corpus-hn.json"))

A = a["rows"]
B = {}
for r in hn["rows"]:
    B.setdefault(r["vid"], r)

units, arms = [], {}

for vid in sorted(A):
    units.append({"vid": vid, "handle": A[vid]["handle"], "arm": "A"})

b_new = sorted(v for v in B if len(v) == 19 and v not in A)
for vid in b_new:
    units.append({"vid": vid, "handle": B[vid]["handle"], "arm": "B"})

b_trunc = sorted(v for v in B if len(v) != 19)
for vid in b_trunc:
    units.append({"vid": vid, "handle": B[vid]["handle"], "arm": "B-truncated"})

arms = {
    "A": {"n": len(A), "source": "MediaWiki exturlusage, 21 Wikipedia language editions",
          "collected": "2026-08-11 (session 109)",
          "independence": "the original source",
          "malformed_kept": sorted(v for v in A if len(v) != 19)},
    "B": {"n": len(b_new),
          "source": "Hacker News public search API, comments and stories",
          "collected": "2026-08-11 (session 110)",
          "independence": "strong — different operator, different population, no notability or "
                          "verifiability policy, no link-maintenance regime",
          "overlap_with_A": len([v for v in B if len(v) == 19 and v in A])},
    "B-truncated": {"n": len(b_trunc),
                    "source": "the same extraction, display-truncated URLs",
                    "role": "control arm — these identifiers are not videos",
                    "prefix_of_a_wellformed_id": len(
                        [v for v in b_trunc
                         if any(f.startswith(v) for f in B if len(f) == 19)])},
}

manifest = {"run_id": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "arms": arms, "n_units": len(units), "units": units}
json.dump(manifest, open("manifest-run2.json", "w"), indent=1)
print(json.dumps({"run_id": manifest["run_id"], "n_units": len(units),
                  "A": len(A), "B": len(b_new), "B-truncated": len(b_trunc)}))
