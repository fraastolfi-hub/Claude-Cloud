// Passaggio verso Amazon che conta i clic senza cookie.
// /vai/amazon?da=libro-alto&utm_source=… → conta il clic e rimanda al link di Amazon Attribution.
// Si salva solo un contatore per giorno: totale e voci «fonte · campagna · bottone».
// Niente IP, user agent o identificativi: non serve il consenso ai cookie.
//
// GET /vai/amazon?conteggio=30  → riepilogo degli ultimi 30 giorni (solo numeri).
//
// Variabili d'ambiente (facoltative):
//   AMAZON_URL   link di destinazione; senza, il tag Attribution «Libro HP · Meta · pagina libro»

import { connectLambda, getStore } from '@netlify/blobs';

const ATTRIBUTION = 'https://www.amazon.it/dp/B0HL3Z4XL7/?maas=maas_adg_5332DAD3AC027CA0D8A1D45F9DD608F0_afap_abs&ref_=aa_maas&tag=maas';
const pulisci = (v) => (v ? String(v).slice(0, 60).replace(/[^\w.\-· ]/g, '') : '');
const giornoRoma = (d = new Date()) => d.toLocaleDateString('sv-SE', { timeZone: 'Europe/Rome' }); // AAAA-MM-GG
const json = (body) => ({ statusCode: 200, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }, body: JSON.stringify(body, null, 1) });

// +1 sul contatore del giorno; con l'etag due clic simultanei non si sovrascrivono
async function conta(store, giorno, voce) {
  const chiave = `giorno-${giorno}`;
  for (let i = 0; i < 5; i++) {
    const r = await store.getWithMetadata(chiave, { type: 'json' });
    const c = r?.data || { totale: 0, voci: {} };
    c.totale += 1;
    c.voci[voce] = (c.voci[voce] || 0) + 1;
    const opz = r ? { onlyIfMatch: r.etag } : { onlyIfNew: true };
    const { modified } = await store.setJSON(chiave, c, opz);
    if (modified) return;
  }
  throw new Error('contatore occupato dopo 5 tentativi');
}

export const handler = async (event) => {
  const q = event.queryStringParameters || {};
  let store;
  try { connectLambda(event); store = getStore('clic-amazon'); } catch (e) { console.error('clic-amazon store', e); }

  if (q.conteggio) {
    const giorni = Math.min(Math.max(parseInt(q.conteggio, 10) || 7, 1), 90);
    const out = {};
    for (let i = 0; i < giorni; i++) {
      const g = giornoRoma(new Date(Date.now() - i * 864e5));
      const c = await store.get(`giorno-${g}`, { type: 'json' });
      if (c) out[g] = c;
    }
    return json(out);
  }

  let errore = null;
  try {
    const voce = `${pulisci(q.utm_source) || 'diretto'} · ${pulisci(q.utm_campaign) || '-'} · ${pulisci(q.da) || '-'}`;
    await conta(store, giornoRoma(), voce);
  } catch (e) {
    errore = String(e && e.message || e);
    console.error('clic-amazon', e); // il conteggio non deve mai fermare chi va a comprare il libro
  }
  if (q.prova) return json({ ok: !errore, errore }); // ?prova=1: conta senza redirect, per verificare
  return { statusCode: 302, headers: { location: process.env.AMAZON_URL || ATTRIBUTION, 'cache-control': 'no-store' }, body: '' };
};
