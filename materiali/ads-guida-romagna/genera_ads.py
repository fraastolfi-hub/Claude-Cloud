# Genera gli HTML delle static ads R1-R8 (route A), formati 1080x1350 e 1080x1920.
import base64, sys, json
from pathlib import Path
G = Path('/home/user/Claude-Cloud/materiali/guida-positioning')
SITE = Path('/home/user/Claude-Cloud/site/src/assets')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
src = (G / 'build_guida.py').read_text()
ns = {'__file__': str(G / 'build_guida.py')}
exec(src[:src.index('hotels_js =')], ns)
def ill(name):  # svg interno delle illustrazioni del PDF
    s = ns[name]()
    return s[s.index('<svg'):s.rindex('</svg>') + 6]
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(Path(p).read_bytes()).decode()
OUTFIT = b64(G / 'outfit.woff2', 'font/woff2'); FIG = b64(G / 'figtree.woff2', 'font/woff2'); FIGI = b64(G / 'figtree-italic.woff2', 'font/woff2')
COVER = b64(SITE / 'guida/copertina@2x.webp', 'image/webp'); CUT = b64(G / 'francesco-2026-scontornato.png', 'image/png')
INK, CR, Y, LI, TE, PK = '#262521', '#faf7f4', '#ffd22e', '#8f8cff', '#22a094', '#ff93c7'
LS, TS, PS, YS = '#d8d6ff', '#bfe8e3', '#ffd3ea', '#fff1b8'

def frame(svg_inner, h):
    s = svg_inner.replace('preserveAspectRatio="xMidYMid slice"', 'preserveAspectRatio="xMidYMid meet"').replace("<svg ", '<svg width="100%" style="display:block" ', 1)
    return f'<div class="ill">{s}</div>'

def phone():
    rows = ''
    for i, (p, sc) in enumerate([('89 €', '8,4'), ('92 €', '8,5'), ('86 €', '8,3'), ('91 €', '8,4')]):
        rows += f'''<div class="row"><div class="ph"></div><div class="rt"><b>Hotel <i class="bl">xxxxxxxx</i></b><span>Riccione · ★★★</span><em>A due passi dal mare</em></div><div class="pr"><small>{sc}</small><b>{p}</b></div></div>'''
    return f'''<div class="phone"><div class="pbar"><span>Riccione</span><small>50 strutture trovate</small></div>{rows}</div>'''

def bars():
    def card(k, tot, q, last):
        bs = ''.join(f'<i><b style="width:{v*10}%;background:{c}"></b></i>' for v, c in zip([6, 6, 6, last], [LI, TE, PK, Y]))
        return f'<div class="bc{" on" if k=="D" else ""}"><div class="bh"><span class="k">{k}</span><p>{q}</p></div><div class="bb">{bs}</div><div class="bt"><small>il valore</small><b>{tot}</b><small>/ 40</small></div></div>'
    return f'<div class="bars">{card("C", 21, "«Famiglia e divertimento»", 3)}<div class="arr">→</div>{card("D", 27, "«L’hotel dei triatleti del circuito di Misano»", 9)}</div><p class="note">Esempio inventato per spiegare il metodo, non un hotel reale.</p>'

def stats():
    return f'''<div class="fr"><div class="arch"><img src="{CUT}" alt=""></div><div class="st"><div style="background:{YS}"><b>0 → 30 M€</b><span>TUI.it</span></div><div style="background:{LS}"><b>20 strutture</b><span>marketing Atahotels</span></div><div style="background:{TS}"><b>10 locali</b><span>aperti con i miei soldi</span></div></div></div>'''

