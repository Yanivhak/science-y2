# ערכת בנייה לשיעורי המדעים על מנוע „מהכביש לחלל”: הרכבת העמוד, הערות המורה, וציורי SVG
# (טבלה מחזורית, אטום עם אלקטרונים חיצוניים במודל הזוגות, מולקולות, מודלים כדוריים).
import base64, html, math, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
def _read(n): return open(os.path.join(HERE, n), encoding='utf8').read()

# ---------- הערות המורה ----------
def notes(text):
    """שורה ראשונה: כותרת מודגשת. שורות שמתחילות ב־• נאספות לרשימה. השאר: פסקאות."""
    lines = [l.rstrip() for l in text.strip().split('\n')]
    out = [f'<b>{html.escape(lines[0])}</b>']
    ul = []
    def flush():
        if ul: out.append('<ul>' + ''.join(f'<li>{x}</li>' for x in ul) + '</ul>'); ul.clear()
    for l in lines[1:]:
        if l.startswith('• '): ul.append(html.escape(l[2:])); continue
        flush()
        if l: out.append(html.escape(l) + '<br>')
    flush()
    return ''.join(out)

class Deck:
    def __init__(self, title, chrome, meta):
        self.title, self.chrome, self.meta, self.S = title, chrome, meta, []
        self.js = ''   # סקריפטים של השיעור (הנפשות), אחרי המנוע
        self.css = ''  # CSS של השיעור, אחרי science.css
    def add(self, body, note, title, ch, sec='', cls='s', mins=1, skip=False, hook=''):
        a = f' data-min="{mins}" data-ch="{ch}"'
        if hook: a += f' data-hook="{hook}"'
        if sec: a += f' data-sec="{html.escape(sec, quote=True)}"'
        a += f' data-title="{html.escape(title, quote=True)}"'
        if skip: a = ' data-skip' + a
        self.S.append(f'<section{a} class="{cls}" data-notes="{html.escape(notes(note), quote=True)}">\n{body}\n</section>')
    def html(self):
        logo = 'data:image/png;base64,' + base64.b64encode(open(os.path.join(HERE, 'logo.png'), 'rb').read()).decode()
        self.logo = logo
        body = '\n\n'.join(self.S).replace('__LOGO__', logo)
        # משתני CSS לא עובדים בתכונות הציור של SVG — רק ב־style
        body = re.sub(r'(fill|stroke)="var\((--[\w-]+)\)"', r'style="\1:var(\2)"', body)
        return f'''<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{html.escape(self.title)}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Assistant:wght@200..800&display=block" rel="stylesheet">
<style>
{_read('deck.css')}
{_read('science.css')}
{self.css}
</style>
</head>
<body tabindex="-1" data-ch="open" data-title="{html.escape(self.title, quote=True)}" data-meta="{html.escape(self.meta, quote=True)}">

<div id="bar"><i></i></div>
<div id="stage"><div id="deck" class="nochrome">

<div id="chrome">
  <div class="ch__sec"><i></i><span id="chSec"></span></div>
  <div class="ch__r"><span class="ch__lesson">{self.chrome}</span><img class="ch__logo" src="{logo}" alt=""></div>
</div>

{body}

<div id="num" class="mono"></div>
<div id="hint"><kbd>?</kbd> עזרה &nbsp; <kbd>G</kbd> דף השיעור &nbsp; <kbd>S</kbd> הערות המורה</div>
</div></div>

<div id="notes"></div>
<div id="ov"><h4>כל השקופיות</h4><div id="ovg"></div></div>
<div id="guide"></div>
<div id="act"><button>סגירה ✕</button><iframe title="משימה" src="about:blank"></iframe></div>
<div id="help"><div>
  <h4>שליטה במצגת</h4>
  <kbd>←</kbd> <kbd>רווח</kbd> <kbd>PageDown</kbd> קדימה, כולל חשיפת תשובות<br>
  <kbd>→</kbd> <kbd>PageUp</kbd> אחורה<br>
  <kbd>T</kbd> טיימר &nbsp;·&nbsp; <kbd>F</kbd> מסך מלא<br>
  <kbd>S</kbd> הערות המורה &nbsp;·&nbsp; <kbd>G</kbd> דף השיעור להדפסה<br>
  <kbd>O</kbd> כל השקופיות &nbsp;·&nbsp; <kbd>H</kbd> לשקופית הראשונה<br>
  <kbd>?</kbd> סגירת החלון הזה
</div></div>
<script>
{_read('deck.js')}
</script>
<script>
{self.js}
</script>
</body>
</html>
'''

