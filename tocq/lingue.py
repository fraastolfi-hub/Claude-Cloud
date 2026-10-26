"""Tocq · le nove lingue del sito.

Il sito nasce in italiano e verrà tradotto in inglese, francese, tedesco, portoghese, spagnolo, russo,
arabo e cinese. Qui stanno le regole che valgono per tutte: codice, nome nella propria lingua,
direzione del testo, prefisso dell'URL, lingua del booking engine e indirizzi delle pagine.

Una lingua va online (hreflang, sitemap, selettore attivo) solo quando esiste la sua cartella
src/pages/<codice>/ con la pagina tradotta: niente link a pagine che non ci sono.
I testi fissi (menu, footer, pulsanti) stanno in UI; le traduzioni arrivano in src/i18n/<codice>.json,
generati da questo file con le chiavi da riempire.
"""
import json
from pathlib import Path

RADICE = Path(__file__).parent

# codice, nome nativo, hreflang, og:locale, prefisso URL, direzione, lingua_int del booking engine Blastness
LINGUE = [
    {"codice": "it", "nome": "Italiano", "hreflang": "it", "og": "it_IT", "prefisso": "", "dir": "ltr", "blastness": "ita"},
    {"codice": "en", "nome": "English", "hreflang": "en", "og": "en_GB", "prefisso": "/en", "dir": "ltr", "blastness": "eng"},
    {"codice": "fr", "nome": "Français", "hreflang": "fr", "og": "fr_FR", "prefisso": "/fr", "dir": "ltr", "blastness": "fra"},
    {"codice": "de", "nome": "Deutsch", "hreflang": "de", "og": "de_DE", "prefisso": "/de", "dir": "ltr", "blastness": "deu"},
    {"codice": "pt", "nome": "Português", "hreflang": "pt", "og": "pt_PT", "prefisso": "/pt", "dir": "ltr", "blastness": "por"},
    {"codice": "es", "nome": "Español", "hreflang": "es", "og": "es_ES", "prefisso": "/es", "dir": "ltr", "blastness": "spa"},
    {"codice": "ru", "nome": "Русский", "hreflang": "ru", "og": "ru_RU", "prefisso": "/ru", "dir": "ltr", "blastness": "rus"},
    {"codice": "ar", "nome": "العربية", "hreflang": "ar", "og": "ar_AR", "prefisso": "/ar", "dir": "rtl", "blastness": "ara"},
    {"codice": "zh", "nome": "中文", "hreflang": "zh-Hans", "og": "zh_CN", "prefisso": "/zh", "dir": "ltr", "blastness": "chi"},
]
PER_CODICE = {l["codice"]: l for l in LINGUE}

