const { chromium } = require('playwright');
const EXEC='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async()=>{
  const b=await chromium.launch({executablePath:EXEC});
  const p=await b.newPage({viewport:{width:1600,height:950}});
  const fails=[]; p.on('requestfailed',r=>fails.push(r.url()));
  const resp=[]; p.on('response',r=>{ if(/woff2|\.css|\.js/.test(r.url())) resp.push(r.status()+' '+r.url().split('/').slice(-1)[0]); });
  await p.goto('http://localhost:'+(process.argv[3]||4600)+'/',{waitUntil:'networkidle'});
  await p.waitForTimeout(4500);
  const d = await p.evaluate(()=>{
    const g=(sel,prop)=>{const e=document.querySelector(sel);return e?getComputedStyle(e)[prop]:null;};
    const meas=(sel)=>{const e=document.querySelector(sel);if(!e)return null;const r=e.getBoundingClientRect();
      return {w:Math.round(r.width),h:Math.round(r.height),l:Math.round(r.left),sw:e.scrollWidth,cw:e.clientWidth};};
    return {
      fontsLoaded:[...document.fonts].map(f=>f.family+':'+f.status),
      navDisplay:g('#nav','transform'),
      titleFont:g('.hero__title','fontFamily'),
      titleSize:g('.hero__title','fontSize'),
      heroTitle:meas('.hero__title'),
      ghost:meas('.hero__ghost'),
      footMark:meas('.foot__mark span'),
      footMarkBox:meas('.foot__mark'),
      procWrap:meas('.proc__wrap'),
      procSteps:meas('.proc__steps'),
      step0:meas('.step'),
      step0P:meas('.step p'),
      procStickyW:meas('.proc__sticky'),
      loaderGone: !document.querySelector('#loader'),
      lineWidths: [...document.querySelectorAll('.line')].slice(0,8).map(e=>({t:e.textContent.trim().slice(0,26),sw:e.scrollWidth,cw:e.clientWidth}))
    };
  });
  console.log(JSON.stringify({resp,fails,...d},null,1));
  await b.close();
})();
