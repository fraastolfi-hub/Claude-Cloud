# Prompt di analisi

Il testo esatto del prompt e lo schema JSON sono in `motore/analizza.js`: quello è il riferimento, questo file ne spiega le scelte.

## Cosa chiede al modello
Una chiamata con output JSON vincolato dallo schema. Il modello riceve:
- il testo del hero (headline, sottotitolo, altri testi visibili);
- il testo fuori dal hero (title, meta description, h1 sotto la piega, seconda schermata);
- la risposta dell'albergatore alla domanda del modulo, se c'è.

E restituisce:
- `nome_hotel`, ricavato da title e testi;
- le tre caselle del posizionamento: `target`, `beneficio`, `sostituibilita` (con citazioni);
- `frase_posizionamento`, sempre intera, con `[vuoto]` nelle caselle che il hero non riempie;
- `apertura` (tipo di headline, per l'hook);
- `elementi_concreti` del hero e al massimo 5 `concreti_fuori_hero`;
- `superlativo` (per la segnalazione "promessa da provare");
- `distanza` e `frase_distanza`, solo se l'albergatore ha risposto.

## Taratura
Il prompt contiene esempi presi dal test sui 6 siti (Veridia landing e homepage, Olympic, Club Family, Hoxton, Moko). Servono a fissare i casi di confine concordati:
- un'esclusiva dichiarata ("the only... within a protected nature reserve") vale `solo_questo_hotel`: se è provata lo misura la riprova sociale;
- parole astratte (silenzio, natura, benessere) e categorie (SPA, piscina) non sono elementi concreti;
- "solo adulti 14+" è un target esplicito, "Family" nel nome è implicito, "famiglie e coppie" è assente.

## Stabilità
Sui casi di confine lo stesso modello può rispondere in modo diverso da una chiamata all'altra (nel test la landing di Veridia oscillava tra 67 e 75, a cavallo della soglia di 70). Per questo si chiedono 5 risposte nella stessa chiamata (`n: 5`, temperatura 0,3) e per ogni giudizio vince la maggioranza. Il risultato riporta anche l'`accordo` per campo: sotto 0,6 il giudizio è incerto e va guardato nello Smontaggio a mano.

Modello e numero di risposte si cambiano con le variabili `DIAGNOSI_MODELLO` (predefinito `gpt-4.1`) e `DIAGNOSI_RISPOSTE` (predefinito 5).

## Controlli nel codice dopo la risposta (`motore/voto.js`)
- `elementi_concreti`: si tengono solo quelli presenti alla lettera nel hero.
- `concreti_fuori_hero`: si tengono solo quelli presenti fuori dal hero e assenti dal hero.
- `target` o `beneficio` con citazione assente dal hero scendono di un livello.
- `solo_questo_hotel` senza `elemento_unico` trovato nel hero scende a `vera_per_molti`.
- `superlativo` non trovato nel hero viene scartato.