# Indirizzi delle pagine per lingua: parole della lingua per le lingue in alfabeto latino,
# inglese traslitterato per russo, arabo e cinese (gli URL non latini si rompono quando vengono copiati)
URL = {
    "index":     {"it": "/", "en": "/en/", "fr": "/fr/", "de": "/de/", "pt": "/pt/", "es": "/es/", "ru": "/ru/", "ar": "/ar/", "zh": "/zh/"},
    "camere":    {"it": "/camere/", "en": "/en/rooms/", "fr": "/fr/chambres/", "de": "/de/zimmer/", "pt": "/pt/quartos/", "es": "/es/habitaciones/", "ru": "/ru/nomera/", "ar": "/ar/rooms/", "zh": "/zh/rooms/"},
    "meeting":   {"it": "/meeting-eventi/", "en": "/en/meetings-events/", "fr": "/fr/reunions-evenements/", "de": "/de/tagungen-events/", "pt": "/pt/reunioes-eventos/", "es": "/es/reuniones-eventos/", "ru": "/ru/meetings/", "ar": "/ar/meetings/", "zh": "/zh/meetings/"},
    "offerte":   {"it": "/offerte/", "en": "/en/offers/", "fr": "/fr/offres/", "de": "/de/angebote/", "pt": "/pt/ofertas/", "es": "/es/ofertas/", "ru": "/ru/offers/", "ar": "/ar/offers/", "zh": "/zh/offers/"},
    "posizione": {"it": "/posizione/", "en": "/en/location/", "fr": "/fr/emplacement/", "de": "/de/lage/", "pt": "/pt/localizacao/", "es": "/es/ubicacion/", "ru": "/ru/location/", "ar": "/ar/location/", "zh": "/zh/location/"},
    "arrivare": {"it": "/posizione/come-arrivare/", "en": "/en/location/getting-here/", "fr": "/fr/emplacement/acces/", "de": "/de/lage/anreise/", "pt": "/pt/localizacao/como-chegar/", "es": "/es/ubicacion/como-llegar/", "ru": "/ru/location/getting-here/", "ar": "/ar/location/getting-here/", "zh": "/zh/location/getting-here/"},
    "faq":       {"it": "/domande-frequenti/", "en": "/en/faq/", "fr": "/fr/faq/", "de": "/de/faq/", "pt": "/pt/faq/", "es": "/es/preguntas-frecuentes/", "ru": "/ru/faq/", "ar": "/ar/faq/", "zh": "/zh/faq/"},
    "quartiere-aziende": {"it": "/posizione/lavoro/", "en": "/en/location/business/", "fr": "/fr/emplacement/affaires/", "de": "/de/lage/business/", "pt": "/pt/localizacao/negocios/", "es": "/es/ubicacion/negocios/", "ru": "/ru/location/business/", "ar": "/ar/location/business/", "zh": "/zh/location/business/"},
    "quartiere-mangiare": {"it": "/posizione/mangiare/", "en": "/en/location/food/", "fr": "/fr/emplacement/restaurants/", "de": "/de/lage/essen/", "pt": "/pt/localizacao/comer/", "es": "/es/ubicacion/comer/", "ru": "/ru/location/food/", "ar": "/ar/location/food/", "zh": "/zh/location/food/"},
    "quartiere-shopping": {"it": "/posizione/shopping/", "en": "/en/location/shopping/", "fr": "/fr/emplacement/shopping/", "de": "/de/lage/shopping/", "pt": "/pt/localizacao/compras/", "es": "/es/ubicacion/compras/", "ru": "/ru/location/shopping/", "ar": "/ar/location/shopping/", "zh": "/zh/location/shopping/"},
    "eventi":    {"it": "/fiere-ed-eventi/", "en": "/en/trade-fairs-events/", "fr": "/fr/salons-evenements/", "de": "/de/messen-events/", "pt": "/pt/feiras-eventos/", "es": "/es/ferias-eventos/", "ru": "/ru/fairs-events/", "ar": "/ar/fairs-events/", "zh": "/zh/fairs-events/"},
    "fiera":     {"it": "/fiere-ed-eventi/fiera-milano-rho/", "en": "/en/trade-fairs-events/fiera-milano-rho/", "fr": "/fr/salons-evenements/fiera-milano-rho/", "de": "/de/messen-events/fiera-milano-rho/", "pt": "/pt/feiras-eventos/fiera-milano-rho/", "es": "/es/ferias-eventos/fiera-milano-rho/", "ru": "/ru/fairs-events/fiera-milano-rho/", "ar": "/ar/fairs-events/fiera-milano-rho/", "zh": "/zh/fairs-events/fiera-milano-rho/"},
    "sansiro":   {"it": "/fiere-ed-eventi/san-siro/", "en": "/en/trade-fairs-events/san-siro/", "fr": "/fr/salons-evenements/san-siro/", "de": "/de/messen-events/san-siro/", "pt": "/pt/feiras-eventos/san-siro/", "es": "/es/ferias-eventos/san-siro/", "ru": "/ru/fairs-events/san-siro/", "ar": "/ar/fairs-events/san-siro/", "zh": "/zh/fairs-events/san-siro/"},
    "mico":      {"it": "/fiere-ed-eventi/allianz-mico/", "en": "/en/trade-fairs-events/allianz-mico/", "fr": "/fr/salons-evenements/allianz-mico/", "de": "/de/messen-events/allianz-mico/", "pt": "/pt/feiras-eventos/allianz-mico/", "es": "/es/ferias-eventos/allianz-mico/", "ru": "/ru/fairs-events/allianz-mico/", "ar": "/ar/fairs-events/allianz-mico/", "zh": "/zh/fairs-events/allianz-mico/"},
    "monza":     {"it": "/fiere-ed-eventi/gran-premio-monza/", "en": "/en/trade-fairs-events/monza-grand-prix/", "fr": "/fr/salons-evenements/grand-prix-monza/", "de": "/de/messen-events/grand-prix-monza/", "pt": "/pt/feiras-eventos/grande-premio-monza/", "es": "/es/ferias-eventos/gran-premio-monza/", "ru": "/ru/fairs-events/monza-grand-prix/", "ar": "/ar/fairs-events/monza-grand-prix/", "zh": "/zh/fairs-events/monza-grand-prix/"},
    "mangiare":  {"it": "/all-day-eating/", "en": "/en/all-day-eating/", "fr": "/fr/restaurant/", "de": "/de/restaurant/", "pt": "/pt/restaurante/", "es": "/es/restaurante/", "ru": "/ru/restaurant/", "ar": "/ar/restaurant/", "zh": "/zh/restaurant/"},
    "servizi":   {"it": "/servizi/", "en": "/en/services/", "fr": "/fr/services/", "de": "/de/service/", "pt": "/pt/servicos/", "es": "/es/servicios/", "ru": "/ru/services/", "ar": "/ar/services/", "zh": "/zh/services/"},
    "galleria":  {"it": "/galleria/", "en": "/en/gallery/", "fr": "/fr/galerie/", "de": "/de/galerie/", "pt": "/pt/galeria/", "es": "/es/galeria/", "ru": "/ru/gallery/", "ar": "/ar/gallery/", "zh": "/zh/gallery/"},
    "planet":    {"it": "/planet/", "en": "/en/planet/", "fr": "/fr/planete/", "de": "/de/planet/", "pt": "/pt/planeta/", "es": "/es/planeta/", "ru": "/ru/planet/", "ar": "/ar/planet/", "zh": "/zh/planet/"},
    "contatti":  {"it": "/contatti/", "en": "/en/contact/", "fr": "/fr/contact/", "de": "/de/kontakt/", "pt": "/pt/contactos/", "es": "/es/contacto/", "ru": "/ru/contacts/", "ar": "/ar/contact/", "zh": "/zh/contact/"},
}

