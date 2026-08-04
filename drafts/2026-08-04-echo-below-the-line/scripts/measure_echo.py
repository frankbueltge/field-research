#!/usr/bin/env python3
"""
measure_echo.py

Measures the gap between a published "echo index" rule (Rule A, reconstructed
verbatim from a public method sheet) and a near-duplicate-clustering variant
(Rule B) over the same pooled article titles.

Pure standard library. No network access. No randomness. Deterministic:
running this script twice on the same input files produces byte-identical
numeric results (only the `generated_utc` field in the output changes).

Inputs: every file matching provenance/gdelt-*.json in the working directory,
each the verbatim JSON response of a public news-search API in "artlist"
mode. No beat list is hardcoded — the script discovers whatever beat files
are present at run time and reports exactly which ones it read.

Rule definitions (kept here as literal strings so they land unmodified in
the output; edit the prose only in sync with the code below it):

RULE_A_TEXT = (
    "Pool articles (dedupe by URL). Normalise a title: lowercase, replace "
    "any non-alphanumeric run with a single space, trim; tokens = "
    "whitespace split. For every title, take all contiguous 6-token "
    "shingles. A shingle is an echo phrase if it occurs in titles from "
    ">=3 distinct domains. A title belongs to a >=3-domain echo if it "
    "contains at least one echo phrase. Echo index A = share of pooled "
    "titles belonging to a >=3-domain echo. Titles with fewer than 6 "
    "tokens produce no shingle and are counted separately."
)

RULE_B_TEXT = (
    "Same pool, same normalisation. Similarity between two normalised "
    "titles = Jaccard similarity of their token SETS (stopwords kept by "
    "default; a stopword-removed variant is also computed for comparison, "
    "using the explicit stopword list STOPWORDS defined in this file). "
    "Cluster titles by single-linkage at threshold t: two titles link if "
    "similarity >= t; clusters are the connected components of the link "
    "graph. A cluster counts if it spans >=3 distinct domains. Echo index "
    "B(t) = share of pooled titles that fall in a counting cluster. "
    "Single-linkage clustering can chain: two titles can end up in the "
    "same cluster via a path of intermediate titles even if they "
    "themselves are far below the threshold. For each t we therefore also "
    "report the number of clusters, the size of the largest cluster, and "
    "the number of distinct domains in the largest cluster, so that "
    "chaining is visible rather than hidden."
)

Judgement calls are documented inline where they are made, and repeated in
the summary output under "judgement_calls".
"""

import glob
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timezone

WORKDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROVENANCE_DIR = os.path.join(WORKDIR, "provenance")
RESULTS_DIR = os.path.join(WORKDIR, "results")

SHINGLE_N = 6
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]
MIN_ECHO_DOMAINS = 3
MAX_EXAMPLES = 12
EXAMPLE_THRESHOLDS = [0.9, 0.7]

# Explicit, small, auditable stopword list for the Rule-B stopword variant.
# This is a judgement call: it is a short list of very common English
# function words, not a standard corpus-derived list (e.g. not NLTK's),
# chosen by hand so a reader can check it in one glance.
STOPWORDS = {
    "a", "an", "the", "and", "or", "but", "of", "in", "on", "at", "to",
    "for", "with", "as", "is", "are", "was", "were", "be", "been", "being",
    "by", "from", "that", "this", "these", "those", "it", "its", "into",
    "than", "then", "so", "not", "no", "will", "would", "can", "could",
    "has", "have", "had", "do", "does", "did", "over", "after", "before",
    "up", "down", "out", "about", "against",
}

NON_ALNUM_RUN = re.compile(r"[^a-z0-9]+")

RULE_A_TEXT = (
    "Pool articles (dedupe by URL). Normalise a title: lowercase, replace "
    "any non-alphanumeric run with a single space, trim; tokens = "
    "whitespace split. For every title, take all contiguous 6-token "
    "shingles. A shingle is an echo phrase if it occurs in titles from "
    ">=3 distinct domains. A title belongs to a >=3-domain echo if it "
    "contains at least one echo phrase. Echo index A = share of pooled "
    "titles belonging to a >=3-domain echo. Titles with fewer than 6 "
    "tokens produce no shingle and are counted separately."
)

