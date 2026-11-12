// Passaggio verso Amazon che conta i clic senza cookie.
// /vai/amazon?da=libro-alto&utm_source=… → salva il clic e rimanda al link di Amazon Attribution.
// Ogni clic è un blob a sé (nessun conflitto tra clic simultanei) con solo: ora, bottone, utm.
// Niente IP, user agent o identificativi: non serve il consenso ai cookie.
//
// GET /vai/amazon?conteggio=30  → riepilogo degli ultimi 30 giorni (solo numeri).
//
// Variabili d'ambiente (facoltative):
//   AMAZON_URL   link di destinazione; senza, il tag Attribution «Libro HP · Meta · pagina libro»

import { connectLambda, getStore } from '@netlify/blobs';

const ATTRIBUTION = 'https://www.amazon.it/dp/B0HL3Z4XL7/?maas=maas_adg_5332DAD3AC027CA0D8A1D45F9DD608F0_afap_abs&ref_=aa_maas&tag=maas';
const CAMPI = ['da', 'utm_source', 'utm_medium', 'utm_campaign', 'utm_content'];
const pulisci = (v) => (v ? String(v).slice(0, 60).replace(/[^\w.\-· ]/g, '') : '');
const giornoRoma = (d = new Date()) => d.toLocaleDateString('sv-SE', { timeZone: 'Europe/Rome' }); // AAAA-MM-GG

export const handler = async (event) => {
  const q = event.queryStringParameters || {};
  connectLambda(event);
  const store = getStore('clic-amazon');

  if (q.conteggio) {
    const giorni = Math.min(Math.max(parseInt(q.conteggio, 10) || 7, 1), 90);
    const riepilogo = {};
    for (let i = 0; i < giorni; i++) {
      const g = giornoRoma(new Date(Date.now() - i * 864e5));
      const { blobs } = await store.list({ prefix: `${g}/` });
      if (!blobs.length) continue;
      const voci = {};
      for (const b of blobs) {
        const r = (await store.get(b.key, { type: 'json' })) || {};
        const k = `${r.utm_source || 'diretto'} · ${r.utm_campaign || '-'} · ${r.da || '-'}`;
        voci[k] = (voci[k] || 0) + 1;
      }
      riepilogo[g] = { totale: blobs.length, voci };
    }
    return { statusCode: 200, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }, body: JSON.stringify(riepilogo, null, 1) };
  }

  try {
    const r = Object.fromEntries(CAMPI.map((c) => [c, pulisci(q[c])]));
    const chiave = `${giornoRoma()}/${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    await store.setJSON(chiave, r);
  } catch (e) {
    console.error('clic-amazon', e); // il conteggio non deve mai fermare chi va a comprare il libro
  }
  return { statusCode: 302, headers: { location: process.env.AMAZON_URL || ATTRIBUTION, 'cache-control': 'no-store' }, body: '' };
};
