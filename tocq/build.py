#!/usr/bin/env python3
"""Tocq · genera le pagine della bozza.

I corpi delle pagine stanno in src/pages/<pagina>.html. Questo script aggiunge a ciascuna:
head (title, description, canonical, hreflang, Open Graph, dati strutturati), header, footer
e la barra di prenotazione mobile, e scrive bozza/<pagina>.html.

Tutti i fatti dell'hotel (indirizzo, telefono, numeri) stanno in FATTI: una sola fonte,
così pagine, dati strutturati e llms.txt dicono sempre la stessa cosa (conta per Google
e per gli assistenti AI, che premiano i dati coerenti e ripetuti).

Uso: python3 tocq/build.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src" / "pages"
OUT = ROOT / "bozza"
SITO = "https://www.tocq.it"  # dominio di produzione: canonical e dati strutturati puntano qui
AGGIORNATO = "2026-10-22"

# Fonti: factsheet 2025, presentazione MICE rev. 2, brand book 2018, analisi di posizionamento ott. 2026
FATTI = {
    "nome": "Tocq Hotel Milano",
    "via": "Via Alexis De Tocqueville 7/D",
    "cap": "20154",
    "citta": "Milano",
    "telefono": "+39 02 62071",
    "tel_href": "+390262071",
    "email": "info@tocq.it",
    "email_mice": "mice@tocq.it",
    "societa": "Fattore Italia srl",
    "piva": "08581970962",
    "stelle": 4,
    "camere": 133,
    # coordinate dalla scheda OpenStreetMap "Tocq Hotel Milano" (verificate il 22 ottobre 2026)
    "lat": 45.4827602,
    "lng": 9.1864205,
    "stazione_m": 200,
}

# Pagine: url finale, title (≤ 60 caratteri), description (≤ 155), dati per breadcrumb e Open Graph
PAGINE = {
    "index": {
        "url": "/",
        "title": "Tocq Hotel Milano · 4 stelle a Porta Garibaldi",
        "description": "Hotel 4 stelle a 200 m dalla stazione di Porta Garibaldi: 133 camere, 6 sale meeting, cuscino e lato della camera scelti prenotando sul sito.",
        "nav": None,
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "camere": {
        "url": "/camere/",
        "title": "Camere e suite a Porta Garibaldi · Tocq Hotel Milano",
        "description": "133 camere insonorizzate a Porta Garibaldi: Comfort, Superior, Executive, Junior Suite. Scegli cuscino, lato della camera e colazione da asporto.",
        "nav": "Camere",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "meeting": {
        "url": "/meeting-eventi/",
        "title": "Sale meeting a Porta Nuova, Milano · Tocq Hotel",
        "description": "6 sale meeting fino a 100 persone a platea, nello stesso edificio delle 133 camere, a 200 m dalla stazione Garibaldi. Preventivo entro 24 ore.",
        "nav": "Meeting ed eventi",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "offerte": {
        "url": "/offerte/",
        "title": "Offerte e tariffe dirette · Tocq Hotel Milano",
        "description": "Prenota diretto al Tocq Hotel Milano: Direct Flex con cancellazione gratuita fino a 24 ore prima, Direct Save al 10% in meno. Colazione sempre inclusa.",
        "nav": "Offerte",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "posizione": {
        "url": "/posizione/",
        "title": "Hotel vicino alla stazione Garibaldi · Tocq Hotel Milano",
        "description": "Distanze reali dal Tocq: stazione Garibaldi 200 m, Gae Aulenti 70 m, Centrale 1,5 km, Duomo 2,5 km, Linate 9 km, Malpensa 49 km. Fiera, MiCo, San Siro.",
        "nav": "La posizione",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "quartiere": {
        "url": "/quartiere/",
        "title": "Aziende, ristoranti e shopping vicino al Tocq · Milano",
        "description": "Mappa del quartiere del Tocq Hotel Milano: le aziende di Porta Nuova, treni e metro, negozi e ristoranti, ciascuno con i minuti a piedi dall'hotel.",
        "nav": "Il quartiere",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "faq": {
        "url": "/domande-frequenti/",
        "title": "Domande frequenti · Tocq Hotel Milano",
        "description": "Tutte le risposte su Tocq Hotel Milano: prenotazione, camere, colazione, sale meeting, come arrivare dalla stazione Garibaldi e dagli aeroporti, il quartiere.",
        "nav": "Domande frequenti",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "contatti": {
        "url": "/contatti/",
        "title": "Contatti · Tocq Hotel Milano, Porta Garibaldi",
        "description": "Tocq Hotel Milano, Via De Tocqueville 7/D. Reception 24 ore +39 02 62071, info@tocq.it. Meeting ed eventi: mice@tocq.it.",
        "nav": "Contatti",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
}

HOTEL_ID = SITO + "/#hotel"

SALE = [  # nome, m², misure, platea, scuola, ferro di cavallo, tavolo unico, cabaret, cocktail
    ("Duomo", 106, "9,2 × 10,7", 100, 45, 30, 30, 42, 90),
    ("Scala", 55, "8,9 × 5,2", 50, 22, 25, 25, None, 50),
    ("Brera", 53, "5,4 × 5,3", 50, 22, 25, 25, None, 50),
    ("Porta Nuova", 32, "9,1 × 5,9", 20, 10, 10, 10, None, 12),
    ("Castello", 32, "4,1 × 6,0", 20, 12, 12, 12, None, 12),
    ("Arena", 32, "4,5 × 6,0", 20, 12, 12, 12, None, 12),
]

CAMERE = [  # tipologia, numero, descrizione
    ("Comfort", 14, "Camera insonorizzata per una o due notti di lavoro."),
    ("Superior", 63, "La tipologia più diffusa: insonorizzata, con scrivania."),
    ("Executive", 35, "Più spazio per lavorare in camera."),
    ("Junior Suite", 21, "Zona giorno separata, per ricevere senza scendere in hall."),
]


def indirizzo_ld():
    return {
        "@type": "PostalAddress",
        "streetAddress": FATTI["via"],
        "postalCode": FATTI["cap"],
        "addressLocality": FATTI["citta"],
        "addressRegion": "MI",
        "addressCountry": "IT",
    }


def hotel_ld():
    return {
        "@type": "Hotel",
        "@id": HOTEL_ID,
        "name": FATTI["nome"],
        "alternateName": "Tocq Hotel",
        "description": "Hotel 4 stelle a Porta Garibaldi, Milano, a 200 metri dalla stazione: 133 camere insonorizzate rinnovate nel 2021 e 6 sale meeting nello stesso edificio.",
        "url": SITO + "/",
        "telephone": FATTI["telefono"],
        "email": FATTI["email"],
        "image": SITO + "/" + PAGINE["index"]["og_image"],
        "logo": SITO + "/assets/img/logo-verticale.svg",
        "address": indirizzo_ld(),
        "geo": {"@type": "GeoCoordinates", "latitude": FATTI["lat"], "longitude": FATTI["lng"]},
        "hasMap": "https://www.google.com/maps/search/?api=1&query=Tocq+Hotel+Milano",
        "starRating": {"@type": "Rating", "ratingValue": str(FATTI["stelle"])},
        "numberOfRooms": FATTI["camere"],
        "petsAllowed": True,
        "availableLanguage": ["it", "en", "de", "fr", "es"],
        "currenciesAccepted": "EUR",
        "amenityFeature": [
            {"@type": "LocationFeatureSpecification", "name": n, "value": True}
            for n in [
                "Reception 24 ore", "Guardia notturna", "Wifi ad alta velocità in tutto l'hotel",
                "6 sale meeting", "Menu dei cuscini", "Colazione da asporto",
                "Colazione a buffet con opzioni halal, senza glutine e vegane",
                "Camere insonorizzate", "Smart TV 55 pollici", "Deposito bagagli",
                "Parcheggio convenzionato nelle vicinanze",
            ]
        ],
        "containsPlace": [{"@id": SITO + "/meeting-eventi/#sala-" + s[0].lower().replace(" ", "-")} for s in SALE],
        "parentOrganization": {"@type": "Organization", "name": FATTI["societa"], "vatID": "IT" + FATTI["piva"]},
    }


def breadcrumb_ld(key):
    p = PAGINE[key]
    if not p["nav"]:
        return None
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Tocq Hotel Milano", "item": SITO + "/"},
            {"@type": "ListItem", "position": 2, "name": p["nav"], "item": SITO + p["url"]},
        ],
    }


def faq_ld(faq):
    return {
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq
        ],
    }


def schema_pagina(key, faq):
    p = PAGINE[key]
    grafo = [
        {
            "@type": "WebPage",
            "@id": SITO + p["url"] + "#pagina",
            "url": SITO + p["url"],
            "name": p["title"],
            "description": p["description"],
            "inLanguage": "it-IT",
            "dateModified": AGGIORNATO,
            "about": {"@id": HOTEL_ID},
            "isPartOf": {"@type": "WebSite", "@id": SITO + "/#sito", "url": SITO + "/", "name": FATTI["nome"]},
        },
        hotel_ld() if key == "index" else {"@id": HOTEL_ID, "@type": "Hotel", "name": FATTI["nome"], "address": indirizzo_ld(), "telephone": FATTI["telefono"]},
    ]
    if key == "camere":
        grafo += [
            {
                "@type": "HotelRoom",
                "@id": SITO + "/camere/#" + nome.lower().replace(" ", "-"),
                "name": nome,
                "description": f"{desc} {n} camere di questa tipologia al Tocq Hotel Milano.",
                "containedInPlace": {"@id": HOTEL_ID},
                "amenityFeature": [
                    {"@type": "LocationFeatureSpecification", "name": a, "value": True}
                    for a in ["Insonorizzata", "Wifi", "Smart TV 55 pollici", "Minibar", "Cassaforte", "Bollitore per caffè e tè", "Scelta del cuscino"]
                ],
            }
            for nome, n, desc in CAMERE
        ]
    if key == "meeting":
        for nome, mq, misure, platea, scuola, ferro, tavolo, cabaret, cocktail in SALE:
            grafo.append({
                "@type": "MeetingRoom",
                "@id": SITO + "/meeting-eventi/#sala-" + nome.lower().replace(" ", "-"),
                "name": "Sala " + nome,
                "description": f"Sala meeting di {mq} m² ({misure} m, altezza 2,9 m): {platea} persone a platea, {scuola} a banchi di scuola, {ferro} a ferro di cavallo, {cocktail} in piedi.",
                "floorSize": {"@type": "QuantitativeValue", "value": mq, "unitCode": "MTK"},
                "maximumAttendeeCapacity": max(platea, cocktail),
                "containedInPlace": {"@id": HOTEL_ID},
            })
    if key == "offerte":
        grafo.append({
            "@type": "OfferCatalog",
            "@id": SITO + "/offerte/#tariffe",
            "name": "Tariffe dirette del Tocq Hotel Milano",
            "itemListElement": [
                {"@type": "Offer", "name": "Direct Flex", "url": SITO + "/offerte/#tariffe", "offeredBy": {"@id": HOTEL_ID},
                 "description": "Tariffa diretta migliore con colazione inclusa, cancellazione gratuita fino a 24 ore prima dell'arrivo, pagamento in hotel."},
                {"@type": "Offer", "name": "Direct Save", "url": SITO + "/offerte/#tariffe", "offeredBy": {"@id": HOTEL_ID},
                 "description": "10% sotto qualsiasi altro canale, colazione inclusa, pagamento alla prenotazione, non modificabile né rimborsabile."},
            ],
        })
    b = breadcrumb_ld(key)
    if b:
        grafo.append(b)
    if key == "quartiere":
        import mappa
        pezzi = mappa.blocchi()
        if pezzi:
            grafo.append(mappa.schema_luoghi(pezzi["_punti"], SITO))
    if faq:
        grafo.append(faq_ld(faq))
    return json.dumps({"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)


def estrai_faq(corpo):
    """Le FAQ visibili nella pagina (<details class="faq">) diventano anche FAQPage: stesso testo, nessuna differenza."""
    import re
    faq = []
    for q, a in re.findall(r'<details class="faq__item">\s*<summary>(.*?)</summary>\s*<div>(.*?)</div>', corpo, re.S):
        testo = re.sub(r"<[^>]+>", "", a)
        testo = re.sub(r"\s+", " ", testo).strip()
        faq.append((re.sub(r"<[^>]+>", "", q).strip(), testo))
    return faq


def head(key, faq):
    p = PAGINE[key]
    return f"""<!doctype html>
