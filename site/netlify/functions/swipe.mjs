// Swipe file (/swipe-file/). Dati e screenshot in Netlify Blobs, vedi ../lib/swipe.mjs.
//
// Pubblico, senza chiave:
//   GET  ?elenco=1                      → { esempi[] } solo quelli pubblicati, con il conteggio dei cuori
//   POST { azione: 'cuore', id, valore: 1 | -1 } → { cuori } preferito di un visitatore (senza chiave; il browser ricorda i suoi)
//   POST { azione: 'segnala', url?, nota?, nome?, email?, tipo?, dati? } → { ok } un visitatore manda un'idea (link o foto): entra in coda «da valutare»; nome → credito pubblico
//   GET  ?img=<id>                      → lo screenshot (id casuale non indovinabile)
//   GET  ?trad=<id>                     → { pronto, testo } traduzione italiana del copy, se già fatta
//   GET  ?lavoro=<jobid>                → { pronto, ok, testo | errore } risultato di swipe-idea-background
// Con la chiave:
//   GET  ?analisi=<id>&chiave=…         → { pronto, ok, proposta | errore } dell'analisi in background
//   POST { azione, chiave, … }:
//        verifica                       → { ok }
//        elenco                         → { esempi[] } tutti, anche quelli da valutare
//        carica { tipo, dati(base64) }  → { id } dello screenshot
//        salva { esempio, rimosse[] }   → { esempio }   (esempio.stato: 'pubblicato' | 'da_valutare')
//        stato { id, stato }            → { esempio }   pubblica o rimette in coda
//        elimina { id }                 → { ok }
//        copertina { id, off? }         → { esempio }   mette l'idea in copertina (una sola) o la toglie
//        focale { id, focale:{x,y} }    → { esempio }   punto focale del primo screenshot (calcolato da swipe-radar/copertina.py)
//        scarta { immagini[] }          → { ok }        screenshot caricati e poi non salvati
//        candidato { esempio, chiave_radar, immagini[], immagini_url[] } → { ok, id } | { ok, duplicato: true }
//        visto { chiave_radar }         → { visto } (il radar controlla prima di fare lo screenshot)
//            usato dal radar: scarica le immagini dagli URL, salva in coda «da valutare» e ricorda la chiave_radar
//            (URL dell'inserzione, della pagina o id dell'email) per non riproporre lo stesso pezzo.
// L'analisi con Claude parte da swipe-analisi-background.mjs (dura più dei 10 secondi di una funzione normale).
import { createHash, randomUUID } from 'node:crypto';
import { connectLambda } from '@netlify/blobs';
import { ID, TIPI, autorizzato, json, leggiCorpo, store, testo } from '../lib/swipe.mjs';

const MAX_IMG = 4.4 * 1024 * 1024;
const STATI = ['pubblicato', 'da_valutare'];
const FONTI = ['manuale', 'meta', 'email', 'sito', 'landing', 'segnalazione'];
const statoDi = (e) => (e?.stato === 'da_valutare' ? 'da_valutare' : 'pubblicato');

async function tutti(s) {
  const { blobs } = await s.list({ prefix: 'esempi/' });
  const out = [];
  for (let i = 0; i < blobs.length; i += 25) {
    const parte = await Promise.all(blobs.slice(i, i + 25).map((b) => s.get(b.key, { type: 'json' })));
    out.push(...parte.filter(Boolean));
  }
  return out.map((e) => ({ ...e, stato: statoDi(e) })).sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)));
}

const pubblico = ({ chiave_radar, segnalazione, ...e }) => e;

// {x,y} tra 0 e 1, calcolato da swipe-radar/copertina.py (zona con più testo del primo screenshot); null se non ancora calcolato
function focaleDi(f) {
  if (!f || typeof f !== 'object') return null;
  const x = Number(f.x), y = Number(f.y);
  if (!Number.isFinite(x) || !Number.isFinite(y)) return null;
  return { x: Math.round(Math.max(0, Math.min(1, x)) * 1000) / 1000, y: Math.round(Math.max(0, Math.min(1, y)) * 1000) / 1000 };
}

