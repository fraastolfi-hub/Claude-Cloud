# Tocq Hotel Milano · bozza del nuovo sito

Lavoro per il cliente Tocq, fuori dal sito Hotel Positioning (non viene pubblicato da Netlify).

- `PROGETTO.md` – il progetto: dati di partenza, concept "Base a Garibaldi", obiettivi, alberatura, contenuti pagina per pagina, funzioni, tono, misure, fasi, domande aperte per la direzione.
- `BRAND.md` – le regole del brand book applicate al sito, con i colori in esadecimale e i file mancanti.
- `bozza/` – bozza navigabile della fase 1 (home, camere, meeting ed eventi, posizione, contatti). HTML statico: si apre `bozza/index.html` nel browser, senza build.

Nella bozza i segnaposto tratteggiati in giallo (classe `.todo`) sono dati da confermare: rimandano alle domande di `PROGETTO.md` §13.
La bozza applica il Brand Book Tocq v1.0: regole, colori e cosa manca in `BRAND.md`. Logo, simbolo e pattern vettoriali sono in `bozza/assets/img/`.
Le foto sono riquadri con una didascalia che fa anche da lista per lo shooting.

## Come si modifica

Le pagine di `bozza/` sono generate: si modifica il corpo in `src/pages/<pagina>.html` (o i fatti, i meta e i dati strutturati in `build.py`) e poi si lancia `python3 tocq/build.py`. Il generatore scrive anche `sitemap.xml`, `robots.txt` e `llms.txt`.