<html lang="it">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{p['description']}">
  <!-- BOZZA: togliere noindex al lancio -->
  <meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
  <meta name="googlebot" content="noindex, nofollow">
  <link rel="canonical" href="{SITO}{p['url']}">
  <link rel="alternate" hreflang="it" href="{SITO}{p['url']}">
  <link rel="alternate" hreflang="en" href="{SITO}/en{p['url']}">
  <link rel="alternate" hreflang="x-default" href="{SITO}{p['url']}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{FATTI['nome']}">
  <meta property="og:locale" content="it_IT">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['description']}">
  <meta property="og:url" content="{SITO}{p['url']}">
  <meta property="og:image" content="{SITO}/{p['og_image']}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="theme-color" content="#0c0c0c">
  <meta name="geo.region" content="IT-MI">
  <meta name="geo.placename" content="Milano, Porta Garibaldi">
  <meta name="geo.position" content="{FATTI['lat']};{FATTI['lng']}">
  <link rel="icon" href="assets/img/simbolo.svg" type="image/svg+xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <!-- Futura Std (brand book) va servito con licenza web in produzione; nella bozza il sostituto è Jost -->
  <link href="https://fonts.googleapis.com/css2?family=Jost:ital,wght@0,300;0,400;0,500;0,700;1,300&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="assets/style.css">
  <script type="application/ld+json">
{schema_pagina(key, faq)}
  </script>
