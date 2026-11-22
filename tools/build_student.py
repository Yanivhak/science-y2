"""גרסת תלמידים לשיעורי המדעים: בלי הערות המורה, בלי מפת המורה, נגיעה במסך = הלאה, וחצי אחורה/קדימה בשוליים.
שימוש: python3 tools/build_student.py <תיקיית-יעד>
"""
import re, sys, os, html, time, shutil
import phone_mode, phone_deck
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
THUMBS = os.path.join(ROOT, 'tools', 'thumbs')   # תמונות לדף הראשי — נוצרות ב-tools/make_thumbs.js
# מה מפורסם: (קובץ מקור, שם בפרסום, כותרת לדף הפתיחה, תיאור)
PUBLISH = [
    ('science/lessons/01-ביולוגיה-או-כימיה.html', 'lesson-01.html', 'שיעור 1 · ביולוגיה או כימיה?', 'בספר: עמודים 6–9'),
    ('science/lessons/02-מאטום-עד-מבנה-ענק.html', 'lesson-02.html', 'שיעור 2 · מאטום עד מבנה ענק', 'בספר: עמודים 14, 18, 23, 25–27, 31–32'),
    ('science/lessons/03-תגובות-כימיות.html', 'lesson-03.html', 'שיעור 3 · תגובות כימיות', 'בספר: עמודים 15–16'),
    ('science/lessons/04-ניסוח-תהליך-כימי.html', 'lesson-04.html', 'שיעור 4 · ניסוח של תהליך כימי', 'בספר: עמודים 19–21, 161'),
    ('science/lessons/05-קשרים-כימיים-והקשר-היוני.html', 'lesson-05.html', 'שיעור 5 · קשרים כימיים והקשר היוני', 'בספר: עמודים 22–24'),
    ('science/lessons/06-הקשר-השיתופי-עיצוב-חדש.html', 'lesson-06.html', 'שיעור 6 · הקשר השיתופי', 'בספר: עמודים 25–26'),
    ('science/lessons/סיכום-שיעורים-1-5.html', 'lesson-summary-1-5.html', 'סיכום · עיקרי החומר משיעורים 1 עד 5', 'מצגת עם העיקר מכל שיעור ושאלות לבדיקה עצמית'),
    ('science/lab/01-כרוב-סגול-חומצות-ובסיסים.html', 'lab-01.html', 'מעבדה · הכרוב הסגול', 'בספר: עמודים 48–50'),
    ('science/lab/03-משחת-שיניים-לפילים.html', 'lab-02.html', 'מעבדה · משחת שיניים לפילים', 'בספר: עמוד 118'),
]
# דפים רגילים שמועתקים כמו שהם: (קובץ מקור, שם בפרסום, כותרת, תיאור) — מופיעים תחת „מבחנים”
PAGES = [
    ('science/מבחנים/חומר-למבחן-02.11.html', 'exam-0211.html', 'מבחן · החומר למבחן ב־02.11', 'שיעורים 1 עד 5: העמודים בספר והנושאים'),
    ('science/מבחנים/מושגים-1-5.html', 'concepts-1-5.html', 'מושגים · כל המושגים משיעורים 1 עד 5', 'ההגדרות, וטבלה: מה כל חומר, ולמה'),
    ('science/games/משחק-חזרה-1-5.html', 'game-1-5.html', 'משחק · משחק חזרה על שיעורים 1 עד 5', 'חמישה שלבים ואתגר, עם ניקוד ותגים'),
]
# תווית אדומה ליד שורה בדף הראשי: {שם בפרסום: טקסט}
BADGE = {'lesson-06.html': 'לא למבחן ב־02.11'}
# מצגות עם מצב טלפון
PHONE = {name for _, name, _, _ in PUBLISH}
# חידוני חזרה: (קישור, כותרת, תיאור)
QUIZZES = [
    ('https://teachers-6e0bb.web.app/p/sh_QDRTPW', 'חידון חזרה · שיעורים 1–2', 'נפתח באפליקציית QuizPlay'),
    ('https://yanivhak.github.io/yopoy/play.html?q=sh_MR2AJP&t=1', 'חידון חזרה · שיעורים 1–3', 'נפתח באפליקציית QuizPlay'),
    ('https://yanivhak.github.io/yopoy/play.html?q=sh_P5G6HC&t=1', 'חידון חזרה · שיעורים 1–5', 'נפתח באפליקציית QuizPlay'),
]

# ספירת כניסות אנונימית (Firebase · mada-lessons). נשמרים רק מספרים לכל דף — בלי מזהה, בלי IP.
# כל מכשיר סופר אצלו (localStorage) כמה פעמים נכנס לדף, ושולח +1 רק למונים:
#   visits — כל כניסה · devices — כניסה ראשונה של מכשיר · ge2/ge5/ge10 — מכשיר שהגיע לכניסה 2/5/10
#   days/<תאריך>/visits — כל כניסה באותו יום · days/<תאריך>/devices — כניסה ראשונה של מכשיר באותו יום
# שנה חדשה / ספר חדש: לשנות STATS_YEAR / STATS_COURSE. STATS_DB ריק = הספירה כבויה.
STATS_DB = 'https://mada-lessons-default-rtdb.europe-west1.firebasedatabase.app'
STATS_YEAR = '2026-2027'
STATS_COURSE = 'chem-bio-9'

def stats_js(page):
    # לא סופרים: קובץ מקומי (file://) ודפדפן אוטומטי (navigator.webdriver — בדיקות Playwright שלי; יניב, 01.11: „לא ייתכן 230 מכשירים מכיתה של 30”)
    # „all” — מכשירים שונים באתר כולו: מכשיר שנכנס לכמה דפים באותו יום נספר פעם אחת (בלי זה, „כל הדפים” בדף הניהול סכם מכשיר פעם לכל דף)
    if not STATS_DB: return ''
    return ("<script>(function(){try{if(location.protocol!=='https:'||navigator.webdriver)return;"
            "var R='%s/siteStats/%s/%s/',P=R+'%s/',k='v:%s:%s:%s',a='v:%s:%s:all',"
            "n=(parseInt(localStorage.getItem(k),10)||0)+1;localStorage.setItem(k,n);"
            "var d=new Date().toLocaleDateString('sv-SE',{timeZone:'Asia/Jerusalem'}),fd=localStorage.getItem(k+':d')!==d;"
            "if(fd)localStorage.setItem(k+':d',d);"
            "var an=!localStorage.getItem(a),ad=localStorage.getItem(a+':d')!==d;if(an)localStorage.setItem(a,1);if(ad)localStorage.setItem(a+':d',d);"
            "function u(x){fetch(x+'.json',{method:'PUT',body:'{\".sv\":{\"increment\":1}}',keepalive:true}).catch(function(){})}"
            "function s(m){u(P+m)}"
            "s('visits');if(n==1)s('devices');if(n==2)s('ge2');if(n==5)s('ge5');if(n==10)s('ge10');"
            "s('days/'+d+'/visits');if(fd)s('days/'+d+'/devices');"
            "if(an)u(R+'all/devices');if(ad)u(R+'all/days/'+d+'/devices')}catch(e){}})()</script>"
            % (STATS_DB, STATS_YEAR, STATS_COURSE, page, STATS_YEAR, STATS_COURSE, page, STATS_YEAR, STATS_COURSE))

