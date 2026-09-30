"""Calcola il voto della diagnosi su homepage già estratte (casi.json).

Parametri a regole (1-C, 5, 6, 7, penalità) calcolati qui.
Parametri AI (1-K, 2, 3, 8) letti da casi.json: in questo test li ha compilati
Claude seguendo PROMPT.md, non una chiamata al modello in produzione.
Parametro 4 assente (nessuna risposta al modulo): voto riscalato su 90.
"""
import json, re, unicodedata, pathlib

BASE = pathlib.Path(__file__).parent
DIZ = json.load(open(BASE.parent / "cliche.json"))
VOCI = [v for k, l in DIZ.items() if k != "_nota" for v in l]

def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")

def cliche(testo):
    t = norm(testo)
    return [v for v in VOCI if re.search(v, t)]

def p1(testo, concreti):
    k = sum(1 for c in concreti if norm(c) in norm(testo))
    c = cliche(testo)
    return 25 * min(1, max(0, 0.5 + 0.25 * k - 0.25 * len(c))), c, k

SOST = {"vera_per_quasi_tutti": 0, "vera_per_molti": 7, "solo_questo_hotel": 15}
APER = {"promessa_concreta": 5, "problema_soluzione": 3, "storia_immagine": 2, "vuota": 0}

def p3(n):
    return 15 if n == 1 else 8 if n == 2 else 0

def p5(headline, sotto, nome):
    t = norm(headline + " " + sotto)
    segnali = [r"benvenut[oiae]", r"welcome", r"\bnostr[oaie]\b", r"\boffriamo\b", r"\bsiamo\b", r"vi aspettiamo"]
    n = sum(1 for s in segnali if re.search(s, t))
    if norm(headline).strip(" .!") == norm(nome):
        n += 1
    if re.search(r"dal (19|20)\d\d|da \d+ anni|generazioni", norm(headline)):
        n += 1
    return max(0, 10 - 3 * n)

def p7(primari, testo_principale, modulo_date):
    q = 6 if (primari == 1 or (modulo_date and primari <= 1)) else 3 if primari == 2 else 0
    t = norm(testo_principale)
    if modulo_date or re.search(r"prezz|disponibilit|date|preventivo|tariff", t):
        s = 4
    else:
        s = 1
    return q + s

casi = json.load(open(BASE / "casi.json"))
righe = []
for c in casi:
    testo = c["headline"] + " " + c["sottotitolo"]
    v1, trovati, k = p1(testo, c["ai"]["elementi_concreti"])
    v2 = SOST[c["ai"]["sostituibilita"]]
    v3 = p3(c["ai"]["promesse"])
    v5 = p5(c["headline"], c["sottotitolo"], c["nome"])
    v6 = c["prova"]
    v7 = p7(c["cta_primari"], c["cta_testo"], c["modulo_date"])
    v8 = APER[c["ai"]["apertura"]]
    pen = -5 if c.get("scarsita_finta") else 0
    somma = v1 + v2 + v3 + v5 + v6 + v7 + v8
    voto = round(max(0, min(100, somma * 100 / 90 + pen)))
    righe.append((c["nome"], voto, v1, v2, v3, v5, v6, v7, v8, trovati, k))

print(f"{'Hotel':<22}{'Voto':>5} | {'1':>5}{'2':>4}{'3':>4}{'5':>4}{'6':>4}{'7':>4}{'8':>4} | cliché / concreti")
for r in sorted(righe, key=lambda r: -r[1]):
    print(f"{r[0]:<22}{r[1]:>5} | {r[2]:>5.1f}{r[3]:>4}{r[4]:>4}{r[5]:>4}{r[6]:>4}{r[7]:>4}{r[8]:>4} | {r[9]} / K={r[10]}")
