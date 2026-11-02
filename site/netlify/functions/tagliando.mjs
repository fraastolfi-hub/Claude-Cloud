// Il Tagliando (/tagliando/): una funzione, tre passaggi chiamati dalla pagina.
//
//   POST { parte: 'pagina',   url, hotel }   legge la pagina, controlla le prove, l'AI legge il messaggio  → risultato firmato
//   POST { parte: 'velocita', url }          Google PageSpeed Insights, mobile                              → risultato firmato (+ screenshot)
//   POST { parte: 'report',   email, hotel, url, pagina, velocita, privacy }
//        verifica le firme, compone il report, salva il contatto su Brevo (FONTE «Il Tagliando»),
//        manda il report a chi l'ha chiesto e la notifica a Francesco.
//   GET  → controllo della configurazione (solo sì/no).
//
// I primi due passaggi partono insieme dal browser: così nessuna chiamata supera il limite di tempo delle funzioni.
//
// Variabili d'ambiente (oltre a quelle di Brevo, vedi functions/invio.mjs):
//   ANTHROPIC_API_KEY       obbligatoria: lettura del messaggio
//   PAGESPEED_API_KEY       consigliata: senza chiave Google limita molto le richieste
//   TAGLIANDO_SECRET        consigliata: firma dei risultati (se manca usa BREVO_API_KEY)
//   BREVO_LIST_TAGLIANDO    facoltativa: lista dedicata (altrimenti BREVO_LIST_DEFAULT)
//   BREVO_LIST_TAGLIANDO_SEQUENZA  lista della sequenza «errori dell'albergatore»: solo chi ha dato il consenso facoltativo

import { FORMS, brevo, saveContact, notification } from '../lib/brevo.mjs';
import { urlSicuro, leggiPagina, estrai, prove, leggiMessaggio, velocita, frasiFatteTrovate, componi, reportMail, firma, verifica, Errore } from '../lib/tagliando.mjs';

const json = (statusCode, body) => ({ statusCode, headers: { 'content-type': 'application/json', 'cache-control': 'no-store' }, body: JSON.stringify(body) });
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const pacco = (dati) => ({ dati, firma: firma(dati) });

export const handler = async (event) => {
  const env = process.env;
  if (event.httpMethod === 'GET') {
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
    if (d.parte === 'pagina') {
      if (!env.ANTHROPIC_API_KEY) return json(503, { ok: false, errore: 'configurazione' });
      const url = await urlSicuro(d.url);
      const { html, finale } = await leggiPagina(url);
      const pagina = estrai(html);
      if (pagina.parole < 30) throw new Errore('pagina', 'La pagina ha pochissimo testo leggibile: forse si carica tutta con JavaScript. Prova con l\'indirizzo di una landing o di una pagina interna.');
      const p = prove(html, pagina.testo);
      const hotel = String(d.hotel || '').slice(0, 120);
      const m = await leggiMessaggio({ url: finale, hotel, pagina });
      const frasi = frasiFatteTrovate(pagina.testo, m.frasi_fatte);
      return json(200, { ok: true, ...pacco({ url, finale, hotel, titolo: pagina.titolo, prove: p, messaggio: m, frasi, ora: Date.now() }) });
    }

    if (d.parte === 'velocita') {
      const url = await urlSicuro(d.url);
      const { screenshot, ...v } = await velocita(url);
      return json(200, { ok: true, screenshot, ...pacco({ url, ...v, ora: Date.now() }) });
    }

    if (d.parte === 'report') {
      if (!d.email || !EMAIL.test(d.email)) return json(400, { ok: false, errore: 'email' });
      if (!d.privacy) return json(400, { ok: false, errore: 'privacy' });
      if (!env.BREVO_API_KEY || !env.BREVO_SENDER_EMAIL || !env.NOTIFY_EMAIL) return json(503, { ok: false, errore: 'configurazione' });
      const pg = verifica(d.pagina);
      const v = verifica(d.velocita);
      const form = FORMS.tagliando;
      const campi = { 'form-name': 'tagliando', email: d.email, hotel: String(d.hotel || '').slice(0, 120), url: String(d.url || '').slice(0, 300), pagina: '/tagliando/', consenso_email: d.consenso_email ? 'sì' : '' };

      // pagina non leggibile: il contatto si salva lo stesso e Francesco riceve la notifica, per rispondere a mano
      if (!pg) {
        campi.esito = 'Pagina non letta: ' + String(d.motivo || 'motivo sconosciuto').slice(0, 200);
        await Promise.allSettled([saveContact(campi, 'tagliando', form), brevo('/smtp/email', notification(campi, form))]);
        return json(200, { ok: true, report: false });
      }
      if (v && v.url !== pg.url) return json(400, { ok: false, errore: 'risultati' });

      const rep = componi({ ...pg, hotel: campi.hotel || pg.hotel, velocita: v });
      campi.hotel = rep.hotel; campi.url = pg.url;
      campi.semafori = `${rep.semafori.messaggio} · ${rep.semafori.prove} · ${rep.semafori.velocita}`;
      campi.profilo = `Tagliando: messaggio ${rep.semafori.messaggio}, prove ${rep.semafori.prove}, velocità ${rep.semafori.velocita}`;
      if (rep.principale) campi.problema = rep.principale.titolo;

      const [mail, saved, notif] = await Promise.allSettled([
        brevo('/smtp/email', reportMail(rep, d.email)),
        saveContact(campi, 'tagliando', form),
        brevo('/smtp/email', notification(campi, form)),
      ]);
      if (saved.status === 'rejected') console.error('contatto non salvato:', saved.reason?.message);
      if (notif.status === 'rejected') console.error('notifica non inviata:', notif.reason?.message);
      if (mail.status === 'rejected') { console.error('report non inviato:', mail.reason?.message); return json(502, { ok: false, errore: 'invio', report: rep }); }
      return json(200, { ok: true, report: rep });
    }

    return json(400, { ok: false, errore: 'parte' });
  } catch (e) {
    if (e instanceof Errore) return json(422, { ok: false, errore: e.codice, messaggio: e.message });
    console.error('tagliando', d.parte, e);
    // dettaglio tecnico breve (nessun dato segreto): serve a capire il guasto dallo schermo, senza aprire i log
    const dettaglio = [e?.constructor?.name, e?.status, String(e?.message || '').replace(/sk-[\w-]+/g, '…').slice(0, 160)].filter(Boolean).join(' · ');
    return json(500, { ok: false, errore: 'interno', dettaglio, messaggio: 'Qualcosa non ha funzionato dal nostro lato. Riprova tra qualche minuto.' });
  }
};
