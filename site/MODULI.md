# Moduli del sito: Netlify Forms + Brevo

I quattro moduli del sito vengono inviati a Netlify Forms. A ogni invio, la funzione `netlify/functions/submission-created.mjs`:

1. salva o aggiorna il contatto su **Brevo**, nella lista del modulo;
2. manda un'**email di notifica** con tutti i campi all'indirizzo indicato in `NOTIFY_EMAIL`. La risposta all'email va direttamente a chi ha compilato il modulo.

| Modulo (nome su Netlify) | Dove si trova | Valore di FONTE su Brevo |
|---|---|---|
| `candidatura` | home, analisi, casi, metodo, sintomi, landing analisi gratuita | Candidatura |
| `revisione-homepage` | /smontaggio/ | Revisione della homepage |
| `test-posizionamento` | /quiz/ | Test di posizionamento |
| `strumenti-libro` | /bonus/ | Strumenti del libro |

Configurazione scelta: **una sola lista** per tutti i contatti, con il campo `FONTE` che indica il modulo di provenienza (su Brevo i contatti non hanno tag: si filtra e si segmenta su `FONTE`). Liste separate per modulo restano possibili con le variabili `BREVO_LIST_CANDIDATURA` ecc.

Il filtro anti-spam di Netlify (campo nascosto `bot-field`) scarta gli invii automatici prima che arrivino a Brevo. Tutti gli invii restano consultabili anche su Netlify: Forms.

## Configurazione (una volta sola)

### Su Brevo
1. **Chiave API:** Impostazioni, poi SMTP e API, poi API Keys. Generate una chiave.
2. **Mittente:** Mittenti, domini e IP. Verificate l'indirizzo mittente (per esempio `noreply@hotelpositioning.com`) e, se possibile, autenticate il dominio.
3. **Lista:** Contatti, poi Liste. Create una lista (per esempio «Sito Hotel Positioning») e annotate il suo numero ID.
4. **Attributo FONTE:** Contatti, poi Impostazioni, poi Attributi. Create l'attributo `FONTE`, di tipo testo. Altri attributi facoltativi: `STRUTTURA`, `SITO`, `CAMERE`, `CONCORRENTI`, `PROFILO`, `PUNTEGGIO`, `PAGINA`.

### Su Netlify
1. **Forms:** Project configuration, poi Forms. Attivate il rilevamento dei moduli (form detection) e fate un nuovo deploy.
2. **Variabili d'ambiente:** Project configuration, poi Environment variables.

| Variabile | Valore |
|---|---|
| `BREVO_API_KEY` | la chiave API di Brevo |
| `NOTIFY_EMAIL` | l'indirizzo che riceve le notifiche (più indirizzi separati da virgola) |
| `BREVO_SENDER_EMAIL` | il mittente verificato su Brevo |
| `BREVO_LIST_DEFAULT` | ID della lista unica |
| `BREVO_ATTRIBUTES` | `FONTE` (oppure un elenco separato da virgole degli attributi creati su Brevo) |

3. Fate un nuovo deploy. Poi inviate un modulo di prova dal sito pubblicato e controllate: l'invio su Netlify Forms, il contatto su Brevo, l'email di notifica.

Se qualcosa non arriva: Netlify, poi Logs, poi Functions, poi `submission-created`.

## Note
- In anteprima (localhost o link di anteprima) i moduli mostrano solo la conferma: l'invio reale parte solo da `hotelpositioning.com` o da un dominio `netlify.app`.
- Le email automatiche ai contatti (primo capitolo del libro, risultato del test) si configurano su Brevo come automazioni sull'ingresso in lista.
- La privacy policy (/privacy-policy/) descrive già Netlify, Brevo e Google Fonts: se cambiano fornitori o moduli, va aggiornata.

# Google Analytics e Pixel di Meta

Gli script partono solo dopo il consenso dato nel banner dei cookie (`src/partials/cookie-banner.html`, `src/assets/consent.js`). Prima della scelta, o dopo un rifiuto, non viene caricato nulla. La scelta dura 6 mesi; il link «Preferenze cookie» nel piè di pagina riapre il banner.

**Per attivarli** inserite gli ID in `src/partials/head.html`:

```html
window.HP_TRACKING = { ga4: 'G-XXXXXXXXXX', metaPixel: '123456789012345' };
```

- `ga4`: l'ID di misurazione della proprietà GA4 (Amministrazione, poi Stream di dati).
- `metaPixel`: l'ID del set di dati/Pixel (Gestione eventi di Meta).

Se un ID resta vuoto, quello strumento è disattivato anche con il consenso.

**Eventi già collegati:** a ogni modulo inviato con successo partono `generate_lead` su GA4 e `Lead` su Meta, con il nome del modulo (`candidatura`, `revisione-homepage`, `test-posizionamento`, `strumenti-libro`). Su GA4 segnate `generate_lead` come evento chiave; su Meta usate `Lead` come conversione delle campagne.
