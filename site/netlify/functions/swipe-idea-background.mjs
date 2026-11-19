// Lavori con Claude lanciati dalla pagina pubblica /marketing-ideas/ (Netlify risponde subito 202).
// POST { jobid, tipo: 'traduci' | 'adatta', id, struttura?, email?, privacy?, pagina? }
//   traduci → traduzione italiana del copy di un'idea pubblicata; salvata in trad/<id> e riusata per tutti
//   adatta  → «Adattalo al mio hotel»: tre proposte per la struttura indicata; richiede email e consenso,
//             il contatto va su Brevo (modulo marketing-ideas); risposta in cache per (idea, struttura)
// Il risultato finisce in lavori/<jobid>; la pagina lo chiede a swipe.mjs (GET ?lavoro=<jobid>).
import { createHash } from 'node:crypto';
import { connectLambda } from '@netlify/blobs';
import { ID, adatta, leggiCorpo, store, testo, traduci } from '../lib/swipe.mjs';
import { FORMS, saveContact } from '../lib/brevo.mjs';

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405 };
  const d = leggiCorpo(event);
  if (!d || !ID.test(String(d.jobid || '')) || !ID.test(String(d.id || '')) || !['traduci', 'adatta'].includes(d.tipo)) return { statusCode: 400 };
  connectLambda(event);
  const s = store();
  const fine = async (r) => { await s.setJSON(`lavori/${d.jobid}`, r); return { statusCode: 200 }; };

  try {
    const e = await s.get(`esempi/${d.id}`, { type: 'json' });
    if (!e || e.stato === 'da_valutare') return fine({ ok: false, errore: 'non_trovato' });

    if (d.tipo === 'traduci') {
      const fatta = await s.get(`trad/${d.id}`);
      if (fatta) return fine({ ok: true, testo: fatta });
      if (!e.copy?.trim()) return fine({ ok: false, errore: 'vuoto' });
      const t = await traduci(e);
      await s.set(`trad/${d.id}`, t);
      return fine({ ok: true, testo: t });
    }

    // adatta
    const struttura = testo(d.struttura, 200).trim();
    const email = testo(d.email, 200).trim().toLowerCase();
    if (struttura.length < 4) return fine({ ok: false, errore: 'struttura' });
    if (!EMAIL.test(email)) return fine({ ok: false, errore: 'email' });
    if (!d.privacy) return fine({ ok: false, errore: 'privacy' });

    // il contatto si salva anche se Brevo non è configurato per questa lista (cade su BREVO_LIST_DEFAULT)
    if (process.env.BREVO_API_KEY) {
      saveContact({ email, struttura, pagina: testo(d.pagina, 200) || '/marketing-ideas/' }, 'marketing-ideas', FORMS['marketing-ideas'])
        .catch((err) => console.error('marketing-ideas contatto non salvato:', err.message));
    }

    const chiave = `adatta/${d.id}/${createHash('sha256').update(struttura.toLowerCase().replace(/\s+/g, ' ')).digest('hex').slice(0, 24)}`;
    const cache = await s.get(chiave);
    if (cache) return fine({ ok: true, testo: cache });
    const t = await adatta(e, struttura);
    await s.set(chiave, t);
    return fine({ ok: true, testo: t });
  } catch (err) {
    console.error('swipe-idea', d.tipo, err);
    await fine({ ok: false, errore: err?.status === 429 ? 'troppe_richieste' : 'interno' });
  }
  return { statusCode: 200 };
};
