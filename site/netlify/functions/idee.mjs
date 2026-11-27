// Idee per il tuo hotel (/idee/): la pagina chiede qui se il lavoro di idee-background è pronto.
// GET ?id=<id>   → { pronto: false } finché lavora, poi il risultato: { pronto: true, ok, idee[] … } o { pronto: true, ok: false, messaggio }
// GET (senza id) → controllo della configurazione: true/false per ogni variabile, nessun valore.
import { connectLambda } from '@netlify/blobs';
import { ID, storeIdee } from '../lib/idee.mjs';

const json = (statusCode, body) => ({
  statusCode,
  headers: { 'content-type': 'application/json', 'cache-control': 'no-store', 'x-robots-tag': 'noindex' },
  body: JSON.stringify(body),
});

export const handler = async (event) => {
  if (event.httpMethod !== 'GET') return json(405, { ok: false });
  const id = event.queryStringParameters?.id;
  if (!id) {
    const v = ['ANTHROPIC_API_KEY', 'BREVO_API_KEY', 'BREVO_LIST_IDEE', 'NOTIFY_EMAIL'];
    return json(200, Object.fromEntries(v.map((k) => [k, Boolean(process.env[k])])));
  }
  if (!ID.test(id)) return json(400, { ok: false, errore: 'richiesta' });
  connectLambda(event);
  const r = await storeIdee().get(`lavori/${id}`, { type: 'json' });
  return json(200, r ? { pronto: true, ...r } : { pronto: false });
};
