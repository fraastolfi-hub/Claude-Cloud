#!/usr/bin/env python3
"""Compone guida.html (copy v2, 26 pagine) a partire da base.css e dai testi qui sotto.
Uso: python3 build_guida.py && node pdf.mjs"""
from pathlib import Path

HERE = Path(__file__).parent
CSS = (HERE / "base.css").read_text()
TITLE = "Il posizionamento, spiegato semplice a chi ha un hotel"
FOOT = "Hotel Positioning · Il posizionamento, spiegato semplice"

EXTRA_CSS = """
.part{background:var(--ink);color:#fff;border-radius:999px;padding:5px 13px;font:800 7.6pt/1 var(--d);letter-spacing:.08em;text-transform:uppercase;align-self:flex-start;margin-bottom:10px}
.big{font:900 34pt/1.02 var(--d);letter-spacing:-.035em;margin:8px 0 14px}
.scene{font:italic 500 12.4pt/1.6 var(--t);color:var(--ink2);border-left:4px solid var(--yellow);padding-left:14px;margin:6px 0 14px}
.scene p+p{margin-top:2px}
.lines p{margin:0}
.roomy p,.roomy .lines p{font-size:13.4pt;line-height:1.6}
.roomy .lines p+p{margin-top:4px}
.roomy .scene{font-size:13.8pt}
.roomy .scene p{font-size:13.8pt}
.roomy .lead{font-size:14pt}
.roomy .two p{font-size:13pt}
.roomy .two h4{font-size:13.6pt}
.roomy .ans div{font-size:12.6pt;line-height:1.5}
.roomy .q p{font-size:12.8pt}
.roomy .q h3{font-size:15pt}
.roomy .law{font-size:15pt}
.roomy .rule b{font-size:13pt}
.roomy .book-box p{font-size:12.4pt}
.roomy .formula ol{font-size:12.2pt!important}
.roomy .small{font-size:10.6pt}
.roomy .vt span{font-size:12pt}
.lines p+p{margin-top:2px}
.law{font:800 15pt/1.25 var(--d);letter-spacing:-.02em;margin-top:14px}
.law .hl{padding:0 .1em}
.ill{border:2px solid var(--ink);border-radius:22px;box-shadow:5px 5px 0 var(--ink);overflow:hidden;margin:4px 0 18px;height:66mm}
.conto .lines p{font-size:12.6pt;line-height:1.55}
.conto .scene{font-size:13.4pt}
.conto .law{font-size:17pt;margin-top:18px}
.conto .card p,.conto .rule p{font-size:11pt}
.conto .lines+.lines,.conto div>.lines{margin-top:4px}
.ill svg{display:block;width:100%;height:100%}
.conto-n{display:flex;align-items:center;gap:10px}
.conto-n b{width:36px;height:36px;border-radius:11px;background:var(--yellow);border:2px solid var(--ink);display:grid;place-items:center;font:900 13pt var(--d)}
.tbl{width:100%;border-collapse:separate;border-spacing:0;border:2px solid var(--ink);border-radius:18px;overflow:hidden;box-shadow:4px 4px 0 var(--ink);background:#fff;margin:6px 0 16px;font-size:9.8pt}
.tbl th{background:var(--ink);color:#fff;text-align:left;font:800 8pt var(--d);text-transform:uppercase;letter-spacing:.05em;padding:9px 12px}
.tbl td{padding:10px 12px;border-top:1px solid var(--line);vertical-align:top;line-height:1.45}
.tbl td:first-child{font:800 9.6pt var(--d);white-space:nowrap}
.tbl td:nth-child(2){color:var(--ink3)}
.tbl td:nth-child(3){font-weight:600}
.book-box{border:2px solid var(--ink);border-radius:16px;padding:12px 14px;background:#fff;display:flex;gap:14px;align-items:center;margin-top:12px}
.book-box p{font-size:11pt;line-height:1.55}
.book-box .btn{margin-top:6px}
.hotels.three{grid-template-columns:repeat(3,1fr);gap:9px}
.hotels.three .ht{padding:9px 10px;gap:5px}
.hotels.three .ht-t{font-size:8.2pt}
.hotels.three .ht-t small{font-size:7.6pt}
.hotels.three .bar{grid-template-columns:50px 1fr 12px;font-size:6.2pt}
.hotels.three .ht-f .pm b{font-size:16pt}
.hotels.three .ht-f .rev b{font-size:9.4pt}
.vs.tight{padding:9px 13px;margin-top:8px}
.vs.tight p{font-size:9.1pt;line-height:1.45}
.vs.tight .vs-h{margin-bottom:4px}
.vs .law-s{display:block;margin-top:4px;font:800 9.2pt/1.3 var(--d)}
.mixlist{display:grid;gap:10px;margin-top:6px}
.mixlist .card{padding:11px 14px}
.mixlist .card p{font-size:10pt}
.mixlist .chips{gap:5px;margin-bottom:6px}
.mixlist .chip{font-size:7.4pt;padding:4px 9px}
/* ===== copertina ===== */
.cv2{background:var(--yellow);padding:0}
.cv2-top{position:absolute;left:18mm;right:18mm;top:14mm;display:flex;justify-content:space-between;align-items:center}
.cv2-meta{font:700 7.6pt var(--d);letter-spacing:.1em;text-transform:uppercase}
.cv2-body{position:absolute;left:18mm;right:18mm;top:42mm}
.cv2-kick{font:700 10pt var(--d);letter-spacing:.06em;text-transform:uppercase;padding-bottom:8px;border-bottom:2.5px solid var(--ink);display:inline-block}
.cover .cv2-h{font:900 50pt/1 var(--d);letter-spacing:-.04em;margin:11mm 0 8mm;color:var(--ink);max-width:none;white-space:nowrap}
.cv2-sub{font:500 13pt/1.45 var(--t);max-width:96mm;color:var(--ink)}
.cv2-photo{position:absolute;right:-6mm;bottom:28mm;width:120mm;height:132mm}
.cv2-disc{position:absolute;left:12mm;right:0;bottom:0;height:112mm;border-radius:999px 999px 0 0;background:var(--lilac);border:2.5px solid var(--ink);border-bottom:0}
.cv2-photo img{position:absolute;bottom:0;left:50%;transform:translateX(-46%);height:100%}
.cv2-bottom{position:absolute;left:18mm;bottom:28mm;width:84mm;display:flex;flex-direction:column;gap:9mm}
.cv2-author{display:flex;flex-direction:column}
.cv2-author img{height:17mm;width:auto;align-self:flex-start;margin-left:-3mm}
.cv2-author span{font:900 15pt/1.1 var(--d);margin-top:2mm}
.cv2-author small{font:600 8.6pt var(--d);color:var(--ink2)}
.cv2-formula{display:flex;flex-wrap:wrap;gap:5px}
.cv2-formula .chip{font-size:8pt;padding:5px 10px;background-color:#fff}
.cv2-formula .c-loc{background:var(--lsoft)}.cv2-formula .c-cap{background:var(--tsoft)}.cv2-formula .c-ops{background:var(--psoft)}.cv2-formula .c-nar{background:#fff}
.cv2-band{position:absolute;left:0;right:0;bottom:0;height:16mm;background:var(--ink);color:#fff;display:flex;justify-content:space-between;align-items:center;padding:0 18mm;font:700 8pt var(--d);letter-spacing:.08em;text-transform:uppercase}
/* ===== pagine 14-20: testo più grande, icone ===== */
.ico{display:inline-grid;place-items:center;border-radius:50%;border:2px solid var(--ink);flex:none}
.pf{margin-top:14px}
.pf-h{display:flex;align-items:center;gap:14px;padding-bottom:8px;border-bottom:2px solid var(--ink)}
.pf-l{display:block;font:700 7.6pt/1 var(--d);letter-spacing:.1em;text-transform:uppercase;color:var(--ink3);margin-bottom:4px}
.pf-h h3{font-size:17pt}
.pf-b{margin-top:10px}
.pf-b p,.two p,.mx p,.cf p{font-size:11.6pt;line-height:1.6}
.pf-sub{display:grid;grid-template-columns:1fr 1fr;gap:18px;margin-top:14px}
.pf-sub>div{padding:4px 0 4px 14px;border-left:4px solid var(--green)}
.pf-sub .risk{border-left-color:#ff5a3c}
.pf-sub .kick{display:block;margin-bottom:6px;color:var(--ink)}
.pf-sub p{font-size:11pt;line-height:1.55}
.pf-sub.one{grid-template-columns:1fr}
.pf-sub.one p{font-size:12pt}
.pf-sep{height:22px}
.two{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:16px}
.two h4{font:800 12.6pt/1.25 var(--d);margin:6px 0 6px}
.two .num{display:inline-grid;place-items:center;width:28px;height:28px;border-radius:50%;background:var(--yellow);border:2px solid var(--ink);font:900 11pt var(--d)}
.two.cases>div{border-top:2px solid var(--ink);padding-top:8px}
.mxl{display:grid;gap:16px}
.mx{display:grid;grid-template-columns:96px 1fr;gap:16px;align-items:start;padding-bottom:14px;border-bottom:1px solid var(--line)}
.mx-i{display:flex;gap:0}
.mx-i .ico+.ico{margin-left:-10px}
.mx h4{font:800 13pt/1.25 var(--d);margin-bottom:5px}
.mx.all{grid-template-columns:96px 1fr;border-bottom:0;background:var(--ysoft);border-radius:16px;padding:14px}
.mx.all .mx-i{flex-wrap:wrap;gap:4px}
.mx.all .mx-i .ico+.ico{margin-left:0}
.cf{display:grid;grid-template-columns:44mm 1fr;gap:16px;padding:16px 0;border-top:2px solid var(--ink)}
.cf-ab{display:flex;align-items:baseline;gap:6px}
.cf-ab b{font:900 26pt/1 var(--d)}
.cf-ab i{font:900 18pt var(--d);font-style:normal;color:var(--lilac)}
.cf-d{margin-top:10px;display:inline-flex;flex-direction:column;background:var(--lsoft);border-radius:12px;padding:8px 12px;font:900 18pt/1.05 var(--d)}
.cf-d small{font:700 9pt/1.3 var(--d);margin-top:3px}
.cf-r .kick{display:block;margin-bottom:6px}
.cf-law{margin-top:8px!important}
.cf-law span{font:800 11.4pt/1.35 var(--d);box-shadow:inset 0 -.38em 0 var(--lsoft)}
.hr{padding:9px 0}
.hn{font-size:9.4pt}.hn b{font-size:10pt}
.hb i b{height:7px}
.hp b{font-size:17pt}
.hf{font-size:11.4pt}
.votes{margin-top:16px;border:2px solid var(--ink);border-radius:18px;padding:14px 18px;background:#fff}
.votes .kick{display:block;margin-bottom:8px;color:var(--ink)}
.vt{display:grid;grid-template-columns:52mm 1fr 34px;gap:10px;align-items:end;padding:6px 0}
.vt span{display:flex;align-items:center;gap:10px;font:800 11pt var(--d)}
.vt i{display:block;height:24px;border-bottom:1.5px dashed var(--line-field)}
.vt b{font:800 11pt var(--d);color:var(--ink3)}
.vt.tot{border-top:2px solid var(--ink);margin-top:4px;padding-top:10px}
.vt.tot span{font-size:11.6pt}
.vt-note{margin-top:8px;font-size:9.6pt;color:var(--ink2)}
/* ===== copertina della parte seconda ===== */
.op2{background:var(--lilac);padding:0}
.op2-top{position:absolute;left:18mm;right:18mm;top:14mm;display:flex;justify-content:space-between;align-items:center}
.op2-body{position:absolute;left:18mm;right:18mm;top:44mm}
.op2-n{font:700 10pt var(--d);letter-spacing:.1em;text-transform:uppercase;padding-bottom:8px;border-bottom:2.5px solid var(--ink);display:inline-block}
.cover .op2-h{font:900 76pt/.92 var(--d);letter-spacing:-.05em;margin:12mm 0 8mm;max-width:none;color:var(--ink)}
.op2-sub{font:500 13pt/1.45 var(--t);max-width:120mm}
.op2-ill{position:absolute;left:18mm;right:18mm;top:146mm}
.op2-ill .ill{height:70mm;box-shadow:6px 6px 0 var(--ink);background:#fff}
.op2-toc{position:absolute;left:18mm;right:18mm;bottom:16mm;list-style:none;display:grid;grid-template-columns:repeat(4,1fr);gap:6px 14px;border-top:2.5px solid var(--ink);padding-top:10px}
.op2-toc li{font:700 9.4pt/1.3 var(--d)}
.op2-toc b{display:inline-block;width:26px;font-weight:900}
.op3{background:var(--teal)}
.op3 .ill{background:#eaf7f5}
.ill2{box-shadow:none;border-width:2px;margin:6px 0 14px;background:#f4f3ff}
/* ===== versione "documento": meno etichette, meno riquadri ===== */
.page:not(.cover) .tag{background:none;border:0;border-radius:0;padding:0;font:700 7.4pt/1.2 var(--d);letter-spacing:.1em;color:var(--ink3);gap:8px}
.page:not(.cover) .tag::before{content:"";width:18px;height:2px;background:var(--ink)}
.conto-n .tag::before{display:none}
.part{background:none;color:var(--ink);border-radius:0;padding:0 0 4px;border-bottom:2px solid var(--ink);font-size:7.2pt}
.card,.mixlist .card,.vs,.read,.book-box{background:none!important;border:0!important;box-shadow:none!important;border-radius:0!important;padding:0 0 0 14px!important;border-left:3px solid var(--line)!important}
.rule{background:none;border:0;box-shadow:none;border-radius:0;padding:4px 0 4px 16px;border-left:5px solid var(--yellow);margin:16px 0}
.rule .kick{color:var(--ink3)}
.box-end{background:none;border:0;box-shadow:none;border-radius:0;padding:14px 0 0;border-top:3px solid var(--ink)}
.prof{background:none;border:0;box-shadow:none;border-radius:0;overflow:visible;margin-top:16px}
.prof-h{background:none!important;border:0;padding:0 0 4px;border-bottom:2px solid var(--ink)}
.prof-b{padding:10px 0 0}
.sub>div{background:none!important;border:0!important;box-shadow:none!important;border-radius:0;padding:2px 0 2px 12px;border-left:3px solid var(--line)!important}
.sub .risk{border-left-color:#ff5a3c!important}
.sub .ok{border-left-color:var(--green)!important}
.ans div{background:none!important;border-radius:0;padding:3px 0 3px 12px;border-left-width:4px}
.read{grid-template-columns:34px 1fr;gap:12px;padding-left:0!important;border-left:0!important}
.read .n{width:30px;height:30px;border-radius:50%;font-size:12pt}
.reads{gap:18px!important}
.stats div{box-shadow:none;border-width:1.5px}
.tbl{box-shadow:none}
.mixlist{gap:14px}
.ill{box-shadow:none}
/* parte seconda: carta bianca, testatina, titoli sottolineati in lilla */
.p2{background:#fff;padding-top:24mm}
.p2::before{content:"Parte seconda · La formula";position:absolute;left:18mm;right:18mm;top:11mm;padding-bottom:6px;border-bottom:1px solid var(--line);font:700 7pt/1 var(--d);letter-spacing:.12em;text-transform:uppercase;color:var(--lilac)}
.p2 .hl{background:none;border-radius:0;padding:0;box-shadow:inset 0 -.32em 0 var(--lsoft)}
.p2 h2{font-size:23pt}
.p2 .part{display:none}
.p2 .rule{border-left-color:var(--lilac)}
.p2 .formula{box-shadow:5px 5px 0 var(--lilac)}
.p2 .foot{border-top:1px solid var(--line);padding-top:6px;bottom:8mm}
/* pagina 17: tabella dei nove hotel */
.htable{margin-top:6px;border-top:2px solid var(--ink)}
.hr{display:grid;grid-template-columns:22px 1.3fr 1.05fr 46px 76px;gap:10px;align-items:center;padding:8px 0;border-bottom:1px solid var(--line)}
.hh{font:700 6.8pt/1 var(--d);text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);padding:7px 0}
.hg{border-bottom:1.5px solid var(--ink)}
.hg .hr:last-child{border-bottom:0}
.hl2{width:22px;height:22px;border-radius:7px;background:var(--ink);color:var(--yellow);display:grid;place-items:center;font:900 10pt var(--d)}
.hn{font-size:8.6pt;line-height:1.35;color:var(--ink2)}
.hn b{display:block;font:800 9pt/1.3 var(--d);color:var(--ink)}
.hb{display:grid;gap:3px}
.hb i{display:grid;grid-template-columns:1fr 12px;gap:5px;align-items:center;font-style:normal}
.hb i b{display:block;height:6px;border-radius:9px;border:1px solid var(--ink)}
.hb i em{font:800 7pt var(--d);font-style:normal;text-align:right}
.hp{font:600 7.4pt var(--d);color:var(--ink3)}
.hp b{font:900 15pt var(--d);color:var(--ink)}
.hf{font:900 10.4pt var(--d);text-align:right;white-space:nowrap}
/* pagina 18: confronti in due colonne */
.vsgrid{display:grid;grid-template-columns:1fr 1fr;gap:16px 22px;margin-top:4px}
.vs2{border-top:2px solid var(--ink);padding-top:8px}
.vs2-h{display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;margin-bottom:5px}
.vs2-h b{font:900 13pt/1 var(--d)}
.vs2-h i{font-style:normal;font:800 11pt var(--d);color:var(--lilac)}
.vs2-h span{font:700 7.2pt/1.2 var(--d);text-transform:uppercase;letter-spacing:.06em;color:var(--ink3);margin-left:4px}
.vs2 p{font-size:9.2pt;line-height:1.5}
.vs2-law{margin-top:6px!important}
.vs2-law span{font:800 9.2pt/1.35 var(--d);box-shadow:inset 0 -.38em 0 var(--lsoft)}
.ending{margin-top:auto;background:var(--ink);color:#fff;border-radius:24px;padding:18px 22px;box-shadow:6px 6px 0 var(--yellow)}
.ending p{font:900 19pt/1.12 var(--d);letter-spacing:-.03em}
.ending p:last-of-type{color:var(--ink)}
.ending p:last-of-type span{background:var(--yellow);border-radius:7px;padding:0 .12em}
"""

