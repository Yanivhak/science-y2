
/* שיעור 7, חזרה: ההנפשה „שני אטומים משתפים” משיעור 6, כמו שהיא (העתק מקובץ שיעור 6 בעיצוב החדש, 14.11). רק השקופית — .s של המנוע החדש. */
/* אנימציות: שני אטומי מימן (עמ׳ 25–26). data-mode="forces" — דחייה ומשיכה; "share" — היווצרות הקשר ו־H₂.
   מסך רחב — זה לצד זה; טלפון — זה מעל זה. מתחילה כשהשקופית מוצגת, נעצרת כשעוזבים. */
(function(){
  var NS='http://www.w3.org/2000/svg', uid=0;
  function el(tag,attrs,parent){ var e=document.createElementNS(NS,tag); for(var k in attrs) e.setAttribute(k,attrs[k]); if(parent) parent.appendChild(e); return e; }
  function ease(x){ return x<0?0:x>1?1:x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2; }
  function lerp(a,b,x){ return a+(b-a)*x; }
  document.querySelectorAll('.anim.h2a').forEach(function(box){
    var sl=box.closest('.s'), mode=box.getAttribute('data-mode'), svg=box.querySelector('svg');
    var atomsG=box.querySelector('.atoms'), arrG=box.querySelector('.arrows'), cap=box.querySelector('.an-cap'), again=box.querySelector('.an-again');
    var id='h2a'+(uid++), raf=null, t0=0, shown={}, V, C, U, at=[], arrows={}, mlb, bridge, pulse, fr=0;
    
    function say(h){ if(cap.innerHTML===h) return; cap.style.opacity=0; setTimeout(function(){ cap.innerHTML=h; cap.style.opacity=1; },300); }
    function once(k,f){ if(!shown[k]){ shown[k]=1; f(); } }
    function build(){
      V=box.clientWidth<700; box.classList.toggle('v',V);
      svg.setAttribute('viewBox',V?'0 0 600 760':'0 0 1000 360'); C=V?[300,370]:[500,175]; U=V?[0,1]:[1,0];
      atomsG.innerHTML=''; arrG.innerHTML=''; at=[]; arrows={};
      var d=el('defs',{},atomsG);
      var g=el('radialGradient',{id:id+'g'},d);
      el('stop',{offset:'0','stop-color':'#B5DAF8','stop-opacity':'.90'},g); el('stop',{offset:'.45','stop-color':'#5AA9E6','stop-opacity':'.62'},g);
      el('stop',{offset:'.8','stop-color':'#4A93D6','stop-opacity':'.24'},g); el('stop',{offset:'1','stop-color':'#4A93D6','stop-opacity':'0'},g);
      var gh=el('radialGradient',{id:id+'h'},d);   // הילה רחבה וחלשה סביב הענן
      el('stop',{offset:'0','stop-color':'#5AA9E6','stop-opacity':'.30'},gh); el('stop',{offset:'1','stop-color':'#5AA9E6','stop-opacity':'0'},gh);
      var gp=el('radialGradient',{id:id+'p'},d);   // הבזק אור בקשר
      el('stop',{offset:'0','stop-color':'#FFFFFF','stop-opacity':'.9'},gp); el('stop',{offset:'.4','stop-color':'#9FD4FF','stop-opacity':'.45'},gp); el('stop',{offset:'1','stop-color':'#4FB3FF','stop-opacity':'0'},gp);   // הבזק בקשר — כמו בשאר ההנפשות
      var fs=el('filter',{id:id+'s',x:'-50%',y:'-50%',width:'200%',height:'200%'},d); el('feGaussianBlur',{stdDeviation:'6'},fs);   // ענן רך, בלי קצה
      var fg=el('filter',{id:id+'l',x:'-100%',y:'-100%',width:'300%',height:'300%'},d); el('feGaussianBlur',{stdDeviation:'5',result:'b'},fg);
      var fm=el('feMerge',{},fg); el('feMergeNode',{'in':'b'},fm); el('feMergeNode',{'in':'SourceGraphic'},fm);   // זוהר
      [['rep','#C0392B'],['att','#1E8A50']].forEach(function(m){ var mk=el('marker',{id:id+m[0],viewBox:'0 0 10 10',refX:'6',refY:'5',markerWidth:'4',markerHeight:'4',orient:'auto'},d); el('path',{d:'M0,0 L10,5 L0,10 z',fill:m[1]},mk); });
      var cg=el('g',{filter:'url(#'+id+'s)'},atomsG);
      for(var i=0;i<2;i++){ var a={}; a.halo=el('circle',{r:150,fill:'url(#'+id+'h)'},cg); at.push(a); }
      bridge=el('ellipse',{fill:'url(#'+id+'g)',opacity:0},cg);   // הענן המשותף — שני העננים מתמזגים לענן אחד סביב שני הגרעינים
      at.forEach(function(a){ a.cloud=el('circle',{r:100,fill:'url(#'+id+'g)'},cg); });
      pulse=el('ellipse',{fill:'url(#'+id+'p)',opacity:0},atomsG);
      at.forEach(function(a){ a.nglow=el('circle',{r:36,'class':'nglH',filter:'url(#'+id+'s)'},atomsG); a.nuc=el('circle',{r:26,'class':'nucH'},atomsG); a.nt=el('text',{'class':'ntH'},atomsG); a.nt.textContent='+1'; });
      at.forEach(function(a){ a.tr=[]; a.hist=[]; for(var k=0;k<9;k++) a.tr.push(el('circle',{r:9-k*.7,'class':'eT',opacity:0},atomsG)); });
      at.forEach(function(a){ a.e=el('circle',{r:9,'class':'eH',filter:'url(#'+id+'l)'},atomsG); a.el=el('text',{'class':'elb'},atomsG); a.el.textContent='e⁻'; });
      ['ee0','ee1','nn0','nn1','at0','at1','at2','at3'].forEach(function(k){ arrows[k]=el('line',{'class':'arr '+(k[0]==='a'?'att':'rep'),'marker-end':'url(#'+id+(k[0]==='a'?'att':'rep')+')',opacity:0},arrG); });
      mlb=el('text',{'class':'mlb',opacity:0},atomsG); mlb.textContent='מולקולת מימן H₂';
    }
    function P(d,off){ return [C[0]+U[0]*d+(off?off[0]:0), C[1]+U[1]*d+(off?off[1]:0)]; }
    function setArrow(k,from,to,len0,len1,on){ var a=arrows[k], dx=to[0]-from[0], dy=to[1]-from[1], L=Math.hypot(dx,dy)||1;
      a.setAttribute('x1',from[0]+dx/L*len0); a.setAttribute('y1',from[1]+dy/L*len0); a.setAttribute('x2',from[0]+dx/L*len1); a.setAttribute('y2',from[1]+dy/L*len1);
      a.setAttribute('opacity',on?1:0); }
    function away(p,q){ return [2*p[0]-q[0],2*p[1]-q[1]]; }   // נקודה בכיוון ההפוך מ־q
    function frame(now){
      var t=(now-t0)/1000, fin=ease(t/.8), d, m=0;
      if(mode==='forces') d=lerp(330,200,ease((t-.3)/2.5));
      else { d=lerp(200,64,ease((t-.6)/3.6)); m=ease((t-1.6)/3); }
      var nuc=[P(-d),P(d)], e=[];
      var N=[U[1],-U[0]];                              // ניצב לציר — „למעלה” במסך רחב
      // האלקטרון נע כל הזמן, בלי מסלול: תנועה לא סדירה בתוך הענן (שקופית 4: „אי אפשר לומר איפה בדיוק הוא — רק באיזה אזור”)
      function wob(i,t){ var k=i?1.7:0; return [Math.sin(.93*t+k)*.6+Math.sin(1.71*t+2.1+k)*.4, Math.sin(1.27*t+.7+k)*.55+Math.sin(2.03*t+4+k)*.45]; }
      function loc(i,a,b){ return [ (i<0?C:nuc[i])[0]+a*U[0]+b*N[0], (i<0?C:nuc[i])[1]+a*U[1]+b*N[1] ]; }
      function hold(t,T1,T2){ return ease((t-T1+.6)/.6)*(1-ease((t-T2)/.6)); }   // 0 — תנועה, 1 — תמונה קפואה
      for(var i=0;i<2;i++){
        var w=wob(i,t), sg=i?-1:1;
        var own= mode==='share' ? loc(i, 48*w[0], sg*(34+24*Math.abs(w[1])))   // בהתקרבות — כל אחד בצד שלו של הציר, כדי שלא ייפגשו
                                : loc(i, 56*w[0], 56*w[1]);                       // בתוך הענן של האטום שלו
        var dx=own[0]-nuc[i][0], dy=own[1]-nuc[i][1], L=Math.hypot(dx,dy)||1;
        if(L<46) own=[nuc[i][0]+dx/L*46, nuc[i][1]+dy/L*46];                       // לא על הגרעין
        var pos=own;
        if(mode==='forces'){                           // בזמן החצים — תמונה קפואה, כמו הציור בשקופית 6
          var tg=loc(i, sg*24, 52), h=hold(t,3.0,17);
          pos=[lerp(own[0],tg[0],h), lerp(own[1],tg[1],h)];
        } else {                                       // משותף: שני האלקטרונים נעשים זוג אחד — „זוג אלקטרונים משותף” (עמ׳ 26) — בענן שסביב שני הגרעינים, בעיקר ביניהם
          var pw=wob(0,t*.8), pj=wob(i+3,t*1.6);
          var shx=20*pw[0]+3*pj[0], shy=18*pw[1]+sg*10+3*pj[1];
          var sh=loc(-1, shx, shy), h2=hold(t,14.0,18), gl=loc(-1,0,sg*17);
          sh=[lerp(sh[0],gl[0],h2), lerp(sh[1],gl[1],h2)];
          pos=[lerp(own[0],sh[0],m), lerp(own[1],sh[1],m)];
        }
        e.push(pos); }
      fr++;
      var mg=mode==='share'?m:0, rx=d+92, ry=lerp(60,92,mg);   // הענן המשותף: מוארך לאורך הציר
      bridge.setAttribute('cx',C[0]); bridge.setAttribute('cy',C[1]);
      bridge.setAttribute('rx',U[0]?rx:ry); bridge.setAttribute('ry',U[0]?ry:rx); bridge.setAttribute('opacity',fin*mg);
      var pz=mode==='share'?ease((t-13.8)/.8)*(1-ease((t-17.4)/.6)):0, pk=pz*(.55+.45*Math.sin((t-13.8)*3.2));
      pulse.setAttribute('cx',C[0]); pulse.setAttribute('cy',C[1]); pulse.setAttribute('rx',U[0]?70:46); pulse.setAttribute('ry',U[0]?46:70); pulse.setAttribute('opacity',pk);
      at.forEach(function(a,i){
        a.halo.setAttribute('cx',nuc[i][0]); a.halo.setAttribute('cy',nuc[i][1]); a.halo.setAttribute('opacity',fin*(1-.5*mg));
        a.cloud.setAttribute('r',lerp(100,88,mg)); a.cloud.setAttribute('opacity',fin*(1-.35*mg));
        a.nglow.setAttribute('cx',nuc[i][0]); a.nglow.setAttribute('cy',nuc[i][1]); a.nglow.setAttribute('opacity',fin*.35);
        // שובל קצר ודועך: מראה שהאלקטרון נע בלי הפסקה, בתנועה לא סדירה — לא מסלול
        if(fr%2===0){ a.hist.unshift([e[i][0],e[i][1]]); if(a.hist.length>a.tr.length) a.hist.pop(); }
        a.tr.forEach(function(c,k){ var q=a.hist[k]; if(!q){ c.setAttribute('opacity',0); return; } c.setAttribute('cx',q[0]); c.setAttribute('cy',q[1]); c.setAttribute('opacity',fin*.32*(1-k/a.tr.length)); });
        [a.cloud,a.nuc].forEach(function(c){ c.setAttribute('cx',nuc[i][0]); c.setAttribute('cy',nuc[i][1]); c.setAttribute('opacity',fin*(c===a.cloud?(1-.35*mg):1)); });
        a.nt.setAttribute('x',nuc[i][0]); a.nt.setAttribute('y',nuc[i][1]+8); a.nt.setAttribute('opacity',fin);
        a.e.setAttribute('cx',e[i][0]); a.e.setAttribute('cy',e[i][1]); a.e.setAttribute('opacity',fin);
        a.el.setAttribute('x',e[i][0]); a.el.setAttribute('y',e[i][1]-16); a.el.setAttribute('opacity',fin*(1-m));
      });
      if(mode==='forces'){
        var ee=(t>3.2&&t<6.2)||(t>12.2&&t<16.6), nn=(t>6.2&&t<9.2)||(t>12.2&&t<16.6), aa=t>9.2&&t<16.6;
        setArrow('ee0',e[0],away(e[0],e[1]),14,62,ee); setArrow('ee1',e[1],away(e[1],e[0]),14,62,ee);
        setArrow('nn0',nuc[0],away(nuc[0],nuc[1]),32,92,nn); setArrow('nn1',nuc[1],away(nuc[1],nuc[0]),32,92,nn);
        var L0=Math.hypot(nuc[1][0]-e[0][0],nuc[1][1]-e[0][1]), L1=Math.hypot(nuc[0][0]-e[1][0],nuc[0][1]-e[1][1]);
        setArrow('at0',e[0],nuc[1],14,Math.max(20,L0-36),aa); setArrow('at1',e[1],nuc[0],14,Math.max(20,L1-36),aa);
        once('c1',function(){ say('שני אטומי מימן מתקרבים.'); });
        if(t>3.2) once('c2',function(){ say('<span class="cr">דחייה:</span> האלקטרון של אטום אחד והאלקטרון של האטום האחר — מינוס ומינוס.'); });
        if(t>6.2) once('c3',function(){ say('<span class="cr">דחייה:</span> הגרעין של אטום אחד והגרעין של האטום האחר — פלוס ופלוס.'); });
        if(t>9.2) once('c4',function(){ say('<span class="cg">משיכה:</span> האלקטרון של אטום אחד והגרעין של האטום האחר — מינוס ופלוס.'); });
        if(t>12.2) once('c5',function(){ say('״פועלים ביניהם גם כוחות <span class="cr">דחייה</span> וגם כוחות <span class="cg">משיכה</span> חשמליים״ (עמ׳ 25).'); });
        if(t>14.6) once('end',function(){ again.classList.add('on'); });
      } else {
        var aa2=t<3.4, glue=t>14.2&&t<17.6;
        function to(a,b){ return Math.max(20,Math.hypot(b[0]-a[0],b[1]-a[1])-34); }
        if(!glue){ setArrow('at0',e[0],nuc[1],14,to(e[0],nuc[1]),aa2); setArrow('at1',e[1],nuc[0],14,to(e[1],nuc[0]),aa2); setArrow('at2',e[0],nuc[0],14,30,false); setArrow('at3',e[1],nuc[1],14,30,false); }
        else { setArrow('at0',e[0],nuc[1],14,to(e[0],nuc[1]),true); setArrow('at1',e[1],nuc[0],14,to(e[1],nuc[0]),true);
               setArrow('at2',e[0],nuc[0],14,to(e[0],nuc[0]),true); setArrow('at3',e[1],nuc[1],14,to(e[1],nuc[1]),true); }
        // והדחייה בין שני האלקטרונים לא נעלמה — חץ אדום קטן ביניהם (כמו בשקופית 6)
        setArrow('ee0',e[0],away(e[0],e[1]),11,30,glue); setArrow('ee1',e[1],away(e[1],e[0]),11,30,glue);
        var top=V?[C[0],C[1]-215]:[C[0],C[1]-128]; mlb.setAttribute('x',top[0]); mlb.setAttribute('y',top[1]);
        once('c1',function(){ say('הקשר נוצר מ<span class="cg">כוחות המשיכה</span> — בין האלקטרון של אטום אחד לגרעין של האטום האחר.'); });
        if(t>4.8) once('c2',function(){ say('שני אטומי המימן <b>״משתפים״</b> ביניהם את שני האלקטרונים.'); });
        if(t>7.8) once('c3',function(){ say('כל אטום <b>״תורם״</b> אלקטרון אחד לקשר.'); });
        if(t>10.8) once('c4',function(){ say('לכל אטום מימן יש עכשיו <b>שני</b> אלקטרונים — ״האחד ׳שלו׳ והשני ׳של׳ האטום האחר״.'); });
        if(t>13.8) once('c5',function(){ mlb.setAttribute('opacity',1); say('כששני האלקטרונים באזור שבין שני הגרעינים, כל אחד מהם נמשך לשני הגרעינים בבת אחת. זה ה״דבק״.'); });
        if(t>17.6) once('end',function(){ again.classList.add('on'); });
      }
      raf=requestAnimationFrame(frame);
    }
    function start(){ stop(); build(); fr=0; shown={}; cap.innerHTML=''; again.classList.remove('on'); t0=performance.now(); raf=requestAnimationFrame(frame); }
    function stop(){ if(raf){ cancelAnimationFrame(raf); raf=null; } }
    again.addEventListener('click',function(ev){ ev.stopPropagation(); start(); });
    var was=false;
    new MutationObserver(function(){ var on=sl.classList.contains('on'); if(on&&!was) start(); if(!on) stop(); was=on; }).observe(sl,{attributes:true,attributeFilter:['class']});
    addEventListener('resize',function(){ if(raf && (box.clientWidth<700)!==V) start(); });
    if(sl.classList.contains('on')){ was=true; start(); }
  });
})();
