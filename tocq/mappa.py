"""Tocq · mappa del quartiere e guide, generate dai dati verificati in src/dati/poi.json.

Tutto esce come HTML statico (leggibile da Google e dagli assistenti AI); assets/app.js aggiunge
solo filtri ed evidenziazione. La mappa usa una base OpenStreetMap ripassata in nero con i colori
del marchio, con i cerchi dei minuti a piedi, i nomi dei quartieri e ogni punto alla sua posizione reale.
"""
import html
import json
import math
from pathlib import Path

DATI = Path(__file__).parent / "src" / "dati" / "poi.json"
# foto e loghi dai siti ufficiali dei locali e delle aziende (fonte di ogni file in referenze.json)
REFERENZE = Path(__file__).parent / "src" / "dati" / "referenze.json"
# percorsi a piedi reali dal portone (FOSSGIS routed-foot): si disegnano quando si sceglie un punto
PERCORSI = Path(__file__).parent / "src" / "dati" / "percorsi.json"
IMG_REF = "assets/img/referenze/"

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
ETICHETTE_FISSE = {"stazione-porta-garibaldi", "piazza-gae-aulenti", "corso-como", "bosco-verticale", "stazione-centrale"}
ETICHETTA_A_SINISTRA = {"stazione-porta-garibaldi"}  # per non sovrapporsi a Gae Aulenti


def _metri(h, p):
    """Spostamento est/nord in metri dal Tocq (proiezione locale, precisa a questa scala)."""
    dx = (p["lng"] - h["lng"]) * math.cos(math.radians(h["lat"])) * 111320
    dy = (p["lat"] - h["lat"]) * 110540
    return dx, dy


def _minuti(metri):
    """Minuti a piedi arrotondati al più vicino; 0 vuol dire "meno di un minuto"."""
    return 0 if metri < 60 else max(1, round(metri / PASSO_M_MIN))


def _min_testo(q):
    return "meno di 1 min" if q["minuti"] == 0 else f"{q['minuti']} min"


def _arricchisci(dati):
    h = dati["hotel"]
    out = []
    for p in dati["poi"]:
        if p.get("lat") is None or p.get("lng") is None:
            continue
        dx, dy = _metri(h, p)
        linea = math.hypot(dx, dy)
        # distanza a piedi: il percorso reale sulle strade (piedi_m, dal router pedonale OpenStreetMap) quando c'è,
        # altrimenti la stima dalla linea d'aria
        a_piedi = p.get("piedi_m") or linea * FATTORE_STRADA
        q = dict(p)
        q.update(dx=dx, dy=dy, linea=linea, a_piedi=a_piedi, minuti=_minuti(a_piedi))
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
    return sorted(out, key=lambda q: q["a_piedi"])


def _e(s):
    return html.escape(str(s or ""), quote=True)


def _distanza(q):
    m = q["a_piedi"]
    metri = f"{round(m / 10) * 10:.0f} m" if m < 1000 else f"{m / 1000:.1f} km".replace(".", ",")
    return f"{_min_testo(q)} a piedi · {metri}"


def _maps(q):
    from urllib.parse import quote
    return f"https://www.google.com/maps/dir/?api=1&origin=Tocq+Hotel+Milano&destination={quote(q['nome'] + ', ' + q['indirizzo'])}&travelmode=walking"


# Base della mappa: 7×7 tasselli OpenStreetMap a zoom 16 (scaricati una volta, ripassati in nero
# con i colori del marchio), da x 34437 e y 23447. Ogni punto si posa con la stessa proiezione dei tasselli.
BASE_IMG = "assets/img/mappa/quartiere-z16.webp"
BASE_Z, BASE_X0, BASE_Y0, BASE_LATO = 16, 34437, 23447, 1792
# nomi dei quartieri, per orientarsi anche senza punti (posizione indicativa del nome, non un confine)
ZONE = [("Isola", 45.4893, 9.1878), ("Porta Nuova", 45.4822, 9.1968), ("Brera", 45.4728, 9.1872),
        ("Moscova", 45.4772, 9.1838), ("Paolo Sarpi", 45.4802, 9.1772), ("Centrale", 45.4878, 9.2035)]


