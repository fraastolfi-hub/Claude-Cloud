# Static ads «primo capitolo gratis» per la Riviera Romagnola (route A, CSS).
# Design system: il tema editoriale del sito (site/src/assets/editoriale.css), riportato in scala 1080 px.
#   carta #fcfbf8 · sabbia #f2efe8 · foglio #fff · inchiostro #15181c · grafite #4a4f57 · nebbia #6f747c
#   linea #e3e1db · linea forte #c9c6be · notte #121a22 / #1b2530 · testo su notte #eef0f2 / #b8c0c8
#   giallo #ffd22e solo come firma (sottolineatura della parola chiave, un solo elemento acceso)
#   titoli Newsreader 500, -0.012em · testo Figtree · etichette Figtree 600 maiuscolo .14em con trattino
#   niente ombre, filetti sottili, raggi piccoli · logo: segno a barre + «Hotel Positioning» Figtree 600
# Prodotte con la skill creative-statics-hospitality (metodo Creative Statics Kit di Simone Dassereto).
# Uso: python3 genera_ads.py <cartella_output>   poi render con Chrome headless (1080x1350 e 1080x1920).
import base64, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ASSETS = HERE.parent.parent / 'site/src/assets'
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)

def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(Path(p).read_bytes()).decode()
NEWS = b64(ASSETS / 'fonts/newsreader.woff2', 'font/woff2'); FIG = b64(ASSETS / 'fonts/figtree.woff2', 'font/woff2')
COVER = b64(HERE / 'copertina-pdf.png', 'image/png')
FOTO = b64(ASSETS / 'img/francesco-libro@2x.webp', 'image/webp')
CARTA, SABBIA, NOTTE = '#fcfbf8', '#f2efe8', '#121a22'

# ---------- illustrazioni (diagrammi, non foto) ----------
def grid():
    return '<div class="grid">' + ''.join(f'<i class="{"me" if k == 23 else ""}"></i>' for k in range(50)) + '</div>'

def chat():
    return '''<div class="chat"><div class="q">Dove dormo due notti a Riccione, in un posto tranquillo?</div>
<div class="a"><p>Ti consiglio questi tre:</p><ol><li><i>xxxxxxxxxxxx</i></li><li><i>xxxxxxxxxx</i></li><li><i>xxxxxxxxxxxxx</i></li></ol></div></div>'''

def timer():
    return '<div class="tm"><div class="dial"><b>10</b><span>secondi</span></div><div class="bub2">«Boh, sembra carino.»</div></div>'

def bikes():
    rows = ''.join(f'<div class="row"><div class="ph"></div><div class="rt"><b>Hotel <i class="bl">xxxxxxxx</i></b><span>Riviera · ★★★</span><em>Noleggio bici</em></div><div class="pr"><small>{sc}</small><b>{p}</b></div></div>'
                   for p, sc in (('89 €', '8,4'), ('92 €', '8,5'), ('86 €', '8,3')))
    return f'<div class="phone"><div class="pbar"><span>Riviera Romagnola</span><small>tutti con le bici</small></div>{rows}</div>'

def calendar():
    def month(name, full, tag, on):
        cells = ''.join(f'<i class="{"on" if k in full else ""}"></i>' for k in range(31))
        return f'<div class="mo"><div class="mh"><b>{name}</b><span class="{"t-on" if on else ""}">{tag}</span></div><div class="days">{cells}</div></div>'
    return '<div class="cal">' + month('Agosto', set(range(31)), 'Completo', True) + month('Maggio', {4, 5, 11, 12, 25}, '5 notti su 31', False) + '</div>'

def amenities():
    li = ''.join(f'<li>{t}</li>' for t in ('Aria condizionata', 'Wi-Fi', 'Parcheggio', 'A due passi dal mare'))
    return '<div class="ams">' + ''.join(f'<div class="am"><b>Hotel <i class="bl">xxxxxx</i></b><ul>{li}</ul></div>' for _ in range(4)) + '</div>'

COPY = {
 'B1': dict(h='Trova <em>il tuo hotel.</em>', sub='Su Booking sei <b>un rettangolo su cinquanta.</b>', vis=grid),
 'B2': dict(h='L’AI ne nomina<br><em>due o tre.</em>', sub='Se sembri uguale agli altri, <b>non ci sei proprio.</b>', vis=chat),
 'C1': dict(h='Il test dei<br><em>dieci secondi.</em>', sub='Se rispondono così, <b>per l’ospite sei invisibile.</b>', vis=timer),
 'D2': dict(h='Più bici <em>non ti fanno scegliere.</em>', sub='Oltre un certo livello l’ospite <b>non somma: sottrae.</b>', vis=bikes),
 'E1': dict(h='Ad agosto dici no.<br><em>E a maggio?</em>', sub='<b>È il no che fa il prezzo,</b> non il sì.', vis=calendar),
 'E4': dict(h='Ce l’hanno <em>tutti.</em>', sub='Il wi-fi <b>non è un motivo per sceglierti.</b>', vis=amenities),
}
# famiglia 1: illustrazioni · famiglia 2 (F…): la foto di Francesco con il libro, stessi testi
ADS = [dict(id=k, bg=bg, **COPY[k]) for k, bg in (('B1', CARTA), ('B2', NOTTE), ('C1', SABBIA), ('D2', CARTA), ('E1', SABBIA), ('E4', NOTTE))]
ADS += [dict(id='F' + k, foto=True, bg=CARTA, **COPY[k]) for k in COPY]
# senza il fumetto «Boh, sembra carino» la riga di C1 va detta per intero
next(a for a in ADS if a['id'] == 'FC1')['sub'] = '«Boh, sembra carino.» <b>Per l’ospite sei invisibile.</b>'

