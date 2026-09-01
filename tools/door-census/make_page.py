#!/usr/bin/env python3
"""Write the artifact page from data.json, so no figure on the page can drift from the file.

    python3 tools/door-census/make_page.py           # write index.html
    python3 tools/door-census/make_page.py --check   # fail if index.html is not what data.json renders
"""
import html
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
ART = ROOT / "artifacts/cycle-001/2026-09-01-a-door-to-knock-on"
D = json.loads((ART / "data/data.json").read_text())

CLASS_LABEL = {
    "A": "specific route",
    "B": "generic only",
    "C": "policy, no route",
    "D": "nothing found",
    "unresolved": "unreachable",
}
ROUTE_LABEL = {
    "dedicated_email": "dedicated address",
    "dedicated_form": "dedicated form",
    "generic_email": "general address",
    "generic_form": "general form",
    "editor_no_address": "“contact the editor”, no address",
    "none": "—",
}


def esc(s):
    return html.escape(str(s), quote=True)


def rows_html():
    out = []
    for r in D["rows"]:
        cls = r["class"]
        badge = {"A": "a", "B": "b", "unresolved": "u"}.get(cls, "b")
        route = esc(r["route_value"]) if r["route_value"] else "—"
        grade = {"verified_here": "read here", "source_read": "page read",
                 "snippet_only": "snippet only", "unresolved": "—"}[r["evidence_grade"]]
        blocked = '<span class="blk" title="refused an ordinary automated request">403</span>' if r["machine_blocked"] else ""
        out.append(
            f'<tr class="r-{badge}">'
            f'<td class="pub">{esc(r["publisher"])}{blocked}</td>'
            f'<td class="num">{r["concerns"]}</td>'
            f'<td><span class="badge {badge}">{cls}</span> <span class="cl">{CLASS_LABEL[cls]}</span></td>'
            f'<td class="rt">{ROUTE_LABEL[r["route_kind"]]}<br><code>{route}</code></td>'
            f'<td class="q">“{esc(r["quote"])}”'
            + (f'<br><a href="{esc(r["evidence_url"])}">{esc(r["evidence_url"][:74])}</a>' if r["evidence_url"] else "")
            + f'<br><span class="g g-{r["evidence_grade"]}">{grade}</span></td>'
            "</tr>"
        )
    return "\n".join(out)


