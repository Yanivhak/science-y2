/* Deck engine for the lecture "from the road to space".
   A copy of the engine of the four "future in space" lessons, with the same keys, plus two additions:
   each slide can set its chapter colour (data-ch), and a slide can hand the advance key to its own
   controller (data-hook, registered in window.DeckHooks), so the launch scene runs inside the deck. */
(function(){
  var deck=document.getElementById('deck'),
      slides=[].slice.call(deck.querySelectorAll('.s')),
      bar=document.querySelector('#bar i'),
      num=document.getElementById('num'),
      chSec=document.getElementById('chSec'),
      notes=document.getElementById('notes'),
      ov=document.getElementById('ov'), ovg=document.getElementById('ovg'),
      guide=document.getElementById('guide'),
      help=document.getElementById('help'),
      act=document.getElementById('act'),
      stage=document.getElementById('stage'),
      i=0, notesOn=false, t0=null,
      reveal=/[?&]reveal\b/.test(location.search),
      online=/^https?:$/.test(location.protocol);

  /* ---- scale stage to viewport ---- */
  function fit(){
    var nh = notes.classList.contains('on') ? notes.offsetHeight : 0;
    stage.style.bottom = nh+'px';
    var availH = Math.max(120, window.innerHeight - nh);
    var s=Math.min(window.innerWidth/1280, availH/720);
    deck.style.transform='scale('+s+')';
  }
  window.addEventListener('resize',fit); fit();

  function mins(sl){return parseFloat(sl.getAttribute('data-min')||'0')||0;}
  function fmt(m){return String(Math.round(m*10)/10);}
  function pad(n){return (n<10?'0':'')+n;}
  var core=0, extra=0;
  slides.forEach(function(sl){ if(sl.hasAttribute('data-skip')) extra+=mins(sl); else core+=mins(sl); });

  /* ---- overview cards ---- */
  slides.forEach(function(sl,n){
    var t=sl.getAttribute('data-title')||'שקופית';
    var d=document.createElement('div');
    d.className='ovc'+(sl.hasAttribute('data-skip')?' skip':'');
    d.innerHTML='<b>'+pad(n+1)+'</b>'+t+'<em>'+(mins(sl)?fmt(mins(sl))+' דק׳':'')+(sl.hasAttribute('data-skip')?' · ניתן לדלג':'')+'</em>';
    d.onclick=function(){go(n,false);toggleOv(false);};
    ovg.appendChild(d);
  });
  var ovcs=[].slice.call(ovg.children);

  /* ---- printable lesson guide, built from the speaker notes ---- */
  (function(){
    var b=document.body;
    var h='<div class="g"><div class="g__bar"><button id="gPrint">הדפסה</button><button id="gClose">סגירה</button></div>'+
      '<h1>דף ההרצאה: '+(b.getAttribute('data-title')||document.title)+'</h1>'+
      '<p class="g__meta">'+(b.getAttribute('data-meta')||'')+' ליבת ההרצאה: כ-'+fmt(core)+' דקות. עם שקופיות ההרחבה: כ-'+fmt(core+extra)+' דקות.</p><ol>';
    slides.forEach(function(sl,n){
      var m=mins(sl);
      h+='<li class="g__it"><div class="g__h"><span class="mono">'+pad(n+1)+'</span><b>'+(sl.getAttribute('data-title')||'')+'</b>'+
         (m?'<em>'+fmt(m)+' דק׳</em>':'')+(sl.hasAttribute('data-skip')?'<i>ניתן לדלג</i>':'')+'</div>'+
         '<div class="g__n">'+(sl.getAttribute('data-notes')||'')+'</div></li>';
    });
    guide.innerHTML=h+'</ol></div>';
    document.getElementById('gPrint').onclick=function(){window.print();};
    document.getElementById('gClose').onclick=function(){toggleGuide(false);};
  })();

  /* ---- videos: embed when served over http, open YouTube when opened as a local file ---- */
  function poster(el){
    var id=el.getAttribute('data-id'), own=el.getAttribute('data-poster');
    el.classList.remove('playing');
    el.innerHTML='<img alt=""><span class="yt__play"></span>'+
      '<span class="yt__lbl">'+(online?'לחצו להפעלה, או הקישו P':'לחצו לפתיחה ביוטיוב')+'</span>';
    var im=el.querySelector('img');
    /* YouTube answers a missing maxres thumbnail with a 120px grey placeholder, not with an error */
    im.onload=function(){ if(!own && im.naturalWidth<=120 && im.src.indexOf('hqdefault')<0) im.src='https://i.ytimg.com/vi/'+id+'/hqdefault.jpg'; };
    im.onerror=function(){ im.onerror=null; im.src='https://i.ytimg.com/vi/'+id+'/hqdefault.jpg'; };
    im.src=own||('https://i.ytimg.com/vi/'+id+'/maxresdefault.jpg');
  }
  function play(el){
    var id=el.getAttribute('data-id'), st=el.getAttribute('data-start')||'0', en=el.getAttribute('data-end');
    if(!online){ window.open('https://www.youtube.com/watch?v='+id+(st!=='0'?'&t='+st+'s':''),'_blank','noopener'); return; }
    el.innerHTML='<iframe src="https://www.youtube-nocookie.com/embed/'+id+'?autoplay=1&rel=0&hl=he&cc_lang_pref=he&start='+st+(en?'&end='+en:'')+
      '" allow="autoplay; encrypted-media; fullscreen; picture-in-picture" allowfullscreen></iframe>';
    el.classList.add('playing');
  }
  var yts=[].slice.call(document.querySelectorAll('.yt'));
  yts.forEach(function(el){ poster(el); el.addEventListener('click',function(e){ e.stopPropagation(); if(!el.classList.contains('playing')) play(el); }); });

  /* ---- steps: fragments and multiple choice questions, revealed in document order by the advance key ---- */
  function steps(sl){return [].slice.call(sl.querySelectorAll('.frag,.mcq'));}
  function isDone(el){return el.classList.contains(el.classList.contains('mcq')?'done':'show');}
  function countUp(el){
    [].forEach.call(el.querySelectorAll('[data-count]'),function(c){
      var to=parseFloat(c.getAttribute('data-count')), dec=(c.getAttribute('data-count').split('.')[1]||'').length, t1=null, dur=900;
      function tick(ts){ if(t1===null) t1=ts; var k=Math.min(1,(ts-t1)/dur), v=to*(1-Math.pow(1-k,3));
        c.textContent=v.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec});
        if(k<1) requestAnimationFrame(tick); }
      requestAnimationFrame(tick);
      /* if the tab is not painting, requestAnimationFrame never fires: make sure the final value is there */
      setTimeout(function(){ c.textContent=to.toLocaleString('en-US',{minimumFractionDigits:dec,maximumFractionDigits:dec}); },dur+200);
    });
  }
  function setStep(el,show,quiet){
    if(el.classList.contains('mcq')){
      el.classList.toggle('done',show);
      if(!show) [].forEach.call(el.querySelectorAll('button'),function(b){b.classList.remove('wrong');});
    } else {
      el.classList.toggle('show',show);
      if(show && !quiet) countUp(el);
    }
  }
  function setAll(sl,show){steps(sl).forEach(function(el){setStep(el,show,true);});}

  /* ---- hooks: an interactive slide takes the advance key while it has something to do ---- */
  function hook(sl){ var n=sl&&sl.getAttribute('data-hook'), H=window.DeckHooks||{}; return n&&H[n]?H[n]:null; }

  [].forEach.call(document.querySelectorAll('.mcq'),function(m){
    [].forEach.call(m.querySelectorAll('button'),function(b,n){
      if(!b.querySelector('i')){ var t=document.createElement('i'); t.textContent='אבגדהו'.charAt(n); b.insertBefore(t,b.firstChild); }
      b.classList.toggle('right',b.hasAttribute('data-ok'));
      b.addEventListener('click',function(e){
        e.stopPropagation();
        if(m.classList.contains('done')) return;
        if(b.hasAttribute('data-ok')) m.classList.add('done'); else b.classList.add('wrong');
      });
    });
  });

  /* ---- countdown timers for group work ---- */
  function showT(el){ var s=el._left; el.firstChild.nodeValue=pad(Math.floor(s/60))+':'+pad(s%60); }
  [].forEach.call(document.querySelectorAll('.timer'),function(el){
    el._total=parseInt(el.getAttribute('data-sec'),10)||180; el._left=el._total;
    el.innerHTML='00:00<small>לחצו להפעלה, או הקישו T</small>'; showT(el);
    el.addEventListener('click',function(e){ e.stopPropagation(); toggleTimer(el); });
  });
  function toggleTimer(el){
    if(el.classList.contains('end')){ el.classList.remove('end'); el._left=el._total; showT(el); return; }
    if(el._iv){ clearInterval(el._iv); el._iv=null; el.classList.remove('run'); return; }
    el.classList.add('run');
    el._iv=setInterval(function(){
      el._left--; showT(el);
      if(el._left<=0){ clearInterval(el._iv); el._iv=null; el.classList.remove('run'); el.classList.add('end'); }
    },1000);
  }
  function stopTimers(sl){ [].forEach.call(sl.querySelectorAll('.timer'),function(el){ if(el._iv){clearInterval(el._iv);el._iv=null;} el.classList.remove('run','end'); el._left=el._total; showT(el); }); }

  /* ---- activity overlay: the student mission page, shown on the board ---- */
  function openAct(url){ act.querySelector('iframe').src=url; act.classList.add('on'); }
  function closeAct(){ if(!act.classList.contains('on')) return; act.classList.remove('on'); act.querySelector('iframe').src='about:blank'; try{document.body.focus();}catch(e){} }
  [].forEach.call(document.querySelectorAll('[data-act]'),function(b){
    b.addEventListener('click',function(e){ e.preventDefault(); e.stopPropagation(); openAct(b.getAttribute('data-act')); });
  });
  act.querySelector('button').addEventListener('click',closeAct);
  window.addEventListener('message',function(e){ if(e.data==='act-close') closeAct(); });

  function go(n,back){
    if(n<0||n>=slides.length) return;
    [].forEach.call(slides[i].querySelectorAll('.yt.playing'),poster);
    [].forEach.call(slides[i].querySelectorAll('video'),function(v){ try{v.pause();}catch(e){} });
    stopTimers(slides[i]);
    var ho=hook(slides[i]); if(ho&&ho.leave) ho.leave(slides[i]);
    slides[i].classList.remove('on');
    i=n;
    document.body.setAttribute('data-ch',slides[i].getAttribute('data-ch')||'');
    setAll(slides[i],!!back||reveal);
    slides[i].classList.add('on');
    deck.classList.toggle('nochrome',!slides[i].getAttribute('data-sec'));
    deck.classList.toggle('cover-on',i===0);
    chSec.textContent=slides[i].getAttribute('data-sec')||'';
    bar.style.width=((i+1)/slides.length*100)+'%';
    draw();
    notes.innerHTML=slides[i].getAttribute('data-notes')||'<b>אין הערות לשקופית זו</b>';
    ovcs.forEach(function(c,k){c.classList.toggle('cur',k===i);});
    [].forEach.call(slides[i].querySelectorAll('video[data-auto]'),function(v){ try{v.currentTime=0;var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){});}catch(e){} });
    var hn=hook(slides[i]); if(hn&&hn.enter) hn.enter(slides[i],!!back||reveal);
    try{ history.replaceState(null,'','#'+(i+1)); }catch(e){}
  }
  function draw(){
    var s=pad(i+1)+' / '+pad(slides.length);
    if(t0!==null){var e=Math.floor((Date.now()-t0)/1000); s+='  ·  '+pad(Math.floor(e/60))+':'+pad(e%60);}
    num.textContent=s;
  }
  setInterval(draw,1000);
  function next(){
    if(t0===null) t0=Date.now();
    var h=hook(slides[i]); if(h&&h.next&&h.next(slides[i])) return;
    var f=steps(slides[i]).filter(function(x){return !isDone(x);});
    if(f.length){setStep(f[0],true);return;}
    go(i+1,false);
  }
  function prev(){
    var h=hook(slides[i]); if(h&&h.prev&&h.prev(slides[i])) return;
    var f=steps(slides[i]).filter(isDone);
    if(f.length){setStep(f[f.length-1],false);return;}
    go(i-1,true);
  }
  function toggleNotes(v){notesOn=(v===undefined)?!notesOn:v;notes.classList.toggle('on',notesOn);fit();}
  function toggleOv(v){ov.classList.toggle('on',(v===undefined)?!ov.classList.contains('on'):v);}
  function toggleHelp(v){help.classList.toggle('on',(v===undefined)?!help.classList.contains('on'):v);}
  function toggleGuide(v){guide.classList.toggle('on',(v===undefined)?!guide.classList.contains('on'):v);}

  document.addEventListener('keydown',function(e){
    var k=e.key;
    /* S opens the notes, so Cmd+S is an easy slip: do not let it save a copy of the page */
    if((e.metaKey||e.ctrlKey)&&(k==='s'||k==='S'||k==='ד')){e.preventDefault();return;}
    if(e.metaKey||e.ctrlKey||e.altKey) return;
    if(k==='Escape'){closeAct();toggleOv(false);toggleHelp(false);toggleGuide(false);return;}
    if(act.classList.contains('on')) return;
    if(k==='g'||k==='G'||k==='ע'){e.preventDefault();toggleGuide();return;}
    if(guide.classList.contains('on')) return;
    if(k==='?'||k==='/'){e.preventDefault();toggleHelp();return;}
    if(k==='o'||k==='O'||k==='ם'){e.preventDefault();toggleOv();return;}
    if(k==='s'||k==='S'||k==='ד'){e.preventDefault();toggleNotes();return;}
    if(k==='h'||k==='H'||k==='י'){e.preventDefault();go(0,false);return;}
    if(k==='f'||k==='F'||k==='כ'){e.preventDefault();
      if(!document.fullscreenElement){document.documentElement.requestFullscreen&&document.documentElement.requestFullscreen();}
      else{document.exitFullscreen&&document.exitFullscreen();} return;}
    if(k==='p'||k==='P'||k==='פ'){e.preventDefault();
      var y=slides[i].querySelector('.yt'); if(y){ y.classList.contains('playing') ? poster(y) : play(y); return; }
      var v=slides[i].querySelector('video'); if(v){ if(v.ended) v.currentTime=0; if(v.paused){ var pr=v.play(); if(pr&&pr.catch) pr.catch(function(){}); } else v.pause(); } return;}
    if(k==='t'||k==='T'||k==='א'){e.preventDefault(); var tm=slides[i].querySelector('.timer'); if(tm) toggleTimer(tm); return;}
    if(k==='m'||k==='M'||k==='צ'){e.preventDefault(); var a=slides[i].querySelector('[data-act]'); if(a) openAct(a.getAttribute('data-act')); return;}
    if(k==='Home'){e.preventDefault();go(0,false);return;}
    if(k==='End'){e.preventDefault();go(slides.length-1,false);return;}
    /* עברית: חץ שמאלה קדימה, חץ ימינה אחורה (יניב, 27.10). PageDown/PageUp — כמו בשלט מצגות */
    if(k===' '||k==='ArrowLeft'||k==='ArrowDown'||k==='PageDown'||k==='Enter'){e.preventDefault();next();return;}
    if(k==='ArrowRight'||k==='ArrowUp'||k==='PageUp'||k==='Backspace'){e.preventDefault();prev();return;}
  });

  /* click: left half of the screen moves forward, right half moves back */
  stage.addEventListener('click',function(e){
    if(ov.classList.contains('on')||help.classList.contains('on')||guide.classList.contains('on')||act.classList.contains('on'))return;
    if(e.target.closest('.yt,a,button,.timer,video,input,select'))return;
    (e.clientX < window.innerWidth/2) ? next() : prev();
  });

  /* swipe */
  var x0=null;
  document.addEventListener('touchstart',function(e){x0=e.touches[0].clientX;},{passive:true});
  document.addEventListener('touchend',function(e){
    if(x0===null)return; var dx=e.changedTouches[0].clientX-x0;
    if(Math.abs(dx)>50 && !act.classList.contains('on')){ dx<0 ? next() : prev(); } x0=null;
  },{passive:true});

  window.DeckGo=function(d){ go(i+d,false); };

  /* deep link: #12 opens slide 12 */
  function fromHash(){var h=parseInt((location.hash||'').replace('#',''),10); return (h>=1&&h<=slides.length)?h-1:-1;}
  window.addEventListener('hashchange',function(){var n=fromHash(); if(n>=0&&n!==i) go(n,false);});
  go(Math.max(0,fromHash()),false);
  /* ?guide opens the printable lesson plan straight away, for the link on the hub page */
  if(/[?&]guide\b/.test(location.search)) toggleGuide(true);
  try{ window.focus(); document.body.focus(); }catch(e){}
  window.addEventListener('load',function(){ try{document.body.focus();}catch(e){} });
})();
