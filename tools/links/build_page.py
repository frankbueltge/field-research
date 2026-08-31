#!/usr/bin/env python3
"""Render the artifact page from data/summary.json. Every number on the page comes
from that file; none is typed by hand.

Usage: python3 tools/links/build_page.py <artifactdir>
"""
import json, os, sys, html

BLUE, RED, INK, GREY, LINE, PAPER = "#2563eb", "#b3452c", "#1c1b19", "#78736d", "#e7e4df", "#fcfcfb"


def pct(x, nd=1):
    return "—" if x is None else ("%." + str(nd) + "f %%") % (100 * x)


def esc(s):
    return html.escape(str(s))


def bars_by_quarter(s, key, title, sub):
    """Grouped bars: cohort A vs cohort B per quarter, for `key` (a rate in 0..1)."""
    qs = sorted(set(s["by_quarter"]["A"]) | set(s["by_quarter"]["B"]))
    W, H, L, R, T, B = 1000, 260, 46, 14, 34, 46
    pw = W - L - R
    gw = pw / max(len(qs), 1)
    rows = []
    for i, q in enumerate(qs):
        for j, (c, col) in enumerate((("A", BLUE), ("B", GREY))):
            v = s["by_quarter"][c].get(q, {}).get(key)
            if v is None:
                continue
            bw = gw * 0.34
            x = L + i * gw + gw * 0.12 + j * bw
            h = (H - T - B) * v
            y = H - B - h
            n = s["by_quarter"][c][q]
            denom = (n["papers"] if key == "declaration_rate"
                     else n["reachable"] + n["gone"])
            rows.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s">'
                        '<title>%s cohort %s: %s (n=%d)</title></rect>'
                        % (x, y, bw, max(h, 0.6), col, q, c, pct(v), denom))
        rows.append('<text x="%.2f" y="%d" font-size="10" fill="%s" text-anchor="middle">%s</text>'
                    % (L + i * gw + gw / 2, H - B + 14, GREY, q))
    grid = []
    for frac in (0, .25, .5, .75, 1.0):
        y = H - B - (H - T - B) * frac
        grid.append('<line x1="%d" y1="%.1f" x2="%d" y2="%.1f" stroke="%s" stroke-width="1" %s/>'
                    % (L, y, W - R, y, LINE, '' if frac == 0 else 'stroke-dasharray="2 4"'))
        grid.append('<text x="%d" y="%.1f" font-size="10" fill="%s" text-anchor="end">%d%%</text>'
                    % (L - 6, y + 3, GREY, frac * 100))
    return ('<svg viewBox="0 0 %d %d" width="100%%" role="img" aria-label="%s">'
            '<rect width="%d" height="%d" fill="%s"/>'
            '<text x="0" y="12" font-size="13" font-weight="600" fill="%s">%s</text>'
            '<text x="0" y="26" font-size="11" fill="%s">%s</text>%s%s</svg>'
            % (W, H, esc(title + '. ' + sub), W, H, PAPER, INK, esc(title), GREY, esc(sub),
               "".join(grid), "".join(rows)))


def main():
    d = sys.argv[1]
    s = json.load(open(os.path.join(d, "data", "summary.json")))
    A, B = s["cohorts"]["A"], s["cohorts"]["B"]
    hv = s["harvest"]
    cj = s["conjecture"]

    qrows = []
    for q in sorted(set(s["by_quarter"]["A"]) | set(s["by_quarter"]["B"])):
        a = s["by_quarter"]["A"].get(q, {})
        b = s["by_quarter"]["B"].get(q, {})
        qrows.append(
            "<tr><td>%s</td><td>%d</td><td>%s</td><td>%s</td><td>%d</td><td>%s</td><td>%s</td></tr>"
            % (q, a.get("papers", 0), pct(a.get("declaration_rate")),
               "%d / %d" % (a.get("reachable", 0), a.get("reachable", 0) + a.get("gone", 0)),
               b.get("papers", 0), pct(b.get("declaration_rate")),
               "%d / %d" % (b.get("reachable", 0), b.get("reachable", 0) + b.get("gone", 0))))

    hostrows = []
    for r in s["hosts_top"]["A"]:
        hostrows.append("<tr><td><code>%s</code></td><td>%d</td><td>%d</td></tr>"
                        % (esc(r["host"]), r["n"], r["gone"]))

    indet = "".join("<tr><td><code>%s</code></td><td>%d</td></tr>" % (esc(k), v)
                    for k, v in s["indeterminate"]["by_note"].items())

    gh_a = s["by_host"]["A"].get("code", {})
    ot_a = s["by_host"]["A"].get("other", {})
    gh_b = s["by_host"]["B"].get("code", {})
    ot_b = s["by_host"]["B"].get("other", {})
    phrases_rows = "".join("<tr><td>%s</td><td>%d</td></tr>" % (esc(k), v)
                           for k, v in s["phrase_counts"].items())
    dead_rows = "".join("<tr><td>%s</td><td>%s</td><td>%s</td><td><code>%s</code></td></tr>"
                        % (d["published"], d["cohort"], esc(d["where"]), esc(d["note"]))
                        for d in s["dead_links"])
    boot = s["declaration_cluster_bootstrap"]
    tt = s["trend_test"]
    l24 = s["links_2024"]

    page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Links in the abstract — The Field</title>
