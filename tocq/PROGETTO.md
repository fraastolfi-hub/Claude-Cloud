# Tocq Hotel Milano · progetto della bozza del nuovo sito

Fonte: *Analisi di posizionamento, Hotel Positioning OS v7*, ottobre 2026 (3.297 recensioni contate, 1.805 lette per intero, report OTB 2026, sei concorrenti).
Questo documento traduce l'analisi in un progetto di sito: concept, obiettivi, alberatura, contenuti pagina per pagina, funzioni, tono, misure, fasi e domande aperte.
La bozza navigabile è in `bozza/` (si apre `bozza/index.html` nel browser, senza build).
La bozza applica il Brand Book Tocq v1.0 (2018): le regole sono in `BRAND.md`.
I dati dell'hotel vengono dal factsheet 2025 e dalla presentazione MICE (rev. 2), cartella Drive del cliente.

---

## 1. Il punto di partenza, in sei numeri

| Dato | Valore | Cosa vuol dire per il sito |
|---|---|---|
| Notti vendute da sito e app nel 2026 | **434, l'1,4%** | Il sito parte quasi da zero: ogni prenotazione spostata da Booking o Expedia è ricavo in più. |
| Prenotazioni dal sito a tariffa standard | **−64% sul 2025** | Il "Prenota diretto. Costa sempre meno" non funziona: serve un motivo, non uno sconto. |
| Quota MICE sul ricavo camere | **37%**, prezzo medio 310 € | Il MICE non va in fondo al menu: è metà del motivo per cui il sito esiste. |
| Ricavo da clientela business (MICE, corporate, consortia) | **47%** | Il sito parla a chi è a Milano per fare qualcosa. |
| Notti corporate individuali | **−20%** | Il viaggiatore d'affari che prenota da solo è il cliente che si sta perdendo, e quello che vota meglio (4,60 contro 4,35). |
| Occupazione di agosto | **40%** | Il leisure serve a riempire i vuoti (agosto, weekend), non a definire l'identità. |

Il sito di oggi racconta un'altra fase: "rifugio urbano", "Milano Centro" nei titoli, offerte "Stanchi di stare tra le 4 solite mura domestiche?", il PDF "Tocq Safe COVID-19 2021", ultimo articolo del blog ad aprile 2021.

## 2. Il concept

> **Scendi a Garibaldi. Sei arrivato.**
> Il sito della base di chi è a Milano per fare qualcosa: lavorare, riunirsi, partire, andare a un evento.

- **Le tre parole (filtro interno):** Base a Garibaldi. Ogni contenuto passa da qui. "Milano romantica con giro in centro"? No. L'orario del Malpensa Express? Sì.
- **La categoria:** non "hotel 4 stelle Milano centro", ma *la base per chi è a Milano per fare qualcosa*.
- **Il motivo per prenotare diretto:** *Su Booking prenoti una camera. Qui scegli il cuscino, il materasso e il lato da cui dormi.* Accesso e scelta, non sconto.
- **La combinazione che solo il Tocq ha:** camera nuova e grande, a piedi dal treno, sei sale nello stesso edificio delle camere, una squadra di colazione che ti chiama per nome.

> **Correzione rispetto all'analisi.** L'analisi parla di "sei sale fino a 200 persone" e di "circa 350 metri" dalla stazione. I materiali dell'hotel dicono altro: la sala più grande (Duomo) ospita **100 persone a platea** (260 posti a platea in tutto, sulle sei sale) e la stazione di Porta Garibaldi è a **200 metri**. La bozza usa i dati dell'hotel. Da verificare con la direzione se esiste una configurazione da 200 (sale unite, terrazza, Veranda).

## 3. I tre compiti del sito, in quest'ordine

