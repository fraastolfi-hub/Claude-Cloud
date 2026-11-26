// Registro di marcia dell'area clienti Moko: legge e salva lo stato delle voci.
// Serve l'intestazione x-registro (vedi lib/moko-registro.mjs); senza, risponde 401 e non mostra niente.
//   GET                → { voci: n, stati, aggiornato, inviati }
//   GET ?anteprima=1   → l'email che partirebbe il primo di questo mese (non la manda)
//   GET ?controllo=1   → true/false per Brevo e destinatari (nessun valore)
//   POST { id, s, chi, voci? } → salva lo stato di una voce; voci = elenco completo mandato dalla pagina
import { getStore } from '@netlify/blobs';
import { CHIAVE, STORE, applica, destinatari, email, indiceMese, pulisciVoci, tokenValido, vuoto } from '../lib/moko-registro.mjs';

const json = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' },
});

export default async (req) => {
  if (!tokenValido(req.headers.get('x-registro'))) return json(401, { ok: false });
  const store = getStore({ name: STORE, consistency: 'strong' });
  const url = new URL(req.url);

  if (req.method === 'GET') {
    const stato = (await store.get(CHIAVE, { type: 'json' })) || vuoto();
    if (url.searchParams.get('controllo')) {
      const d = destinatari();
      return json(200, { brevo: !!(process.env.BREVO_API_KEY && process.env.BREVO_SENDER_EMAIL), destinatario: d.to.length > 0, copia: d.cc.length, voci: stato.voci.length });
    }
    if (url.searchParams.get('anteprima')) {
      // prima di dicembre 2026 mostra la prima email che partirà
      const m = url.searchParams.get('mese');
      const i = m !== null && Number.isInteger(+m) ? +m : Math.max(0, indiceMese());
      return json(200, { ok: true, email: email(stato, i) });
    }
    return json(200, { ok: true, voci: stato.voci.length, stati: stato.stati, aggiornato: stato.aggiornato, inviati: stato.inviati });
  }

  if (req.method !== 'POST') return json(405, { ok: false });
  let d;
  try { d = await req.json(); } catch { return json(400, { ok: false }); }
  // con l'etag due persone che segnano nello stesso momento non si cancellano a vicenda
  for (let t = 0; t < 5; t++) {
    const r = await store.getWithMetadata(CHIAVE, { type: 'json' });
    const stato = r?.data || vuoto();
    const voci = pulisciVoci(d.voci);
    if (voci && voci.length) stato.voci = voci;
    try { applica(stato, d); } catch (e) { return json(400, { ok: false, errore: e.message }); }
    const { modified } = await store.setJSON(CHIAVE, stato, r ? { onlyIfMatch: r.etag } : { onlyIfNew: true });
    if (modified) return json(200, { ok: true, stato: stato.stati[d.id] || null, aggiornato: stato.aggiornato });
  }
  return json(409, { ok: false, errore: 'occupato, riprova' });
};

export const config = { path: '/api/moko-registro' };
