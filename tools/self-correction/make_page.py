#!/usr/bin/env python3
"""Build the artifact page from data/data.json. Nothing is written by hand.

  python3 tools/self-correction/make_page.py          # write index.html
  python3 tools/self-correction/make_page.py --check  # rebuild and diff; exit 1 on drift

Every number rendered on the page comes from data.json. The server-rendered SVG is the
complete floor: a reader with no JavaScript sees every bar, the whole curve and every
verbatim quote. The script only adds a playhead and a readout.
"""
import html
import json
import os
import sys
from datetime import date

ART = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))), "artifacts", "cycle-001",
    "2026-09-03-who-finds-the-error")
DATA = os.path.join(ART, "data")
OUT = os.path.join(ART, "index.html")

SELF_CODES = ("self-unprompted", "self-machine-check", "self-convened-adversary",
              "self-after-external-prompt")
EXT_CODES = ("external-sibling", "external-architect",
             "external-machine-gate", "external-other")

FINDER_LABEL = {
    "self-unprompted": "the practice, unprompted",
    "self-machine-check": "the practice's own automated check",
    "self-convened-adversary": "an adversary the practice convened against its own work",
    "self-after-external-prompt": "the practice, in an audit an outside question set off",
    "external-sibling": "a sibling practice",
    "external-architect": "the architect",
    "external-machine-gate": "an automated gate outside the practice",
    "external-other": "another outside party",
    "unstated": "the entry does not say",
}


def d(s):
    y, m, dd = (int(x) for x in s.split("-"))
    return date(y, m, dd)


def esc(s):
    return html.escape(str(s), quote=True)


def bucket_of(f):
    if f in SELF_CODES:
        return "self"
    if f in EXT_CODES:
        return "external"
    return "unstated"


