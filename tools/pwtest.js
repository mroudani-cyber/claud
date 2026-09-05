const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage();
  await p.setContent('<h1 style="font:700 40px system-ui">OK</h1>');
  await p.screenshot({ path: 'tools/t.png' });
  await b.close();
  console.log('playwright ok');
})();