</head>
<body class="tema-notte">

"""


def header(key):
    voci = [("camere", "Camere"), ("meeting", "Meeting ed eventi"), ("offerte", "Offerte"), ("quartiere", "Il quartiere"), ("posizione", "Come arrivare"), ("contatti", "Contatti")]
    links = "\n".join(
        f'      <a href="{k}.html"{" aria-current=\"page\"" if k == key else ""}>{t}</a>' for k, t in voci
    )
    return f"""
<a class="skip" href="#contenuto">Vai al contenuto</a>
<header class="header">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/img/logo-orizzontale-neg.svg" alt="Tocq Hotel Milano, home" width="92" height="44"></a>
    <button class="nav-toggle" aria-controls="nav" aria-expanded="false">Menu</button>
    <nav class="nav" id="nav" aria-label="Principale">
{links}
      <span class="lang">IT · <a href="#" title="Inglese al lancio" lang="en">EN</a></span>
      <a class="btn btn--primary btn--small" href="https://book.blastness.com/?id_albergo=16496&amp;dc=6326&amp;lingua_int=ita&amp;id_stile=21247" target="_blank" rel="noopener" data-prenota>Prenota</a>
    </nav>
  </div>
</header>
"""


def footer():
    f = FATTI
    return f"""
<div class="pattern pattern--salmone" aria-hidden="true"></div>
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__logo"><img src="assets/img/logo-verticale-neg.svg" alt="Tocq Hotel Milano" width="81" height="110" loading="lazy"></div>
      <div>
        <h2 class="footer__h">Tocq Hotel Milano</h2>
        <address>{f['via']}<br>{f['cap']} {f['citta']}</address>
        <span>Hotel 4 stelle · {f['camere']} camere</span>
        <span>Reception aperta 24 ore</span>
      </div>
      <div>
        <h2 class="footer__h">Scrivi o chiama</h2>
        <a href="tel:{f['tel_href']}">{f['telefono']}</a>
        <a href="mailto:{f['email']}">{f['email']}</a>
        <a href="mailto:{f['email_mice']}">{f['email_mice']}</a>
      </div>
      <div>
        <h2 class="footer__h">Soggiorna</h2>
        <a href="camere.html">Camere e suite</a>
        <a href="camere.html#colazione">Colazione</a>
        <a href="https://book.blastness.com/?id_albergo=16496&amp;dc=6326&amp;lingua_int=ita&amp;id_stile=21247" target="_blank" rel="noopener" data-prenota>Prenota sul sito</a>
      </div>
      <div>
        <h2 class="footer__h">Lavora</h2>
        <a href="meeting.html">Sale meeting</a>
        <a href="meeting.html#preventivo">Richiedi un preventivo</a>
        <a href="contatti.html#aziende">Tariffe aziendali</a>
        <a href="quartiere.html">Il quartiere e le aziende</a>
        <a href="posizione.html">Come arrivare</a>
        <a href="offerte.html">Offerte e tariffe dirette</a>
        <a href="faq.html">Domande frequenti</a>
      </div>
    </div>
    <div class="footer__base">
      <span>© 2026 {f['nome']} · {f['societa']} · P.IVA {f['piva']}</span>
      <span>Bozza di lavoro a cura di Francesco Astolfi · non è il sito ufficiale · aggiornata il 22 ottobre 2026</span>
    </div>
  </div>
