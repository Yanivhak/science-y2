# מחולל: שיעור AI 1 לפי מסמך האב, „מהי בינה מלאכותית ומה היא מסוגלת לעשות?" (23.11.2026).
# מנוע: tools/deck (העיצוב של ט3, שיעורים 7–8). שימוש: python3 tools/gen_ai01_deck.py [קובץ פלט]
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deck'))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from kit import Deck
import phone_deck   # מצב טלפון (?phone=1, או טלפון אמיתי): מועתק מ-lesson-plans-2026, ענף claude/gifted-faraday-i1uxrr

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = sys.argv[1] if len(sys.argv) > 1 else ROOT + '/lessons/AI-01-מהי-בינה-מלאכותית.html'

META = ('שיעור AI 1 לפי מסמך האב: מהי בינה מלאכותית ומה היא מסוגלת לעשות. '
        'מטרה: התלמידים יכירו בינה מלאכותית יוצרת, יבינו במה היא שונה מתוכנה רגילה, ויזהו שימושים משמעותיים שלה. '
        'בדיקת הבנה: התלמיד מסביר במה שונה מודל שפה ממאגר תשובות מוכנות, ונותן דוגמה לשימוש מועיל. '
        'ציוד: מקרן, Gemini פתוח בחשבון המורה. התנסות התלמידים: רק אחרי אישור הורים.')
D = Deck('בינה מלאכותית, שיעור 1: מה היא ומה היא יודעת לעשות', 'מבוא למדעים, י2, בינה מלאכותית, שיעור 1', META)

SRC = ('מקורות: מחוון כשירויות בינה מלאכותית 2.0, על-יסודי, משרד החינוך (sources/), עמ׳ 6, תחום 1א: '
       '„כיצד פועלים כלי בינה מלאכותית… חיזוי המילה הבאה בטקסט", „מהם מקורות המידע שלהם? אימון מודל, מאגרי מידע, רשת", '
       '„מודלי שפה אינם ‚מבינים׳ את המידע כמו בני אדם". Google, Machine Learning Crash Course, „Introduction to Large Language Models".')


def head(eyebrow, title, size='t-md'):
    return f'  <p class="eyebrow anim">{eyebrow}</p>\n  <h2 class="ttl {size} anim">{title}</h2>'


# ======================= 1. מה נעשה היום =======================
PLAN = ['מה Gemini יודע לעשות', 'תוכנה רגילה מול תוכנה שלמדה', 'מאגר תשובות או מודל שפה?', 'התוכנה היא לא אדם',
        'למה כדאי להשתמש בה', 'אתם מנסים']
D.add('  <p class="eyebrow anim">בינה מלאכותית, שיעור 1</p>\n  <h2 class="ttl t-lg anim">מהי בינה מלאכותית,<br>ומה היא יודעת לעשות?</h2>'
      + '\n  <ol class="today mt">' + ''.join(f'<li class="frag">{x}</li>' for x in PLAN) + '</ol>',
      '''מה נעשה היום
זמן מתוכנן: כ-55 דקות. בשיעור של 45 דקות: עצירה אחרי „התוכנה היא לא אדם", וההמשך (מיון, אתם מנסים, סיכום) בשיעור הבא. לא לקצר את „אתם מנסים".
כל לחיצה מגלה שלב. לקרוא בקול. מבנה קבוע בכל שיעור.
זה השיעור הראשון ביחידה. בהמשך כל תלמיד יבנה בעזרת בינה מלאכותית עבודה מדעית על נושא שבחר.''',
      'מה נעשה היום', 'open', 'פתיחה', mins=2)


# ======================= 2. הדגמה חיה =======================
DEMOS = [('✍️', 'הסבר', 'הסבר לי בשלושה משפטים למה השמיים כחולים.'),
         ('🖼️', 'תמונה', 'צור תמונה של תא בעל חיים, עם שמות החלקים.'),
         ('❓', 'בוחן', 'בנה לי בוחן של שלוש שאלות על מערכת הדם.'),
         ('📅', 'תכנון', 'תכנן לי לוח זמנים ללמידה למבחן שיש לי בעוד שבוע.')]
