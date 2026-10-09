// Codice comune alle funzioni dei moduli: contatto su Brevo e email di notifica.
// Le variabili d'ambiente sono descritte in functions/invio.mjs.

export const API = 'https://api.brevo.com/v3';

export const FORMS = {
  'candidatura': { label: 'Richiesta analisi (vecchio modulo)', list: 'BREVO_LIST_CANDIDATURA' },
  'revisione-homepage': { label: 'Smontaggio della homepage', list: 'BREVO_LIST_REVISIONE' },
  'test-posizionamento': { label: 'Test di posizionamento', list: 'BREVO_LIST_TEST' },
  'strumenti-libro': { label: 'Strumenti del libro', list: 'BREVO_LIST_BONUS' },
  'questionario': { label: 'Questionario di posizionamento', list: 'BREVO_LIST_QUESTIONARIO' },
};

// etichette leggibili per l'email di notifica
export const LABELS = {
  nome: 'Nome', nome_ruolo: 'Nome e ruolo', email: 'Email', telefono: 'Telefono',
  hotel: 'Struttura', struttura: 'Struttura', sito: 'Sito', url: 'Homepage', camere: 'Camere',
  concorrenti: 'Concorrenti', tipologia: 'Tipologia', prezzo: 'Prezzo medio a notte', canali: 'Canali di prenotazione', unicita: 'Unicità più importante', pubblicazione: 'Pubblicazione', riga: "Cosa vorrebbe che l'ospite capisse",
  profilo: 'Profilo del test', punteggio: 'Punteggio', pagina: 'Pagina', privacy: 'Privacy',
  // questionario dell'analisi completa
  nome_localita: 'Nome e località', numero_camere: 'Numero camere', stagionalita: 'Stagionalità', adr: 'ADR (€)',
  sito_web: 'Sito web', canali_prenotazione: 'Canali di prenotazione', quota_dirette: '% dirette', quota_ota: '% OTA',
  descrizione_frase: 'Descrizione in una frase', perche_noi: 'Perché voi', promessa: 'Promessa',
  cosa_offrono_loro: 'Cosa offrono loro', alternativa_sparizione: 'Alternativa se sparisse',
  ospite_che_torna: "L'ospite che torna", occasione: 'Occasione', vita_prima_di_prenotare: 'Il giorno prima di prenotare',
  difficile_copiare: 'Difficile da copiare', sorpresa_positiva: 'Sorpresa positiva', cosa_non_diamo: 'Cosa non diamo',
  cosa_rifiuti: 'Cosa rifiuta', unico_ospite: 'Un solo tipo di ospite', fastidio_competitor: 'Fastidio nella comunicazione degli altri',
  obiettivo_12_mesi: 'Obiettivo a 12 mesi', chi_comunica: 'Chi comunica, con che tono',
  link_tripadvisor: 'Recensioni TripAdvisor', link_booking: 'Recensioni Booking', link_google: 'Recensioni Google',
  note_materiali: 'Note e materiali', nome_referente: 'Referente',
};
export const SKIP = new Set(['form-name', 'bot-field', 'ip', 'user_agent', 'referrer', 'inviato']);

export const esc = (v) => String(v ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));

export async function brevo(path, body) {
  const r = await fetch(API + path, {
    method: 'POST',
    headers: { 'api-key': process.env.BREVO_API_KEY, 'content-type': 'application/json', accept: 'application/json' },
    body: JSON.stringify(body),
  });
  if (!r.ok) throw new Error(`Brevo ${path} ${r.status}: ${await r.text()}`);
  return r.status === 204 ? null : r.json().catch(() => null);
}

export function contact(d, formName, form) {
  const full = (d.nome || d.nome_ruolo || d.nome_referente || '').trim();
  const [first, ...rest] = full.split(/\s+/);
  // su questo account Brevo nome e cognome si chiamano NOME e COGNOME (non FIRSTNAME/LASTNAME)
  const attributes = { NOME: first || '', COGNOME: rest.join(' ') };
  const extra = {
    STRUTTURA: d.hotel || d.struttura || d.nome_localita || '', SITO: d.sito || d.url || d.sito_web || '', CAMERE: d.camere || d.numero_camere || '',
    CONCORRENTI: d.concorrenti || '', PROFILO: d.profilo || '', PUNTEGGIO: d.punteggio || '',
    FONTE: form.label, PAGINA: d.pagina || '',
    TIPOLOGIA: d.tipologia || '', PREZZO: d.prezzo || '', CANALI: d.canali || '', UNICITA: d.unicita || '',
  };
  const want = (process.env.BREVO_ATTRIBUTES || '').trim();
  const keys = want === '1' ? Object.keys(extra) : want.split(',').map((k) => k.trim().toUpperCase()).filter((k) => k in extra);
  for (const k of keys) attributes[k] = extra[k];
  for (const k of Object.keys(attributes)) if (attributes[k] === '') delete attributes[k];
  const id = Number(process.env[form.list] || process.env.BREVO_LIST_DEFAULT);
  return { email: d.email, attributes, updateEnabled: true, ...(id ? { listIds: [id] } : {}) };
}