# famiglia 3 (registro Toskich, 27 novembre 2026): T1 il tappo di sughero, T2 la serranda abbassata
def tappo():
    waves = ''.join(f'<path d="M0 {y} C 75 {y-18}, 150 {y+18}, 225 {y} S 375 {y-18}, 450 {y} S 600 {y+18}, 675 {y} S 825 {y-18}, 900 {y}" fill="none" stroke="{c}" stroke-width="3"/>'
                    for y, c in ((250, '#eef0f2'), (300, '#5b6875'), (350, '#3a4652')))
    dots = ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#a98352"/>' for x, y, r in ((-18,-30,3),(6,-40,2.5),(16,-18,3.5),(-6,-10,2.5),(-20,0,2),(12,4,3),(0,-26,2)))
    bob = ('<g transform="translate(450 262) rotate(-14) scale(1.7)">'
           '<path d="M -46 -58 L 46 -58 L 36 22 L -36 22 Z" fill="#d6b37a"/>'
           '<ellipse cx="0" cy="-58" rx="46" ry="11" fill="#e6c995"/>'
           + dots + '</g>')
    return f'<svg class="sea" viewBox="0 0 900 400" width="100%">{waves}{bob}</svg>'

def serranda():
    return '<div class="shut"><div class="box"><i class="bar"></i><div class="slats"></div><div class="handle"></div><div class="glow"></div></div><div class="floor"></div></div>'

ADS += [
 dict(id='T1', bg=NOTTE, foto=True, img=b64(HERE / 'foto-artlist/tappo_b.png', 'image/png'), opos='60% 70%',
      h='Il tappo di sughero<br><em>non sceglie dove andare.</em>', hs=80,
      sub='Agosto tira. Maggio si ferma. <b>Il prezzo lo fa chi ha gente alla porta.</b>'),
 dict(id='T2', bg=CARTA, foto=True, img=b64(HERE / 'foto-artlist/serranda_a.png', 'image/png'), opos='50% 60%',
      h='Dentro è tutto perfetto.<br><em>Da fuori si vede la serranda.</em>', hs=72,
      sub='<b>La qualità li fa tornare.</b> Non li fa arrivare.'),
]

# famiglia 4 (angoli Toskich, 27 novembre 2026 sera): N2 il report pieno di clic, N6 ChatGPT consiglia chi sa descrivere
def report():
    def row(lab, hs, tag, flat=False):
        bars = ''.join(f'<i style="height:{h}%"></i>' for h in hs)
        return f'<div class="rr{" fl" if flat else ""}"><b>{lab}</b><div class="bars">{bars}</div><span>{tag}</span></div>'
    up1 = (22, 26, 24, 33, 38, 36, 47, 55, 52, 66, 78, 92)
    up2 = (30, 28, 36, 41, 39, 50, 57, 61, 70, 74, 86, 96)
    flat = (34, 31, 35, 33, 32, 34, 33, 35, 32, 34, 33, 34)
    return ('<div class="rep"><div class="rh"><b>Report dell’agenzia</b><span>Ottobre</span></div>'
            + row('Clic', up1, 'in salita') + row('Impression', up2, 'in salita') + row('Prenotazioni', flat, 'uguali', True)
            + '<div class="postit">E le camere?</div></div>')

def chat_desc():
    li = ''.join(f'<li><i>xxxxxxxxxx</i><span>{t}</span></li>' for t in ('quello delle bici', 'quello del silenzio', 'quello dei bambini'))
    return f'''<div class="chat cd"><div class="q">Dove dormo tre notti a Rimini?</div>
<div class="a"><p>Ti consiglio questi tre:</p><ol>{li}</ol></div>
<div class="ghost"><b>Il tuo hotel</b><span>«vicino al mare»</span><em>non nominato</em></div></div>'''

ADS += [
 dict(id='N2', bg=CARTA, h='Tanti clic.<br><em>Le stesse prenotazioni.</em>', hs=88, vis=report,
      sub='È come il contapassi. <b>Hai camminato tanto. Sei ancora in cucina.</b>'),
 dict(id='N6', bg=SABBIA, h='Chi consiglia ChatGPT?<br><em>Chi sa descrivere.</em>', hs=84, vis=chat_desc,
      sub='Se di te sa solo «vicino al mare», <b>non ti nomina.</b>'),
]