ADS = [
 dict(id='R1', bg=CR, h='Mille hotel.<br><mark>Un mare solo.</mark>', vis=lambda H: frame(ill('ill_spiaggia'), H), sub='Il mare ce l’hanno tutti. <b>Il motivo, no.</b>'),
 dict(id='R2', bg=LS, h='Tre secondi,<br><mark>in coda sull’A14.</mark>', vis=lambda H: phone(), sub='Il tuo hotel, in quei tre secondi, <b>che cosa dice?</b>'),
 dict(id='R3', bg=Y, h='«A due passi<br><mark>dal mare.»</mark>', vis=None, sub='Anche quello a due chilometri.', big=True),
 dict(id='R4', bg=CR, h='Il vicino di viale<br><mark>abbassa di dieci euro.</mark>', vis=lambda H: frame(ill('ill_sconto'), H), sub='10 € × 40 camere × 100 notti = <b>40.000 €</b>. Una stagione di margine.'),
 dict(id='R5', bg=CR, h='Stessa Cattolica.<br><mark>Altro racconto.</mark>', vis=lambda H: bars(), sub='Stessi muri, stesso staff. <b>Cambia una voce sola.</b>'),
 dict(id='R6', bg=TS, h='Lo stesso ospite,<br><mark>pagato due volte.</mark>', vis=lambda H: frame(ill('ill_bagnino'), H), sub='Ad aprile il bagnino rifà la spiaggia. <b>Tu rifai i clienti.</b>'),
 dict(id='R7', bg=INK, h='Il prezzo<br>lo decidi tu.<br><mark>Il valore no.</mark>', vis=None, sub='Lo decide l’ospite. In Romagna, lo decide in fretta.', big=True, dark=True),
 dict(id='R8', bg=LS, h='Una guida<br><mark>scritta da Rimini.</mark>', vis=lambda H: stats(), sub='I consulenti vendono consigli. <b>Gli operatori vendono cicatrici.</b>'),
]

def photo_row(quote):
    return f'''<div class="pr2"><div class="bub"><p>{quote}</p><span>Francesco Astolfi · Rimini</span></div><div class="arch a2"><img src="{CUT}" alt=""></div></div>'''

ADS += [
 dict(id='R1B', bg=CR, h='Mille hotel.<br><mark>Un mare solo.</mark>', vis=lambda H: photo_row('In Romagna il mare ce l’hanno tutti. <b>Quindi non è un motivo per scegliere te.</b>'), sub='Il mare ce l’hanno tutti. <b>Il motivo, no.</b>'),
 dict(id='R3B', bg=Y, h='«A due passi<br><mark>dal mare.»</mark>', vis=lambda H: photo_row('Copri il logo della tua homepage. Poi quello del vicino di viale. <b>Cosa resta?</b>'), sub='In Romagna lo scrivono tutti. Anche quello a due chilometri.'),
 dict(id='R4B', bg=CR, h='Il vicino di viale<br><mark>abbassa di dieci euro.</mark>', vis=lambda H: photo_row('Dieci euro, quaranta camere, cento notti: <b>sono 40.000 €.</b> Una stagione di margine.'), sub='Lo sconto è il prezzo di un motivo <b>che non hai.</b>'),
 dict(id='R7B', bg=INK, h='Il prezzo lo decidi tu.<br><mark>Il valore no.</mark>', vis=lambda H: photo_row('Il mare è uguale per tutti. Le stelle anche. <b>Resta una voce sola che vi distingue.</b>'), sub='Ed è l’unica che si cambia da lunedì.', dark=True),
]

