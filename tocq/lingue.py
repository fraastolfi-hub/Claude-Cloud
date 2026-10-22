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
    "posizione": {"it": "/posizione/", "en": "/en/location/", "fr": "/fr/acces/", "de": "/de/lage/", "pt": "/pt/localizacao/", "es": "/es/ubicacion/", "ru": "/ru/location/", "ar": "/ar/location/", "zh": "/zh/location/"},
    "quartiere": {"it": "/quartiere/", "en": "/en/neighbourhood/", "fr": "/fr/quartier/", "de": "/de/viertel/", "pt": "/pt/bairro/", "es": "/es/barrio/", "ru": "/ru/neighbourhood/", "ar": "/ar/neighbourhood/", "zh": "/zh/neighbourhood/"},
    "faq":       {"it": "/domande-frequenti/", "en": "/en/faq/", "fr": "/fr/faq/", "de": "/de/faq/", "pt": "/pt/faq/", "es": "/es/preguntas-frecuentes/", "ru": "/ru/faq/", "ar": "/ar/faq/", "zh": "/zh/faq/"},
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
    "nav_meeting": "Meeting ed eventi",
    "nav_offerte": "Offerte",
    "nav_quartiere": "Il quartiere",
    "nav_posizione": "Come arrivare",
    "nav_contatti": "Contatti",
    "lingua": "Lingua",
    "lingua_presto": "In traduzione",
    "prenota": "Prenota",
    "f_hotel": "Hotel 4 stelle",
    "f_camere": "camere",
    "f_reception": "Reception aperta 24 ore",
    "f_scrivi": "Scrivi o chiama",
    "f_soggiorna": "Soggiorna",
    "f_camere_suite": "Camere e suite",
    "f_colazione": "Colazione",
    "f_prenota": "Prenota sul sito",
    "f_lavora": "Lavora",
    "f_sale": "Sale meeting",
    "f_preventivo": "Richiedi un preventivo",
    "f_aziendali": "Tariffe aziendali",
    "f_quartiere": "Il quartiere e le aziende",
    "f_arrivare": "Come arrivare",
    "f_offerte": "Offerte e tariffe dirette",
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