# famiglia 4, seconda tornata (27 novembre 2026): N8 il gemello, N9 il sito rifatto, N10 prima dei lavori, N11 la vasca senza tappo
def facade(name):
    # facciata da Riviera: insegna sul tetto, quattro piani di balconi, tenda a righe sull'ingresso
    ink = '#15181c'
    wins = ''
    for r in range(4):
        y = 92 + r * 52
        for c in range(4):
            x = 58 + c * 74
            wins += f'<rect x="{x}" y="{y}" width="40" height="30" rx="2" fill="#dfe6ea" stroke="{ink}" stroke-width="2"/>'
        wins += f'<path d="M48 {y+34} H352 M48 {y+34} v-10 M352 {y+34} v-10" stroke="{ink}" stroke-width="3" fill="none"/>'
    stripes = ''.join(f'<rect x="{150 + k*20}" y="306" width="10" height="22" fill="#4a4f57"/>' for k in range(5))
    return f"""<svg viewBox="0 0 400 400" width="100%" class="fac">
<rect x="96" y="20" width="208" height="44" rx="4" fill="#fff" stroke="{ink}" stroke-width="3"/>
<text x="200" y="51" text-anchor="middle" font-family="Newsreader" font-weight="500" font-size="25" fill="{ink}">{name}</text>
<path d="M130 64 v12 M270 64 v12" stroke="{ink}" stroke-width="3"/>
<rect x="36" y="76" width="328" height="312" fill="#f2efe8" stroke="{ink}" stroke-width="3"/>
{wins}
<rect x="140" y="306" width="120" height="22" fill="#fff" stroke="{ink}" stroke-width="2"/>{stripes}
<rect x="170" y="330" width="60" height="58" fill="#c9d5db" stroke="{ink}" stroke-width="2"/>
<path d="M200 330 v58" stroke="{ink}" stroke-width="2"/>
<rect x="64" y="340" width="70" height="34" rx="2" fill="#dfe6ea" stroke="{ink}" stroke-width="2"/>
<rect x="266" y="340" width="70" height="34" rx="2" fill="#dfe6ea" stroke="{ink}" stroke-width="2"/>
<path d="M10 388 H390" stroke="{ink}" stroke-width="3"/>
</svg>"""

def twins():
    def card(name):
        return (f'<div class="hp">{facade(name)}<b>{name}</b>'
                '<ul><li>Camere confortevoli</li><li>A due passi dal mare</li><li>Staff cordiale</li></ul></div>')
    return ('<div class="twins"><div class="tw-row">'
            f'<div><small class="tw-l">Il tuo hotel</small>{card("Hotel Miramare")}</div>'
            f'<div><small class="tw-l">Quello accanto</small>{card("Hotel Bellavista")}</div>'
            '</div><div class="tw-sol">Soluzione: nessuna.</div></div>')

def browsers():
    old = ('<div class="br old"><div class="br-bar"><i></i><i></i><i></i></div><div class="br-in">'
           '<div class="o-logo">HOTEL <i class="bl">xxxxxx</i> ★★★</div><div class="o-ban"></div>'
           '<p class="claim"><span>Camere confortevoli a due passi dal mare</span></p><div class="o-nav"><i></i><i></i><i></i><i></i></div></div></div>')
    new = ('<div class="br new"><div class="br-bar"><i></i><i></i><i></i></div><div class="br-in">'
           '<div class="n-hero"><p class="claim"><span>Camere confortevoli a due passi dal mare</span></p><span class="n-bt">Prenota ora</span></div></div></div>')
    return f'<div class="sites"><div class="st"><small>Prima</small>{old}</div><div class="st"><small>Dopo</small>{new}</div></div>'

def estimate():
    rows = ''.join(f'<div class="er"><span>{t}</span><b><i class="bl">{v}</i></b></div>' for t, v in
                   (('Bagni nuovi', '48.000 €'), ('Parquet nelle camere', '36.000 €'), ('Testiere imbottite', '9.500 €'), ('Facciata e balconi', '27.000 €')))
    return ('<div class="est"><div class="rh"><b>Preventivo ristrutturazione</b><span>Inverno</span></div>' + rows
            + '<div class="er why"><span>Perché sceglierti</span><b class="empty"></b></div></div>')

