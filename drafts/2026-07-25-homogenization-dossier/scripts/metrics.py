"""
scripts/metrics.py — PREREGISTRATION.md §3 margin metrics + §8 marker channel, per
(stratum, half-year unit) cell. Stdlib only.

Seeded draws (§3): for a cell, `rng = random.Random("20260725:{stratum}:{unit}")` is
constructed ONCE, the cell's arXiv IDs are sorted lexicographically, and `rng.shuffle`
is applied to that sorted list EXACTLY ONCE. That single shuffled order is the cell's
one seeded order, and it is consumed by all three draw-based uses below by taking a
prefix of the appropriate size — never by re-invoking the RNG or re-shuffling:

  - MTLD:        first min(1000, n) ids of the seeded order.
  - 15,000-token pool (hapax share, Zipf-tail slope): abstracts concatenated, in the
    same seeded order (as many ids as needed to reach 15,000 tokens, or all of them).
  - Between-abstract similarity: first min(150, n) ids of the seeded order.

This is the deterministic realization of §3's "seeded and deterministic" draws.

Marker channel (§8) is not a draw-based margin metric: it is computed over the WHOLE
cell, no sampling, and is not reoriented collapse-negative here (see envelope.py's
module docstring for why: §8 states its own "excess direction" anomaly convention,
distinct from §3's collapse-negative reorientation, which applies only to the four
margin metrics).
"""
import argparse
import csv
import json
import math
import os
import random
import sys
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from stats import ols_simple  # noqa: E402
from tokenizer import tokenize  # noqa: E402

MTLD_THRESHOLD = 0.72
MTLD_DRAW = 1000
POOL_TOKENS = 15000
SIM_DRAW = 150
ZIPF_MIN_TYPES = 300
ZIPF_MAX_RANK = 1000
ZIPF_START_RANK = 101
MARKER_STYLE_COUNT = 407
SEED_DATE = "20260725"

MARGIN_METRICS = ("mtld", "hapax_share", "zipf_slope", "similarity")


# ---------------------------------------------------------------------------
# Seeded draw
# ---------------------------------------------------------------------------

def seeded_order(stratum, unit, ids):
    """The cell's one seeded order: sort ids lexicographically, shuffle once."""
    rng = random.Random(f"{SEED_DATE}:{stratum}:{unit}")
    order = sorted(ids)
    rng.shuffle(order)
    return order


# ---------------------------------------------------------------------------
# MTLD (McCarthy & Jarvis 2010), bidirectional
# ---------------------------------------------------------------------------

def _mtld_factor_pass(tokens, threshold=MTLD_THRESHOLD):
    """One directional MTLD pass. Returns MTLD for this direction, or None if the
    factor count is 0 (undefined — per §3, skip the abstract in that case)."""
    if not tokens:
        return None
    factor_count = 0
    types = set()
    seg_len = 0
    for tok in tokens:
        types.add(tok)
        seg_len += 1
        ttr = len(types) / seg_len
        if ttr <= threshold:
            factor_count += 1
            types = set()
            seg_len = 0
    if seg_len > 0:
        remaining_ttr = len(types) / seg_len
        factor_count += (1 - remaining_ttr) / (1 - threshold)
    if factor_count == 0:
        return None
    return len(tokens) / factor_count


def mtld_bidirectional(tokens, threshold=MTLD_THRESHOLD):
    """Bidirectional MTLD: mean of forward and backward passes. None if either pass
    is undefined (factor_count == 0 in that direction)."""
    forward = _mtld_factor_pass(tokens, threshold)
    backward = _mtld_factor_pass(list(reversed(tokens)), threshold)
    if forward is None or backward is None:
        return None
    return (forward + backward) / 2.0


# ---------------------------------------------------------------------------
# Hapax share + Zipf-tail slope (shared 15,000-token pool)
# ---------------------------------------------------------------------------

def build_pool(order, tokens_by_id, pool_size=POOL_TOKENS):
    """Concatenate abstracts' tokens in seeded `order` until `pool_size` tokens are
    reached. Returns (pool_tokens, short_flag) where short_flag is True if fewer than
    pool_size tokens were available across the whole cell."""
    pool = []
    for rid in order:
        if len(pool) >= pool_size:
            break
        pool.extend(tokens_by_id[rid])
    short = len(pool) < pool_size
    if not short:
        pool = pool[:pool_size]
    return pool, short


