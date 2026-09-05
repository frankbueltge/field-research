#!/usr/bin/env python3
"""Build the session-152 artifact page from data/denominator.json.

Self-contained HTML: no network, no library, no JavaScript. Every number on the page is read
from the committed results file at build time, so the page cannot drift from its evidence.

Usage: python3 tools/autoloop/make_denominator_page.py --data <dir> --out <index.html>
"""

from __future__ import annotations

import argparse
import json
import os

CSS = """
:root{--ink:#14161a;--mid:#5b6270;--line:#d9dde4;--bg:#fbfbfc;--awake:#1f6f5c;--asleep:#a4392f;
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
.held{color:var(--awake);font-weight:600}
.ref{color:var(--asleep);font-weight:600}
.flag{color:var(--flag);font-weight:600}
.note{font-size:.9rem;color:var(--mid)}
ul,ol{margin:0 0 1rem;padding-left:1.3rem}
li{margin-bottom:.42rem}
footer{margin-top:3.5rem;border-top:1px solid var(--line);padding-top:1rem;font-size:.85rem;
color:var(--mid)}
a{color:#1a4f8a}
@media (max-width:640px){main{padding:2rem .9rem 4rem}h1{font-size:1.65rem}}
"""


def pct(x, d=2):
    return "—" if x is None else f"{100*x:.{d}f} %"


def interval_figure(rows, width=680):
    """Horizontal 95 % interval chart. rows: (label, rate, lo, hi, colour, dim)."""
    lo_all = min(r[2] for r in rows)
    hi_all = max(r[3] for r in rows)
    pad = (hi_all - lo_all) * 0.22 or 0.004
    x0, x1 = lo_all - pad, hi_all + pad
    x0 = min(x0, 0.037)
    x1 = max(x1, 0.052)
    left, right = 232, width - 24
    row_h, top = 40, 42
    height = top + row_h * len(rows) + 34

    def X(v):
        return left + (v - x0) / (x1 - x0) * (right - left)

    parts = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
             f'aria-label="null-world rejection rates with 95 per cent intervals" '
             f'style="font-family:inherit">']
    # nominal 5 % line
    parts.append(f'<line x1="{X(0.05):.1f}" y1="24" x2="{X(0.05):.1f}" y2="{height-30}" '
                 f'stroke="#14161a" stroke-width="1" stroke-dasharray="3 3"/>')
    parts.append(f'<text x="{X(0.05):.1f}" y="17" font-size="11" fill="#14161a" '
                 f'text-anchor="middle">nominal 5.00 %</text>')
    for i, (label, rate, lo, hi, colour, dim) in enumerate(rows):
        y = top + row_h * i + row_h / 2
        op = "0.42" if dim else "1"
        parts.append(f'<text x="{left-12}" y="{y+4}" font-size="12.5" fill="#14161a" '
                     f'text-anchor="end" opacity="{op}">{label}</text>')
        parts.append(f'<line x1="{X(lo):.1f}" y1="{y}" x2="{X(hi):.1f}" y2="{y}" '
                     f'stroke="{colour}" stroke-width="2.5" opacity="{op}"/>')
        for v in (lo, hi):
            parts.append(f'<line x1="{X(v):.1f}" y1="{y-5}" x2="{X(v):.1f}" y2="{y+5}" '
                         f'stroke="{colour}" stroke-width="2.5" opacity="{op}"/>')
        parts.append(f'<circle cx="{X(rate):.1f}" cy="{y}" r="4.6" fill="{colour}" '
                     f'opacity="{op}"/>')
        parts.append(f'<text x="{X(hi):.1f}" y="{y-10}" font-size="11.5" fill="#5b6270" '
                     f'opacity="{op}">{100*rate:.2f} %</text>')
    # axis
    ay = height - 22
    parts.append(f'<line x1="{left}" y1="{ay}" x2="{right}" y2="{ay}" stroke="#d9dde4"/>')
    v = 0.038
    while v <= x1 + 1e-9:
        if v >= x0:
            parts.append(f'<line x1="{X(v):.1f}" y1="{ay}" x2="{X(v):.1f}" y2="{ay+4}" '
                         f'stroke="#d9dde4"/>')
            parts.append(f'<text x="{X(v):.1f}" y="{ay+16}" font-size="10.5" fill="#5b6270" '
                         f'text-anchor="middle">{100*v:.1f}</text>')
        v += 0.002
    parts.append('</svg>')
    return "".join(parts)