ADS += [
 dict(id='N8', bg=CARTA, h='Trova le differenze.<br><em>Non ce ne sono.</em>', hs=88, vis=twins,
      sub='Il tuo hotel è bellissimo. <b>E identico a quello accanto.</b>'),
 dict(id='N9', bg=SABBIA, h='Sito nuovo.<br><em>Stesse parole.</em>', vis=browsers,
      sub='Più bello. Più veloce. <b>Dice le stesse cose.</b>'),
 dict(id='N10', bg=CARTA, h='Gli interni li rifanno tutti.<br><em>Il motivo no.</em>', hs=80, vis=estimate,
      sub='<b>Prima dei lavori,</b> decidi per chi li fai.'),
]
# N11 disegnata (la foto Artlist foto-artlist/vasca.png resta come alternativa): rubinetto = traffico, scarico aperto, tappo appeso fuori
def vasca():
    ink, w1, w2 = '#15181c', '#c9d5db', '#dfe6ea'
    stream = f'<path d="M262 132 C 258 220, 270 330, 262 452" stroke="{w1}" stroke-width="16" fill="none" stroke-linecap="round"/>'
    out = ''.join(f'<path d="M{x} 478 C {x-4} 500, {x+4} 520, {x} 548" stroke="{w1}" stroke-width="8" fill="none" stroke-linecap="round"/>' for x in (498, 520, 542))
    arrow = f'<path d="M520 552 l-14 -14 M520 552 l14 -14" stroke="{ink}" stroke-width="3" fill="none"/>'
    return f'''<svg class="vasca" viewBox="0 0 900 600" width="100%" font-family="Figtree">
<rect x="0" y="0" width="900" height="600" fill="none"/>
<path d="M196 40 V108 H270 V128" stroke="{ink}" stroke-width="10" fill="none" stroke-linejoin="round"/>
<rect x="180" y="58" width="32" height="14" rx="4" fill="{ink}"/>
<path d="M128 214 L772 214 L736 444 Q730 474 696 474 L204 474 Q170 474 164 444 Z" fill="#fff" stroke="{ink}" stroke-width="4"/>
<path d="M170 452 Q176 470 204 470 L696 470 Q724 470 730 452 L732 440 L168 440 Z" fill="{w2}"/>
<rect x="104" y="200" width="692" height="20" rx="10" fill="#fff" stroke="{ink}" stroke-width="4"/>
<path d="M210 474 l-14 36 M690 474 l14 36" stroke="{ink}" stroke-width="6" stroke-linecap="round"/>
{stream}
<ellipse cx="520" cy="472" rx="26" ry="7" fill="{ink}"/>
{out}{arrow}
<path d="M760 210 C 800 240, 790 280, 810 308" stroke="#6f747c" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round" fill="none"/>
<circle cx="810" cy="330" r="22" fill="#ffd22e" stroke="{ink}" stroke-width="3"/>
<text x="300" y="72" font-size="28" font-weight="600" fill="{ink}">Il rubinetto: campagne, post, agenzia</text>
<text x="830" y="392" font-size="28" font-weight="600" fill="{ink}" text-anchor="middle">Il tappo</text>
<text x="566" y="540" font-size="27" font-weight="600" fill="{ink}">Scarico aperto:</text>
<text x="566" y="574" font-size="27" fill="#4a4f57">nessun motivo per sceglierti</text>
</svg>'''

ADS.append(dict(id='N11', bg=CARTA, h='Più clic, camere vuote?<br><em>Manca il tappo.</em>', hs=92, vis=vasca,
                sub='Il tappo è <b>un motivo per scegliere te.</b>'))

# P1 (27 novembre 2026): l'annuncio sull'offerta stessa, il capitolo e cosa c'è dentro (voci dalla pagina /capitolo/)
def indice():
    voci = ('Le pesche di mio nonno', 'Perché l’ospite guarda solo prezzo e recensioni', 'Il noleggio bici del vicino',
            'Il filtro nuovo: l’AI', 'Il test dei dieci secondi')
    li = ''.join(f'<li><span>{k+1}</span>{v}</li>' for k, v in enumerate(voci))
    return (f'<div class="pdf"><div class="pdf-cov"><img src="{COVER}" alt=""><em>13 pagine · PDF</em></div>'
            f'<div class="pdf-toc"><small>Nel PDF</small><ol>{li}</ol><p>+ il link per fare il test sul tuo sito</p></div></div>')

ADS.append(dict(id='P1', bg=SABBIA, h='Il primo capitolo.<br><em>Gratis, in venti minuti.</em>', hs=84, vis=indice,
                sub='Meno di una riunione col commercialista. <b>Lasci la mail, il PDF arriva lì.</b>'))

