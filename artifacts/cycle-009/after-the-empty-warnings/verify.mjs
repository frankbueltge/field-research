// Study 31 page check: headless, 390 px light and 1100 px dark. Usage: NODE_PATH=<dir with playwright> node verify.mjs
import { createRequire } from "module"; import path from "path"; import url from "url"; import fs from "fs";
const require = createRequire(import.meta.url);
const pw = require("playwright");
const here = path.dirname(url.fileURLToPath(import.meta.url));
const R = JSON.parse(fs.readFileSync(path.join(here, "data/results31.json"), "utf8"));
let pass = 0, fail = 0; const ok = (n, c) => { c ? pass++ : fail++; console.log((c ? "PASS " : "FAIL ") + n); };
const b = await pw.chromium.launch(process.env.CHROMIUM ? { executablePath: process.env.CHROMIUM } : {});
for (const [w, scheme] of [[390, "light"], [1100, "dark"]]) {
  const p = await b.newPage({ viewport: { width: w, height: 900 }, colorScheme: scheme });
  const errs = []; p.on("pageerror", e => errs.push(String(e))); p.on("console", m => m.type() === "error" && errs.push(m.text()));
  await p.goto("file://" + path.join(here, "index.html"));
  ok(`${w}: no script errors`, errs.length === 0);
  ok(`${w}: no horizontal overflow`, await p.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1));
  ok(`${w}: across view: 5 rows`, await p.locator("#forest circle.pt").count() === 5);
  ok(`${w}: injuries: one filled dot (office, year before)`, await p.locator("#forest circle.pt.above").count() === 1);
  await p.locator("#forest g.row").nth(0).dispatchEvent("click");
  ok(`${w}: tap gives the replication's numbers`, (await p.textContent("#det")).includes(`${R.fits.past_inj.irr.toFixed(2)} per standard deviation (95 % interval ${R.fits.past_inj.lo.toFixed(2)}–${R.fits.past_inj.hi.toFixed(2)})`));
  await p.click("#seg-y button[data-v=fat]");
  ok(`${w}: deaths: past and future filled, the unconverged state fit dashed`, await p.locator("#forest circle.pt.above").count() === 2 && await p.locator("#forest circle.pt.nc").count() === 1);
  await p.locator("#forest g.row").nth(2).dispatchEvent("click");
  ok(`${w}: state deaths fit flagged as not converged`, (await p.textContent("#det")).includes("did not converge"));
  await p.click("#seg-v button[data-v=within]");
  ok(`${w}: within view: 2 rows`, await p.locator("#forest circle.pt").count() === 2);
  await p.click("#seg-y button[data-v=inj]");
  await p.locator("#forest g.row").nth(0).dispatchEvent("click");
  ok(`${w}: within injuries: 1.01 and 22 offices left out`, (await p.textContent("#det")).includes("1.01 per standard deviation") && (await p.textContent("#det")).includes("22 offices"));
  ok(`${w}: tercile table 3 rows`, await p.locator("#terc tbody tr").count() === 3);
  ok(`${w}: six predictions, six held`, (await p.locator("#pred tbody tr").count()) === 6 && (await p.locator("#pred td.held").count()) === 6);
  const bb = await p.locator("#forest").boundingBox();
  const ext = await p.evaluate(() => { const r = [...document.querySelectorAll("#forest text")].map(t => t.getBoundingClientRect()); return [Math.min(...r.map(x => x.left)), Math.max(...r.map(x => x.right))]; });
  ok(`${w}: figure and its labels fit the viewport`, bb && bb.x >= 0 && bb.x + bb.width <= w + 1 && ext[0] >= 0 && ext[1] <= w + 1);
  await p.click("#seg-v button[data-v=across]");
  await p.locator("#forest").scrollIntoViewIfNeeded();
  await p.screenshot({ path: path.join(process.env.SHOTS || "/tmp", `s31_${w}.png`), clip: { x: 0, y: Math.max(0, (await p.locator("#forest").boundingBox()).y - 80), width: w, height: 520 } });
  await p.close();
}
await b.close(); console.log(`${pass} of ${pass + fail} passed`); process.exit(fail ? 1 : 0);
