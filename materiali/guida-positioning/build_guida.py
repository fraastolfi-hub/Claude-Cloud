#!/usr/bin/env python3
"""Compone guida.html (copy v2, 26 pagine) a partire da base.css e dai testi qui sotto.
Uso: python3 build_guida.py && node pdf.mjs"""
from pathlib import Path

HERE = Path(__file__).parent
CSS = (HERE / "base.css").read_text()
TITLE = "Il tuo hotel paga tutti"
FOOT = "Hotel Positioning · Il tuo hotel paga tutti"

EXTRA_CSS = """
.part{background:var(--ink);color:#fff;border-radius:999px;padding:5px 13px;font:800 7.6pt/1 var(--d);letter-spacing:.08em;text-transform:uppercase;align-self:flex-start;margin-bottom:10px}
.big{font:900 34pt/1.02 var(--d);letter-spacing:-.035em;margin:8px 0 14px}
.scene{font:italic 500 12.4pt/1.6 var(--t);color:var(--ink2);border-left:4px solid var(--yellow);padding-left:14px;margin:6px 0 14px}
.scene p+p{margin-top:2px}
.lines p{margin:0}
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
.book-box p{font-size:9.6pt;line-height:1.45}
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
.cover .cv2-h{font:900 82pt/.9 var(--d);letter-spacing:-.05em;margin:12mm 0 9mm;color:var(--ink);max-width:none}
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
.p2::before{content:"Parte seconda · Come funziona";position:absolute;left:18mm;right:18mm;top:11mm;padding-bottom:6px;border-bottom:1px solid var(--line);font:700 7pt/1 var(--d);letter-spacing:.12em;text-transform:uppercase;color:var(--lilac)}
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
   <div class="ht-f"><div class="pm">Posizionamento<b>${tot}</b></div><div class="rev">Fatturato stimato<br><b>${f}</b></div></div></div>`}).join('');
});
"""

P = []
# 1 · copertina
P.append(f'''<section class="page cover cv2">
  <div class="cv2-top"><span class="logo"><span class="mark"></span>Hotel Positioning</span><span class="cv2-meta">Guida pratica · 26 pagine</span></div>
  <div class="cv2-body">
    <p class="cv2-kick">Booking. L'agenzia. Il vicino che abbassa.</p>
    <h1 class="cv2-h">Il tuo hotel<br>paga tutti.</h1>
    <p class="cv2-sub">Che hotel sei, quale leva fa davvero il tuo fatturato, e perché senza un motivo per sceglierti resta solo il prezzo.</p>
  </div>
  <div class="cv2-photo"><span class="cv2-disc"></span><img src="cutout.png" alt=""></div>
  <div class="cv2-bottom">
    <div class="cv2-author"><img src="firma.png" alt="Firma di Francesco Astolfi"><span>Francesco Astolfi</span><small>Posizionamento per hotel e resort</small></div>
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
  <p class="law"><span class="hl">Se sembri uguale, costi di meno.</span></p>'''))

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
  <div class="rule" style="margin-top:16px"><span class="kick">Il nome</span><b>Quel motivo ha un nome: posizionamento.</b><p>Nelle prossime pagine vediamo da cosa è fatto, e quale parte puoi cambiare da lunedì.</p></div>'''))

# --- parte seconda
P.append(page(9, f'''  <span class="part">Parte seconda · Come funziona</span>
  <span class="tag">01 · Le basi</span>
  <h2>Un hotel <span class="hl">non è una cosa sola.</span></h2>
  <p>Quello che il mercato pensa del tuo hotel è la somma di quattro cose.</p>
  <div style="margin-top:8px">{lines("Dove sei.", "Cosa hai costruito.", "Come lavori ogni giorno.", "Come ti racconti.")}</div>
  <div class="formula">
    <span class="kick">La formula</span>
    <div class="chips"><span class="chip c-loc">Location</span><span class="op">+</span><span class="chip c-cap">Capitale</span><span class="op">+</span><span class="chip c-ops">Operations</span><span class="op">+</span><span class="chip c-nar">Narrativa</span></div>
    <div class="res"><span class="op">=</span><span class="chip">Posizionamento di mercato</span><em>come ti vede il cliente</em></div>
  </div>
  {lines("Puoi vincere con una sola componente molto alta e le altre nella media.", "Puoi vincere con due o tre alte.", "Con tutte e quattro alte vinci quasi sempre. Ma succede di rado.", "Con tutte e quattro basse non vinci mai: sei un hotel che si sceglie solo per prezzo.")}
  <p style="margin-top:12px">Due parole che si confondono spesso. Il <b>posizionamento di mercato</b> è il risultato: come ti percepisce il cliente. La <b>narrativa</b> è una delle quattro componenti: come scegli di raccontarti.</p>
  <p>Location, capitale e operations cambiano in anni, o con investimenti importanti.</p>
  <p class="law"><span class="hl">La narrativa è l'unica che puoi cambiare in fretta, senza toccare i mattoni.</span></p>'''))

