# Hotel Positioning Library v4: metodologia

Francesco Astolfi · aggiornata al 1 ottobre 2026

La Library ha due funzioni:

1. **Ispirazione:** mostrare a un albergatore che "generico non esiste" e che esistono modi concreti di farsi scegliere.
2. **Strumento di lavoro:** classificare i casi del mondo in modo coerente, così da leggere dove si muove il mercato e dove l'Italia è indietro.

Le due funzioni chiedono la stessa cosa: **dati giusti e confrontabili**. Un esempio sbagliato rovina l'ispirazione, una classificazione incoerente rovina l'analisi dei trend.

---

## 1. I concetti

### Pattern
Un pattern è una **scelta strutturale** che cambia il conto economico: cosa fatturi e cosa no, chi servi e chi respingi, come funziona l'operatività. Non è un tema estetico, uno slogan o una tagline.

Test di inclusione: *se l'hotel smettesse di applicare il pattern, cambierebbero i ricavi o gli ospiti?* Se la risposta è no, è decorazione, non un pattern.

### Famiglia
Dodici famiglie (A–L) raggruppano i pattern per **meccanismo**: contro chi ti definisci (A), quale limite ti dai (B), per chi progetti (C), quale lavoro fai per l'ospite (D), con cosa ti ibridi (E), il luogo (F), la persona (G), l'operatività (H), il tempo (I), il genere che rifiuti (J), la visione (K), chi escludi (L).

C ed L sono speculari: C è *progettato per*, L è *riservato a*. Ogni pattern L ha il suo corrispettivo C nel campo `correlati`.

### Categoria emergente
Una categoria è un **mercato** (in che gioco giochi), non un meccanismo. Un hotel sta in una categoria e la attraversa con 2-3 pattern. Esempio: Lanserhof sta in *Wellness Medico* (categoria) usando *Anti-Wellness-Fuffa* + *Vendiamo la Trasformazione* (pattern).

### Fusion
I posizionamenti più forti combinano **2-4 pattern di famiglie diverse**. Il pattern singolo serve a spiegare; nella realtà quasi sempre i pattern sono combinati. Le fusion documentate sono nel blocco `fusion` del file dati.

---

## 2. Le scale di valutazione

Tre scale indipendenti. Non vanno mescolate.

