# Static ads del libro «Hotel Positioning» L1-L5, formati 1080x1350 (feed) e 1080x1920 (storie/reel).
# Stile: tema editoriale del sito (Newsreader + Figtree, carta, inchiostro, giallo solo come sottolineatura).
# Uso: python3 genera_ads.py <cartella_output>   poi: node render.mjs <cartella_output>
import base64, sys
from pathlib import Path
HERE = Path(__file__).parent
SITE = Path('/home/user/Claude-Cloud/site/src/assets')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(Path(p).read_bytes()).decode()
SERIF = b64(SITE / 'fonts/newsreader.woff2', 'font/woff2'); SANS = b64(SITE / 'fonts/figtree.woff2', 'font/woff2')
FOTO = b64(HERE / 'francesco-libro.webp', 'image/webp')
CARTA, SABBIA, INK, GRAF, NEB, NOTTE, NFG, NFG2, Y = '#fcfbf8', '#f2efe8', '#15181c', '#4a4f57', '#6f747c', '#121a22', '#eef0f2', '#b8c0c8', '#ffd22e'

ADS = [
 dict(id='L1', h='Il tuo hotel ha una risposta. <mark>Ce l’ha anche il vicino.</mark>', sub='«Posizione, servizio, camere.» Quando le risposte sono uguali, l’ospite confronta il prezzo. Il libro ti porta alla risposta solo tua.', bg=CARTA),
 dict(id='L2', h='Ogni notte su Booking <mark>costa una volta e mezza questo libro.</mark>', sub='Esempio: camera da 180 €, commissione di circa 30 €. Il libro costa 19,90 €, e lo paghi una volta.', bg=NOTTE, dark=True, hs=66),
 dict(id='L3', h='Questo non è un libro <mark>di marketing alberghiero.</mark>', sub='Foto, diretto, AI: consigli giusti, inutili finché non sai perché l’ospite dovrebbe scegliere te. Il libro parte da lì.', bg=SABBIA),
 dict(id='L4', h='Sei passaggi per trovare <mark>perché ti scelgono.</mark>', sub='Bisogno, alternative, unicità, persona, categoria, trend. Alla fine stanno su un foglio solo.', bg=CARTA),
 dict(id='L5', h='La SPA nuova. Il ristorante rifatto. <mark>Le parole del vicino.</mark>', sub='Sulla homepage: «relax, benessere, posizione strategica». Più servizi aggiungi, più assomigli agli altri.', bg=SABBIA, hs=66),
]

CSS = '''
@font-face{font-family:Newsreader;src:url(@@SERIF@@) format("woff2");font-weight:200 800}
@font-face{font-family:Figtree;src:url(@@SANS@@) format("woff2");font-weight:300 900}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:@@HPX@@px;overflow:hidden}
.c{position:absolute;inset:0;background:@@BG@@;color:@@FG@@;font-family:Figtree}
.txt{position:absolute;left:72px;right:72px;top:@@TOP@@px}
.k{display:inline-block;padding:4px 0 4px 52px;background:linear-gradient(@@K@@,@@K@@) 0 50%/38px 2px no-repeat;color:@@K@@;font:600 22px/1.2 Figtree;letter-spacing:.14em;text-transform:uppercase}
h1{margin-top:22px;font:500 @@HS@@px/1.04 Newsreader;letter-spacing:-.015em;text-wrap:balance}
h1 mark{background:linear-gradient(#ffd22e,#ffd22e) 0 92%/100% .1em no-repeat;color:inherit;padding-bottom:.02em}
.sub{margin-top:22px;font:400 @@SS@@px/1.45 Figtree;color:@@SUBC@@;max-width:900px}
.ph{position:absolute;left:0;right:0;top:@@PHT@@px;bottom:@@PHB@@px;overflow:hidden}
.ph img{width:100%;height:100%;object-fit:cover;object-position:50% @@OPOS@@}
.tag{position:absolute;right:72px;bottom:@@TAGB@@px;background:#fcfbf8;color:#15181c;padding:18px 26px;border-radius:6px;display:flex;align-items:baseline;gap:14px;box-shadow:0 12px 30px rgba(21,24,28,.18)}
.tag b{font:500 52px/1 Newsreader}.tag span{font:600 22px/1.2 Figtree;letter-spacing:.1em;text-transform:uppercase;color:#4a4f57}
.note{position:absolute;right:72px;bottom:@@NOTEB@@px;font:400 18px/1.3 Figtree;color:#fcfbf8;opacity:.9;text-shadow:0 1px 6px rgba(0,0,0,.6)}
'''
FMT = {
 '45': dict(H=1350, TOP=60, HS=72, SS=28, PHT=530, PHB=0, OPOS='40%', TAGB=230, NOTEB=28),
 '916': dict(H=1920, TOP=200, HS=80, SS=31, PHT=650, PHB=0, OPOS='86%', TAGB=560, NOTEB=360),
}
for a in ADS:
    for f, v in FMT.items():
        dark = a.get('dark')
        css = CSS
        for k, val in dict(K=NFG2 if dark else NEB, HPX=v['H'], BG=a['bg'], FG=NFG if dark else INK, TOP=v['TOP'], HS=a.get('hs', v['HS']) if f=='45' else v['HS'], SS=v['SS'],
                           SUBC=NFG2 if dark else GRAF, PHT=v['PHT'], PHB=v['PHB'], OPOS=v['OPOS'], TAGB=v['TAGB'], NOTEB=v['NOTEB']).items():
            css = css.replace('@@'+k+'@@', str(val))
        css = css.replace('@@SERIF@@', SERIF).replace('@@SANS@@', SANS)
        note = f'<p class="note">{a["note"]}</p>' if a.get('note') else ''
        html = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c">
<div class="txt"><span class="k">Il libro · Hotel Positioning</span><h1>{a["h"]}</h1><p class="sub">{a["sub"]}</p></div>
<div class="ph"><img src="{FOTO}" alt=""></div>
<div class="tag"><b>19,90 €</b><span>su Amazon</span></div>{note}
</div></body></html>'''
        (OUT / f'{a["id"].lower()}_{f}.html').write_text(html)
print('ok', len(ADS) * 2)
