// Scrive la pageFunction di Apify come modulo TypeScript per la funzione Supabase del sito.
//   node genera-pagefunction-ts.mjs > ../../../hotelpositioning/supabase/functions/_shared/diagnosi/pagefunction.ts
import { VIEWPORT, leggiSchermata, cercaProve, estraiDaPagina } from './estrai.js';
const codice = `async function pageFunction(context) {
  const VIEWPORT = ${JSON.stringify(VIEWPORT)};
  const leggiSchermata = ${leggiSchermata.toString()};
  const cercaProve = ${cercaProve.toString()};
  const estraiDaPagina = ${estraiDaPagina.toString()};
  await context.page.waitForTimeout(3000);
  return { url: context.request.url, ...(await estraiDaPagina(context.page)) };
}`;
process.stdout.write(`// Generato da diagnosi-smontaggio/motore/genera-pagefunction-ts.mjs (repo Claude-Cloud) a partire da estrai.js.
// Non modificare a mano: si rigenera.
export const PAGE_FUNCTION = ${JSON.stringify(codice)};
`);