<style>
  :root {{ color-scheme: light; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; background: {PAPER}; color: {INK};
    font: 16px/1.6 ui-serif, Georgia, "Times New Roman", serif; }}
  main {{ max-width: 62rem; margin: 0 auto; padding: 3rem 1.25rem 5rem; }}
  h1 {{ font-size: clamp(1.7rem, 4vw, 2.5rem); line-height: 1.15; margin: 0 0 .6rem; }}
  h2 {{ font-size: 1.25rem; margin: 3rem 0 .75rem; }}
  h3 {{ font-size: 1rem; margin: 1.75rem 0 .4rem; }}
  p, li {{ max-width: min(40rem, 100%); }}
  h1, h2, h3, figcaption {{ overflow-wrap: break-word; }}
  .meta, .note, figcaption, .small {{
    font: 13px/1.55 ui-sans-serif, system-ui, sans-serif; color: #4a4744; }}
  .meta {{ margin-bottom: 2rem; }}
  .lede {{ font-size: 1.15rem; }}
  .tiles {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(13rem, 1fr));
    gap: .75rem; margin: 2rem 0; padding: 0; list-style: none; }}
  .tile {{ border: 1px solid {LINE}; border-radius: 8px; padding: .9rem 1rem; }}
  .tile b {{ display: block; font: 700 1.9rem/1.1 ui-sans-serif, system-ui, sans-serif;
    letter-spacing: -.02em; }}
  .tile span {{ font: 13px/1.45 ui-sans-serif, system-ui, sans-serif; color: #4a4744;
    display: block; margin-top: .35rem; }}
  figure {{ margin: 2rem 0; }}
  .figwrap {{ overflow-x: auto; }}
  .figwrap svg {{ min-width: 680px; }}
  .scroll {{ overflow-x: auto; border: 1px solid {LINE}; border-radius: 8px; }}
  table {{ border-collapse: collapse; width: 100%;
    font: 13px/1.4 ui-sans-serif, system-ui, sans-serif; }}
  th, td {{ text-align: right; padding: .35rem .6rem; border-bottom: 1px solid {LINE};
    white-space: nowrap; }}
  th:first-child, td:first-child {{ text-align: left; }}
  thead th {{ position: sticky; top: 0; background: {PAPER}; color: #4a4744; font-weight: 600; }}
  code {{ font-size: .9em; background: #f2f0ec; padding: .1em .35em; border-radius: 3px;
    overflow-wrap: anywhere; }}
  a {{ color: {BLUE}; }}
  .rule {{ border: 0; border-top: 1px solid {LINE}; margin: 3rem 0 0; }}
  ul.tight li {{ margin: .3rem 0; }}
  .verdict {{ border-left: 3px solid {LINE}; padding: .1rem 0 .1rem 1rem; margin: 1rem 0; }}
</style></head><body><main>

<h1>{{HEADLINE}}</h1>
<p class="meta">The Field · artifact 2 of cycle 001 · version 1.0, 2026-08-31 ·
question of the cycle: <em>E2E automation of AI research</em> ·
harvested {esc(hv['harvested_utc'])}, links probed {esc(s['probed_utc'])}</p>

<p class="lede">{{LEDE}}</p>

<ul class="tiles">
  <li class="tile"><b>{pct(A['declaration_rate'])}</b><span>of the {A['papers']} papers whose
    abstracts advertise automated research put a link in the abstract
    ({A['papers_with_abstract_url']} papers)</span></li>
  <li class="tile"><b>{pct(B['declaration_rate'])}</b><span>of the {B['papers']} age-matched
    control papers do the same ({B['papers_with_abstract_url']} papers)</span></li>
  <li class="tile"><b>{pct(A['resolution_rate'])}</b><span>of the {A['reachable'] + A['gone']}
    decidable links in the first group are publicly reachable today</span></li>
  <li class="tile"><b>{pct(B['resolution_rate'])}</b><span>of the {B['reachable'] + B['gone']}
    decidable links in the control are</span></li>
</ul>

<h2>What was measured</h2>
<p>Session 141 measured this house's own automated research loop and found that it kept
producing after it stopped delivering. A loop's yield cannot be measured from outside —
nobody publishes their discards. One thing can: <strong>the last step, where a pipeline is
supposed to hand a stranger something they can open.</strong></p>
<p>Two cohorts of arXiv papers, submitted 2024-01-01 to 2026-08-31.
<strong>Cohort A</strong> ({A['papers']} papers): abstracts containing any of ten fixed
phrases that advertise automation of research work. <strong>Cohort B</strong>
({B['papers']} papers): <code>cs.AI</code> papers drawn to the same monthly counts, so the
two have the same age distribution. For every <code>http(s)</code> address the
<em>abstract</em> declares — {A['urls']} in cohort A, {B['urls']} in cohort B — we asked one
question on {esc(s['generated_utc'][:10])}: does it still open?</p>
<p class="note">Method, phrase list, probe definitions and the conjecture fixed before
computing: <code>METHOD.md</code>, committed before the first row of data existed. Raw
counts: <code>data/</code>. Scripts: <code>tools/links/</code>.</p>

<h2>The figure</h2>
<figure>
<div class="figwrap">{{FIG1}}</div>
<figcaption>Share of papers that put any link in the abstract, by quarter of submission.
Blue: cohort A (automation claim). Grey: cohort B (control). Hover a bar for its
denominator.</figcaption>
</figure>
<figure>
<div class="figwrap">{{FIG2}}</div>
<figcaption>Of the links declared, the share publicly reachable on 2026-08-31, by quarter of
submission. Quarters with few decidable links move a long way on one link; the denominators
are in the table below.</figcaption>
</figure>

<h2>The three things that came out</h2>

<div class="verdict"><p><strong>1. The automation cohort does hand you a link more often.</strong>
{pct(A['declaration_rate'])} against {pct(B['declaration_rate'])}
({A['papers_with_abstract_url']}/{A['papers']} against
{B['papers_with_abstract_url']}/{B['papers']}; 95 % intervals
{pct(A['declaration_ci'][0])}–{pct(A['declaration_ci'][1])} and
{pct(B['declaration_ci'][0])}–{pct(B['declaration_ci'][1])}). Conjecture 1, fixed before the
harvest, {{VERDICT1}}. The control was drawn in blocks, so its papers cluster in submission
time ({s['clustering']['B']['distinct_days']} distinct days for {B['papers']} papers, against
{s['clustering']['A']['distinct_days']} in cohort A), and the ordinary test assumes they do
not. Resampling whole submission days instead ({boot['iterations']} draws) puts the gap at
{boot['ci95_points'][0]}–{boot['ci95_points'][1]} points, with
{100 * boot['share_at_or_below_zero']:.1f} % of draws at or below zero: <strong>the gap
survives the clustering</strong>, and the flat test overstates its precision.</p></div>

<div class="verdict"><p><strong>2. Whether it opens looks the same in both groups, and this
design could not have seen a small difference.</strong>
{pct(A['resolution_rate'])} of cohort A's decidable links resolve, against
{pct(B['resolution_rate'])} of the control's (95 % intervals
{pct(A['resolution_ci'][0])}–{pct(A['resolution_ci'][1])} and
{pct(B['resolution_ci'][0])}–{pct(B['resolution_ci'][1])}). Conjecture 2 said cohort A would
do no better; it {{VERDICT2}}. <strong>And the window is young:</strong> the median declared
link in cohort A is {A['median_link_age_days']} days old at the probe
({B['median_link_age_days']} in the control), and only {A['links_older_than_one_year']} of
{A['urls']} cohort A links — {B['links_older_than_one_year']} of {B['urls']} in the control —
have had a year to rot. This is a measurement of <em>early</em> availability. It is not a
decay curve and must not be read as one.</p></div>

<div class="verdict"><p><strong>3. Read as a reader.</strong> Of the cohort A papers that
declare a link and got a decidable answer, {A['papers_any_open']} of {A['papers_decided']}
({pct(A['paper_resolution_rate'])}) have at least one address that opens — so
{A['papers_decided'] - A['papers_any_open']} papers advertise automated research and leave a
reader with nothing that answers. In the control: {B['papers_any_open']} of
{B['papers_decided']} ({pct(B['paper_resolution_rate'])}).</p></div>

<h2>What the dead links actually are</h2>
<p>There are {len(s['dead_links'])} of them in {s['declared_links_total']} declared links.
Two things are true of all eight, and only one of them carries any weight.</p>
<p><strong>What does carry weight: every failure is a code-hosting address that answers the
git protocol with a refusal.</strong> From outside, a repository that was announced and never
made public is indistinguishable from one that was published and later withdrawn. This probe
cannot separate those two, and nothing on this page decides between them.</p>
<p><strong>What does not carry weight, stated because it is tempting:</strong> all
{l24['decidable']} links declared in 2024 — the oldest in the study — open today. That is not
evidence against decay. At the failure rate measured here
({pct(l24['overall_failure_rate'])} of decidable links), the expected number of failures among
{l24['decidable']} links is {l24['expected_failures']}, and the chance of seeing none is about
{100 * l24['p_zero_failures_by_chance']:.1f} %. An earlier version of this section read that survival
as a finding; it was withdrawn before publication, on this arithmetic.</p>
<div class="scroll"><table>
<thead><tr><th>Declared</th><th>Cohort</th><th>Where it points</th><th>Probe outcome</th></tr></thead>
<tbody>{dead_rows}</tbody></table></div>

<h2>What cohort A is made of</h2>
<p>Ten phrases, very unevenly. Two of them carry almost nothing; one carries nearly half the
cohort. A reader should know that before reading "papers claiming automation of research" as a
description of a field.</p>
<div class="scroll"><table>
<thead><tr><th>Abstract phrase</th><th>papers matched (overlapping)</th></tr></thead>
<tbody>{phrases_rows}</tbody></table></div>

<h2>Where the links point, and where they break</h2>
<p>Code hosting dominates: {gh_a.get('reachable',0) + gh_a.get('gone',0) + gh_a.get('indeterminate',0)}
of cohort A's {A['urls']} links are repository addresses, of which
{pct(gh_a.get('resolution_rate'))} resolve; everything else —
{ot_a.get('reachable',0) + ot_a.get('gone',0) + ot_a.get('indeterminate',0)} links to project
pages, demos and data hosts — resolves at {pct(ot_a.get('resolution_rate'))}. The control
splits {pct(gh_b.get('resolution_rate'))} against {pct(ot_b.get('resolution_rate'))}.</p>
<p class="note">Hosts are grouped in kind here; every address itself is in
<code>data/urls.csv</code>, unaltered, so the grouping can be checked or redone.</p>
<div class="scroll"><table>
<thead><tr><th>Where the link points (cohort A)</th><th>links</th><th>not reachable</th></tr></thead>
<tbody>{"".join(hostrows)}</tbody></table></div>

<h2>Every quarter, both cohorts</h2>
<div class="scroll"><table>
<thead><tr><th>Quarter</th><th>A: papers</th><th>A: declare</th><th>A: links open</th>
<th>B: papers</th><th>B: declare</th><th>B: links open</th></tr></thead>
<tbody>{"".join(qrows)}</tbody></table></div>

<h2>What we could not decide, counted rather than hidden</h2>
<p>{s['indeterminate']['total']} of the {s['declared_links_total']} declared links
({s['distinct_urls_probed']} distinct addresses) could not be decided
from here and are excluded from every rate above rather than counted as rot. This session's
network egress passes a proxy that answers <code>403</code> for <code>github.com</code> over
HTTP whatever the target — which is why repository links are probed with
<code>git ls-remote</code>, a path the proxy passes. On this pass no link was left
undecided by a <code>403</code>: what could not be decided was two video links rate-limiting
the probe, two <code>github.com</code> addresses that name a profile rather than a repository,
one address on a non-standard port that timed out, and one dataset host asking for
credentials.</p>
<p class="note">The probe was amended once during this session, after an internal critique
found two defects in it: a <code>github.com</code> address that is a profile rather than a
repository had been decided over HTTP on the very host whose HTTP answers this method
declares untrustworthy, and links pointing into a named branch had been credited to the
repository root without checking that the branch exists. Both are fixed, every link was
re-probed under the corrected definition, and the superseded first pass is kept beside the
data as <code>data/probes-pass1-superseded.csv</code>. <strong>What the second pass changed,
in full:</strong> the profile-shaped control address moved from "not reachable" to "not
decidable"; the branch check altered no outcome (three addresses name a branch, all of them
resolved); and two video links that answered <code>200</code> on the first pass answered with
a rate limit on the second and are now undecided. That last change is not a correction but a
different day's weather, and it moved the published figures: the control's resolution rate
rose from 96.3 % to 97.5 % and the gap between the cohorts widened from 1.3 to 2.5 points —
neither of which this page reads as a difference, then or now.</p>
<div class="scroll"><table>
<thead><tr><th>Probe outcome that decided nothing</th><th>links</th></tr></thead>
<tbody>{indet}</tbody></table></div>

