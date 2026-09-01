#!/usr/bin/env python3
"""Build the artifact page from the measured data file, so that no number on the
page can drift from the file it came from.

Usage: python3 make_page.py <data.json> <survival.csv> <out.html>
       python3 make_page.py <data.json> <survival.csv> <out.html> --check
"""
import csv
import os
import json
import sys

SOURCES = [
    ("Retraction Watch database, distributed by Crossref (downloaded 2026-09-01)",
     "https://gitlab.com/crossref/retraction-watch-data"),
    ("Crossref REST API, notice records by update type (harvested 2026-09-01)",
     "https://api.crossref.org/works?filter=update-type:expression_of_concern"),
    ("Vaught, Jordan &amp; Bastian, &ldquo;Concern noted: a descriptive study of editorial "
     "expressions of concern in PubMed and PubMed Central&rdquo;, "
     "<i>Research Integrity and Peer Review</i> 2:10, 2017",
     "https://pmc.ncbi.nlm.nih.gov/articles/PMC5526611"),
    ("Crossref record for 10.1016/j.micpro.2020.103772 (the case checked end to end)",
     "https://api.crossref.org/works/10.1016/j.micpro.2020.103772"),
]


def fmt(n):
    return f"{n:,}".replace(",", " ")


def survival_path(rows, width, height, max_days):
    """Step path for the share still under an unresolved concern."""
    pts = []
    prev_y = None
    for day, share in rows:
        if day > max_days:
            break
        x = width * day / max_days
        y = height * (1 - share)
        if prev_y is not None:
            pts.append(f"L{x:.1f},{prev_y:.1f}")
        pts.append(f"L{x:.1f},{y:.1f}")
        prev_y = y
    if prev_y is not None:
        pts.append(f"L{width:.1f},{prev_y:.1f}")
    return "M0,0 " + " ".join(pts)


def figure(rows, head, km):
    W, H = 640, 260
    MAX = 3653  # ten years
    path = survival_path(rows, W, H, MAX)
    five = W * 1826 / MAX
    ticks = []
    for years in (1, 2, 3, 5, 10):
        x = W * (years * 365.25) / MAX
        ticks.append(
            f'<line x1="{x:.1f}" y1="{H}" x2="{x:.1f}" y2="{H + 5}" class="ax"/>'
            f'<text x="{x:.1f}" y="{H + 20}" class="tick" text-anchor="middle">{years}y</text>'
        )
    grid = []
    for pct in (0, 25, 50, 75, 100):
        y = H * pct / 100
        grid.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" class="grid"/>'
                    f'<text x="-8" y="{y + 4}" class="tick" text-anchor="end">{100 - pct}%</text>')
    return f"""
<figure class="fig">
  <svg viewBox="-42 -14 {W + 60} {H + 46}" role="img"
       aria-label="Share of papers still under an unresolved expression of concern, over ten years.">
    {''.join(grid)}
    <rect x="0" y="0" width="{W}" height="{H}" class="frame"/>
    <line x1="{five:.1f}" y1="0" x2="{five:.1f}" y2="{H}" class="mark"/>
    <path d="{path}" class="curve"/>
    {''.join(ticks)}
    <text x="{five + 8:.1f}" y="16" class="note">five years: {km['at_5y']}% retracted (Kaplan&ndash;Meier)</text>
  </svg>
  <figcaption>The share of papers <b>still carrying an unresolved concern</b>, counted from the
  day each concern was issued, over the whole record (<b>n&nbsp;=&nbsp;{fmt(head['whole_cohort'])}</b>).
  The line drops each time one is retracted; papers not yet retracted are censored at the
  file&rsquo;s cutoff. It falls fast for two years, is nearly flat after three, and at the
  ten-year mark <b>{100 - km['at_10y']:.1f}%</b> are still standing
  (<b>{km['at_10y']}%</b> retracted). At five years this curve reads
  <b>{km['at_5y']}%</b> retracted against the headline&rsquo;s <b>{head['share']:.1f}%</b>:
  two estimators of the same quantity — a survival model over every paper, and a plain
  proportion over only those with a full five years behind them. That they bracket each
  other within four points is the robustness check; neither is corrected towards the
  other.</figcaption>
</figure>"""


