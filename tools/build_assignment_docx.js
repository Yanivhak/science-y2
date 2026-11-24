// בונה את דף המשימה לחופש כקובץ Word בעברית (RTL): כותרות, חלקים מופרדים, יישור לימין.
// התוכן: הקובץ של יניב (24.11.2026) אחרי התיקונים. שימוש: node tools/build_assignment_docx.js [קובץ פלט]
const fs = require('fs');
const path = require('path');
const { Document, Packer, Paragraph, TextRun, AlignmentType, LevelFormat, Footer, Header, ImageRun, BorderStyle } = require('docx');
// הסמל של בית הספר (מקיף שש שנתי ע"ש יונתן נתניהו), אותו קובץ שבמצגות
const LOGO = fs.readFileSync(path.join(__dirname, 'deck', 'logo.png'));

const OUT = process.argv[2] || path.join(__dirname, '..', 'lessons', 'עבודה-לחופש', 'עבודה-במדעים.docx');
const FONT = 'Arial';
const INK = '000000', MUTED = '555555', RULE = '000000';

// כל פסקה: מימין לשמאל, גופן עברי, ריווח קבוע
function run(text, o = {}) {
  return new TextRun({ text, font: { ascii: FONT, hAnsi: FONT, cs: FONT }, rightToLeft: true,
    size: o.size || 24, sizeComplexScript: o.size || 24, bold: !!o.bold, boldComplexScript: !!o.bold,
    italics: !!o.italic, italicsComplexScript: !!o.italic, color: o.color || INK });
}
function para(children, o = {}) {
  return new Paragraph({ bidirectional: true, alignment: o.align || AlignmentType.START, children,
    spacing: { before: o.before ?? 0, after: o.after ?? 120, line: 300 }, keepNext: !!o.keepNext,
    border: o.rule ? { bottom: { style: BorderStyle.SINGLE, size: 8, color: RULE, space: 4 } } : undefined,
    numbering: o.bullet ? { reference: 'bul', level: 0 } : undefined });
}
const body = (t, o = {}) => para([run(t)], o);
const label = (lab, t) => para([run(lab + ' ', { bold: true }), run(t)]);
const len = t => para([run(t, { italic: true, color: MUTED, size: 22 })], { after: 240 });
const h2 = t => para([run(t, { bold: true, size: 30 })], { before: 360, after: 160, rule: true, keepNext: true });
const h3 = t => para([run(t, { bold: true, size: 26 })], { before: 240, after: 80, keepNext: true });
const h4 = t => para([run(t, { bold: true })], { before: 120, after: 60, keepNext: true });
const bullet = t => para([run(t)], { bullet: true, after: 40 });

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  numbering: { config: [{ reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
    alignment: AlignmentType.START, style: { paragraph: { indent: { start: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1134, bottom: 1134, left: 1134, right: 1134 } }, bidi: true },
    headers: { default: new Header({ children: [new Paragraph({ bidirectional: true, alignment: AlignmentType.END, spacing: { after: 0 },
      children: [new ImageRun({ type: 'png', data: LOGO, transformation: { width: 72, height: 72 } })] })] }) },
    footers: { default: new Footer({ children: [para([run('עבודה במדעים | כיתה י׳2', { size: 18, color: MUTED })], { align: AlignmentType.CENTER, after: 0 })] }) },
    children: [
      // פתיחה
      para([run('עבודה במדעים', { color: MUTED })], { after: 40 }),
      para([run('האם בני אדם יכולים להרוס את כדור הארץ?', { bold: true, size: 36 })], { after: 240 }),
      body('בני האדם משפיעים על הסביבה בדרכים רבות. חלק מהפעולות שלנו גורמות לנזקים חמורים, ולעיתים גם בלתי הפיכים. אבל האם פירוש הדבר שאנחנו יכולים להרוס את כדור הארץ עצמו?'),
      body('בעבודה זו תבדקו כיצד בני האדם משפיעים על הסביבה, תכירו דוגמאות לפגיעה ולשיקום סביבתי, ולבסוף תגבשו מסקנה המבוססת על המידע שאספתם.'),

      // השאלות
      h2('מה כותבים בעבודה'),
      h3('1. השפעת האדם על הסביבה'),
      body('פעילויות שונות של בני האדם פוגעות בסביבה. פגיעה בסביבה יכולה להתבטא בזיהום האוויר, המים והקרקע, בהרס בתי גידול ובפגיעה בצמחים, בבעלי חיים ובבני אדם.'),
      h4('א. בחרו אחת מהפעילויות הבאות:'),
      bullet('כריתת יערות'), bullet('השלכת פלסטיק לים'), bullet('דיג יתר'), bullet('פליטת גזי חממה'),
      body('חקרו כיצד הפעילות שבחרתם פוגעת בסביבה ומהן השפעותיה על צמחים, בעלי חיים ובני אדם.', { before: 80 }),
      len('היקף: חצי עמוד.'),
      h4('ב. מה עלול לקרות בעתיד?'),
      body('פגיעה אחת בסביבה יכולה לגרום לשרשרת של שינויים.'),
      body('לדוגמה: כאשר נחל מזדהם, חלק מהדגים עלולים למות. בעקבות זאת, לציפורים שניזונות מהדגים יהיה פחות מזון, ולכן מספרן עלול לרדת. אם יהיו פחות ציפורים, בעלי חיים שניזונים מהן עלולים גם הם להיפגע.'),
      body('כך פגיעה אחת יכולה להוביל לפגיעה נוספת, וזו לפגיעה אחרת.'),
      body('כעת חשבו על הפעילות שבחרתם: מה עלול לקרות אם היא תימשך לאורך שנים? תארו שרשרת של לפחות שלושה שינויים והסבירו כיצד כל שינוי מוביל לשינוי הבא.'),
      len('היקף: 5 שורות.'),
      h3('2. כדור הארץ וסביבת החיים'),
      body('מה ההבדל בין הרס כדור הארץ עצמו לבין פגיעה בתנאים המאפשרים חיים עליו? הסבירו את ההבדל במילים שלכם.'),
      len('היקף: 5 שורות.'),
      h3('3. שיקום הסביבה'),
      body('מצאו דוגמה אמיתית למקרה שבו בני אדם הצליחו לצמצם נזק סביבתי או לשקם סביבה שנפגעה. תארו מה היה הנזק, אילו פעולות נעשו כדי לטפל בו ומה היו התוצאות.'),
      len('היקף: חצי עמוד.'),
      h3('4. מסקנה'),
      body('לאחר שבדקתם את הנושא, האם לדעתכם בני האדם יכולים להרוס את כדור הארץ? נמקו את תשובתכם בעזרת המידע שהצגתם בעבודה.'),
      len('היקף: 5 שורות.'),
      h3('5. מקורות מידע'),
      body('ציינו לפחות שלושה מקורות מידע שבהם השתמשתם. למקורות מהאינטרנט צרפו קישורים. אם נעזרתם בבינה מלאכותית, ציינו באיזה כלי השתמשתם. כלי בינה מלאכותית ומנועי חיפוש אינם תחליף למקורות מידע.'),

      // ההוראות
      h2('הוראות הגשה'),
      label('מועד הגשה:', 'יום ראשון, 13 בדצמבר 2026.'),
      label('אופן הגשה:', 'עבודה מודפסת או קובץ שנשלח אליי.'),
      label('היקף העבודה:', 'כעמוד וחצי, לא כולל מקורות.'),
      label('עיצוב:', 'גופן Arial, גודל 12, יישור לשני הצדדים.'),
      label('שימוש בבינה מלאכותית:', 'השימוש אינו חובה ומותר רק באישור ההורים. אפשר להיעזר בבינה מלאכותית כדי להבין מושגים, למצוא כיווני חיפוש ולארגן רעיונות. את העבודה יש לכתוב במילים שלכם. חשוב לזכור שבינה מלאכותית עלולה לטעות, ולכן יש לבדוק את המידע בעזרת מקורות אמינים נוספים.'),

      h2('לפני שמגישים'),
      body('לאחר שסיימתם לכתוב, קראו שוב את העבודה מתחילתה ועד סופה. בדקו שעניתם על כל השאלות ושההסברים ברורים ומדויקים. תקנו שגיאות, הסירו חזרות ומידע שאינו נחוץ, וודאו שכל משפט תורם להסבר. רק לאחר מכן הגישו את העבודה.'),
    ],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('→', OUT); });
