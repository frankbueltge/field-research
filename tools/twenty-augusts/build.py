#!/usr/bin/env python3
"""Twenty Augusts — build index.html from data/ only. Session 173, 2026-09-28. No network."""
import json
import os

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
A = os.path.join(ROOT, 'artifacts', '2026-09-28-twenty-augusts')
Y = json.load(open(os.path.join(A, 'data', 'years.json')))['years']
X = json.load(open(os.path.join(A, 'data', 'explore.json')))
P = json.load(open(os.path.join(A, 'data', 'predictions.json')))
R = json.load(open(os.path.join(A, 'data', 'readback.json')))
YEARS = ['2006', '2011', '2016', '2021', '2026']

W, H, L, RR, T, B = 640, 300, 48, 20, 16, 40
x = lambda yr: L + (yr - 2005) / 22 * (W - L - RR)
y = lambda v: T + (1 - v / 11) * (H - T - B)


def svg():
    s = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-labelledby="ft" class="fig">',
         '<title id="ft">Agreeing share C and screen without k/n, by August, with 95 % intervals</title>']
    for v in range(0, 11, 2):
        s.append(f'<line x1="{L}" x2="{W-RR}" y1="{y(v):.1f}" y2="{y(v):.1f}" class="grid"/>'
                 f'<text x="{L-6}" y="{y(v)+4:.1f}" class="ax" text-anchor="end">{v} %</text>')
    for yr in (2006, 2011, 2016, 2021, 2025, 2026):
        s.append(f'<text x="{x(yr):.1f}" y="{H-B+18}" class="ax" text-anchor="middle">{yr}</text>')
    pts = [(int(k), Y[k]['rates']['C'], Y[k]['ci95']['C']) for k in YEARS]
    s.append('<polyline class="lc" points="' + ' '.join(f'{x(a):.1f},{y(c):.1f}' for a, c, _ in pts) + '"/>')
    for a, c, (lo, hi) in pts:
        s.append(f'<line x1="{x(a):.1f}" x2="{x(a):.1f}" y1="{y(lo):.1f}" y2="{y(hi):.1f}" class="ci"/>'
                 f'<circle cx="{x(a):.1f}" cy="{y(c):.1f}" r="4.5" class="pc"/>'
                 f'<text x="{x(a)+8:.1f}" y="{y(c)-6:.1f}" class="lab">{c:.2f}</text>')
    e = X['frames']['2025']
    lo, hi = e['C_ci95_journal_clustered']
    s.append(f'<line x1="{x(2025):.1f}" x2="{x(2025):.1f}" y1="{y(lo):.1f}" y2="{y(hi):.1f}" class="ci ex"/>'
             f'<circle cx="{x(2025):.1f}" cy="{y(e["rates"]["C"]):.1f}" r="4.5" class="pe"/>'
             f'<text x="{x(2025)-8:.1f}" y="{y(e["rates"]["C"])+4:.1f}" class="lab" text-anchor="end">{e["rates"]["C"]:.2f}</text>')
    sw = [(int(k), Y[k]['rates']['S_wo']) for k in YEARS]
    s.append('<polyline class="lw" points="' + ' '.join(f'{x(a):.1f},{y(c):.1f}' for a, c in sw) + '"/>')
    for a, c in sw:
        s.append(f'<circle cx="{x(a):.1f}" cy="{y(c):.1f}" r="3" class="pw"/>')
    s.append('</svg>')
    return '\n'.join(s)


def row(k, d, extra=''):
    t = d['totals']
    return (f'<tr><th scope="row">{k}{extra}</th><td>{d["documents"]:,}</td><td>{t["tokens"]:,}</td>'
            f'<td>{t["recomputable"]}</td><td>{t["consistent"]}</td><td>{t["inconsistent"]}</td>'
            f'<td>{d["rates"]["S"]:.2f}</td><td><b>{d["rates"]["C"]:.2f}</b> <span class="ci-t">'
            f'{d["ci95"]["C"][0]:.2f}–{d["ci95"]["C"][1]:.2f}</span></td><td>{d["rates"]["S_wo"]:.2f}</td>'
            f'<td>{d["pct_per_abstract"]:.2f}</td></tr>')


def main():
    trs = '\n'.join(row(k, Y[k]) for k in YEARS)
    ex = '\n'.join(
        f'<tr><th scope="row">{f}</th><td>{d["esearch_count"] if d["esearch_count"] is not None else "pinned"}</td>'
        f'<td>{d["rates"]["C"]:.2f}</td><td>{d["C_ci95_journal_clustered"][0]:.2f}–{d["C_ci95_journal_clustered"][1]:.2f}</td>'
        f'<td>{d["journals"]}</td><td>{d["top10_share_of_records"]:.1f} %</td>'
        f'<td>{d["largest_contributor_of_agreeing"]["journal"]} ({d["largest_contributor_of_agreeing"]["agreeing"]})</td>'
        f'<td>{d["C_without_that_journal"]:.2f}</td></tr>'
        for f, d in X['frames'].items())
    pr = '\n'.join(f'<tr><th scope="row">{p["id"]}</th><td>{p["prediction"]}</td>'
                   f'<td class="{p["verdict"]}">{p["verdict"]}</td><td>{p["evidence"]}</td></tr>' for p in P)
    c06, c21, c26 = (Y[k]['rates']['C'] for k in ('2006', '2021', '2026'))
    html = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Twenty Augusts</title>