# דף הניהול (docs/admin.html) — קורא את המונים אחרי כניסה עם Google. לא מקושר מהדף הראשי.
# ההגדרות הן של אפליקציית ה-Web בפרויקט mada-lessons (לא סוד — ההגנה היא כללי המסד).
ADMIN_CONFIG = {
    'apiKey': 'AIzaSyArfI75uEh0OXhPwZdRWMs3fo54oiNhmC4',
    'authDomain': 'mada-lessons.firebaseapp.com',
    'databaseURL': 'https://mada-lessons-default-rtdb.europe-west1.firebasedatabase.app',
    'projectId': 'mada-lessons',
    'storageBucket': 'mada-lessons.firebasestorage.app',
    'messagingSenderId': '480805389223',
    'appId': '1:480805389223:web:a193d8a3ab37c9515dac82',
}

def admin_page():
    import json
    s = open(os.path.join(ROOT, 'tools', 'admin_stats.html'), encoding='utf8').read()
    titles = {'index': 'הדף הראשי', 'quizzes': 'חידונים · חידוני חזרה'}
    for _, name, t, _ in PUBLISH + PAGES: titles[name[:-len('.html')]] = t
    s = re.sub(r'/\*CONFIG\*/.*?/\*END\*/', lambda m: json.dumps(ADMIN_CONFIG), s, count=1)
    s = re.sub(r'/\*TITLES\*/.*?/\*END\*/', lambda m: json.dumps(titles, ensure_ascii=False), s, count=1)
    return s

def add_stats(s, name):
    i = s.rindex('</body>')
    return s[:i] + stats_js(name[:-len('.html')]) + s[i:]

APP_META = ('<meta name="apple-mobile-web-app-capable" content="yes"><meta name="mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="black"><meta name="apple-mobile-web-app-title" content="מדעים ט3">'
            '<meta name="theme-color" content="#080F1A">')

END_JS = '''<script>
(function(){
  var nx=document.getElementById('navnext'), all=document.querySelectorAll('section.slide');
  function atEnd(){ var sl=document.querySelector('.slide.on'); return sl===all[all.length-1] && !sl.querySelector('.step:not(.show)'); }
  function upd(){ var e=atEnd(); nx.classList.toggle('end',e); nx.title=e?'סיום — חזרה לדף הראשי':'קדימה'; nx.setAttribute('aria-label',nx.title); }
  nx.addEventListener('click',function(ev){ if(nx.classList.contains('end')){ ev.stopImmediatePropagation(); location.href='./'; } },true);
  new MutationObserver(upd).observe(document.getElementById('stage'),{subtree:true,attributes:true,attributeFilter:['class']});
  upd();
})();
</script>
'''

# תוויות בשורת התחתית שמיועדות למורה — לא מוצגות לתלמידים
TEACHER_ONLY = {'נקודת עצירה אפשרית', 'נקודת עצירה מומלצת', 'הצבעה מהחזית', 'הדגמת מורה'}

def foot_text(t):
    """שורת התחתית לתלמידים: „שיעור 2 · חלק ג · עמוד 18” ← „שיעור 2, חלק ג. בספר: עמוד 18”.
    בלי נקודות מפרידות — בעקבות הערת המנהלת שהניסוח נראה כמו הנחיות ל־AI. קובצי המורה לא משתנים."""
    parts = [x.strip() for x in t.split(' · ') if x.strip() not in TEACHER_ONLY]
    if len(parts) == 1: return t
    head = ''
    if parts[:2] == ['מדע וטכנולוגיה', 'כיתה ט']:   # השקופית הראשונה
        head, parts = 'מדע וטכנולוגיה, כיתה ט. ', parts[2:]
    pages = [x for x in parts if re.match(r'עמוד(ים)? ', x)]
    rest = [x for x in parts if x not in pages]
    txt = rest[0] + (': ' + ', '.join(rest[1:]) if rest[0] == 'מעבדה' and len(rest) > 1 else ''.join(', ' + x for x in rest[1:]))
    if pages: txt += '. בספר: ' + '; '.join(pages)
    return head + txt

# משפטים שבהם המורה „מדבר” לכיתה מתוך המצגת (ניהול הפעילות, הסבר על השקופיות) — לא מוצגים לתלמידים.
# (מקור, החלפה) — מחרוזת מדויקת מקובץ המורה. יניב: „אין צורך להכניס במצגות מה שאני אומר לתלמידים”.
CLASS_VOICE = [
    (' אני עובר אחד־אחד ואתם מרימים יד.', ''),
    (' אני עובר אחת־אחת ואתם מרימים יד.', ''),
    ('<div class="sub">כל שורה היא שלב. עוצרים איפה שעצרנו.</div>', ''),
    ('<div class="sub">כל שורה היא שלב.</div>', ''),
    (' נבנה אותן לאט, אחת־אחת.', ''),
    ('<div class="sub">השקופית הבאה נשענת עליהן, ולכן נבנה אותן קודם.</div>', ''),
    ('<div class="sub">לפני כל שורה — מה אתם אומרים?</div>', ''),
    # שיעור 3, שקופית הפתיחה: הצעד הרביעי היה רק המשפט הזה — יורד, והשקופית בת 3 צעדים
    ('\n    <div class="step" data-s="4" style="font-size:calc(22px * var(--fs));color:#6E8199">נתחיל בחזרה קצרה, וממשיכים.</div>', ''),
]

