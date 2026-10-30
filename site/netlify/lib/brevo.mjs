// Codice comune alle funzioni dei moduli: contatto su Brevo e email di notifica.
// Le variabili d'ambiente sono descritte in functions/invio.mjs.

export const API = 'https://api.brevo.com/v3';

export const FORMS = {
  'candidatura': { label: 'Richiesta analisi (vecchio modulo)', list: 'BREVO_LIST_CANDIDATURA' },
  'revisione-homepage': { label: 'Smontaggio della homepage', list: 'BREVO_LIST_REVISIONE' },
  'test-posizionamento': { label: 'Test di posizionamento', list: 'BREVO_LIST_TEST' },
  'strumenti-libro': { label: 'Strumenti del libro', list: 'BREVO_LIST_BONUS' },
  'questionario': { label: 'Questionario di posizionamento', list: 'BREVO_LIST_QUESTIONARIO' },
  'scommessa': { label: 'La scommessa (landing /sfida/)', list: 'BREVO_LIST_SCOMMESSA' },
  // campagna Meta per il libro: chi spunta il secondo consenso entra anche nella lista che fa partire la sequenza
  'cassetta': { label: 'La cassetta (landing /cassetta/)', list: 'BREVO_LIST_CASSETTA', optIn: 'BREVO_LIST_CASSETTA_SEQUENZA', optInField: 'consenso_email' },
  // guida gratuita «Che hotel sei?» (landing /guida/), stessa logica della cassetta
  'guida': { label: 'La guida «Che hotel sei?» (landing /guida/)', list: 'BREVO_LIST_GUIDA', optIn: 'BREVO_LIST_GUIDA_SEQUENZA', optInField: 'consenso_email' },
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
  consenso_email: 'Mail successive (consenso)',
};
export const SKIP = new Set(['form-name', 'bot-field', 'ip', 'user_agent', 'referrer', 'inviato', 'evento', 'mkt', 'fbp', 'fbc']);

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
  const optIn = form.optIn && d[form.optInField] ? Number(process.env[form.optIn]) : 0;
  const listIds = [id, optIn].filter(Boolean);
  return { email: d.email, attributes, updateEnabled: true, ...(listIds.length ? { listIds } : {}) };
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
    'Se hai qualcosa da aggiungere, rispondi a questa mail.',
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

// Mail a chi si registra su /bonus: i link agli strumenti, con ?accesso=1 che li sblocca su qualsiasi dispositivo.
const STRUMENTI = [
  ['01', 'I 6 step del posizionamento', 'worksheet'], ['02', 'La matrice delle 4 caselle', 'matrice'],
  ['03', 'I 200 attributi', 'attributi'], ['04', 'Coerenza in 7 punti di contatto', 'coerenza'],
  ['05', 'Dal fatto alla trasformazione', 'scala'], ['06', 'I 5 livelli di consapevolezza', 'livelli'],
  ['07', 'Il Positioning Canvas', 'canvas'],
];
export function bonusMail(d) {
  const nome = ((d.nome || '').trim().split(/\s+/)[0]) || '';
  const base = 'https://hotelpositioning.com';
  const links = [...STRUMENTI.map(([n, t, s]) => [n, t, `${base}/bonus/${s}/?accesso=1`]), ['08', 'Il test del posizionamento', `${base}/quiz/`]];
  const intro = [`Ciao${nome ? ' ' + nome : ''},`, 'ecco gli otto strumenti del libro. Si compilano sul sito, dieci minuti l\'uno, e le risposte restano salvate sul dispositivo che usi.', 'Comincia dal primo: i sei step sono la base, gli altri si appoggiano lì.'];
  const chiusa = ['Se ti blocchi su uno strumento, rispondi a questa mail.', 'Francesco Astolfi\nHotel Positioning'];
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    to: [{ email: d.email, ...(nome ? { name: nome } : {}) }],
    replyTo: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    subject: 'Gli otto strumenti del posizionamento',
    textContent: [...intro, links.map(([n, t, u]) => `${n} · ${t}\n${u}`).join('\n\n'), ...chiusa].join('\n\n'),
    htmlContent: `<div style="font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;color:#0a0a0a;max-width:560px">${intro.map((x) => `<p style="margin:0 0 14px">${esc(x)}</p>`).join('')}<ol style="list-style:none;padding:0;margin:18px 0">${links.map(([n, t, u]) => `<li style="margin:0 0 10px"><a href="${u}" style="color:#0a0a0a;font-weight:700">${n} · ${esc(t)}</a></li>`).join('')}</ol>${chiusa.map((x) => `<p style="margin:0 0 14px">${esc(x).replace('\n', '<br>')}</p>`).join('')}</div>`,
  };
}