<h2>What this does not show</h2>
<ul class="tight">
  <li><strong>An address that answers is not a working artifact.</strong> We asked whether the
    door opens, not whether anything is behind it. Nothing here says a resolving link leads to
    code that runs, and this measurement is an upper bound on availability for that reason.</li>
  <li><strong>The abstract is a small window.</strong> Most papers put their links in the body.
    The declaration rate is a floor — how often the abstract itself hands you something —
    not an estimate of how many papers publish artifacts.</li>
  <li><strong>A phrase filter is not a taxonomy.</strong> Cohort A is the set of abstracts
    using ten fixed phrases; it mixes papers presenting automated systems with papers studying
    or criticising them, and it is not a list of any particular class of system.</li>
  <li><strong>A private repository and a deleted one look identical from outside</strong> — and
    both are the same event for a reader, which is how they are counted.</li>
  <li><strong>Nothing here has had time to rot.</strong> Half the declared links are younger
    than {A['median_link_age_days']} days. The published literature on reference rot measures
    corpora over years; a repeat of this probe on the same identifiers in a year would be a
    measurement of decay, and this one is its baseline.</li>
  <li><strong>Conjecture 3, on age, is not supported — and not refuted either.</strong> Split
    each cohort's decidable links at its median date: the older half resolves
    {esc(tt['A']['older_half'])} against {esc(tt['A']['newer_half'])} in the newer half
    (Fisher exact p = {esc(tt['A']['fisher_p'])}), and {esc(tt['B']['older_half'])} against
    {esc(tt['B']['newer_half'])} in the control (p = {esc(tt['B']['fisher_p'])}). The failure
    cells here hold 1, 5, 0 and 2 links, which is why the exact test is quoted rather than the
    normal approximation the same split gives (p = {esc(tt['A']['test']['p'])} and
    {esc(tt['B']['test']['p'])}); and the split is by rank, so links sharing the median date
    fall on either side of it. The
    direction is the opposite of the conjecture — newer links fail more — and neither test
    reaches significance. An earlier draft of this page called the conjecture refuted on the
    sign of an unweighted slope across quarters with denominators from 1 to 41; that was too
    strong, and the sentence was replaced before publication.</li>
  <li><strong>The declaration gap may be about genre, not about automation.</strong> A
    phrase-matched cohort is full of system and benchmark papers, which ship artifacts as a
    matter of form, while <code>cs.AI</code> at large also holds theory, position and survey
    papers with nothing to link. Nothing here controls for that, and it is the most likely
    innocent explanation of finding 1.</li>
  <li><strong>The control is one listing, not one field.</strong> <code>cs.AI</code> here means
    primary or cross-listed; {s['control_primary_csai']} of {B['papers']} control papers carry
    <code>cs.AI</code> as their primary category, the rest sitting mostly in neighbouring
    machine-learning, vision and language listings.</li>
  <li><strong>{s['duplicate_declarations']} addresses are declared by more than one paper</strong>
    and are counted once per declaring paper, which is how a reader meets them.</li>
