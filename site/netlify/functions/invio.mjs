// Riceve i moduli del sito (POST, application/x-www-form-urlencoded), salva il contatto su Brevo
// e manda la notifica email. Risponde 200 solo se la notifica è partita: altrimenti la pagina
// mostra l'errore, invece di far credere a chi compila che la richiesta sia arrivata.
//
// GET /.netlify/functions/invio  → controllo della configurazione (solo sì/no, nessun valore segreto).
//
// Variabili d'ambiente (Netlify → Project configuration → Environment variables):
//   BREVO_API_KEY, NOTIFY_EMAIL, BREVO_SENDER_EMAIL   obbligatorie per la notifica
//   BREVO_LIST_DEFAULT, BREVO_LIST_*, BREVO_ATTRIBUTES facoltative (vedi lib/brevo.mjs)
//   BREVO_LIST_CASSETTA, BREVO_LIST_CASSETTA_SEQUENZA   liste della campagna /cassetta/ (la seconda: chi ha dato il consenso alle mail successive)
//   META_PIXEL_ID, META_CAPI_TOKEN, META_TEST_EVENT_CODE  Conversions API di Meta per l'evento Lead (facoltative)

import { FORMS, brevo, saveContact, notification, confirmation, bonusMail, cassettaMail, guidaMail, metaLead } from '../lib/brevo.mjs';

const json = (statusCode, body) => ({ statusCode, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }, body: JSON.stringify(body) });

export const handler = async (event) => {
  const env = process.env;
  if (event.httpMethod === 'GET') {
    return json(200, {
      BREVO_API_KEY: !!env.BREVO_API_KEY, NOTIFY_EMAIL: !!env.NOTIFY_EMAIL, BREVO_SENDER_EMAIL: !!env.BREVO_SENDER_EMAIL,
      BREVO_LIST_DEFAULT: !!env.BREVO_LIST_DEFAULT, BREVO_LIST_REVISIONE: !!env.BREVO_LIST_REVISIONE,
      BREVO_LIST_CASSETTA: !!env.BREVO_LIST_CASSETTA, BREVO_LIST_CASSETTA_SEQUENZA: !!env.BREVO_LIST_CASSETTA_SEQUENZA,
      BREVO_LIST_GUIDA: !!env.BREVO_LIST_GUIDA, BREVO_LIST_GUIDA_SEQUENZA: !!env.BREVO_LIST_GUIDA_SEQUENZA,
      META_PIXEL_ID: !!env.META_PIXEL_ID, META_CAPI_TOKEN: !!env.META_CAPI_TOKEN, META_TEST_EVENT_CODE: !!env.META_TEST_EVENT_CODE,
      META_PIXEL_ID_UGUALE_A_GTM: env.META_PIXEL_ID === '28889512877380364',
    });
  }
  if (event.httpMethod !== 'POST') return json(405, { ok: false });

  console.log('invio ricevuto', event.httpMethod);
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

  const [saved, mailed, meta] = await Promise.allSettled([
    saveContact(d, d['form-name'], form),
    brevo('/smtp/email', notification(d, form)),
    ['cassetta', 'guida'].includes(d['form-name']) ? metaLead(d, event.headers || {}) : Promise.resolve('non serve'),
  ]);
  // esito della Conversions API: nei log della funzione e nella risposta (visibile in Network, senza dati riservati)
  const metaEsito = meta.status === 'fulfilled' ? meta.value : 'errore: ' + (meta.reason?.message || meta.reason);
  if (['cassetta', 'guida'].includes(d['form-name'])) console.log('Meta CAPI:', metaEsito);
  if (saved.status === 'rejected') console.error(saved.reason);
  if (mailed.status === 'rejected') { console.error(mailed.reason); return json(502, { ok: false, errore: 'notifica' }); }
  // conferma a chi ha compilato: solo per lo smontaggio; se non parte, la richiesta resta valida
  const reply = d['form-name'] === 'revisione-homepage' ? confirmation(d) : d['form-name'] === 'strumenti-libro' ? bonusMail(d) : d['form-name'] === 'cassetta' ? cassettaMail(d) : d['form-name'] === 'guida' ? guidaMail(d) : null;
  if (reply) {
    try { await brevo('/smtp/email', reply); console.log('conferma inviata'); } catch (e) { console.error('conferma non inviata:', e.message); }
  }
  console.log('notifica inviata', d['form-name'], 'contatto salvato:', saved.status === 'fulfilled');
  return json(200, { ok: true, contatto: saved.status === 'fulfilled', ...(['cassetta', 'guida'].includes(d['form-name']) ? { meta: metaEsito } : {}) });
};
