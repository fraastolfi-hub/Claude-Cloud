# Diagnosi immediata · Smontaggio

Primo step automatico dello Smontaggio di hotelpositioning.com.
L'albergatore inserisce l'URL e riceve subito un voto 0-100 su quello che un ospite vede nei primi 3 secondi: la prima schermata della homepage.

La domanda a cui risponde: **in quella schermata c'è un posizionamento, e viene eseguito bene?**

## Cosa fa la macchina, cosa fa Francesco

| | Diagnosi automatica | Smontaggio a mano |
|---|---|---|
| Voto 0-100 | Sì | Confermato o corretto |
| Concorrenti reali | No (solo stima della sostituibilità) | Sì: headline di 3 hotel vicini a confronto |
| Recensioni | No | Sì: i 5 temi più lodati confrontati con il hero |
| Riscrittura | No | 3 headline + 1 sottotitolo + ragionamento |

## Estrazione della prima schermata

1. Rendering con browser headless (Playwright), lingua `it-IT`, due viewport: desktop 1366×768 e mobile 390×844. Vale la versione peggiore delle due: l'ospite può arrivare da entrambe.
2. **Si escludono**: menu e navigazione, pulsanti e link a forma di pulsante, moduli (etichette, campi, titoli dei moduli), banner cookie e consenso, popup e finestre modali (`role=dialog`, `aria-modal`, classi `modal|popup|newsletter|cookie|consent|iubenda|onetrust|cmp`), logo.
3. **Testo del hero** = tutto il testo rimasto con `top < altezza viewport`:
   - **headline**: l'`h1` visibile; se non c'è, il blocco di almeno 3 parole con il font più grande;
   - **sottotitolo**: il primo blocco sotto la headline;
   - **supporto**: gli altri testi visibili (badge, claim, barre promozionali).
4. **Frase visibile**: vero se esiste una headline nella prima schermata e il suo centro non è coperto da un popup (`elementFromPoint`).
5. Slider nel hero: si prende la prima slide.
6. **Fuori dal hero** (non entrano nel voto, servono al controllo "parole nel posto sbagliato"): title, meta description, `h1` fuori dalla prima schermata.
7. Sito illeggibile (blocco bot, testo solo dentro immagini): si chiede all'albergatore di incollare headline e sottotitolo. Nessun voto inventato.

## I parametri

### Posizionamento (45)

La macchina prova a completare questa frase usando **solo il testo del hero**:

> *Per* **[target]**, *[hotel] è* **[beneficio]**, *a differenza di* **[alternativa]**.

| Casella | Peso | Giudizio AI → punti |
|---|---|---|
| **Target** | 15 | `esplicito_escludente` 15 · `implicito` 7 · `assente` 0 |
| **Beneficio** | 15 | `concreto` 15 · `generico` 7 · `solo_caratteristiche` 4 · `assente` 0 |
| **Differenziazione** | 15 | `solo_questo_hotel` 15 · `vera_per_molti` 7 · `vera_per_quasi_tutti` 0 |

