#!/usr/bin/env python3
"""
verify_echo.py — independent re-implementation, standard library only.

Does NOT import scripts/measure_echo.py. Recomputes Rule A, Rule B (sweep),
Rule C and the examples check straight from provenance/gdelt-*.json, using
only the rule text given in the verification brief (not the builder's own
prose/code comments).

No network access. Deterministic.
"""

import glob
import json
import os
import re
from urllib.parse import urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PROV_DIR = os.path.join(ROOT, "provenance")

SHINGLE_N = 6
MIN_DOMAINS = 3
THRESHOLDS = [0.9, 0.8, 0.7, 0.6, 0.5]


# ---------- loading / pooling ----------

def load_pool():
    files = sorted(glob.glob(os.path.join(PROV_DIR, "gdelt-*.json")))
    seen_urls = set()
    pool = []
    per_file = []
    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        arts = data.get("articles", []) if isinstance(data, dict) else []
        added = 0
        for a in arts:
            url = a.get("url")
            if not url:
                continue
            if url in seen_urls:
                continue
            seen_urls.add(url)
            pool.append(a)
            added += 1
        per_file.append((os.path.basename(path), len(arts), added))
    return pool, files, per_file


# ---------- normalisation (independent reading of the rule) ----------

def normalise(title):
    """lowercase, replace every run of non-alphanumeric chars with one
    space, trim. Uses Python's (unicode-aware) str.isalnum() as the
    definition of 'alphanumeric', character by character."""
    if title is None:
        return ""
    t = title.lower()
    out = []
    prev_was_sep = True  # so leading separators collapse away naturally
    for ch in t:
        if ch.isalnum():
            out.append(ch)
            prev_was_sep = False
        else:
            if not prev_was_sep:
                out.append(" ")
            prev_was_sep = True
    return "".join(out).strip()


# ASCII-only variant (mirrors the literal regex [^a-z0-9]+) — used only to
# check whether the normalisation choice actually matters on this dataset.
ASCII_NON_ALNUM = re.compile(r"[^a-z0-9]+")


def normalise_ascii(title):
    if title is None:
        return ""
    t = title.lower()
    t = ASCII_NON_ALNUM.sub(" ", t)
    return t.strip()


def tokens_of(norm):
    return norm.split(" ") if norm else []


def shingles6(tokens):
    n = len(tokens)
    if n < SHINGLE_N:
        return []
    return [tuple(tokens[i:i + SHINGLE_N]) for i in range(n - SHINGLE_N + 1)]


# ---------- union-find ----------

class DSU:
    def __init__(self, n):
        self.p = list(range(n))

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[ra] = rb


def jaccard(a, b):
    if not a and not b:
        return 0.0
    u = len(a | b)
    if u == 0:
        return 0.0
    return len(a & b) / u


