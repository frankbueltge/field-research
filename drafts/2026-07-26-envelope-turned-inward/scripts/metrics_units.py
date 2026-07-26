"""
scripts/metrics_units.py — PREREGISTRATION.md §3 per-unit margin metrics.

Computes, for every one of the 73 units in `provenance/units.jsonl`, every series §3
requires (prefix600 decisional, whole_unit context, prop40 sensitivity branch, and the
three between-unit similarity series: trailing-window, content-word-only, disjoint-block)
and writes `results/metrics.json`.

Reuse discipline (see PREREGISTRATION.md §0 and the task's scope note): MTLD, hapax
share, the Zipf-tail diagnostic, the marker set loader/rate, and the cosine primitive are
the parent instrument's OWN functions, imported unchanged from
`works/2026-07-25-no-signal-to-extend/scripts/metrics.py` — not reimplemented — so
agreement with the parent is structural, not just tested. Only the corpus-forced
adaptation (§3 metric 4: window-based, not draw-based, similarity) and the two metrics
with no parent analogue (top-50 frequency mass; the prop40 sensitivity branch) are
implemented here.

This module computes NO envelope, z-score, window mean, classification or verdict —
that is the next stage's scope (§4 onward), never this one's.
"""
import hashlib
import json
import math
import os
import sys
from collections import Counter

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DRAFT_DIR = os.path.dirname(_SCRIPT_DIR)
_REPO_ROOT = os.path.dirname(os.path.dirname(_DRAFT_DIR))
_PARENT_SCRIPTS = os.path.join(
    _REPO_ROOT, "works", "2026-07-25-no-signal-to-extend", "scripts"
)
sys.path.insert(0, _PARENT_SCRIPTS)
sys.path.insert(0, _SCRIPT_DIR)
from metrics import (  # noqa: E402
    mtld_bidirectional,
    hapax_share as parent_hapax_share,
    zipf_tail_slope,
    marker_rate,
    load_marker_set,
    _cosine,
)
from pools import ranked_types, load_pool  # noqa: E402

UNITS_PATH = os.path.join(_DRAFT_DIR, "provenance", "units.jsonl")
MARKER_CSV_PATH = os.path.join(_DRAFT_DIR, "provenance", "excess_words.csv")
MARKER_CSV_SHA256 = "f5786f3cc83f9578043aaecf2774c6200cb68b5e774afc3afe40af4eb0cf8285"
OUT_PATH = os.path.join(_DRAFT_DIR, "results", "metrics.json")

PREFIX_LEN = 600
PROP40_MIN_LEN = 100
MTLD_THRESHOLD = 0.72
TOP50_K = 200  # for content-word-only removal (§3(d))
SIM_WINDOW = 5


# ---------------------------------------------------------------------------
# provenance check
# ---------------------------------------------------------------------------

def verify_marker_csv(path=MARKER_CSV_PATH, expected_sha256=MARKER_CSV_SHA256):
    with open(path, "rb") as f:
        digest = hashlib.sha256(f.read()).hexdigest()
    assert digest == expected_sha256, (
        f"provenance/excess_words.csv sha256 mismatch: got {digest}, "
        f"expected {expected_sha256} (PREREGISTRATION.md §0). Refusing to run on an "
        f"unverified marker list."
    )
    return digest


# ---------------------------------------------------------------------------
# top-50 frequency mass (no parent analogue — new for this instrument)
# ---------------------------------------------------------------------------

def top50_frequency_mass(tokens):
    """Share of `tokens` accounted for by its own 50 most frequent types (ties broken
    alphabetically ascending, same rule as `pools.ranked_types` / parent's
    `_ranked_types`). If fewer than 50 types exist, uses all types and sets `partial`.
    Returns {"mass": float|None, "partial": bool|None}."""
    total = len(tokens)
    if total == 0:
        return {"mass": None, "partial": None}
    freq = Counter(tokens)
    ranked = ranked_types(freq)
    k = min(50, len(ranked))
    mass_tokens = sum(count for _tok, count in ranked[:k])
    return {"mass": mass_tokens / total, "partial": len(ranked) < 50}


# ---------------------------------------------------------------------------
# per-token-list metric set (prefix600 / whole_unit / prop40 all use this)
# ---------------------------------------------------------------------------