def comp(n, cls, title, body):
    return f'<div class="comp"><span class="kick"><span class="chip {cls}" style="font-size:7pt;padding:3px 8px">Componente {n}</span></span><h3>{title}</h3>{body}</div>'

P.append(page(10, f'''  <span class="tag">02 · Le componenti</span>
  <h2>Quattro componenti. <span class="hl">Tre costano anni.</span></h2>
  {comp(1, 'c-loc', 'Dove sei: la location', '<p>La location non è un indirizzo. È il flusso di clienti che arriva da solo. È il nome che la gente riconosce al bar.</p><p><b>Portofino, Capri, Positano, Venezia centro, Taormina:</b> location da dieci. L\'hotel vende prima ancora che il proprietario apra bocca.</p><p><b>Rimini, Jesolo, Senigallia, Caorle:</b> da sei o sette. I flussi ci sono, ma la tua fetta te la devi prendere.</p><p><b>Un quattro stelle a Modena, Padova, Brescia:</b> da cinque. Lavoro e cultura, nessuna cartolina.</p><p><b>Un paese dell\'entroterra abruzzese o del Monferrato:</b> da tre o quattro. Qui la location non ti aiuta, ti frena. Chi arriva, arriva per un motivo preciso.</p>')}
  {comp(2, 'c-cap', 'Cosa hai costruito: il capitale', '<p>Il capitale è quanto hai investito nella struttura. Non il valore dell\'immobile: la qualità che il cliente sente quando entra in camera, apre il bagno, si siede al ristorante.</p><p>Camere rifatte nel 2024 con un investimento serio dicono una cosa. Moquette del 2003 e materasso stanco ne dicono un\'altra. Qualunque cosa ci sia scritto sulla brochure.</p>')}
  <div class="rule"><span class="kick">Regola uno</span><b>Il capitale pesa moltissimo nei primi tre minuti. Nessun racconto salva un bagno brutto.</b></div>'''))

P.append(page(11, f'''  {comp(3, 'c-ops', 'Come lavori ogni giorno: le operations', '<p>Le operations sono il lavoro di tutti i giorni. Il check-in. La pulizia, uguale il lunedì e il sabato. La colazione puntuale. Le risposte alle recensioni. I prezzi che seguono il mercato. Lo staff formato. I fornitori.</p><p>Un hotel nella media con operations eccellenti sopravvive e cresce. Un hotel bellissimo con operations scadenti brucia la reputazione in diciotto mesi.</p><p><b>Sono la componente che i proprietari sottovalutano di più. E quella che conta di più nel lungo periodo.</b></p>').replace('class="comp"', 'class="comp" style="margin-top:0"', 1)}
  <div style="height:10px"></div>
  {comp(4, 'c-nar', 'Come ti racconti: la narrativa', '<p>La narrativa è la promessa che fai al mercato. Il cliente che scegli di servire. La ragione precisa per cui deve scegliere te, e pagare il prezzo che chiedi.</p><p>Un hotel senza narrativa è un hotel generico. Il prezzo lo decide Booking. Nessuno ha un motivo per sceglierlo al posto del vicino. Puoi avere location, struttura e staff buoni: il risultato resta basso, perché manca il quarto addendo.</p><p>Una narrativa forte si appoggia su qualcosa di vero. La storia della famiglia. Un modo di lavorare che hai solo tu. Un cliente molto specifico. Una presa di posizione contro quello che fanno tutti.</p><p>Non è uno slogan. È una scelta che decide cosa offri, a chi, come organizzi il lavoro e come comunichi.</p>')}
  <p class="law"><span class="hl">E una volta scelta, va mantenuta ogni giorno.</span></p>'''))