def main():
    pool, files, per_file = load_pool()
    n = len(pool)
    domains = [a.get("domain") for a in pool]
    distinct_domains = len(set(d for d in domains if d))

    titles = [a.get("title", "") or "" for a in pool]
    norms = [normalise(t) for t in titles]
    norms_ascii = [normalise_ascii(t) for t in titles]
    norm_diff = sum(1 for a, b in zip(norms, norms_ascii) if a != b)

    toks = [tokens_of(x) for x in norms]
    tok_sets = [frozenset(t) for t in toks]
    short_titles = sum(1 for t in toks if len(t) < SHINGLE_N)

    print("=" * 70)
    print("POOL")
    print("=" * 70)
    for fname, raw, added in per_file:
        print(f"  {fname}: raw={raw} added_after_dedup={added}")
    print(f"provenance files matched: {len(files)}")
    print(f"pool size after url dedup: {n}")
    print(f"distinct domains: {distinct_domains}")
    print(f"titles with <{SHINGLE_N} tokens: {short_titles}")
    print(f"normalisation choice (unicode isalnum vs ascii [a-z0-9]) "
          f"differs on {norm_diff} titles")

    # ---------------- RULE A ----------------
    shingle_to_domains = {}
    per_title_shingles = []
    for i in range(n):
        sh = shingles6(toks[i])
        per_title_shingles.append(sh)
        for s in set(sh):
            shingle_to_domains.setdefault(s, set()).add(domains[i])

    echo_phrases = {s for s, doms in shingle_to_domains.items()
                     if len(doms) >= MIN_DOMAINS}

    a_covered = set()
    for i, sh in enumerate(per_title_shingles):
        if any(s in echo_phrases for s in sh):
            a_covered.add(i)

    echo_index_a = len(a_covered) / n if n else 0.0

    headline = None
    if echo_phrases:
        best = max(echo_phrases,
                    key=lambda s: (len(shingle_to_domains[s]), s))
        headline = (" ".join(best), len(shingle_to_domains[best]))

    print()
    print("=" * 70)
    print("RULE A")
    print("=" * 70)
    print(f"echo index A = {echo_index_a*100:.2f}%  "
          f"({len(a_covered)}/{n})")
    print(f"distinct echo phrases: {len(echo_phrases)}")
    if headline:
        print(f"headline phrase: \"{headline[0]}\"  domains={headline[1]}")

    # ---------------- RULE B ----------------
    # pairwise jaccard via inverted index (exact, not approximate)
    inv = {}
    for i, s in enumerate(tok_sets):
        for tok in s:
            inv.setdefault(tok, []).append(i)
    cand = set()
    for tok, idxs in inv.items():
        if len(idxs) < 2:
            continue
        for a_ in range(len(idxs)):
            for b_ in range(a_ + 1, len(idxs)):
                i, j = idxs[a_], idxs[b_]
                if i > j:
                    i, j = j, i
                cand.add((i, j))
    sims = {(i, j): jaccard(tok_sets[i], tok_sets[j]) for i, j in cand}

    print()
    print("=" * 70)
    print("RULE B sweep")
    print("=" * 70)
    hdr_anb = "A_not_B"
    hdr_bna = "B_not_A"
    print(f"{'t':>4} {'echo_B':>8} {hdr_anb:>8} {hdr_bna:>8} {'both':>5}")

    b_results = {}
    for t in THRESHOLDS:
        dsu = DSU(n)
        for (i, j), s in sims.items():
            if s >= t:
                dsu.union(i, j)
        comp_members = {}
        for i in range(n):
            r = dsu.find(i)
            comp_members.setdefault(r, []).append(i)
        b_covered = set()
        for r, members in comp_members.items():
            doms = {domains[m] for m in members}
            if len(doms) >= MIN_DOMAINS:
                b_covered.update(members)
        echo_index_b = len(b_covered) / n if n else 0.0
        a_not_b = len(a_covered - b_covered)
        b_not_a = len(b_covered - a_covered)
        both = len(a_covered & b_covered)
        b_results[t] = dict(echo_index=echo_index_b, covered=b_covered,
                             a_not_b=a_not_b, b_not_a=b_not_a, both=both,
                             comp_members=comp_members)
        print(f"{t:>4} {echo_index_b*100:7.2f}% {a_not_b:>8} {b_not_a:>8} {both:>5}")

    # ---------------- RULE C ----------------
    def url_path(u):
        if not u:
            return ""
        try:
            return urlsplit(u).path or ""
        except ValueError:
            return ""

    path_to_domains = {}
    for i in range(n):
        p = url_path(pool[i].get("url"))
        if not p:
            continue
        path_to_domains.setdefault(p, set()).add(domains[i])

    ge2 = [p for p, d in path_to_domains.items() if len(d) >= 2]
    ge3 = [p for p, d in path_to_domains.items() if len(d) >= 3]
    largest_path = max(path_to_domains.items(), key=lambda kv: (len(kv[1]), kv[0])) \
        if path_to_domains else None

    all_domains_sorted = sorted({d for d in domains if d})
    idx_of = {d: i for i, d in enumerate(all_domains_sorted)}
    dsu_d = DSU(len(all_domains_sorted))
    for p, doms in path_to_domains.items():
        if len(doms) < 2:
            continue
        doms_sorted = sorted(doms)
        for d in doms_sorted[1:]:
            dsu_d.union(idx_of[doms_sorted[0]], idx_of[d])

    root_to_group = {}
    domain_to_group = {}
    for d in all_domains_sorted:
        r = dsu_d.find(idx_of[d])
        if r not in root_to_group:
            root_to_group[r] = len(root_to_group)
        domain_to_group[d] = root_to_group[r]

    n_domains_c = len(all_domains_sorted)
    n_groups_c = len(root_to_group)

    from collections import Counter
    group_sizes = Counter(domain_to_group.values())
    group_size_hist = Counter(group_sizes.values())

    # Recompute rule A with publisher group instead of raw domain
    shingle_to_groups = {}
    for i in range(n):
        sh = per_title_shingles[i]
        grp = domain_to_group.get(domains[i], domains[i])
        for s in set(sh):
            shingle_to_groups.setdefault(s, set()).add(grp)
    echo_phrases_c = {s for s, g in shingle_to_groups.items()
                        if len(g) >= MIN_DOMAINS}
    c_covered = set()
    for i, sh in enumerate(per_title_shingles):
        if any(s in echo_phrases_c for s in sh):
            c_covered.add(i)
    echo_index_c = len(c_covered) / n if n else 0.0
    drop_pp = (echo_index_a - echo_index_c) * 100.0

    print()
    print("=" * 70)
    print("RULE C")
    print("=" * 70)
    print(f"paths with >=2 domains: {len(ge2)}")
    print(f"paths with >=3 domains: {len(ge3)}")
    if largest_path:
        print(f"largest path group: {len(largest_path[1])} domains "
              f"-> {largest_path[0]}")
    print(f"domains: {n_domains_c}  -> publisher groups: {n_groups_c}")
    print(f"publisher group size histogram: {dict(sorted(group_size_hist.items()))}")
    print(f"echo index A (domain-unit)   = {echo_index_a*100:.2f}%  "
          f"({len(a_covered)}/{n})")
    print(f"echo index A (publisher-unit)= {echo_index_c*100:.2f}%  "
          f"({len(c_covered)}/{n})")
    print(f"drop = {drop_pp:.2f} pp")
    print(f"distinct echo phrases (publisher-unit): {len(echo_phrases_c)}")

    # ---------------- EXAMPLES CHECK ----------------
    print()
    print("=" * 70)
    print("EXAMPLES CHECK (t=0.9 and t=0.7)")
    print("=" * 70)

    def qualifying_pairs(t):
        info = b_results[t]
        comp_members = info["comp_members"]
        dsu = DSU(n)
        for (i, j), s in sims.items():
            if s >= t:
                dsu.union(i, j)
        counting_roots = set()
        for r, members in comp_members.items():
            doms = {domains[m] for m in members}
            if len(doms) >= MIN_DOMAINS:
                counting_roots.add(r)
        out = []
        for (i, j), s in sims.items():
            if s < t:
                continue
            if domains[i] == domains[j]:
                continue
            if dsu.find(i) not in counting_roots:
                continue
            if (i in a_covered) and (j in a_covered):
                continue
            out.append((s, i, j))
        return out

    for t in (0.9, 0.7):
        qp = qualifying_pairs(t)
        print(f"t={t}: qualifying pairs found = {len(qp)}")

    # verify each claimed t=0.7 example against raw data + our own sims
    examples_path = os.path.join(ROOT, "results", "examples.json")
    with open(examples_path, "r", encoding="utf-8") as f:
        claimed = json.load(f)

    url_to_idx = {}
    for i in range(n):
        u = pool[i].get("url")
        if u:
            url_to_idx.setdefault(u, i)

    print()
    print("Checking each claimed t=0.7 example row against raw data:")
    t = 0.7
    info = b_results[t]
    dsu = DSU(n)
    for (i, j), s in sims.items():
        if s >= t:
            dsu.union(i, j)
    comp_members = {}
    for i in range(n):
        r = dsu.find(i)
        comp_members.setdefault(r, []).append(i)
    counting_roots = set()
    for r, members in comp_members.items():
        doms = {domains[m] for m in members}
        if len(doms) >= MIN_DOMAINS:
            counting_roots.add(r)

    ex_list = claimed["examples_by_threshold"]["0.7"]["examples"]
    claimed_count_09 = claimed["examples_by_threshold"]["0.9"]["count"]
    claimed_count_07 = claimed["examples_by_threshold"]["0.7"]["count"]
    print(f"claimed count at 0.9: {claimed_count_09}  (ours: "
          f"{len(qualifying_pairs(0.9))})")
    print(f"claimed count at 0.7: {claimed_count_07}  (ours: "
          f"{len(qualifying_pairs(0.7))})")

    all_ok = True
    for row_num, ex in enumerate(ex_list, 1):
        u1, u2 = ex["url_1"], ex["url_2"]
        ttl1, ttl2 = ex["title_1"], ex["title_2"]
        dom1, dom2 = ex["domain_1"], ex["domain_2"]
        i1 = url_to_idx.get(u1)
        i2 = url_to_idx.get(u2)
        problems = []
        if i1 is None:
            problems.append("url_1 not found in raw pool")
        if i2 is None:
            problems.append("url_2 not found in raw pool")
        if i1 is not None and pool[i1].get("title") != ttl1:
            problems.append("title_1 mismatch vs raw")
        if i2 is not None and pool[i2].get("title") != ttl2:
            problems.append("title_2 mismatch vs raw")
        if i1 is not None and pool[i1].get("domain") != dom1:
            problems.append("domain_1 mismatch vs raw")
        if i2 is not None and pool[i2].get("domain") != dom2:
            problems.append("domain_2 mismatch vs raw")
        if i1 is not None and i2 is not None:
            key = (i1, i2) if i1 < i2 else (i2, i1)
            our_sim = sims.get(key, 0.0 if key not in cand else None)
            # compute directly regardless of cand membership
            our_sim = jaccard(tok_sets[i1], tok_sets[i2])
            if round(our_sim, 6) != ex["similarity"]:
                problems.append(
                    f"similarity mismatch: claimed {ex['similarity']} "
                    f"ours {round(our_sim,6)}")
            if our_sim < t:
                problems.append(f"our similarity {our_sim} < t={t}")
            if dom1 == dom2:
                problems.append("same domain (should differ)")
            r1, r2 = dsu.find(i1), dsu.find(i2)
            if r1 != r2:
                problems.append("pair not linked at t=0.7 in our clustering")
            elif r1 not in counting_roots:
                problems.append("cluster does not span >=3 domains in our clustering")
            a1 = i1 in a_covered
            a2 = i2 in a_covered
            if ex["caught_by_rule_a_1"] != a1:
                problems.append(f"caught_by_rule_a_1 mismatch: claimed "
                                 f"{ex['caught_by_rule_a_1']} ours {a1}")
            if ex["caught_by_rule_a_2"] != a2:
                problems.append(f"caught_by_rule_a_2 mismatch: claimed "
                                 f"{ex['caught_by_rule_a_2']} ours {a2}")
            if a1 and a2:
                problems.append("BOTH sides caught by rule A (should be at least one NOT caught)")
        if problems:
            all_ok = False
            print(f"  row {row_num}: PROBLEMS: {problems}")
        else:
            print(f"  row {row_num}: OK")
    print(f"all {len(ex_list)} example rows verified clean: {all_ok}")

    # ---------------- SUMMARY.JSON CROSS-CHECK ----------------
    print()
    print("=" * 70)
    print("summary.json / summary.md cross-check")
    print("=" * 70)
    summary_path = os.path.join(ROOT, "results", "summary.json")
    with open(summary_path, "r", encoding="utf-8") as f:
        claimed_summary = json.load(f)

    checks = []
    checks.append(("pool_size_after_url_dedup",
                    claimed_summary["pool"]["pool_size_after_url_dedup"], n))
    checks.append(("distinct_domains",
                    claimed_summary["pool"]["distinct_domains"], distinct_domains))
    checks.append(("short_titles_lt_6_tokens",
                    claimed_summary["rule_a_result"]["short_titles_lt_6_tokens"],
                    short_titles))
    checks.append(("rule_a titles_in_echo",
                    claimed_summary["rule_a_result"]["titles_in_echo"],
                    len(a_covered)))
    checks.append(("rule_a distinct_echo_phrases",
                    claimed_summary["rule_a_result"]["distinct_echo_phrases"],
                    len(echo_phrases)))
    checks.append(("rule_a headline domain_count",
                    claimed_summary["rule_a_result"]["headline"]["domain_count"],
                    headline[1] if headline else None))
    for br in claimed_summary["rule_b_sweep"]:
        t = br["threshold"]
        checks.append((f"rule_b echo_index t={t}",
                        round(br["echo_index"], 6),
                        round(b_results[t]["echo_index"], 6)))
    for gt in claimed_summary["gap_table_a_vs_b"]:
        t = gt["threshold"]
        checks.append((f"gap t={t} a_not_b", gt["titles_caught_by_a_not_b"],
                        b_results[t]["a_not_b"]))
        checks.append((f"gap t={t} b_not_a", gt["titles_caught_by_b_not_a"],
                        b_results[t]["b_not_a"]))
        checks.append((f"gap t={t} both", gt["titles_caught_by_both"],
                        b_results[t]["both"]))
    rc = claimed_summary["rule_c_result"]
    checks.append(("rule_c paths_with_ge2_domains",
                    rc["path_stats"]["paths_with_ge2_domains"], len(ge2)))
    checks.append(("rule_c paths_with_ge3_domains",
                    rc["path_stats"]["paths_with_ge3_domains"], len(ge3)))
    checks.append(("rule_c distinct_domains", rc["distinct_domains"], n_domains_c))
    checks.append(("rule_c distinct_publisher_groups",
                    rc["distinct_publisher_groups_after_collapse"], n_groups_c))
    checks.append(("rule_c echo_index_a_collapsed",
                    round(rc["echo_index_a_collapsed_by_publisher"], 6),
                    round(echo_index_c, 6)))
    checks.append(("rule_c titles_in_echo_collapsed",
                    rc["titles_in_echo_collapsed"], len(c_covered)))
    checks.append(("rule_c distinct_echo_phrases_collapsed",
                    rc["distinct_echo_phrases_collapsed"], len(echo_phrases_c)))
    checks.append(("rule_c drop_pp", round(rc["drop_pp_original_minus_collapsed"], 2),
                    round(drop_pp, 2)))

    any_mismatch = False
    for name, claimed_v, ours_v in checks:
        status = "OK" if claimed_v == ours_v else "MISMATCH"
        if status == "MISMATCH":
            any_mismatch = True
        print(f"  {name}: claimed={claimed_v} ours={ours_v}  [{status}]")
    print(f"any mismatch found: {any_mismatch}")


if __name__ == "__main__":
    main()
