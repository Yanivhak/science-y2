"""מצב טלפון למצגות על המנוע החדש (tools/deck, משיעור 7): אותו קובץ ואותו תוכן — פריסה אחרת כשהמסך הוא של טלפון.

השקופית לא מוקטנת כתמונה: לאורך היא נבנית ברוחב 640 והעמודות נערמות (טקסט מעל ציור, כרטיסים זה מתחת לזה); לרוחב — ברוחב 1000, בלי ערימה;
והכול מוגדל לרוחב המסך. שקופית ארוכה מהמסך — גוללים, וכשנחשף צעד מתחת לגובה המסך הוא נגלל אליו.
סרגל בתחתית: אחורה, בית, מונה, קדימה. טיימרים מוסתרים (כלי של המורה). ההנפשות עוברות לבד לסידור „זה מעל זה”.
זיהוי — כמו במצגות הישנות (tools/phone_mode.py): הצד הקצר של המסך < 500 ומסך מגע. לבדיקה במחשב: ?phone=1
"""

CSS = r'''
html.ph,html.ph body{overflow:hidden}
html.ph #stage{bottom:48px!important;overflow-y:auto;overflow-x:hidden;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
html.ph #deck{position:relative;left:auto;top:auto;margin:0;width:var(--phw);height:auto;min-height:var(--phh);transform:none!important;zoom:var(--phz)}
html.ph #deck .s{position:relative;inset:auto;display:none;opacity:1;visibility:visible;transition:none;min-height:var(--phh);padding:84px 26px 36px;overflow:visible}
html.ph #deck .s.on{display:flex}
html.ph #deck .s--sec,html.ph #deck .s--cover{justify-content:center}
html.ph .s--cover>.art{display:none}
html.ph .cover__brand{position:static!important;margin-bottom:28px}
html.ph.phport .split{grid-template-columns:1fr!important;gap:22px}
html.ph.phport .cards.c2,html.ph.phport .cards.c3,html.ph.phport .cards.c4{grid-template-columns:1fr!important}
html.ph.phport .cards.c5,html.ph.phport .mcq.four{grid-template-columns:1fr 1fr!important}
html.ph.phport .stats,html.ph.phport .stats.two,html.ph.phport .stats.four{grid-template-columns:1fr!important}
html.ph.phport .tiles5{grid-template-columns:repeat(3,1fr)}
html.ph .figrow{flex-wrap:wrap;gap:18px}
html.ph .art svg,html.ph .fig svg,html.ph .card svg{max-width:100%;height:auto}
html.ph.phport .hdr{display:block}
html.ph .timer,html.ph #hint{display:none!important}
html.ph .tbl{font-size:22px}
html.ph .tbl td,html.ph .tbl th{padding:6px 8px}
html.ph .t-xl{font-size:68px}
html.ph .sec__n{font-size:120px;line-height:1;margin-bottom:18px}
html.ph .ttl{line-height:1.2}
html.ph .an-cap{padding:0 8px 44px}
html.ph #phbar{position:fixed;inset-inline:0;bottom:0;height:48px;background:#04060C;z-index:24;border-top:1px solid rgba(255,255,255,.1)}
html.ph #navprev,html.ph #navnext,html.ph #home{top:auto;bottom:5px;transform:none}
html.ph #navprev{right:10px;left:auto}
html.ph #home{right:58px;left:auto}
html.ph #navnext{left:10px;right:auto}
html.ph #navnext.end{width:auto;padding:0 18px;border-radius:19px}
html.ph #navnext.end .lbl{font-size:16px}
html.ph #num{position:fixed;left:50%;bottom:16px;transform:translateX(-50%);z-index:25}
html.ph #bar{z-index:25}
html.ph .ch__lesson{display:none}
html.ph #chrome{padding:0 26px}
html.ph #chrome::after{inset-inline:26px}
'''