CSS = '''
@font-face{font-family:Outfit;src:url(@@OUTFIT@@) format("woff2");font-weight:100 900}
@font-face{font-family:Figtree;src:url(@@FIG@@) format("woff2");font-weight:300 900}
@font-face{font-family:Figtree;src:url(@@FIGI@@) format("woff2");font-weight:300 900;font-style:italic}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:WPX;height:HPX;overflow:hidden}
.canvas{position:absolute;inset:0;width:WPX;height:HPX;overflow:hidden;background:BG;color:INK;font-family:Figtree;padding:PT 72px PB}
.col{position:absolute;left:72px;right:72px;top:PT;bottom:PB;display:flex;flex-direction:column}
.kick{align-self:flex-start;display:inline-flex;align-items:center;gap:10px;border:3px solid INK;border-radius:999px;background:#fff;padding:10px 20px;font:800 26px/1 Outfit;letter-spacing:0;text-transform:uppercase}
.kick i{width:14px;height:14px;border-radius:50%;background:#ffd22e;border:2.5px solid INK}
h1{margin-top:34px;font:900 HSIZE/1.02 Outfit;letter-spacing:0;color:INK}
h1 mark{background:#ffd22e;color:#262521;border-radius:12px;padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.big h1{font-size:BIGSIZE;margin-top:auto}
.yb h1 mark{background:#fff}
.sub{margin-top:26px;margin-bottom:26px;font:500 34px/1.3 Figtree;color:#57534c;max-width:880px}
.sub b{color:INK;font-weight:800}
.big .sub{font-size:40px;margin-bottom:auto}
.dk .canvas,.dk{color:#faf7f4}
.dk h1{color:#faf7f4}.dk .sub{color:#c4bdb1}.dk .sub b{color:#faf7f4}
.dk .kick{background:#262521;color:#faf7f4;border-color:#faf7f4}
.vis{flex:1;display:flex;flex-direction:column;justify-content:center;margin:34px 0 26px;min-height:0}
.ill{border:3px solid INK;border-radius:28px;overflow:hidden;box-shadow:8px 8px 0 INK;background:#fff}
.foot{display:flex;align-items:center;justify-content:space-between;gap:24px;padding-top:26px;border-top:3px solid INK}
.dk .foot{border-color:#57534c}
.logo{display:inline-flex;align-items:center;gap:14px;font:800 32px/1 Outfit}
.mark{width:44px;height:36px;flex:none;background:linear-gradient(INK,INK) 0 14px/10px 22px no-repeat,linear-gradient(INK,INK) 12px 6px/10px 30px no-repeat,linear-gradient(#ffd22e,#ffd22e) 24px 2px/10px 34px no-repeat,linear-gradient(INK,INK) 36px 12px/8px 24px no-repeat}
.dk .mark{background:linear-gradient(#faf7f4,#faf7f4) 0 14px/10px 22px no-repeat,linear-gradient(#faf7f4,#faf7f4) 12px 6px/10px 30px no-repeat,linear-gradient(#ffd22e,#ffd22e) 24px 2px/10px 34px no-repeat,linear-gradient(#faf7f4,#faf7f4) 36px 12px/8px 24px no-repeat}
.gift{display:flex;align-items:center;gap:16px}
.gift img{width:70px;border:2.5px solid INK;border-radius:6px;transform:rotate(4deg)}
.gift span{display:block;font:800 26px/1.2 Outfit;text-align:right}
.gift small{display:block;font:600 22px/1.2 Figtree;color:#57534c;text-align:right}
.dk .gift small{color:#c4bdb1}
.phone{align-self:center;width:640px;background:#fff;border:4px solid INK;border-radius:44px;padding:26px 22px;box-shadow:10px 10px 0 INK}
.pbar{display:flex;justify-content:space-between;align-items:baseline;padding:4px 8px 18px;border-bottom:2px solid #e8e2d8;margin-bottom:12px}
.pbar span{font:800 32px Outfit}.pbar small{font:600 20px Figtree;color:#6b665d}
.row{display:grid;grid-template-columns:120px 1fr auto;gap:16px;align-items:center;padding:12px 6px;border-bottom:2px solid #f0ebe3}
.ph{height:86px;border-radius:14px;background:linear-gradient(180deg,#bfe3f2 0 50%,#7cc4d8 50% 66%,#f1dfb8 66%)}
.rt b{display:block;font:800 25px/1.2 Outfit}.rt .bl{font-style:normal;filter:blur(6px)}
.rt span{display:block;font:500 19px Figtree;color:#6b665d}.rt em{display:inline-block;margin-top:6px;font:700 19px Figtree;font-style:normal;background:#fff1b8;border-radius:6px;padding:2px 8px}
.pr{text-align:right}.pr small{display:block;font:700 18px Figtree;color:#fff;background:#22a094;border-radius:8px;padding:2px 8px}.pr b{display:block;margin-top:6px;font:900 30px Outfit}
.bars{display:grid;grid-template-columns:1fr auto 1fr;gap:18px;align-items:center}
.bc{background:#fff;border:3px solid INK;border-radius:24px;padding:22px;box-shadow:6px 6px 0 INK}
.bc.on{background:#fff1b8}
.bh{display:flex;gap:12px;align-items:flex-start;min-height:96px}.bh .k{flex:none;width:44px;height:44px;border-radius:12px;background:INK;color:#fff;display:grid;place-items:center;font:900 24px Outfit}
.bh p{font:600 21px/1.3 Figtree}
.bb{display:grid;gap:12px;margin:16px 0}.bb i{display:block;height:18px;border-radius:999px;background:#ece6dc;overflow:hidden}.bb b{display:block;height:100%;border-radius:999px}
.bt{display:flex;align-items:baseline;gap:10px;border-top:2px solid #e8e2d8;padding-top:12px}.bt small{font:700 18px Figtree;text-transform:uppercase;color:#6b665d}.bt b{font:900 64px/1 Outfit}
.arr{font:900 50px Outfit}
.note{margin-top:18px;font:italic 500 21px Figtree;color:#6b665d}
.fr{display:grid;grid-template-columns:420px 1fr;gap:30px;align-items:end}
.arch{height:520px;border:3px solid INK;border-radius:210px 210px 26px 26px;background:#8f8cff;overflow:hidden;position:relative;box-shadow:8px 8px 0 INK}
.arch img{position:absolute;bottom:0;left:50%;width:86%;transform:translateX(-50%)}
.a2 img{bottom:auto;top:-1%;width:122%}
.pr2{display:grid;grid-template-columns:1fr 400px;gap:28px;align-items:end}
.bub{position:relative;background:#fff;border:3px solid INK;border-radius:28px;padding:30px 30px 26px;box-shadow:8px 8px 0 INK;margin-bottom:60px;color:#262521}
.bub:after{content:"";position:absolute;right:-22px;bottom:46px;width:34px;height:34px;background:#fff;border-right:3px solid INK;border-top:3px solid INK;transform:rotate(45deg)}
.bub p{font:500 34px/1.3 Figtree}.bub b{font-weight:800}
.bub span{display:block;margin-top:18px;font:800 22px Outfit;text-transform:uppercase;color:#57534c}
.a2{height:400px;border-radius:50%}
.st{display:grid;gap:16px}.st div{border:3px solid INK;border-radius:20px;padding:18px 20px;box-shadow:5px 5px 0 INK}
.st b{display:block;font:900 42px/1 Outfit}.st span{display:block;margin-top:6px;font:600 21px Figtree;color:#57534c}
'''