def F(x): return f'<span class="f">{x}</span>'

# ---------- צבעים ----------
EL = '#2E6FE0'          # אלקטרון: אותו כחול כהה בכל הציורים ובכל השיעורים (יניב, 14.11)
EL_D = '#2F7FC0'        # אלקטרון שבתנועה / מסומן (כהה יותר)
NUC = {'H': '#E8EEF7', 'He': '#F0A6FF', 'Ne': '#F0A6FF', 'C': '#A9B4C2', 'Si': '#C9A27E', 'N': '#9C8CFF',
       'O': '#FF6B6B', 'S': '#F5D547', 'F': '#9BE15D', 'Cl': '#3FD18F', 'Br': '#E08A5A', 'I': '#C77DFF', 'X': '#C9D3E3'}
MUTED, INK, LINE = '#C9D3E3', '#FFFFFF', 'rgba(255,255,255,.45)'
CELL = 'rgba(255,255,255,.11)'

def svg(w, h, inner, width=None, cls=''):
    width = width or w
    c = f' class="{cls}"' if cls else ''
    return (f'<svg{c} viewBox="0 0 {w} {h}" width="{width}" height="{round(width * h / w)}" '
            f'xmlns="http://www.w3.org/2000/svg" font-family="Assistant, sans-serif" direction="ltr">{inner}</svg>')

def T(x, y, s, size=16, fill=INK, w=700, anchor='middle', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" font-weight="{w}" fill="{fill}" text-anchor="{anchor}" {extra}>{s}</text>'

# ---------- אטום: גרעין, פס (אזור) לכל שכבה, ואלקטרונים במודל הזוגות ----------
DIRS = {'r': 0, 't': 90, 'l': 180, 'b': 270}
def outer_layout(n, single_first=('r', 't', 'b', 'l')):
    """עד 4 אזורים, עד 2 בכל אזור. עד 4 אלקטרונים: כולם בודדים. מעל 4: (n−4) זוגות ו־(8−n) בודדים."""
    if n <= 4:
        return {d: 1 for d in single_first[:n]}
    singles = 8 - n
    lay = {}
    for d in single_first[:singles]: lay[d] = 1
    for d in ('t', 'l', 'b', 'r'):
        if d not in lay and len([v for v in lay.values() if v == 2]) < n - 4: lay[d] = 2
    return lay

def dots(cx, cy, r, lay, er=5.2, col=EL, gap=7.5):
    out = []
    for d, k in lay.items():
        a = math.radians(DIRS[d]) if isinstance(d, str) else math.radians(d)
        x, y = cx + r * math.cos(a), cy - r * math.sin(a)
        if k == 1:
            out.append(f'<circle class="el s1" cx="{x:.1f}" cy="{y:.1f}" r="{er}" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
        else:
            px, py = -math.sin(a) * gap, -math.cos(a) * gap
            out.append(f'<circle class="el p2" cx="{x + px:.1f}" cy="{y + py:.1f}" r="{er}" fill="{col}" stroke="#fff" stroke-width="1.2"/><circle class="el p2" cx="{x - px:.1f}" cy="{y - py:.1f}" r="{er}" fill="{col}" stroke="#fff" stroke-width="1.2"/>')
    return ''.join(out)

def band(cx, cy, r, w=16, op=.30):
    """פס: האזור שבו נעים האלקטרונים של השכבה (לא מסלול). רך, בלי קווי מתאר — שלוש טבעות שקופות זו על זו,
    כדי שייקרא כ„אזור” ולא כ„מסילה” (יניב, 14.11: „שיהיה עקבי תמיד”). בהיר, כדי שייראה על הרקע הכהה."""
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#CFE3FF" stroke-opacity="{op * .33:.3f}" stroke-width="{w * 1.7:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#CFE3FF" stroke-opacity="{op * .5:.3f}" stroke-width="{w * 1.1:.1f}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#CFE3FF" stroke-opacity="{op * .55:.3f}" stroke-width="{w * .5:.1f}"/>')

def nucleus(cx, cy, sym, r=19, label=None, size=None):
    fill = NUC.get(sym, '#C9D3E3')
    lab = label if label is not None else sym
    size = size or (19 if len(lab) < 3 else 15)
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}"/>'
            + T(cx, cy + size * .36, lab, size, '#0B1A2E', 800))

