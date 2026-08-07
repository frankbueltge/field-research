#!/usr/bin/env python3
"""resolve_bindings.py — answer defect D6: follow a data-bound link attribute back to the
field it renders, so that the census's presentation figure stops being a 27-point bound.

WHY THIS EXISTS
---------------
`inventory.py` decides `linked` vs `displayed` from the characters immediately before an
identifier (`LINK_OPENERS`). That list contains `href={"` and `href={'` but not
`href={c.source_url}` — a bare expression with no quote after the brace, which is how every
linking work in this archive actually links. The URL sits in a JSON file behind a key; the
opener sits in a component with nothing behind it. Neither half looks like a link on its own,
and the extractor only ever sees halves. Logged as D6 in `FINDINGS-V2.md` §3.

The design is pre-registered in `PREREGISTRATION-D6.md`, committed before this file existed,
and amended in its §7 by the pre-read in `SKEPTIC-PREREAD-D6.md` — also before this file
existed. Amendment B1 is the load-bearing one and is implemented in `resolve_binding_rows`:
a `??` chain is resolved PER CONTAINER OBJECT, not per key name, because `??` short-circuits.

WHAT IT DOES NOT DO
-------------------
It computes no liveness verdict, sends no request, reads no clock into any output value, and
edits no committed result. It reads the corpus at a pinned git commit and writes one new file.

USAGE
-----
    python3 scripts/resolve_bindings.py --selftest
    python3 scripts/resolve_bindings.py                       # Arm S only
    python3 scripts/resolve_bindings.py --dist <site-dist>    # Arm S + Arm R
"""

from __future__ import annotations

import argparse
import html
import json
import re
import subprocess
import sys
from pathlib import Path

SCRIPT_PATH = Path(__file__).resolve()
DRAFT_DIR = SCRIPT_PATH.parent.parent
REPO_ROOT = SCRIPT_PATH.parents[3]

sys.path.insert(0, str(SCRIPT_PATH.parent))
from inventory import extract_identifiers, normalize, SITE_FILENAMES  # noqa: E402

# The census population, pinned. See PREREGISTRATION-D6.md §2.
PINNED_COMMIT = "712a013735cb88ecf4fa6cd713261dfc1b8a1ff3"

# S2: a plain member path. Anything else is UNRESOLVED-EXPRESSION and resolves to nothing.
MEMBER_PATH_RE = re.compile(r"^[A-Za-z_$][A-Za-z0-9_$]*(?:\.[A-Za-z_$][A-Za-z0-9_$]*)+$")

# S4: `import <name> from './<file>.json'`
IMPORT_JSON_RE = re.compile(r"""import\s+\w+\s+from\s+['"]\./([\w.\-/]+\.json)['"]""")

ATTR_RE = re.compile(r"\b(href|src)\s*=\s*\{")


# ---------------------------------------------------------------------------
# Reading the pinned corpus
# ---------------------------------------------------------------------------

def git_show(commit: str, path: str) -> str:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f"{commit}:{path}"],
        capture_output=True, check=True,
    )
    return out.stdout.decode("utf-8", errors="replace")


def git_list_works(commit: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-tree", "-r", "--name-only", commit, "works/"],
        capture_output=True, text=True, check=True,
    )
    works: set[str] = set()
    for line in out.stdout.splitlines():
        parts = line.split("/")
        if len(parts) >= 2 and parts[0] == "works":
            works.add(parts[1])
    return sorted(works)


