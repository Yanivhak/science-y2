# מחולל: שיעור AI 1, „מה זה בינה מלאכותית, ולמה בודקים אותה". פיילוט: שקופיות 3–4 (22.11.2026).
# התכנון: lessons/AI-01-תכנון.md. השיטה: lessons/איך-בונים-מצגת.md.
# שימוש: python3 tools/gen_ai01_deck.py [קובץ פלט]
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deck'))
from kit import Deck

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/lessons/AI-01-מה-זה-AI-פיילוט.html'

META = ('שיעור AI 1, פיילוט: שקופיות 3–4 מתוך התכנון (lessons/AI-01-תכנון.md). '
        'מטרה: התוכנה כותבת מילה אחרי מילה, ובכל פעם בוחרת מתוך המילים שהכי סביר שיבואו. ציוד: מקרן.')
D = Deck('שיעור AI 1: מה זה בינה מלאכותית', 'מבוא למדעים, י2, בינה מלאכותית, שיעור 1', META)

SRC = ('מקור (תוספת מורה): Google, Machine Learning Crash Course, „Introduction to Large Language Models": '
       'מודל שפה מעריך את ההסתברות של המילה הבאה, ובוחר את הסבירה ביותר או בוחר באקראי מתוך המילים הסבירות.')


def head(eyebrow, title, size='t-md'):
    return f'  <p class="eyebrow anim">{eyebrow}</p>\n  <h2 class="ttl {size} anim">{title}</h2>'


def bars(cands, cls):
    """עמודות של מילים אפשריות. cands: [(מילה, אורך 0–100)]. הראשונה היא הסבירה ביותר. האורכים להמחשה."""
    rows = ''.join(f'<div class="br{" top" if k == 0 else ""}"><b>{w}</b><span><i style="--w:{v}%"></i></span></div>'
                   for k, (w, v) in enumerate(cands))
    return f'<div class="bars {cls}">{rows}</div>'


# ======================= שקופית 3: התוכנה כותבת מילה אחרי מילה =======================
S3 = [('זורחת', [('זורחת', 92), ('חמה', 30), ('שוקעת', 16), ('כחולה', 4)]),
      ('במזרח', [('במזרח', 80), ('בשמיים', 42), ('מאוחר', 18), ('בים', 6)])]
words = '<span class="wd">בבוקר</span><span class="wd">השמש</span>' + ''.join(
    f'<span class="wd nw n{k + 1}">{w}</span>' for k, (w, _) in enumerate(S3)) + '<span class="cur"></span>'
panels = ''.join(bars(c, f'pn p{k + 1}') for k, (_, c) in enumerate(S3))
marks = ''.join(f'<i class="frag mk b{k + 1}"></i><i class="frag mk w{k + 1}"></i>' for k in range(len(S3)))
D.add(head('איך התוכנה כותבת', 'התוכנה כותבת מילה אחרי מילה') + f'''
  <div class="gen mt">
    <div class="sent">{words}</div>
    <div class="pane"><p class="pq">איזו מילה תבוא עכשיו?</p>{panels}<p class="pnote">אורך העמודה: כמה סביר שהמילה תבוא. להמחשה.</p></div>
  </div>
  {marks}
  <p class="frag concl">בכל פעם התוכנה בוחרת מילה מתוך המילים שהכי סביר שיבואו אחרי המילים שכבר כתובות.</p>''',
      f'''התוכנה כותבת מילה אחרי מילה
מה רואים: משפט שנבנה. לפני כל מילה מופיעות עמודות של מילים אפשריות, והמילה עם העמודה הארוכה נכנסת למשפט.
• לחיצה 1: העמודות למילה השלישית. לשאול: „איזו מילה הייתם כותבים?" לפני הלחיצה הבאה.
• לחיצה 2: „זורחת" נבחרת ונכנסת למשפט.
• לחיצות 3–4: אותו דבר למילה הרביעית, „במזרח".
• לחיצה 5: המשפט שמסכם.
לומר במילים: „התוכנה בוחרת", „התוכנה כותבת". לא „היא חושבת" ולא „היא יודעת". התלמידים לוקחים מילים כפשוטן.
אורכי העמודות הומצאו להמחשה, ולכן אין עליהן מספרים. בהדמיה נבחרת תמיד המילה הסבירה ביותר. בפועל התוכנה לפעמים בוחרת מילה סבירה אחרת: על זה שקופית 4.
{SRC}''', 'התוכנה כותבת מילה אחרי מילה', 'a', 'איך התוכנה כותבת', mins=4)


