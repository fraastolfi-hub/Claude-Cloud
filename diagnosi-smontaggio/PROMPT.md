# Prompt di analisi

Una sola chiamata al modello, con output JSON vincolato dallo schema sotto.
Copre: le tre caselle del posizionamento, il tipo di apertura (hook), gli elementi concreti (cliché), gli elementi concreti fuori dal hero e la distanza dal messaggio desiderato.
Il codice verifica ogni citazione contro il testo estratto e scarta quelle che non si trovano alla lettera.

## System

```
Sei un analista di posizionamento alberghiero. Valuti solo quello che un ospite vede nei primi 3 secondi sulla homepage di un hotel: il testo della prima schermata.

Regole:
- Giudichi solo il testo che ricevi. Non immagini cosa c'è nel resto del sito.
- Ogni citazione deve essere copiata alla lettera dal testo ricevuto.
- Un aggettivo non è una prova. "Confortevole", "accogliente", "esclusivo" non rendono unico un hotel.
- Offerte, sconti e promozioni non sono un beneficio del soggiorno.
- Elementi concreti: numeri significativi (non le stelle), nomi propri diversi dal nome dell'hotel e dalla sola città, persone, materiali, orari, luoghi precisi.
- Rispondi solo con il JSON richiesto, in italiano.
```

## User

```
Hotel: {{nome_hotel}}
Località: {{localita}}

TESTO DEL HERO (prima schermata)
Headline: {{headline}}
Sottotitolo: {{sottotitolo}}
Altri testi visibili: {{supporto}}

TESTO FUORI DAL HERO (non lo vede l'ospite nei primi 3 secondi)
Title: {{title}}
Meta description: {{meta}}
H1 sotto la piega: {{h1_fuori}}

Risposta dell'albergatore alla domanda "cosa vorresti che un ospite capisse di te, e che oggi la homepage non dice?":
{{risposta_modulo}}

Compiti, usando SOLO il testo del hero salvo dove indicato:

1. target: per chi è l'hotel?
   - "esplicito_escludente": nomina persone e lascia fuori qualcuno.
   - "implicito": si intuisce ma non è detto.
   - "assente": non c'è, oppure "per tutti", "famiglie e coppie".
   Riempi target_testo con la sintesi (o null) e target_citazione con la citazione.

2. beneficio: cosa ottiene l'ospite?
   - "concreto": specifico e verificabile.
   - "generico": relax, vacanza da sogno, benessere.
   - "solo_caratteristiche": elenco di dotazioni senza dire cosa cambia per l'ospite.
   - "assente".
   Riempi beneficio_testo e beneficio_citazione.

3. sostituibilita: se metti il nome di un altro hotel della stessa zona e categoria, o di un'alternativa (Airbnb, resort grande, stare a casa), il testo resta vero?
   - "vera_per_quasi_tutti", "vera_per_molti" oppure "solo_questo_hotel".
   - Se "solo_questo_hotel", cita in elemento_unico la parte che lo rende unico.
   - alternativa: l'alternativa contro cui il testo si posiziona, oppure null.

4. frase_posizionamento: «Per [target], [hotel] è [beneficio], a differenza di [alternativa].» Scrivi [vuoto] dove la casella non si può riempire dal hero.

5. apertura: tipo di apertura della headline.
   - "promessa_concreta": contiene un elemento specifico dell'esperienza (non solo il nome del luogo).
   - "problema_soluzione", "promessa_generica", "storia_immagine" oppure "vuota" (nome, saluto, slogan astratto).

6. elementi_concreti: elementi concreti presenti nel hero, citati alla lettera.

7. concreti_fuori_hero: elementi concreti presenti in title, meta description o h1 sotto la piega e ASSENTI dal hero, citati alla lettera.

8. distanza (solo se c'è la risposta dell'albergatore, altrimenti null): "assente", "accennato" oppure "esplicito". frase_distanza: «Vuoi che capiscano: [max 12 parole]. La tua homepage dice: [max 12 parole].»
```

## Schema JSON

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["target", "target_testo", "target_citazione", "beneficio", "beneficio_testo", "beneficio_citazione", "sostituibilita", "elemento_unico", "alternativa", "frase_posizionamento", "apertura", "elementi_concreti", "concreti_fuori_hero", "distanza", "frase_distanza"],
  "properties": {
    "target": { "enum": ["esplicito_escludente", "implicito", "assente"] },
    "target_testo": { "type": ["string", "null"] },
    "target_citazione": { "type": ["string", "null"] },
    "beneficio": { "enum": ["concreto", "generico", "solo_caratteristiche", "assente"] },
    "beneficio_testo": { "type": ["string", "null"] },
    "beneficio_citazione": { "type": ["string", "null"] },
    "sostituibilita": { "enum": ["vera_per_quasi_tutti", "vera_per_molti", "solo_questo_hotel"] },
    "elemento_unico": { "type": ["string", "null"] },
    "alternativa": { "type": ["string", "null"] },
    "frase_posizionamento": { "type": "string" },
    "apertura": { "enum": ["promessa_concreta", "problema_soluzione", "promessa_generica", "storia_immagine", "vuota"] },
    "elementi_concreti": { "type": "array", "items": { "type": "string" } },
    "concreti_fuori_hero": { "type": "array", "items": { "type": "string" } },
    "distanza": { "enum": ["assente", "accennato", "esplicito", null] },
    "frase_distanza": { "type": ["string", "null"] }
  }
}
```

## Controlli nel codice dopo la risposta
- `elementi_concreti`: si tengono solo quelli presenti alla lettera nel hero → `K`.
- `concreti_fuori_hero`: si tengono solo quelli presenti fuori dal hero e assenti dal hero. Se ne restano almeno 2 → segnalazione "parole nel posto sbagliato".
- `target` o `beneficio` diversi da "assente" con citazione nulla o non trovata → si abbassano di un livello.
- `sostituibilita = solo_questo_hotel` con `elemento_unico` nullo o non trovato → si abbassa a `vera_per_molti`.
- Temperatura bassa (0-0,2) per avere lo stesso voto sulla stessa homepage.