D.add(head('הדגמה, על המקרן', 'מה Gemini יודע לעשות?') + '\n  <div class="demos mt">' + ''.join(
    f'<div class="dm frag"><span class="di">{i}</span><b>{t}</b><p>„{p}"</p></div>' for i, t, p in DEMOS)
      + '</div>\n  <p class="frag concl">מה דומה בכל ארבע הבקשות? ומה שונה?</p>',
      '''הדגמה חיה: מה Gemini יודע לעשות
המורה מקליד כל בקשה ב-Gemini על המקרן (חשבון המורה). כל לחיצה מגלה בקשה. אחרי כל בקשה מראים את התשובה של Gemini.
• הסבר: טקסט. • תמונה: יצירת תמונה זמינה גם לתלמידים מתחת לגיל 18 (Google, 20.10.2026). אם בתמונה יש שגיאה בשמות החלקים — מצוין. לשמור אותה לשיעור על תמונות.
• בוחן ותכנון: Gemini מחזיר מבנה, לא רק פסקה.
השאלה בסוף („מה דומה ומה שונה?"): התשובה בשקופית הבאה. לתת לתלמידים לענות קודם.
אם אין חיבור: לספר מה Gemini היה עושה, ולהמשיך.''',
      'מה Gemini יודע לעשות', 'a', 'מה Gemini יודע לעשות', mins=10)


# ======================= 3. מה משותף =======================
D.add(head('מה דומה?', 'בכל הבקשות: כותבים מילים, ומקבלים משהו חדש') + '''
  <div class="flow mt">
    <div class="fl frag"><span class="fi">⌨️</span><b>כתבתי בקשה</b><p>במילים רגילות</p></div>
    <span class="far frag">←</span>
    <div class="fl frag hot"><span class="fi">⚙️</span><b>התוכנה יצרה</b><p>תשובה שלא הייתה קיימת קודם</p></div>
    <span class="far frag">←</span>
    <div class="fl frag"><span class="fi">📄</span><b>קיבלתי</b><p>טקסט, תמונה, בוחן או תוכנית</p></div>
  </div>
  <p class="frag concl">לכן קוראים לזה <em>בינה מלאכותית יוצרת</em>: היא יוצרת משהו חדש.</p>''',
      '''מה משותף לכל הבקשות
התשובה לשאלה מהשקופית הקודמת. כל לחיצה מוסיפה שלב.
המונח: „בינה מלאכותית יוצרת" (Generative AI). זה המונח של משרד החינוך („הנחיות שימוש בכלי בינה מלאכותית יוצרת", ינואר 2026).
ההבדל בין הבקשות: סוג התוצר (טקסט, תמונה, בוחן). הדמיון: אותה דרך עבודה.''',
      'בינה מלאכותית יוצרת', 'a', 'מה Gemini יודע לעשות', mins=3)


