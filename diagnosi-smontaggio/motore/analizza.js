// Chiamata al modello per i giudizi AI (PROMPT.md). Provider: OpenAI Chat Completions con output strutturato.

const MODELLO = process.env.DIAGNOSI_MODELLO || 'gpt-4.1';
// Il modello non dà sempre lo stesso giudizio sui casi di confine: si chiedono più risposte e vince la maggioranza.
const RISPOSTE = Number(process.env.DIAGNOSI_RISPOSTE || 5);
const GIUDIZI = ['target', 'beneficio', 'sostituibilita', 'apertura'];

function maggioranza(risposte) {
  const scelto = {};
  for (const campo of GIUDIZI) {
    const conta = {};
    for (const r of risposte) conta[r[campo]] = (conta[r[campo]] || 0) + 1;
    scelto[campo] = Object.entries(conta).sort((a, b) => b[1] - a[1])[0][0];
  }
  // Le citazioni e la frase vengono dalla risposta che concorda di più con i giudizi scelti.
  const punteggio = r => GIUDIZI.filter(c => r[c] === scelto[c]).length;
  const base = [...risposte].sort((a, b) => punteggio(b) - punteggio(a))[0];
  const accordo = Object.fromEntries(GIUDIZI.map(c => [c, risposte.filter(r => r[c] === scelto[c]).length / risposte.length]));
  return { ...base, ...scelto, accordo };
}

const SYSTEM = `Sei un analista di posizionamento alberghiero. Valuti solo quello che un ospite vede nei primi 3 secondi sulla homepage di un hotel: il testo della prima schermata.

Regole:
- Giudichi solo il testo che ricevi. Non immagini cosa c'è nel resto del sito.
- Ogni citazione deve essere copiata alla lettera dal testo ricevuto.
- Un aggettivo non è una prova. "Confortevole", "accogliente", "esclusivo" non rendono unico un hotel.
- Offerte, sconti e promozioni non sono un beneficio del soggiorno.
- Elementi concreti: numeri significativi (non le stelle), nomi propri diversi dal nome dell'hotel e dalla sola città, persone, materiali, orari, luoghi precisi.
  NON sono concreti: parole astratte (silenzio, natura, benessere, relax, bellezza, tradizioni), categorie di servizio (SPA, piscina, ristorante), nomi di città o regione da soli.
- Rispondi solo con il JSON richiesto, in italiano.

Esempi di taratura:
- "Silence, Wild Nature, and the Cleanest Sea in Italy. The only elegant retreat set within a protected Mediterranean nature reserve"
  → beneficio "concreto" (tre cose che l'ospite ottiene, una verificabile: il mare più pulito d'Italia);
  → sostituibilita "solo_questo_hotel", elemento_unico "The only elegant retreat set within a protected Mediterranean nature reserve" (un fatto esclusivo; se è provato o no lo valuta un altro parametro);
  → elementi_concreti ["the Cleanest Sea in Italy", "protected Mediterranean nature reserve"] ("Silence" e "Wild Nature" no: sono astratti).
  → target "implicito": "where true luxury means being completely surrounded by wild nature" lascia intuire per chi è (chi intende il lusso come natura intorno), senza dirlo.
- "Un rifugio sul mare tra silenzio, natura e bellezza" → beneficio "generico", target "assente", sostituibilita "vera_per_molti".
- "HOTEL SOLO PER ADULTI 14+" → target "esplicito_escludente". "Club Family Hotel" nel nome → target "implicito". "Per famiglie e coppie" → "assente".
- "Benvenuti al nostro hotel" o "Hello, Shoreditch!" → apertura "vuota".
- "Camere · SPA e Benessere · Esperienze" (titoli di sezioni) → beneficio "solo_caratteristiche", apertura "vuota".`;

