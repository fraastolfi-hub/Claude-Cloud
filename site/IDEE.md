# Idee per il tuo hotel (/idee/)

Strumento gratuito sul modello di marketingideas.ai, fatto per gli hotel e alimentato dall'Archivio del Marketing (/marketing-ideas/). L'albergatore lascia l'indirizzo del sito e l'email. In due o tre minuti vede tre idee scritte per il suo hotel, ognuna con i passi, il numero da guardare e l'esempio dell'archivio da cui parte. Porta allo smontaggio gratuito.

## Dove sta

| Pezzo | File |
|---|---|
| Pagina, modulo, attesa, idee | `src/pages/idee/index.html` (design system morbido, come /tagliando/) |
| Lavoro lungo in background (fino a 15 minuti, Netlify risponde 202) | `netlify/functions/idee-background.mjs` |
| Risultato pronto (GET `?id=`), controllo configurazione (GET senza id) | `netlify/functions/idee.mjs` |
| Lettura del sito, ricerca, scelta delle idee, cache, limiti | `netlify/lib/idee.mjs` |
| Lettura delle pagine e controllo degli indirizzi | riusati da `netlify/lib/tagliando.mjs` |
| Modulo Brevo `idee` | `netlify/lib/brevo.mjs` (`FORMS`) |

## Come funziona

1. **Il sito.** Legge la homepage e fino a 6 pagine interne, una per tipo: camere, offerte, preventivo, ristorante, benessere, storia, esperienze, eventi, recensioni. Raccoglie anche i percorsi delle pagine, così le idee citano pagine vere (`/offers/…`).
2. **La ricerca.** Claude (`claude-opus-5-5`, effort `low`) con la ricerca web, fino a 6 ricerche: concorrenti vicini, parole che tornano nelle recensioni, eventi in zona nei prossimi 6 mesi, buchi del sito. Esce un dossier di massimo 600 parole.
3. **Le idee.** Claude (`claude-opus-5-5`, effort `medium`, risposta JSON con schema fisso) riceve il dossier, il testo del sito e tutte le idee pubblicate dell'archivio. Ne sceglie 3, se possibile in canali diversi, e le scrive con la formula: verbo + cosa che solo quell'hotel ha + pagina o canale. Ogni idea deve citare l'id di un esempio dell'archivio: lo schema accetta solo id esistenti. L'archivio sta in un blocco del prompt messo in cache per un'ora.
4. **Contatto e notifica.** L'email va su Brevo (`FONTE` = «Idee per il tuo hotel»), anche se il sito non si lascia leggere. Francesco riceve la notifica con le idee uscite, o con il motivo del fallimento.

Fallback automatico su un altro modello se una richiesta venisse rifiutata, come nel Tagliando.

## Costi e limiti

- **Cache per sito:** 14 giorni (`CACHE_GIORNI`). Stesso indirizzo, stesse idee, nessuna nuova spesa.
- **Limiti:** 3 richieste al giorno per email, 150 al giorno in tutto (`LIMITE`). Oltre, la pagina chiede di riprovare domani.
- Un giro costa due chiamate a Claude più le ricerche web: indicativamente pochi centesimi, da misurare sui primi giri reali.

## Configurazione su Netlify

| Variabile | Serve a |
|---|---|
| `ANTHROPIC_API_KEY` | **obbligatoria** (già usata da Tagliando e archivio) |
| `BREVO_API_KEY`, `NOTIFY_EMAIL`, `BREVO_SENDER_EMAIL` | contatto e notifica (già in uso) |
| `BREVO_LIST_IDEE` | facoltativa: lista dedicata (altrimenti `BREVO_LIST_DEFAULT`) |
| `BREVO_LIST_IDEE_SEQUENZA` | facoltativa: chi spunta «mandami ogni tanto un'idea» |

Controllo rapido: `/.netlify/functions/idee` mostra `true`/`false` per ogni variabile.

## Da fare

- [ ] Provare 10-15 siti veri sul deploy di branch e rileggere le idee: tono, pagine citate, concorrenti.
- [ ] Decidere se mandare le idee anche via email (oggi solo a schermo, più la notifica a Francesco).
- [ ] Collegamento diretto alla scheda dell'archivio (oggi il link porta a /marketing-ideas/, che non apre una scheda precisa).
- [ ] L'archivio è sbilanciato su homepage e fase di valutazione (34 su 69): servono più esempi di email, soggiorno e post-soggiorno perché le tre idee stiano davvero in canali diversi.
- [ ] Collegare la pagina da /marketing-ideas/ e da /risorse/ (oggi solo link diretto; `?url=` precompila l'indirizzo).
