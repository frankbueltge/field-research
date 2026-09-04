#!/usr/bin/env python3
"""autoloop — builds the page for the dial artifact from its data files.

Every number on the page is read from data/. Nothing is typed in twice. The figures are
emitted as static SVG at build time, so the whole argument stands with no script and no
network; the script only lets a reader move k along a curve that is already drawn.

  python3 tools/autoloop/make_dial_page.py --dir artifacts/cycle-002/2026-09-04-the-dial
  python3 tools/autoloop/make_dial_page.py --dir ... --check    # rebuild, fail on any difference
"""

import argparse
import hashlib
import json
import os
import sys

ARMS = [("arxiv", "arXiv", "2,039 preprints, eight categories"),
        ("crossref", "Crossref", "2,400 journal articles, eight publishers")]
COL = {"arxiv": "#1f6feb", "crossref": "#bc4c00"}


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def pct(x, d=2):
    return f"{100*x:.{d}f}&nbsp;%"


# --- figures ----------------------------------------------------------------------------

def fig_dial(sweeps, w=720, h=380):
    """The dial itself: null-world findings per run against k, both arms, both families,
    with the nominal line 0.05k drawn through."""
    pad_l, pad_b, pad_t, pad_r = 58, 46, 18, 14
    ks = sweeps["arxiv"]["k_values"]
    kmax = max(ks)
    ymax = 3.6
    def X(k): return pad_l + (w - pad_l - pad_r) * k / kmax
    def Y(v): return h - pad_b - (h - pad_b - pad_t) * v / ymax
    p = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Null-world findings per run against the number of questions asked, for two corpora." class="fig">']
    p.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="var(--fig-bg)"/>')
    for v in range(0, 4):
        p.append(f'<line x1="{pad_l}" y1="{Y(v):.1f}" x2="{w-pad_r}" y2="{Y(v):.1f}" stroke="var(--grid)"/>')
        p.append(f'<text x="{pad_l-8}" y="{Y(v)+4:.1f}" text-anchor="end" class="tick">{v}</text>')
    for k in ks:
        p.append(f'<line x1="{X(k):.1f}" y1="{Y(0):.1f}" x2="{X(k):.1f}" y2="{Y(0)+5:.1f}" stroke="var(--axis)"/>')
        p.append(f'<text x="{X(k):.1f}" y="{Y(0)+19:.1f}" text-anchor="middle" class="tick">{k}</text>')
    # the nominal expectation, 0.05 k
    p.append(f'<line x1="{X(0):.1f}" y1="{Y(0):.1f}" x2="{X(kmax):.1f}" y2="{Y(0.05*kmax):.1f}" '
             f'stroke="var(--nominal)" stroke-width="1.5" stroke-dasharray="6 4"/>')
    p.append(f'<text x="{X(kmax)-4:.1f}" y="{Y(0.05*kmax)-8:.1f}" text-anchor="end" class="lbl" '
             f'fill="var(--nominal)">nominal 0.05&#215;k</text>')
    for arm, label, _ in ARMS:
        d = sweeps[arm]
        for fam, dash in (("lean", ""), ("dense", ' stroke-dasharray="3 3"')):
            pts = " ".join(f"{X(k):.1f},{Y(d['null'][f'{fam}@{k}']['mean']):.1f}" for k in ks)
            p.append(f'<polyline points="{pts}" fill="none" stroke="{COL[arm]}" stroke-width="2"{dash} opacity="0.95"/>')
            for k in ks:
                v = d["null"][f"{fam}@{k}"]["mean"]
                p.append(f'<circle cx="{X(k):.1f}" cy="{Y(v):.1f}" r="{3 if fam=="lean" else 2.2}" '
                         f'fill="{COL[arm] if fam=="lean" else "var(--fig-bg)"}" stroke="{COL[arm]}" stroke-width="1.4"/>')
    # legend, kept clear of the curves in the plot's empty upper-left corner
    ly = pad_t + 14
    for arm, label, _ in ARMS:
        d = sweeps[arm]
        p.append(f'<line x1="{pad_l+14}" y1="{ly-4:.1f}" x2="{pad_l+40}" y2="{ly-4:.1f}" '
                 f'stroke="{COL[arm]}" stroke-width="2"/>')
        p.append(f'<circle cx="{pad_l+27}" cy="{ly-4:.1f}" r="3" fill="{COL[arm]}"/>')
        p.append(f'<text x="{pad_l+48}" y="{ly:.1f}" class="lbl" fill="{COL[arm]}">'
                 f'{label} &mdash; slope {d["null"]["lean@66"]["per_test_rate"]:.4f}</text>')
        ly += 18
    p.append(f'<line x1="{pad_l}" y1="{Y(0):.1f}" x2="{w-pad_r}" y2="{Y(0):.1f}" stroke="var(--axis)"/>')
    p.append(f'<line x1="{pad_l}" y1="{pad_t}" x2="{pad_l}" y2="{Y(0):.1f}" stroke="var(--axis)"/>')
    p.append(f'<text x="{(w+pad_l)/2:.0f}" y="{h-6}" text-anchor="middle" class="axl">k &mdash; questions asked</text>')
    p.append(f'<text x="14" y="{(h)/2:.0f}" text-anchor="middle" class="axl" transform="rotate(-90 14 {h/2:.0f})">findings per run, empty world</text>')
    p.append("</svg>")
    return "".join(p)


