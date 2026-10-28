# La verifica della sfida

Pagina: `/sfida/`. Brief del flusso: richiesta in due passi, bozza preparata con l'AI, revisione di Francesco, esito con Calendly o libro, promemoria.

## Il flusso

1. **Passo 1** (`verifica-invio`, `azione: passo1`): pagina della campagna ed email. Il contatto si salva qui (archivio e Brevo) e parte l'evento `Lead`. Link di portali (Booking, Expedia, Google…) rifiutati. Stessa email e stessa pagina negli ultimi 30 giorni: niente doppione. Massimo 5 richieste al giorno per email.
2. **Passo 2** (`azione: passo2`): campagna, visite al mese, partenza, nome.
   - **Meno di 2.000 visite:** «no» subito a schermo e per email, con il libro.
   - **Altrimenti:** parte `verifica-analisi-background` (fino a 15 minuti), che legge la pagina, prepara la bozza con Claude (esito sì/no, 2-3 punti con citazioni esatte, mai la soluzione) e manda a Francesco l'email «Rivedi e invia». Se la pagina non si legge, l'email arriva lo stesso, «senza bozza».
3. **Revisione** (`/verifica/rivedi/?id=…&t=…`, funzione `verifica-admin`): Francesco invia così com'è, corregge, salva o rifà l'analisi. Senza il suo clic non parte niente.
4. **Esito** (`/verifica/esito/?t=…`, funzione `verifica-esito`): verdetto, punti e, se è sì, Calendly incorporato (la prenotazione viene registrata); se è no, il libro.
5. **Promemoria** (`verifica-promemoria`, ogni mattina alle 8 UTC): dopo un sì senza call prenotata, un'email a 3 giorni e una a 7, poi basta.

## Archivio

Netlify Blobs, store `verifiche`: `r/<id>` la richiesta, `e/<token>` per la pagina dell'esito, `m/<hash email>/<id>` per i doppioni. Si consulta dal pannello Netlify (Blobs) o con `netlify blobs:list verifiche`.

## Configurazione (Netlify, Environment variables)

Oltre alle variabili Brevo già in uso (`BREVO_API_KEY`, `BREVO_SENDER_EMAIL`, `NOTIFY_EMAIL`, `BREVO_LIST_DEFAULT`, `BREVO_ATTRIBUTES`):

| Variabile | Valore |
|---|---|
| `ANTHROPIC_API_KEY` | chiave dell'API di Anthropic: senza, ogni richiesta arriva a Francesco «senza bozza» |
| `VERIFICA_SECRET` | una stringa lunga a caso: protegge la funzione di background |
| `VERIFICA_CALENDLY_URL` | il link Calendly della call di 60 minuti: senza, al posto del calendario c'è un pulsante email |
| `BREVO_LIST_VERIFICA` | facoltativa: lista Brevo dedicata (altrimenti `BREVO_LIST_DEFAULT`) |

Attributi Brevo facoltativi, da aggiungere a `BREVO_ATTRIBUTES` se creati: `SITO`, `PAGINA`, `VERIFICA_ESITO`. Il `FONTE` dei contatti è «Verifica della sfida».

Le dipendenze delle funzioni (`@anthropic-ai/sdk`, `@netlify/blobs`) sono in `package.json`: Netlify le installa da solo.

## Prova in locale

```bash
npx netlify-cli dev
```

Apre il sito con funzioni e archivio locali su http://localhost:8888. Con le variabili in un file `.env` nella cartella `site/` si prova anche l'invio delle email e la bozza.
