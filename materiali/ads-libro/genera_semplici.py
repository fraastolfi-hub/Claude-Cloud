# Static ads del libro, versione semplice: foto di Francesco + headline + subheadline. Niente altro.
# Fascia gialla (il giallo della copertina) con testo nero, foto sotto. 1080x1350 (feed) e 1080x1920 (storie/reel).
# Uso: python3 genera_semplici.py <cartella_output>   poi: node render.mjs <cartella_output>
import base64, sys
from pathlib import Path
HERE = Path(__file__).parent
SITE = Path('/home/user/Claude-Cloud/site/src/assets')
OUT = Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
def b64(p, mime): return f'data:{mime};base64,' + base64.b64encode(Path(p).read_bytes()).decode()
SANS = b64(SITE / 'fonts/figtree.woff2', 'font/woff2')
FOTO = b64(HERE / 'francesco-libro.webp', 'image/webp')

ADS = [
 dict(id='S1', h='Perché un ospite dovrebbe scegliere il tuo hotel?', s='Se non sai rispondere in una frase, sceglierà quello che costa meno.'),
 dict(id='S2', h='Il tuo hotel e quello accanto dicono le stesse cose.', s='«Bella posizione, ottimo servizio, camere confortevoli.» Così l’ospite guarda solo il prezzo.'),
 dict(id='S3', h='Smetti di abbassare i prezzi per riempire le camere.', s='Un libro pratico per farti scegliere senza fare sconti.'),
 dict(id='S4', h='Booking ti prende 30 € a notte. Questo libro costa 19,90 €.', s='E ti aiuta a dipendere meno dai portali.'),
 dict(id='S6', h='Stai per rifare il sito del tuo hotel? Non farlo.', s='Non ancora. Prima scopri perché un ospite dovrebbe scegliere te. Se no avrai un sito più bello che dice le stesse cose.'),
 dict(id='S5', h='Ho scritto un libro per chi gestisce un hotel.', s='Sei passi semplici per far capire all’ospite perché scegliere te.'),
]

CSS = '''
@font-face{font-family:Figtree;src:url(@@SANS@@) format("woff2");font-weight:300 900}
*{box-sizing:border-box;margin:0;padding:0}
html,body{width:1080px;height:@@H@@px;overflow:hidden}
.c{position:absolute;inset:0;background:#ffd22e;color:#15181c;font-family:Figtree}
.txt{position:absolute;left:64px;right:64px;top:@@TOP@@px;height:@@BAND@@px;display:flex;flex-direction:column;justify-content:center}
h1{font:800 @@HS@@px/1.02 Figtree;letter-spacing:-.025em;text-wrap:balance}
p{margin-top:22px;font:500 @@SS@@px/1.3 Figtree;color:#2b2f35;text-wrap:balance}
.ph{position:absolute;left:0;right:0;top:@@PHT@@px;bottom:0;overflow:hidden;background:#fff}
.ph img{width:100%;height:100%;object-fit:cover;object-position:50% @@OPOS@@}
'''
FMT = {
 '45': dict(H=1350, TOP=20, BAND=420, HS=78, SS=34, PHT=450, OPOS='30%'),
 '916': dict(H=1920, TOP=190, BAND=530, HS=90, SS=40, PHT=740, OPOS='34%'),
}
for a in ADS:
    for f, v in FMT.items():
        css = CSS
        for k, val in v.items(): css = css.replace('@@' + k + '@@', str(val))
        css = css.replace('@@SANS@@', SANS)
        html = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><style>{css}</style></head><body><div class="c">
<div class="txt"><h1>{a["h"]}</h1><p>{a["s"]}</p></div>
<div class="ph"><img src="{FOTO}" alt=""></div>
</div></body></html>'''
        (OUT / f'{a["id"].lower()}_{f}.html').write_text(html)
print('ok', len(ADS) * 2)