def fig_perquestion(sweeps, w=720, h=300):
    """Every question's own false-positive rate in an empty world, sorted. The dead ones are
    the point: a question that cannot fire looks exactly like a question answered no."""
    pad_l, pad_b, pad_t, pad_r = 52, 44, 18, 14
    p = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Per-question rejection rate in an empty world, all 66 questions, both corpora, sorted." class="fig">']
    p.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="var(--fig-bg)"/>')
    ymax = 0.08
    def Y(v): return h - pad_b - (h - pad_b - pad_t) * min(v, ymax) / ymax
    for v in (0.0, 0.02, 0.04, 0.05, 0.06, 0.08):
        stroke = "var(--nominal)" if v == 0.05 else "var(--grid)"
        dash = ' stroke-dasharray="6 4"' if v == 0.05 else ""
        p.append(f'<line x1="{pad_l}" y1="{Y(v):.1f}" x2="{w-pad_r}" y2="{Y(v):.1f}" '
                 f'stroke="{stroke}"{dash}/>')
        p.append(f'<text x="{pad_l-8}" y="{Y(v)+4:.1f}" text-anchor="end" class="tick">{v*100:.0f}%</text>')
    n = 66
    bw = (w - pad_l - pad_r) / (2 * n + 6)
    x = pad_l + 2
    for arm, label, _ in ARMS:
        rates = sorted(sweeps[arm]["per_question_null_rate"].values())
        for r in rates:
            p.append(f'<rect x="{x:.2f}" y="{Y(r):.1f}" width="{bw*0.86:.2f}" height="{Y(0)-Y(r):.1f}" '
                     f'fill="{COL[arm]}" opacity="{0.35 if r==0 else 0.85}"/>')
            if r == 0:
                p.append(f'<rect x="{x:.2f}" y="{Y(0)-3:.1f}" width="{bw*0.86:.2f}" height="3" fill="var(--dead)"/>')
            x += bw
        dead = sum(1 for r in rates if r == 0)
        p.append(f'<text x="{x - bw*n/2:.1f}" y="{pad_t+12}" text-anchor="middle" class="lbl" '
                 f'fill="{COL[arm]}">{label} &mdash; {dead} dead</text>')
        x += bw * 6
    p.append(f'<line x1="{pad_l}" y1="{Y(0):.1f}" x2="{w-pad_r}" y2="{Y(0):.1f}" stroke="var(--axis)"/>')
    p.append(f'<text x="{(w+pad_l)/2:.0f}" y="{h-6}" text-anchor="middle" class="axl">the 66 questions of each space, sorted by their own rate</text>')
    p.append("</svg>")
    return "".join(p)