def class_voice(s):
    if 'נתחיל בחזרה קצרה, וממשיכים.' in s:
        s = s.replace('<section class="slide dark" data-steps="4"', '<section class="slide dark" data-steps="3"', 1)
    # שיעור 1, שקופית 3: הצעד השני היה רק „על חלק מהם אשאל ״למה״…” — יורד, והשקופית בת צעד אחד
    s, n = re.subn(r'(<section class="slide" data-steps=")2(" data-timer="5"[^>]*>(?:(?!</section>).)*?)\n  <div class="step" data-s="2"[^>]*>על חלק מהם אשאל ״למה״\. הקטגוריה קלה, הנימוק פחות\.</div>',
                   r'\g<1>1\2', s, count=1, flags=re.S)
    for a, b in CLASS_VOICE:
        s = s.replace(a, b)
    return s

def sec_text(t):
    """כיתוב בשורה העליונה של המנוע החדש: „חלק א · מספר אטומי · עמ׳ 41” ← „חלק א, מספר אטומי. בספר: עמוד 41” (כמו foot_text)."""
    parts = [x.strip() for x in t.split(' · ') if x.strip()]
    if len(parts) == 1 and not parts[0].startswith('עמ׳ '): return t
    def pg(x):
        n = x[len('עמ׳ '):]
        return ('עמודים ' if re.search(r'[–,]', n) else 'עמוד ') + n
    pages = [pg(x) for x in parts if x.startswith('עמ׳ ')]
    rest = [x for x in parts if not x.startswith('עמ׳ ')]
    txt = ', '.join(rest)
    if pages: txt += ('. ' if txt else '') + 'בספר: ' + '; '.join(pages)
    return txt

END_JS_DECK = '''<script>
(function(){
  var nx=document.getElementById('navnext'), all=document.querySelectorAll('#deck > section.s');
  function atEnd(){ var sl=document.querySelector('#deck > section.s.on'); return sl===all[all.length-1] && !sl.querySelector('.frag:not(.show),.mcq:not(.done)'); }
  function upd(){ var e=atEnd(); nx.classList.toggle('end',e); nx.title=e?'סיום — חזרה לדף הראשי':'קדימה'; nx.setAttribute('aria-label',nx.title); }
  nx.addEventListener('click',function(ev){ if(nx.classList.contains('end')){ ev.stopImmediatePropagation(); location.href='./'; } },true);
  new MutationObserver(upd).observe(document.getElementById('deck'),{subtree:true,attributes:true,attributeFilter:['class']});
  upd();
})();
</script>
'''

def student_deck(s):
    """גרסת תלמידים למצגת על המנוע החדש (tools/deck, משיעור 7). אותם עקרונות כמו student():
    בלי הערות המורה ובלי דף השיעור, נגיעה = הלאה, חצים בשוליים, בית, „סיום” בסוף, כיתובים בלי נקודות מפרידות."""
    # 1. הערות המורה, ותיאור השיעור למורה (דף השיעור, G)
    s = re.sub(r'data-notes="[^"]*"', 'data-notes=""', s)
    s = re.sub(r'data-meta="[^"]*"', 'data-meta=""', s, count=1)
    # 2. כיתובים: השורה העליונה בכל שקופית, הכיתוב ליד הסמל, והשורה בשער — בלי „·”
    s = re.sub(r'data-sec="([^"]*)"', lambda m: 'data-sec="' + html.escape(sec_text(html.unescape(m.group(1))), quote=True) + '"', s)
    s = re.sub(r'(<span class="ch__lesson">)([^<]*)(</span>)', lambda m: m.group(1) + m.group(2).replace(' · ', ', ') + m.group(3), s, count=1)
    s = re.sub(r'(<div class="byline anim">)([^<]*)(</div>)', lambda m: m.group(1) + sec_text(m.group(2).replace('עמודים ', 'עמ׳ ')) + m.group(3), s, count=1)
    # 3. נגיעה בכל מקום = הלאה (במנוע: חצי שמאלי קדימה, ימני אחורה — בלבל, כמו במצגות הישנות)
    a = "(e.clientX < window.innerWidth/2) ? next() : prev();"
    assert a in s; s = s.replace(a, 'next();', 1)
    # 4. בלי הערות, דף השיעור, כל השקופיות ועזרה; רמז לתלמידים
    s = s.replace('</style>', '#notes,#guide,#ov,#help{display:none!important}\n*{touch-action:manipulation}\n'
                  '.navc{position:fixed;z-index:45;width:38px;height:38px;border-radius:50%;border:none;padding:0;cursor:pointer;'
                  'background:rgba(245,166,35,.92);color:#0E1B2E;display:flex;align-items:center;justify-content:center;'
                  'box-shadow:0 2px 8px rgba(0,0,0,.35);-webkit-tap-highlight-color:transparent}\n'
                  '.navc svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}\n'
                  '#navprev{right:4px;top:50%;transform:translateY(-50%)}\n'
                  '#navnext{left:4px;top:50%;transform:translateY(-50%)}\n'
                  '#home{left:4px;top:6px}\n'
                  '.navc .lbl{display:none;font-family:inherit;font-weight:700;font-size:12px}\n'
                  '#navnext.end svg{display:none}#navnext.end .lbl{display:inline}\n'
                  '@media (max-width:1000px){#hint{display:none}}\n</style>', 1)
    s = re.sub(r'<div id="hint">.*?</div>', '<div id="hint">נגיעה במסך = הלאה · החצים בצדדים = אחורה וקדימה</div>', s, count=1, flags=re.S)
    # 5. ניווט: אחורה מימין, קדימה משמאל, בית למעלה. במנוע: חץ שמאלה = קדימה, חץ ימינה = אחורה
    key = lambda k: ("onclick=\"event.stopPropagation();document.dispatchEvent("
                     "new KeyboardEvent('keydown',{key:'%s',bubbles:true}))\"" % k)
    nav = ('<button id="navprev" class="navc" title="אחורה" aria-label="אחורה" ' + key('ArrowRight') +
           '><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>\n'
           '<button id="navnext" class="navc" title="קדימה" aria-label="קדימה" ' + key('ArrowLeft') +
           '><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg><span class="lbl">סיום</span></button>\n'
           '<a id="home" class="navc" href="./" title="כל השיעורים" aria-label="כל השיעורים" onclick="event.stopPropagation()">'
           '<svg viewBox="0 0 24 24"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg></a>\n')
    s = s.replace('<div id="bar"><i></i></div>', '<div id="bar"><i></i></div>\n' + nav, 1)
    # 6. „סיום” בסוף המצגת
    i = s.rindex('</body>')
    s = s[:i] + END_JS_DECK + s[i:]
    # 7. 44px בכל צד לחצים; בטלפון לרוחב — בלי שוליים למעלה ולמטה
    a = 'var s=Math.min(window.innerWidth/1280, availH/720);'
    assert a in s; s = s.replace(a, 'var s=Math.min((window.innerWidth-88)/1280, availH/(availH<500?720:746));', 1)
    # 8. „הוספה למסך הבית” פותחת כאפליקציה
    a = '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">'
    assert a in s; s = s.replace(a, a + APP_META, 1)
    return s