def atom(sym, n, r=46, inner=None, label=None, lay=None, pad=14):
    """אטום אחד. inner — מספר האלקטרונים הפנימיים (פס נוסף). label — מה כתוב על הגרעין."""
    R = r + 12 + pad
    c = R
    g = band(c, c, r, 22 if r >= 80 else 16)
    big = r >= 80
    er = 6.5 if big else 5.2
    if inner:
        g += band(c, c, r * .55, 14 if big else 12, .2) + '<g class="e-in">' + dots(c, c, r * .55, {'t': 2} if inner == 2 else {'t': 1}, er, gap=9 if big else 7.5) + '</g>'
    nr = round(max(17, r * .2))
    g += nucleus(c, c, sym, nr, label, 24 if big else None)
    g += '<g class="e-out">' + dots(c, c, r, lay or outer_layout(n), er, gap=9 if big else 7.5) + '</g>'
    return svg(2 * R, 2 * R, g, 2 * R)

# ---------- מולקולות בנקודות: זוגות משותפים בין הגרעינים ----------
def _pair(x, y, a, gap=7.5, er=5.2, col=EL):
    px, py = -math.sin(a) * gap, -math.cos(a) * gap
    return f'<circle class="el sh" cx="{x + px:.1f}" cy="{y + py:.1f}" r="{er}" fill="{col}" stroke="#fff" stroke-width="1.2"/><circle class="el sh" cx="{x - px:.1f}" cy="{y - py:.1f}" r="{er}" fill="{col}" stroke="#fff" stroke-width="1.2"/>'

def mol2(a, b, shared, lone_a, lone_b, ra=44, rb=44, w=None):
    """שני אטומים בשורה. shared — מספר הזוגות המשותפים. lone — מילון כיוון→1/2 (בלי הצד שפונה לשותף)."""
    d = ra + rb - 10
    pad = 30
    ax, bx, cy = pad + ra, pad + ra + d, pad + max(ra, rb)
    W, H = bx + rb + pad, 2 * cy
    g = band(ax, cy, ra) + band(bx, cy, rb)
    g += nucleus(ax, cy, a, 14 if a == 'H' else 19) + nucleus(bx, cy, b, 14 if b == 'H' else 19)
    mx = (ax + bx) / 2
    for k in range(shared):
        off = (k - (shared - 1) / 2) * 17
        # בזוג המשותף: sa — האלקטרון שבצד האטום השמאלי (a), sb — שבצד הימני (b); לספירה בהדלקה (7 + 1 = 8)
        g += f'<g class="e-sh"><circle class="el sh sa" cx="{mx - 6:.1f}" cy="{cy + off:.1f}" r="5.2" fill="{EL}" stroke="#fff" stroke-width="1.2"/><circle class="el sh sb" cx="{mx + 6:.1f}" cy="{cy + off:.1f}" r="5.2" fill="{EL}" stroke="#fff" stroke-width="1.2"/></g>'
    g += '<g class="e-la">' + dots(ax, cy, ra, lone_a) + '</g><g class="e-lb">' + dots(bx, cy, rb, lone_b) + '</g>'
    return svg(W, H, g, w or W)

