// Modulo in due passi di /sfida/ (vedi VERIFICA.md).
// passo1: pagina della campagna + email (il contatto si salva qui) · passo2: campagna, visite, partenza, nome.
// Sotto le 2.000 visite al mese il "no" arriva subito; altrimenti parte l'analisi in background.
import {
  AVVIO, CAMPAGNE, TRAFFICO, avviaAnalisi, controllaUrl, crea, json, leggi, mailFiltro, manda, perEmail, salva, salvaContatto,
} from '../lib/verifica.mjs';

const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const testo = (v, max) => (typeof v === 'string' ? v.trim().slice(0, max) : '');

export default async (req) => {
  if (req.method !== 'POST') return json(405, { ok: false });
  let d;
  try {
    d = await req.json();
  } catch {
    return json(400, { ok: false, errore: 'richiesta' });
  }

  if (d.azione === 'passo1') {
    if (testo(d.sito_web, 200)) return json(200, { ok: true, id: 'x', token: 'x' }); // trappola per i bot
    const email = testo(d.email, 320).toLowerCase();
    if (!EMAIL.test(email)) return json(400, { ok: false, errore: 'email_invalid' });
    if (d.consenso !== true) return json(400, { ok: false, errore: 'consenso_required' });
    const url = controllaUrl(d.url);
    if (!url.ok) return json(400, { ok: false, errore: url.errore });

    const precedenti = await perEmail(email);
    const mese = Date.now() - 30 * 24 * 3600e3;
    const doppione = precedenti.find((v) => v.url_pagina === url.url && Date.parse(v.creata) > mese);
    if (doppione) return json(200, { ok: true, id: doppione.id, token: doppione.token_modulo, duplicata: doppione.stato !== 'parziale' });
    if (precedenti.filter((v) => Date.parse(v.creata) > Date.now() - 24 * 3600e3).length >= 5) return json(429, { ok: false, errore: 'rate_limited' });

    const utm = d.utm && typeof d.utm === 'object' ? d.utm : {};
    const v = await crea({
      email,
      url_pagina: url.url,
      consenso_privacy: true,
      utm: Object.fromEntries(['source', 'medium', 'campaign', 'content'].map((k) => [k, testo(utm[k], 200)]).filter(([, x]) => x)),
    });
    try {
      await salvaContatto(v);
    } catch (e) {
      console.error('contatto Brevo non salvato', e.message);
    }
    return json(200, { ok: true, id: v.id, token: v.token_modulo });
  }

  if (d.azione === 'passo2') {
    const tipo = testo(d.tipo_campagna, 40);
    const traffico = testo(d.traffico, 40);
    const avvio = testo(d.avvio, 40);
    const nome = testo(d.nome, 200);
    if (!CAMPAGNE[tipo] || !TRAFFICO[traffico] || !AVVIO[avvio] || !nome) return json(400, { ok: false, errore: 'campi_mancanti' });
    const v = await leggi(testo(d.id, 64));
    if (!v || v.token_modulo !== d.token) return json(404, { ok: false, errore: 'not_found' });
    if (v.stato !== 'parziale') return json(200, { ok: true, filtrata: v.stato === 'filtrata' }); // doppio invio

    const filtrata = traffico === 'meno_2000';
    Object.assign(v, { nome, tipo_campagna: tipo, traffico, avvio, stato: filtrata ? 'filtrata' : 'in_analisi', ...(filtrata ? { esito: 'no' } : {}) });
    await salva(v);

    if (filtrata) {
      const m = mailFiltro(nome);
      await Promise.allSettled([manda({ a: v.email, nome, oggetto: m.oggetto, html: m.html }), salvaContatto(v, 'no_traffico')])
        .then((r) => r.forEach((x) => x.status === 'rejected' && console.error('filtro', x.reason?.message)));
    } else {
      try {
        await avviaAnalisi(v.id);
      } catch (e) {
        // la richiesta è salvata: Francesco la ritrova con "Rifai l'analisi" o dall'email di errore
        console.error(e.message);
        v.stato = 'da_rivedere';
        v.errore_analisi = 'analisi non avviata';
        await salva(v);
      }
      salvaContatto(v).catch((e) => console.error('contatto Brevo non aggiornato', e.message));
    }
    return json(200, { ok: true, filtrata });
  }

  return json(400, { ok: false, errore: 'azione_sconosciuta' });
};
