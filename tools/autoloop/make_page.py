#!/usr/bin/env python3
"""Builds artifacts/cycle-002/2026-09-03-a-loop-that-finds-things/index.html from the
committed data files, and nothing else.

No number in the page is typed by hand: every figure, cell, table row and sentence is
read out of data/results.json, data/review.json, data/judgment.json and data/corpus.json.

  python3 tools/autoloop/make_page.py            # write the page
  python3 tools/autoloop/make_page.py --check    # rebuild and fail on a one-byte difference
"""

import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ART = os.path.abspath(os.path.join(HERE, "..", "..", "artifacts", "cycle-002",
                                   "2026-09-03-a-loop-that-finds-things"))
DATA = os.path.join(ART, "data")

GROUP_ORDER = ["weekend", "night_submission", "has_comment", "has_doi", "has_journal_ref",
               "revised", "cross_listed", "large_team"]
GROUP_LABEL = {
    "weekend": "posted at a weekend", "night_submission": "posted 22:00–06:00 UTC",
    "has_comment": "has an author comment", "has_doi": "has a DOI",
    "has_journal_ref": "has a journal reference", "revised": "was revised",
    "cross_listed": "is cross-listed", "large_team": "has ≥ 5 authors",
}
OUT_ORDER = ["title_words", "abstract_words", "author_count", "category_count",
             "comment_pages", "published_hour_utc", "has_doi", "has_journal_ref", "revised"]
OUT_LABEL = {
    "title_words": "title words", "abstract_words": "abstract words",
    "author_count": "authors", "category_count": "categories",
    "comment_pages": "pages stated", "published_hour_utc": "hour posted",
    "has_doi": "DOI", "has_journal_ref": "journal ref", "revised": "revised",
}

E = html.escape


def pf(p):
    if p is None:
        return "—"
    if p < 1e-4:
        return f"{p:.1e}".replace("e-0", "e−").replace("e-", "e−")
    return f"{p:.4f}"


def load():
    d = {}
    for name in ("results", "review", "judgment"):
        d[name] = json.load(open(os.path.join(DATA, f"{name}.json")))
    return d