def bent(center, n_lone_pairs=2, r=46, rh=30, w=None):
    """מולקולה כפופה עם שני מימנים (כמו מים): מימן מימין ומימן למטה, זוגות לא משותפים למעלה ומשמאל."""
    pad = 22
    d = r + rh - 16
    cx, cy = pad + rh * 0 + r + 10, pad + r + 4
    hx1, hy1 = cx + d, cy
    hx2, hy2 = cx, cy + d
    W, H = hx1 + rh + pad, hy2 + rh + pad
    g = band(cx, cy, r) + band(hx1, hy1, rh, 14) + band(hx2, hy2, rh, 14)
    g += nucleus(cx, cy, center) + nucleus(hx1, hy1, 'H', 14) + nucleus(hx2, hy2, 'H', 14)
    g += _pair((cx + hx1) / 2 + 2, cy, 0) + _pair(cx, (cy + hy2) / 2 + 2, math.radians(270))
    g += dots(cx, cy, r, {'t': 2, 'l': 2})
    return svg(W, H, g, w or W)

# ---------- מודל כדורי (כמו בספר): אטום מרכזי ומימנים ----------
def ballstick(nh, w=120, center='#A9B4C2'):
    ang = {4: [0, 90, 180, 270], 3: [270, 150, 30], 2: [315, 225], 1: [180]}[nh]
    g = ''
    for a in ang:
        x, y = 60 + 40 * math.cos(math.radians(a)), 55 - 40 * math.sin(math.radians(a))
        g += f'<line x1="60" y1="55" x2="{x:.1f}" y2="{y:.1f}" stroke="#8A97A8" stroke-width="5"/>'
        g += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="11" fill="#F2F5FA" stroke="#8A97A8" stroke-width="2"/>'
    g += f'<circle cx="60" cy="55" r="20" fill="{center}" stroke="#6B7787" stroke-width="2"/>'
    return svg(120, 110, g, w)

# ---------- הטבלה המחזורית: 8 הטורים העיקריים ----------
ROWS = [
    [('H', 1, 'מימן'), None, None, None, None, None, None, ('He', 2, 'הליום')],
    [('Li', 3, 'ליתיום'), ('Be', 4, 'בריליום'), ('B', 5, 'בור'), ('C', 6, 'פחמן'), ('N', 7, 'חנקן'), ('O', 8, 'חמצן'), ('F', 9, 'פלואור'), ('Ne', 10, 'ניאון')],
    [('Na', 11, 'נתרן'), ('Mg', 12, 'מגנזיום'), ('Al', 13, 'אלומיניום'), ('Si', 14, 'צורן'), ('P', 15, 'זרחן'), ('S', 16, 'גפרית'), ('Cl', 17, 'כלור'), ('Ar', 18, 'ארגון')],
    [('K', 19, ''), ('Ca', 20, ''), ('Ga', 31, ''), ('Ge', 32, ''), ('As', 33, ''), ('Se', 34, ''), ('Br', 35, 'ברום'), ('Kr', 36, '')],
    [('Rb', 37, ''), ('Sr', 38, ''), ('In', 49, ''), ('Sn', 50, ''), ('Sb', 51, ''), ('Te', 52, ''), ('I', 53, 'יוד'), ('Xe', 54, '')],
    [('Cs', 55, ''), ('Ba', 56, ''), ('Tl', 81, ''), ('Pb', 82, ''), ('Bi', 83, ''), ('Po', 84, ''), ('At', 85, ''), ('Rn', 86, 'רדון')],
    [('Fr', 87, ''), ('Ra', 88, 'רדיום'), ('Nh', 113, ''), ('Fl', 114, ''), ('Mc', 115, ''), ('Lv', 116, ''), ('Ts', 117, ''), ('Og', 118, '')],
]
def valence(sym, col):
    return 2 if sym == 'He' else col