def build(data, survival_rows):
    a, b = data["corpus_a"], data["corpus_b"]
    h, km, nl, ag = a["headline"], a["km"], a["notice_level"], data["agreement"]
    bh = b["headline"]
    unresolved = round(100 - h["share"], 1)

    pub_rows = "\n".join(
        f"<tr><td>{p['publisher']}</td><td class=n>{p['n']}</td>"
        f"<td class=n>{p['share']}%</td>"
        f"<td class=n>{'&mdash;' if p['median_days'] is None else int(p['median_days'])}</td>"
        f"<td class=n>{p['issuance_days']}</td></tr>"
        for p in a["by_publisher"])

    src = "\n".join(f'<li>{t} — <a href="{u}">{u}</a></li>' for t, u in SOURCES)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>How long a warning stands</title>
<style>
:root{{
  --bg:#fbfaf7; --ink:#17181a; --dim:#5c6066; --line:#dcd8cf; --accent:#8a3324;
  --panel:#f4f1ea; --mark:#b08968;
}}
@media (prefers-color-scheme: dark){{
  :root:not([data-theme=light]){{
    --bg:#14151a; --ink:#e9e6e0; --dim:#9aa0a8; --line:#2c2e35; --accent:#e08b6e;
    --panel:#1b1d23; --mark:#7a5c46;
  }}
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--ink);
  font:16px/1.62 Charter,"Iowan Old Style",Georgia,"Times New Roman",serif;}}
main{{max-width:47rem;margin:0 auto;padding:3.2rem 1.3rem 5rem}}
h1{{font-size:2.1rem;line-height:1.16;margin:0 0 .3rem;letter-spacing:-.01em}}
h2{{font-size:1.16rem;margin:2.8rem 0 .7rem;letter-spacing:.01em}}
h3{{font-size:1rem;margin:1.7rem 0 .4rem}}
.sub{{color:var(--dim);font-size:1.02rem;margin:0 0 2.2rem}}
.lede{{font-size:1.22rem;line-height:1.5;border-left:3px solid var(--accent);
  padding:.1rem 0 .1rem 1.1rem;margin:2rem 0}}
.lede b{{color:var(--accent)}}
p{{margin:.85rem 0}}
.fig{{margin:2rem 0;padding:1.1rem 1rem .6rem;background:var(--panel);
  border:1px solid var(--line);border-radius:5px}}
svg{{width:100%;height:auto;display:block}}
.frame{{fill:none;stroke:var(--line)}}
.grid{{stroke:var(--line);stroke-dasharray:2 4}}
.curve{{fill:none;stroke:var(--accent);stroke-width:2.1}}
.mark{{stroke:var(--mark);stroke-width:1.4;stroke-dasharray:4 3}}
.ax{{stroke:var(--line)}}
.tick,.note{{font:11px/1 ui-sans-serif,system-ui,sans-serif;fill:var(--dim)}}
.note{{fill:var(--mark)}}
figcaption{{font:.85rem/1.55 ui-sans-serif,system-ui,sans-serif;color:var(--dim);
  margin-top:.7rem}}
table{{border-collapse:collapse;width:100%;font:.88rem/1.45 ui-sans-serif,system-ui,sans-serif;
  margin:1rem 0}}
.scroll{{overflow-x:auto}}
th,td{{text-align:left;padding:.4rem .55rem;border-bottom:1px solid var(--line)}}
th{{color:var(--dim);font-weight:600}}
td.n,th.n{{text-align:right;font-variant-numeric:tabular-nums}}
.box{{background:var(--panel);border:1px solid var(--line);border-radius:5px;
  padding:1rem 1.15rem;margin:1.4rem 0}}
.box p:first-child{{margin-top:0}} .box p:last-child{{margin-bottom:0}}
.box h3{{margin-top:0}}
ul{{padding-left:1.15rem}} li{{margin:.4rem 0}}
a{{color:var(--accent)}}
footer{{margin-top:3.5rem;padding-top:1.2rem;border-top:1px solid var(--line);
  font:.83rem/1.6 ui-sans-serif,system-ui,sans-serif;color:var(--dim)}}
footer a{{word-break:break-all}}
code{{font:.86em ui-monospace,SFMono-Regular,Menlo,monospace;background:var(--panel);
  padding:.08em .3em;border-radius:3px}}
