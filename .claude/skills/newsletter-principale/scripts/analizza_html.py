#!/usr/bin/env python3
"""Misura i segnali strutturali di una newsletter (HTML o testo) che pesano
sulla classificazione Principale/Promozioni di Gmail.

Uso:
    python3 analizza_html.py newsletter.html [--oggetto "..."] [--preheader "..."] [--json]

Solo libreria standard. Non invia nulla: legge il file e stampa le misure.
Le soglie sono euristiche, non regole di Gmail: servono a dare un ordine di
grandezza, il giudizio finale resta di chi revisiona.
"""
import argparse
import json
import re
import sys
from html import unescape
from html.parser import HTMLParser
from urllib.parse import urlparse, parse_qs

# Lessico commerciale: (regex, peso, etichetta). Peso 3 = forte, 1 = debole.
LESSICO = [
    (r"\bsconto|\bscontat|\bsconti\b", 3, "sconto"),
    (r"\d+\s?%|\bper ?cento\b", 3, "percentuale"),
    (r"€\s?\d[\d.,]*|\d[\d.,]*\s?€|\b\d+\s?euro\b", 2, "prezzo"),
    (r"\bofferta|\bofferte\b|\bpromo(zion\w*)?\b|\bdeal\b", 3, "offerta/promo"),
    (r"\bgratis\b|\bgratuit\w*|\bin omaggio\b|\bomaggio\b|\bregalo\b|\bfree\b", 2, "gratis/omaggio"),
    (r"\bprenota (ora|subito|adesso)\b|\bacquista\b|\bcompra\b|\bbook now\b|\bscopri (l'offerta|di più|ora)\b|\bapprofitta\w*", 3, "CTA commerciale"),
    (r"\bsolo per (oggi|pochi|te)\b|\bultim[ie] (post|camer|giorn|ore)\w*|\bscade\w*|\bscadenza\b|\bfino al\b|\bentro il\b|\ba tempo limitato\b|\blimitat\w*|\bnon perdere\b|\baffrettati\b|\bposti limitati\b|\blast minute\b|\bearly booking\b", 2, "urgenza/scarsità"),
    (r"\besclusiv\w*|\bimperdibil\w*|\bspecial[ei]\b|\bincredibil\w*|\bunic[ao] occasione\b", 1, "superlativo commerciale"),
    (r"\bcodice (sconto|promo)\b|\bcoupon\b|\bvoucher\b|\bgift ?card\b|\bbuono\b", 2, "coupon/voucher"),
    (r"\bmiglior prezzo\b|\bprezzo (speciale|bloccato|garantito)\b|\ba partire da\b|\bda soli\b|\bsoltanto\b", 2, "leva di prezzo"),
    (r"\baltre (proposte|offerte)\b|\bpotrebbe (anche )?interessarti\b|\bti potrebbero piacere\b|\bnon solo\b.*\boffert", 2, "blocco altre offerte"),
    (r"\bblack friday\b|\bcyber monday\b|\bsaldi\b", 3, "evento commerciale"),
]

SOCIAL = ("facebook.com", "instagram.com", "linkedin.com", "twitter.com", "x.com",
          "tiktok.com", "youtube.com", "pinterest.", "tripadvisor.")
TRACKING_PARAMS = ("utm_", "mc_cid", "mc_eid", "_hsenc", "_hsmi", "fbclid", "gclid")
BLOCK_TAGS = {"p", "div", "td", "tr", "h1", "h2", "h3", "h4", "h5", "h6", "li", "br", "table", "section", "article"}