RULE_B_TEXT = (
    "Same pool, same normalisation. Similarity between two normalised "
    "titles = Jaccard similarity of their token SETS (stopwords kept by "
    "default; a stopword-removed variant is also computed for comparison, "
    "using the explicit stopword list STOPWORDS defined in this file). "
    "Cluster titles by single-linkage at threshold t: two titles link if "
    "similarity >= t; clusters are the connected components of the link "
    "graph. A cluster counts if it spans >=3 distinct domains. Echo index "
    "B(t) = share of pooled titles that fall in a counting cluster. "
    "Single-linkage clustering can chain: two titles can end up in the "
    "same cluster via a path of intermediate titles even if they "
    "themselves are far below the threshold. For each t we therefore also "
    "report the number of clusters, the size of the largest cluster, and "
    "the number of distinct domains in the largest cluster, so that "
    "chaining is visible rather than hidden."
)

JUDGEMENT_CALLS = [
    "Normalisation is lossy: lowercase + collapse any non-alphanumeric run "
    "to a single space. Numbers, hyphens, punctuation, and diacritics are "
    "all flattened; 'Bio-tech' and 'Biotech 2026' can end up sharing "
    "tokens they would not share in a stricter scheme.",
    "The 6-token shingle length for Rule A is taken verbatim from the "
    "published method sheet; it was not tuned or chosen by us.",
    "Rule B's default similarity keeps stopwords in the token set, so two "
    "titles that mostly share function words ('a', 'the', 'of') can look "
    "more similar than they are topically. A stopword-removed variant is "
    "computed alongside for comparison, using a short hand-written list "
    "(STOPWORDS in the code), not a standard corpus list.",
    "Jaccard-over-token-sets ignores word order and duplicate tokens "
    "entirely; 'X beats Y' and 'Y beats X' can score identically to "
    "'X beats X'.",
    "Single-linkage clustering chains by construction: A-B and B-C above "
    "threshold puts A and C in one cluster even if A-C similarity is 0. "
    "This is disclosed, not hidden, but it means Echo index B is an "
    "upper-bound-leaning estimate of near-duplicate coordination, not a "
    "tight one. The per-threshold largest-cluster diagnostics exist "
    "specifically so a reader can see how much chaining occurred.",
    "The >=3-distinct-domain rule is applied identically to Rule A echo "
    "phrases and Rule B clusters, as the method sheet's own bar for "
    "counting as 'echo' rather than coincidence. Any threshold is "
    "somewhat arbitrary; 3 is the published instrument's choice, not "
    "ours.",
    "Titles with fewer than SHINGLE_N=6 tokens cannot produce a Rule-A "
    "shingle at all and are excluded from Rule A's echo count by "
    "construction (not by evidence of non-echo); they are still eligible "
    "for Rule B clustering. This asymmetry is reported explicitly.",
    "Deduplication is by exact URL string match only. It does not catch "
    "tracking-parameter variants, http/https variants, or mirrored "
    "copies at different URLs; GDELT's own upstream deduplication "
    "behaviour (if any) is unknown to us and not corrected for.",
    "Threshold sweep (0.9 down to 0.5) is a fixed, pre-declared grid, not "
    "a search for the most dramatic gap; all five values are reported "
    "together, not cherry-picked.",
    "Domain is taken as GDELT's reported 'domain' field verbatim; no "
    "attempt is made to detect co-owned outlets or wire-service syndicates "
    "publishing under multiple domains, which would tend to inflate the "
    "apparent domain count of a real echo.",
    "Example pairs (Rule B catches, Rule A does not) are chosen "
    "deterministically by sorting on (similarity descending, then url pair "
    "ascending) and are illustrative, not a random or representative "
    "sample of the gap.",
]


def sha256_of_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


def normalise_title(title):
    if title is None:
        return ""
    t = title.lower()
    t = NON_ALNUM_RUN.sub(" ", t)
    return t.strip()


def tokenise(normalised_title):
    if not normalised_title:
        return []
    return normalised_title.split(" ")


