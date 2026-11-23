"""מצב טלפון לגרסת התלמידים: אותו קובץ, אותו תוכן — רק פריסה אחרת כשהמסך הוא של טלפון.

השקופית לא מוקטנת כתמונה אלא נפרסת לרוחב המסך: הטקסט בגודל קריא, כרטיסים נערמים,
וכשהשקופית ארוכה מהמסך — גוללים. רכיב רחב מדי (ציור, סולם, משוואה) מוקטן לבדו לרוחב המסך.
סרגל כלים קבוע בתחתית: אחורה, בית, מונה, קדימה.
זיהוי: הצד הקצר של המסך < 500 ומסך מגע. לבדיקה במחשב: ‎?phone=1
"""

CSS = r'''
html.ph,html.ph body{overflow:hidden}
html.ph #viewport{display:block;overflow-y:auto;overflow-x:hidden;bottom:48px;-webkit-overflow-scrolling:touch;overscroll-behavior:contain}
html.ph #stage{transform:none!important;width:var(--phw);height:auto;border-radius:0;box-shadow:none;overflow:visible;zoom:var(--phz)}
html.ph .slide{position:relative;inset:auto;display:none;opacity:1;transition:none;min-height:var(--phh);padding:30px 28px 64px}
html.ph .slide.on{display:block}
html.ph .slide.fl.on{display:flex}
html.ph #hint,html.ph #fsbtn{display:none!important}
html.ph #phbar{position:fixed;inset-inline:0;bottom:0;height:48px;background:#080F1A;z-index:24;border-top:1px solid rgba(255,255,255,.08)}
html.ph #navprev,html.ph #navnext,html.ph #home{top:auto;bottom:5px;transform:none}
html.ph #navprev{right:10px;left:auto}
html.ph #home{right:58px;left:auto}
html.ph #navnext{left:10px;right:auto}
html.ph #counter{bottom:12px;inset-inline-end:auto;left:50%;transform:translateX(-50%);z-index:25;background:none;font-size:14px}
html.ph #bar{bottom:48px;z-index:25}
html.ph #tapme{bottom:64px}
html.ph .timer{display:none}
html.ph .slide .pages{position:static;display:inline-block;margin:0 0 14px}
html.ph .slide .center-block{position:relative;inset:auto;padding:10px 20px}
html.ph .rowline{display:block}
html.ph .rowline .num{display:inline-flex;vertical-align:middle;margin-inline-end:10px}
html.ph .rowline>b:first-child{margin-inline-end:8px}
html.ph #navnext.end{width:auto;padding:0 18px;border-radius:19px}
html.ph #navnext.end .lbl{font-size:16px}
html.ph .head.indent{padding-inline-start:0}
html.ph [data-phflow]{position:static!important;inset:auto!important;width:auto!important;margin-top:24px!important}
html.ph .secwrap{transform:none!important}   /* שקופית מחיצה בעיצוב החדש (שיעור 6): ממורכזת ב־translateY, שבזרימה מעלה אותה מעבר לראש המסך */
'''