# ======================= שקופית 4: עכשיו אתם התוכנה =======================
S4 = [('שלוליות', 88), ('קשת', 52), ('בוץ', 34), ('חול', 5)]
btns = ''.join(f'<button type="button" data-k="{k}">{w}</button>' for k, (w, _) in enumerate(S4))
D.add(head('עכשיו אתם התוכנה', 'איזו מילה תבוא עכשיו?') + f'''
  <div class="gen mt">
    <div class="sent"><span class="wd">אחרי</span><span class="wd">הגשם</span><span class="wd">יש</span><span class="wd pk"></span><span class="cur"></span></div>
    <div class="pick">{btns}</div>
    <div class="pane rv">{bars(S4, "pn on")}<p class="pnote">אורך העמודה: כמה סביר שהמילה תבוא. להמחשה.</p></div>
  </div>
  <p class="concl rv">יש כמה מילים סבירות, והתוכנה בוחרת מתוכן. לכן אותה שאלה יכולה לקבל תשובות שונות.</p>''',
      f'''עכשיו אתם התוכנה
מה עושים: הכיתה בוחרת את המילה הבאה. לוחצים על הכפתור שהכיתה בחרה (או מצביעים, והמורה לוחץ).
אחרי הבחירה: המילה נכנסת למשפט, והעמודות מתגלות. מקש ההתקדמות מגלה אותן גם בלי בחירה.
• אם בחרו „קשת" או „בוץ": זו לא טעות. גם הן סבירות. זו הנקודה של השקופית.
• אם בחרו „חול": „האם זה יכול לקרות? כן, אבל זה פחות סביר. התוכנה כמעט לא תבחר בה."
המסקנה מחברת לשיעור: כי התוכנה בוחרת מתוך כמה מילים סבירות, שני תלמידים ששואלים את אותה שאלה יכולים לקבל תשובות שונות.
{SRC}''', 'עכשיו אתם התוכנה', 'a', 'עכשיו אתם התוכנה', mins=4, hook='pick')


