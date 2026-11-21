// Reading 89 (state 5, after the presentation, session 287): open the page at 1100 px light and 390 px dark, read
// every figure of reading 89 (data-k89), the squares of its figure, a readout and the verdicts of P144 and P145 from the
// page a visitor sees, and compare them with counts recomputed here from the per-pair records of join89.json,
// heirs89.json and agree89.json, independently of join89.py's summary and of the page's own script. With CLONES set (a
// directory of bare clones named <repo>.git) every same-commit pair, every mending and every earlier heir is looked up
// again in Git; with ATELIER set (the Atelier's sort.json at ulysses aa8a96e) the agreement is recounted from its file.
// Checks errors and sideways scroll; writes process/5.png from the light pass (NOSHOT=1 skips it).
import { createRequire } from 'module'; import path from 'path'; import fs from 'fs'; import { fileURLToPath } from 'url';
import { execFileSync } from 'child_process';
const require = createRequire('/opt/node-tools/node_modules/'); const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url)); const url = 'file://' + path.join(here, 'index.html');
const rd = f => JSON.parse(fs.readFileSync(path.join(here, f), 'utf8'));
let checks = 0, fails = 0;
const eq = (a, b, what) => { checks++; if (String(a).trim() !== String(b).trim()) { fails++; console.log('FAIL', what, JSON.stringify(a), '!=', JSON.stringify(b)); } };
const ok = (c, what) => { checks++; if (!c) { fails++; console.log('FAIL', what); } };
const g = x => x.toLocaleString('en-GB');
const median = xs => { const s = [...xs].sort((a, b) => a - b), n = s.length; return n % 2 ? s[(n - 1) / 2] : (s[n / 2 - 1] + s[n / 2]) / 2; };

// ---- the pairs, recounted
const J = rd('join89.json').pairs, CR = rd('credit88.json').deeds, HR = rd('heirs89.json'), AG = rd('agree89.json');
const SET = CR.filter(d => d.repair_found);
eq(J.length, SET.length, 'one record per pair of reading 88'); eq(J.length, 77, 'the 77 pairs');
const KC = Object.fromEntries(SET.map(d => [d.row + '|' + d.deed, d]));
for (const p of J) { const c = KC[p.row + '|' + p.deed]; ok(c, `pair ${p.row}|${p.deed} in reading 88`); if (!c) continue;
  eq(p.repair, c.repair_hash, `mending of ${p.row}|${p.deed}`);
  eq(p.same_commit, c.deed_commits.some(x => x && x.hash === c.repair_hash), `same commit ${p.row}|${p.deed}`);
  eq(p.name, !!c.names_deed, `name ${p.row}|${p.deed}`);
  const code = p.same_commit ? 'same_commit' : p.lines ? 'lines' : p.name ? 'name' : p.file ? 'file' : 'log_only';
  eq(p.code, code, `precedence ${p.row}|${p.deed}`);
  eq(p.lines, (p.lines_taken_out || 0) > 0, `lines flag ${p.row}|${p.deed}`);
  if (p.code === 'lines') { ok(p.git_points === (p.heirs_before === 0), `heir count and flag ${p.row}|${p.deed}`); } }
const by = k => J.filter(p => p.code === k).length;
const SAME = by('same_commit'), LINES = by('lines'), FILE = by('file'), LOG = by('log_only');
const LEAD1 = J.filter(p => p.code === 'lines' && p.git_points === true).length;
const HASH = J.filter(p => p.name && p.code !== 'same_commit'), HASHNL = HASH.filter(p => p.git_points !== true).length;
const JOINED = SAME + LINES + by('name'), LEAD = SAME + LEAD1 + HASHNL;
eq(SAME + LINES + by('name') + FILE + LOG, 77, 'the codes partition the pairs');
const HEIRS = HR.heirs; eq(HEIRS.length, LINES - LEAD1, 'one earlier heir per pair whose mending came second');
for (const h of HEIRS) { const p = J.find(q => q.row === h.row && q.deed === h.deed); ok(p && p.heirs_before_hashes[0] === h.heir, `heir of ${h.row}|${h.deed}`);
  ok(h.hours_after_deed >= 0 && h.days_before_mending >= 0, `heir of ${h.row}|${h.deed} lies between deed and mending`);
  eq(h.heir_is_a_mending, J.some(q => q.repair === h.heir), `heir ${h.heir.slice(0, 7)} as a mending`); }
