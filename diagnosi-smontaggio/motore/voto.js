// Calcolo del voto e delle segnalazioni (SPEC.md, "I parametri").
import { readFileSync } from 'node:fs';

const DIZ = JSON.parse(readFileSync(new URL('../cliche.json', import.meta.url), 'utf8'));
const VOCI = ['it', 'en'].flatMap(l => Object.values(DIZ[l]).flat());

const TARGET = { esplicito_escludente: 15, implicito: 7, assente: 0 };
const BENEFICIO = { concreto: 15, generico: 7, solo_caratteristiche: 4, assente: 0 };
const SOST = { solo_questo_hotel: 15, vera_per_molti: 7, vera_per_quasi_tutti: 0 };
const APERTURA = { promessa_concreta: 9, problema_soluzione: 6, promessa_generica: 5, storia_immagine: 4, vuota: 0 };
const PROVA = { voto: 15, riconoscimento: 9 };
const GIU = { target: ['esplicito_escludente', 'implicito', 'assente'], beneficio: ['concreto', 'generico', 'solo_caratteristiche', 'assente'] };

export const norm = s => (s || '').toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/[’‘]/g, "'").replace(/\s+/g, ' ').trim();
// Una citazione può unire più pezzi del hero ("A; B", "A | B"): devono esserci tutti.
const contiene = (testo, cit) => !!cit && cit.split(/\s*[;|·]\s*/).filter(Boolean).every(p => norm(testo).includes(norm(p)));

export function testoHero(s) {
  return [s.headline, s.sottotitolo, ...s.supporto].filter(Boolean).join(' \n ');
}

export function cliche(testo) {
  const t = norm(testo);
  const span = VOCI.flatMap(v => [...t.matchAll(new RegExp(v, 'g'))].map(m => [m.index, m.index + m[0].length])).sort((a, b) => a[0] - b[0]);
  const uniti = [];
  for (const [a, b] of span) {
    if (uniti.length && a < uniti.at(-1)[1]) uniti.at(-1)[1] = Math.max(uniti.at(-1)[1], b);
    else uniti.push([a, b]);
  }
  return uniti.map(([a, b]) => t.slice(a, b));
}

const MESI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];

export function dateScadute(testo, oggi = new Date()) {
  const t = norm(testo);
  const trovate = [];
  for (const m of t.matchAll(new RegExp(`(\\d{1,2})\\s+(${MESI.join('|')})\\s+(20\\d\\d)`, 'g'))) {
    const d = new Date(+m[3], MESI.indexOf(m[2]), +m[1]);
    if (d < oggi) trovate.push(m[0]);
  }
  for (const m of t.matchAll(/(\d{1,2})[/.](\d{1,2})[/.](20\d\d)/g)) {
    const d = new Date(+m[3], +m[2] - 1, +m[1]);
    if (d < oggi) trovate.push(m[0]);
  }
  return trovate;
}

const SCARSITA = /solo \d+ camer|ultim[ae] \d+|offerta scade|affrettati|only \d+ rooms? left|hurry/;

function riprova(prove) {
  let migliore = { punti: 0, prova: null };
  for (const p of prove) {
    const fattore = p.schermate < 1 ? 1 : p.schermate <= 1.5 ? 0.8 : 0.33;
    const punti = PROVA[p.tipo] * fattore;
    if (punti > migliore.punti) migliore = { punti, prova: p };
  }
  return migliore;
}

function azione(s) {
  const q = s.cta_primari === 1 ? 6 : s.cta_primari === 2 ? 3 : 0;
  const chiaro = s.modulo_date || /prezz|disponibilit|date|preventivo|tariff|price|availability|quote/.test(norm(s.cta_testo));
  return q + (s.cta_testo || s.modulo_date ? (chiaro ? 4 : 1) : 0);
}

function hookVisibilita(s) {
  if (!s.frase_visibile) return 0;
  return 2 + (s.headline.split(/\s+/).length <= 12 ? 2 : 0) + (s.headline_piu_grande ? 2 : 0);
}

// Porta giù di un livello un giudizio la cui citazione non si trova nel hero.
function verifica(ai, hero) {
  const v = { ...ai };
  for (const campo of ['target', 'beneficio']) {
    if (v[campo] !== 'assente' && !contiene(hero, v[`${campo}_citazione`])) {
      const scala = GIU[campo];
      v[campo] = scala[Math.min(scala.length - 1, scala.indexOf(v[campo]) + 1)];
    }
  }
  if (v.sostituibilita === 'solo_questo_hotel' && !contiene(hero, v.elemento_unico)) v.sostituibilita = 'vera_per_molti';
  v.elementi_concreti = v.elementi_concreti.filter(c => contiene(hero, c));
  if (v.superlativo && !contiene(hero, v.superlativo)) v.superlativo = null;
  return v;
}