1. **Generare richieste MICE e gruppi.** KPI: richieste di preventivo, download della presentazione.
2. **Riportare sul diretto il viaggiatore d'affari individuale.** KPI: prenotazioni dirette online, richieste di tariffa aziendale.
3. **Riempire i vuoti** (agosto, fine settimana) con offerte legate agli eventi della città. KPI: prenotazioni delle offerte.

Due percorsi con lo stesso peso fin dalla home: **Soggiorna** e **Meeting ed eventi**. Il messaggio della home è comune ai due: la posizione a Garibaldi e una squadra che risolve.

## 4. Chi parla il sito, e a chi non parla

**Best-fit (le pagine sono costruite per loro):**
- chi lavora in Porta Nuova e torna ("I travel every month to Milan for business");
- chi parte all'alba (treno, volo, Malpensa Express);
- chi viene per un evento raggiungibile da Garibaldi: F1 a Monza, San Siro, concerti, Fiera, Design Week;
- chi organizza una riunione e deve far dormire le persone.

**Bad-fit (niente pagine, foto o pacchetti pensati per loro):** il turista che vuole uscire in Piazza Duomo, chi cerca il lusso di design, chi vuole la movida e il silenzio insieme senza chiedere il lato corte, chi sceglie solo per prezzo all'ultimo minuto. Non si mandano via: il weekend delle coppie resta come *resa*, con il lato corte garantito.

## 5. Tono di voce: il Custode, con un accento milanese

Gli ospiti premiano chi toglie attriti e puniscono chi li lascia soli con un problema. L'accento milanese è nel ritmo: **orari, metri, nomi. Niente atmosfere.**

| Regola | Esempio |
|---|---|
| Il dato prima dell'aggettivo | "350 metri dal binario", non "posizione strategica" |
| Un nome prima di una categoria | "La colazione te la prepara Rosetta", non "il nostro staff attento" |
| Dire prima quello che si scoprirebbe dopo | "Il Duomo è a 25 minuti a piedi. Lo diciamo prima." |
| Il green si dice solo con un dono accanto | "Ti diamo la caraffa", non "ti togliamo la bottiglia" |

**Parole bandite** (da controllare in ogni testo prima della pubblicazione):

| Categoria | Parole | Perché |
|---|---|---|
| Solo vostre | rifugio urbano, movida, Milano centro, nel vivo di | Richiamano i due temi più delicati: il rumore e la distanza dal Duomo |
| Lontane dal carattere | raffinato, esclusivo, lusso, trend | Il Custode non impressiona: risolve |
| Le dicono tutti | esperienza, il posto giusto, mettiti comodo, scopri di più | Passano il test del logo di chiunque |
| Fuori tempo | mura domestiche, prigioniero, libertà, safe | Lessico 2020–2021 |
| Solo con un gesto accanto | green, eco, sostenibile | Oggi accompagnano una sottrazione |

Anche le etichette dei bottoni seguono la regola: "Vedi le camere", "Calcola il tragitto", "Scarica la scheda sale", mai "Scopri di più".

## 6. L'alberatura

Fase 1 in **grassetto** (presente nella bozza), fase 2 in corsivo.

```
HOME · "Base a Garibaldi"
├── Soggiorna
│   ├── **Camere e suite** · con la scelta di cuscino, materasso e lato della camera
│   ├── **Colazione** · orari, da asporto per chi parte presto, aperta agli esterni
│   ├── Bar e ristorante
│   └── **Prenota** · booking engine con i vantaggi del canale diretto
├── Meeting ed eventi
│   ├── **Le sale** · una scheda per sala: capienze per allestimento, planimetria, dotazioni, foto
│   ├── **Formule** · mezza giornata, giornata intera, residenziale con camere
│   ├── **Gruppi e blocchi camere**
│   ├── *Eventi ospitati* · casi reali e referenze
│   ├── **Richiedi un preventivo**
│   └── **Scarica presentazione e fact sheet**
├── *Business travel*
│   ├── *Tariffe aziendali e convenzioni* · richiesta accordo corporate
│   └── *Servizi per chi lavora* · wifi, spazi, fattura unica, early check-in, late check-out
├── La posizione
│   ├── **Come arrivare** · stazione di Porta Garibaldi, metro, aeroporti
│   ├── **Porta Nuova e le aziende vicine**
│   ├── *Fiere, congressi, stadio ed eventi* · una pagina per destinazione
│   └── **Mappa**
├── *Offerte* · legate agli eventi della città e ai fine settimana
├── *Il Tocq* · la squadra, la storia del progetto, la sostenibilità che dà
└── **Contatti**
```

