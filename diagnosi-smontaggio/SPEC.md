# Diagnosi immediata · Smontaggio

Primo step automatico dello Smontaggio di hotelpositioning.com.
L'albergatore inserisce l'URL e riceve subito un voto 0-100 sulla prima cosa che legge un ospite: headline, sottotitolo e prima schermata della homepage.

Principi di riferimento: skill `landing-hospitality` (idea-madre unica, specificità al posto degli aggettivi, headline sull'ospite, trust above the fold, CTA unica che dichiara il passo successivo, consapevolezza di Schwartz, scarsità onesta).

## Cosa fa la macchina, cosa fa Francesco

| | Diagnosi automatica | Smontaggio a mano |
|---|---|---|
| Voto 0-100 | Sì, su 8 parametri | Confermato o corretto |
| Concorrenti reali | No | Sì: headline di 3 hotel vicini a confronto |
| Recensioni | No | Sì: i 5 temi più lodati confrontati con il hero |
| Riscrittura | No | 3 headline + 1 sottotitolo + ragionamento |

## Estrazione del testo

1. Rendering con browser headless (Playwright), lingua `it-IT`, due viewport: desktop 1366×768 e mobile 390×844.
2. **Headline**: il primo `h1` visibile nella prima schermata. Se manca o è solo il logo, il blocco di testo visibile con il font più grande.
3. **Sottotitolo**: il primo blocco di testo sotto la headline, dentro la prima schermata.
4. Slider nel hero: si prende la prima slide.
5. **Prima schermata**: tutto il testo, i pulsanti e le immagini con `top < altezza viewport`.
6. Title e meta description: si leggono e si mostrano come informazione, fuori dal voto.
7. Sito illeggibile (blocco bot, tutto dentro un'immagine): si chiede all'albergatore di incollare headline e sottotitolo. Nessun voto inventato.

## Gli 8 parametri

| # | Parametro | Peso | Metodo |
|---|---|---|---|
| 1 | Indice di già visto | 25 | Dizionario + AI |
| 2 | Sostituibilità | 15 | AI |
| 3 | Idea-madre unica | 15 | AI |
| 4 | Distanza da ciò che vuoi dire | 10 | AI |
| 5 | Parla all'ospite | 10 | Regole |
| 6 | Prova nella prima schermata | 10 | Regole |
| 7 | CTA chiara | 10 | Regole |
| 8 | Apertura giusta per chi arriva | 5 | AI |
| – | Penalità scarsità finta | fino a −5 | Regole |

Voto finale = somma, limitata tra 0 e 100, arrotondata all'intero.

### 1. Indice di già visto (25)
Su headline + sottotitolo.

- `C` = cliché trovati con il dizionario `cliche.json` (confronto senza maiuscole e accenti, ogni voce conta una volta).
- `K` = elementi concreti: numeri significativi (non le stelle), nomi propri diversi dal nome dell'hotel e dalla sola città, persone, materiali, orari, luoghi precisi. Li estrae l'AI (campo `elementi_concreti`); si tengono solo quelli presenti alla lettera nel testo.

```
punti = 25 × limita(0.5 + 0.25·K − 0.25·C, 0, 1)
```

Esempi: 3 cliché e 0 concreti → 0. Nessuno dei due → 12,5. 2 concreti e 0 cliché → 25.

Nel report: headline e sottotitolo con i cliché in rosso e gli elementi concreti in verde.

### 2. Sostituibilità (15)
Se al posto del nome metti quello di un altro hotel dello stesso posto e della stessa categoria, la frase resta vera?

| Giudizio AI | Punti |
|---|---|
| `vera_per_quasi_tutti` | 0 |
| `vera_per_molti` | 7 |
| `solo_questo_hotel` | 15 |

`solo_questo_hotel` vale solo se l'AI cita alla lettera l'elemento che lo rende unico (campo `elemento_unico`). Senza citazione si scende a `vera_per_molti`.

Nota: è una stima senza dati sui concorrenti. Il confronto vero è nello Smontaggio a mano.

### 3. Idea-madre unica (15)
Quante promesse distinte fanno headline e sottotitolo (campo `promesse`).

| Promesse | Punti |
|---|---|
| 1 | 15 |
| 2 | 8 |
| 0 (solo nome o saluto) oppure 3 o più (elenco di servizi) | 0 |

### 4. Distanza da ciò che vuoi dire (10)
Confronto tra la risposta al modulo ("cosa vorresti che un ospite capisse di te, e che oggi la homepage non dice?") e headline + sottotitolo.

| Giudizio AI | Punti |
|---|---|
| `assente` | 0 |
| `accennato` | 5 |
| `esplicito` | 10 |

Nel report, una frase: *«Vuoi che capiscano: [X]. La tua homepage dice: [Y].»*

### 5. Parla all'ospite (10)
Si parte da 10 e si tolgono 3 punti per ogni segnale trovato in headline + sottotitolo (minimo 0):

- saluto: `benvenut[oiae]`, `welcome`
- l'azienda che parla di sé: `\bnostr[oaie]\b`, `\boffriamo\b`, `\bsiamo\b`, `vi aspettiamo`
- headline uguale al nome dell'hotel (dopo normalizzazione)
- la storia in apertura (solo headline): `dal (19|20)\d\d`, `da \d+ anni`, `generazioni`

### 6. Prova nella prima schermata (10)
Solo elementi visibili nella prima schermata (desktop o mobile, vale il migliore).

| Trovato | Punti |
|---|---|
| Voto con la fonte (`9,2 su Booking`, `4,8 ★ Google`) oppure numero di recensioni | 10 |
| Riconoscimento con nome (Travellers' Choice, Michelin, guida citata) senza numero | 6 |
| Solo frasi generiche ("ospiti soddisfatti", "i più amati") oppure nulla | 0 |

Segnali: testo `\d[,.]\d\s*(\/\s*(10|5)|su 10|su 5|★)`, `\d+\s+recensioni`; `alt`/`src` delle immagini con `tripadvisor|booking|google|holidaycheck|michelin`.

### 7. CTA chiara (10)
Pulsanti principali nella prima schermata: `<button>`, link con classi `btn|button|cta`, modulo del motore di prenotazione. Le voci del menu non contano.

Quantità (max 6):

| Pulsanti principali | Punti |
|---|---|
| 1 (oppure il modulo date del booking engine) | 6 |
| 2 | 3 |
| 0 oppure 3 o più | 0 |

Testo del pulsante principale (max 4):

| Tipo | Punti |
|---|---|
| Dice cosa succede dopo (`prezzi`, `disponibilità`, `date`, `preventivo`, `tariffa`) oppure modulo date | 4 |
| Generico (`prenota`, `book now`, `scopri`, `invia`, `di più`) | 1 |

### 8. Apertura giusta per chi arriva (5)
Sulla homepage arriva chi cerca già il nome dell'hotel o sta confrontando strutture: serve una promessa concreta.

| Tipo di apertura (AI) | Punti |
|---|---|
| `promessa_concreta` | 5 |
| `problema_soluzione` | 3 |
| `storia_immagine` | 2 |
| `vuota` (nome, saluto, slogan astratto) | 0 |

### Penalità: scarsità finta (fino a −5)
Nella prima schermata: `solo \d+ camer`, `ultim[ae] \d+`, `offerta scade`, `affrettati`, oppure un conto alla rovescia. −5 se trovata. Se la disponibilità viene dal booking engine vero, niente penalità.

## Fasce e verdetto

| Voto | Verdetto |
|---|---|
| 0–39 | Scritta come tutti gli altri |
| 40–69 | Quasi: il motivo c'è, ma è affogato |
| 70–84 | Ha un motivo, va affilato |
| 85–100 | Smontata: lavora già |

Le etichette riprendono il linguaggio della pagina /smontaggio ("Già visto" → "Smontata").

## Cosa vede l'albergatore

**Subito, senza email:**
- voto e verdetto
- headline e sottotitolo con i colori dell'Indice di già visto
- la frase sulla distanza (parametro 4)
- una riga sulla sostituibilità (parametro 2)

**Nello Smontaggio a mano (6 al mese):**
- il dettaglio degli 8 parametri
- confronto con 3 concorrenti reali
- temi delle recensioni contro la promessa del hero
- la verità cruda, 3 headline + 1 sottotitolo, il ragionamento
- voto rivisto, se il giudizio umano lo cambia

## Regole di onestà (non negoziabili)
- Barra di avanzamento vera, legata ai passaggi reali. Niente attese finte.
- Nessun numero fisso di problemi ("3 punti"): si mostra quello che c'è.
- Ogni frase citata nel report deve comparire alla lettera sulla pagina. Le citazioni dell'AI che non si trovano nel testo vengono scartate.
- Sito illeggibile: si dice, non si inventa un voto.
