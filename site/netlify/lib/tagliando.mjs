// Tagliando Hotel: il controllo gratuito di un sito o di una landing d'hotel prima di metterci sopra una campagna.
// Scheda del sistema (obiettivo, aree, semafori, uscite): https://claude.ai/artifact/HV2CXp6tBCKLYaE4bTSDyy
//
// Tre aree, in quest'ordine nel report: Messaggio (il cuore, letto dall'AI), Prove e conversione (dall'HTML),
// Velocità (Google PageSpeed Insights, mobile). Sul messaggio si dà solo la prova, mai la riscrittura.
// Le soglie dei semafori sono una prima versione: vanno tarate su 15-20 siti reali (vedi SOGLIE).

import { createHmac, timingSafeEqual } from 'node:crypto';
import { lookup } from 'node:dns/promises';
import { isIP } from 'node:net';
import Anthropic from '@anthropic-ai/sdk';
import { esc } from './brevo.mjs';
import { FRASI_FATTE } from './frasi-fatte.mjs';

export const SOGLIE = {
  velocita: { punteggioRosso: 50, punteggioGiallo: 90, lcpRosso: 4000, lcpGiallo: 2500, clsGrave: 0.25, immaginiKb: 300 },
  messaggio: { frasiFatteGiallo: 3 },
  prove: { mancanzeGiallo: 3 },
};

const UA = 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1 HotelPositioning-Tagliando';

// ---------------------------------------------------------------- indirizzo