def student(s):
    if '<div id="deck"' in s: return student_deck(s)   # המנוע החדש (משיעור 7)
    s = class_voice(s)
    # 0. שורת התחתית בניסוח רגיל (foot_text)
    s = re.sub(r'(<div class="foot"[^>]*>)([^<]*)(</div>)', lambda m: m.group(1) + foot_text(m.group(2)) + m.group(3), s)
    # 1. הערות המורה
    s = re.sub(r'data-notes="[^"]*"', 'data-notes=""', s)
    # 2. מפת המורה — השקופית האחרונה
    secs = list(re.finditer(r'<section\b[^>]*\bclass="slide[^>]*>.*?</section>', s, re.S))   # גם כש־data-notes לפני class (שיעור 6, עיצוב חדש)
    last = secs[-1]
    assert 'maprows' in last.group(0), 'השקופית האחרונה אינה מפת המורה'
    s = s[:last.start()] + s[last.end():]
    s = s.replace("var mr=document.getElementById('maprows');",
                  "var mr=document.getElementById('maprows')||document.createElement('div');")
    s = s.replace('slides.length-2', 'slides.length-1')   # End → הסיכום, שהוא עכשיו האחרונה
    # 3. נגיעה בכל מקום במסך = הלאה; אחורה — בכפתור (נגיעה בצד ימין בלבלה: התוכן העברי נמצא שם)
    # 4. בלי פאנל הערות, ורמז שמתאים לטלפון
    s = s.replace('</style>', '#notes{display:none!important}\n*{touch-action:manipulation}\n</style>', 1)   # בלי זום בנגיעה כפולה — תלמידים נוגעים מהר
    s = re.sub(r'<div id="hint">[^<]*</div>',
               '<div id="hint">נגיעה במסך = הלאה · החצים בצדדים = אחורה וקדימה</div>', s)
    # 5. ניווט: עיגולים קטנים בשוליים הכהים — אחורה מימין, קדימה משמאל, בית למעלה. A+/A− ושאר הסרגל מוסתרים
    s = s.replace('#notes{display:none!important}', '#notes{display:none!important}\n'
                  '#fsbtn{display:none!important}\n'
                  '.navc{position:fixed;z-index:25;width:38px;height:38px;border-radius:50%;border:none;padding:0;cursor:pointer;'
                  'background:rgba(245,166,35,.92);color:#0E1B2E;display:flex;align-items:center;justify-content:center;'
                  'box-shadow:0 2px 8px rgba(0,0,0,.35);-webkit-tap-highlight-color:transparent}\n'
                  '.navc svg{width:20px;height:20px;stroke:currentColor;fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}\n'
                  '#navprev{right:4px;top:50%;transform:translateY(-50%)}\n'
                  '#navnext{left:4px;top:50%;transform:translateY(-50%)}\n'
                  '#home{left:4px;top:6px}\n'
                  '.navc .lbl{display:none;font-family:inherit;font-weight:700;font-size:12px}\n'
                  '#navnext.end svg{display:none}#navnext.end .lbl{display:inline}\n'
                  '@media (max-width:1000px){#hint{display:none}}', 1)   # במסך צר הרמז מתנגש
    key = lambda k: ("onclick=\"event.stopPropagation();document.dispatchEvent("
                     "new KeyboardEvent('keydown',{key:'%s',bubbles:true}))\"" % k)
    nav = ('<button id="navprev" class="navc" title="אחורה" aria-label="אחורה" ' + key('ArrowRight') +
           '><svg viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg></button>\n'
           '<button id="navnext" class="navc" title="קדימה" aria-label="קדימה" ' + key('ArrowLeft') +
           '><svg viewBox="0 0 24 24"><path d="M15 5l-7 7 7 7"/></svg><span class="lbl">סיום</span></button>\n'
           '<a id="home" class="navc" href="./" title="כל השיעורים" aria-label="כל השיעורים" onclick="event.stopPropagation()">'
           '<svg viewBox="0 0 24 24"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg></a>\n')
    s = s.replace('<div id="fsbtn">', nav + '<div id="fsbtn">', 1)
    # בסוף המצגת (שקופית אחרונה, כל הצעדים גלויים) החץ קדימה הופך ל„סיום” שחוזר לדף הראשי
    i = s.rindex('</body>')
    s = s[:i] + END_JS + s[i:]
    # השקופית משאירה 44px בכל צד לחצים (במסך צר אין שוליים טבעיים)
    # בטלפון לרוחב (גובה קטן) — בלי שוליים מסביב, כל פיקסל של גובה לשקופית
    s, k = re.subn(r'Math\.min\((window\.)?innerWidth/1280,\s*(window\.)?innerHeight/720\)\*0\.965',
                   'Math.min((innerWidth-88)/1280,innerHeight/(innerHeight<500?720:746))', s)
    assert k == 1, k
    # „הוספה למסך הבית” פותחת כאפליקציה, בלי סרגלי הדפדפן
    s = s.replace('<meta name="viewport" content="width=device-width, initial-scale=1">',
                  '<meta name="viewport" content="width=device-width, initial-scale=1">' + APP_META, 1)
    # 6. בלי A+/A− — גודל גופן קבוע (גם המקשים + ו- לא עושים כלום)
    assert 'var STEPS=[1,1.12,1.25,1.4]' in s
    s = s.replace('var STEPS=[1,1.12,1.25,1.4]', 'var STEPS=[1]', 1)
    s = s.replace('#notes{display:none!important}', '#notes{display:none!important}\n#fsdown,#fsup,#fslabel{display:none!important}', 1)
    return s