// Mail 1 della campagna /cassetta/: la consegna degli strumenti (testo di funnel-libro-cassetta-v1, email 1, oggetto A).
// Le mail 2-7 partono dall'automazione su Brevo, solo per chi è nella lista BREVO_LIST_CASSETTA_SEQUENZA.
export function cassettaMail(d) {
  const nome = ((d.nome || '').trim().split(/\s+/)[0]) || '';
  const base = 'https://hotelpositioning.com';
  const primo = `${base}/bonus/worksheet/?accesso=1`;
  const altri = [...STRUMENTI.slice(1).map(([n, t, s]) => [n, t, `${base}/bonus/${s}/?accesso=1`]), ['08', 'Il test del posizionamento', `${base}/quiz/`]];
  const p1 = [
    `Ciao${nome ? ' ' + nome : ''},`,
    'i link ai tuoi otto strumenti sono in fondo a questa mail. Prima di aprirli, però, fai una cosa che ti prende due minuti.',
    'Apri la homepage del tuo hotel e quella di un concorrente vicino.\nCopri i due loghi con la mano.\nLeggi la prima riga di tutti e due.',
    'Se le puoi scambiare senza che nessuno se ne accorga, hai appena trovato il punto da cui partire.',
    'Non è un difetto tuo. Succede quasi sempre agli hotel curati: si lavora tanto sul prodotto, e la frase che lo vende la si scrive l\'ultimo giorno, di fretta, copiando un po\' da tutti.',
    'Il foglio 01 serve a riscriverla partendo dai fatti, non dagli aggettivi.',
  ];
  const ps = 'P.S. Domani ti racconto di un hotel che aveva tutto: 118 camere, la SPA più grande del Lazio, il più recensito della zona. Ed era invisibile lo stesso.';
  const firma = 'A domani,\nFrancesco';
  const para = (x) => `<p style="margin:0 0 14px">${esc(x).replace(/\n/g, '<br>')}</p>`;
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    to: [{ email: d.email, ...(nome ? { name: nome } : {}) }],
    replyTo: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    subject: 'I tuoi 8 strumenti [comincia dal 01]',
    tags: ['cassetta-email-1'],
    textContent: [...p1, `Apri il foglio 01 →\n${primo}`, 'Gli altri sette:', altri.map(([n, t, u]) => `${n} · ${t}\n${u}`).join('\n\n'), firma, ps].join('\n\n'),
    htmlContent: `<div style="font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;color:#0a0a0a;max-width:560px">${p1.map(para).join('')}<p style="margin:20px 0 22px"><a href="${primo}" style="display:inline-block;background:#ffd22e;color:#0a0a0a;font-weight:700;text-decoration:none;padding:12px 18px;border-radius:10px;border:2px solid #0a0a0a">Apri il foglio 01 →</a></p><p style="margin:0 0 8px">Gli altri sette:</p><ul style="list-style:none;padding:0;margin:0 0 18px">${altri.map(([n, t, u]) => `<li style="margin:0 0 8px"><a href="${u}" style="color:#0a0a0a">${n} · ${esc(t)}</a></li>`).join('')}</ul>${para(firma)}${para(ps)}</div>`,
  };
}