def page(n, body, foot=True, cls=''):
    f = f'  <div class="foot"><span>{FOOT}</span><span class="n">{n}</span></div>\n' if foot else ''
    return f'<section class="page {cls}">\n{body}\n{f}</section>\n'

def scene(*lines):
    return '<div class="scene">' + ''.join(f'<p>{l}</p>' for l in lines) + '</div>'

def lines(*ls):
    return '<div class="lines">' + ''.join(f'<p>{l}</p>' for l in ls) + '</div>'

# --- illustrazioni (SVG semplici nei colori del design system) ---
INK, Y, L, T, PK, S, CR = '#262521', '#ffd22e', '#d8d6ff', '#bfe8e3', '#ffd3ea', '#f3efe9', '#faf7f4'

def svg(inner, bg=S):
    return f'<div class="ill"><svg viewBox="0 0 600 200" preserveAspectRatio="xMidYMid slice" xmlns="http://www.w3.org/2000/svg"><rect width="600" height="200" fill="{bg}"/>{inner}</svg></div>'

def ill_casello():
    road = f'<rect x="0" y="150" width="600" height="50" fill="#d9d2c7"/>' + ''.join(f'<rect x="{x}" y="172" width="34" height="6" rx="3" fill="#fff"/>' for x in range(10, 600, 70))
    roof = f'<rect x="140" y="38" width="320" height="22" rx="8" fill="{Y}" stroke="{INK}" stroke-width="3"/>'
    booths = ''.join(f'<rect x="{x}" y="60" width="52" height="90" rx="8" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="{x+10}" y="72" width="32" height="26" rx="5" fill="{L}" stroke="{INK}" stroke-width="2"/>' for x in (160, 274, 388))
    bars = ''.join(f'<rect x="{x+52}" y="112" width="58" height="8" rx="4" fill="#ff5a3c" stroke="{INK}" stroke-width="2"/>' for x in (160, 274))
    car = f'<rect x="40" y="118" width="90" height="34" rx="12" fill="{T}" stroke="{INK}" stroke-width="3"/><circle cx="62" cy="154" r="10" fill="{INK}"/><circle cx="108" cy="154" r="10" fill="{INK}"/>'
    coin = f'<circle cx="520" cy="80" r="34" fill="{Y}" stroke="{INK}" stroke-width="3"/><text x="520" y="91" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="28" fill="{INK}">15%</text>'
    return svg(road + roof + booths + bars + car + coin)

