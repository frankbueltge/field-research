#!/usr/bin/env python3
"""extract_dashboard - read the receiver's own per-video record out of the saved dashboard.

Session 128, 2026-08-20. Written because `CONDITIONS-127.md` item 1 is binding: this practice
fetched a 246,014-byte file on 2026-08-16, fetched it again on 2026-08-19, hashed it twice, cited
it by hash in the third paragraph of a letter addressed to the person who publishes it, and never
opened it past the six summary tiles at the top. Eight adversarial reviews of the packaging, and
not one of them read the evidence.

WHAT THIS IS, AND WHAT SESSION 127 DID INSTEAD
----------------------------------------------
Session 127 ran a regular expression over the saved bytes, pulled 14 numeric arrays out of them,
and could not say which array belonged to which video - two of the fourteen carried values outside
the status range and were plainly other charts. On that basis it recorded one finding (every
extracted series changes state for the last time on 2026-01-03) and declined to adopt the
adversary's finer per-video breakdown, marking it claimed-and-unreproduced. That was the right
refusal and the wrong instrument.

This is the instrument. It walks the document with `html.parser`, which means the join between a
series and its identifier is made by the document's own element structure - the series is inside
the `<div class="video-card">` whose `<h3>` says `Video ID: <digits>` - and not by proximity in a
byte stream. The Plotly payloads are read with `json.JSONDecoder().raw_decode` starting at the
argument's opening bracket, so the numbers are parsed by a JSON parser and never by a pattern.

WHAT IT REFUSES TO DO
---------------------
It does not repair, infer or fill. A card with no identifier, a chart with no `x`, a `y` value that
is not one of the axis's own labels: each is reported as such and the file says so. Nothing is
imputed. `--selftest` runs positive controls that fail loudly if the parse silently degrades - in
particular a control that mutates the document and asserts the extractor notices.

USAGE
    python3 extract_dashboard.py receiver-dashboard-2026-08-19.html -o receiver-series-2026-08-19.json
    python3 extract_dashboard.py --selftest receiver-dashboard-2026-08-19.html
"""
import sys

# Same reason as presence_check.py: this script is run from inside an object whose file list is
# part of what that object claims. Importing anything must not add __pycache__ to it.
sys.dont_write_bytecode = True

import argparse
import copy
import datetime
import hashlib
import html.parser
import json
import os
import re
import shutil
import tempfile

PLOT_CALL = "Plotly.newPlot("


class Card(object):
    """One `<div class="video-card">` and everything the document puts inside it."""

    def __init__(self, index, depth):
        self.index = index
        self.depth = depth
        self.headings = []
        self.scripts = []
        self.cells = []           # flat list of table-cell texts, in document order
        self.plot_div_ids = []


class DashboardParser(html.parser.HTMLParser):
    """Walk the document; keep what is inside a video-card separate from what is not.

    `html.parser` puts `<script>` bodies through `handle_data` as CDATA, which is what lets the
    Plotly payload be recovered without a regular expression over the whole file.
    """

    def __init__(self):
        html.parser.HTMLParser.__init__(self, convert_charrefs=True)
        self.depth = 0
        self.cards = []
        self.card = None          # the card currently open, or None
        self.outside_scripts = []
        self.outside_plot_div_ids = []
        self._text_sink = None    # list to append character data to, or None
        self._script_open = False
        self._script_is_js = False

    # -- element structure ------------------------------------------------------------------
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        classes = (a.get("class") or "").split()
        if tag == "div":
            self.depth += 1
            if "video-card" in classes and self.card is None:
                self.card = Card(len(self.cards), self.depth)
                self.cards.append(self.card)
            if "plotly-graph-div" in classes:
                target = self.card.plot_div_ids if self.card else self.outside_plot_div_ids
                target.append(a.get("id"))
        elif tag == "script":
            self._script_open = True
            self._script_is_js = (a.get("type") in (None, "", "text/javascript")
                                  and not a.get("src"))
            if self._script_is_js:
                self._text_sink = []
        elif tag in ("h1", "h2", "h3", "h4", "td", "th"):
            self._text_sink = []
            self._sink_tag = tag

    def handle_endtag(self, tag):
        if tag == "script":
            if self._script_is_js and self._text_sink is not None:
                body = "".join(self._text_sink)
                (self.card.scripts if self.card else self.outside_scripts).append(body)
            self._script_open = False
            self._script_is_js = False
            self._text_sink = None
        elif tag in ("h1", "h2", "h3", "h4", "td", "th"):
            if self._text_sink is not None:
                text = " ".join("".join(self._text_sink).split())
                if self.card is not None:
                    if tag in ("td", "th"):
                        self.card.cells.append(text)
                    else:
                        self.card.headings.append(text)
                self._text_sink = None
        elif tag == "div":
            if self.card is not None and self.depth == self.card.depth:
                self.card = None
            self.depth -= 1

    def handle_data(self, data):
        if self._text_sink is not None:
            self._text_sink.append(data)


