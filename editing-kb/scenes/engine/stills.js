const {chromium}=require('playwright');
(async()=>{const b=await chromium.launch({args:['--allow-file-access-from-files']});const p=await b.newPage({viewport:{width:1080,height:1920}});
p.on('pageerror',e=>console.log('ERR',e.message));p.on('console',m=>{if(m.type()==='error')console.log('CERR',m.text())});
await p.goto('file://'+process.cwd()+'/'+(process.env.SCENE||'scene.html'));await p.waitForFunction(()=>window.READY,null,{timeout:20000});
const ts=process.argv[2].split(',').map(Number);let i=0;
for(const t of ts){await p.evaluate(t=>seek(t),t);await p.screenshot({path:`st_${i++}.jpg`,type:'jpeg',quality:80});}
await b.close();})();
