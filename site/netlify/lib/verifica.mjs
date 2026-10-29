// Codice comune al flusso "Verifica se posso vincere" di /sfida/ (vedi VERIFICA.md):
// archivio su Netlify Blobs, controllo dell'indirizzo, lettura della pagina, bozza con Claude, email.
//
// Variabili d'ambiente (oltre a quelle di Brevo descritte in functions/invio.mjs):
//   ANTHROPIC_API_KEY        obbligatoria per la bozza automatica
//   VERIFICA_SECRET          protegge la funzione di background (stringa lunga a caso)
//   VERIFICA_CALENDLY_URL    link Calendly della call di 60 minuti (senza: pulsante email)
//   BREVO_LIST_VERIFICA      facoltativa: lista Brevo dei contatti della verifica (altrimenti BREVO_LIST_DEFAULT)

import { createHash, randomBytes } from 'node:crypto';
import { getStore } from '@netlify/blobs';
import Anthropic from '@anthropic-ai/sdk';
import { brevo, esc } from './brevo.mjs';

export const SITE = (process.env.URL || 'https://hotelpositioning.com').replace(/\/$/, '');
export const LIBRO_URL = 'https://www.amazon.it/dp/B0HL3Z4XL7/';
export const MITTENTE = 'consulting@francescoastolfi.net';

export const CAMPAGNE = {
  pacchetti: 'Pacchetti e offerte',
  bassa_stagione: 'Bassa stagione',
  matrimoni_eventi: 'Matrimoni ed eventi',
  mice_gruppi: 'MICE e gruppi',
};
export const TRAFFICO = {
  meno_2000: 'Meno di 2.000 visite al mese',
  '2000_5000': '2.000 – 5.000 visite al mese',
  oltre_5000: 'Più di 5.000 visite al mese',
  non_so: 'Non lo sa ancora',
};
export const AVVIO = {
  subito: 'Subito',
  '30_giorni': 'Entro 30 giorni',
  '60_giorni': 'Entro 60 giorni',
  non_ho_fretta: 'Non ha fretta',
};

export const json = (status, body) =>
  new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' } });

export const token = (n = 18) => randomBytes(n).toString('hex');

// ---------- archivio ----------
// r/<id>             la richiesta (JSON)
// e/<token_esito>    -> id, per la pagina pubblica dell'esito
// m/<hash email>/<id> -> '', per doppioni e limite di richieste

const store = () => getStore({ name: 'verifiche', consistency: 'strong' });
const hashEmail = (email) => createHash('sha256').update(email).digest('hex').slice(0, 24);

export async function leggi(id) {
  if (!/^[a-f0-9]{24}$/.test(id || '')) return null;
  return store().get(`r/${id}`, { type: 'json' });
}

export async function salva(v) {
  v.aggiornata = new Date().toISOString();
  await store().setJSON(`r/${v.id}`, v);
  return v;
}

export async function crea(dati) {
  const v = {
    id: token(12),
    creata: new Date().toISOString(),
    stato: 'parziale', // parziale · filtrata · in_analisi · bozza_pronta · da_rivedere · inviata
    esito: null,
    bozza: null,
    errore_analisi: null,
    token_modulo: token(),
    token_esito: token(),
    token_admin: token(24),
    inviata: null,
    esito_visto: null,
    call_prenotata: null,
    promemoria_1: null,
    promemoria_2: null,
    ...dati,
  };
  const s = store();
  await Promise.all([
    s.setJSON(`r/${v.id}`, v),
    s.set(`e/${v.token_esito}`, v.id),
    s.set(`m/${hashEmail(v.email)}/${v.id}`, ''),
  ]);
  return v;
}

export async function perEmail(email) {
  const { blobs } = await store().list({ prefix: `m/${hashEmail(email)}/` });
  const out = await Promise.all(blobs.map((b) => leggi(b.key.split('/').pop())));
  return out.filter(Boolean);
}

export async function perTokenEsito(t) {
  if (!/^[a-f0-9]{36}$/.test(t || '')) return null;
  const id = await store().get(`e/${t}`);
  return id ? leggi(id) : null;
}