class Parser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.testo = []
        self.nascosto = []          # testo in elementi display:none (preheader)
        self.immagini = []
        self.link = []
        self.bottoni = 0
        self.pixel = 0
        self.css_esterni = 0
        self._skip = 0              # dentro <style>/<script>/<head title>
        self._stack_hidden = []
        self._link_aperto = None

    def handle_starttag(self, tag, attrs):
        a = {k: (v or "") for k, v in attrs}
        style = a.get("style", "").replace(" ", "").lower()
        if tag in ("style", "script", "title"):
            self._skip += 1
        if tag == "link" and "stylesheet" in a.get("rel", ""):
            self.css_esterni += 1
        hidden = "display:none" in style or "max-height:0" in style
        if tag not in ("img", "br", "meta", "link", "hr", "input"):
            self._stack_hidden.append(hidden)
        if tag in BLOCK_TAGS:
            self.testo.append("\n")
        if tag == "img":
            w, h = a.get("width", ""), a.get("height", "")
            if (w in ("1", "0") and h in ("1", "0", "")) or ("width:1px" in style and "height:1px" in style):
                self.pixel += 1
            else:
                self.immagini.append({"src": a.get("src", ""), "alt": a.get("alt", ""), "width": w,
                                      "in_link": self._link_aperto is not None})
        if tag == "a":
            href = a.get("href", "")
            bottone = any(k in style for k in ("background:", "background-color:", "border-radius", "padding:"))
            if bottone and "display:block" not in style:
                self.bottoni += 1
            self._link_aperto = {"href": href, "testo": "", "bottone": bottone}
            self.link.append(self._link_aperto)

    def handle_endtag(self, tag):
        if tag in ("style", "script", "title") and self._skip:
            self._skip -= 1
        if tag not in ("img", "br", "meta", "link", "hr", "input") and self._stack_hidden:
            self._stack_hidden.pop()
        if tag == "a":
            self._link_aperto = None
        if tag in BLOCK_TAGS:
            self.testo.append("\n")

    def handle_data(self, data):
        if self._skip:
            return
        if any(self._stack_hidden):
            self.nascosto.append(data)
            return
        self.testo.append(data)
        if self._link_aperto is not None:
            self._link_aperto["testo"] += data


def righe_pulite(testo):
    righe = []
    for r in re.split(r"\n+", testo):
        r = re.sub(r"\s+", " ", r).strip()
        if r:
            righe.append(r)
    return righe


def colpi_lessico(testo):
    trovati = []
    for rx, peso, etichetta in LESSICO:
        for m in re.finditer(rx, testo, flags=re.I):
            trovati.append({"etichetta": etichetta, "match": m.group(0), "peso": peso})
    return trovati


