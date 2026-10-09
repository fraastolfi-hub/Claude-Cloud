// Riceve i moduli del sito (POST, application/x-www-form-urlencoded), salva il contatto su Brevo
// e manda la notifica email. Risponde 200 solo se la notifica è partita: altrimenti la pagina
// mostra l'errore, invece di far credere a chi compila che la richiesta sia arrivata.
//
// GET /.netlify/functions/invio  → controllo della configurazione (solo sì/no, nessun valore segreto).
//
// Variabili d'ambiente (Netlify → Project configuration → Environment variables):
//   BREVO_API_KEY, NOTIFY_EMAIL, BREVO_SENDER_EMAIL   obbligatorie per la notifica
//   BREVO_LIST_DEFAULT, BREVO_LIST_*, BREVO_ATTRIBUTES facoltative (vedi lib/brevo.mjs)

import { FORMS, brevo, contact, notification } from '../lib/brevo.mjs';

const json = (statusCode, body) => ({ statusCode, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }, body: JSON.stringify(body) });

export const handler = async (event) => {
  const env = process.env;
  if (event.httpMethod === 'GET') {
    return json(200, {
      BREVO_API_KEY: !!env.BREVO_API_KEY, NOTIFY_EMAIL: !!env.NOTIFY_EMAIL, BREVO_SENDER_EMAIL: !!env.BREVO_SENDER_EMAIL,
      BREVO_LIST_DEFAULT: !!env.BREVO_LIST_DEFAULT, BREVO_LIST_REVISIONE: !!env.BREVO_LIST_REVISIONE,
    });
  }
  if (event.httpMethod !== 'POST') return json(405, { ok: false });

  const raw = event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '');
  const d = Object.fromEntries(new URLSearchParams(raw));
  if (d['bot-field']) return json(200, { ok: true }); // trappola per i bot: si finge l'invio
  const form = FORMS[d['form-name']];
  if (!form) return json(400, { ok: false, errore: 'modulo sconosciuto' });
  if (!d.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(d.email)) return json(400, { ok: false, errore: 'email' });
  if (!env.BREVO_API_KEY || !env.NOTIFY_EMAIL || !env.BREVO_SENDER_EMAIL) {
    console.error('Configurazione Brevo incompleta: impossibile mandare la notifica', d['form-name'], d.email);
    return json(503, { ok: false, errore: 'configurazione' });
  }

  const [saved, mailed] = await Promise.allSettled([
    brevo('/contacts', contact(d, d['form-name'], form)),
    brevo('/smtp/email', notification(d, form)),
  ]);
  if (saved.status === 'rejected') console.error(saved.reason);
  if (mailed.status === 'rejected') { console.error(mailed.reason); return json(502, { ok: false, errore: 'notifica' }); }
  return json(200, { ok: true, contatto: saved.status === 'fulfilled' });
};
