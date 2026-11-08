// Study 64: open the page at 1100 px light and 390 px dark, check for errors and sideways scroll, write process/1.png.
import { createRequire } from 'module'; import path from 'path'; import { fileURLToPath } from 'url';
const require = createRequire('/opt/node-tools/node_modules/'); const { chromium } = require('playwright');
const here = path.dirname(fileURLToPath(import.meta.url)); const url = 'file://' + path.join(here, 'index.html');
const b = await chromium.launch(); let fails = 0;
for (const [w, scheme, shot] of [[1100, 'light', 'process/1.png'], [390, 'dark', null]]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme }); const errs = [];
  p.on('pageerror', e => errs.push(e.message)); p.on('console', m => m.type() === 'error' && errs.push(m.text()));
  await p.goto(url); await p.waitForTimeout(500);
  const r = await p.evaluate(() => ({ cells: document.querySelectorAll('.cell').length, rows: document.querySelectorAll('.rrow').length,
    preds: document.querySelectorAll('#preds tbody tr').length, sx: document.documentElement.scrollWidth > window.innerWidth,
    ans: document.querySelector('#answer').textContent.slice(0, 60) }));
  await p.click('[data-sort="deliv"]'); const top = await p.evaluate(() => document.querySelector('.rrow .cname b').textContent);
  const ok = !errs.length && r.cells === 61 && r.rows === 12 && r.preds === 5 && !r.sx && top === '10';
  if (!ok) fails++; console.log(w, scheme, ok ? 'PASS' : 'FAIL', JSON.stringify(r), 'top after sort:', top, errs.join('; '));
  if (shot) { await p.click('[data-sort="n"]'); await p.screenshot({ path: path.join(here, shot), fullPage: true }); }
  await p.close();
}
await b.close(); process.exit(fails ? 1 : 0);