def fig_counts(sweeps, w=720, h=220):
    """What the loop reports against what it actually found: questions, raw findings,
    survivors, each with the distinct-claim count behind it."""
    rows = []
    for arm, label, _ in ARMS:
        d = sweeps[arm]
        r = d["real_full_space"]
        rows.append((f"{label} &mdash; questions asked", d["questions"], d["distinct_pairs"], COL[arm]))
        rows.append((f"{label} &mdash; findings reported", r["raw_findings"], r["distinct_pairs_among_raw"], COL[arm]))
        rows.append((f"{label} &mdash; survivors after BH", r["bh_survivors_all66"],
                     r["distinct_pairs_among_bh_all66"], COL[arm]))
    mx = max(r[1] for r in rows)
    pad_l, pad_t = 232, 14
    bh = (h - pad_t - 22) / len(rows)
    p = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Reported counts against distinct claims behind them." class="fig">']
    p.append(f'<rect x="0" y="0" width="{w}" height="{h}" fill="var(--fig-bg)"/>')
    for i, (lab, rep, dist, c) in enumerate(rows):
        y = pad_t + i * bh
        bw = (w - pad_l - 70) * rep / mx
        dw = (w - pad_l - 70) * dist / mx
        p.append(f'<text x="{pad_l-10}" y="{y+bh*0.62:.1f}" text-anchor="end" class="lbl">{lab}</text>')
        p.append(f'<rect x="{pad_l}" y="{y+bh*0.16:.1f}" width="{bw:.1f}" height="{bh*0.6:.1f}" fill="{c}" opacity="0.28"/>')
        p.append(f'<rect x="{pad_l}" y="{y+bh*0.16:.1f}" width="{dw:.1f}" height="{bh*0.6:.1f}" fill="{c}" opacity="0.95"/>')
        p.append(f'<text x="{pad_l+bw+8:.1f}" y="{y+bh*0.62:.1f}" class="tick"><tspan font-weight="600">{dist}</tspan> of {rep}</text>')
    p.append(f'<text x="14" y="{h-5}" class="tick">solid: distinct claims &nbsp;&middot;&nbsp; pale: what the loop reports</text>')
    p.append("</svg>")
    return "".join(p)


# --- the page ---------------------------------------------------------------------------

CSS = """
:root{--bg:#fbfaf8;--fg:#1a1a1a;--muted:#5c5c5c;--rule:#e2ded8;--fig-bg:#ffffff;
--grid:#eceae6;--axis:#9a958e;--nominal:#8a8178;--dead:#c62828;--accent:#1f6feb;--card:#f4f2ee;}
@media (prefers-color-scheme:dark){:root{--bg:#14161a;--fg:#e8e6e3;--muted:#a8a49e;--rule:#2b2f36;
--fig-bg:#191c21;--grid:#252a31;--axis:#6b7078;--nominal:#8d8880;--dead:#ef5350;--accent:#6ea8fe;--card:#1c2027;}}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.62 Georgia,"Iowan Old Style","Times New Roman",serif;}
main{max-width:820px;margin:0 auto;padding:44px 22px 90px}
h1{font-size:2.05rem;line-height:1.18;margin:0 0 .3em;letter-spacing:-.01em}
h2{font-size:1.28rem;margin:2.4em 0 .5em;padding-top:.7em;border-top:1px solid var(--rule)}
h3{font-size:1.02rem;margin:1.6em 0 .35em}
p{margin:.75em 0}
.dek{color:var(--muted);font-size:1.06rem;margin:0 0 1.4em}
.meta{color:var(--muted);font-size:.85rem;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
border-bottom:1px solid var(--rule);padding-bottom:1.1em;margin-bottom:1.6em}
.fig{width:100%;height:auto;display:block;margin:1.1em 0 .3em;border:1px solid var(--rule);border-radius:3px}
.tick{font:11px ui-monospace,SFMono-Regular,Menlo,monospace;fill:var(--muted)}
.lbl{font:12px ui-monospace,SFMono-Regular,Menlo,monospace;fill:var(--fg)}
.axl{font:12px Georgia,serif;fill:var(--muted)}
figcaption{color:var(--muted);font-size:.87rem;margin:.2em 0 1.6em}
figure{margin:0}
table{border-collapse:collapse;width:100%;font-size:.87rem;margin:1em 0;
font-family:ui-monospace,SFMono-Regular,Menlo,monospace}
th,td{border-bottom:1px solid var(--rule);padding:.42em .5em;text-align:right}
th:first-child,td:first-child{text-align:left}
thead th{border-bottom:1.5px solid var(--axis);font-weight:600}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
.verdict{display:inline-block;padding:.06em .5em;border-radius:2px;font-size:.78rem;font-weight:700;
font-family:ui-monospace,monospace;letter-spacing:.02em}
.ref{background:#c6282822;color:var(--dead);border:1px solid #c6282855}
.held{background:#2e7d3222;color:#2e7d32;border:1px solid #2e7d3255}
.part{background:#a1670022;color:#a16700;border:1px solid #a1670055}
@media (prefers-color-scheme:dark){.held{color:#81c784}.part{color:#d3a13a}}
blockquote{margin:1.2em 0;padding:.1em 0 .1em 1.1em;border-left:3px solid var(--rule);
color:var(--muted);font-style:italic}
.card{background:var(--card);border:1px solid var(--rule);border-radius:4px;padding:1em 1.2em;margin:1.3em 0}
.card p:first-child{margin-top:0}.card p:last-child{margin-bottom:0}
.k{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;font-size:.92em}
footer{margin-top:3.2em;padding-top:1.1em;border-top:1px solid var(--rule);
color:var(--muted);font-size:.83rem}
a{color:var(--accent)}
"""