def ptable(rows=3, cw=86, ch=78, names=True, z=True, val=False, val_frag=False, row_frag=False,
           hl_cols=None, hl_cells=None, hl_rows=None, atoms=False, labels=True, width=None, marks=None):
    """
    hl_cols: {טור: (צבע, מחלקה)} — מסגרת סביב טור שלם. מחלקה: 'frag' או 'w1'.. או ''.
    hl_cells: {סמל: (צבע, מחלקה)}. hl_rows: {שורה: (צבע, מחלקה)}.
    atoms: שורת אטומים בנקודות מעל מספרי הטורים (כמו האיור בעמ׳ 32).
    """
    hl_cols, hl_cells, hl_rows = hl_cols or {}, hl_cells or {}, hl_rows or {}
    lw = 30 if labels else 6
    top = (cw + 10 if atoms else 0) + (30 if labels else 6)
    W = lw + 8 * cw + 8
    H = top + rows * ch + 8
    g = ''
    if atoms:
        r = cw * .30
        g += '<g class="frag">'
        for c in range(1, 9):
            cx, cy = lw + (c - .5) * cw, (cw + 10) / 2
            g += band(cx, cy, r, 9, .2) + f'<circle cx="{cx}" cy="{cy}" r="7" fill="#E8EEF7"/>' + dots(cx, cy, r, outer_layout(c), 4.4, gap=5.6)
        g += '</g>'
    if labels:
        for c in range(1, 9):
            g += T(lw + (c - .5) * cw, top - 9, str(c), 19, 'var(--ac)', 800)
        for r_ in range(rows):
            g += T(lw / 2 - 2, top + (r_ + .5) * ch + 6, str(r_ + 1), 19, MUTED, 800)
    for r_ in range(rows):
        cells = ''
        for c in range(8):
            e = ROWS[r_][c]
            if not e: continue
            sym, Z, nm = e
            x, y = lw + c * cw + 3, top + r_ * ch + 3
            w_, h_ = cw - 6, ch - 6
            hc = hl_cells.get(sym)
            cell = f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" rx="9" fill="{CELL}" stroke="{LINE}" stroke-width="1.5"/>'
            if hc:
                cell += f'<rect class="{hc[1]}" x="{x}" y="{y}" width="{w_}" height="{h_}" rx="9" fill="{hc[0]}" fill-opacity=".16" stroke="{hc[0]}" stroke-width="2.5"/>'
            sy = y + h_ * (.50 if (names and nm) else .66)
            cell += T(x + w_ / 2, sy + 2, sym, round(ch * .34), INK, 800)
            if z: cell += T(x + 6, y + 16, str(Z), 12.5, '#DDE6F2', 700, 'start', 'class="pt-z"')
            if val:
                v = T(x + w_ - 7, y + 20, str(valence(sym, c + 1)), 19, 'var(--ac)', 800, 'end')
                cell += f'<g class="frag">{v}</g>' if val_frag == 'each' else v
            if names and nm: cell += T(x + w_ / 2, y + h_ - 8, nm, 13.5, MUTED, 600)
            cells += cell
        if val_frag is True and val:
            pass
        cls = 'frag' if row_frag else ''
        g += f'<g class="{cls}">{cells}</g>' if cls else cells
        if r_ + 1 in hl_rows:
            col, k = hl_rows[r_ + 1]
            g += f'<rect class="{k}" x="{lw - 2}" y="{top + r_ * ch}" width="{8 * cw + 4}" height="{ch}" rx="12" fill="none" stroke="{col}" stroke-width="3"/>'
    for c, (col, k) in hl_cols.items():
        x = lw + (c - 1) * cw
        y0 = top + (0 if ROWS[0][c - 1] else ch)
        last = max(i for i in range(rows) if ROWS[i][c - 1]) + 1
        g += f'<rect class="{k}" x="{x}" y="{y0 - 2}" width="{cw}" height="{top + last * ch - y0 + 4}" rx="12" fill="{col}" fill-opacity=".10" stroke="{col}" stroke-width="3"/>'
    if marks: g += marks
    out = svg(W, H, g, width or W)
    if val and val_frag is True:
        # המספרים של האלקטרונים החיצוניים נחשפים יחד: עוטפים אותם בקבוצה אחת
        nums = re.findall(r'<text [^>]*fill="var\(--ac\)"[^>]*>\d</text>', out)
        for n_ in nums: out = out.replace(n_, '', 1)
        out = out.replace('</svg>', f'<g class="frag">{"".join(nums)}</g></svg>')
    return out

