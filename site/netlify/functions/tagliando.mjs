// Tagliando Hotel (/tagliando/).
//
// I due controlli lunghi (lettura della pagina con l'AI, PageSpeed) girano in tagliando-background.mjs,
// che salva il risultato firmato in Netlify Blobs. Questa funzione:
//   GET  ?id=…&parte=pagina|velocita   → il risultato, o { pronto: false } se non è ancora finito
//   POST { parte: 'report',   email, hotel, url, pagina, velocita, privacy }
//        verifica le firme, compone il report, salva il contatto su Brevo (FONTE «Tagliando Hotel»),
//        manda il report a chi l'ha chiesto e la notifica a Francesco.
//   GET  → controllo della configurazione (solo sì/no).
//
//
// Variabili d'ambiente (oltre a quelle di Brevo, vedi functions/invio.mjs):
//   ANTHROPIC_API_KEY       obbligatoria: lettura del messaggio
//   PAGESPEED_API_KEY       consigliata: senza chiave Google limita molto le richieste
//   TAGLIANDO_SECRET        consigliata: firma dei risultati (se manca usa BREVO_API_KEY)
//   BREVO_LIST_TAGLIANDO    facoltativa: lista dedicata (altrimenti BREVO_LIST_DEFAULT)
//   BREVO_LIST_TAGLIANDO_SEQUENZA  lista della sequenza «errori dell'albergatore»: solo chi ha dato il consenso facoltativo

import { FORMS, brevo, saveContact, notification, metaLead } from '../lib/brevo.mjs';
import { connectLambda, getStore } from '@netlify/blobs';
import { componi, reportMail, verifica } from '../lib/tagliando.mjs';
import { ID } from '../lib/tagliando-lavori.mjs';

const json = (statusCode, body) => ({ statusCode, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }, body: JSON.stringify(body) });
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export const handler = async (event) => {
  const env = process.env;
  if (event.httpMethod === 'GET') {
    const q = event.queryStringParameters || {};
    if (q.id) {
      if (!ID.test(q.id) || !['pagina', 'velocita'].includes(q.parte)) return json(400, { ok: false, errore: 'richiesta' });
      connectLambda(event);
      const r = await getStore('tagliando').get(`${q.id}-${q.parte}`, { type: 'json' });
      return json(200, r ? { pronto: true, ...r } : { pronto: false });
    }
    return json(200, {
      ANTHROPIC_API_KEY: !!env.ANTHROPIC_API_KEY, PAGESPEED_API_KEY: !!env.PAGESPEED_API_KEY, TAGLIANDO_SECRET: !!env.TAGLIANDO_SECRET,
      BREVO_API_KEY: !!env.BREVO_API_KEY, BREVO_SENDER_EMAIL: !!env.BREVO_SENDER_EMAIL, NOTIFY_EMAIL: !!env.NOTIFY_EMAIL,
      BREVO_LIST_TAGLIANDO: !!env.BREVO_LIST_TAGLIANDO, BREVO_LIST_TAGLIANDO_SEQUENZA: !!env.BREVO_LIST_TAGLIANDO_SEQUENZA,
    });
  }
  if (event.httpMethod !== 'POST') return json(405, { ok: false });

  let d;
  try { d = JSON.parse(event.isBase64Encoded ? Buffer.from(event.body || '', 'base64').toString('utf8') : (event.body || '{}')); } catch { return json(400, { ok: false, errore: 'richiesta' }); }
  if (d['bot-field']) return json(200, { ok: true });

  try {
    if (d.parte === 'report') {
      if (!d.email || !EMAIL.test(d.email)) return json(400, { ok: false, errore: 'email' });
      if (!d.privacy) return json(400, { ok: false, errore: 'privacy' });
      if (!env.BREVO_API_KEY || !env.BREVO_SENDER_EMAIL || !env.NOTIFY_EMAIL) return json(503, { ok: false, errore: 'configurazione' });
      const pg = verifica(d.pagina);
      const v = verifica(d.velocita);
      const form = FORMS.tagliando;
      const campi = { 'form-name': 'tagliando', email: d.email, hotel: String(d.hotel || '').slice(0, 120), url: String(d.url || '').slice(0, 300), pagina: d.lingua === 'en' ? '/en/tagliando/' : '/tagliando/', consenso_email: d.consenso_email ? 'sì' : '' };
      // evento Lead per la Conversions API di Meta (stesso id del pixel, solo con il consenso marketing: lo controlla metaLead)
      const lead = () => metaLead({ ...campi, evento: String(d.evento || '').slice(0, 64), mkt: d.mkt === '1' ? '1' : '', fbp: String(d.fbp || '').slice(0, 200), fbc: String(d.fbc || '').slice(0, 300) }, event.headers || {})
        .then((r) => console.log('Meta CAPI tagliando:', r)).catch((e) => console.error('Meta CAPI tagliando:', e.message));

      // pagina non leggibile: il contatto si salva lo stesso e Francesco riceve la notifica, per rispondere a mano
      if (!pg) {
        campi.esito = 'Pagina non letta: ' + String(d.motivo || 'motivo sconosciuto').slice(0, 200);
        await Promise.allSettled([saveContact(campi, 'tagliando', form), brevo('/smtp/email', notification(campi, form)), lead()]);
        return json(200, { ok: true, report: false });
      }
      if (v && v.url !== pg.url) return json(400, { ok: false, errore: 'risultati' });

      const rep = componi({ ...pg, hotel: campi.hotel || pg.hotel, velocita: v });
      campi.hotel = rep.hotel; campi.url = pg.url;
      campi.semafori = `${rep.semafori.messaggio} · ${rep.semafori.prove} · ${rep.semafori.velocita}`;
      campi.profilo = `Tagliando: messaggio ${rep.semafori.messaggio}, prove ${rep.semafori.prove}, velocità ${rep.semafori.velocita}`;
      if (rep.principale) campi.problema = rep.principale.titolo;

      const [mail, saved, notif, capi] = await Promise.allSettled([
        brevo('/smtp/email', reportMail(rep, d.email)),
        saveContact(campi, 'tagliando', form),
        brevo('/smtp/email', notification(campi, form)),
        lead(),
      ]);
      if (saved.status === 'rejected') console.error('contatto non salvato:', saved.reason?.message);
      if (notif.status === 'rejected') console.error('notifica non inviata:', notif.reason?.message);
      if (mail.status === 'rejected') { console.error('report non inviato:', mail.reason?.message); return json(502, { ok: false, errore: 'invio', report: rep }); }
      return json(200, { ok: true, report: rep });
    }

    return json(400, { ok: false, errore: 'parte' });
  } catch (e) {
    console.error('tagliando', d.parte, e);
    // dettaglio tecnico breve (nessun dato segreto): serve a capire il guasto dallo schermo, senza aprire i log
    const dettaglio = [e?.constructor?.name, e?.status, String(e?.message || '').replace(/sk-[\w-]+/g, '…').slice(0, 160)].filter(Boolean).join(' · ');
    return json(500, { ok: false, errore: 'interno', dettaglio, messaggio: 'Qualcosa non ha funzionato dal nostro lato. Riprova tra qualche minuto.' });
  }
};