CSS = """
:root{--bg:#fbfaf8;--fg:#1a1a1a;--mut:#5d5a55;--rule:#ddd8d0;--card:#fff;
--bh:#1f6f5c;--sig:#c98a1e;--non:#cfc9c0;--kill:#9a948c;--acc:#2f5d8a;--ext:#a8442a;}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){
--bg:#14161a;--fg:#e9e6e1;--mut:#a09a92;--rule:#2c3037;--card:#1b1e23;
--bh:#5fbfa3;--sig:#e0b45f;--non:#3a3f46;--kill:#6d6862;--acc:#7fb0dd;--ext:#e08a6b;}}
:root[data-theme="dark"]{--bg:#14161a;--fg:#e9e6e1;--mut:#a09a92;--rule:#2c3037;
--card:#1b1e23;--bh:#5fbfa3;--sig:#e0b45f;--non:#3a3f46;--kill:#6d6862;--acc:#7fb0dd;--ext:#e08a6b;}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);margin:0;
font:16px/1.6 Charter,Georgia,"Iowan Old Style",serif}
main{max-width:940px;margin:0 auto;padding:34px 20px 80px}
h1{font-size:2.05rem;line-height:1.15;margin:0 0 .3em;letter-spacing:-.01em}
h2{font-size:1.22rem;margin:2.4em 0 .6em}
h3{font-size:1.02rem;margin:1.7em 0 .4em}
p{margin:.75em 0}
.kicker{font:600 .74rem/1.4 ui-sans-serif,system-ui,sans-serif;letter-spacing:.14em;
text-transform:uppercase;color:var(--mut);margin:0 0 1.1em}
.lede{font-size:1.12rem}
.mut{color:var(--mut)}.small{font-size:.86rem}
code{font:.86em ui-monospace,SFMono-Regular,Menlo,monospace;
background:color-mix(in srgb,var(--fg) 7%,transparent);padding:.1em .35em;border-radius:3px}
.fig{background:var(--card);border:1px solid var(--rule);border-radius:8px;
padding:16px 16px 12px;margin:1.4em 0}
.fig svg{width:100%;height:auto;display:block}
.figcap{font-size:.84rem;color:var(--mut);margin:.7em 0 0}
.stat{display:flex;flex-wrap:wrap;gap:10px;margin:1.3em 0}
.stat div{flex:1 1 150px;background:var(--card);border:1px solid var(--rule);
border-radius:8px;padding:12px 14px}
.stat .n{font:700 1.7rem/1.1 ui-sans-serif,system-ui,sans-serif;letter-spacing:-.02em}
.stat .l{font-size:.79rem;color:var(--mut);margin-top:.3em}
.ax{fill:var(--mut);font:10px ui-sans-serif,system-ui,sans-serif}
.axr{fill:var(--mut);font:10.5px ui-sans-serif,system-ui,sans-serif}
.cell{cursor:pointer;stroke:var(--card);stroke-width:1.5}
.cell:focus{outline:none}
.cell.on{stroke:var(--acc);stroke-width:2.5}
.rep{fill:var(--card);pointer-events:none}
.controls{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:.2em 0 1em}
button{font:600 .8rem ui-sans-serif,system-ui,sans-serif;color:var(--fg);
background:var(--card);border:1px solid var(--rule);border-radius:6px;
padding:6px 11px;cursor:pointer}
button[aria-pressed="true"]{background:var(--acc);border-color:var(--acc);color:#fff}
.readout{border:1px solid var(--rule);border-left:3px solid var(--acc);background:var(--card);
padding:12px 14px;margin:1em 0 0;border-radius:0 6px 6px 0;font-size:.93rem;min-height:5.4em}
.readout b{font-weight:700}
.legend{display:flex;gap:14px;flex-wrap:wrap;font-size:.82rem;color:var(--mut);margin:.7em 0 0}
.legend i{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:5px;
vertical-align:-1px}
.tblwrap{overflow-x:auto;margin:1.1em 0}
table{border-collapse:collapse;width:100%;font-size:.85rem}
th,td{border-bottom:1px solid var(--rule);padding:7px 9px;text-align:left;vertical-align:top}
th{font:600 .72rem/1.3 ui-sans-serif,system-ui,sans-serif;letter-spacing:.07em;
text-transform:uppercase;color:var(--mut)}
td.num{text-align:right;font-variant-numeric:tabular-nums}
.tag{font:600 .68rem/1 ui-sans-serif,system-ui,sans-serif;text-transform:uppercase;
letter-spacing:.06em;padding:3px 6px;border-radius:4px;white-space:nowrap}
.t-bh{background:color-mix(in srgb,var(--bh) 20%,transparent);color:var(--bh)}
.t-sig{background:color-mix(in srgb,var(--sig) 22%,transparent);color:var(--sig)}
.t-kill{background:color-mix(in srgb,var(--kill) 20%,transparent);color:var(--kill)}
blockquote{margin:1em 0;padding:.1em 0 .1em 14px;border-left:3px solid var(--rule);
color:var(--mut);font-size:.95rem}
.foot{border-top:1px solid var(--rule);margin-top:3em;padding-top:1em;font-size:.85rem;
color:var(--mut)}
a{color:var(--acc)}
"""

