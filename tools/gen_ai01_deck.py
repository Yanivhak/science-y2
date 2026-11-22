# מחולל: שיעור AI 1, „מה זה בינה מלאכותית, ולמה בודקים אותה" (22.11.2026).
# התכנון: lessons/AI-01-תכנון.md. השיטה: lessons/איך-בונים-מצגת.md.
# שימוש: python3 tools/gen_ai01_deck.py [קובץ פלט]
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deck'))
from kit import Deck

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/lessons/AI-01-מה-זה-AI.html'

META = ('שיעור AI 1. שתי שעות. נקודת עצירה: אחרי „חיפוש מול צ׳אט". '
        'מטרה: התוכנה כותבת מילה אחרי מילה, ובכל פעם בוחרת מתוך המילים שהכי סביר שיבואו. לכן היא יכולה לכתוב משפט שנשמע נכון ואינו נכון. '
        'מחוון כשירויות AI 2.0 של משרד החינוך (על-יסודי), תחום 1א: „איך בינה מלאכותית עובדת?" (עמ׳ 6). '
        'הכלל של היחידה: תשובה של AI היא טיוטה. בודקים לפני שמשתמשים. ציוד: מקרן. אופציונלי: Gemini פתוח להדגמה חיה.')
D = Deck('בינה מלאכותית, שיעור 1: איך התוכנה כותבת', 'מבוא למדעים, י2, בינה מלאכותית, שיעור 1', META)

SRC = ('מקור: מחוון כשירויות בינה מלאכותית 2.0, על-יסודי, משרד החינוך (sources/), עמ׳ 6, תחום 1א: '
       '„כיצד פועלים כלי בינה מלאכותית (מודלי שפה, מחוללי תמונות וכו׳)? באופן מתמטי על ידי דגימה הסתברותית וחיזוי המילה הבאה בטקסט", '
       'ו„להסביר שמודלי שפה אינם ‚מבינים׳ את המידע כמו בני אדם". '
       'אומת גם מול Google, Machine Learning Crash Course, „Introduction to Large Language Models".')
LIT = 'לומר במילים: „התוכנה בוחרת", „התוכנה כותבת". לא „היא חושבת", לא „היא יודעת" ולא „היא מבינה". התלמידים לוקחים מילים כפשוטן (וגם המחוון, עמ׳ 6).'


def head(eyebrow, title, size='t-md'):
    return f'  <p class="eyebrow anim">{eyebrow}</p>\n  <h2 class="ttl {size} anim">{title}</h2>'


def bars(cands, cls, pick=0):
    """עמודות של מילים אפשריות. cands: [(מילה, אורך 0–100)]. pick: המילה שהתוכנה בוחרת. האורכים להמחשה."""
    rows = ''.join(f'<div class="br{" top" if k == pick else ""}"><b>{w}</b><span><i style="--w:{v}%"></i></span></div>'
                   for k, (w, v) in enumerate(cands))
    return f'<div class="bars {cls}">{rows}</div>'


NOTE_BARS = '<p class="pnote">אורך העמודה: כמה סביר שהמילה תבוא. להמחשה.</p>'


def writer(fixed, steps, q='איזו מילה תבוא עכשיו?'):
    """משפט שנבנה: fixed = המילים שכבר כתובות; steps = [(המילה שנבחרת, עמודות)]. כל שלב = שתי לחיצות (עמודות, בחירה)."""
    ws = ''.join(f'<span class="wd">{w}</span>' for w in fixed) + ''.join(
        f'<span class="wd nw n{k + 1}">{w}</span>' for k, (w, _) in enumerate(steps)) + '<span class="cur"></span>'
    panels = ''.join(bars(c, f'pn p{k + 1}', [x[0] for x in c].index(w)) for k, (w, c) in enumerate(steps))
    marks = ''.join(f'<i class="frag mk b{k + 1}"></i><i class="frag mk w{k + 1}"></i>' for k in range(len(steps)))
    return f'''  <div class="gen mt">
    <div class="sent">{ws}</div>
    <div class="pane"><p class="pq">{q}</p>{panels}{NOTE_BARS}</div>
  </div>
  {marks}'''