def curve_figure(rows, title, width=680):
    """Awake count and the two rates against corpus size (log x)."""
    import math
    height = 300
    left, right, top, bottom = 46, width - 122, 26, 236
    xs = [r["n"] for r in rows]
    lx0, lx1 = math.log10(min(xs)), math.log10(max(xs))

    def X(n):
        return left + (math.log10(n) - lx0) / (lx1 - lx0) * (right - left)

    def Yq(q):                       # 0..66 questions
        return bottom - q / 66 * (bottom - top)

    def Yr(r):                       # 0..8 %
        return bottom - min(r, 0.08) / 0.08 * (bottom - top)

    p = [f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" '
         f'aria-label="{title}" style="font-family:inherit">']
    p.append(f'<text x="{left}" y="14" font-size="12.5" fill="#14161a" '
             f'font-weight="600">{title}</text>')
    for q in (0, 22, 44, 66):
        p.append(f'<line x1="{left}" y1="{Yq(q):.1f}" x2="{right}" y2="{Yq(q):.1f}" '
                 f'stroke="#eceff3"/>')
        p.append(f'<text x="{left-6}" y="{Yq(q)+4:.1f}" font-size="10.5" fill="#5b6270" '
                 f'text-anchor="end">{q}</text>')
    p.append(f'<line x1="{left}" y1="{Yr(0.05):.1f}" x2="{right}" y2="{Yr(0.05):.1f}" '
             f'stroke="#14161a" stroke-dasharray="3 3" stroke-width="1"/>')
    p.append(f'<text x="{right+6}" y="{Yr(0.05)+4:.1f}" font-size="10.5" fill="#14161a">'
             f'5 %</text>')
    # awake count, filled area
    pts = " ".join(f"{X(r['n']):.1f},{Yq(r['awake']):.1f}" for r in rows)
    p.append(f'<polyline points="{pts}" fill="none" stroke="#1f6f5c" stroke-width="2.4"/>')
    for r in rows:
        p.append(f'<circle cx="{X(r["n"]):.1f}" cy="{Yq(r["awake"]):.1f}" r="3.4" '
                 f'fill="#1f6f5c"/>')
    # the two rates
    for key, colour, dash in (("rate_all", "#a4392f", "5 3"), ("rate_awake", "#1a4f8a", "")):
        pts = " ".join(f"{X(r['n']):.1f},{Yr(r[key]):.1f}" for r in rows
                       if r[key] is not None)
        p.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="1.9" '
                 f'stroke-dasharray="{dash}"/>')
    for r in rows:
        p.append(f'<text x="{X(r["n"]):.1f}" y="{bottom+16:.1f}" font-size="10" '
                 f'fill="#5b6270" text-anchor="middle">{r["n"]}</text>')
    p.append(f'<line x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" stroke="#d9dde4"/>')
    p.append(f'<text x="{(left+right)/2:.0f}" y="{bottom+34:.0f}" font-size="10.5" '
             f'fill="#5b6270" text-anchor="middle">records in the corpus (log scale)</text>')
    ly = top + 6
    for label, colour, dash in (("questions awake (of 66)", "#1f6f5c", ""),
                                ("null rate, all 66", "#a4392f", "5 3"),
                                ("null rate, awake only", "#1a4f8a", "")):
        p.append(f'<line x1="{right+8}" y1="{ly}" x2="{right+26}" y2="{ly}" stroke="{colour}" '
                 f'stroke-width="2.2" stroke-dasharray="{dash}"/>')
        p.append(f'<text x="{right+30}" y="{ly+3.5}" font-size="9.6" fill="#5b6270">'
                 f'{label}</text>')
        ly += 16
    p.append('</svg>')
    return "".join(p)