def tile(sym, Z, name, v=None, w=320, lab_z=None, lab_v=None):
    """משבצת גדולה, כמו המשבצת המוגדלת בעמ׳ 31. lab_z / lab_v: (טקסט, מחלקה) — תווית מעל הפינה, עם קו."""
    W, H = 320, 330
    x, y = 60, 120
    g = f'<rect x="{x}" y="{y}" width="200" height="200" rx="22" fill="rgba(255,255,255,.12)" stroke="rgba(255,255,255,.7)" stroke-width="2.5"/>'
    g += T(x + 22, y + 46, str(Z), 36, '#C9D3E3', 800, 'start')
    if v is not None: g += T(x + 178, y + 46, str(v), 36, 'var(--ac)', 800, 'end')
    g += T(x + 100, y + 135, sym, 78, INK, 800)
    g += T(x + 100, y + 182, name, 24, '#DDE6F2', 700)
    if lab_z:
        g += f'<g class="{lab_z[1]}"><line x1="{x + 34}" y1="{y + 8}" x2="{x + 34}" y2="{y - 34}" stroke="#C9D3E3" stroke-width="2.5"/>'
        g += T(x - 40, y - 44, lab_z[0], 22, '#C9D3E3', 800, 'start') + '</g>'
    if lab_v:
        g += f'<g class="{lab_v[1]}"><line x1="{x + 166}" y1="{y + 8}" x2="{x + 166}" y2="{y - 86}" stroke="var(--ac)" stroke-width="2.5"/>'
        g += T(x + 250, y - 96, lab_v[0], 22, 'var(--ac)', 800, 'end') + '</g>'
    return svg(W, H, g, w)

# ---------- הטבלה המלאה בקווים כלליים: 8 הטורים העיקריים מודגשים, והיסודות שבאמצע מעומעמים ----------
def fulltable(w=900, mid_cls=''):
    """18 עמודות × 7 שורות, כמו הטבלה בעמ׳ 32 (בלי הלנתנידים והאקטינידים). טורים 1–2 ו־13–18 — 8 הטורים העיקריים."""
    c, gap = 40, 4
    main = {1: 1, 2: 2, 13: 3, 14: 4, 15: 5, 16: 6, 17: 7, 18: 8}
    g = ''
    for r in range(1, 8):
        for k in range(1, 19):
            if r == 1 and k not in (1, 18): continue
            if r in (2, 3) and 3 <= k <= 12: continue
            x, y = 10 + (k - 1) * (c + gap), 40 + (r - 1) * (c + gap)
            if k in main:
                g += f'<rect x="{x}" y="{y}" width="{c}" height="{c}" rx="6" fill="var(--ac)" fill-opacity=".75" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>'
            else:
                g += f'<rect class="{mid_cls}" x="{x}" y="{y}" width="{c}" height="{c}" rx="6" fill="rgba(255,255,255,.10)" stroke="rgba(255,255,255,.35)" stroke-width="1.2"/>'
    for k, n in main.items():
        g += T(10 + (k - 1) * (c + gap) + c / 2, 28, str(n), 20, 'var(--ac)', 800)
    W = 10 + 18 * (c + gap) + 6
    H = 40 + 7 * (c + gap) + 6
    return svg(W, H, g, w)