const HH = HEIRS.map(h => h.hours_after_deed);
const FR = J.filter(p => !p.seen_before), frL = FR.filter(p => p.code === 'lines');
// agreement, recounted from the per-pair codes
const CL = { same_commit: 'joined', lines: 'joined', name: 'joined', file: 'file', log_only: 'log' };
const AC = { same: 'joined', lines: 'joined', name: 'joined', file: 'file', log: 'log' };
const AK = { same_commit: 'same', lines: 'lines', name: 'name', file: 'file', log_only: 'log' };
let at = AG.by_pair;
if (process.env.ATELIER) { const A = JSON.parse(fs.readFileSync(process.env.ATELIER, 'utf8')).act.deeds;
  at = Object.fromEntries(A.filter(d => d.join && d.join !== 'none').map(d => [d.row + '|' + d.n, d.join]));
  for (const [k, v] of Object.entries(AG.by_pair)) eq(at[k], v, `the Atelier's code of ${k} as its file holds it`); }
const AGREE = J.filter(p => AC[at[p.row + '|' + p.deed]] === CL[p.code]).length, CODEAG = J.filter(p => at[p.row + '|' + p.deed] === AK[p.code]).length;
const kap = (() => { const xs = J.map(p => [CL[p.code], AC[at[p.row + '|' + p.deed]]]), n = xs.length, po = xs.filter(([a, b]) => a === b).length / n;
  const ks = ['joined', 'file', 'log'], pe = ks.reduce((s, k) => s + xs.filter(x => x[0] === k).length * xs.filter(x => x[1] === k).length, 0) / n / n; return (po - pe) / (1 - pe); })();
eq(Math.round(kap * 1000) / 1000, AG.results.class_kappa, 'kappa recounted');
const V = { P144: AGREE >= 70 ? 'held' : 'failed', P145: LEAD1 * 2 >= LINES ? 'held' : 'failed' };

// ---- optional: every pair looked up again in Git
if (process.env.CLONES) {
  const G = (repo, ...a) => { try { return execFileSync('git', ['--git-dir', path.join(process.env.CLONES, repo + '.git'), ...a], { stdio: ['ignore', 'pipe', 'ignore'] }).toString().trim(); } catch { return null; } };
  const anc = (repo, a, b) => { try { execFileSync('git', ['--git-dir', path.join(process.env.CLONES, repo + '.git'), 'merge-base', '--is-ancestor', a, b], { stdio: 'ignore' }); return true; } catch { return false; } };
  for (const p of J) { ok(G(p.repair_repo, 'cat-file', '-t', p.repair) === 'commit', `mending ${p.repair.slice(0, 8)} in ${p.repair_repo}`); }
  for (const h of HEIRS) { const p = J.find(q => q.row === h.row && q.deed === h.deed);
    ok(G(h.repo, 'cat-file', '-t', h.heir) === 'commit', `heir ${h.heir.slice(0, 8)} in ${h.repo}`);
    ok(anc(h.repo, h.heir, p.repair), `heir ${h.heir.slice(0, 8)} comes before its mending`);
    const dps = new Set(), hps = (G(h.repo, 'diff', '--name-only', '--no-renames', h.heir + '^', h.heir) || '').split('\n');
    for (const c of KC[p.row + '|' + p.deed].deed_commits.filter(x => x && x.repo === h.repo)) (G(h.repo, 'diff', '--name-only', '--no-renames', c.hash + '^1', c.hash) || '').split('\n').forEach(x => x && dps.add(x));
    ok(hps.some(x => dps.has(x)), `heir ${h.heir.slice(0, 8)} changes a path the deed changed`); }
}