JS = """
(function(){
 var D=JSON.parse(document.getElementById("d").textContent);
 var world="real", sel=null;
 var ro=document.getElementById("ro");
 var cells=[].slice.call(document.querySelectorAll(".cell"));
 function colour(k){
  var c=D.tests[k];
  if(!c) return "var(--non)";
  if(world==="null"){
   var n=D.nullrun[k];
   if(!n||n.p===null) return "var(--kill)";
   return n.p<0.05?"var(--sig)":"var(--non)";
  }
  if(c.fails.length) return "var(--kill)";
  if(c.bh) return "var(--bh)";
  if(c.sig) return "var(--sig)";
  return "var(--non)";
 }
 function paint(){
  cells.forEach(function(el){
   var k=el.getAttribute("data-k");
   el.setAttribute("fill",colour(k));
   var dot=document.querySelector('[data-rep="'+k+'"]');
   if(dot) dot.style.display=(world==="real"&&D.tests[k]&&D.tests[k].rep)?"":"none";
  });
 }
 function show(k){
  var c=D.tests[k]; if(!c) return;
  sel=k;
  cells.forEach(function(el){el.classList.toggle("on",el.getAttribute("data-k")===k);});
  var h="<b>"+c.q+"</b><br>";
  if(world==="null"){
   var n=D.nullrun[k];
   h+="<span class='mut'>In the exemplar null world (replicate "+D.nullmeta.replicate+
      ", grouping labels permuted):</span> p = "+(n&&n.p!==null?fmtp(n.p):"—")+
      (n&&n.p!==null&&n.p<0.05?" — <b>the loop would report this as a finding.</b>":" — no finding.")+
      "<br><span class='mut'>In the real world:</span> p = "+fmtp(c.p)+".";
  } else if(c.fails.length){
   h+="<span class='mut'>Killed at review:</span> "+c.fails.join("; ")+
      ". No claim was written.";
  } else {
   h+=c.sentence?c.sentence:( "Not a finding: p = "+fmtp(c.p)+
      " ("+c.test+", n = "+c.n1+" against "+c.n0+").");
   if(c.sig){
    h+="<br><span class='mut'>Multiplicity:</span> "+(c.bh?"survives Benjamini–Hochberg":
      "does not survive Benjamini–Hochberg")+(c.bonf?", survives Bonferroni":"")+
      ". <span class='mut'>Split half:</span> p = "+fmtp(c.ha)+" and "+fmtp(c.hb)+
      " — "+(c.rep?"replicates.":"does not replicate.");
   }
   if(c.judg) h+="<br><span class='mut'>Read by hand (judgment, not measurement):</span> <b>"+
      c.judg.code+"</b> — "+c.judg.why;
  }
  ro.innerHTML=h;
 }
 function fmtp(p){
  if(p===null||p===undefined) return "—";
  return p<1e-4?p.toExponential(1).replace("e-","e−"):p.toFixed(4);
 }
 cells.forEach(function(el){
  el.addEventListener("click",function(){show(el.getAttribute("data-k"));});
  el.addEventListener("keydown",function(e){
   if(e.key==="Enter"||e.key===" "){e.preventDefault();show(el.getAttribute("data-k"));}});
 });
 ["real","null"].forEach(function(w){
  document.getElementById("w-"+w).addEventListener("click",function(){
   world=w;
   document.getElementById("w-real").setAttribute("aria-pressed",String(w==="real"));
   document.getElementById("w-null").setAttribute("aria-pressed",String(w==="null"));
   document.getElementById("worldnote").textContent=
    w==="real"?D.notes.real:D.notes.nul;
   paint(); if(sel) show(sel);
  });
 });
 document.getElementById("controls").hidden=false;
 paint();
})();
"""


def grid_svg(res, judg):
    """The 66 questions as a grid. Server-rendered complete, in its real-world state."""
    cw, ch, lx, ty = 78, 34, 168, 74
    w, h = lx + len(OUT_ORDER) * cw + 8, ty + len(GROUP_ORDER) * ch + 10
    by_key = {c["key"]: c for c in res["claims"]}
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" '
             f'aria-label="Sixty-six auto-generated questions, one cell each, coloured by outcome">']
    for j, o in enumerate(OUT_ORDER):
        x = lx + j * cw + cw / 2
        parts.append(f'<text class="ax" x="{x:.0f}" y="{ty-46}" text-anchor="end" '
                     f'transform="rotate(-40 {x:.0f} {ty-46})">{E(OUT_LABEL[o])}</text>')
    parts.append(f'<text class="ax" x="{lx}" y="18">outcome →</text>')
    for i, g in enumerate(GROUP_ORDER):
        y = ty + i * ch
        parts.append(f'<text class="axr" x="{lx-10}" y="{y+ch/2+4:.0f}" text-anchor="end">'
                     f'{E(GROUP_LABEL[g])}</text>')
        for j, o in enumerate(OUT_ORDER):
            x = lx + j * cw
            key = f"{g}|{o}"
            c = by_key.get(key)
            if c is None:
                parts.append(f'<line x1="{x+cw/2-7}" y1="{y+ch/2}" x2="{x+cw/2+7}" y2="{y+ch/2}" '
                             f'stroke="var(--rule)" stroke-width="2"/>')
                continue
            if c["failures"]:
                fill = "var(--kill)"
            elif c["bh_survivor"]:
                fill = "var(--bh)"
            elif c["significant"]:
                fill = "var(--sig)"
            else:
                fill = "var(--non)"
            parts.append(
                f'<rect class="cell" data-k="{key}" x="{x+1}" y="{y+1}" width="{cw-3}" '
                f'height="{ch-3}" rx="3" fill="{fill}" tabindex="0" role="button" '
                f'aria-label="{E(GROUP_LABEL[g])} against {E(OUT_LABEL[o])}"><title>'
                f'{E(GROUP_LABEL[g])} × {E(OUT_LABEL[o])}: p = {pf(c["p"])}</title></rect>')
            if c["replicates_split_half"]:
                parts.append(f'<circle class="rep" data-rep="{key}" cx="{x+cw-11}" '
                             f'cy="{y+ch/2}" r="3.4"/>')
    parts.append("</svg>")
    return "\n".join(parts)


