// Registro di marcia dell'area clienti /clienti/moko/registro/: logica comune alle due funzioni.
// Il repository è pubblico: qui non c'è nessun contenuto del cliente. Le voci (testi del piano) arrivano
// dalla pagina cifrata quando qualcuno con la password la apre, e restano solo in Netlify Blobs.
//
// Accesso: la pagina manda l'intestazione x-registro = sha256("moko-registro:" + chiave derivata dalla password).
// Qui si confronta solo sha256(token), scritto da genera.py in moko-registro-token.mjs: senza password non si legge né si scrive.
import { createHash } from 'node:crypto';
import { TOKEN_SHA } from './moko-registro-token.mjs';

export const STORE = 'moko-registro';
export const CHIAVE = 'stato';
export const LINK = 'https://hotelpositioning.com/clienti/moko/#checklist';
// mese 0 del registro = dicembre 2026
export const INIZIO = { anno: 2026, mese: 12 };
const NOMI = ['gennaio', 'febbraio', 'marzo', 'aprile', 'maggio', 'giugno', 'luglio', 'agosto', 'settembre', 'ottobre', 'novembre', 'dicembre'];
const STATI = new Set(['', 'fatto', 'saltato']);
const TIPI = { online: 'Va online', prepara: 'Da preparare', decide: 'Da decidere', controlla: 'Da controllare' };

export const esc = (v) => String(v ?? '').replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
const testo = (v, max) => (typeof v === 'string' ? v.slice(0, max).trim() : '');

export function tokenValido(token) {
  if (typeof token !== 'string' || !/^[0-9a-f]{64}$/.test(token)) return false;
  return createHash('sha256').update(token).digest('hex') === TOKEN_SHA;
}

// indice del mese del registro per una data (fuso di Roma); può essere < 0 o oltre l'ultimo mese
export function indiceMese(d = new Date()) {
  const [a, m] = d.toLocaleDateString('sv-SE', { timeZone: 'Europe/Rome' }).split('-').map(Number);
  return (a - INIZIO.anno) * 12 + (m - INIZIO.mese);
}
export function nomeMese(i) {
  const tot = INIZIO.mese - 1 + i;
  return `${NOMI[((tot % 12) + 12) % 12]} ${INIZIO.anno + Math.floor(tot / 12)}`;
}
export const chiaveMese = (i) => {
  const tot = INIZIO.mese - 1 + i;
  return `${INIZIO.anno + Math.floor(tot / 12)}-${String((((tot % 12) + 12) % 12) + 1).padStart(2, '0')}`;
};

export const vuoto = () => ({ voci: [], stati: {}, aggiornato: null, inviati: {} });

// voci mandate dalla pagina: solo i campi attesi, testi accorciati
export function pulisciVoci(voci) {
  if (!Array.isArray(voci)) return null;
  return voci.slice(0, 400).map((v) => ({
    id: testo(v.id, 20), mese: Math.max(0, Math.min(40, parseInt(v.mese, 10) || 0)),
    tipo: TIPI[v.tipo] ? v.tipo : 'prepara', testo: testo(v.testo, 400), chi: testo(v.chi, 80), entro: testo(v.entro, 40),
  })).filter((v) => /^[\w-]{1,20}$/.test(v.id) && v.testo);
}

export function applica(stato, { id, s, chi }, ora = new Date()) {
  if (!/^[\w-]{1,20}$/.test(String(id || '')) || !STATI.has(s)) throw new Error('voce o stato non valido');
  if (s === '') delete stato.stati[id];
  else stato.stati[id] = { s, chi: testo(chi, 40), quando: ora.toISOString() };
  stato.aggiornato = ora.toISOString();
  return stato;
}