_NON_COMPUTABLE_METRIC_SET = {
    "mtld": None,
    "hapax_share": None,
    "top50_mass": None,
    "top50_partial": None,
    "zipf_slope": None,
    "zipf_types": None,
    "zipf_non_computable": None,
    "marker_rate_per_1000": None,
    "marker_tokens": None,
    "pool_tokens": None,
}


def compute_metric_set(tokens, marker_set):
    zipf = zipf_tail_slope(tokens)
    t50 = top50_frequency_mass(tokens)
    mk = marker_rate(tokens, marker_set)
    return {
        "mtld": mtld_bidirectional(tokens, threshold=MTLD_THRESHOLD),
        "hapax_share": parent_hapax_share(tokens),
        "top50_mass": t50["mass"],
        "top50_partial": t50["partial"],
        "zipf_slope": zipf["slope"],
        "zipf_types": zipf["types"],
        "zipf_non_computable": zipf["non_computable"],
        "marker_rate_per_1000": mk["value"],
        "marker_tokens": mk["marker_tokens"],
        "pool_tokens": len(tokens),
    }


def metric_block(computable, tokens, marker_set):
    out = {"computable": computable}
    if computable:
        out.update(compute_metric_set(tokens, marker_set))
    else:
        out.update(_NON_COMPUTABLE_METRIC_SET)
    return out


# ---------------------------------------------------------------------------
# window similarity (§3 metric 4): TF-IDF WITHIN the window, tf=raw count,
# idf=ln(n_window/df), L2-normalized, mean pairwise cosine. Generalized over window
# size n_window so the same function serves the 5-document trailing window and the
# (possibly shorter, final-block) disjoint-block realization.
# ---------------------------------------------------------------------------

def window_similarity(window_indices, docs_by_index):
    """docs_by_index: {index: token list} for every index in window_indices.

    Returns (mean_cosine, contributions, total) where `contributions` is a
    Counter mapping token -> summed contribution to the total of the pairwise
    cosines (contribution = sum over pairs of the product of the token's two
    normalized weights), and `total` is that sum (== sum of the pairwise cosines,
    == sum(contributions.values())). The per-pair cosine is computed with the
    parent instrument's OWN `_cosine`, so agreement is structural."""
    n = len(window_indices)
    tf_by_doc = {idx: Counter(docs_by_index[idx]) for idx in window_indices}
    df = Counter()
    for idx in window_indices:
        for tok in tf_by_doc[idx]:
            df[tok] += 1
    idf = {tok: math.log(n / df[tok]) for tok in df}

    vectors = {}
    for idx in window_indices:
        raw = {tok: count * idf[tok] for tok, count in tf_by_doc[idx].items()}
        norm = math.sqrt(sum(v * v for v in raw.values()))
        vectors[idx] = {} if norm == 0 else {tok: v / norm for tok, v in raw.items()}

    total = 0.0
    n_pairs = 0
    contributions = Counter()
    for i in range(n):
        for j in range(i + 1, n):
            va = vectors[window_indices[i]]
            vb = vectors[window_indices[j]]
            pair_cos = _cosine(va, vb)
            total += pair_cos
            n_pairs += 1
            small, large = (va, vb) if len(va) <= len(vb) else (vb, va)
            for tok, w in small.items():
                wl = large.get(tok)
                if wl:
                    contributions[tok] += w * wl

    mean_cos = total / n_pairs if n_pairs else None
    return mean_cos, contributions, total


def top_contributors(contributions, total, k=5):
    ranked = sorted(contributions.items(), key=lambda kv: (-kv[1], kv[0]))[:k]
    return [
        [tok, contrib, (contrib / total if total > 0 else 0.0)]
        for tok, contrib in ranked
    ]


def content_filtered(tokens, stopset):
    return [t for t in tokens if t not in stopset]


# ---------------------------------------------------------------------------
# orchestration
# ---------------------------------------------------------------------------

def load_units(path=UNITS_PATH):
    units = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                units.append(json.loads(line))
    return units


