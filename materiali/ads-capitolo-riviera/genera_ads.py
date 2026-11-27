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
<div class="photo"><img src="{FOTO}" alt=""></div>{foot}</div>'''
    else:
        body = f'''<div class="canvas"><div class="col">{kick}<h1>{ad["h"]}</h1><div class="vis">{ad["vis"]()}</div><p class="sub">{ad["sub"]}</p>{foot}</div></div>'''
    return f'<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}">{body}</body></html>'

man = {'batch': OUT.name, 'palette': [CARTA, SABBIA, NOTTE, '#ffffff', '#15181c', '#e3e1db', '#1b2530', '#ffd22e'], 'ads': []}
for ad in ADS:
    for (W, H, suf) in ((1080, 1350, '45'), (1080, 1920, '916')):
        f = f'{ad["id"].lower()}_{suf}.html'
        (OUT / f).write_text(build(ad, W, H))
        man['ads'].append({'id': f'{ad["id"]}_{suf}', 'file': f.replace('.html', '.png'), 'size': [W, H],
                           # foto reale a tutta larghezza: esce dai bordi a sinistra e a destra, e i suoi colori non sono in palette
                           'route': 'A+foto' if ad.get('foto') else 'A', 'bleeds': 'LR' if ad.get('foto') else '',
                           'route_reason': 'foto reale di Francesco con il libro' if ad.get('foto') else 'diagrammi in CSS, nessuna foto della struttura',
                           'assets': ['newsreader.woff2', 'figtree.woff2', 'copertina-pdf.png'] + (['francesco-libro@2x.webp'] if ad.get('foto') else [])})
(OUT / 'manifest.json').write_text(json.dumps(man, indent=1, ensure_ascii=False))
print(len(man['ads']), 'html')
