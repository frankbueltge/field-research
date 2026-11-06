// Who the Curve Speaks For (study 56). Every number on the page is read from data56.js, written by analyse56.py.
(function () {
  const D = window.DATA56, P = window.PRED56;
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim();
  const MON = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const day = (rec, i) => { const t = new Date(rec.first + 'T00:00:00Z'); t.setUTCDate(t.getUTCDate() + i); return t; };
  const fmt = t => t.getUTCDate() + ' ' + MON[t.getUTCMonth()] + ' ' + t.getUTCFullYear();
  const pct = (k, n) => n ? Math.round(100 * k / n) + ' %' : '–';
  const longQ = rec => rec.quiets.filter(q => (q.L === null ? rec.N - 1 - q.a : q.L) >= 21).sort((x, y) => x.a - y.a || x.z.localeCompare(y.z));
  // status of a quiet at day d, by study 53's own rule
  function status(rec, q, d) {
    if (q.L !== null && q.L <= d) return 'gone';
    if (q.a + d + 42 > rec.N - 1) return 'edge';
    return (q.L !== null && q.L <= d + 42) ? 'brk' : 'hld';
  }
  function tally(rec, d) {
    const c = { gone: 0, edge: 0, brk: 0, hld: 0 };
    for (const q of longQ(rec)) c[status(rec, q, d)]++;
    return c;
  }
  let R = 'Congo 2026', d = 42;

  // the answer, from the data
  (function answer() {
    const k = D['Kivu 2018-2020'], c = D['Congo 2026'];
    const p60 = c.quiets.filter(q => status(c, q, 60) === 'brk' || status(c, q, 60) === 'hld');
    const a0 = Math.min(...p60.map(q => q.a)), a1 = Math.max(...p60.map(q => q.a));
    let kFirst = null; for (let x = 21; x <= 120 && kFirst === null; x++) if (tally(k, x).edge > 0) kFirst = x;
    const inK = (q, x) => status(k, q, x) === 'brk' || status(k, q, x) === 'hld';
    const drop = k.quiets.filter(q => inK(q, 42) && !inK(q, 60));
    const dropBroke = drop.filter(q => status(k, q, 60) === 'gone').length, dropEarly = drop.filter(q => q.a < k.p42.medStart).length;
    document.getElementById('ans').innerHTML =
      '<p><b>In Kivu, not at all.</b> Between day 42 and day 60 the record\'s end removes no quiet from the count: all ' + k.p42.n +
      ' quiets counted at day 42 began early enough to be counted at 60 too. The edge first removes a quiet at day ' + kFirst +
      '. The ' + k.p60.n + ' counted at day 60 even began later on the median (' + fmt(new Date(k.p60.medStartDate + 'T00:00:00Z')) + ' against ' +
      fmt(new Date(k.p42.medStartDate + 'T00:00:00Z')) + '): of the ' + drop.length + ' that dropped out, ' + dropBroke + ' broke, and ' + dropEarly + ' of them had begun before the median. Between day 42 and day 60 Kivu\'s curve changes by who breaks, not by where the record ends.</p>' +
      '<p><b>In Congo 2026, yes.</b> Of the ' + c.p42.n + ' quiets counted at day 42, ' + c.band.n + ' began after ' + fmt(day(c, c.cutoff60)) +
      ' and are left out at day 60 by the record\'s end alone; ' + (c.p42.n - c.band.n - c.p60.n) + ' more broke before day 60. The curve at day 60 speaks for ' + c.p60.n +
      ' quiets, begun between ' + fmt(day(c, a0)) + ' and ' + fmt(day(c, a1)) + '.</p>' +
      '<p><b>Does the edge alone move the 2026 answer?</b> Not measurably. At day 42, ' + c.p42.k + ' of ' + c.p42.n + ' broke (' + pct(c.p42.k, c.p42.n) +
      '); among the ' + c.matched.n + ' that began early enough to count at 60, ' + c.matched.k + ' of ' + c.matched.n + ' (' + pct(c.matched.k, c.matched.n) +
      '). The gap, ' + String(Math.round(100 * c.gap)).replace('-', '−') + ' points, has an interval from ' + Math.round(100 * c.gapCI[0]) + ' to +' + Math.round(100 * c.gapCI[1]) +
      ': the direction we predicted, too few quiets to tell it from chance.</p>';
  })();

  // Figure 1
  const cal = document.getElementById('cal'), rd = document.getElementById('rd');
  function setup(cv, h) {
    const w = cv.clientWidth, r = window.devicePixelRatio || 1;
    cv.width = w * r; cv.height = h * r; cv.style.height = h + 'px';
    const g = cv.getContext('2d'); g.setTransform(r, 0, 0, r, 0, 0); return [g, w];
  }
  let hover = null;
  function drawCal() {
    const rec = D[R], qs = longQ(rec), N = rec.N;
    const rowH = Math.max(2, Math.min(6, Math.floor(380 / qs.length)));
    const top = 18, h = top + qs.length * rowH + 30;
    const [g, w] = setup(cal, h);
    const L = 8, Rr = w - 8, x = i => L + (Rr - L) * i / (N - 1);
    const latest = N - 1 - d - 42;
    g.fillStyle = css('--shade'); g.fillRect(x(Math.max(0, latest)), top - 6, Rr - x(Math.max(0, latest)), qs.length * rowH + 8);
    g.strokeStyle = css('--edge'); g.lineWidth = 1.5; g.beginPath(); g.moveTo(x(Math.max(0, latest)), top - 8); g.lineTo(x(Math.max(0, latest)), top + qs.length * rowH + 2); g.stroke();
    const col = { gone: css('--gone'), edge: css('--edge'), brk: css('--brk'), hld: css('--hld') };
    qs.forEach((q, i) => {
      const s = status(rec, q, d), end = q.L === null ? N - 1 : q.a + q.L;
      g.fillStyle = col[s]; g.globalAlpha = s === 'gone' ? 0.8 : 1;
      g.fillRect(x(q.a), top + i * rowH, Math.max(1.5, x(end) - x(q.a)), Math.max(1, rowH - 1));
      if (s !== 'gone') { g.globalAlpha = 1; g.fillStyle = css('--fg'); g.fillRect(x(Math.min(q.a + d, N - 1)), top + i * rowH, 1.2, Math.max(1, rowH - 1)); }
    });
    g.globalAlpha = 1;
    if (hover !== null && qs[hover]) { g.strokeStyle = css('--fg'); g.lineWidth = 1; g.strokeRect(L - 2, top + hover * rowH - 1, Rr - L + 4, rowH + 1); }
    // axis: months
    g.fillStyle = css('--mute'); g.font = '12px system-ui,sans-serif'; g.textAlign = 'center';
    let lastX = -99;
    for (let i = 0; i < N; i++) {
      const t = day(rec, i);
      if (t.getUTCDate() !== 1) continue;
      const step = N > 300 ? (t.getUTCMonth() % 3 === 0) : true;
      if (!step || x(i) - lastX < 44) continue;
      lastX = x(i);
      g.fillText(MON[t.getUTCMonth()] + (t.getUTCMonth() === 0 || N <= 300 && i < 31 ? ' ' + t.getUTCFullYear() : ''), x(i), top + qs.length * rowH + 18);
    }
    g.textAlign = 'right'; g.fillStyle = css('--edge');
    g.fillText(latest >= 0 ? 'latest start counted: ' + fmt(day(rec, latest)) : 'no start can be counted', Rr, 12);
    cal._geo = { top, rowH, n: qs.length, x, L, Rr, N };
    readCal();
  }
  function readCal() {
    const rec = D[R], c = tally(rec, d), pd = rec.perD.find(p => p.d === d);
    let s = '<b>' + d + ' days quiet, ' + R.replace('-', '–') + ':</b> ';
    if (pd) s += 'the curve counts ' + pd.n + ' quiets, ' + pd.k + ' broke within 42 days (' + pct(pd.k, pd.n) + '), median start ' + fmt(day(rec, pd.med)) + '. ';
    else s += 'the curve counts no quiet here. ';
    s += c.edge + ' are left out by the record\'s end; ' + c.gone + ' had broken before day ' + d + '.';
    if (hover !== null) {
      const q = longQ(rec)[hover];
      if (q) s += '<br>' + q.z + ': quiet from ' + fmt(day(rec, q.a)) + (q.L === null ? ', still quiet at the record\'s end' : ', broke after ' + q.L + ' days') + ' — ' +
        { gone: 'broke before day ' + d, edge: 'left out at day ' + d + ' (its 42 days run past ' + fmt(day(rec, rec.N - 1)) + ')', brk: 'counted, broke within 42 days', hld: 'counted, held 42 days' }[status(rec, q, d)] + '.';
    }
    rd.innerHTML = s;
  }
  cal.addEventListener('pointermove', e => {
    const g = cal._geo; if (!g) return;
    const r = cal.getBoundingClientRect(), i = Math.floor((e.clientY - r.top - g.top) / g.rowH);
    const h = i >= 0 && i < g.n ? i : null; if (h !== hover) { hover = h; drawCal(); }
  });
  cal.addEventListener('pointerleave', () => { hover = null; drawCal(); });

  // Figure 2
  const stk = document.getElementById('stk'), rd2 = document.getElementById('rd2');
  let hd = null;
  function drawStk() {
    const rec = D[R], [g, w] = setup(stk, 260), L = 40, Rr = w - 10, T = 12, B = 226;
    const ds = []; for (let x = 21; x <= 120; x++) ds.push([x, tally(rec, x)]);
    const tot = longQ(rec).length, X = x => L + (Rr - L) * (x - 21) / 99, Y = v => B - (B - T) * v / tot;
    const layers = [['brk', '--brk'], ['hld', '--hld'], ['edge', '--edge'], ['gone', '--gone']];
    let base = ds.map(() => 0);
    for (const [k, c] of layers) {
      g.fillStyle = css(c); g.beginPath();
      ds.forEach(([x, t], i) => { const y = Y(base[i] + t[k]); i ? g.lineTo(X(x), y) : g.moveTo(X(x), y); });
      for (let i = ds.length - 1; i >= 0; i--) g.lineTo(X(ds[i][0]), Y(base[i]));
      g.closePath(); g.fill();
      base = base.map((b, i) => b + ds[i][1][k]);
    }
    g.strokeStyle = css('--fg'); g.lineWidth = 1.5; g.beginPath(); g.moveTo(X(d), T); g.lineTo(X(d), B); g.stroke();
    if (hd !== null) { g.setLineDash([3, 3]); g.beginPath(); g.moveTo(X(hd), T); g.lineTo(X(hd), B); g.stroke(); g.setLineDash([]); }
    g.fillStyle = css('--mute'); g.font = '12px system-ui,sans-serif'; g.textAlign = 'center';
    for (const x of [21, 42, 60, 80, 100, 120]) g.fillText(x, X(x), B + 16);
    g.fillText('days quiet', (L + Rr) / 2, B + 31);
    g.textAlign = 'right'; g.fillText(tot, L - 6, T + 4); g.fillText('0', L - 6, B);
    stk._geo = { X, L, Rr };
    const x = hd === null ? d : hd, t = tally(rec, x);
    rd2.innerHTML = '<b>Day ' + x + ', ' + R.replace('-', '–') + ':</b> of ' + tot + ' quiets that reached three weeks, ' + (t.brk + t.hld) + ' counted (' + t.brk + ' broke within 42, ' + t.hld + ' held), ' + t.edge + ' left out at the edge, ' + t.gone + ' broke earlier.';
  }
  stk.addEventListener('pointermove', e => {
    const g = stk._geo; if (!g) return;
    const r = stk.getBoundingClientRect(), x = Math.round(21 + 99 * (e.clientX - r.left - g.L) / (g.Rr - g.L));
    const h = x >= 21 && x <= 120 ? x : null; if (h !== hd) { hd = h; drawStk(); }
  });
  stk.addEventListener('pointerleave', () => { hd = null; drawStk(); });

  // predictions
  const ex = {
    P15: v => 'Kivu ' + v['Kivu 2018-2020'][0] + ' → ' + v['Kivu 2018-2020'][1] + '; 2026 ' + v['Congo 2026'][0] + ' → ' + v['Congo 2026'][1],
    P16: v => '2026 ' + Math.round(100 * v['2026']) + ' %; Kivu ' + Math.round(100 * v.Kivu) + ' %',
    P17: v => 'gap ' + (100 * v.gap).toFixed(1) + ' points, interval ' + (100 * v.ci[0]).toFixed(1) + ' to ' + (100 * v.ci[1]).toFixed(1) + ': no quiet in Kivu\'s edge band, so nothing to compare',
    P18: v => 'gap ' + (100 * v.gap).toFixed(1) + ' points (' + (100 * v.ci[0]).toFixed(1) + ' to +' + (100 * v.ci[1]).toFixed(1) + ')'
  };
  const tb = document.querySelector('#pred tbody');
  for (const [id, p] of Object.entries(P)) {
    const uninf = id === 'P17';
    const tr = document.createElement('tr');
    tr.innerHTML = '<td>' + id + '</td><td>' + p.text + '</td><td>' + ex[id](p.value) + '</td><td class="' + (uninf ? 'held uninf' : p.held ? 'held' : 'failed') + '">' + (p.held ? (uninf ? 'held, uninformative' : 'held') : 'failed') + '</td>';
    tb.appendChild(tr);
  }

  function all() { document.getElementById('dv').textContent = d; drawCal(); drawStk(); }
  document.getElementById('d').addEventListener('input', e => { d = +e.target.value; all(); });
  document.querySelectorAll('button[data-r]').forEach(b => b.addEventListener('click', () => {
    R = b.dataset.r; hover = null;
    document.querySelectorAll('button[data-r]').forEach(o => o.setAttribute('aria-pressed', String(o === b))); all();
  }));
  window.addEventListener('resize', all);
  matchMedia('(prefers-color-scheme: dark)').addEventListener('change', all);
  all();
})();