# ======================= 4. תוכנה רגילה מול תוכנה שלמדה =======================
D.add(head('איך תוכנה יודעת מה לעשות?', 'תוכנה רגילה מול תוכנה שלמדה') + '''
  <div class="vs2 mt">
    <div class="side frag hl-rule">
      <p class="lab">תוכנה רגילה, כמו מחשבון</p>
      <div class="code"><span>אם לחצו <b>+</b></span><span>חבר את שני המספרים</span></div>
      <p class="cap">פועלת לפי כללים שאנשים הגדירו מראש.<br>אותה בקשה, תמיד אותה תשובה.</p>
    </div>
    <div class="side frag hl-learn">
      <p class="lab">בינה מלאכותית</p>
      <div class="train"><div class="docs">''' + ''.join(f'<i style="--d:{k * .35}s"></i>' for k in range(8)) + '''</div>
        <svg class="netm" viewBox="0 0 160 120">''' + ''.join(
          f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}"/>' for (x1, a), (x2, b) in [((20, (20, 60, 100)), (80, (10, 45, 75, 110))), ((80, (10, 45, 75, 110)), (140, (40, 80)))] for y1 in a for y2 in b) + ''.join(
          f'<circle cx="{x}" cy="{y}" r="7"/>' for x, ys in [(20, (20, 60, 100)), (80, (10, 45, 75, 110)), (140, (40, 80))] for y in ys) + '''</svg></div>
      <p class="cap">למדה דפוסים מתוך כמות עצומה של טקסטים שאנשים כתבו.<br>אף אחד לא כתב לה את התשובות.</p>
    </div>
  </div>
  <p class="frag concl">לתהליך הזה קוראים <em>אימון</em>: התוכנה לומדת דפוסים מתוך דוגמאות.</p>''',
      f'''תוכנה רגילה מול תוכנה שלמדה
לחיצה 1: תוכנה רגילה, שפועלת לפי כללים שהוגדרו מראש. לחיצה 2: בינה מלאכותית. טקסטים „נכנסים" לרשת, והרשת נדלקת. לחיצה 3: המונח „אימון".
להדגיש: במחשבון, 2+2 תמיד 4. ב-Gemini, אותה שאלה יכולה לקבל תשובה אחרת. למה — בשיעור הבא.
„כמות עצומה": לא נותנים מספר. בשיעור הבא מסבירים מה בדיוק היא לומדת.
דיוק: גם תוכנות רגילות יכולות להיות מורכבות מאוד, ולא כל מערכות ה-AI פועלות אותו דבר. ההבחנה כאן: כללים שהוגדרו מראש, מול דפוסים שנלמדו מנתונים.
{SRC}''', 'תוכנה רגילה מול תוכנה שלמדה', 'a', 'תוכנה רגילה מול תוכנה שלמדה', mins=5)


# ======================= 5. מאגר תשובות או מודל שפה (אינטראקטיבי) =======================
D.add(head('מה קורה בפנים?', 'מאגר תשובות, או מודל שפה?') + '''
  <div class="cab mt">
    <div class="qq"><span class="frag hl-q1">שאלה: <b>מה בירת צרפת?</b></span><span class="frag hl-q2">שאלה חדשה: <b>תסביר לי את הגשם כאילו אני בן 8</b></span></div>
    <div class="vs2">
      <div class="side">
        <p class="lab">מאגר תשובות מוכנות</p>
        <div class="drawer"><span>מה בירת צרפת? ← פריז</span><span>כמה זה 2+2? ← 4</span><span>מתי נוסדה המדינה? ← 1948</span></div>
        <p class="ans a1">פריז ✔<br><small>מצאתי את התשובה במגירה.</small></p>
        <p class="ans a2 no">אין לי תשובה כזו ✗<br><small>היא לא במגירה.</small></p>
      </div>
      <div class="side">
        <p class="lab">מודל שפה</p>
        <div class="writer"><span class="w1">פריז היא בירת צרפת.</span><span class="w2">כשהשמש מחממת מים, הם עולים לשמיים והופכים לעננים. כשבענן יש הרבה מים, הם נופלים בחזרה. זה הגשם.</span></div>
        <p class="ans b1">כתב תשובה ✔</p>
        <p class="ans b2">כתב תשובה חדשה ✔<br><small>אף אחד לא כתב אותה קודם.</small></p>
      </div>
    </div>
  </div>
  <p class="frag concl">מודל שפה לא שולף תשובה מוכנה ממגירה. הוא כותב אותה.</p>
  <p class="frag concl2">לפעמים הוא גם מחפש ברשת, ואז כותב תשובה מתוך מה שמצא. על זה, בשיעור הבא.</p>''',
      f'''מאגר תשובות או מודל שפה
לחיצה 1: שאלה רגילה. שניהם עונים. לחיצה 2: שאלה חדשה. המאגר לא מוצא; המודל כותב. לחיצה 3: המסקנה.
לשאול לפני לחיצה 2: „מה יקרה כשנשאל משהו שאף אחד לא שאל קודם?"
זו נקודת בדיקת ההבנה של השיעור (מסמך האב): „במה שונה מודל שפה ממאגר תשובות מוכנות?"
הכנה לשיעור הבא: כי המודל כותב ולא מעתיק, הוא יכול גם לכתוב משהו שלא נכון. לא לפתח עכשיו.
התשובה על הגשם היא פישוט שנכתב לילד בן 8. היא נכונה בעיקרה.
{SRC}''', 'מאגר תשובות או מודל שפה', 'a', 'מאגר תשובות או מודל שפה', mins=5)


