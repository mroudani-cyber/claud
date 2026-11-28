const {chromium}=require('playwright');const fs=require('fs');
(async()=>{const fps=30,sub=8,shutter=0.5;const b=await chromium.launch({args:['--allow-file-access-from-files']});
const p=await b.newPage({viewport:{width:1080,height:1920}});await p.goto('file://'+process.cwd()+'/scene.html');
await p.waitForFunction(()=>window.READY);const D=await p.evaluate(()=>VIDEO.duration);fs.mkdirSync('fr',{recursive:true});
const F=Math.round(D*fps);const t0=Date.now();let i=0;
for(let f=0;f<F;f++)for(let k=0;k<sub;k++){const t=Math.max(0,Math.min(D-1e-3,(f+(k/(sub-1)-0.5)*shutter)/fps));
 await p.evaluate(t=>seek(t),t);await p.screenshot({path:`fr/${String(i++).padStart(5,'0')}.jpg`,type:'jpeg',quality:92});
 if(i%400==0)console.log(i,'/',F*sub,((Date.now()-t0)/1000).toFixed(0)+'s');}
await b.close();})();
