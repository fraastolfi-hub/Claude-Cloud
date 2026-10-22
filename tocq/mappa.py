"""Tocq · mappa del quartiere e guide, generate dai dati verificati in src/dati/poi.json.

Tutto esce come HTML statico (leggibile da Google e dagli assistenti AI); assets/app.js aggiunge
solo filtri ed evidenziazione. La mappa è un "radar" centrato sul Tocq: ogni punto sta alla sua
direzione e distanza reali, con i cerchi dei minuti a piedi. Non usa mappe di terzi.
"""
import html
import json
import math
from pathlib import Path

DATI = Path(__file__).parent / "src" / "dati" / "poi.json"

CATEGORIE = {
    "aziende": "Aziende",
    "trasporti": "Treni e metro",
    "luoghi": "Da vedere",
    "shopping": "Shopping",
    "food": "Mangiare e bere",
}
TIPI_FOOD = [("colazione", "Colazione e caffè"), ("pranzo", "Pranzo di lavoro"), ("aperitivo", "Aperitivo"), ("cena", "Cena")]

PASSO_M_MIN = 80        # metri al minuto a piedi
FATTORE_STRADA = 1.3    # dalla linea d'aria al percorso reale
RAGGIO_M = 1600         # raggio della mappa, in linea d'aria
CERCHI_MIN = [5, 10, 15]
# punti con l'etichetta sempre visibile, per orientarsi
ETICHETTE_FISSE = {"stazione-porta-garibaldi", "piazza-gae-aulenti", "corso-como", "bosco-verticale"}


def _metri(h, p):
    """Spostamento est/nord in metri dal Tocq (proiezione locale, precisa a questa scala)."""
    dx = (p["lng"] - h["lng"]) * math.cos(math.radians(h["lat"])) * 111320
    dy = (p["lat"] - h["lat"]) * 110540
    return dx, dy


def _arricchisci(dati):
    h = dati["hotel"]
    out = []
    for p in dati["poi"]:
        if p.get("lat") is None or p.get("lng") is None:
            continue
        dx, dy = _metri(h, p)
        linea = math.hypot(dx, dy)
        a_piedi = linea * FATTORE_STRADA
        q = dict(p)
        q.update(dx=dx, dy=dy, linea=linea, a_piedi=a_piedi, minuti=max(1, math.ceil(a_piedi / PASSO_M_MIN)))
        out.append(q)
    # punti nello stesso edificio (es. Accenture e Bending Spoons): si allargano a ventaglio per restare cliccabili
    posati = []
    for q in sorted(out, key=lambda q: q["linea"]):
        vicini = sum(1 for (x, y) in posati if math.hypot(q["dx"] - x, q["dy"] - y) < 30)
        if vicini:
            ang = math.radians(60 * vicini)
            q["dx"] += 34 * math.cos(ang)
            q["dy"] += 34 * math.sin(ang)
        posati.append((q["dx"], q["dy"]))
    return sorted(out, key=lambda q: q["linea"])


def _e(s):
    return html.escape(str(s or ""), quote=True)


def _distanza(q):
    m = q["a_piedi"]
    metri = f"{round(m / 10) * 10:.0f} m" if m < 1000 else f"{m / 1000:.1f} km".replace(".", ",")
    return f"{q['minuti']} min a piedi · {metri}"


def _maps(q):
    from urllib.parse import quote
    return f"https://www.google.com/maps/dir/?api=1&origin=Tocq+Hotel+Milano&destination={quote(q['nome'] + ', ' + q['indirizzo'])}&travelmode=walking"


R_PX = 480


def _raggio(m):
    """Scala a radice quadrata: allarga i primi 500 metri, dove sta quasi tutto, e comprime il resto."""
    return R_PX * math.sqrt(max(m, 0) / RAGGIO_M)


def mappa_svg(punti):
    parti = [f'<svg class="radar" viewBox="-520 -520 1040 1040" role="img" aria-labelledby="radar-titolo radar-desc">',
             '<title id="radar-titolo">Mappa del quartiere del Tocq Hotel Milano</title>',
             '<desc id="radar-desc">Il Tocq al centro; i cerchi indicano 5, 10 e 15 minuti a piedi, con la scala che allarga i dintorni immediati; ogni punto è un\'azienda, una fermata, un negozio o un locale alla sua direzione e distanza reali. Il nord è in alto.</desc>']
    for mnt in CERCHI_MIN:
        r = _raggio(mnt * PASSO_M_MIN / FATTORE_STRADA)
        parti.append(f'<circle class="radar__cerchio" r="{r:.1f}"/>')
        parti.append(f'<text class="radar__minuti" x="0" y="{-r - 8:.1f}" text-anchor="middle">{mnt} min</text>')
    parti.append('<line class="radar__asse" x1="0" y1="-500" x2="0" y2="500"/><line class="radar__asse" x1="-500" y1="0" x2="500" y2="0"/>')
    parti.append('<text class="radar__nord" x="0" y="-500" text-anchor="middle">N</text>')
    for q in punti:
        if q["linea"] > RAGGIO_M:
            continue
        k = _raggio(q["linea"]) / q["linea"] if q["linea"] else 0
        x, y = q["dx"] * k, -q["dy"] * k
        fissa = " radar__punto--fisso" if q["id"] in ETICHETTE_FISSE else ""
        parti.append(
            f'<g class="radar__punto{fissa}" data-id="{_e(q["id"])}" data-cat="{_e(q["categoria"])}" transform="translate({x:.1f} {y:.1f})" tabindex="0" role="button" aria-label="{_e(q["nome"])}, {_e(_distanza(q))}">'
            f'<circle r="7"/><text x="12" y="4">{_e(q["nome"])}</text></g>')
    parti.append('<g class="radar__tocq" aria-hidden="true"><circle r="14"/><text y="34" text-anchor="middle">TOCQ</text></g>')
    parti.append('</svg>')
    return "\n".join(parti)


