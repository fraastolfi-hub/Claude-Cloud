// Sintesi con Claude del diario di bordo (funzione in background: Netlify risponde subito 202,
// il lavoro può durare minuti). Il risultato finisce in stato.sintesi[<ambito>], la pagina lo rilegge.
//
// POST { viaggio, codice, ambito: 'viaggio' | 'persona' | 'hotel', autore?, hotelId? }
//   viaggio  → le idee del gruppo: convergenze, divergenze, le 10 da portare a casa
//   persona  → cosa porta a casa una persona, partendo dalla sua sfida e dalla sua struttura
//   hotel    → le lezioni di un singolo hotel visitato

import { VIAGGIO, store, vuoto, t, leggiCorpo, codiceOk, adminOk, modifica, v2 } from '../lib/voyager.mjs';

const MODELLO = 'claude-sonnet-5-5';
const TIPI = { rubare: 'Da rubare', evitare: 'Da non fare mai', dettaglio: 'Dettaglio invisibile', domanda: 'Domanda aperta', stimolo: 'Risposta a uno stimolo' };
const AREE = { management: 'Management', comunicazione: 'Comunicazione', design: 'Design e ristrutturazione', esperienza: 'Guest experience e servizio' };

function materiale(s, filtroHotel) {
  const nomeHotel = Object.fromEntries(s.hotel.map((h) => [h.id, h.nome]));
  const righe = [];
  righe.push('PARTECIPANTI:');
  s.partecipanti.forEach((p) => righe.push(`- ${p.nome}${p.struttura ? ` (${p.struttura})` : ''}`));
  righe.push('\nHOTEL VISITATI:');
  s.hotel.forEach((h) => righe.push(`- ${h.nome}${h.zona ? `, ${h.zona}` : ''}`));
  righe.push('\nNOTE DEL GRUPPO (voti = quanti altri partecipanti erano d\'accordo):');
  s.note
    .filter((n) => !filtroHotel || n.hotelId === filtroHotel)
    .forEach((n) => {
      const dove = n.hotelId ? nomeHotel[n.hotelId] || 'hotel' : (n.domanda ? `stimolo «${n.domanda}»` : 'generale');
      righe.push(`- [${TIPI[n.tipo] || n.tipo}${n.area ? ' · ' + AREE[n.area] : ''} · ${dove} · ${n.autore} · voti ${(n.voti || []).length}] ${n.testo}${n.applicazione ? ` → da me: ${n.applicazione}` : ''}`);
    });
  if (!filtroHotel) {
    righe.push('\nSFIDE PORTATE AL MASTERMIND E RISPOSTE:');
    s.sfide.forEach((f) => {
      righe.push(`- SFIDA di ${f.autore}${f.struttura ? ` (${f.struttura})` : ''}: ${f.testo}${f.provato ? ` | Già provato: ${f.provato}` : ''}`);
      s.risposte.filter((r) => r.sfidaId === f.id).forEach((r) => righe.push(`   · ${r.autore}${r.hotelId ? ` (visto da ${nomeHotel[r.hotelId] || 'un hotel'})` : ''}: ${r.testo}`));
    });
  }
  return righe.join('\n').slice(0, 120000);
}

const BASE = `Sei l'assistente di Hotel Voyager, il viaggio formativo per albergatori di Nicola Delvecchio: un piccolo gruppo di titolari e manager visita dal vivo gli hotel più innovativi e raccoglie impressioni.
Questo gruppo viene dal Garda Trentino (Arco, Riva del Garda e dintorni) e non gestisce solo hotel: ci sono campeggi, residence, villaggi e ville. Lavorano con turismo outdoor e di lago, molto stagionale. Quando adatti un'idea vista in un hotel di città, tienine conto: dì come funzionerebbe in un campeggio, in un residence o in un resort sul lago, e cosa non si trasferisce.
Scrivi in italiano, dando del tu, con tono diretto e concreto da collega esperto, senza enfasi e senza frasi di circostanza.
Usa solo ciò che c'è nel materiale: non inventare hotel, nomi o dati. Cita chi ha detto cosa quando è utile. Se il materiale è scarso, dillo in una riga e lavora con quello che c'è.
Formato: titoli con "## ", elenchi con "- ", grassetto con **. Niente tabelle. Massimo 450 parole.`;