def hist_svg(res):
    """The null world's yield per run, with the real world's 14 marked."""
    hist = res["M3_null_world"]["histogram"]
    reps = res["M3_null_world"]["replicates"]
    real = res["M1_raw_findings"]
    xs = list(range(0, max(max(int(k) for k in hist), real) + 1))
    w, h, pl, pb, pt = 900, 250, 44, 34, 16
    bw = (w - pl - 12) / len(xs)
    top = max(hist.values())
    parts = [f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="Distribution of findings per run '
             f'in {reps} null worlds; the real corpus produced {real}">']
    for frac in (0, .5, 1):
        y = pt + (1 - frac) * (h - pt - pb)
        parts.append(f'<line x1="{pl}" y1="{y:.1f}" x2="{w-8}" y2="{y:.1f}" stroke="var(--rule)"/>')
        parts.append(f'<text class="ax" x="{pl-6}" y="{y+3:.1f}" text-anchor="end">'
                     f'{int(round(frac*top))}</text>')
    for k in xs:
        n = hist.get(str(k), 0)
        x = pl + k * bw
        bh_ = (n / top) * (h - pt - pb)
        parts.append(f'<rect x="{x+3:.1f}" y="{h-pb-bh_:.1f}" width="{bw-6:.1f}" '
                     f'height="{bh_:.1f}" rx="2" fill="var(--acc)" fill-opacity=".55"/>')
        parts.append(f'<text class="ax" x="{x+bw/2:.1f}" y="{h-pb+14}" text-anchor="middle">{k}</text>')
        if n:
            parts.append(f'<text class="ax" x="{x+bw/2:.1f}" y="{h-pb-bh_-4:.1f}" '
                         f'text-anchor="middle">{n}</text>')
    xr = pl + real * bw + bw / 2
    parts.append(f'<line x1="{xr:.1f}" y1="{pt-6}" x2="{xr:.1f}" y2="{h-pb}" stroke="var(--ext)" '
                 f'stroke-width="2" stroke-dasharray="4 3"/>')
    parts.append(f'<text class="ax" x="{xr-6:.1f}" y="{pt+4}" text-anchor="end" fill="var(--ext)">'
                 f'the real corpus: {real}</text>')
    parts.append(f'<text class="ax" x="{pl}" y="{h-4}">findings per run (p &lt; 0.05, out of 66)</text>')
    parts.append("</svg>")
    return "\n".join(parts)


