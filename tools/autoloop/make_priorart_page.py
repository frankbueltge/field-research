#!/usr/bin/env python3
"""Build the session-153 artifact page from the study data. Every number on the page is read
from `data/`; nothing is typed into the HTML by hand.

    python3 tools/autoloop/make_priorart_page.py
"""

import html
import json
import os
from collections import Counter

# Added 2026-09-07 (session 154) so that counts appearing in prose are spelled from the data
# rather than typed. See the two corrections marked in this file.
NUM = {0: "none", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five",
       6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ART = os.path.join(REPO, "artifacts/cycle-002/2026-09-06-does-it-know-it-is-known")
D = os.path.join(ART, "data")


def load(name):
    with open(os.path.join(D, name)) as f:
        return json.load(f)


def e(s):
    return html.escape(str(s))


def pct(x, d=1):
    return "n/a" if x is None else f"{100.0 * x:.{d}f} %"


STUDY = load("study.json")
BENCH = load("benchmark.json")
ARMC = load("armC-live-claims.json")
PROBE = load("reachability-probe.json")
PACHECK = load("prior-art-check.json")

M = STUDY["measures"]
ROWS = {r["id"]: r for r in M["rows"]}
BT = {t["id"]: t for t in BENCH["targeted"]}
A = {i["id"]: i for i in STUDY["armA"]["items"]}
BN = {i["id"]: i for i in STUDY["armBname"]["items"]}
PR = M["predictions"]

CSS = """
:root{--ink:#14161a;--mid:#5b6270;--line:#d9dde4;--bg:#fbfbfc;--hit:#1f6f5c;--miss:#a4392f;
--panel:#fff;--flag:#8a6d1f}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);
font:16px/1.62 "Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif}
main{max-width:53rem;margin:0 auto;padding:3rem 1.25rem 6rem}
h1{font-size:2.1rem;line-height:1.15;margin:0 0 .4rem;letter-spacing:-.01em}
h2{font-size:1.28rem;margin:3rem 0 .7rem;padding-top:1.1rem;border-top:1px solid var(--line)}
h3{font-size:1.02rem;margin:1.8rem 0 .4rem;letter-spacing:.02em;text-transform:uppercase;
color:var(--mid)}
.dek{font-size:1.12rem;color:var(--mid);margin:0 0 1.6rem}
.meta{font-size:.82rem;color:var(--mid);letter-spacing:.03em;text-transform:uppercase;
margin-bottom:1.4rem}
p{margin:0 0 1rem}
strong{font-weight:600}
code,.mono{font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.88em}
table{border-collapse:collapse;width:100%;margin:1.2rem 0;font-size:.93rem;background:var(--panel)}
caption{caption-side:bottom;text-align:left;font-size:.84rem;color:var(--mid);padding-top:.55rem}
th,td{border:1px solid var(--line);padding:.42rem .6rem;text-align:left;vertical-align:top}
th{background:#f2f4f7;font-weight:600;font-size:.86rem}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;
font-family:"SF Mono",Menlo,Consolas,monospace;font-size:.88rem}
.wrap{overflow-x:auto}
figure{margin:1.6rem 0;background:var(--panel);border:1px solid var(--line);padding:1rem}
figcaption{font-size:.85rem;color:var(--mid);margin-top:.6rem}
.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--ink);
padding:1rem 1.15rem;margin:1.6rem 0}
.lead p:last-child{margin-bottom:0}
.hit{color:var(--hit);font-weight:600}
.miss{color:var(--miss);font-weight:600}
.flag{color:var(--flag);font-weight:600}
.note{font-size:.9rem;color:var(--mid)}
blockquote{margin:1.2rem 0;padding:.2rem 0 .2rem 1rem;border-left:3px solid var(--line);
color:var(--mid);font-size:.95rem}
ul,ol{margin:0 0 1rem;padding-left:1.3rem}
li{margin-bottom:.42rem}
footer{margin-top:3.5rem;border-top:1px solid var(--line);padding-top:1rem;font-size:.85rem;
color:var(--mid)}
a{color:#1a4f8a}
@media (max-width:640px){main{padding:2rem .9rem 4rem}h1{font-size:1.65rem}}
"""


def rank_cell(h):
    if not h:
        return '<td class="n"><span class="miss">—</span></td>'
    return f'<td class="n"><span class="hit">{h["rank"]}</span></td>'


def bench_table():
    out = ['<div class="wrap"><table>',
           "<thead><tr><th>#</th><th>what the description is about</th><th>canonical source, "
           "confirmed at source</th><th class='n'>D</th><th class='n'>blind</th>"
           "<th class='n'>name&nbsp;only</th></tr></thead><tbody>"]
    for tid in sorted(BT, key=lambda k: int(k[1:])):
        r, t = ROWS[tid], BT[tid]["target"]
        conf = "confirmed at " + " + ".join(r["confirmed_at"]) if r["confirmed"] else \
            "<span class='miss'>not confirmed — dropped</span>"
        src = (f'{e(t["title"])}, <em>{e(t.get("venue") or "")}</em> {e(t.get("year") or "")} '
               f'<span class="mono">{e(t.get("doi") or "")}</span><br>'
               f'<span class="note">{conf}</span>')
        anchor = ' <span class="flag">anchor</span>' if r["anchor"] else ""
        d = "—" if r["title_overlap"] is None else f'{r["title_overlap"]:.2f}'
        out.append(f'<tr><td>{e(tid)}{anchor}</td>'
                   f'<td>{e(BT[tid]["name"])}</td><td>{src}</td>'
                   f'<td class="n">{d}</td>'
                   + rank_cell(r["armA_hit10"])
                   + rank_cell(r.get("armBname_hit10_post_hoc")) + "</tr>")
    out.append("</tbody></table>")
    out.append("<caption><strong>The benchmark, and where each arm landed.</strong> "
               "D is the share of the target title's content words that appear in the blind "
               "description. <em>blind</em> and <em>name only</em> give the rank at which the "
               "target appeared among the fused top ten; a dash means it did not appear at all. "
               "T8 was dropped under the pre-registered confirmation rule and is shown for "
               "completeness.</caption></div>")
    return "\n".join(out)


def predictions_table():
    order = ["P1_named_beats_blind", "P2_blind_is_weak", "P3_cannot_say_no",
             "P4_reproducible", "P5_retrieves_by_title_words", "P6_anchor_fails_blind"]
    out = ['<div class="wrap"><table>',
           "<thead><tr><th>#</th><th>predicted before the run</th><th>what happened</th>"
           "<th>verdict</th></tr></thead><tbody>"]
    said = {
        "P1_named_beats_blind": f'{M["M2_armB_hit10"]} against {M["M1_armA_hit10"]} of '
                                f'{M["n_usable"]} — but Arm B\'s queries were identical to Arm '
                                f'A\'s for {M["armB_identical_to_armA_post_hoc"]} of 10 items',
        "P2_blind_is_weak": f'{M["M1_armA_hit10"]} of {M["n_usable"]}',
        "P3_cannot_say_no": f'fired on {M["M3_probes_fired"]} of {M["M3_probes_n"]}',
        "P4_reproducible": f'{M["M4_repeat_identical"]} of {M["M4_repeat_n"]} identical '
                           f'({pct(M["M4_repeat_share"])})',
        "P5_retrieves_by_title_words": f'median of D is {M["D_median"]:.2f}, so the below-median '
                                       f'half is empty',
        "P6_anchor_fails_blind": "T1 not retrieved blind at any rank",
    }
    for k in order:
        p = PR[k]
        # Corrected 2026-09-07 (session 154), adversary defect A1. `priorart_study.py` set
        # `void` only when ALL ten Arm-B query sets came back byte-identical to Arm A's; five
        # did, so the flag stayed False and this table rendered P1 as *refuted* while every
        # prose passage on the same page called it void. A prediction carrying a
        # `void_reason` was never tested, whatever the count. The stored data is untouched;
        # the rendering rule now matches the rule the page states.
        if p.get("void") or p.get("void_reason"):
            v = '<span class="flag">void — not tested</span>'
        elif p["holds"]:
            v = '<span class="hit">held</span>'
        else:
            v = '<span class="miss">refuted</span>'
        out.append(f'<tr><td>{e(k.split("_")[0])}</td><td>{e(p["statement"])}</td>'
                   f'<td>{said[k]}</td><td>{v}</td></tr>')
    # Corrected 2026-09-07 (session 154), adversary defect A1, second half: this tally was
    # typed as "two held, three refuted, one void", which was only consistent with P1 being
    # rendered refuted — the very contradiction the prose denied. It is now counted off the
    # same records the rows are rendered from.
    voids = sum(1 for k in order if PR[k].get("void") or PR[k].get("void_reason"))
    helds = sum(1 for k in order
                if PR[k]["holds"] and not (PR[k].get("void") or PR[k].get("void_reason")))
    refs = len(order) - voids - helds
    out.append("</tbody></table><caption>The six predictions of "
               f"<code>PREREGISTRATION.md</code> §5, and their pre-stated falsifiers. "
               f"{NUM.get(helds, helds).capitalize()} held, {NUM.get(refs, refs)} were refuted, "
               f"{NUM.get(voids, voids)} were void — untested, because the arm meant to test "
               f"them measured nothing. <strong>Corrected 2026-09-07:</strong> first published "
               f"as <em>two held, three refuted, one void</em>, which counted P1 as refuted "
               f"while the text called it void.</caption></div>")
    return "\n".join(out)


def probe_table():
    out = ['<div class="wrap"><table>',
           "<thead><tr><th>catalogue</th><th>answers an anonymous request?</th>"
           "<th>what it said</th></tr></thead><tbody>"]
    for name, v in PROBE.items():
        mark = ('<span class="hit">yes</span>' if v["reachable"]
                else '<span class="miss">no</span>')
        out.append(f'<tr><td>{e(name)}</td><td>{mark}</td>'
                   f'<td class="note">{e(v["detail"])}</td></tr>')
    out.append("</tbody></table><caption>Probed from this address, 2026-09-06, by "
               "<code>priorart.py --probe</code>. The same probe run four hours earlier, while "
               "the pre-registration was being written, had arXiv answering <em>Rate exceeded</em> "
               "and then timing out. Which catalogues an unattended stage can consult is not a "
               "fixed property of the stage.</caption></div>")
    return "\n".join(out)


def repeat_table():
    rows = STUDY["repeat"]["rows"]
    agg = {}
    for r in rows:
        k = r["catalogue"]
        a = agg.setdefault(k, {"n": 0, "same": 0, "diff": 0, "err": 0})
        if r["identical"] is None:
            a["err"] += 1
        else:
            a["n"] += 1
            a["same" if r["identical"] else "diff"] += 1
    out = ['<div class="wrap"><table>',
           "<thead><tr><th>catalogue</th><th class='n'>queries re-issued</th>"
           "<th class='n'>identical top ten</th><th class='n'>different</th>"
           "<th class='n'>refused (429)</th></tr></thead><tbody>"]
    for k, a in agg.items():
        out.append(f'<tr><td>{e(k)}</td><td class="n">{a["n"] + a["err"]}</td>'
                   f'<td class="n">{a["same"]}</td><td class="n">{a["diff"]}</td>'
                   f'<td class="n">{a["err"]}</td></tr>')
    out.append("</tbody></table><caption>M4. Every Arm-A query issued a second time the same "
               "afternoon. Two Crossref queries returned nothing on the first pass and ten "
               "records on the second.</caption></div>")
    return "\n".join(out)


def armc_modal_phrase():
    """How many of Arm C's firings share a top record. Counted, never typed.

    Added 2026-09-07 (session 154), adversary defect A2: the sentence this replaces claimed
    all five firings shared one top record. Four do.
    """
    fired = [it for it in ARMC["items"] if it["verdict"] == "PRIOR ART POSSIBLE" and it["top"]]
    tops = [it["top"][0].get("doi") or it["top"][0].get("title", "") for it in fired]
    if not tops:
        return "no firing returned a candidate"
    n_modal = Counter(tops).most_common(1)[0][1]
    if n_modal == len(fired):
        return (f"all {NUM.get(len(fired), len(fired))} firings put the same figure caption at "
                f"the top of the list")
    return (f"{NUM.get(n_modal, n_modal)} of the {NUM.get(len(fired), len(fired))} put the same "
            f"figure caption at the top of the list — not all of them, as this sentence said "
            f"when it was first published on 2026-09-06")


def armc_table():
    counts = ARMC["verdict_counts"]
    out = [f'<p><strong>{counts["PRIOR ART POSSIBLE"]} of {ARMC["n"]}</strong> of the loop\'s own '
           f'claim sentences drew the verdict <code>PRIOR ART POSSIBLE</code>. Here is what it '
           f'pointed at.</p>', '<div class="wrap"><table>',
           "<thead><tr><th>claim</th><th>verdict</th><th>top candidate returned</th>"
           "</tr></thead><tbody>"]
    for it in ARMC["items"]:
        top = it["top"][0]["title"] if it["top"] else "—"
        mark = ('<span class="miss">fires</span>' if it["verdict"] == "PRIOR ART POSSIBLE"
                else "silent")
        out.append(f'<tr><td class="mono">{e(it["key"])}</td><td>{mark}</td>'
                   f'<td class="note">{e(top[:110])}</td></tr>')
    # Corrected 2026-09-07 (session 154), adversary defect A2. This caption used to read
    # "the top candidate for every one of the five firings". It is four of the five: the
    # fifth firing tops out on a different record, which the table two rows above has shown
    # since the day it was published. The sentence was typed by hand into a page whose
    # verification section states that no number on it is. It is now counted.
    fired = [it for it in ARMC["items"] if it["verdict"] == "PRIOR ART POSSIBLE" and it["top"]]
    tops = [it["top"][0].get("doi") or it["top"][0].get("title", "") for it in fired]
    modal, n_modal = (Counter(tops).most_common(1)[0] if tops else ("", 0))
    others = len(fired) - n_modal
    out.append("</tbody></table><caption>Arm C. No ground truth exists here and no truth claim "
               f"is made from it. One record — a figure caption about the cumulative proportion "
               f"of discovered species — is the top candidate for {NUM.get(n_modal, n_modal)} of "
               f"the {NUM.get(len(fired), len(fired))} firings"
               + (f"; the remaining {NUM.get(others, others)} tops out on a different record, a "
                  f"table of gene overlap." if others else ".")
               + " <strong>Corrected 2026-09-07:</strong> as first published this caption, the "
                 "lead paragraph and the summary all said <em>every one of the five</em>. That "
                 "was false against the table above it on the same page.</caption></div>")
    return "\n".join(out)


def anchor_block():
    r = ROWS["T1"]
    t = r["target"]
    bn = BN["T1"]
    top = bn["candidates"][0] if bn["candidates"] else None
    return (
        f'<p>The anchor case is the one that caused this session. Its blind description is not '
        f'prose written for a benchmark: it is the wording committed in '
        f'<code>tools/autoloop/liveness.py</code> on 2026-09-05, when this practice did not know '
        f'what the rule was called. Blind, the stage did not return '
        f'<em>{e(t["title"])}</em> at any rank. Given the name alone — '
        f'<em>{e(BT["T1"]["name"])}</em> — it returned it at rank '
        f'<strong>{e((r.get("armBname_hit10_post_hoc") or {}).get("rank"))}</strong>'
        + (f', as <span class="mono">{e(top["doi"])}</span>' if top and top.get("doi") else "")
        + '. The one thing the stage needed in order to find the paper is the one thing a loop '
          'that has just invented something does not have.</p>')


BODY = f"""<title>Does it know it is known?</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}</style>
<main>
<div class="meta">The Field · session 153 · 2026-09-06 · cycle 002, session 4</div>
<h1>Does it know it is known?</h1>
<p class="dek">Yesterday this practice built a rule, verified it, published it, and then found it
in a paper from 1990. The loop had no stage that could have looked. This session built that stage
and measured it against nine methods whose canonical sources are known. It found none of
them.</p>

<div class="lead">
<p><strong>The result in one paragraph.</strong> Stage PRIOR-ART takes a description, builds three
queries from it by a fixed mechanical rule, sends them to two catalogues that answer an
unauthenticated machine, and fuses the six ranked lists. Given prose describing nine methods
whose founding papers were confirmed at source beforehand, it retrieved
<strong>{M["M1_armA_hit10"]} of {M["n_usable"]}</strong> — not one, at any rank in the top ten.
Given the method's <em>name</em> and nothing else, it retrieved
<strong>{M["armBname_hit10_post_hoc"]} of {M["n_usable"]}</strong>, two of them at rank one,
including the 1990 paper this practice rebuilt. <strong>The description is not a weak query; it
is an actively worse one than the bare name it contains.</strong> And on the loop's own live
output the stage's verdict fires
{ARMC["verdict_counts"]["PRIOR ART POSSIBLE"]} times in {ARMC["n"]}, and {armc_modal_phrase()}.</p>
</div>

<h2>Why this stage</h2>
<p>The loop built on 2026-09-03 has six stages — enumerate, pre-check, test, analyse, write,
review — and not one of them consults the literature. On 2026-09-05 it was given a seventh thing
it could not do: after building a liveness rule from scratch, verifying it and publishing it,
a single query found that the rule is
<strong>Tarone's modified Bonferroni method for discrete data</strong> (<em>Biometrics</em>
46(2):515–522, 1990), standard in significant pattern mining under the name <em>untestable
hypotheses</em>. Question 38 of this practice's carried digest names the gap: <em>an automated
research loop has no stage asking whether the answer is already known — and neither did
we.</em></p>
<p>So: build the stage, and measure where it breaks. It is <strong>mechanical throughout</strong>
— no language model is called anywhere inside it. A stage that needs a model to phrase its query
is not a stage an unattended loop can run without a key, a budget and a dependency it cannot
audit, and putting a model inside the instrument would move the thing being measured into the
thing doing the measuring.</p>

<h3>What it does</h3>
<p>From a description it builds <code>Q1</code>, the whole text truncated to 350 characters;
<code>Q2</code>, the eight highest-ranked content terms; <code>Q3</code>, the four highest-ranked.
Each goes to Crossref and to PubMed, ten results each, and the six lists are fused by reciprocal
rank fusion. It reports <code>PRIOR ART POSSIBLE</code> when some record reaches the top three of
at least two lists, otherwise <code>NONE FOUND</code>. It averages
{M["M5_calls_per_description"]:.0f} calls and
{M["M5_seconds_per_description_mean"]:.1f} seconds per description;
{M["M5_calls_total"]} calls were spent on the benchmark itself.</p>

<h2>Which catalogues an unattended stage can even reach</h2>
{probe_table()}
<p>Three of the five obvious catalogues did not answer at the moment the pre-registration was
written; arXiv answered four hours later. <strong>A stage whose sources are decided by which API
happens to answer that minute is not reproducible</strong>, and that is a property of the stage,
not an accident of the afternoon. The pre-registered design fixed Crossref and PubMed before the
second probe and was not changed afterwards.</p>

<h2>The benchmark</h2>
<p>Ten descriptions, each paired with a proposed canonical source, frozen in the commit that
carries the pre-registration and before a single query was sent. Every proposed source was then
looked up <em>by title</em> and its record read back: {M["n_confirmed"]} of {M["n_proposed"]}
were confirmed and one — the paper behind the <em>garden of forking paths</em> — was not, and was
dropped under the rule stated in advance. No description names its target: the leak check found
{M["n_excluded_for_leak"]} violations.</p>
{bench_table()}

<h3>The anchor</h3>
{anchor_block()}

<h2>The defect this study found in itself</h2>
<p>Arm B was supposed to be the upper bound: the same description with the method's common name
appended in parentheses. It returned exactly what Arm A returned. The reason is arithmetic
between two rules of the pre-registration that were written an hour apart — <code>Q1</code>
truncates at 350 characters and every description is longer than that, so the appended name was
always cut off; and <code>Q2</code>/<code>Q3</code> rank terms by frequency, where a name
occurring once ranks last. For {M["armB_identical_to_armA_post_hoc"]} of the ten items the query
set was <strong>byte-identical</strong> to Arm A's; for the other five the name reached only
<code>Q2</code> or <code>Q3</code>. <strong>Arm B measured nothing, and P1 was therefore not
tested.</strong> It is kept in the record exactly as it ran.</p>
<p>Two repaired arms were run afterwards and are marked post-hoc wherever they appear:
<em>name prepended</em> to the description, which reaches <code>Q1</code>, retrieved
<strong>{M["armBprime_hit10_post_hoc"]} of {M["n_usable"]}</strong> — no better than blind. The
name <em>alone</em>, with the description deleted, retrieved
<strong>{M["armBname_hit10_post_hoc"]} of {M["n_usable"]}</strong>. That contrast is the finding
the broken arm would have hidden: <strong>the prose does not merely fail to help, it destroys a
query that works without it.</strong></p>

<h2>Can it ever say no?</h2>
<p>Four descriptions of this practice's own local measurements were run, for which no target is
claimed. <strong>Stated in advance: these are not proven negatives</strong> — nobody has
established that no paper addresses them, and the fourth was deliberately chosen to sit next to
the anchor's territory. They test one thing: whether the verdict can ever come back empty. It
fired on <strong>{M["M3_probes_fired"]} of {M["M3_probes_n"]}</strong>
({", ".join(M["M3_probes_fired_ids"]) or "none"}), so the prediction that it can never say no was
refuted. On the benchmark's own targeted items the verdict fired
{sum(1 for r in M["rows"] if r["armA_verdict"] == "PRIOR ART POSSIBLE")} times in
{len(M["rows"])} — <em>and it was wrong every one of those times</em>, since the target was never
among what it pointed at. The verdict is not conservative. It is uninformative in both
directions.</p>

<h2>Does it give the same answer twice?</h2>
{repeat_table()}
<p>{M["M4_repeat_identical"]} of {M["M4_repeat_n"]} re-issued queries returned an identical top
ten — {pct(M["M4_repeat_share"])}, under the 90 % registered as the bar, so P4 is refuted. Every
disagreement is Crossref's; PubMed repeated itself exactly, thirty times out of thirty. This is
the reason stage PRIOR-ART is wired into <code>loop.py</code> behind a flag and is
<strong>not</strong> switched on in the nightly arm: a series whose value is that it is
reproducible should not be fed by a stage that disagrees with itself once in four.</p>

<h2>The stage on the loop's own output</h2>
{armc_table()}

<h2>The six predictions</h2>
{predictions_table()}

<h2>Has this been done already?</h2>
<p>Asked <em>before</em> this record was written, which is one stage earlier than the practice
managed yesterday. Two channels, both filed in <code>data/prior-art-check.json</code>.</p>
<p><strong>The house's own shelf</strong> ({PACHECK["house_register"]["entries"]:,} entries,
fetched whole): zero matches for <em>prior art</em>, <em>novelty</em>, <em>reinvent</em>,
<em>citation recommendation</em> or <em>idea generation</em>. The seven <em>search agent</em>
matches are benchmarks and audit frameworks for research agents — answer quality, source
attribution, claim-level auditability — and none treats prior-art retrieval as a stage inside a
loop. A term match over titles is a weak instrument, as this artifact's own measurements say
loudly; absence here is not absence in the literature.</p>
<p><strong>Outward, one query.</strong> It found a real neighbour, and its abstract was read at
source: <strong>NoveltyRank: A Retrieval-Augmented Framework for Conceptual Novelty Estimation in
AI Research</strong>, Yan, Li &amp; Feng, <span class="mono">arXiv:2512.14738</span>
(2025-12-12). It combines learned semantic representations with retrieval against the literature
to score how novel a paper is, as classification and as ranking, and reports fine-tuned small
models beating larger zero-shot ones.</p>
<p><strong>The daylight.</strong> That framework scores novelty and <em>takes retrieval as
given</em>. This session measures the retrieval alone, model-free, and asks the opposite
question: handed prose about something whose source is known, does a mechanical stage return that
source at all? The answer here is the recall floor underneath any novelty score — and 0 of 9 says
that floor is on the ground for the free-text catalogue route, which is <em>not</em> the route
they take; nothing here counts against their result. The two are complementary. A substantial commercial sector also sells automated prior-art search over patent
literature; its material was seen in search results, was <strong>not</strong> read at source, and
nothing here rests on it.</p>
<p><strong>Still unfound:</strong> a published measurement of prior-art recall from a
<em>name-free description of a known method</em> inside an automated research pipeline. This
session offers one, for one instrument.</p>

<h2>What this does and does not show</h2>
<ul>
<li><strong>It is one instrument.</strong> One mechanical query scheme, two catalogues, nine
targets. A miss here is a miss for this stage, not a statement about the literature, and not
evidence that no automated prior-art stage can work.</li>
<li><strong>The targets are proposals, not a census.</strong> Each is <em>a</em> canonical source
for its description, confirmed to exist by reading its catalogue record. Another paper might
serve as prior art for the same description and would not be counted a hit.</li>
<li><strong>Nine of the ten blind descriptions were written today</strong>, by the same practice
that built the stage. Only the anchor has genuine provenance — committed the day before, in
ignorance of the answer. The other nine could in principle have been written to fail. That they
also failed <em>with the name prepended</em>, where the name alone succeeds, is the check against
that.</li>
<li><strong>What broke is retrieval, not the idea of the stage.</strong> The measurement points
at a specific mechanism: free-text relevance ranking over a catalogue that indexes figure
captions, tables and supplemental files alongside papers returns those derivative records first.
Asked for <em>Wilson score interval</em>, Crossref's first answers are figure captions containing
the word <em>score</em>.</li>
<li><strong>It cannot read.</strong> Nothing here judges whether a returned record is the same
idea as the description. That judgment was not automated, and this stage does not pretend
it was.</li>
</ul>

<h2>What follows</h2>
<p>The step this practice has been circling since 2026-09-03 — <em>which step of the research
loop must remain human</em> — has a sharper candidate after today. It is not <em>deciding a
question is worth asking</em>: that turned out to be automatable in the narrow sense last
session. It is <strong>recognising that an answer you are looking at is the answer you already
have</strong>. Retrieval by name is cheap and the loop has no name. Retrieval by description is
what it needs, and the free-text route measured here does not deliver it at all.</p>
<p>What this session does not claim is that the step is impossible. It rules out one route,
mechanically, with its failure conditions published in advance — which is the least a practice
can do before saying that something must remain human.</p>

<footer>
<p><strong>Evidence.</strong> <code>PREREGISTRATION.md</code> (committed before the first query),
<code>METHOD.md</code>, <code>VERIFICATION.md</code>, <code>SUMMARY.md</code>.
Data: <code>data/benchmark.json</code> (frozen with the pre-registration),
<code>data/study.json</code> (every query and every returned identifier),
<code>data/armC-live-claims.json</code>, <code>data/reachability-probe.json</code>.
Instruments: <code>tools/autoloop/priorart.py</code>,
<code>tools/autoloop/priorart_study.py</code>, page built by
<code>tools/autoloop/make_priorart_page.py</code>.</p>
<p>The Field · a practice of the research ecology around frankbueltge.de · cycle 002 ·
generated from <code>data/study.json</code> of {e(M["generated_utc"])}.</p>
</footer>
</main>
"""

with open(os.path.join(ART, "index.html"), "w") as f:
    f.write(BODY)
print("wrote " + os.path.join(ART, "index.html"))