def shingles(tokens, n=SHINGLE_N):
    if len(tokens) < n:
        return []
    return [tuple(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]


def jaccard(set_a, set_b):
    if not set_a and not set_b:
        return 0.0
    inter = len(set_a & set_b)
    union = len(set_a | set_b)
    if union == 0:
        return 0.0
    return inter / union


def load_pool():
    """Read every provenance/gdelt-*.json, concatenate, dedupe by url.

    Returns (pool, per_file_report, digests) where pool is a list of dicts
    each augmented with '_beat' (the source beat name derived from the
    filename) and per_file_report is a list of
    {file, beat, raw_records, sha256}.
    """
    pattern = os.path.join(PROVENANCE_DIR, "gdelt-*.json")
    files = sorted(glob.glob(pattern))
    per_file_report = []
    seen_urls = set()
    pool = []
    for path in files:
        fname = os.path.basename(path)
        # beat name = text between 'gdelt-' and '.json'
        beat = fname
        if beat.startswith("gdelt-"):
            beat = beat[len("gdelt-"):]
        if beat.endswith(".json"):
            beat = beat[:-len(".json")]
        digest = sha256_of_file(path)
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        articles = data.get("articles", []) if isinstance(data, dict) else []
        raw_count = len(articles)
        added = 0
        for art in articles:
            url = art.get("url")
            if not url:
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            rec = dict(art)
            rec["_beat"] = beat
            pool.append(rec)
            added += 1
        per_file_report.append({
            "file": fname,
            "beat": beat,
            "raw_records": raw_count,
            "added_after_dedup": added,
            "sha256": digest,
        })
    return pool, per_file_report


def build_norm_records(pool):
    """Attach normalised title, tokens, token set to each pool record."""
    recs = []
    for art in pool:
        title = art.get("title", "") or ""
        norm = normalise_title(title)
        toks = tokenise(norm)
        rec = {
            "url": art.get("url"),
            "domain": art.get("domain"),
            "title": title,
            "norm": norm,
            "tokens": toks,
            "token_set": frozenset(toks),
        }
        recs.append(rec)
    return recs


def rule_a(recs):
    """Compute Echo index A and supporting diagnostics.

    Returns a dict with: echo_index, titles_in_echo, short_titles_count,
    pool_size, shingle_domain_counts (for diagnostics), headline info.
    """
    n = len(recs)
    shingle_to_domains = {}
    short_titles = 0
    per_title_shingles = []
    for rec in recs:
        sh = shingles(rec["tokens"])
        per_title_shingles.append(sh)
        if len(rec["tokens"]) < SHINGLE_N:
            short_titles += 1
        for s in set(sh):
            shingle_to_domains.setdefault(s, set()).add(rec["domain"])

    echo_shingles = {s for s, doms in shingle_to_domains.items()
                      if len(doms) >= MIN_ECHO_DOMAINS}

    titles_in_echo = 0
    for rec, sh in zip(recs, per_title_shingles):
        if any(s in echo_shingles for s in sh):
            titles_in_echo += 1

    echo_index = (titles_in_echo / n) if n else 0.0

    headline = None
    if echo_shingles:
        best_shingle = max(
            echo_shingles,
            key=lambda s: (len(shingle_to_domains[s]), s),
        )
        headline = {
            "shingle": " ".join(best_shingle),
            "domain_count": len(shingle_to_domains[best_shingle]),
        }

    return {
        "pool_size": n,
        "titles_in_echo": titles_in_echo,
        "echo_index": echo_index,
        "short_titles_lt_6_tokens": short_titles,
        "distinct_echo_phrases": len(echo_shingles),
        "headline": headline,
    }


class DSU:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


def build_similarity_pairs(token_sets):
    """Compute pairwise Jaccard similarity for all pairs with intersection > 0.

    Uses an inverted index (token -> record indices) to avoid the full
    O(n^2) pair set when the pool is sparse in shared tokens; still
    computes an exact Jaccard for every candidate pair actually compared.
    Returns dict {(i, j): similarity} for i < j, restricted to pairs that
    share at least one token (pairs sharing zero tokens have similarity 0
    and can never meet any threshold in THRESHOLDS, so they are safely
    omitted from clustering AND from example generation).
    """
    inverted = {}
    for i, toks in enumerate(token_sets):
        for t in toks:
            inverted.setdefault(t, []).append(i)

    candidate_pairs = set()
    for t, idxs in inverted.items():
        if len(idxs) < 2:
            continue
        for a in range(len(idxs)):
            for b in range(a + 1, len(idxs)):
                i, j = idxs[a], idxs[b]
                if i > j:
                    i, j = j, i
                candidate_pairs.add((i, j))

    sims = {}
    for (i, j) in candidate_pairs:
        sims[(i, j)] = jaccard(token_sets[i], token_sets[j])
    return sims


def rule_b_for_threshold(recs, sims, t, n):
    dsu = DSU(n)
    for (i, j), s in sims.items():
        if s >= t:
            dsu.union(i, j)

    clusters = {}
    for i in range(n):
        root = dsu.find(i)
        clusters.setdefault(root, []).append(i)

    counting_cluster_members = 0
    largest_size = 0
    largest_domain_count = 0
    for root, members in clusters.items():
        doms = {recs[m]["domain"] for m in members}
        if len(members) > largest_size:
            largest_size = len(members)
            largest_domain_count = len(doms)
        if len(doms) >= MIN_ECHO_DOMAINS:
            counting_cluster_members += len(members)

    echo_index_b = (counting_cluster_members / n) if n else 0.0

    return {
        "threshold": t,
        "echo_index": echo_index_b,
        "titles_in_counting_cluster": counting_cluster_members,
        "num_clusters": len(clusters),
        "largest_cluster_size": largest_size,
        "largest_cluster_domain_count": largest_domain_count,
    }


def rule_a_covered_titles(recs):
    """Return the set of indices whose title contains an echo phrase (Rule A)."""
    shingle_to_domains = {}
    per_title_shingles = []
    for rec in recs:
        sh = shingles(rec["tokens"])
        per_title_shingles.append(sh)
        for s in set(sh):
            shingle_to_domains.setdefault(s, set()).add(rec["domain"])
    echo_shingles = {s for s, doms in shingle_to_domains.items()
                      if len(doms) >= MIN_ECHO_DOMAINS}
    covered = set()
    for idx, sh in enumerate(per_title_shingles):
        if any(s in echo_shingles for s in sh):
            covered.add(idx)
    return covered


def find_examples(recs, sims, t, a_covered_indices, n, max_examples=MAX_EXAMPLES):
    """Find up to max_examples directly-linked pairs (i, j) with sim >= t,
    different domains, where:
      - the pair's single-linkage cluster at threshold t actually COUNTS
        under Rule B (spans >=3 distinct domains) -- i.e. this pair is part
        of what makes Echo index B(t) larger than 0, not a link that gets
        thrown away by Rule B's own domain bar; and
      - at least one of i, j is NOT in a_covered_indices (i.e. that title
        does not individually belong to a Rule A echo phrase).
    This isolates pairs that are genuinely part of the A-vs-B gap, rather
    than pairs that merely look similar but would not count under either
    rule's >=3-domain condition.
    Deterministic ordering: similarity desc, then (url_i, url_j) asc.
    """
    dsu = DSU(n)
    for (i, j), s in sims.items():
        if s >= t:
            dsu.union(i, j)
    cluster_domains = {}
    for i in range(n):
        root = dsu.find(i)
        cluster_domains.setdefault(root, set()).add(recs[i]["domain"])
    counting_roots = {root for root, doms in cluster_domains.items()
                       if len(doms) >= MIN_ECHO_DOMAINS}

    candidates = []
    for (i, j), s in sims.items():
        if s < t:
            continue
        if recs[i]["domain"] == recs[j]["domain"]:
            continue
        if dsu.find(i) not in counting_roots:
            continue
        if i in a_covered_indices and j in a_covered_indices:
            continue
        candidates.append((s, i, j))

    def sort_key(item):
        s, i, j = item
        url_i = recs[i]["url"] or ""
        url_j = recs[j]["url"] or ""
        # normalise pair order for a stable, direction-independent key
        lo, hi = (url_i, url_j) if url_i <= url_j else (url_j, url_i)
        return (-s, lo, hi)

    candidates.sort(key=sort_key)

    out = []
    for s, i, j in candidates[:max_examples]:
        out.append({
            "similarity": round(s, 6),
            "title_1": recs[i]["title"],
            "domain_1": recs[i]["domain"],
            "url_1": recs[i]["url"],
            "caught_by_rule_a_1": i in a_covered_indices,
            "title_2": recs[j]["title"],
            "domain_2": recs[j]["domain"],
            "url_2": recs[j]["url"],
            "caught_by_rule_a_2": j in a_covered_indices,
        })
    return out


def main():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    pool, per_file_report = load_pool()
    n = len(pool)
    distinct_domains = len({a.get("domain") for a in pool if a.get("domain")})

    recs = build_norm_records(pool)

    a_result = rule_a(recs)
    a_covered = rule_a_covered_titles(recs)

    token_sets = [r["token_set"] for r in recs]
    sims = build_similarity_pairs(token_sets)

    # stopword-removed variant, for comparison only (documented judgement call)
    token_sets_nostop = [frozenset(t for t in r["tokens"] if t not in STOPWORDS)
                          for r in recs]
    sims_nostop = build_similarity_pairs(token_sets_nostop)

    b_results = []
    b_results_nostop = []
    for t in THRESHOLDS:
        b_results.append(rule_b_for_threshold(recs, sims, t, n))
        b_results_nostop.append(rule_b_for_threshold(recs, sims_nostop, t, n))

    gap_table = []
    for br in b_results:
        t = br["threshold"]
        gap_pp = (br["echo_index"] - a_result["echo_index"]) * 100.0
        # count of titles caught by B's counting clusters but not by A's echo phrases
        dsu = DSU(n)
        for (i, j), s in sims.items():
            if s >= t:
                dsu.union(i, j)
        clusters = {}
        for i in range(n):
            root = dsu.find(i)
            clusters.setdefault(root, []).append(i)
        b_covered = set()
        for root, members in clusters.items():
            doms = {recs[m]["domain"] for m in members}
            if len(doms) >= MIN_ECHO_DOMAINS:
                b_covered.update(members)
        caught_by_b_not_a = len(b_covered - a_covered)
        gap_table.append({
            "threshold": t,
            "echo_index_b": br["echo_index"],
            "gap_pp": gap_pp,
            "titles_caught_by_b_not_a": caught_by_b_not_a,
        })

    examples_by_threshold = {}
    for t in EXAMPLE_THRESHOLDS:
        examples_by_threshold[str(t)] = find_examples(recs, sims, t, a_covered, n)

    generated_utc = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    summary = {
        "generated_utc": generated_utc,
        "rule_definitions": {
            "rule_a": RULE_A_TEXT,
            "rule_b": RULE_B_TEXT,
        },
        "parameters": {
            "shingle_n": SHINGLE_N,
            "min_echo_domains": MIN_ECHO_DOMAINS,
            "thresholds_swept": THRESHOLDS,
            "stopwords": sorted(STOPWORDS),
        },
        "input_files": per_file_report,
        "pool": {
            "pool_size_after_url_dedup": n,
            "distinct_domains": distinct_domains,
        },
        "rule_a_result": a_result,
        "rule_b_sweep": b_results,
        "rule_b_sweep_stopwords_removed_variant": b_results_nostop,
        "gap_table_b_minus_a": gap_table,
        "judgement_calls": JUDGEMENT_CALLS,
    }

    examples_out = {
        "generated_utc": generated_utc,
        "note": (
            "Each entry is a directly-linked pair (Jaccard similarity of "
            "token sets, stopwords kept, >= the stated threshold) of "
            "titles from different domains, where (a) their single-linkage "
            "cluster at that threshold spans >=3 distinct domains -- i.e. "
            "it is a cluster that actually counts toward Echo index B, not "
            "one discarded by Rule B's own domain bar -- and (b) at least "
            "one of the two titles does not individually belong to any "
            "Rule A echo phrase. 'caught_by_rule_a_1/2' indicates whether "
            "that specific title individually belongs to a Rule A echo, "
            "so a reader can see which side of the pair (if either) Rule A "
            "already caught. Ordering is deterministic: similarity "
            "descending, then by the lexicographically smaller url in the "
            "pair."
        ),
        "examples_by_threshold": examples_by_threshold,
    }

    summary_path = os.path.join(RESULTS_DIR, "summary.json")
    examples_path = os.path.join(RESULTS_DIR, "examples.json")
    md_path = os.path.join(RESULTS_DIR, "summary.md")

    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
        f.write("\n")

    with open(examples_path, "w", encoding="utf-8") as f:
        json.dump(examples_out, f, indent=2, ensure_ascii=False)
        f.write("\n")

    md_lines = []
    md_lines.append("# Echo index: published rule vs near-duplicate rule\n")
    md_lines.append(f"Generated: {generated_utc}\n")
    md_lines.append("## Input files\n")
    md_lines.append("| beat file | beat | raw records | after url dedup | sha256 |")
    md_lines.append("|---|---|---|---|---|")
    for r in per_file_report:
        md_lines.append(
            f"| {r['file']} | {r['beat']} | {r['raw_records']} | "
            f"{r['added_after_dedup']} | `{r['sha256'][:16]}...` |"
        )
    md_lines.append("")
    md_lines.append(f"Pool size after URL dedup: **{n}**  ")
    md_lines.append(f"Distinct domains: **{distinct_domains}**\n")

    md_lines.append("## Rule A (published rule, reconstructed)\n")
    md_lines.append(f"Echo index A: **{a_result['echo_index']*100:.2f}%** "
                     f"({a_result['titles_in_echo']} / {n} titles)  ")
    md_lines.append(f"Titles with fewer than {SHINGLE_N} tokens "
                     f"(cannot produce a shingle): "
                     f"**{a_result['short_titles_lt_6_tokens']}**  ")
    md_lines.append(f"Distinct echo phrases found: "
                     f"{a_result['distinct_echo_phrases']}  ")
    if a_result["headline"]:
        md_lines.append(f"Headline (most-replicated echo phrase): "
                         f"\"{a_result['headline']['shingle']}\" "
                         f"({a_result['headline']['domain_count']} domains)\n")
    else:
        md_lines.append("No echo phrase reached the domain threshold.\n")

    md_lines.append("## Rule B sweep (near-duplicate clustering)\n")
    md_lines.append("| t | echo index B | clusters | largest cluster size | "
                     "largest cluster domains | gap vs A (pp) | "
                     "caught by B not A |")
    md_lines.append("|---|---|---|---|---|---|---|")
    for br, gt in zip(b_results, gap_table):
        md_lines.append(
            f"| {br['threshold']} | {br['echo_index']*100:.2f}% | "
            f"{br['num_clusters']} | {br['largest_cluster_size']} | "
            f"{br['largest_cluster_domain_count']} | "
            f"{gt['gap_pp']:+.2f} | {gt['titles_caught_by_b_not_a']} |"
        )
    md_lines.append("")
    md_lines.append("## Judgement calls\n")
    for jc in JUDGEMENT_CALLS:
        md_lines.append(f"- {jc}")
    md_lines.append("")

    with open(md_path, "w", encoding="utf-8") as f:
        f.write("\n".join(md_lines))

    # compact stdout summary
    print("=== measure_echo.py ===")
    print(f"generated_utc: {generated_utc}")
    print("input files:")
    for r in per_file_report:
        print(f"  {r['file']}: raw_records={r['raw_records']} "
              f"added_after_dedup={r['added_after_dedup']}")
    print(f"pool_size_after_url_dedup: {n}")
    print(f"distinct_domains: {distinct_domains}")
    print(f"short_titles_lt_6_tokens: {a_result['short_titles_lt_6_tokens']}")
    print(f"echo_index_A: {a_result['echo_index']*100:.2f}%  "
          f"({a_result['titles_in_echo']}/{n})")
    if a_result["headline"]:
        print(f"headline_phrase: \"{a_result['headline']['shingle']}\" "
              f"domains={a_result['headline']['domain_count']}")
    print("rule_B_sweep:")
    for br, gt in zip(b_results, gap_table):
        print(f"  t={br['threshold']}: echo_index_B={br['echo_index']*100:.2f}%  "
              f"gap={gt['gap_pp']:+.2f}pp  "
              f"caught_by_B_not_A={gt['titles_caught_by_b_not_a']}  "
              f"clusters={br['num_clusters']}  "
              f"largest_cluster={br['largest_cluster_size']} "
              f"(domains={br['largest_cluster_domain_count']})")
    print(f"wrote: {summary_path}")
    print(f"wrote: {examples_path}")
    print(f"wrote: {md_path}")


if __name__ == "__main__":
    main()