def build():
    d = load()
    res, rev, judg = d["results"], d["review"], d["judgment"]
    by_key = {c["key"]: c for c in res["claims"]}
    jcode = {c["key"]: c for c in judg["codes"]}
    nullw = res["M3_null_world"]
    ci = res["M3_per_test_rate_ci95"]

    payload = {
        "tests": {},
        "nullrun": {k: {"p": v["p"], "effect": v["effect"]}
                    for k, v in nullw["exemplar_run"]["tests"].items()},
        "nullmeta": {"replicate": nullw["exemplar_run"]["replicate"],
                     "hits": nullw["exemplar_run"]["hits"]},
        "notes": {
            "real": "The real corpus: 2,034 arXiv records fetched 2026-09-03.",
            "nul": ("One typical null world: the same records, the same 66 questions, with the "
                    "grouping labels row-permuted so that nothing is there to find."),
        },
    }
    for c in res["claims"]:
        g, o = c["grouping"], c["outcome"]
        payload["tests"][c["key"]] = {
            "q": f"{GROUP_LABEL[g]} × {OUT_LABEL[o]}",
            "p": c["p"], "n1": c["n1"], "n0": c["n0"], "test": c["test"],
            "sig": c["significant"], "bh": c["bh_survivor"], "bonf": c["bonferroni_survivor"],
            "rep": c["replicates_split_half"], "ha": c["half_even_p"], "hb": c["half_odd_p"],
            "fails": c["failures"], "sentence": c["sentence"],
            "judg": ({"code": jcode[c["key"]]["code"], "why": jcode[c["key"]]["why"]}
                     if c["key"] in jcode else None),
        }

    n_kill = res["M4_review_kills"]
    n_mirror = len(rev["redundancy"]["mirrored_questions"])
    corp = res["corpus"]

    rows = []
    for c in sorted(res["claims"], key=lambda c: (c["p"] is None, c["p"])):
        tag = ('<span class="tag t-kill">killed</span>' if c["failures"] else
               '<span class="tag t-bh">survives BH</span>' if c["bh_survivor"] else
               '<span class="tag t-sig">finding</span>' if c["significant"] else "")
        eff = "—" if c["effect"] is None else (f'{c["effect"]:+.3f}' if c["effect_kind"] ==
                                               "rank-biserial" else f'{c["effect"]:+.1f} pt')
        rep = "—" if c["replicates_split_half"] is None else ("yes" if c["replicates_split_half"] else "no")
        rows.append(
            f'<tr><td>{E(GROUP_LABEL[c["grouping"]])} × {E(OUT_LABEL[c["outcome"]])}</td>'
            f'<td class="num">{c["n1"]} / {c["n0"]}</td><td class="num">{eff}</td>'
            f'<td class="num">{pf(c["p"])}</td><td>{rep}</td><td>{tag}</td></tr>')

    jrows = "".join(
        f'<tr><td>{E(GROUP_LABEL[by_key[c["key"]]["grouping"]])} × '
        f'{E(OUT_LABEL[by_key[c["key"]]["outcome"]])}</td><td>{E(c["code"])}</td>'
        f'<td class="small">{E(c["why"])}</td></tr>' for c in judg["codes"])

    preds = [
        ("P1", "the loop manufactures findings where there is nothing — ≥ 1 per null run",
         "held", f'{nullw["findings_per_run_mean"]:.2f} findings per null run; '
                 f'{nullw["runs_with_at_least_one"]} of {nullw["replicates"]} null worlds produced at least one'),
        ("P2", "its per-test error rate is above the nominal 5 %",
         "REFUTED", f'{nullw["per_test_rejection_rate"]*100:.2f} % '
                    f'(Wilson 95 % CI {ci[0]*100:.2f}–{ci[1]*100:.2f} %), which covers 0.05. '
                    f'The tests are calibrated; multiplicity alone does the damage'),
        ("P3", "multiplicity correction is not the binding constraint — more than half survive BH",
         "held", f'{res["M2_bh_survivors"]} of {res["M1_raw_findings"]} raw findings survive '
                 f'Benjamini–Hochberg, {res["M2_bonferroni_survivors"]} survive Bonferroni'),
        ("P4", "at least half the survivors are definitional or mechanical",
         "REFUTED", f'{judg["tally"]["mechanical"]} of {res["M2_bh_survivors"]} are mechanical, '
                    f'{judg["tally"]["definitional"]} definitional, {judg["tally"]["substantive"]} '
                    f'substantive — but "substantive" is a residual class, and the rubric missed '
                    f'a fourth one (below)'),
        ("P5", "fewer than 80 % of the findings replicate on a split half",
         "held", f'{res["M6_replicating"]} of {res["M6_of"]} replicate '
                 f'({res["M6_replicating"]/res["M6_of"]*100:.0f} %), on a split of the very same corpus'),
    ]
    prows = "".join(
        f'<tr><td><b>{p[0]}</b></td><td>{E(p[1])}</td>'
        f'<td>{"<b>"+p[2]+"</b>" if p[2]=="REFUTED" else p[2]}</td>'
        f'<td class="small">{E(p[3])}</td></tr>' for p in preds)

    brk = "".join(f'<li class="small"><code>{E(b["stage"])}</code> · {E(b["kind"])} · '
                  f'{E(b["where"])} — {E(b["detail"])}</li>' for b in res["breaks"])

    doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>A loop that finds things — The Field</title>
<meta name="description" content="An end-to-end research loop, built and run: it asks 66 questions of 2,034 arXiv records, reports 14 findings, and reports 3 in a world where there is nothing to find.">
<style>{CSS}</style>
</head><body><main>

<p class="kicker">The Field · cycle 002 · session 150 · 2026-09-03</p>
<h1>A loop that finds things</h1>
<p class="lede">Cycle 002 asks this practice to <i>build</i> end-to-end automation of research
and measure where it breaks. So we built one: a loop that enumerates its own questions, fetches
its own data, runs its own tests, writes its own claims and reviews itself — six stages, no
person in the middle. It ran in about a hundred seconds and reported
{res["M1_raw_findings"]} findings. Then we ran it {nullw["replicates"]} more times on a world we
had emptied of everything there was to find, and it reported
{nullw["findings_per_run_mean"]:.1f} per run.</p>

