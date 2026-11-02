# Il Tagliando (/tagliando/)

Strumento gratuito di lead generation: l'albergatore scrive l'indirizzo del sito o della landing, vede subito tre semafori e riceve il report completo via email. Porta all'analisi di posizionamento; il libro è l'alternativa.
Scheda del sistema (obiettivo, criteri, semafori, uscite): https://claude.ai/artifact/HV2CXp6tBCKLYaE4bTSDyy

## Dove sta

| Pezzo | File |
|---|---|
| Pagina, modulo, schermata dei semafori | `src/pages/tagliando/index.html` (design system morbido, come il resto del sito) |
| Controlli lunghi in background (`pagina`, `velocita`), risultato in Netlify Blobs | `netlify/functions/tagliando-background.mjs`, `netlify/lib/tagliando-lavori.mjs` |
| Risultati pronti (GET), report, configurazione | `netlify/functions/tagliando.mjs` |
| Analisi, soglie, semafori, report email | `netlify/lib/tagliando.mjs` |
| Libreria delle frasi fatte (bozza da completare) | `netlify/lib/frasi-fatte.mjs` |
| Dipendenza della funzione (SDK di Claude) | `package.json` |

Lo stack è quello del sito (Netlify + Brevo) al posto di Lovable + Supabase previsti nella scheda: niente strumenti nuovi, e i contatti finiscono nella stessa lista Brevo con `FONTE` = «Il Tagliando».

## Come funziona

1. Il browser avvia insieme due funzioni in background (fino a 15 minuti, Netlify risponde subito 202): `pagina` (legge l'HTML, controlla le prove, l'AI legge il messaggio) e `velocita` (Google PageSpeed Insights, mobile). Ognuna salva il risultato in Netlify Blobs (store `tagliando`); la pagina chiede ogni 3 secondi se è pronto, per al massimo 3 minuti. Le funzioni normali si fermano dopo pochi secondi (codice 504): PageSpeed da solo ne richiede 20-40.
2. Ogni risultato torna firmato (HMAC). Poi il browser chiama `report`: la funzione verifica le firme, compone il report e:
   - manda il report a chi l'ha chiesto (Brevo, mittente Francesco, tag `tagliando-report`);
   - salva il contatto su Brevo (`FONTE` = «Il Tagliando», `PROFILO` = i tre semafori);
   - chi ha spuntato il consenso facoltativo entra anche nella lista della sequenza «errori dell'albergatore»;
   - manda la notifica a Francesco.
3. Se la pagina non si lascia leggere (sito tutto in JavaScript, blocco dei bot), il contatto si salva lo stesso e la notifica arriva a Francesco con il motivo, per rispondere a mano.

Ordine del report: tre semafori, il problema principale (sempre dal messaggio, se giallo o rosso), frasi fatte trovate, 2-4 altri punti con «cosa fare», poi le due uscite. Messaggio verde: il report lo dice e propone il libro, non l'analisi.

La lettura del messaggio usa Claude (`claude-opus-5-5`, effort `low`, risposta in JSON con schema fisso). È attivo il fallback automatico di Anthropic su un altro modello se la richiesta venisse rifiutata. All'AI arriva solo il testo della pagina, mai l'email.

## Configurazione su Netlify (Environment variables)

| Variabile | Serve a |
|---|---|
| `ANTHROPIC_API_KEY` | **obbligatoria**: lettura del messaggio |
| `PAGESPEED_API_KEY` | **di fatto obbligatoria**: senza chiave Google risponde quasi sempre «quota superata». Si crea gratis su Google Cloud (API PageSpeed Insights) |
| `TAGLIANDO_SECRET` | consigliata: una stringa lunga a caso per firmare i risultati (se manca usa `BREVO_API_KEY`) |
| `BREVO_LIST_TAGLIANDO` | facoltativa: lista dedicata (altrimenti `BREVO_LIST_DEFAULT`) |
| `BREVO_LIST_TAGLIANDO_SEQUENZA` | lista che fa partire la sequenza su Brevo: solo chi ha dato il consenso |

Più quelle di Brevo già in uso (`BREVO_API_KEY`, `BREVO_SENDER_EMAIL`, `NOTIFY_EMAIL`). Per avere i semafori come attributo del contatto, `BREVO_ATTRIBUTES` deve includere `PROFILO`.
Controllo rapido: `https://hotelpositioning.com/.netlify/functions/tagliando` mostra `true`/`false` per ogni variabile.

**Provare prima di pubblicare (0 crediti):** il branch di sviluppo ha i deploy di branch attivi (Project configuration › Build & deploy › Branches and deploy contexts › «Let me add individual branches»). Ogni push sul branch che tocca `site/` crea un'anteprima su `https://<nome-branch-con-trattini>--<nome-progetto>.netlify.app`: lì si aprono `/tagliando/` e `/.netlify/functions/tagliando`. Le variabili d'ambiente devono valere per tutti i deploy context, non solo per Production.

**Tempo:** di solito un minuto in tutto. I risultati restano in Netlify Blobs (pochi KB l'uno); si possono svuotare ogni tanto dal pannello di Netlify (Blobs › tagliando).

## Da fare (decisioni aperte della scheda)

- [ ] **Libreria delle frasi fatte**: la bozza in `netlify/lib/frasi-fatte.mjs` ha 56 voci scritte come prima proposta. Va riletta e completata da Francesco.
- [ ] **Tarare le soglie** su 15-20 siti reali (`SOGLIE` in `netlify/lib/tagliando.mjs`): le regole del messaggio sono quelle della scheda; quelle delle prove sono una prima proposta.
- [ ] Dominio: oggi `/tagliando/` sul sito. Sottodominio o dominio a sé?
- [ ] Limite di analisi per email o per IP, contro abusi e costi API (oggi non c'è).
- [ ] Sequenza «errori dell'albergatore» su Brevo: automazione sull'ingresso nella lista `BREVO_LIST_TAGLIANDO_SEQUENZA`.
- [ ] Report in PDF (oggi HTML via email) e screenshot della prima schermata dato all'AI (oggi l'AI legge il testo; lo screenshot di PageSpeed compare solo a schermo).
- [ ] Copy della pagina d'ingresso: prima versione scritta sul tono del sito, da validare.
- [ ] Collegare la pagina dal menu o da /risorse/ (oggi si raggiunge solo con il link diretto; `?url=` precompila l'indirizzo).
