# Hotel Positioning · architettura del sito

## Il problema del sito attuale

1. **La homepage smista, non posiziona.** Si apre con sei sintomi e rimanda subito altrove. Chi arriva non capisce che Francesco è *lo* specialista di posizionamento alberghiero, con un metodo che ha un nome e un libro.
2. **Sei landing quasi identiche.** `landing-booking`, `-prezzi`, `-sostituibili`, `-agenzie`, `-valore` e `-apertura` cambiano solo l'hero: le altre 13 sezioni sono le stesse. Per Google si fanno concorrenza a vicenda, e ogni modifica va ripetuta sei volte.
3. **Il metodo non ha una casa.** I 6 passaggi, la TAC del posizionamento e il Positioning Canvas sono il patrimonio intellettuale che rende Francesco un esperto, ma stanno sepolti nella pagina del libro.
4. **La scala delle offerte non si vede.** Quiz, smontaggio, strumenti, library, libro, analisi gratuita e analisi a €697 esistono, ma nessuna pagina li mette in fila e dice "parti da qui".
5. **Fatti incoerenti tra le pagine**, elencati in fondo a questo documento.

## Il principio

Una categoria, una persona, un metodo, una scala.

- **Categoria:** brand positioning per hotel indipendenti. Non marketing, non agenzia, non revenue.
- **Persona:** Francesco Astolfi, vent'anni da ogni lato del tavolo, operatore e non consulente ("vendo cicatrici").
- **Metodo:** Hotel Positioning, in sei passaggi. Il libro lo racconta, l'analisi lo applica.
- **Scala:** gratis (quiz, smontaggio, strumenti, library) → libro (€19,90) → analisi (gratuita su richiesta oppure €697) → affiancamento continuativo.

Ogni pagina ha **un'azione principale** e al massimo una secondaria, presa dal gradino subito sotto della scala.

## Alberatura

```
/                         Home · categoria + metodo + prova + scala        → CTA: Candida il tuo hotel
├── /metodo/              Il metodo in 6 passaggi (pagina pilastro SEO)     → Analisi · sec.: Libro
├── /analisi/             L'offerta: analisi gratuita su richiesta o €697 + garanzia  → Modulo di richiesta · sec.: Acquista
│   └── /problemi/        Sei ingressi per sintomo (destinazioni delle ads)
│       ├── booking/      "Ogni anno regali €150.000 a Booking"             → Richiesta analisi gratuita
│       ├── prezzi/       "Il tuo prezzo è fermo al 2022"
│       ├── sostituibili/ "Bellissimo. E identico a quello accanto"
│       ├── agenzie/      "Tre agenzie, stesso risultato"
│       ├── valore/       "Quanto vale davvero il tuo hotel?"
│       └── apertura/     "Sto aprendo: non voglio nascere commodity"
├── /casi/                Silva Splendid · Veridia · Yume Ramen             → Analisi
├── /libro/               Pagina di vendita del libro                        → Amazon · sec.: Strumenti gratis
├── /risorse/             Hub degli strumenti gratuiti: "parti da qui"
│   ├── /quiz/            Che hotel sei? 7 domande                           → risultato + Analisi o Libro
│   ├── /smontaggio/      Ti smonto la homepage (6 al mese)                 → form
│   ├── /bonus/           Gli 8 strumenti del libro (i bonus)                → opt-in email
│   └── /library/         69 pattern + 19 categorie, con filtri              → Analisi
├── /francesco/           Chi sono: autorità, storia, cicatrici              → Analisi · sec.: Libro
└── /privacy-policy/
```

Gli URL di quiz, smontaggio, bonus, library, libro, francesco e privacy restano quelli di oggi: il libro stampato e le campagne ci puntano già. Il file `_redirects` porta i vecchi `landing-*` sulle nuove pagine `/problemi/*` mantenendo i parametri UTM.

### Perché le pagine per sintomo restano

Servono alle campagne: chi clicca su "commissioni Booking" deve trovare la sua frase nell'hero. Però diventano **corte e specifiche**: hero, i dieci segnali di quel sintomo, un ponte verso il metodo, l'offerta compatta e il form. Il racconto completo (garanzia, caso Silva, FAQ, tre strade) vive solo in `/analisi/`, una volta sola.

## Navigazione