# ---------- הטבלה המחזורית המלאה: 118 יסודות, כמו הטבלה בעמ׳ 32, עם 104–118 (IUPAC, 2016) ----------
PT_ROWS = [
    'H' + ' .' * 16 + ' He',
    'Li Be' + ' .' * 10 + ' B C N O F Ne',
    'Na Mg' + ' .' * 10 + ' Al Si P S Cl Ar',
    'K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr',
    'Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe',
    'Cs Ba * Hf Ta W Re Os Ir Pt Au Hg Tl Pb Bi Po At Rn',
    'Fr Ra ** Rf Db Sg Bh Hs Mt Ds Rg Cn Nh Fl Mc Lv Ts Og',
]
PT_F = ['La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu', 'Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr']
PT_MAIN = {1: 1, 2: 2, 13: 3, 14: 4, 15: 5, 16: 6, 17: 7, 18: 8}

def pt_cells():
    """(סמל, מספר אטומי, שורה, עמודה 1–18 או None, שורת f 0/1 או None) — לפי סדר המספר האטומי."""
    out, Z = [], 0
    for r, row in enumerate(PT_ROWS, 1):
        for k, sym in enumerate(row.split(), 1):
            if sym == '.': continue
            if sym in ('*', '**'):
                for j, fs in enumerate(PT_F[len(sym) - 1].split()):
                    Z += 1; out.append((fs, Z, r, None, len(sym) - 1, j))
                continue
            Z += 1; out.append((sym, Z, r, k, None, None))
    assert Z == 118, Z
    return out

def realtable(w=880, cls='', click=False):
    """כל 118 היסודות: 7 שורות ועוד שתי שורות f מתחת (כמו בעמ׳ 32). משבצות 8 הטורים העיקריים — מחלקה m, האמצע — d, שורות f — f.
    מספרי הטורים (1–8, כמו בספר) — בקבוצה colnum; מספרי השורות — משמאל."""
    c, gap, lw, top = 56, 4, 30, 62
    p = c + gap
    fy = top + 7 * p + 16
    g = ''
    for r in range(1, 8):
        g += T(lw / 2, top + (r - 1) * p + c / 2 + 6, str(r), 19, MUTED, 800)
    NAMES = {e[0]: e[2] for row in ROWS for e in row if e and e[2]}
    def cell(x, y, sym, z, k, col=0, row=0):
        # click=True: כל משבצת היא כפתור (tools/lesson08_read.js) — הטור 1–18 (0 בשורות שמתחת), הטור בספר (0 מחוץ ל־8 הטורים העיקריים), השם אם יש
        a = (f' tabindex="0" role="button" aria-label="{sym}" data-sym="{sym}" data-z="{z}" data-k="{col}" data-b="{PT_MAIN.get(col, 0)}" data-r="{row}" data-n="{NAMES.get(sym, "")}"'
             if click else '')
        return (f'<g class="pc {k}"{a}><rect x="{x}" y="{y}" width="{c}" height="{c}" rx="7"/>'
                + T(x + 4, y + 15, str(z), 14, '#DDE6F2', 700, 'start', 'class="pt-z"')
                + T(x + c / 2, y + c * .76, sym, 23, INK, 800) + '</g>')
    for sym, z, r, k, fr, j in pt_cells():
        if k:
            g += cell(lw + (k - 1) * p, top + (r - 1) * p, sym, z, 'm' if k in PT_MAIN else 'd', k, r)
        else:
            g += cell(lw + (j + 2) * p, fy + fr * p, sym, z, 'f', 0, r)
    for r, lab in ((6, '57–71'), (7, '89–103')):
        x, y = lw + 2 * p, top + (r - 1) * p
        g += (f'<g class="pc f ph"><rect x="{x}" y="{y}" width="{c}" height="{c}" rx="7"/>'
              + T(x + c / 2, y + c / 2 + 5, lab, 12.5, MUTED, 700) + '</g>')
    # תוויות לשתי שורות המספור, מימין לטבלה (שם העין מתחילה לקרוא): „היום” ליד 1–18, „בספר” ליד 1–8
    lx = lw + 18 * p + 10
    g += '<g class="n18">' + ''.join(T(lw + (k - 1) * p + c / 2, top - 9, str(k), 19, MUTED, 700) for k in range(1, 19)) + T(lx, top - 9, 'היום', 19, MUTED, 700, 'start') + '</g>'
    g += '<g class="colnum">' + ''.join(T(lw + (k - 1) * p + c / 2, top - 36, str(n), 26, 'var(--ac)', 800) for k, n in PT_MAIN.items()) + T(lx, top - 36, 'בספר', 22, 'var(--ac)', 800, 'start') + '</g>'
    W, H = lx + 62, fy + 2 * p + 4
    return svg(W, H, g, w, cls)

