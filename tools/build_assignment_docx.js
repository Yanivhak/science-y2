// בונה את דף המשימה לחופש כקובץ Word בעברית (RTL): כותרות, חלקים מופרדים, יישור לימין.
// התוכן: הנוסח של יניב, 25.11.2026, מילה במילה. שימוש: node tools/build_assignment_docx.js [קובץ פלט]
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
    spacing: { before: o.before ?? 0, after: o.after ?? 70, line: 276 }, keepNext: !!o.keepNext,
    border: o.rule ? { bottom: { style: BorderStyle.SINGLE, size: 8, color: RULE, space: 4 } } : undefined,
    numbering: o.bullet ? { reference: 'bul', level: 0 } : undefined });
}
const body = (t, o = {}) => para([run(t)], o);
const label = (lab, t) => para([run(lab + ' ', { bold: true }), run(t)]);
const len = t => para([run(t, { italic: true, color: MUTED, size: 22 })], { after: 140 });
const h2 = t => para([run(t, { bold: true, size: 30 })], { before: 240, after: 120, rule: true, keepNext: true });
const h3 = t => para([run(t, { bold: true, size: 26 })], { before: 180, after: 60, keepNext: true });
const h4 = t => para([run(t, { bold: true })], { before: 120, after: 60, keepNext: true });
const bullet = t => para([run(t)], { bullet: true, after: 40 });

const doc = new Document({
  styles: { default: { document: { run: { font: FONT, size: 24 } } } },
  numbering: { config: [{ reference: 'bul', levels: [{ level: 0, format: LevelFormat.BULLET, text: '•',
    alignment: AlignmentType.START, style: { paragraph: { indent: { start: 540, hanging: 270 } } } }] }] },
  sections: [{
    properties: { page: { margin: { top: 1000, bottom: 900, left: 1134, right: 1134, header: 400 } }, bidi: true },
    headers: { default: new Header({ children: [new Paragraph({ bidirectional: true, alignment: AlignmentType.END, spacing: { after: 0 },
      children: [new ImageRun({ type: 'png', data: LOGO, transformation: { width: 60, height: 60 } })] })] }) },
    footers: { default: new Footer({ children: [para([run('עבודה במדעים – כיתה ט׳', { size: 18, color: MUTED })], { align: AlignmentType.CENTER, after: 0 })] }) },
    children: [
      // פתיחה
      para([run('עבודה במדעים – כיתה ט׳', { color: MUTED })], { after: 40 }),
      para([run('האם בני האדם יכולים להרוס את כדור הארץ?', { bold: true, size: 36 })], { after: 240 }),
      body('בני האדם משפיעים על הסביבה בדרכים רבות. חלק מהפעולות שלנו גורמות לזיהום ולפגיעה בצמחים, בבעלי חיים ובבני אדם.'),
      body('בעבודה זו תבדקו כיצד בני האדם פוגעים בסביבה, כיצד אפשר לתקן נזקים ומה אפשר ללמוד מכך.'),

      h3('1. השפעת האדם על הסביבה'),
      h4('בחרו נושא אחד:'),
      bullet('כריתת יערות'), bullet('השלכת פלסטיק לים'), bullet('דיג יתר'), bullet('פליטת גזי חממה'),
      h4('ענו על השאלות הבאות:'),
      body('א. הסבירו מהי הפעילות שבחרתם וכיצד היא פוגעת בסביבה.'),
      body('ב. הסבירו כיצד הפגיעה משפיעה על צמחים, בעלי חיים או בני אדם. הביאו שתי דוגמאות.'),
      len('היקף: 6–8 שורות בסך הכול.'),

      h3('2. שיקום הסביבה'),
      body('מצאו דוגמה אמיתית למקרה שבו בני אדם פעלו כדי לתקן נזק סביבתי.'),
      h4('ענו על השאלות:'),
      body('א. היכן התרחש המקרה ומה היה הנזק?'),
      body('ב. מה עשו בני האדם כדי לתקן את הנזק?'),
      body('ג. האם הפעולות הצליחו? הסבירו את תשובתכם.'),
      len('היקף: 5–6 שורות בסך הכול.'),

      h3('3. מסקנה'),
      body('האם לדעתכם בני האדם יכולים להרוס את כדור הארץ עצמו, או בעיקר לפגוע בתנאים המאפשרים חיים עליו?'),
      body('הסבירו את תשובתכם בעזרת המידע שאספתם בעבודה.'),
      len('היקף: 4–5 שורות.'),

      h3('מקורות מידע'),
      body('ציינו לפחות שני מקורות מידע שבהם השתמשתם. למקורות מהאינטרנט צרפו קישורים.'),

      // ההוראות
      h2('הוראות הגשה'),
      label('מועד הגשה:', 'יום ראשון, 13 בדצמבר 2026.'),
      label('היקף העבודה:', 'כעמוד אחד.'),
      label('אופן ההגשה:', 'עבודה מודפסת או קובץ שנשלח למורה.'),
      label('שימוש בבינה מלאכותית:', 'מותר רק באישור ההורים. אפשר להיעזר בה כדי להבין מושגים, לחפש מידע ולארגן רעיונות. את העבודה יש לכתוב במילים שלכם ולבדוק שהמידע נכון.'),

      h2('לפני שמגישים'),
      body('קראו שוב את העבודה ובדקו שעניתם על כל השאלות, שההסברים ברורים ושהמידע נכון. תקנו שגיאות והסירו מידע שאינו נחוץ.'),
      para([run('זכרו: איכות ההסברים והחשיבה חשובה יותר מכמות הכתיבה.', { bold: true })], { before: 120 }),
    ],
  }],
});

Packer.toBuffer(doc).then(b => { fs.writeFileSync(OUT, b); console.log('→', OUT); });