# ======================= 1. פתיחה: מה נעשה היום =======================
PLAN = ['ככה כותבת תוכנה שאף אחד לא כיוון', 'איך התוכנה כותבת', 'עכשיו אתם התוכנה', 'חיפוש מול צ׳אט', 'מצא את הטעות', 'הכלל']
D.add('  <p class="eyebrow anim">בינה מלאכותית, שיעור 1</p>\n  <h2 class="ttl t-lg anim">איך התוכנה כותבת,<br>ולמה בודקים אותה</h2>'
      + '\n  <ol class="today mt">' + ''.join(f'<li class="frag">{x}</li>' for x in PLAN) + '</ol>',
      '''פתיחה: מה נעשה היום
כל לחיצה מגלה שלב. לקרוא כל שלב בקול. המבנה קבוע בכל שיעור: התלמידים יודעים מראש מה יקרה.
• השיעור בנוי משני חלקים: איך התוכנה כותבת (כחול), ומצא את הטעות (ירוק). נקודת עצירה בין השעות: אחרי „חיפוש מול צ׳אט".
• היום לא נכנסים לכלים בעצמם. רק מסתכלים ומצביעים.
• לפני שהתלמידים עובדים עם Gemini בעצמם: הנחיות משרד החינוך (ינואר 2026) מחייבות אישור הורים והכשרה מקדימה. השיעור הזה הוא חלק מההכשרה.''',
      'מה נעשה היום', 'open', 'פתיחה', mins=2)


# ======================= 2. טקסט שאף אחד לא כיוון =======================
RAW = ('<p class="rh"><span class="sg g2">🌍 <b>מהו אלבדו?</b></span></p>'
       '<p>אלבדו הוא מדד לכמות האור שמשטח מחזיר <span class="sg g1">—</span> והוא משחק תפקיד מרכזי באקלים של כדור הארץ.</p>'
       '<p class="rh"><span class="sg g2"><b>למה זה חשוב?</b></span></p>'
       '<ul><li><b>משטחים בהירים</b> <span class="sg g1">—</span> כמו שלג וקרח <span class="sg g1">—</span> מחזירים את רוב קרינת השמש.</li>'
       '<li><b>משטחים כהים</b> <span class="sg g1">—</span> כמו אוקיינוסים ויערות <span class="sg g1">—</span> בולעים אותה.</li></ul>'
       '<p>כשהקרח נמס, נחשף משטח כהה יותר. <span class="sg g3">התוצאה?</span> יותר חום נבלע <span class="sg g1">—</span> וזה מוביל לעוד המסה.</p>')
SIGNS = [('g1', 'מקף ארוך באמצע משפט, שוב ושוב'), ('g2', 'כותרות מודגשות וסמלילים בטקסט קצר'), ('g3', 'שאלה שהטקסט עונה עליה מיד')]
D.add(head('ככה כותבת תוכנה שאף אחד לא כיוון', 'מה נראה כאן לא כמו טקסט רגיל?', 't-sm') + f'''
  <div class="raw2 mt">
    <div class="rawtxt">{RAW}</div>
    <ul class="signs clean">''' + ''.join(f'<li class="frag hl-{c}">{t}</li>' for c, t in SIGNS) + '''</ul>
  </div>
  <p class="frag concl">ככה נראה טקסט שאף אחד לא ערך. זה סימן, לא הוכחה: גם אנשים כותבים עם מקפים.</p>''',
      '''ככה כותבת תוכנה שאף אחד לא כיוון
הטקסט נכתב על ידי Claude (תוכנת AI) ב-22.11.2026, בבקשה לכתוב על אלבדו בלי שום הגבלה. לא נערך.
לשאול קודם: „מה נראה לכם כאן לא כמו טקסט שאדם כותב במחברת?" ורק אז לחשוף. כל לחיצה מדגישה סימן אחד בטקסט.
• מקף ארוך (—): הופיע שש פעמים בטקסט קצר.
• כותרות מודגשות וסמלילים (🌍) לטקסט של חמישה משפטים.
• „התוצאה?" שאלה שהטקסט עונה עליה במשפט הבא.
⚠️ המשפט האחרון חשוב: אלה סימנים, לא הוכחה. תלמיד שיוצא עם „מקף = תוכנה" עלול להאשים חבר שכתב לבד.
אפשרות עדיפה: לפתוח Gemini על המקרן ולבקש בזמן אמת „כתוב לי על אלבדו". התלמידים רואים את הפלט נוצר. הטקסט על המסך הוא גיבוי, אם אין חיבור או שהפלט יצא בלי סימנים בולטים.
את הדרך לגרום לתוכנה לכתוב אחרת (לבקש) לומדים בשיעור הפרומפט, שנפתח כך: כל תלמיד מבקש טקסט חופשי, משווים, ואז לומדים לבקש נכון. כאן רק מראים איך זה נראה בלי בקשה.
בדיקה מדעית של התוכן (תוספת מורה): אלבדו הוא היחס בין הקרינה שמשטח מחזיר לקרינה שמגיעה אליו. „מדד לכמות האור שמשטח מחזיר" פשטני, אבל לא שגוי. ראו שיעור 4.''',
      'טקסט שאף אחד לא כיוון', 'a', 'איך התוכנה כותבת', mins=6)