# ציור קטן ליד כותרת של תחום — לקוח מהשיעורים עצמם, בלי תנועה. כימיה: מולקולת מימן כמו בשיעור 6 (ענן, שני גרעינים, זוג משותף)
SECTION_ART = {
    'כימיה': '<svg class="art" viewBox="0 0 170 74" aria-hidden="true"><defs><radialGradient id="artH"><stop offset="0" stop-color="#7DBDF0" stop-opacity=".95"/>'
             '<stop offset=".6" stop-color="#5AA9E6" stop-opacity=".45"/><stop offset="1" stop-color="#5AA9E6" stop-opacity="0"/></radialGradient></defs>'
             '<circle cx="62" cy="37" r="36" fill="url(#artH)"/><circle cx="108" cy="37" r="36" fill="url(#artH)"/>'
             '<circle cx="62" cy="37" r="12" fill="#1F3A63" stroke="#fff" stroke-width="2"/><circle cx="108" cy="37" r="12" fill="#1F3A63" stroke="#fff" stroke-width="2"/>'
             '<text x="62" y="41.5" fill="#fff" font-size="11" font-weight="900" text-anchor="middle" direction="ltr">+1</text><text x="108" y="41.5" fill="#fff" font-size="11" font-weight="900" text-anchor="middle" direction="ltr">+1</text>'
             '<circle cx="85" cy="30" r="4.5" fill="#F5A623" stroke="#0E1B2E" stroke-width="1.5"/><circle cx="85" cy="44" r="4.5" fill="#F5A623" stroke="#0E1B2E" stroke-width="1.5"/></svg>',
}

def section(title):
    return f'<h2 class="sec"><span>{html.escape(title)}</span>{SECTION_ART.get(title, "")}</h2>'

SCHOOL = 'מקיף שש שנתי למנהיגות ולמצוינות ע״ש יונתן נתניהו, חולון'
# חותמת קטנה במצגות (יניב, 27.10: „השם שלי, נוצר על ידי, ומתחת בית הספר, בקטן ממש כמו חותמת שלא יפריע ולא יבלוט”):
# במחשב — בפינה השמאלית התחתונה, מחוץ לשקופית; בטלפון — בסוף אזור הגלילה, מתחת לשקופית
STAMP_CSS = ('#stamp{position:fixed;left:12px;bottom:6px;z-index:5;pointer-events:none;font-family:inherit;font-size:10.5px;line-height:1.35;'
             'color:rgba(255,255,255,.38);text-align:left;direction:rtl}#stamp small{display:block;font-size:9px;color:rgba(255,255,255,.3)}'
             'html.ph #stamp{position:static;text-align:center;padding:10px 12px 14px}html.ph #viewport>#stamp{padding-bottom:60px}')
def stamp(s):
    s = s.replace('</style>', STAMP_CSS + '</style>', 1)
    i = s.rindex('</body>')
    return s[:i] + ('<div id="stamp">נוצר על ידי ד״ר חכים יניב<small>' + SCHOOL + '</small></div>\n'
                    '<script>(function(){var t=document.getElementById("stamp");function f(){var ph=document.documentElement.classList.contains("ph"),'
                    'c=document.getElementById("viewport")||document.getElementById("stage");(ph?c:document.body).appendChild(t);}'
                    'f();addEventListener("resize",f);})();</script>\n') + s[i:]

# צבע לכל שורה בדף הראשי — הצבעים של השלבים במשחק החזרה
ROW_C = {'quizzes.html': '#2EE6C5', 'concepts-1-5.html': '#8EC5FF', 'lesson-01.html': '#FFB020', 'lesson-02.html': '#8EC5FF', 'lesson-03.html': '#2EE6C5', 'lesson-04.html': '#B49CFF', 'lesson-05.html': '#FF6A4A',
         'lesson-06.html': '#9BE15D', 'lesson-07.html': '#4FB3FF', 'lesson-08.html': '#FF7AC6', 'lesson-summary-1-5.html': '#FFC24B',
         'exam-0211.html': '#FFB020', 'game-1-5.html': '#FF6A4A', 'lab-01.html': '#B49CFF', 'lab-02.html': '#2EE6C5'}
SCI_CSS = open(os.path.join(ROOT, 'tools', 'deck', 'science.css'), encoding='utf8').read()
MOL = re.search(r'-webkit-mask:(url\("data:image/svg\+xml,.*?"\)) center/contain no-repeat', SCI_CSS).group(1)   # המולקולה המוארת של המצגות

# ציורים לשורות שאין להן תמונה מוקטנת (יניב, 27.10: „על המשחק שים לוגו של משחק שיהיה ברור”)
def _art(body):
    return f'<svg class="th art" viewBox="0 0 104 66" aria-hidden="true">{body}</svg>'
ROW_ART = {
    # משחק: שלט משחק וכוכבים
    'game-1-5.html': _art('<path d="M30 30 C30 23 35 21 41 21 H63 C69 21 74 23 74 30 L79 47 C81 54 74 57 70 52 L64 45 H40 L34 52 C30 57 23 54 25 47 Z" fill="#FF6A4A"/>'
                          '<rect x="36" y="29" width="4" height="12" rx="1" fill="#04060C"/><rect x="32" y="33" width="12" height="4" rx="1" fill="#04060C"/>'
                          '<circle cx="64" cy="31" r="3" fill="#FFC24B"/><circle cx="70" cy="37" r="3" fill="#FFC24B"/><circle cx="58" cy="37" r="3" fill="#04060C"/><circle cx="64" cy="43" r="3" fill="#04060C"/>'
                          '<g fill="#FFC24B"><path d="M38 6l1.8 3.7 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z"/><path d="M52 2l2.2 4.5 5 .7-3.6 3.5.9 4.9-4.5-2.4-4.5 2.4.9-4.9-3.6-3.5 5-.7z"/>'
                          '<path d="M66 6l1.8 3.7 4 .6-2.9 2.8.7 4-3.6-1.9-3.6 1.9.7-4-2.9-2.8 4-.6z"/></g>'),
    # החומר למבחן: לוח כתיבה עם רשימה מסומנת
    'exam-0211.html': _art('<rect x="34" y="9" width="36" height="50" rx="5" fill="#FFB020"/><rect x="38" y="15" width="28" height="40" rx="2" fill="#F6F1E6"/>'
                           '<rect x="44" y="6" width="16" height="7" rx="3" fill="#8A5A00"/>'
                           '<g stroke="#2EA36B" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"><path d="M41 23l2.5 2.5 4-4.5"/><path d="M41 33l2.5 2.5 4-4.5"/><path d="M41 43l2.5 2.5 4-4.5"/></g>'
                           '<g fill="#9AA6B8"><rect x="51" y="22" width="12" height="3" rx="1.5"/><rect x="51" y="32" width="12" height="3" rx="1.5"/><rect x="51" y="42" width="12" height="3" rx="1.5"/></g>'),
    # חידון: בועת שאלה ותשובות לבחירה
    'quizzes.html': None,
    # מושגים: כרטיסייה עם מושג והגדרה
    'concepts-1-5.html': _art('<rect x="26" y="10" width="52" height="46" rx="6" fill="#8EC5FF"/><rect x="26" y="10" width="52" height="12" rx="6" fill="#5AA9E6"/>'
                              '<text x="52" y="20" text-anchor="middle" font-family="Assistant,Arial" font-weight="800" font-size="9" fill="#04060C">אטום</text>'
                              '<g fill="#04060C" opacity=".55"><rect x="33" y="28" width="38" height="3.5" rx="1.75"/><rect x="33" y="35" width="32" height="3.5" rx="1.75"/><rect x="33" y="42" width="36" height="3.5" rx="1.75"/></g>'
                              '<circle cx="74" cy="52" r="10" fill="#FFC24B"/><text x="74" y="56.5" text-anchor="middle" font-family="Assistant,Arial" font-weight="800" font-size="12" fill="#04060C">?</text>'),
    'quiz': _art('<path d="M28 8 H76 C80 8 82 10 82 14 V32 C82 36 80 38 76 38 H48 L40 45 V38 H28 C24 38 22 36 22 32 V14 C22 10 24 8 28 8 Z" fill="#2EE6C5"/>'
                 '<text x="52" y="31" text-anchor="middle" font-family="Assistant,Arial" font-weight="800" font-size="22" fill="#04060C">?</text>'
                 '<g><rect x="22" y="49" width="28" height="7" rx="3.5" fill="#B49CFF"/><rect x="54" y="49" width="28" height="7" rx="3.5" fill="#FFB020"/>'
                 '<rect x="22" y="58" width="28" height="6" rx="3" fill="#8EC5FF" opacity=".8"/><rect x="54" y="58" width="28" height="6" rx="3" fill="#FF6A4A" opacity=".8"/></g>'),
}

