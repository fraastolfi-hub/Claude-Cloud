"""Calcola il voto della diagnosi su homepage già estratte (casi.json), secondo SPEC.md.

Parametri a regole (hook-visibilità, cliché, riprova sociale, azione, penalità) calcolati qui.
Giudizi AI (caselle del posizionamento, apertura, elementi concreti) letti da casi.json:
in questo test li ha compilati Claude seguendo PROMPT.md, non una chiamata al modello in produzione.
"""
import json, re, unicodedata, pathlib

BASE = pathlib.Path(__file__).parent
DIZ = json.load(open(BASE.parent / "cliche.json"))
VOCI = [v for lingua in ("it", "en") for l in DIZ[lingua].values() for v in l]

TARGET = {"esplicito_escludente": 15, "implicito": 7, "assente": 0}
BENEFICIO = {"concreto": 15, "generico": 7, "solo_caratteristiche": 4, "assente": 0}
SOST = {"solo_questo_hotel": 15, "vera_per_molti": 7, "vera_per_quasi_tutti": 0}
APERTURA = {"promessa_concreta": 9, "problema_soluzione": 6, "promessa_generica": 5, "storia_immagine": 4, "vuota": 0}


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


def cliche(testo):
    """Corrispondenze del dizionario; quelle sovrapposte contano come una sola."""
    t = norm(testo)
    spans = sorted((m.start(), m.end()) for v in VOCI for m in re.finditer(v, t))
    uniti = []
    for a, b in spans:
        if uniti and a < uniti[-1][1]:
            uniti[-1][1] = max(uniti[-1][1], b)
        else:
            uniti.append([a, b])
    return [t[a:b] for a, b in uniti]


def hook(c):
    if not c["frase_visibile"]:
        return 0
    vis = 2 + (2 if len(c["headline"].split()) <= 12 else 0) + (2 if c["headline_piu_grande"] else 0)
    return vis + APERTURA[c["ai"]["apertura"]]


def niente_cliche(testo, concreti):
    if not testo.strip():
        return 0, [], 0
    trovati = cliche(testo)
    k = sum(1 for x in concreti if norm(x) in norm(testo))
    return 15 * min(1, max(0, 0.25 + 0.25 * k - 0.25 * len(trovati))), trovati, k


def azione(primari, testo, modulo_date):
    q = 6 if primari == 1 else 3 if primari == 2 else 0
    t = norm(testo)
    s = 4 if modulo_date or re.search(r"prezz|disponibilit|date|preventivo|tariff", t) else 1
    return q + s


risultati = []
for c in json.load(open(BASE / "casi.json")):
    hero = " ".join([c["headline"], c["sottotitolo"], *c["supporto"]])
    ai = c["ai"]
    pos = TARGET[ai["target"]] + BENEFICIO[ai["beneficio"]] + SOST[ai["sostituibilita"]]
    h = hook(c)
    cl, trovati, k = niente_cliche(hero, ai["elementi_concreti"])
    az = azione(c["cta_primari"], c["cta_testo"], c["modulo_date"])
    pen = (-5 if c["scarsita_finta"] else 0) + (-5 if c["scaduta"] else 0)
    voto = round(max(0, min(100, pos + h + cl + c["prova"] + az + pen)))
    fuori = [x for x in ai["concreti_fuori_hero"] if norm(x) in norm(c["fuori_hero"]) and norm(x) not in norm(hero)]
    risultati.append(dict(nome=c["nome"], voto=voto, pos=pos, t=TARGET[ai["target"]], b=BENEFICIO[ai["beneficio"]],
                          d=SOST[ai["sostituibilita"]], hook=h, cliche=cl, prova=c["prova"], azione=az, pen=pen,
                          trovati=trovati, k=k, frase=ai["frase_posizionamento"], visibile=c["frase_visibile"], fuori=fuori))

print(f"{'Hotel':<22}{'Voto':>5} | {'Pos':>4} ({'T':>2} {'B':>2} {'D':>2}) | {'Hook':>4} {'Cli':>5} {'Prova':>5} {'Az':>3} {'Pen':>4}")
for r in sorted(risultati, key=lambda r: -r["voto"]):
    print(f"{r['nome']:<22}{r['voto']:>5} | {r['pos']:>4} ({r['t']:>2} {r['b']:>2} {r['d']:>2}) | {r['hook']:>4} {r['cliche']:>5.1f} {r['prova']:>5} {r['azione']:>3} {r['pen']:>4}")
print()
for r in sorted(risultati, key=lambda r: -r["voto"]):
    print(f"## {r['nome']} · {r['voto']}")
    print(f"   {r['frase']}")
    print(f"   cliché: {r['trovati']} · concreti nel hero: {r['k']}")
    if not r["visibile"]:
        print("   ! Nessuna frase nella prima schermata")
    if len(r["fuori"]) >= 2:
        print(f"   ! Parole nel posto sbagliato: {r['fuori']}")