P.append(page(12, f'''  <span class="tag">03 · La scelta</span>
  <h2>Due hotel uguali. <span class="hl">Due racconti.</span></h2>
  <p>Un quattro stelle, dieci camere, su una collina umbra. Può essere:</p>
  <div class="chips" style="margin:10px 0 10px;gap:8px">
    <span class="chip" style="background:var(--psoft)">Il rifugio romantico per coppie</span>
    <span class="chip" style="background:var(--tsoft)">Il ritiro silenzioso per professionisti che non staccano mai</span>
    <span class="chip" style="background:var(--lsoft)">La casa di campagna per matrimoni piccoli</span>
  </div>
  {lines("Stesse camere. Stesso staff. Stesso mutuo.", "<b>Clienti diversi. Prezzi diversi. Posizionamento diverso.</b>")}
  <div class="rule" style="margin-top:16px"><span class="kick">Il punto</span><b>Il racconto giusto non è il più bello. È quello coerente con le altre tre componenti.</b><p>La narrativa deve amplificare quello che hai. Oppure creare valore dove le altre componenti non arrivano.</p></div>
  <div class="card" style="background:var(--white);margin-top:6px">
    <span class="kick" style="display:block;margin-bottom:6px">Un caso vero, non un esempio</span>
    <p>Al <b>Silva Splendid di Fiuggi</b> il lavoro sul posizionamento ha portato a una scelta che quasi nessuno ha lo stomaco di fare: meno tipi di ospite, non di più.</p>
    <div class="stats" style="margin:12px 0 10px;grid-template-columns:repeat(4,1fr)">
      <div><b>5,6 → 7 M€</b><span>fatturato in cinque anni*</span></div>
      <div><b>~×2</b><span>tariffa media</span></div>
      <div><b>8,6 → 9</b><span>recensioni su Booking</span></div>
      <div style="background:var(--psoft)"><b>5,8%</b><span>quanto costa un ospite diretto, su quello che spende</span></div>
    </div>
    <p class="small"><em>*Nello stesso periodo c'è stata una ristrutturazione, con investimenti importanti della proprietà. Il posizionamento ha dato la direzione, gli investimenti l'hanno resa credibile.</em></p>
  </div>'''))

def prof(color, label, title, body, ok, risk):
    return f'''<div class="prof"><div class="prof-h" style="background:{color}">{label}</div><div class="prof-b"><h3>{title}</h3>{body}<div class="sub"><div class="ok"><span class="kick">Racconto coerente</span>{ok}</div><div class="risk"><span class="kick">Rischio</span>{risk}</div></div></div></div>'''

P.append(page(13, f'''  <span class="tag">04 · I profili</span>
  <h2>Qual è il motore <span class="hl">del tuo hotel?</span></h2>
  <p class="lead">Ci sono quattro profili, uno per componente. Capire il tuo cambia la risposta a due domande: dove investire, e cosa raccontare.</p>
  <div class="chips" style="margin:12px 0 4px;gap:8px"><span class="chip c-loc">Profilo location</span><span class="chip c-cap">Profilo capitale</span><span class="chip c-ops">Profilo operations</span><span class="chip c-nar">Profilo narrativa</span></div>
  {prof('var(--lsoft)', 'Profilo location', 'Il motore è il luogo', '<p>Location da nove o dieci, il resto nella media o sotto. Una piccola struttura a Positano, investimenti modesti, gestione familiare, racconto ancora da fare.</p><p>Il cliente paga per vivere Positano. L\'hotel è il mezzo, non il protagonista.</p>', 'Il luogo come identità. «Siamo Positano.» «La vera Capri.» Arredi, colazione, bar: tutto deve raccontare quel posto. Quello vero, non quello delle cartoline.', 'Dipendi tutto dal turismo della zona. Se la zona cala, non hai un piano B. Col tempo conviene costruire anche altro.')}'''))

P.append(page(14, f'''  {prof('var(--tsoft)', 'Profilo capitale', 'Il motore è la struttura', '<p>Capitale da nove o dieci, il resto nella media. Un hotel in una zona secondaria con un restauro da diversi milioni, o un edificio nuovo che si fa notare. Gestione ancora in rodaggio.</p><p>Il cliente paga per la bellezza dello spazio, che nella zona non trova altrove.</p>', 'L\'investimento come promessa. «Il posto più bello della regione.» «Un design che non trovi altrove.»', 'Un investimento così chiede tariffe alte per rientrare. Se la reception non è all\'altezza della hall, l\'ospite si sente preso in giro alla prima richiesta.').replace('class="prof"', 'class="prof" style="margin-top:0"', 1)}
  {prof('var(--psoft)', 'Profilo operations', 'Il motore è il lavoro fatto bene, sempre', '<p>Operations da nove o dieci, il resto nella media. Un hotel in città o sulla costa, in una zona senza cartolina. Struttura curata ma senza grandi investimenti. Prezzi gestiti con attenzione, staff stabile, recensioni seguite una per una, colazione curata, pulizia senza eccezioni.</p><p>Il cliente paga per non pensarci.</p>', 'L\'affidabilità come promessa. Fuori dall\'Italia lo fanno citizenM («il tuo hotel ovunque tu vada») e YOTEL, tutti e due costruiti su una gestione impeccabile.', '«Qualità del servizio» lo scrivono tutti. Per distinguerti devi trasformare l\'eccellenza in cose che si vedono e si possono nominare. Non in aggettivi.')}'''))