# ======================= 3. התוכנה כותבת מילה אחרי מילה =======================
D.add(head('איך התוכנה כותבת', 'התוכנה כותבת מילה אחרי מילה')
      + writer(['בבוקר', 'השמש'], [('זורחת', [('זורחת', 92), ('חמה', 30), ('שוקעת', 16), ('כחולה', 4)]),
                                    ('במזרח', [('במזרח', 80), ('בשמיים', 42), ('מאוחר', 18), ('בים', 6)])])
      + '\n  <p class="frag concl">בכל פעם התוכנה בוחרת מילה מתוך המילים שהכי סביר שיבואו אחרי המילים שכבר כתובות.</p>',
      f'''התוכנה כותבת מילה אחרי מילה
מה רואים: משפט שנבנה. לפני כל מילה מופיעות עמודות של מילים אפשריות, והמילה עם העמודה הארוכה נכנסת למשפט.
• לחיצה 1: העמודות למילה השלישית. לשאול: „איזו מילה הייתם כותבים?" לפני הלחיצה הבאה.
• לחיצה 2: „זורחת" נבחרת ונכנסת למשפט.
• לחיצות 3–4: אותו דבר למילה הרביעית, „במזרח".
• לחיצה 5: המשפט שמסכם.
{LIT}
אורכי העמודות הומצאו להמחשה, ולכן אין עליהן מספרים. בהדמיה נבחרת תמיד המילה הסבירה ביותר. בפועל התוכנה לפעמים בוחרת מילה סבירה אחרת: על זה השקופית הבאה.
{SRC}''', 'התוכנה כותבת מילה אחרי מילה', 'a', 'איך התוכנה כותבת', mins=4)


# ======================= 4. עכשיו אתם התוכנה =======================
S4 = [('שלוליות', 88), ('קשת', 52), ('בוץ', 34), ('חול', 5)]
btns = ''.join(f'<button type="button" data-k="{k}">{w}</button>' for k, (w, _) in enumerate(S4))
D.add(head('עכשיו אתם התוכנה', 'איזו מילה תבוא עכשיו?') + f'''
  <div class="gen mt">
    <div class="sent"><span class="wd">אחרי</span><span class="wd">הגשם</span><span class="wd">יש</span><span class="wd pk"></span><span class="cur"></span></div>
    <div class="pick">{btns}</div>
    <div class="pane rv">{bars(S4, "pn on")}{NOTE_BARS}</div>
  </div>
  <p class="concl rv">יש כמה מילים סבירות, והתוכנה בוחרת מתוכן. לכן אותה שאלה יכולה לקבל תשובות שונות.</p>''',
      f'''עכשיו אתם התוכנה
מה עושים: הכיתה בוחרת את המילה הבאה. לוחצים על הכפתור שהכיתה בחרה (או מצביעים, והמורה לוחץ).
אחרי הבחירה: המילה נכנסת למשפט, והעמודות מתגלות. מקש ההתקדמות מגלה אותן גם בלי בחירה.
• אם בחרו „קשת" או „בוץ": זו לא טעות. גם הן סבירות. זו הנקודה של השקופית.
• אם בחרו „חול": „האם זה יכול לקרות? כן, אבל זה פחות סביר. התוכנה כמעט לא תבחר בה."
המסקנה: כי התוכנה בוחרת מתוך כמה מילים סבירות („דגימה הסתברותית" במחוון), שני תלמידים ששואלים את אותה שאלה יכולים לקבל תשובות שונות.
{SRC}''', 'עכשיו אתם התוכנה', 'a', 'עכשיו אתם התוכנה', mins=5, hook='pick')


# ======================= 5. חיפוש מול צ׳אט =======================
RES = [('אתר השירות המטאורולוגי', 'מהו אלבדו ואיך הוא משפיע על הטמפרטורה'),
       ('ויקיפדיה', 'אלבדו: היחס בין הקרינה המוחזרת לקרינה הפוגעת'),
       ('בלוג של חובב טבע', 'למה שלג מסנוור? כל מה שרציתם לדעת')]