const COMPITI = `Compiti, usando SOLO il testo del hero salvo dove indicato:

0. nome_hotel: il nome della struttura, ricavato da title e testi (es. "Veridia Resort", "Olympic SPA Hotel"). Usalo nella frase del punto 4.

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

4. frase_posizionamento: scrivi SEMPRE la frase intera «Per [target], [nome hotel] è [beneficio], a differenza di [alternativa].» con il nome dell'hotel. Metti [vuoto] solo nelle caselle che non si possono riempire dal hero. Esempio: «Per [vuoto], Hotel Aurora è un'oasi di relax sul mare, a differenza di [vuoto].»

5. apertura: tipo di apertura della headline.
   - "promessa_concreta": contiene un elemento specifico dell'esperienza (non solo il nome del luogo).
   - "problema_soluzione", "promessa_generica", "storia_immagine" oppure "vuota" (nome, saluto, slogan astratto).

6. elementi_concreti: elementi concreti presenti nel hero, citati alla lettera.

7. concreti_fuori_hero: al massimo 5 elementi concreti presenti nel TESTO FUORI DAL HERO e ASSENTI dal hero, citati alla lettera, dal più forte al più debole. Includi riconoscimenti (premi, classifiche). Escludi prezzi, date di offerte, città e regioni da sole.

8. superlativo: la frase del hero con un superlativo o un'esclusiva ("il più", "l'unico", "the only", "the best", "migliore", "-est") citata alla lettera, oppure null.

9. distanza (solo se c'è la risposta dell'albergatore, altrimenti null): "assente", "accennato" oppure "esplicito". frase_distanza: «Vuoi che capiscano: [max 12 parole]. La tua homepage dice: [max 12 parole].»`;

const nullable = tipo => ({ type: [tipo, 'null'] });
const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['nome_hotel', 'target', 'target_testo', 'target_citazione', 'beneficio', 'beneficio_testo', 'beneficio_citazione',
    'sostituibilita', 'elemento_unico', 'alternativa', 'frase_posizionamento', 'apertura', 'elementi_concreti',
    'concreti_fuori_hero', 'superlativo', 'distanza', 'frase_distanza'],
  properties: {
    nome_hotel: { type: 'string' },
    target: { type: 'string', enum: ['esplicito_escludente', 'implicito', 'assente'] },
    target_testo: nullable('string'),
    target_citazione: nullable('string'),
    beneficio: { type: 'string', enum: ['concreto', 'generico', 'solo_caratteristiche', 'assente'] },
    beneficio_testo: nullable('string'),
    beneficio_citazione: nullable('string'),
    sostituibilita: { type: 'string', enum: ['vera_per_quasi_tutti', 'vera_per_molti', 'solo_questo_hotel'] },
    elemento_unico: nullable('string'),
    alternativa: nullable('string'),
    frase_posizionamento: { type: 'string' },
    apertura: { type: 'string', enum: ['promessa_concreta', 'problema_soluzione', 'promessa_generica', 'storia_immagine', 'vuota'] },
    elementi_concreti: { type: 'array', items: { type: 'string' } },
    concreti_fuori_hero: { type: 'array', items: { type: 'string' } },
    superlativo: nullable('string'),
    distanza: { type: ['string', 'null'], enum: ['assente', 'accennato', 'esplicito', null] },
    frase_distanza: nullable('string'),
  },
};

export function messaggioUtente({ nome, localita, hero, fuori, risposta }) {
  return `Hotel (dal title o indicato dall'albergatore): ${nome}
Località: ${localita || 'non indicata'}

TESTO DEL HERO (prima schermata)
Headline: ${hero.headline || '(nessuna frase visibile)'}
Sottotitolo: ${hero.sottotitolo || '(nessuno)'}
Altri testi visibili: ${hero.supporto.length ? hero.supporto.join(' | ') : '(nessuno)'}

TESTO FUORI DAL HERO (non lo vede l'ospite nei primi 3 secondi)
${fuori}

Risposta dell'albergatore alla domanda "cosa vorresti che un ospite capisse di te, e che oggi la homepage non dice?":
${risposta || '(nessuna risposta)'}

${COMPITI}`;
}

export async function analizza(input) {
  const r = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      ...(process.env.OPENAI_API_KEY ? { Authorization: `Bearer ${process.env.OPENAI_API_KEY}` } : {}),
    },
    body: JSON.stringify({
      model: MODELLO,
      temperature: RISPOSTE > 1 ? 0.3 : 0,
      n: RISPOSTE,
      messages: [
        { role: 'system', content: SYSTEM },
        { role: 'user', content: messaggioUtente(input) },
      ],
      response_format: { type: 'json_schema', json_schema: { name: 'diagnosi', strict: true, schema: SCHEMA } },
    }),
  });
  if (!r.ok) throw new Error(`Modello: ${r.status} ${await r.text()}`);
  const j = await r.json();
  return maggioranza(j.choices.map(c => JSON.parse(c.message.content)));
}
