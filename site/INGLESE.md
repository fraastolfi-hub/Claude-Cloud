# Versione inglese del sito (/en/)

Dal 3 novembre 2026. Scelte di Francesco: solo le pagine pubbliche (le landing delle campagne italiane restano in italiano), analisi e smontaggio consegnati in inglese, il libro presentato come «Italian edition», Tagliando Hotel con report in inglese, indirizzi con prefisso `/en/`.

## Dove sta

| Pezzo | File |
|---|---|
| Pagine | `src/pages/en/...` (una per ogni pagina italiana pubblica, con slug inglesi) |
| Parti comuni | `src/partials/*-en.html`: head-en (og:locale en_GB), header-en, footer-en, form-smontaggio-en, cookie-banner-en, exit-intent-en, sticky-candidatura-en |
| Coppie di pagine IT/EN | `build.py`, dizionario `IT2EN`: genera il selettore IT/EN (`@@ALT@@` nei menu) e i tag `hreflang` (it, en, x-default = italiano) |
| Testi negli script comuni | `src/assets/site.js`: variabile `EN` (da `<html lang="en">`), pop-up d'uscita con chiavi `/en/...`, passi del modulo, errore d'invio |
| Mail automatiche | `netlify/lib/brevo.mjs`: conferma dello smontaggio e mail degli strumenti in inglese quando il campo `pagina` comincia con `/en/`; la notifica a Francesco ha `[EN]` nell'oggetto |
| Tagliando Hotel | pagina `src/pages/en/tagliando/`; la pagina manda `lingua: 'en'`, l'AI scrive in inglese, testi del report in `netlify/lib/tagliando-en.mjs`, frasi fatte inglesi in `netlify/lib/frasi-fatte.mjs` (`FRASI_FATTE_EN`, bozza) |

## Indirizzi

| Italiano | Inglese |
|---|---|
| / | /en/ |
| /metodo/ | /en/method/ |
| /analisi/ | /en/analysis/ |
| /casi/ | /en/cases/ |
| /libro/ | /en/book/ |
| /risorse/ | /en/resources/ |
| /quiz/ | /en/quiz/ |
| /smontaggio/ | /en/teardown/ |
| /tagliando/ | /en/tagliando/ |
| /library/ | /en/library/ |
| /bonus/ (+ 7 strumenti) | /en/tools/ (+ stessi slug) |
| /francesco/ | /en/francesco/ |
| /privacy-policy/ | /en/privacy-policy/ |
| /problemi/booking, prezzi, sostituibili, agenzie, valore, apertura | /en/problems/booking, prices, replaceable, agencies, value, opening |

Restano solo in italiano: /guida/, /guida-hotel-romagna/, /cassetta/, /sfida/, /hday/, /questionario/, /vai/libro/. Il selettore EN su queste pagine porta a /en/.

## Glossario

smontaggio della homepage → homepage teardown · analisi di posizionamento → positioning analysis · posizionato / sostituibile / invisibile → positioned / replaceable / invisible · Tagliando Hotel resta «Tagliando Hotel» (the website check-up for hotels) · «Se non ti convince, ti pago io» → «If it doesn't convince you, I pay you» · inglese britannico.

## Quando si modifica una pagina italiana

La versione inglese non si aggiorna da sola: va ritoccata a mano in `src/pages/en/`. Le pagine generate (library, problemi) hanno i generatori solo in italiano: la versione inglese è HTML scritto a mano.