def ill_spiaggia():
    sea = f'<rect x="0" y="0" width="600" height="46" fill="{L}"/>'
    um = ''
    for r, y in enumerate(range(70, 200, 34)):
        for i, x in enumerate(range(22 + (r % 2) * 22, 600, 44)):
            me = (r == 2 and i == 7)
            c = Y if me else '#ff93c7'
            um += f'<circle cx="{x}" cy="{y}" r="13" fill="{c}" stroke="{INK}" stroke-width="{3 if me else 1.5}"/>'
    return svg(sea + um, bg='#f6e7c8')

def ill_sconto():
    tags = ''
    for i, (x, price) in enumerate([(40, '120 €'), (190, '110 €'), (340, '100 €'), (490, '90 €')]):
        c = '#fff' if i % 2 == 0 else PK
        tags += f'<g transform="rotate({-6 + i * 4} {x+40} 100)"><rect x="{x}" y="64" width="86" height="64" rx="12" fill="{c}" stroke="{INK}" stroke-width="3"/><circle cx="{x+16}" cy="80" r="5" fill="{INK}"/><text x="{x+43}" y="112" text-anchor="middle" font-family="Outfit" font-weight="900" font-size="22" fill="{INK}">{price}</text></g>'
    arrows = ''.join(f'<path d="M{x} 150 l24 14 l24 -14" fill="none" stroke="#ff5a3c" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>' for x in (100, 250, 400))
    return svg(tags + arrows)

def ill_vetrina():
    shops = ''
    for i, x in enumerate(range(20, 600, 116)):
        shops += f'<rect x="{x}" y="40" width="100" height="130" rx="10" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="{x}" y="40" width="100" height="22" rx="8" fill="{T}" stroke="{INK}" stroke-width="3"/><rect x="{x+14}" y="78" width="72" height="56" rx="6" fill="{S}" stroke="{INK}" stroke-width="2"/><text x="{x+50}" y="112" text-anchor="middle" font-family="Figtree" font-weight="700" font-size="12" fill="#6b665d">accogliente</text>'
    people = ''.join(f'<circle cx="{x}" cy="182" r="7" fill="{INK}"/>' for x in range(40, 600, 38))
    return svg(shops + people)

def ill_bagnino():
    sea = f'<rect x="0" y="0" width="600" height="70" fill="{L}"/><path d="M0 70 Q75 52 150 70 T300 70 T450 70 T600 70 V80 H0Z" fill="#fff"/>'
    sun = f'<circle cx="520" cy="40" r="24" fill="{Y}" stroke="{INK}" stroke-width="3"/>'
    poles = ''
    for i, x in enumerate((90, 200, 310, 420)):
        open_ = i == 0
        poles += f'<line x1="{x}" y1="110" x2="{x}" y2="180" stroke="{INK}" stroke-width="4"/>'
        if open_:
            poles += f'<path d="M{x-46} 112 Q{x} 70 {x+46} 112 Z" fill="{Y}" stroke="{INK}" stroke-width="3"/>'
        else:
            poles += f'<rect x="{x-6}" y="96" width="12" height="40" rx="5" fill="#ff93c7" stroke="{INK}" stroke-width="2"/>'
    return svg(sea + sun + poles, bg='#f6e7c8')