P.append(page(15, f'''  <div class="prof" style="margin-top:0"><div class="prof-h" style="background:var(--yellow)">Profilo narrativa</div><div class="prof-b">
    <h3>Il motore è come ti racconti</h3>
    <p>Narrativa da nove o dieci, il resto nella media o sotto. Le operations però devono stare almeno a sei o sette. Sotto quella soglia nessun racconto regge.</p>
    <p><b>Due casi tipici.</b> Il primo: l'hotel di famiglia con una storia vera. «Quattro generazioni.» «Qui dal 1897.» La storia c'è già. La narrativa la mette in parole e la trasforma in promessa.</p>
    <p>Il secondo: l'hotel senza cartolina, senza grandi investimenti e senza una storia di famiglia, che ha scelto un racconto netto e specifico. Non «hotel di charme per famiglie»: quello lo dicono in cento. Qualcosa come «l'hotel dei triatleti che si allenano al circuito di Misano».</p>
    <p><b>Due casi italiani.</b> L'Eremito, in Umbria: ritiro con silenzio obbligatorio, menu unico vegetariano, niente wifi, niente televisione. Location difficile, investimenti contenuti. Il racconto fa il lavoro che le altre componenti non possono fare, con tariffe sopra i 300 euro.</p>
    <p>Sextantio, a Santo Stefano di Sessanio, in Abruzzo: Daniele Kihlgren ha trasformato un borgo quasi abbandonato nel «lusso dell'imperfezione», un albergo diffuso conosciuto in tutto il mondo.</p>
    <div class="sub"><div class="ok" style="background:var(--ysoft)"><span class="kick">Come si costruisce</span>Scegli un cliente molto preciso. Fagli una promessa netta. Sostienila con scelte che si vedono: menu, orari, servizi, divieti. Il racconto si costruisce con le scelte di ogni giorno, non con gli slogan.</div><div class="risk"><span class="kick">Rischio</span>Un racconto forte che la gestione non mantiene è peggio di nessun racconto. Diventa un contratto da onorare ogni mattina.</div></div>
  </div></div>
  <div class="book-box"><div><span class="kick" style="display:block;margin-bottom:4px">Per approfondire</span><p>Come si passa da un fatto vero del tuo hotel a un racconto che regge? È il cuore del libro. Sei passaggi, i casi veri, e otto strumenti per applicarli.</p><a class="btn" href="https://hotelpositioning.com/vai/libro/?da=guida-p15">Il libro su Amazon →</a> <span class="url">hotelpositioning.com/vai/libro</span></div></div>'''))

def mix(chips, text):
    return f'<div class="card"><div class="chips">{chips}</div><p>{text}</p></div>'

P.append(page(16, f'''  <span class="tag">05 · I profili misti</span>
  <h2>I profili puri <span class="hl">sono rari.</span></h2>
  <p class="lead">Quasi tutti gli hotel hanno due o tre componenti alte. Qui il racconto deve parlare dell'incrocio, non di una sola componente.</p>
  <div class="mixlist">
    {mix('<span class="chip c-loc">Location alta</span><b>+</b><span class="chip c-cap">Capitale alto</span>', 'Struttura di lusso recente in una location da cartolina. L\'Hotel Caruso, prima di LVMH. Il racconto è vivere il luogo attraverso l\'investimento. Attenzione che la gestione non diventi il punto debole.')}
    {mix('<span class="chip c-loc">Location alta</span><b>+</b><span class="chip c-nar">Narrativa alta</span>', 'Casa Cipriani a Milano: location forte, e un racconto («l\'ambasciata di Venezia») costruito sulla storia vera della famiglia Cipriani dal 1931. Il racconto non sta sotto la location: la fa crescere.')}
    {mix('<span class="chip c-ops">Operations alte</span><b>+</b><span class="chip c-nar">Narrativa alta</span>', 'The Pig, in Inghilterra: il fondatore Robin Hutson ha trasformato «l\'imperfezione curata» in un modo di lavorare. Da noi è l\'hotel storico di famiglia in una città d\'arte minore: gestione rigorosa più «quattro generazioni di ospitalità».')}
    {mix('<span class="chip c-cap">Capitale alto</span><b>+</b><span class="chip c-ops">Operations alte</span>', 'Hotel moderno, investimento serio, gestione professionale, in una zona secondaria. Il racconto è «quello che non ti aspetti dove non te lo aspetti». Qui l\'hotel può diventare il motivo del viaggio.')}
    <div class="card" style="background:var(--ysoft)"><div class="chips"><span class="chip c-loc">Location</span><span class="chip c-cap">Capitale</span><span class="chip c-ops">Operations</span><span class="chip c-nar">Narrativa</span><b style="font:800 8.4pt var(--d)">tutte e quattro alte</b></div><p>Il lusso dove tutto funziona. Il racconto qui non salva niente: tira fuori il valore che resta sul tavolo. Belmond, Rocco Forte, Baglioni ci investono di continuo. La differenza si misura in milioni di fatturato in più all'anno.</p></div>
  </div>'''))

