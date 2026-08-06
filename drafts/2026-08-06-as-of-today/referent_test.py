#!/usr/bin/env python3
"""referent_test.py — PREREGISTRATION-3, the referent test.

Every V hit recorded by the two locked runs (signals.json, session 94, EC; and
signals-2.json, session 95, GOVUK/NIST/IE) is re-extracted from a FRESH fetch of
the same URL, and classified SELF / OTHER / UNATTRIBUTABLE by the criteria fixed
in PREREGISTRATION-3.md. The locked runs themselves are not touched or amended.

Standard library only. Deterministic given the same live pages (the live web is
the one input this script does not control; a page can change between the locked
run and this one — that is exactly what the CHANGED flag records).

Outputs:
  referents.json  — one record per hit, full evidence, run timestamp, counts.
  stdout          — the summary and the R1/R2(check)/R3/R5 scoring.

Usage:
  python3 referent_test.py
"""

from __future__ import annotations

import datetime as dt
import json
import re
import sys
import time
import urllib.error
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

# The three extraction rules, reused unchanged from the session-94 collector —
# this is the one and only place they are implemented; re-importing them (not
# re-typing them) is what makes "the same three extraction rules" true rather
# than asserted.
from collect_signals import (  # noqa: E402
    DATE_RE,
    TIME_RE,
    V1_RE,
    V2_RE,
    extract_v,
    normalise_v,
)

# ---------------------------------------------------------------------------
# Fetch
# ---------------------------------------------------------------------------

UA = (
    "field-research-referent-test/1.0 "
    "(re-fetching URLs already fetched by the same public-interest measurement "
    "project, PREREGISTRATION-3.md; contact: f.bueltge@gmail.com)"
)
PAUSE_SECONDS = 1.5
TIMEOUT_SECONDS = 30