// l'email del primo del mese: le voci del mese e quelle dei mesi passati non ancora fatte
export function email(stato, i = indiceMese()) {
  const voci = stato.voci || [];
  const st = (v) => stato.stati?.[v.id]?.s || '';
  const delMese = voci.filter((v) => v.mese === i);
  const indietro = voci.filter((v) => v.mese < i && !st(v));
  if (!delMese.length && !indietro.length) return null;
  const mese = nomeMese(i);
  const riga = (v, conMese) => {
    const fatto = st(v) === 'fatto', saltato = st(v) === 'saltato';
    const extra = [v.entro && `entro il ${v.entro}`, v.chi, conMese && nomeMese(v.mese)].filter(Boolean).join(' · ');
    const segno = fatto ? '✓ ' : saltato ? '– ' : '';
    return {
      html: `<li style="margin:0 0 10px;${fatto || saltato ? 'color:#8a7470;' : ''}">${segno}${esc(v.testo)}${extra ? `<br><span style="font-size:13px;color:#8a7470">${esc(extra)}</span>` : ''}</li>`,
      text: `- ${segno}${v.testo}${extra ? ` (${extra})` : ''}`,
    };
  };
  const blocchi = [];
  for (const [tipo, titolo] of Object.entries({ online: 'Questo mese va online', prepara: 'Da preparare', decide: 'Da decidere', controlla: 'Da controllare' })) {
    const g = delMese.filter((v) => v.tipo === tipo);
    if (g.length) blocchi.push({ titolo, righe: g.map((v) => riga(v, false)) });
  }
  if (indietro.length) blocchi.push({ titolo: 'Rimasto indietro dai mesi scorsi', righe: indietro.map((v) => riga(v, true)) });
  const titoloMese = mese.charAt(0).toUpperCase() + mese.slice(1);
  const subject = `Moko · il piano di ${mese}${indietro.length ? ` · ${indietro.length} cose rimaste indietro` : ''}`;
  const html = `<!doctype html><html lang="it"><body style="margin:0;background:#F2EAE7;font-family:Helvetica,Arial,sans-serif;color:#301612">
<div style="max-width:560px;margin:0 auto;padding:28px 20px">
<p style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;margin:0 0 6px">Checklist · ${esc(titoloMese)}</p>
<h1 style="font-size:24px;line-height:1.2;margin:0 0 14px">Ecco il piano di ${esc(mese)}.</h1>
<p style="font-size:15px;line-height:1.5;margin:0 0 20px">Le cose del mese e quelle rimaste indietro. Quando una è fatta, segnala nella checklist: il mese prossimo non la ritrovi qui.</p>
${blocchi.map((b) => `<h2 style="font-size:16px;margin:22px 0 8px;padding-top:12px;border-top:1px solid #DCCFC9">${esc(b.titolo)}</h2><ul style="padding-left:18px;margin:0;font-size:15px;line-height:1.45">${b.righe.map((r) => r.html).join('')}</ul>`).join('\n')}
<p style="margin:28px 0"><a href="${LINK}" style="background:#DA4054;color:#fff;text-decoration:none;padding:12px 22px;border-radius:999px;font-weight:bold;display:inline-block">Apri la checklist</a></p>
<p style="font-size:12px;color:#8a7470;margin:0">Promemoria automatico del primo del mese · Hotel Positioning · Hotel Voyager</p>
</div></body></html>`;
  const text = [`Checklist · ${titoloMese}`, '', `Ecco il piano di ${mese}.`, '',
    ...blocchi.flatMap((b) => [b.titolo.toUpperCase(), ...b.righe.map((r) => r.text), '']), `Apri la checklist: ${LINK}`].join('\n');
  return { subject, html, text, mese: chiaveMese(i), voci: delMese.length, indietro: indietro.length };
}

export const destinatari = (env = process.env) => {
  const lista = (v) => String(v || '').split(',').map((x) => x.trim()).filter((x) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(x));
  return { to: lista(env.MOKO_REGISTRO_TO), cc: lista(env.MOKO_REGISTRO_CC) };
};

export async function invia({ subject, html, text }, { to, cc }, env = process.env) {
  if (!env.BREVO_API_KEY || !env.BREVO_SENDER_EMAIL) throw new Error('Brevo non configurato');
  if (!to.length) throw new Error('nessun destinatario');
  const r = await fetch('https://api.brevo.com/v3/smtp/email', {
    method: 'POST',
    headers: { 'api-key': env.BREVO_API_KEY, 'content-type': 'application/json', accept: 'application/json' },
    body: JSON.stringify({
      sender: { email: env.BREVO_SENDER_EMAIL, name: 'Registro Moko' },
      to: to.map((email) => ({ email })), ...(cc.length ? { cc: cc.map((email) => ({ email })) } : {}),
      subject, htmlContent: html, textContent: text,
    }),
  });
  if (!r.ok) throw new Error(`Brevo ${r.status}: ${await r.text()}`);
}
