#!/usr/bin/env python3
"""Run the hand-over rule over a corpus and write every percentage token it found.

Session 168, 2026-09-23. Output stays outside the repository for the world corpora.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from handover import analyse                                        # noqa: E402


def main():
    src, out = sys.argv[1], sys.argv[2]
    d = json.load(open(src, encoding="utf-8"))
    toks, docs_with = [], 0
    for doc in d["docs"]:
        got = analyse(doc["text"], doc_id=doc["id"])
        if got:
            docs_with += 1
        toks.extend(got)
    counts = {"corpus": d["corpus"], "documents": len(d["docs"]),
              "documents_with_a_percentage": docs_with, "tokens": len(toks)}
    for v in ("not_recomputable", "consistent", "complement", "inconsistent"):
        counts[v] = sum(1 for t in toks if t["verdict"] == v)
    counts["recomputable"] = counts["tokens"] - counts["not_recomputable"]
    json.dump({"counts": counts, "tokens": toks}, open(out, "w", encoding="utf-8"),
              ensure_ascii=False)
    print(json.dumps(counts))


if __name__ == "__main__":
    main()