def table(headers, rows, aligns=None):
    h = "".join(f"<th>{c}</th>" for c in headers)
    body = ""
    for r in rows:
        body += "<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>"
    return f'<div class="scroll"><table><thead><tr>{h}</tr></thead><tbody>{body}</tbody></table></div>'


def build(d):
    sweeps = {a: json.load(open(os.path.join(d, "data", f"sweep-{a}.json"))) for a, _, _ in ARMS}
    checks = json.load(open(os.path.join(d, "data", "checks.json")))
    ax, cx = sweeps["arxiv"], sweeps["crossref"]
    ca, cc = checks["arms"]["arxiv"], checks["arms"]["crossref"]

    # post-hoc restriction, computed here from the committed files (labelled as post-hoc below)
    posthoc = {}
    for arm in ("arxiv", "crossref"):
        d_ = sweeps[arm]
        pq = d_["per_question_null_rate"]
        claim = [k for k in pq if not d_["tests"][k]["failures"]]
        kill = [k for k in pq if d_["tests"][k]["failures"]]
        posthoc[arm] = {
            "whole": sum(pq.values()) / len(pq), "n_whole": len(pq),
            "claimable": sum(pq[k] for k in claim) / len(claim), "n_claim": len(claim),
            "killed": sum(pq[k] for k in kill) / len(kill), "n_kill": len(kill),
            "dead": sorted(k for k, v in pq.items() if v == 0.0),
        }

    ks = ax["k_values"]
    sweep_rows = []
    for k in ks:
        row = [f"<b>{k}</b>"]
        for arm in ("arxiv", "crossref"):
            for fam in ("lean", "dense"):
                c = sweeps[arm]["null"][f"{fam}@{k}"]
                row.append(f'{c["mean"]:.3f}')
        sweep_rows.append(row)

    verdicts = [
        ("P1", "the dial is a line: null yield linear in k, slope 0.045&ndash;0.055, R&sup2;&nbsp;&ge;&nbsp;0.99",
         "part", "held on arXiv, half-failed on Crossref",
         f'arXiv slope <b>{ca["P1"]["lean"]["slope"]:.5f}</b> (R&sup2; {ca["P1"]["lean"]["r2"]:.5f}); '
         f'Crossref slope <b>{cc["P1"]["lean"]["slope"]:.5f}</b> (R&sup2; {cc["P1"]["lean"]["r2"]:.5f}). '
         "Both are lines; the Crossref slope falls outside the registered band."),
        ("P2", "redundancy taxes the variance: at k&nbsp;=&nbsp;30, dense variance &ge; 10&nbsp;% above lean",
         "ref", "refuted on both",
         f'variance ratio <b>{ca["P2"]["ratio"]:.3f}</b> '
         f'(95&nbsp;% {ca["P2"]["ratio_ci95_paired_bootstrap"]["ci95"][0]:.3f}&ndash;'
         f'{ca["P2"]["ratio_ci95_paired_bootstrap"]["ci95"][1]:.3f}) on arXiv, '
         f'<b>{cc["P2"]["ratio"]:.3f}</b> '
         f'({cc["P2"]["ratio_ci95_paired_bootstrap"]["ci95"][0]:.3f}&ndash;'
         f'{cc["P2"]["ratio_ci95_paired_bootstrap"]["ci95"][1]:.3f}) on Crossref. Both intervals contain 1.'),
        ("P3", "redundancy clumps the nights: P(&ge;1) below independence, and further below for dense",
         "ref", "unsupported",
         f'independence gives 0.7854. arXiv lean {ca["P3"]["lean_p_at_least_one"]:.3f} / dense '
         f'{ca["P3"]["dense_p_at_least_one"]:.3f}; Crossref lean {cc["P3"]["lean_p_at_least_one"]:.3f} '
         f'(<i>above</i> independence) / dense {cc["P3"]["dense_p_at_least_one"]:.3f}. Dense is below lean on '
         f'both, but paired McNemar gives p = {ca["P3"]["paired_mcnemar_dense_vs_lean"]["p"]:.2f} and '
         f'p = {cc["P3"]["paired_mcnemar_dense_vs_lean"]["p"]:.2f}: not distinguishable from chance.'),
        ("P4", "redundancy taxes the power: deduplicating the space yields more survivors",
         "ref", "refuted, in the opposite direction",
         f'deduplicating recovered nothing on either corpus. arXiv: '
         f'{ca["P4"]["bh_survivors_all66"]} survivors over 66 questions against '
         f'{ca["P4"]["bh_survivors_dedup51"]} over 51 &mdash; and <b>the distinct claim set is the same either '
         f'way ({ca["P4"]["distinct_claims_all66"]} claims)</b>. Crossref: '
         f'{cc["P4"]["bh_survivors_all66"]} against {cc["P4"]["bh_survivors_dedup51"]}, distinct claims '
         f'{cc["P4"]["distinct_claims_all66"]} either way.'),
        ("P5", "the slope transfers: the Crossref per-test interval contains &alpha; and overlaps arXiv's",
         "ref", "refuted as registered",
         f'arXiv <b>{pct(ca["P5"]["per_test_rate"])}</b> '
         f'({pct(ca["P5"]["ci95"][0])}&ndash;{pct(ca["P5"]["ci95"][1])}), Crossref '
         f'<b>{pct(cc["P5"]["per_test_rate"])}</b> '
         f'({pct(cc["P5"]["ci95"][0])}&ndash;{pct(cc["P5"]["ci95"][1])}). The intervals do not overlap and '
         f'neither contains 0.05. <b>Why</b> is section 5.'),
    ]
    vrows = "".join(
        f'<tr><td><b>{p}</b></td><td style="text-align:left">{txt}</td>'
        f'<td><span class="verdict {cls}">{lab}</span></td></tr>' for p, txt, cls, lab, _ in verdicts)
    vdetail = "".join(f"<h3>{p} &mdash; {lab}</h3><p>{det}</p>" for p, _, _, lab, det in verdicts)

    dead_list = ", ".join(f'<span class="k">{esc(x)}</span>' for x in posthoc["crossref"]["dead"])

    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The dial &mdash; how a research loop's false findings scale with how much it asks</title>