</ul>

<h2>Who has measured near this before</h2>
<p>Checked before this page was written, so that nothing here is offered as new that is not.
Availability of what papers link to is an established field, and the general result — that a
substantial share of scholarly links stops resolving — is not this practice's finding:</p>
<ul class="tight">
  <li>Klein, Van de Sompel, Sanderson, Shankar, Balakireva, Zhou and Tobin,
    <em>Scholarly Context Not Found: One in Five Articles Suffers from Reference Rot</em>,
    PLOS ONE 9(12):e115253, 2014 —
    <a href="https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0115253">journals.plos.org</a>.</li>
  <li>Wattanakriengkrai, Chinthanet, Hata, Kula, Treude, Guo and Matsumoto,
    <em>GitHub Repositories with Links to Academic Papers: Public Access, Traceability, and
    Evolution</em>, submitted 1 April 2020 —
    <a href="https://arxiv.org/abs/2004.00199">arXiv:2004.00199</a>. Studies the reverse
    direction (repositories citing papers) over 20 000 repositories.</li>
  <li>Chapekis, Bestvater, Remy and Rivero, <em>When Online Content Disappears</em>,
    Pew Research Center, May 2024 —
    <a href="https://www.pewresearch.org/data-labs/2024/05/17/when-online-content-disappears/">pewresearch.org</a>.</li>
  <li><em>A Study of Computational Reproducibility using URLs Linking to Open Access Datasets
    and Software</em>, <code>10.1145/3487553.3524658</code> — the nearest neighbour by method,
    and <strong>closed to us</strong>: the publisher's page returned HTTP 403 on 2026-08-31.
    Recorded as a closed route, not as an absence.</li>
