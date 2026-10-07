# Moduli del sito: Netlify Forms + Brevo

I quattro moduli del sito vengono inviati a Netlify Forms. A ogni invio, la funzione `netlify/functions/submission-created.mjs`:

1. salva o aggiorna il contatto su **Brevo**, nella lista del modulo;
2. manda un'**email di notifica** con tutti i campi all'indirizzo indicato in `NOTIFY_EMAIL`. La risposta all'email va direttamente a chi ha compilato il modulo.

| Modulo (nome su Netlify) | Dove si trova | Lista Brevo |
|---|---|---|
| `candidatura` | home, analisi, casi, metodo, sintomi, landing analisi gratuita | `BREVO_LIST_CANDIDATURA` |
| `revisione-homepage` | /smontaggio/ | `BREVO_LIST_REVISIONE` |
| `test-posizionamento` | /quiz/ | `BREVO_LIST_TEST` |
| `strumenti-libro` | /bonus/ | `BREVO_LIST_BONUS` |

Il filtro anti-spam di Netlify (campo nascosto `bot-field`) scarta gli invii automatici prima che arrivino a Brevo. Tutti gli invii restano consultabili anche su Netlify: Forms.

## Configurazione (una volta sola)

### Su Brevo
1. **Chiave API:** Impostazioni, poi SMTP e API, poi API Keys. Generate una chiave.
2. **Mittente:** Mittenti, domini e IP. Verificate l'indirizzo mittente (per esempio `noreply@hotelpositioning.com`) e, se possibile, autenticate il dominio.
3. **Liste:** Contatti, poi Liste. Create quattro liste (Candidature, Revisione homepage, Test di posizionamento, Strumenti del libro) e annotate i loro numeri ID.
4. **Attributi (facoltativo):** Contatti, poi Impostazioni, poi Attributi. Create come testo: `STRUTTURA`, `SITO`, `CAMERE`, `CONCORRENTI`, `PROFILO`, `PUNTEGGIO`, `FONTE`, `PAGINA`. Poi impostate `BREVO_ATTRIBUTES=1` su Netlify.

### Su Netlify
1. **Forms:** Project configuration, poi Forms. Attivate il rilevamento dei moduli (form detection) e fate un nuovo deploy.
2. **Variabili d'ambiente:** Project configuration, poi Environment variables.

| Variabile | Valore |
|---|---|
| `BREVO_API_KEY` | la chiave API di Brevo |
| `NOTIFY_EMAIL` | l'indirizzo che riceve le notifiche (più indirizzi separati da virgola) |
| `BREVO_SENDER_EMAIL` | il mittente verificato su Brevo |
| `BREVO_LIST_CANDIDATURA` | ID della lista |
| `BREVO_LIST_REVISIONE` | ID della lista |
| `BREVO_LIST_TEST` | ID della lista |
| `BREVO_LIST_BONUS` | ID della lista |
| `BREVO_LIST_DEFAULT` | facoltativa: lista usata se una delle precedenti manca |
| `BREVO_ATTRIBUTES` | `1` dopo aver creato gli attributi su Brevo |

3. Fate un nuovo deploy. Poi inviate un modulo di prova dal sito pubblicato e controllate: l'invio su Netlify Forms, il contatto su Brevo, l'email di notifica.

Se qualcosa non arriva: Netlify, poi Logs, poi Functions, poi `submission-created`.

## Note
- In anteprima (localhost o link di anteprima) i moduli mostrano solo la conferma: l'invio reale parte solo da `hotelpositioning.com` o da un dominio `netlify.app`.
- Le email automatiche ai contatti (primo capitolo del libro, risultato del test) si configurano su Brevo come automazioni sull'ingresso in lista.
- La privacy policy (/privacy-policy/) descrive già Netlify, Brevo e Google Fonts: se cambiano fornitori o moduli, va aggiornata.