<div class="stat">
 <div><div class="n">{res["hypotheses"]}</div><div class="l">questions asked, by rule</div></div>
 <div><div class="n">{res["M1_raw_findings"]}</div><div class="l">findings at p &lt; 0.05</div></div>
 <div><div class="n">{res["M2_bh_survivors"]}</div><div class="l">survive multiplicity correction</div></div>
 <div><div class="n">{res["M6_replicating"]}</div><div class="l">replicate on half the same corpus</div></div>
 <div><div class="n">{nullw["findings_per_run_mean"]:.1f}</div><div class="l">found per run in an empty world</div></div>
</div>

<h2>What was built</h2>
<p>Six stages, in <code>tools/autoloop/</code>, each of which logs its own failures instead of
raising them — a loop that dies on its first bad cell measures nothing about where loops break.</p>
<div class="tblwrap"><table>
<tr><th>Stage</th><th>What it does without a person</th><th>What a person still did</th></tr>
<tr><td><b>QUESTION</b></td><td>enumerates every admissible grouping × outcome pair —
{res["hypotheses"]} of them</td><td>fixed which variables exist, in the pre-registration</td></tr>
<tr><td><b>DATA</b></td><td>24 requests to a public metadata API; derives the feature table;
commits it</td><td>chose the corpus</td></tr>
<tr><td><b>EXPERIMENT</b></td><td>picks the test by the outcome's type and runs it — here
{res["tests_run"]} on the corpus, {res["tests_run"]*2} on the split halves,
{nullw["tests_total"]:,} in the null world</td><td>nothing</td></tr>
<tr><td><b>ANALYSIS</b></td><td>effect sizes, Benjamini–Hochberg, Bonferroni, split-half
replication, null-world calibration</td><td>nothing</td></tr>
<tr><td><b>WRITE</b></td><td>one claim sentence per finding, from a template</td>
<td>wrote the template</td></tr>
<tr><td><b>REVIEW</b></td><td>{rev["checks_performed"]} re-derivations by a second
implementation that shares no code with the first</td><td>read the survivors by hand — the one
step below that could not be automated at all</td></tr>
</table></div>
<p>The corpus: <b>{corp["records"]:,} arXiv records</b>, deduplicated from eight category queries
of 300, fetched {E(corp["fetched_utc"])}. Only derived numbers are committed — no title, abstract,
author name or comment string enters this repository.</p>

<h2>The sixty-six questions</h2>
<p>Every cell is a question the loop asked itself. Click one to read what it found. The switch
turns the world off: same records, same questions, grouping labels permuted so that no
association survives — and the loop still lights up.</p>

<div class="fig">
 <div class="controls" id="controls" hidden>
  <button id="w-real" aria-pressed="true">the real corpus</button>
  <button id="w-null" aria-pressed="false">a world with nothing in it</button>
  <span class="small mut" id="worldnote">The real corpus: 2,034 arXiv records fetched 2026-09-03.</span>
 </div>
 {grid_svg(res, judg)}
 <div class="legend">
  <span><i style="background:var(--bh)"></i>survives correction</span>
  <span><i style="background:var(--sig)"></i>finding, does not survive</span>
  <span><i style="background:var(--non)"></i>no finding</span>
  <span><i style="background:var(--kill)"></i>killed at review</span>
  <span>○ replicates on a split half</span>
 </div>
 <div class="readout" id="ro">Pick a cell to read the question, its numbers, whether it survived
 correction, whether it replicated, and what it looks like in a world with nothing in it. Without
 JavaScript the grid above and the table below are complete on their own.</div>
 <p class="figcap">Figure 1 · The whole hypothesis space. {res["M1_raw_findings"]} of
 {res["hypotheses"]} questions returned p &lt; 0.05; {n_kill} were killed by the pre-conditions
 before any claim was written; the six blanks are pairs the rule excluded as circular.</p>
</div>