LIL, LS2 = '#8f8cff', '#d8d6ff'

def svg2(inner, h=''):
    return f'<div class="ill ill2"{h}><svg viewBox="0 0 600 200" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg"><rect width="600" height="200" fill="#f4f3ff"/>{inner}</svg></div>'

def ill_hotel_quattro():
    # un hotel fatto di quattro blocchi: le quattro componenti
    blocks = [(200, 130, 200, 38, LS2, 'Location'), (200, 90, 200, 38, T, 'Capitale'), (200, 50, 200, 38, PK, 'Operations'), (200, 10, 200, 38, Y, 'Narrativa')]
    out = '<rect x="0" y="170" width="600" height="30" fill="#e9e7ff"/>'
    for x, y, w, h, c, t in blocks:
        out += f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}" stroke="{INK}" stroke-width="3"/><text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="16" fill="{INK}">{t}</text>'
    return out

def ill_insegne():
    out = '<rect x="0" y="168" width="600" height="32" fill="#e9e7ff"/>'
    for i, (x, sign, c) in enumerate([(40, 'Rifugio romantico', PK), (225, 'Ritiro silenzioso', T), (410, 'Matrimoni piccoli', LS2)]):
        out += f'<rect x="{x+20}" y="70" width="110" height="98" rx="8" fill="#fff" stroke="{INK}" stroke-width="3"/>'
        out += ''.join(f'<rect x="{x+34+cx*30}" y="{86+cy*26}" width="20" height="16" rx="3" fill="{S}" stroke="{INK}" stroke-width="1.5"/>' for cx in range(3) for cy in range(3))
        out += f'<rect x="{x}" y="30" width="150" height="30" rx="15" fill="{c}" stroke="{INK}" stroke-width="3"/><text x="{x+75}" y="50" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="13" fill="{INK}">{sign}</text>'
        out += f'<line x1="{x+75}" y1="60" x2="{x+75}" y2="70" stroke="{INK}" stroke-width="3"/>'
    return out

def ill_motori():
    out = ''
    for i, (x, c, t, v) in enumerate([(30, LS2, 'Location', 9), (175, T, 'Capitale', 5), (320, PK, 'Operations', 6), (465, Y, 'Narrativa', 4)]):
        cx = x + 52
        out += f'<path d="M{cx-44} 140 A44 44 0 0 1 {cx+44} 140" fill="{c}" stroke="{INK}" stroke-width="3"/>'
        import math
        a = math.pi * (1 - v / 10)
        out += f'<line x1="{cx}" y1="140" x2="{cx + 34*math.cos(a):.1f}" y2="{140 - 34*math.sin(a):.1f}" stroke="{INK}" stroke-width="4" stroke-linecap="round"/><circle cx="{cx}" cy="140" r="6" fill="{INK}"/>'
        out += f'<text x="{cx}" y="172" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="14" fill="{INK}">{t}</text>'
    return out

def ill_venn():
    cs = [(230, 95, LS2, 'Location'), (300, 95, T, 'Capitale'), (230, 140, PK, 'Operations'), (300, 140, Y, 'Narrativa')]
    out = ''.join(f'<circle cx="{x}" cy="{y}" r="58" fill="{c}" fill-opacity=".75" stroke="{INK}" stroke-width="2.5"/>' for x, y, c, t in cs)
    out += ''.join(f'<text x="{x + (-100 if x < 265 else 100)}" y="{y + (-30 if y < 120 else 40)}" text-anchor="middle" font-family="Outfit" font-weight="800" font-size="14" fill="{INK}">{t}</text>' for x, y, c, t in cs)
    return out.replace('<circle', '<circle transform="translate(35 -18)"').replace('<text', '<text transform="translate(35 -18)"')

def ill_montagna():
    out = f'<path d="M0 200 L150 60 L240 140 L340 30 L470 150 L600 70 V200Z" fill="{LS2}" stroke="{INK}" stroke-width="3"/><path d="M315 54 L340 30 L365 54 L350 50 L340 60 L328 50Z" fill="#fff" stroke="{INK}" stroke-width="2"/>'
    out += f'<rect x="250" y="130" width="100" height="58" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/><path d="M240 132 L300 100 L360 132Z" fill="#ff5a3c" stroke="{INK}" stroke-width="3"/><rect x="290" y="156" width="20" height="32" fill="{S}" stroke="{INK}" stroke-width="2"/>'
    out += f'<g transform="translate(372 150)"><ellipse cx="0" cy="0" rx="22" ry="11" fill="{T}" stroke="{INK}" stroke-width="2.5"/><path d="M20 0 L34 -10 L34 10Z" fill="{T}" stroke="{INK}" stroke-width="2.5"/><circle cx="-10" cy="-2" r="2.5" fill="{INK}"/></g>'
    return out

TEAL = '#22a094'

def ill_lista():
    # un foglio con le due domande, una spuntata, e una matita
    out = '<rect x="0" y="0" width="600" height="200" fill="#eaf7f5"/>'
    out += f'<rect x="170" y="14" width="260" height="176" rx="14" fill="#fff" stroke="{INK}" stroke-width="3"/><rect x="250" y="6" width="100" height="20" rx="8" fill="{T}" stroke="{INK}" stroke-width="3"/>'
    for i, (t, ok) in enumerate([('La gestione tiene?', True), ('La voce più bassa?', False)]):
        y = 66 + i * 58
        out += f'<rect x="192" y="{y}" width="26" height="26" rx="7" fill="{Y if ok else "#fff"}" stroke="{INK}" stroke-width="2.5"/>'
        if ok:
            out += f'<path d="M198 {y+13} l6 6 l10 -12" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>'
        out += f'<text x="232" y="{y+19}" font-family="Outfit" font-weight="800" font-size="17" fill="{INK}">{i+1} · {t}</text>'
    out += f'<g transform="rotate(35 470 110)"><rect x="450" y="30" width="26" height="130" rx="4" fill="{Y}" stroke="{INK}" stroke-width="3"/><path d="M450 160 L463 190 L476 160Z" fill="#f6e7c8" stroke="{INK}" stroke-width="3"/><rect x="450" y="22" width="26" height="16" rx="4" fill="#ff93c7" stroke="{INK}" stroke-width="3"/></g>'
    return out

hotels_js = """
const H={
 A:['4 stelle a Positano, 25 camere','«Siamo a Positano, siamo accoglienti»',[10,6,6,3],'3,0 M€'],
 B:['Stesso hotel','«La casa positanese autentica»',[10,6,6,8],'4,5 M€'],
 C:['4 stelle a Cattolica, 50 camere','«Famiglia e divertimento»',[6,6,6,3],'1,3 M€'],
 D:['Stesso hotel','«L’hotel dei triatleti del circuito di Misano»',[6,6,6,9],'2,0 M€'],
 E:['4 stelle business, Milano Linate, 80 camere','Operations eccellenti',[5,6,9,7],'5,2 M€'],
 F:['4 stelle storico a Mantova, 30 camere','«Quattro generazioni di famiglia»',[5,5,7,9],'1,8 M€'],
 G:['3 stelle sulla Riviera del Conero, 22 camere','«Hotel di famiglia da sempre»',[6,4,5,2],'440.000 €'],
 H:['Agriturismo nel Monferrato, 10 camere','«Esperienza enogastronomica piemontese»',[4,5,5,3],'490.000 €'],
 I:['Stesso agriturismo','«La residenza del vignaiolo per enologi professionisti»',[4,5,5,9],'800.000 €']};
const C=['var(--lilac)','var(--teal)','var(--pink)','var(--yellow)'], N=['Location','Capitale','Operations','Narrativa'];
document.querySelectorAll('[data-htable]').forEach(box=>{
  const head=`<div class="hr hh"><span></span><span>Hotel e racconto</span><span>Le quattro leve</span><span>Posiz.</span><span>Fatturato</span></div>`;
  box.innerHTML=head+box.dataset.htable.split('|').map(g=>`<div class="hg">`+g.split(',').map(k=>{const [t,s,v,f]=H[k];const tot=v.reduce((a,b)=>a+b,0);
    return `<div class="hr"><span class="hl2">${k}</span><span class="hn"><b>${t}</b>${s}</span><span class="hb">${v.map((x,i)=>`<i title="${N[i]} ${x}"><b style="width:${x*10}%;background:${C[i]}"></b><em>${x}</em></i>`).join('')}</span><span class="hp"><b>${tot}</b>/40</span><span class="hf">${f}</span></div>`}).join('')+`</div>`).join('');
});
document.querySelectorAll('[data-hotels]').forEach(box=>{
  box.innerHTML=box.dataset.hotels.split(',').map(k=>{const [t,s,v,f]=H[k];const tot=v.reduce((a,b)=>a+b,0);
   return `<div class="ht"><div class="ht-h"><span class="ht-l">${k}</span><div class="ht-t">${t}<small>${s}</small></div></div>
   <div class="bars">${v.map((x,i)=>`<div class="bar">${N[i]}<i><b style="width:${x*10}%;background:${C[i]}"></b></i><span>${x}</span></div>`).join('')}</div>
   <div class="ht-f"><div class="pm">Il valore<b>${tot}</b></div><div class="rev">Fatturato stimato<br><b>${f}</b></div></div></div>`}).join('');
});
"""

