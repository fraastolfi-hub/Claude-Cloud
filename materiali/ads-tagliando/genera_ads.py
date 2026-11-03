# Genera gli HTML delle static ads Tagliando Hotel T1-T8 (route A), formati 1080x1350 e 1080x1920.
# Stesso sistema grafico degli annunci Guida Romagna v2 (materiali/ads-guida-romagna-v2), con la foto di
# Francesco in tuta da meccanico come visual principale. Metodo: Creative Statics Kit (Simone Dassereto).
# Uso: python3 genera_ads.py <cartella_output>   poi render con playwright (vedi render.mjs)
import base64, sys, json
from pathlib import Path
G = Path('/home/user/Claude-Cloud/materiali/guida-positioning')
SITE = Path('/home/user/Claude-Cloud/site/src/assets')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(Path(p).read_bytes()).decode()
OUTFIT = b64(G / 'outfit.woff2', 'font/woff2'); FIG = b64(G / 'figtree.woff2', 'font/woff2')
FOTO = b64(SITE / 'img/tagliando-francesco@2x.webp', 'image/webp')
INK, CR, Y, LS, TS = '#262521', '#faf7f4', '#ffd22e', '#d8d6ff', '#bfe8e3'
GREEN, TOM = '#5fd08a', '#ff5a3c'

def dots(): return f'<span class="dots"><i style="background:{GREEN}"></i><i style="background:{Y}"></i><i style="background:{TOM}"></i></span>'

PK = '#ffd3ea'
STICK = {
 'T1': f'<div class="stk tr">{dots()}<b>21 controlli</b><small>gratis · due minuti</small></div>',
 'T2': '',
 'T3': f'<div class="stk tr ver big"><p><i style="background:{GREEN}"></i>Sì</p><p><i style="background:{Y}"></i>Quasi</p><p><i style="background:{TOM}"></i>Non ancora</p></div>',
 'T4': '<div class="chat tr"><p class="q">Perché scegliere l’Hotel <i>xxxx</i>?</p><p class="a">Accogliente, posizione comoda, staff cordiale.</p><small>Esempio</small></div>',
 'T5': '<div class="stk tr swap"><p>Hotel <s>Bellavista</s></p><p class="nw">Hotel Miramare</p><small>«A due passi dal mare»</small></div>',
 'T6': '<div class="bub tr"><p>L’agenzia porta gente.</p><p><b>Il sito la deve tenere.</b></p></div>',
 'T7': '<div class="stk tr cal"><span>Nov</span><b>Tagliando</b><span class="feb">Feb</span><b>Campagna</b></div>',
 'T8': '<div class="bub tr"><p>Il sito l’hai provato</p><p><b>dal telefono?</b></p></div>',
}

ADS = [
 dict(id='T1', bg=CR, h='Fai il tagliando<br><mark>al sito del tuo hotel.</mark>', sub='Nessuno parte per Napoli con la spia accesa. <b>Il tuo sito merita un budget?</b>', hs=82),
 dict(id='T2', bg=Y, h='La campagna è la benzina.<br><mark>Il sito, il motore.</mark>', sub='Se il motore perde olio, <b>la benzina finisce sull’asfalto.</b>', hs=72),
 dict(id='T3', bg=LS, h='Il tuo sito merita un budget?<br><mark>Sì, quasi, non ancora.</mark>', sub='21 controlli, un verdetto. <b>Prima di pagare la campagna.</b>', hs=66),
 dict(id='T4', bg=CR, h='Cosa dice ChatGPT<br><mark>del tuo hotel?</mark>', sub='Se risponde così, hai un problema. <b>Lo dice di tutti.</b>', hs=88),
 dict(id='T5', bg=TS, h='Metti il nome del vicino.<br><mark>Regge?</mark>', sub='Cancella il nome del tuo hotel. Scrivi quello del vicino. <b>La frase è ancora vera?</b>', hs=78),
 dict(id='T6', bg=INK, h='Prima di firmare la campagna,<br><mark>il tagliando.</mark>', sub='Se il sito non dice perché scegliere te, paghi due volte. <b>L’agenzia. E poi Booking.</b>', hs=60, dark=True),
 dict(id='T7', bg=PK, h='A novembre<br><mark>si fa il tagliando.</mark>', sub='A febbraio parte la campagna per l’estate. <b>Il sito si controlla adesso.</b>', hs=92),
 dict(id='T8', bg=LS, h='Il tuo sito,<br><mark>visto dall’A14.</mark>', sub='In coda sull’A14, il sabato del cambio. <b>L’ospite ti sceglie da lì.</b>', hs=92, kick='E tu, albergatore della Romagna?'),
]