P.append(page(17, f'''  <span class="tag">06 · Nove hotel</span>
  <h2>Stesso hotel. Altro racconto. <span class="hl">Altro conto.</span></h2>
  <p class="small">Nove hotel inventati, per vedere il metodo al lavoro. Ogni componente da zero a dieci. Il posizionamento di mercato è la somma, da zero a quaranta. Il fatturato dipende dal posizionamento, ma anche da camere, giorni di apertura e tariffa possibile in quel segmento. <b>Esempi per spiegare il metodo. Non sono hotel reali, e non sono risultati promessi.</b></p>
  <div class="legend" style="margin-top:4px"><span><i style="background:var(--lilac)"></i>Location</span><span><i style="background:var(--teal)"></i>Capitale</span><span><i style="background:var(--pink)"></i>Operations</span><span><i style="background:var(--yellow)"></i>Narrativa</span></div>
  <div class="htable" data-htable="A,B|C,D|E|F|G|H,I"></div>'''))

def vs(a, b, sub, text, law=''):
    head = f'<b>{a}</b>' + (f' <i>→</i> <b>{b}</b>' if b else '') + f'<span>{sub}</span>'
    return f'<div class="vs2"><div class="vs2-h">{head}</div><p>{text}</p>' + (f'<p class="vs2-law"><span>{law}</span></p>' if law else '') + '</div>'

P.append(page(18, f'''  <span class="tag">I confronti</span>
  <h2>Sei confronti, <span class="hl">una lezione.</span></h2>
  <div class="vsgrid">
  {vs('A', 'B', 'stesso hotel, stessa Positano', 'Stesse camere, stesso staff. Cambia solo il racconto. A dice «siamo a Positano, siamo accoglienti», come tutti. B è «la casa positanese autentica»: oggetti del paese, menu solo locale, arredi che raccontano Positano, uscite in barca con i pescatori del porto. Il posizionamento passa da 25 a 30. Nell\'esempio, un milione e mezzo in più con le stesse tre componenti.', 'Il racconto ha fatto crescere la location.')}
  {vs('C', 'D', 'stesso hotel, stessa Cattolica', 'C è «famiglia e divertimento», come altri cinquanta sulla stessa costa. D è «l\'hotel dei triatleti del circuito di Misano»: deposito bici, nutrizionista sportivo, accordi con il circuito, pacchetti di allenamento, apertura lunga per le gare d\'autunno. Il posizionamento passa da 21 a 27. Nell\'esempio, settecentomila euro in più e trenta giorni di apertura in più.', 'Il racconto ha trasformato un hotel come tanti in uno specialista.')}
  {vs('A', 'E', 'Positano contro Linate', 'Positano apre 180 giorni l\'anno. Linate 360, con operations eccellenti e un racconto chiaro. Il posizionamento è simile, 25 e 27. Ma Linate fattura quasi il doppio: ha 80 camere contro 25, e lavora il doppio dei giorni.', 'Il posizionamento dice quanto è forte l\'hotel. Il fatturato dipende anche da dimensione e stagione.')}
  {vs('F', '', 'l\'hotel storico di Mantova', 'Non vince su location e struttura. Ha operations buone e una storia di famiglia vera: quattro generazioni. La storia non è una componente a parte. È la base su cui il racconto costruisce la promessa. Posizionamento 26, un milione e otto con sole 30 camere, da clienti che pagano di più per qualcosa che non si copia.')}
  {vs('G', '', 'il tre stelle del Conero', '22 camere, quasi solo estate, 440 mila euro. Posizionamento 17. Non sbaglia niente di grave. Ma non ha leve: vive del turismo che passa. Un racconto preciso, come «l\'hotel di chi fa immersioni nel Parco del Conero» o «la casa degli escursionisti del Monte Conero», porterebbe la narrativa da 2 a 8. Nell\'esempio il fatturato supera i 600 mila euro, con clienti che oggi scelgono altrove.')}
  {vs('H', 'I', 'lo stesso agriturismo nel Monferrato', 'Dieci camere, gestione familiare, la cantina di casa. H vende «esperienza enogastronomica piemontese», come altri cinquanta agriturismi della zona. I è «la residenza del vignaiolo per enologi professionisti»: un workshop all\'anno con una cantina diversa, visite tecniche per gruppi di enologi stranieri, settimane dedicate a un singolo produttore. Il posizionamento passa da 17 a 23. Nell\'esempio, 310 mila euro in più.', 'Il racconto funziona anche nel piccolo. Se è abbastanza preciso.')}
  </div>'''))

