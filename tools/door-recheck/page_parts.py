"""Style and behaviour for the artifact page of session 146.

Kept beside the generator so `make_page.py` stays readable. Nothing here holds a
measured number: every figure on the page comes from the data files.
"""

CSS = """
:root {
  --bg:#fbfbf9; --fg:#17171a; --mut:#5c5c66; --line:#dedcd6; --card:#ffffff;
  --open:#1d6b45; --open-bg:#e7f2ec;
  --shape:#8a4b12; --shape-bg:#f7ece0;
  --name:#7a3570; --name-bg:#f3e6f1;
  --pace:#1f5c78; --pace-bg:#e2eef4;
  --imp:#4a4a55; --imp-bg:#e6e5e3;
  --accent:#123a63;
}
@media (prefers-color-scheme: dark) {
  :root {
    --bg:#131316; --fg:#ececeb; --mut:#a2a2ac; --line:#33333a; --card:#1b1b1f;
    --open:#6fc79a; --open-bg:#16301f;
    --shape:#e0a463; --shape-bg:#33230f;
    --name:#d79ccd; --name-bg:#2e1b2b;
    --pace:#7cc0dd; --pace-bg:#122b36;
    --imp:#b8b8c2; --imp-bg:#26262b;
    --accent:#8fb8e0;
  }
}
* { box-sizing:border-box; }
body { margin:0; background:var(--bg); color:var(--fg);
  font:16px/1.6 ui-serif,Georgia,'Times New Roman',serif; }
main { max-width:56rem; margin:0 auto; padding:2.5rem 1.25rem 5rem; }
h1 { font-size:2.4rem; line-height:1.15; margin:0 0 .4rem; letter-spacing:-.01em; }
h2 { font-size:1.3rem; margin:2.6rem 0 .7rem; }
h3 { font-size:1.02rem; margin:1.6rem 0 .4rem; }
.kicker { font:600 .78rem/1.4 ui-sans-serif,system-ui,sans-serif; letter-spacing:.09em;
  text-transform:uppercase; color:var(--mut); margin-bottom:.9rem; }
.stand { font-size:1.16rem; color:var(--mut); margin:.2rem 0 2rem; }
p { margin:.8rem 0; }
a { color:var(--accent); }
.lede { font-size:1.06rem; }
blockquote { margin:1.2rem 0; padding:.2rem 0 .2rem 1.1rem; border-left:3px solid var(--line);
  color:var(--mut); font-size:.98rem; }
.big { display:flex; flex-wrap:wrap; gap:.9rem; margin:1.6rem 0; }
.big div { flex:1 1 11rem; background:var(--card); border:1px solid var(--line);
  border-radius:.5rem; padding:1rem 1.1rem; }
.big b { display:block; font:700 2.1rem/1.1 ui-sans-serif,system-ui,sans-serif;
  letter-spacing:-.02em; }
.big span { font-size:.88rem; color:var(--mut); }
.verdict { border-left:4px solid var(--open); background:var(--open-bg); padding:1rem 1.2rem;
  border-radius:0 .4rem .4rem 0; margin:1.6rem 0; }
.verdict.warn { border-left-color:var(--shape); background:var(--shape-bg); }
.verdict.grey { border-left-color:var(--imp); background:var(--imp-bg); }
table { border-collapse:collapse; width:100%; font:13px/1.45 ui-sans-serif,system-ui,sans-serif; }
.wrap { overflow-x:auto; border:1px solid var(--line); border-radius:.5rem; margin:1rem 0; }
th,td { text-align:left; padding:.5rem .6rem; border-bottom:1px solid var(--line);
  vertical-align:top; }
th { background:var(--card); font-weight:600; }
td.num { text-align:right; font-variant-numeric:tabular-nums; white-space:nowrap; }
td.pub { min-width:11rem; font-weight:600; }
td.url { color:var(--mut); overflow-wrap:anywhere; font-size:11px; }
code { font:12px/1.4 ui-monospace,SFMono-Regular,Menlo,monospace; word-break:break-all; }
ul { padding-left:1.1rem; } li { margin:.35rem 0; }
.foot { margin-top:3rem; padding-top:1.2rem; border-top:1px solid var(--line);
  font-size:.9rem; color:var(--mut); }

/* --- the knock sequence --- */
.fig { border:1px solid var(--line); border-radius:.6rem; background:var(--card);
  padding:1.1rem 1.1rem 1.3rem; margin:1.8rem 0; }
.fig h3 { margin:0 0 .2rem; font:600 1rem/1.3 ui-sans-serif,system-ui,sans-serif; }
.fig .cap { font-size:.85rem; color:var(--mut); margin:0 0 .9rem; }
.grid { display:grid; grid-template-columns:repeat(8,1fr); gap:4px; }
@media (max-width:640px) { .grid { grid-template-columns:repeat(5,1fr); } }
.cell { position:relative; aspect-ratio:1/1.15; border-radius:.3rem; border:1px solid var(--line);
  background:var(--imp-bg); color:var(--imp); overflow:hidden; padding:.25rem .3rem;
  font:600 9px/1.15 ui-sans-serif,system-ui,sans-serif; text-align:left;
  transition:background-color .45s ease, color .45s ease, border-color .45s ease; }
.cell .w { position:absolute; left:0; bottom:0; height:3px; background:currentColor;
  opacity:.55; }
.cell.s-open { background:var(--open-bg); color:var(--open); border-color:var(--open-bg); }
.cell.s-shape { background:var(--shape-bg); color:var(--shape); border-color:var(--shape-bg); }
.cell.s-name { background:var(--name-bg); color:var(--name); border-color:var(--name-bg); }
.cell.s-pace { background:var(--pace-bg); color:var(--pace); border-color:var(--pace-bg); }
.cell.s-closed { background:var(--card); color:var(--mut); border-style:dashed; }
.cell.s-refused { background:var(--imp-bg); color:var(--imp); }
.cell.sel { outline:2px solid var(--accent); outline-offset:1px; }
button.cell { cursor:pointer; font-family:inherit; }
.steps { display:flex; flex-wrap:wrap; gap:.4rem; margin:.9rem 0 .6rem; }
.steps button { font:600 12px/1 ui-sans-serif,system-ui,sans-serif; padding:.45rem .6rem;
  border:1px solid var(--line); background:var(--bg); color:var(--fg); border-radius:.3rem;
  cursor:pointer; }
.steps button[aria-pressed=true] { background:var(--accent); color:var(--bg);
  border-color:var(--accent); }
.readout { font:13px/1.5 ui-sans-serif,system-ui,sans-serif; color:var(--fg);
  background:var(--bg); border:1px solid var(--line); border-radius:.35rem;
  padding:.6rem .75rem; min-height:3.6rem; }
.readout b { font-variant-numeric:tabular-nums; }
.legend { display:flex; flex-wrap:wrap; gap:.75rem; margin:.8rem 0 0;
  font:12px/1.4 ui-sans-serif,system-ui,sans-serif; color:var(--mut); }
.legend span::before { content:''; display:inline-block; width:.7rem; height:.7rem;
  border-radius:.15rem; margin-right:.3rem; vertical-align:-1px; background:var(--imp-bg); }
.legend .l-open::before { background:var(--open-bg); box-shadow:inset 0 0 0 2px var(--open); }
.legend .l-shape::before { background:var(--shape-bg); box-shadow:inset 0 0 0 2px var(--shape); }
.legend .l-name::before { background:var(--name-bg); box-shadow:inset 0 0 0 2px var(--name); }
.legend .l-pace::before { background:var(--pace-bg); box-shadow:inset 0 0 0 2px var(--pace); }
.legend .l-imp::before { background:var(--imp-bg); box-shadow:inset 0 0 0 2px var(--imp); }
.nojs { font-size:.85rem; color:var(--mut); margin:.7rem 0 0; }
@media (prefers-reduced-motion: reduce) { .cell { transition:none; } }
"""

