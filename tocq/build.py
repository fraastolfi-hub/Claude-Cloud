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
import lingue
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
        "description": "Hotel 4 stelle a Porta Garibaldi, la metro a 3 minuti: 133 camere, 6 sale meeting, cuscino e lato della camera scelti prenotando sul sito.",
        "nav": None,
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "camere": {
        "url": "/camere/",
        "title": "Camere e suite a Porta Garibaldi · Tocq Hotel Milano",
        "description": "Camere insonorizzate a Porta Garibaldi da 129 € a notte, colazione inclusa: Comfort, Superior, Executive, Junior Suite e Family Room. Scegli cuscino e lato della camera.",
        "nav": "Camere",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "meeting": {
        "url": "/meeting-eventi/",
        "title": "Sale meeting a Porta Nuova, Milano · Tocq Hotel",
        "description": "6 sale meeting fino a 100 persone a platea, nello stesso edificio delle 133 camere, a 3 minuti dalla metro Garibaldi. Preventivo entro 24 ore.",
        "nav": "Sale meeting",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "offerte": {
        "url": "/offerte/",
        "title": "Offerte e tariffe dirette · Tocq Hotel Milano",
        "description": "Prenota diretto al Tocq Hotel Milano: Direct Flex con cancellazione gratuita fino a 24 ore prima, Direct Save al 10% in meno. Colazione sempre inclusa.",
        "nav": "Miglior prezzo",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "posizione": {
        "url": "/posizione/",
        "title": "Posizione: hotel a Porta Garibaldi, Milano · Tocq Hotel",
        "description": "Il Tocq Hotel Milano è a 5 minuti a piedi dalla stazione Porta Garibaldi, a un minuto da Corso Como e dalle torri di Porta Nuova. Mappa del quartiere con aziende, ristoranti e negozi.",
        "nav": "Posizione",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "arrivare": {
        "url": "/posizione/come-arrivare/",
        "title": "Come arrivare al Tocq Hotel Milano · stazione Garibaldi",
        "description": "Distanze reali dal Tocq: metro Garibaldi 3 minuti a piedi, stazione 5, Centrale 1,5 km, Duomo 2,5 km, Linate 9 km, Malpensa 49 km con il Malpensa Express. Fiera, MiCo, San Siro.",
        "nav": "Come arrivare",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "quartiere-aziende": {
        "url": "/posizione/lavoro/",
        "title": "Aziende vicino al Tocq Hotel Milano · Porta Nuova",
        "description": "Le sedi aziendali di Porta Nuova a piedi dal Tocq Hotel Milano: UniCredit, Accenture, Microsoft, Google, Bending Spoons e altre, con i minuti a piedi.",
        "nav": "Per chi lavora",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "quartiere-mangiare": {
        "url": "/posizione/mangiare/",
        "title": "Dove mangiare vicino a Porta Garibaldi · Tocq Hotel Milano",
        "description": "Ristoranti, bar e colazioni a pochi minuti a piedi dal Tocq Hotel Milano, fra Corso Como, Corso Garibaldi e Isola: colazione, pranzo, aperitivo, cena.",
        "nav": "Mangiare e bere",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "quartiere-shopping": {
        "url": "/posizione/shopping/",
        "title": "Shopping a Corso Como e Gae Aulenti · Tocq Hotel Milano",
        "description": "Negozi a pochi minuti a piedi dal Tocq Hotel Milano: 10 Corso Como, Eataly, Feltrinelli, Nike e le vie di Corso Garibaldi e Gae Aulenti.",
        "nav": "Shopping",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "portanuova": {
        "url": "/comodo-per/porta-nuova/",
        "title": "Hotel a Porta Nuova, Milano: tutto a piedi · Tocq Hotel",
        "description": "Il Tocq Hotel Milano è dentro Porta Nuova: Corso Como a 1 minuto, Piazza Gae Aulenti a 3, il Bosco Verticale a 8. Cosa vedere, dove mangiare e lavorare, a piedi.",
        "nav": "Porta Nuova",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
        "landing": True,
    },
    "centrale": {
        "url": "/comodo-per/stazione-centrale/",
        "title": "Hotel vicino alla Stazione Centrale di Milano · Tocq Hotel",
        "description": "Dalla Stazione Centrale al Tocq Hotel Milano: due fermate di metro M2 fino a Garibaldi, poi 3 minuti a piedi. Treni, Malpensa Express, bus per gli aeroporti e cosa c'è intorno.",
        "nav": "Stazione Centrale",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
        "landing": True,
    },
    "privacy": {
        "url": "/privacy-policy/",
        "title": "Privacy policy e cookie policy · Tocq Hotel Milano",
        "description": "Informativa sul trattamento dei dati personali (art. 13 GDPR) e cookie policy del Tocq Hotel Milano.",
        "nav": "Privacy policy",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "eventi": {
        "url": "/comodo-per/",
        "title": "Hotel comodo per Fiera, MiCo, San Siro e Centrale · Tocq Hotel",
        "description": "Dal Tocq Hotel Milano senza cambi: Fiera Milano Rho in 15 minuti di treno, Allianz MiCo in 10 di metro, San Siro con la M5, Monza in treno, la Stazione Centrale a due fermate, Porta Nuova a piedi.",
        "nav": "Comodo per…",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "fiera": {
        "url": "/comodo-per/fiera-milano-rho/",
        "title": "Hotel per Fiera Milano Rho: 15 minuti di treno · Tocq Hotel",
        "description": "Dal Tocq Hotel Milano alla Fiera di Rho in treno senza cambi, 15 minuti da Porta Garibaldi. La sera sei a Corso Como. Calendario fiere 2026-2027 e prenotazione.",
        "nav": "Fiera Milano Rho",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
        "landing": True,
    },
    "sansiro": {
        "url": "/comodo-per/san-siro/",
        "title": "Hotel per concerti a San Siro: M5 diretta · Tocq Hotel Milano",
        "description": "Concerti allo stadio San Siro e agli I-Days all'Ippodromo: dal Tocq Hotel Milano la M5 lilla senza cambi. Dopo il live sei a Corso Como. Calendario 2027.",
        "nav": "Concerti a San Siro",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
        "landing": True,
    },
    "mico": {
        "url": "/comodo-per/allianz-mico/",
        "title": "Hotel per congressi all'Allianz MiCo · Tocq Hotel Milano",
        "description": "Dal Tocq Hotel Milano all'Allianz MiCo in 10 minuti di metro M5, senza cambi: si scende a Portello, a 50 metri dal centro congressi. Calendario congressi 2026-2027.",
        "nav": "Allianz MiCo",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
        "landing": True,
    },
    "monza": {
        "url": "/comodo-per/gran-premio-monza/",
        "title": "Hotel per il Gran Premio di Monza 2027 · Tocq Hotel Milano",
        "description": "Gran Premio d'Italia di Formula 1, 3-5 settembre 2027: da Porta Garibaldi il treno per Monza senza cambi. La sera sei a Corso Como. Prenota il weekend.",
        "nav": "Gran Premio di Monza",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
        "landing": True,
    },
    "mangiare": {
        "url": "/all-day-eating/",
        "title": "Ristorante e colazione · Tocq Hotel Milano, Porta Garibaldi",
        "description": "Colazione dalle 6:30 (anche da asporto e per ospiti esterni a 16 €), pranzo a buffet, aperitivo e cena al Clorofilla dalle 18:30 alle 23. La Veranda per eventi.",
        "nav": "All Day Eating",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "servizi": {
        "url": "/servizi/",
        "title": "Servizi, parcheggio e palestra · Tocq Hotel Milano",
        "description": "Reception 24 ore, garage convenzionato a 50 metri, palestra e piscina a prezzo convenzionato in Corso Como, animali ammessi, baby-sitting, stireria.",
        "nav": "Garage e servizi",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "galleria": {
        "url": "/galleria/",
        "title": "Foto del Tocq Hotel Milano · camere, hall, ristorante",
        "description": "Le foto del Tocq Hotel Milano a Porta Garibaldi: camere e bagni, hall e bar, ristorante, Veranda e piatti della cucina.",
        "nav": "Foto del Tocq",
        "og_image": "assets/img/foto/tocq-hotel-milano-og.jpg",
    },
    "planet": {
        "url": "/planet/",
        "title": "Meno plastica, carta e sprechi · Tocq Hotel Milano",
        "description": "Cosa fa il Tocq Hotel Milano: zero plastica, niente carta in camera, luci LED, lavanderia a basso consumo, dispenser riciclati. E tre gesti per gli ospiti.",
        "nav": "Il nostro impegno",
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
        "nav": "Contatti 24h",
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

CAMERE = [  # tipologia, numero, descrizione, prezzo "da" a notte (direzione, 27 ottobre 2026)
    ("Comfort", 14, "20 m², letto queen: camera insonorizzata per una o due notti di lavoro.", 129),
    ("Superior", 63, "22 m², letto matrimoniale con 4 cuscini, arredi su misura: la tipologia più diffusa.", 149),
    ("Executive", 35, "24 m², letto matrimoniale e bollitore con infusi: più spazio per lavorare in camera.", 179),
    ("Junior Suite", 21, "34 m², zona living separata dal letto, per ricevere senza scendere in hall.", 199),
    ("Family Room", None, "40 m², due camere Superior comunicanti con balcone, due letti matrimoniali e due bagni: fino a 4 adulti, più un bambino sotto i 2 anni nel letto dei genitori.", 239),
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
        "award": "Green Key, eco-label internazionale per le strutture turistiche (dal 2024)",
        "checkinTime": "14:00",
        "checkoutTime": "12:00",
        "sameAs": ["https://www.instagram.com/tocqhotelmilano/", "https://www.facebook.com/tocqhotelmilano",
                   "https://www.linkedin.com/company/tocq-hotel-milano-corso-como/"],
        "description": "Hotel 4 stelle a Porta Garibaldi, Milano, a 3 minuti a piedi dalla metro Garibaldi: 133 camere insonorizzate rinnovate nel 2021 e 6 sale meeting nello stesso edificio.",
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
                "Camere insonorizzate", "Smart TV", "Deposito bagagli",
                "Parcheggio convenzionato nelle vicinanze",
            ]
        ],
        "containsPlace": [{"@id": SITO + "/meeting-eventi/#sala-" + s[0].lower().replace(" ", "-")} for s in SALE],
        "parentOrganization": {"@type": "Organization", "name": FATTI["societa"], "vatID": "IT" + FATTI["piva"]},
    }


# pagine figlie: la voce madre nel breadcrumb
GENITORE = {"quartiere-aziende": "posizione", "quartiere-mangiare": "posizione", "quartiere-shopping": "posizione", "arrivare": "posizione",
            "portanuova": "eventi", "centrale": "eventi",
            "fiera": "eventi", "mico": "eventi", "sansiro": "eventi", "monza": "eventi"}


def breadcrumb_ld(key):
    p = PAGINE[key]
    if not p["nav"]:
        return None
    return {
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Tocq Hotel Milano", "item": SITO + "/"},
            *([{"@type": "ListItem", "position": 2, "name": PAGINE[GENITORE[key]]["nav"], "item": SITO + PAGINE[GENITORE[key]]["url"]}]
              if key in GENITORE else []),
            {"@type": "ListItem", "position": 3 if key in GENITORE else 2, "name": p["nav"], "item": SITO + p["url"]},
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
                "description": f"{desc}" + (f" {n} camere di questa tipologia al Tocq Hotel Milano." if n else ""),
                "offers": {"@type": "Offer", "priceCurrency": "EUR", "price": prezzo, "description": "Prezzo a notte a partire da, colazione inclusa, prenotando sul sito"},
                "containedInPlace": {"@id": HOTEL_ID},
                "amenityFeature": [
                    {"@type": "LocationFeatureSpecification", "name": a, "value": True}
                    for a in ["Insonorizzata", "Wifi", "Smart TV", "Minibar", "Cassaforte", "Bollitore per caffè e tè", "Scelta del cuscino"]
                ],
            }
            for nome, n, desc, prezzo in CAMERE
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
    if key == "mangiare":
        grafo += [
            {"@type": "Restaurant", "@id": SITO + "/all-day-eating/#clorofilla", "name": "Clorofilla",
             "description": "Wine bar con cucina del Tocq Hotel Milano: piatti di stagione, tradizione italiana con un tocco internazionale, aperitivo e cena.",
             "servesCuisine": ["Italiana", "Internazionale"], "openingHours": "Mo-Su 18:30-23:00",
             "telephone": FATTI["telefono"], "address": indirizzo_ld(), "containedInPlace": {"@id": HOTEL_ID}},
            {"@type": "FoodEstablishment", "@id": SITO + "/all-day-eating/#colazione", "name": "Colazione del Tocq Hotel Milano",
             "description": "Colazione a buffet italiana, americana, asiatica e halal, con opzioni senza glutine e vegane; da asporto dalle 5:30; aperta agli ospiti esterni a 16 €.",
             "openingHours": ["Mo-Fr 06:30-10:30", "Sa-Su 07:00-11:00"], "address": indirizzo_ld(), "containedInPlace": {"@id": HOTEL_ID}},
        ]
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
    if key.startswith("quartiere") or key == "posizione":
        import mappa
        pezzi = mappa.blocchi()
        if pezzi:
            cat = {"quartiere-aziende": "aziende", "quartiere-mangiare": "food", "quartiere-shopping": "shopping"}.get(key)
            punti = [q for q in pezzi["_punti"] if cat is None or q["categoria"] == cat]
            grafo.append(mappa.schema_luoghi(punti, SITO))
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


# caratteri in più per gli alfabeti che Jost (e Futura) non coprono
FONT_LINGUA = {
    "ar": '  <link href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@300;400;500;700&display=swap" rel="stylesheet">\n',
    "zh": '  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">\n',
}


def alternate(key):
    """hreflang verso le lingue in cui la pagina esiste davvero, più x-default sull'italiano."""
    righe = [f'  <link rel="alternate" hreflang="{l["hreflang"]}" href="{SITO}{lingue.URL[key][l["codice"]]}">'
             for l in lingue.LINGUE if lingue.attiva(l["codice"], key)]
    righe.append(f'  <link rel="alternate" hreflang="x-default" href="{SITO}{lingue.URL[key]["it"]}">')
    return "\n".join(righe)


def head(key, faq, codice="it"):
    p = PAGINE[key]
    l = lingue.PER_CODICE[codice]
    og_alt = "\n".join(f'  <meta property="og:locale:alternate" content="{x["og"]}">'
                       for x in lingue.LINGUE if x["codice"] != codice and lingue.attiva(x["codice"], key))
    return f"""<!doctype html>
<html lang="{l['hreflang']}" dir="{l['dir']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="format-detection" content="telephone=no">
  <title>{p['title']}</title>
  <meta name="description" content="{p['description']}">
  <!-- BOZZA: togliere noindex al lancio -->
  <meta name="robots" content="noindex, nofollow, noarchive, nosnippet, noimageindex">
  <meta name="googlebot" content="noindex, nofollow">
  <link rel="canonical" href="{SITO}{p['url']}">
{alternate(key)}
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{FATTI['nome']}">
  <meta property="og:locale" content="{l['og']}">
{og_alt}
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
{FONT_LINGUA.get(codice, "")}  <link rel="stylesheet" href="assets/style.css">
  <script type="application/ld+json">
{schema_pagina(key, faq)}
  </script>
</head>
<body class="tema-notte">

"""


def prenota_url(codice="it"):
    return f"https://book.blastness.com/?id_albergo=16496&amp;dc=6326&amp;lingua_int={lingue.PER_CODICE[codice]['blastness']}&amp;id_stile=21247"


def selettore_lingue(key, codice, t):
    """Tutte e nove le lingue, ciascuna scritta nella propria; quelle non ancora tradotte restano visibili ma spente."""
    voci = []
    for l in lingue.LINGUE:
        attr = f'lang="{l["hreflang"]}" dir="{l["dir"]}"'
        if l["codice"] == codice:
            voci.append(f'<li><a {attr} aria-current="true">{l["nome"]}</a></li>')
        elif lingue.attiva(l["codice"], key):
            voci.append(f'<li><a {attr} hreflang="{l["hreflang"]}" href="{SITO}{lingue.URL[key][l["codice"]]}">{l["nome"]}</a></li>')
        else:
            voci.append(f'<li><span {attr} aria-disabled="true" title="{t["lingua_presto"]}: {SITO}{lingue.URL[key][l["codice"]]}">{l["nome"]}</span></li>')
    corrente = lingue.PER_CODICE[codice]["codice"].upper()
    return (f'<details class="lingue"><summary aria-label="{t["lingua"]}: {lingue.PER_CODICE[codice]["nome"]}">{corrente}</summary>'
            f'<ul class="lingue__menu">{"".join(voci)}</ul></details>')


def header_landing(key, codice="it"):
    """Landing per le campagne: niente menu che porti fuori, solo marchio, telefono e Prenota."""
    t = lingue.ui(codice)
    return f"""
<a class="skip" href="#contenuto">{t['salta']}</a>
<header class="header header--landing">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/img/logo-orizzontale-neg.svg" alt="{t['logo_alt']}" width="92" height="44"></a>
    <a class="header__su" href="{GENITORE.get(key, 'index')}.html">{t['nav_' + GENITORE[key]] if key in GENITORE else 'Tocq Hotel Milano'}</a>
    <div class="header__azioni">
      <a class="header__tel" href="tel:{FATTI['tel_href']}">{FATTI['telefono']}</a>
      <a class="btn btn--primary btn--small" href="{prenota_url(codice)}" target="_blank" rel="noopener" data-prenota>{t['prenota']}</a>
    </div>
  </div>
</header>
"""


def header(key, codice="it"):
    t = lingue.ui(codice)
    # menu principale (sempre visibile) e voci secondarie (solo nel menu mobile; su desktop stanno nel footer)
    principali = [("posizione", t["nav_posizione"]), ("camere", t["nav_camere"]), ("mangiare", t["nav_mangiare"]), ("meeting", t["nav_meeting"]), ("eventi", t["nav_eventi"]), ("offerte", t["nav_offerte"]), ("contatti", t["nav_contatti"])]
    secondarie = [("servizi", t["nav_servizi"]), ("galleria", t["nav_galleria"]), ("planet", t["nav_planet"])]
    # sottopagine con menu a discesa (su mobile appaiono rientrate sotto la voce madre)
    sottomenu = {"posizione": [("quartiere-aziende", t["sub_lavoro"]), ("quartiere-mangiare", t["sub_mangiare"]),
                               ("quartiere-shopping", t["sub_shopping"]), ("arrivare", t["sub_arrivare"])],
                 "eventi": [("fiera", t["sub_fiera"]), ("mico", t["sub_mico"]), ("sansiro", t["sub_sansiro"]), ("monza", t["sub_monza"]),
                            ("centrale", t["sub_centrale"]), ("portanuova", t["sub_portanuova"])]}
    def voce(k, v, classe=""):
        corrente = k == key or any(k2 == key for k2, _ in sottomenu.get(k, []))
        return f'      <a href="{k}.html"{classe}{" aria-current=\"page\"" if corrente else ""}>{v}</a>'
    def gruppo(k, v):
        figli = [(k2, v2) for k2, v2 in sottomenu[k] if k2 in PAGINE]
        voci = "".join(f'<li><a href="{k2}.html"{" aria-current=\"page\"" if k2 == key else ""}>{v2}</a></li>' for k2, v2 in figli)
        return (f'      <div class="nav__gruppo">{voce(k, v).strip()}'
                f'<button type="button" class="nav__apri" aria-expanded="false" aria-controls="sub-{k}" aria-label="{t["sottomenu"]}: {v}"></button>'
                f'<ul class="nav__sub" id="sub-{k}">{voci}</ul></div>')
    links = "\n".join([gruppo(k, v) if k in sottomenu else voce(k, v) for k, v in principali if k in PAGINE] +
                       [voce(k, v, ' class="nav__secondaria"') for k, v in secondarie if k in PAGINE])
    return f"""
<a class="skip" href="#contenuto">{t['salta']}</a>
<header class="header">
  <div class="wrap">
    <a class="logo" href="index.html"><img src="assets/img/logo-orizzontale-neg.svg" alt="{t['logo_alt']}" width="92" height="44"></a>
    <button class="nav-toggle" aria-controls="nav" aria-expanded="false" data-apri="{t['menu']}" data-chiudi="{t['chiudi']}"><span class="nav-toggle__icona" aria-hidden="true"><i></i><i></i></span><span class="nav-toggle__testo">{t['menu']}</span></button>
    <nav class="nav" id="nav" aria-label="{t['nav_aria']}">
{links}
      <a class="nav__tel" href="tel:{FATTI['tel_href']}">{FATTI['telefono']}<small>{t['f_reception']}</small></a>
      {selettore_lingue(key, codice, t)}
      <a class="btn btn--primary btn--small" href="{prenota_url(codice)}" target="_blank" rel="noopener" data-prenota>{t['prenota']}</a>
    </nav>
  </div>
</header>
"""


def footer(codice="it"):
    f = FATTI
    t = lingue.ui(codice)
    pren = prenota_url(codice)
    return f"""
<div class="pattern pattern--salmone" aria-hidden="true"></div>
<footer class="footer">
  <div class="wrap">
    <div class="footer__grid">
      <div class="footer__logo"><img src="assets/img/logo-verticale-neg.svg" alt="Tocq Hotel Milano" width="81" height="110" loading="lazy"></div>
      <div>
        <h2 class="footer__h">Tocq Hotel Milano</h2>
        <address>{f['via']}<br>{f['cap']} {f['citta']}</address>
        <span>{t['f_hotel']} · {f['camere']} {t['f_camere']}</span>
        <span>{t['f_reception']}</span>
      </div>
      <div>
        <h2 class="footer__h">{t['f_scrivi']}</h2>
        <a href="tel:{f['tel_href']}">{f['telefono']}</a>
        <a href="mailto:{f['email']}">{f['email']}</a>
        <a href="mailto:{f['email_mice']}">{f['email_mice']}</a>
        <a class="footer__social" href="https://www.instagram.com/tocqhotelmilano/" target="_blank" rel="noopener"><svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r="1.1" fill="currentColor" stroke="none"/></svg><span>Instagram</span></a>
      </div>
      <div>
        <h2 class="footer__h">{t['f_soggiorna']}</h2>
        <a href="camere.html">{t['f_camere_suite']}</a>
        <a href="mangiare.html">{t['f_colazione']}</a>
        <a href="servizi.html">{t['nav_servizi']}</a>
        <a href="galleria.html">{t['nav_galleria']}</a>
        <a href="planet.html">{t['nav_planet']}</a>
        <a href="{pren}" target="_blank" rel="noopener" data-prenota>{t['f_prenota']}</a>
      </div>
      <div>
        <h2 class="footer__h">{t['f_lavora']}</h2>
        <a href="meeting.html">{t['f_sale']}</a>
        <a href="meeting.html#preventivo">{t['f_preventivo']}</a>
        <a href="contatti.html#aziende">{t['f_aziendali']}</a>
        <a href="eventi.html">{t['nav_eventi']}</a>
        <a href="fiera.html">Fiera Milano Rho</a>
        <a href="sansiro.html">Concerti a San Siro</a>
        <a href="mico.html">Congressi all'Allianz MiCo</a>
        <a href="monza.html">Gran Premio di Monza</a>
        <a href="centrale.html">Stazione Centrale</a>
        <a href="portanuova.html">Porta Nuova</a>
        <a href="posizione.html">{t['f_quartiere']}</a>
        <a href="arrivare.html">{t['f_arrivare']}</a>
        <a href="offerte.html">{t['f_offerte']}</a>
        <a href="faq.html">{t['f_faq']}</a>
      </div>
    </div>
    <a class="footer__greenkey" href="planet.html">
      <img class="footer__gk" src="assets/img/marchi/green-key.svg" alt="Marchio Green Key" width="44" height="55" loading="lazy">
      <span>{t['f_greenkey']}</span>
    </a>
    <div class="footer__base">
      <span>© 2026 {f['nome']} · {f['societa']} · {t['f_piva']} {f['piva']} · <a href="privacy.html">{t['f_privacy']}</a></span>
      <span>{t['f_bozza']} · <button type="button" class="note-toggle" aria-pressed="false">Mostra le note di lavoro</button></span>
    </div>
  </div>
</footer>

<div class="sticky-cta" aria-label="{t['cta_aria']}">
  <a class="btn btn--primary" href="{pren}" target="_blank" rel="noopener" data-prenota>{t['prenota']}</a>
  <a class="btn btn--chiama" href="tel:{f['tel_href']}" aria-label="{t['cta_chiama_aria']}" data-chiama><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 5a2 2 0 0 1 2-2z"/></svg>{t['cta_chiama']}</a>
</div>

<script src="assets/app.js"></script>
</body>
</html>
"""


def alternate_sitemap(key):
    righe = [f'    <xhtml:link rel="alternate" hreflang="{l["hreflang"]}" href="{SITO}{lingue.URL[key][l["codice"]]}"/>'
             for l in lingue.LINGUE if lingue.attiva(l["codice"], key)]
    righe.append(f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITO}{lingue.URL[key]["it"]}"/>')
    return "\n".join(righe)


def sitemap():
    voci = "".join(
        f"""  <url>
    <loc>{SITO}{p['url']}</loc>
    <lastmod>{AGGIORNATO}</lastmod>
{alternate_sitemap(k)}
  </url>
""" for k, p in PAGINE.items())
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
    camere = "\n".join(f"- {n}: " + (f"{q} camere. " if q else "") + f"{d} Da {p} € a notte, colazione inclusa." for n, q, d, p in CAMERE)
    return f"""# {f['nome']}

> Hotel 4 stelle a Porta Garibaldi, Milano, a 3 minuti a piedi dalla metro Garibaldi (M2, M5) e 5 dalla stazione di Milano Porta Garibaldi. {f['camere']} camere insonorizzate rinnovate nel 2021 e 6 sale meeting nello stesso edificio. È la base per chi è a Milano per lavorare, riunirsi, partire presto o andare a un evento raggiungibile da Garibaldi (Fiera Milano Rho, MiCo, San Siro, Autodromo di Monza).

## Fatti
- Indirizzo: {f['via']}, {f['cap']} {f['citta']}
- Check-in dalle 14:00, check-out fino alle 12:00; reception aperta 24 ore
- Telefono: {f['telefono']} (reception 24 ore) · Email: {f['email']} · Eventi: {f['email_mice']}
- Categoria: 4 stelle · Riapertura dopo ristrutturazione: aprile 2021
- Distanze a piedi (percorso reale): stazione Porta Garibaldi 5 minuti · metro Garibaldi 3 minuti · Corso Como 1 minuto · Accenture e Bending Spoons davanti all'hotel · Piazza Gae Aulenti e UniCredit 4 minuti · Bosco Verticale 8 minuti · Milano Centrale 1,5 km · Duomo 2,5 km · Linate 9 km · Malpensa 49 km (Malpensa Express da Garibaldi)
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


# Ritmo delle sezioni: due sezioni nere di fila pesano. Le sezioni con foto, trama o colore propri
# restano come sono; quelle semplici si alternano nero, chiaro, nero, e le chiare a loro volta
# alternano fondo pieno e fondo con il motivo del marchio.
TONO_FOTO = ("hero-full", "band", "section--foto", "finale", "capitolo--notte", "planet-hero", "hero--bleed")
TONO_SCURO = ("hero", "board", "mappa-sezione")
SCURE_PER_SCELTA = ('id="tariffe"',)  # sezioni disegnate per il nero: restano nere anche se ne segue un'altra
TONO_COLORE = ("section--verde",)


def ritmo(corpo):
    import re
    trovate = list(re.finditer(r'\n  <section class="([^"]*)"([^>]*)', corpo))

    def fisso(m):
        classi, resto = m.group(1).split(), m.group(2)
        if any(c in classi for c in TONO_FOTO):
            return "foto"
        if "faq-hero" in classi:  # hero di solo testo: segue il ritmo come una sezione semplice
            return None
        if any(c in classi for c in TONO_SCURO) or any(x in resto for x in SCURE_PER_SCELTA):
            return "scuro"
        if any(c in classi for c in TONO_COLORE):
            return "colore"
        return None

    fissi = [fisso(m) for m in trovate]
    toni, prima = [], "scuro"
    for k, f in enumerate(fissi):
        if f:
            tono = f
        else:
            tono = "chiaro" if prima in ("scuro", "foto") else "scuro"
            # guarda avanti: se dopo viene una sezione nera fissa, questa si schiarisce (meglio due chiare che due nere)
            if tono == "scuro" and k + 1 < len(fissi) and fissi[k + 1] in ("scuro", "foto"):
                tono = "chiaro"
        toni.append(tono)
        prima = tono
    out, ultimo, chiare = [], 0, 0
    for m, f, tono in zip(trovate, fissi, toni):
        classi, resto = m.group(1).split(), m.group(2)
        if not f and tono == "chiaro":
            classi = [c for c in classi if c != "section--dark"] + ["tono-chiaro"] + (["tono-trama"] if chiare % 2 else [])
            chiare += 1
        out.append(corpo[ultimo:m.start()] + f'\n  <section class="{" ".join(classi)}"{resto}')
        ultimo = m.end()
    return "".join(out) + corpo[ultimo:]


def main():
    lingue.modelli(PAGINE)
    import mappa
    pezzi = mappa.blocchi() or {}
    import eventi
    pezzi.update(eventi.blocchi())
    import faq as faq_pagina
    corpi = {}
    for key in PAGINE:
        corpo = (SRC / f"{key}.html").read_text()
        if pezzi:
            for segnaposto, testo in pezzi.items():
                if segnaposto.startswith("<!--"):
                    corpo = corpo.replace(segnaposto, testo)
        if pezzi and "_punti" in pezzi:  # schede e tempi per punti scelti: <!-- @guida:id1,id2 --> e <!-- @tempi:id1,id2 -->
            import re as _re
            corpo = _re.sub(r"<!-- @guida:([\w,-]+) -->", lambda m: mappa.guida_ids(pezzi["_punti"], m.group(1).split(",")), corpo)
            corpo = _re.sub(r"<!-- @tempi:([\w,-]+) -->", lambda m: mappa.tempi_ids(pezzi["_punti"], m.group(1).split(",")), corpo)
        corpi[key] = corpo
    for key in PAGINE:
        if key == "faq":
            corpo = corpi[key].replace("<!-- @faq-tutte -->", faq_pagina.pagina(corpi))
            import re as _re  # le domande scritte solo per la pagina FAQ sono già state raccolte: il modello si toglie
            corpo = _re.sub(r"\s*<!-- domande scritte solo per questa pagina.*?</template>", "", corpo, flags=_re.S)
            faq = estrai_faq(corpo)  # lo schema FAQPage sta solo sulla pagina FAQ
        elif PAGINE[key].get("landing"):
            corpo = corpi[key]  # nelle landing le domande restano tutte, con il loro schema FAQPage
            faq = estrai_faq(corpo)
        else:
            corpo = faq_pagina.accorcia(corpi[key], key)
            faq = []
        corpo = ritmo("\n" + corpo)
        testa = header_landing(key) if PAGINE[key].get("landing") else header(key)
        html = head(key, faq) + testa + '\n<main id="contenuto">' + corpo + "</main>\n" + footer()
        (OUT / f"{key}.html").write_text(html)
        print(f"{key}.html · {len(estrai_faq(corpo))} FAQ")
    (OUT / "sitemap.xml").write_text(sitemap())
    (OUT / "robots.txt").write_text(robots())
    (OUT / "llms.txt").write_text(llms())
    print("sitemap.xml · robots.txt · llms.txt")


if __name__ == "__main__":
    main()