def compute_all(units, marker_set, envelope_pool):
    by_index = {u["index"]: u for u in units}
    n_units = len(units)

    prefix600_map = {}       # index -> 600-token prefix, only for computable units
    prefix600_content_map = {}  # same, with the 200 most frequent envelope-pool types removed
    stop200 = envelope_pool.type_set(TOP50_K)

    for u in units:
        if u["n_tokens"] >= PREFIX_LEN:
            prefix = u["tokens"][:PREFIX_LEN]
            prefix600_map[u["index"]] = prefix
            prefix600_content_map[u["index"]] = content_filtered(prefix, stop200)

    results = []
    for u in units:
        idx = u["index"]
        n_tokens = u["n_tokens"]

        # prefix600 (decisional)
        p600_computable = n_tokens >= PREFIX_LEN
        prefix600_block = metric_block(
            p600_computable,
            prefix600_map.get(idx),
            marker_set,
        )

        # whole_unit (context only) — always computable in this corpus (min unit
        # length is 349 tokens; see DEVIATIONS-CANDIDATES.md item 3).
        whole_unit_block = metric_block(True, u["tokens"], marker_set)

        # prop40 (non-decisional sensitivity branch)
        prop40_len = int(0.4 * n_tokens)
        prop40_computable = prop40_len >= PROP40_MIN_LEN
        prop40_block = metric_block(
            prop40_computable,
            u["tokens"][:prop40_len] if prop40_computable else None,
            marker_set,
        )

        # sim_trailing: window {x-4..x}
        if idx < SIM_WINDOW:
            window_indices = None
            sim_trailing_computable = False
        else:
            window_indices = list(range(idx - (SIM_WINDOW - 1), idx + 1))
            sim_trailing_computable = all(i in prefix600_map for i in window_indices)

        if sim_trailing_computable:
            value, contributions, total = window_similarity(
                window_indices, {i: prefix600_map[i] for i in window_indices}
            )
            sim_trailing_block = {
                "value": value,
                "computable": True,
                "window_indices": window_indices,
                "top_contributors": top_contributors(contributions, total),
            }
        else:
            sim_trailing_block = {
                "value": None,
                "computable": False,
                "window_indices": window_indices,
                "top_contributors": [],
            }

        # sim_content: identical window, content-filtered documents
        if sim_trailing_computable:
            value_c, _contrib_c, _total_c = window_similarity(
                window_indices, {i: prefix600_content_map[i] for i in window_indices}
            )
            sim_content_block = {
                "value": value_c,
                "computable": True,
                "window_indices": window_indices,
            }
        else:
            sim_content_block = {
                "value": None,
                "computable": False,
                "window_indices": window_indices,
            }

        # sim_block: disjoint 5-unit blocks (1-5, 6-10, ...), last block may be short
        block_no = (idx - 1) // SIM_WINDOW
        block_start = block_no * SIM_WINDOW + 1
        block_end = min(block_start + SIM_WINDOW - 1, n_units)
        block_indices = list(range(block_start, block_end + 1))
        block_computable = all(i in prefix600_map for i in block_indices)
        if block_computable:
            value_b, _contrib_b, _total_b = window_similarity(
                block_indices, {i: prefix600_map[i] for i in block_indices}
            )
            sim_block_block = {
                "value": value_b,
                "computable": True,
                "block_indices": block_indices,
            }
        else:
            sim_block_block = {
                "value": None,
                "computable": False,
                "block_indices": block_indices,
            }

        results.append({
            "index": idx,
            "date": u["date"],
            "heading": u["heading"],
            "n_tokens": n_tokens,
            "prefix600": prefix600_block,
            "whole_unit": whole_unit_block,
            "prop40": prop40_block,
            "sim_trailing": sim_trailing_block,
            "sim_content": sim_content_block,
            "sim_block": sim_block_block,
        })

    return results


def main():
    verify_marker_csv()
    marker_set = load_marker_set(MARKER_CSV_PATH)
    units = load_units()
    envelope_pool = load_pool()
    unit_results = compute_all(units, marker_set, envelope_pool)

    out = {
        "n_units": len(unit_results),
        "marker_csv_sha256": MARKER_CSV_SHA256,
        "marker_style_word_count": len(marker_set),
        "envelope_pool_tokens": len(envelope_pool.tokens),
        "envelope_pool_types": len(envelope_pool.ranked),
        "units": unit_results,
    }
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False, ensure_ascii=False)
    print(f"wrote {OUT_PATH}: {len(unit_results)} units")


if __name__ == "__main__":
    main()