JS = r'''
<script>
(function(){
  var forced=/[?&]phone=1/.test(location.search);
  function isPhone(){ return forced || (Math.min(screen.width,screen.height)<500 && matchMedia('(pointer:coarse)').matches); }
  var root=document.documentElement, stage=document.getElementById('stage'), deck=document.getElementById('deck');
  var bar=document.createElement('div'); bar.id='phbar'; document.body.appendChild(bar);
  // גודל המסך האמיתי (layout viewport) — לא inner*, שבאייפון משתנים בזום של אצבעות
  function layout(){
    var on=isPhone(); root.classList.toggle('ph',on); if(!on) return;
    // לאורך: רוחב 640 והעמודות נערמות; לרוחב: רוחב 1000 והעמודות נשארות זו ליד זו
    var w=root.clientWidth, port=root.clientHeight>w, lw=port?640:1000, z=w/lw;
    root.classList.toggle('phport',port);
    root.style.setProperty('--phw',lw+'px'); root.style.setProperty('--phz',z);
    root.style.setProperty('--phh',((root.clientHeight-48)/z)+'px');
  }
  new MutationObserver(function(ms){
    if(!root.classList.contains('ph')) return;
    for(var i=0;i<ms.length;i++){ var t=ms[i].target, was=ms[i].oldValue||'';
      if(t.parentNode===deck && t.classList.contains('s') && t.classList.contains('on') && !/\bon\b/.test(was)) stage.scrollTop=0;
      else if((t.classList.contains('show')&&!/\bshow\b/.test(was)) || (t.classList.contains('done')&&!/\bdone\b/.test(was))){
        var r=t.getBoundingClientRect(), vr=stage.getBoundingClientRect();
        if(r.bottom>vr.bottom-8) stage.scrollBy({top:Math.min(r.bottom-vr.bottom+24, r.top-vr.top-12),behavior:'smooth'});
      }
    }
  }).observe(deck,{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});
  // מה שעדיין רחב מהשקופית (שורת אטומים, טבלה, תרשים זרימה) — מוקטן כיחידה אחת לרוחב שלו (22.11)
  function fit(sl){
    if(!sl||!root.classList.contains('ph')) return;
    var z=sl.querySelectorAll('[data-phz]'); for(var i=0;i<z.length;i++){ z[i].style.zoom=''; z[i].removeAttribute('data-phz'); }
    for(var pass=0;pass<3;pass++){
      var all=sl.querySelectorAll('*'), done=false;
      for(var i=0;i<all.length;i++){ var e=all[i];
        if(e.closest('svg')||e.closest('[data-phz]')||!e.children.length||!e.offsetParent) continue;
        var cs=getComputedStyle(e); if(cs.position==='absolute'||cs.position==='fixed') continue;
        var r=e.getBoundingClientRect(); if(r.width<40) continue;
        var lo=r.left, hi=r.right;
        for(var c=0;c<e.children.length;c++){ var k=e.children[c], kc=getComputedStyle(k);
          if(kc.position==='absolute'||kc.position==='fixed'||kc.display==='none') continue;
          var q=k.getBoundingClientRect(); if(!q.width) continue; lo=Math.min(lo,q.left); hi=Math.max(hi,q.right); }
        var need=hi-lo; if(need>r.width+4){ e.style.zoom=(r.width/need).toFixed(3); e.setAttribute('data-phz','1'); done=true; }
      }
      if(!done) break;
    }
  }
  function cur(){ return deck.querySelector('.s.on'); }
  new MutationObserver(function(ms){ for(var i=0;i<ms.length;i++){ var t=ms[i].target;
    if(t.parentNode===deck&&t.classList.contains('on')&&!/\bon\b/.test(ms[i].oldValue||'')) setTimeout(function(){fit(cur())},30); } })
    .observe(deck,{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});
  addEventListener('resize',function(){ setTimeout(function(){fit(cur())},60); });
  addEventListener('resize',layout);
  layout();
  setTimeout(function(){fit(cur())},60);
})();
</script>
'''

def apply(s):
    s = s.replace('</style>', CSS + '</style>', 1)
    i = s.rindex('</body>')
    return s[:i] + JS + s[i:]