CSS = '''
@font-face{font-family:Newsreader;src:url(@@NEWS@@) format("woff2");font-weight:200 800}
@font-face{font-family:Figtree;src:url(@@FIG@@) format("woff2");font-weight:300 900}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:WPX;height:HPX;overflow:hidden}
.canvas{position:absolute;inset:0;background:BG;color:#15181c;font-family:Figtree}
.col{position:absolute;left:72px;right:72px;top:PT;bottom:PB;display:flex;flex-direction:column}
/* etichetta: Figtree 600 maiuscolo, tracking .14em, trattino davanti (come .eyebrow) */
.kick{display:flex;align-items:center;gap:20px;font:600 25px/1.3 Figtree;letter-spacing:.14em;text-transform:uppercase;color:#6f747c}
.kick:before{content:"";width:52px;height:2px;background:currentColor}
/* titolo: Newsreader 500, parola chiave sottolineata di giallo (come h1 em) */
h1{margin-top:30px;font:500 HSIZE/1.04 Newsreader;letter-spacing:-.012em;color:#15181c;text-wrap:balance}
h1 em{font-style:normal;background:linear-gradient(#ffd22e,#ffd22e) 0 92%/100% .09em no-repeat;padding-bottom:.04em}
.sub{margin-bottom:28px;font:400 36px/1.4 Figtree;color:#4a4f57;max-width:900px}
.sub b{color:#15181c;font-weight:600}
.vis{flex:1;display:flex;flex-direction:column;justify-content:center;align-items:center;margin:34px 0 30px;min-height:0}
.foot{display:flex;align-items:center;justify-content:space-between;gap:24px;padding-top:26px;border-top:2px solid #e3e1db}
.logo{display:inline-flex;align-items:center;gap:18px;font:600 34px/1 Figtree}
.mark{width:44px;height:36px;flex:none;background:linear-gradient(#15181c,#15181c) 0 14px/10px 22px no-repeat,linear-gradient(#15181c,#15181c) 12px 6px/10px 30px no-repeat,linear-gradient(#ffd22e,#ffd22e) 24px 2px/10px 34px no-repeat,linear-gradient(#15181c,#15181c) 36px 12px/8px 24px no-repeat}
.gift{display:flex;align-items:center;gap:18px}
.gift img{width:66px;border:1px solid #c9c6be;border-radius:3px}
.gift span{display:block;font:600 26px/1.25 Figtree;text-align:right}
.gift small{display:block;font:400 22px/1.25 Figtree;color:#6f747c;text-align:right}
/* fondo notte */
.dk .canvas,.dk h1,.dk .sub b,.dk .logo,.dk .gift span{color:#eef0f2}
.dk .sub,.dk .kick,.dk .gift small{color:#b8c0c8}
.dk .foot{border-color:#2c3742}
.dk .mark{background:linear-gradient(#eef0f2,#eef0f2) 0 14px/10px 22px no-repeat,linear-gradient(#eef0f2,#eef0f2) 12px 6px/10px 30px no-repeat,linear-gradient(#ffd22e,#ffd22e) 24px 2px/10px 34px no-repeat,linear-gradient(#eef0f2,#eef0f2) 36px 12px/8px 24px no-repeat}
.dk .gift img{border-color:#2c3742}
/* pannelli: foglio bianco, filetto sottile, niente ombre */
.grid,.phone,.mo,.am,.chat .a{background:#fff;border:2px solid #e3e1db;border-radius:12px}
/* griglia di Booking: un solo rettangolo acceso */
.grid{display:grid;grid-template-columns:repeat(10,1fr);gap:12px;width:100%;max-width:900px;padding:60px 32px 32px}
.grid i{position:relative;aspect-ratio:1.15;border-radius:4px;background:#e9e5dc}
.grid i:nth-child(3n){background:#f2efe8}
.grid i.me{background:#ffd22e;transform:scale(1.25);box-shadow:0 0 0 2px #15181c;z-index:1}
.grid i.me:before{content:"";position:absolute;left:30%;bottom:100%;width:2px;height:30px;background:#15181c}
.grid i.me:after{content:"";position:absolute;left:calc(30% + 2px);bottom:calc(100% + 14px);border-left:22px solid #15181c;border-top:9px solid transparent;border-bottom:9px solid transparent}
/* chat */
.chat{width:100%;max-width:880px;display:grid;gap:24px}
.chat .q{justify-self:end;max-width:640px;background:#eef0f2;color:#15181c;border-radius:24px 24px 6px 24px;padding:26px 30px;font:500 34px/1.35 Figtree}
.chat .a{justify-self:start;width:620px;background:#1b2530;border-color:#2c3742;color:#eef0f2;border-radius:24px 24px 24px 6px;padding:26px 30px;font:400 32px/1.35 Figtree}
.chat ol{margin:14px 0 0 40px;font:600 32px/1.6 Figtree}
.chat i,.bl{font-style:normal;filter:blur(7px)}
/* timer */
.tm{display:grid;justify-items:center;gap:36px}
.dial{width:400px;height:400px;border-radius:50%;border:2px solid #15181c;display:grid;place-content:center;text-align:center;background:conic-gradient(#ffd22e 0 60deg,#fff 60deg)}
.dial b{display:block;font:500 200px/1 Newsreader;letter-spacing:-.02em;background:#fff;border-radius:12px;padding:0 18px}
.dial span{display:block;margin-top:4px;font:600 26px Figtree;letter-spacing:.14em;text-transform:uppercase;color:#6f747c;background:#fff}
.bub2{background:#fff;border:2px solid #e3e1db;border-radius:12px;padding:22px 34px;font:italic 500 48px/1.2 Newsreader;color:#15181c}
/* lista in stile Booking */
.phone{width:680px;border-radius:28px;padding:26px 22px}
.pbar{display:flex;justify-content:space-between;align-items:baseline;padding:4px 8px 18px;border-bottom:2px solid #e3e1db;margin-bottom:10px}
.pbar span{font:600 30px Figtree}.pbar small{font:400 22px Figtree;color:#6f747c}
.row{display:grid;grid-template-columns:120px 1fr auto;gap:18px;align-items:center;padding:14px 6px;border-bottom:1px solid #e3e1db}
.ph{height:86px;border-radius:8px;background:linear-gradient(180deg,#dfe6ea 0 52%,#c9d5db 52% 66%,#ece4d4 66%)}
.rt b{display:block;font:600 26px/1.2 Figtree}
.rt span{display:block;font:400 20px Figtree;color:#6f747c}
.rt em{display:inline-block;margin-top:6px;font:600 20px Figtree;font-style:normal;color:#15181c;border:1px solid #c9c6be;border-radius:3px;padding:2px 8px}
.pr{text-align:right}.pr small{display:inline-block;font:600 19px Figtree;color:#fff;background:#15181c;border-radius:4px;padding:2px 8px}.pr b{display:block;margin-top:6px;font:500 34px Newsreader}
/* calendario */
.cal{display:grid;grid-template-columns:1fr 1fr;gap:28px;width:100%}
.mo{padding:26px}
.mh{display:flex;justify-content:space-between;align-items:center;margin-bottom:20px}
.mh b{font:500 40px Newsreader}.mh span{font:600 19px Figtree;letter-spacing:.06em;color:#6f747c;border:1px solid #c9c6be;border-radius:3px;padding:4px 10px}
.mh span.t-on{color:#15181c;border-color:#15181c}
.days{display:grid;grid-template-columns:repeat(7,1fr);gap:8px}
.days i{aspect-ratio:1;border-radius:4px;background:#f2efe8}
.days i.on{background:#15181c}
/* servizi */
.ams{display:grid;grid-template-columns:1fr 1fr;gap:22px;width:100%}
.am{background:#1b2530;border-color:#2c3742;color:#eef0f2;padding:26px}
.am b{display:block;font:500 34px Newsreader;margin-bottom:14px}
.am ul{list-style:none;display:grid;gap:6px}
.am li{font:400 28px/1.3 Figtree;color:#b8c0c8;padding-left:40px;position:relative}
.am li:before{content:"";position:absolute;left:2px;top:8px;width:20px;height:11px;border-left:3px solid #eef0f2;border-bottom:3px solid #eef0f2;transform:rotate(-45deg)}
/* T1: il mare e il galleggiante */
.sea{display:block;max-width:900px}
/* T2: la serranda abbassata, uno spiraglio di luce gialla */
.shut{width:100%;max-width:820px}
.shut .box{position:relative;height:440px;border:2px solid #4a4f57;border-bottom:0;border-radius:6px 6px 0 0;overflow:hidden;background:#d9d6cf}
.shut .bar{position:absolute;left:0;right:0;top:0;height:34px;background:#4a4f57;z-index:2}
.shut .slats{position:absolute;inset:34px 0 0 0;background:repeating-linear-gradient(180deg,#c9c6be 0 22px,#b3b0a8 22px 24px,#e3e1db 24px 30px)}
.shut .handle{position:absolute;left:50%;bottom:36px;width:90px;height:12px;margin-left:-45px;border-radius:6px;background:#6f747c;z-index:2}
.shut .glow{position:absolute;left:0;right:0;bottom:0;height:14px;background:#ffd22e;box-shadow:0 -6px 18px rgba(255,210,46,.55);z-index:1}
.shut .floor{height:6px;background:#4a4f57;border-radius:0 0 3px 3px}
/* N2: il report dell'agenzia, un solo post-it giallo */
.rep{position:relative;width:100%;max-width:900px;background:#fff;border:2px solid #e3e1db;border-radius:12px;padding:30px 36px 18px}
.rh{display:flex;justify-content:space-between;align-items:center;padding-bottom:18px;border-bottom:2px solid #e3e1db}
.rh b{font:500 38px Newsreader}.rh span{font:600 19px Figtree;letter-spacing:.06em;color:#6f747c;border:1px solid #c9c6be;border-radius:3px;padding:4px 10px}
.rr{display:grid;grid-template-columns:200px 1fr 120px;gap:24px;align-items:end;padding:20px 0;border-bottom:1px solid #e3e1db}
.rr:last-of-type{border-bottom:0}
.rr b{font:600 28px/1.2 Figtree;align-self:center}
.rr span{font:600 20px Figtree;color:#6f747c;text-align:right;align-self:center}
.bars{display:flex;align-items:flex-end;gap:8px;height:96px}
.bars i{flex:1;background:#4a4f57;border-radius:3px 3px 0 0}
.fl .bars i{background:#c9c6be}
.fl b,.fl span{color:#15181c}
.postit{position:absolute;right:-18px;bottom:-44px;transform:rotate(-3deg);background:#ffd22e;padding:20px 28px;font:italic 500 44px/1 Newsreader;color:#15181c;border-radius:2px}
/* N6: la chat che descrive, e il tuo hotel che non c'è */
.cd{gap:20px}
.cd .a{width:760px}
.cd ol{margin-left:36px}
.cd li span{font-weight:400;color:#b8c0c8;margin-left:14px}
.ghost{justify-self:start;width:760px;display:grid;grid-template-columns:auto 1fr auto;gap:18px;align-items:center;border:2px dashed #c9c6be;border-radius:12px;padding:22px 28px;color:#6f747c}
.ghost b{font:500 34px Newsreader;color:#4a4f57}.ghost span{font:italic 400 28px Figtree}
.ghost em{font:600 19px Figtree;font-style:normal;letter-spacing:.06em;text-transform:uppercase;border:1px solid #c9c6be;border-radius:3px;padding:4px 10px}
/* N8: due homepage gemelle */
.twins{width:100%;max-width:900px;display:grid;gap:22px;justify-items:center}
.tw-l{display:block;margin-bottom:12px;font:600 22px Figtree;letter-spacing:.14em;text-transform:uppercase;color:#6f747c}
.tw-row{display:grid;grid-template-columns:1fr 1fr;gap:28px;width:100%}
.hp{background:#fff;border:2px solid #e3e1db;border-radius:12px;padding:20px}
.hp-ph{height:170px;border-radius:8px;background:linear-gradient(180deg,#dfe6ea 0 52%,#c9d5db 52% 66%,#ece4d4 66%)}
.hp b{display:block;margin:14px 0 8px;font:500 32px Newsreader}
.fac{display:block}
.hp ul{list-style:none;display:grid;gap:4px;font:400 26px/1.35 Figtree;color:#4a4f57}
.hp-bt{display:inline-block;margin-top:16px;font:600 22px Figtree;border:2px solid #15181c;border-radius:999px;padding:8px 22px}
.tw-sol{font:600 18px Figtree;letter-spacing:.14em;text-transform:uppercase;color:#6f747c;transform:rotate(180deg)}
/* N9: il sito prima e dopo, la stessa frase cerchiata */
.sites{display:grid;grid-template-columns:1fr 1fr;gap:28px;width:100%}
.st small{display:block;margin-bottom:12px;font:600 22px Figtree;letter-spacing:.14em;text-transform:uppercase;color:#6f747c}
.br{background:#fff;border:2px solid #c9c6be;border-radius:10px;overflow:hidden}
.br-bar{display:flex;gap:8px;padding:12px 14px;background:#e3e1db}
.br-bar i{width:14px;height:14px;border-radius:50%;background:#c9c6be}
.br-in{height:420px;padding:22px;display:flex;flex-direction:column;gap:18px}
.old .br-in{background:#f2efe8;align-items:center;text-align:center}
.o-logo{font:700 22px Newsreader;letter-spacing:.08em}
.o-ban{width:100%;height:120px;border:4px double #4a4f57;background:linear-gradient(180deg,#dfe6ea 0 55%,#c9d5db 55%)}
.o-nav{display:flex;gap:10px}.o-nav i{width:58px;height:16px;background:#4a4f57;border-radius:2px}
.old .claim{font:700 30px/1.2 Newsreader;color:#15181c}
.n-hero{flex:1;border-radius:8px;background:linear-gradient(180deg,#b9c7cf,#8fa3ae);padding:26px;display:flex;flex-direction:column;justify-content:flex-end;gap:16px}
.new .claim{font:600 34px/1.15 Figtree;color:#fff}
.n-bt{align-self:flex-start;font:600 20px Figtree;background:#fff;color:#15181c;border-radius:999px;padding:8px 20px}
.claim span{background:linear-gradient(#ffd22e,#ffd22e) 0 96%/100% .16em no-repeat;-webkit-box-decoration-break:clone;box-decoration-break:clone}
/* N10: il preventivo dei lavori, l'ultima riga vuota */
.est{width:100%;max-width:900px;background:#fff;border:2px solid #e3e1db;border-radius:12px;padding:30px 36px 26px}
.er{display:flex;justify-content:space-between;align-items:center;padding:18px 0;border-bottom:1px solid #e3e1db;font:400 30px Figtree;color:#4a4f57}
.er b{font:500 32px Newsreader;color:#15181c}
.er.why{border-bottom:0;margin-top:10px;padding-top:26px;border-top:2px solid #15181c;color:#15181c;font-weight:600}
.er.why span{background:linear-gradient(#ffd22e,#ffd22e) 0 92%/100% .14em no-repeat;padding-bottom:.06em}
.er .empty{width:220px;height:40px;border-bottom:3px dashed #c9c6be}
/* N11: la vasca disegnata */
.vasca{display:block;max-width:920px;overflow:visible}
/* P1: copertina del PDF e indice */
.pdf{display:grid;grid-template-columns:330px 1fr;gap:44px;align-items:center;width:100%}
.pdf-cov{display:grid;gap:14px;justify-items:center}
.pdf-cov img{width:100%;border:2px solid #c9c6be;border-radius:4px;background:#fff}
.pdf-cov em{font:600 20px Figtree;font-style:normal;letter-spacing:.14em;text-transform:uppercase;color:#6f747c}
.pdf-toc small{display:block;margin-bottom:16px;font:600 22px Figtree;letter-spacing:.14em;text-transform:uppercase;color:#6f747c}
.pdf-toc ol{list-style:none;display:grid;gap:4px}
.pdf-toc li{display:grid;grid-template-columns:44px 1fr;align-items:baseline;padding:14px 0;border-bottom:1px solid #e3e1db;font:500 31px/1.2 Newsreader;color:#15181c}
.pdf-toc li span{font:600 22px Figtree;color:#6f747c}
.pdf-toc li:last-child span{color:#15181c}
.pdf-toc li:last-child{background:linear-gradient(#ffd22e,#ffd22e) 44px 88%/calc(100% - 44px) .12em no-repeat}
.pdf-toc p{margin-top:16px;font:400 24px/1.3 Figtree;color:#4a4f57}
/* famiglia foto: testo in alto, foto a tutta larghezza, piede su carta */
.fo .txt{position:absolute;left:72px;right:72px;top:PT}
.fo .txt .sub{margin:22px 0 0}
.fo .photo{position:absolute;left:0;right:0;top:PHT;bottom:FOOTH;overflow:hidden;background:#f2efe8}
.fo .photo img{width:100%;height:100%;object-fit:cover;object-position:50% OPOS}
.fo .foot{position:absolute;left:72px;right:72px;bottom:FOOTB;border-top:0;padding-top:0}
'''