def hapax_share(pool_tokens):
    if not pool_tokens:
        return None
    freq = Counter(pool_tokens)
    total_types = len(freq)
    if total_types == 0:
        return None
    hapax_types = sum(1 for c in freq.values() if c == 1)
    return hapax_types / total_types


def _ranked_types(freq):
    """Rank a {token: count} table by descending frequency, ties broken by ascending
    alphabetical token order (determinism). Returns a list of (token, count)."""
    return sorted(freq.items(), key=lambda kv: (-kv[1], kv[0]))


def zipf_tail_slope(pool_tokens):
    """OLS slope of log10(freq) on log10(rank) over ranks 101..min(1000, max_rank).

    Ties in frequency are broken by ascending alphabetical token order (determinism).
    Returns a dict with keys: slope, types, non_computable, partial_range.
    """
    if not pool_tokens:
        return {"slope": None, "types": 0, "non_computable": True, "partial_range": False}
    freq = Counter(pool_tokens)
    ranked = _ranked_types(freq)
    types = len(ranked)
    if types < ZIPF_MIN_TYPES:
        return {"slope": None, "types": types, "non_computable": True, "partial_range": False}
    end_rank = min(ZIPF_MAX_RANK, types)
    partial_range = types < ZIPF_MAX_RANK
    xs, ys = [], []
    for rank in range(ZIPF_START_RANK, end_rank + 1):
        token, count = ranked[rank - 1]
        xs.append(math.log10(rank))
        ys.append(math.log10(count))
    if len(xs) < 2:
        return {"slope": None, "types": types, "non_computable": True, "partial_range": partial_range}
    _, slope, _, _, _ = ols_simple(xs, ys)
    return {"slope": slope, "types": types, "non_computable": False, "partial_range": partial_range}


# ---------------------------------------------------------------------------
# Between-abstract similarity (TF-IDF, cosine)
# ---------------------------------------------------------------------------

def _cosine(vec_a, vec_b):
    """Cosine similarity between two ALREADY L2-NORMALIZED sparse vectors (dicts):
    for unit vectors, cosine = dot product. Iterates over the smaller dict for speed;
    result is symmetric and exact regardless of argument order."""
    if not vec_a or not vec_b:
        return 0.0
    small, large = (vec_a, vec_b) if len(vec_a) <= len(vec_b) else (vec_b, vec_a)
    return sum(w * large.get(tok, 0.0) for tok, w in small.items())


def between_abstract_similarity(draw_ids, tokens_by_id):
    n_draw = len(draw_ids)
    small_draw = n_draw < SIM_DRAW
    if n_draw < 2:
        return {"value": None, "n_draw": n_draw, "small_draw": small_draw}

    tf_by_doc = {}
    df = Counter()
    for rid in draw_ids:
        tf = Counter(tokens_by_id[rid])
        tf_by_doc[rid] = tf
        for tok in tf:
            df[tok] += 1

    idf = {tok: math.log(n_draw / df[tok]) for tok in df}

    vectors = {}
    for rid in draw_ids:
        tf = tf_by_doc[rid]
        raw = {tok: count * idf[tok] for tok, count in tf.items()}
        norm = math.sqrt(sum(v * v for v in raw.values()))
        if norm == 0:
            vectors[rid] = {}
        else:
            vectors[rid] = {tok: v / norm for tok, v in raw.items()}

    total = 0.0
    pairs = 0
    for i in range(n_draw):
        vi = vectors[draw_ids[i]]
        for j in range(i + 1, n_draw):
            vj = vectors[draw_ids[j]]
            total += _cosine(vi, vj)
            pairs += 1

    mean_cos = total / pairs if pairs else None
    return {"value": mean_cos, "n_draw": n_draw, "small_draw": small_draw}


# ---------------------------------------------------------------------------
# Marker channel (§8)
# ---------------------------------------------------------------------------

def load_marker_set(csv_path):
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        style_words = [row["word"] for row in reader if row["type"] == "style"]
    assert len(style_words) == MARKER_STYLE_COUNT, (
        f"expected {MARKER_STYLE_COUNT} style-typed marker words, found {len(style_words)}"
    )
    return set(style_words)


def marker_rate(all_tokens, marker_set):
    total = len(all_tokens)
    if total == 0:
        return {"value": None, "total_tokens": 0, "marker_tokens": 0}
    marker_tokens = sum(1 for tok in all_tokens if tok in marker_set)
    return {
        "value": marker_tokens / total * 1000.0,
        "total_tokens": total,
        "marker_tokens": marker_tokens,
    }