| Scala | Valuta | Valori |
|---|---|---|
| **Tier** (sull'esempio) | Quanto il caso rappresenta il pattern | T1 archetipico · T2 solido ma parziale · T3 nascente |
| **Verifica** (sull'esempio) | Quanto sono provati i claim | verificato · da_verificare · proposto |
| **Maturità** (sul pattern) | Quanto il pattern è diffuso nel mondo | consolidato · emergente · nascente |

Più due attributi:

- **caveat** (sì/no): il posizionamento era forte ma il business non ha retto o l'identità è stata abbandonata. È un dato, non un tier. Selina è T1 *e* caveat.
- **proprietà**: indipendente · gruppo indipendente · major. Serve a non vendere a un indipendente un modello che regge solo con le spalle di Marriott o LVMH.

**Regola di pubblicazione:** sul sito vanno solo esempi `verificato`. Gli esempi `da_verificare` possono comparire con un'etichetta esplicita, i `proposto` mai.

**Regola di coerenza:** un pattern senza esempi pubblicabili deve essere `nascente`. Lo controlla lo script.

---

## 3. Il modello dati

Fonte unica: `library-v4.json`. Tutto il resto (sito, CSV, fogli di calcolo, presentazioni) si genera da qui.

```
famiglie[]        codice, nome, core, rischio
pattern[]         codice (A01), famiglia, nome, definizione, maturita, correlati[]
categorie[]       id (CAT01), nome, definizione, stadio, pattern_affini[]
esempi[]          id, nome, paese, area, luogo, proprieta, stato, tier, verifica,
                  caveat, pattern[], categorie[], sito, evidenza, fonti[], note
fusion[]          esempio, pattern[]
segnali_trend[]   data, tipo, esempio, categoria, fatto, lettura
```

Regole che impediscono il ripetersi degli errori della v2:

1. **Codici locali alla famiglia** (A01…A05, B01…B05). Nessun numero globale.
2. **Collegamenti solo per codice completo.** Vietati codici generici ("E", "K", "nascente").
3. **Un esempio sta su un pattern solo se l'`evidenza` lo dimostra.** Se l'evidenza non nomina il meccanismo, l'esempio non va su quel pattern.
4. **Ogni correzione passa da `tools/validate.py`**, che blocca riferimenti rotti e incoerenze ed esporta i CSV.

---

## 4. Protocollo di verifica

Un esempio diventa `verificato` quando:

1. ogni claim nell'`evidenza` (date, numeri, persone, primati) ha **almeno una fonte** in `fonti`: sito ufficiale per i fatti di prodotto, fonte terza per primati, numeri e vicende societarie;
2. lo `stato` è aggiornato (attivo, acquisito, venduto, chiuso), perché un brand acquisito o fallito cambia il significato del caso;
3. la `proprieta` è controllata.

Numeri economici (quote di fatturato, durata dei soggiorni, crescite di categoria) si pubblicano **solo con fonte citata**. Le stime interne vanno etichettate come tali: per esempio "delta dichiarato-vissuto 40-60%" è un'osservazione dal lavoro sui clienti, non un dato di mercato.

**Cadenza:** revisione completa ogni sei mesi. Controllo dello `stato` di tutti gli esempi ogni trimestre: acquisizioni e chiusure sono i segnali di trend più preziosi.

---

## 5. Usare la Library per leggere i trend

La v4 aggiunge i campi che servono all'analisi: `area`, `proprieta`, `stato`, `maturita`, `stadio` e il registro `segnali_trend`.

### Cinque letture da fare a ogni revisione

1. **Ciclo di vita delle categorie.** Quante categorie passano da nascente a emergente a matura? Uno spostamento è un segnale, e va registrato in `segnali_trend`.
2. **Assorbimento da parte delle major.** Quota di esempi passati da indipendente a major (citizenM → Marriott, The Hoxton → Ennismore/Accor, Six Senses → IHG, Kimpton → IHG). Se un pattern viene comprato, funziona, ma diventa più difficile da difendere per un indipendente.
3. **Caveat per categoria.** Dove i posizionamenti forti falliscono (Selina nel workation) c'è un rischio di modello di business, non di posizionamento.
4. **Mappa geografica.** Distribuzione per `area`: oggi la Library pesa molto su Europa e Nord America. Asia, America Latina e Medio Oriente vanno arricchite per poter parlare di trend *mondiali*.
5. **Gap Italia.** Per ogni categoria e pattern: c'è almeno un caso italiano? Le caselle vuote sono le opportunità di pionierato da proporre ai clienti (oggi: Sober Hospitality, Sleep Tourism, Stagione Invertita, Women Only).

### Il registro dei segnali
Ogni evento rilevante (acquisizione, chiusura, nuova apertura che crea una categoria, cambio di identità) va in `segnali_trend` con data, fatto verificato e una riga di **lettura**: cosa significa per un hotel indipendente italiano. È la parte della Library che diventa contenuto: newsletter, post, slide.

---

## 6. Il motore dell'hotel: il ponte con la guida

La guida "Come funziona davvero il positioning di un hotel" scompone il Posizionamento di Mercato in quattro componenti, ciascuna da 0 a 10: **Location**, **Capital**, **Operations**, **Narrativa**. La Library è il catalogo dei meccanismi della quarta componente, la narrativa. I due strumenti si usano in sequenza: prima la guida dice qual è il motore dell'hotel, poi la Library dice con quale pattern costruire la narrativa.

Nel file dati:

- ogni pattern ha `motore`, cioè i profili per cui è più adatto, e `gestione_minima`, cioè il voto minimo di Operations sotto cui la promessa non regge (per esempio "Una sola cena, un solo orario" richiede Operations ≥ 8);
- alcuni esempi hanno `motore`, una valutazione editoriale del motore principale dell'hotel (Eremito: narrativa; citizenM: operations; Casa Cipriani: location + narrativa).

Regola di lettura per un cliente: conta le componenti con voto ≥ 8. Se sono zero, la leva è la narrativa. Se è una, il profilo è puro e la narrativa deve amplificare quella componente. Se sono due o più, il profilo è misto e la narrativa racconta l'incrocio. Prima di tutto, Operations deve superare la `gestione_minima` del pattern scelto.

## 7. Diagnosi del cliente (invariata nella sostanza)

Quattro input:

1. **Struttura e vincoli:** edificio, camere, posizione, staff.
2. **Dichiarato:** cosa dice il proprietario (sito, brochure, pitch).
3. **Vissuto:** cosa dicono le recensioni, con temi presenti in almeno il 5% delle recensioni.
4. **Delta dichiarato-vissuto:** il motore della diagnosi.

Sei fasi:

| Fase | Azione | Output |
|---|---|---|
| 0 | Pre-diagnosi | I 4 input raccolti |
| 1 | Pattern candidati | 3-5 codici dalla Library, scelti partendo dal *vissuto* |
| 2 | Sostenibilità | Filtro per struttura, volontà del proprietario, mercato locale, saturazione |
| 3 | Fusion | Combinazione di 2-3 pattern di famiglie diverse |
| 4 | Ancoraggio | 1-2 casi della Library, preferibilmente italiani e indipendenti |
| 5 | Caveat | Il caso che mostra il rischio di modello di business (Selina) |
| 6 | Roadmap | 3-5 scelte operative concrete |

---

## 8. Principi strategici (rivisti)

- **P1. Identità chiara = brand separato.** Sandals (coppie, solo adulti) non ha annacquato il brand per le famiglie: ha creato Beaches. Nota: Beaches è *pensato* per le famiglie, non *riservato* a loro.
- **P2. Rifondare la categoria con un vocabolario tecnico.** Vivamayr e Lanserhof non si chiamano spa: sono resort medici con protocolli e diagnostica.
- **P3. Il luogo italiano come leva.** Sextantio ed Egnazia hanno costruito identità rifiutando il format dominante nel loro territorio.
- **P4. I numeri rendono il posizionamento credibile, ma solo con fonte.** I dati Six Senses sono sospesi finché non si trova la fonte.
- **P5. Il brand forte si estende al residenziale** (Aman Residences, Casa Cipriani Miami). Il dato "+150% in 10 anni" va ricollegato alla sua fonte prima di usarlo.
- **P6 (nuovo). Il pattern anti-catena si compra.** citizenM e The Hoxton sono finiti in Marriott e Accor, Postcard Cabins in Marriott. Per un indipendente, la difesa duratura è legare il pattern a ciò che una major non può comprare: persona (G), luogo (F), visione (K).
- **P7 (nuovo). Le catene industrializzano la sottrazione.** Scandic GO, Bob W e MM:NT tolgono reception, ristorante e personale in loco. Un indipendente non può vincere sul prezzo togliendo servizi: la sottrazione funziona per lui solo se toglie ciò che il suo target non vuole (AVIVA toglie le coppie, Eremito toglie il wifi).
- **P8 (nuovo). Il "club layer".** The Ned, Hotel Bardo e Casa Cipriani aprono ristoranti e spazi al pubblico e vendono, sopra, un livello riservato ai soci. È una forma di Members Only adatta anche a un hotel cittadino di medie dimensioni.
- **P9 (nuovo). L'hotel come piazza.** YellowSquare, Oderberger e The Ned fatturano anche sui residenti: il bar, la piscina, i concerti. L'ospite trova un quartiere vivo e l'hotel ha un ricavo che non dipende dall'occupazione.

---

## 9. Roadmap della Library

1. **Chiudere le verifiche** in `CORREZIONI-v4.md`, sezione 5.
2. **Sito:** importare `library-v4.json` (o i CSV) al posto dei dati attuali; titolo, description e canonical propri per `/library` con pre-rendering; una pagina per pattern e per categoria.
3. **Campi da aggiungere alla v4.1:** anno di apertura, numero di camere, fascia di prezzo, `data_verifica` per esempio. Servono per filtrare per dimensione e per misurare i trend nel tempo.
4. **Copertura:** almeno un caso T1/T2 per ogni pattern non nascente e almeno un caso italiano indipendente per famiglia.
5. **Candidati v5** (dall'estratto v3): Rooftop-Driven, Festival-Driven, catene di ex monasteri, Diaspora Hospitality. Entrano solo con un caso verificato.
