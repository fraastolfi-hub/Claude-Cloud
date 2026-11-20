// Link di condivisione di una scheda di /marketing-ideas/: https://hotelpositioning.com/marketing-ideas/i/<id>
// (_redirects, scritto da build.py, manda /marketing-ideas/i/* qui).
//   - ai crawler dei social (Facebook, WhatsApp, LinkedIn, X, Telegram, Slack, iMessage…) risponde una pagina
//     minima con i meta Open Graph della scheda: titolo, «perché funziona», primo screenshot;
//   - a tutti gli altri risponde un 302 verso /marketing-ideas/?idea=<id>, che apre la scheda nella pagina.
// Solo le schede pubblicate: le altre rimandano all'archivio.
import { connectLambda } from '@netlify/blobs';
import { ID, store, testo } from '../lib/swipe.mjs';

const SITO = 'https://hotelpositioning.com';
const CRAWLER = /facebookexternalhit|facebot|whatsapp|linkedinbot|twitterbot|telegrambot|slackbot|discordbot|pinterest|embedly|skypeuripreview|redditbot|mastodon|bluesky|applebot/i;
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const vai = (dove) => ({ statusCode: 302, headers: { location: dove, 'cache-control': 'no-store' }, body: '' });

export const handler = async (event) => {
  if (event.httpMethod !== 'GET') return { statusCode: 405 };
  const id = String((event.queryStringParameters || {}).id || '').replace(/\/+$/, '');
  if (!ID.test(id)) return vai('/marketing-ideas/');
  const pagina = `/marketing-ideas/?idea=${id}`;
  const ua = event.headers?.['user-agent'] || '';
  if (!CRAWLER.test(ua)) return vai(pagina);

  connectLambda(event);
  let e = null;
  try { e = await store().get(`esempi/${id}`, { type: 'json' }); } catch {}
  if (!e || e.stato !== 'pubblicato') return vai('/marketing-ideas/');

  const titolo = testo(e.title, 120) || 'Idea di marketing per hotel e ristoranti';
  const descr = (testo(e.why, 300) || "Un'idea presa da annunci, email e landing che funzionano: perché funziona e come portarla nel tuo hotel.")
    .replace(/\s+/g, ' ').trim().slice(0, 200);
  const img = (e.images || [])[0];
  const url = `${SITO}/marketing-ideas/i/${id}`;
  const html = `<!DOCTYPE html><html lang="it"><head><meta charset="utf-8">
<title>${esc(titolo)} · L'Archivio del Marketing dell'Ospitalità</title>
<meta name="description" content="${esc(descr)}">
<meta name="robots" content="noindex"><link rel="canonical" href="${SITO}/marketing-ideas/">
<meta property="og:type" content="article"><meta property="og:site_name" content="Hotel Positioning">
<meta property="og:locale" content="it_IT"><meta property="og:url" content="${url}">
<meta property="og:title" content="${esc(titolo)}${e.brand ? ' · ' + esc(testo(e.brand, 60)) : ''}">
<meta property="og:description" content="${esc(descr)}">
${img ? `<meta property="og:image" content="${SITO}/.netlify/functions/swipe?img=${img}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="${SITO}/.netlify/functions/swipe?img=${img}">` : '<meta name="twitter:card" content="summary">'}
<meta name="twitter:title" content="${esc(titolo)}"><meta name="twitter:description" content="${esc(descr)}">
<meta http-equiv="refresh" content="0;url=${pagina}">
</head><body><p><a href="${pagina}">${esc(titolo)}</a> — L'Archivio del Marketing dell'Ospitalità, Hotel Positioning.</p></body></html>`;
  return {
    statusCode: 200,
    headers: { 'content-type': 'text/html; charset=utf-8', 'cache-control': 'public, max-age=0, must-revalidate', 'netlify-cdn-cache-control': 'public, max-age=300, stale-while-revalidate=3600' },
    body: html,
  };
};