// cuori dei visitatori: un solo blob { id: conteggio }
async function cuori(s) {
  return (await s.get('cuori', { type: 'json' })) || {};
}

function normalizza(e, esistente) {
  const ora = new Date().toISOString();
  return {
    id: esistente?.id || randomUUID(),
    created_at: esistente?.created_at || ora,
    updated_at: ora,
    stato: STATI.includes(e.stato) ? e.stato : statoDi(esistente),
    fonte: FONTI.includes(e.fonte) ? e.fonte : (esistente?.fonte || 'manuale'),
    title: testo(e.title, 200).trim(),
    brand: testo(e.brand, 120).trim(),
    url: testo(e.url, 1000).trim(),
    copy: testo(e.copy, 20000),
    why: testo(e.why, 8000),
    steal: testo(e.steal, 8000),
    rating: Math.max(0, Math.min(5, Math.round(Number(e.rating) || 0))),
    tags: [...new Set((Array.isArray(e.tags) ? e.tags : []).filter((t) => typeof t === 'string' && t.includes(':')).map((t) => t.slice(0, 120)))].slice(0, 80),
    images: (Array.isArray(e.images) ? e.images : []).filter((x) => ID.test(String(x))).slice(0, 20),
    credito: testo(e.credito ?? esistente?.credito, 120).trim(), // chi l'ha segnalata («Segnalata da Marta, Rimini»), visibile a tutti
    copertina: !!(e.copertina ?? esistente?.copertina), // l'idea in testa alla pagina (una sola): la sceglie Francesco
    focale: focaleDi(e.focale ?? esistente?.focale), // punto focale del primo screenshot {x,y} in frazioni: dove ritagliare la copertina e le miniature
    ...(esistente?.chiave_radar ? { chiave_radar: esistente.chiave_radar } : {}),
    ...(esistente?.segnalazione ? { segnalazione: esistente.segnalazione } : {}),
  };
}

