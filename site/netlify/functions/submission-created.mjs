// Netlify la esegue da sola a ogni invio verificato di Netlify Forms (evento "submission-created").
// Gli invii fatti dal sito passano già da functions/invio.mjs (campo inviato=funzione): qui si saltano,
// così la notifica non arriva due volte. Resta per gli invii che arrivano solo da Netlify Forms.
// 1. salva o aggiorna il contatto su Brevo, nella lista del modulo;
// 2. manda a NOTIFY_EMAIL una email con tutti i campi, tramite Brevo.
//
// Variabili d'ambiente (Netlify → Site configuration → Environment variables):
//   BREVO_API_KEY            obbligatoria
//   NOTIFY_EMAIL             chi riceve le notifiche (più indirizzi separati da virgola)
//   BREVO_SENDER_EMAIL       mittente verificato su Brevo (es. consulting@francescoastolfi.net)
//   BREVO_LIST_DEFAULT       id della lista unica in cui finiscono tutti i contatti
//   BREVO_LIST_CANDIDATURA, BREVO_LIST_REVISIONE, BREVO_LIST_TEST, BREVO_LIST_BONUS
//                            facoltative: una lista diversa per modulo (prevalgono su quella unica)
//   BREVO_ATTRIBUTES         attributi personalizzati da compilare, creati prima su Brevo come testo:
//                            "FONTE" (consigliato: il modulo di provenienza), oppure un elenco separato
//                            da virgole tra STRUTTURA, SITO, CAMERE, CONCORRENTI, PROFILO, PUNTEGGIO,
//                            FONTE, PAGINA, TIPOLOGIA, PREZZO, CANALI, UNICITA, oppure "1" per tutti

import { FORMS, brevo, saveContact, notification } from '../lib/brevo.mjs';

export const handler = async (event) => {
  const { payload } = JSON.parse(event.body || '{}');
  const formName = payload?.form_name || payload?.data?.['form-name'];
  const form = FORMS[formName];
  if (!form) return { statusCode: 200, body: 'form ignorato' };
  const d = payload.data || {};
  if (d.inviato === 'funzione') return { statusCode: 200, body: 'già gestito da invio' };

  if (!process.env.BREVO_API_KEY) {
    console.error('BREVO_API_KEY mancante: invio salvato solo su Netlify Forms');
    return { statusCode: 200, body: 'brevo non configurato' };
  }

  const jobs = [];
  if (d.email) jobs.push(saveContact(d, formName, form));
  if (process.env.NOTIFY_EMAIL && process.env.BREVO_SENDER_EMAIL) jobs.push(brevo('/smtp/email', notification(d, form)));

  const results = await Promise.allSettled(jobs);
  results.filter((r) => r.status === 'rejected').forEach((r) => console.error(r.reason));
  // 200 comunque: l'invio resta in Netlify Forms anche se Brevo non risponde
  return { statusCode: 200, body: 'ok' };
};