SITE_CSS = r'''/* בעיצוב של משחק החזרה (יניב, 27.10): רקע שחור, זוהר ומולקולה מוארת בפינה, כרטיסים כהים עם פס צבע */
:root{--bg:#04060C;--panel:rgba(255,255,255,.085);--panel2:rgba(255,255,255,.13);--line:rgba(255,255,255,.22);--text:#EEF2F9;--muted:#B9C4D6;--ac:#FFB020;--ac-rgb:255,176,32}
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Assistant',system-ui,Arial,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
body::before{content:'';position:fixed;inset:0;z-index:0;pointer-events:none;
  background:radial-gradient(560px 520px at 9% 96%,rgba(var(--ac-rgb),.20),rgba(var(--ac-rgb),.06) 45%,transparent 72%),radial-gradient(900px 520px at 100% 0%,rgba(var(--ac-rgb),.10),transparent 62%)}
body::after{content:'';position:fixed;z-index:0;left:-130px;bottom:-190px;width:430px;height:430px;pointer-events:none;transform:rotate(14deg);
  background:radial-gradient(circle at 62% 38%,rgba(var(--ac-rgb),.42),rgba(var(--ac-rgb),.18) 55%,rgba(var(--ac-rgb),.07) 80%);
  -webkit-mask:__MOL__ center/contain no-repeat;mask:__MOL__ center/contain no-repeat}
.wrap{position:relative;z-index:1;max-width:680px;margin:0 auto;padding:20px 16px 40px}
h1{font-size:44px;font-weight:800;color:#fff;line-height:1.05;margin-top:6px;letter-spacing:-.01em}
.sub{color:var(--muted);margin:12px 0 26px;font-size:18px;line-height:1.5}
.row{--c:var(--ac);background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--c);border-radius:16px;margin-bottom:12px;overflow:hidden;transition:background .2s}
.row:hover{background:var(--panel2)}
.main{display:flex;align-items:center;gap:14px;color:#fff;text-decoration:none;padding:14px 16px}
.main:active{transform:scale(.99)}
.tx{display:flex;flex-direction:column;gap:2px;flex:1;min-width:0}
.th{width:104px;height:66px;object-fit:contain;background:#F1F4F8;border-radius:10px;padding:4px;flex-shrink:0;box-shadow:0 0 22px -8px var(--c)}
.k{font-size:13px;font-weight:700;color:var(--c);letter-spacing:.04em}
.t{font-size:20px;font-weight:800}
.n{direction:ltr;unicode-bidi:isolate;white-space:nowrap}
.d{font-size:14.5px;color:var(--muted)}
.b{align-self:flex-start;background:#FF5C6C;color:#fff;font-size:13px;font-weight:700;border-radius:8px;padding:2px 10px;margin-top:4px}
.wrap h2{font-size:28px;font-weight:800;color:#fff;margin:8px 0 10px;padding-bottom:8px;border-bottom:2px solid rgba(var(--ac-rgb),.6)}
.wrap h3{display:flex;align-items:center;gap:10px;font-size:16px;font-weight:700;color:var(--ac);letter-spacing:.02em;margin:26px 0 12px}
.wrap h3::before{content:'';width:26px;height:2px;background:var(--ac)}
.wrap h2.sec{display:flex;align-items:center;justify-content:space-between;gap:12px}
.wrap h2.sec .art{width:150px;height:auto;flex-shrink:0;margin-bottom:-8px}
.wrap h2+h3{margin-top:10px}
.note{color:var(--muted);font-size:15px;margin-top:22px;line-height:1.55}
.th.art{background:rgba(255,255,255,.06);border:1px solid var(--line);padding:0}
.row.big .t{font-size:24px}
/* בטלפון (יניב, 27.10: „בטלפון המולקולה מפריעה”): מולקולה קטנה ועמומה יותר, וכרטיסים אטומים כדי שלא תיראה דרכם */
@media (max-width:560px){
body::after{width:240px;height:240px;left:-80px;bottom:-110px;opacity:.55}
.row{background:#14161D}
}
.site{display:inline-flex;align-items:center;gap:8px;margin-bottom:18px;padding:0 14px 0 4px;height:40px;border-radius:20px;background:rgba(255,255,255,.07);border:1px solid var(--line);color:#fff;text-decoration:none;font-size:15px;font-weight:700}
.site i{width:32px;height:32px;border-radius:50%;background:#F5A623;color:#0E1B2E;display:flex;align-items:center;justify-content:center}
.site svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
.copy{color:#7F93AD;font-size:12.5px;margin-top:28px;padding-top:12px;border-top:1px solid var(--line);line-height:1.7;text-align:center}
.school{display:flex;align-items:center;gap:12px;margin-bottom:18px;font-size:15px;font-weight:700;color:var(--text);line-height:1.4}
.school img{height:52px;width:auto;flex-shrink:0}
.copy a{color:inherit;white-space:nowrap}
'''.replace('__MOL__', MOL)

