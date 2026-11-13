// Diario di bordo Hotel Voyager: dati condivisi di un viaggio formativo.
// Tutto sta in Netlify Blobs, store «voyager»:
//   <viaggio>/stato        hotel, note, sfide, risposte, partecipanti, sintesi (lo leggono tutti col codice)
//   <viaggio>/testimonial  testimonianze di fine viaggio (le legge solo Nicola con la chiave admin)
//
// Variabili d'ambiente (Netlify → Project configuration → Environment variables):
//   VOYAGER_CODICE     codice del viaggio da dare ai partecipanti (obbligatoria)
//   VOYAGER_ADMIN      chiave di Nicola per moderare e leggere i testimonial (obbligatoria)
//   ANTHROPIC_API_KEY  facoltativa: senza, la sintesi con Claude resta spenta

import { getStore } from '@netlify/blobs';

export const VIAGGIO = /^[a-z0-9-]{2,40}$/;
export const store = () => getStore('voyager');

export const vuoto = () => ({
  hotel: [], note: [], sfide: [], risposte: [], partecipanti: [],
  cartaDelGiorno: null, sintesi: {},
});

export const nuovoId = () => Date.now().toString(36) + Math.random().toString(36).slice(2, 7);

// Testo pulito e accorciato: niente HTML (la pagina usa comunque textContent)
export const t = (v, max = 1500) => String(v ?? '').replace(/\u0000/g, '').trim().slice(0, max);

export const json = (statusCode, body) => ({
  statusCode,
  headers: { 'content-type': 'application/json; charset=utf-8', 'cache-control': 'no-store' },
  body: JSON.stringify(body),
});

export const leggiCorpo = (event) => {
  try {
    const raw = event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '{}');
    return JSON.parse(raw);
  } catch { return null; }
};

export const codiceOk = (c) => !!process.env.VOYAGER_CODICE && t(c, 60).toUpperCase() === process.env.VOYAGER_CODICE.trim().toUpperCase();
export const adminOk = (c) => !!process.env.VOYAGER_ADMIN && t(c, 120) === process.env.VOYAGER_ADMIN.trim();

// Legge, modifica e riscrive un documento. Con l'etag due scritture simultanee non si cancellano a vicenda.
export async function modifica(chiave, fn, iniziale = vuoto) {
  const s = store();
  for (let i = 0; i < 8; i++) {
    const r = await s.getWithMetadata(chiave, { type: 'json' });
    const dati = r?.data || iniziale();
    const esito = fn(dati);
    if (esito === false) return { dati, cambiato: false };
    const opz = r ? { onlyIfMatch: r.etag } : { onlyIfNew: true };
    const { modified } = await s.setJSON(chiave, dati, opz);
    if (modified) return { dati, cambiato: true };
    await new Promise((ok) => setTimeout(ok, 60 + Math.random() * 140));
  }
  throw new Error('documento occupato, riprova');
}