# Testi fissi di menu, footer e pulsanti. L'italiano è la fonte; le altre lingue arrivano dai file in src/i18n/
UI = {"it": {
    "salta": "Vai al contenuto",
    "logo_alt": "Tocq Hotel Milano, home",
    "menu": "Menu",
    "chiudi": "Chiudi",
    "nav_aria": "Principale",
    "nav_camere": "Camere",
    "nav_mangiare": "All Day Eating",
    "nav_servizi": "Garage e servizi",
    "nav_galleria": "Guarda il Tocq",
    "nav_planet": "Il nostro impegno",
    "nav_meeting": "Sale meeting",
    "nav_offerte": "Miglior prezzo",
    "nav_quartiere": "Il quartiere",
    "nav_posizione": "Posizione",
    "nav_eventi": "Fiere ed eventi",
    "sub_fiera": "Fiera Milano Rho",
    "sub_mico": "Congressi al MiCo",
    "sub_sansiro": "Concerti a San Siro",
    "sub_monza": "Gran Premio di Monza",
    "tutti_eventi": "Fiere ed eventi",
    "nav_arrivare": "Come arrivare",
    "sub_lavoro": "Per chi lavora",
    "sub_mangiare": "Mangiare e bere",
    "sub_shopping": "Shopping",
    "sub_arrivare": "Come arrivare",
    "sottomenu": "Apri il sottomenu",
    "nav_contatti": "Contatti 24h",
    "lingua": "Lingua",
    "lingua_presto": "In traduzione",
    "prenota": "Prenota",
    "f_hotel": "Hotel 4 stelle",
    "f_camere": "camere",
    "f_reception": "Reception aperta 24 ore",
    "f_scrivi": "Scrivi o chiama",
    "f_soggiorna": "Soggiorna",
    "f_camere_suite": "Camere e suite",
    "f_colazione": "All Day Eating",
    "f_prenota": "Prenota sul sito",
    "f_lavora": "Lavora",
    "f_sale": "Sale meeting",
    "f_preventivo": "Richiedi un preventivo",
    "f_aziendali": "Tariffe aziendali",
    "f_quartiere": "Posizione e quartiere",
    "f_arrivare": "Come arrivare",
    "f_offerte": "Miglior prezzo, prenotando qui",
    "f_faq": "Domande frequenti",
    "f_piva": "P.IVA",
    "f_bozza": "Bozza di lavoro a cura di Francesco Astolfi · non è il sito ufficiale · aggiornata il 22 ottobre 2026",
    "cta_aria": "Azioni rapide",
    "cta_chiama": "Chiama",
    "cta_chiama_aria": "Chiama la reception, risponde 24 ore su 24",
}}


def ui(codice):
    """Testi fissi nella lingua richiesta; ogni chiave non ancora tradotta resta in italiano."""
    testi = dict(UI["it"])
    f = RADICE / "src" / "i18n" / f"{codice}.json"
    if codice != "it" and f.exists():
        testi.update({k: v for k, v in json.loads(f.read_text()).get("ui", {}).items() if v})
    return testi


def attiva(codice, key):
    """Una pagina esiste in una lingua se c'è il suo sorgente tradotto (l'italiano c'è sempre)."""
    return codice == "it" or (RADICE / "src" / "pages" / codice / f"{key}.html").exists()


def modelli(pagine):
    """Scrive src/i18n/<codice>.json per i traduttori: stesse chiavi dell'italiano, valori vuoti da riempire."""
    cartella = RADICE / "src" / "i18n"
    cartella.mkdir(parents=True, exist_ok=True)
    for l in LINGUE[1:]:
        f = cartella / f"{l['codice']}.json"
        vecchio = json.loads(f.read_text()) if f.exists() else {}
        nuovo = {
            "_nota": f"Traduzione {l['nome']}. Riempire i valori vuoti; l'italiano di riferimento è in it.json. Regole di tono in PROGETTO.md §16.",
            "ui": {k: vecchio.get("ui", {}).get(k, "") for k in UI["it"]},
            "pagine": {k: {c: vecchio.get("pagine", {}).get(k, {}).get(c, "") for c in ("title", "description", "nav")} for k in pagine},
        }
        f.write_text(json.dumps(nuovo, ensure_ascii=False, indent=1) + "\n")
    (cartella / "it.json").write_text(json.dumps({
        "_nota": "Riferimento italiano: generato dal build, non modificare a mano.",
        "ui": UI["it"],
        "pagine": {k: {c: p[c] or "" for c in ("title", "description", "nav")} for k, p in pagine.items()},
    }, ensure_ascii=False, indent=1) + "\n")
