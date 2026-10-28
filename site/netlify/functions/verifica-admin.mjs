// Revisione di Francesco: carica la bozza, salva le modifiche, rifà l'analisi, invia l'esito.
// Autorizzata dal token_admin che viaggia solo nell'email mandata a Francesco.
import {
  AVVIO, CAMPAGNE, TRAFFICO, avviaAnalisi, bozzaValida, json, leggi, linkEsito, mailEsito, manda, salva, salvaContatto,
} from '../lib/verifica.mjs';

const vista = (v) => ({
  id: v.id, email: v.email, nome: v.nome, url_pagina: v.url_pagina,
  campagna: CAMPAGNE[v.tipo_campagna] || null, traffico: TRAFFICO[v.traffico] || null, avvio: AVVIO[v.avvio] || null,
  stato: v.stato, bozza: v.bozza, errore_analisi: v.errore_analisi, inviata: v.inviata, link_esito: linkEsito(v),
});

export default async (req) => {
  if (req.method !== 'POST') return json(405, { ok: false });
  const { azione, id, token, bozza } = await req.json().catch(() => ({}));
  const v = await leggi(id);
  if (!v || typeof token !== 'string' || v.token_admin !== token) return json(404, { ok: false, errore: 'not_found' });

  if (azione === 'carica') return json(200, { ok: true, verifica: vista(v) });
  if (v.stato === 'inviata') return json(409, { ok: false, errore: 'gia_inviata' });

  if (azione === 'rigenera') {
    Object.assign(v, { stato: 'in_analisi', errore_analisi: null });
    await salva(v);
    try {
      await avviaAnalisi(v.id);
    } catch (e) {
      Object.assign(v, { stato: 'da_rivedere', errore_analisi: 'analisi non avviata' });
      await salva(v);
    }
    return json(200, { ok: true, verifica: vista(v) });
  }

  if (azione === 'salva' || azione === 'invia') {
    const b = bozzaValida(bozza);
    if (!b) return json(400, { ok: false, errore: 'bozza_non_valida' });
    Object.assign(v, { bozza: b, esito: b.esito, stato: 'bozza_pronta' });
    if (azione === 'invia') {
      const m = mailEsito(v, b);
      try {
        await manda({ a: v.email, nome: v.nome, oggetto: m.oggetto, html: m.html });
      } catch (e) {
        console.error('esito non inviato', e.message);
        await salva(v);
        return json(502, { ok: false, errore: 'invio_non_riuscito' });
      }
      Object.assign(v, { stato: 'inviata', inviata: new Date().toISOString() });
      salvaContatto(v, b.esito).catch((e) => console.error('contatto Brevo non aggiornato', e.message));
    }
    await salva(v);
    return json(200, { ok: true, verifica: vista(v) });
  }

  return json(400, { ok: false, errore: 'azione_sconosciuta' });
};
