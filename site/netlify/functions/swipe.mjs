// Swipe file privato (/swipe-file/). Dati e screenshot in Netlify Blobs, vedi ../lib/swipe.mjs.
//
//   GET  ?img=<id>                      → lo screenshot (id casuale non indovinabile, noindex)
//   GET  ?analisi=<id>&chiave=…         → { pronto, ok, proposta | errore } dell'analisi in background
//   POST { azione, chiave, … }:
//        verifica                       → { ok }
//        elenco                         → { esempi[] }
//        carica { tipo, dati(base64) }  → { id } dello screenshot
//        salva { esempio, rimosse[] }   → { esempio }
//        elimina { id }                 → { ok }
//        scarta { immagini[] }          → { ok } (screenshot caricati e poi non salvati)
// L'analisi con Claude parte da swipe-analisi-background.mjs (dura più dei 10 secondi di una funzione normale).
import { randomUUID } from 'node:crypto';
import { connectLambda } from '@netlify/blobs';
import { ID, TIPI, autorizzato, json, leggiCorpo, store, testo } from '../lib/swipe.mjs';

const MAX_IMG = 4.4 * 1024 * 1024;

async function usate(s) {
  const { blobs } = await s.list({ prefix: 'esempi/' });
  const tutte = new Set();
  for (const b of blobs) {
    const e = await s.get(b.key, { type: 'json' });
    (e?.images || []).forEach((i) => tutte.add(i));
  }
  return tutte;
}

async function elenco(s) {
  const { blobs } = await s.list({ prefix: 'esempi/' });
  const out = [];
  for (let i = 0; i < blobs.length; i += 25) {
    const parte = await Promise.all(blobs.slice(i, i + 25).map((b) => s.get(b.key, { type: 'json' })));
    out.push(...parte.filter(Boolean));
  }
  return out.sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
}

export const handler = async (event) => {
  connectLambda(event);
  const s = store();
  const q = event.queryStringParameters || {};

  if (event.httpMethod === 'GET') {
    if (q.img) {
      if (!ID.test(q.img)) return { statusCode: 404 };
      const r = await s.getWithMetadata(`img/${q.img}`, { type: 'arrayBuffer' });
      if (!r) return { statusCode: 404 };
      return {
        statusCode: 200,
        headers: { 'content-type': r.metadata?.tipo || 'image/jpeg', 'cache-control': 'private, max-age=31536000, immutable', 'x-robots-tag': 'noindex' },
        body: Buffer.from(r.data).toString('base64'),
        isBase64Encoded: true,
      };
    }
    if (q.analisi) {
      if (!autorizzato(q.chiave)) return json(401, { ok: false, errore: 'chiave_errata' });
      if (!ID.test(q.analisi)) return json(400, { ok: false, errore: 'richiesta' });
      const r = await s.get(`analisi/${q.analisi}`, { type: 'json' });
      if (r) await s.delete(`analisi/${q.analisi}`);
      return json(200, r ? { pronto: true, ...r } : { pronto: false });
    }
    return json(200, { ANTHROPIC_API_KEY: !!process.env.ANTHROPIC_API_KEY, SWIPE_KEY_SHA256: !!process.env.SWIPE_KEY_SHA256 });
  }
  if (event.httpMethod !== 'POST') return json(405, { ok: false });

  const d = leggiCorpo(event);
  if (!d) return json(400, { ok: false, errore: 'richiesta' });
  if (!autorizzato(d.chiave)) return json(401, { ok: false, errore: 'chiave_errata' });

  try {
    switch (d.azione) {
      case 'verifica':
        return json(200, { ok: true });

      case 'elenco':
        return json(200, { ok: true, esempi: await elenco(s) });

      case 'carica': {
        if (!TIPI[d.tipo]) return json(400, { ok: false, errore: 'formato_non_supportato' });
        const buf = Buffer.from(String(d.dati || ''), 'base64');
        if (!buf.length) return json(400, { ok: false, errore: 'richiesta' });
        if (buf.length > MAX_IMG) return json(413, { ok: false, errore: 'immagine_grande' });
        const id = randomUUID();
        await s.set(`img/${id}`, buf, { metadata: { tipo: d.tipo } });
        return json(200, { ok: true, id });
      }

      case 'salva': {
        const e = d.esempio || {};
        const esistente = typeof e.id === 'string' && ID.test(e.id) ? await s.get(`esempi/${e.id}`, { type: 'json' }) : null;
        if (e.id && !esistente) return json(404, { ok: false, errore: 'non_trovato' });
        const images = (Array.isArray(e.images) ? e.images : []).filter((x) => ID.test(String(x))).slice(0, 20);
        const tags = [...new Set((Array.isArray(e.tags) ? e.tags : []).filter((t) => typeof t === 'string' && t.includes(':')).map((t) => t.slice(0, 120)))].slice(0, 80);
        const ora = new Date().toISOString();
        const riga = {
          id: esistente?.id || randomUUID(),
          created_at: esistente?.created_at || ora,
          updated_at: ora,
          title: testo(e.title, 200).trim(),
          brand: testo(e.brand, 120).trim(),
          url: testo(e.url, 1000).trim(),
          copy: testo(e.copy, 20000),
          why: testo(e.why, 8000),
          steal: testo(e.steal, 8000),
          rating: Math.max(0, Math.min(5, Math.round(Number(e.rating) || 0))),
          tags,
          images,
        };
        if (!riga.title && !riga.copy.trim() && !images.length) return json(400, { ok: false, errore: 'vuoto' });
        await s.setJSON(`esempi/${riga.id}`, riga);
        const rimosse = (Array.isArray(d.rimosse) ? d.rimosse : []).filter((x) => ID.test(String(x)) && !images.includes(x));
        await Promise.allSettled(rimosse.map((x) => s.delete(`img/${x}`)));
        return json(200, { ok: true, esempio: riga });
      }

      case 'elimina': {
        if (!ID.test(String(d.id || ''))) return json(400, { ok: false, errore: 'richiesta' });
        const e = await s.get(`esempi/${d.id}`, { type: 'json' });
        await s.delete(`esempi/${d.id}`);
        await Promise.allSettled((e?.images || []).map((x) => s.delete(`img/${x}`)));
        return json(200, { ok: true });
      }

      case 'scarta': {
        const ids = (Array.isArray(d.immagini) ? d.immagini : []).filter((x) => ID.test(String(x))).slice(0, 20);
        if (ids.length) {
          const u = await usate(s);
          await Promise.allSettled(ids.filter((x) => !u.has(x)).map((x) => s.delete(`img/${x}`)));
        }
        return json(200, { ok: true });
      }

      default:
        return json(400, { ok: false, errore: 'azione' });
    }
  } catch (e) {
    console.error('swipe', d.azione, e);
    return json(500, { ok: false, errore: 'interno' });
  }
};