def _px(lat, lng):
    n = 2 ** BASE_Z * 256
    x = (lng + 180) / 360 * n - BASE_X0 * 256
    y = (1 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2 * n - BASE_Y0 * 256
    return x, y


def _metri_px(lat):
    return 156543.03392 * math.cos(math.radians(lat)) / 2 ** BASE_Z


def mappa_interattiva(punti, hotel):
    """Mappa vera del quartiere: base OpenStreetMap, cerchi dei minuti a piedi, nomi dei quartieri e i punti.
    Senza JavaScript resta un'immagine con i punti; app.js aggiunge trascinamento, zoom e temi."""
    hx, hy = _px(hotel["lat"], hotel["lng"])
    mpx = _metri_px(hotel["lat"])
    cerchi = []
    for mnt in CERCHI_MIN:
        r = mnt * PASSO_M_MIN / FATTORE_STRADA / mpx
        cerchi.append(f'<circle class="qmap__cerchio" cx="{hx:.1f}" cy="{hy:.1f}" r="{r:.1f}"/>'
                      f'<text class="qmap__minuti" x="{hx:.1f}" y="{hy - r - 10:.1f}" text-anchor="middle">{mnt} min a piedi</text>')
    zone = "".join(f'<span class="qmap__zona" style="left:{x:.0f}px;top:{y:.0f}px">{_e(n)}</span>'
                   for n, la, ln in ZONE for x, y in [_px(la, ln)])
    ref = _referenze()
    percorsi = json.loads(PERCORSI.read_text()) if PERCORSI.exists() else {}
    segni, linee, occupati = [], [], []
    for q in punti:
        x, y = _px(q["lat"], q["lng"])
        # due sedi allo stesso indirizzo (Accenture e Bending Spoons): il secondo pin scivola di lato
        while any(abs(x - ox) < 30 and abs(y - oy) < 20 for ox, oy in occupati):
            y += 22
        occupati.append((x, y))
        if not (0 <= x <= BASE_LATO and 0 <= y <= BASE_LATO):
            continue
        fissa = " qmap__punto--fisso" if q["id"] in ETICHETTE_FISSE else ""
        fissa += " qmap__punto--sx" if q["id"] in ETICHETTA_A_SINISTRA else ""
        logo = ref.get(q["id"], {}).get("logo") if q["categoria"] == "aziende" else None
        pin = (f'<span class="qmap__pin qmap__pin--logo" aria-hidden="true"><img src="{IMG_REF}{logo}" alt="" loading="lazy" decoding="async"></span>'
               if logo else '<span class="qmap__pin" aria-hidden="true"></span>')
        nome = q["nome"].split(" (")[0].split(" – ")[0]
        dati = (f' data-nome="{_e(nome)}" data-via="{_e(q["indirizzo"].split(", 2")[0])}" data-dist="{_e(_distanza(q))}" data-maps="{_e(_maps(q))}"'
                + (f' data-logo="{IMG_REF}{logo}"' if logo else ""))
        segni.append(
            f'<button type="button" class="qmap__punto{fissa}{" qmap__punto--logo" if logo else ""}" data-id="{_e(q["id"])}" data-cat="{_e(q["categoria"])}"{dati} '
            f'style="left:{x:.1f}px;top:{y:.1f}px" aria-label="{_e(q["nome"])}, {_e(_distanza(q))}">'
            f'{pin}<span class="qmap__nome">{_e(nome)}<small>{_e(_distanza(q))}</small></span></button>')
        tratto = percorsi.get(q["id"])
        if tratto:
            d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in (_px(la, ln) for ln, la in tratto["coords"]))
            linee.append(f'<path class="qmap__percorso" data-id="{_e(q["id"])}" d="{d}"/>')
    return (
        f'<div class="qmap" data-lato="{BASE_LATO}" data-hx="{hx:.1f}" data-hy="{hy:.1f}" role="region" aria-label="Mappa del quartiere del Tocq Hotel Milano">'
        f'<div class="qmap__vista">'
        f'<div class="qmap__piano" style="width:{BASE_LATO}px;height:{BASE_LATO}px">'
        f'<img class="qmap__base" src="{BASE_IMG}" width="{BASE_LATO}" height="{BASE_LATO}" alt="" decoding="async" draggable="false">'
        f'<svg class="qmap__anelli" viewBox="0 0 {BASE_LATO} {BASE_LATO}" aria-hidden="true">{"".join(cerchi)}</svg>'
        f'<svg class="qmap__percorsi" viewBox="0 0 {BASE_LATO} {BASE_LATO}" aria-hidden="true">{"".join(linee)}</svg>'
        f'{zone}{"".join(segni)}'
        f'<span class="qmap__tocq" style="left:{hx:.1f}px;top:{hy:.1f}px" aria-hidden="true"><span class="qmap__tocq-pin"></span><b>TOCQ</b></span>'
        f'</div></div>'
        f'<div class="qmap__comandi" role="group" aria-label="Zoom della mappa">'
        f'<button type="button" data-zoom="1" aria-label="Avvicina">+</button><button type="button" data-zoom="-1" aria-label="Allontana">−</button>'
        f'<button type="button" data-zoom="0" aria-label="Torna al Tocq"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/></svg></button></div>'
        f'<div class="qmap__scheda" hidden aria-live="polite"><button type="button" class="qmap__chiudi" aria-label="Chiudi">×</button>'
        f'<span class="qmap__scheda-logo"></span><b class="qmap__scheda-nome"></b><span class="qmap__scheda-via"></span>'
        f'<span class="qmap__scheda-dist"></span><a class="qmap__scheda-maps" target="_blank" rel="noopener">Apri il percorso in Google Maps</a></div>'
        f'<p class="qmap__aiuto" aria-hidden="true">Trascina per spostarti · usa + e − per lo zoom</p>'
        f'<p class="qmap__crediti">Mappa © <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a> contributors</p>'
        f'</div>')


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


