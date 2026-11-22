// בדיקת מצב טלפון: כל שקופית, כל הצעדים גלויים, 3 גדלי טלפון. מדווח טקסט על טקסט (OVL), טקסט מחוץ לשקופית (OUT), רכיבים שהוקטנו (zoom) וגובה מול מסך (h=).
// שימוש: PW=$(npm root -g)/playwright node tools/qa/phone.js docs <תיקיית-צילומים> lesson-01
const pw=require(process.env.PW);(async()=>{const b=await pw.chromium.launch();const D=require('path').resolve(process.argv[2]),SP=process.argv[3],F=process.argv[4]||'lesson-01';
const sizes=[['port',{viewport:{width:390,height:664},deviceScaleFactor:2,isMobile:true,hasTouch:true}],['land',{viewport:{width:844,height:300},deviceScaleFactor:2,isMobile:true,hasTouch:true}],['se-port',{viewport:{width:375,height:553},deviceScaleFactor:2,isMobile:true,hasTouch:true}]];
for(const [name,opt] of sizes){const c=await b.newContext(opt);const p=await c.newPage();
 p.on('pageerror',e=>console.log('JSERR',e.message));
 await p.goto('file://'+D+'/'+F+'.html?phone=1');await p.waitForTimeout(800);
 const deck=await p.evaluate(()=>!!document.getElementById('deck'));const n=await p.evaluate(()=>document.querySelectorAll('section.slide, #deck > section.s').length);const issues=[];
 for(let i=0;i<n;i++){
  if(deck){ await p.evaluate(i=>{location.hash='#'+(i+1)},i); await p.waitForTimeout(200); await p.evaluate(()=>{const sl=document.querySelector('#deck > section.s.on');sl.querySelectorAll('.frag').forEach(e=>e.classList.add('show'));sl.querySelectorAll('.mcq').forEach(e=>e.classList.add('done'));}); }
  else await p.evaluate(i=>{ document.dispatchEvent(new KeyboardEvent('keydown',{key:'Home',bubbles:true})); for(let k=0;k<i;k++) document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowDown',bubbles:true}));},i);
  await p.waitForTimeout(150);
  // all steps
  for(let k=0;k<(deck?0:12);k++){ const more=await p.evaluate(()=>{const sl=document.querySelector('.slide.on');const n=+sl.dataset.steps||0;return sl.querySelectorAll('.step.show').length<sl.querySelectorAll('.step').length;}); if(!more) break; await p.evaluate(()=>document.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowLeft',bubbles:true}))); await p.waitForTimeout(80);}
  await p.waitForTimeout(700);
  const r=await p.evaluate(()=>{const sl=document.querySelector('.slide.on, #deck > section.s.on');const sr=sl.getBoundingClientRect();const out=[];
   const rects=[];const w=document.createTreeWalker(sl,NodeFilter.SHOW_TEXT);let t;
   while(t=w.nextNode()){ if(!t.textContent.trim())continue; const pe=t.parentElement; if(getComputedStyle(pe).opacity==='0'||pe.closest('svg .w1,svg .w2,svg .frag:not(.show)'))continue;
     const rg=document.createRange();rg.selectNodeContents(t);for(const q of rg.getClientRects()){ if(q.width<1)continue;
       if(q.left<sr.left-1||q.right>sr.right+1) out.push('OUT:'+t.textContent.trim().slice(0,15));
       rects.push([q,t.textContent.trim().slice(0,15),pe]);}}
   for(let a=0;a<rects.length;a++)for(let b2=a+1;b2<rects.length;b2++){const [x,tx,pa]=rects[a],[y,ty,pb]=rects[b2]; if(pa===pb)continue;
     const ix=Math.min(x.right,y.right)-Math.max(x.left,y.left), iy=Math.min(x.bottom,y.bottom)-Math.max(x.top,y.top);
     if(ix>3&&iy>3) out.push('OVL:'+tx+'|'+ty);}
   const zs=[...sl.querySelectorAll('[data-phorig]')].filter(e=>e.style.zoom).map(e=>(e.className||e.tagName)+'@'+(+e.style.zoom).toFixed(2));
   return {out:[...new Set(out)].slice(0,6),zs,h:Math.round(sl.getBoundingClientRect().height),vh:Math.round((document.getElementById('viewport')||document.getElementById('stage')).clientHeight)};});
  if(r.out.length||r.zs.length) issues.push((i+1)+': '+r.out.join(', ')+(r.zs.length?' zoom['+r.zs.join(',')+']':''));
  issues.push((i+1)+' h='+r.h+'/'+r.vh);
  await p.screenshot({path:`${SP}/ph-${name}-${String(i+1).padStart(2,'0')}.png`,fullPage:false});
 }
 console.log('==',name);console.log(issues.join('\n'));await c.close();}
await b.close();})();