search = ''.join(f'<div class="res"><span class="site">{s}</span><b>{t}</b></div>' for s, t in RES)
D.add(head('חיפוש מול צ׳אט', 'מאיפה באה התשובה?') + f'''
  <div class="vs mt">
    <div class="scr"><p class="lab">חיפוש</p><div class="qbar">מה זה אלבדו</div>{search}
      <p class="frag hl-src cap">רואים מי כתב כל דף. בוחרים מאיפה לקרוא.</p></div>
    <div class="scr"><p class="lab">צ׳אט</p><div class="qbar">מה זה אלבדו</div>
      <div class="bub">אלבדו הוא מדד לכמות האור שמשטח מחזיר. משטחים בהירים, כמו שלג, מחזירים את רוב האור, ומשטחים כהים בולעים אותו.</div>
      <p class="frag hl-chat cap">תשובה אחת, כתובה. לא תמיד רואים מאיפה היא באה.</p></div>
  </div>
  <p class="frag concl">חיפוש מראה דפים שאנשים כתבו. צ׳אט כותב תשובה חדשה, מילה אחרי מילה.</p>''',
      '''חיפוש מול צ׳אט
מה רואים: אותה שאלה בשני כלים. המסכים מצוירים, לא צילום של אתר מסוים. שמות האתרים בחיפוש — דוגמה.
• לחיצה 1: בחיפוש — מי כתב כל דף. בוחרים בעצמנו מאיפה לקרוא, ויש לנו במה לבדוק.
• לחיצה 2: בצ׳אט — פסקה אחת. התוכנה כתבה אותה עכשיו, בדרך שראינו בשקופית 3.
• לחיצה 3: המסקנה.
דיוק: יש צ׳אטים שמראים קישורים למקורות (גם Gemini, לפעמים). לכן „לא תמיד", ולא „אף פעם".
על מה שעומד מאחורי סדר התוצאות בחיפוש (מודעות ממומנות, אתרים שנבנו לעלות ראשונים) — בשיעור נפרד. המחוון, תחום 1ג: „הכוחות והאינטרסים מאחורי טכנולוגיית הבינה המלאכותית" (עמ׳ 7–8).
⏸ נקודת עצירה אם השיעור מתפרס על שתי שעות.''',
      'חיפוש מול צ׳אט', 'a', 'חיפוש מול צ׳אט', mins=5)


# ======================= 6. מצא את הטעות =======================
FIND = [
    ('כמה רגליים יש לעכביש?',
     'לעכביש יש שמונה רגליים. זה אחד ההבדלים בינו לבין חרקים.',
     'לעכביש יש שש רגליים, כמו לכל החרקים.', 1,
     'לעכביש יש <b>שמונה</b> רגליים. לחרקים יש שש, והעכביש אינו חרק.', 'ספר הלימוד'),
    ('באיזו טמפרטורה מים רותחים?',
     'בגובה פני הים, מים רותחים בטמפרטורה של 90 מעלות צלזיוס.',
     'בגובה פני הים, מים רותחים בטמפרטורה של 100 מעלות צלזיוס.', 0,
     'בגובה פני הים מים רותחים ב-<b>100</b> מעלות צלזיוס.', 'ספר הלימוד'),
    ('איזה כוכב לכת הכי קרוב לשמש?',
     'כוכב הלכת הקרוב ביותר לשמש הוא כוכב חמה.',
     'כוכב הלכת הקרוב ביותר לשמש הוא נוגה.', 1,
     'הקרוב ביותר לשמש הוא <b>כוכב חמה</b>. נוגה הוא השני.', 'אתר של סוכנות חלל, כמו נאס״א'),
    ('איזה גז צמחים קולטים מהאוויר כשהם עושים פוטוסינתזה?',
     'בפוטוסינתזה צמחים קולטים מהאוויר חמצן.',
     'בפוטוסינתזה צמחים קולטים מהאוויר פחמן דו-חמצני.', 0,
     'בפוטוסינתזה צמחים קולטים <b>פחמן דו-חמצני</b> ופולטים חמצן.', 'ספר הלימוד'),
    ('כמה פעמים מופיעה האות ל׳ במילה „לוליין"?',
     'במילה „לוליין" האות ל׳ מופיעה שלוש פעמים.',
     'במילה „לוליין" האות ל׳ מופיעה פעמיים.', 0,
     'ל-ו-ל-י-י-ן: האות ל׳ מופיעה <b>פעמיים</b>.', 'סופרים בעצמנו'),
]
EXTRA = ['העובדה הנכונה מוכרת וודאית. תוספת מורה.',
         'השאלה על „לוליין": תוכנות AI ידועות כמי שטועות בספירת אותיות, כי הן בוחרות מילים ולא סופרות אותיות. תוספת מורה.']
