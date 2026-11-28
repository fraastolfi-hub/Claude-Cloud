// App delle idee dell'area clienti Moko (/clienti/moko/idee/): salva le decisioni sulle idee.
// Il repository è pubblico: qui ci sono solo i codici delle idee e le decisioni, mai i testi (restano nella pagina cifrata).
// Accesso con lo stesso token del registro (intestazione x-registro, vedi lib/moko-registro.mjs).
//   GET                        → { ok, stati: { id: { s, m?, f?, t } }, aggiornato }
//   POST { id, s, m?, f? }     → s: '' (di nuovo da guardare) | si | no | dopo | fatta | pubblicata
//                                m: motivo del no · f: data (AAAA-MM-GG) fino a cui «non ora» la tiene da parte
import { getStore } from '@netlify/blobs';
import { tokenValido } from '../lib/moko-registro.mjs';

const STORE = 'moko-idee';
const CHIAVE = 'stato';
const STATI = new Set(['', 'si', 'no', 'dopo', 'fatta', 'pubblicata']);
const MOTIVI = new Set(['non-moko', 'aggressiva', 'non-si-gira', 'gia-vista']);
const MAX = 2000;

const json = (status, body) => new Response(JSON.stringify(body), {
  status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' },
});
const vuoto = () => ({ stati: {}, aggiornato: null });

function applica(stato, d) {
  if (typeof d?.id !== 'string' || !/^[a-z0-9_]{2,40}$/.test(d.id)) throw new Error('id');
  if (typeof d.s !== 'string' || !STATI.has(d.s)) throw new Error('stato');
  const ora = new Date().toISOString();
  if (d.s === '') delete stato.stati[d.id];
  else {
    if (!(d.id in stato.stati) && Object.keys(stato.stati).length >= MAX) throw new Error('troppe');
    const v = { s: d.s, t: ora };
    if (d.s === 'no') { if (!MOTIVI.has(d.m)) throw new Error('motivo'); v.m = d.m; }
    if (d.s === 'dopo') { if (typeof d.f !== 'string' || !/^\d{4}-\d{2}-\d{2}$/.test(d.f)) throw new Error('data'); v.f = d.f; }
    stato.stati[d.id] = v;
  }
  stato.aggiornato = ora;
}

export default async (req) => {
  if (!tokenValido(req.headers.get('x-registro'))) return json(401, { ok: false });
  const store = getStore({ name: STORE, consistency: 'strong' });

  if (req.method === 'GET') {
    const stato = (await store.get(CHIAVE, { type: 'json' })) || vuoto();
    return json(200, { ok: true, stati: stato.stati, aggiornato: stato.aggiornato });
  }
  if (req.method !== 'POST') return json(405, { ok: false });
  let d;
  try { d = await req.json(); } catch { return json(400, { ok: false }); }
  // con l'etag due decisioni nello stesso momento non si cancellano a vicenda
  for (let t = 0; t < 5; t++) {
    const r = await store.getWithMetadata(CHIAVE, { type: 'json' });
    const stato = r?.data || vuoto();
    try { applica(stato, d); } catch (e) { return json(400, { ok: false, errore: e.message }); }
    const { modified } = await store.setJSON(CHIAVE, stato, r ? { onlyIfMatch: r.etag } : { onlyIfNew: true });
    if (modified) return json(200, { ok: true, stato: stato.stati[d.id] || null, aggiornato: stato.aggiornato });
  }
  return json(409, { ok: false, errore: 'occupato, riprova' });
};

export const config = { path: '/api/moko-idee' };
