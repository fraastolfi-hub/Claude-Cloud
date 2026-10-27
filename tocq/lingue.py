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
    "portanuova":{"it": "/posizione/porta-nuova/", "en": "/en/close-to/porta-nuova/", "fr": "/fr/a-proximite/porta-nuova/", "de": "/de/in-der-naehe/porta-nuova/", "pt": "/pt/perto-de/porta-nuova/", "es": "/es/cerca-de/porta-nuova/", "ru": "/ru/close-to/porta-nuova/", "ar": "/ar/close-to/porta-nuova/", "zh": "/zh/close-to/porta-nuova/"},
    "centrale":  {"it": "/posizione/stazione-centrale/", "en": "/en/close-to/milano-centrale-station/", "fr": "/fr/a-proximite/gare-milano-centrale/", "de": "/de/in-der-naehe/bahnhof-milano-centrale/", "pt": "/pt/perto-de/estacao-milano-centrale/", "es": "/es/cerca-de/estacion-milano-centrale/", "ru": "/ru/close-to/milano-centrale-station/", "ar": "/ar/close-to/milano-centrale-station/", "zh": "/zh/close-to/milano-centrale-station/"},
    "privacy":   {"it": "/privacy-policy/", "en": "/en/privacy-policy/", "fr": "/fr/politique-de-confidentialite/", "de": "/de/datenschutz/", "pt": "/pt/politica-de-privacidade/", "es": "/es/politica-de-privacidad/", "ru": "/ru/privacy-policy/", "ar": "/ar/privacy-policy/", "zh": "/zh/privacy-policy/"},
    "eventi":    {"it": "/posizione/sei-a-milano-per/", "en": "/en/close-to/", "fr": "/fr/a-proximite/", "de": "/de/in-der-naehe/", "pt": "/pt/perto-de/", "es": "/es/cerca-de/", "ru": "/ru/close-to/", "ar": "/ar/close-to/", "zh": "/zh/close-to/"},
    "fiera":     {"it": "/posizione/fiera-milano-rho/", "en": "/en/close-to/fiera-milano-rho/", "fr": "/fr/a-proximite/fiera-milano-rho/", "de": "/de/in-der-naehe/fiera-milano-rho/", "pt": "/pt/perto-de/fiera-milano-rho/", "es": "/es/cerca-de/fiera-milano-rho/", "ru": "/ru/close-to/fiera-milano-rho/", "ar": "/ar/close-to/fiera-milano-rho/", "zh": "/zh/close-to/fiera-milano-rho/"},
    "sansiro":   {"it": "/posizione/san-siro/", "en": "/en/close-to/san-siro/", "fr": "/fr/a-proximite/san-siro/", "de": "/de/in-der-naehe/san-siro/", "pt": "/pt/perto-de/san-siro/", "es": "/es/cerca-de/san-siro/", "ru": "/ru/close-to/san-siro/", "ar": "/ar/close-to/san-siro/", "zh": "/zh/close-to/san-siro/"},
    "mico":      {"it": "/posizione/allianz-mico/", "en": "/en/close-to/allianz-mico/", "fr": "/fr/a-proximite/allianz-mico/", "de": "/de/in-der-naehe/allianz-mico/", "pt": "/pt/perto-de/allianz-mico/", "es": "/es/cerca-de/allianz-mico/", "ru": "/ru/close-to/allianz-mico/", "ar": "/ar/close-to/allianz-mico/", "zh": "/zh/close-to/allianz-mico/"},
    "monza":     {"it": "/posizione/autodromo-monza/", "en": "/en/close-to/monza-grand-prix/", "fr": "/fr/a-proximite/grand-prix-monza/", "de": "/de/in-der-naehe/grand-prix-monza/", "pt": "/pt/perto-de/grande-premio-monza/", "es": "/es/cerca-de/gran-premio-monza/", "ru": "/ru/close-to/monza-grand-prix/", "ar": "/ar/close-to/monza-grand-prix/", "zh": "/zh/close-to/monza-grand-prix/"},
    "mangiare":  {"it": "/ristorante-e-bar/", "en": "/en/restaurant-and-bar/", "fr": "/fr/restaurant/", "de": "/de/restaurant/", "pt": "/pt/restaurante/", "es": "/es/restaurante/", "ru": "/ru/restaurant/", "ar": "/ar/restaurant/", "zh": "/zh/restaurant/"},
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
    "nav_mangiare": "Ristorante e bar",
    "nav_servizi": "Garage e servizi",
    "nav_galleria": "Foto del Tocq",
    "nav_planet": "Il nostro impegno",
    "nav_meeting": "Sale meeting",
    "nav_offerte": "Miglior prezzo",
    "nav_quartiere": "Il quartiere",
    "nav_posizione": "Posizione",
    "f_privacy": "Privacy e cookie",
    "f_greenkey": "Dal 2024 il Tocq ha il Green Key, l'eco-label internazionale per le strutture turistiche. Cosa facciamo in concreto, nella pagina del nostro impegno.",
    "nav_eventi": "Sei a Milano per…",
    "sub_portanuova": "Porta Nuova",
    "sub_centrale": "Dalla Stazione Centrale",
    "sub_fiera": "la Fiera di Rho",
    "sub_mico": "un congresso al MiCo",
    "sub_sansiro": "un concerto a San Siro",
    "sub_monza": "l'Autodromo di Monza",
    "tutti_eventi": "Tutte le destinazioni",
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
    "f_colazione": "Ristorante e bar",
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