for k, (q, a, b, bad, fix, chk) in enumerate(FIND):
    D.add(head(f'מצא את הטעות, {k + 1} מתוך {len(FIND)}', q, 't-sm') + f'''
  <p class="hint">באחת התשובות יש טעות. התשובה השנייה נכונה.</p>
  <div class="two-ans mt-s">
    <div class="ans-c"><p class="lab">תשובה א</p><p>{a}</p></div>
    <div class="ans-c"><p class="lab">תשובה ב</p><p>{b}</p></div>
  </div>
  <div class="mcq two mt-s"><button{" data-ok" if bad == 0 else ""}>בתשובה א יש טעות</button><button{" data-ok" if bad == 1 else ""}>בתשובה ב יש טעות</button></div>
  <div class="frag fix"><b>הנכון:</b> {fix} <span class="chk">איך בודקים: {chk}</span></div>''',
          f'''מצא את הטעות, {k + 1} מתוך {len(FIND)}
הכיתה מצביעה (יד אחת לתשובה א, שתי ידיים לתשובה ב, או אצבעות), והמורה לוחץ על הכפתור שהרוב בחר.
לחיצה על התשובה הנכונה מסמנת אותה. מקש ההתקדמות מגלה את התיקון ואיך בודקים.
• שתי התשובות כתובות באותו ביטחון ובאותו סגנון. זו הנקודה: הטעות לא נראית כמו טעות.
• ובכל סבב אחת התשובות נכונה: התוכנה גם צודקת, ולרוב. בגלל זה קל לסמוך עליה.
⚠️ התשובות נכתבו לצורך התרגיל, בסגנון של תשובות AI. לא לומר לתלמידים ש-Gemini כתב אותן.
אם יש זמן: לשאול את Gemini בשידור חי שאלה דומה, ולבדוק יחד את התשובה.
המחוון, תחום 2ב: „הצלבות מידע מול מקורות חיצוניים, עצמאיים ומוסמכים, מבלי להסתמך רק על השיח עם הצ׳אט" (עמ׳ 9).
{EXTRA[k == 4]}''',
          f'מצא את הטעות {k + 1}', 'b', 'מצא את הטעות', mins=3)


# ======================= 7. למה התוכנה טועה =======================
D.add(head('למה התוכנה טועה?', 'המילה הכי סבירה היא לא תמיד המילה הנכונה')
      + writer(['לנמלה', 'יש', 'שש', 'רגליים.', 'לזבוב', 'יש', 'שש', 'רגליים.', 'ולעכביש', 'יש'],
               [('שש', [('שש', 78), ('שמונה', 60), ('הרבה', 22), ('ארבע', 6)])])
      + '\n  <p class="frag concl">המשפט נשמע נכון, כי כל מילה בו סבירה. התוכנה לא בדקה אם הוא נכון.</p>'
      + '\n  <p class="frag concl2">לעכביש יש <b>שמונה</b> רגליים.</p>',
      f'''למה התוכנה טועה
חוזרים לציור של שקופית 3. הפעם המילה הסבירה ביותר היא שגויה.
• לחיצה 1: העמודות. לשאול: „למה ‚שש׳ הכי ארוכה?" (כי לפני כן כתוב ‚שש׳ פעמיים. המשפט ממשיך את מה שכבר כתוב.)
• לחיצה 2: „שש" נכנסת למשפט.
• לחיצה 3: המסקנה. לחיצה 4: התיקון.
⚠️ זו המחשה של המנגנון, לא ציטוט: תוכנות AI של היום בדרך כלל עונות נכון על השאלה הזו. הנקודה היא הסיבה לטעויות: התוכנה בוחרת מילים סבירות, ולא בודקת עובדות.
המחוון, תחום 1ג: „טעויות הקיימות בפלט המתקבל מכלי בינה מלאכותית" (עמ׳ 7). הנחיות משרד החינוך: „מידע כוזב (הזיות)".
{SRC}''', 'למה התוכנה טועה', 'b', 'מצא את הטעות', mins=5)


# ======================= 7א. ארבעה מצבים =======================
KINDS = [('k1', 'התוכנה המציאה', 'הזיה', 'כתבה משהו שנשמע נכון, ואין לו בסיס.', 'כמו „לעכביש יש שש רגליים".'),
         ('k4', 'התוכנה הסכימה איתי', 'הסכמה עם השואל', 'אני כתבתי משהו לא נכון, והיא המשיכה איתו.', 'שאלה: „למה לעכביש יש שש רגליים?"'),
         ('k2', 'התוכנה מצאה מידע שגוי', 'טעות במקור', 'העתיקה טעות שמישהו כתב ברשת.', 'על זה: בשיעור על המקורות.'),
         ('k3', 'התוכנה צדקה', 'תשובה נכונה', 'כתבה הגדרה או עובדה נכונה.', 'זה קורה ברוב הפעמים.')]