# ---------------------------------------------------------------------------
# Per-cell orchestration
# ---------------------------------------------------------------------------

def compute_cell(stratum, unit, rows, marker_set):
    """rows: list of {id, created, unit, abstract} dicts for this (stratum, unit) cell."""
    ids = [r["id"] for r in rows]
    tokens_by_id = {r["id"]: tokenize(r["abstract"]) for r in rows}
    order = seeded_order(stratum, unit, ids)

    n_kept = len(rows)

    # MTLD
    mtld_ids = order[:min(MTLD_DRAW, n_kept)]
    per_abstract = []
    n_undefined = 0
    for rid in mtld_ids:
        score = mtld_bidirectional(tokens_by_id[rid])
        if score is None:
            n_undefined += 1
        else:
            per_abstract.append(score)
    mtld_value = sum(per_abstract) / len(per_abstract) if per_abstract else None
    mtld_result = {
        "value": mtld_value,
        "n_drawn": len(mtld_ids),
        "n_used": len(per_abstract),
        "n_undefined": n_undefined,
        "small_cell": n_kept < MTLD_DRAW,
    }

    # Shared 15,000-token pool
    pool, pool_short = build_pool(order, tokens_by_id, POOL_TOKENS)

    hapax_value = hapax_share(pool)
    hapax_result = {
        "value": hapax_value,
        "pool_tokens": len(pool),
        "pool_short": pool_short,
    }

    zipf_result = zipf_tail_slope(pool)
    zipf_result = {
        "value": zipf_result["slope"],
        "types": zipf_result["types"],
        "non_computable": zipf_result["non_computable"],
        "partial_range": zipf_result["partial_range"],
        "pool_short": pool_short,
    }

    # Similarity
    sim_ids = order[:min(SIM_DRAW, n_kept)]
    sim_result = between_abstract_similarity(sim_ids, tokens_by_id)

    # Marker channel: whole cell, no sampling
    all_tokens = []
    for rid in order:
        all_tokens.extend(tokens_by_id[rid])
    marker_result = marker_rate(all_tokens, marker_set)

    return {
        "unit": unit,
        "n_kept": n_kept,
        "mtld": mtld_result,
        "hapax_share": hapax_result,
        "zipf_slope": zipf_result,
        "similarity": sim_result,
        "marker_rate": marker_result,
    }


def compute_stratum(stratum, rows, marker_set):
    """rows: all kept rows for this stratum (across units). Returns list of per-unit dicts,
    sorted by unit label."""
    by_unit = {}
    for r in rows:
        by_unit.setdefault(r["unit"], []).append(r)
    units = sorted(by_unit)
    return [compute_cell(stratum, unit, by_unit[unit], marker_set) for unit in units]


# ---------------------------------------------------------------------------
# I/O / CLI
# ---------------------------------------------------------------------------

def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def default_marker_csv():
    draft_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(draft_dir, "provenance", "excess_words.csv")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Compute §3 margin metrics + §8 marker channel per cell.")
    parser.add_argument("--corpus-dir", required=True, help="Directory with per-stratum JSONL files (filter_corpus.py output).")
    parser.add_argument("--outdir", required=True, help="Directory to write per-stratum metrics JSON.")
    parser.add_argument("--marker-csv", default=None, help="Path to excess_words.csv (default: provenance/excess_words.csv).")
    parser.add_argument("--strata", nargs="+", default=["cs.CL", "cs.CV", "math.NT"], help="Strata to process.")
    args = parser.parse_args(argv)

    marker_csv = args.marker_csv or default_marker_csv()
    marker_set = load_marker_set(marker_csv)

    os.makedirs(args.outdir, exist_ok=True)

    for stratum in args.strata:
        corpus_path = os.path.join(args.corpus_dir, f"{stratum}.jsonl")
        if not os.path.exists(corpus_path):
            print(f"skip {stratum}: {corpus_path} not found", file=sys.stderr)
            continue
        rows = load_jsonl(corpus_path)
        unit_results = compute_stratum(stratum, rows, marker_set)
        out = {
            "stratum": stratum,
            "marker_csv": os.path.abspath(marker_csv),
            "marker_style_word_count": len(marker_set),
            "units": unit_results,
        }
        out_path = os.path.join(args.outdir, f"{stratum}.metrics.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(out, f, indent=2, sort_keys=True)
        print(f"wrote {out_path}")


if __name__ == "__main__":
    main()
