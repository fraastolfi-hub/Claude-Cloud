// Genera la pageFunction per apify/playwright-scraper con lo stesso codice di estrai.js.
import { VIEWPORT, leggiSchermata, cercaProve, estraiDaPagina } from './estrai.js';
const codice = `async function pageFunction(context) {
  const VIEWPORT = ${JSON.stringify(VIEWPORT)};
  const leggiSchermata = ${leggiSchermata.toString()};
  const cercaProve = ${cercaProve.toString()};
  const estraiDaPagina = ${estraiDaPagina.toString()};
  await context.page.waitForTimeout(3000);
  return { url: context.request.url, ...(await estraiDaPagina(context.page)) };
}`;
process.stdout.write(JSON.stringify(codice));