# ======================= 6. התוכנה היא לא אדם (הומור) =======================
def person_svg():
    return ('<svg viewBox="0 0 200 230" width="190"><circle cx="100" cy="52" r="34" fill="#FFD7A8"/>'
            '<circle cx="88" cy="48" r="4" fill="#1B2433"/><circle cx="112" cy="48" r="4" fill="#1B2433"/>'
            '<path d="M86 64 Q100 76 114 64" stroke="#1B2433" stroke-width="4" fill="none" stroke-linecap="round"/>'
            '<rect x="56" y="94" width="88" height="96" rx="30" fill="#5AA9E6"/>'
            '<rect x="66" y="186" width="22" height="40" rx="9" fill="#1B3050"/><rect x="112" y="186" width="22" height="40" rx="9" fill="#1B3050"/></svg>')
def computer_svg():
    rows = ''.join(f'<rect x="{34 + (k % 2) * 14}" y="{44 + k * 22}" width="{96 - (k % 3) * 18}" height="10" rx="5" fill="#8EC5FF" opacity=".85"/>' for k in range(5))
    return ('<svg viewBox="0 0 200 230" width="190"><rect x="18" y="24" width="164" height="136" rx="14" fill="#1B3050" stroke="#8EC5FF" stroke-width="4"/>'
            + rows + '<rect x="146" y="132" width="6" height="16" fill="#8EC5FF"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>'
            '<rect x="70" y="160" width="60" height="22" fill="#1B3050"/><rect x="40" y="182" width="120" height="14" rx="7" fill="#1B3050" stroke="#8EC5FF" stroke-width="3"/></svg>')
ROWS_NP = [('אוכל פלאפל', True, False), ('ישן בלילה', True, False), ('יש לו גוף', True, False), ('מנהל שיחה', True, True)]
rows_np = ''.join(f'<div class="np-r frag"><span class="np-t">{t}</span><span class="np-m {"y" if a else "n"}">{"✓" if a else "✗"}</span><span class="np-m {"y" if b else "n"}">{"✓" if b else "✗"}</span></div>' for t, a, b in ROWS_NP)
D.add(head('רגע, מי זה?', 'התוכנה היא לא אדם') + f'''
  <div class="np mt">
    <div class="np-h"><span></span><span class="np-fig">{person_svg()}<b>אדם</b></span><span class="np-fig">{computer_svg()}<b>תוכנה</b></span></div>
    {rows_np}
  </div>
  <p class="frag concl">התוכנה כותבת כמו אדם, כי היא למדה מטקסטים שאנשים כתבו. זה לא הופך אותה לאדם.</p>''',
      f'''התוכנה היא לא אדם
שקופית קלה, עם הומור. לשאול לפני כל שורה: „מי מהשניים עושה את זה?"
• מנהל שיחה: שניהם. בגלל זה קל לשכוח שמדברים עם תוכנה.
• אם תלמיד שואל „יש לה רגשות?": „העובדה שהיא כותבת כמו אדם לא מוכיחה שיש לה רגשות כמו לאדם. מדענים עדיין מתווכחים על זה." לא לקבוע „אין לה רגשות" כעובדה מוכרעת.
  (בשורות בטבלה בכוונה רק דברים שאפשר לבדוק: אוכל, שינה, גוף.)
⚠️ ההומור מילולי: כל שורה נכונה כפשוטה.
מסמך האב, שיעור 1: „מדוע אין להסיק מהיכולת לנהל שיחה שהמערכת היא אדם?"
{SRC}''', 'התוכנה היא לא אדם', 'b', 'התוכנה היא לא אדם', mins=3)


