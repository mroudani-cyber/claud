const { chromium } = require('playwright');
const EXEC='/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
(async()=>{
  const [,, port, W, H] = process.argv;
  const b=await chromium.launch({executablePath:EXEC});
  const p=await b.newPage({viewport:{width:+W,height:+H}});
  await p.goto('http://localhost:'+port+'/',{waitUntil:'networkidle'});
  await p.waitForTimeout(6200);
  const out = await p.evaluate(()=>{
    const de=document.documentElement, res=[];
    const path = el => { const a=[]; for(let n=el;n&&n!==document.body;n=n.parentElement)
      a.unshift(n.tagName.toLowerCase()+(n.className?'.'+String(n.className).trim().split(/\s+/).join('.'):'')); return a.join(' > '); };
    const clipped = el => { for(let q=el.parentElement;q&&q!==document.body;q=q.parentElement){
      const c=getComputedStyle(q); if(/hidden|clip|auto|scroll/.test(c.overflowX)||/hidden|clip/.test(c.overflow)) return true;} return false; };
    document.querySelectorAll('body *').forEach(el=>{
      const cs=getComputedStyle(el);
      if(cs.display==='none'||cs.visibility==='hidden'||cs.position==='fixed') return;
      const r=el.getBoundingClientRect(); if(!r.width||!r.height) return;
      if((r.right>de.clientWidth+2||r.left<-2)&&!clipped(el))
        res.push({p:path(el),l:Math.round(r.left),r:Math.round(r.right),vw:de.clientWidth});
    });
    return res.slice(0,12);
  });
  console.log(JSON.stringify(out,null,1));
  await b.close();
})();