def build(ad, W, H):
    story = H > 1500
    PT, PB = (250, 300) if story else (72, 64)
    foto = ad.get('foto')
    vals = {'WPX': f'{W}px', 'HPX': f'{H}px', 'BG': ad['bg'], 'PT': f'{PT}px', 'PB': f'{PB}px',
            'HSIZE': f"{ad.get('hs', 92 if foto else 100)}px",
            'PHT': f"{740 if story else 470}px", 'FOOTH': f"{450 if story else 168}px", 'FOOTB': f"{330 if story else 52}px",
            'OPOS': '18%' if story else '20%'}  # inquadratura: volto intero e titolo del libro
    css = CSS
    for k, v in vals.items(): css = css.replace(k, v)
    css = css.replace('@@NEWS@@', NEWS).replace('@@FIG@@', FIG)  # dopo i segnaposto: il base64 contiene lettere maiuscole a caso
    cls = 'dk' if ad['bg'] == NOTTE else ''
    kick = '<span class="kick">Per gli albergatori della Riviera</span>'
    foot = f'<div class="foot"><span class="logo"><span class="mark"></span>Hotel Positioning</span><div class="gift"><div><span>Primo capitolo gratis · 13 pagine</span><small>hotelpositioning.com</small></div><img src="{COVER}" alt=""></div></div>'
    if foto:
        body = f'''<div class="canvas fo"><div class="txt">{kick}<h1>{ad["h"]}</h1><p class="sub">{ad["sub"]}</p></div>
<div class="photo"><img src="{ad.get('img', FOTO)}" alt="" style="object-position:{ad.get('opos', '50% ' + vals['OPOS'])}"></div>{foot}</div>'''
    else:
        body = f'''<div class="canvas"><div class="col">{kick}<h1>{ad["h"]}</h1><div class="vis">{ad["vis"]()}</div><p class="sub">{ad["sub"]}</p>{foot}</div></div>'''
    return f'<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}">{body}</body></html>'