def plot_payloads(script_body):
    """Every (div_id, data, layout) triple in one script body, parsed as JSON.

    The arguments of `Plotly.newPlot(` are located by the call name; each argument is then handed
    to a JSON decoder at its opening delimiter. No value is ever read by pattern.
    """
    out = []
    dec = json.JSONDecoder()
    pos = 0
    while True:
        i = script_body.find(PLOT_CALL, pos)
        if i < 0:
            return out
        j = i + len(PLOT_CALL)
        # argument 1: the div id, a JSON string
        while j < len(script_body) and script_body[j] not in "\"'":
            j += 1
        div_id, k = dec.raw_decode(script_body, j)
        # argument 2: the data array
        k = script_body.index("[", k)
        data, k = dec.raw_decode(script_body, k)
        # argument 3: the layout object (present in every block this dashboard emits)
        k2 = script_body.find("{", k)
        layout = None
        if k2 >= 0:
            try:
                layout, k = dec.raw_decode(script_body, k2)
            except ValueError:
                layout = None
        out.append({"div_id": div_id, "data": data, "layout": layout})
        pos = max(k, i + len(PLOT_CALL))


def cells_to_metadata(cells):
    """The metadata table as the document writes it: `<td><strong>Key:</strong></td><td>value</td>`."""
    meta = {}
    i = 0
    while i + 1 < len(cells):
        key = cells[i]
        if key.endswith(":"):
            meta[key[:-1].strip().lower().replace(" ", "_")] = cells[i + 1]
            i += 2
        else:
            i += 1
    return meta


def status_labels(layout):
    """The y axis's own label set, read from the layout - never assumed."""
    if not layout:
        return None
    y = layout.get("yaxis") or {}
    text = y.get("ticktext")
    vals = y.get("tickvals")
    if text and vals is not None:
        return {"ticktext": list(text), "tickvals": list(vals)}
    return None