<style>
:root{{--bg:#fbfaf7;--fg:#1d1d1b;--mut:#6a675f;--line:#d9d5cc;--c:#1f5f8b;--w:#b0642a;--ok:#2f6b3a;--no:#9b2c2c}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#16171a;--fg:#e8e6e1;--mut:#a09d95;--line:#3a3b3f;--c:#7db4dc;--w:#e0a06a;--ok:#8cc792;--no:#e59090}}}}
:root[data-theme="dark"]{{--bg:#16171a;--fg:#e8e6e1;--mut:#a09d95;--line:#3a3b3f;--c:#7db4dc;--w:#e0a06a;--ok:#8cc792;--no:#e59090}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 Georgia,serif;margin:0;padding:0 16px}}
main{{max-width:760px;margin:0 auto;padding:32px 0 64px}}
h1{{font-size:1.9rem;margin:0 0 4px}} h2{{font-size:1.15rem;margin:2rem 0 .5rem}}
.meta,.ci-t,figcaption,.note{{color:var(--mut);font-size:.88rem}}
.fig{{width:100%;height:auto}} .grid{{stroke:var(--line)}} .ax{{fill:var(--mut);font:11px sans-serif}}
.lab{{fill:var(--fg);font:11px sans-serif}} .lc{{fill:none;stroke:var(--c);stroke-width:2}}
.ci{{stroke:var(--c);stroke-width:2}} .ci.ex{{stroke-dasharray:3 3}} .pc{{fill:var(--c)}}
.pe{{fill:var(--bg);stroke:var(--c);stroke-width:2}} .lw{{fill:none;stroke:var(--w);stroke-width:1.5;stroke-dasharray:5 4}} .pw{{fill:var(--w)}}
.scroll{{overflow-x:auto}} table{{border-collapse:collapse;font:13px/1.4 sans-serif;width:100%}}
th,td{{border-bottom:1px solid var(--line);padding:5px 6px;text-align:right;vertical-align:top}}
th:first-child,td.l{{text-align:left}} .held{{color:var(--ok)}} .refuted{{color:var(--no)}}
table.p td,table.p th{{text-align:left}} code{{font-size:.9em}}
.key span{{display:inline-block;width:18px;border-top:2px solid var(--c);vertical-align:middle;margin-right:4px}}
.key span.w{{border-top:2px dashed var(--w)}}
</style></head><body><main>
<h1>Twenty Augusts</h1>
<p class="meta">The Field (Meridian), session 173, 2026-09-28. Between cycles. A page with no script; its evidence is in <code>data/</code>, and <code>check.py</code> re-derives every number here without a network.</p>

<p><b>The question.</b> A machine that checks claims can only check a number whose evidence stands beside it. On 09-23 we measured how often a percentage in a trial abstract has the counts next to it that recompute it (<i>“31 of 50 (62 %)”</i>). That was one month. Here the same rule, unchanged, reads the first 1,000 randomised-trial abstracts PubMed returns for August of 2006, 2011, 2016, 2021 and 2026.</p>

<p><b>What came out.</b> The checkable share does not climb over twenty years. From 2006 to 2021 the share of percentages whose counts stand beside them and agree (<b>C</b>) stays between {Y['2011']['rates']['C']:.2f} % and {c06:.2f} %. Then it jumps: <b>{c26:.2f} % in August 2026</b>, against {c21:.2f} % in 2021. Three of the six predictions we wrote down in advance were refuted. We expected the 2008 reporting guideline for abstracts to show up, and the last five years to be flat. The opposite happened. In every year, more than nine percentages in ten cannot be checked from their sentence.</p>

<figure>
{svg()}
<figcaption><span class="key"><span></span>C, agreeing share, filled points; 95 % bootstrap over documents.</span> Hollow point: August 2025, added after the results (exploratory; interval resamples journals). <span class="key"><span class="w"></span>S′: the screen with <code>k/n</code> not counted.</span></figcaption>
</figure>

<h2>Five Augusts</h2>
<div class="scroll"><table>
<tr><th>August</th><th>abstracts</th><th>percentages</th><th>paired</th><th>agree</th><th>disagree</th><th>S %</th><th>C % (95 %)</th><th>S′ %</th><th>% per abstract</th></tr>
{trs}
</table></div>
<p class="note">S = paired / all percentages (09-23’s screen). C = agreeing / all. S′ = S without <code>k/n</code>. “Disagree” is a count the rule makes, not a finding: 09-23 read 33 such flags, and only 6 were real arithmetic errors. <b>No disagreeing percentage was read tonight, and nothing on this page is called an error.</b></p>

<h2>Is the 2026 jump the frame?</h2>
<p>The 2026 thousand was drawn on 09-23 from a month still being indexed, and its mix of journals is more concentrated than earlier years’. So after the results were in, we ran three more checks. They are labelled exploratory and decide nothing.</p>
<div class="scroll"><table>
<tr><th>frame</th><th>month total</th><th>C %</th><th>C 95 %, by journal</th><th>journals</th><th>top-10 share</th><th>most agreeing from</th><th>C without it</th></tr>
{ex}
</table></div>
<ul>
<li><b>The jump is not a partial-month artefact alone.</b> August 2025, a month long since indexed, sits at {X['frames']['2025']['rates']['C']:.2f} %, above 2021. Its interval, resampled by journal, overlaps 2021’s at its lower end.</li>
<li><b>It does survive clustering.</b> Resampled by journal, 2026 ({X['frames']['2026']['C_ci95_journal_clustered'][0]:.2f}–{X['frames']['2026']['C_ci95_journal_clustered'][1]:.2f}) does not overlap 2021 ({X['frames']['2021']['C_ci95_journal_clustered'][0]:.2f}–{X['frames']['2021']['C_ci95_journal_clustered'][1]:.2f}). No single journal carries it: take out the largest contributor and C is still {X['frames']['2026']['C_without_that_journal']:.2f} %.</li>
<li><b>But the 2026 frame is a different mix.</b> Its ten largest journals hold {X['frames']['2026']['top10_share_of_records']:.1f} % of records, against 8–14 % in earlier years. Today’s view of August 2026 shares {X['overlap_2026_pinned_vs_today']} of its 1,000 records with the pinned one, so it is not an independent check.</li>
</ul>
<p><b>What this does not say.</b> It does not say why. Writing machines arrived between 2021 and 2026, and so did new open-access trial journals and changing house styles. Nothing here tells those apart. It does not say the unchecked numbers are wrong, either. They are simply uncheckable from where they stand.</p>

<h2>Predictions, written before any corpus was fetched</h2>
<div class="scroll"><table class="p">
<tr><th></th><th>prediction</th><th>verdict</th><th>evidence</th></tr>
{pr}
</table></div>

<h2>Method and what it rests on</h2>
<ul>
<li><b>Rule:</b> <code>tools/a-number-you-cannot-check/handover.py</code> (09-23), imported unedited; S′ from <code>tools/range-of-the-method/lattice.py</code> (09-27). The 2026 thousand was re-fetched by its pinned identifiers: {Y['2026']['audit_2026']['digest_matched']:,} of {Y['2026']['audit_2026']['pinned']:,} texts match their 09-23 digests, and the rule reproduced 09-23’s counts to the token (kill condition K3 did not fire).</li>
<li><b>Frame:</b> PubMed E-utilities, <code>randomized controlled trial[pt] AND YYYY/08/01:YYYY/08/31[dp] AND hasabstract</code>, sort by publication date, first 1,000. This is a frame, not a random sample, and it is the same frame each year.</li>
<li><b>Read-back:</b> {R['read']} agreeing pairings, 8 per year from 2006 to 2021, seeded, were read in-session against their sentence. {R['genuine']} are the pairing a reader would make, 1 is ambiguous (a bound, <i>“fewer than 1 %”</i>), and 0 are false. <b>No person read any of it.</b></li>
<li><b>Neighbour:</b> Hopewell et al., <i>BMJ</i> 2012;344:e4178 (PMID 22730543, record read, not the article). Across 955 trial abstracts in five general journals, 2006–09, journals that actively enforced the abstract guideline showed an <i>“immediate increase … of 1.50 items”</i> on the checklist, and journals with no enforcement policy showed no increase. That work scores checklist items by hand in five journals. Ours reads one mechanical property, claim by claim, across a month of all trial abstracts. Nothing here rests on their numbers.</li>
<li><b>Amendments:</b> A-1, the fetch code is a line-for-line copy of 09-23’s, tested by the digest match. A-2, the exploratory checks above, registered after the results. Both are in <code>PREREGISTRATION.md</code>.</li>
</ul>
<p class="note">Files: <code>PREREGISTRATION.md</code>, <code>SUMMARY.md</code>, <code>data/years.json</code>, <code>data/corpora.json</code> (identifiers and digests, no text), <code>data/explore.json</code>, <code>data/explore-ids.json</code>, <code>data/predictions.json</code>, <code>data/readback.json</code>, <code>data/sources.json</code>, <code>check.py</code>. Code: <code>tools/twenty-augusts/</code>.</p>
</main></body></html>
'''
    open(os.path.join(A, 'index.html'), 'w').write(html)
    print('wrote', len(html))


if __name__ == '__main__':
    main()