URL proposti (fase 1): `/`, `/camere/`, `/meeting/`, `/posizione/`, `/contatti/`; inglese sotto `/en/` con gli stessi slug tradotti.
URL fase 2 (dai CEP, pensati per Google e per gli assistenti AI): `/hotel-fiera-milano-rho/`, `/hotel-san-siro/`, `/hotel-gran-premio-monza/`, `/hotel-mico-congressi/`, `/hotel-malpensa-express/`, `/business-travel/`.

## 7. Le pagine della fase 1, sezione per sezione

### 7.1 Home · `bozza/index.html`

| # | Sezione | Contenuto | Fonte nell'analisi |
|---|---|---|---|
| 1 | Hero | "Scendi a Garibaldi. Sei arrivato." + le quattro promesse (treno, sala, cuscino, colazione all'alba). Due bottoni di pari peso: *Prenota una camera* / *Organizza un evento* | Cap. 8, 13.1 |
| 2 | Tabellone | Distanze in stile orario ferroviario: binario, metro, Malpensa Express, Porta Nuova, Fiera, San Siro, Monza | Cap. 13.4 |
| 3 | Due percorsi | Soggiorna / Meeting ed eventi, stessa larghezza | Cap. 13.1 |
| 4 | Il motivo diretto | "Su Booking prenoti una camera. Qui scegli il cuscino, il materasso e il lato da cui dormi." Quattro vantaggi | Cap. 10, 13.5 |
| 5 | Una giornata dal Tocq | La mappa del lavoro dell'ospite in 5 momenti con orari (arrivo, sera, notte, alba, ritorno) | Cap. 6 (JTBD) |
| 6 | La squadra | Nomi e citazioni vere dalle recensioni | Cap. 3.6 |
| 7 | Sale sotto le camere | Teaser MICE: 6 sale fino a 200 persone, preventivo in 24 ore, scheda scaricabile | Cap. 4, 13.3 |
| 8 | Le recensioni | Expedia 8,8 su 973 + citazioni scelte fra quelle di chi lavora (non "movida") | Cap. 13.5 |
| 9 | Il Duomo, detto prima | Riga onesta sulla distanza dal centro storico | Cap. 3.1, 13.4 |

### 7.2 Camere · `bozza/camere.html`
- Le tipologie (nomi e metrature da confermare).
- **Il configuratore della notte**: cuscino (Neckroll, Kapok, lattice, piuma d'oca), materasso, lato della camera (corte / via Tocqueville), colazione in sala o da asporto con l'orario di partenza, richiesta di check-in anticipato. Nella bozza è una demo; in produzione i campi passano al booking engine come richieste speciali o, meglio, come pacchetti/servizi del motore.
- **Colazione**: orari, da asporto, aperta agli esterni a 16 €.
- **Le regole della casa, dette prima**: il clima (regola unica, una frase sola, da decidere con la direzione), il lato corte, il deposito bagagli sempre, la fattura unica.
- La dotazione che dà: caraffa d'acqua filtrata, bicchieri veri, due cialde, listino minibar in vista, borraccia Tocq (tutto da confermare: è la Mossa 3).

### 7.3 Meeting ed eventi · `bozza/meeting.html`
- Hero "Dormi dove ti riunisci."
- Le sei sale in tabella: capienze per platea, banchi di scuola, ferro di cavallo, banchetto; mq; luce naturale. **Tutti i numeri sono segnaposto.**
- Formule: mezza giornata, giornata intera, residenziale.
- Gruppi e blocchi camere.
- **Preventivo rapido** (date, persone, allestimento, camere, servizi) con il tempo di risposta dichiarato.
- **Download** presentazione e fact sheet in cambio di nome, azienda, email.
- Ogni richiesta e download entra nel CRM con la fonte (campo nascosto `fonte` già nel form).

### 7.4 La posizione · `bozza/posizione.html`
- "A Milano sei già dove devi essere."
- Tabella delle destinazioni filtrabile per motivo: *lavorare*, *partire*, *eventi*, *tempo libero*.
- Mappa (segnaposto: in produzione Google Maps o Mapbox con i punti della tabella).
- Il centro storico detto con onestà: tempi reali, senza promettere il "centro".

### 7.5 Contatti · `bozza/contatti.html`
- Indirizzo, telefono, email, reception h24.
- Tre richieste distinte, perché vanno a persone diverse: soggiorno, evento/gruppo, tariffa aziendale.
- Come arrivare in tre righe.

## 8. Funzioni

| Funzione | Fase | Note tecniche |
|---|---|---|
| Booking engine con personalizzazione | 1 | Verificare con il fornitore attuale se cuscino, lato e colazione da asporto possono essere *servizi* selezionabili, non solo note libere |
| Preventivo MICE | 1 | Form breve, risposta dichiarata, ingresso nel CRM con fonte |
| Download presentazione | 1 | Gate leggero (nome, azienda, email), PDF da produrre |
| Richiesta tariffa aziendale | 1 (form contatti) → 2 (pagina dedicata) | |
| Recensioni in vista | 1 | Widget o numeri aggiornati a mano ogni trimestre |
| Richiesta recensione automatica post soggiorno | 1 (CRM, fuori dal sito) | Entro 24 ore dal check-out, verso Google e TripAdvisor (Mossa 5) |
| Pagine destinazione (CEP) | 2 | Una per destinazione, con tempi verificati |
| Lingue | IT + EN al lancio; DE, FR, ES in fase 2 | Le lingue più presenti nelle recensioni |
| Tour virtuale delle sale | 2 | |
| Dati strutturati | 1 | `Hotel`, `MeetingRoom`, `FAQPage` in JSON-LD (già nella home della bozza, da completare) |

## 9. Misurare dal primo giorno

Tre eventi tracciati (GA4 o equivalente), tutti con la fonte di provenienza:
1. `prenotazione_diretta` (conversione dal booking engine, con ricavo);
2. `richiesta_preventivo_mice`;
3. `download_presentazione`.
Più due secondari: `richiesta_tariffa_aziendale`, `uso_configuratore`.
Base di partenza: 434 notti da sito e app nel 2026. Gli obiettivi si fissano con il revenue.

## 9 bis. SEO e GEO: cosa c'è già nella bozza

**Una sola fonte dei fatti.** `build.py` contiene indirizzo, telefono, numeri di camere e sale e distanze una volta sola, e li scrive in pagine, dati strutturati e `llms.txt`. Google e gli assistenti AI (ChatGPT, Perplexity, Gemini, Claude) premiano i dati coerenti e ripetuti in modo identico.

| Elemento | Dove |
|---|---|
| Title ≤ 60 caratteri e description ≤ 155, uno per pagina, costruiti sulle ricerche dei CEP ("hotel vicino stazione Garibaldi", "sale meeting Porta Nuova") | head di ogni pagina |
| URL definitivi, canonical, hreflang it/en/x-default | `/`, `/camere/`, `/meeting-eventi/`, `/posizione/`, `/contatti/` |
| Open Graph e Twitter card, immagine 1200×630 | `assets/img/foto/tocq-hotel-milano-og.jpg` |
| Dati strutturati JSON-LD in un unico grafo: Hotel (geo, stelle, 133 camere, servizi, animali ammessi), WebPage, BreadcrumbList, FAQPage, 4 HotelRoom, 6 MeetingRoom con m² e capienza | head di ogni pagina |
| Blocco "In breve": i fatti in forma di elenco, la forma che gli assistenti AI citano più volentieri | home, camere, meeting, posizione |
| FAQ visibili scritte come le domande vere (29 in tutto), riprese uguali in FAQPage | fondo di ogni pagina |
| Tabelle HTML per distanze, sale e confronti | posizione, meeting, home |
| Un solo H1 per pagina, gerarchia dei titoli corretta, salto al contenuto, testi alternativi descrittivi su tutte le immagini | tutte |
| Immagini WebP a 800 e 1600 px con srcset, dimensioni dichiarate, caricamento differito, nomi file descrittivi | `assets/img/foto/` |
| `sitemap.xml` con hreflang, `robots.txt` che ammette i crawler AI, `llms.txt` con la scheda dell'hotel | `bozza/` |
| Data di aggiornamento visibile e in `dateModified` | footer e dati strutturati |

**Al lancio:** togliere `noindex` dall'head (è in `build.py`); verificare le coordinate su Google Maps; aggiornare la scheda Google Business Profile con le stesse identiche parole (nome, indirizzo, telefono, categoria "Hotel", servizi, foto); pubblicare la versione inglese con gli stessi dati; validare i dati strutturati con il Rich Results Test di Google.

**Nota sulle valutazioni:** i voti di Expedia, Booking e Google compaiono nel testo con la fonte, ma non come `aggregateRating` nei dati strutturati: Google non accetta recensioni di terzi segnate dall'hotel stesso.

## 9 ter. Elementi persuasivi

Tutti costruiti su fatti veri; dove il fatto dipende da una decisione della direzione, è segnato "da confermare".

- **Prova sociale accanto ai bottoni:** 8,8/10 su Expedia (973 recensioni), 4,60/5 dei viaggiatori d'affari su Google, 8,98 su pulizia e comfort.
- **Confronto "agenzia online / tocq.it":** il motivo per prenotare diretto in sei righe (camera, cuscino, colazione all'alba, arrivo, prezzo, chi risponde).
- **Confronto per chi organizza:** centro congressi, hotel di catena in stazione, Tocq.
- **Processo MICE in 4 passi**, con una persona sola dalla richiesta al check-out: abbassa l'attrito di chi deve chiedere un preventivo.
- **Impegno piccolo prima di quello grande:** il configuratore della notte prima delle date.
- **Onestà che crea fiducia:** "Detto prima" (il Duomo a 2,5 km, le regole della casa).
- **Citazioni vere vicino alle decisioni:** "C'era il menù cuscini, quindi colpa mia a non averli richiesti" accanto al form di prenotazione.
- **Barra fissa su mobile** con Prenota e Preventivo evento.
- Niente scarsità finta, niente conti alla rovescia: non sono nel carattere del Custode e danneggiano la fiducia.

## 9 quater. Foto

Inserite 15 foto dalla cartella Drive del cliente: 9 camere (shooting 2021), 4 piatti, 2 del quartiere. Mancano:
- **sale meeting, hall, bar, colazione a buffet, squadra, esterno:** le foto ci sono nel Drive ("Tocq Hotel Photos & Videos", serie TEAM, HALL, BREAKFAST, BAR, e le cartelle delle sale), ma il connettore Drive non scarica file sopra i 6 MB circa. Servono copie esportate più piccole (lato lungo 2500 px) o un download manuale;
- **licenza** delle foto del quartiere (Porta Nuova, Bosco Verticale): sembrano foto stock, da verificare;
- **abbinamento** fra la serie 2021 (Cozy, Stylish, Roomy, Snuggle) e le tipologie attuali (Comfort, Superior, Executive, Junior Suite).

## 10. Prima del sito: rendere vero, prima di dirlo

Il sito promette la notte. Le cinque mosse del capitolo 10 vanno avviate prima o insieme al lancio, altrimenti il sito accelera le recensioni negative:

1. **La camera si assegna, non capita** (lato corte o piani alti a chi chiede silenzio, gio–dom, e ott–apr quando il clima è fermo).
2. **Una regola dell'aria, una spiegazione sola** (e togliere "aria condizionata" dalle schede nei mesi in cui non c'è).
3. **Il green che dà** (caraffa, bicchieri, due cialde, listino minibar, borraccia).
4. **La regola del banco** (valigie sempre accettate, parcheggio scritto, camera declassata = differenza restituita).
5. **Riattivare la voce degli ospiti soddisfatti** nel nuovo CRM.

Nella bozza queste mosse compaiono già come promesse: sono segnate *da confermare* finché la direzione non le adotta.

## 11. Interventi rapidi sul sito attuale (prima del nuovo)

- Archiviare il PDF "Tocq Safe COVID-19 2021".
- Ritirare le offerte "mura domestiche" e "prigioniero a casa".
- Sostituire "Milano Centro" nei titoli con Porta Garibaldi e Porta Nuova.
- Cambiare "Prenota diretto. Costa sempre meno" con il motivo della scelta (cuscino, materasso, lato).

## 12. Fasi e calendario indicativo

| Fase | Contenuti | Durata indicativa |
|---|---|---|
| 0 · Raccolta | Risposte alle domande aperte (§13), brand book, foto, piantine sale, accesso al booking engine | 2 settimane |
| 1 · Bozza approvata | Questa bozza, rivista con la direzione: testi, struttura, segnaposto chiusi | 1–2 settimane |
| 2 · Design | Brand book già applicato alla bozza (`BRAND.md`); restano licenza Futura web, lettering, scelta delle foto dall'archivio e shooting mirato (lista foto nei segnaposto) | 2–3 settimane |
| 3 · Sviluppo fase 1 | Home, camere + booking, meeting + preventivo + download, posizione, contatti. IT + EN | 4 settimane |
| 4 · Lancio e misura | Tracciamento, CRM, richiesta recensioni | 1 settimana |
| 5 · Fase 2 | Pagine destinazione, business travel, eventi ospitati, altre lingue, tour sale | nei mesi successivi |

Momento consigliato per il lancio: prima della stagione fiere di gennaio–febbraio 2027, così la fase 2 (pagine Fiera, Salone del Mobile ad aprile) arriva in tempo per la primavera.

## 13. Domande aperte per la direzione

Ogni segnaposto tratteggiato nella bozza rimanda a una di queste.

**Già chiuse dai materiali dell'hotel** (factsheet 2025, presentazione MICE rev. 2):
- camere: 133, di cui 14 Comfort, 63 Superior, 35 Executive, 21 Junior Suite;
- sale: Duomo, Scala, Brera, Porta Nuova, Castello, Arena, con capienze per allestimento, misure e m² (in `bozza/meeting.html`);
- distanze: stazione Garibaldi 200 m, Gae Aulenti 70 m, Corso Como 50 m, Bosco Verticale 100 m, Centrale 1,5 km, Duomo 2,5 km, Linate 9 km, Malpensa 49 km;
- contatti: +39 02 62071, info@tocq.it, mice@tocq.it; società: Fattore Italia srl, P.IVA 08581970962;
- colazione: buffet italiano e internazionale con selezione orientale, halal, senza glutine e vegana.

**Incoerenze fra i materiali dell'hotel e il posizionamento** (da decidere con la direzione):
- factsheet e presentazione MICE usano proprio il lessico da abbandonare: "urban retreat", "in the heart of Corso Como", "trendiest district", "refined", "experience". Vanno riscritti insieme al sito;
- il factsheet elenca l'aria condizionata fra le dotazioni senza limiti: è il tema di 23 recensioni Booking (mossa 2);
- il factsheet cita ristorante Clorofilla, Veranda, terrazza, Smart Working Suite, Virgin Active vicino, hotel pet-friendly: da decidere cosa entra nel sito e dove (Smart Working Suite e terrazza servono al percorso business e MICE).

**Ancora aperte:**

1. **Tempi e linee:** linee metro da Garibaldi (M2, M5); tempi per Malpensa, Linate, Rho Fiera, MiCo, San Siro, Monza, Duomo in metro.
2. **Le sei sale:** planimetrie e foto per sala; luce naturale; se esiste una configurazione oltre i 100 posti. Valutare il nome "Duomo" per la sala principale, che contraddice il "non vendiamo il Duomo".
3. **Tempo di risposta ai preventivi** che il commerciale può garantire (la bozza dice 24 ore lavorative).
4. **Tipologie di camera:** metrature e letti; quante danno sulla corte e quante su Via Tocqueville; quali sono sotto i motori del tetto; cosa sono le Smart Working Suite.
5. **Menu cuscini e materassi:** opzioni attuali, e se il booking engine può raccoglierle come servizi.
6. **Colazione:** orari in settimana e nel weekend, orario minimo per quella da asporto, prezzo per esterni (16 € è il dato dalle recensioni).
7. **La squadra:** chi c'è oggi, e chi è d'accordo a comparire per nome sul sito (Rosetta, Maria, Marco, Giorgio, Oliver, Andrea).
8. **Il clima:** la regola dell'aria (impianto o Green Key?) e la frase unica da usare.
9. **Borraccia Tocq:** è mai stata prodotta?
10. **Eventi ospitati citabili** (convegni, aziende, Giochi 2026) e relative autorizzazioni.
11. **Nome e orari del commerciale MICE**; email per gli accordi aziendali.
12. **Booking engine e CRM in uso**, per collegare form e tracciamento.
13. **Brand:** file del lettering proprietario (font o tracciati vettoriali); licenza web di Futura Std; marchio in positivo in formato vettoriale originale (in cartella c'è solo il negativo); pittogrammi in vettoriale. Dettagli in `BRAND.md`.
14. **Foto:** quali scatti dell'archivio (cartelle "Tocq Hotel Photos & Videos", "Foto Sale Costantino", "Per Mission") sono approvati per il web.

## 14. Spunti presi da hoteltocqmilano.it (pagina "Concerti San Siro Estate 2026")

- **Motore di prenotazione:** Blastness, `id_albergo=16496`, `dc=6326`. Il form "Verifica le date" della bozza apre già le disponibilità reali con le date scelte. Da verificare con Blastness il parametro per il codice aziendale e come passare le scelte del configuratore.
- **Promesse già pubbliche, quindi non più "da confermare" nella bozza:** tariffa diretta migliore garantita, cancellazione gratuita, custodia bagagli prima del check-in e dopo il check-out.
- **Dati:** M5 lilla a 2 minuti a piedi, San Siro in 15 minuti senza cambi. La pagina riporta su Booking 8,7/10 con oltre 3.200 recensioni e posizione 9,1 (aprile 2026); l'analisi di ottobre misura 8,5 e 8,96. Nella bozza restano i numeri dell'analisi, più recenti: da allineare al lancio.
- **Foto:** hall con poltrone in velluto verde (copre il vuoto "hall"), cuscini sistemati sul letto, Corso Como, Corso Garibaldi, skyline di Porta Nuova al tramonto. Le prime due sono dell'hotel; le altre del quartiere, da verificare la licenza come per le altre foto di città.
- **Struttura:** le tre schede del quartiere con i minuti a piedi (Corso Como 1, Corso Garibaldi 4, Porta Nuova 6) sono entrate nel capitolo "La sera". Il tono "movida" della pagina concerti resta fuori: nella bozza la sera si vive, la notte è sul lato corte.