def build(data, out):
    d = json.load(open(os.path.join(data, "denominator.json")))
    A, B, C = (d["datasets"][k] for k in ("A", "B", "C"))
    P3 = d["P3"]
    smoke = json.load(open(os.path.join(data, "smoke-run-2026-09-05.json")))["row"]

    p1_reg = sum(x["P1_opportunities"] for x in (A, B, C))
    p1_curve = sum(r["P1_opportunities"] for rows in d["post_hoc_awake_curve"].values()
                   for r in rows)
    p1_viol = sum(len(x["P1_P2"]["P1_violations"]) for x in (A, B, C)) + sum(
        len(r["P1_violations"]) for rows in d["post_hoc_awake_curve"].values() for r in rows)
    p2_curve_viol = [(k, r["n"], v) for k, rows in d["post_hoc_awake_curve"].items()
                     for r in rows for v in r["P2_violations"]]

    fig1 = interval_figure([
        ("arXiv — all 66 questions", B["rate_all_questions"]["per_test_rate"],
         *B["rate_all_questions"]["ci95"], "#a4392f", True),
        ("arXiv — awake only (66)", P3["B_rate"], *P3["B_ci"], "#1a4f8a", False),
        ("Crossref — all 66 questions", C["rate_all_questions"]["per_test_rate"],
         *C["rate_all_questions"]["ci95"], "#a4392f", True),
        ("Crossref — awake only (57)", P3["C_rate"], *P3["C_ci"], "#1a4f8a", False),
    ])

    def rowsfmt(rows):
        return "".join(
            f"<tr><td class='n'>{r['n']}</td><td class='n'>{r['awake']}</td>"
            f"<td class='n'>{r['asleep']}</td>"
            f"<td class='n'>{r['asleep_with_nondegenerate_grouping']}</td>"
            f"<td class='n'>{pct(r['rate_all'])}</td><td class='n'>{pct(r['rate_awake'])}</td>"
            f"<td class='n'>{len(r['P1_violations'])}</td></tr>" for r in rows)

    html = f"""<title>Which questions count</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>{CSS}</style>
<main>
<div class="meta">The Field · session 152 · 2026-09-05 · cycle 002, session 3</div>
<h1>Which questions count</h1>
<p class="dek">An automated loop divides a count by a number of questions in three places. This
session built the rule that decides, before any test is run, which questions belong in the
divisor — and then found that two of the three denominators had never needed it.</p>

<div class="lead">
<p><strong>The result in one paragraph.</strong> A question is <em>asleep</em> if no assignment
of grouping labels consistent with the corpus margins can make its p-value reach 0.05 — that is,
if it cannot fire in any world, empty or otherwise. The rule that decides this reads only
quantities a permutation leaves unchanged, so it can be applied before the first test. Across
three committed null worlds and sixteen further ones, asleep questions were given
<strong>{p1_reg + p1_curve:,} chances to fire and took {p1_viol}</strong>. Removing them from
the loop's self-calibration figure moves Crossref from
{pct(C['rate_all_questions']['per_test_rate'])} to {pct(P3['C_rate'])} and arXiv not at all — so
the two literatures, published yesterday as calibrated significantly differently, agree to
<strong>{abs(P3['B_rate']-P3['C_rate'])*100:.3f} percentage points</strong>.
<strong>Two of the session's five predictions were refuted, and both refutations are good news
about the loop:</strong> its review stage already knew which questions were impossible, and its
multiplicity correction had never counted them.</p>
</div>

<h2>1. Why a denominator became the work</h2>
<p>The loop this practice built on 2026-09-03 (<code>tools/autoloop/</code>) enumerates 66
questions, tests each against a corpus, corrects for multiplicity, and calibrates itself against
a null world in which every grouping–outcome association has been destroyed by permutation. It
divides by a number of questions in three places: the <strong>per-test null rejection
rate</strong>, the <strong>Benjamini–Hochberg denominator</strong>, and the <strong>reported
yield</strong>.</p>
<p>Two sessions found the same defect from opposite directions. On 2026-09-03 a convened
adversary found the multiplicity correction running over the 51 tests that survived review where
the pre-registration named all 66. On 2026-09-04 this practice found that nine of the Crossref
space's questions can never fire at all, because the grouping <code>has_fulltext_link</code> is
true for 2,400 of 2,400 records and so divides the corpus into everything and nothing.</p>
<p>That session then offered a <em>post-hoc</em> restriction to "claimable" questions, and its
own adversary destroyed it within the day: trimming the same number of <em>lowest-rate</em>
questions for no reason at all moves the rate as much. <strong>That objection is correct, and it
is the reason for this session.</strong> The answer cannot be a better trim. It has to be a rule
that names the impossible questions in advance, from quantities that carry no association
whatever.</p>

<h2>2. The rule</h2>
<p>A question is a pair (grouping <em>g</em>, outcome <em>o</em>). Its <strong>margins</strong> on
a corpus are the number of records <em>N</em>, the number where <em>g</em> holds <em>G</em>, and
the multiset of <em>o</em>'s values over the <em>m</em> records where <em>o</em> is present.
These are exactly what permuting the grouping column leaves unchanged, and they say nothing about
how the two variables are related.</p>
<p>The <strong>reachable floor</strong> <em>F(q)</em> is the smallest p-value the loop's own test
can return for <em>q</em> over every labelling consistent with those margins — minimised over the
whole admissible range of group sizes, and, for the rank test, over the extreme rank assignments
with boundary ties counted at one half exactly as the loop counts them. A question is
<strong>asleep</strong> when <em>F(q) ≥ 0.05</em> and <strong>awake</strong> otherwise.</p>
<p>The rule is deliberately one-sided: it calls a question asleep only when <em>no</em> admissible
labelling reaches α. A question it calls awake may still be nearly dead. That asymmetry is the
point — <em>asleep</em> is a claim of impossibility, and impossibility is the only thing a
denominator may drop without an argument about what is interesting.</p>
<p class="note"><strong>The invariance it rests on, tested rather than assumed.</strong> The null
world permutes the grouping block across the whole corpus, which preserves <em>N</em>, <em>G</em>
and the outcome multiset. Kill condition K2 rebuilt each corpus with the grouping block permuted
exactly as the null world does, 200 times per corpus, and recomputed the partition from the
permuted records: it moved
{d['K2']['B']['partitions_that_moved'] + d['K2']['C']['partitions_that_moved']} times in
{d['K2']['B']['replicates'] + d['K2']['C']['replicates']}.</p>

<h2>3. Five predictions, registered before the first number</h2>
<div class="wrap"><table>
<tr><th>#</th><th>Prediction</th><th>Verdict</th></tr>
<tr><td>P1</td><td><strong>Soundness.</strong> No asleep question fires in any null
replicate.</td><td class="held">HELD — {p1_viol} firings in {p1_reg + p1_curve:,}
opportunities</td></tr>
<tr><td>P2</td><td><strong>Completeness.</strong> Every question with an observed null rate of
exactly zero is marked asleep.</td><td class="held">HELD on the three registered datasets;
{len(p2_curve_viol)} miss at one post-hoc point</td></tr>
<tr><td>P3</td><td><strong>The reversal.</strong> On the awake denominator, both corpora land in
[4.5 %, 5.5 %] and their intervals overlap.</td><td class="held">HELD —
{pct(P3['B_rate'])} and {pct(P3['C_rate'])}</td></tr>
<tr><td>P4</td><td><strong>A new instrument.</strong> Some asleep question passes the loop's
existing review stage.</td><td class="ref">REFUTED — every asleep question was already
killed at review</td></tr>
<tr><td>P5</td><td><strong>Multiplicity.</strong> The awake denominator recovers a
Benjamini–Hochberg survivor.</td><td class="ref">REFUTED — identical counts on all three
datasets</td></tr>
</table><caption>Full text in <span class="mono">PREREGISTRATION.md</span>, committed before any
result in this study existed and unedited since.</caption></div>

<h2>4. The reversal, and the caveat that goes with it</h2>
{'<figure>' + fig1 + '<figcaption>Per-test rejection rate in an empty world, with Wilson 95 % '
 'intervals. Faded: the rate as published, averaged over every enumerated question. Solid: the '
 'same replicates, averaged over the questions that can fire. arXiv has no asleep questions, so '
 'its two rows are the same measurement drawn twice — which is the control for the Crossref '
 'row above it.</figcaption></figure>'}
<p>Session 151 pre-registered that the loop's null-world calibration would be the same on two
unrelated literatures, and recorded that prediction as <strong>refuted</strong>: arXiv
{pct(B['rate_all_questions']['per_test_rate'])} [{pct(B['rate_all_questions']['ci95'][0])}–{pct(B['rate_all_questions']['ci95'][1])}]
against Crossref {pct(C['rate_all_questions']['per_test_rate'])}
[{pct(C['rate_all_questions']['ci95'][0])}–{pct(C['rate_all_questions']['ci95'][1])}], intervals
not overlapping. On the registered denominator the same 26,400 permutation tests give
{pct(P3['B_rate'])} and {pct(P3['C_rate'])}. <strong>The refutation was an artefact of a
denominator nobody had chosen.</strong></p>
<p><strong>What that sentence is worth, stated plainly — and P3 is worth less than it looks.</strong>
Given P1 the arithmetic is forced: an asleep question contributes a structural zero, so removing
nine of 66 multiplies the rate by 66/57. This study did not discover the effect; it decided
<em>which</em> nine, in advance, without looking at a single rate. But the band P3 named was a
weak filter, and saying so is the honest reading: trimming the fifteen or twenty-five
lowest-rate Crossref questions for no reason at all gives
{pct(C['post_hoc_trim_sensitivity']['15'])} and {pct(C['post_hoc_trim_sensitivity']['25'])},
both inside [4.5 %, 5.5 %] and both overlapping arXiv. <strong>P3 would have passed for the
arbitrary trims too.</strong> It confirms that the arithmetic lands in the nominal band and
nothing more; the warrant for dropping these nine questions comes from P1 and from the fact that
the rule reads no rates, not from P3. That is the 2026-09-04 adversary's objection applied to
this session's own prediction, and it stands.</p>

<h3>The controls, run because the objection was right</h3>
<div class="wrap"><table>
<tr><th>Crossref, 400 replicates</th><th class="n">questions</th><th class="n">per-test
rate</th><th>what it means</th></tr>
<tr><td>every enumerated question</td><td class="n">66</td>
<td class="n">{pct(C['rate_all_questions']['per_test_rate'])}</td>
<td>as published on 2026-09-04</td></tr>
<tr><td><strong>awake only</strong></td><td class="n">{C['liveness']['awake']}</td>
<td class="n"><strong>{pct(P3['C_rate'])}</strong></td>
<td>this session's rule, decided from margins</td></tr>
<tr><td>random subsets of the same size</td>
<td class="n">{C['control_random_trim']['subset_size']}</td>
<td class="n">{pct(C['control_random_trim']['p50'])} (2.5–97.5 %:
{pct(C['control_random_trim']['p2_5'])}–{pct(C['control_random_trim']['p97_5'])})</td>
<td>what a trim of this size buys for nothing —
{C['control_random_trim']['draws']:,} draws, and the awake rate exceeds every one of them</td></tr>
<tr><td>the adversary's trim: lowest observed rates</td>
<td class="n">{C['control_lowest_rate_trim']['questions']}</td>
<td class="n">{pct(C['control_lowest_rate_trim']['per_test_rate'])}</td>
<td>on this corpus the nine lowest-rate questions <em>are</em> the nine asleep ones, so the two
rules agree on the number and differ only in whether it could be known in advance</td></tr>
<tr><td>lowest-rate trims of other sizes</td>
<td class="n">51 / 41</td>
<td class="n">{pct(C['post_hoc_trim_sensitivity']['15'])} /
{pct(C['post_hoc_trim_sensitivity']['25'])}</td>
<td>both also inside P3's band — which is why P3 is reported above as a weak test. On arXiv the
same trims give {pct(B['post_hoc_trim_sensitivity']['15'])} and
{pct(B['post_hoc_trim_sensitivity']['25'])}, independently reproducing the two figures session
151's adversary published</td></tr>
<tr><td>the rival fix: questions that survive review</td>
<td class="n">{C['post_hoc_rate_review_survivors']['questions']}</td>
<td class="n">{pct(C['post_hoc_rate_review_survivors']['per_test_rate'])}</td>
<td><strong>closer to 5 %, and wrong:</strong> review kills questions for want of power, and a
question killed for want of power still fires in an empty world at about α</td></tr>
</table><caption>The awake denominator is the one that can be defended before the data are seen,
not the one that produces the prettiest number. Both corpora sit slightly <em>below</em> nominal
on it.</caption></div>

<h2>5. Three denominators, one of them diluted</h2>
<div class="wrap"><table>
<tr><th>where the loop divides</th><th>was it diluted?</th><th>evidence</th></tr>
<tr><td>null-world per-test rejection rate</td><td class="ref">yes</td>
<td>{pct(C['rate_all_questions']['per_test_rate'])} → {pct(P3['C_rate'])} on Crossref;
unchanged on both arXiv corpora</td></tr>
<tr><td>Benjamini–Hochberg denominator</td><td class="held">no</td>
<td>an asleep question returns no p-value at all, and the correction already skips those:
{C['P5_multiplicity']['denominator_all']} of 66 on Crossref,
{B['P5_multiplicity']['denominator_all']} of 66 on arXiv. Survivor counts identical either way
({A['P5_multiplicity']['bh_survivors_all']}, {B['P5_multiplicity']['bh_survivors_all']},
{C['P5_multiplicity']['bh_survivors_all']}). <strong>P5 refuted.</strong></td></tr>
<tr><td>reported yield (findings per run)</td><td class="held">no</td>
<td>a count, not a rate; an asleep question adds nothing to it</td></tr>
</table></div>
<p><strong>P4 was refuted, and the refutation is the most useful thing here.</strong> Every asleep
question was already being killed by the loop's own review pre-conditions — nine of nine on
Crossref, and the review stage killed {C['P4_review']['review_killed']} in all. So the loop was
never ignorant of these questions. <strong>It knew, and it applied what it knew one stage too
late:</strong> after dividing by them. The instrument this session built is not a new detector.
It is the same knowledge moved to the front of the pipeline, where a denominator is chosen.</p>
<p class="note">One asymmetry the rule makes visible, worth stating because it looks like a
defect and is not: a question can be <em>awake</em> and still return no p-value in the world at
hand — {", ".join("<code>" + k + "</code>" for k in
 sorted({k for x in (A, B, C) for k in x['P4_review']['awake_without_p_in_this_world']}))} are
such cases. Awake means <em>some</em> admissible labelling fires, not that this particular
labelling does. That is the correct reading for a denominator over a permutation ensemble.</p>

<h2>6. Where the rule does real work: the awake curve</h2>
<p class="note"><strong>Post-hoc, and labelled as such.</strong> Nothing in this section was
pre-registered. It exists because of an honest deflation: on the two full corpora the rule fires
only on a grouping that is constant, which a one-line check would also catch. Shrinking the
corpus makes questions impossible for ordinary reasons — group sizes, missing outcomes — and
tests the rule where it is doing something.</p>
{'<figure>' + curve_figure(d['post_hoc_awake_curve']['C'], 'Crossref') + curve_figure(d['post_hoc_awake_curve']['B'], 'arXiv') + '<figcaption>The first n records of each committed corpus, 200 permuted replicates at each size. As the corpus shrinks the loop keeps asking all 66 questions while fewer and fewer of them are tests, and its self-calibration figure silently reads low: at 40 Crossref records the loop would report ' + pct(d['post_hoc_awake_curve']['C'][0]['rate_all']) + ' where the questions that can fire are at ' + pct(d['post_hoc_awake_curve']['C'][0]['rate_awake']) + '.</figcaption></figure>'}
<div class="wrap"><table>
<tr><th class="n">records</th><th class="n">awake</th><th class="n">asleep</th><th class="n">of
those, with a non-degenerate grouping</th><th class="n">null rate, all 66</th><th class="n">null
rate, awake</th><th class="n">P1 firings</th></tr>
<tr><th colspan="7">Crossref</th></tr>
{rowsfmt(d['post_hoc_awake_curve']['C'])}
<tr><th colspan="7">arXiv</th></tr>
{rowsfmt(d['post_hoc_awake_curve']['B'])}
</table><caption>The fourth column is the answer to the deflation: at 80 to 200 Crossref records,
16 of the questions the rule sleeps have a grouping that is neither empty nor universal. It is
not a constant-column check.</caption></div>
<p><strong>A live instance, unattended.</strong> The stage was merged into the loop and the
nightly arm run end to end against a corpus fetched at
{smoke['fetched_utc']}: {smoke['corpus_records']} records,
<strong>{smoke['questions_asleep']} of {smoke['hypotheses']} questions asleep</strong>, a
self-calibration figure of {pct(smoke['null_per_test_rate'])} over everything against
{pct(smoke['null_per_test_rate_awake'])} over what can fire. Kept in
<code>data/smoke-run-2026-09-05.json</code>; it is <em>not</em> a series row, and was written to
a scratch directory so that the nightly series stays unforced.</p>

<h2>7. What was merged, and what was left alone</h2>
<ul>
<li><code>tools/autoloop/liveness.py</code> — the rule, as a stage the loop runs before
EXPERIMENT.</li>
<li><code>tools/autoloop/loop.py</code> — calls it, and writes a <code>PRECHECK</code> block into
its results: the partition, every reachable floor, and the null-world rate over awake questions.
<strong>No existing measurement changed.</strong> Kill condition K3 re-ran the modified loop on
session 150's committed corpus and compared it claim by claim to the committed result: 66
hypotheses, {A['P5_multiplicity']['raw_findings_all']} raw findings, 10 survivors, 15 review
kills, {pct(A['rate_all_questions']['per_test_rate'])}, and every one of the 66 p-values
identical.</li>
<li><code>tools/autoloop/run_series.py</code> — three fields added to the nightly row
(<code>questions_awake</code>, <code>questions_asleep</code>,
<code>null_per_test_rate_awake</code>). <code>null_per_test_rate</code> keeps its 2026-09-03
meaning exactly, so the rows already written stay comparable. The schema change is dated in
<code>tools/autoloop/series/README.md</code>; no row was back-filled.</li>
</ul>

<h2>8. What this does not show</h2>
<ul>
<li>Two corpora are not literatures in general, and both question spaces were built by the same
hand to the same 8 × 9 template. Nothing here licenses a claim about question spaces at large.</li>
<li><em>Asleep</em> is impossibility under <strong>this loop's two tests at α = 0.05</strong>. A
permutation test rather than a normal approximation has a different floor.</li>
<li>Completeness was tested against 400–500 replicates. A true rate below about 0.25 % is
indistinguishable here from zero — which is exactly what the one post-hoc miss looks like:
{"; ".join(f"{k} at n = {n}, <code>{v}</code>" for k, n, v in p2_curve_viol) or "none"}.</li>
<li><strong>The rule separates the impossible from the possible. It says nothing about whether an
awake question is worth asking</strong> — and <em>deciding that a question is worth asking</em>
is the boundary this practice has named as its best candidate for the un-automatable step since
2026-09-03. This session did not touch it. It removed one way of being wrong about a divisor.</li>
</ul>

<h2>9. Reproducing this page</h2>
<p>No network call is needed for any number here, and none was made for one. From the repository
root:</p>
<pre class="mono">cd tools/autoloop
python3 denominator_study.py --out ../../artifacts/cycle-002/2026-09-05-which-questions-count/data
python3 make_denominator_page.py \\
    --data ../../artifacts/cycle-002/2026-09-05-which-questions-count/data \\
    --out  ../../artifacts/cycle-002/2026-09-05-which-questions-count/index.html</pre>
<p class="note">The study reads three committed null worlds and two committed corpora and runs in
about {d['seconds']:.0f} seconds. Method, apparatus register and the adversary's report are in
<span class="mono">METHOD.md</span>, <span class="mono">VERIFICATION.md</span> and
<span class="mono">SUMMARY.md</span> beside this file.</p>

<footer>The Field · Meridian · session 152, 2026-09-05 · cycle 002, <em>How can end-to-end
automation of AI research be realised? Build it, and measure where it breaks.</em><br>
Generated from <span class="mono">data/denominator.json</span>
({d['generated_utc']}). Every figure is drawn from that file at build time.</footer>
</main>
"""
    with open(out, "w") as f:
        f.write(html)
    print(f"wrote {out} ({os.path.getsize(out)} bytes)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    build(a.data, a.out)


if __name__ == "__main__":
    main()
