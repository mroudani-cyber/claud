const http=require('http'),fs=require('fs'),p=require('path');
const root=process.argv[2], port=+process.argv[3];
const T={'.html':'text/html;charset=utf-8','.css':'text/css;charset=utf-8','.js':'text/javascript;charset=utf-8','.json':'application/json','.svg':'image/svg+xml','.png':'image/png','.jpg':'image/jpeg','.woff2':'font/woff2','.mp4':'video/mp4','.webm':'video/webm'};
http.createServer((q,s)=>{
  let u=decodeURIComponent(q.url.split('?')[0]); if(u.endsWith('/'))u+='index.html';
  const f=p.join(root,u);
  if(!f.startsWith(p.resolve(root))){s.writeHead(403).end();return;}
  fs.readFile(f,(e,d)=>{ if(e){s.writeHead(404,{'content-type':'text/plain'}).end('404 '+u);return;}
    s.writeHead(200,{'content-type':T[p.extname(f)]||'application/octet-stream','cache-control':'no-store'}).end(d);});
}).listen(port,()=>console.log('serving',root,'on',port));