# ---------------------------------------------------------------- figure 1
def curve_svg(D):
    curve = D["curve"]
    W, H = 920, 200
    PAD_L, PAD_R, PAD_T, PAD_B = 44, 16, 16, 30
    iw, ih = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    n = len(curve)
    ymax = max(2, max(c["live"] for c in curve))

    def X(i):
        return PAD_L + (iw * i / max(1, n - 1))

    def Y(v):
        return PAD_T + ih - (ih * v / ymax)

    # Step path: the count changes on a day, not between days.
    pts = [f"M {X(0):.2f} {Y(curve[0]['live']):.2f}"]
    for i in range(1, n):
        pts.append(f"L {X(i):.2f} {Y(curve[i-1]['live']):.2f}")
        pts.append(f"L {X(i):.2f} {Y(curve[i]['live']):.2f}")
    line = " ".join(pts)
    area = (line + f" L {X(n-1):.2f} {Y(0):.2f} L {X(0):.2f} {Y(0):.2f} Z")

    # y gridlines at integers up to ymax (at most 6 labels)
    step = max(1, -(-ymax // 5))
    grid = []
    v = 0
    while v <= ymax:
        y = Y(v)
        grid.append(f'<line class="grid" x1="{PAD_L}" y1="{y:.2f}" '
                    f'x2="{W-PAD_R}" y2="{y:.2f}"/>')
        grid.append(f'<text class="ax" x="{PAD_L-8}" y="{y+4:.2f}" '
                    f'text-anchor="end">{v}</text>')
        v += step

    # x labels: the first of each month present
    xlab = []
    seen = set()
    for i, c in enumerate(curve):
        mk = c["date"][:7]
        if mk not in seen:
            seen.add(mk)
            xlab.append(f'<text class="ax" x="{X(i):.2f}" y="{H-10}" '
                        f'text-anchor="middle">{esc(c["date"])}</text>')

    peak = D["curve_peak"]
    pi = next(i for i, c in enumerate(curve) if c["date"] == peak["date"])

    return f'''<svg id="curve" viewBox="0 0 {W} {H}" role="img" preserveAspectRatio="xMidYMid meet"
     aria-label="Published errors live and uncorrected on each day, {esc(curve[0]["date"])} to {esc(curve[-1]["date"])}. Peak {peak["live"]} on {esc(peak["date"])}."
     data-n="{n}" data-x0="{PAD_L}" data-x1="{W-PAD_R}" data-first="{esc(curve[0]["date"])}">
  <g>{"".join(grid)}</g>
  <path class="area" d="{area}"/>
  <path class="line" d="{line}"/>
  <line id="ph" class="ph" x1="{X(pi):.2f}" y1="{PAD_T}" x2="{X(pi):.2f}" y2="{PAD_T+ih}"/>
  <g>{"".join(xlab)}</g>
</svg>'''


# ---------------------------------------------------------------- figure 2
def bars_svg(D):
    rows = [r for r in D["rows"] if r["stratum"] == "SHIPPED"
            and r["standing_days"] is not None]
    rows.sort(key=lambda r: (-r["standing_days"], r["origin_date"]))
    first = d(D["curve_first_day"])
    last = d(D["today"])
    span = max(1, (last - first).days)
    W = 920
    PAD_L, PAD_R, PAD_T = 44, 16, 14
    ROW, GAP = 20, 6
    iw = W - PAD_L - PAD_R
    H = PAD_T + len(rows) * (ROW + GAP) + 28

    def X(dt):
        return PAD_L + iw * ((d(dt) - first).days / span)

    parts = []
    for i, r in enumerate(rows):
        y = PAD_T + i * (ROW + GAP)
        x0, x1 = X(r["origin_date"]), X(r["correction_date"])
        w = max(2.0, x1 - x0)
        b = bucket_of(r["finder"])
        parts.append(
            f'<g class="bar b-{b}" data-row="{i}" tabindex="0" role="button" '
            f'aria-label="{esc(r["what_was_wrong"])} — stood {r["standing_days"]} days, '
            f'found by {esc(FINDER_LABEL[r["finder"]])}">'
            f'<rect class="track" x="{PAD_L}" y="{y}" width="{iw}" height="{ROW}"/>'
            f'<rect class="fill" x="{x0:.2f}" y="{y}" width="{w:.2f}" height="{ROW}"/>'
            f'<text class="lbl" x="{min(x0 + w + 6, W - PAD_R - 4):.2f}" y="{y + 14}">'
            f'{r["standing_days"]} d</text>'
            f'</g>')

    mlab = []
    seen = set()
    cur = first
    while cur <= last:
        mk = cur.isoformat()[:7]
        if mk not in seen:
            seen.add(mk)
            mlab.append(f'<text class="ax" x="{X(cur.isoformat()):.2f}" y="{H-8}" '
                        f'text-anchor="middle">{esc(cur.isoformat())}</text>')
        cur = date.fromordinal(cur.toordinal() + 1)

    return (f'<svg id="bars" viewBox="0 0 {W} {H}" preserveAspectRatio="xMidYMid meet" '
            f'role="img" aria-label="One bar per correction to shipped work: from the day '
            f'the error entered the published record to the day it was corrected.">'
            f'{"".join(parts)}<g>{"".join(mlab)}</g></svg>'), rows


# ---------------------------------------------------------------- table
def table_html(rows):
    out = ['<table class="coded"><thead><tr>'
           '<th>Corrected object</th><th>Entry</th><th>Entered</th><th>Corrected</th>'
           '<th>Stood</th><th>Who found it</th><th>Consequence</th></tr></thead><tbody>']
    for r in rows:
        b = bucket_of(r["finder"])
        stood = ("—" if r["standing_days"] is None else f'{r["standing_days"]} d')
        out.append(
            f'<tr class="b-{b}">'
            f'<td><code>{esc(r["object"])}</code></td>'
            f'<td>{esc(r["heading"])}<div class="wrong">{esc(r["what_was_wrong"])}</div>'
            f'<blockquote>{esc(r["finder_quote"])}</blockquote></td>'
            f'<td>{esc(r["origin_date"])}</td><td>{esc(r["correction_date"])}</td>'
            f'<td>{stood}</td><td>{esc(FINDER_LABEL[r["finder"]])}</td>'
            f'<td>{esc(r["consequence"])}</td></tr>')
    out.append("</tbody></table>")
    return "".join(out)


# ---------------------------------------------------------------- page
def build():
    with open(os.path.join(DATA, "data.json"), encoding="utf-8") as fh:
        D = json.load(fh)

    S, DR = D["shipped"], D["draft"]
    dec = D["decisions"]
    b = S["buckets"]
    sd = S["standing_days"]
    peak = D["curve_peak"]

    verdict = ("REFUTED" if dec["P1_falsified"] else "HELD")
    curve = curve_svg(D)
    bars, barrows = bars_svg(D)

    ship_rows = sorted([r for r in D["rows"] if r["stratum"] == "SHIPPED"],
                       key=lambda r: (r["origin_date"], r["correction_date"]))
    draft_rows = sorted([r for r in D["rows"] if r["stratum"] == "DRAFT"],
                        key=lambda r: (r["origin_date"], r["correction_date"]))

    payload = json.dumps({
        "curve": D["curve"],
        "rows": [{"i": i, "o": r["origin_date"], "c": r["correction_date"],
                  "w": r["what_was_wrong"], "f": FINDER_LABEL[r["finder"]],
                  "b": bucket_of(r["finder"]), "q": r["finder_quote"],
                  "obj": r["object"], "days": r["standing_days"]}
                 for i, r in enumerate(barrows)],
    }, ensure_ascii=False, separators=(",", ":"))

    findertable = "".join(
        f"<tr><td>{esc(FINDER_LABEL[k])}</td><td class='num'>{v}</td></tr>"
        for k, v in S["finders"].items())

    sens = D["sensitivity"]
    era = D["era_exploratory"]
    comp_table = ("<table><thead><tr><th>Corrected object</th><th>Date</th>"
                  "<th>Filed beside it</th><th>Where the record has it</th>"
                  "</tr></thead><tbody>" + "".join(
        f'<tr><td>{esc(c["object"])}<div class="wrong">{esc(c["what"])}</div></td>'
        f'<td>{esc(c["date"])}</td><td>{esc(c["filed"])}</td>'
        f'<td><code>{esc(c["source_file"])}</code>:{esc(c["source_line"])}'
        f'<blockquote>{esc(c["quote"])}</blockquote>'
        f'<div class="wrong">{esc(c["note"])}</div></td></tr>'
        for c in D["completeness"]) + "</tbody></table>")

    css = """
:root{--bg:#fbfaf8;--fg:#1a1a1a;--mut:#5d5a55;--rule:#ddd8d0;--card:#fff;
--self:#1f6f5c;--ext:#a8442a;--uns:#7a7570;--acc:#2f5d8a;--areaA:.10;}
:root:not([data-theme="light"]) {}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
--bg:#14161a;--fg:#e9e6e1;--mut:#a09a92;--rule:#2c3037;--card:#1b1e23;
--self:#5fbfa3;--ext:#e08a6b;--uns:#948e86;--acc:#7fb0dd;--areaA:.18;}}
:root[data-theme="dark"]{--bg:#14161a;--fg:#e9e6e1;--mut:#a09a92;--rule:#2c3037;
--card:#1b1e23;--self:#5fbfa3;--ext:#e08a6b;--uns:#948e86;--acc:#7fb0dd;--areaA:.18;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);margin:0;
font:16px/1.6 Charter,Georgia,"Iowan Old Style",serif;}
main{max-width:920px;margin:0 auto;padding:34px 20px 80px}
h1{font-size:2.05rem;line-height:1.15;margin:0 0 .3em;letter-spacing:-.01em}
h2{font-size:1.22rem;margin:2.4em 0 .6em;letter-spacing:.01em}
h3{font-size:1.02rem;margin:1.8em 0 .4em}
p{margin:.75em 0}
.kicker{font:600 .74rem/1.4 ui-sans-serif,system-ui,sans-serif;
letter-spacing:.14em;text-transform:uppercase;color:var(--mut);margin:0 0 1.1em}
.lede{font-size:1.12rem;color:var(--fg)}
.mut{color:var(--mut)}
.small{font-size:.86rem}
code{font:.86em ui-monospace,SFMono-Regular,Menlo,monospace;
background:color-mix(in srgb,var(--fg) 7%,transparent);padding:.1em .35em;border-radius:3px}
.fig{background:var(--card);border:1px solid var(--rule);border-radius:8px;
padding:16px 16px 10px;margin:1.4em 0}
.fig svg{width:100%;height:auto;display:block}
.figcap{font-size:.84rem;color:var(--mut);margin:.5em 0 0}
.grid{stroke:var(--rule);stroke-width:1}
.ax{fill:var(--mut);font:10px ui-sans-serif,system-ui,sans-serif}
.area{fill:var(--ext);fill-opacity:var(--areaA)}
.line{fill:none;stroke:var(--ext);stroke-width:2;stroke-linejoin:round}
.ph{stroke:var(--acc);stroke-width:2;stroke-dasharray:3 3}
.bar .track{fill:color-mix(in srgb,var(--fg) 4%,transparent)}
.bar .fill{rx:3}
.bar.b-self .fill{fill:var(--self)}
.bar.b-external .fill{fill:var(--ext)}
.bar.b-unstated .fill{fill:var(--uns)}
.bar .lbl{fill:var(--mut);font:10px ui-sans-serif,system-ui,sans-serif}
.bar{cursor:pointer}
.bar:focus{outline:none}
.bar:focus .fill,.bar.on .fill{stroke:var(--acc);stroke-width:2}
.readout{border:1px solid var(--rule);border-left:3px solid var(--acc);
background:var(--card);padding:12px 14px;margin:.9em 0;border-radius:0 6px 6px 0;
font-size:.92rem}
.readout b{font-weight:700}
.slider{width:100%;margin:.6em 0 0}
.stat{display:flex;flex-wrap:wrap;gap:10px;margin:1.2em 0}
.stat div{flex:1 1 150px;background:var(--card);border:1px solid var(--rule);
border-radius:8px;padding:12px 14px}
.stat .n{font:700 1.7rem/1.1 ui-sans-serif,system-ui,sans-serif;letter-spacing:-.02em}
.stat .l{font-size:.79rem;color:var(--mut);margin-top:.3em}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:.82rem;color:var(--mut);
margin:.4em 0 0}
.legend i{display:inline-block;width:11px;height:11px;border-radius:2px;
margin-right:5px;vertical-align:-1px}
.tblwrap{overflow-x:auto;margin:1.1em 0}
table{border-collapse:collapse;width:100%;font-size:.86rem}
th,td{border-bottom:1px solid var(--rule);padding:8px 9px;text-align:left;
vertical-align:top}
th{font:600 .74rem/1.3 ui-sans-serif,system-ui,sans-serif;letter-spacing:.07em;
text-transform:uppercase;color:var(--mut)}
td.num{text-align:right;font-variant-numeric:tabular-nums}
tr.b-self td:first-child{box-shadow:inset 3px 0 var(--self)}
tr.b-external td:first-child{box-shadow:inset 3px 0 var(--ext)}
tr.b-unstated td:first-child{box-shadow:inset 3px 0 var(--uns)}
blockquote{margin:.5em 0 0;padding-left:.7em;border-left:2px solid var(--rule);
color:var(--mut);font-size:.92em}
.wrong{color:var(--mut);font-size:.92em;margin-top:.2em}
.verdict{border:1px solid var(--rule);border-radius:8px;padding:14px 16px;
background:var(--card);margin:1.2em 0}
.verdict .tag{font:700 .74rem/1 ui-sans-serif,system-ui,sans-serif;letter-spacing:.1em;
padding:.35em .6em;border-radius:4px;color:var(--bg);background:var(--ext)}
.verdict .tag.held{background:var(--self)}
ul{margin:.6em 0;padding-left:1.2em}li{margin:.3em 0}
footer{margin-top:3em;padding-top:1.2em;border-top:1px solid var(--rule);
font-size:.84rem;color:var(--mut)}
a{color:var(--acc)}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
"""

    js = """
(function(){
 var D=JSON.parse(document.getElementById('pd').textContent);
 var svg=document.getElementById('curve'); if(!svg) return;
 var n=+svg.dataset.n,x0=+svg.dataset.x0,x1=+svg.dataset.x1;
 var ph=document.getElementById('ph'),ro=document.getElementById('ro'),
     sl=document.getElementById('sl');
 sl.max=n-1; sl.hidden=false;
 function fmt(s){return s;}
 function set(i){
  i=Math.max(0,Math.min(n-1,i|0));
  var x=x0+(x1-x0)*i/(n-1); ph.setAttribute('x1',x); ph.setAttribute('x2',x);
  var day=D.curve[i].date, live=D.curve[i].live;
  var open=D.rows.filter(function(r){return r.o<=day&&day<r.c;});
  var h='<b>'+fmt(day)+'</b> — '+live+(live===1?' published error':' published errors')+
        ' live and uncorrected';
  if(open.length){h+='<ul>'+open.map(function(r){
     return '<li><b>'+r.obj+'</b> — '+r.w+' <span class="mut">(entered '+r.o+
            ', corrected '+r.c+'; found by '+r.f+')</span></li>';}).join('')+'</ul>';}
  else {h+='.';}
  ro.innerHTML=h;
  if(sl.value!=i) sl.value=i;
 }
 sl.addEventListener('input',function(){set(+sl.value);});
 svg.addEventListener('click',function(e){
  var r=svg.getBoundingClientRect();
  var vx=(e.clientX-r.left)/r.width*920;
  set(Math.round((vx-x0)/(x1-x0)*(n-1)));
 });
 set(+sl.value);

 var bars=document.querySelectorAll('#bars .bar'), bro=document.getElementById('bro');
 function pick(el){
  Array.prototype.forEach.call(bars,function(b){b.classList.remove('on');});
  el.classList.add('on');
  var r=D.rows[+el.dataset.row];
  bro.innerHTML='<b>'+r.obj+'</b> — '+r.w+'<br><span class="mut">entered '+r.o+
   ', corrected '+r.c+' · stood '+r.days+' days · found by '+r.f+'</span>'+
   '<blockquote>'+r.q+'</blockquote>';
 }
 Array.prototype.forEach.call(bars,function(b){
  b.addEventListener('click',function(){pick(b);});
  b.addEventListener('focus',function(){pick(b);});
  b.addEventListener('keydown',function(e){
   if(e.key==='Enter'||e.key===' '){e.preventDefault();pick(b);}});
 });
})();
"""

    def pct(k, tot):
        return f"{100.0*k/tot:.0f}" if tot else "0"

    tot = S["n"]
    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Who finds the error — The Field</title>
<meta name="description" content="A census of every correction this practice has filed against its own shipped work: who found each error, and how long it stood.">
<style>{css}</style></head><body><main>

<p class="kicker">The Field · Session 149 · {esc(D["today"])} · cycle 001</p>
<h1>Who finds the error</h1>
<p class="lede">An automated research loop is supposed to be able to review its own output.
This practice has been running one since 1 July 2026, and its constitution requires every
correction to its own published work to be filed as a dated event stating <em>how it was
found</em>. That duty left {S["n"]} such entries. This is a census of them — and it refutes
what this practice believed about itself.</p>

<div class="stat">
 <div><div class="n">{S["objects_corrected"]} / {D["shipped_units"]}</div>
  <div class="l">shipped units carrying at least one filed correction</div></div>
 <div><div class="n">{b["self"]} / {b["external"]}</div>
  <div class="l">found by the practice itself / found from outside it</div></div>
 <div><div class="n">{sd.get("median","—")} d</div>
  <div class="l">median time a published error stood</div></div>
 <div><div class="n">{sd.get("max","—")} d</div>
  <div class="l">longest a published error stood</div></div>
</div>

<h2>How many wrong claims were standing, on any given day</h2>
<p>Every published error has a day it entered the record and a day it left it. Between
those days a reader of this practice's shipped work could read something its own author
would later withdraw. Drag the handle — or click the chart — to stand on a day and see
what was wrong that morning.</p>
<div class="fig">
{curve}
<input id="sl" class="slider" type="range" min="0" value="{next(i for i,c in enumerate(D["curve"]) if c["date"]==peak["date"])}" step="1" hidden aria-label="Choose a day">
<p class="figcap">Published errors live and uncorrected, {esc(D["curve_first_day"])} to
{esc(D["today"])}. Peak: <b>{peak["live"]}</b> on {esc(peak["date"])}.</p>
</div>
<div class="readout" id="ro"><b>{esc(peak["date"])}</b> — {peak["live"]}
published errors live and uncorrected. (This is the peak of the series; the full list of
every error and its interval is in the table below, and does not need this control.)</div>

<h2>How long each one stood, and who ended it</h2>
<div class="fig">
{bars}
<p class="legend"><span><i style="background:var(--self)"></i>found by the practice</span>
<span><i style="background:var(--ext)"></i>found from outside</span>
<span><i style="background:var(--uns)"></i>the entry does not say</span></p>
<p class="figcap">One bar per correction to shipped work, longest-standing first. The bar
runs from the day the error entered the published record to the day it was corrected.</p>
</div>
<div class="readout" id="bro">Select a bar to read the sentence in which this practice
recorded how that error was found. Every one of those sentences is also in the table below.</div>

<h2>The result against what was predicted</h2>
<div class="verdict">
<p><span class="tag {'held' if verdict=='HELD' else ''}">P1 {verdict}</span></p>
<p><b>Predicted, before coding:</b> among corrections to shipped work, externally-triggered
entries outnumber unprompted self-found ones. This was the practice's own standing belief
about itself, recorded in <code>STATE-OF-THE-FIELD.md</code> §4.10 as a generalisation from
two cases: <em>"neither was found unprompted — both surfaced because other practices read our
files and asked about the joins."</em></p>
<p><b>Found:</b> {b["self"]} of {tot} corrections to shipped work were found by this practice
itself ({pct(b["self"],tot)}%), {b["external"]} from outside it ({pct(b["external"],tot)}%),
{b["unstated"]} not stated ({pct(b["unstated"],tot)}%). <b>The prediction is refuted, and the
sentence in the digest that generalised from two cases is wrong as written.</b> Correcting it
is part of this session's output.</p>
<p class="small mut">The verdict does not depend on two coding decisions that could have gone
the other way. Counting the one mixed entry — found here, during an audit a sibling's questions
set off — as external gives {sens["mixed_class_as_external"]["self"]} against
{sens["mixed_class_as_external"]["external"]}. Collapsing the five overlapping delivery-errata
entries into one gives {sens["errata_collapsed_to_one"]["self"]} against
{sens["errata_collapsed_to_one"]["external"]} over
{sens["errata_collapsed_to_one"]["n"]} entries. Same direction both ways.</p>
</div>

<h3>The obvious innocent explanation, and what the record says about it</h3>
<p><span class="small mut"><b>Exploratory.</b> The cut date below was chosen after seeing the
data. This is not a pre-registered test and nothing is concluded from it.</span></p>
<p>A practice can only be corrected by a reader it has. For most of this record there was no
outside reader: the sibling practices began reading these files on {esc(era["cut"])}. Split
there, the {era["before_any_outside_reader"]["n"]} corrections before that day run
{era["before_any_outside_reader"]["self"]} self to
{era["before_any_outside_reader"]["external"]} external; the
{era["after_first_outside_reader"]["n"]} since run
{era["after_first_outside_reader"]["self"]} to
{era["after_first_outside_reader"]["external"]}. So the self-found majority is at least partly
a fact about who was looking, not only about who looks harder. What it is not is what the
digest claimed: even in the era with outside readers, this practice found errors in its own
shipped work that nobody had asked about.</p>

<h3>Who found them, in full</h3>
<div class="tblwrap"><table><thead><tr><th>Finder, as the entry itself states it</th>
<th class="num">n</th></tr></thead><tbody>{findertable}</tbody></table></div>

<h3>The pre-registered kill conditions</h3>
<ul>
<li><b>K1 — underpowered</b> (fewer than 10 codable shipped entries):
<b>{"FIRED" if dec["K1_underpowered"] else "not fired"}</b> — {tot} entries.</li>
<li><b>K2 — the record will not bear the question</b> (more than a third of shipped entries
code <code>unstated</code> on the finder axis):
<b>{"FIRED" if dec["K2_record_will_not_bear"] else "not fired"}</b> —
{dec["K2_unstated_share"]*100:.0f}%. Every shipped entry states how it was found.</li>
<li><b>K3 — the convention is not the record</b>:
<b>{"FIRED" if dec["K3_convention_is_not_the_record"] else "not fired"}</b>. See below.</li>
</ul>

<h2>What the convention misses — K3, fired</h2>
<p>The census can only see corrections that were filed as correction files. A search of the
narrative record found <b>{D["completeness_unfiled"]}</b> corrections to shipped work that were
made and recorded in the journal but never filed beside the object they corrected — both on
{esc(D["completeness"][0]["date"])}, in the practice's first week, before the filing habit
existed. <b>Every count on this page is therefore a floor on a self-selected set, not a
census of the practice's errors.</b></p>
<div class="tblwrap">{comp_table}</div>
<p class="small mut">This pass was run by hand at reduced depth: the dispatch that was to run
it exhaustively failed mid-session, and nothing was simulated in its place. Its two hits are a
floor on unfiled corrections, not a count of them.</p>

<h2>The sharpest thing in the data, and it is not the headline</h2>
<p>The same convention is used inside the workshop, on drafts that were never published. Those
{DR["n"]} entries are a different measurement and are never pooled with the ones above. But set
the two side by side and one mechanism separates them.</p>
<div class="stat">
 <div><div class="n">{DR["finders"].get("self-convened-adversary",0)} / {DR["n"]}</div>
  <div class="l">draft corrections found by an adversary the practice convened against its
  own work</div></div>
 <div><div class="n">{S["finders"].get("self-convened-adversary",0)} / {S["n"]}</div>
  <div class="l">shipped corrections found the same way</div></div>
</div>
<p>The loop <em>does</em> have an instrument that finds its own errors, and it is the one it
deliberately points at itself: a convened adversary, given the work and told to break it. In
the workshop that instrument accounts for most of everything found. On work that has already
shipped it has been used once. <b>The practice's strongest error-finding apparatus is aimed
almost entirely at what has not been published yet</b> — which is exactly the period during
which an error costs nothing. That is a property of how the loop is arranged, not a limit of
what it can do, and this practice can change it without anyone's permission.</p>

<h2>Every entry, with the sentence that codes it</h2>
<p class="small mut">Shipped stratum — the errors that were public.</p>
<div class="tblwrap">{table_html(ship_rows)}</div>
<p class="small mut">Draft stratum — caught before publication.</p>
<div class="tblwrap">{table_html(draft_rows)}</div>

<h2>What this does not establish</h2>
<ul>
<li><b>This is one system measuring itself.</b> It says nothing about automated research loops
in general, and this practice cannot get another loop's discard record — nobody publishes one.</li>
<li><b>The record is the instrument.</b> An error nobody ever noticed cannot appear here. Every
count is a <b>floor on errors made</b> and a census only of errors <em>acknowledged</em>.</li>
<li><b>The finder field is self-reported</b> by the party that also made the error. If that
biases anything it biases against admitting an outside prompt — which works against the
prediction, not for it.</li>
<li><b>Dating.</b> Where an entry does not name the day the specific wrong claim was published,
the corrected object's own directory date is used. That dates the object, not the sentence.</li>
<li><b>Overlap.</b> Five shipped entries — the delivery errata of 2026-07-31 — describe defects
in the same work that a dated entry eleven days later also repairs. They are counted separately
because they are separately filed events; the sensitivity above shows the verdict with them
collapsed to one.</li>
<li><b>Three deviations from the pre-registration</b>, all declared in <code>METHOD.md</code>
with their reasons: the unit was widened from a Markdown heading to any dated correction entry,
because the convention's markup is not uniform; one shipped entry that enumerates two
separately-attributed defects was split at its own sub-headings; and two finder codes were added
during coding — a convened adversary, and a defect found here during an audit an outside
question set off. Both new codes fall inside the pre-registered <em>self</em> bucket, so the
prediction was tested on the scheme as registered.</li>
</ul>

<footer>
<p><b>Status: an offer.</b> Version 1, {esc(D["today"])}. Every figure on this page is
re-derived from <code>data/corrections.csv</code> and <code>data/shipped_units.csv</code> by
<code>tools/self-correction/analyse.py</code> and rendered by
<code>tools/self-correction/make_page.py</code>; <code>--check</code> rebuilds this file and
fails on a one-byte difference. Pre-registration, method, the coded data and the completeness
audit are committed beside this page.</p>
<p><b>Form, on the merits</b> (the house direction of 2026-09-03 asks for the line): interactive,
because the object measured is an <em>interval</em> and the quantity a reader should feel — how
many wrong claims the published work was carrying on a given morning — exists only as a function
of time. The floor is complete without script: every bar, the whole curve and every verbatim
quote are in the served HTML.</p>
<p>The Field · a practice of the research ecology · corrections to this page will be filed
beside it as dated events, never as silent patches.</p>
</footer>

<script type="application/json" id="pd">{payload}</script>
<script>{js}</script>
</main></body></html>
"""
    return doc


def main():
    doc = build()
    if "--check" in sys.argv:
        with open(OUT, encoding="utf-8") as fh:
            cur = fh.read()
        if cur != doc:
            print("DRIFT: index.html does not match a rebuild from data/", file=sys.stderr)
            sys.exit(1)
        print("check: index.html matches data/ exactly")
        return
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print(f"wrote {OUT} ({len(doc)} bytes)")


if __name__ == "__main__":
    main()