// Scarica un'immagine per il radar: solo https verso nomi di dominio pubblici, solo immagini, al massimo 4,4 MB.
async function scarica(url) {
  let u;
  try { u = new URL(url); } catch { return null; }
  if (u.protocol !== 'https:' || /^(localhost|.*\.local|.*\.internal|\d+\.\d+\.\d+\.\d+|\[.*\])$/i.test(u.hostname)) return null;
  const r = await fetch(u, { redirect: 'follow', signal: AbortSignal.timeout(8000) }).catch(() => null);
  if (!r?.ok) return null;
  const tipo = (r.headers.get('content-type') || '').split(';')[0].trim();
  if (!TIPI[tipo]) return null;
  const buf = Buffer.from(await r.arrayBuffer());
  if (!buf.length || buf.length > MAX_IMG) return null;
  return { buf, tipo };
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
        headers: { 'content-type': r.metadata?.tipo || 'image/jpeg', 'cache-control': 'public, max-age=31536000, immutable' },
        body: Buffer.from(r.data).toString('base64'),
        isBase64Encoded: true,
      };
    }
    if (q.elenco) {
      const c = await cuori(s);
      const esempi = (await tutti(s)).filter((e) => e.stato === 'pubblicato').map((e) => ({ ...pubblico(e), cuori: c[e.id] || 0 }));
      return { ...json(200, { ok: true, esempi }), headers: { 'content-type': 'application/json', 'cache-control': 'public, max-age=0, must-revalidate', 'netlify-cdn-cache-control': 'public, max-age=60, stale-while-revalidate=300' } };
    }
    if (q.trad) {
      if (!ID.test(q.trad)) return json(400, { ok: false, errore: 'richiesta' });
      const t = await s.get(`trad/${q.trad}`);
      return json(200, t ? { pronto: true, testo: t } : { pronto: false });
    }
    if (q.lavoro) {
      if (!ID.test(q.lavoro)) return json(400, { ok: false, errore: 'richiesta' });
      const r = await s.get(`lavori/${q.lavoro}`, { type: 'json' });
      return json(200, r ? { pronto: true, ...r } : { pronto: false });
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

  if (d.azione === 'cuore') {
    if (!ID.test(String(d.id || '')) || ![1, -1].includes(d.valore)) return json(400, { ok: false, errore: 'richiesta' });
    const e = await s.get(`esempi/${d.id}`, { type: 'json' });
    if (!e || statoDi(e) !== 'pubblicato') return json(404, { ok: false, errore: 'non_trovato' });
    const c = await cuori(s);
    c[d.id] = Math.max(0, (c[d.id] || 0) + d.valore);
    if (!c[d.id]) delete c[d.id];
    await s.setJSON('cuori', c);
    return json(200, { ok: true, cuori: c[d.id] || 0 });
  }

  if (d.azione === 'segnala') {
    if (d['bot-field']) return json(200, { ok: true });
    const url = testo(d.url, 1000).trim();
    const nota = testo(d.nota, 2000).trim();
    let img = null;
    if (d.dati && TIPI[d.tipo]) {
      const buf = Buffer.from(String(d.dati), 'base64');
      if (buf.length > 3.2 * 1024 * 1024) return json(413, { ok: false, errore: 'immagine_grande' });
      if (buf.length) img = { buf, tipo: d.tipo };
    }
    if (!/^https?:\/\/\S+\.\S+/i.test(url) && !img) return json(400, { ok: false, errore: 'serve_link_o_immagine' });
    const images = [];
    if (img) { const id = randomUUID(); await s.set(`img/${id}`, img.buf, { metadata: { tipo: img.tipo } }); images.push(id); }
    let host = '';
    try { host = url ? new URL(url).hostname.replace(/^www\./, '') : ''; } catch { /* url non valido: resta vuoto */ }
    const nome = testo(d.nome, 120).trim();
    const riga = normalizza({ stato: 'da_valutare', fonte: 'segnalazione', title: host ? `Segnalazione: ${host}` : 'Segnalazione con foto', url, why: nota, images, credito: nome }, null);
    riga.segnalazione = { nome, email: testo(d.email, 200).trim(), nota, quando: riga.created_at };
    await s.setJSON(`esempi/${riga.id}`, riga);
    return json(200, { ok: true });
  }

  if (!autorizzato(d.chiave)) return json(401, { ok: false, errore: 'chiave_errata' });

  try {
    switch (d.azione) {
      case 'verifica':
        return json(200, { ok: true });

      case 'elenco': {
        const c = await cuori(s);
        return json(200, { ok: true, esempi: (await tutti(s)).map((e) => ({ ...e, cuori: c[e.id] || 0 })) });
      }

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
        const riga = normalizza(e, esistente);
        if (!riga.title && !riga.copy.trim() && !riga.images.length) return json(400, { ok: false, errore: 'vuoto' });
        await s.setJSON(`esempi/${riga.id}`, riga);
        const rimosse = (Array.isArray(d.rimosse) ? d.rimosse : []).filter((x) => ID.test(String(x)) && !riga.images.includes(x));
        await Promise.allSettled(rimosse.map((x) => s.delete(`img/${x}`)));
        return json(200, { ok: true, esempio: riga });
      }

      case 'stato': {
        if (!ID.test(String(d.id || '')) || !STATI.includes(d.stato)) return json(400, { ok: false, errore: 'richiesta' });
        const e = await s.get(`esempi/${d.id}`, { type: 'json' });
        if (!e) return json(404, { ok: false, errore: 'non_trovato' });
        const riga = { ...e, stato: d.stato, updated_at: new Date().toISOString() };
        await s.setJSON(`esempi/${d.id}`, riga);
        return json(200, { ok: true, esempio: riga });
      }

      case 'copertina': {
        // una sola idea in copertina: metterla su una la toglie dalle altre; { id, off: true } la toglie e basta
        if (!ID.test(String(d.id || ''))) return json(400, { ok: false, errore: 'richiesta' });
        const e = await s.get(`esempi/${d.id}`, { type: 'json' });
        if (!e) return json(404, { ok: false, errore: 'non_trovato' });
        const ora = new Date().toISOString();
        if (!d.off) {
          for (const altro of (await tutti(s)).filter((x) => x.copertina && x.id !== d.id)) await s.setJSON(`esempi/${altro.id}`, { ...altro, copertina: false, updated_at: ora });
        }
        const riga = { ...e, copertina: !d.off, updated_at: ora };
        await s.setJSON(`esempi/${d.id}`, riga);
        return json(200, { ok: true, esempio: riga });
      }

      case 'focale': {
        // salva il punto focale calcolato dallo script, senza toccare il resto della scheda
        if (!ID.test(String(d.id || ''))) return json(400, { ok: false, errore: 'richiesta' });
        const e = await s.get(`esempi/${d.id}`, { type: 'json' });
        if (!e) return json(404, { ok: false, errore: 'non_trovato' });
        const riga = { ...e, focale: focaleDi(d.focale), updated_at: new Date().toISOString() };
        await s.setJSON(`esempi/${d.id}`, riga);
        return json(200, { ok: true, esempio: riga });
      }

      case 'elimina': {
        if (!ID.test(String(d.id || ''))) return json(400, { ok: false, errore: 'richiesta' });
        const e = await s.get(`esempi/${d.id}`, { type: 'json' });
        await s.delete(`esempi/${d.id}`);
        await Promise.allSettled((e?.images || []).map((x) => s.delete(`img/${x}`)));
        const c = await cuori(s);
        if (c[d.id]) { delete c[d.id]; await s.setJSON('cuori', c); }
        return json(200, { ok: true });
      }

      case 'scarta': {
        const ids = (Array.isArray(d.immagini) ? d.immagini : []).filter((x) => ID.test(String(x))).slice(0, 20);
        if (ids.length) {
          const usate = new Set((await tutti(s)).flatMap((e) => e.images || []));
          await Promise.allSettled(ids.filter((x) => !usate.has(x)).map((x) => s.delete(`img/${x}`)));
        }
        return json(200, { ok: true });
      }

      case 'visto': {
        const k = testo(d.chiave_radar, 1000).trim();
        if (!k) return json(400, { ok: false, errore: 'chiave_radar' });
        return json(200, { ok: true, visto: !!(await s.get(`visti/${createHash('sha256').update(k).digest('hex')}`)) });
      }

      case 'candidato': {
        const k = testo(d.chiave_radar, 1000).trim();
        if (!k) return json(400, { ok: false, errore: 'chiave_radar' });
        const visto = `visti/${createHash('sha256').update(k).digest('hex')}`;
        if (await s.get(visto)) return json(200, { ok: true, duplicato: true });
        // immagini già caricate con «carica» (screenshot fatti dal radar) + immagini da scaricare dagli URL
        const images = (Array.isArray(d.immagini) ? d.immagini : []).filter((x) => ID.test(String(x))).slice(0, 4);
        for (const url of (Array.isArray(d.immagini_url) ? d.immagini_url : []).slice(0, 4)) {
          const img = await scarica(String(url));
          if (!img) continue;
          const id = randomUUID();
          await s.set(`img/${id}`, img.buf, { metadata: { tipo: img.tipo } });
          images.push(id);
        }
        const riga = normalizza({ ...(d.esempio || {}), stato: 'da_valutare', images }, null);
        riga.chiave_radar = k;
        if (!riga.title && !riga.copy.trim() && !images.length) return json(400, { ok: false, errore: 'vuoto' });
        await s.setJSON(`esempi/${riga.id}`, riga);
        await s.set(visto, riga.id);
        return json(200, { ok: true, id: riga.id, immagini: images.length });
      }

      default:
        return json(400, { ok: false, errore: 'azione' });
    }
  } catch (e) {
    console.error('swipe', d.azione, e);
    return json(500, { ok: false, errore: 'interno' });
  }
};
