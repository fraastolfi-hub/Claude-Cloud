---
name: newsletter-principale
description: Revisiona una newsletter o DEM (hotel, ristoranti, SPA, strutture ricettive) secondo le logiche con cui Gmail smista le email tra Principale e Promozioni. Misura i segnali strutturali dell'HTML, segna ogni riga in verde/giallo/rosso, riscrive solo le righe a rischio mantenendo tono, URL, nomi e date, e dice onestamente quando a un'email conviene restare in Promozioni. Usala ogni volta che l'utente chiede di controllare, revisionare o "passare" una newsletter prima dell'invio, o chiede "finisce in Promozioni?", "come arrivo in Principale?", "perché le aperture sono basse?", "deliverability", "scheda Promozioni", "rendila meno promozionale", "check Gmail", "stile ByeByePromo"; e anche quando incolla l'HTML o il testo di una newsletter appena scritta e chiede un parere, anche senza nominare Gmail.
---

# Newsletter → Principale

Revisione **pre-invio** di una newsletter secondo i segnali che Gmail usa per smistarla tra Principale e Promozioni. Il metodo imita quello di strumenti come ByeByePromo (diagnosi riga per riga, riscrittura mirata, ricontrollo) ma lavora **senza invii reali**. Per questo il risultato è una stima del rischio, non una verifica. Dillo sempre all'utente, in una riga: è la differenza tra un consiglio serio e una promessa falsa.

Prima di pesare un caso dubbio o spiegare un segnale, leggi `references/segnali-gmail.md` (cosa è documentato, cosa è solo osservato, leve specifiche per hospitality).

## 1. Raccogli l'input

Ti servono il **corpo** (HTML del template o testo), l'**oggetto** e il **preheader**. Se ci sono, sono utili anche il nome e l'indirizzo del mittente, l'ESP e lo scopo dell'email.

- Se il file HTML contiene un commento con oggetto e preheader (succede spesso), prendili da lì. Se ci sono più varianti di oggetto (A/B/C), valutale tutte.
- Chiedi solo ciò che manca e cambia il giudizio, soprattutto lo **scopo**. Se non puoi chiedere o l'utente vuole solo il report, procedi: deduci dal contenuto e dichiara le ipotesi in una riga in cima al report.
- Già che ci sei, controlla i riferimenti a date ed eventi rispetto a oggi. Un gancio come "la notte del 25 ottobre" scaduto o imminente va segnalato.

## 2. Decidi prima l'obiettivo giusto

Non tutte le email devono arrivare in Principale. Forzare una DEM di offerta a sembrare una lettera può farle perdere la leva che vende. Classifica l'email:

| Tipo | Obiettivo consigliato |
|---|---|
| Lettera del direttore o dello chef, racconto, novità della stagione | **Principale**: è il caso ideale |
| Email ad habitué, ricontatto dopo il soggiorno, invito personale | **Principale** |
| Newsletter editoriale con un pacchetto dentro | **Principale possibile**, con compromessi sul prezzo e sulle CTA |
| DEM di offerta pura (Black Friday, early booking, last minute con prezzo) | **Promozioni ben presidiata**: annotazioni Gmail, oggetto forte. Proponi in alternativa una versione "lettera" da testare in A/B |
| Transazionali (conferma, pre-arrivo) | Arrivano già in Principale/Aggiornamenti: controlla solo che non contengano blocchi promozionali |

Dichiara l'obiettivo all'inizio del report. Se l'utente ne vuole un altro, segui il suo.

## 3. Misura con lo script

```bash
python3 <percorso-skill>/scripts/analizza_html.py <file> --oggetto "A" --oggetto "B" --preheader "..."
```

Accetta HTML o testo semplice. `--oggetto` è ripetibile, uno per variante; l'indice usa l'oggetto più pulito. Aggiungi `--json` se devi rielaborare i dati. Se l'utente ha incollato il testo in chat, salvalo prima in un file temporaneo.

Lo script ti dà:

- i segnali strutturali con semaforo: immagini ogni 100 parole, link, domini, bottoni, link social, etichette in maiuscolo, peso dell'HTML;
- i colpi di lessico commerciale riga per riga;
- un rischio indicativo.

È un **punto di partenza meccanico** e lo correggerai spesso:

- riconosce "sconto" ma non il tono, quindi una riga senza parole proibite può essere promozionale da cima a fondo ("Regalati il weekend che meriti");
- vede i bottoni solo dallo stile del link;
- non capisce il contesto visivo (un prezzo grande in un riquadro scuro pesa più dello stesso prezzo dentro una frase).