function istruzioni(ambito, d, s) {
  if (ambito === 'persona') {
    const p = s.partecipanti.find((x) => x.nome === d.autore) || { nome: d.autore };
    const sfide = s.sfide.filter((f) => f.autore === d.autore).map((f) => f.testo).join(' | ');
    return `${BASE}

Scrivi la pagina personale di ${p.nome}${p.struttura ? `, che gestisce ${p.struttura}` : ''}.${sfide ? ` La sua sfida dichiarata: ${sfide}.` : ''}
Struttura:
## Le 3 idee che fanno al caso tuo
(scelte dalle note di tutto il gruppo, non solo dalle sue; per ognuna: cosa, dove è stata vista, come adattarla alla sua struttura)
## Cosa ti ha risposto il gruppo
(solo se ci sono risposte alla sua sfida: il succo)
## Il primo passo lunedì mattina
(una sola azione piccola e concreta)`;
  }
  if (ambito === 'hotel') {
    const h = s.hotel.find((x) => x.id === d.hotelId);
    return `${BASE}

Riassumi cosa ha imparato il gruppo visitando ${h ? h.nome : 'questo hotel'}.
## In una frase
## Da rubare
## Da non fare
## Su cosa il gruppo non era d'accordo
(salta la sezione se non ci sono divergenze)`;
  }
  return `${BASE}

Fai la sintesi del viaggio per tutto il gruppo.
## Le idee più forti
(le 7-10 con più voti o ripetute da più persone: cosa, dove, perché funziona)
## Dove il gruppo converge
## Dove il gruppo si divide
(punti di vista diversi sulla stessa cosa: valgono oro, mettili a confronto)
## I fili rossi del viaggio
(2-3 tendenze che attraversano più hotel)
## Domande ancora aperte
(da portare all'ultima cena o al prossimo viaggio)`;
}

async function chiediClaude(prompt) {
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'content-type': 'application/json', 'x-api-key': process.env.ANTHROPIC_API_KEY, 'anthropic-version': '2023-06-01' },
    body: JSON.stringify({ model: MODELLO, max_tokens: 2500, messages: [{ role: 'user', content: prompt }] }),
  });
  if (!r.ok) throw new Error(`Claude ${r.status}: ${(await r.text()).slice(0, 300)}`);
  const j = await r.json();
  return (j.content || []).filter((c) => c.type === 'text').map((c) => c.text).join('\n').trim();
}

const gestisci = async (event) => {
  if (event.httpMethod !== 'POST') return { statusCode: 405 };
  const d = leggiCorpo(event);
  if (!d) return { statusCode: 400 };
  const viaggio = t(d.viaggio, 40);
  if (!VIAGGIO.test(viaggio) || (!codiceOk(d.codice) && !adminOk(d.admin))) return { statusCode: 401 };
  if (!process.env.ANTHROPIC_API_KEY) return { statusCode: 503 };
  const ambito = ['viaggio', 'persona', 'hotel'].includes(d.ambito) ? d.ambito : 'viaggio';
  d.autore = t(d.autore, 60);
  d.hotelId = t(d.hotelId, 20);
  const chiaveSintesi = ambito === 'persona' ? `persona:${d.autore}` : ambito === 'hotel' ? `hotel:${d.hotelId}` : 'viaggio';
  if ((ambito === 'persona' && !d.autore) || (ambito === 'hotel' && !d.hotelId)) return { statusCode: 400 };

  const chiave = `${viaggio}/stato`;

  // segna «in corso»; se ce n'è già una partita da meno di 3 minuti, non ne lancia un'altra
  const { cambiato } = await modifica(chiave, (s) => {
    const prec = s.sintesi[chiaveSintesi];
    if (prec?.stato === 'in corso' && Date.now() - prec.ts < 180000) return false;
    s.sintesi[chiaveSintesi] = { ...(prec || {}), stato: 'in corso', ts: Date.now() };
  });
  if (!cambiato) return { statusCode: 200 };

  let esito;
  try {
    const s = (await store().get(chiave, { type: 'json' })) || vuoto();
    const testo = await chiediClaude(`${istruzioni(ambito, d, s)}\n\nMATERIALE:\n${materiale(s, ambito === 'hotel' ? d.hotelId : null)}`);
    esito = { stato: 'pronta', testo, ts: Date.now(), note: s.note.length };
  } catch (e) {
    console.error('voyager sintesi', e);
    esito = { stato: 'errore', errore: 'La sintesi non è riuscita, riprova tra poco.', ts: Date.now() };
  }
  await modifica(chiave, (s) => {
    const prec = s.sintesi[chiaveSintesi] || {};
    // se fallisce, resta visibile l'ultima sintesi buona
    s.sintesi[chiaveSintesi] = esito.stato === 'errore' ? { ...prec, ...esito, testo: prec.testo } : esito;
  });
  return { statusCode: 200 };
};

export default v2(gestisci);

// formato v2: la modalità background si dichiara qui (il suffisso -background nel nome resta come ripiego)
export const config = { background: true };