JS = r'''
<script>
(function(){
  var forced=/[?&]phone=1/.test(location.search);
  function isPhone(){ return forced || (Math.min(screen.width,screen.height)<500 && matchMedia('(pointer:coarse)').matches); }
  var root=document.documentElement, vp=document.getElementById('viewport'), stage=document.getElementById('stage');
  var bar=document.createElement('div'); bar.id='phbar'; document.body.appendChild(bar);
  // גודל המסך האמיתי (layout viewport) — לא inner*, שבאייפון משתנים בזום של אצבעות
  function W(){ return root.clientWidth; } function H(){ return root.clientHeight; }
  function setZ(z){ root.style.setProperty('--phz',z); root.style.setProperty('--phw',(W()/z)+'px'); }
  // כל שקופית בנפרד: הכי גדולה שאפשר, ומוקטנת רק עד שהיא נכנסת במסך. מתחת לרצפה — גוללים
  function layout(){
    var on=isPhone(); root.classList.toggle('ph',on); if(!on) return;
    var sl=document.querySelector('.slide.on'); if(!sl) return;
    var availH=H()-48, zmax=Math.max(0.72,Math.min(1,W()/1100));
    var zmin=Math.min(zmax, W()>H() ? availH/720 : 0.55), z=zmax;
    for(var i=0;i<10;i++){
      setZ(z); fitWide(sl);
      sl.style.minHeight='0px'; var vis=sl.offsetHeight*z; sl.style.minHeight='';
      if(vis<=availH+1 || z<=zmin) break;
      z=Math.max(zmin, z*Math.max(0.8, availH/vis));
    }
    root.style.setProperty('--phh',(availH/z)+'px');
  }
  // רכיב רחב מהשקופית מוקטן לבדו
  function fitWide(sl){
    var ch=sl.querySelectorAll('[data-phorig]');
    for(var i=0;i<ch.length;i++){ ch[i].style.cssText=ch[i].getAttribute('data-phorig'); ch[i].removeAttribute('data-phorig'); }
    // פס שמוצמד לתחתית השקופית — חוזר לזרימה, אחרי התוכן (אחרת הוא נופל על הטקסט כשהשקופית נגללת)
    for(var c0=sl.firstElementChild;c0;c0=c0.nextElementSibling){
      if(/\b(foot|timer|center-block|pages)\b/.test(c0.className)) continue;
      if(c0.hasAttribute('data-phflow') || getComputedStyle(c0).position==='absolute') c0.setAttribute('data-phflow','');
    }
    var cs=getComputedStyle(sl), sr=sl.getBoundingClientRect(), k=sr.width/sl.offsetWidth;
    var avail=sr.width-(parseFloat(cs.paddingLeft)+parseFloat(cs.paddingRight))*k+2;
    function mark(c){ if(!c.hasAttribute('data-phorig')) c.setAttribute('data-phorig',c.style.cssText); }
    // מעבר 1, מלמטה למעלה: שורות שגולשות ועמודות טקסט שנמחצו
    (function fix(el){
      for(var c=el.firstElementChild;c;c=c.nextElementSibling){
        if(c.classList.contains('foot')) continue;
        fix(c);
        var st=getComputedStyle(c), row=st.display==='flex' && st.flexDirection.indexOf('row')===0 && st.flexWrap==='nowrap';
        var longKid=false; for(var g0=c.firstElementChild;g0;g0=g0.nextElementSibling) if(g0.textContent.trim().length>40) longKid=true;
        if(row && longKid){
          // עמודת טקסט צרה מדי — העמודות נערמות זו מתחת לזו
          for(var g=c.firstElementChild;g;g=g.nextElementSibling)
            if(g.textContent.trim().length>40 && g.offsetWidth<260){
              mark(c); c.style.flexWrap='wrap';
              for(var g2=c.firstElementChild;g2;g2=g2.nextElementSibling){ mark(g2); g2.style.flex='1 1 100%'; g2.style.width='auto'; }
              break;
            }
        }
        else if(c.clientWidth>0 && c.scrollWidth>c.clientWidth+2 && st.overflowX==='visible'){
          // שורה שגולשת (משוואה, ממורכזת לשני הצדדים) — מקבלת את רוחב התוכן האמיתי, ובמעבר 2 מוקטנת
          mark(c); c.style.width=row?'max-content':c.scrollWidth+'px'; c.style.maxWidth='none'; c.style.flex='none';
        }
      }
    })(sl);
    // מעבר 2, מלמעלה למטה: רכיב רחב מהשקופית מוקטן כיחידה אחת
    (function walk(el){
      for(var c=el.firstElementChild;c;c=c.nextElementSibling){
        if(c.classList.contains('foot')) continue;
        var r=c.getBoundingClientRect();
        if(r.width>avail){ mark(c); c.style.zoom=avail/r.width; }
        else walk(c);
      }
    })(sl);
  }
  new MutationObserver(function(ms){
    for(var i=0;i<ms.length;i++){ var t=ms[i].target;
      if(t.classList.contains('slide') && t.classList.contains('on') && ms[i].oldValue.indexOf('on')<0){ vp.scrollTop=0; layout(); }
      else if(root.classList.contains('ph') && t.classList.contains('step') && t.classList.contains('show') && t.closest('.slide.on')){
        var r=t.getBoundingClientRect(), vr=vp.getBoundingClientRect();
        if(r.bottom>vr.bottom-8) vp.scrollBy({top:Math.min(r.bottom-vr.bottom+24, r.top-vr.top-12),behavior:'smooth'});
      }
    }
  }).observe(stage,{subtree:true,attributes:true,attributeFilter:['class'],attributeOldValue:true});
  addEventListener('resize',layout);
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(layout);
  layout();
})();
</script>
'''

def apply(s):
    s = s.replace('</style>', CSS + '</style>', 1)
    i = s.rindex('</body>')
    return s[:i] + JS + s[i:]