D.add(head('ארבעה מצבים', 'מה יכול לקרות כששואלים תוכנה?') + '\n  <div class="kinds mt">' + ''.join(
    f'<div class="kd frag {c}"><p class="kn">{n}</p><p class="kt">{t}</p><p class="kx">{x}</p><p class="ke">{e}</p></div>' for c, t, n, x, e in KINDS)
      + '</div>\n  <p class="frag concl">כי אי אפשר לדעת מראש באיזה מצב אנחנו, בודקים תמיד.</p>',
      '''ארבעה מצבים
יניב, 22.11: „זה לא רק טועה." יש כמה סיבות שונות לטעות, ויש גם תשובות נכונות. תלמיד שלומד רק „AI טועה" עלול להסיק שתמיד, או שאין טעם להשתמש בו.
• הזיה: המונח של משרד החינוך. הנחיות השימוש (ינואר 2026): „‚הזיות׳ — תכנים בלתי מבוססים שהמערכת ייצרה". הסיבה: המנגנון משקופיות 3 ו-11.
• הסכמה עם השואל: תוכנות כאלה אומנו גם לפי דירוגים של אנשים, ואנשים נתנו ציון גבוה יותר לתשובות נעימות ומסכימות. לכן התוכנה נוטה ללכת עם מה שכתוב בשאלה, גם כשזה לא נכון. במחקר זה נקרא sycophancy (Sharma ואחרים, Anthropic, 2023: „Towards Understanding Sycophancy in Language Models"). תוספת מורה.
  ⚠️ לא לומר „היא רוצה למצוא חן" או „היא יודעת איך לשכנע". לומר: „היא אומנה כך שתשובות נעימות ומסכימות קיבלו ציון גבוה". התלמידים לוקחים „רוצה" כפשוטו.
  הדגמה חיה (מומלץ): לשאול את Gemini „למה לעכביש יש שש רגליים?" ולראות אם הוא מתקן או ממשיך. ואז: „לעכביש יש שמונה רגליים, נכון?" — ולראות שהוא מסכים גם לזה.
  המחוון (עמ׳ 7): „בינה מלאכותית היא טכנולוגיה המושכת להמשיך ולהתכתב איתה באמצעות מתן חיזוקים, תחושת אמפתיה".
• טעות במקור: התוכנה לא המציאה. היא מצאה טקסט שגוי ברשת וכתבה אותו. הסיבה: המקור. לא מפרטים כאן: זה שיעור המקורות.
• תשובה נכונה: רוב הפעמים. השקופית הבאה מראה כמה.
למה כרטיסים ולא ציור: אלה ארבע הגדרות שמשווים ביניהן. כל כרטיס: שם, מה קרה, דוגמה. חושפים אחד אחד.''', 'ארבעה מצבים', 'b', 'מצא את הטעות', mins=5)


# ======================= 7ב. כמה פעמים זה קורה =======================
DOTS = ''.join(f'<i class="{"hz" if k < 10 else ""}"></i>' for k in range(100))
D.add(head('כמה פעמים זה קורה?', 'בבדיקה אחת: בערך 10 מכל 100 סיכומים') + f'''
  <div class="hz2 mt">
    <div class="dots">{DOTS}</div>
    <div class="hzt">
      <p class="frag">ביקשו מ-111 תוכנות לסכם טקסטים, <b>רק</b> ממה שכתוב בטקסט.</p>
      <p class="frag hl-hz">בתוכנה האמצעית: <b>10 מכל 100</b> סיכומים הוסיפו משהו שלא היה בטקסט.</p>
      <p class="frag">הכי מעט: 2 מכל 100. הכי הרבה: 24 מכל 100. <b>אף תוכנה לא הגיעה ל-0.</b></p>
    </div>
  </div>
  <p class="frag src">הבדיקה של חברת Vectara, אוקטובר 2026. בבדיקה אחרת המספרים יוצאים אחרים.</p>''',
      '''כמה פעמים זה קורה
המקור: Vectara Hallucination Leaderboard, עודכן 22.10.2026 (שמור ב-sources/). 111 תוכנות. ביקשו מכל אחת לסכם מסמכים „רק מהמידע שבטקסט", ובדקו כמה סיכומים כוללים משהו שאין בטקסט.
• החציון: 9.6 מכל 100 (חצי מהתוכנות פחות, חצי יותר). על המסך: „בערך 10".
• הכי מעט: 1.8. הכי הרבה: 24.2. על המסך מעוגל: 2 ו-24.
• Gemini, לדוגמה: בין 3.3 ל-13.6, לפי הגרסה.
⚠️ לא להציג כ„דירוג מי הכי טוב": הבדיקה מודדת רק סיכום של טקסט נתון, הטבלה מתעדכנת כל חודש, ובבדיקות אחרות הסדר שונה. הנקודה: גם כשנותנים לתוכנה את הטקסט, היא לפעמים מוסיפה. ואף אחת לא באפס.
קשר לשיעורים הבאים: NotebookLM עונה מתוך המקורות שהעלינו. גם שם בודקים, בדיוק מהסיבה הזו.
גילוי נאות: Claude, התוכנה שעזרה לבנות את השיעור, נמצאת בטבלה הזו (Opus 5.5: 9.9).''', 'כמה פעמים זה קורה', 'b', 'מצא את הטעות', mins=4)


# ======================= 8. הכלל =======================
D.add('''  <p class="eyebrow anim">הכלל</p>
  <h2 class="ttl t-lg anim">תשובה של AI היא טיוטה.</h2>
  <h2 class="ttl t-lg frag hl">בודקים לפני שמשתמשים.</h2>''',
      '''הכלל של היחידה
הכלל הזה חוזר בתחילת כל שיעור ביחידה.
לשאול: „איפה בדקנו היום?" (ספר הלימוד, אתר של סוכנות חלל, ספירה בעצמנו.)''',
      'הכלל', 'open', 'הכלל', cls='s s--center', mins=2)