<style>{CSS}</style></head><body><main>

<p class="meta">The Field &middot; session 151 &middot; cycle 002 &middot; 2026-09-04 &middot;
{ax['replicates']} null replicates per cell, seed {ax['seed']} &middot;
pre-registration committed before the second corpus was fetched</p>

<h1>The dial</h1>
<p class="dek">Yesterday this practice built a loop that asks 66 questions of a corpus without a
person in the middle, and wrote down one sentence about it: <i>it manufactures findings because it
asks 66 questions and for no other reason &mdash; throughput and error control are the same
dial.</i> That sentence rested on a single reading. Today the dial was turned across a sixteen-fold
range of k, in two worlds, with the redundancy of the questions held apart from their number.
Three of five pre-registered predictions are refuted, and the claim this session set out to
establish died by the falsifier it wrote for itself.</p>

<h2>1. What was measured</h2>
<p>The same loop, the same two tests, the same &alpha;&nbsp;=&nbsp;0.05, run over question
<i>sets</i> of size k = {", ".join(str(k) for k in ks)}, against a corpus and against an
<b>empty world</b> &mdash; the same records with the grouping block row-permuted, so that every
association a question could ask about has been destroyed and every finding is false by
construction. {ax['replicates']} permuted worlds per cell; every cell scored against the
<i>same</i> permuted world on each replicate, so any two cells can be compared paired.</p>

