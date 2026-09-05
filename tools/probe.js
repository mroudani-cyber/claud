const { chromium } = require('playwright');
const EXEC='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async()=>{
  const [,, port, ...ys] = process.argv;
  const b=await chromium.launch({executablePath:EXEC});
  const p=await b.newPage({viewport:{width:1600,height:950}});
  await p.goto('http://localhost:'+port+'/',{waitUntil:'networkidle'});
  await p.waitForTimeout(6200);
  for (const y of ys){
    await p.evaluate(v=>{ if(window.__itm&&window.__itm.lenis) window.__itm.lenis.scrollTo(v,{immediate:true}); window.scrollTo(0,v); }, +y);
    await p.waitForTimeout(2500);
    await p.screenshot({path:`tools/probe-${y}.png`});
    console.log('shot', y);
  }
  await b.close();
})();