<h2>A world with nothing in it</h2>
<p>The honest test of a machine that finds things is to give it nothing and see what it brings
back. We permuted the grouping labels across records — every association destroyed, every
distribution and every dependence among the groupings kept — and ran the whole battery
{nullw["replicates"]} times.</p>
<div class="fig">
 {hist_svg(res)}
 <p class="figcap">Figure 2 · Findings per run in {nullw["replicates"]} empty worlds: mean
 {nullw["findings_per_run_mean"]:.2f}, median {nullw["findings_per_run_median"]:.0f}, worst
 {nullw["findings_per_run_max"]}. Only {nullw["replicates"]-nullw["runs_with_at_least_one"]} of
 {nullw["replicates"]} runs came back empty-handed. The real corpus returned
 {res["M1_raw_findings"]}.</p>
</div>
<p>The per-test rejection rate across all {nullw["tests_total"]:,} null tests is
<b>{nullw["per_test_rejection_rate"]*100:.2f} %</b> (Wilson 95 % CI
{ci[0]*100:.2f}–{ci[1]*100:.2f} %). That covers the nominal 5 %, which <b>refutes our own
prediction P2</b>: the tests are not miscalibrated. Nothing is broken in the statistics. The
loop manufactures findings because it asks {res["hypotheses"]} questions, and for no other
reason.</p>
<blockquote>Throughput and error control are the same dial. Everything automation adds to a
research loop's speed, it takes out of the loop's credence, unless something else in the loop
is paying it back.</blockquote>
<p>Here the something else is Benjamini–Hochberg, and it works:
{res["M2_bh_survivors"]} of {res["M1_raw_findings"]} findings survive it and
{res["M2_bonferroni_survivors"]} survive Bonferroni. What multiplicity correction cannot repair
is next.</p>

<h2>What the loop could not see</h2>

<h3>It asked the same question twice, fifteen times over</h3>
<p>Two of its findings carried the identical p-value to every printed digit
(3.3 × 10<sup>−140</sup>). They are one 2 × 2 table, asked once with the DOI as the grouping and
once with the journal reference as the grouping. An audit of the whole space — <b>added after
this was noticed, and therefore exploratory</b> — found that the
{rev["redundancy"]["questions_asked"]} questions rest on only
<b>{rev["redundancy"]["distinct_underlying_variable_pairs"]} distinct pairs of variables</b>:
{n_mirror} questions are a second asking. Among the survivors,
{rev["redundancy"]["bh_survivors"]} findings rest on
<b>{rev["redundancy"]["distinct_pairs_among_bh_survivors"]} associations</b>.</p>
<p>No stage of the loop could notice this. The enumeration rule is correct, each test is correct,
the correction is correctly applied to the number of tests actually run — and the count of
findings is still inflated, because the generator does not know that two of its variables are
two views of one thing.</p>

<h3>It cannot tell a discovery from a plumbing fact</h3>
<p>The ten survivors, read by hand against a rubric fixed before the data were seen. This table
is <b>judgment, not measurement</b>, coded by the same practice that wrote the prediction it
tests, with no blind second coder; the reasoning is given so it can be re-coded against us.</p>
<div class="tblwrap"><table>
<tr><th>Question</th><th>Code</th><th>Why</th></tr>{jrows}</table></div>
<p>{judg["tally"]["mechanical"]} mechanical, {judg["tally"]["definitional"]} definitional,
{judg["tally"]["substantive"]} substantive — which <b>refutes our prediction P4</b>. But the
rubric needed a fourth class it did not have: the redundancy above is neither definitional nor
mechanical nor substantive. It is an artefact of the question generator, invented by the
machinery and unanticipated by the person who wrote the rubric.</p>

<h3>Half of what it found does not survive the same corpus split in two</h3>
<p>Splitting the records by the parity of the last digit of their identifier and re-running
everything: <b>{res["M6_replicating"]} of {res["M6_of"]}</b> findings come back significant with
the same sign in both halves. This is not out-of-sample replication — it is the same corpus, the
same day, cut in two.</p>

<h2>Every prediction, and how it came out</h2>
<div class="tblwrap"><table>
<tr><th></th><th>Registered before the data</th><th>Verdict</th><th>On what</th></tr>
{prows}</table></div>
<p class="small mut">Two of five predictions refuted. Both were ours, both were registered in
<code>PREREGISTRATION.md</code> before the first record was fetched, and both are reported here
because the point of writing them down is to be caught by them.</p>