def build(ad, W, H):
    story = H > 1500
    PT, PB = (250, 300) if story else (72, 64)
    hs = 104
    css = CSS
    for k, v in {'WPX': f'{W}px', 'HPX': f'{H}px', 'BG': ad['bg'], 'INK': INK, 'PT': f'{PT}px', 'PB': f'{PB}px', 'BIGSIZE': '150px' if ad['id'] == 'R3' else '128px', 'HSIZE': f'{84 if ad["id"].startswith("R4") else (92 if ad["id"] == "R7B" else hs)}px'}.items():
        css = css.replace(k, v)
    css = css.replace('@@OUTFIT@@', OUTFIT).replace('@@FIGI@@', FIGI).replace('@@FIG@@', FIG)
    visH = (H - PT - PB) - 520
    vis = f'<div class="vis">{ad["vis"](max(300, min(visH, 520 if not story else 700)))}</div>' if ad.get('vis') else ''
    cls = ' '.join(c for c in ['big' if ad.get('big') else '', 'dk' if ad.get('dark') else '', 'yb' if ad['bg'] == Y else ''] if c)
    kick = 'Per gli hotel della Romagna'
    html = f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}">
<div class="canvas"><div class="col">
<span class="kick"><i></i>{kick}</span>
<h1>{ad["h"]}</h1>
{"" if ad.get("big") else ""}
{vis if not ad.get("big") else ""}
<p class="sub">{ad["sub"]}</p>
<div class="foot" style="{'' if not ad.get('big') else ''}"><span class="logo"><span class="mark"></span>Hotel Positioning</span><div class="gift"><div><span>Guida gratuita · 18 pagine</span><small>hotelpositioning.com</small></div><img src="{COVER}" alt=""></div></div>
</div></div></body></html>'''
    if not ad.get('vis') or ad.get('big'):
        pass
    return html

man = {'batch': OUT.name, 'palette': [CR, INK, Y, LI, TE, PK, LS, TS], 'ads': []}
for ad in ADS:
    for (W, H, suf) in ((1080, 1350, '45'), (1080, 1920, '916')):
        f = f'{ad["id"].lower()}_{suf}.html'
        (OUT / f).write_text(build(ad, W, H))
        man['ads'].append({'id': f'{ad["id"]}_{suf}', 'file': f.replace('.html', '.png'), 'size': [W, H], 'route': 'A', 'route_reason': 'tutti gli asset esistono: illustrazioni del PDF, foto e copertina reali, font del brand', 'assets': ['outfit.woff2', 'figtree.woff2', 'copertina@2x.webp'] + (['cutout.png'] if ad['id'] == 'R8' else [])})
(OUT / 'manifest.json').write_text(json.dumps(man, indent=1, ensure_ascii=False))
print(len(man['ads']), 'html')