def site_page(title, body):
    """דף באתר בעיצוב של הדף הראשי (רקע שחור, מולקולה בפינה, כרטיסים כהים), עם בית, הסמל וזכויות היוצרים"""
    return f'''<!DOCTYPE html>
<!-- © 2026 ד״ר חכים יניב · {SCHOOL} · רישיון CC BY-NC-ND 4.0: מותר לשתף עם ציון היוצר ובית הספר, בלי שינויים ובלי שימוש מסחרי · https://creativecommons.org/licenses/by-nc-nd/4.0/ -->
<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{APP_META}
<title>{html.escape(title)}</title>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400..800&display=swap" rel="stylesheet">
<style>
{SITE_CSS}
</style></head><body><div class="wrap">
<div class="school"><img src="img/logo-mark.png" alt="הסמל של בית הספר"><span>{SCHOOL}</span></div>
<a class="site" href="./"><i><svg viewBox="0 0 24 24"><path d="M4 11l8-7 8 7"/><path d="M6 10v10h12V10"/></svg></i>כל חומרי הלימוד</a>
{body}
{COPY}
</div></body></html>
'''

COPY = '<div class="copy">נוצר על ידי ד״ר חכים יניב · © 2026<br>מותר לשתף עם ציון היוצר ובית הספר, בלי שינויים ובלי שימוש מסחרי · <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" dir="ltr">CC BY-NC-ND 4.0</a><br>התכנים מהמקורות שצוינו שייכים לבעליהם</div>'

# דפים רגילים שמקבלים את העיצוב של הדף הראשי (יניב, 27.10: „החומר למבחן … העיצוב הישן. עצב עם החדש”):
# התוכן נלקח מקובץ המקור כמו שהוא, רק העיצוב מתחלף
RESTYLE = {'exam-0211.html', 'concepts-1-5.html'}
EXAM_CSS = (
    '.wrap h2{font-size:24px;margin:28px 0 12px}'
    '.card{--c:var(--ac);background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--c);border-radius:16px;padding:14px 18px;margin-bottom:12px;color:var(--text);line-height:1.55}'
    '.card h3{display:block;font-size:19px;font-weight:800;color:#fff;margin:0 0 6px;letter-spacing:0}.card h3::before{display:none}'
    '.card .pg{color:var(--muted);font-size:15px;margin-bottom:8px}'
    '.card ul{padding-right:20px}.card li{margin:4px 0;font-size:16.5px}.card li::marker{color:var(--c)}'
    'a.deck{display:flex;justify-content:space-between;gap:12px;align-items:center;text-decoration:none;color:#fff}'
    'a.deck .tx{display:flex;flex-direction:column;gap:2px}a.deck .k{font-size:13px;font-weight:700;color:var(--c)}'
    'a.deck .t{font-size:19px;font-weight:800}a.deck .go{color:var(--c);font-weight:700;font-size:15px}'
    'a.deck img{width:104px;height:66px;object-fit:contain;background:#F1F4F8;border-radius:10px;padding:4px;flex-shrink:0;box-shadow:0 0 22px -8px var(--c)}'
    'table{width:100%;border-collapse:collapse;font-size:16.5px}td{padding:9px 4px;border-bottom:1px solid var(--line);vertical-align:top}'
    'tr:last-child td{border-bottom:none}td:first-child{font-weight:800;white-space:nowrap;padding-left:12px;color:var(--ac)}'
    '.sum{background:rgba(var(--ac-rgb),.12);border-radius:12px;padding:10px 14px;margin-top:10px;font-weight:700}'
    '.card.no{--c:#FF5C6C}.card.tip{--c:#2EE6C5}'
    '.f{direction:ltr;unicode-bidi:isolate;font-weight:800}'
    + ''.join(f'.card:has(a[href="{k}"]){{--c:{v}}}' for k, v in ROW_C.items() if k.startswith('lesson-0'))
    + '@media (max-width:560px){.card{background:#14161D}}'
    # דף המושגים: מושג מימין והגדרה משמאל; הטבלה — בטלפון כל שורה כרטיס
    '.def{display:grid;grid-template-columns:130px 1fr;gap:14px;padding:10px 0;border-bottom:1px solid var(--line);font-size:17px;line-height:1.55}'
    '.def:last-child{border-bottom:none}.def>b{color:var(--c);font-weight:800;font-size:18px}'
    '.def small{display:block;font-size:14px;color:var(--muted);margin-top:4px}.def b.in{color:#fff}'
    '.ex{padding:6px 14px}.ex th{font-size:13px;color:var(--muted);text-align:start;padding:8px 4px;border-bottom:1px solid var(--line)}'
    '.ex td{font-size:16px;line-height:1.5}.ex td:first-child{color:#fff;font-size:22px;padding-left:16px}.ex td:first-child small{display:block;font-size:13px;font-weight:400;color:var(--muted)}'
    '.ex i{display:inline-block;font-style:normal;font-size:13px;font-weight:700;color:#04060C;background:var(--c);border-radius:10px;padding:1px 9px;margin:2px 0 2px 4px;white-space:nowrap}'
    '.ex td:nth-child(2){width:150px}'
    '@media (max-width:560px){.def{grid-template-columns:1fr;gap:2px}.ex table,.ex tbody,.ex tr,.ex td{display:block;width:auto!important}.ex thead{display:none}'
    '.ex tr{padding:12px 0;border-bottom:1px solid var(--line)}.ex tr:last-child{border-bottom:none}.ex td{border:none;padding:3px 0}.ex td:first-child small{display:inline;margin-right:8px}}')
def restyle(src, title):
    body = src[src.index('<div class="wrap">') + len('<div class="wrap">'):src.rindex('</div></body>')]
    body = re.sub(r'<a class="home"[^>]*>.*?</a>\s*', '', body, count=1)   # כפתור הבית — מ-site_page
    return site_page(title.split(' · ')[-1], body).replace('</style>', EXAM_CSS + '</style>', 1)

