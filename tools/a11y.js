const { chromium } = require('playwright');
const EXEC='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async()=>{
  const port=process.argv[2];
  const b=await chromium.launch({executablePath:EXEC});
  const p=await b.newPage({viewport:{width:1440,height:900}});
  const errs=[]; p.on('pageerror',e=>errs.push(e.message));
  await p.goto('http://localhost:'+port+'/',{waitUntil:'networkidle'});
  await p.waitForTimeout(6500);
  const r = await p.evaluate(()=>{
    const heads=[...document.querySelectorAll('h1,h2,h3,h4')].map(h=>h.tagName+': '+h.textContent.trim().replace(/\s+/g,' ').slice(0,44));
    const imgsNoAlt=[...document.querySelectorAll('img')].filter(i=>!i.hasAttribute('alt')).map(i=>i.src.split('/').pop());
    const emptyLinks=[...document.querySelectorAll('a')].filter(a=>!a.textContent.trim()&&!a.getAttribute('aria-label')).length;
    const lang=document.documentElement.lang;
    const title=document.title;
    const invisible=[...document.querySelectorAll('h1,h2,h3,p,li,dd')]
      .filter(e=>{const c=getComputedStyle(e);return c.opacity==='0'&&e.getBoundingClientRect().top<window.innerHeight&&e.getBoundingClientRect().bottom>0;}).length;
    return {lang,title,heads,imgsNoAlt,emptyLinks,invisibleInViewport:invisible};
  });
  // keyboard focus walk
  const focus=[];
  for(let i=0;i<9;i++){ await p.keyboard.press('Tab');
    focus.push(await p.evaluate(()=>{const a=document.activeElement;
      return a? a.tagName+(a.className?'.'+String(a.className).trim().split(/\s+/)[0]:'')+' :: '+(a.textContent||'').trim().replace(/\s+/g,' ').slice(0,28):'none';})); }
  console.log(JSON.stringify({...r, pageErrors:errs, tabOrder:focus},null,1));
  await b.close();
})();
