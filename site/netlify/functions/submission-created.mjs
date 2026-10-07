// Netlify la esegue da sola a ogni invio verificato di Netlify Forms (evento "submission-created").
// 1. salva o aggiorna il contatto su Brevo, nella lista del modulo;
// 2. manda a NOTIFY_EMAIL una email con tutti i campi, tramite Brevo.
//
// Variabili d'ambiente (Netlify → Site configuration → Environment variables):
//   BREVO_API_KEY            obbligatoria
//   NOTIFY_EMAIL             chi riceve le notifiche (più indirizzi separati da virgola)
//   BREVO_SENDER_EMAIL       mittente verificato su Brevo (es. noreply@hotelpositioning.com)
//   BREVO_LIST_CANDIDATURA, BREVO_LIST_REVISIONE, BREVO_LIST_TEST, BREVO_LIST_BONUS
//                            id numerici delle liste Brevo; BREVO_LIST_DEFAULT se una manca
//   BREVO_ATTRIBUTES=1       manda anche gli attributi personalizzati (vanno creati prima su Brevo:
//                            STRUTTURA, SITO, CAMERE, CONCORRENTI, PROFILO, PUNTEGGIO, FONTE, PAGINA)

const API = 'https://api.brevo.com/v3';

const FORMS = {
  'candidatura': { label: 'Candidatura', list: 'BREVO_LIST_CANDIDATURA' },
  'revisione-homepage': { label: 'Revisione della homepage', list: 'BREVO_LIST_REVISIONE' },
  'test-posizionamento': { label: 'Test di posizionamento', list: 'BREVO_LIST_TEST' },
  'strumenti-libro': { label: 'Strumenti del libro', list: 'BREVO_LIST_BONUS' },
};

// etichette leggibili per l'email di notifica
const LABELS = {
  nome: 'Nome', nome_ruolo: 'Nome e ruolo', email: 'Email', telefono: 'Telefono',
  hotel: 'Struttura', struttura: 'Struttura', sito: 'Sito', url: 'Homepage', camere: 'Camere',
  concorrenti: 'Concorrenti', pubblicazione: 'Pubblicazione', riga: 'Prima riga della homepage',
  profilo: 'Profilo del test', punteggio: 'Punteggio', pagina: 'Pagina', privacy: 'Privacy',
};
const SKIP = new Set(['form-name', 'bot-field', 'ip', 'user_agent', 'referrer']);

const esc = (v) => String(v ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

async function brevo(path, body) {
  const r = await fetch(API + path, {
    method: 'POST',
    headers: { 'api-key': process.env.BREVO_API_KEY, 'content-type': 'application/json', accept: 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`Brevo ${path} ${r.status}: ${await r.text()}`);
  return r.status === 204 ? null : r.json().catch(() => null);
}

function contact(d, formName, form) {
  const full = (d.nome || d.nome_ruolo || '').trim();
  const [first, ...rest] = full.split(/\s+/);
  const attributes = { FIRSTNAME: first || '', LASTNAME: rest.join(' ') };
  if (process.env.BREVO_ATTRIBUTES === '1') {
    Object.assign(attributes, {
      STRUTTURA: d.hotel || d.struttura || '', SITO: d.sito || d.url || '', CAMERE: d.camere || '',
      CONCORRENTI: d.concorrenti || '', PROFILO: d.profilo || '', PUNTEGGIO: d.punteggio || '',
      FONTE: form.label, PAGINA: d.pagina || '',
    });
  }
  for (const k of Object.keys(attributes)) if (attributes[k] === '') delete attributes[k];
  const id = Number(process.env[form.list] || process.env.BREVO_LIST_DEFAULT);
  return { email: d.email, attributes, updateEnabled: true, ...(id ? { listIds: [id] } : {}) };
}

function notification(d, form) {
  const rows = Object.entries(d)
    .filter(([k, v]) => !SKIP.has(k) && v !== '' && v != null)
    .map(([k, v]) => `<tr><td style="padding:6px 14px 6px 0;color:#6E6E73;vertical-align:top">${esc(LABELS[k] || k)}</td><td style="padding:6px 0">${esc(v)}</td></tr>`)
    .join('');
  const who = d.hotel || d.struttura || d.email;
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Hotel Positioning' },
    to: process.env.NOTIFY_EMAIL.split(',').map((e) => ({ email: e.trim() })).filter((x) => x.email),
    ...(d.email ? { replyTo: { email: d.email, ...(d.nome ? { name: d.nome } : {}) } } : {}),
    subject: `${form.label}: ${who}`,
    htmlContent: `<div style="font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif;color:#1D1D1F"><p style="font-size:18px;font-weight:600;margin:0 0 14px">${esc(form.label)}</p><table style="border-collapse:collapse">${rows}</table></div>`,
  };
}

export const handler = async (event) => {
  const { payload } = JSON.parse(event.body || '{}');
  const formName = payload?.form_name || payload?.data?.['form-name'];
  const form = FORMS[formName];
  if (!form) return { statusCode: 200, body: 'form ignorato' };
  const d = payload.data || {};

  if (!process.env.BREVO_API_KEY) {
    console.error('BREVO_API_KEY mancante: invio salvato solo su Netlify Forms');
    return { statusCode: 200, body: 'brevo non configurato' };
  }

  const jobs = [];
  if (d.email) jobs.push(brevo('/contacts', contact(d, formName, form)));
  if (process.env.NOTIFY_EMAIL && process.env.BREVO_SENDER_EMAIL) jobs.push(brevo('/smtp/email', notification(d, form)));

  const results = await Promise.allSettled(jobs);
  results.filter((r) => r.status === 'rejected').forEach((r) => console.error(r.reason));
  // 200 comunque: l'invio resta in Netlify Forms anche se Brevo non risponde
  return { statusCode: 200, body: 'ok' };
};