P.append(page(19, f'''  <span class="tag">Da portare via</span>
  <h2>Quattro cose <span class="hl">da ricordare.</span></h2>
  <div class="reads">
    <div class="read"><span class="n">1</span><p>Il posizionamento di mercato è la somma di quattro componenti. La narrativa è una delle quattro. Può essere la leva principale, o amplificare le altre. In tutti e due i casi sposta i numeri.</p></div>
    <div class="read"><span class="n">2</span><p>Un posizionamento alto non vuol dire automaticamente fatturato alto. Contano anche camere, giorni di apertura e tariffa possibile. Un hotel piccolo e fortissimo può fatturare meno di uno grande nella media. Positano e Linate, appunto.</p></div>
    <div class="read"><span class="n">3</span><p>La location da cartolina non basta. Molti proprietari in zone secondarie se la prendono con la location. Spesso il problema è altrove: nel racconto che non c'è.</p></div>
    <div class="read"><span class="n">4</span><p>Negli esempi, lo stesso hotel con un racconto diverso fattura dal 35% a oltre il 60% in più. Dal lusso all'agriturismo da dieci camere. Ed è l'unica leva che non chiede di rifare i muri.</p></div>
  </div>'''))

P.append(page(20, f'''  <span class="tag">07 · Le regole</span>
  <h2>Due regole <span class="hl">che valgono per tutti.</span></h2>
  <h3>Regola uno · La gestione deve mantenere la promessa</h3>
  <p style="margin-top:6px">Il racconto crea un'aspettativa. La gestione la paga, ogni giorno.</p>
  <div class="ans" style="margin-top:10px">
    <div class="no">Prometti silenzio e niente wifi, e il wifi in camera prende benissimo? Promessa tradita.</div>
    <div class="no">Prometti cucina del territorio, e il cuoco cambia ogni tre mesi? Promessa tradita.</div>
    <div class="no">Prometti un servizio su misura, e alle recensioni negative risponde un messaggio automatico? Promessa tradita.</div>
  </div>
  <p style="margin-top:12px">Se la gestione non tiene, il racconto non porta valore. Moltiplica il danno. Gli ospiti arrivati per la promessa ripartono delusi. E scrivono recensioni proprio su quello che avevi promesso.</p>
  <p class="small" style="margin-top:8px">Selina, la catena di spazi per lavorare in viaggio, è l'esempio: racconto fortissimo, gestione che non reggeva, crescita troppo veloce. Nel 2024 è finita in amministrazione controllata.</p>
  <div class="rule" style="margin-top:14px"><span class="kick">Regola operativa</span><b>Prima le operations. Dopo il racconto.</b><p>Se le recensioni non stanno sopra 4,3 su 5 (8,6 su Booking), lo staff non è stabile, i prezzi non seguono il mercato e le criticità non hanno risposta rapida: un racconto forte non è la mossa giusta. Prima si sistema la gestione. Poi si lavora sul racconto.</p></div>'''))

