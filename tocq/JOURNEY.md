# Tocq · il percorso del sito, dalla prima schermata all'ultima call to action

Progetto di esperienza per il nuovo tocq.it. Parte dal posizionamento ("Base a Garibaldi"), dal brand book e dalla bozza in `bozza/`. Definisce struttura, racconto, gerarchia, transizioni, interazioni e punti di conversione.

---

## 0. Che cosa vuol dire "lusso" per il Tocq

Il posizionamento esclude il lusso inteso come opulenza: "lusso", "esclusivo" e "raffinato" sono parole bandite, e chi cerca il design di categoria superiore è un ospite da non inseguire. Il Tocq non deve sembrare un cinque stelle.

Il lusso che il Tocq può offrire è un altro: **non dover pensare a niente.** Il treno a 200 metri, il cuscino già sul letto, la colazione pronta alle sei, qualcuno che ti chiama per nome. Il sito deve dare la stessa sensazione:

| Lusso come opulenza (no) | Lusso come assenza di attrito (sì) |
|---|---|
| Video a tutto schermo, musica, effetti | Una foto vera, una frase, un orario |
| Scroll guidato, animazioni lunghe | Lo scroll resta dell'utente; ogni movimento sotto i 400 ms |
| Aggettivi ("un'oasi raffinata") | Numeri ("200 m dal binario") |
| Tutto in un menu nascosto | Due percorsi visibili, sempre |
| Il form arriva alla fine | Si può agire da qualunque punto |

**Principio guida:** immersivo nel ritmo, essenziale nella forma. L'immersione nasce dal racconto (una giornata dall'arrivo alla partenza), dalla luce che cambia e dal simbolo del marchio che si apre, non dagli effetti.

---

## 1. Chi percorre il sito, e cosa deve succedere

| Visitatore | Arriva da | Cosa cerca nei primi 10 secondi | Conversione principale | Conversione di riserva |
|---|---|---|---|---|
| **Il viaggiatore d'affari** (best-fit, 4,60 su Google) | Google "hotel Porta Nuova", link aziendale, assistente AI | Distanza da ufficio e treno, notte tranquilla | Prenotazione diretta con configuratore | Richiesta tariffa aziendale |
| **Chi organizza un evento** (MICE, 37% del ricavo) | Google "sale meeting Porta Nuova", passaparola | Capienze, camere nello stesso edificio, tempi di risposta | Richiesta preventivo | Download della presentazione |
| **Chi viene per un evento** (Fiera, San Siro, Monza) | Google "hotel per San Siro", app di eventi | Come arrivo, a che ora parto | Prenotazione diretta | Salva/condividi tragitto |
| **La coppia del weekend** (coppie straniere 48,7% su Booking) | Booking: controlla il sito prima di prenotare | Foto, prezzo, rumore | Prenotazione diretta con lato corte | Nessuna: va bene anche che prenoti sull'agenzia |

Il sito non deve scegliere fra i quattro: la home li serve tutti con **un bivio esplicito** (§3, capitolo 2) e poi li accompagna con la stessa storia.

---

## 2. L'arco del racconto

Il sito racconta **una giornata dal Tocq**, in sei capitoli, che seguono la mappa del lavoro dell'ospite nell'analisi (decidere, arrivare, eseguire, dormire, ripartire, tornare):

```
ARRIVO ─── IL BIVIO ─── LA SERA ─── LA NOTTE ─── L'ALBA ─── IL RITORNO
 18:40      perché       20:00       23:00        06:30      +30 giorni
            sei qui
```

**La luce come filo conduttore.** Mentre si scende, i fondi seguono l'ora del giorno, usando solo i colori del brand book:

| Capitolo | Ora | Fondo | Perché |
|---|---|---|---|
| Arrivo | 18:40 | Bianco | Chiarezza, il primo colpo d'occhio |
| Il bivio | — | Bianco | Due percorsi a parità di peso |
| La sera | 20:00 | Corallo 20% → Corallo 50% | Luce calda di Corso Como |
| La notte | 23:00 | Nero | Il silenzio, il lato corte |
| L'alba | 06:30 | Verde 20% | La luce fredda del mattino |
| Il ritorno | +30 gg | Bianco | Si chiude dove si è iniziato |

Il cambio di fondo è una dissolvenza di 300 ms quando la sezione supera metà schermo. Non c'è scrolljacking.