</footer>

<div class="sticky-cta" aria-label="Azioni rapide">
  <a class="btn btn--primary" href="https://book.blastness.com/?id_albergo=16496&amp;dc=6326&amp;lingua_int=ita&amp;id_stile=21247" target="_blank" rel="noopener" data-prenota>Prenota</a>
  <a class="btn" href="meeting.html#preventivo" aria-label="Richiedi un preventivo per un evento">Preventivo</a>
</div>

<script src="assets/app.js"></script>
</body>
</html>
"""


def sitemap():
    voci = "".join(
        f"""  <url>
    <loc>{SITO}{p['url']}</loc>
    <lastmod>{AGGIORNATO}</lastmod>
    <xhtml:link rel="alternate" hreflang="it" href="{SITO}{p['url']}"/>
    <xhtml:link rel="alternate" hreflang="en" href="{SITO}/en{p['url']}"/>
  </url>
""" for p in PAGINE.values())
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">
{voci}</urlset>
"""


def robots():
    # Versione di produzione. Gli assistenti AI sono ammessi apposta: il GEO serve a farsi citare.
    return f"""User-agent: *
Allow: /

User-agent: GPTBot
Allow: /

User-agent: OAI-SearchBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: Google-Extended
Allow: /

Sitemap: {SITO}/sitemap.xml
"""


