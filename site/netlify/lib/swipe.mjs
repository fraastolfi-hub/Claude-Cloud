// Swipe file (/swipe-file/): pezzi comuni alle funzioni swipe.mjs e swipe-analisi-background.mjs.
//
// Tutto sta in Netlify Blobs, store «swipe»:
//   esempi/<id>   un esempio (JSON)
//   img/<id>      uno screenshot (binario, tipo nei metadati)
//   analisi/<id>  il risultato di un'analisi con Claude (JSON), letto dalla pagina finché non è pronto
//   visti/<sha256> i pezzi già proposti dal radar (URL o id), per non riproporli
//   trad/<id>     la traduzione italiana del copy di un'idea pubblicata (testo), fatta una volta sola
//   adatta/<id>/<sha> «Adattalo al mio hotel»: risposta per una struttura, in cache
//   lavori/<jobid> risultato di un lavoro in background (traduzione o adattamento) letto dalla pagina
//
// Accesso: la pagina manda la chiave, qui si confronta il suo SHA-256 con SWIPE_KEY_SHA256
// (variabile d'ambiente facoltativa) o con l'hash predefinito qui sotto.
import { createHash, timingSafeEqual } from 'node:crypto';
import { getStore } from '@netlify/blobs';
import Anthropic from '@anthropic-ai/sdk';

const HASH_PREDEFINITO = 'f1d29816669aa3080462a9193415900906b8759b934d497708bc2c048f2d5585';

export const ID = /^[0-9a-f-]{36}$/;
export const TIPI = { 'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/gif': 'gif' };

// consistenza «eventual» (default): la «strong» non è disponibile nelle funzioni in stile Lambda
export const store = () => getStore('swipe');

export const json = (statusCode, body) => ({
  statusCode,
  headers: { 'content-type': 'application/json', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' },
  body: JSON.stringify(body),
});

export function leggiCorpo(event) {
  try {
    return JSON.parse(event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '{}'));
  } catch {
    return null;
  }
}

export function autorizzato(chiave) {
  if (typeof chiave !== 'string' || chiave.length < 8 || chiave.length > 200) return false;
  const atteso = Buffer.from((process.env.SWIPE_KEY_SHA256 || HASH_PREDEFINITO).toLowerCase(), 'hex');
  const h = createHash('sha256').update(chiave).digest();
  return h.length === atteso.length && timingSafeEqual(h, atteso);
}

export const testo = (v, max) => (typeof v === 'string' ? v.slice(0, max) : '');

// ---------------------------------------------------------------- analisi

function schema(tax) {
  const tags = {};
  for (const f of tax) tags[f.key] = { type: 'array', items: { type: 'string', enum: f.values } };
  return {
    type: 'object',
    additionalProperties: false,
    required: ['title', 'brand', 'copy', 'why', 'steal', 'tags', 'extra'],
    properties: {
      title: { type: 'string' },
      brand: { type: 'string' },
      copy: { type: 'string' },
      why: { type: 'string' },
      steal: { type: 'string' },
      tags: { type: 'object', additionalProperties: false, required: tax.map((f) => f.key), properties: tags },
      extra: { type: 'array', items: { type: 'string' } },
    },
  };
}

const SISTEMA = `Sei un copy chief esperto di marketing per hotel e ristoranti indipendenti (posizionamento alla April Dunford, livelli di consapevolezza di Eugene Schwartz, direct response). Archivi esempi di marketing in uno swipe file. Rispondi in italiano.

Campi:
- title: massimo 8 parole che nominano l'idea o la tecnica, non il brand.
- brand: brand o struttura se riconoscibile, altrimenti stringa vuota.
- copy: trascrizione fedele del testo visibile (headline, sottotitolo, corpo, CTA), una riga per blocco, massimo 1500 caratteri.
- why: perché funziona, 2-4 frasi concrete sul meccanismo persuasivo, senza aggettivi vuoti.
- steal: come adattarlo a un hotel o ristorante indipendente italiano, 2-3 idee concrete in elenco con trattini.
- tags: da 0 a 4 valori per categoria, solo tra quelli ammessi; per "consapevolezza" al massimo 1; se l'esempio non è hospitality usa settore "Fuori settore".
- extra: al massimo 3 tag liberi brevi in minuscolo.

Scrivi per un albergatore, non per un marketer: niente nomi di autori o esperti di marketing e niente gergo inglese (CTA, upsell, target, hook, funnel, claim, social proof). Italiano comune: «il bottone», «proporre un extra», «i clienti a cui ti rivolgi», «quello che dicono gli altri ospiti». RevPAR e ADR vanno bene.

I dati già inseriti dall'utente hanno la precedenza: non contraddirli.`;