# The figure is a progressive enhancement: the server render below is the final state,
# complete and readable with no JavaScript. Script only adds the sequence and the readout.
JS = """
(function () {
  var node = document.getElementById('door-data');
  if (!node) return;
  var data = JSON.parse(node.textContent);
  var fig = document.getElementById('knock');
  if (!fig) return;
  var cells = Array.prototype.slice.call(fig.querySelectorAll('.cell'));
  var readout = document.getElementById('readout');
  var stepsBox = document.getElementById('steps');
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var STEPS = data.steps;
  var state = STEPS.length - 1;
  var selected = null;
  var timer = null;

  function stateAt(door, step) {
    if (door.verdict === 'declared_closed') return 'closed';
    var order = { open: 0, shape: 1, name: 2, pace: 3 };
    if (door.verdict === 'impasse') return 'refused';
    return order[door.verdict] <= step ? door.verdict : 'refused';
  }

  function render() {
    var step = STEPS[state];
    cells.forEach(function (cell, i) {
      var door = data.doors[i];
      var s = stateAt(door, state);
      cell.className = 'cell s-' + s + (selected === i ? ' sel' : '');
      cell.setAttribute('aria-label', door.publisher + ' — ' + step.label + ': ' + LABEL[s]);
    });
    Array.prototype.forEach.call(stepsBox.children, function (b, i) {
      b.setAttribute('aria-pressed', String(i === state));
    });
    if (selected === null) {
      readout.innerHTML = step.readout;
    } else {
      readout.innerHTML = doorLine(data.doors[selected]);
    }
  }

  var LABEL = { open: 'open', shape: 'opened by the shape of the request',
                name: 'opened by the name in the request', pace: 'opened by waiting',
                refused: 'still refusing', closed: 'declared closed — not knocked on' };

  function doorLine(d) {
    var arms = Object.keys(d.status).map(function (k) {
      return k + ' ' + d.status[k];
    }).join(' · ');
    return '<b>' + d.publisher + '</b> — ' + d.concerns + ' concerns · ' +
      LABEL[d.verdict === 'declared_closed' ? 'closed' : (d.verdict === 'impasse' ? 'refused' : d.verdict)] +
      '<br>' + arms + (d.layer ? ' · refused at: ' + d.layer : '') +
      '<br><span style="opacity:.7">' + d.url + '</span>';
  }

  cells.forEach(function (cell, i) {
    cell.addEventListener('click', function () {
      selected = (selected === i) ? null : i;
      stop();
      render();
    });
  });

  STEPS.forEach(function (s, i) {
    var b = document.createElement('button');
    b.type = 'button';
    b.textContent = s.label;
    b.addEventListener('click', function () { stop(); selected = null; state = i; render(); });
    stepsBox.appendChild(b);
  });

  var play = document.createElement('button');
  play.type = 'button';
  play.textContent = '▶ replay';
  play.addEventListener('click', function () { selected = null; start(); });
  stepsBox.appendChild(play);

  function start() {
    stop();
    state = 0; render();
    timer = setInterval(function () {
      if (state >= STEPS.length - 1) { stop(); return; }
      state += 1; render();
    }, 1500);
  }
  function stop() { if (timer) { clearInterval(timer); timer = null; } }

  render();
  if (!reduce) start();
})();
"""
