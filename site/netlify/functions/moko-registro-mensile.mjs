// Registro di marcia Moko: il primo di ogni mese alle 9 (ora di Roma) manda il promemoria.
// A: MOKO_REGISTRO_TO (una o più email separate da virgola) · Copia: MOKO_REGISTRO_CC (facoltativa).
// Mittente e chiave: BREVO_SENDER_EMAIL, BREVO_API_KEY (le stesse dei moduli del sito).
// Non parte se manca un destinatario, se il mese non ha niente da dire o se è già partita per quel mese.
import { getStore } from '@netlify/blobs';
import { CHIAVE, STORE, destinatari, email, indiceMese, invia, vuoto } from '../lib/moko-registro.mjs';

export default async () => {
  const d = destinatari();
  if (!d.to.length) { console.log('registro: nessun destinatario, niente email'); return; }
  const store = getStore({ name: STORE, consistency: 'strong' });
  const stato = (await store.get(CHIAVE, { type: 'json' })) || vuoto();
  const m = email(stato, indiceMese());
  if (!m) { console.log('registro: niente da mandare questo mese'); return; }
  if (stato.inviati?.[m.mese]) { console.log('registro: già inviata per', m.mese); return; }
  await invia(m, d);
  // segna l'invio (rilegge per non cancellare spunte arrivate nel frattempo)
  for (let t = 0; t < 5; t++) {
    const r = await store.getWithMetadata(CHIAVE, { type: 'json' });
    const s = r?.data || vuoto();
    s.inviati = { ...(s.inviati || {}), [m.mese]: new Date().toISOString() };
    const { modified } = await store.setJSON(CHIAVE, s, r ? { onlyIfMatch: r.etag } : { onlyIfNew: true });
    if (modified) break;
  }
  console.log('registro: inviata', m.mese, m.voci, 'voci,', m.indietro, 'indietro');
};

// 7:00 UTC = 9:00 in estate, 8:00 in inverno a Roma
export const config = { schedule: '0 7 1 * *' };