def fetch(url: str) -> dict:
    """One plain HTTPS GET. Honest recording of any non-200 or failure — never
    guessed, never substituted."""
    req = urllib.request.Request(
        url, headers={"User-Agent": UA, "Accept": "text/html,application/xhtml+xml"}
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
            status = resp.getcode()
            raw = resp.read()
            charset = resp.headers.get_content_charset() or "utf-8"
            try:
                body = raw.decode(charset, errors="replace")
            except (LookupError, TypeError):
                body = raw.decode("utf-8", errors="replace")
            if status != 200:
                return {"ok": False, "status": status, "error": f"non-200 status {status}"}
            return {"ok": True, "status": status, "body": body}
    except urllib.error.HTTPError as e:
        return {"ok": False, "status": e.code, "error": f"HTTPError {e.code}: {e.reason}"}
    except urllib.error.URLError as e:
        return {"ok": False, "status": None, "error": f"URLError: {e.reason}"}
    except Exception as e:  # noqa: BLE001 — a failed fetch must never crash the run
        return {"ok": False, "status": None, "error": f"{type(e).__name__}: {e}"}


# ---------------------------------------------------------------------------
# A minimal DOM builder — standard-library html.parser only.
#
# Builds a real element tree (tag, attrs, parent, children) AND, in lockstep,
# a flattened "visible text" character buffer whose every character carries
# a reference back to the element that owns it. This lets us find, for any
# position in the flattened text a date was matched at, the exact chain of
# enclosing elements — which is the referent evidence the lock requires.
#
# The flattening follows the same shape as collect_signals.visible_text():
# script/style content is dropped, every tag boundary becomes a single space,
# and runs of whitespace collapse to one space. It is not byte-identical to
# that function (a DOM walk and a pair of regexes are not the same machine),
# so the ACTUAL v_raw/v_rule/v_context reported for every hit always comes
# from calling extract_v() itself (imported above, unmodified) on the fetched
# page — this DOM builder is used only to locate that already-determined
# match inside the tree. Where the two disagree on where the match sits, the
# location is marked "approximate" in the evidence rather than presented as
# exact.
# ---------------------------------------------------------------------------

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

BLOCK_TAGS = {
    "address", "article", "aside", "blockquote", "details", "dialog", "dd",
    "div", "dl", "dt", "fieldset", "figcaption", "figure", "footer", "form",
    "h1", "h2", "h3", "h4", "h5", "h6", "header", "hgroup", "li", "main",
    "nav", "ol", "p", "pre", "section", "table", "tbody", "thead", "tr",
    "td", "th", "ul", "body", "html",
}

QUOTE_CHARS = "\"'“”‘’‚«»"

CARD_TOKENS = (
    "card", "teaser", "listing", "result", "related", "promo",
    "views-row", "node--teaser", "search",
)

SELF_LABELS = (
    "last update", "last updated", "updated", "last modified",
    "last reviewed", "page last reviewed", "page updated",
)


class Node:
    __slots__ = ("tag", "attrs", "parent", "children", "start_offset")

    def __init__(self, tag, attrs, parent):
        self.tag = tag
        self.attrs = attrs
        self.parent = parent
        self.children = []
        self.start_offset = None  # raw-buffer offset where this element begins


class DomBuilder(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root", {}, None)
        self.stack = [self.root]
        self.skip_depth = 0
        self.buf_chars: list[str] = []
        self.buf_owner: list[Node] = []
        self.time_nodes: list[Node] = []

    def _cur(self):
        return self.stack[-1]

    def _append_text(self, s, node):
        for ch in s:
            self.buf_chars.append(ch)
            self.buf_owner.append(node)

    def _mkattrs(self, attrs):
        d = {}
        for k, v in attrs:
            d[k.lower()] = v if v is not None else ""
        return d

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        node = Node(tag, self._mkattrs(attrs), self._cur())
        node.start_offset = len(self.buf_chars)
        self._cur().children.append(node)
        if tag == "time":
            self.time_nodes.append(node)
        if tag in ("script", "style"):
            self.skip_depth += 1
        if tag not in VOID_TAGS:
            self.stack.append(node)
        self._append_text(" ", self._cur())

    def handle_startendtag(self, tag, attrs):
        tag = tag.lower()
        node = Node(tag, self._mkattrs(attrs), self._cur())
        node.start_offset = len(self.buf_chars)
        self._cur().children.append(node)
        if tag == "time":
            self.time_nodes.append(node)
        self._append_text(" ", self._cur())

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script", "style") and self.skip_depth > 0:
            self.skip_depth -= 1
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break
        self._append_text(" ", self._cur())

    def handle_data(self, data):
        if self.skip_depth > 0:
            return
        self._append_text(data, self._cur())


def collapse_with_map(chars: list[str]):
    """Reproduce re.sub(r'\\s+', ' ', s) while keeping a map back to the
    uncollapsed buffer, so a position in the collapsed text can be traced to
    the element that owns it."""
    out = []
    idxmap = []
    i, n = 0, len(chars)
    while i < n:
        c = chars[i]
        if c.isspace():
            start = i
            while i < n and chars[i].isspace():
                i += 1
            out.append(" ")
            idxmap.append(start)
        else:
            out.append(c)
            idxmap.append(i)
            i += 1
    return "".join(out), idxmap


def raw_to_collapsed_map(idxmap, raw_len):
    r2c = [None] * raw_len
    for ci, ri in enumerate(idxmap):
        r2c[ri] = ci
    last = 0
    for ri in range(raw_len):
        if r2c[ri] is None:
            r2c[ri] = last
        else:
            last = r2c[ri]
    return r2c


def build_dom(html_source: str):
    parser = DomBuilder()
    parser.feed(html_source)
    parser.close()
    collapsed, idxmap = collapse_with_map(parser.buf_chars)
    r2c = raw_to_collapsed_map(idxmap, len(parser.buf_chars))
    return parser, collapsed, idxmap, r2c


def owner_at(parser: DomBuilder, idxmap, collapsed_pos: int):
    if not idxmap:
        return None
    collapsed_pos = max(0, min(collapsed_pos, len(idxmap) - 1))
    raw_idx = idxmap[collapsed_pos]
    return parser.buf_owner[raw_idx]


def element_chain(node: "Node | None"):
    """Self-and-ancestors, nearest first, up to (not including) the synthetic root."""
    chain = []
    n = node
    while n is not None and n.tag != "#root":
        chain.append(n)
        n = n.parent
    return chain


def subtree_has_tag(node: Node, tag: str) -> bool:
    for c in node.children:
        if isinstance(c, Node):
            if c.tag == tag:
                return True
            if subtree_has_tag(c, tag):
                return True
    return False


def subtree_text(node: Node) -> str:
    parts = []

    def walk(n: Node):
        for c in n.children:
            if isinstance(c, Node):
                if c.tag in ("script", "style"):
                    continue
                walk(c)
            else:
                parts.append(c)

    walk(node)
    return "".join(parts)


def enclosing_block(node: Node) -> "Node | None":
    n = node
    while n is not None and n.tag not in ("#root",):
        if n.tag in BLOCK_TAGS:
            return n
        n = n.parent
    return n


def is_cardish(node: Node) -> bool:
    hay = " ".join([node.attrs.get("class", ""), node.attrs.get("id", "")]).lower()
    return any(tok in hay for tok in CARD_TOKENS)


def node_brief(node: Node) -> dict:
    return {"tag": node.tag, "class": node.attrs.get("class"), "id": node.attrs.get("id")}


def find_self_label(collapsed: str, date_start: int):
    """(a): does a page-currency label from the fixed set end within 40
    characters before the date? Scanned generally against the live text —
    not proxied by which extraction rule fired — per the lock's literal
    wording. See the run report for what this implies for R2."""
    window_start = max(0, date_start - 80)
    window = collapsed[window_start:date_start]
    best = None
    for phrase in SELF_LABELS:
        for m in re.finditer(re.escape(phrase), window, re.I):
            gap = date_start - (window_start + m.end())
            if 0 <= gap <= 40:
                cand = (gap, phrase, window[m.start():m.end()])
                if best is None or cand[0] < best[0]:
                    best = cand
    if best is None:
        return False, None, None, None
    gap, phrase, matched_text = best
    return True, phrase, matched_text, gap


def locate_v1_v2(collapsed: str, rule: str):
    rx = V1_RE if rule == "V1-last-update" else V2_RE
    for m in rx.finditer(collapsed):
        d = DATE_RE.search(m.group(1))
        if d:
            date_start = m.start(1) + d.start()
            date_end = m.start(1) + d.end()
            return {
                "v_raw": d.group(1),
                "date_start": date_start,
                "date_end": date_end,
                "match_start": m.start(0),
                "match_end": m.end(0),
            }
    return None


# ---------------------------------------------------------------------------
# Classification
# ---------------------------------------------------------------------------

def classify(html_source: str, fresh_v_raw: str, fresh_v_rule: str) -> dict:
    parser, collapsed, idxmap, r2c = build_dom(html_source)

    node = None
    approximate = False
    match_context = None

    if fresh_v_rule in ("V1-last-update", "V2-published"):
        loc = locate_v1_v2(collapsed, fresh_v_rule)
        if loc is None or loc["v_raw"] != fresh_v_raw:
            approximate = True
            pos = collapsed.find(fresh_v_raw) if fresh_v_raw else -1
            if pos == -1:
                pos = 0
            loc = {"v_raw": fresh_v_raw, "date_start": pos, "date_end": pos + len(fresh_v_raw or ""),
                   "match_start": pos, "match_end": pos + len(fresh_v_raw or "")}
        node = owner_at(parser, idxmap, loc["date_start"])
        date_start_collapsed = loc["date_start"]
        match_context = collapsed[max(0, loc["match_start"] - 20):loc["match_end"] + 20]
    elif fresh_v_rule == "V3-time-element":
        cand = next((n for n in parser.time_nodes if "datetime" in n.attrs), None)
        if cand is None or cand.attrs.get("datetime") != fresh_v_raw:
            approximate = True
        node = cand
        if node is not None and node.start_offset is not None:
            date_start_collapsed = r2c[min(node.start_offset, len(r2c) - 1)] if r2c else 0
            match_context = collapsed[max(0, date_start_collapsed - 20):date_start_collapsed + 60]
        else:
            date_start_collapsed = None
    else:
        date_start_collapsed = None

    if node is None:
        return {
            "class": "UNATTRIBUTABLE",
            "class_reason": "the re-extracted date's location in the fresh page could not be recovered",
            "evidence": {"located": False, "approximate": True},
        }

    chain = element_chain(node)
    chain_brief = [node_brief(n) for n in chain]

    in_a = any(n.tag == "a" for n in chain)
    in_li = any(n.tag == "li" for n in chain)
    cardish_hits = [n for n in chain if is_cardish(n)]
    in_card = len(cardish_hits) > 0

    article_nodes = [n for n in chain if n.tag == "article"]
    main_article = None
    other_article_hits = []
    if article_nodes:
        main_article = article_nodes[-1]  # outermost article ancestor-or-self
        other_article_hits = [n for n in article_nodes if n is not main_article]

    b_holds = not (in_a or in_li or bool(other_article_hits) or in_card)

    block = enclosing_block(node)
    block_has_a = subtree_has_tag(block, "a") if block is not None else False
    block_text = subtree_text(block) if block is not None else ""
    block_has_quote = any(q in block_text for q in QUOTE_CHARS)
    c_holds = not (block_has_a or block_has_quote)

    if date_start_collapsed is not None:
        a_holds, a_phrase, a_text, a_gap = find_self_label(collapsed, date_start_collapsed)
    else:
        a_holds, a_phrase, a_text, a_gap = False, None, None, None

    date_in_link_or_card = in_a or in_card

    if a_holds and b_holds and c_holds:
        cls = "SELF"
        reason = "(a) label within 40 chars, (b) no disqualifying ancestor, (c) clean enclosing block — all hold"
    elif (not c_holds) or (not b_holds and date_in_link_or_card):
        cls = "OTHER"
        if not c_holds:
            reason = "enclosing text block links or quotes (criterion c fails)"
        else:
            reason = "date sits inside a link or card-like container (criterion b fails, and the date is inside a link/card)"
    else:
        cls = "UNATTRIBUTABLE"
        reason = "no page-currency label found within 40 chars before the date, and no link/card evidence either way"

    evidence = {
        "located": True,
        "approximate_location": approximate,
        "match_context": match_context,
        "element_chain": chain_brief,
        "in_a_ancestor": in_a,
        "in_li_ancestor": in_li,
        "in_card_like_ancestor": in_card,
        "card_like_ancestor_matches": [node_brief(n) for n in cardish_hits],
        "other_article_ancestor": bool(other_article_hits),
        "other_article_ancestor_details": [node_brief(n) for n in other_article_hits],
        "main_article_designee": node_brief(main_article) if main_article is not None else None,
        "enclosing_block_tag": block.tag if block is not None else None,
        "enclosing_block_class": block.attrs.get("class") if block is not None else None,
        "enclosing_block_id": block.attrs.get("id") if block is not None else None,
        "enclosing_block_has_a": block_has_a,
        "enclosing_block_has_quote": block_has_quote,
        "label_within_40_chars": a_holds,
        "label_phrase_matched": a_phrase,
        "label_text_as_found": a_text,
        "label_gap_chars": a_gap,
        "self_label_fixed_set": list(SELF_LABELS),
        "date_in_link_or_card": date_in_link_or_card,
        "criterion_a": a_holds,
        "criterion_b": b_holds,
        "criterion_c": c_holds,
    }

    return {"class": cls, "class_reason": reason, "evidence": evidence}


# ---------------------------------------------------------------------------
# Load the 62 hits from the two locked runs
# ---------------------------------------------------------------------------

def load_hits():
    signals_ec = json.load(open(HERE / "signals.json", encoding="utf-8"))
    signals_2 = json.load(open(HERE / "signals-2.json", encoding="utf-8"))

    total_measured_pages = len(signals_ec["rows"])
    for a in signals_2["authorities"].values():
        total_measured_pages += len(a["rows"])

    hits = []
    for row in signals_ec["rows"]:
        if row.get("v"):
            hits.append({
                "url": row["url"], "authority": "EC",
                "locked_v": row.get("v"), "locked_v_raw": row.get("v_raw"),
                "locked_v_rule": row.get("v_rule"), "locked_v_context": row.get("v_context"),
            })
    for key, a in signals_2["authorities"].items():
        for row in a["rows"]:
            if row.get("v"):
                hits.append({
                    "url": row["url"], "authority": key,
                    "locked_v": row.get("v"), "locked_v_raw": row.get("v_raw"),
                    "locked_v_rule": row.get("v_rule"), "locked_v_context": row.get("v_context"),
                })
    return hits, total_measured_pages


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> int:
    hits, total_measured_pages = load_hits()
    print(f"loaded {len(hits)} V hits from the two locked runs "
          f"(expected 62); {total_measured_pages} total measured pages across both runs")
    if len(hits) != 62:
        print(f"WARNING: expected exactly 62 V hits per the lock, found {len(hits)}. "
              "Proceeding with the true count and reporting it as found.")

    run_started = dt.datetime.now(dt.timezone.utc)
    records = []

    for i, hit in enumerate(hits):
        rec = dict(hit)
        fr = fetch(hit["url"])
        if i < len(hits) - 1:
            time.sleep(PAUSE_SECONDS)

        if not fr["ok"]:
            rec.update({
                "fetch": "FETCH-FAIL",
                "fetch_status": fr.get("status"),
                "fetch_error": fr.get("error"),
                "fresh_v": None, "fresh_v_raw": None, "fresh_v_rule": None, "fresh_v_context": None,
                "changed": None,
                "class": None, "class_reason": "fetch failed — not classified, not guessed",
                "evidence": None,
            })
            records.append(rec)
            print(f"[{i+1}/{len(hits)}] FETCH-FAIL {hit['authority']} {hit['url']} "
                  f"({fr.get('error')})")
            continue

        html_source = fr["body"]
        official = extract_v(html_source)
        fresh_v_raw = official["v_raw"]
        fresh_v_rule = official["v_rule"]
        fresh_v_context = official["v_context"]
        fresh_v = normalise_v(fresh_v_raw)

        changed = fresh_v != hit["locked_v"]

        rec.update({
            "fetch": "OK",
            "fetch_status": fr["status"],
            "fresh_v": fresh_v, "fresh_v_raw": fresh_v_raw,
            "fresh_v_rule": fresh_v_rule, "fresh_v_context": fresh_v_context,
            "changed": changed,
        })

        if fresh_v_raw is None:
            rec.update({
                "class": "UNATTRIBUTABLE",
                "class_reason": "no date re-located on the fresh fetch by any of the three rules",
                "evidence": None,
            })
        else:
            result = classify(html_source, fresh_v_raw, fresh_v_rule)
            rec.update(result)

        records.append(rec)
        flag = " CHANGED" if changed else ""
        print(f"[{i+1}/{len(hits)}] OK {hit['authority']} {hit['url']} "
              f"-> {rec['class']} ({fresh_v_rule}){flag}")

    run_finished = dt.datetime.now(dt.timezone.utc)

    # ------------------------------------------------------------------
    # Counts
    # ------------------------------------------------------------------
    n_total = len(records)
    n_fetch_fail = sum(1 for r in records if r["fetch"] == "FETCH-FAIL")
    n_ok = n_total - n_fetch_fail
    n_changed = sum(1 for r in records if r.get("changed") is True)
    usable = [r for r in records if r["fetch"] == "OK" and not r.get("changed")]

    class_counts = {"SELF": 0, "OTHER": 0, "UNATTRIBUTABLE": 0}
    for r in usable:
        class_counts[r["class"]] += 1

    by_rule = {}
    for r in usable:
        rule = r["fresh_v_rule"]
        by_rule.setdefault(rule, {"SELF": 0, "OTHER": 0, "UNATTRIBUTABLE": 0})
        by_rule[rule][r["class"]] += 1

    by_authority = {}
    for r in usable:
        auth = r["authority"]
        by_authority.setdefault(auth, {"SELF": 0, "OTHER": 0, "UNATTRIBUTABLE": 0})
        by_authority[auth][r["class"]] += 1

    counts = {
        "hits_processed": n_total,
        "fetch_fail": n_fetch_fail,
        "fetch_ok": n_ok,
        "changed": n_changed,
        "usable_for_scoring": len(usable),
        "class_totals": class_counts,
        "by_rule": by_rule,
        "by_authority": by_authority,
    }

    # ------------------------------------------------------------------
    # R1 — fewer than 60% of all V hits classify SELF. KILLED at >=60%.
    # ------------------------------------------------------------------
    base_n = len(usable)
    self_n = class_counts["SELF"]
    self_rate = (100.0 * self_n / base_n) if base_n else None
    r1_verdict = None
    if self_rate is not None:
        r1_verdict = "KILLED" if self_rate >= 60.0 else "HELD"

    # ------------------------------------------------------------------
    # R2 — no V3-time-element hit classifies SELF. Scores nothing; code check only.
    # ------------------------------------------------------------------
    v3_self = [r for r in usable if r["fresh_v_rule"] == "V3-time-element" and r["class"] == "SELF"]
    r2_check_true = len(v3_self) == 0

    # ------------------------------------------------------------------
    # R3 — at least half of the V2-published hits classify non-SELF. KILLED below 50%.
    # "the V2-published hits" is the fixed population named by the LOCKED runs'
    # own v_rule (that population exists independent of anything this script
    # does); CHANGED rows are excluded per the lock's instruction.
    # ------------------------------------------------------------------
    v2_hits = [r for r in usable if r["locked_v_rule"] == "V2-published"]
    v2_non_self = [r for r in v2_hits if r["class"] != "SELF"]
    v2_n = len(v2_hits)
    v2_non_self_rate = (100.0 * len(v2_non_self) / v2_n) if v2_n else None
    r3_verdict = None
    if v2_non_self_rate is not None:
        r3_verdict = "KILLED" if v2_non_self_rate < 50.0 else "HELD"

    # ------------------------------------------------------------------
    # R5 — fewer than 20% of the 177 measured pages carry a defensible date
    # (post-test: only SELF is defensible). KILLED at >=20%.
    # ------------------------------------------------------------------
    defensible_n = self_n  # SELF rows among the usable (fetch-OK, not-CHANGED) V hits
    defensible_rate = 100.0 * defensible_n / total_measured_pages
    r5_verdict = "KILLED" if defensible_rate >= 20.0 else "HELD"

    predictions = {
        "R1": {
            "statement": "fewer than 60% of all V hits classify SELF",
            "self_n": self_n, "base_n": base_n, "self_rate_pct": round(self_rate, 1) if self_rate is not None else None,
            "kill_threshold": ">=60%", "verdict": r1_verdict,
        },
        "R2": {
            "statement": "no V3-time-element hit classifies SELF (scores nothing; code check only)",
            "v3_self_n": len(v3_self), "check_holds": r2_check_true,
        },
        "R3": {
            "statement": "at least half of the V2-published hits classify non-SELF",
            "v2_n": v2_n, "v2_non_self_n": len(v2_non_self),
            "v2_non_self_rate_pct": round(v2_non_self_rate, 1) if v2_non_self_rate is not None else None,
            "kill_threshold": "<50%", "verdict": r3_verdict,
        },
        "R5": {
            "statement": "fewer than 20% of the 177 measured pages carry a defensible date",
            "defensible_n": defensible_n, "total_measured_pages": total_measured_pages,
            "defensible_rate_pct": round(defensible_rate, 1),
            "before_test_n": 62, "before_test_rate_pct": 35.0,
            "kill_threshold": ">=20%", "verdict": r5_verdict,
        },
    }

    out = {
        "test": "referent test (PREREGISTRATION-3.md)",
        "run_started_utc": run_started.isoformat(timespec="seconds"),
        "run_finished_utc": run_finished.isoformat(timespec="seconds"),
        "expected_hit_count": 62,
        "true_hit_count": n_total,
        "total_measured_pages": total_measured_pages,
        "counts": counts,
        "predictions": predictions,
        "records": records,
    }

    with open(HERE / "referents.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, ensure_ascii=False)
        fh.write("\n")

    # ------------------------------------------------------------------
    # Console summary
    # ------------------------------------------------------------------
    print()
    print("=== referent_test.py summary ===")
    print(f"hits processed: {n_total} (expected 62)")
    print(f"FETCH-FAIL: {n_fetch_fail}")
    print(f"fetch OK:   {n_ok}")
    print(f"CHANGED (fresh date differs from locked v_raw, excluded from scoring): {n_changed}")
    print(f"usable for scoring: {len(usable)}")
    print()
    print("class distribution (usable hits):")
    for k in ("SELF", "OTHER", "UNATTRIBUTABLE"):
        print(f"  {k:15s} {class_counts[k]}")
    print()
    print("class distribution by rule:")
    for rule, c in sorted(by_rule.items(), key=lambda kv: str(kv[0])):
        print(f"  {str(rule):20s} SELF {c['SELF']:3d}  OTHER {c['OTHER']:3d}  UNATTRIBUTABLE {c['UNATTRIBUTABLE']:3d}")
    print()
    print("class distribution by authority:")
    for auth, c in sorted(by_authority.items()):
        print(f"  {auth:10s} SELF {c['SELF']:3d}  OTHER {c['OTHER']:3d}  UNATTRIBUTABLE {c['UNATTRIBUTABLE']:3d}")
    print()
    if n_changed:
        print("CHANGED rows (reported separately, excluded from scoring):")
        for r in records:
            if r.get("changed"):
                print(f"  {r['authority']} {r['url']}  locked={r['locked_v_raw']!r} fresh={r['fresh_v_raw']!r}")
        print()

    print("=== predictions ===")
    p = predictions["R1"]
    print(f"R1: {p['statement']}")
    print(f"    SELF {p['self_n']}/{p['base_n']} = {p['self_rate_pct']}%  (killed at >=60%)  -> {p['verdict']}")
    p = predictions["R2"]
    print(f"R2 (code check only, scores nothing): {p['statement']}")
    print(f"    V3-time-element hits classified SELF: {p['v3_self_n']}  -> holds: {p['check_holds']}")
    p = predictions["R3"]
    print(f"R3: {p['statement']}")
    print(f"    non-SELF {p['v2_non_self_n']}/{p['v2_n']} = {p['v2_non_self_rate_pct']}%  (killed below 50%)  -> {p['verdict']}")
    p = predictions["R5"]
    print(f"R5: {p['statement']}")
    print(f"    defensible {p['defensible_n']}/{p['total_measured_pages']} = {p['defensible_rate_pct']}%  "
          f"(before test: 62/177 = 35.0%)  (killed at >=20%)  -> {p['verdict']}")
    print()
    print("R4 is not scored here — it requires a blind hand adjudication run separately by the conductor.")
    print()
    print(f"wrote {HERE / 'referents.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