P.append(page(21, f'''  <h3>Regola due · Il racconto deve stare dentro un mercato che esiste</h3>
  <p style="margin-top:8px">C'è anche la trappola opposta: un racconto così di nicchia che i clienti non bastano.</p>
  <div class="card" style="margin-top:12px"><span class="kick" style="display:block;margin-bottom:6px">Il caso Saorsa 1875</span><p>In Scozia, è stato il primo hotel completamente vegano del Regno Unito. Un racconto perfetto, sulla carta. Ma undici camere, Pitlochry fuori mano e prezzi alti per una cucina vegetale rigorosa hanno trovato un mercato troppo piccolo. I proprietari lo hanno messo in vendita, e l'agenzia incaricata lo presentava anche come hotel da aprire a un'offerta più ampia del solo vegano.</p></div>
  <div style="margin-top:14px">{scene("È come aprire una trattoria di solo pesce crudo in montagna.", "Magari è la migliore d'Italia.", "Ma il sabato sera devi riempire i tavoli.")}</div>
  <div class="rule"><span class="kick">Il punto</span><b>Il racconto deve restringere abbastanza da darti un'identità. Non così tanto da chiuderti la porta.</b></div>
  <p>Se la location è debole e le camere sono poche, prima di partire verifica che i clienti raggiungibili bastino a coprire il fatturato minimo.</p>
  <p><b>Spesso la soluzione non è un racconto meno netto. È un racconto altrettanto netto, su un tema con più clienti.</b></p>'''))

# --- parte terza
def q(n, title, body, ans):
    return f'<div class="q"><span class="n">{n}</span><div><h3>{title}</h3>{body}<div class="ans">{ans}</div></div></div>'

P.append(page(22, f'''  <span class="part">Parte terza · Tocca a te</span>
  <span class="tag">08 · L'autodiagnosi</span>
  <h2>Tre domande <span class="hl">prima di spendere un euro.</span></h2>
  <p class="lead">Rispondi con onestà. Nessuno ti guarda.</p>
  {q(1, 'La gestione tiene?', '<p>Guarda le recensioni degli ultimi due anni su Google, Booking e TripAdvisor. La media è sopra 4,3 su 5 (8,6 su Booking)? Lo staff è formato e stabile? I prezzi seguono il mercato? Rispondi in fretta a recensioni e segnalazioni?</p>', '<div class="no"><b>Se no:</b> il racconto non è la tua priorità adesso. Prima la gestione. Un racconto forte oggi ti farebbe più male che bene.</div><div class="si"><b>Se sì:</b> passa alla domanda due.</div>')}
  {q(2, 'Qual è il tuo profilo?', '<p>Dai un voto da zero a dieci a ognuna delle quattro componenti. Senza barare. Sommale: è il tuo posizionamento di oggi.</p>', '<div class="n1"><b>Una componente domina</b> (una a nove o dieci, le altre sotto sette): il racconto deve amplificare quella. Sei un profilo location, capitale, operations o narrativa.</div><div class="n2"><b>Due o tre componenti alte:</b> il racconto deve parlare dell\'incrocio. Sei un profilo misto.</div><div class="n3"><b>Tutte tra sei e sette, nessuna che spicca:</b> la leva da costruire è il racconto. È l\'unica che puoi cambiare in fretta, senza grandi investimenti.</div>')}'''))

P.append(page(23, f'''  {q(3, 'I clienti bastano?', '<p>Pensa al racconto che hai in mente, coerente con il tuo profilo. I clienti raggiungibili, per distanza e per capacità di spesa, bastano a farti stare in piedi?</p><div class="formula" style="margin:12px 0"><span class="kick">Il conto è semplice</span><div class="chips"><span class="chip" style="background:#fff">Camere</span><span class="op">×</span><span class="chip" style="background:#fff">Occupazione obiettivo</span><span class="op">×</span><span class="chip" style="background:#fff">Giorni di apertura</span><span class="op">×</span><span class="chip" style="background:#fff">Tariffa media obiettivo</span></div><div class="res"><span class="op">=</span><span class="chip">Fatturato minimo</span></div></div><p>Poi chiediti: ci sono abbastanza persone, per quel racconto, nel bacino che riesci a raggiungere?</p>', '<div class="si"><b>Se sì:</b> procedi.</div><div class="no"><b>Se no:</b> sposta il racconto su un tema con più clienti, prima di investire.</div>').replace('class="q"', 'class="q" style="margin-top:0"', 1)}'''))

