"""
scripts/pools.py — the envelope-era donor pool.

PREREGISTRATION.md §9 refers to "the envelope-era pool" (as the donor source for the
synthetic-injection recipes) without defining it in the locked text; §3's top-50 frequency
mass metric similarly needs "the pool's 50 most frequent types" but that pool is the
PER-UNIT 600-token prefix, not this one. This module implements the corpus-wide
envelope-era pool per the definition fixed by the conductor at implementation time (see
DEVIATIONS-CANDIDATES.md item 2 for the exact citation and reasoning):

    The concatenation, in unit-index order, of the 600-token prefixes of every
    COMPUTABLE unit in the envelope window (units 1-47; a unit is computable iff
    n_tokens >= 600).

Determinism rule for ranking (ties broken by ascending alphabetical token order) matches
the parent instrument's `_ranked_types` exactly (`works/2026-07-25-no-signal-to-extend/
scripts/metrics.py`).
"""
import json
import os
from collections import Counter

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_SCRIPT_DIR)
UNITS_PATH = os.path.join(_DRAFT_DIR, "provenance", "units.jsonl")
OUT_PATH = os.path.join(_DRAFT_DIR, "provenance", "envelope-pool.json")

ENVELOPE_WINDOW = (1, 47)
PREFIX_LEN = 600


def load_units(path=UNITS_PATH):
    units = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                units.append(json.loads(line))
    return units


def build_envelope_pool_tokens(units):
    """Concatenate 600-token prefixes of every computable unit in units 1-47, in
    unit-index order."""
    lo, hi = ENVELOPE_WINDOW
    pool_tokens = []
    for u in units:
        if not (lo <= u["index"] <= hi):
            continue
        if u["n_tokens"] < PREFIX_LEN:
            continue
        pool_tokens.extend(u["tokens"][:PREFIX_LEN])
    return pool_tokens


def ranked_types(freq):
    """Rank a {token: count} table by descending frequency, ties broken by ascending
    alphabetical token order — same determinism rule as the parent's `_ranked_types`.
    Returns a list of (token, count)."""
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))


class EnvelopePool:
    def __init__(self, tokens):
        self.tokens = tokens
        self.freq = Counter(tokens)
        self.ranked = ranked_types(self.freq)  # list of (token, count), rank = index+1

    def top_types(self, k):
        """The k most frequent types (token, count), ties broken alphabetically."""
        return self.ranked[:k]

    def rank_slice(self, a, b):
        """Types at ranks a..b inclusive (1-indexed), same ordering as top_types."""
        return self.ranked[a - 1:b]

    def type_set(self, k):
        return {tok for tok, _count in self.top_types(k)}

    def to_table(self):
        return [
            {"token": tok, "count": count, "rank": i + 1}
            for i, (tok, count) in enumerate(self.ranked)
        ]


def load_pool(units_path=UNITS_PATH):
    units = load_units(units_path)
    tokens = build_envelope_pool_tokens(units)
    return EnvelopePool(tokens)


def main():
    pool = load_pool()
    out = {
        "envelope_window": list(ENVELOPE_WINDOW),
        "prefix_len": PREFIX_LEN,
        "pool_tokens": len(pool.tokens),
        "pool_types": len(pool.ranked),
        "table": pool.to_table(),
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False, ensure_ascii=False)
    print(f"wrote {OUT_PATH}: {len(pool.tokens)} pool tokens, {len(pool.ranked)} types")


if __name__ == "__main__":
    main()