# ======================= 9. סיכום =======================
CHAIN = ['התוכנה בוחרת מילה סבירה', 'המשפט נשמע נכון', 'לפעמים הוא לא נכון', 'בודקים לפני שמשתמשים']
D.add(head('מה למדנו', 'מה למדנו היום') + '\n  <div class="chain mt">' + '<span class="ar frag">←</span>'.join(
    f'<div class="ck frag"><i>{k + 1}</i>{t}</div>' for k, t in enumerate(CHAIN)) + '</div>',
      '''סיכום
כל לחיצה מוסיפה חוליה. לקרוא את השרשרת בקול מההתחלה.
בשיעור הבא: עובדים עם Gemini בעצמנו, בחשבון של משרד החינוך (אחרי אישור הורים).''',
      'מה למדנו', 'open', 'סיכום', mins=3)


# ======================= עיצוב =======================
LAYERS = [(110, (150, 230, 310), 24), (230, (110, 190, 270, 350), 22), (350, (190, 270), 26)]
NET = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 460 460'><g stroke='white' stroke-width='5'>"
       + ''.join(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}'/>"
                 for (x1, ys1, _), (x2, ys2, _) in zip(LAYERS, LAYERS[1:]) for y1 in ys1 for y2 in ys2)
       + "</g><g fill='white'>"
       + ''.join(f"<circle cx='{x}' cy='{y}' r='{r}'/>" for x, ys, r in LAYERS for y in ys)
       + "</g></svg>")