def elenco(punti):
    righe = []
    for q in punti:
        if q["linea"] > RAGGIO_M:
            continue
        ed = f'<span class="poi__edificio">{_e(q["edificio"])}</span>' if q.get("edificio") else ""
        righe.append(
            f'<li class="poi" data-id="{_e(q["id"])}" data-cat="{_e(q["categoria"])}">'
            f'<span class="poi__cat">{_e(CATEGORIE.get(q["categoria"], q["categoria"]))}</span>'
            f'<b class="poi__nome">{_e(q["nome"])}</b>{ed}'
            f'<span class="poi__dist">{_e(_distanza(q))}</span>'
            f'<a class="poi__vai" href="{_e(_maps(q))}" target="_blank" rel="noopener">Percorso</a></li>')
    return '<ol class="poi-elenco" id="poi-elenco">\n' + "\n".join(righe) + "\n</ol>"


def filtri():
    bott = ['<button type="button" data-filtro="tutti" aria-pressed="true">Tutto</button>']
    bott += [f'<button type="button" data-filtro="{k}" aria-pressed="false">{v}</button>' for k, v in CATEGORIE.items()]
    return '<div class="filters mappa-filtri" role="group" aria-label="Mostra sulla mappa">' + "".join(bott) + "</div>"


def tabella_aziende(punti):
    righe = "".join(
        f'<tr><td>{_e(q["nome"])}</td><td>{_e(q.get("edificio") or q["indirizzo"])}</td><td>{_e(q.get("tipo") or "")}</td><td class="n">{q["minuti"]} min</td></tr>'
        for q in punti if q["categoria"] == "aziende")
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Azienda</th><th>Sede</th><th>Settore</th><th>A piedi</th></tr></thead>'
            f'<tbody>{righe}</tbody></table></div>')


def _scheda(q):
    tipo = f'<span class="guida__tipo">{_e(q.get("tipo") or "")}</span>' if q.get("tipo") else ""
    return (f'<article class="guida__voce" data-id="{_e(q["id"])}">{tipo}<h3>{_e(q["nome"])}</h3>'
            f'<p>{_e(q.get("descrizione"))}</p><p class="guida__dove">{_e(q["indirizzo"])} · {_e(_distanza(q))}</p>'
            f'<a href="{_e(_maps(q))}" target="_blank" rel="noopener">Percorso a piedi</a></article>')


def guida_shopping(punti):
    voci = [q for q in punti if q["categoria"] == "shopping"]
    return '<div class="guida">' + "".join(_scheda(q) for q in voci) + "</div>"


def guida_food(punti):
    out = []
    for tipo, titolo in TIPI_FOOD:
        voci = [q for q in punti if q["categoria"] == "food" and (q.get("tipo") or "").lower() == tipo]
        if voci:
            out.append(f'<h3 class="guida__gruppo">{titolo}</h3><div class="guida">' + "".join(_scheda(q) for q in voci) + "</div>")
    altri = [q for q in punti if q["categoria"] == "food" and (q.get("tipo") or "").lower() not in dict(TIPI_FOOD)]
    if altri:
        out.append('<h3 class="guida__gruppo">Altri indirizzi</h3><div class="guida">' + "".join(_scheda(q) for q in altri) + "</div>")
    return "\n".join(out)


def schema_luoghi(punti, sito):
    """ItemList di luoghi con distanza a piedi: utile a Google e agli assistenti AI per le domande 'vicino a'."""
    elementi = []
    for i, q in enumerate([q for q in punti if q["linea"] <= RAGGIO_M], 1):
        tipo = {"food": "FoodEstablishment", "shopping": "Store", "aziende": "Organization", "trasporti": "TrainStation" if "stazione" in q["nome"].lower() else "Place"}.get(q["categoria"], "Place")
        el = {"@type": tipo, "name": q["nome"], "description": f"{q.get('descrizione') or ''} {_distanza(q)} dal Tocq Hotel Milano.".strip(),
              "address": q["indirizzo"], "geo": {"@type": "GeoCoordinates", "latitude": q["lat"], "longitude": q["lng"]}}
        if q["categoria"] == "aziende":
            el = {"@type": "Organization", "name": q["nome"], "description": el["description"],
                  "location": {"@type": "Place", "address": q["indirizzo"], "geo": el["geo"]}}
        elementi.append({"@type": "ListItem", "position": i, "item": el})
    return {"@type": "ItemList", "name": "Aziende, trasporti, negozi e ristoranti vicino al Tocq Hotel Milano", "itemListElement": elementi}


def blocchi():
    """Restituisce i pezzi da sostituire nella pagina, o None se i dati non ci sono ancora."""
    if not DATI.exists():
        return None
    dati = json.loads(DATI.read_text())
    punti = _arricchisci(dati)
    conta = {k: sum(1 for q in punti if q["categoria"] == k and q["linea"] <= RAGGIO_M) for k in CATEGORIE}
    return {
        "<!-- @mappa -->": mappa_svg(punti),
        "<!-- @elenco -->": elenco(punti),
        "<!-- @filtri -->": filtri(),
        "<!-- @aziende -->": tabella_aziende(punti),
        "<!-- @shopping -->": guida_shopping(punti),
        "<!-- @food -->": guida_food(punti),
        "<!-- @conta-aziende -->": str(conta["aziende"]),
        "<!-- @conta-food -->": str(conta["food"]),
        "<!-- @conta-shopping -->": str(conta["shopping"]),
        "_punti": punti,
        "_hotel": dati["hotel"],
    }