- **Target** esplicito ed escludente: nomina persone e lascia fuori qualcuno ("solo adulti 14+", "famiglie con bambini sotto i 6 anni", "chi viaggia in bici"). Implicito: si intuisce ("Family" nel nome, "romantico"). "Per famiglie e coppie" o "per tutti" = assente.
- **Beneficio**: cosa ottiene l'ospite. Concreto = verificabile e specifico ("il primo bagno in piscina prima che arrivino gli altri"). Generico = relax, vacanza da sogno. Solo caratteristiche = elenco di dotazioni (piscina, spa, 3 stelle) senza dire cosa cambia per l'ospite. Offerte e sconti non sono un beneficio del soggiorno.
- **Differenziazione**: test della sostituibilità. Se metti il nome di un altro hotel della stessa zona e categoria (o di un'alternativa: Airbnb, il resort grande, stare a casa), la frase resta vera? `solo_questo_hotel` vale solo con citazione alla lettera dell'elemento che lo rende unico.

Nel report la frase compare con le caselle vuote in evidenza:
*«Per [vuoto], Veridia è un rifugio sul mare tra silenzio e natura, a differenza di [vuoto].»*

### Esecuzione (55)

#### Hook entro 3 secondi (15)
Visibilità (max 6), si calcola con regole:

| Condizione | Punti |
|---|---|
| Frase visibile nella prima schermata e non coperta | 2 |
| Headline di 12 parole o meno | 2 |
| Headline è il testo più grande del hero | 2 |

Contenuto (max 9), giudizio AI sul tipo di apertura:

| Apertura | Punti |
|---|---|
| `promessa_concreta` (un elemento specifico dell'esperienza, non solo il nome del luogo) | 9 |
| `problema_soluzione` | 6 |
| `promessa_generica` | 5 |
| `storia_immagine` | 4 |
| `vuota` (nome, saluto, slogan astratto) | 0 |

Se la frase non è visibile, l'hook vale 0.

#### Niente cliché (15)
Sul testo del hero.

- `C` = voci trovate in `cliche.json` (italiano e inglese, compresi saluti e frasi autoreferenziali).
- `K` = elementi concreti citati alla lettera (numeri significativi, nomi propri diversi dal nome dell'hotel e dalla sola città, persone, materiali, orari, luoghi precisi).

```
punti = 15 × limita(0.25 + 0.25·K − 0.25·C, 0, 1)
```

Senza testo nel hero: 0. Nessun cliché e nessun elemento concreto: 3,75. Servono elementi concreti per salire.

#### Riprova sociale (15)
Solo elementi visibili nella prima schermata.

| Trovato | Punti |
|---|---|
| Voto con la fonte (`9,2 su Booking`, `4,8 ★ Google`) oppure numero di recensioni | 15 |
| Riconoscimento con nome (Travellers' Choice, Michelin, guida citata) senza numero | 9 |
| Frasi generiche ("ospiti soddisfatti") oppure nulla | 0 |

Segnali: `\d[,.]\d\s*(\/\s*(10|5)|su 10|su 5|★)`, `\d+\s+recensioni`; `alt`/`src` delle immagini con `tripadvisor|booking|google|holidaycheck|michelin`.

#### Focus sull'azione (10)
Pulsanti principali nella prima schermata (esclusi menu e popup). Il modulo date del booking engine conta come un pulsante.

| Pulsanti principali | Punti |
|---|---|
| 1 | 6 |
| 2 | 3 |
| 0 oppure 3 o più | 0 |

| Testo del pulsante principale | Punti |
|---|---|
| Dice cosa succede dopo (`prezzi`, `disponibilità`, `date`, `preventivo`, `tariffa`) oppure modulo date | 4 |
| Generico (`prenota`, `book now`, `scopri`, `invia`) | 1 |

### Penalità (sottrazioni)
- **Scarsità finta** (−5): `solo \d+ camer`, `ultim[ae] \d+`, `offerta scade`, `affrettati`, conto alla rovescia. Niente penalità se il dato viene dal booking engine vero.
- **Informazioni scadute** (−5): date già passate nella prima schermata ("aperti fino al 2 novembre 2025" letto nel 2026), offerte scadute.

Voto finale = posizionamento + esecuzione + penalità, limitato tra 0 e 100, arrotondato.

## Segnalazioni fuori voto

- **Nessuna frase nella prima schermata**: se `frase visibile` è falso, è il primo problema del report.
- **Parole nel posto sbagliato**: se meta description, title o `h1` sotto la piega contengono almeno 2 elementi concreti assenti dal hero. Frase: *«Hai già le parole giuste. Sono nel posto sbagliato.»* con le citazioni.
- **Distanza da ciò che vuoi dire**: se l'albergatore ha risposto alla domanda del modulo, una frase: *«Vuoi che capiscano: [X]. La tua homepage dice: [Y].»*

## Fasce e verdetto

| Voto | Verdetto |
|---|---|
| 0–39 | Scritta come tutti gli altri |
| 40–69 | Quasi: il motivo c'è, ma è affogato |
| 70–84 | Ha un motivo, va affilato |
| 85–100 | Smontata: lavora già |

## Cosa vede l'albergatore

**Subito, senza email:**
- voto e verdetto
- la frase di posizionamento con le caselle vuote in evidenza
- il testo del hero con cliché in rosso ed elementi concreti in verde
- le segnalazioni fuori voto

**Nello Smontaggio a mano (6 al mese):**
- il dettaglio di ogni parametro
- confronto con 3 concorrenti reali
- temi delle recensioni contro la promessa del hero
- la verità cruda, 3 headline + 1 sottotitolo, il ragionamento
- voto rivisto, se il giudizio umano lo cambia

## Regole di onestà (non negoziabili)
- Barra di avanzamento vera, legata ai passaggi reali. Niente attese finte.
- Nessun numero fisso di problemi: si mostra quello che c'è.
- Ogni frase citata nel report deve comparire alla lettera sulla pagina. Le citazioni dell'AI che non si trovano nel testo vengono scartate.
- Sito illeggibile: si dice, non si inventa un voto.