export function notification(d, form) {
  const rows = Object.entries(d)
    .filter(([k, v]) => !SKIP.has(k) && v !== '' && v != null)
    .map(([k, v]) => `<tr><td style="padding:6px 14px 6px 0;color:#6E6E73;vertical-align:top">${esc(LABELS[k] || k)}</td><td style="padding:6px 0">${esc(v)}</td></tr>`)
    .join('');
  const who = d.hotel || d.struttura || d.nome_localita || d.email;
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Hotel Positioning' },
    to: process.env.NOTIFY_EMAIL.split(',').map((e) => ({ email: e.trim() })).filter((x) => x.email),
    ...(d.email ? { replyTo: { email: d.email, ...((d.nome || d.nome_referente) ? { name: d.nome || d.nome_referente } : {}) } } : {}),
    subject: `${form.label}: ${who}`,
    htmlContent: `<div style="font:15px/1.5 -apple-system,Helvetica,Arial,sans-serif;color:#1D1D1F"><p style="font-size:18px;font-weight:600;margin:0 0 14px">${esc(form.label)}</p><table style="border-collapse:collapse">${rows}</table></div>`,
  };
}

// Salva il contatto. Se Brevo rifiuta un attributo o la lista, riprova con meno dati:
// meglio un contatto con la sola email che nessun contatto.
export async function saveContact(d, formName, form) {
  const full = contact(d, formName, form);
  const tries = [full, { email: full.email, updateEnabled: true, attributes: { FONTE: form.label }, ...(full.listIds ? { listIds: full.listIds } : {}) }, { email: full.email, updateEnabled: true }];
  let last;
  for (const body of tries) {
    try { return await brevo('/contacts', body); } catch (e) { last = e; console.error('contatto non salvato, riprovo con meno dati:', e.message); }
  }
  throw last;
}

// Mail di conferma a chi richiede lo smontaggio. Testo approvato da Francesco il 9 ottobre 2026.
// Versione /hday: in più il paragrafo sull'offerta dell'Hospitality Day.
export function confirmation(d) {
  const nome = ((d.nome_ruolo || d.nome || '').split(',')[0].trim().split(/\s+/)[0]) || '';
  const hotel = (d.hotel || '').trim() || 'il tuo hotel';
  const hday = /\/hday/.test(d.pagina || '');
  const p = [
    `Ciao${nome ? ' ' + nome : ''},`,
    `ho ricevuto la richiesta di smontaggio per ${hotel}.`,
    'Nei prossimi 3 giorni lavorativi metto la prima riga della tua homepage accanto a quella dei concorrenti che mi hai indicato, con il logo coperto. Ti mando una pagina con il verdetto (posizionato, sostituibile o invisibile) e un indizio su dove cercare il tuo motivo.',
    'Nel frattempo prova tu: copri il logo sulla tua homepage e su quella di un concorrente, e leggi le due prime frasi. Se si possono scambiare, sai già da dove partiamo.',
    'Nessuna telefonata. Se hai qualcosa da aggiungere, rispondi a questa mail.',
  ];
  if (hday) p.push("Ci siamo visti all'Hospitality Day: con lo smontaggio ti mando anche il link per l'analisi completa a €697 + IVA invece di €2.500. Vale fino al 31 ottobre, se dopo il verdetto vuoi andare avanti.");
  const firma = ['Francesco Astolfi', 'Hotel Positioning'];
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    to: [{ email: d.email, ...(nome ? { name: nome } : {}) }],
    replyTo: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    subject: `Ho ricevuto la tua richiesta${nome ? ', ' + nome : ''}`,
    textContent: p.join('\n\n') + '\n\n' + firma.join('\n'),
    htmlContent: `<div style="font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;color:#0a0a0a;max-width:560px">${p.map((x) => `<p style="margin:0 0 14px">${esc(x)}</p>`).join('')}<p style="margin:22px 0 0">${firma.map(esc).join('<br>')}</p></div>`,
  };
}