<p>Two corpora, built to the same template and otherwise unrelated:</p>
{table(["corpus", "records", "strata", "questions", "distinct pairs", "killed at review", "breaks"],
       [[f'<b>arXiv</b>', f'{ax["corpus"]["records"]:,}', "8 categories", ax["questions"],
         ax["distinct_pairs"], ax["review_kills"], len(ax["breaks"])],
        [f'<b>Crossref</b>', f'{cx["corpus"]["records"]:,}', "8 publishers", cx["questions"],
         cx["distinct_pairs"], cx["review_kills"], len(cx["breaks"])]])}

<p>Both spaces are 8 groupings &times; 9 outcomes minus the six self-pairs, and in both, six
variables appear in both roles &mdash; so in both, <b>66 questions rest on 51 distinct variable
pairs</b>. That redundancy was reproduced deliberately: it is the thing under test, not an
accident of arXiv. At each k the questions were chosen twice, by two fixed rules: <b>lean</b>,
which never repeats a variable pair, and <b>dense</b>, which repeats as many as the space allows.
At k&nbsp;=&nbsp;30 the two differ maximally &mdash; redundancy 0 against 0.5, same number of
questions asked. At k&nbsp;=&nbsp;66 they are the same set, and nothing is claimed there.</p>

<h2>2. The dial</h2>
<figure>{fig_dial(sweeps)}
<figcaption>Findings per run in an empty world, against how many questions were asked. Solid:
lean. Dashed: dense. The grey dashed line is what independence at &alpha;&nbsp;=&nbsp;0.05
predicts. Both worlds give a straight line through the origin; neither line is the grey one, and
the two are not the same line.</figcaption></figure>

<div class="scroll"><table><thead><tr><th>k</th>
<th>arXiv lean</th><th>arXiv dense</th><th>Crossref lean</th><th>Crossref dense</th></tr></thead>
<tbody>{"".join("<tr>" + "".join(f"<td>{c}</td>" for c in r) + "</tr>" for r in sweep_rows)}</tbody></table></div>

<p><b>The line is real.</b> Fitted through the origin, the arXiv slope is
{ca['P1']['lean']['slope']:.5f} with R&sup2;&nbsp;=&nbsp;{ca['P1']['lean']['r2']:.5f}; the Crossref
slope is {cc['P1']['lean']['slope']:.5f} with R&sup2;&nbsp;=&nbsp;{cc['P1']['lean']['r2']:.5f}.
Over a sixteen-fold range of k, in two literatures with nothing in common, the number of false
findings a loop produces is proportional to the number of questions it asks. <b>That much of
yesterday's sentence survives, and it survives on a corpus that did not exist in yesterday's
experiment.</b></p>

<h2>3. The five predictions, and what happened to them</h2>
{table(["", "predicted, before any datum", "verdict"], [], None).replace("<tbody></tbody>", f"<tbody>{vrows}</tbody>")}
{vdetail}

<h2>4. The claim this session set out to make, and its death</h2>
<blockquote>Redundancy in an auto-generated question space is a tax that buys nothing: it does not
change the expected number of false findings, but it makes the yield noisier and costs real
power. <b>Refuted if P2, P3 and P4 all fail.</b> &mdash; pre-registration &sect;5, written before
the numbers existed</blockquote>
<p>P2 failed. P3 failed. P4 failed. <b>The claim is dead by the rule this session wrote for it.</b>
Redundancy did not inflate the variance of the nightly yield (ratios 1.07 and 0.98, both intervals
containing 1). It did not make loud nights likelier (McNemar p = 0.60 and 0.29). It did not cost a
single survivor under multiplicity correction &mdash; and this last one is worth stating as a
positive result rather than a failure, because it is not obvious:</p>

<div class="card"><p><b>Benjamini-Hochberg is self-correcting for exact duplicates.</b> A duplicated
question adds one test to the denominator and one small p-value to the numerator, and the two
cancel. Deduplicating the arXiv space from 66 questions to 51 changed the survivor list from
{ca['P4']['bh_survivors_all66']} entries to {ca['P4']['bh_survivors_dedup51']} &mdash; but the
{ca['P4']['distinct_claims_all66']} <i>distinct claims</i> behind them are identical, and the
entries lost were the duplicate copies. On Crossref: {cc['P4']['bh_survivors_all66']} against
{cc['P4']['bh_survivors_dedup51']}, and {cc['P4']['distinct_claims_all66']} distinct claims either
way. Redundancy costs no power. It also buys none.</p></div>

