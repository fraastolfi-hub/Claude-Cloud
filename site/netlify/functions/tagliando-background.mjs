// Funzione in background del Tagliando (Netlify risponde subito 202, il lavoro può durare fino a 15 minuti).
// POST { id, parte: 'pagina' | 'velocita', url, hotel }  → il risultato finisce in Netlify Blobs, store «tagliando»,
// chiave «<id>-<parte>». La pagina lo chiede a functions/tagliando.mjs (GET ?id=…&parte=…) finché non è pronto.
import { connectLambda, getStore } from '@netlify/blobs';
import { esegui, ID } from '../lib/tagliando-lavori.mjs';

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405 };
  let d;
  try { d = JSON.parse(event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '{}')); } catch { return { statusCode: 400 }; }
  if (!ID.test(String(d.id || '')) || !['pagina', 'velocita'].includes(d.parte)) return { statusCode: 400 };
  connectLambda(event);
  const store = getStore('tagliando');
  const risultato = await esegui(d.parte, d);
  await store.setJSON(`${d.id}-${d.parte}`, risultato);
  return { statusCode: 200 };
};