if len(sys.argv) > 2: ADS = [a for a in ADS if a['id'] in sys.argv[2].split(',')]  # es. N2,N6
man = {'batch': OUT.name, 'palette': [CARTA, SABBIA, NOTTE, '#ffffff', '#15181c', '#e3e1db', '#1b2530', '#ffd22e', '#c9c6be', '#4a4f57', '#d9d6cf'], 'ads': []}
for ad in ADS:
    for (W, H, suf) in ((1080, 1350, '45'), (1080, 1920, '916')):
        f = f'{ad["id"].lower()}_{suf}.html'
        (OUT / f).write_text(build(ad, W, H))
        man['ads'].append({'id': f'{ad["id"]}_{suf}', 'file': f.replace('.html', '.png'), 'size': [W, H],
                           # foto reale a tutta larghezza: esce dai bordi a sinistra e a destra, e i suoi colori non sono in palette
                           'route': ('hybrid' if ad['id'].startswith('T') else 'A+foto') if ad.get('foto') else 'A', 'bleeds': 'LR' if ad.get('foto') else '',
                           'route_reason': 'foto reale di Francesco con il libro' if ad.get('foto') else 'diagrammi in CSS, nessuna foto della struttura',
                           'assets': ['newsreader.woff2', 'figtree.woff2', 'copertina-pdf.png'] + ((['foto-artlist (Nano Banana Pro, generata AI)'] if ad['id'].startswith('T') else ['francesco-libro@2x.webp']) if ad.get('foto') else [])})
(OUT / 'manifest.json').write_text(json.dumps(man, indent=1, ensure_ascii=False))
print(len(man['ads']), 'html')