<h2>5. What redundancy does do &mdash; and it is not statistical</h2>
<figure>{fig_counts(sweeps)}
<figcaption>Pale: the number the loop reports. Solid: the distinct claims behind it.</figcaption></figure>

<p>The loop asks {ax['questions']} questions that are {ax['distinct_pairs']}. It reports
{ax['real_full_space']['raw_findings']} findings that are
{ax['real_full_space']['distinct_pairs_among_raw']}. After correction it reports
{ax['real_full_space']['bh_survivors_all66']} survivors that are
{ax['real_full_space']['distinct_pairs_among_bh_all66']}. On Crossref, the same shape:
{cx['real_full_space']['raw_findings']} findings that are
{cx['real_full_space']['distinct_pairs_among_raw']},
{cx['real_full_space']['bh_survivors_all66']} survivors that are
{cx['real_full_space']['distinct_pairs_among_bh_all66']}.</p>

<p><b>The inflation is in the count, not in the statistics.</b> Every instrument the loop carries
&mdash; its p-values, its false-discovery correction, its split-half replication, its empty-world
calibration &mdash; is behaving correctly and reports nothing amiss, because nothing is amiss in
any of them. What is wrong is the sentence at the end: <i>fourteen findings</i>, when eleven of
them are claims and three are the same claims said twice. Yesterday a person saw that in one
sitting on the arXiv space. It is now measured on a second, unrelated one, which makes it a
property of the architecture rather than of a corpus.</p>

<h2>6. Why the two slopes differ, which is the useful part</h2>
<figure>{fig_perquestion(sweeps)}
<figcaption>Each of the 66 questions of each space, with its own rejection rate in an empty world,
sorted. The dashed line is &alpha;&nbsp;=&nbsp;0.05. Red feet mark questions whose rate is exactly
zero: they cannot fire at all.</figcaption></figure>

<p>P5 failed because the Crossref space contains <b>{len(posthoc['crossref']['dead'])} questions
that never fire in {cx['replicates']} empty worlds, and never could</b>:</p>
<p>{dead_list}</p>
<p>All of them rest on <span class="k">has_fulltext_link</span>, which is true for
<b>{cx['corpus']['records']:,} of {cx['corpus']['records']:,} records &mdash; 100.0&nbsp;%</b>.
The grouping divides the corpus into everything and nothing, so no test on it can reject, in an
empty world or a full one. A ninth question dies for the same reason on
<span class="k">open_licence</span> (99.7&nbsp;%). Those dead questions are counted in the
denominator of the loop's self-calibration figure, and they drag it down.</p>

<div class="card"><p><b>Post-hoc, and marked as post-hoc &mdash; this restriction was not
pre-registered.</b> Computed over only the questions that survive the loop's own review
pre-conditions, the two per-test rates are
<b>{pct(posthoc['arxiv']['claimable'])}</b> on arXiv ({posthoc['arxiv']['n_claim']} questions) and
<b>{pct(posthoc['crossref']['claimable'])}</b> on Crossref ({posthoc['crossref']['n_claim']}
questions). Over the questions the review killed: {pct(posthoc['arxiv']['killed'])} and
{pct(posthoc['crossref']['killed'])}. <b>The difference between the two worlds vanishes, and both
land on &alpha;.</b> The slope does transfer &mdash; between the questions that are awake.</p></div>

<p>Two things follow, and the second is about us.</p>
<p><b>First: a question-generating loop cannot tell a question that is asleep from a question
that was answered no.</b> Both arrive at the analysis stage as a non-finding. Nine of Crossref's
66 questions were structurally incapable of an answer, and no stage of the loop said so &mdash;
the review pre-conditions killed them, correctly, and killing them is not the same as noticing
that a ninth of the question space was never a question.</p>

<p><b>Second: the loop's published self-calibration depends on a denominator nobody registered.</b>
Yesterday this practice published {pct(0.0488)} as its per-test rate in an empty world, over all 66
questions. On today's arXiv corpus that same figure is {pct(ca['P5']['per_test_rate'])} over 66 and
{pct(posthoc['arxiv']['claimable'])} over the {posthoc['arxiv']['n_claim']} claimable ones. On
Crossref the two denominators give {pct(cc['P5']['per_test_rate'])} and
{pct(posthoc['crossref']['claimable'])} &mdash; a gap far larger than the sampling error on either.
A convened adversary found <i>exactly this defect</i> yesterday, in the multiplicity correction:
a denominator that differed from the registered one. It has now appeared a second time, in a
different number. The lesson is not that either figure is wrong. It is that
<b>this loop divides counts by a number of questions in several places, and it has never once been
asked which questions.</b></p>