# ======================= 7. למה כדאי להשתמש בה (מיון) =======================
TASKS = [('להבין מושג במדעים שלא הבנתי בשיעור', 'ok', 'מתאים. ואם משהו נשמע מוזר, בודקים.'),
         ('לתכנן לוח זמנים ללמידה למבחן', 'ok', 'מתאים. ההחלטה מה ללמוד נשארת שלי.'),
         ('להגיש עבודה שהיא כתבה ואני לא הבנתי', 'no', 'לא. היא יודעת לכתוב עבודה. הבעיה: אני מגיש משהו שלא למדתי ולא הבנתי.'),
         ('לבדוק אם מותר לקחת שתי תרופות ביחד', 'chk', 'אפשר לשאול, אבל ההחלטה עם רוקח או רופא.'),
         ('לנסח הודעה למורה שאני חולה', 'ok', 'מתאים. קוראים לפני ששולחים.')]
cards = ''.join(f'<div class="tk frag {c}"><b>{t}</b><span class="tv">{v}</span></div>' for t, c, v in TASKS)
D.add(head('מתי כן ומתי לא?', 'למה כדאי להשתמש בה?') + f'''
  <div class="tasks mt">{cards}</div>
  <div class="legend mt-s"><span class="ok">מתאים</span><span class="chk">אפשר, ובודקים עם אדם</span><span class="no">לא מתאים</span></div>''',
      '''למה כדאי להשתמש בה
כל לחיצה מגלה משימה. לשאול קודם: „מתאים, לא מתאים, או צריך לבדוק עם מישהו?" ורק אז לחשוף (הצבע והמשפט מופיעים יחד עם המשימה; אפשר לכסות ביד).
העבודה: הבעיה אינה שהכלי יודע לכתוב, אלא הגשה של תוצר שהתלמיד לא למד ולא הבין (מחוון, תחום 4ג: גילוי נאות).
מסמך האב, שיעור 1: „אילו משימות מתאימות לשימוש בבינה מלאכותית?" ושיעור 6 (מתי נדרשת התייעצות אנושית) — כאן רק טעימה.
תרופות: מחוון משרד החינוך, „ייעוץ בתחומים רגישים". ההנחיות: „בינה מלאכותית אינה יכולה להחליף היוועצות עם מבוגר משמעותי".''',
      'למה כדאי להשתמש בה', 'b', 'למה כדאי להשתמש בה', mins=5)


# ======================= 8. אתם מנסים =======================
STEPS = ['פתחו את Gemini בחשבון של בית הספר.', 'בחרו תופעה מדעית שאתם לא מבינים.', 'בקשו מ-Gemini להסביר לכם אותה.',
         'כתבו במחברת: מה הבנתי, ודבר אחד שהייתי רוצה לבדוק.', 'כתבו: איך אדע אם ההסבר שקיבלתי נכון?']
