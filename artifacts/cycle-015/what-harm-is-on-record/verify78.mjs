// Study 78 (fourth state): open the page at 1100 px light and 390 px dark; read the new figures from the page a
// visitor sees and compare them with results78.json and an independent recount from check78/harmed-press.json and
// data75.js; check the share scale and the intake mode of the first figure; check errors and sideways scroll;
// write process/4.png from the light pass. The third state's checks stay in verify77.mjs (run with NOSHOT=1).
import { createRequire } from 'module'; import path from 'path'; import fs from 'fs'; import { fileURLToPath } from 'url';
const require = createRequire('/opt/node-tools/node_modules/'); const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url));
const page = process.argv[2] ? path.resolve(process.argv[2]) : path.join(here, 'index.html');
const url = 'file://' + page; const noshot = !!process.env.NOSHOT;
const J = f => JSON.parse(fs.readFileSync(path.join(here, f), 'utf8'));
const R = J('results78.json'), R7 = J('results77.json'), HP = J('check78/harmed-press.json'), PS = J('check77/press-sample.json');
const X = R.press_itself, I = R.intake;
const en = n => n.toLocaleString('en-GB');
// independent recount
const drawn = PS.items.filter(x => x.code === 'harmed').map(x => Number(x.id));
const itself = HP.items.filter(x => x.in_draw && x.press_itself).map(x => x.id);
const outside = drawn.filter(i => !itself.includes(i));
const est = Math.round(outside.length / 120 * R7.press.population) + R7.A.final_harmed;
const D75 = JSON.parse(fs.readFileSync(path.join(here, 'data75.js'), 'utf8').split('=').slice(1).join('=').trim().replace(/;$/, ''));
const top = new Set(I.top_ids);
const y26 = D75.rows.filter(r => r[1] === 2026 && r[2] !== 'no report' && r[2] !== 'unknown');
const b = await chromium.launch(); let fails = 0;
for (const [w, scheme, shot] of [[1100, 'light', 'process/4.png'], [390, 'dark', 'shot-390.png']]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme }); const errs = []; const bad = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(url); await p.waitForTimeout(300);
  const q = s => p.evaluate(s); const t = s => q(`document.querySelector('${s}').textContent`);
  const want = (name, cond) => { if (!cond) bad.push(name); };
  want('recount', outside.length === X.harmed_outside_the_press_in_draw.length && est === X.whole_record_estimate_without_the_press_itself && top.size === I.top_alone);
  want('kicker', (await t('.kicker')).includes('fourth state, the paper') && (await t('.kicker')).includes('presented'));
  const a8 = await t('#a8'), a9 = await t('#a9');
  want('a8', a8.includes(`Of the ${drawn.length} harmed who wrote first`) && a8.includes(`${itself.length} are publications`) && a8.includes(`wrote ${outside.length} of 120`) &&
    a8.includes(`an estimated ${est} of ${en(R7.all_first_reports)} first reports (${X.whole_record_estimate_without_the_press_itself_pct} %; between ${X.whole_record_estimate_without_the_press_itself_ci[0]} and ${X.whole_record_estimate_without_the_press_itself_ci[1]})`));
  want('a9', a9.includes(`first report of ${en(top.size)} of the ${en(I.first_reports)} incidents (${I.top_alone_pct} %)`) &&
    a9.includes(`${y26.filter(r => top.has(r[0])).length} of ${y26.length} in 2026`) && a9.includes(`${en(I.top_by_first_reporter_class['press and other'])} of that submitter's`));
  const c5 = await t('#chk5'), c6 = await t('#chk6');
  want('chk5', c5.includes(`(incidents ${itself.join(' and ')})`) && c5.includes(`(${R7.whole_record.estimate}, between ${R7.whole_record.estimate_ci[0]} and ${R7.whole_record.estimate_ci[1]})`) && c5.includes('incident 428'));
  want('chk6', c6.includes(`entered ${en(top.size)} of ${en(I.first_reports)}`) && c6.includes(`${en(I.atelier_figure)}`));
  // first figure, intake mode: every bar segment's count matches a recount from data75.js and top_ids
  await p.click('[data-mode="intake"]');
  const segs = await q(`[...document.querySelectorAll('#fig rect.seg')].map(r=>[r.dataset.year,r.dataset.cat,Number(r.dataset.n)])`);
  const yr = y => y === null ? null : (y < 2012 ? '<2012' : String(y));
  const want2 = {}; D75.rows.forEach(r => { const y = yr(r[1]); if (!y) return; const k = y + '|' + (top.has(r[0]) ? 'top' : 'other'); want2[k] = (want2[k] || 0) + 1; });
  want('intake segs', segs.length === Object.keys(want2).length && segs.every(([y, c, n]) => want2[y + '|' + c] === n));
  const leg = await q(`Object.fromEntries([...document.querySelectorAll('#legend span')].map(s=>[s.dataset.cat,Number(s.dataset.n)]))`);
  want('intake legend', leg.top === top.size && leg.top + leg.other === 1803);
  want('intake tally', (await t('#tally')).includes(`${en(top.size)} of ${en(I.first_reports)} incidents (${I.top_alone_pct} %)`));
  // share scale: in a year's bar the segments' heights sum to the full scale
  await p.click('[data-scale="share"]');
  const hs = await q(`(()=>{const o={};document.querySelectorAll('#fig rect.seg').forEach(r=>{const y=r.dataset.year;o[y]=(o[y]||0)+Number(r.getAttribute('height'));});return o;})()`);
  const vals = Object.values(hs); want('share heights', vals.length > 10 && Math.max(...vals) - Math.min(...vals) < 4);
  want('share axis', (await q(`[...document.querySelectorAll('#fig text')].some(t=>t.textContent==='100 %')`)));
  want('basenote', (await t('#basenote')).includes('The legend counts all 1,803 incidents, 2 of them with no report') && (await t('#basenote')).includes(`counts the ${en(R7.all_first_reports)} with a first report`));
  await p.click('#fig rect.seg[data-year="2026"]');
  want('readout', (await t('#readout')).includes(`Entered by one submitter: ${y26.filter(r => top.has(r[0])).length + D75.rows.filter(r => r[1] === 2026 && top.has(r[0]) && (r[2] === 'no report' || r[2] === 'unknown')).length} (`));
  await p.click('[data-scale="count"]'); await p.click('[data-mode="who"]');
  want('paper link', await q(`[...document.querySelectorAll('a')].some(a=>/paper\\.md$/.test(a.getAttribute('href')))`));
  want('no sideways scroll', !(await q(`document.documentElement.scrollWidth > window.innerWidth`)));
  const ok = !errs.length && !bad.length; if (!ok) fails++;
  console.log(w, scheme, ok ? 'PASS' : 'FAIL', bad.join(', '), errs.join('; '));
  if (shot && !noshot) await p.screenshot({ path: path.join(here, shot), fullPage: true });
  await p.close();
}
await b.close(); process.exit(fails ? 1 : 0);