def git_list_files(commit: str, work: str) -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-tree", "-r", "--name-only", commit, f"works/{work}/"],
        capture_output=True, text=True, check=True,
    )
    return [ln for ln in out.stdout.splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
# S1 / S2 / S3 — find the bindings the opener list misses, and read them
# ---------------------------------------------------------------------------

def balanced_brace_expr(text: str, open_idx: int) -> str | None:
    """text[open_idx] == '{'. Return the inner text of the balanced brace, or None."""
    if open_idx >= len(text) or text[open_idx] != "{":
        return None
    depth = 0
    i = open_idx
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[open_idx + 1:i]
        i += 1
    return None


def find_dynamic_bindings(text: str) -> list[dict]:
    """S1+S2+S3. Every href=/src= whose value opens `{` and is NOT immediately quoted —
    exactly the case `inventory.py`'s LINK_OPENERS misses. Returns one record per site,
    with the operand keys or an UNRESOLVED-EXPRESSION marker."""
    out: list[dict] = []
    for m in ATTR_RE.finditer(text):
        brace = text.index("{", m.end() - 1)
        nxt = text[brace + 1: brace + 2]
        if nxt in ('"', "'", "`"):
            continue                      # already caught by LINK_OPENERS
        expr = balanced_brace_expr(text, brace)
        if expr is None:
            out.append({"attr": m.group(1), "expr": None, "status": "UNBALANCED-BRACE",
                        "keys": [], "offset": m.start()})
            continue
        raw = expr.strip()
        operands = [o.strip() for o in raw.split("??")]
        if all(MEMBER_PATH_RE.match(o) for o in operands) and operands:
            out.append({"attr": m.group(1), "expr": raw, "status": "RESOLVED-EXPRESSION",
                        "keys": [o.split(".")[-1] for o in operands], "offset": m.start()})
        else:
            out.append({"attr": m.group(1), "expr": raw, "status": "UNRESOLVED-EXPRESSION",
                        "keys": [], "offset": m.start()})
    return out


def line_of(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


# ---------------------------------------------------------------------------
# S4 — resolve against the work's own imported data, PER CONTAINER OBJECT
# ---------------------------------------------------------------------------

def walk_objects(node, path: str = ""):
    """Yield (container_pattern, obj) for every dict in the tree. Array indices collapse
    to `[]` so that sibling rows share one pattern."""
    if isinstance(node, dict):
        yield (path or ".", node)
        for k, v in node.items():
            yield from walk_objects(v, f"{path}.{k}")
    elif isinstance(node, list):
        for v in node:
            yield from walk_objects(v, f"{path}[]")


def single_identifier(value) -> str | None:
    """The value is usable as a link target only if it is a string yielding exactly one
    identifier under the census's own extractor. Returns the normalised URL or None."""
    if not isinstance(value, str):
        return None
    idents = extract_identifiers(value)
    if len(idents) != 1:
        return None
    return normalize(idents[0]["cls"], idents[0]["raw"])


def resolve_binding_rows(binding_keys: list[str], data_trees: list[tuple[str, object]]) -> list[dict]:
    """AMENDMENT B1. For each container object carrying at least one operand key, mark the
    FIRST operand with a usable value on that object; later operands are marked only on
    objects where every earlier operand is absent or null. This is `??` semantics evaluated
    against the data, not assumed."""
    hits: list[dict] = []
    for filename, tree in data_trees:
        for pattern, obj in walk_objects(tree):
            if not any(k in obj for k in binding_keys):
                continue
            for idx, key in enumerate(binding_keys):
                if key not in obj:
                    continue
                url = single_identifier(obj.get(key))
                if url is None:
                    continue                      # absent/null/not-a-URL: fall through
                hits.append({
                    "file": filename,
                    "container": f"{pattern}.{key}",
                    "key": key,
                    "operand_index": idx,
                    "normalized_url": url,
                    "shadowed_by_earlier_operand": False,
                })
                break                             # `??` short-circuits here
            else:
                continue
    return hits


def shadowed_rows(binding_keys: list[str], data_trees: list[tuple[str, object]]) -> list[dict]:
    """The counterpart of B1, reported rather than hidden: values that a NAIVE per-key rule
    would have marked linked and that `??` never reaches. This is the false-linked set the
    pre-read found by hand."""
    out: list[dict] = []
    if len(binding_keys) < 2:
        return out
    for filename, tree in data_trees:
        for pattern, obj in walk_objects(tree):
            chosen = None
            for key in binding_keys:
                if key in obj and single_identifier(obj.get(key)) is not None:
                    chosen = key
                    break
            if chosen is None:
                continue
            for key in binding_keys:
                if key == chosen:
                    continue
                url = single_identifier(obj.get(key)) if key in obj else None
                if url is not None:
                    out.append({"file": filename, "container": f"{pattern}.{key}",
                                "key": key, "normalized_url": url,
                                "shadowed_by": chosen})
    return out


# ---------------------------------------------------------------------------
# Arm S
# ---------------------------------------------------------------------------

def arm_s(commit: str) -> dict:
    works = git_list_works(commit)
    per_work: dict[str, dict] = {}

    for work in works:
        files = git_list_files(commit, work)
        site_files = [f for f in files
                      if len(f.split("/")) == 3 and f.split("/")[2] in SITE_FILENAMES]
        bindings: list[dict] = []
        imports: list[str] = []
        for rel in sorted(site_files):
            text = git_show(commit, rel)
            for b in find_dynamic_bindings(text):
                b = dict(b)
                b["path"] = rel
                b["line"] = line_of(text, b.pop("offset"))
                bindings.append(b)
            if rel.endswith(".astro") or rel.endswith(".html"):
                imports.extend(IMPORT_JSON_RE.findall(text))

        data_trees: list[tuple[str, object]] = []
        for imp in sorted(set(imports)):
            rel = f"works/{work}/{imp}"
            if rel not in files:
                continue
            try:
                data_trees.append((imp, json.loads(git_show(commit, rel))))
            except json.JSONDecodeError:
                continue

        resolved: list[dict] = []
        shadowed: list[dict] = []
        for b in bindings:
            if b["status"] != "RESOLVED-EXPRESSION":
                continue
            rows = resolve_binding_rows(b["keys"], data_trees)
            for r in rows:
                r = dict(r)
                r["binding_line"] = b["line"]
                r["binding_expr"] = b["expr"]
                resolved.append(r)
            for s in shadowed_rows(b["keys"], data_trees):
                s = dict(s)
                s["binding_line"] = b["line"]
                s["binding_expr"] = b["expr"]
                shadowed.append(s)

        # B3: the container-ambiguity flag is a disclosure, not a downgrade.
        containers_by_key: dict[str, set[str]] = {}
        for r in resolved:
            containers_by_key.setdefault(r["key"], set()).add(
                r["container"].rsplit(".", 1)[0] or "."
            )
        ambiguous_keys = sorted(k for k, c in containers_by_key.items() if len(c) > 1)

        per_work[work] = {
            "bindings": bindings,
            "imports": sorted(set(imports)),
            "linked_by_binding": sorted({r["normalized_url"] for r in resolved}),
            "resolved_rows": resolved,
            "shadowed_rows": shadowed,
            "container_patterns_by_key": {k: sorted(v) for k, v in containers_by_key.items()},
            "ambiguous_keys": ambiguous_keys,
        }
    return per_work


# ---------------------------------------------------------------------------
# S5 — recompute the displayed-only set exactly as inventory.py does
# ---------------------------------------------------------------------------

def recompute(inventory: dict, per_work: dict) -> dict:
    idents = inventory["identifiers"]
    works = sorted({i["work"] for i in idents})
    linked: dict[str, set[str]] = {w: set() for w in works}
    site_urls: dict[str, set[str]] = {w: set() for w in works}
    for i in idents:
        if i["role"] != "evidence":
            continue
        if i["presentation"] == "linked":
            linked[i["work"]].add(i["normalized_url"])
        if i["tier"] == "site":
            site_urls[i["work"]].add(i["normalized_url"])

    before = [{"work": w, "normalized_url": u}
              for w in works for u in sorted(site_urls[w] - linked[w])]

    linked_after = {w: set(linked[w]) for w in works}
    for w, rec in per_work.items():
        if w in linked_after:
            linked_after[w] |= set(rec["linked_by_binding"])

    after = [{"work": w, "normalized_url": u}
             for w in works for u in sorted(site_urls[w] - linked_after[w])]

    denom = len({(w, u) for w in works for u in site_urls[w]})
    moved = [p for p in before if p not in after]
    return {
        "denominator_site_unique_work_url_pairs": denom,
        "displayed_only_before": len(before),
        "displayed_only_after": len(after),
        "share_before": round(len(before) / denom, 4) if denom else None,
        "share_after": round(len(after) / denom, 4) if denom else None,
        "pairs_reclassified": moved,
        "displayed_only_after_pairs": after,
    }


# ---------------------------------------------------------------------------
# Arm R — the render check
# ---------------------------------------------------------------------------

HREF_LITERAL_RE = re.compile(r"""<a\b[^>]*?\bhref\s*=\s*["']([^"']+)["']""", re.I | re.S)


def page_links(page: Path) -> set[str] | None:
    if not page.is_file():
        return None
    text = page.read_text(encoding="utf-8", errors="replace")
    urls: set[str] = set()
    for raw in HREF_LITERAL_RE.findall(text):
        u = single_identifier(html.unescape(raw).strip())
        if u:
            urls.add(u)
    return urls


def chrome_links(dist_dir: Path) -> list[str]:
    """AMENDMENT B6 (2026-08-07, after the first run — see RESULT-D6.md §5). The receiving
    site appends its own markup to every instrument page. A URL linked on EVERY rendered
    instrument page is that chrome, not any one work's citation, and Arm R must not credit a
    work with it. Decided by universality across the pages, not by inspecting one of them."""
    pages = sorted((dist_dir / "field" / "werke").glob("*/index.html"))
    sets = [s for s in (page_links(p) for p in pages) if s is not None]
    if not sets:
        return []
    common = set.intersection(*sets)
    return sorted(common)


def arm_r(dist_dir: Path, works: list[str]) -> dict:
    out: dict = {}
    chrome = set(chrome_links(dist_dir))
    out["_chrome_links_excluded"] = sorted(chrome)
    for work in works:
        page = dist_dir / "field" / "werke" / work / "index.html"
        urls = page_links(page)
        if urls is None:
            out[work] = {"status": "PAGE-NOT-FOUND", "linked_urls": []}
            continue
        out[work] = {"status": "READ",
                     "page_bytes": page.stat().st_size,
                     "linked_urls_before_chrome_exclusion": sorted(urls),
                     "linked_urls": sorted(urls - chrome)}
    return out


def corpus_check(dist_dir: Path, per_work: dict, inventory: dict) -> dict:
    """Arm R over the WHOLE pinned corpus, not only the binding works. For every work, the
    set of census URLs the served page actually links is compared with the set this practice
    calls linked after S5 (census `linked` + `linked-by-binding`). This is what turns the
    corpus-wide share from a claim about source into a claim about the served page."""
    chrome = set(chrome_links(dist_dir))
    linked_census: dict[str, set[str]] = {}
    site_urls: dict[str, set[str]] = {}
    for i in inventory["identifiers"]:
        if i["role"] != "evidence":
            continue
        if i["presentation"] == "linked":
            linked_census.setdefault(i["work"], set()).add(i["normalized_url"])
        if i["tier"] == "site":
            site_urls.setdefault(i["work"], set()).add(i["normalized_url"])

    out: dict = {}
    for work in sorted(site_urls):
        urls = page_links(dist_dir / "field" / "werke" / work / "index.html")
        if urls is None:
            out[work] = {"status": "PAGE-NOT-FOUND"}
            continue
        page = (urls - chrome) & site_urls[work]
        ours = (linked_census.get(work, set())
                | set(per_work.get(work, {}).get("linked_by_binding", [])))
        out[work] = {
            "status": "GRADED",
            "page_linked": len(page),
            "we_call_linked": len(ours),
            "we_say_linked_page_does_not": sorted(ours - page),
            "page_links_we_call_displayed": sorted(page - ours),
        }
    return out


def grade(per_work: dict, render: dict, inventory: dict) -> dict:
    """Arm R grades Arm S. It changes no figure of Arm S."""
    site_urls: dict[str, set[str]] = {}
    for i in inventory["identifiers"]:
        if i["role"] == "evidence" and i["tier"] == "site":
            site_urls.setdefault(i["work"], set()).add(i["normalized_url"])

    result: dict = {}
    for work, r in render.items():
        if work.startswith("_"):
            continue
        if r["status"] != "READ":
            result[work] = {"status": r["status"]}
            continue
        s_linked = set(per_work.get(work, {}).get("linked_by_binding", []))
        census = site_urls.get(work, set())
        page = set(r["linked_urls"]) & census      # chrome links are not census URLs
        result[work] = {
            "status": "GRADED",
            "agreement": sorted(s_linked & page),
            "s_over_counts": sorted(s_linked - page),
            "s_misses": sorted(page - s_linked),
        }
    return result


# ---------------------------------------------------------------------------
# Selftest
# ---------------------------------------------------------------------------

def selftest() -> int:
    n = 0

    def ok(cond, label):
        nonlocal n
        assert cond, f"SELFTEST FAILED: {label}"
        n += 1

    # brace balance
    ok(balanced_brace_expr("x={a.b}", 2) == "a.b", "simple brace")
    ok(balanced_brace_expr("x={`${a}`}", 2) == "`${a}`", "nested brace")
    ok(balanced_brace_expr("x={a.b", 2) is None, "unbalanced brace returns None")

    # S1: quoted-brace openers are already caught by inventory.py and must be skipped
    ok(find_dynamic_bindings('<a href={"http://x/"}>') == [], "quoted brace skipped")
    ok(len(find_dynamic_bindings("<a href={c.source_url}>")) == 1, "bare binding found")
    ok(find_dynamic_bindings("<a href={c.source_url}>")[0]["keys"] == ["source_url"],
       "terminal key")
    ok(find_dynamic_bindings("<img src={p.u.v}>")[0]["keys"] == ["v"], "nested member path")

    # S2: anything that is not a plain member path resolves to nothing
    for expr in ("shortUrl(c.url)", "a ? b.c : d.e", "rows[0].url", "c"):
        b = find_dynamic_bindings(f"<a href={{{expr}}}>")[0]
        ok(b["status"] == "UNRESOLVED-EXPRESSION" and b["keys"] == [],
           f"unresolved: {expr}")
    # a template literal opens with a backtick, which IS in inventory.py's LINK_OPENERS, so
    # it is that extractor's case and not this one's — skipped here rather than double-counted
    ok(find_dynamic_bindings("<a href={`${a}/b`}>") == [], "template literal left to LINK_OPENERS")

    # S3: `??` chain keeps both operand keys, in order
    b = find_dynamic_bindings("<a href={r.official_url ?? r.pdf_mirror}>")[0]
    ok(b["status"] == "RESOLVED-EXPRESSION" and b["keys"] == ["official_url", "pdf_mirror"],
       "?? chain keys in order")

    # B1: per-row `??` — the second operand is NOT linked where the first has a value
    trees = [("d.json", {"rows": [
        {"official_url": "https://a.example/one", "pdf_mirror": "https://b.example/two"},
        {"official_url": None, "pdf_mirror": "https://b.example/three"},
        {"pdf_mirror": "https://b.example/four"},
    ]})]
    rows = resolve_binding_rows(["official_url", "pdf_mirror"], trees)
    got = sorted(r["normalized_url"] for r in rows)
    ok(got == ["https://a.example/one", "https://b.example/four", "https://b.example/three"],
       f"B1 per-row ?? resolution, got {got}")
    ok("https://b.example/two" not in got, "B1 shadowed value is not linked")
    sh = shadowed_rows(["official_url", "pdf_mirror"], trees)
    ok([s["normalized_url"] for s in sh] == ["https://b.example/two"], "shadowed set reported")

    # single-operand case
    rows1 = resolve_binding_rows(["url"], [("d.json", {"a": [{"url": "https://c.example/x"}],
                                                       "b": {"url": "https://c.example/y"}})])
    ok(sorted(r["normalized_url"] for r in rows1) == ["https://c.example/x",
                                                      "https://c.example/y"],
       "single operand across two containers")
    ok(sorted({r["container"].rsplit(".", 1)[0] for r in rows1}) == [".a[]", ".b"],
       "container patterns distinguished")

    # a non-URL or absent value must not resolve
    ok(resolve_binding_rows(["url"], [("d.json", {"url": "not a url"})]) == [],
       "non-URL value resolves to nothing")
    ok(resolve_binding_rows(["url"], [("d.json", {"url": None})]) == [],
       "null value resolves to nothing")

    # Arm R link extraction
    ok(single_identifier("https://x.example/a") == normalize("U1", "https://x.example/a"),
       "Arm R normalises through the census's own normaliser")
    ok(single_identifier("doi:10.1234/abc") == "https://doi.org/10.1234/abc",
       "a DOI resolves through the census's own class handling")
    ok(HREF_LITERAL_RE.findall('<a class="k" href="https://x.example/a">t</a>')
       == ["https://x.example/a"], "Arm R href extraction")

    print(f"selftest OK — {n} assertions")
    return 0


# ---------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--commit", default=PINNED_COMMIT)
    ap.add_argument("--dist", default=None, help="built site dist/ for Arm R")
    ap.add_argument("--site-commit", default=None, help="commit of the receiving site built")
    ap.add_argument("--out", default=str(DRAFT_DIR / "results" / "bindings.json"))
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    inventory = json.loads((DRAFT_DIR / "results" / "inventory.json").read_text())
    per_work = arm_s(args.commit)
    rec = recompute(inventory, per_work)

    binding_works = sorted(w for w, r in per_work.items() if r["bindings"])
    payload = {
        "_what": "D6 — resolving a data-bound link attribute back to the field it renders",
        "_preregistration": "PREREGISTRATION-D6.md (locked before this script existed; "
                            "amended in its §7 by SKEPTIC-PREREAD-D6.md, also before it existed)",
        "_pinned_commit": args.commit,
        "_arm_s": per_work,
        "_recomputed": rec,
        "_binding_works": binding_works,
    }

    if args.dist:
        dist = Path(args.dist)
        render = arm_r(dist, binding_works)
        payload["_arm_r"] = {
            "status": "RAN",
            "site_commit": args.site_commit,
            "pages": render,
            "grade": grade(per_work, render, inventory),
            "corpus_check": corpus_check(dist, per_work, inventory),
        }
    else:
        payload["_arm_r"] = {"status": "DID-NOT-RUN",
                             "consequence": "P7 is UNSCORED and every share touched by a "
                                            "multi-operand binding is a bound (amendment B2)"}

    Path(args.out).write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {args.out}")
    print(f"displayed-only {rec['displayed_only_before']} -> {rec['displayed_only_after']} "
          f"of {rec['denominator_site_unique_work_url_pairs']} "
          f"({rec['share_before']} -> {rec['share_after']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