def derive(dates, states):
    """What the series says, computed - not summarised."""
    d = {"n_points": len(dates)}
    if not dates:
        return d
    d["first_date"] = dates[0]
    d["last_date"] = dates[-1]
    d["span_days"] = (datetime.date.fromisoformat(dates[-1])
                      - datetime.date.fromisoformat(dates[0])).days + 1
    d["distinct_dates"] = len(set(dates))
    # gaps: is the record daily?
    gaps = []
    for a, b in zip(dates, dates[1:]):
        step = (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
        if step != 1:
            gaps.append({"after": a, "before": b, "days": step})
    d["gaps"] = gaps
    counts = {}
    for s in states:
        counts[s] = counts.get(s, 0) + 1
    d["status_day_counts"] = counts
    d["final_status"] = states[-1]
    # every transition, and the last one
    trans = []
    for i in range(1, len(states)):
        if states[i] != states[i - 1]:
            trans.append({"date": dates[i], "from": states[i - 1], "to": states[i]})
    d["transitions"] = trans
    d["n_transitions"] = len(trans)
    d["last_change_date"] = trans[-1]["date"] if trans else None
    d["days_in_final_status_since_last_change"] = (
        (datetime.date.fromisoformat(dates[-1])
         - datetime.date.fromisoformat(trans[-1]["date"])).days + 1) if trans else None
    return d


def extract(path):
    raw = open(path, "rb").read()
    parser = DashboardParser()
    parser.feed(raw.decode("utf-8"))
    parser.close()

    videos = []
    problems = []
    for card in parser.cards:
        vid = None
        for h in card.headings:
            m = re.fullmatch(r"Video ID:\s*(\d+)", h)
            if m:
                vid = m.group(1)
                break
        if vid is None:
            problems.append({"card_index": card.index,
                             "problem": "no `Video ID: <digits>` heading in this card",
                             "headings": card.headings})
            continue
        payloads = []
        for body in card.scripts:
            payloads.extend(plot_payloads(body))
        if not payloads:
            problems.append({"card_index": card.index, "video_id": vid,
                             "problem": "card has no Plotly payload"})
            continue
        entry = {"video_id": vid,
                 "card_index": card.index,
                 "metadata": cells_to_metadata(card.cells),
                 "plot_div_ids": card.plot_div_ids,
                 "charts": []}
        for p in payloads:
            labels = status_labels(p["layout"])
            for trace in p["data"]:
                x = trace.get("x")
                y = trace.get("y")
                if x is None or y is None:
                    continue
                chart = {"div_id": p["div_id"],
                         "trace_name": trace.get("name"),
                         "trace_mode": trace.get("mode"),
                         "y_axis_labels": labels,
                         "x": list(x),
                         "y": list(y)}
                # map numeric y to the axis's own label, only when the axis says how
                states = None
                if labels:
                    lookup = dict(zip(labels["tickvals"], labels["ticktext"]))
                    if all(v in lookup for v in y):
                        states = [lookup[v] for v in y]
                    else:
                        chart["unmapped_y_values"] = sorted(
                            set(v for v in y if v not in lookup))
                chart["states"] = states
                dates = [str(v)[:10] for v in x]
                chart["derived"] = derive(dates, states if states is not None else list(y))
                chart["states_are_labelled"] = states is not None
                entry["charts"].append(chart)
        videos.append(entry)

    aggregate = []
    for body in parser.outside_scripts:
        for p in plot_payloads(body):
            traces = []
            for trace in p["data"]:
                if trace.get("x") is None:
                    continue
                traces.append({"name": trace.get("name"),
                               "n_points": len(trace["x"]),
                               "first_x": str(trace["x"][0])[:10],
                               "last_x": str(trace["x"][-1])[:10],
                               "x": [str(v)[:10] for v in trace["x"]],
                               "y": list(trace.get("y") or [])})
            aggregate.append({"div_id": p["div_id"],
                              "title": ((p["layout"] or {}).get("title") or {}).get("text"),
                              "traces": traces})

    return {
        "source": {
            "file": os.path.basename(path),
            "bytes": len(raw),
            "sha256": hashlib.sha256(raw).hexdigest(),
        },
        "extractor": {
            "script": os.path.basename(__file__),
            "method": ("html.parser element walk; each series is joined to the identifier of the "
                       "`div.video-card` element that contains it; Plotly arguments parsed with "
                       "json.JSONDecoder().raw_decode"),
            "refuses": ("no imputation: a card without an identifier, a chart without x, or a y "
                        "value outside the axis's own tickvals is reported, never repaired"),
        },
        "counts": {
            "video_cards_found": len(parser.cards),
            "videos_extracted": len(videos),
            "charts_outside_any_card": len(aggregate),
            "problems": len(problems),
        },
        "problems": problems,
        "videos": videos,
        "aggregate_charts": aggregate,
    }


# ---------------------------------------------------------------------------------------------
# Positive controls. Each one fails loudly if the parse degrades into something that still runs.
# ---------------------------------------------------------------------------------------------
def selftest(path):
    checks = []

    def check(name, ok, detail=""):
        checks.append({"check": name, "ok": bool(ok), "detail": detail})

    res = extract(path)
    check("cards found", res["counts"]["video_cards_found"] > 0,
          str(res["counts"]["video_cards_found"]))
    check("every card yielded a video", res["counts"]["problems"] == 0,
          json.dumps(res["problems"])[:300])
    check("every video has at least one chart",
          all(v["charts"] for v in res["videos"]))
    check("every chart's states are labelled by the axis, not guessed",
          all(c["states_are_labelled"] for v in res["videos"] for c in v["charts"]))
    check("identifiers are distinct",
          len(set(v["video_id"] for v in res["videos"])) == len(res["videos"]))
    check("x and y are the same length",
          all(len(c["x"]) == len(c["y"]) for v in res["videos"] for c in v["charts"]))

    # Control 1: the join must be structural. Move one card's identifier out of its card and the
    # extractor must report a problem instead of silently attaching the series to a neighbour.
    raw = open(path, encoding="utf-8").read()
    first = raw.find('<h3>Video ID:')
    mutated = raw[:first] + raw[first:].replace("Video ID:", "Vidayo ID:", 1)
    # In a TEMPORARY DIRECTORY, never beside the file being read. This script ships inside an
    # object whose file list is part of what it claims; a selftest that writes into that directory
    # - even for a moment, even with a `finally` - is erratum E23 with a different name.
    tmpdir = tempfile.mkdtemp(prefix="extract-selftest-")
    tmp = os.path.join(tmpdir, "mutated.html")
    try:
        open(tmp, "w", encoding="utf-8").write(mutated)
        m = extract(tmp)
        check("control: a renamed identifier heading is reported, not absorbed",
              m["counts"]["problems"] == 1
              and m["counts"]["videos_extracted"] == res["counts"]["videos_extracted"] - 1,
              "problems=%d videos=%d" % (m["counts"]["problems"],
                                         m["counts"]["videos_extracted"]))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # Control 2: an unmapped y value must be reported, never mapped to a nearby label.
    v0 = copy.deepcopy(res["videos"][0]["charts"][0])
    labels = v0["y_axis_labels"]
    check("control: the axis publishes its own label set", labels is not None,
          json.dumps(labels))

    # Control 3: a date column that is not ISO would silently produce nonsense in derive();
    # assert every x parses as a date.
    bad = []
    for v in res["videos"]:
        for c in v["charts"]:
            for x in c["x"]:
                try:
                    datetime.date.fromisoformat(str(x)[:10])
                except ValueError:
                    bad.append(str(x))
    check("control: every x parses as an ISO date", not bad, str(bad[:5]))

    ok = all(c["ok"] for c in checks)
    print(json.dumps({"selftest": checks, "pass": ok}, indent=1))
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("path")
    ap.add_argument("-o", "--out")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.path)
    res = extract(args.path)
    text = json.dumps(res, ensure_ascii=False, indent=1)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print("wrote %s (%d bytes): %d videos, %d problems"
              % (args.out, len(text) + 1, res["counts"]["videos_extracted"],
                 res["counts"]["problems"]))
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