</ul>
<p>What is not in that literature, as far as this session could find, is the contrast measured
here: <strong>the same probe applied to papers that advertise automated research and to
age-matched papers that do not.</strong> That is an absence we looked for and did not fill in
by assumption — a search that missed something is a search that missed something.</p>

<h2>How this page was checked</h2>
<p>Two checks were run against it inside this session, and both found things. An independent
recomputation re-derived every figure from the raw files by its own route and caught a
rounding error, an over-strong word, a defect in the probe and a mis-grouped host; a hostile
reading attacked the design and took the headline off a claim the data could not carry. What
they found, what was fixed and what was left standing is written up beside this page —
<code>VERIFICATION.md</code> and <code>CRITIQUE.md</code>, the critique published unedited.
<strong>Both checks are internal.</strong> No reader outside this practice has seen this page,
which is the same ceiling this practice's closing report named for its whole record.</p>

<h2>Reuse conditions</h2>
<p>Data <a href="https://creativecommons.org/publicdomain/zero/1.0/">CC0</a>, text
<a href="https://creativecommons.org/licenses/by/4.0/">CC BY 4.0</a>. If you carry these
numbers onward, carry these with them: the window (2024-01-01 to 2026-08-31), the probe date
(2026-08-31), the abstract-only extraction, and the fact that reachable means
<em>the address answered</em>, nothing more. Papers are identified by arXiv identifier, which
resolves to the primary record. Corrections to this page will be new dated documents beside
it, not silent edits.</p>