D.css = '''
.gen{display:grid;gap:18px;width:100%}
#deck::after{display:none}   /* המולקולה בפינה היא סמל הכימיה של ט3; בשיעור הזה בלי. ⏳ יניב יחליט מה במקומה */
.sent{display:flex;flex-wrap:wrap;align-items:center;gap:16px;min-height:84px;padding:10px 26px;border-radius:18px;
  background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.22);font-size:46px;font-weight:800;color:#fff}
.sent .nw{opacity:0;transform:translateY(-14px);transition:opacity .5s,transform .5s;color:var(--ac)}
.s:has(.mk.w1.show) .sent .n1,.s:has(.mk.w2.show) .sent .n2{opacity:1;transform:none}
.s:has(.mk.w1.show):not(:has(.mk.b2.show)) .sent .n1,.s:has(.mk.w2.show) .sent .n2{text-shadow:0 0 18px rgba(var(--ac-rgb),.7)}
.sent .cur{width:4px;height:54px;background:var(--ac);animation:blink 1.1s steps(1) infinite}
@keyframes blink{50%{opacity:0}}
.pane{display:grid;gap:8px;padding:14px 26px;border-radius:18px;background:rgba(255,255,255,.04);border:1px solid rgba(255,255,255,.14)}
.pq{font-size:26px;font-weight:700;color:#DDE6F2;margin:0}
.pnote{font-size:18px;color:#C9D3E3;margin:0}
.bars{display:none;gap:7px}
.s:has(.mk.b1.show):not(:has(.mk.b2.show)) .bars.p1,.s:has(.mk.b2.show) .bars.p2,.bars.on{display:grid}
.br{display:grid;grid-template-columns:170px 1fr;align-items:center;gap:18px}
.br b{font-size:27px;font-weight:800;color:#fff;text-align:start}
.br span{height:24px;border-radius:8px;background:rgba(255,255,255,.08);overflow:hidden}
.br i{display:block;height:100%;width:var(--w);border-radius:8px;background:rgba(255,255,255,.55);animation:grow 1.1s cubic-bezier(.2,.8,.2,1)}
@keyframes grow{from{width:0}}
.s:not(.got) .bars.on .br i{animation:none;width:0}
.s:has(.mk.w1.show) .p1 .br.top i,.s:has(.mk.w2.show) .p2 .br.top i,.s.got .bars.on .br.top i{background:var(--ac);box-shadow:0 0 16px rgba(var(--ac-rgb),.7)}
.s:has(.mk.w1.show) .p1 .br.top b,.s:has(.mk.w2.show) .p2 .br.top b,.s.got .bars.on .br.top b{color:var(--ac)}
.mk{position:absolute;width:0;height:0}
.concl{font-size:28px;font-weight:700;color:#fff;margin:16px 0 0}
.pick{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.pick button{font:inherit;font-size:32px;font-weight:800;padding:10px;border-radius:16px;cursor:pointer;color:#fff;
  background:rgba(255,255,255,.07);border:2px solid rgba(255,255,255,.35);transition:border-color .3s,background .3s,opacity .3s}
.pick button:hover{border-color:var(--ac)}
.pick button.sel{border-color:var(--ac);background:rgba(var(--ac-rgb),.2)}
.s.got .pick button:not(.sel){opacity:.5}
.rv{opacity:0;transition:opacity .6s}
.s.got .rv{opacity:1}
.sent .pk{opacity:0;transition:opacity .4s;color:var(--ac)}
.sent .pk:empty{display:none}
.s.got .sent .pk:not(:empty){opacity:1}
@media (prefers-reduced-motion:reduce){.br i{animation:none!important}.sent .nw{transition:none!important}.sent .cur{animation:none}}
'''

D.js = r'''
(function(){
  window.DeckHooks=window.DeckHooks||{};
  function words(sl){ return [].map.call(sl.querySelectorAll('.pick button'),function(b){return b.textContent;}); }
  function choose(sl,k){
    var bs=sl.querySelectorAll('.pick button'); [].forEach.call(bs,function(b){b.classList.remove('sel');});
    if(k!=null){ bs[k].classList.add('sel'); sl.querySelector('.pk').textContent=words(sl)[k]; }
    else sl.querySelector('.pk').textContent='';
    sl.classList.toggle('got',k!=null||sl._shown===true);
  }
  function reveal(sl){ sl._shown=true; sl.classList.add('got'); }
  window.DeckHooks.pick={
    enter:function(sl,back){ if(!sl._wired){ sl._wired=1; [].forEach.call(sl.querySelectorAll('.pick button'),function(b){
        b.addEventListener('click',function(e){ e.stopPropagation(); choose(sl,+b.getAttribute('data-k')); reveal(sl); b.blur(); }); }); }
      if(back){ reveal(sl); } else { sl._shown=false; choose(sl,null); sl.classList.remove('got'); } },
    next:function(sl){ if(sl.classList.contains('got')) return false; reveal(sl); return true; },
    prev:function(sl){ if(!sl.classList.contains('got')) return false; sl._shown=false; choose(sl,null); sl.classList.remove('got'); return true; }
  };
})();
'''

open(OUT, 'w', encoding='utf8').write(D.html())
print('slides', len(D.S), '→', OUT)