- **Barra in alto:** Il metodo · Casi · Libro · Risorse gratis · Chi sono · [Candida il tuo hotel]
- **Ticker:** novità del libro, collegato a `/libro/`
- **Footer:** quattro colonne (Metodo, Risorse, Libro e Francesco, Contatti e note legali) con una frase-manifesto.
- **CTA fissa su mobile:** solo sulle pagine con form (analisi, sintomi, smontaggio).

## Tono di voce (vincolante)

Vedi [TONO.md](TONO.md): "voi", registro professionale, il dato prima dell'aggettivo, niente provocazioni. Sostituisce le regole precedenti ("tu", ironia, parolacce).

## Fatti canonici (usare solo questi)

| Tema | Versione canonica | In conflitto con |
|---|---|---|
| Esperienza | 20 anni tra ospitalità e viaggi | — |
| TUI | Da stagista a responsabile marketing, TUI.it da 0 a 30 milioni | — |
| Ata Hotels | Responsabile marketing, gruppo di 20 hotel | "responsabile digital" (home) |
| Web agency | Direttore di una web agency verticale sugli hotel | — |
| Ristorazione | Yume Ramen: 5 locali, da 0 a 2,5 M€, inventato da lui. Enzu Asian Food: altri 5 locali, ghost kitchen lanciata nel 2020 | "due catene portate alla vendita" (landing analisi gratuita) |
| Hotel seguiti | "Decine di hotel" | "142 hotel seguiti" (landing-booking) |
| Silva Splendid | 118 camere, SPA da 1.600 m² (la più grande del Lazio). Posizionamento: **L'Hotel Benessere di Fiuggi**. Fatturato da 3,5 a oltre 7 M€ in cinque anni, insieme alla ristrutturazione. Tariffa media circa ×2. Recensioni Booking da 8,6 a 9 | "Deep Reset Destination" (landing-booking) |
| Veridia | The nature resort of Chia. Vendite dirette sopra il 60%. Nessun prima/dopo di fatturato | — |
| Clienti attuali | Veridia Resort (Chia), Silva Splendid (Fiuggi), Tocq Hotel (Milano), Radisson Blu Bergamo ChorusLife | — |
| Palco | Hospitality Day 2026 | — |
| Analisi | Analisi gratuita su richiesta: fatta a mano da Francesco, massimo 5 al mese, solo hotel e resort dalle 40 camere, consegna in 48-72 ore, 20-25 pagine; dopo, il posizionamento su misura solo se è l'hotel a ricontattare Francesco. La homepage è la pagina della richiesta (`/#richiedi`); /analisi-gratuita.html reindirizza lì. A pagamento: €697 + IVA, 5 documenti operativi (39 pagine), consegna in 48 ore dal questionario, 3 call di controllo (mese 1, 3, 6), garanzia: rimborso più €500 entro 30 giorni | "4 a settimana, entro 72 ore" (landing analisi gratuita) |
| Lettura recensioni | In cinque lingue (italiano, inglese, russo, arabo, cinese), con il supporto dell'AI per le traduzioni: dirlo sempre così, mai come conoscenza diretta delle lingue | — |
| Smontaggio | Gratis, 6 al mese, risposta in 3 giorni lavorativi | — |
| Libro | 120 pagine, 8 figure, 6 passaggi, €19,90 su Amazon (https://www.amazon.it/dp/B0HL3Z4XL7/), anche Kindle, rimborso Amazon 14 giorni. Bonus gratuiti: gli 8 strumenti (non esiste un capitolo gratuito) | — |
| Acquisto analisi | https://buy.stripe.com/aFa8wI5uaduM6LM3fr3AY00 | — |
| Dati legali | Francesco Astolfi, Via Cupa 5, 47923 Rimini (RN), P. IVA 04283940403, consulting@francescoastolfi.net | — |

## Cose da decidere (per Francesco)

1. (Risolto: la landing è stata unita alla homepage.) La landing `analisi-gratuita.html` (mappa del compset, "4 a settimana", consegna in 72 ore) promette un'offerta diversa dalla candidatura del sito. Va allineata, oppure diventa un'offerta separata.
2. Il gradino "affiancamento continuativo / fractional CMO" esiste nei fatti (Tocq, Radisson), ma nessuna pagina lo vende. In `/analisi/` compare solo come "dopo l'analisi, se serve", senza prezzo.
3. Le domande del quiz non erano leggibili dal sito pubblicato: sono state riscritte da zero e vanno validate.
4. I form non inviano ancora dati: vanno collegati al CRM o al servizio di email marketing.
