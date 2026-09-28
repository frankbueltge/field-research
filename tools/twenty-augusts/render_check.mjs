// Twenty Augusts — render the page from the filesystem at three widths, scripting off;
// record horizontal overflow and any network request. Session 173, 2026-09-28.
import { chromium } from 'playwright';
import { writeFileSync } from 'fs';
import { resolve } from 'path';
const art = resolve(process.argv[2]);
const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
const out = { note: 'Rendered from the filesystem with scripting off.', widths: [] };
for (const w of [390, 768, 1280]) {
  const ctx = await b.newContext({ viewport: { width: w, height: 900 }, javaScriptEnabled: false });
  const pg = await ctx.newPage(); const reqs = [];
  pg.on('request', r => { if (!r.url().startsWith('file:')) reqs.push(r.url()); });
  await pg.goto('file://' + art + '/index.html');
  const sw = await pg.evaluate(() => document.documentElement.scrollWidth);
  if (w === 390 && process.argv[3]) await pg.screenshot({ path: process.argv[3], fullPage: true });
  out.widths.push({ width: w, scrollWidth: sw, overflow: sw > w, external_requests: reqs.length });
  await ctx.close();
}
await b.close();
writeFileSync(art + '/data/render-check.json', JSON.stringify(out, null, 1));
console.log(JSON.stringify(out));
