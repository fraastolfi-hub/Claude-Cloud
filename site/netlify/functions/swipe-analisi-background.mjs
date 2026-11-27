// Analisi con Claude di un esempio dello swipe file (/swipe-file/), in background: Netlify risponde subito 202.
// POST { chiave, id, campi, immagini[], tassonomia } → risultato in Blobs, store «swipe», chiave «analisi/<id>»;
// la pagina lo chiede a swipe.mjs (GET ?analisi=<id>) finché non è pronto.
import { connectLambda } from '@netlify/blobs';
import { ID, analizza, autorizzato, leggiCorpo, store } from '../lib/swipe.mjs';

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405 };
  const d = leggiCorpo(event);
  if (!d || !autorizzato(d.chiave) || !ID.test(String(d.id || ''))) return { statusCode: 400 };
  connectLambda(event);
  let risultato;
  try {
    risultato = await analizza(d);
  } catch (e) {
    console.error('swipe analisi', e);
    risultato = { ok: false, errore: e?.status === 429 ? 'troppe_richieste' : 'interno' };
  }
  await store().setJSON(`analisi/${d.id}`, risultato);
  return { statusCode: 200 };
};