/** Legge screenshot e testo con Claude e restituisce la proposta di campi e tag. */
export async function analizza({ campi = {}, immagini = [], tassonomia = [] }) {
  const tax = (Array.isArray(tassonomia) ? tassonomia : [])
    .filter((f) => f && typeof f.key === 'string' && Array.isArray(f.values))
    .map((f) => ({ key: f.key.slice(0, 40), values: f.values.filter((v) => typeof v === 'string').slice(0, 60) }));
  if (!tax.length) throw new Error('tassonomia mancante');

  const s = store();
  const blocchi = [];
  for (const id of immagini.filter((x) => ID.test(String(x))).slice(0, 4)) {
    const r = await s.getWithMetadata(`img/${id}`, { type: 'arrayBuffer' });
    if (!r) continue;
    const tipo = TIPI[r.metadata?.tipo] ? r.metadata.tipo : 'image/jpeg';
    blocchi.push({ type: 'image', source: { type: 'base64', media_type: tipo, data: Buffer.from(r.data).toString('base64') } });
  }

  const dati = [
    blocchi.length ? "Le immagini allegate sono screenshot dell'esempio." : 'Non ci sono immagini: lavora sul testo fornito.',
    '',
    'Dati già inseriti dall\'utente (possono essere vuoti):',
    `Titolo: ${testo(campi.title, 200) || '-'}`,
    `Brand: ${testo(campi.brand, 120) || '-'}`,
    `Fonte: ${testo(campi.url, 1000) || '-'}`,
    `Copy: ${testo(campi.copy, 4000) || '-'}`,
    `Note: ${testo(campi.why, 1500) || '-'}`,
  ].join('\n');

  const client = new Anthropic({ timeout: 180000, maxRetries: 1 });
  const r = await client.beta.messages.create({
    model: 'claude-opus-5-5',
    max_tokens: 6000,
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
    output_config: { effort: 'low', format: { type: 'json_schema', schema: schema(tax) } },
    system: SISTEMA,
    messages: [{ role: 'user', content: [...blocchi, { type: 'text', text: dati }] }],
  });
  if (r.stop_reason === 'refusal') return { ok: false, errore: 'rifiutato' };
  const blocco = r.content.find((b) => b.type === 'text');
  if (!blocco) return { ok: false, errore: 'risposta_illeggibile' };
  try {
    return { ok: true, proposta: JSON.parse(blocco.text) };
  } catch {
    return { ok: false, errore: 'risposta_illeggibile' };
  }
}


// ---------------------------------------------------------------- traduzione e «Adattalo al mio hotel» (pagina pubblica)

/** Traduce in italiano il copy trascritto di un'idea, riga per riga, senza commenti. */
export async function traduci(esempio) {
  const client = new Anthropic({ timeout: 60000, maxRetries: 1 });
  const r = await client.messages.create({
    model: 'claude-haiku-5-5',
    max_tokens: 1500,
    system: "Traduci in italiano il testo di marketing che ricevi (annuncio, email o pagina web). Mantieni la divisione in righe e l'ordine. Non aggiungere commenti, titoli o note: solo la traduzione. Lascia in originale nomi propri, brand e slogan intraducibili, mettendo tra parentesi la resa italiana se aiuta. Se il testo è già in italiano, restituiscilo identico.",
    messages: [{ role: 'user', content: esempio.copy.slice(0, 6000) }],
  });
  return r.content.filter((b) => b.type === 'text').map((b) => b.text).join('').trim();
}

/** Riscrive il «come rubarlo» per una struttura precisa: tre proposte concrete, pronte da usare. */
export async function adatta(esempio, struttura) {
  const client = new Anthropic({ timeout: 90000, maxRetries: 1 });
  const dati = [
    `Idea: ${esempio.title}`,
    `Brand d'origine: ${esempio.brand || '-'}`,
    `Copy originale:\n${(esempio.copy || '').slice(0, 2500)}`,
    `Perché funziona: ${esempio.why || '-'}`,
    `Come rubarlo (generico): ${esempio.steal || '-'}`,
    '',
    `La struttura del lettore: ${struttura}`,
  ].join('\n');
  const r = await client.messages.create({
    model: 'claude-sonnet-5-5',
    max_tokens: 1200,
    system: `Sei il copy chief di Hotel Positioning, specialista di posizionamento per hotel e ristoranti indipendenti italiani (metodo April Dunford, livelli di consapevolezza di Schwartz, direct response). Ricevi un'idea di marketing presa da un altro brand e la descrizione della struttura di chi legge. Devi adattare il meccanismo a quella struttura.

Rispondi in italiano, dando del tu, in questo formato e niente altro:

**Il meccanismo in una riga**
Una frase: cosa fa funzionare l'idea, spogliata dal brand.

**Tre modi per usarla in ${struttura}**
1. *Dove:* (il canale: annuncio, homepage, email, menu, cartello…) — il copy pronto, tra virgolette, 1-3 righe, con dettagli plausibili per quel tipo di struttura. Poi una riga su cosa serve perché sia vero.
2. idem
3. idem

**Attenzione a**
Una o due righe: l'errore tipico quando si copia questa idea.

Regole: scrivi per un albergatore, non per un marketer: niente nomi di autori o metodi (Dunford, Schwartz…) e niente gergo inglese (CTA, upsell, target, funnel). Niente aggettivi vuoti (unico, esclusivo, emozionante), niente «esperienza». Numeri, nomi, orari, oggetti. Non inventare recensioni o dati della struttura: dove servono, metti un segnaposto tra parentesi quadre, es. [il nome del tuo chef].`,
    messages: [{ role: 'user', content: dati }],
  });
  return r.content.filter((b) => b.type === 'text').map((b) => b.text).join('').trim();
}