P = []
# 1 · copertina
P.append(f'''<section class="page cover cv2">
  <div class="cv2-top"><span class="logo"><span class="mark"></span>Hotel Positioning</span><span class="cv2-meta">Guida pratica · 18 pagine</span></div>
  <div class="cv2-body">
    <p class="cv2-kick">Booking. L'agenzia. Il vicino che abbassa.</p>
    <h1 class="cv2-h">Il posizionamento,<br>spiegato semplice<br>a chi ha un hotel.</h1>
    <p class="cv2-sub">La guida per capire che hotel sei, prima di spendere un altro euro in marketing.</p>
  </div>
  <div class="cv2-photo"><span class="cv2-disc"></span><img src="cutout.png" alt=""></div>
  <div class="cv2-bottom">
    <div class="cv2-author"><span>Francesco Astolfi</span><small>Posizionamento per hotel e resort</small></div>
    <div class="cv2-formula"><span class="chip c-loc">Location</span><span class="chip c-cap">Capitale</span><span class="chip c-ops">Operations</span><span class="chip c-nar">Narrativa</span></div>
  </div>
  <div class="cv2-band"><span>Rimini · 2026</span><span>hotelpositioning.com</span></div>
</section>
''')

# 2 · la sera delle fatture
P.append(page(2, cls='conto', body=f'''  <span class="part">Parte prima · I conti</span>
  <span class="tag">00 · Prima di cominciare</span>
  <h2 class="big">A novembre <span class="hl">si fanno i conti.</span></h2>
  {scene("La stagione è chiusa.", "Le sdraio sono in magazzino.", "Sul tavolo della reception c'è una pila di fatture.")}
  {lines("Booking. L'agenzia. Il channel manager.", "Il fotografo, che le foto erano vecchie.", "Il sito nuovo, che quello vecchio non convertiva.")}
  {scene("Fai la somma.", "Poi guardi il fatturato.", "Poi rifai la somma, perché non ci credi.")}
  {lines("È stata una buona stagione.", "Pieno ad agosto. Bene a luglio.", "Eppure in tasca resta meno di cinque anni fa.")}
  <p class="law">Non hai lavorato meno. <span class="hl">Hai pagato più persone.</span></p>
  <div style="margin-top:16px">{lines("Nelle prossime pagine ci sono i cinque conti che un hotel indipendente paga ogni anno.", "Alcuni li vedi in fattura. Altri no.", "<b>Quelli che non vedi sono i più cari.</b>")}</div>'''))

def conto(n, num, title, ill, body):
    return page(n, f'''  <span class="conto-n"><b>{num}</b><span class="tag">Conto {num}</span></span>
  <h2 class="big">{title}</h2>
  {ill}
{body}''', cls='conto')

P.append(conto(3, '01', 'Il <span class="hl">casello.</span>', ill_casello(), f'''  {scene("Booking è un casello autostradale.", "Paghi ogni volta che passi.", "Anche se la strada l'hai costruita tu.")}
  {lines("Il 15%, spesso di più con i programmi di visibilità.", "Su ogni notte. Su ogni ospite.", "Anche su quello che ti conosceva già.", "Anche su quello che ti ha cercato per nome, e ha trovato prima Booking di te.")}
  <div style="margin-top:10px">{lines("Non è un furto. È un servizio.", "Booking ti porta ospiti che da solo non vedresti.", "Il problema non è pagarlo.")}</div>
  <p class="law"><span class="hl">Il problema è pagarlo per tutti.</span></p>
  <div style="margin-top:12px">{scene("Un hotel che vive di Booking è come un negozio dentro un centro commerciale.", "Se cambiano l'affitto, cambia la tua vita.", "E l'affitto non lo decidi tu.")}</div>'''))

P.append(conto(4, '02', 'Il mare <span class="hl">d\'agosto.</span>', ill_spiaggia(), f'''  {scene("Guardi la spiaggia dall'alto ad agosto.", "File di ombrelloni. Stesso colore. Stessa distanza.", "Prova a dire quale è il tuo.")}
  {lines("Apri Booking. Cerca la tua zona.", "Cinquanta rettangoli.", "Stesse piscine, stesse stelle, stesse foto della colazione.")}
  <p style="margin-top:10px">E sotto, sempre le stesse parole:</p>
  <div class="chips" style="margin:8px 0 10px;gap:6px"><span class="chip" style="background:#fff;text-decoration:line-through;color:var(--ink3)">accogliente</span><span class="chip" style="background:#fff;text-decoration:line-through;color:var(--ink3)">confortevole</span><span class="chip" style="background:#fff;text-decoration:line-through;color:var(--ink3)">immerso nel verde</span><span class="chip" style="background:#fff;text-decoration:line-through;color:var(--ink3)">a due passi dal mare</span></div>
  <div class="card" style="margin-top:4px"><span class="kick" style="display:block;margin-bottom:5px">Il test del logo</span><p>Copri il logo della tua homepage. Poi copri quello del vicino. Se le due frasi si possono scambiare, per l'ospite siete lo stesso hotel.</p></div>
  <div style="margin-top:12px">{lines("E tra due hotel uguali, l'ospite fa l'unica cosa sensata.", "Guarda il prezzo.")}</div>
  <p class="law"><span class="hl">Se sembri uguale, il prezzo lo fanno i tuoi concorrenti.</span></p>'''))

P.append(conto(5, '03', 'Il vicino abbassa <span class="hl">di dieci euro.</span>', ill_sconto(), f'''  {scene("Lo vedi sul channel manager.", "O te lo dice la ragazza della reception.", "E tu abbassi. Se no, scelgono lui.")}
  {lines("Funziona una settimana.", "Poi lui abbassa ancora.", "Poi tu.", "È una gara in cui vince chi perde più margine.")}
  <div class="rule" style="margin:12px 0"><span class="kick">Fai il conto, una volta sola</span><b>Dieci euro in meno, su quaranta camere, per cento notti: sono quarantamila euro.</b><p>Il rifacimento dei bagni. Lo stipendio di una persona in più. Regalati a un ospite che, il giorno dopo, non ricorda il nome dell'hotel.</p></div>
  {scene("Lo sconto è come l'aspirina.", "Toglie la febbre.", "Non toglie l'infezione.")}
  <p class="law"><span class="hl">Lo sconto è il prezzo di un motivo che non hai.</span></p>'''))