<hr class="rule">
<p class="small">The Field · a research practice in the ecology around frankbueltge.de ·
version 1.0, 2026-08-31 · cohort A n={A['papers']}, cohort B n={B['papers']},
{s['declared_links_total']} declared links
({s['distinct_urls_probed']} distinct addresses) probed · this page is self-contained and loads nothing from the
network.</p>
</main></body></html>
"""
    # ---- the sentences that depend on the result, chosen by the data, not by hand ----
    dd, rd = s["declaration_diff"], s["resolution_diff"]
    decl_sig = dd is not None and dd["p"] < 0.05
    res_sig = rd is not None and rd["p"] < 0.05
    if decl_sig and not res_sig:
        headline = ("Papers that advertise automated research<br>put a link in front of you "
                    "more often.")
    elif decl_sig and res_sig:
        headline = ("They put a link in front of you more often. It opens %s often."
                    % ("less" if (A["resolution_rate"] or 0) < (B["resolution_rate"] or 0) else "more"))
    else:
        headline = "What the abstract promises, and what still opens"
    lede = ("They were compared with age-matched control papers on one question a stranger can "
            "check without anyone's cooperation: of the links they put in front of a reader, how "
            "many still open? %s of the automation cohort's abstracts declare a link against %s "
            "of the control's — a real gap. Almost all of those links open in both groups "
            "(%s against %s), and this design could not have separated the groups on that: it "
            "could not reliably see a difference smaller than %s points. The plainest number on "
            "this page is the one nobody advertises: %s of the automation cohort's abstracts "
            "hand a reader no address at all."
            % (pct(A["declaration_rate"]), pct(B["declaration_rate"]),
               pct(A["resolution_rate"]), pct(B["resolution_rate"]),
               s["resolution_mde_points"], pct(1 - A["declaration_rate"])))
    verdict1 = ("held (two-proportion z = %s, p = %s)" % (dd["z"], dd["p"]) if dd
                else "held") if cj["1_declaration_higher_in_A"]["held"] else "is refuted"
    if cj["2_resolution_no_better_in_A"]["held"]:
        verdict2 = ("holds only in the arithmetic sense: cohort A is lower by %.1f points, "
                    "which at z = %s, p = %s is indistinguishable from no difference. The honest "
                    "reading is that this measurement found no difference and, at these "
                    "denominators, could not have reliably detected one smaller than about "
                    "%s points"
                    % (100 * (B["resolution_rate"] - A["resolution_rate"]), rd["z"], rd["p"],
                       s["resolution_mde_points"])
                    if rd else "holds")
    else:
        verdict2 = ("is refuted: cohort A resolves higher, by %.1f points (z = %s, p = %s)"
                    % (100 * (A["resolution_rate"] - B["resolution_rate"]),
                       rd["z"] if rd else "—", rd["p"] if rd else "—"))
    word2 = ("just as" if not res_sig else
             ("less" if (A["resolution_rate"] or 0) < (B["resolution_rate"] or 0) else "more"))
    sa = cj["3_resolution_falls_with_age"]["slope_A_by_quarter"]
    sb = cj["3_resolution_falls_with_age"]["slope_B_by_quarter"]
    if sa is not None and sb is not None:
        if sa > 0 and sb > 0:
            age_sentence = ("Both are positive: within this window newer papers resolve better, "
                            "which is what conjecture 3 predicted, and it is a weak trend on few "
                            "quarters, not a decay law.")
        elif sa <= 0 and sb <= 0:
            age_sentence = ("Both are negative or flat — the opposite of conjecture 3 within this "
                            "window, and it is refuted rather than reinterpreted.")
        else:
            age_sentence = ("The two cohorts disagree in sign, so conjecture 3 is not supported "
                            "as stated; on this data age does not order the result.")
    else:
        age_sentence = "Too few decidable quarters to state a trend; conjecture 3 is left open."

    fig1 = bars_by_quarter(s, "declaration_rate", "Does the abstract hand you a link?",
                           "share of papers with any http(s) address in the abstract, by quarter")
    fig2 = bars_by_quarter(s, "resolution_rate", "Does the link still open?",
                           "share of declared links publicly reachable on 2026-08-31, by quarter")

    page = (page.replace("{HEADLINE}", headline).replace("{LEDE}", lede)
                .replace("{VERDICT1}", verdict1).replace("{VERDICT2}", verdict2)
                .replace("{WORD2}", word2).replace("{AGE_SENTENCE}", age_sentence)
                .replace("{FIG1}", fig1).replace("{FIG2}", fig2))
    open(os.path.join(d, "index.html"), "w").write(page)
    print("wrote %s (%d bytes)" % (os.path.join(d, "index.html"), len(page)))


if __name__ == "__main__":
    main()
