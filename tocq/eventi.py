"""Tocq · calendari degli eventi per le landing (Fiera Milano Rho, San Siro e Ippodromo, MiCo, Monza).

I dati stanno in src/dati/eventi.json, con fonte e affidabilità per ogni evento. Qui si generano le
righe del calendario: solo eventi futuri; il pulsante "Prenota" compare solo per le date confermate o
annunciate da fonti affidabili, e apre il motore di prenotazione già sulle notti giuste.
"""
import datetime as dt
import html
import json
import re
from pathlib import Path

DATI = Path(__file__).parent / "src" / "dati" / "eventi.json"
MESI = ["gen", "feb", "mar", "apr", "mag", "giu", "lug", "ago", "set", "ott", "nov", "dic"]
MESI_LUNGHI = ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno", "Luglio", "Agosto",
               "Settembre", "Ottobre", "Novembre", "Dicembre"]
BLASTNESS = "https://book.blastness.com/results"

# quale calendario mostra quali sedi
CALENDARI = {
    "fiera": lambda e: e["sede"] == "Fiera Milano Rho" and e["categoria"] == "fiera",
    "sansiro": lambda e: "San Siro" in e["sede"] or "I-Days" in e["sede"],
    "mico": lambda e: "MiCo" in e["sede"],
    "monza": lambda e: "Monza" in e["sede"],
}


def _e(s):
    return html.escape(str(s or ""), quote=True)


def _data(s):
    return dt.date.fromisoformat(s) if s else None


def _intervallo(a, b):
    if a == b:
        return f"{a.day} {MESI[a.month - 1]} {a.year}"
    if a.month == b.month:
        return f"{a.day}–{b.day} {MESI[a.month - 1]} {a.year}"
    return f"{a.day} {MESI[a.month - 1]} – {b.day} {MESI[b.month - 1]} {b.year}"


def _nome(e):
    """Nome pulito per il calendario; trattini, parentesi e "gate" diventano una nota piccola."""
    nome, note = e["nome"], []
    prima, _, dopo = nome.partition(" - ")
    if dopo:
        if len(prima) <= 4:          # "AF - L'Artigiano in Fiera"
            nome = dopo
        else:
            nome = prima
            if not dopo.lower().startswith("fonti"):
                note.append(dopo)
    m = re.search(r"\s*\(([^)]*)\)", nome)
    if m:
        note.insert(0, m.group(1))
        nome = (nome[:m.start()] + nome[m.end():]).strip()
    nome, _, gate = nome.partition(", gate")
    if gate:
        note.append("gate" + gate)
    return nome.strip(" ,"), " · ".join(n.strip() for n in note if n.strip())


def _prenotabile(e):
    nota = (e.get("note") or "").lower()
    return (e["confidenza"] in ("confirmed", "announced") and e.get("data_inizio")
            and "fonte singola" not in nota and "da verificare" not in nota and "da verificare" not in e["sede"])


def _link(e, tipo):
    """Fiera: arrivo la sera prima e partenza l'ultimo giorno, una persona. Concerto: la notte dell'evento, due persone."""
    a, b = _data(e["data_inizio"]), _data(e["data_fine"])
    if tipo == "fiera":
        dentro, fuori, adulti = a - dt.timedelta(days=1), b, 1
    else:
        dentro, fuori, adulti = a, b + dt.timedelta(days=1), 2
    return (f"{BLASTNESS}?id_albergo=16496&amp;dc=6326&amp;language=it&amp;currency=EUR"
            f"&amp;checkin_date={dentro.isoformat()}&amp;checkout_date={fuori.isoformat()}"
            f"&amp;rooms=1&amp;adults_1={adulti}&amp;children_1=0")


def _sede_breve(e):
    s = e["sede"]
    if "Ippodromo" in s or "I-Days" in s:
        return "Ippodromo · I-Days"
    if "Stadio" in s:
        return "Stadio"
    return ""


VISIBILI = {"fiera": 6, "mico": 6}  # i primi eventi in vista; gli altri dietro "Mostra tutte"