export function calcola(estrazione, aiGrezzo, { oggi = new Date() } = {}) {
  const d = estrazione.desktop;
  const m = estrazione.mobile || d;
  const hero = testoHero(d);
  const ai = verifica(aiGrezzo, hero);

  const fuori = [estrazione.title, estrazione.meta, ...d.h1_fuori, ...d.seconda_schermata].join(' \n ');
  ai.concreti_fuori_hero = aiGrezzo.concreti_fuori_hero.filter(c => contiene(fuori, c) && !contiene(hero, c));

  const posizionamento = { target: TARGET[ai.target], beneficio: BENEFICIO[ai.beneficio], differenziazione: SOST[ai.sostituibilita] };

  // Per le regole di esecuzione vale la versione peggiore tra desktop e mobile.
  const hook = Math.min(hookVisibilita(d), hookVisibilita(m)) + (d.frase_visibile && m.frase_visibile ? APERTURA[ai.apertura] : 0);
  const trovati = cliche(hero);
  const k = ai.elementi_concreti.length;
  const puntiCliche = hero.trim() ? 15 * Math.min(1, Math.max(0, 0.25 + 0.25 * k - 0.25 * trovati.length)) : 0;
  const provaD = riprova(d.prove), provaM = riprova(m.prove);
  const prova = provaD.punti <= provaM.punti ? provaD : provaM;
  const puntiAzione = Math.min(azione(d), azione(m));

  const scadute = dateScadute(d.testo_schermata + ' \n ' + m.testo_schermata, oggi);
  const scarsita = SCARSITA.test(norm(d.testo_schermata));
  const penalita = (scadute.length ? -5 : 0) + (scarsita ? -5 : 0);

  const somma = posizionamento.target + posizionamento.beneficio + posizionamento.differenziazione + hook + puntiCliche + prova.punti + puntiAzione + penalita;
  const voto = Math.round(Math.max(0, Math.min(100, somma)));
  const verdetto = voto < 40 ? 'Scritta come tutti gli altri' : voto < 70 ? "Quasi: il motivo c'è, ma è affogato"
    : voto < 85 ? 'Ha un motivo, va affilato' : 'Smontata: lavora già';

  const segnalazioni = [];
  if (!d.frase_visibile || !m.frase_visibile) {
    segnalazioni.push({ tipo: 'nessuna_frase', testo: `Nella prima schermata${!d.frase_visibile ? '' : ' da telefono'} non c'è nessuna frase che dica perché scegliervi.` });
  }
  if (ai.superlativo && prova.punti < 15) {
    segnalazioni.push({ tipo: 'promessa_da_provare', testo: `«${ai.superlativo}» è la promessa più forte della pagina. Chi la prova?` });
  }
  if (ai.concreti_fuori_hero.length >= 2 || ai.concreti_fuori_hero.some(c => /premio|miglior|best|award|travellers/i.test(c))) {
    segnalazioni.push({ tipo: 'parole_posto_sbagliato', testo: 'Hai già le parole giuste. Sono nel posto sbagliato.', citazioni: ai.concreti_fuori_hero });
  }
  if (scadute.length) segnalazioni.push({ tipo: 'scaduta', testo: `Nella prima schermata c'è un'informazione scaduta: «${scadute[0]}».` });
  if (ai.frase_distanza) segnalazioni.push({ tipo: 'distanza', testo: ai.frase_distanza });

  return {
    voto, verdetto,
    parametri: {
      posizionamento: { ...posizionamento, totale: posizionamento.target + posizionamento.beneficio + posizionamento.differenziazione },
      hook, cliche: +puntiCliche.toFixed(1), riprova: +prova.punti.toFixed(1), azione: puntiAzione, penalita,
    },
    frase_posizionamento: ai.frase_posizionamento,
    hero: { headline: d.headline, sottotitolo: d.sottotitolo, supporto: d.supporto },
    cliche_trovati: trovati, elementi_concreti: ai.elementi_concreti,
    prova_migliore: prova.prova,
    segnalazioni,
    ai,
  };
}