def loghi_aziende(punti):
    ref = _referenze()
    voci = []
    for q in punti:
        if q["categoria"] != "aziende":
            continue
        logo = _logo(q, ref, "azienda__logo") or f'<span class="azienda__logo azienda__logo--testo">{_e(q["nome"].split(" (")[0].split(" — ")[0])}</span>'
        via = q["indirizzo"].split(", 2")[0]  # via e civico, senza CAP e città
        voci.append((q["a_piedi"],
                     f'<li class="azienda" data-id="{_e(q["id"])}">{logo}<div class="azienda__dati">'
                     f'<b class="azienda__nome">{_e(q["nome"].split(" (")[0].split(" – ")[0])}</b>'
                     f'<span class="azienda__via">{_e(via)}</span>'
                     f'<a class="azienda__min" href="{_maps(q)}" target="_blank" rel="noopener">{_distanza(q)}</a>'
                     f'<button type="button" class="azienda__mappa" data-vai="{_e(q["id"])}">Vedi sulla mappa</button></div></li>'))
    voci.sort(key=lambda v: v[0])
    return '<ul class="aziende-loghi" aria-label="Aziende a pochi minuti a piedi">' + "".join(v for _, v in voci) + "</ul>"


def tabella_aziende(punti):
    righe = "".join(
        f'<tr><td>{_e(q["nome"])}</td><td>{_e(q.get("edificio") or q["indirizzo"])}</td><td>{_e(q.get("tipo") or "")}</td><td class="n">{_min_testo(q)}</td></tr>'
        for q in punti if q["categoria"] == "aziende")
    return ('<div class="table-scroll"><table class="data"><thead><tr><th>Azienda</th><th>Sede</th><th>Settore</th><th>A piedi</th></tr></thead>'
            f'<tbody>{righe}</tbody></table></div>')


def _referenze():
    return json.loads(REFERENZE.read_text()) if REFERENZE.exists() else {}


def _logo(q, ref, classe):
    r = ref.get(q["id"], {})
    if not r.get("logo"):
        return ""
    scuro = f" {classe}--scuro" if r.get("logo_scuro") else ""
    return f'<span class="{classe}{scuro}"><img src="{IMG_REF}{r["logo"]}" alt="{_e(q["nome"])}" loading="lazy" decoding="async"></span>'


def _iniziali(nome):
    import unicodedata
    articoli = {"l", "il", "lo", "la", "i", "gli", "le", "the", "de", "del", "della"}
    parole = [w for w in nome.replace("'", " ").replace("’", " ").split() if w[:1].isalnum() and w.lower() not in articoli]
    sigla = "".join(w[0] for w in parole[:2]).upper()
    return unicodedata.normalize("NFKD", sigla).encode("ascii", "ignore").decode() or sigla