// Conversions API di Meta: l'evento Lead lato server, con lo stesso id del pixel (Meta lo conta una volta sola).
// Parte solo se chi compila ha accettato i cookie di marketing (campo mkt=1) e se ci sono META_PIXEL_ID e META_CAPI_TOKEN.
export async function metaLead(d, headers = {}) {
  const pixel = process.env.META_PIXEL_ID, token = process.env.META_CAPI_TOKEN;
  if (!pixel || !token) return 'saltato: META_PIXEL_ID o META_CAPI_TOKEN mancanti';
  if (d.mkt !== '1') return 'saltato: niente consenso ai cookie di marketing';
  const { createHash } = await import('node:crypto');
  const sha = (v) => createHash('sha256').update(String(v).trim().toLowerCase()).digest('hex');
  const nome = (d.nome || '').trim().split(/\s+/)[0];
  const user = {
    em: [sha(d.email)], ...(nome ? { fn: [sha(nome)] } : {}),
    client_ip_address: headers['x-nf-client-connection-ip'] || (headers['x-forwarded-for'] || '').split(',')[0].trim() || undefined,
    client_user_agent: headers['user-agent'] || undefined,
    ...(d.fbp ? { fbp: d.fbp } : {}), ...(d.fbc ? { fbc: d.fbc } : {}),
  };
  const body = { data: [{
    event_name: 'Lead', event_time: Math.floor(Date.now() / 1000), action_source: 'website',
    event_source_url: `https://hotelpositioning.com/${d['form-name']}/grazie/`, ...(d.evento ? { event_id: d.evento } : {}),
    user_data: user, custom_data: { form: d['form-name'], struttura: d.struttura || '', camere: d.camere || '' },
  }], ...(process.env.META_TEST_EVENT_CODE ? { test_event_code: process.env.META_TEST_EVENT_CODE } : {}) };
  const r = await fetch(`https://graph.facebook.com/v21.0/${pixel}/events?access_token=${encodeURIComponent(token)}`, {
    method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body),
  });
  const txt = await r.text();
  if (!r.ok) throw new Error(`Meta CAPI ${r.status}: ${txt.slice(0, 300)}`);
  return `inviato${body.test_event_code ? ' (con codice di test)' : ''}: ${txt.slice(0, 120)}`;
}

// Mail della guida /guida/: il link al PDF, subito. La sequenza successiva parte da Brevo (lista BREVO_LIST_GUIDA_SEQUENZA).
export function guidaMail(d) {
  const nome = ((d.nome || '').trim().split(/\s+/)[0]) || '';
  const pdf = 'https://hotelpositioning.com/assets/guida/che-hotel-sei.pdf';
  const big = d.camere === '40-80' || d.camere === 'oltre 80';
  const p = [
    `Ciao${nome ? ' ' + nome : ''},`,
    'ecco la guida «Il posizionamento, spiegato semplice a chi ha un hotel». Trenta pagine, mezz\'ora di lettura.',
    'Comincia dalla pagina 2: i cinque conti che paghi ogni anno, e la causa comune. Poi, a pagina 23, la regola più scomoda: prima le operations, dopo il racconto.',
  ];
  const ps = big
    ? 'P.S. Se vuoi vedere come ti legge oggi un ospite, ti faccio lo smontaggio gratuito della tua homepage: la tua prima riga accanto a quella di 2-3 concorrenti, con il logo coperto, e un verdetto. https://hotelpositioning.com/#richiedi'
    : 'P.S. Se dopo la guida vuoi il metodo per scrivere il tuo motivo, è nel libro Hotel Positioning (19,90 €): https://hotelpositioning.com/vai/libro/?da=guida-email1';
  const para = (x) => `<p style="margin:0 0 14px">${esc(x)}</p>`;
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    to: [{ email: d.email, ...(nome ? { name: nome } : {}) }],
    replyTo: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    subject: 'La tua guida: il posizionamento, spiegato semplice',
    tags: ['guida-email-1'],
    textContent: [...p, `Apri la guida →\n${pdf}`, 'Francesco', ps].join('\n\n'),
    htmlContent: `<div style="font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;color:#0a0a0a;max-width:560px">${p.map(para).join('')}<p style="margin:20px 0 22px"><a href="${pdf}" style="display:inline-block;background:#ffd22e;color:#0a0a0a;font-weight:700;text-decoration:none;padding:12px 18px;border-radius:10px;border:2px solid #0a0a0a">Apri la guida (PDF) →</a></p>${para('Francesco')}${para(ps)}</div>`,
  };
}
