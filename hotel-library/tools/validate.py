#!/usr/bin/env python3
"""Valida library-v4.json ed esporta i CSV per sito e fogli di calcolo.

Uso: python3 hotel-library/tools/validate.py
Esce con codice 1 se trova errori bloccanti.
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "library-v4.json"
EXPORT = ROOT / "export"

TIER = {"T1", "T2", "T3"}
VERIFICA = {"verificato", "da_verificare", "proposto"}
MATURITA = {"consolidato", "emergente", "nascente"}
PROPRIETA = {"indipendente", "gruppo_indipendente", "major"}
STATO = {"attivo", "acquisito", "venduto", "chiuso"}


def main() -> int:
    lib = json.loads(DATA.read_text(encoding="utf-8"))
    errors, warnings = [], []

    families = {f["codice"]: f for f in lib["famiglie"]}
    patterns = {}
    for p in lib["pattern"]:
        code = p["codice"]
        if code in patterns:
            errors.append(f"pattern duplicato: {code}")
        if not re.fullmatch(r"[A-L]\d{2}", code):
            errors.append(f"codice pattern non valido: {code}")
        if code[0] != p["famiglia"] or p["famiglia"] not in families:
            errors.append(f"{code}: famiglia incoerente ({p['famiglia']})")
        if p["maturita"] not in MATURITA:
            errors.append(f"{code}: maturità non valida")
        patterns[code] = p
    for p in lib["pattern"]:
        for c in p["correlati"]:
            if c not in patterns:
                errors.append(f"{p['codice']}: correlato inesistente {c}")

    motori = {m["id"] for m in lib.get("motori", [])}
    for p in lib["pattern"]:
        if motori:
            if not p.get("motore") or set(p["motore"]) - motori:
                errors.append(f"{p['codice']}: motore mancante o non valido {p.get('motore')}")
            if not isinstance(p.get("gestione_minima"), int) or not 0 <= p["gestione_minima"] <= 10:
                errors.append(f"{p['codice']}: gestione_minima non valida")

    names = Counter(p["nome"].lower() for p in lib["pattern"])
    for n, k in names.items():
        if k > 1:
            errors.append(f"nome pattern ripetuto: {n}")

    cats = {c["id"]: c for c in lib["categorie"]}
    for c in lib["categorie"]:
        for code in c["pattern_affini"]:
            if code not in patterns:
                errors.append(f"{c['id']}: pattern affine inesistente {code}")

    examples = {}
    for e in lib["esempi"]:
        eid = e["id"]
        if eid in examples:
            errors.append(f"esempio duplicato: {eid}")
        examples[eid] = e
        for field, allowed in (("tier", TIER), ("verifica", VERIFICA),
                               ("proprieta", PROPRIETA), ("stato", STATO)):
            if e[field] not in allowed:
                errors.append(f"{eid}: {field} non valido ({e[field]})")
        for code in e["pattern"]:
            if code not in patterns:
                errors.append(f"{eid}: pattern inesistente {code}")
        for cid in e["categorie"]:
            if cid not in cats:
                errors.append(f"{eid}: categoria inesistente {cid}")
        if e.get("motore") and set(e["motore"]) - {m["id"] for m in lib.get("motori", [])}:
            errors.append(f"{eid}: motore non valido {e['motore']}")
        if not e["pattern"] and not e["categorie"]:
            errors.append(f"{eid}: né pattern né categoria")
        if e["verifica"] == "verificato" and not e["evidenza"]:
            warnings.append(f"{eid}: verificato senza evidenza")

    for f in lib["fusion"]:
        e = examples.get(f["esempio"])
        if not e:
            errors.append(f"fusion: esempio inesistente {f['esempio']}")
            continue
        missing = set(f["pattern"]) - set(e["pattern"])
        if missing:
            errors.append(f"fusion {f['esempio']}: pattern non presenti nell'esempio {sorted(missing)}")
    for s in lib["segnali_trend"]:
        if s["esempio"] not in examples:
            errors.append(f"segnale: esempio inesistente {s['esempio']}")
        if s["categoria"] and s["categoria"] not in cats:
            errors.append(f"segnale: categoria inesistente {s['categoria']}")

    # Pattern senza casi pubblicabili: coerenti solo se dichiarati nascenti.
    published = {c for e in lib["esempi"] if e["verifica"] != "proposto" for c in e["pattern"]}
    strong = {c for e in lib["esempi"]
              if e["verifica"] != "proposto" and e["tier"] in ("T1", "T2") for c in e["pattern"]}
    for code, p in patterns.items():
        if code not in published and p["maturita"] != "nascente":
            warnings.append(f"{code} {p['nome']}: nessun esempio pubblicabile ma maturità '{p['maturita']}'")
        if code in strong and p["maturita"] == "nascente":
            warnings.append(f"{code} {p['nome']}: ha esempi T1/T2 ma è marcato nascente")

    export(lib, patterns, cats)
    report(lib, patterns, warnings, errors)
    return 1 if errors else 0


def export(lib, patterns, cats):
    EXPORT.mkdir(exist_ok=True)
    fam = {f["codice"]: f["nome"] for f in lib["famiglie"]}
    with open(EXPORT / "pattern.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["codice", "famiglia", "nome", "nome_tecnico", "definizione", "maturita", "motore",
                    "gestione_minima", "correlati", "esempi"])
        for p in lib["pattern"]:
            ex = [e["nome"] for e in lib["esempi"] if p["codice"] in e["pattern"]]
            w.writerow([p["codice"], fam[p["famiglia"]], p["nome"], p.get("nome_en", ""), p["definizione"],
                        p["maturita"], " ".join(p.get("motore", [])), p.get("gestione_minima", ""),
                        " ".join(p["correlati"]), "; ".join(ex)])
    with open(EXPORT / "esempi.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "nome", "paese", "area", "luogo", "proprieta", "stato", "tier",
                    "verifica", "caveat", "pattern", "categorie", "sito", "evidenza", "fonti", "note"])
        for e in lib["esempi"]:
            w.writerow([e["id"], e["nome"], e["paese"], e["area"], e["luogo"], e["proprieta"],
                        e["stato"], e["tier"], e["verifica"], "sì" if e["caveat"] else "",
                        " ".join(e["pattern"]),
                        "; ".join(cats[c]["nome"] for c in e["categorie"]),
                        e["sito"], e["evidenza"], " | ".join(e["fonti"]), e["note"]])
    with open(EXPORT / "categorie.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "nome", "definizione", "stadio", "pattern_affini", "esempi"])
        for c in lib["categorie"]:
            ex = [e["nome"] for e in lib["esempi"] if c["id"] in e["categorie"]]
            w.writerow([c["id"], c["nome"], c["definizione"], c["stadio"],
                        " ".join(c["pattern_affini"]), "; ".join(ex)])


def report(lib, patterns, warnings, errors):
    ex = lib["esempi"]
    print(f"Famiglie: {len(lib['famiglie'])}  Pattern: {len(patterns)}  "
          f"Categorie: {len(lib['categorie'])}  Esempi: {len(ex)}")
    print("Maturità pattern:", dict(Counter(p["maturita"] for p in lib["pattern"])))
    print("Verifica esempi:", dict(Counter(e["verifica"] for e in ex)))
    print("Proprietà esempi:", dict(Counter(e["proprieta"] for e in ex)))
    print("Area esempi:", dict(Counter(e["area"] for e in ex)))
    print("Italiani:", sum(1 for e in ex if e["paese"] == "Italia"))
    for w in warnings:
        print("AVVISO:", w)
    for e in errors:
        print("ERRORE:", e)
    print("OK" if not errors else f"{len(errors)} errori")


if __name__ == "__main__":
    sys.exit(main())