def quiz_rows():
    nums = lambda t: re.sub(r'\d+–\d+', lambda m: f'<span class="n">{m.group(0)}</span>', t)
    return ''.join(f'<div class="row" style="--c:#2EE6C5"><a class="main" href="{u}" target="_blank" rel="noopener"><span class="tx"><span class="k">{html.escape(t.split(' · ')[0])}</span><span class="t">{nums(html.escape(t.split(' · ')[-1]))}</span><span class="d">{html.escape(d)}</span></span>{ROW_ART['quiz']}</a></div>'
                   for u, t, d in QUIZZES)

def quiz_page():
    # חידוני החזרה בדף משלהם (יניב, 27.10), והדף הראשי מקשר אליו מ„לקראת המבחן”
    return site_page('חידוני חזרה', '<h1>חידוני חזרה</h1><div class="sub">חידונים באפליקציית QuizPlay על החומר שלמדנו. כל חידון נפתח בחלון חדש.</div>' + quiz_rows())
ROW_ART['quizzes.html'] = ROW_ART['quiz']

def index_page():
    VER = time.strftime('%Y%m%d%H%M')   # הקישורים משתנים בכל בנייה — הדפדפן לא יציג עותק ישן
    def deck_rows(items, label=None):
        out_ = ''
        for _, out, t, d in items:
            k, t = t.split(' · ', 1) if ' · ' in t else (label, t)   # „שיעור 1 · שם” ← תווית קטנה + כותרת
            img = f'<img class="th" src="img/{out[:-5]}.jpg" alt="">' if os.path.exists(os.path.join(THUMBS, out[:-5] + '.jpg')) else ROW_ART.get(out, '')
            kk = f'<span class="k">{html.escape(k)}</span>' if k else ''
            out_ += f'<div class="row" style="--c:{ROW_C.get(out, "#FFB020")}"><a class="main" href="{out}?v={VER}"><span class="tx">{kk}<span class="t">{html.escape(t)}</span><span class="d">{nums(html.escape(d))}</span>{badge(out)}</span>{img}</a></div>'
        return out_
    def nums(s):   # טווח עמודים כמו 6–9 — משמאל לימין, אחרת מתהפך
        return re.sub(r'\d+–\d+', lambda m: f'<span class="n">{m.group(0)}</span>', s)
    def badge(out):
        return f'<span class="b">{html.escape(BADGE[out])}</span>' if out in BADGE else ''
    summ = [x for x in PUBLISH if x[1].startswith('lesson-summary')]   # מצגת הסיכום — תחת „לקראת המבחן”, לא בין השיעורים
    exams = deck_rows(PAGES + summ + [('', 'quizzes.html', 'חידונים · חידוני חזרה', 'שלושה חידונים באפליקציית QuizPlay')])
    rows = deck_rows([x for x in PUBLISH if not x[1].startswith('lab-') and x not in summ])
    labs = deck_rows([x for x in PUBLISH if x[1].startswith('lab-')])
    return f'''<!DOCTYPE html>
<!-- © 2026 ד״ר חכים יניב · מקיף שש שנתי למנהיגות ולמצוינות ע״ש יונתן נתניהו, חולון · רישיון CC BY-NC-ND 4.0: מותר לשתף עם ציון היוצר ובית הספר, בלי שינויים ובלי שימוש מסחרי · https://creativecommons.org/licenses/by-nc-nd/4.0/ -->
<html lang="he" dir="rtl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{APP_META}
<title>מדעים בכיתה ט3 יהלו״ם</title>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@400..800&display=swap" rel="stylesheet">
<style>
{SITE_CSS}
</style></head><body><div class="wrap">
<div class="school"><img src="img/logo-mark.png" alt="הסמל של בית הספר"><span>{SCHOOL}</span></div>
<h1>מדעים בכיתה ט3 יהלו״ם</h1><div class="sub">כאן נמצאים כל חומרי הלימוד שלנו במדעים: המצגות מהשיעורים, המעבדות וחידוני החזרה. מספרי העמודים מתייחסים לספר ״כימיה ומדעי החיים לכיתה ט״.</div>
{section('כימיה')}
<h3>לקראת המבחן</h3>
{exams}
<h3>המצגות מהשיעורים</h3>
{rows}
<h3>המעבדות</h3>
{labs}
<div class="note">איך משתמשים במצגות: נוגעים בשקופית כדי להתקדם. החצים שבצדי המסך מעבירים אחורה וקדימה, וכפתור הבית מחזיר לדף הזה. במחשב אפשר להשתמש גם בחצים שבמקלדת.</div>
<div class="copy">נוצר על ידי ד״ר חכים יניב · © 2026<br>מותר לשתף עם ציון היוצר ובית הספר, בלי שינויים ובלי שימוש מסחרי · <a href="https://creativecommons.org/licenses/by-nc-nd/4.0/" dir="ltr">CC BY-NC-ND 4.0</a><br>התכנים מהמקורות שצוינו שייכים לבעליהם</div>
</div></body></html>
'''

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for src, name, _, _ in PUBLISH:
        s = open(os.path.join(ROOT, src), encoding='utf8').read()
        s = student(s)
        if name in PHONE: s = (phone_deck if '<div id="deck"' in s else phone_mode).apply(s)
        s = stamp(s)
        s = add_stats(s, name)
        open(os.path.join(out, name), 'w', encoding='utf8').write(s)
        print('built', name)
    for src, name, t, _ in PAGES:
        s = open(os.path.join(ROOT, src), encoding='utf8').read()
        if name in RESTYLE: s = restyle(s, t)
        open(os.path.join(out, name), 'w', encoding='utf8').write(add_stats(s, name))
        print('built', name)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf8').write(add_stats(index_page(), 'index.html'))
    open(os.path.join(out, 'quizzes.html'), 'w', encoding='utf8').write(add_stats(quiz_page(), 'quizzes.html'))
    print('built quizzes.html')
    open(os.path.join(out, 'admin.html'), 'w', encoding='utf8').write(admin_page())
    print('built admin.html')
    os.makedirs(os.path.join(out, 'img'), exist_ok=True)
    for f in os.listdir(THUMBS): shutil.copy(os.path.join(THUMBS, f), os.path.join(out, 'img', f))
    shutil.copy(os.path.join(ROOT, 'tools', 'assets', 'logo-mark-112.png'), os.path.join(out, 'img', 'logo-mark.png'))   # הסמל של בית הספר
    open(os.path.join(out, '.nojekyll'), 'w').close()