**Il simbolo come firma.** Il brand book descrive il simbolo come "una porta che si apre e invita a entrare" e "una finestra su Milano". Il sito lo usa in due soli momenti:
1. **All'ingresso:** le due ante del simbolo si aprono (600 ms, una volta sola per sessione) e lasciano vedere la foto della camera con le torri di Porta Nuova. La finestra su Milano diventa letterale.
2. **Alla fine:** nell'ultima call to action le ante sono aperte e tengono dentro di sé i due bottoni. La porta è aperta: entra.

Tutto il resto del sito è fermo e preciso.

---

## 3. La home, sezione per sezione

Ogni sezione ha **un solo messaggio**, un titolo di 8 parole al massimo, un dato prima di ogni aggettivo, e una via d'uscita verso la conversione.

### Capitolo 1 · Arrivo

**S1 · Ingresso (hero)**
- **Messaggio:** "Scendi a Garibaldi. Sei arrivato."
- **Gerarchia:** H1 → quattro promesse con il loro dato (200 M, SALA, PRIMA, ALL'ALBA) → due bottoni di pari peso visivo (Prenota una camera · Organizza un evento) → tre voti con fonte.
- **Visivo:** a destra, foto della camera con le torri dalla finestra (`camera-vista-torri-porta-nuova`). Su mobile la foto va sopra, alta il 45% dello schermo, così il titolo resta visibile senza scorrere.
- **Interazione:** apertura delle ante del simbolo (vedi §2). Con `prefers-reduced-motion` la foto è già visibile.
- **Conversione:** primaria (Prenota) e secondaria (Evento) visibili senza scorrere su tutte le larghezze da 360 px in su.
- **Uscita verso:** il tabellone, con un piccolo indicatore "↓ 18:40, scendi dal treno".

**S2 · Il tabellone**
- **Messaggio:** la posizione detta come un orario ferroviario, non come "centro".
- **Gerarchia:** destinazione → mezzo → tempo (in corallo, l'unico colore acceso) → motivo.
- **Interazione:**
  - le cifre dei tempi arrivano con un effetto a palette, come i tabelloni di stazione: 250 ms, una volta sola, solo per i numeri;
  - l'orologio segna l'ora di Milano;
  - toccando una riga si apre il tragitto (link a Google Maps con le indicazioni a piedi o con i mezzi).
- **Conversione:** micro, "Vedi tutte le destinazioni" verso `/posizione/`.
- **Transizione:** fascia del pattern nero/bianco di 48 px, la "soglia" fra un capitolo e l'altro.

### Capitolo 2 · Il bivio

**S3 · Perché sei a Milano**
- **Messaggio:** "Due motivi, un indirizzo."
- **Interazione chiave: il selettore di intenzione.** Un controllo a due posizioni, "Sono qui per dormire e lavorare" / "Sto organizzando un evento". Non nasconde nulla: cambia **l'ordine e i bottoni** del resto della home.
  - *Dormire e lavorare:* la sezione MICE scende dopo la squadra; il bottone fisso diventa "Prenota".
  - *Evento:* la sezione sale sale subito dopo il bivio; il bottone fisso diventa "Preventivo"; il configuratore mostra "Blocco camere per i partecipanti".
  - La scelta è ricordata per la visita (localStorage) e mandata alle analytics come segmento.
- **Visivo:** due card con foto, stessa larghezza, stesso peso (regola del posizionamento: il MICE non va in fondo al menu).
- **Conversione:** è il primo punto in cui il visitatore si dichiara. Dato da misurare: la percentuale che sceglie, divisa per sorgente.

**S4 · In breve**
- **Messaggio:** il Tocq in nove righe, per chi decide velocemente, per Google e per gli assistenti AI.
- **Interazione:** nessuna. È la sezione di riferimento, si legge come una carta d'identità.

### Capitolo 3 · La sera (fondo corallo)

**S5 · Una giornata da qui, prima parte: 18:40 e 20:00**
- **Messaggio:** "Fai quello che sei venuto a fare."
- **Struttura:** linea del tempo orizzontale su desktop, verticale su mobile. Ogni momento è fatto di ora, una frase, una foto e un fatto verificabile:
  - **18:40 · Arrivo:** il trolley dalla stazione; fatto: 200 m.
  - **20:00 · La sera:** Corso Como a 50 m; fatto: la guardia notturna all'ingresso al ritorno.
- **Interazione:** l'ora è "agganciata" in alto mentre si scorre il momento, così si sa sempre dove si è nella giornata. Su mobile si scorre normalmente, senza aggancio.

### Capitolo 4 · La notte (fondo nero)

**S6 · 23:00 · Prepara la tua notte (configuratore in versione breve)**
- **Messaggio:** "Su Booking prenoti una camera. Qui scegli il cuscino, il materasso e il lato da cui dormi."
- **Interazione:** tre scelte già in home (cuscino, lato, colazione) con il riepilogo che si compone a destra in corallo; il bottone porta a `/camere/#configura` con le scelte già compilate (parametri nell'URL). È un **impegno piccolo prima di quello grande**: chi ha scelto il cuscino ha già immaginato la notte.
- **Conversione:** primaria. Evento `uso_configuratore` e passaggio con le scelte alla pagina camere.

**S7 · Il confronto**
- **Messaggio:** "Stessa camera, due modi di prenotarla."
- **Posizione:** subito dopo il desiderio, dove nasce l'obiezione ("costerà di più?").
- **Interazione:** la colonna "tocq.it" si illumina in corallo riga per riga mentre entra nello schermo (100 ms fra una riga e l'altra).
- **Conversione:** bottone "Scegli le date" in fondo alla tabella.

### Capitolo 5 · L'alba (fondo verde chiaro)

**S8 · 06:30 · La colazione da portare via**
- **Messaggio:** "Se parti all'alba, la colazione te la portiamo via noi."
- **Visivo:** foto del sacchetto della colazione da asporto sul banco, fuori ancora buio (da scattare).
- **Fatto:** buffet con opzioni halal, senza glutine e vegane; aperto anche agli esterni a 16 €.

**S9 · La squadra**
- **Messaggio:** "A colazione qualcuno ti chiama per nome."
- **Interazione:** i nomi sono etichette; toccandone una compare la citazione dell'ospite che l'ha nominata, con fonte e voto. Prova sociale legata a persone vere, non a stelline.
- **Visivo:** ritratti della squadra in luce naturale (da scattare, con consenso).

**S10 · Le sale sotto le camere** (posizione mobile: sale qui con l'intenzione "dormire", dopo il bivio con "evento")
- **Messaggio:** "Dormi dove ti riunisci."
- **Gerarchia:** quattro numeri (6 sale · 100 a platea · 200 m · 24 h) → foto della Sala Duomo → due bottoni.
- **Conversione:** secondaria, Richiedi un preventivo · Scarica la presentazione.

### Capitolo 6 · Il ritorno (fondo bianco)

**S11 · Prove**
- **Messaggio:** i voti con la fonte e la data (8,8/10 Expedia, 4,60/5 di chi viaggia per lavoro, 8,98 pulizia e comfort). Più la frase di chi torna: "una vera seconda casa".

**S12 · Detto prima**
- **Messaggio:** "Il Duomo è a 2,5 km."
- **Perché qui, così tardi:** è la risposta onesta all'unica vera obiezione dei turisti. Arriva dopo che il valore è chiaro, e chiude la porta alle recensioni "30 minuti dal centro".

**S13 · Domande**
- **Struttura:** otto domande chiuse, la prima aperta. Ogni risposta comincia con il dato.
- **Interazione:** apertura a fisarmonica, 200 ms, l'URL prende l'ancora della domanda (così si può condividere una risposta).

**S14 · La porta aperta (call to action finale)**
- **Messaggio:** "Il treno a 200 metri. La sala al piano. Il cuscino già scelto."
- **Visivo:** il simbolo del marchio grande, con le ante aperte; dentro, i due bottoni (Prenota · Preventivo) e sotto il numero della reception 24 ore. Fondo nero, fascia del pattern salmone sopra il footer.
- **Conversione:** primaria e secondaria, più il telefono per chi preferisce parlare con qualcuno.

---

## 4. Le pagine interne: lo stesso ritmo, più corto

Ogni pagina segue la stessa grammatica: **promessa → fatti → prova → scelta → obiezioni → azione**.

| Pagina | Promessa (H1) | Fatti | Prova | Scelta | Obiezioni | Azione |
|---|---|---|---|---|---|---|
| Camere | "Stanotte dormi. Domani lavori." | In breve; 4 tipologie con foto e numero | Citazione sul menu cuscini | Configuratore completo | Regole della casa (clima, silenzio, valigie, parcheggio); FAQ | Booking engine con le scelte compilate |
| Meeting | "Dormi dove ti riunisci." | In breve; tabella delle 6 sale | Eventi ospitati; Olimpiadi 2026 | Formule; selettore della sala per numero di persone | Confronto con centro congressi e catena; FAQ | Preventivo in 6 campi; download |
| Posizione | "A Milano sei già dove devi essere." | In breve; tabella filtrabile | Recensioni sulla posizione | Filtri lavoro / partire / eventi / tempo libero | "Il Duomo è a 2,5 km" | "Calcola il tragitto"; Prenota |
| Contatti | "Una domanda, una persona." | Tre contatti con nome | — | Motivo della richiesta | FAQ | Form instradato alla persona giusta |

**Due interazioni da aggiungere alle pagine interne:**
1. **Meeting · "Quante persone siete?"**: un cursore da 10 a 100. Mentre si muove, le sale che non bastano si spengono nella tabella, e quelle giuste si evidenziano con l'allestimento possibile. Poi un bottone: "Preventivo per 40 persone in Sala Scala", con il form già compilato.
2. **Posizione · "Dove devi andare domani?"**: un campo con suggerimenti (Fiera Rho, MiCo, San Siro, Monza, Linate, Malpensa, un indirizzo). Risposta: mezzo, tempo e l'ultima partenza utile. Diventa il ponte verso la prenotazione: "Domani alle 9 a Rho? Dormi a 200 m dal treno."

---

## 5. Navigazione e punti di conversione

**Sempre visibili:**
- Header con marchio orizzontale, quattro voci, lingua e il bottone **Prenota** (nero pieno).
- Su mobile, barra fissa in basso con due bottoni (Prenota · Preventivo evento). L'ordine dei bottoni segue il selettore di intenzione. La barra si nasconde quando c'è un form nello schermo, per non coprire i campi.

**Mappa dei punti di conversione:**

| Livello | Azione | Dove | Evento da misurare |
|---|---|---|---|
| Primaria | Prenotazione diretta | Hero, S6, S7, S14, header, barra mobile, camere | `prenotazione_diretta` (con ricavo) |
| Primaria | Richiesta preventivo | Hero, S10, S14, barra mobile, meeting | `richiesta_preventivo_mice` |
| Secondaria | Download presentazione | S10, meeting | `download_presentazione` |
| Secondaria | Richiesta tariffa aziendale | Footer, contatti, pagina business (fase 2) | `richiesta_tariffa_aziendale` |
| Micro | Selettore di intenzione | S3 | `intenzione_scelta` |
| Micro | Configuratore | S6, camere | `uso_configuratore` |
| Micro | Tragitto | S2, posizione | `tragitto_aperto` |
| Micro | Telefono | S14, footer, FAQ | `chiamata_reception` |

**Regola:** non c'è mai più di una call to action primaria per schermata, e non c'è mai una schermata senza un'uscita verso la conversione.

---

## 6. Sistema di movimento

| Principio | Regola |
|---|---|
| Lo scroll è dell'utente | Niente scrolljacking, niente sezioni bloccate oltre l'aggancio dell'ora in S5 (solo desktop) |
| Movimento con un significato | Si muove solo ciò che porta informazione: le ante (ingresso), le cifre (tabellone), la colonna del confronto, il riepilogo del configuratore |
| Durate | 150–300 ms per le interazioni, 600 ms per le ante; curva `cubic-bezier(.2,.7,.2,1)` |
| Una volta sola | Le animazioni d'ingresso non si ripetono tornando indietro |
| Movimento ridotto | Con `prefers-reduced-motion` tutto appare già al suo posto, senza dissolvenze |
| Soglie fra capitoli | Fascia del pattern alta 48 px che entra con una traslazione di 24 px; è l'unico elemento decorativo |

**Micro-interazioni:**
- Bottoni: il nero diventa nero 80% e la freccia si sposta di 4 px.
- Scelte del configuratore: il bordo diventa nero pieno e il riepilogo aggiorna il valore con una dissolvenza di 150 ms.
- Link nel testo: sottolineatura che cresce da sinistra.
- Foto: nessun zoom al passaggio del mouse (sono prove, non decorazioni).

---

## 7. Gerarchia dei contenuti

- **Titoli:** Futura Bold, 8 parole al massimo, frasi intere con il punto.
- **Etichette:** Futura Medium maiuscolo spaziato, 11–12 px; dicono dove sei (es. "UNA GIORNATA DA QUI").
- **Dati:** sempre in cifre, mai in lettere; in corallo su nero, in nero su chiaro.
- **Testo corrente:** Futura Light 17 px, righe di 60–70 caratteri, un paragrafo per idea.
- **Prove:** citazione in corsivo con la fonte in etichetta (canale, voto, contesto).
- **Ordine dentro ogni sezione:** etichetta → titolo → una riga di contesto → il dato o la scelta → l'azione.

---

## 8. Usabilità e accessibilità, senza compromessi

- Contrasto almeno AA: il corallo si usa solo su nero (rapporto 9:1), mai come testo su bianco.
- Bersagli di tocco di almeno 44 px; i bottoni della barra mobile sono alti 48 px.
- Ogni interazione funziona da tastiera; focus visibile in corallo su nero e in nero su chiaro.
- Il selettore di intenzione è un vero gruppo di pulsanti radio; il configuratore è un form vero.
- Tempi di caricamento: foto WebP a 800 e 1600 px, la prima immagine caricata con priorità, LCP sotto 2,5 s su 4G, nessuna libreria di animazione esterna (CSS e un JavaScript sotto i 10 KB).
- I contenuti principali sono nell'HTML, non generati dal JavaScript: servono a Google e agli assistenti AI.

---

## 9. Mobile: lo stesso viaggio, nel palmo

- **Ordine:** foto (45% dello schermo) → H1 → promesse → bottoni. Il tabellone mostra tre colonne (destinazione, mezzo, tempo).
- **Il bivio** diventa una barra a due segmenti agganciata sotto l'header per tutta la home, così si può cambiare intenzione senza tornare su.
- **La giornata** è una lista verticale con l'ora grande a sinistra.
- **Il configuratore** usa scelte a schede scorrevoli orizzontali; il riepilogo diventa una riga fissa sopra la barra dei bottoni ("Piuma d'oca · Corte · Da asporto 06:30").
- **Il telefono** è un'azione di prima classe: "Chiama la reception" in S14 e nel footer.

---

## 10. Come si misura il successo

| Domanda | Metrica | Obiettivo iniziale (da fissare con il revenue) |
|---|---|---|
| Il bivio funziona? | % di visite che scelgono un'intenzione | > 35% |
| Il configuratore spinge alla prenotazione? | Prenotazioni di chi lo usa / prenotazioni di chi non lo usa | > 1,5× |
| Il confronto toglie l'obiezione prezzo? | Clic su "Scegli le date" da S7 | da misurare |
| Il MICE ha la stessa dignità del soggiorno? | Richieste preventivo / mese | base: da misurare al lancio |
| Il sito toglie notti alle agenzie? | Notti da sito e app | base 2026: 434 notti, 1,4% |

**Primi test A/B dopo il lancio:**
1. Hero con le ante animate contro hero statico (tempo al primo clic e rimbalzo).
2. Confronto prima o dopo la squadra.
3. Selettore di intenzione visibile in S3 contro agganciato sotto l'header anche su desktop.

---

## 11. Cosa cambia rispetto alla bozza attuale

| Elemento | Oggi nella bozza | Da fare |
|---|---|---|
| Ante del simbolo all'ingresso e nella CTA finale | — | Nuovo (SVG del simbolo già pronto, `assets/img/simbolo.svg`) |
| Selettore di intenzione | — | Nuovo, con riordino delle sezioni |
| Luce che cambia per capitolo | Fondi fissi | Nuovo, dissolvenza al cambio capitolo |
| Configuratore breve in home | Solo link | Nuovo, con passaggio delle scelte nell'URL |
| Ora agganciata nella giornata | Linea statica | Nuovo, solo desktop |
| Cifre a palette nel tabellone | Statiche | Nuovo |
| Cursore "Quante persone siete?" | — | Nuovo, pagina meeting |
| "Dove devi andare domani?" | Filtri | Nuovo, pagina posizione |
| CTA finale con il simbolo aperto | Footer | Nuovo, S14 |
| Foto colazione da asporto, squadra, sale | Segnaposto | Shooting o file più leggeri dal Drive |
| In breve, FAQ, confronto, prove, barra mobile | Presenti | Restano, riordinati secondo §3 |
