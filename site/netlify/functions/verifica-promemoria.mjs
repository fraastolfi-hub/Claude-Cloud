// Ogni mattina: dopo un "sì" senza call prenotata, un promemoria a 3 giorni e uno a 7, poi basta.
import { mailPromemoria, manda, salva, tutte } from '../lib/verifica.mjs';

const GIORNO = 24 * 3600e3;

export default async () => {
  const ora = Date.now();
  const da = (await tutte()).filter((v) => v.stato === 'inviata' && v.esito === 'si' && !v.call_prenotata && !v.promemoria_2 && v.inviata);
  for (const v of da) {
    const giorni = (ora - Date.parse(v.inviata)) / GIORNO;
    const n = !v.promemoria_1 && giorni >= 3 ? 1 : v.promemoria_1 && giorni >= 7 ? 2 : null;
    if (!n) continue;
    try {
      const m = mailPromemoria(v, n);
      await manda({ a: v.email, nome: v.nome, oggetto: m.oggetto, html: m.html });
      v[n === 1 ? 'promemoria_1' : 'promemoria_2'] = new Date().toISOString();
      await salva(v);
    } catch (e) {
      console.error('promemoria non inviato', v.id, e.message);
    }
  }
};

export const config = { schedule: '0 8 * * *' };
