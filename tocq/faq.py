"""Tocq · pagina delle domande frequenti.

Le domande si scrivono nelle pagine di provenienza (<details class="faq__item">). La pagina FAQ le
raccoglie tutte, divise per argomento e senza doppioni; nelle altre pagine restano le prime tre con
il link alla pagina completa. Lo schema FAQPage sta solo sulla pagina FAQ, per non segnalare a Google
le stesse domande più volte.
"""
import re

# da quale pagina vengono le domande, e con quale titolo; "faq" sono le domande scritte solo per la pagina FAQ
GRUPPI = [
    ("faq", "Prenotare e soggiornare"),
    ("index", "Prima di prenotare"),
    ("offerte", "Tariffe e offerte"),
    ("camere", "Camere e colazione"),
    ("mangiare", "Mangiare e bere"),
    ("servizi", "Servizi e parcheggio"),
    ("meeting", "Sale meeting ed eventi"),
    ("posizione", "La posizione e il quartiere"),
    ("arrivare", "Come arrivare"),
    ("contatti", "Contatti"),
]
VISIBILI = 3


def blocchi(corpo):
    return re.findall(r'<details class="faq__item">.*?</details>', corpo, re.S)


def accorcia(corpo, key):
    """Nelle pagine normali tiene le prime domande e aggiunge il link alla pagina FAQ."""
    tutti = blocchi(corpo)
    if not tutti:
        return corpo
    for b in tutti[VISIBILI:]:
        corpo = corpo.replace(b, "", 1)
    ultimo = tutti[:VISIBILI][-1]
    link = f'\n        <p class="faq__tutte"><a href="faq.html#gruppo-{key}">Tutte le domande frequenti</a></p>'
    return corpo.replace(ultimo, ultimo + link, 1)


def _domanda(b):
    return re.sub(r"<[^>]+>", "", re.search(r"<summary>(.*?)</summary>", b, re.S).group(1)).strip()


def pagina(corpi):
    """Corpo completo della pagina FAQ a partire dai corpi di tutte le pagine."""
    visti, sezioni, indice = set(), [], []
    for key, titolo in GRUPPI:
        voci = []
        for b in blocchi(corpi.get(key, "")):
            q = _domanda(b)
            if q in visti:
                continue
            visti.add(q)
            voci.append("          " + b.strip())
        if not voci:
            continue
        indice.append(f'<a href="#gruppo-{key}">{titolo}</a>')
        sezioni.append(
            f'      <section class="faq-gruppo" id="gruppo-{key}" aria-labelledby="t-{key}">\n'
            f'        <h2 id="t-{key}">{titolo}</h2>\n'
            f'        <div class="faq">\n' + "\n".join(voci) + '\n        </div>\n      </section>')
    return ('<nav class="faq-indice" aria-label="Argomenti">' + "".join(indice) + "</nav>\n" + "\n".join(sezioni))