// Normalizza l'URL scritto dall'albergatore e rifiuta indirizzi interni (la funzione non deve leggere la rete di Netlify).
export async function urlSicuro(raw) {
  let s = String(raw || '').trim();
  if (!s) throw new Errore('url', "Scrivi l'indirizzo della pagina.");
  if (!/^https?:\/\//i.test(s)) s = 'https://' + s;
  let u;
  try { u = new URL(s); } catch { throw new Errore('url', "L'indirizzo non sembra valido."); }
  if (!['http:', 'https:'].includes(u.protocol) || u.username || u.password) throw new Errore('url', "L'indirizzo non sembra valido.");
  if (u.port && !['80', '443'].includes(u.port)) throw new Errore('url', "L'indirizzo non sembra valido.");
  const host = u.hostname.toLowerCase();
  if (host === 'localhost' || host.endsWith('.local') || host.endsWith('.internal') || !host.includes('.')) throw new Errore('url', "L'indirizzo non sembra valido.");
  const ips = isIP(host) ? [{ address: host }] : await lookup(host, { all: true }).catch(() => []);
  if (!ips.length) throw new Errore('url', 'Non trovo questo sito: controlla l\'indirizzo.');
  if (ips.some(({ address }) => privato(address))) throw new Errore('url', "L'indirizzo non sembra valido.");
  u.hash = '';
  return u.toString();
}

function privato(ip) {
  if (ip.includes(':')) {
    const v = ip.toLowerCase();
    if (v.startsWith('::ffff:')) return privato(v.slice(7));
    return v === '::1' || v === '::' || v.startsWith('fc') || v.startsWith('fd') || v.startsWith('fe80');
  }
  const [a, b] = ip.split('.').map(Number);
  return a === 10 || a === 127 || a === 0 || (a === 169 && b === 254) || (a === 172 && b >= 16 && b <= 31) || (a === 192 && b === 168) || (a === 100 && b >= 64 && b <= 127) || a >= 224;
}

export class Errore extends Error {
  constructor(codice, messaggio) { super(messaggio); this.codice = codice; }
}

// ---------------------------------------------------------------- firma
// I risultati passano dal browser tra una chiamata e l'altra: la firma impedisce di mandare via email un report inventato.

const segreto = () => process.env.TAGLIANDO_SECRET || process.env.BREVO_API_KEY || '';
export function firma(dati) {
  return createHmac('sha256', segreto()).update(JSON.stringify(dati)).digest('base64url');
}
export function verifica(pacco) {
  if (!pacco || typeof pacco !== 'object' || !pacco.dati || !pacco.firma || !segreto()) return null;
  const atteso = Buffer.from(firma(pacco.dati)), arrivato = Buffer.from(String(pacco.firma));
  if (atteso.length !== arrivato.length || !timingSafeEqual(atteso, arrivato)) return null;
  if (Date.now() - (pacco.dati.ora || 0) > 30 * 60 * 1000) return null; // validi 30 minuti
  return pacco.dati;
}

// ---------------------------------------------------------------- pagina

export async function leggiPagina(url) {
  const r = await fetch(url, {
    headers: { 'user-agent': UA, accept: 'text/html,application/xhtml+xml', 'accept-language': 'it-IT,it;q=0.9,en;q=0.6' },
    redirect: 'follow', signal: AbortSignal.timeout(9000),
  }).catch(() => { throw new Errore('pagina', 'Il sito non ha risposto in tempo. Riprova tra qualche minuto.'); });
  if (!r.ok) throw new Errore('pagina', `Il sito ha risposto con un errore (${r.status}). Controlla l'indirizzo.`);
  const tipo = r.headers.get('content-type') || '';
  if (!/html/i.test(tipo)) throw new Errore('pagina', "L'indirizzo non porta a una pagina web.");
  // dopo i redirect, ricontrolla dove si è arrivati
  await urlSicuro(r.url);
  const html = (await r.text()).slice(0, 1_500_000);
  return { html, finale: r.url };
}

const ENTITA = { amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', egrave: 'è', eacute: 'é', agrave: 'à', ograve: 'ò', ugrave: 'ù', igrave: 'ì', rsquo: '’', lsquo: '‘', ldquo: '“', rdquo: '”', hellip: '…', ndash: '–', mdash: '—', euro: '€', laquo: '«', raquo: '»' };
const decodifica = (s) => s
  .replace(/&#(\d+);/g, (_, n) => String.fromCodePoint(Number(n)))
  .replace(/&#x([0-9a-f]+);/gi, (_, n) => String.fromCodePoint(parseInt(n, 16)))
  .replace(/&([a-z]+);/gi, (m, n) => ENTITA[n.toLowerCase()] ?? m);
const testo = (h) => decodifica(h.replace(/<br\s*\/?>/gi, '\n').replace(/<\/(p|div|li|h\d|section|header|footer|tr|a|button)>/gi, '\n').replace(/<[^>]+>/g, ' '))
  .replace(/[ \t\f\v ]+/g, ' ').replace(/\s*\n\s*/g, '\n').replace(/\n{2,}/g, '\n').trim();

export function estrai(html) {
  const pulito = html
    .replace(/<!--[\s\S]*?-->/g, ' ')
    .replace(/<(script|style|noscript|svg|template|iframe)\b[\s\S]*?<\/\1>/gi, ' ');
  const titolo = testo((pulito.match(/<title[^>]*>([\s\S]*?)<\/title>/i) || [])[1] || '');
  const descr = decodifica((html.match(/<meta[^>]+name=["']description["'][^>]*content=["']([^"']*)/i) || html.match(/<meta[^>]+content=["']([^"']*)["'][^>]*name=["']description["']/i) || [])[1] || '');
  const h1 = [...pulito.matchAll(/<h1\b[^>]*>([\s\S]*?)<\/h1>/gi)].map((m) => testo(m[1])).filter(Boolean).slice(0, 3);
  const body = (pulito.match(/<body[^>]*>([\s\S]*)<\/body>/i) || [, pulito])[1];
  // prima schermata, in approssimazione: il testo che viene prima, tolto il menu
  const senzaMenu = body.replace(/<nav\b[\s\S]*?<\/nav>/gi, ' ');
  const tutto = testo(senzaMenu);
  const primaSchermata = tutto.slice(0, 700);
  return { titolo, descrizione: descr, h1, primaSchermata, testo: tutto.slice(0, 14000), parole: tutto.split(/\s+/).length };
}

// ---------------------------------------------------------------- prove e conversione (dall'HTML)

const MOTORI = /simplebooking|bookassist|synxis|vertical-?booking|ermes|blastness|d-edge|availpro|bookingexpert|hotelincloud|octorate|scidoo|siteminder|thebookingbutton|mirai|cloudbeds|hotelrunner|zak|passepartout|book\.|booking-engine|be\.|reservations?\./i;
const PRENOTA = /\b(prenota|prenotazione|book now|book your stay|reserve|verifica disponibilit|controlla disponibilit|check availability|richiedi (un )?preventivo)/i;

export function prove(html, testoPagina) {
  const h = html.toLowerCase(), t = testoPagina.toLowerCase();
  const links = [...html.matchAll(/<a\b[^>]*href=["']([^"']+)["'][^>]*>([\s\S]*?)<\/a>/gi)].map((m) => ({ href: m[1], txt: testo(m[2]).toLowerCase() }));
  const bottoniPrenota = [...links.filter((l) => PRENOTA.test(l.txt) || MOTORI.test(l.href)), ...[...html.matchAll(/<button\b[^>]*>([\s\S]*?)<\/button>/gi)].map((m) => ({ txt: testo(m[1]).toLowerCase(), href: '' })).filter((b) => PRENOTA.test(b.txt))];
  const r = {
    recensioni: /trustyou|revinate|reviewpro|elfsight|trustindex|tripadvisor.*widget|widget.*tripadvisor|google-?reviews|"review"\s*:|itemprop=["']review|testimonial/.test(h) || /\brecension|dicono di noi|cosa dicono|i nostri ospiti dicono|guest reviews|what our guests say/.test(t),
    rating: /"ratingvalue"|aggregaterating/.test(h) || /\b\d[,.]\d\s*(\/|su)\s*10\b|\b\d[,.]\d\s*\/\s*5\b|travellers'? choice|eccezionale \d|superb \d/.test(t),
    referenze: /\b(premio|premi|award|michelin|condé nast|conde nast|gambero rosso|slow food|travellers'? choice|green key|ecolabel|dicono di noi sulla stampa|rassegna stampa|press|certificat|selezionato da|forbes|lonely planet)\b/.test(t),
    faq: /faqpage/.test(h) || /\bfaq\b|domande frequenti|domande e risposte/.test(t),
    cta: bottoniPrenota.length > 0,
    diretto: /miglior prezzo garantito|prezzo migliore garantito|best (price|rate)s? guarante|prenota (direttamente|diretto|sul sito)|vantaggi (della prenotazione|di prenotare|esclusivi)|book direct|tariffa (migliore|più bassa) garantita|solo per chi prenota/.test(t),
    telefono: /href=["']tel:/.test(h),
    whatsapp: /wa\.me\/|api\.whatsapp\.com|whatsapp/.test(h),
    email: /href=["']mailto:/.test(h),
  };
  r.contatti = r.telefono || r.whatsapp;
  return r;
}

// ---------------------------------------------------------------- leggibilità per motori e AI (dall'HTML)

export function segnaliAi(html, pagina) {
  const tipi = [...html.matchAll(/<script[^>]+application\/ld\+json[^>]*>([\s\S]*?)<\/script>/gi)].map((m) => m[1]).join(' ');
  return {
    datiStrutturati: /"@type"\s*:\s*\[?\s*"(Hotel|Resort|LodgingBusiness|BedAndBreakfast|Hostel|Motel|Campground|VacationRental)"/i.test(tipi),
    descrizione: (pagina.descrizione || '').trim().length >= 50,
    titolo: pagina.h1.length > 0,
    testo: pagina.parole >= 150,
  };
}

const SEGNALI_AI = [
  ['datiStrutturati', 'Dati strutturati per motori e AI (schema.org Hotel)', 'Chiedi alla web agency di aggiungere i dati schema.org Hotel: nome, indirizzo, servizi, foto, recensioni.'],
  ['descrizione', 'Descrizione della pagina per Google e AI', 'Scrivi una meta description di 140-160 caratteri con il motivo per sceglierti, non con un elenco di servizi.'],
  ['titolo', 'Un titolo principale (H1) leggibile', 'Metti nel titolo principale cosa trova qui l\'ospite, non solo il nome dell\'hotel.'],
  ['testo', 'Abbastanza testo leggibile senza JavaScript', 'Fai in modo che i testi principali siano nella pagina, non caricati dopo: le AI spesso leggono solo quelli.'],
];

// ---------------------------------------------------------------- velocità

export async function velocita(url) {
  const q = new URLSearchParams({ url, strategy: 'mobile', category: 'performance', locale: 'it' });
  if (process.env.PAGESPEED_API_KEY) q.set('key', process.env.PAGESPEED_API_KEY);
  const r = await fetch('https://www.googleapis.com/pagespeedonline/v5/runPagespeed?' + q, { signal: AbortSignal.timeout(120000) })
    .catch(() => { throw new Errore('velocita', 'PageSpeed non ha risposto in tempo.'); });
  if (!r.ok) throw new Errore('velocita', `PageSpeed ha risposto con un errore (${r.status}).`);
  const j = await r.json();
  const lh = j.lighthouseResult || {}, a = lh.audits || {};
  const risparmio = ['uses-optimized-images', 'modern-image-formats', 'uses-responsive-images', 'offscreen-images']
    .reduce((s, k) => s + (a[k]?.details?.overallSavingsBytes || 0), 0);
  return {
    punteggio: Math.round((lh.categories?.performance?.score ?? 0) * 100),
    lcp: Math.round(a['largest-contentful-paint']?.numericValue || 0),
    cls: Number((a['cumulative-layout-shift']?.numericValue || 0).toFixed(3)),
    immaginiKb: Math.round(risparmio / 1024),
    screenshot: a['final-screenshot']?.details?.data || null, // data URI jpeg, solo per lo schermo
  };
}

// ---------------------------------------------------------------- messaggio (Claude)

const SCHEMA = {
  type: 'object', additionalProperties: false,
  required: ['prima_schermata', 'posizionamento', 'promessa', 'sostituzione', 'frasi_fatte', 'cta_prima_schermata', 'recensioni_visibili', 'problema_principale', 'frase_semaforo', 'lettura_ai'],
  properties: {
    prima_schermata: { type: 'object', additionalProperties: false, required: ['risposta', 'citazione'], properties: {
      risposta: { type: 'boolean', description: "true se la prima schermata dice all'ospite cosa trova qui e per chi è; false se c'è solo un benvenuto, il nome, uno slogan generico o una foto" },
      citazione: { type: 'string', description: 'la frase principale della prima schermata, copiata alla lettera' } } },
    posizionamento: { type: 'object', additionalProperties: false, required: ['esito', 'prova'], properties: {
      esito: { type: 'string', enum: ['chiaro', 'vago', 'assente'] },
      prova: { type: 'string', description: 'perché, in una frase, con le parole della pagina tra virgolette' } } },
    promessa: { type: 'object', additionalProperties: false, required: ['esito', 'citazione'], properties: {
      esito: { type: 'string', enum: ['specifica', 'generica', 'assente'] },
      citazione: { type: 'string', description: 'la frase che più si avvicina a una promessa, alla lettera; vuota se assente' } } },
    sostituzione: { type: 'object', additionalProperties: false, required: ['esito', 'frase_testata', 'spiegazione'], properties: {
      esito: { type: 'string', enum: ['regge_del_tutto', 'regge_in_parte', 'non_regge'], description: 'regge_del_tutto: con il nome di un concorrente il testo resta vero; non_regge: contiene fatti che valgono solo per questo hotel' },
      frase_testata: { type: 'string', description: 'la frase più rappresentativa, copiata alla lettera, su cui hai fatto il test' },
      spiegazione: { type: 'string', description: 'una frase: perché regge o non regge' } } },
    frasi_fatte: { type: 'array', items: { type: 'string' }, description: 'frasi fatte alberghiere trovate nella pagina, copiate alla lettera (anche varianti della libreria), al massimo 12' },
    cta_prima_schermata: { type: 'boolean', description: 'true se nella prima parte della pagina c\'è un invito chiaro a prenotare o verificare la disponibilità' },
    recensioni_visibili: { type: 'boolean', description: 'true se la pagina mostra recensioni o voti degli ospiti' },
    problema_principale: { type: 'object', additionalProperties: false, required: ['titolo', 'prova', 'cosa_costa'], properties: {
      titolo: { type: 'string', description: 'massimo 10 parole, al tu' },
      prova: { type: 'string', description: 'la prova: la frase della pagina citata e cosa succede con il test di sostituzione. Massimo 45 parole' },
      cosa_costa: { type: 'string', description: 'cosa costa all\'hotel, in concreto (confronto sul prezzo, Booking, campagne che portano traffico che non sceglie). Massimo 35 parole' } } },
    frase_semaforo: { type: 'string', description: 'una sola frase, massimo 20 parole, che riassume il messaggio per il semaforo' },
    lettura_ai: { type: 'object', additionalProperties: false, required: ['esito', 'risposta', 'benefici', 'cosa_manca'], properties: {
      esito: { type: 'string', enum: ['chiara', 'parziale', 'confusa'], description: "chiara: un assistente AI capisce benefici concreti e il motivo per scegliere proprio questo hotel; parziale: capisce i servizi ma non il motivo; confusa: non capisce nemmeno per chi è" },
      risposta: { type: 'string', description: "la risposta che darebbe un assistente AI (ChatGPT, Gemini, Perplexity) a «Perché scegliere questo hotel?» usando SOLO questa pagina. Una o due frasi, in terza persona, senza inventare. Massimo 45 parole" },
      benefici: { type: 'array', items: { type: 'string' }, description: "i benefici concreti per l'ospite che si capiscono dalla pagina, al massimo 4, ognuno in poche parole" },
      cosa_manca: { type: 'string', description: "cosa un'AI non riesce a capire o a dire di questo hotel (il motivo di scelta, per chi è, una prova). Una frase, massimo 30 parole, al tu" } } },
  },
};

const SISTEMA = `Leggi la pagina di un hotel come la leggerebbe un ospite che arriva da un annuncio su Instagram o Google e non conosce la struttura.
Il tuo lavoro è solo dire cosa non funziona nel messaggio e dare la prova. Non riscrivi nulla, non proponi frasi alternative, non dai consigli di copy: quello è il lavoro dell'analisi di posizionamento.

Cosa valuti:
1. Prima schermata: c'è una risposta per l'ospite (cosa trova qui, per chi è) o solo "Benvenuti", il nome e una foto?
2. Posizionamento: si capisce per chi è l'hotel e perché sceglierlo?
3. Promessa distintiva: c'è una ragione che solo questo hotel può dare, specifica e verificabile (un fatto, un numero, un luogo, un servizio preciso)?
4. Test di sostituzione: togli il nome dell'hotel e metti quello di un concorrente della stessa zona. Se il testo resta vero, regge del tutto. Una piscina, una SPA, "a due passi dal mare" non bastano: li hanno anche gli altri.
5. Frasi fatte: confronta il testo con questa libreria e trova anche le varianti.
6. Lettura delle AI: immagina che un ospite chieda a ChatGPT o Gemini «perché scegliere questo hotel?» e che l'assistente abbia solo questa pagina. Cosa risponderebbe? Capisce i benefici concreti e il motivo per scegliere proprio questo hotel?
${FRASI_FATTE.map((f) => '- ' + f).join('\n')}

Come scrivi (le risposte finiscono nel report che legge il titolare):
- Dai del tu al titolare: "il tuo hotel", "la tua homepage".
- Frasi corte, il dato prima dell'aggettivo, parole semplici, niente gergo da marketer (niente "brand awareness", "storytelling", "USP").
- Cita sempre le parole della pagina tra virgolette «». Non inventare nulla che non sia nella pagina.
- Niente sarcasmo, niente metafore mediche (mai "sintomo", "malattia", "diagnosi", "cura"), niente lineette lunghe.
- Parla delle scelte della pagina, mai dei difetti di chi l'ha scritta.
- Se il messaggio funziona, dillo con onestà.`;

export async function leggiMessaggio({ url, hotel, pagina }) {
  const client = new Anthropic({ timeout: 180000, maxRetries: 1 });
  const contenuto = [
    `Indirizzo: ${url}`,
    hotel ? `Nome dell'hotel indicato dal titolare: ${hotel}` : '',
    `Titolo della pagina: ${pagina.titolo}`,
    pagina.descrizione ? `Meta description: ${pagina.descrizione}` : '',
    pagina.h1.length ? `Titoli H1: ${pagina.h1.join(' | ')}` : 'Nessun titolo H1.',
    `PRIMA SCHERMATA (il testo che compare per primo, approssimato dal codice):\n${pagina.primaSchermata}`,
    `TESTO DELLA PAGINA:\n${pagina.testo}`,
  ].filter(Boolean).join('\n\n');
  const r = await client.beta.messages.create({
    model: 'claude-opus-5-5',
    max_tokens: 6000,
    betas: ['server-side-fallback-2026-07-01'],
    fallbacks: 'default',
    output_config: { effort: 'low', format: { type: 'json_schema', schema: SCHEMA } },
    system: SISTEMA,
    messages: [{ role: 'user', content: contenuto }],
  });
  if (r.stop_reason === 'refusal') throw new Errore('messaggio', "L'AI non ha letto la pagina.");
  const blocco = r.content.find((b) => b.type === 'text');
  if (!blocco) throw new Errore('messaggio', "L'AI non ha restituito la lettura.");
  const m = JSON.parse(blocco.text);
  m.frasi_fatte = (m.frasi_fatte || []).slice(0, 12);
  if (m.lettura_ai) m.lettura_ai.benefici = (m.lettura_ai.benefici || []).slice(0, 4);
  return m;
}

// ---------------------------------------------------------------- semafori e problemi

export function frasiFatteTrovate(testoPagina, dalAi = []) {
  const t = testoPagina.toLowerCase();
  const dirette = FRASI_FATTE.filter((f) => t.includes(f.toLowerCase()));
  const tutte = [...dirette, ...dalAi.map((f) => f.trim()).filter(Boolean)];
  // una frase contenuta in un'altra già trovata non si conta due volte («ogni comfort» dentro «dotate di ogni comfort»)
  const norm = (f) => f.toLowerCase().replace(/[^a-zàèéìòù ]/g, '').replace(/\s+/g, ' ').trim();
  const uniche = [...new Map(tutte.map((f) => [norm(f), f])).entries()].sort((a, b) => b[0].length - a[0].length);
  const tenute = new Set(uniche.filter(([k], i) => !uniche.slice(0, i).some(([l]) => l.includes(k))).map(([k]) => k));
  const pos = (f) => { const i = t.indexOf(norm(f)); return i < 0 ? Infinity : i; };
  return [...tenute].map((k) => uniche.find(([l]) => l === k)[1]).sort((a, b) => pos(a) - pos(b));
}

export function semaforoMessaggio(m, frasi) {
  if (!m.prima_schermata.risposta || m.sostituzione.esito === 'regge_del_tutto') return 'rosso';
  if (m.promessa.esito !== 'specifica' || frasi.length > SOGLIE.messaggio.frasiFatteGiallo) return 'giallo';
  return 'verde';
}

const PROVE = [
  ['recensioni', 'Non mostri neanche una recensione', 'Metti tre recensioni vere, con nome e data, vicino al pulsante per prenotare.'],
  ['cta', 'Il pulsante per prenotare non si vede subito', 'Metti «Verifica la disponibilità» nella prima schermata da telefono.'],
  ['diretto', 'Non dici perché conviene prenotare da te invece che da Booking', 'Scrivi accanto al pulsante cosa ha in più chi prenota sul sito: un fatto, non uno sconto generico.'],
  ['rating', 'Hai dei voti sui portali e non li fai vedere', 'Mostra il voto di Booking o Google con il numero di recensioni.'],
  ['contatti', 'Chi vuole chiedere una cosa al volo non trova telefono o WhatsApp', 'Aggiungi un telefono cliccabile e un link WhatsApp, visibili da telefono.'],
  ['faq', 'Le domande pratiche restano senza risposta', 'Aggiungi 5-6 risposte brevi: parcheggio, animali, orari di check-in, colazione.'],
  ['referenze', 'Nessun premio, guida o citazione che rassicuri', 'Se hai premi, guide o articoli, mettine due in vista, con il logo.'],
];

export function semaforoProve(p, m) {
  const recensioni = p.recensioni || p.rating || m?.recensioni_visibili;
  const cta = p.cta || m?.cta_prima_schermata;
  if (!recensioni && !cta) return 'rosso';
  const mancanze = PROVE.filter(([k]) => !({ ...p, recensioni: p.recensioni || m?.recensioni_visibili, cta })[k]).length;
  return mancanze >= SOGLIE.prove.mancanzeGiallo ? 'giallo' : 'verde';
}

export function semaforoVelocita(v) {
  if (!v) return 'grigio';
  const s = SOGLIE.velocita;
  if (v.punteggio < s.punteggioRosso || v.lcp > s.lcpRosso) return 'rosso';
  if (v.punteggio < s.punteggioGiallo || v.lcp > s.lcpGiallo) return 'giallo';
  return 'verde';
}

const sec = (ms) => (ms / 1000).toFixed(1).replace('.', ',');

export function problemiVelocita(v) {
  if (!v) return [];
  const s = SOGLIE.velocita, out = [];
  if (v.lcp > s.lcpGiallo) out.push({ area: 'Velocità', titolo: `Chi arriva da Instagram aspetta ${sec(v.lcp)} secondi prima di vedere qualcosa`, fare: 'Chiedi alla web agency di alleggerire la prima schermata: l\'immagine grande e gli script che la precedono.' });
  else if (v.punteggio < s.punteggioGiallo) out.push({ area: 'Velocità', titolo: `Il tuo sito su telefono prende ${v.punteggio} su 100`, fare: 'Gira il link di PageSpeed alla web agency: le voci da sistemare sono già in ordine.' });
  if (v.immaginiKb > s.immaginiKb) out.push({ area: 'Velocità', titolo: `Le foto pesano ${v.immaginiKb} KB più del necessario`, fare: 'Si sistemano in un pomeriggio: formato WebP e misure adatte al telefono.' });
  if (v.cls > s.clsGrave) out.push({ area: 'Velocità', titolo: 'La pagina salta mentre carica', fare: 'Chiedi di fissare le misure di immagini e banner, così il testo resta fermo.' });
  return out;
}

export function problemiProve(p, m) {
  const ok = { ...p, recensioni: p.recensioni || m?.recensioni_visibili, cta: p.cta || m?.cta_prima_schermata };
  return PROVE.filter(([k]) => !ok[k]).map(([, titolo, fare]) => ({ area: 'Prove e conversione', titolo, fare }));
}

// Il report: messaggio prima di tutto, velocità per ultima. 3-5 problemi in tutto.
export function componi({ url, hotel, titolo, prove: p, messaggio: m, frasi, ai: segnali, velocita: v }) {
  const semafori = { messaggio: semaforoMessaggio(m, frasi), prove: semaforoProve(p, m), velocita: semaforoVelocita(v) };
  const frasiSemaforo = {
    messaggio: m.frase_semaforo,
    prove: { rosso: 'Niente recensioni e niente pulsante per prenotare in vista: chi arriva non trova un motivo per fidarsi.', giallo: 'Alcune prove ci sono, altre mancano proprio dove l\'ospite decide.', verde: 'Recensioni, pulsante e contatti sono al loro posto.' }[semafori.prove],
    velocita: v ? { rosso: `Da telefono prende ${v.punteggio} su 100: una parte di chi clicca se ne va prima di vedere la pagina.`, giallo: `Da telefono prende ${v.punteggio} su 100: si può migliorare, ma non è il punto principale.`, verde: `Da telefono prende ${v.punteggio} su 100: la velocità non è un problema.` }[semafori.velocita] : 'Non sono riuscito a misurarla questa volta.',
  };
  const altri = [...problemiProve(p, m).slice(0, 3), ...problemiVelocita(v)].slice(0, semafori.messaggio === 'verde' ? 5 : 4);
  // la domanda centrale del Tagliando: la pagina merita un budget pubblicitario?
  const verdetto = semafori.messaggio === 'rosso'
    ? { codice: 'no', titolo: 'Non ancora. Prima di investire, sistema il messaggio.', testo: 'Una campagna porterebbe persone su una pagina che non dice perché scegliere te. Chi arriva confronta il prezzo, e il confronto prezzi lo vince Booking.' }
    : semafori.messaggio === 'verde' && semafori.prove !== 'rosso' && semafori.velocita !== 'rosso'
      ? { codice: 'si', titolo: 'Sì, la pagina può reggere una campagna.', testo: 'Il messaggio regge. Sistema i punti qui sotto e misura i risultati dal primo giorno.' }
      : { codice: 'quasi', titolo: 'Quasi. Prima di investire, qualche modifica.', testo: 'La pagina ha una base. Prima di metterci sopra un budget, sistema i punti qui sotto: ogni clic pagato arriva su una pagina più convincente.' };
  const lai = m.lettura_ai || null;
  const ai = lai ? { esito: lai.esito, risposta: lai.risposta, benefici: lai.benefici || [], cosaManca: lai.cosa_manca,
    segnali: segnali ? SEGNALI_AI.map(([k, nome, fare]) => ({ nome, ok: !!segnali[k], fare })) : [] } : null;
  return {
    url, hotel: hotel || (titolo || '').split(/[|\-–·]/)[0].trim() || new URL(url).hostname,
    data: new Date().toLocaleDateString('it-IT', { day: 'numeric', month: 'long', year: 'numeric', timeZone: 'Europe/Rome' }),
    verdetto, semafori, frasiSemaforo, frasiFatte: frasi, ai,
    principale: semafori.messaggio === 'verde' ? null : { ...m.problema_principale, frase: m.sostituzione.frase_testata, sostituzione: m.sostituzione.spiegazione },
    altri,
    velocita: v ? { punteggio: v.punteggio, lcp: v.lcp } : null,
  };
}

// ---------------------------------------------------------------- report via email (design system Hotel Positioning, versione morbida)

const C = { crema: '#faf7f4', bianco: '#ffffff', sabbia: '#f3efe9', ink: '#262521', ink2: '#57534c', muted: '#6b665d', line: '#e3ddd4', giallo: '#ffd22e', verde: '#5fd08a', rosso: '#ff5a3c', grigio: '#c9c3b8' };
const NOMI = { messaggio: 'Messaggio', prove: 'Prove e conversione', velocita: 'Velocità' };
const ETICHETTE = { rosso: 'Rosso', giallo: 'Giallo', verde: 'Verde', grigio: 'Non misurata' };
const FONT = "Figtree,'Helvetica Neue',Helvetica,Arial,sans-serif";
const TITOLI = "Outfit,'Helvetica Neue',Helvetica,Arial,sans-serif";
export const LINK = {
  analisi: 'https://hotelpositioning.com/analisi/?utm_source=tagliando&utm_medium=email&utm_campaign=tagliando',
  libro: 'https://www.amazon.it/dp/B0HL3Z4XL7/',
};

export function reportMail(rep, email) {
  const pallino = (c) => `<span style="display:inline-block;width:16px;height:16px;border-radius:50%;background:${C[c]};border:2px solid ${C.ink};vertical-align:-3px"></span>`;
  const p = (t, st = '') => `<p style="margin:0 0 14px;font:16px/1.55 ${FONT};color:${C.ink};${st}">${t}</p>`;
  const card = (inner, bg = C.bianco) => `<div style="background:${bg};border:2px solid ${C.ink};border-radius:16px;padding:20px 22px;margin:0 0 18px">${inner}</div>`;
  const h = (t) => `<p style="margin:0 0 10px;font:700 13px/1.3 ${TITOLI};letter-spacing:.04em;text-transform:uppercase;color:${C.muted}">${t}</p>`;
  const btn = (t, u, bg = C.giallo) => `<a href="${u}" style="display:inline-block;background:${bg};color:${C.ink};font:700 16px/1 ${FONT};text-decoration:none;padding:14px 20px;border-radius:999px;border:2px solid ${C.ink}">${t}</a>`;
  const s = rep.semafori;
  const semafori = ['messaggio', 'prove', 'velocita'].map((k) => `<tr><td style="padding:10px 12px 10px 0;vertical-align:top">${pallino(s[k])}</td><td style="padding:10px 0;border-bottom:1px solid ${C.line}"><b style="font:700 16px/1.3 ${TITOLI};color:${C.ink}">${NOMI[k]}</b> <span style="font:600 13px ${FONT};color:${C.muted}">${ETICHETTE[s[k]]}</span><br><span style="font:15px/1.5 ${FONT};color:${C.ink2}">${esc(rep.frasiSemaforo[k])}</span></td></tr>`).join('');
  const principale = rep.principale ? card(`${h('Il problema principale')}<p style="margin:0 0 12px;font:800 22px/1.2 ${TITOLI};color:${C.ink}">${esc(rep.principale.titolo)}</p>${rep.principale.frase ? `<p style="margin:0 0 12px;padding:12px 14px;background:${C.sabbia};border-radius:10px;font:italic 16px/1.5 ${FONT};color:${C.ink}">«${esc(rep.principale.frase.replace(/^[«"]|[»"]$/g, ''))}»</p>` : ''}${p(esc(rep.principale.prova))}${p('<b>Il test di sostituzione:</b> ' + esc(rep.principale.sostituzione))}${p('<b>Cosa costa:</b> ' + esc(rep.principale.cosa_costa), 'margin:0')}`, C.bianco) : '';
  const frasi = rep.frasiFatte.length ? card(`${h(`Frasi fatte trovate: ${rep.frasiFatte.length}`)}${p(rep.frasiFatte.slice(0, 8).map((f) => `«${esc(f)}»`).join(' · '))}${p('Sono frasi che usano quasi tutti gli hotel: l\'ospite le legge e passa oltre.', `margin:0;color:${C.muted};font-size:14px`)}`) : '';
  const altri = rep.altri.length ? card(`${h('Gli altri punti')}${rep.altri.map((x, i) => `<div style="margin:0 0 ${i === rep.altri.length - 1 ? 0 : 16}px"><p style="margin:0 0 4px;font:700 17px/1.3 ${TITOLI};color:${C.ink}">${esc(x.titolo)}</p><p style="margin:0;font:15px/1.5 ${FONT};color:${C.ink2}"><b>Cosa fare:</b> ${esc(x.fare)}</p></div>`).join('')}`) : '';
  const verde = s.messaggio === 'verde';
  const VC = { no: 'rosso', quasi: 'giallo', si: 'verde' };
  const verdetto = rep.verdetto ? card(`${h('La tua pagina merita un budget pubblicitario?')}<p style="margin:0 0 10px;font:800 24px/1.2 ${TITOLI};color:${C.ink}">${pallino(VC[rep.verdetto.codice])}&nbsp; ${esc(rep.verdetto.titolo)}</p>${p(esc(rep.verdetto.testo), 'margin:0')}`, C.bianco) : '';
  const AIC = { chiara: 'verde', parziale: 'giallo', confusa: 'rosso' };
  const AIE = { chiara: 'Ti capisce', parziale: 'Ti capisce a metà', confusa: 'Non ti capisce' };
  const a = rep.ai;
  const ai = a ? card(`${h('Come ti legge l\'intelligenza artificiale')}<p style="margin:0 0 12px;font:800 20px/1.25 ${TITOLI};color:${C.ink}">${pallino(AIC[a.esito])}&nbsp; ${AIE[a.esito]}</p>${p('Ospiti e agenzie cominciano a chiedere a ChatGPT, Gemini o Perplexity dove dormire. L\'AI risponde con quello che trova scritto. Ho fatto leggere la tua pagina a un\'AI e le ho chiesto: «Perché un ospite dovrebbe scegliere questo hotel?». Ha risposto così:')}<p style="margin:0 0 14px;padding:12px 14px;background:${C.sabbia};border-radius:10px;font:italic 16px/1.5 ${FONT};color:${C.ink}">«${esc(a.risposta.replace(/^[«"]|[»"]$/g, ''))}»</p>${a.benefici.length ? p('<b>I benefici che ha capito:</b> ' + a.benefici.map(esc).join(' · ')) : p('<b>I benefici che ha capito:</b> nessuno di concreto.')}${p('<b>Cosa non ha capito:</b> ' + esc(a.cosaManca))}${a.segnali.length ? `<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;margin-top:4px">${a.segnali.map((x) => `<tr><td style="padding:6px 10px 6px 0;vertical-align:top;font:700 15px ${FONT};color:${x.ok ? '#2f8f57' : C.rosso}">${x.ok ? '✓' : '✗'}</td><td style="padding:6px 0;font:15px/1.45 ${FONT};color:${C.ink2}">${esc(x.nome)}${x.ok ? '' : `<br><span style="color:${C.muted}">${esc(x.fare)}</span>`}</td></tr>`).join('')}</table>` : ''}`) : '';
  const libroLink = `<a href="${LINK.libro}" style="color:${C.ink};font-weight:700">Hotel Positioning, su Amazon</a>`;
  const uscite = verde
    ? card(`${p('<b>E adesso?</b>')}${p('Gira questo report alla tua agenzia: i punti qui sopra si sistemano con le indicazioni di una riga. Il tuo messaggio regge: succede di rado, e va detto.')}${p('Se vuoi parlarne con me prima di lanciare la campagna, rispondi a questa mail.')}${p(`Se vuoi capire perché funziona e come portarlo nelle campagne, il metodo è nel libro: ${libroLink}.`, 'margin:0')}`, C.sabbia)
    : card(`${p('<b>E adesso?</b>')}${p('Gira questo report alla tua agenzia: velocità e prove si sistemano in pochi giorni, con le indicazioni qui sopra.')}${p('Il messaggio è un\'altra cosa. Non si sistema con un pulsante: va trovato cosa rende diverso il tuo hotel, partendo dalle recensioni dei tuoi ospiti. Due strade, scegli tu:')}${p('<b>Vuoi che lo faccia io:</b> l\'analisi di posizionamento.', 'margin:0 0 12px')}<p style="margin:0 0 16px">${btn('Scopri l\'analisi di posizionamento', LINK.analisi)}</p>${p(`<b>Vuoi il metodo:</b> il libro, ${libroLink}.`)}${p('Se vuoi parlarne con me, rispondi a questa mail: la leggo io.', 'margin:0')}`, C.sabbia);
  const html = `<div style="background:${C.crema};padding:24px 12px"><div style="max-width:600px;margin:0 auto">
<p style="margin:0 0 4px;font:700 13px/1.3 ${TITOLI};letter-spacing:.04em;text-transform:uppercase;color:${C.muted}">Tagliando Hotel · Hotel Positioning</p>
<p style="margin:0 0 6px;font:800 30px/1.1 ${TITOLI};color:${C.ink}">${esc(rep.hotel)}</p>
<p style="margin:0 0 22px;font:14px/1.5 ${FONT};color:${C.muted}"><a href="${esc(rep.url)}" style="color:${C.muted}">${esc(rep.url.replace(/^https?:\/\//, '').replace(/\/$/, ''))}</a> · ${esc(rep.data)} · lettura da telefono</p>
${verdetto}
${card(`${h('I tre semafori')}<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse">${semafori}</table>`)}
${principale}${ai}${frasi}${altri}${uscite}
${p(`Francesco Astolfi<br><span style="color:${C.muted}">Hotel Positioning</span>`, 'margin-top:22px')}
<p style="margin:18px 0 0;font:12px/1.5 ${FONT};color:${C.muted}">Hai ricevuto questo report perché hai chiesto Tagliando Hotel su hotelpositioning.com/tagliando. La velocità è misurata con Google PageSpeed Insights da telefono; messaggio, prove e lettura dell'AI vengono dal testo della pagina, letto da un'intelligenza artificiale.</p>
</div></div>`;
  const txt = [
    `Tagliando Hotel · ${rep.hotel}`, `${rep.url} · ${rep.data}`, '',
    ...(rep.verdetto ? ['La tua pagina merita un budget pubblicitario?', rep.verdetto.titolo, rep.verdetto.testo, ''] : []),
    ...['messaggio', 'prove', 'velocita'].map((k) => `${NOMI[k]}: ${ETICHETTE[s[k]]}. ${rep.frasiSemaforo[k]}`), '',
    ...(rep.principale ? [`Il problema principale: ${rep.principale.titolo}`, rep.principale.prova, `Cosa costa: ${rep.principale.cosa_costa}`, ''] : []),
    ...(a ? ['Come ti legge l\'intelligenza artificiale: ' + AIE[a.esito], `Alla domanda «Perché scegliere questo hotel?» un'AI risponde: «${a.risposta}»`, `Benefici capiti: ${a.benefici.join(' · ') || 'nessuno di concreto'}`, `Cosa non ha capito: ${a.cosaManca}`, ...a.segnali.filter((x) => !x.ok).map((x) => `Da sistemare: ${x.nome}. ${x.fare}`), ''] : []),
    ...(rep.frasiFatte.length ? [`Frasi fatte trovate: ${rep.frasiFatte.join(' · ')}`, ''] : []),
    ...rep.altri.flatMap((x) => [x.titolo, `Cosa fare: ${x.fare}`, '']),
    verde ? `E adesso? Gira questo report alla tua agenzia. Il tuo messaggio regge. Se vuoi parlarne con me, rispondi a questa mail. Il metodo è nel libro: ${LINK.libro}` : `E adesso? Gira questo report alla tua agenzia: velocità e prove si sistemano in pochi giorni. Il messaggio è un'altra cosa: va trovato cosa rende diverso il tuo hotel. Due strade:\nVuoi che lo faccia io: l'analisi di posizionamento ${LINK.analisi}\nVuoi il metodo: il libro ${LINK.libro}\nSe vuoi parlarne con me, rispondi a questa mail.`,
    '', 'Francesco Astolfi', 'Hotel Positioning',
  ].join('\n');
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    to: [{ email }],
    replyTo: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    subject: `Tagliando Hotel: la pagina di ${rep.hotel} merita un budget?`,
    tags: ['tagliando-report'],
    htmlContent: html, textContent: txt,
  };
}
