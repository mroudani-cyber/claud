// Launch Refract via Playwright's Electron driver, wait, screenshot. Env S = workdir from setup.sh
const {_electron}=require('playwright');
(async()=>{const app=await _electron.launch({executablePath:process.env.S+'/el/node_modules/electron/dist/electron',args:['--no-sandbox',process.env.S+'/app'],env:{...process.env,NODE_OPTIONS:''}});
const p=await app.firstWindow();await p.waitForTimeout(6000);await p.screenshot({path:process.argv[2]||'refract.png'});await app.close();})();
