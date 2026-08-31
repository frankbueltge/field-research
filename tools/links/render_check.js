// Render check: opens the artifact page from the filesystem at three viewport widths
// and reports horizontal overflow and console errors. Adopted from a sibling practice's
// transferable finding: read the page as a picture, not only as code.
//
// Usage: NODE_PATH=/opt/node22/lib/node_modules node tools/links/render_check.js <file.html>
const { chromium } = require('playwright');

(async () => {
  const file = 'file://' + require('path').resolve(process.argv[2]);
  const browser = await chromium.launch();
  let bad = 0;
  for (const width of [390, 768, 1280]) {
    const page = await browser.newPage({ viewport: { width, height: 900 } });
    const errors = [];
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    page.on('pageerror', e => errors.push(String(e)));
    const requests = [];
    page.on('request', r => { if (!r.url().startsWith('file://')) requests.push(r.url()); });
    await page.goto(file, { waitUntil: 'load' });
    const m = await page.evaluate(() => ({
      scroll: document.documentElement.scrollWidth,
      client: document.documentElement.clientWidth,
      wide: [...document.querySelectorAll('main *')]
        .filter(el => el.getBoundingClientRect().right > document.documentElement.clientWidth + 1)
        .map(el => el.tagName + '.' + (el.className || '')).slice(0, 6),
      text: document.body.innerText.length,
    }));
    const overflow = m.scroll > m.client + 1;
    if (overflow || errors.length || requests.length) bad++;
    console.log(`${width}px  overflow=${overflow} (${m.scroll}>${m.client})  ` +
      `console_errors=${errors.length}  network_requests=${requests.length}  text_chars=${m.text}`);
    if (m.wide.length) console.log('   wide elements:', m.wide.join(', '));
    errors.slice(0, 3).forEach(e => console.log('   error:', e.slice(0, 160)));
    requests.slice(0, 3).forEach(r => console.log('   network:', r.slice(0, 160)));
    await page.screenshot({ path: `/tmp/render-${width}.png`, fullPage: false });
    await page.close();
  }
  await browser.close();
  process.exit(bad ? 1 : 0);
})();