P.append(conto(6, '04', 'Più clic. <span class="hl">Stessa vetrina.</span>', ill_vetrina(), f'''  {scene("Hai cambiato agenzia.", "Quella nuova aveva i grafici più belli.", "Dopo sei mesi, i grafici sono saliti. Le prenotazioni no.")}
  {lines("Non è sempre colpa dell'agenzia.", "L'agenzia fa quello per cui la paghi: porta gente.", "Ma la porta su una pagina uguale ad altre cinquanta.")}
  <div style="margin-top:10px">{lines("L'ospite arriva. Guarda. Non trova un motivo.", "Torna su Booking a confrontare il prezzo.", "E prenota lì. Magari proprio da te. Con la commissione.")}</div>
  <div style="margin-top:12px">{scene("È come fare pubblicità a un negozio con la vetrina uguale a quella accanto.", "La gente entra.", "Poi compra dove costa meno.")}</div>
  <p class="law">Non hai un problema di traffico. <span class="hl">Hai un problema di motivo.</span></p>
  <p style="margin-top:6px">Il traffico si compra. Il motivo va costruito.</p>'''))

P.append(conto(7, '05', 'Ad aprile si rimettono <span class="hl">gli ombrelloni.</span>', ill_bagnino(), f'''  {scene("Ogni primavera il bagnino rifà la spiaggia.", "Le mareggiate d'inverno si sono portate via tutto.", "Si ricomincia dalla sabbia.")}
  {lines("Per tanti hotel i clienti funzionano così.", "Ad aprile si riparte da zero.", "Nuove campagne. Nuove offerte. Nuove commissioni.")}
  <div style="margin-top:10px">{lines("L'ospite dell'anno scorso è stato bene.", "Ha lasciato una buona recensione.", "Ma non ricorda perché ha scelto te.", "Ricorda il prezzo. E dove l'ha trovato.")}</div>
  <div style="margin-top:10px">{lines("Quindi quest'anno ti ricerca su Booking.", "E tu lo ripaghi. Lo stesso ospite. Due volte.")}</div>
  <p class="law"><span class="hl">Chi non ricorda perché ti ha scelto, la prossima volta sceglie il prezzo.</span></p>'''))

P.append(page(8, cls='conto', body=f'''  <span class="tag">Il conto totale</span>
  <h2 class="big">Cinque conti. <span class="hl">Una causa.</span></h2>
  <table class="tbl"><thead><tr><th>Il conto</th><th>Cosa sembra</th><th>Cosa è</th></tr></thead><tbody>
    <tr><td>01 · Booking</td><td>Un costo di distribuzione</td><td>Paghi per ospiti che non hanno un motivo per cercarti da te</td></tr>
    <tr><td>02 · Tutti uguali</td><td>Un problema di comunicazione</td><td>Il mercato non vede la differenza</td></tr>
    <tr><td>03 · Lo sconto</td><td>Una scelta commerciale</td><td>L'unica leva che resta quando non c'è un motivo</td></tr>
    <tr><td>04 · L'agenzia</td><td>Un fornitore sbagliato</td><td>Traffico portato su un messaggio identico agli altri</td></tr>
    <tr><td>05 · Ripartire</td><td>La stagionalità</td><td>Un ospite che non ha un motivo per tornare</td></tr>
  </tbody></table>
  {lines("Sembrano cinque problemi.", "Con cinque fornitori diversi da pagare.")}
  <p class="law" style="margin-top:12px">È uno solo.</p>
  {scene("Il mercato non vede un motivo per sceglierti.")}
  {lines("E quando il motivo non c'è, decide il prezzo.", "Il prezzo lo decide qualcun altro.")}
  <div class="rule" style="margin-top:16px"><span class="kick">Il nome</span><b>Quel motivo ha un nome: posizionamento.</b><p>Nelle prossime pagine trovi la formula del valore del tuo hotel. E la voce che puoi cambiare da lunedì.</p></div>'''))

# --- parte seconda (v3 corta: la formula, un esempio, un caso vero, la regola)

P.append('''<section class="page cover op2">
  <div class="op2-top"><span class="logo"><span class="mark"></span>Hotel Positioning</span><span class="cv2-meta">Il posizionamento, spiegato semplice</span></div>
  <div class="op2-body">
    <p class="op2-n">Parte seconda</p>
    <h1 class="op2-h">La formula.</h1>
    <p class="op2-sub">Quattro voci decidono quanto l'ospite paga per scegliere te. Una sola si cambia da lunedì.</p>
  </div>
  <div class="op2-ill">''' + svg2(ill_hotel_quattro()) + '''</div>
  <ol class="op2-toc"><li><b>01</b>La formula del valore</li><li><b>02</b>Un esempio</li><li><b>03</b>Un caso vero</li><li><b>04</b>La regola</li></ol>
</section>
''')

# --- icone dei profili (SVG in un cerchio colorato)
ICONS = {
 'loc': '<path d="M24 8c-7 0-12 5-12 12 0 9 12 20 12 20s12-11 12-20c0-7-5-12-12-12z" fill="#fff" stroke="#262521" stroke-width="3"/><circle cx="24" cy="20" r="4.5" fill="#262521"/>',
 'cap': '<rect x="10" y="16" width="28" height="24" rx="3" fill="#fff" stroke="#262521" stroke-width="3"/><path d="M8 18 L24 7 L40 18" fill="none" stroke="#262521" stroke-width="3" stroke-linejoin="round"/><rect x="16" y="22" width="6" height="6" fill="#262521"/><rect x="26" y="22" width="6" height="6" fill="#262521"/><rect x="21" y="32" width="6" height="8" fill="#262521"/>',
 'ops': '<path d="M12 32 a12 12 0 0 1 24 0 z" fill="#fff" stroke="#262521" stroke-width="3"/><rect x="9" y="32" width="30" height="5" rx="2" fill="#262521"/><circle cx="24" cy="17" r="2.5" fill="#262521"/>',
 'nar': '<path d="M9 12 h30 a3 3 0 0 1 3 3 v15 a3 3 0 0 1 -3 3 h-17 l-8 7 v-7 h-5 a3 3 0 0 1 -3 -3 v-15 a3 3 0 0 1 3 -3z" fill="#fff" stroke="#262521" stroke-width="3" stroke-linejoin="round"/><path d="M15 20h18M15 26h12" stroke="#262521" stroke-width="3" stroke-linecap="round"/>',
}
def icon(k, bg, size=46):
    return f'<span class="ico" style="background:{bg};width:{size}px;height:{size}px"><svg viewBox="0 0 48 48" width="{size-12}" height="{size-12}">{ICONS[k]}</svg></span>'

def voce(k, bg, title, text, extra=''):
    return f'<div><div style="display:flex;align-items:center;gap:10px">{icon(k, bg, 40)}<h4 style="margin:0">{title}</h4></div><p style="margin-top:8px">{text}</p>{extra}</div>'

P.append(page(10, f'''  <span class="tag">01 · La formula</span>
  <h2>Un hotel <span class="hl">non è una cosa sola.</span></h2>
  <p>Quello che l'ospite è disposto a pagare dipende da quattro voci.</p>
  <div class="formula">
    <span class="kick">La formula del valore del tuo hotel</span>
    <div class="chips"><span class="chip c-loc">Location</span><span class="op">+</span><span class="chip c-cap">Capitale</span><span class="op">+</span><span class="chip c-ops">Operations</span><span class="op">+</span><span class="chip c-nar">Narrativa</span></div>
    <div class="res"><span class="op">=</span><span class="chip">Il valore commerciale del tuo hotel</span><em>quanto l'ospite è disposto a pagare per sceglierti</em></div>
  </div>
  <div class="two" style="gap:14px 22px">
    {voce('loc', 'var(--lsoft)', 'Location · dove sei.', 'Portofino vende da sola. L\'entroterra no. Non la sposti.')}
    {voce('cap', 'var(--tsoft)', 'Capitale · cosa hai costruito.', 'Camere rifatte nel 2024, o moquette del 2003. Si cambia con un mutuo.', '<p style="margin-top:4px"><em>Nessun racconto salva un bagno brutto.</em></p>')}
    {voce('ops', 'var(--psoft)', 'Operations · come lavori ogni giorno.', 'Il check-in, la pulizia, le risposte alle recensioni. Si sistema in qualche stagione.')}
    {voce('nar', 'var(--yellow)', 'Narrativa · come ti racconti.', 'La ragione precisa per cui l\'ospite sceglie te. E paga il prezzo che chiedi.')}
  </div>
  <p class="law"><span class="hl">È l'unica voce che cambi da lunedì. Senza toccare un mattone.</span></p>
  <div style="margin-top:10px">{lines("Con tutte e quattro basse, ti scelgono solo per prezzo.", "Basta una voce alta per uscire dal mucchio.", "Quale, dipende dal tuo hotel. Lo scopri a pagina 15.")}</div>'''))

