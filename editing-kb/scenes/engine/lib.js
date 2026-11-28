// Shared editorial motion engine: pure seek(t), camera, depth of field from z, physical drops.
const clamp=(x,a=0,b=1)=>Math.min(b,Math.max(a,x)),lerp=(a,b,t)=>a+(b-a)*t,seg=(t,a,b)=>clamp((t-a)/(b-a));
const E={expoOut:x=>x>=1?1:1-Math.pow(2,-10*x),expoIn:x=>x<=0?0:Math.pow(2,10*x-10),cubicOut:x=>1-Math.pow(1-x,3),cubicIn:x=>x*x*x,
 inOutCubic:x=>x<.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2,inOutQuart:x=>x<.5?8*x**4:1-Math.pow(-2*x+2,4)/2,inOutSine:x=>-(Math.cos(Math.PI*x)-1)/2,quadIn:x=>x*x,quartOut:x=>1-Math.pow(1-x,4),lin:x=>x};
// kf([[t, v1, v2, ..., 'ease'], ...]) -> t => [v1, v2, ...]
const kf=keys=>t=>{if(t<=keys[0][0])return keys[0].slice(1,-1);for(let i=1;i<keys.length;i++){const a=keys[i-1],b=keys[i];if(t<=b[0]){const e=E[b[b.length-1]](seg(t,a[0],b[0]));return a.slice(1,-1).map((v,j)=>lerp(v,b[j+1],e))}}return keys[keys.length-1].slice(1,-1)};
const $=id=>document.getElementById(id);
const place=(id,x,y,r=0)=>{const e=$(id);e._x=x;e._y=y;e._r=r;};
// a physical drop: falls from height h to rest z in dur (gravity = quadIn), no bounce; returns {z,o,rr}
const drop=(t,t0,dur,h,zRest,r0=0)=>{const k=seg(t,t0,t0+dur);return {z:lerp(h,zRest,E.quadIn(k)),o:k>0?clamp(k*3):0,rr:lerp(r0,0,E.cubicOut(k))}};
const shake=(t,t0,amp=10,len=.22)=>{const k=seg(t,t0,t0+len);if(k<=0||k>=1)return[0,0];const a=(1-k)*(1-k)*amp;return[a*Math.sin(k*34),a*Math.cos(k*29)]};
// ink-in words: per-word opacity+blur, no translate
const inkWords=(sel,t,times,d=.14)=>[...document.querySelectorAll(sel+' .w')].forEach((w,i)=>{const k=seg(t,times[i],times[i]+d);w.style.opacity=k;w.style.filter=`blur(${(1-k)*6}px)`});
const typeText=(el,full,t,t0,cps)=>{const n=Math.floor(clamp((t-t0)*cps,0,full.length));el.textContent=full.slice(0,n);};
// render all .el with camera + depth of field. st[id] = {z,o,rr,sc}
function renderWorld(t,camv,fz,st,shk=[0,0]){
 const [cx,cy,s,r]=camv;
 $('world').style.transform=`translate(${540+shk[0]}px,${960+shk[1]}px) rotate(${r}deg) scale(${s}) translate(${-cx}px,${-cy}px)`;
 for(const e of document.querySelectorAll('.el')){
  const S=st[e.id]||{};const z=S.z!==undefined?S.z:+(e.dataset.z||0),o=S.o!==undefined?S.o:1;
  const sc=(1+z*0.0022)*(S.sc||1), blur=Math.min(14,Math.abs(z-fz)*0.16)/Math.max(s,0.3);
  const flat=e.dataset.flat!==undefined;
  const sh=flat?'':`drop-shadow(${(z*0.18+2).toFixed(1)}px ${(z*0.36+4).toFixed(1)}px ${(z*0.5+5).toFixed(1)}px rgba(40,28,10,${(0.30-Math.min(z,300)*0.0006).toFixed(3)}))`;
  e.style.transform=`translate(${e._x}px,${e._y}px) rotate(${e._r+(S.rr||0)}deg) scale(${sc})`;
  e.style.filter=sh+(blur>0.25?` blur(${blur.toFixed(2)}px)`:'')+(S.extra||'');
  e.style.opacity=o;
 }
 $('grain').style.transform=`translate(${(Math.floor(t*24)*37)%50}px,${(Math.floor(t*24)*53)%50}px)`;
}