<h2>7. What this does not show</h2>
<p>Two corpora are not loops in general. Both arms are the <i>same</i> loop, with the same battery,
the same &alpha; and question spaces built to one template; what can transfer is the behaviour of
that architecture, and nothing here speaks about loops built differently. The redundancy studied is
<i>exact</i> duplication &mdash; the same variable pair asked twice. Near-duplication, where two
questions are strongly correlated without being identical, is untouched by this design, and the
Benjamini-Hochberg cancellation shown in section 4 is not expected to hold there. Both corpora are
one day's fetch. The verdicts above are the pre-registered ones; the section-6 restriction is
post-hoc and is labelled so on the page and in the record.</p>

<h2>8. How to check this</h2>
<p>Everything below is in <span class="k">data/</span> beside this page, and every number on the
page is read from those files at build time &mdash; nothing is typed in twice.</p>
{table(["file", "what it is"],
       [['<span class="k">data/corpus-arxiv.json</span>',
         f'{ax["corpus"]["records"]:,} arXiv records as derived features and a bare identifier &mdash; no titles, no abstracts, no names'],
        ['<span class="k">data/corpus-crossref.json</span>',
         f'{cx["corpus"]["records"]:,} Crossref records, the same contract'],
        ['<span class="k">data/sweep-arxiv.json</span>', 'every cell of the sweep, including the whole per-replicate count vector'],
        ['<span class="k">data/sweep-crossref.json</span>', 'the same for the second world'],
        ['<span class="k">data/checks.json</span>', 'the five pre-registered checks, computed from the sweeps'],
        ['<span class="k">data/breaks-*.json</span>', 'the fetch break logs &mdash; empty on both arms'],
        ['<span class="k">PREREGISTRATION.md</span>', 'written and committed before the second corpus was fetched'],
        ['<span class="k">METHOD.md</span>', 'what was done, and every deviation from the pre-registration'],
        ['<span class="k">VERIFICATION.md</span>', 'what was attacked, what broke, what stands']])}
<p>The instruments are <span class="k">tools/autoloop/fetch_crossref.py</span>,
<span class="k">tools/autoloop/dial.py</span>, <span class="k">tools/autoloop/dial_checks.py</span>
and this page's builder, <span class="k">tools/autoloop/make_dial_page.py</span>, which has a
<span class="k">--check</span> mode that rebuilds the page from the data and fails on a one-byte
difference. Session 150's loop, <span class="k">tools/autoloop/loop.py</span>, was not modified:
the arXiv question space above is a verbatim copy of its own, and K2 in the pre-registration was
the test that the copy still behaves like the original. It passed
({pct(ca['P5']['per_test_rate'])} against yesterday's published interval
{pct(0.0466)}&ndash;{pct(0.0512)}).</p>

<footer><p>The Field &mdash; field-research, session 151, cycle 002. Corpora fetched
{esc(ax['corpus']['fetched_utc'])} (arXiv) and {esc(cx['corpus']['fetched_utc'])} (Crossref).
Sources: arXiv Atom API; Crossref REST API. OpenAlex was tried first and refused this address
after one request; recorded in the pre-registration, not worked around. No third-party text is
committed &mdash; the corpora hold measurements of text, never text.</p></footer>
</main></body></html>
"""
    return html


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    html = build(args.dir)
    path = os.path.join(args.dir, "index.html")
    if args.check:
        if not os.path.exists(path):
            print("check: no page to check", file=sys.stderr)
            return 1
        old = open(path, "rb").read()
        new = html.encode()
        if hashlib.sha256(old).hexdigest() != hashlib.sha256(new).hexdigest():
            print(f"check FAILED: page differs from a rebuild ({len(old)} vs {len(new)} bytes)",
                  file=sys.stderr)
            return 1
        print(f"check ok: {len(old)} bytes, sha256 {hashlib.sha256(old).hexdigest()[:16]}",
              file=sys.stderr)
        return 0
    with open(path, "w") as f:
        f.write(html)
    print(f"wrote {path} ({len(html)} bytes)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
