const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const EXEC = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

const site = process.argv[2];            // 'site-a-forge' | 'site-b-blueprint'
const port = process.argv[3] || '4600';
const label = process.argv[4] || 'a';
const vp = (process.argv[5] || 'desktop');
const SIZES = { desktop: [1600, 950], laptop: [1440, 900], tablet: [834, 1112], mobile: [390, 844] };
const [W, H] = SIZES[vp];

(async () => {
  const outDir = `tools/shots/${label}-${vp}`;
  fs.rmSync(outDir, { recursive: true, force: true });
  fs.mkdirSync(outDir, { recursive: true });

  const browser = await chromium.launch({ executablePath: EXEC, args: ['--force-color-profile=srgb'] });
  const ctx = await browser.newContext({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  const page = await ctx.newPage();

  const errors = [], warns = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); if (m.type() === 'warning') warns.push(m.text()); });
  page.on('pageerror', e => errors.push('PAGEERROR: ' + e.message));
  page.on('requestfailed', r => errors.push('REQFAIL: ' + r.url() + ' :: ' + (r.failure()||{}).errorText));

  await page.goto(`http://localhost:${port}/`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(6200);              // let preloader finish

  const total = await page.evaluate(() => document.documentElement.scrollHeight);
  
  // scroll in even increments across full page height
  const N = parseInt(process.env.STEPS || '18', 10);
  const overflow = [];
  for (let i = 0; i < N; i++) {
    const target = Math.round((total - H) * (i / (N - 1)));
    await page.evaluate(y => {
      if (window.__itm && window.__itm.lenis) { window.__itm.lenis.scrollTo(y, { immediate: true }); }
      window.scrollTo(0, y);
    }, target);
    await page.waitForTimeout(820);
    await page.screenshot({ path: path.join(outDir, `${String(i).padStart(2,'0')}.png`) });
    const ov = await page.evaluate(() => {
      const de = document.documentElement;
      const bad = [];
      const clipped = el => {
        for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
          const c = getComputedStyle(p);
          if (/hidden|clip|auto|scroll/.test(c.overflowX) || /hidden|clip/.test(c.overflow)) return true;
          if (c.position === 'fixed' || c.position === 'sticky') { /* keep walking */ }
        }
        return false;
      };
      document.querySelectorAll('body *').forEach(el => {
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden' || cs.opacity === '0') return;
        const r = el.getBoundingClientRect();
        if (r.width === 0 || r.height === 0) return;
        if ((r.right > de.clientWidth + 2 || r.left < -2) && !clipped(el)) {
          bad.push(`${el.tagName.toLowerCase()}.${(el.className||'').toString().trim().split(' ')[0]} L${Math.round(r.left)} R${Math.round(r.right)}`);
        }
      });
      // also detect text clipped by its own box (overflow of readable content)
      const cut = [];
      document.querySelectorAll('h1,h2,h3,p,li,span,a,b').forEach(el => {
        if (el.children.length) return;
        const cs = getComputedStyle(el);
        if (cs.display === 'none' || cs.visibility === 'hidden') return;
        if (el.scrollWidth > el.clientWidth + 4 && /hidden|clip/.test(cs.overflowX) && cs.textOverflow !== 'ellipsis' && cs.whiteSpace !== 'nowrap') {
          cut.push(`${el.tagName.toLowerCase()}.${(el.className||'').toString().trim().split(' ')[0]} sw${el.scrollWidth}>cw${el.clientWidth}`);
        }
      });
      return { docW: de.scrollWidth, cliW: de.clientWidth, bad: bad.slice(0, 8), cut: cut.slice(0, 6) };
    });
    if (ov.docW > ov.cliW + 1 || ov.bad.length || ov.cut.length) overflow.push({ step: i, y: target, ...ov });
  }
  await browser.close();
  const report = { site, vp, viewport: [W, H], pageHeight: total, screens: N, errors, warns: warns.slice(0,5), overflow };
  fs.writeFileSync(`tools/shots/${label}-${vp}.json`, JSON.stringify(report, null, 2));
  console.log(JSON.stringify({ vp, pageHeight: total, errors: errors.length, overflowSteps: overflow.length }, null, 2));
  if (errors.length) console.log('ERRORS:', errors.slice(0, 8));
  if (overflow.length) console.log('OVERFLOW:', JSON.stringify(overflow.slice(0, 3), null, 1));
})();