export async function tutte() {
  const { blobs } = await store().list({ prefix: 'r/' });
  return (await Promise.all(blobs.map((b) => store().get(b.key, { type: 'json' })))).filter(Boolean);
}

// ---------- indirizzo della pagina ----------

const PORTALI = ['booking.com', 'expedia.', 'hotels.com', 'airbnb.', 'tripadvisor.', 'trivago.', 'agoda.com', 'google.', 'goo.gl', 'facebook.com', 'instagram.com'];

export function controllaUrl(raw) {
  let s = String(raw || '').trim();
  if (!s || s.length > 500) return { ok: false, errore: 'url_invalid' };
  if (!/^https?:\/\//i.test(s)) s = `https://${s}`;
  let u;
  try {
    u = new URL(s);
  } catch {
    return { ok: false, errore: 'url_invalid' };
  }
  const host = u.hostname.toLowerCase();
  if (!host.includes('.') || host === 'localhost' || /^\d+\.\d+\.\d+\.\d+$/.test(host)) return { ok: false, errore: 'url_invalid' };
  if (PORTALI.some((p) => host === p || host.startsWith(p) || host.includes(`.${p}`))) return { ok: false, errore: 'url_ota' };
  u.hash = '';
  return { ok: true, url: u.toString() };
}

export const host = (url) => {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return url;
  }
};

// ---------- lettura della pagina ----------

const decode = (s) =>
  s.replace(/&nbsp;/g, ' ').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;|&apos;/g, "'")
    .replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&#(\d+);/g, (_, n) => String.fromCharCode(Number(n)));
const strip = (s) => decode(s.replace(/<[^>]+>/g, ' ')).replace(/\s+/g, ' ').trim();
const tutti = (html, rx) => [...html.matchAll(rx)].map((m) => strip(m[1])).filter(Boolean);