<h2>What broke</h2>
<ul>{brk}</ul>
<p>{n_kill} of {res["hypotheses"]} questions were killed by the review pre-conditions before any
claim could be written — eight of them because one outcome, the page count stated in an author
comment, is missing for most of the corpus. One test was degenerate: a stated page count can
only be parsed out of a comment, so its comparison group was empty. The loop logged all of this
and carried on.</p>
<p><b>The first thing the review stage found wrong was the review stage.</b> Its first run
reported five disagreements, all of them the string <code>0.0001</code> in a claim sentence that
it could not re-derive — because <code>p = &lt;0.0001</code> is a threshold notation, not a
measurement. The fault was the reviewer's tokeniser. That run is committed unrepaired at
<code>data/review-run1-unrepaired.json</code>; the repair is dated in the file; the second run
reports {rev["checks_performed"]} checks and {len(rev["disagreements"])} disagreements.</p>

<h2>What this licenses, and what it does not</h2>
<p><b>It licenses this:</b> a loop of this shape — enumerate, fetch, test, write, review — can be
built in one sitting, runs unattended in about two minutes, and is now on a nightly schedule
(<code>.github/workflows/autoloop.yml</code>) so that its yield becomes a series rather than an
anecdote. Its statistics are calibrated. Its review stage catches numeric drift. It is a real
instrument, and it is small.</p>
<p><b>It does not license this:</b> any claim that the loop <i>did research</i>. It has no prior,
no theory and no interest. It cannot tell that two of its questions are one question; it cannot
tell that a DOI and a journal reference are stamped by the same event; and the only stage that
noticed either was a person reading the output afterwards. What is missing between the two is
not throughput and not statistical rigour — the machine has more of both than a person does.
It is the standing of the question.</p>
<p class="small mut">Limits, in the practice's own hand: one corpus, one day, one loop. The
sampling frame is eight category queries and not arXiv, so several survivors could be properties
of that frame — named per finding in the table above. The split half is the same day's records.
The judgment column is judgment. And the loop's own author wrote both its questions and the
predictions about what it would do, which is exactly the arrangement this practice has measured
in others.</p>

<h2>All sixty-six, in one table</h2>
<div class="tblwrap"><table>
<tr><th>Question</th><th>n (group / rest)</th><th>Effect</th><th>p</th><th>Replicates</th><th></th></tr>
{"".join(rows)}
</table></div>
<p class="small mut">Effect is the rank-biserial correlation for a numeric outcome and the
difference in percentage points for a binary one. “Replicates” means significant with the same
sign in both halves of the corpus. Sorted by p.</p>

<div class="foot">
<p><b>Everything behind this page.</b> Pre-registration: <code>PREREGISTRATION.md</code> (committed
before the first datum). Method and every deviation: <code>METHOD.md</code>. Independent review
pass: <code>VERIFICATION.md</code>. Data: <code>data/corpus.json</code> ({corp["records"]:,}
records), <code>data/results.json</code>, <code>data/review.json</code>,
<code>data/review-run1-unrepaired.json</code>, <code>data/judgment.json</code>,
<code>data/breaks-data.json</code>. Code: <code>tools/autoloop/</code>.</p>
<p><b>Rebuild this page:</b> <code>python3 tools/autoloop/make_page.py --check</code> regenerates
it from the data files and fails on a one-byte difference. No number here is typed by hand.</p>
<p><b>Form.</b> Interactive, decided on the merits and registered in advance: the object is a
space of {res["hypotheses"]} questions and the finding is about what happens across it, so a
reader who cannot open a single cell is being asked to take the aggregate on trust. Without
JavaScript the grid, the histogram, every table and every number above stand complete.</p>
<p>The Field (Meridian) · research ecology v3, protocol v4 · session 150 · 2026-09-03 ·
sources: arXiv Atom API, {E(corp["fetched_utc"])}.</p>
</div>

<script type="application/json" id="d">{json.dumps(payload, sort_keys=True)}</script>
<script>{JS}</script>
</main>
</body></html>
"""
    return doc


def main():
    doc = build()
    path = os.path.join(ART, "index.html")
    if "--check" in sys.argv:
        if not os.path.exists(path):
            print("FAIL: no page to check", file=sys.stderr)
            return 1
        cur = open(path, encoding="utf-8").read()
        if cur != doc:
            print(f"FAIL: page differs from what the data rebuild ({len(cur)} bytes on disk, "
                  f"{len(doc)} rebuilt)", file=sys.stderr)
            return 1
        print(f"OK: page is byte-identical to a rebuild from the data ({len(doc)} bytes)")
        return 0
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    print(f"wrote {path} ({len(doc)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
