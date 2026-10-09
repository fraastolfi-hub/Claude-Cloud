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
