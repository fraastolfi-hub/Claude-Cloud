// Funzione di background (fino a 15 minuti): legge la pagina dell'hotel, prepara la bozza con Claude,
// la salva e manda a Francesco l'email "Rivedi e invia". La avviano verifica-invio e verifica-admin.
import { analizza } from '../lib/verifica.mjs';

export default async (req) => {
  const segreto = process.env.VERIFICA_SECRET;
  if (segreto && req.headers.get('x-verifica-secret') !== segreto) return;
  const { id } = await req.json().catch(() => ({}));
  if (id) await analizza(id); // analizza solo richieste in stato in_analisi
};