def analizza(html, oggetti=(), preheader=""):
    is_html = bool(re.search(r"<(html|table|div|p|body)\b", html, re.I))
    p = Parser()
    if is_html:
        p.feed(html)
        testo = unescape("".join(p.testo))
    else:
        testo = html
    righe = righe_pulite(testo)
    corpo = " ".join(righe)
    parole = len(re.findall(r"\w+", corpo))

    domini = sorted({urlparse(l["href"]).netloc.lower() for l in p.link if l["href"].startswith("http")})
    tracciati = [l for l in p.link if any(t in l["href"] for t in TRACKING_PARAMS)]
    social = [l for l in p.link if any(s in l["href"] for s in SOCIAL)]
    unsub = [l for l in p.link if re.search(r"unsub|disiscri|cancella|annulla l'iscrizione|preferen", l["href"] + " " + l["testo"], re.I)]
    img_link = [i for i in p.immagini if i["in_link"]]
    img_no_alt = [i for i in p.immagini if not i["alt"].strip()]

    testi_bottoni = {re.sub(r"\s+", " ", l["testo"]).strip().lower() for l in p.link if l["bottone"]}
    analisi_righe = []
    for i, r in enumerate(righe, 1):
        colpi = colpi_lessico(r)
        if r.lower() in testi_bottoni:
            colpi.append({"etichetta": "testo di bottone", "match": "bottone CTA", "peso": 2})
        excl = r.count("!")
        # Una riga tutta maiuscola e corta è un'etichetta grafica: la contiamo a parte.
        etichetta = r.upper() == r and len(r.split()) <= 6
        maiusc = [] if etichetta else re.findall(r"\b[A-ZÀ-Ý]{4,}\b", r)
        emoji = len(re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", r))
        punti = sum(c["peso"] for c in colpi) + excl + (1 if maiusc else 0) + emoji
        analisi_righe.append({"n": i, "riga": r, "punti": punti,
                              "segnali": [c["match"] for c in colpi] + (["!" * excl] if excl else [])
                              + maiusc + (["emoji"] * emoji)})

    def sem(x, verde, giallo):
        return "verde" if x <= verde else ("giallo" if x <= giallo else "rosso")

    etichette_maiuscolo = sum(1 for r in righe if r.upper() == r and len(r.split()) <= 6 and re.search(r"[A-ZÀ-Ý]{3,}", r))
    ratio_img = round(len(p.immagini) / max(parole / 100, 1), 2)  # immagini ogni 100 parole
    strutturali = {
        "parole_visibili": parole,
        "immagini": len(p.immagini),
        "immagini_ogni_100_parole": ratio_img,
        "immagini_cliccabili": len(img_link),
        "immagini_senza_alt": len(img_no_alt),
        "link_totali": len(p.link),
        "domini_distinti": domini,
        "link_con_tracciamento_utm_o_esp": len(tracciati),
        "bottoni_cta": p.bottoni,
        "link_social": len(social),
        "link_disiscrizione": len(unsub),
        "pixel_tracciamento_nel_html": p.pixel,
        "css_esterni_o_webfont": p.css_esterni,
        "etichette_in_maiuscolo": etichette_maiuscolo,
        "preheader_nascosto": re.sub(r"\s+", " ", " ".join(p.nascosto)).strip()[:200],
        "dimensione_html_kb": round(len(html.encode("utf-8")) / 1024, 1),
    }
    semafori = {
        "immagini_ogni_100_parole": sem(ratio_img, 1, 2.5),
        "link_totali": sem(len(p.link), 3, 8),
        "bottoni_cta": sem(p.bottoni, 0, 1),
        "link_social": sem(len(social), 0, 2),
        "domini_distinti": sem(len(domini), 2, 4),
        "dimensione_html_kb": sem(strutturali["dimensione_html_kb"], 30, 90),
        "etichette_in_maiuscolo": sem(etichette_maiuscolo, 2, 5),
    }
    extra = {}
    voci = [(f"oggetto {chr(65 + i)}" if len(oggetti) > 1 else "oggetto", o) for i, o in enumerate(oggetti)]
    for nome, val in voci + [("preheader", preheader)]:
        if val:
            c = colpi_lessico(val)
            extra[nome] = {"testo": val, "segnali": [x["match"] for x in c] + (["!"] if "!" in val else []),
                           "punti": sum(x["peso"] for x in c) + val.count("!")}

    punti_righe = sum(r["punti"] for r in analisi_righe)
    punti_strutt = sum({"verde": 0, "giallo": 1, "rosso": 2}[v] for v in semafori.values())
    indice = punti_righe + 2 * punti_strutt + 2 * min([e["punti"] for k, e in extra.items() if k.startswith("oggetto")] or [0])  # con l'oggetto più pulito
    indice += 2 * extra.get("preheader", {}).get("punti", 0)
    rischio = "basso" if indice <= 6 else ("medio" if indice <= 18 else "alto")

    return {"rischio_indicativo": rischio, "indice": indice, "strutturali": strutturali,
            "semafori_strutturali": semafori, "oggetto_preheader": extra,
            "righe": analisi_righe}


def stampa(r):
    print(f"RISCHIO INDICATIVO: {r['rischio_indicativo'].upper()} (indice {r['indice']})\n")
    print("SEGNALI STRUTTURALI")
    for k, v in r["strutturali"].items():
        s = r["semafori_strutturali"].get(k)
        if isinstance(v, list):
            v = f"{len(v)} → " + ", ".join(v)
        print(f"  - {k}: {v}" + (f"  [{s}]" if s else ""))
    for nome, e in r["oggetto_preheader"].items():
        print(f"\n{nome.upper()}: {e['testo']}  → segnali: {', '.join(e['segnali']) or 'nessuno'}")
    print("\nRIGHE (punti >0 = da guardare)")
    for x in r["righe"]:
        flag = "🔴" if x["punti"] >= 3 else ("🟡" if x["punti"] > 0 else "🟢")
        seg = f"  ← {', '.join(x['segnali'])}" if x["segnali"] else ""
        print(f"  {flag} {x['n']:>3}. {x['riga'][:140]}{seg}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--oggetto", action="append", default=[],
                    help="ripetibile: passa ogni variante di oggetto (A/B/C)")
    ap.add_argument("--preheader", default="")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    with open(a.file, encoding="utf-8", errors="ignore") as f:
        html = f.read()
    r = analizza(html, a.oggetto, a.preheader)
    if a.json:
        json.dump(r, sys.stdout, ensure_ascii=False, indent=2)
    else:
        stampa(r)


if __name__ == "__main__":
    main()