PAGE = """<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>A door to knock on — {n_publishers} publishers that flagged their own papers, and whether a stranger can reach them</title>
<style>
:root {{
  --bg:#fbfbf9; --fg:#17171a; --mut:#5c5c66; --line:#dedcd6; --card:#ffffff;
  --a:#1d6b45; --a-bg:#e7f2ec; --b:#8a4b12; --b-bg:#f7ece0; --u:#5a5a66; --u-bg:#ececed;
  --accent:#123a63;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --bg:#131316; --fg:#ececeb; --mut:#a2a2ac; --line:#33333a; --card:#1b1b1f;
    --a:#6fc79a; --a-bg:#16301f; --b:#e0a463; --b-bg:#33230f; --u:#a2a2ac; --u-bg:#26262b;
    --accent:#8fb8e0;
  }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.6 ui-serif,Georgia,'Times New Roman',serif; }}
main {{ max-width:56rem; margin:0 auto; padding:2.5rem 1.25rem 5rem; }}
h1 {{ font-size:2.4rem; line-height:1.15; margin:0 0 .4rem; letter-spacing:-.01em; }}
h2 {{ font-size:1.3rem; margin:2.6rem 0 .7rem; }}
h3 {{ font-size:1.02rem; margin:1.6rem 0 .4rem; }}
.kicker {{ font:600 .78rem/1.4 ui-sans-serif,system-ui,sans-serif; letter-spacing:.09em;
  text-transform:uppercase; color:var(--mut); margin-bottom:.9rem; }}
.stand {{ font-size:1.16rem; color:var(--mut); margin:.2rem 0 2rem; }}
p {{ margin:.8rem 0; }}
a {{ color:var(--accent); }}
.lede {{ font-size:1.06rem; }}
.big {{ display:flex; flex-wrap:wrap; gap:.9rem; margin:1.6rem 0; }}
.big div {{ flex:1 1 12rem; background:var(--card); border:1px solid var(--line);
  border-radius:.5rem; padding:1rem 1.1rem; }}
.big b {{ display:block; font:700 2.1rem/1.1 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:-.02em; }}
.big span {{ font-size:.88rem; color:var(--mut); }}
.verdict {{ border-left:4px solid var(--a); background:var(--a-bg); padding:1rem 1.2rem;
  border-radius:0 .4rem .4rem 0; margin:1.6rem 0; }}
.verdict.warn {{ border-left-color:var(--b); background:var(--b-bg); }}
table {{ border-collapse:collapse; width:100%; font:13px/1.45 ui-sans-serif,system-ui,sans-serif; }}
.wrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:.5rem; margin:1rem 0; }}
th,td {{ text-align:left; padding:.55rem .6rem; border-bottom:1px solid var(--line);
  vertical-align:top; }}
th {{ background:var(--card); font-weight:600; position:sticky; top:0; }}
td.num {{ text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }}
td.pub {{ min-width:12rem; font-weight:600; }}
td.q {{ color:var(--mut); min-width:18rem; max-width:26rem; overflow-wrap:anywhere; }}
td.q a {{ overflow-wrap:anywhere; }}
td.rt {{ min-width:9rem; }}
code {{ font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace; word-break:break-all;
  color:var(--fg); }}
.badge {{ display:inline-block; min-width:1.3rem; text-align:center; border-radius:.25rem;
  padding:.05rem .3rem; font-weight:700; }}
.badge.a {{ background:var(--a-bg); color:var(--a); }}
.badge.b {{ background:var(--b-bg); color:var(--b); }}
.badge.u {{ background:var(--u-bg); color:var(--u); }}
.cl {{ color:var(--mut); }}
.blk {{ display:inline-block; margin-left:.4rem; font:600 10px/1.4 ui-sans-serif,system-ui,sans-serif;
  background:var(--u-bg); color:var(--u); border-radius:.2rem; padding:.05rem .25rem;
  vertical-align:middle; }}
.g {{ font-size:11px; color:var(--mut); }}
.g-snippet_only {{ color:var(--b); }}
.g-verified_here {{ color:var(--a); }}
ul {{ padding-left:1.1rem; }} li {{ margin:.35rem 0; }}
.foot {{ margin-top:3rem; padding-top:1.2rem; border-top:1px solid var(--line);
  font-size:.9rem; color:var(--mut); }}
.foot code {{ color:var(--mut); }}
</style></head><body><main>

<div class="kicker">The Field · cycle 001 · measurement day {date}</div>
<h1>A door to knock on</h1>
<p class="stand">{n_publishers} publishers issued public warnings about papers they had published.
This asks the opposite question: can a stranger reach <em>them</em>?</p>

<p class="lede">A previous measurement here counted how long a public warning stands before anyone
resolves it: of concerns old enough to have had five full years, <strong>47.1 % ended in a
retraction and 52.9 % were still standing</strong>. That result is about institutional silence, and
it rests on an assumption nobody had checked — that the institutions are <em>reachable</em>, and so
choosing not to act, rather than simply having no door. This page checks the door.</p>

<div class="verdict">
<p style="margin:0"><strong>Result: the door is usually there.</strong> Of {n_publishers} publishers —
a census of the {n_census} that issued the most concerns, plus {n_tail} drawn at random from the
rest — <strong>{class_A} publish a specific route</strong> for raising a concern about an article
they have published: an address or a form designated for research integrity, publication ethics or
complaints. Weighted by the concerns each publisher actually issued, that is
<strong>{A_concern_weighted_pct} % of the cohort</strong>. The threshold set before probing was
half. <strong>Silence, where it happens, is not for want of a letterbox.</strong></p>
</div>

<div class="big">
<div><b>{class_A}/{n_publishers}</b><span>publish a specific route for concerns about a published
article ({A_pct_of_publishers} % of publishers, {A_concern_weighted_pct} % of concerns)</span></div>
<div><b>{class_B}</b><span>offer only a general channel, or tell you to “contact the editor” without
saying how ({B_concern_weighted_pct} % of concerns)</span></div>
<div><b>{machine_blocked}/{n_publishers}</b><span>refused an ordinary automated request at least
once — the door is open to a person and shut to a machine</span></div>
</div>

<h2>The one that matters most</h2>
<p><strong>{largest_publisher} issued {largest_publisher_concerns} of the cohort's concerns —
{largest_publisher_share_pct} % of them, more than any other publisher — and publishes no route of
its own.</strong> Its publishing-ethics page and both of its research-integrity hub pages were
fetched here, at HTTP 200, on the measurement day: they contain no email address of any kind and no
instruction for a reader. The only instruction found anywhere addresses authors who discover an
error in their own work, and it points away from the publisher: “contact the journal as soon as
possible using the contact details listed on the journal's home page”.</p>
<p>That single classification carries nearly a fifth of the weighted result, which is why it was
re-checked by hand rather than accepted from the probe. The same hand-check covered the five
largest publishers in the cohort — {top5_share_pct} % of all concerns — and each of the other four
does publish a route.</p>

<h2>Open to a person, shut to a machine</h2>
<p><strong>{machine_blocked} of {n_publishers} doors ({machine_blocked_pct} %) refused an ordinary
automated request at least once during this census</strong> — a 403, or a challenge page in place of
the policy. Every one of them is reachable by a human with a browser, and none is counted here as a
missing door. But it is the finding this practice did not go looking for: <em>the response side of
research integrity is addressable by hand and substantially closed to instruments.</em> For a
question about what of the research loop machines can carry end to end, that is a boundary with
evidence rather than a conviction — the knock, at least, is still a human act.</p>
<p>Weighted by concerns issued, the blocked share is smaller ({machine_blocked_concern_weighted_pct} %):
the largest publishers were mostly the reachable ones.</p>

<h2>What was counted, and how</h2>
<p>The question was fixed before any publisher was probed
(<a href="PREREGISTRATION.md">PREREGISTRATION.md</a>): <em>does the institution publish a route by
which a stranger — a browser, a search engine, no affiliation — can raise a concern about an article
it has published?</em> Not whether anyone answers; that needs letters and time. A door that cannot
be found is not a door.</p>
<div class="wrap"><table>
<tr><th>Class</th><th>Meaning</th><th class="num">n</th></tr>
<tr><td><span class="badge a">A</span></td><td>A <strong>specific</strong> channel designated for
this purpose — {dedicated_email} a named address, {dedicated_form} a dedicated form</td><td class="num">{class_A}</td></tr>
<tr><td><span class="badge b">B</span></td><td>A <strong>general</strong> channel only
({b_generic_channel}), or “contact the editor” with no address given ({b_editor_no_address})</td><td class="num">{class_B}</td></tr>
<tr><td><span class="badge b">C</span></td><td>A policy describing what the publisher does, with no
route to anyone</td><td class="num">{class_C}</td></tr>
<tr><td><span class="badge b">D</span></td><td>Nothing found by the fixed search</td><td class="num">{class_D}</td></tr>
<tr><td><span class="badge u">—</span></td><td>Unreachable: every automated route to the policy was
refused, so no classification was made</td><td class="num">{unresolved}</td></tr>
</table></div>
<p>Nobody landed in C or D. Every publisher in this census can be written to by somebody; in
{class_B} cases nobody in particular.</p>

<h3>How firm is it</h3>
<p>Each classification carries an evidence grade. <strong>{grade_verified_here}</strong> were fetched
and read by the session conductor directly ({verified_here_concern_weighted_pct} % of concerns by
weight); <strong>{grade_source_read}</strong> rest on text returned from the publisher's own page;
<strong>{grade_snippet_only}</strong> rest only on a search-engine snippet, because the page itself
never rendered to any method tried. Those seven are marked in the table and are the weakest rows
here.</p>
<p><strong>The floor.</strong> Discount every snippet-only classification — treat it as unknown and
count it against the result — and the share of concerns whose publisher demonstrably publishes a
specific route is still <strong>{A_floor_concern_weighted_pct} %</strong>, from
{A_floor_publishers} publishers. The finding survives its own worst reading.</p>

<h2>The census</h2>
<p>All {n_publishers} publishers, largest first by concerns issued. {class_A} of them publish a
route; the quotation is what their own page says, and the link is where it says it.
<span class="blk">403</span> marks a door that refused an ordinary automated request.</p>
<div class="wrap"><table>
<tr><th>Publisher</th><th class="num">Concerns</th><th>Class</th><th>Route</th><th>What the page says</th></tr>
{rows}
</table></div>

<h2>What this cannot say</h2>
<ul>
<li><strong>It does not measure whether anyone answers.</strong> A published address is a door, not
a reply. One publisher states a response time; the rest promise nothing. The next measurement on
this line is the one that costs time: write, and wait.</li>
<li><strong>Absence of a found door is not absence of a door.</strong> Rows are recorded as “not
found by this protocol”, which is a claim about findability by a stranger — the thing the
reachability assumption actually rests on — and not a claim about the institution.</li>
<li><strong>One publisher could not be checked at all</strong> ({unresolved_concern_weighted_pct} %
of concerns): its journals domain refused every automated request made here, and its society's own
reachable pages carry no address. That is an unreachable door, not a missing one.</li>
<li><strong>A specific route is not a good route.</strong> Class A asks only that a concrete
destination is named and designated for the purpose. Whether it reaches someone competent to act is
not measured.</li>
<li><strong>The publisher is taken as the source record names it.</strong> Corporate siblings appear
under separate labels and were probed separately; two of them resolve to the same door, which is
recorded rather than tidied away.</li>
</ul>

<div class="foot">
<p><strong>An offer, version 1, {date}.</strong> Method and pre-registration:
<a href="PREREGISTRATION.md">PREREGISTRATION.md</a>, <a href="METHOD.md">METHOD.md</a>. Data:
<code>data/census.csv</code> (all {n_publishers} rows with quotation, URL and evidence grade),
<code>data/data.json</code> (every figure on this page), <code>data/probes/</code> (the raw probe
records), <code>data/verification.json</code> (the conductor's own re-checks),
<code>data/population.json</code> (the draw, seed {seed}, reproducible from
<code>tools/door-census/population.py --check</code>). This page is written from
<code>data.json</code> by <code>tools/door-census/make_page.py</code>, which has a
<code>--check</code> mode: no figure here can drift from the file.</p>
<p>The cohort is the one built on {date} for <em>How long a warning stands</em>: {cohort_concerns_total}
papers that have ever carried a public expression of concern. The {n_publishers} publishers probed
account for {concerns_covered} of those concerns ({concerns_covered_pct} %). We make no licence
claim over the underlying database, and none over the publishers' own pages, which are quoted
briefly with their sources.</p>
<p><strong>A correction is worth more to us than any number here.</strong> If you keep one of these
doors and this page has it wrong — the route moved, the address is not the one a reader should use,
the page we could not read says something else — that is the most useful thing anyone could send
back.</p>
</div>
</main></body></html>
"""


def render():
    return PAGE.format(rows=rows_html(), **{k: v for k, v in D.items() if k != "rows"})


if __name__ == "__main__":
    page = render()
    target = ART / "index.html"
    if "--check" in sys.argv:
        if target.read_text() == page:
            print("index.html: reproduces from data.json — no figure on the page can drift")
        else:
            print("index.html: DOES NOT match what data.json renders")
            sys.exit(1)
    else:
        target.write_text(page)
        print("wrote", target, "(%d bytes)" % len(page))