Il semaforo finale lo decidi tu. Quando la tua stima si discosta da quella dello script, scrivi in mezza riga il perché. Il dato su webfont e CSS esterni è solo informativo.

## 4. Leggi come Gmail, riga per riga

Rileggi l'email intera e assegna a ogni riga o blocco un colore:

- 🟢 **verde**: suona come una persona che scrive a una persona; informa o racconta.
- 🟡 **giallo**: neutro ma con un segnale debole (un prezzo dato come informazione, un'etichetta in maiuscolo, un link in più).
- 🔴 **rosso**: tono da volantino, leva di prezzo o di urgenza, CTA imperativa, superlativo, blocco "altre offerte", fila di icone social.

Valuta anche gli elementi che non sono righe di testo:

- **Mittente**: nome di persona o di brand? noreply?
- **Oggetto e preheader**.
- **Struttura**: immagini, bottoni, colonne, footer.

Ricorda che il segnale più forte è il **tono complessivo**. Cinque righe verdi non salvano un layout a volantino.

## 5. Riscrivi solo il rosso (e il giallo che costa poco)

Regole di riscrittura, con il perché:

- **Cambia il minimo.** L'utente ha già scritto un'email che gli piace. Riscrivi solo le righe rosse e lascia intatto il resto: è la promessa del metodo ed è ciò che rende la revisione accettabile.
- **Mantieni il tono dell'autore.** Niente frasi fatte da marketing. Se l'email dà del tu, continua col tu.
- **Non toccare URL, nomi propri, date, numeri di telefono.** Il prezzo può spostarsi (nel testo invece che in un riquadro, o sulla landing) ma non va inventato né cambiato.
- **Trasforma le leve invece di cancellarle.** L'urgenza diventa informazione ("La notte tra il 24 e il 25 dura un'ora in più"), la CTA diventa invito ("Se vuoi venire, rispondi a questa mail"), il prezzo diventa contesto.
- **Proponi i cambi strutturali come elenco di interventi**, senza riscrivere l'HTML se non te lo chiedono: "sostituisci i 2 bottoni con un link nel testo", "togli il blocco altre proposte".
- **Valuta l'effetto sulle vendite.** Per ogni intervento che toglie una leva commerciale, scrivi in mezza riga cosa si perde. L'obiettivo è la prenotazione, non la scheda.

## 6. Formato del report

Usa questa struttura, in italiano:

```
# Revisione Gmail: <oggetto o nome campagna>

**Obiettivo:** Principale | Promozioni ben presidiata | A/B tra le due — <perché, una riga>
**Rischio Promozioni (stima):** oggi Basso/Medio/Alto → dopo gli interventi Basso/Medio/Alto — <i 2-3 motivi principali>
<se hai fatto ipotesi su scopo, mittente o ESP: "Ipotesi: …" in una riga>
> Stima basata sul contenuto: per la conferma serve un seed test (vedi in fondo).

## Segnali strutturali
| Segnale | Valore | Semaforo | Intervento |
(solo le righe gialle e rosse, più quelle verdi che conviene sapere)

## Mittente, oggetto, preheader
<valutazione; se ci sono più varianti di oggetto, confrontale e consiglia quale usare; al massimo 3 alternative nuove>

## Mappa riga per riga
<l'email con 🟢🟡🔴 accanto a ogni riga o blocco; le verdi si possono raggruppare>

## Riscritture
Per ogni riga rossa, e per le gialle che hai scelto di riscrivere (prima le rosse):
- 🔴 Prima: "…"
- 🟢 Dopo: "…"
- Perché: <segnale rimosso> · Costo: <cosa si perde, se qualcosa>

## Interventi sul template
<elenco numerato, dal più efficace al meno>

## Come verificarlo
Seed test su 2–3 caselle Gmail (una nuova, una che ha già interagito), inviando dall'ESP reale. In alternativa ByeByePromo o GlockApps. Prerequisiti tecnici da controllare: SPF/DKIM/DMARC, disiscrizione con un clic, reply-to reale.
```

Se l'utente lo chiede, o se le riscritture sono più di cinque, aggiungi in fondo la **versione completa riscritta** (testo; HTML solo se fornito e richiesto).

## Esempio di riscrittura

- 🔴 Prima: "Approfitta dell'offerta esclusiva: -20% solo fino a domenica! PRENOTA ORA"
- 🟢 Dopo: "Fino a domenica le camere vista lago costano un po' meno. Se ti va di venire, rispondi qui e ti dico cosa c'è libero."
- Perché: tolti esclusiva, percentuale, punti esclamativi, CTA in maiuscolo; la risposta diretta è il segnale di interazione più forte · Costo: lo sconto non salta più all'occhio, quindi va ripreso nell'oggetto o sulla landing.