CSS = '''
@font-face{font-family:Outfit;src:url(@@OUTFIT@@) format("woff2");font-weight:100 900}
@font-face{font-family:Figtree;src:url(@@FIG@@) format("woff2");font-weight:300 900}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:WPX;height:HPX;overflow:hidden}
.canvas{position:absolute;inset:0;background:BG;color:INK;font-family:Figtree}
.col{position:absolute;left:72px;right:72px;top:PT;bottom:PB;display:flex;flex-direction:column}
.kick{align-self:flex-start;display:inline-flex;align-items:center;gap:10px;border:3px solid INK;border-radius:999px;background:#fff;padding:10px 20px;font:800 26px/1 Outfit;text-transform:uppercase}
.kick i{width:14px;height:14px;border-radius:50%;background:#ffd22e;border:2.5px solid INK}
h1{margin-top:30px;font:900 HSIZE/1.06 Outfit;color:INK}
h1 mark{background:#ffd22e;color:#262521;border-radius:12px;padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
.yb h1 mark{background:#fff}
.vis{flex:1;min-height:0;margin:34px 0 28px;position:relative}
.ph{position:absolute;inset:0 10px 10px 0;border:3px solid INK;border-radius:28px;overflow:hidden;box-shadow:10px 10px 0 INK;background:#e3ddd4}
.ph img{width:100%;height:100%;object-fit:cover;object-position:50% OPOS}
.tr{position:absolute;right:30px;top:auto;bottom:34px}
.stk{background:#fff;border:3px solid INK;border-radius:22px;padding:16px 20px;box-shadow:6px 6px 0 INK;color:#262521}
.stk b{display:block;font:900 38px/1.05 Outfit}.stk small{display:block;margin-top:4px;font:600 20px/1.2 Figtree;color:#57534c}
.stk .dots{display:flex;gap:8px;margin-bottom:10px}.dots i{width:20px;height:20px;border-radius:50%;border:2.5px solid INK}
.ver p{display:flex;align-items:center;gap:12px;font:800 28px/1.5 Outfit}.ver i{width:22px;height:22px;border-radius:50%;border:2.5px solid INK}
.cred b + small{margin-bottom:12px}
.big p{font-size:34px}.big i{width:26px;height:26px}
.swap p{font:800 30px/1.3 Outfit}.swap s{text-decoration-thickness:4px;text-decoration-color:#ff5a3c}
.swap .nw{background:#ffd22e;border-radius:8px;padding:0 8px;margin-top:4px}
.cal{display:grid;grid-template-columns:auto 1fr;gap:6px 14px;align-items:center}
.cal span{font:900 22px/1 Outfit;text-transform:uppercase;background:#262521;color:#fff;border-radius:8px;padding:6px 10px;text-align:center}
.cal .feb{background:#d8d6ff;color:#262521}
.cal b{font-size:30px}
.bub{max-width:330px;background:#fff;border:3px solid INK;border-radius:26px;padding:20px 24px;box-shadow:6px 6px 0 INK;color:#262521}
.bub p{font:500 25px/1.3 Figtree}.bub b{font-weight:800}
.chat{max-width:370px;display:grid;gap:10px}
.chat p{border:3px solid INK;border-radius:20px;padding:12px 16px;font:600 22px/1.3 Figtree;box-shadow:5px 5px 0 INK;color:#262521}
.chat .q{background:#fff;justify-self:end;border-bottom-right-radius:6px}.chat .q i{font-style:normal;filter:blur(5px)}
.chat .a{background:#d8d6ff;border-bottom-left-radius:6px}
.chat small{justify-self:start;font:700 17px Figtree;text-transform:uppercase;background:#fff;border:2px solid INK;border-radius:999px;padding:3px 10px;color:#262521}
.sub{font:500 36px/1.28 Figtree;color:#57534c;margin-bottom:26px}
.sub b{color:INK;font-weight:800}
.foot{display:flex;align-items:center;justify-content:space-between;gap:24px;padding-top:24px;border-top:3px solid INK}
.logo{display:inline-flex;align-items:center;gap:14px;font:800 32px/1 Outfit}
.mark{width:44px;height:36px;flex:none;background:linear-gradient(INK,INK) 0 14px/10px 22px no-repeat,linear-gradient(INK,INK) 12px 6px/10px 30px no-repeat,linear-gradient(#ffd22e,#ffd22e) 24px 2px/10px 34px no-repeat,linear-gradient(INK,INK) 36px 12px/8px 24px no-repeat}
.yb .mark{background:linear-gradient(INK,INK) 0 14px/10px 22px no-repeat,linear-gradient(INK,INK) 12px 6px/10px 30px no-repeat,linear-gradient(#fff,#fff) 24px 2px/10px 34px no-repeat,linear-gradient(INK,INK) 36px 12px/8px 24px no-repeat}
.dest{text-align:right}.dest span{display:block;font:800 27px/1.2 Outfit}.dest small{display:block;font:600 22px/1.2 Figtree;color:#57534c}
.dk .canvas{color:#faf7f4}.dk h1{color:#faf7f4}.dk .sub{color:#c4bdb1}.dk .sub b{color:#faf7f4}
.dk .kick{background:#262521;color:#faf7f4;border-color:#faf7f4}.dk .kick i{border-color:#faf7f4}
.dk .ph{border-color:#faf7f4;box-shadow:10px 10px 0 #ffd22e}
.dk .foot{border-color:#57534c}.dk .dest small{color:#c4bdb1}
.dk .mark{background:linear-gradient(#faf7f4,#faf7f4) 0 14px/10px 22px no-repeat,linear-gradient(#faf7f4,#faf7f4) 12px 6px/10px 30px no-repeat,linear-gradient(#ffd22e,#ffd22e) 24px 2px/10px 34px no-repeat,linear-gradient(#faf7f4,#faf7f4) 36px 12px/8px 24px no-repeat}
'''