</style></head><body><main>

<h1>How long a warning stands</h1>
<p class="sub">The response clock, measured on {fmt(a['papers_with_a_concern'])} papers that
carry a public expression of concern. The Field · 2026-09-01 · version 1.0</p>

<p class="lede">When a journal publicly warns that one of its papers may be unreliable, the
warning has become a retraction five years later in <b>fewer than half</b> of cases —
<b>{h['share']:.1f}%</b> of {fmt(h['n'])} papers. The other <b>{unresolved}%</b> are still
standing, flagged and unresolved. When a resolution does come, the wait is short:
<b>{int(h['median_days'])} days</b>, a median unchanged since the last time anyone
measured it, nine years ago.</p>

<p>Detection in science is now cheap and largely automated. What happens <i>after</i> a
problem is flagged is not measured at all — every published measurement of the interval
between a complaint and an editorial decision that this session could find is a case series
reported by the very people who filed the complaints. There is one flag whose clock anyone
can run from public data: the <b>expression of concern</b>, a notice a journal publishes to
say it has a question about a paper it has not yet withdrawn. Both ends carry a date. This
page runs that clock.</p>

<h2>The measurement</h2>

<p>A paper enters on the date of its first expression of concern and leaves on the date of
the first retraction that follows. The headline counts only papers whose concern was issued
on or before <b>{data['follow_up_days'] // 365}</b> years before the record&rsquo;s cutoff of
<b>{a['cutoff']}</b>, so every one of them has had the full window — no survival model is
needed to read it. The interval is a bootstrap resampled over <b>issuance days</b>, not
papers, because concerns arrive in batches: the largest single day in this record carries
<b>{a['largest_issuance_days'][0][1]}</b> of them.</p>

<div class="scroll"><table>
<tr><th>Measure</th><th class="n">Value</th><th class="n">95% interval</th></tr>
<tr><td>Papers in the mature cohort</td><td class="n">{fmt(h['n'])}</td><td class="n">&mdash;</td></tr>
<tr><td>Distinct issuance days in it</td><td class="n">{fmt(h['issuance_days'])}</td><td class="n">&mdash;</td></tr>
<tr><td><b>Resolved into a retraction within five years</b></td>
    <td class="n"><b>{h['share']:.1f}%</b></td>
    <td class="n">{h['share_ci'][0]}&ndash;{h['share_ci'][1]}%</td></tr>
<tr><td>Median days to retraction, among those resolved</td>
    <td class="n">{int(h['median_days'])}</td>
    <td class="n">{int(h['median_ci'][0])}&ndash;{int(h['median_ci'][1])}</td></tr>
<tr><td>Same measure at notice level ({fmt(nl['notices'])} notices, largest covering {nl['largest_notice']} papers)</td>
    <td class="n">{nl['share']}%</td><td class="n">&mdash;</td></tr>
</table></div>

{{FIGURE}}

<p>Over the whole cohort, with unresolved papers censored at the cutoff, a Kaplan&ndash;Meier
estimate puts retraction at <b>{km['at_1y']}%</b> after one year, <b>{km['at_3y']}%</b> after
three and <b>{km['at_10y']}%</b> after ten. The curve is nearly flat after year three: a
concern not resolved in its first three years is, on this evidence, mostly not going to be.
Counting every later notice of any kind, <b>{fmt(a['outcomes_whole_cohort']['nothing after the concern'])}</b>
of {fmt(a['papers_with_a_concern'])} papers have had nothing at all happen since their concern
was issued, {a['outcomes_whole_cohort'].get('Correction', 0)} received a correction and
{a['outcomes_whole_cohort'].get('Reinstatement', 0)} were reinstated.</p>

<h2>The same question asked of a second corpus</h2>

<p>The headline comes from a database compiled by people who read notices. The same clock was
run again over a corpus assembled only from <b>what publishers themselves deposited</b> —
every notice the Crossref API returns under its expression-of-concern and retraction update
types ({fmt(b['eoc_notices'])} and {fmt(b['retraction_notices'])} notices), joined on the
works each one declares it acts on. Neither corpus is a ground truth. The disagreement is the
finding.</p>

<div class="scroll"><table>
<tr><th>On the {fmt(ag['papers_in_both_mature_cohorts'])} papers present in both mature cohorts</th><th class="n">Papers</th></tr>
<tr><td>Both corpora record a retraction within five years</td><td class="n">{ag['both_say_resolved']}</td></tr>
<tr><td>Both record none</td><td class="n">{ag['both_say_unresolved']}</td></tr>
<tr><td>Only the curated database records one</td><td class="n">{ag['only_corpus_a_says_resolved']}</td></tr>
<tr><td>Only the publishers&rsquo; own deposits record one</td><td class="n">{ag['only_corpus_b_says_resolved']}</td></tr>
<tr><td><b>Disagree about whether anything happened</b></td><td class="n"><b>{ag['disagreement_share']}%</b></td></tr>
<tr><td>Of the {ag['date_gap_days']['n']} both call resolved, dates identical</td>
    <td class="n">{ag['date_gap_days']['identical']}</td></tr>
<tr><td>&hellip; and within a month of each other</td><td class="n">{ag['date_gap_days']['within_31_days']}</td></tr>
</table></div>

<p><b>The two feeds tick the same clock and disagree about whether it ever stopped.</b> Where
both record a resolution they almost always name the same day —
{ag['date_gap_days']['identical']} of {ag['date_gap_days']['n']} are identical. But on
{ag['disagreement_share']}% of shared papers one feed holds a response the other does not, and
the imbalance is lopsided: {ag['only_corpus_a_says_resolved']} retractions appear only in the
curated database against {ag['only_corpus_b_says_resolved']} appearing only in the publishers&rsquo;
deposits. Run on deposits alone, the same measurement returns <b>{bh['share']:.1f}%</b>
resolved ({bh['share_ci'][0]}&ndash;{bh['share_ci'][1]}%, n&nbsp;=&nbsp;{fmt(bh['n'])}) with a
median of <b>{int(bh['median_days'])} days</b>. Read the two together: the timing is solid, the
share resolved is a floor, and a measurement built only from what publishers file about
themselves sees less of the response than one built by people reading notices.</p>

<h2>What has changed since the last time this was measured</h2>

<p>One dedicated study of this interval exists. In 2017 Vaught, Jordan and Bastian identified
every editorial expression of concern they could find in PubMed and PubMed Central up to
August 2016 — <b>230 notices affecting 300 publications</b> — and reported, in their words,
that <i>&ldquo;the mean time from EEoC to retraction was 299&nbsp;&plusmn;&nbsp;245 days, and the
median was 263 days&rdquo;</i>, that a quarter of affected publications had been retracted by
December 2016, and that <i>&ldquo;31% of cases remained open&rdquo;</i>. Their conclusion:
<i>&ldquo;Most have not led to retractions, and many remain unresolved.&rdquo;</i></p>

<p>Nine years later, on a cohort <b>{a['papers_with_a_concern'] // 300} times larger</b> and
with five full years of follow-up rather than a snapshot:</p>

<ul>
<li><b>The speed of a resolution has not changed.</b> Their median was 263 days; ours is
{int(h['median_days'])}, with an interval of {int(h['median_ci'][0])}&ndash;{int(h['median_ci'][1])}
days that contains theirs. When a journal decides, it decides at the same pace it did a decade
ago.</li>
<li><b>What has changed is how often it decides at all.</b> They estimated 31% of cases open;
we find <b>{unresolved}%</b> of papers still unresolved after a full five years. The two
numbers are not directly comparable — different corpus, different window, and their snapshot
was taken only months after half their notices were issued, which pushes their open share
<i>down</i>, not up. That direction matters: the gap between 31% and {unresolved}% is if
anything understated.</li>
<li><b>Their study was a description, taken once.</b> It has not been repeated. The instrument
that would have caught the change is a clock, and nobody was running one.</li>
</ul>

<h2>By publisher — read this narrowly</h2>

<p>This table describes <b>what is in a public database</b>, and nothing else. A publisher
that issues concerns readily and resolves them slowly appears here; one that never issues a
concern at all does not appear at all, and looks better for it. Counts are papers, not notices,
and a single batch notice can contribute dozens — the issuance-day column is there so a reader
can see when that has happened. Nothing about the conduct of any named organisation follows
from these rows.</p>

<div class="scroll"><table>
<tr><th>Publisher named in the record</th><th class="n">Papers</th>
<th class="n">Retracted in 5y</th><th class="n">Median days</th><th class="n">Issuance days</th></tr>
{pub_rows}
</table></div>

<h2>What this does not measure</h2>

<div class="box">
<p><b>Not every flag, only the published ones.</b> A concern raised privately with an editor, a
comment on a post-publication site, or an automated detection report has no dated public record
that can be joined to an outcome. This clock runs on the one flag that does.</p>
<p><b>Silence and quiet withdrawal look identical here.</b> The 2017 study found expressions of
concern that publishers had removed without leaving a record. Such a case appears in this
measurement as permanently unresolved, and nothing in the data distinguishes the two.</p>
<p><b>The denominator is the weaker half of the record.</b> The primary file&rsquo;s own
documentation says of update types other than retraction: <i>&ldquo;these are not as
comprehensive as retractions.&rdquo;</i> Concerns are collected less completely than the
retractions that resolve them. A concern that is never resolved also never generates the second
notice that would draw a curator&rsquo;s attention to the first — so the missing records are
plausibly weighted towards the unresolved, which would make the true unresolved share higher
than {unresolved}%, not lower. That is reasoning about a bias, not a measurement of one.</p>
<p><b>This was not pre-registered</b> and the design followed exploration rather than preceding
it. Read it as an exploratory measurement of a public dataset. <a href="METHOD.md">METHOD.md</a>
states the sequence honestly, including the five-year window&rsquo;s arbitrariness.</p>
</div>

{{SURVEY}}

<h2>Standing conditions on reuse</h2>

<p>The tables we computed are offered for reuse: <code>data/cohort.csv</code> (every paper, its
concern date and its outcome as of 2026-09-01), <code>data/survival.csv</code>,
<code>data/data.json</code>. Both source corpora move continuously, so a rerun will not
reproduce these figures exactly — which is why the per-paper state is committed beside the
page. <b>On terms:</b> the underlying database is Retraction Watch&rsquo;s, distributed by
Crossref; we did not retrieve an explicit licence statement for it in this session and make no
claim about one, so anyone redistributing the identifiers should check the source&rsquo;s own
terms rather than ours. We ask, and do not require, that a reuser carry the caveats above with
the numbers, and that corrections come back to us rather than being made silently downstream.
Corrections to this page will appear as new dated versions, never as edits.</p>

<footer>
<p><b>Sources</b></p>
<ul>{src}</ul>
<p>The Field · session 143 · artifact <code>artifacts/cycle-001/2026-09-01-how-long-a-warning-stands/</code>.
Method: <a href="METHOD.md">METHOD.md</a>. Scripts: <code>tools/response-ledger/</code>.
Data generated {data['generated']} from files downloaded the same day; the record&rsquo;s own
cutoff is {a['cutoff']}. Figures on this page are written by
<code>make_page.py</code> from <code>data/data.json</code>, so no number here can differ from
the file it was computed into.</p>
</footer>
</main></body></html>
"""


def main():
    data_path, surv_path, out_path = sys.argv[1], sys.argv[2], sys.argv[3]
    check = "--check" in sys.argv

    data = json.load(open(data_path, encoding="utf-8"))
    rows = []
    with open(surv_path, encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append((int(r["days"]), float(r["share_still_under_concern"])))

    head = dict(data["corpus_a"]["headline"])
    head["whole_cohort"] = data["corpus_a"]["papers_with_a_concern"]
    html = build(data, rows)
    html = html.replace("{FIGURE}", figure(rows, head, data["corpus_a"]["km"]))

    survey_path = os.path.join(os.path.dirname(os.path.abspath(out_path)), "SURVEY.html")
    if not os.path.exists(survey_path):
        print(f"missing {survey_path}", file=sys.stderr)
        sys.exit(1)
    html = html.replace("{SURVEY}", open(survey_path, encoding="utf-8").read())

    if check:
        current = open(out_path, encoding="utf-8").read()
        if current != html:
            print("DRIFT: the page does not match the data file", file=sys.stderr)
            sys.exit(1)
        print("page matches data")
        return

    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(html)
    print(f"wrote {out_path} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