def _testata(q, ref):
    """Foto del locale se c'è; altrimenti il logo; altrimenti le iniziali, senza inventare immagini."""
    r = ref.get(q["id"], {})
    logo = _logo(q, ref, "guida__logo")
    if r.get("foto"):
        w, h = r["foto_wh"]
        return (f'<figure class="guida__foto"><img src="{IMG_REF}{r["foto"]}" alt="{_e(q["nome"])}, {_e(q["indirizzo"])}" width="{w}" height="{h}" loading="lazy" decoding="async">'
                f'{logo}</figure>')
    if logo:
        return f'<div class="guida__foto guida__foto--logo">{logo}</div>'
    return f'<div class="guida__foto guida__foto--iniziali" aria-hidden="true"><span>{_e(_iniziali(q["nome"]))}</span></div>'


def _scheda(q, ref=None):
    """Scheda corta: foto, tipo, nome, minuti a piedi, una riga, percorso. L'indirizzo resta nei dati strutturati."""
    ref = ref if ref is not None else _referenze()
    tipo = (q.get("tipo") or "").lower()
    etichetta = f'<span class="guida__tipo">{_e(q.get("tipo"))}</span>' if q.get("tipo") else ""
    return (f'<article class="guida__voce" data-id="{_e(q["id"])}" data-tipo="{_e(tipo)}">{_testata(q, ref)}{etichetta}<h3>{_e(q["nome"])}</h3>'
            f'<p class="guida__min">{_min_testo(q)} a piedi</p><p>{_e(q.get("descrizione"))}</p>'
            f'<a href="{_e(_maps(q))}" target="_blank" rel="noopener">Percorso a piedi</a></article>')


def guida_shopping(punti):
    voci = [q for q in punti if q["categoria"] == "shopping"]
    ref = _referenze()
    return '<div class="guida">' + "".join(_scheda(q, ref) for q in voci) + "</div>"


def guida_food(punti):
    """Una griglia sola, filtrabile per momento della giornata (assets/app.js): si vedono 3-4 schede alla volta."""
    ref = _referenze()
    voci = [q for q in punti if q["categoria"] == "food"]
    presenti = [(k, v) for k, v in TIPI_FOOD if any((q.get("tipo") or "").lower() == k for q in voci)]
    bott = '<button type="button" data-momento="tutti" aria-pressed="false">Tutti</button>' + "".join(
        f'<button type="button" data-momento="{k}" aria-pressed="{"true" if i == 0 else "false"}">{v}</button>' for i, (k, v) in enumerate(presenti))
    return (f'<div class="filters momenti-filtri" role="group" aria-label="Scegli il momento">{bott}</div>'
            '<div class="guida guida--momenti">' + "".join(_scheda(q, ref) for q in voci) + "</div>")


def guida_ids(punti, ids):
    """Schede per una lista di punti scelti a mano (landing di Porta Nuova e Centrale), nell'ordine dato."""
    ref = _referenze()
    per_id = {q["id"]: q for q in punti}
    return '<div class="guida guida--compatta">' + "".join(_scheda(per_id[i], ref) for i in ids if i in per_id) + "</div>"


def tempi_ids(punti, ids):
    """Striscia di tempi a piedi: nome e minuti, nell'ordine dato."""
    per_id = {q["id"]: q for q in punti}
    voci = "".join(f'<li><b>{_min_testo(per_id[i])}</b><span>{_e(per_id[i]["nome"].split(" – ")[0].split(" (")[0])}</span></li>'
                   for i in ids if i in per_id)
    return f'<ul class="tempi">{voci}</ul>'


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
        "<!-- @mappa -->": mappa_interattiva(punti, dati["hotel"]),
        "<!-- @elenco -->": elenco(punti),
        "<!-- @filtri -->": filtri(),
        "<!-- @aziende -->": loghi_aziende(punti),
        "<!-- @shopping -->": guida_shopping(punti),
        "<!-- @food -->": guida_food(punti),
        "<!-- @conta-aziende -->": str(conta["aziende"]),
        "<!-- @conta-food -->": str(conta["food"]),
        "<!-- @conta-shopping -->": str(conta["shopping"]),
        "_punti": punti,
        "_hotel": dati["hotel"],
    }