def llms():
    f = FATTI
    sale = "\n".join(
        f"- Sala {n}: {mq} m², {pl} persone a platea, {sc} a banchi di scuola, {fc} a ferro di cavallo, {ck} in piedi"
        for n, mq, _, pl, sc, fc, _, _, ck in SALE)
    camere = "\n".join(f"- {n}: {q} camere. {d}" for n, q, d in CAMERE)
    return f"""# {f['nome']}

> Hotel 4 stelle a Porta Garibaldi, Milano, a {f['stazione_m']} metri dalla stazione di Milano Porta Garibaldi. {f['camere']} camere insonorizzate rinnovate nel 2021 e 6 sale meeting nello stesso edificio. È la base per chi è a Milano per lavorare, riunirsi, partire presto o andare a un evento raggiungibile da Garibaldi (Fiera Milano Rho, MiCo, San Siro, Autodromo di Monza).

## Fatti
- Indirizzo: {f['via']}, {f['cap']} {f['citta']}
- Telefono: {f['telefono']} (reception 24 ore) · Email: {f['email']} · Eventi: {f['email_mice']}
- Categoria: 4 stelle · Riapertura dopo ristrutturazione: aprile 2021
- Distanze: stazione Porta Garibaldi 200 m · Corso Como 50 m · Piazza Gae Aulenti 70 m · Bosco Verticale 100 m · Milano Centrale 1,5 km · Duomo 2,5 km · Linate 9 km · Malpensa 49 km (Malpensa Express da Garibaldi)
- Servizi: reception 24 ore con guardia notturna, menu dei cuscini (neckroll, kapok, lattice, piuma d'oca), colazione a buffet con opzioni halal, senza glutine e vegane, colazione da asporto, deposito bagagli, animali ammessi, parcheggio convenzionato

## Camere
{camere}

## Sale meeting (altezza 2,9 m)
{sale}

## Cosa sapere
- Il Tocq non è in centro storico: il Duomo è a 2,5 km.
- Le camere sul lato corte non danno sulla strada: si chiedono prenotando sul sito.
- Prenotando sul sito si scelgono cuscino, materasso e lato della camera.
- Tariffe dirette, colazione inclusa: Direct Flex (cancellazione gratuita fino a 24 ore prima, si paga in hotel) e Direct Save (10% sotto qualsiasi altro canale, prepagata, non rimborsabile).

## Pagine
- [Camere e suite]({SITO}/camere/)
- [Sale meeting ed eventi]({SITO}/meeting-eventi/)
- [Offerte e tariffe dirette]({SITO}/offerte/)
- [Posizione e distanze]({SITO}/posizione/)
- [Contatti]({SITO}/contatti/)

Aggiornato il {AGGIORNATO}.
"""


def main():
    import mappa
    pezzi = mappa.blocchi()
    import faq as faq_pagina
    corpi = {}
    for key in PAGINE:
        corpo = (SRC / f"{key}.html").read_text()
        if pezzi:
            for segnaposto, testo in pezzi.items():
                if segnaposto.startswith("<!--"):
                    corpo = corpo.replace(segnaposto, testo)
        corpi[key] = corpo
    for key in PAGINE:
        if key == "faq":
            corpo = corpi[key].replace("<!-- @faq-tutte -->", faq_pagina.pagina(corpi))
            import re as _re  # le domande scritte solo per la pagina FAQ sono già state raccolte: il modello si toglie
            corpo = _re.sub(r"\s*<!-- domande scritte solo per questa pagina.*?</template>", "", corpo, flags=_re.S)
            faq = estrai_faq(corpo)  # lo schema FAQPage sta solo sulla pagina FAQ
        else:
            corpo = faq_pagina.accorcia(corpi[key], key)
            faq = []
        html = head(key, faq) + header(key) + '\n<main id="contenuto">\n' + corpo + "</main>\n" + footer()
        (OUT / f"{key}.html").write_text(html)
        print(f"{key}.html · {len(estrai_faq(corpo))} FAQ")
    (OUT / "sitemap.xml").write_text(sitemap())
    (OUT / "robots.txt").write_text(robots())
    (OUT / "llms.txt").write_text(llms())
    print("sitemap.xml · robots.txt · llms.txt")


if __name__ == "__main__":
    main()