P.append(page(11, f'''  <span class="tag">02 · Un esempio</span>
  <h2>Stesso hotel. Altro racconto. <span class="hl">Altro conto.</span></h2>
  <p class="lead">Un quattro stelle a Cattolica. Cinquanta camere.</p>
  <div class="legend" style="margin-top:8px"><span><i style="background:var(--lilac)"></i>Location</span><span><i style="background:var(--teal)"></i>Capitale</span><span><i style="background:var(--pink)"></i>Operations</span><span><i style="background:var(--yellow)"></i>Narrativa</span></div>
  <div class="hotels" data-hotels="C,D" style="margin-top:10px"></div>
  <div class="two" style="margin-top:12px">
    <div><span class="num">C</span><p style="margin-top:6px">«Famiglia e divertimento». Come altri cinquanta sulla stessa costa.</p></div>
    <div><span class="num">D</span><p style="margin-top:6px">Stesso hotel. «L'hotel dei triatleti del circuito di Misano». Deposito bici, nutrizionista sportivo, accordi con il circuito, apertura lunga per le gare d'autunno.</p></div>
  </div>
  <div style="margin-top:14px">{lines("Le altre tre voci non si sono mosse.", "Nessun mutuo. Nessun cantiere.")}</div>
  <p class="law"><span class="hl">Si è mossa la voce che si cambia da lunedì.</span></p>
  <p class="small" style="margin-top:12px"><em>Esempio inventato per spiegare il metodo. Non è un hotel reale, e non è un risultato promesso. Il fatturato dipende anche da camere, giorni di apertura e tariffa possibile.</em></p>'''))

def libro_box(da, testo, cta='Il libro su Amazon →'):
    return f'<div class="book-box" style="margin-top:16px"><img src="libro.webp" alt="" style="width:22mm;flex:none;border:2px solid var(--ink);border-radius:4px"><div><span class="kick" style="display:block;margin-bottom:4px">Nel libro</span><p>{testo}</p><a class="btn" href="https://hotelpositioning.com/vai/libro/?da={da}">{cta}</a> <span class="url">hotelpositioning.com/vai/libro</span></div></div>'

P.append(page(12, f'''  <span class="tag">03 · Un caso vero</span>
  <h2>Fuori <span class="hl">dagli esempi.</span></h2>
  <p class="lead">Al <b>Silva Splendid di Fiuggi</b> il lavoro sul posizionamento ha portato a una scelta che quasi nessuno ha lo stomaco di fare: <em>meno tipi di ospite, non di più.</em></p>
  <div class="stats" style="margin:14px 0 12px;grid-template-columns:repeat(2,1fr)">
    <div><b>5,6 → 7 M€</b><span>fatturato in cinque anni*</span></div>
    <div><b>~×2</b><span>tariffa media</span></div>
    <div><b>8,6 → 9</b><span>recensioni su Booking</span></div>
    <div style="background:var(--psoft)"><b>5,8%</b><span>quanto costa un ospite diretto, su quello che spende</span></div>
  </div>
  {scene("Gli interni li rifanno tutti.", "Cambiare cosa dice l'hotel, quasi nessuno.")}
  {libro_box('guida-p12', 'Cosa hanno tolto. In che ordine. Con quali parole. Il caso completo è nel capitolo 10. Insieme al Veridia Resort di Chia.')}
  <p class="small" style="margin-top:14px"><em>*Nello stesso periodo c'è stata una ristrutturazione, con investimenti importanti della proprietà. Il posizionamento ha dato la direzione, gli investimenti l'hanno resa credibile.</em></p>'''))

P.append(page(13, f'''  <span class="tag">04 · La regola</span>
  <h2>Prima le operations. <span class="hl">Dopo il racconto.</span></h2>
  <p class="lead">Il racconto è una promessa. La gestione la paga, ogni giorno.</p>
  <div class="ans" style="margin-top:12px">
    <div class="no">Prometti silenzio, e il wifi in camera prende benissimo? <b>Promessa tradita.</b></div>
    <div class="no">Prometti cucina del territorio, e il cuoco cambia ogni tre mesi? <b>Promessa tradita.</b></div>
    <div class="no">Prometti un servizio su misura, e alle recensioni negative risponde un messaggio automatico? <b>Promessa tradita.</b></div>
  </div>
  <div style="margin-top:14px">{lines("Se la gestione non tiene, il racconto non porta valore.", "Moltiplica il danno.")}</div>
  <div class="rule" style="margin-top:16px"><span class="kick">Regola operativa</span><b>Recensioni sotto 4,3 su 5 (8,6 su Booking)? Staff che cambia ogni stagione? Prezzi decisi a sensazione?</b><p>Prima si sistema la gestione. Poi si lavora sul racconto.</p></div>'''))

# --- parte terza
def q(n, title, body, ans):
    return f'<div class="q"><span class="n">{n}</span><div><h3>{title}</h3>{body}<div class="ans">{ans}</div></div></div>'

P.append('''<section class="page cover op2 op3">
  <div class="op2-top"><span class="logo"><span class="mark"></span>Hotel Positioning</span><span class="cv2-meta">Il posizionamento, spiegato semplice</span></div>
  <div class="op2-body">
    <p class="op2-n">Parte terza</p>
    <h1 class="op2-h">Tocca a te.</h1>
    <p class="op2-sub">Due domande, dieci minuti, una penna. Alla fine sai quale voce ti tiene sul prezzo.<br><b>1 · La gestione tiene?</b><br><b>2 · Qual è la voce più bassa?</b></p>
  </div>
  <div class="op2-ill">''' + svg2(ill_lista()) + '''</div>
  <ol class="op2-toc"><li><b>05</b>L'autodiagnosi</li><li><b>06</b>E adesso?</li><li><b>·</b>Chi lo fa</li><li><b>·</b>Il prossimo passo</li></ol>
</section>
''')

P.append(page(15, f'''
  <span class="tag">05 · L'autodiagnosi</span>
  <h2>Due domande <span class="hl">prima di spendere un euro.</span></h2>
  <p class="lead">Rispondi con onestà. Nessuno ti guarda.</p>
  {q(1, 'La gestione tiene?', '<p>Guarda le recensioni degli ultimi due anni su Google, Booking e TripAdvisor. La media è sopra 4,3 su 5 (8,6 su Booking)? Lo staff è stabile? Rispondi in fretta a recensioni e segnalazioni?</p>', '<div class="no"><b>Se no:</b> il racconto non è la tua priorità adesso. Prima la gestione (pagina 13).</div><div class="si"><b>Se sì:</b> passa alla domanda due.</div>')}
  {q(2, 'Qual è la voce più bassa?', '<p>Dai un voto da zero a dieci a ognuna delle quattro voci. Senza barare.</p>', '<div class="n1"><b>La voce più alta è il tuo motore.</b> Il racconto deve farla crescere.</div><div class="n2"><b>La voce più bassa ti dice dove guardare.</b></div><div class="n3"><b>Se sono tutte tra sei e sette, nessuna che spicca:</b> la voce da alzare è la narrativa. È l\'unica che cambi da lunedì.</div>')}
  <div class="votes"><span class="kick">I voti del tuo hotel, oggi</span>
    <div class="vt"><span>{icon('loc','var(--lsoft)',30)}Location</span><i></i><b>/10</b></div>
    <div class="vt"><span>{icon('cap','var(--tsoft)',30)}Capitale</span><i></i><b>/10</b></div>
    <div class="vt"><span>{icon('ops','var(--psoft)',30)}Operations</span><i></i><b>/10</b></div>
    <div class="vt"><span>{icon('nar','var(--yellow)',30)}Narrativa</span><i></i><b>/10</b></div>
    <div class="vt tot"><span>Il valore del tuo hotel, oggi</span><i></i><b>/40</b></div>
  </div>'''))

