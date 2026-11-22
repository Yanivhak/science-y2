
/* אנימציות שיעור 7: F₂ (עמ׳ 27), CH₄ (עמ׳ 28) ו־H₂O (עמ׳ 28, הציור של המורה). רק האלקטרונים החיצוניים, בזוגות ובבודדים — כמו בספר.
   אין מסלול: המעגל הוא פס, וכל זוג / בודד נע בתוך האזור שלו. קשר = שני בודדים נעשים זוג משותף בין הגרעינים.
   14.11: מראה עשיר יותר (כמו שיעור 6): ענן זוהר סביב כל אטום, זוהר משותף באזור הקשר, זוהר ושובל קצר לבודדים, הבזק כשהזוג נוצר.
   התזמון, התנועה והכיתובים של F₂ ו־CH₄ — כמו קודם. */
(function(){
  var NS='http://www.w3.org/2000/svg', uid=0;
  function el(tag,attrs,parent){ var e=document.createElementNS(NS,tag); for(var k in attrs) e.setAttribute(k,attrs[k]); if(parent) parent.appendChild(e); return e; }
  function ease(x){ return x<0?0:x>1?1:x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2; }
  function lerp(a,b,x){ return a+(b-a)*x; }
  function wob(n,t){ return [Math.sin(.9*t+n*1.7)*.6+Math.sin(1.63*t+n*2.9)*.4, Math.sin(1.21*t+n*.8)*.55+Math.sin(2.1*t+n*3.7)*.45]; }
  function grad(d,id,stops){ var g=el('radialGradient',{id:id},d); stops.forEach(function(s){ el('stop',{offset:s[0],'stop-color':s[1],'stop-opacity':s[2]},g); }); }
  var PI=Math.PI;
  document.querySelectorAll('.anim.a7').forEach(function(box){
    var sl=box.closest('.s'), mode=box.getAttribute('data-mode'), svg=box.querySelector('svg'), G=box.querySelector('.atoms');
    var cap=box.querySelector('.an-cap'), again=box.querySelector('.an-again'), id='a7x'+(uid++);
    var raf=null, t0=0, tw0=0, fr=0, shown={}, waiting=false, mq=sl.querySelector('.mcq'), V, A=[], B=[], mlb, W, H, Lg, L0, L1, L2, Lt;   // שכבות ציור: זוהר, פסים, גרעינים, שובלים, אלקטרונים
    function say(h){ if(cap.innerHTML===h) return; cap.style.opacity=0; setTimeout(function(){ cap.innerHTML=h; cap.style.opacity=1; },300); }
    function once(k,f){ if(!shown[k]){ shown[k]=1; f(); } }
    // אטום: סמל, רדיוס הפס, מיקום התחלה וסוף, זמני תנועה, ואזורים: [זווית, כמה אלקטרונים]
    function atom(sym,R,p0,p1,tA,tB,sites){ var a={sym:sym,R:R,p0:p0,p1:p1,tA:tA,tB:tB,sites:[]};
      a.glow=el('circle',{r:R+52,fill:'url(#'+id+'c)'},Lg);
      a.bands=['b1','b2','b3'].map(function(c){ return el('circle',{r:R,'class':'band '+c},L0); });   // פס רך, בלי קצוות
      a.ng=el('circle',{r:(sym==='H'?15:24)+12,fill:'#E9FFD6',opacity:0,filter:'url(#'+id+'s)'},L1);
      a.nuc=el('circle',{r:sym==='H'?15:24,'class':'nuc7'},L1);
      a.txt=el('text',{'class':'sym'},L1); a.txt.textContent=sym;
      sites.forEach(function(s,i){ var d=[], tr=[]; for(var j=0;j<s[1];j++) d.push(el('circle',{r:7,'class':'e7'},L2));
        if(s[1]===1) for(var k=0;k<8;k++) tr.push(el('circle',{r:6.5-k*.6,fill:'#2E6FE0',opacity:0},Lt));   // שובל — רק לבודדים, הם אלה שנעים לקשר
        a.sites.push({ang:s[0],d:d,tr:tr,hist:[],n:A.length*7+i}); });
      A.push(a); return a; }
    function bond(a,sa,b,sb,t0b){ var o={a:a,sa:sa,b:b,sb:sb,t0:t0b};
      o.br=el('ellipse',{fill:'url(#'+id+'b)',opacity:0},Lg);                       // הזוהר המשותף באזור הקשר
      o.fl=el('circle',{r:34,fill:'url(#'+id+'f)',opacity:0},Lt);                    // הבזק כשהזוג נוצר
      B.push(o); }
    function build(){
      V=box.clientWidth<(+box.getAttribute('data-vmin')||700); box.classList.toggle('v',V); G.innerHTML=''; A=[]; B=[];
      var d=el('defs',{},G);
      grad(d,id+'c',[['0','#7FBFF0','.48'],['.55','#5AA9E6','.22'],['1','#5AA9E6','0']]);
      grad(d,id+'b',[['0','#D6ECFF','.95'],['.5','#7FBFF0','.5'],['1','#5AA9E6','0']]);
      grad(d,id+'f',[['0','#FFFFFF','.9'],['.4','#9FD4FF','.45'],['1','#4FB3FF','0']]);
      var fs=el('filter',{id:id+'s',x:'-60%',y:'-60%',width:'220%',height:'220%'},d); el('feGaussianBlur',{stdDeviation:'6'},fs);
      var fg=el('filter',{id:id+'l',x:'-60%',y:'-60%',width:'220%',height:'220%'},d); el('feGaussianBlur',{stdDeviation:'5',result:'b'},fg);
      var fm=el('feMerge',{},fg); el('feMergeNode',{'in':'b'},fm); el('feMergeNode',{'in':'SourceGraphic'},fm);
      Lg=el('g',{filter:'url(#'+id+'s)'},G); L0=el('g',{},G); L1=el('g',{},G); Lt=el('g',{},G); L2=el('g',{filter:'url(#'+id+'l)'},G);
      if(mode==='f2'){
        W=V?600:1000; H=V?760:380; var c=V?[300,390]:[500,200], u=V?[0,1]:[1,0], R=80, d1=65, d0=V?250:250;
        var P=function(s){ return [c[0]+u[0]*s, c[1]+u[1]*s]; };
        var toB=Math.atan2(u[1],u[0]), back=toB+PI, side1=toB-PI/2, side2=toB+PI/2;
        atom('F',R,P(-d0),P(-d1),3.4,6.4,[[toB,1],[side1,2],[back,2],[side2,2]]);
        atom('F',R,P(d0),P(d1),3.4,6.4,[[back,1],[side1,2],[toB,2],[side2,2]]);
        bond(0,0,1,0,5.0);
        mlb=el('text',{'class':'mlb',opacity:0,x:c[0],y:V?70:40},G); mlb.textContent='מולקולת פלואור F₂';
      } else if(mode==='ch4'){
        W=V?600:1000; H=V?660:430; var c=V?[300,350]:[500,226], RC=70, RH=46, dB=RC+RH-22;
        atom('C',RC,c,c,0,0,[[-PI/2,1],[0,1],[PI/2,1],[PI,1]]);
        [[-PI/2,0],[0,1],[PI/2,2],[PI,3]].forEach(function(q,k){ var ang=q[0], ux=Math.cos(ang), uy=Math.sin(ang), ts=2.6+k*2.1, d0=(Math.abs(uy)>.5?(V?230:150):(V?220:250));
          atom('H',RH,[c[0]+ux*d0,c[1]+uy*d0],[c[0]+ux*dB,c[1]+uy*dB],ts,ts+1.6,[[ang+PI,1]]);
          bond(0,k,k+1,0,ts+.9); });
        mlb=el('text',{'class':'mlb',opacity:0,x:V?c[0]:180,y:V?60:226},G); mlb.textContent='מולקולת מתאן CH₄';
      } else if(mode==='fill'){
        // „כמה מקום יש באזור?” — פלואור: ארבעה מקומות; קודם ארבעה בודדים, אחר כך זוגות; בסוף 3 זוגות ובודד
        W=V?600:1000; H=V?560:420; var c=V?[300,280]:[500,215], R=118;
        var fa=atom('F',R,c,c,0,0,[[0,1],[-PI/2,2],[PI,2],[PI/2,2]]);
        fa.sites.forEach(function(st){ el('circle',{cx:c[0]+R*Math.cos(st.ang),cy:c[1]+R*Math.sin(st.ang),r:26,fill:'none',stroke:'#CFE3FF','stroke-opacity':.45,'stroke-width':2,'stroke-dasharray':'5 6'},L0);   // מקום
          st.d.forEach(function(d){ d.setAttribute('r',10); }); st.tr.forEach(function(x){ x.remove(); }); st.tr=[]; });
        var T1=[1.6,2.6,3.6,4.6], T2=[7.0,8.0,9.0];
        fa.sites.forEach(function(st,i){ st.d[0].ta=T1[i]; if(st.d[1]) st.d[1].ta=T2[i-1]; });
        mlb=el('text',{'class':'mlb',opacity:0,x:c[0],y:30},G);
      } else {
        // מים: כמו הציור בשקופית „מים: ניחוש והדמיה” — מימן מימין ומימן למטה, שני הזוגות של החמצן למעלה ומשמאל
        W=V?600:640; H=V?660:430; var c=V?[270,290]:[250,170], RO=80, RH=46, dB=RO+RH-22;   // שטח צמוד: המולקולה היא העיקר בשקופית
        atom('O',RO,c,c,0,0,[[-PI/2,2],[PI,2],[0,1],[PI/2,1]]);
        [[0,2,V?230:270],[PI/2,3,V?240:170]].forEach(function(q,k){ var ang=q[0], ux=Math.cos(ang), uy=Math.sin(ang), ts=2.6+k*3.0, d0=q[2];
          atom('H',RH,[c[0]+ux*d0,c[1]+uy*d0],[c[0]+ux*dB,c[1]+uy*dB],ts,ts+1.6,[[ang+PI,1]]);
          bond(0,q[1],k+1,0,ts+.9); });
        mlb=el('text',{'class':'mlb',opacity:0,x:V?c[0]+30:470,y:V?60:395},G); mlb.textContent='מולקולת מים H₂O';
      }
      svg.setAttribute('viewBox','0 0 '+W+' '+H);
    }
    function pos(a,t){ var m=ease((t-a.tA)/(a.tB-a.tA||1)); return [lerp(a.p0[0],a.p1[0],m), lerp(a.p0[1],a.p1[1],m)]; }
    function frame(now){
      // tw — שעון התנועה הלא סדירה (רץ תמיד); t — ציר הזמן של התהליך (עומד על 0 עד הניחוש, ב־data-wait="mcq")
      var tw=(now-tw0)/1000, t=waiting?0:(now-t0)/1000, fin=ease(tw/.8); fr++;
      var P=A.map(function(a){ return pos(a,t); });
      A.forEach(function(a,i){ var p=P[i], op=a.sym==='H'?Math.min(fin,ease((t-a.tA+1.2)/1)):fin;
        [a.glow,a.ng,a.nuc].concat(a.bands).forEach(function(x){ x.setAttribute('cx',p[0]); x.setAttribute('cy',p[1]); });
        a.txt.setAttribute('x',p[0]); a.txt.setAttribute('y',p[1]+8);
        [a.glow,a.nuc,a.txt].concat(a.bands).forEach(function(x){ x.setAttribute('opacity',op); }); a.ng.setAttribute('opacity',op*.45);
        a.sites.forEach(function(s){ s.d.forEach(function(d){ d.setAttribute('opacity',op); }); });
        a.op=op; });
      // מיקום כל אזור: זווית + תנועה לא סדירה; זוג — שני אלקטרונים זה ליד זה
      A.forEach(function(a,i){ a.sites.forEach(function(s){ var w=wob(s.n,tw), ang=s.ang+w[0]*.32, r=a.R+4*w[1];
        s.c=[P[i][0]+r*Math.cos(ang), P[i][1]+r*Math.sin(ang)]; s.tg=[-Math.sin(ang),Math.cos(ang)]; }); });
      // קשרים: שני הבודדים עוברים למרכז האזור המשותף ונעשים זוג
      B.forEach(function(b){ var a1=A[b.a], a2=A[b.b], s1=a1.sites[b.sa], s2=a2.sites[b.sb], p1=P[b.a], p2=P[b.b];
        var dx=p2[0]-p1[0], dy=p2[1]-p1[1], L=Math.hypot(dx,dy)||1, ov=a1.R+a2.R-L, k=(a1.R-ov/2)/L;
        var w=wob(s1.n+50,tw*1.2), mid=[p1[0]+dx*k+4*w[0], p1[1]+dy*k+4*w[1]], pr=[-dy/L,dx/L], f=ease((t-b.t0)/1.4);
        b.f=f; b.p=[[mid[0]+pr[0]*10,mid[1]+pr[1]*10],[mid[0]-pr[0]*10,mid[1]-pr[1]*10]]; s1.bond=b; s2.bond=b; s1.bi=0; s2.bi=1;
        // זוהר משותף: אליפסה לאורך הציר, באזור שבין שני הגרעינים
        var cx=p1[0]+dx*k, cy=p1[1]+dy*k, rot=Math.atan2(dy,dx)*180/PI, op=Math.min(a1.op,a2.op);
        b.br.setAttribute('cx',cx); b.br.setAttribute('cy',cy); b.br.setAttribute('rx',Math.min(a1.R,a2.R)*.95); b.br.setAttribute('ry',Math.min(a1.R,a2.R)*.6);
        b.br.setAttribute('transform','rotate('+rot+' '+cx+' '+cy+')'); b.br.setAttribute('opacity',op*f);
        var fl=ease((t-b.t0-1.0)/.35)*(1-ease((t-b.t0-1.5)/.9));
        b.fl.setAttribute('cx',mid[0]); b.fl.setAttribute('cy',mid[1]); b.fl.setAttribute('opacity',fl*op); });
      A.forEach(function(a){ a.sites.forEach(function(s){
        if(s.d.length===2){ for(var i=0;i<2;i++){ var sg=i?1:-1, j=wob(s.n*5+i,tw*1.6); s.d[i].setAttribute('cx',s.c[0]+sg*8*s.tg[0]+1.5*j[0]); s.d[i].setAttribute('cy',s.c[1]+sg*8*s.tg[1]+1.5*j[1]); } }
        else { var q=s.c; if(s.bond){ var f=s.bond.f, tg=s.bond.p[s.bi]; q=[lerp(s.c[0],tg[0],f), lerp(s.c[1],tg[1],f)]; }
          s.d[0].setAttribute('cx',q[0]); s.d[0].setAttribute('cy',q[1]);
          // שובל קצר ודועך: האלקטרון נע בלי הפסקה, בתנועה לא סדירה — לא מסלול
          if(fr%2===0){ s.hist.unshift(q); if(s.hist.length>s.tr.length) s.hist.pop(); }
          s.tr.forEach(function(c,k){ var h=s.hist[k]; if(!h){ c.setAttribute('opacity',0); return; } c.setAttribute('cx',h[0]); c.setAttribute('cy',h[1]); c.setAttribute('opacity',a.op*.45*(1-k/s.tr.length)); }); } }); });
      if(mode==='fill'){
        A[0].sites.forEach(function(st){ st.d.forEach(function(d,i){
          var cx=+d.getAttribute('cx'), cy=+d.getAttribute('cy');
          if(st.d.length===2 && i===0){ var k=ease((t-st.d[1].ta)/.35); cx=lerp(st.c[0],cx,k); cy=lerp(st.c[1],cy,k); }   // לבד במקום — במרכז המקום
          var pz=ease((t-d.ta)/.7), far=[st.c[0]+Math.cos(st.ang)*190, st.c[1]+Math.sin(st.ang)*190];
          d.setAttribute('cx',lerp(far[0],cx,pz)); d.setAttribute('cy',lerp(far[1],cy,pz)); d.setAttribute('opacity',pz*A[0].op); }); });
        once('c1',function(){ say('באזור החיצוני של האטום יש <b>ארבעה מקומות</b>, ובכל מקום יש מקום ל<b>שני</b> אלקטרונים לכל היותר.'); });
        if(t>1.4) once('c2',function(){ say('אלקטרונים דוחים זה את זה, ולכן כל אלקטרון תופס קודם <b>מקום פנוי</b>.'); });
        if(t>6.6) once('c3',function(){ say('רק כשאין יותר מקום פנוי, אלקטרון נכנס ל<b>זוג</b>.'); });
        if(t>10.0) once('c4',function(){ say('לפלואור 7 אלקטרונים חיצוניים: שלושה זוגות ו<b>אלקטרון בודד אחד</b>. האלקטרון הבודד הוא זה שמשתתף בקשר.'); });
        if(t>12.4) once('end',function(){ again.classList.add('on'); });
      } else if(mode==='f2'){
        once('c1',function(){ say('לכל אטום פלואור <b>7</b> אלקטרונים חיצוניים.'); });
        if(t>2.6) once('c2',function(){ A.forEach(function(a){ a.sites[0].d[0].classList.add('d'); }); say('כל אטום פלואור <b>״תורם״</b> אלקטרון חיצוני אחד לקשר.'); });
        if(t>7.2) once('c3',function(){ say('שני האטומים משתפים ביניהם <b>שני אלקטרונים חיצוניים</b>. זה קשר שיתופי אחד.'); });
        if(t>10.2) once('c4',function(){ mlb.setAttribute('opacity',1); say('לכל אטום פלואור 7 אלקטרונים חיצוניים, ורק <b>אחד</b> מהם משתתף בקשר.'); });
        if(t>12.6) once('end',function(){ again.classList.add('on'); });
      } else if(mode==='ch4'){
        once('c1',function(){ say('לפחמן <b>4</b> אלקטרונים חיצוניים, ולכל מימן אלקטרון <b>אחד</b>.'); });
        if(t>2.6) once('c2',function(){ say('״אטום פחמן יכול ליצור <b>4 קשרים שיתופיים</b>, למשל עם 4 אטומים של מימן…״'); });
        if(t>7.0) once('c3',function(){ say('״…שבהם הוא משתף אלקטרון חיצוני אחד עם כל אטום מימן.״ (עמ׳ 28)'); });
        if(t>12.6) once('c4',function(){ mlb.setAttribute('opacity',1); say('זו מולקולת מתאן, <b>CH₄</b>. כל ארבעת האלקטרונים החיצוניים של הפחמן משתתפים בקשרים.'); });
        if(t>15.0) once('end',function(){ again.classList.add('on'); });
      } else {
        if(tw>1.6) once('cd',function(){ A[0].sites[2].d[0].classList.add('d'); A[0].sites[3].d[0].classList.add('d'); });
        if(waiting){ raf=requestAnimationFrame(frame); return; }   // לפני הניחוש: רק החמצן, בלי כיתובים
        // הכיתובים — המשפטים מהשקופית „מים: ניחוש והדמיה”
        once('c1',function(){ say('לחמצן יש יכולת קישור <b>2</b>, כי חסרים לו 2 אלקטרונים עד 8. למימן יש יכולת קישור <b>1</b>.'); });
        if(t>8.6) once('c2',function(){ mlb.setAttribute('opacity',1); say('לכן חמצן אחד קשור ל<b>שני</b> אטומי מימן: <span class="f">H–O–H</span>, כלומר <span class="f">H₂O</span>.'); });
        if(t>11.8) once('c3',function(){ say('לחמצן יש 6 אלקטרונים משלו ועוד 2 מהקשרים, ובסך הכול <b>8</b>. לכל מימן יש 1 משלו ועוד 1 מהקשר, ובסך הכול <b>2</b>.'); });
        if(t>14.6) once('end',function(){ again.classList.add('on'); });
      }
      raf=requestAnimationFrame(frame);
    }
    function start(){ stop(); build(); fr=0; shown={}; cap.innerHTML=''; again.classList.remove('on'); t0=tw0=performance.now();
      waiting=box.getAttribute('data-wait')==='mcq' && !!mq && !mq.classList.contains('done'); raf=requestAnimationFrame(frame); }
    function stop(){ if(raf){ cancelAnimationFrame(raf); raf=null; } }
    again.addEventListener('click',function(ev){ ev.stopPropagation(); start(); });
    var was=false;
    // ניחוש ← הציור עונה: התהליך מתחיל רק כשהשאלה נענתה (התשובה הנכונה נבחרה או נחשפה)
    if(box.getAttribute('data-wait')==='mcq' && mq) new MutationObserver(function(){ if(!sl.classList.contains('on')) return;
      if(mq.classList.contains('done') && waiting){ waiting=false; t0=performance.now(); } else if(!mq.classList.contains('done') && !waiting) start(); }).observe(mq,{attributes:true,attributeFilter:['class']});
    new MutationObserver(function(){ var on=sl.classList.contains('on'); if(on&&!was) start(); if(!on) stop(); was=on; }).observe(sl,{attributes:true,attributeFilter:['class']});
    addEventListener('resize',function(){ if(raf && (box.clientWidth<(+box.getAttribute('data-vmin')||700))!==V) start(); });
    if(sl.classList.contains('on')){ was=true; start(); }
  });
})();