const E = { a_joined: g(JOINED), a_pairs: g(77), a_lead: g(LEAD), joined: g(JOINED), pairs: g(77), same: g(SAME), lines: g(LINES), file: g(FILE), log: g(LOG),
  points: g(LEAD1), lines2: g(LINES), notpoints: g(LINES - LEAD1), heir_med: median(HH).toLocaleString('en-GB', { minimumFractionDigits: 1, maximumFractionDigits: 1 }),
  heir_1h: g(HH.filter(h => h < 1).length), heir_24h: g(HH.filter(h => h < 24).length),
  heir_arch: g(HEIRS.filter(h => h.signer === "the architect's name").length), heir_wf: g(HEIRS.filter(h => h.signer === 'a workflow or bot').length),
  heir_mend: g(HEIRS.filter(h => h.heir_is_a_mending).length), same2: g(SAME), hash: HASH.length === 1 ? 'one' : g(HASH.length), lead: g(LEAD), pairs2: g(77), pairs3: g(77),
  agree: g(AGREE), kappa: (Math.round(kap * 1000) / 1000).toLocaleString('en-GB', { minimumFractionDigits: 2, maximumFractionDigits: 3 }), code_agree: g(CODEAG),
  lines_equal: g(AG.results.lines_equal), both_lines: g(AG.results.both_lines),
  fr_joined: g(FR.filter(p => CL[p.code] === 'joined').length), fr_pairs: g(FR.length), fr_points: g(frL.filter(p => p.git_points).length), fr_lines: g(frL.length) };
ok(HEIRS.every(h => ['the architect\'s name', 'a workflow or bot'].includes(h.signer)), 'every heir signed by his name or a workflow');
const groups = { 'j-same': SAME, 'j-lead': LEAD1, 'j-join': LINES - LEAD1, 'j-file': FILE, 'j-log': LOG };

const browser = await chromium.launch();
for (const [w, scheme] of [[1100, 'light'], [390, 'dark']]) {
  const page = await browser.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme, deviceScaleFactor: 1 });
  const errs = []; page.on('pageerror', e => errs.push(String(e))); page.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
  await page.goto(url); await page.waitForTimeout(600);
  eq(errs.length, 0, `${w}: no errors ${errs.join(' | ')}`);
  eq(await page.evaluate(() => document.documentElement.scrollWidth), w, `${w}: no sideways scroll`);
  const got = await page.$$eval('[data-k89]', es => es.map(e => [e.getAttribute('data-k89'), e.textContent]));
  eq(got.length, Object.keys(E).length, `${w}: every figure of reading 89 is on the page`);
  for (const [k, v] of got) { ok(k in E, `${w}: figure ${k} is recomputed`); eq(v, E[k], `${w}: figure ${k}`); }
  for (const [c, n] of Object.entries(groups)) eq(await page.$$eval(`#joins rect.${c}`, rs => rs.length), n, `${w}: ${c} squares`);
  const au = await page.$$eval('#joins rect.au', rs => rs.map(r => r.dataset.pair));
  eq(au.length, J.filter(p => rd('results87.json').deeds.some(d => +d.row === p.row && +d.n === p.deed && d.kind === 'authority')).length, `${w}: acts of authority ringed`);
  const W = await page.evaluate(() => document.getElementById('joins').getBoundingClientRect().right);
  ok(W <= w, `${w}: the figure fits`);
  const pick = J.find(p => p.code === 'lines' && p.git_points === false);
  await page.click(`#joins rect[data-pair="${pick.row}|${pick.deed}"]`);
  const ro = await page.$eval('#joinout', e => ({ t: e.textContent, h: [...e.querySelectorAll('a')].map(a => a.href) }));
  ok(ro.h.some(h => h.endsWith('#L' + pick.log_line)), `${w}: readout links log line ${pick.log_line}`);
  ok(ro.h.some(h => h.endsWith('/commit/' + pick.repair)), `${w}: readout links the mending`);
  ok(ro.h.some(h => h.endsWith('/commit/' + pick.heirs_before_hashes[0])), `${w}: readout links the earlier heir`);
  const P = await page.$$eval('#preds89 p', ps => ps.map(p => [p.dataset.pred, p.querySelector('span').textContent]));
  eq(P.length, 2, `${w}: two predictions`); for (const [k, v] of P) eq(v, V[k], `${w}: prediction ${k}`);
  ok(await page.$eval('.kicker', e => e.textContent.includes('state 5, after the presentation')), `${w}: kicker names state 5`);
  ok(await page.$eval('#what-git-joins + p.note', e => e.textContent.includes('Corrected 21 November 2026') && e.textContent.includes("is the log's row, not Git")), `${w}: the corrected sentence is quoted and marked`);
  if (w === 1100 && !process.env.NOSHOT) { fs.mkdirSync(path.join(here, 'process'), { recursive: true });
    await page.screenshot({ path: path.join(here, 'process', '5.png'), fullPage: true }); }
  await page.close();
}
await browser.close();
console.log(`${checks - fails} of ${checks} checks passed`); process.exit(fails ? 1 : 0);