def build(ad, W, H):
    story = H > 1500
    PT, PB = (250, 320) if story else (72, 64)
    css = CSS
    for k, v in {'WPX': f'{W}px', 'HPX': f'{H}px', 'BG': ad['bg'], 'INK': INK, 'PT': f'{PT}px', 'PB': f'{PB}px',
                 'HSIZE': f'{ad["hs"]}px', 'OPOS': '0%' if story else '4%'}.items():
        css = css.replace(k, v)
    css = css.replace('@@OUTFIT@@', OUTFIT).replace('@@FIG@@', FIG)
    cls = ' '.join(c for c in ['dk' if ad.get('dark') else '', 'yb' if ad['bg'] == Y else ''] if c)
    return f'''<!DOCTYPE html><html lang="it"><head><meta charset="utf-8"><style>{css}</style></head><body class="{cls}">
<div class="canvas"><div class="col">
<span class="kick"><i></i>{ad.get("kick", "E tu, albergatore?")}</span>
<h1>{ad["h"]}</h1>
<div class="vis"><div class="ph"><img src="{FOTO}" alt=""></div>{STICK[ad["id"]]}</div>
<p class="sub">{ad["sub"]}</p>
<div class="foot"><span class="logo"><span class="mark"></span>Hotel Positioning</span><div class="dest"><span>Tagliando Hotel · gratis</span><small>hotelpositioning.com/tagliando</small></div></div>
</div></div></body></html>'''

man = {'batch': OUT.name, 'palette': [CR, INK, Y, LS, TS, PK, '#ffffff'], 'ads': []}
for ad in ADS:
    for (W, H, suf) in ((1080, 1350, '45'), (1080, 1920, '916')):
        f = f'{ad["id"].lower()}_{suf}.html'
        (OUT / f).write_text(build(ad, W, H))
        man['ads'].append({'id': f'{ad["id"]}_{suf}', 'file': f.replace('.html', '.png'), 'size': [W, H], 'route': 'A',
                           'route_reason': 'tutti gli asset esistono: foto reale di Francesco (approvata), font e colori del brand; nessuna immagine generata',
                           'assets': ['tagliando-francesco@2x.webp', 'outfit.woff2', 'figtree.woff2']})
(OUT / 'manifest.json').write_text(json.dumps(man, indent=1, ensure_ascii=False))
print(len(man['ads']), 'html')
