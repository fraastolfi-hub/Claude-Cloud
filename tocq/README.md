# Tocq Hotel Milano · bozza del nuovo sito

Lavoro per il cliente Tocq, fuori dal sito Hotel Positioning (non viene pubblicato da Netlify).

- `PROGETTO.md` – il progetto: dati di partenza, concept "Base a Garibaldi", obiettivi, alberatura, contenuti pagina per pagina, funzioni, tono, misure, fasi, domande aperte per la direzione.
- `JOURNEY.md` – il progetto di esperienza: percorso, racconto, sezioni, transizioni, interazioni e punti di conversione.
- `HERO.md` – le tre proposte per la prima schermata, il brief del video e le recensioni Trustindex.
- `BRAND.md` – le regole del brand book applicate al sito, con i colori in esadecimale e i file mancanti.
- `bozza/` – bozza navigabile della fase 1 (home, camere, meeting ed eventi, posizione, contatti). HTML statico: si apre `bozza/index.html` nel browser, senza build.

Nella bozza i segnaposto tratteggiati in giallo (classe `.todo`) sono dati da confermare: rimandano alle domande di `PROGETTO.md` §13.
La bozza applica il Brand Book Tocq v1.0: regole, colori e cosa manca in `BRAND.md`. Logo, simbolo e pattern vettoriali sono in `bozza/assets/img/`.
Le foto sono riquadri con una didascalia che fa anche da lista per lo shooting.

## Come si modifica

Le pagine di `bozza/` sono generate: si modifica il corpo in `src/pages/<pagina>.html` (o i fatti, i meta e i dati strutturati in `build.py`) e poi si lancia `python3 tocq/build.py`. Il generatore scrive anche `sitemap.xml`, `robots.txt` e `llms.txt`.

## Lavorare sul proprio computer

1. **Scaricare il progetto**
   - con Git: `git clone https://github.com/fraastolfi-hub/Claude-Cloud.git` e poi `git checkout claude/exciting-cannon-5mcwws`;
   - senza Git: su GitHub scegliere il ramo `claude/exciting-cannon-5mcwws`, poi **Code → Download ZIP**.
2. **Vedere il sito**: aprire `tocq/bozza/index.html` nel browser (doppio clic). Funziona senza server.
3. **Modificare e rigenerare**: i testi stanno in `tocq/src/pages/*.html`, i dati in `tocq/src/dati/`, lo stile in `tocq/bozza/assets/style.css`. Dopo ogni modifica: `python3 tocq/build.py` (serve Python 3; Pillow solo per rigenerare foto e mappe: `pip install pillow`).
4. **Continuare con Claude Code**: aprire Claude Code nella cartella del progetto scaricato, sullo stesso ramo. Il contesto del lavoro è nei file `PROGETTO.md`, `REVISIONE.md`, `BRAND.md` e `JOURNEY.md`.
