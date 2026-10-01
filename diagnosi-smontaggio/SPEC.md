# Diagnosi immediata · Smontaggio

Primo step automatico dello Smontaggio di hotelpositioning.com.
L'albergatore inserisce l'URL e riceve subito un voto 0-100 su quello che un ospite vede nei primi 3 secondi: la prima schermata della homepage.

La domanda a cui risponde: **in quella schermata c'è un posizionamento, e viene eseguito bene?**

## Dove vive

- **Diagnosi automatica:** `hotelpositioning.com/diagnosi`. L'albergatore inserisce l'URL e vede subito voto, frase di posizionamento e segnalazioni.
- **Smontaggio a mano:** resta su `hotelpositioning.com/smontaggio`. La diagnosi ci porta con un pulsante, passando URL e nome dell'hotel per non farli riscrivere.

## Cosa fa la macchina, cosa fa Francesco

| | Diagnosi automatica | Smontaggio a mano |
|---|---|---|
| Voto 0-100 | Sì | Confermato o corretto |
| Concorrenti reali | No (solo stima della sostituibilità) | Sì: headline di 3 hotel vicini a confronto |
| Recensioni | No | Sì: i 5 temi più lodati confrontati con il hero |
| Riscrittura | No | 3 headline + 1 sottotitolo + ragionamento |

## Estrazione della prima schermata

Implementata in `motore/estrai.js`.

1. Rendering con browser headless (Playwright), lingua `it-IT`, due viewport: desktop 1366×768 e mobile 390×844. Per le regole di esecuzione vale la versione peggiore delle due.
2. Prima della lettura si nascondono i banner cookie (li chiude ogni visitatore). Popup, newsletter e finestre modali restano: se coprono la headline, la frase non è visibile.
3. **Si escludono** dal testo del hero: menu e navigazione, moduli, pulsanti, footer, popup, elementi fissi sullo schermo (barre, chat, notifiche, pannelli laterali), testi dentro link salvo i titoli di slide cliccabili, righe fatte solo di pulsanti.
4. **Testo del hero** = tutto il testo rimasto con `top < altezza viewport`:
   - **headline**: l'`h1` visibile; se non c'è, il blocco di 3-20 parole con il font più grande;
   - **sottotitolo**: il primo blocco di almeno 3 parole sotto la headline;
   - **supporto**: gli altri testi visibili.
5. **Frase visibile**: vero se esiste una headline nella prima schermata e il suo centro non è coperto da un popup (`elementFromPoint`).
6. **Pulsanti principali**: sfondo pieno sull'elemento o sul primo figlio. Non contano: pulsanti con solo il bordo, link testuali, link grandi quanto una slide, link di pochi pixel (accessibilità), telefono ed email, il pulsante accanto al campo date (fa parte del modulo di prenotazione).
7. **Riprova sociale**: si scorre tutta la pagina e si registrano voti e riconoscimenti con la posizione in schermate. Il voto spezzato in più elementi si ricompone leggendo fino a tre contenitori sopra. Loghi delle piattaforme sì, icone del sito no, testi di reCAPTCHA e privacy no.
8. **Fuori dal hero** (non entrano nel voto, servono alla segnalazione "parole nel posto sbagliato"): title, meta description, `h1` fuori dalla prima schermata, testi della seconda schermata.
9. Sito illeggibile (blocco bot, testo solo dentro immagini): si chiede all'albergatore di incollare headline e sottotitolo. Nessun voto inventato.

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
Si cerca in tutta la pagina e si guarda **quanto è vicina al hero**. Una barra di rating subito sotto la prima schermata lavora quasi quanto una dentro.

Punti = valore del tipo × fattore di posizione (si tiene l'elemento migliore).

| Tipo | Valore |
|---|---|
| Voto con la fonte (`8,5 Booking`, `4,5 ★ Google`) oppure numero di recensioni | 15 |
| Riconoscimento con nome (Travellers' Choice, Michelin, guida citata) oppure recensione citata con nome e fonte | 9 |
| Frasi generiche ("ospiti soddisfatti", "i più amati") | 0 |

| Posizione (in schermate dall'inizio della pagina, vale la versione peggiore tra desktop e mobile) | Fattore |
|---|---|
| Nella prima schermata (< 1) | 1 |
| Subito sotto (fino a 1,5) | 0,8 |
| Più in basso nella pagina | 0,33 |

Segnali: `\d[,.]\d\s*(\/\s*(10|5)|su 10|su 5|★)`, `\d+\s+(recensioni|reviews)`, `superb|eccellente|travellers.? choice`; `alt`/`src` delle immagini con `tripadvisor|booking|google|holidaycheck|michelin`.

#### Focus sull'azione (10)
Pulsanti principali nella prima schermata (esclusi menu e popup). Il modulo date del booking engine conta come un pulsante. **I pulsanti secondari non contano**: sfondo trasparente con solo il bordo, oppure link testuali (sottolineati o senza sfondo). Stanno lì per chi non è pronto e non rubano attenzione all'azione principale.

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
- **Promessa da provare**: se il hero contiene un superlativo o un'esclusiva (`il più`, `l'unico`, `the only`, `the best`, `-est`, `migliore`) e accanto non c'è la fonte che lo dimostra. Frase: *«"[citazione]" è la promessa più forte della pagina. Chi la prova?»*
- **Parole nel posto sbagliato**: se meta description, title, `h1` sotto la piega o le prime 2 schermate contengono almeno 2 elementi concreti (o un riconoscimento) assenti dal hero. Frase: *«Hai già le parole giuste. Sono nel posto sbagliato.»* con le citazioni.
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
