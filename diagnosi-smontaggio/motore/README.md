# Motore della diagnosi

Legge la prima schermata di una homepage, chiede i giudizi al modello e calcola il voto secondo `../SPEC.md`.

| File | Cosa fa |
|---|---|
| `estrai.js` | Apre la pagina con Playwright (desktop e mobile) ed estrae hero, pulsanti, riprova sociale e testi fuori dal hero |
| `analizza.js` | Chiede i giudizi al modello (prompt, schema JSON, voto di maggioranza su 5 risposte) |
| `voto.js` | Verifica le citazioni, calcola i parametri, il voto, il verdetto e le segnalazioni |
| `diagnosi.js` | Comando che mette insieme i tre passaggi |
| `apify-pagefunction.mjs` | Genera la `pageFunction` per `apify/playwright-scraper` con lo stesso codice di `estrai.js` |

## Uso

```sh
npm install
export OPENAI_API_KEY=...
node diagnosi.js https://www.hotel.it/ --risposta "Che siamo l'unico hotel con..."
node diagnosi.js --estrazione prove/estrazioni/veridia.json   # senza browser, da un'estrazione salvata
```

Opzioni: `--nome` (nome dell'hotel), `--localita`, `--risposta` (la risposta alla domanda del modulo), `--salva file.json` (salva il risultato completo).

## Prove
`prove/estrazioni/` contiene le estrazioni di 6 siti fatte il 30/09/2026 e i risultati. `prove/ripeti.sh` rilancia la diagnosi su tutte e stampa voti e parametri: serve a controllare che una modifica alle regole o al prompt non sposti i voti in modo inatteso.

Risultati di riferimento (30/09/2026, `gpt-4.1`, 5 risposte, uguali in 3 giri consecutivi):

| Sito | Voto |
|---|---|
| stay.veridiaresort.com | 75 |
| olympicspahotel.it | 32 |
| veridiaresort.com/it | 29 |
| hoxton shoreditch | 16 |
| hotelmoko.it | 13 |
| clubfamilyhotelriccione.com | 9 |

## Limiti noti
- Il testo dentro le immagini non viene letto (es. il banner "perfect day" di Club Family).
- Gli slider mostrano slide diverse a ogni visita: la headline di Olympic è cambiata tra un giro e l'altro.
- Il dizionario dei cliché non distingue una parola usata come cliché da una usata per rovesciarlo ("true luxury means...").