def calendario(chiave, oggi=None):
    oggi = oggi or dt.date.today()
    eventi = json.loads(DATI.read_text())["eventi"]
    filtro = CALENDARI[chiave]
    tipo = "fiera" if chiave in ("fiera", "mico") else "evento"
    futuri = [e for e in eventi if filtro(e) and e.get("data_fine") and _data(e["data_fine"]) >= oggi]
    futuri.sort(key=lambda e: e["data_inizio"])
    righe, mese_prima, gruppi = [], None, []
    limite = VISIBILI.get(chiave)
    for n, e in enumerate(futuri):
        if limite and n == limite:
            gruppi.append(righe); righe, mese_prima = [], None
        a, b = _data(e["data_inizio"]), _data(e["data_fine"])
        if (a.year, a.month) != mese_prima:
            righe.append(f'<li class="calendario__mese">{MESI_LUNGHI[a.month - 1]} {a.year}</li>')
            mese_prima = (a.year, a.month)
        nome, nota = _nome(e)
        sede = _sede_breve(e)
        dettaglio = " · ".join(x for x in (sede, nota) if x and not (x == nota and nota in sede))
        if _prenotabile(e):
            stato = "" if e["confidenza"] == "confirmed" else '<span class="calendario__stato">data annunciata</span>'
            azione = (f'<a class="btn btn--primary btn--small" href="{_link(e, tipo)}" target="_blank" rel="noopener" '
                      f'data-prenota data-evento="{_e(nome)}">Prenota le notti</a>')
        else:
            stato = '<span class="calendario__stato calendario__stato--attesa">da confermare</span>'
            azione = ""
        righe.append(
            f'<li class="calendario__evento"><time datetime="{a.isoformat()}">{_intervallo(a, b)}</time>'
            f'<div><b>{_e(nome)}</b>{f"<small>{_e(dettaglio)}</small>" if dettaglio else ""}{stato}</div>{azione}</li>')
    senza_data = [e for e in eventi if filtro(e) and not e.get("data_inizio") and e["categoria"] != "calcio"]
    attesa = ""
    if senza_data:
        attesa = ('<p class="calendario__attesa small">In attesa di date ufficiali: '
                  + ", ".join(_e(_nome(e)[0]) for e in senza_data) + ".</p>")
    agg = json.loads(DATI.read_text())["meta"].get("aggiornato", "")
    gruppi.append(righe)
    lista = f'<ol class="calendario">{"".join(gruppi[0])}</ol>'
    if len(gruppi) > 1:
        altri = len(futuri) - limite
        lista += (f'<details class="calendario__altre"><summary>Mostra le altre {altri} date</summary>'
                  f'<ol class="calendario">{"".join(gruppi[1])}</ol></details>')
    return (f'{lista}{attesa}'
            f'<p class="board__foot">Date dalle fonti ufficiali (organizzatori, Regione Lombardia), aggiornate al '
            f'{_e(agg)}. Controlla sempre il sito dell\'evento prima di partire.</p>')


def prossimi(chiave, n=3, oggi=None):
    """Le prossime date di una sede, in breve, per la pagina che raccoglie fiere ed eventi."""
    oggi = oggi or dt.date.today()
    eventi = [e for e in json.loads(DATI.read_text())["eventi"]
              if CALENDARI[chiave](e) and e.get("data_fine") and _data(e["data_fine"]) >= oggi]
    eventi.sort(key=lambda e: e["data_inizio"])
    righe = "".join(f'<li><time datetime="{e["data_inizio"]}">{_intervallo(_data(e["data_inizio"]), _data(e["data_fine"]))}</time> {_e(_nome(e)[0])}</li>'
                    for e in eventi[:n])
    return f'<ul class="prossimi">{righe}</ul>' if righe else ""


def blocchi():
    b = {f"<!-- @calendario-{k} -->": calendario(k) for k in CALENDARI}
    b.update({f"<!-- @prossimi-{k} -->": prossimi(k) for k in CALENDARI})
    return b
