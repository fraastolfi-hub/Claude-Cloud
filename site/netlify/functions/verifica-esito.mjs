// Pagina pubblica dell'esito (/verifica/esito/?t=...): verdetto e punti, mai la nota interna.
// call_prenotata: Calendly ha confermato la prenotazione dalla pagina.
import { LIBRO_URL, json, perTokenEsito, salva } from '../lib/verifica.mjs';

export default async (req) => {
  if (req.method !== 'POST') return json(405, { ok: false });
  const { azione, token } = await req.json().catch(() => ({}));
  const v = await perTokenEsito(token);
  if (!v || v.stato !== 'inviata' || !v.bozza) return json(404, { ok: false, errore: 'not_found' });

  if (azione === 'call_prenotata') {
    if (!v.call_prenotata) {
      v.call_prenotata = new Date().toISOString();
      await salva(v);
    }
    return json(200, { ok: true });
  }

  if (!v.esito_visto) {
    v.esito_visto = new Date().toISOString();
    await salva(v);
  }
  const { esito, motivo, punti } = v.bozza;
  return json(200, {
    ok: true,
    esito: {
      nome: v.nome, email: v.email, url_pagina: v.url_pagina, esito, motivo, punti,
      calendly_url: process.env.VERIFICA_CALENDLY_URL || null, libro_url: LIBRO_URL, call_prenotata: Boolean(v.call_prenotata),
    },
  });
};