IDEAS = ['למה הים מלוח?', 'איך עובד חיסון?', 'למה יש עונות בשנה?', 'איך מטוס נשאר באוויר?']
D.add(head('עבודה אישית, 15 דקות', 'אתם מנסים') + '''
  <div class="task mt">
    <ol class="steps">''' + ''.join(f'<li class="frag">{t}</li>' for t in STEPS) + '''</ol>
    <div class="qlist frag"><p class="lab">אם אין לכם רעיון</p>''' + ''.join(f'<p>{q}</p>' for q in IDEAS) + '''
      <p class="pr">דוגמה לבקשה:<br>„הסבר לי למה הים מלוח. אני בכיתה י׳."</p></div>
  </div>''',
      '''אתם מנסים
עבודה אישית, כל תלמיד על מכשיר, Gemini בחשבון של משרד החינוך. משימה משמעותית: תופעה שהתלמיד באמת לא מבין.
⚠️ רק אחרי אישור הורים (הנחיות משרד החינוך, ינואר 2026). בלי אישור: התלמיד בוחר תופעה, המורה מקליד אותה ב-Gemini על המקרן, והתלמיד כותב במחברת.
• „אני בכיתה י׳": מראה שאפשר לבקש הסבר ברמה שמתאימה. בלי להרחיב — פרומפטים בשיעור 8.
• „דבר אחד שהייתי רוצה לבדוק" ו„איך אדע אם ההסבר נכון?": מעוררים חשיבה ביקורתית ומכינים את שיעור 3. רק לכתוב, לא לבדוק מקורות עכשיו. לשמוע 2–3 תשובות בקול.
• מעבר בין התלמידים: מי שנתקע בבחירה — אחת מהרשימה.''',
      'אתם מנסים', 'b', 'אתם מנסים', mins=15)


# ======================= 9. בדיקת הבנה + סיכום =======================
D.add(head('לפני שיוצאים', 'הסבירו במילים שלכם') + '''
  <div class="chk2 mt">
    <div class="cq frag"><i>1</i><p>במה שונה מודל שפה ממאגר תשובות מוכנות?</p><span class="ca">מאגר מחפש תשובה שמישהו כתב. מודל שפה כותב תשובה חדשה.</span></div>
    <div class="cq frag"><i>2</i><p>תנו דוגמה לשימוש מועיל בבינה מלאכותית.</p><span class="ca">למשל: להסביר לי מושג שלא הבנתי.</span></div>
  </div>
  <p class="frag concl">בינה מלאכותית יכולה לעזור הרבה בלמידה. כדי להשתמש בה נכון, צריך להבין איך היא עובדת. על זה, בשיעור הבא.</p>''',
      '''בדיקת הבנה וסיכום
בדיקת ההבנה ממסמך האב. כל תלמיד עונה בקול או במחברת, ורק אז חושפים תשובה לדוגמה (לחיצה על השאלה מגלה גם את התשובה; אפשר לשאול לפני הלחיצה).
המסר המרכזי (מסמך האב): בינה מלאכותית יכולה לבצע משימות מורכבות ולסייע בלמידה, אך יש להבין כיצד היא פועלת כדי להשתמש בה נכון.
השיעור הבא: איך היא מייצרת תשובה.''',
      'סיכום', 'open', 'סיכום', mins=5)


# ======================= עיצוב =======================
LAYERS = [(110, (150, 230, 310), 24), (230, (110, 190, 270, 350), 22), (350, (190, 270), 26)]
NET = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 460 460'><g stroke='white' stroke-width='5'>"
       + ''.join(f"<line x1='{x1}' y1='{y1}' x2='{x2}' y2='{y2}'/>"
                 for (x1, ys1, _), (x2, ys2, _) in zip(LAYERS, LAYERS[1:]) for y1 in ys1 for y2 in ys2)
       + "</g><g fill='white'>"
       + ''.join(f"<circle cx='{x}' cy='{y}' r='{r}'/>" for x, ys, r in LAYERS for y in ys)
       + "</g></svg>")