export async function leggiPagina(url) {
  const r = await fetch(url, {
    redirect: 'follow',
    signal: AbortSignal.timeout(20_000),
    headers: {
      'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
      Accept: 'text/html,application/xhtml+xml',
      'Accept-Language': 'it-IT,it;q=0.9',
    },
  });
  if (!r.ok) throw new Error(`la pagina risponde ${r.status}`);
  const tipo = r.headers.get('content-type') || '';
  if (!tipo.includes('html')) throw new Error(`la pagina non è HTML (${tipo || 'tipo sconosciuto'})`);
  const html = (await r.text()).slice(0, 1_500_000)
    .replace(/<script[\s\S]*?<\/script>/gi, ' ')
    .replace(/<style[\s\S]*?<\/style>/gi, ' ')
    .replace(/<noscript[\s\S]*?<\/noscript>/gi, ' ')
    .replace(/<svg[\s\S]*?<\/svg>/gi, ' ');
  const body = strip(html.match(/<body[^>]*>([\s\S]*)<\/body>/i)?.[1] ?? html);
  if (body.length < 80) throw new Error('pagina quasi vuota: probabilmente il testo è caricato in JavaScript');
  return {
    titolo: tutti(html, /<title[^>]*>([\s\S]*?)<\/title>/gi)[0] || '',
    descrizione: decode(html.match(/<meta[^>]+name=["']description["'][^>]+content=["']([^"']*)["']/i)?.[1] || ''),
    titoli: tutti(html, /<h[1-3][^>]*>([\s\S]*?)<\/h[1-3]>/gi).slice(0, 40),
    azioni: [...new Set(tutti(html, /<(?:a|button)[^>]*>([\s\S]*?)<\/(?:a|button)>/gi))].filter((t) => t.length <= 60).slice(0, 60),
    testo: body.slice(0, 24_000),
  };
}

// ---------- bozza con Claude ----------

const SCHEMA = {
  type: 'object',
  additionalProperties: false,
  required: ['esito', 'motivo', 'punti', 'nota_per_francesco'],
  properties: {
    esito: { type: 'string', enum: ['si', 'no'] },
    motivo: { type: 'string' },
    punti: {
      type: 'array',
      items: {
        type: 'object',
        additionalProperties: false,
        required: ['titolo', 'citazione', 'cosa_vede_l_ospite', 'perche_perde'],
        properties: {
          titolo: { type: 'string' },
          citazione: { type: 'string' },
          cosa_vede_l_ospite: { type: 'string' },
          perche_perde: { type: 'string' },
        },
      },
    },
    nota_per_francesco: { type: 'string' },
  },
};

/** Controlla una bozza (dall'AI o dalla pagina di revisione). Restituisce la bozza pulita o null. */
export function bozzaValida(b) {
  if (!b || (b.esito !== 'si' && b.esito !== 'no')) return null;
  const t = (x, max) => (typeof x === 'string' ? x.trim().slice(0, max) : '');
  const punti = Array.isArray(b.punti) ? b.punti.slice(0, 3).map((p) => ({
    titolo: t(p?.titolo, 160),
    citazione: t(p?.citazione, 400),
    cosa_vede_l_ospite: t(p?.cosa_vede_l_ospite, 1200),
    perche_perde: t(p?.perche_perde, 1200),
  })) : [];
  const motivo = t(b.motivo, 1500);
  if (!motivo || punti.length < 2 || punti.some((p) => !p.titolo || !p.citazione || !p.cosa_vede_l_ospite || !p.perche_perde)) return null;
  return { esito: b.esito, motivo, punti, nota_per_francesco: t(b.nota_per_francesco, 1500) };
}

const SYSTEM = `Prepari la bozza di una "verifica gratuita" per Francesco Astolfi, consulente di posizionamento per hotel.
Un albergatore ha chiesto: "puoi battere la pagina dove arriva la mia campagna?". Francesco scommette così: scrive una landing per quella campagna, la mette in test A/B contro la pagina attuale per 30 giorni a metà traffico, e se non vince rimborsa tutto. La bozza la rivede e firma Francesco prima che parta.

Il metodo con cui giudichi la pagina:
- Chi arriva da un annuncio ha una domanda sola: perché questo hotel e non un altro. Se nei primi secondi la pagina non risponde, l'ospite torna su Booking e confronta il prezzo.
- Una pagina perde quando parla a tutti (famiglie, coppie, lavoro insieme), quando usa aggettivi che potrebbe firmare qualsiasi hotel vicino ("comfort", "relax", "accogliente", "immerso nel verde", "a pochi passi"), quando non riprende la promessa dell'annuncio, quando ha più uscite (menu, "scopri di più") invece di una sola azione, quando nasconde il prezzo o l'offerta.
- La prova del nome: copri il nome dell'hotel. Se la frase potrebbe essere del vicino, non fa scegliere.

Esito:
- "si" se la pagina ha difetti concreti che una landing dedicata può correggere: in quel caso Francesco ha buone probabilità di vincere.
- "no" se la pagina è già specifica e costruita per la campagna, oppure se non è la pagina giusta da mettere in gara (per esempio una homepage generica di una catena dove la campagna non esiste ancora, o una pagina che non appartiene all'hotel). Un no detto davvero rende credibile il sì: non forzare il sì.

Regole di scrittura (italiano, dai del tu, frasi brevi, un'idea per frase, tono calmo e preciso, il dato prima dell'aggettivo, niente sarcasmo, niente metafore mediche, niente lineette lunghe):
- Da 2 a 3 punti. Ogni punto: un titolo breve; una citazione presa ALLA LETTERA dal testo della pagina (copiala esattamente, massimo 160 caratteri); cosa vede l'ospite che arriva dall'annuncio; perché lì la pagina perde ospiti.
- Mostra il problema, mai la soluzione: non scrivere titoli alternativi, slogan, il motivo per cui scegliere l'hotel o come riscrivere la pagina. Quella è la "frase-radice", il primo pezzo del lavoro pagato.
- Niente numeri inventati, niente percentuali di conversione, niente promesse di risultato.
- "motivo": 2-3 frasi che spiegano l'esito all'albergatore.
- "nota_per_francesco": cosa controllare prima di inviare (dubbi, testo forse caricato in JavaScript, pagina che sembra non quella della campagna). Vuota se non c'è niente da segnalare.`;

export async function generaBozza(v, pagina) {
  if (!process.env.ANTHROPIC_API_KEY) throw new Error('manca la chiave ANTHROPIC_API_KEY su Netlify');
  const client = new Anthropic();
  const testo = [
    `Campagna da mettere in gara: ${CAMPAGNE[v.tipo_campagna] || 'non indicata'}`,
    `Traffico dichiarato: ${TRAFFICO[v.traffico] || 'non indicato'}`,
    `Partenza della campagna: ${AVVIO[v.avvio] || 'non indicata'}`,
    `URL: ${v.url_pagina}`,
    '',
    `<titolo>${pagina.titolo}</titolo>`,
    `<meta_description>${pagina.descrizione}</meta_description>`,
    `<titoli_della_pagina>\n${pagina.titoli.join('\n')}\n</titoli_della_pagina>`,
    `<pulsanti_e_link>\n${pagina.azioni.join(' | ')}\n</pulsanti_e_link>`,
    `<testo_della_pagina>\n${pagina.testo}\n</testo_della_pagina>`,
  ].join('\n');

  // Server-side fallback: se il modello rifiuta, l'API riprova da sola con il modello consigliato.
  const stream = client.beta.messages.stream({
    model: 'claude-opus-5-5',
    max_tokens: 64000,
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
    thinking: { type: 'adaptive' },
    output_config: { effort: 'high', format: { type: 'json_schema', schema: SCHEMA } },
    system: SYSTEM,
    messages: [{ role: 'user', content: testo }],
  });
  const msg = await stream.finalMessage();
  if (msg.stop_reason === 'refusal') throw new Error('il modello ha rifiutato la richiesta');
  if (msg.stop_reason === 'max_tokens') throw new Error('risposta troncata');
  const out = msg.content.filter((b) => b.type === 'text').map((b) => b.text).join('');
  const bozza = bozzaValida(JSON.parse(out));
  if (!bozza) throw new Error('bozza incompleta');
  return bozza;
}

// ---------- email ----------

const mittente = () => ({ email: process.env.BREVO_SENDER_EMAIL || MITTENTE, name: 'Francesco Astolfi' });

export async function manda({ a, nome, oggetto, html, rispondiA }) {
  return brevo('/smtp/email', {
    sender: mittente(),
    to: [{ email: a, ...(nome ? { name: nome } : {}) }],
    replyTo: { email: rispondiA || mittente().email },
    subject: oggetto,
    htmlContent: html,
  });
}

export async function salvaContatto(v, esito) {
  const [first, ...rest] = (v.nome || '').trim().split(/\s+/);
  const list = Number(process.env.BREVO_LIST_VERIFICA || process.env.BREVO_LIST_DEFAULT || 0);
  const ammessi = new Set((process.env.BREVO_ATTRIBUTES || 'FONTE').split(',').map((s) => s.trim()).filter(Boolean));
  const attributi = { NOME: first || '', COGNOME: rest.join(' ') };
  if (ammessi.has('FONTE')) attributi.FONTE = 'Verifica della sfida';
  if (ammessi.has('SITO')) attributi.SITO = v.url_pagina;
  if (ammessi.has('PAGINA')) attributi.PAGINA = '/sfida/';
  if (esito && ammessi.has('VERIFICA_ESITO')) attributi.VERIFICA_ESITO = esito;
  return brevo('/contacts', { email: v.email, attributes: attributi, updateEnabled: true, ...(list ? { listIds: [list] } : {}) });
}

const guscio = (dentro) => `<div style="font:16px/1.55 -apple-system,Helvetica,Arial,sans-serif;color:#0a0a0a;max-width:560px">${dentro}<p style="margin:22px 0 0">Francesco</p><p style="margin:18px 0 0;font-size:12px;color:#666">Francesco Astolfi · Hotel Positioning · Via Cupa 5, 47923 Rimini</p></div>`;
const p = (t) => `<p style="margin:0 0 14px">${t}</p>`;
const bottone = (href, label) => `<p style="margin:22px 0"><a href="${href}" style="display:inline-block;padding:14px 22px;background:#ffd22e;color:#0a0a0a;border:2px solid #0a0a0a;text-decoration:none;font-weight:700">${esc(label)}</a></p>`;
const ciao = (nome) => (nome ? `Ciao ${esc(nome.split(' ')[0])},` : 'Ciao,');

export const linkEsito = (v) => `${SITE}/verifica/esito/?t=${v.token_esito}`;
export const linkRivedi = (v) => `${SITE}/verifica/rivedi/?id=${v.id}&t=${v.token_admin}`;

export function mailBozza(v, bozza, errore) {
  const riga = (k, val) => `<tr><td style="padding:7px 10px;border:1px solid #0a0a0a;background:#f4efe2;font-weight:700;vertical-align:top">${k}</td><td style="padding:7px 10px;border:1px solid #0a0a0a">${esc(val)}</td></tr>`;
  const dati = `<table style="border-collapse:collapse;font-size:14px;margin:0 0 20px;width:100%">${riga('Nome', v.nome || '—')}${riga('Email', v.email)}${riga('Pagina', v.url_pagina)}${riga('Campagna', CAMPAGNE[v.tipo_campagna] || '—')}${riga('Traffico', TRAFFICO[v.traffico] || '—')}${riga('Partenza', AVVIO[v.avvio] || '—')}</table>`;
  if (!bozza) {
    return {
      oggetto: `Verifica senza bozza: ${host(v.url_pagina)}`,
      html: guscio(`${p('Ciao Francesco,')}${p(`è arrivata una richiesta ma l'analisi automatica non è riuscita: <strong>${esc(errore || 'errore sconosciuto')}</strong>.`)}${p("Apri la pagina dell'hotel, scrivi tu l'esito e i punti, poi invia.")}${dati}${bottone(linkRivedi(v), "Scrivi l'esito")}`),
    };
  }
  const punti = bozza.punti.map((pt, i) => `<div style="border:2px solid #0a0a0a;padding:12px 14px;margin:0 0 10px"><p style="margin:0 0 6px;font-weight:700">${i + 1}. ${esc(pt.titolo)}</p><p style="margin:0 0 6px;font-size:14px;background:#f4efe2;padding:6px 8px">«${esc(pt.citazione)}»</p><p style="margin:0 0 4px;font-size:14px">${esc(pt.cosa_vede_l_ospite)}</p><p style="margin:0;font-size:14px">${esc(pt.perche_perde)}</p></div>`).join('');
  return {
    oggetto: `Verifica da rivedere: ${bozza.esito === 'si' ? 'SÌ' : 'NO'} · ${host(v.url_pagina)}`,
    html: guscio(`${p('Ciao Francesco,')}${p(`bozza pronta per <strong>${esc(host(v.url_pagina))}</strong>. Esito proposto: <strong style="background:#ffd22e;padding:0 6px">${bozza.esito === 'si' ? 'SÌ, POSSO VINCERE' : 'NO'}</strong>.`)}${bozza.nota_per_francesco ? `<p style="margin:0 0 14px;font-size:15px;border:2px solid #d85a30;padding:8px 10px"><strong>Da controllare:</strong> ${esc(bozza.nota_per_francesco)}</p>` : ''}${p(esc(bozza.motivo))}${punti}${bottone(linkRivedi(v), 'Rivedi e invia')}<p style="margin:0 0 20px;font-size:13px;color:#555">Nella pagina di revisione puoi inviare così com'è con un clic, o correggere prima.</p>${dati}`),
  };
}

export function mailEsito(v, bozza) {
  const si = bozza.esito === 'si';
  return {
    oggetto: si ? 'La tua verifica: sì, posso batterla.' : 'La tua verifica: no, e ti dico perché.',
    html: guscio(`${p(ciao(v.nome))}${p(`ho guardato la pagina che vuoi mettere in gara, <strong>${esc(host(v.url_pagina))}</strong>.`)}<p style="margin:6px 0 18px;font-size:24px;line-height:1.1;font-weight:800;text-transform:uppercase">${si ? 'Sì, posso batterla.' : 'No, per ora non la metto in gara.'}</p>${p(si ? `Ti ho segnato i ${bozza.punti.length} punti in cui oggi perde ospiti, con le parole esatte della tua pagina. Se ti tornano, prenotiamo la call di 60 minuti e partiamo con il test.` : 'Ti spiego perché, punto per punto, con le parole esatte della tua pagina. Un no detto adesso ti risparmia un test che non avrebbe senso.')}${bottone(linkEsito(v), si ? 'Leggi la verifica' : 'Leggi il perché')}`),
  };
}

export function mailFiltro(nome) {
  return {
    oggetto: 'La tua verifica: per ora no, e ti dico perché.',
    html: guscio(`${p(ciao(nome))}${p('grazie per la richiesta. Ti rispondo subito, così non aspetti due giorni per niente.')}${p('<strong>Per ora la sfida non ha senso.</strong> Il test mette la mia pagina contro la tua a metà traffico per 30 giorni e chiede almeno 1.000 visite per pagina: 2.000 al mese dalla campagna. Sotto quella soglia nessuna delle due vince davvero, e non ti faccio pagare una scommessa che non si può chiudere.')}${p('Se vuoi lavorare da solo sul motivo per cui un ospite dovrebbe scegliere te, il metodo è tutto nel libro.')}${bottone(LIBRO_URL, 'Il libro · 19,90 € su Amazon')}${p('Quando la campagna cresce, rimandami la pagina.')}`),
  };
}

export function mailPromemoria(v, n) {
  return n === 1
    ? {
        oggetto: 'La sfida è ancora aperta',
        html: guscio(`${p(ciao(v.nome))}${p(`qualche giorno fa ti ho scritto che posso battere <strong>${esc(host(v.url_pagina))}</strong>. Il calendario per la call è nella pagina della verifica: 60 minuti, poi decidi tu.`)}${bottone(linkEsito(v), 'Prenota la call')}`),
      }
    : {
        oggetto: 'Ultimo messaggio sulla verifica',
        html: guscio(`${p(ciao(v.nome))}${p('non ti scrivo più dopo questo. Se la campagna parte e vuoi mettere la pagina in gara, la verifica resta lì e il calendario pure.')}${bottone(linkEsito(v), 'Riapri la verifica')}${p('Se invece hai deciso di no, va benissimo: rispondi a questa email con due parole sul perché. Mi serve.')}`),
      };
}

/** Legge la pagina, prepara la bozza, salva lo stato e avvisa Francesco. */
export async function analizza(id) {
  const v = await leggi(id);
  if (!v || v.stato !== 'in_analisi') return;
  let bozza = null;
  let errore = null;
  try {
    bozza = await generaBozza(v, await leggiPagina(v.url_pagina));
  } catch (e) {
    errore = e instanceof Error ? e.message : String(e);
    console.error('analisi non riuscita', id, errore);
  }
  Object.assign(v, bozza ? { stato: 'bozza_pronta', bozza, esito: bozza.esito, errore_analisi: null } : { stato: 'da_rivedere', errore_analisi: errore });
  await salva(v);
  const m = mailBozza(v, bozza, errore);
  const a = (process.env.NOTIFY_EMAIL || MITTENTE).split(',')[0].trim();
  await manda({ a, oggetto: m.oggetto, html: m.html, rispondiA: v.email });
}

/** Avvia l'analisi nella funzione di background (fino a 15 minuti). */
export async function avviaAnalisi(id) {
  const r = await fetch(`${SITE}/.netlify/functions/verifica-analisi-background`, {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-verifica-secret': process.env.VERIFICA_SECRET || '' },
    body: JSON.stringify({ id }),
  });
  if (r.status !== 202 && !r.ok) throw new Error(`analisi non avviata: ${r.status}`);
}