P.append(page(16, f'''  <span class="tag">06 · E adesso?</span>
  <h2>Hai trovato la voce. <span class="hl">E adesso?</span></h2>
  {lines("Ricordi la pila di fatture?", "Booking. Tutti uguali. Lo sconto. L'agenzia. Ripartire da zero.", "Adesso sai da dove vengono.", "<b>Da un motivo per sceglierti che l'ospite non vede.</b>")}
  <div style="margin-top:10px">{scene("È come quando il meccanico ti dice: «È la frizione.»", "Bene. Adesso sai cos'è.", "Ma la macchina è ancora ferma.")}</div>
  {lines("Sapere quale voce alzare è metà del lavoro.", "L'altra metà è il come.")}
  <p style="margin-top:8px"><b>Nel libro il come sta in sei domande.</b> Le stesse che uso con gli hotel che seguo.</p>
  <div class="formula" style="margin:10px 0 8px"><span class="kick">I sei passaggi</span>
    <ol style="margin:4px 0 0 18px;padding:0;font-size:10.6pt;line-height:1.55">
      <li>Che problema, o che desiderio profondo, ha il tuo ospite?</li>
      <li>Che alternative ha, oltre a te?</li>
      <li>Quali unicità hai? E che valore producono?</li>
      <li>A chi interessa davvero quel valore?</li>
      <li>Di quale categoria puoi essere il leader?</li>
      <li>C'è un trend che ti spinge?</li>
    </ol>
  </div>
  <p><em>Le risposte non sono in questa guida. Sono nel tuo hotel.</em></p>
  {lines("Il libro ti insegna a tirarle fuori.", "Con La TAC: le tue recensioni, quelle dei vicini, il tuo sito.", "Con il Positioning Canvas, per fissare tutto su una pagina.", "Poi le trasformi in parole, per sito e campagne.", "E hai gli otto strumenti per farlo da solo.")}
  <p style="margin-top:10px"><a class="btn" href="https://hotelpositioning.com/vai/libro/?da=guida-p16">Prendi il libro su Amazon · 19,90 € →</a> <span class="url">hotelpositioning.com/vai/libro</span></p>
  <p class="small" style="margin-top:8px">Se invece la prima risposta è stata no, il libro può aspettare. Sistema prima la gestione.</p>'''))
P.append(page(17, f'''  <span class="tag">Chi lo fa</span>
  <h2>Francesco Astolfi. <span class="hl">Vent'anni di hotel, da ogni lato.</span></h2>
  <div class="bio">
    <div class="ph"><img src="francesco.jpg" alt="Francesco Astolfi"></div>
    <div>
      <div class="stats" style="margin-top:0">
        <div><b>0 → 30 M€</b><span>TUI.it</span></div>
        <div><b>20 hotel</b><span>marketing di Atahotels</span></div>
        <div><b>10 locali</b><span>aperti con i miei soldi</span></div>
      </div>
      {lines("Ho portato TUI.it da zero a trenta milioni.", "Ho guidato il marketing di Atahotels, venti strutture.", "Ho diretto una web agency che lavorava solo per hotel.", "Poi ho aperto dieci locali con i miei soldi.")}
      <p style="margin-top:10px">So cosa vuol dire guardare il conto a fine stagione e vedere quanto è andato in commissioni.</p>
      <p>Ogni smontaggio e ogni analisi li faccio io, a mano. Per questo gli smontaggi gratuiti sono al massimo sei al mese.</p>
      <div class="rule" style="margin-top:14px"><b>I consulenti vendono consigli. Gli operatori vendono cicatrici.</b></div>
      <img src="firma.png" alt="Firma di Francesco Astolfi" style="height:18mm;margin-top:6px">
    </div>
  </div>'''))

P.append(page(18, f'''  <span class="tag">Il prossimo passo</span>
  <h2>La guida ti dice dove sei. <span class="hl">Il libro, come si cambia.</span></h2>
  <div class="cta b" style="display:grid;grid-template-columns:34mm 1fr;gap:14px;align-items:start;margin-top:12px">
    <img src="libro.webp" alt="Copertina del libro Hotel Positioning" style="width:100%;border:2px solid var(--ink);border-radius:6px;box-shadow:3px 3px 0 var(--ink)">
    <div>
      <span class="tag" style="background:#fff">Il libro · 19,90 €</span>
      <h3>Hotel Positioning. Il metodo in sei passaggi.</h3>
      <p class="small">Il metodo completo per trovare il motivo per cui l'ospite sceglie il tuo hotel. E scriverlo.</p>
      <ul>
        <li><span>Le sei domande, una per una, con un esempio passo per passo.</span></li>
        <li><span>La TAC e il Positioning Canvas.</span></li>
        <li><span>Il caso Silva e il caso Veridia, per intero.</span></li>
        <li><span>Otto strumenti gratuiti da usare sul tuo hotel.</span></li>
      </ul>
      <p class="small"><b>Costa meno di una notte in una delle tue camere.</b></p>
      <a class="btn" href="https://hotelpositioning.com/vai/libro/?da=guida-fine">Prendi il libro su Amazon →</a>
      <span class="url">hotelpositioning.com/vai/libro</span>
    </div>
  </div>
  <div class="cta a" style="margin-top:10px">
    <span class="tag" style="background:var(--tsoft)">Gratis · fatto a mano</span>
    <h3 style="font-size:12pt">Hai più di 40 camere e preferisci che lo guardi io?</h3>
    <p class="small">Lo smontaggio della tua homepage: la tua prima riga accanto a quelle di 2-3 concorrenti, a logo coperto. Un verdetto e un indizio. Una pagina, scritta da me.</p>
    <p class="meta">Massimo 6 al mese · dalle 40 camere · in 3 giorni lavorativi</p>
    <a class="btn" href="https://hotelpositioning.com/#richiedi">Richiedi lo smontaggio →</a> <span class="url">hotelpositioning.com/#richiedi</span>
  </div>
  <div class="ending" style="margin-top:8mm">
    <span class="logo" style="color:#fff;margin-bottom:10px;display:flex"><span class="mark w"></span>Hotel Positioning</span>
    <p>Booking si paga.</p><p>L'agenzia si paga.</p><p>Lo sconto si paga.</p><p style="margin-top:4px"><span>Il motivo, una volta sola.</span></p>
  </div>'''))

_a = next(i for i, x in enumerate(P) if 'op2"' in x and 'Parte seconda' in x)
_b = next(i for i, x in enumerate(P) if 'op3' in x)
P = [x.replace('<section class="page', '<section class="page p2', 1) if _a < i < _b else x for i, x in enumerate(P)]
import re as _re
ROOMY = ('01 · La formula', '02 · Un esempio', '03 · Un caso vero', '04 · La regola', "05 · L'autodiagnosi", '06 · E adesso?')
P = [x.replace('<section class="page', '<section class="page roomy', 1) if any(f'<span class="tag">{t}</span>' in x for t in ROOMY) else x for x in P]
P = [_re.sub(r'(<span class="n">)\d+(</span></div>\n</section>)', lambda m, n=i + 1: m.group(1) + str(n) + m.group(2), x) for i, x in enumerate(P)]

html = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<title>{TITLE} · Francesco Astolfi</title>
<style>{CSS}{EXTRA_CSS}</style>
</head>
<body>
{''.join(P)}
<script>{hotels_js}</script>
</body>
</html>
'''
(HERE / 'guida.html').write_text(html)
print(len(P), 'pagine')
