// Idee per il tuo hotel (/idee/): il lavoro lungo (lettura del sito, ricerca web, scelta delle idee) gira qui,
// in background: Netlify risponde subito 202 e la funzione può durare fino a 15 minuti.
// POST { id, url, email, privacy, consenso_email?, pagina? }
//   → il risultato finisce in Netlify Blobs, store «idee», chiave lavori/<id>; la pagina lo chiede a idee.mjs (GET ?id=…).
// Il contatto va su Brevo anche se il sito non si lascia leggere: Francesco riceve la notifica e può rispondere a mano.
import { connectLambda } from '@netlify/blobs';
import { FORMS, brevo, notification, saveContact } from '../lib/brevo.mjs';
import { ID, chiaveSito, dallaCache, dentroLimite, esegui, storeIdee } from '../lib/idee.mjs';

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const testo = (v, max) => (typeof v === 'string' ? v.slice(0, max).trim() : '');

export const handler = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405 };
  let d;
  try { d = JSON.parse(event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '{}')); } catch { return { statusCode: 400 }; }
  if (!ID.test(String(d.id || ''))) return { statusCode: 400 };
  connectLambda(event);
  const s = storeIdee();
  const fine = (r) => s.setJSON(`lavori/${d.id}`, r);

  const url = testo(d.url, 500);
  const email = testo(d.email, 200).toLowerCase();
  if (!url) { await fine({ ok: false, errore: 'url', messaggio: "Scrivi l'indirizzo del sito." }); return { statusCode: 200 }; }
  if (!EMAIL.test(email)) { await fine({ ok: false, errore: 'email', messaggio: "Controlla l'indirizzo email." }); return { statusCode: 200 }; }
  if (!d.privacy) { await fine({ ok: false, errore: 'privacy', messaggio: 'Serve il consenso alla privacy policy.' }); return { statusCode: 200 }; }

  const contatto = { email, url, consenso_email: d.consenso_email ? 'sì' : '', pagina: testo(d.pagina, 200) || '/idee/' };
  const form = FORMS.idee;
  if (process.env.BREVO_API_KEY) await saveContact(contatto, 'idee', form).catch((e) => console.error('idee: contatto non salvato', e.message));

  let r = await dallaCache(s, url);
  if (!r) {
    if (!(await dentroLimite(s, email))) {
      r = { ok: false, errore: 'limite', messaggio: 'Per oggi hai già chiesto tutte le idee possibili. Riprova domani, oppure rispondi alla mail di Francesco.' };
    } else {
      r = await esegui({ url });
      if (r.ok) await s.setJSON(`siti/${chiaveSito(url)}`, r);
    }
  }
  await fine(r);

  // notifica a Francesco: chi ha chiesto, per quale sito, quali idee sono uscite (o perché no)
  if (process.env.BREVO_API_KEY && process.env.NOTIFY_EMAIL) {
    const esito = r.ok ? (r.idee || []).map((i, n) => `${n + 1}. ${i.titolo}`).join(' · ') : `Non riuscito: ${r.messaggio || r.errore}${r.dettaglio ? ` (${r.dettaglio})` : ''}`;
    await brevo('/smtp/email', notification({ ...contatto, struttura: r.struttura || url, esito }, form)).catch((e) => console.error('idee: notifica non inviata', e.message));
  }
  return { statusCode: 200 };
};