D.css = '''
#deck::after{-webkit-mask:url("data:image/svg+xml,''' + NET + '''") center/contain no-repeat;mask:url("data:image/svg+xml,''' + NET + '''") center/contain no-repeat;transform:rotate(-8deg)}
.today{list-style:none;counter-reset:t;padding:0;margin:0;display:grid;grid-template-columns:1fr 1fr;gap:10px 40px;width:100%}
.today li{counter-increment:t;font-size:28px;font-weight:700;color:#fff;display:flex;align-items:center;gap:14px}
.today li::before{content:counter(t);flex:0 0 auto;display:grid;place-items:center;width:42px;height:42px;border-radius:50%;border:2px solid var(--ac);color:var(--ac);font-size:20px;font-weight:800}
.concl{font-size:28px;font-weight:700;color:#fff;margin:22px 0 0}
.concl em{font-style:normal;color:var(--ac)}
.concl2{font-size:23px;font-weight:600;color:#C9D3E3;margin:6px 0 0}
.lab{margin:0;font-size:20px;font-weight:800;color:var(--ac)}
/* 2 */
.demos{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;width:100%}
.dm{padding:18px;border-radius:18px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2);display:grid;gap:8px;align-content:start}
.dm .di{font-size:40px}.dm b{font-size:26px;color:var(--ac)}.dm p{margin:0;font-size:21px;color:#fff;line-height:1.4}
/* 3 */
.flow{display:flex;align-items:stretch;gap:14px;width:100%}
.fl{flex:1;display:grid;justify-items:center;gap:6px;text-align:center;padding:22px 16px;border-radius:18px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2)}
.fl .fi{font-size:44px}.fl b{font-size:27px;color:#fff}.fl p{margin:0;font-size:21px;color:#C9D3E3}
.fl.hot{border-color:var(--ac);box-shadow:0 0 24px rgba(var(--ac-rgb),.35)}
.far{align-self:center;font-size:36px;font-weight:800;color:var(--ac)}
/* 4, 5 */
.vs2{display:grid;grid-template-columns:1fr 1fr;gap:28px;width:100%}
.side{display:grid;gap:12px;align-content:start;padding:18px 22px;border-radius:18px;background:rgba(255,255,255,.05);border:1px solid rgba(255,255,255,.18)}
.cap{margin:0;font-size:22px;color:#fff;line-height:1.45}
.code{display:grid;gap:6px;font-family:inherit;font-weight:700;direction:rtl;font-size:24px;color:#9FD4FF;padding:14px 18px;border-radius:12px;background:#0B1424}
.code b{color:#FFC24B}
.train{position:relative;display:flex;align-items:center;gap:10px;height:130px}
.docs{position:relative;width:120px;height:120px}
.docs i{position:absolute;right:0;top:calc(var(--d) * 26px);width:44px;height:12px;border-radius:4px;background:#C9D3E3;opacity:0}
.s.on:has(.hl-learn.show) .docs i{animation:fly 2.8s var(--d) ease-in infinite}
@keyframes fly{0%{opacity:0;transform:translateX(0)}15%{opacity:1}80%{opacity:.9;transform:translateX(-90px) scale(.5)}100%{opacity:0;transform:translateX(-110px) scale(.3)}}
.netm{width:170px;height:auto}
.netm line{stroke:rgba(255,255,255,.25);stroke-width:2}
.netm circle{fill:#5B6B80;transition:fill .6s}
.s.on:has(.hl-learn.show) .netm circle{animation:glow 1.6s ease-in-out infinite}
.s.on:has(.hl-learn.show) .netm circle:nth-of-type(3n){animation-delay:.5s}
.s.on:has(.hl-learn.show) .netm circle:nth-of-type(3n+1){animation-delay:1s}
@keyframes glow{0%,100%{fill:#5B6B80}50%{fill:var(--ac)}}
.qq{display:grid;min-height:46px;font-size:28px;color:#fff;margin-bottom:12px}
.qq>span{grid-area:1/1}
.qq b{color:var(--ac)}
.s:has(.hl-q2.show) .qq .hl-q1{opacity:0}
.drawer{display:grid;gap:6px}
.drawer span{font-size:19px;color:#1B2433;background:#F4F6FA;border-radius:8px;padding:6px 12px}
.writer{display:grid;min-height:96px}
.writer span{grid-area:1/1;font-size:21px;line-height:1.45;color:#fff;opacity:0;transition:opacity .6s}
.ans{margin:0;font-size:24px;font-weight:800;color:var(--ok);opacity:0;display:none}
.ans.no{color:var(--no)}
.ans small{font-size:18px;font-weight:600;color:#C9D3E3}
.s:has(.hl-q1.show):not(:has(.hl-q2.show)) :is(.a1,.b1){display:block;opacity:1}
.s:has(.hl-q2.show) :is(.a2,.b2){display:block;opacity:1}
.s:has(.hl-q1.show):not(:has(.hl-q2.show)) .w1,.s:has(.hl-q2.show) .w2{opacity:1}
/* 6 */
.np{display:grid;gap:4px;width:100%;max-width:880px;margin-inline:auto}
.np-fig svg{width:100px!important}
.np-h,.np-r{display:grid;grid-template-columns:1fr 200px 200px;align-items:center;gap:10px}
.np-fig{display:grid;justify-items:center;gap:2px}
.np-fig svg{width:120px;height:auto}
.np-fig b{font-size:24px;color:#fff;font-weight:800}
.np-t{font-size:28px;font-weight:700;color:#fff}
.np-m{justify-self:center;font-size:36px;font-weight:900}
.np-m.y{color:#3DDC97}.np-m.n{color:#FF5C6C}
.np-r{padding:6px 0;border-top:1px solid rgba(255,255,255,.12)}
/* 7 */
.tasks{display:grid;grid-template-columns:repeat(5,1fr);gap:14px;width:100%}
.tk{display:grid;gap:10px;align-content:start;padding:16px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2);border-top:5px solid var(--c)}
.tk.ok{--c:#3DDC97}.tk.chk{--c:#FFC24B}.tk.no{--c:#FF5C6C}
.tk b{font-size:22px;color:#fff;line-height:1.35}
.tv{font-size:18px;color:var(--c);font-weight:700;line-height:1.35}
.legend{display:flex;gap:26px;font-size:19px;font-weight:700}
.legend span::before{content:'';display:inline-block;width:14px;height:14px;border-radius:50%;margin-inline-end:8px;vertical-align:middle;background:var(--c)}
.legend .ok{--c:#3DDC97;color:#3DDC97}.legend .chk{--c:#FFC24B;color:#FFC24B}.legend .no{--c:#FF5C6C;color:#FF5C6C}
/* 8 */
.task{display:grid;grid-template-columns:1.1fr .9fr;gap:34px;align-items:start;width:100%}
.steps{margin:0;padding-inline-start:34px;display:grid;gap:12px}
.steps li{font-size:28px;font-weight:700;color:#fff;line-height:1.35}
.steps li::marker{color:var(--ac);font-weight:800}
.qlist{padding:16px 22px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2)}
.qlist p{margin:0 0 8px;font-size:23px;color:#fff;line-height:1.4}
.qlist .lab{font-size:19px}
.qlist .pr{margin-top:12px;font-size:20px;color:#FFE3A3}
/* 9 */
.chk2{display:grid;gap:16px;width:100%}
.cq{display:grid;grid-template-columns:auto 1fr;gap:6px 18px;padding:16px 22px;border-radius:16px;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.2)}
.cq i{grid-row:span 2;font-style:normal;display:grid;place-items:center;width:44px;height:44px;border-radius:50%;border:2px solid var(--ac);color:var(--ac);font-size:20px;font-weight:800}
.cq p{margin:0;font-size:28px;font-weight:800;color:#fff}
.ca{font-size:22px;color:var(--ok)}
/* טלפון לאורך (tools/phone_deck.py, ?phone=1): הרשתות של השיעור — זו מתחת לזו */
html.ph.phport :is(.vs2,.task,.today){grid-template-columns:1fr!important}
html.ph.phport :is(.demos,.tasks){grid-template-columns:1fr 1fr!important}
html.ph.phport .flow{flex-direction:column}
html.ph.phport .far{transform:rotate(-90deg)}
html.ph.phport .np-h,html.ph.phport .np-r{grid-template-columns:1fr 90px 90px}
html.ph.phport .np-fig svg{width:70px}
@media (prefers-reduced-motion:reduce){.docs i,.netm circle{animation:none!important}}
'''

open(OUT, 'w', encoding='utf8').write(phone_deck.apply(D.html()))
print('slides', len(D.S), '→', OUT)