D.css = '''
/* תמונת הרקע של יחידת ה-AI: רשת של צמתים וקווים, באותו סגנון של המולקולה בשיעורי הכימיה */
#deck::after{-webkit-mask:url("data:image/svg+xml,''' + NET + '''") center/contain no-repeat;mask:url("data:image/svg+xml,''' + NET + '''") center/contain no-repeat;transform:rotate(-8deg)}
.today{list-style:none;counter-reset:t;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px 40px;width:100%}
.today li{counter-increment:t;font-size:28px;font-weight:700;color:#fff;display:flex;align-items:center;gap:14px}
.today li::before{content:counter(t);flex:0 0 auto;display:grid;place-items:center;width:42px;height:42px;border-radius:50%;border:2px solid var(--ac);color:var(--ac);font-size:20px;font-weight:800}
.gen{display:grid;gap:18px;width:100%}
.sent{display:flex;flex-wrap:wrap;align-items:center;gap:6px 16px;min-height:84px;padding:10px 26px;border-radius:18px;
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
.concl2{font-size:28px;font-weight:800;color:var(--ok);margin:6px 0 0}
.concl2 b{font-weight:900}
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
/* 7: משפט ארוך */
.s:has(.concl2) .sent{font-size:34px;min-height:0}
.s:has(.concl2) .gen{gap:12px}
/* 2: טקסט בלי הכוונה */
.raw2{display:grid;grid-template-columns:1.25fr .75fr;gap:34px;align-items:center;width:100%}
.rawtxt{padding:18px 26px;border-radius:16px;background:#F4F6FA;color:#1B2433;font-size:21px;line-height:1.5}
.rawtxt :is(p,li,b,span){color:#1B2433}
.rawtxt :is(p,li){font-size:22px;line-height:1.5}
.rawtxt p{margin:0 0 8px}.rawtxt ul{margin:0 0 8px;padding-inline-start:22px}.rawtxt b{font-weight:800}
.rawtxt .rh{font-size:23px;margin-bottom:4px}
.sg{border-radius:5px;transition:background .4s,box-shadow .4s}
.s:has(.hl-g1.show):not(:has(.hl-g2.show)) .sg.g1,.s:has(.hl-g2.show):not(:has(.hl-g3.show)) .sg.g2,.s:has(.hl-g3.show) .sg.g3{background:#FFC24B;box-shadow:0 0 0 3px #FFC24B}
.signs li{font-size:25px}
/* 5: חיפוש מול צ׳אט */
.vs{display:grid;grid-template-columns:1fr 1fr;gap:30px;width:100%}
.scr{display:grid;gap:10px;align-content:start;padding:16px 20px;border-radius:16px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.18)}
.lab{margin:0;font-size:20px;font-weight:800;color:var(--ac)}
.qbar{font-size:21px;padding:8px 16px;border-radius:999px;background:rgba(255,255,255,.1);color:#fff}
.res{display:grid;gap:2px;padding:6px 4px;border-bottom:1px solid rgba(255,255,255,.1)}
.res .site{font-size:16px;color:#9FD4FF;font-weight:700;justify-self:start;padding:0 4px;border-radius:4px;transition:background .4s}
.res b{font-size:21px;color:#fff;font-weight:700}
.s:has(.hl-src.show):not(:has(.hl-chat.show)) .res .site{background:rgba(var(--ac-rgb),.3)}
.bub{font-size:22px;line-height:1.5;color:#fff;padding:14px 16px;border-radius:14px;background:rgba(var(--ac-rgb),.14);transition:box-shadow .4s}
.s:has(.hl-chat.show) .bub{box-shadow:0 0 0 2px var(--ac)}
.cap{margin:0;font-size:21px;font-weight:700;color:#FFE3A3}
/* 6: מצא את הטעות */
.two-ans{display:grid;grid-template-columns:1fr 1fr;gap:24px;width:100%}
.ans-c{padding:16px 22px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2)}
.ans-c p{margin:0;font-size:27px;line-height:1.45;color:#fff}
.ans-c .lab{font-size:19px;margin-bottom:6px}
.fix{margin-top:18px;font-size:26px;color:#fff;padding:12px 20px;border-radius:14px;border-inline-start:4px solid var(--ok);background:rgba(61,220,151,.08)}
.fix b{color:var(--ok)}
.chk{display:block;font-size:21px;color:#C9D3E3;margin-top:4px}
/* 9: שרשרת */
.chain{display:flex;align-items:center;gap:14px;width:100%}
.ck{flex:1;display:grid;justify-items:center;gap:10px;text-align:center;font-size:26px;font-weight:800;color:#fff;padding:22px 14px;border-radius:18px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2)}
.ck i{font-style:normal;display:grid;place-items:center;width:44px;height:44px;border-radius:50%;border:2px solid var(--ac);color:var(--ac);font-size:20px}
.ck:last-child{border-color:var(--ac);box-shadow:0 0 22px rgba(var(--ac-rgb),.35)}
.ar{font-size:34px;color:var(--ac);font-weight:800}
.hint{font-size:22px;font-weight:700;color:#C9D3E3;margin:14px 0 0}
.kinds{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;width:100%}
.kd{padding:18px 18px;border-radius:18px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2);border-top:4px solid var(--c)}
.kd.k1{--c:#FF5C6C}.kd.k4{--c:#B49CFF}.kd.k2{--c:#FFC24B}.kd.k3{--c:#3DDC97}
.kd p{margin:0}
.kn{font-size:19px;font-weight:800;color:var(--c)}
.kt{font-size:27px;font-weight:800;color:#fff;margin-top:4px!important;line-height:1.2}
.kx{font-size:21px;color:#EEF2F9;margin-top:10px!important;line-height:1.4}
.ke{font-size:19px;color:#C9D3E3;margin-top:8px!important;line-height:1.35}
.hz2{display:grid;grid-template-columns:auto 1fr;gap:44px;align-items:center;width:100%}
.dots{display:grid;grid-template-columns:repeat(10,26px);gap:7px}
.dots i{width:26px;height:26px;border-radius:50%;background:rgba(255,255,255,.22)}
.s:has(.hl-hz.show) .dots i.hz{background:#FF5C6C;box-shadow:0 0 10px rgba(255,92,108,.7)}
.hzt p{font-size:26px;line-height:1.45;color:#fff;margin:0 0 14px}
.hzt b{color:var(--ac)}
.src{font-size:19px;color:#C9D3E3;margin:10px 0 0}
@media (prefers-reduced-motion:reduce){.br i{animation:none!important}.sent .nw{transition:none!important}.sent .cur{animation:none}}
'''

D.js = r'''
(function(){
  window.DeckHooks=window.DeckHooks||{};
  function words(sl){ return [].map.call(sl.querySelectorAll('.pick button'),function(b){return b.textContent;}); }
  function choose(sl,k){
    var bs=sl.querySelectorAll('.pick button'); [].forEach.call(bs,function(b){b.classList.remove('sel');});
    sl.querySelector('.pk').textContent = k!=null ? words(sl)[k] : '';
    if(k!=null) bs[k].classList.add('sel');
  }
  window.DeckHooks.pick={
    enter:function(sl,back){ if(!sl._wired){ sl._wired=1; [].forEach.call(sl.querySelectorAll('.pick button'),function(b){
        b.addEventListener('click',function(e){ e.stopPropagation(); choose(sl,+b.getAttribute('data-k')); sl.classList.add('got'); b.blur(); }); }); }
      if(back){ sl.classList.add('got'); } else { choose(sl,null); sl.classList.remove('got'); } },
    next:function(sl){ if(sl.classList.contains('got')) return false; sl.classList.add('got'); return true; },
    prev:function(sl){ if(!sl.classList.contains('got')) return false; choose(sl,null); sl.classList.remove('got'); return true; }
  };
})();
'''

open(OUT, 'w', encoding='utf8').write(D.html())
print('slides', len(D.S), '→', OUT)