P.append(page(24, f'''  <span class="tag">09 · Il prossimo passo</span>
  <h2>Torna alla pila <span class="hl">di fatture.</span></h2>
  {lines("Ricordi i cinque conti dell'inizio?", "Booking. Tutti uguali. Lo sconto. L'agenzia. Ripartire da zero.")}
  <div style="margin-top:10px">{lines("Adesso sai da dove vengono.", "Non da Booking, non dall'agenzia, non dal vicino.", "<b>Da un motivo per sceglierti che il mercato non vede.</b>")}</div>
  <p style="margin-top:10px">Il racconto giusto dipende dal tuo profilo. Un hotel che vive della location racconta il luogo. Uno che vive della gestione racconta l'affidabilità. Uno senza cartolina e senza grandi investimenti ha bisogno di un racconto netto, che crei valore dove le altre componenti non arrivano.</p>
  <p>Chi ti vende lo stesso racconto per ogni hotel, non ti ha guardato. Prima si capisce il profilo. Poi si sceglie il racconto. Poi si controlla che la gestione lo mantenga e che i clienti bastino.</p>
  <p>Se dopo le tre domande il racconto è la tua leva, il passo dopo è scegliere quale. Ne esistono una cinquantina, osservati in Italia e all'estero. Scegliere quello giusto per te è un lavoro di diagnosi, e serve uno sguardo da fuori. Se vuoi provarci da solo, il metodo completo è nel libro. Dalla diagnosi alle parole, un passaggio alla volta.</p>
  <p style="margin-top:8px"><a class="btn" href="https://hotelpositioning.com/vai/libro/?da=guida-p24">Prendi il libro su Amazon →</a></p>
  <p style="margin-top:10px">Se invece la prima risposta è stata no, il racconto può aspettare. Sistema prima quello che va sistemato.</p>
  <div class="box-end"><b>In tutti e due i casi hai fatto la cosa più importante: hai capito di cosa ha bisogno il tuo hotel, adesso.</b><p><em>Quasi nessuno lo fa prima di firmare con un'altra agenzia. Tu sì.</em></p></div>'''))

P.append(page(25, f'''  <span class="tag">Chi lo fa</span>
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

P.append(page(26, f'''  <span class="tag">Il prossimo passo</span>
  <h2>Due modi <span class="hl">per andare avanti.</span></h2>
  <p class="lead">Se vuoi sapere come ti vede l'ospite oggi, parti dallo smontaggio. Se vuoi il metodo completo da applicare da solo, parti dal libro.</p>
  <div class="ctas">
    <div class="cta a">
      <span class="tag" style="background:var(--tsoft)">Gratis · fatto a mano</span>
      <h3>Lo smontaggio della tua homepage</h3>
      <p class="small">Copro i loghi e leggo le prime righe come un ospite che non vi conosce. Una pagina, scritta da me. Niente accessi, niente password.</p>
      <ul>
        <li><span><b>Il confronto:</b> la prima riga della tua homepage accanto a quelle di 2-3 concorrenti, con il logo coperto.</span></li>
        <li><span><b>Il verdetto:</b> posizionato, sostituibile o invisibile. Con il perché.</span></li>
        <li><span><b>L'indizio:</b> dove sta, probabilmente, il tuo motivo.</span></li>
      </ul>
      <p class="meta">Massimo 6 al mese · hotel e resort dalle 40 camere · in 3 giorni lavorativi</p>
      <a class="btn" href="https://hotelpositioning.com/#richiedi">Richiedi lo smontaggio gratuito →</a>
      <span class="url">hotelpositioning.com/#richiedi</span>
    </div>
    <div class="cta b">
      <span class="tag" style="background:#fff">Il libro · 19,90 €</span>
      <h3>Hotel Positioning. Il metodo in sei passaggi</h3>
      <p class="small">Il metodo completo per trovare il motivo per cui l'ospite sceglie il tuo hotel, e scriverlo. Con otto strumenti gratis per applicarlo.</p>
      <ul>
        <li><span>Il metodo in sei passaggi, dalla diagnosi alle parole.</span></li>
        <li><span>Otto strumenti gratuiti da usare sul tuo hotel.</span></li>
        <li><span>Per strutture di ogni dimensione, anche sotto le 40 camere.</span></li>
      </ul>
      <a class="btn" href="https://hotelpositioning.com/vai/libro/?da=guida-fine">Prendi il libro su Amazon →</a>
      <span class="url">hotelpositioning.com/vai/libro</span>
    </div>
  </div>
  <div class="ending" style="margin-top:12mm">
    <span class="logo" style="color:#fff;margin-bottom:10px;display:flex"><span class="mark w"></span>Hotel Positioning</span>
    <p>Booking si paga.</p><p>L'agenzia si paga.</p><p>Lo sconto si paga.</p><p style="margin-top:4px"><span>Il motivo, una volta sola.</span></p>
  </div>'''))

P = [x.replace('<section class="page', '<section class="page p2', 1) if 8 <= i <= 20 else x for i, x in enumerate(P)]

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