# ---------- מולקולה בנקודות: אטום מרכזי ושכנים סביבו (מתאן, פחמן ארבע־כלורי) ----------
def star(center, subs, r=46, w=None):
    """subs: רשימה של (סמל, רדיוס, זווית במעלות, זוגות שלא בקשר — מילון כיוון→2). בכל קשר — זוג משותף בין הגרעינים."""
    reach = max(r + s[1] - 12 + s[1] for s in subs) + 26
    c = reach
    g = band(c, c, r)
    parts = ''
    for k, (sym, rs, ang, lone) in enumerate(subs):
        a = math.radians(ang)
        d = r + rs - 12
        x, y = c + d * math.cos(a), c - d * math.sin(a)
        g += band(x, y, rs, 14 if rs < 40 else 16)
        mx, my = c + (r - 6) * math.cos(a), c - (r - 6) * math.sin(a)
        parts += nucleus(x, y, sym, 14 if sym == 'H' else 17)
        # כל שכן בקבוצה משלו (sub0, sub1…): הזוג המשותף שלו והאלקטרונים שלו — כדי להדליק אטום אחד
        parts += f'<g class="sub sub{k}">' + _pair(mx, my, a, 7.5) + dots(x, y, rs, lone) + '</g>'
    g += nucleus(c, c, center) + parts
    return svg(2 * c, 2 * c, g, w or 2 * c)

# ---------- מודל כדורי צבעוני, כמו המודלים בעמ׳ 29 (מקרא הספר: חמצן אדום, מימן לבן, פחמן אפור, חנקן כחול, פלואור ירוק) ----------
BALL = {'O': '#FF5C5C', 'H': '#F2F5FA', 'C': '#8A97A8', 'N': '#4F7BFF', 'F': '#9BE15D', 'Si': '#A9B4C2', 'Cl': '#3FD18F'}
def model(atoms, bonds, w=170, vb=(0, 0, 200, 170), labels=True):
    """atoms: [(סמל, x, y)], bonds: [(i, j)]. מימן קטן, השאר גדולים."""
    g = ''.join(f'<line x1="{atoms[i][1]}" y1="{atoms[i][2]}" x2="{atoms[j][1]}" y2="{atoms[j][2]}" stroke="#C9D3E3" stroke-width="6"/>' for i, j in bonds)
    for sym, x, y in atoms:
        rr = 12 if sym == 'H' else 20
        g += f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{BALL[sym]}" stroke="#fff" stroke-opacity=".6" stroke-width="1.5"/>'
        if labels and sym != 'H': g += T(x, y + 6, sym, 16, '#0B1A2E', 800)
    return svg(vb[2], vb[3], g, w).replace(f'viewBox="0 0 {vb[2]} {vb[3]}"', f'viewBox="{vb[0]} {vb[1]} {vb[2]} {vb[3]}"')
