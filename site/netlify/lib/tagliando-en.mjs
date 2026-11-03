// Tagliando Hotel in inglese: i testi del report (pagina /en/tagliando/). La logica sta in tagliando.mjs;
// qui solo le parole. Stessa struttura e stesso stile del report italiano.
import { esc } from './brevo.mjs';

export const EN = {
  prove: {
    recensioni: ['You don\'t show a single review', 'Put three real reviews, with name and date, next to the booking button.'],
    cta: ['The booking button isn\'t visible straight away', 'Put «Check availability» on the first mobile screen.'],
    diretto: ['You don\'t say why booking with you beats booking on Booking', 'Next to the button, write what direct bookers get: a fact, not a generic discount.'],
    rating: ['You have scores on the portals and don\'t show them', 'Show your Booking or Google score with the number of reviews.'],
    contatti: ['Anyone with a quick question can\'t find a phone or WhatsApp', 'Add a tappable phone number and a WhatsApp link, visible on mobile.'],
    faq: ['Practical questions go unanswered', 'Add 5-6 short answers: parking, pets, check-in times, breakfast.'],
    referenze: ['No award, guide or press mention to reassure', 'If you have awards, guides or articles, show two of them, with the logo.'],
  },
  segnali: {
    datiStrutturati: ['Structured data for search engines and AI (schema.org Hotel)', 'Ask your web agency to add schema.org Hotel data: name, address, amenities, photos, reviews.'],
    descrizione: ['A page description for Google and AI', 'Write a 140-160 character meta description with the reason to choose you, not a list of amenities.'],
    titolo: ['A readable main heading (H1)', 'Put what guests find here in the main heading, not just the hotel\'s name.'],
    testo: ['Enough text readable without JavaScript', 'Make sure the main texts are in the page, not loaded later: AI tools often read only those.'],
  },
  provePhr: { rosso: 'No reviews and no booking button in sight: visitors find no reason to trust you.', giallo: 'Some proof is there, some is missing exactly where guests decide.', verde: 'Reviews, booking button and contacts are in place.' },
  velPhr: (p) => ({ rosso: `On mobile it scores ${p} out of 100: some of the people who click leave before they see the page.`, giallo: `On mobile it scores ${p} out of 100: it can improve, but it isn't the main point.`, verde: `On mobile it scores ${p} out of 100: speed isn't a problem.` }),
  velNone: 'I couldn\'t measure it this time.',
  verdetto: {
    no: { codice: 'no', titolo: 'Not yet. Before investing, fix the message.', testo: 'A campaign would bring people to a page that doesn\'t say why they should choose you. Visitors compare prices, and Booking wins the price comparison.' },
    si: { codice: 'si', titolo: 'Yes, the page can carry a campaign.', testo: 'The message holds. Fix the points below and measure results from day one.' },
    quasi: { codice: 'quasi', titolo: 'Almost. A few changes before investing.', testo: 'The page has a foundation. Before putting a budget behind it, fix the points below: every paid click lands on a more convincing page.' },
  },
  vel: (v, s) => {
    const sec = (ms) => (ms / 1000).toFixed(1);
    const out = [];
    if (v.lcp > s.lcpGiallo) out.push({ area: 'Speed', titolo: `Visitors from Instagram wait ${sec(v.lcp)} seconds before they see anything`, fare: 'Ask your web agency to lighten the first screen: the large image and the scripts that load before it.' });
    else if (v.punteggio < s.punteggioGiallo) out.push({ area: 'Speed', titolo: `Your site scores ${v.punteggio} out of 100 on mobile`, fare: 'Send the PageSpeed link to your web agency: the items to fix are already in order.' });
    if (v.immaginiKb > s.immaginiKb) out.push({ area: 'Speed', titolo: `Your photos weigh ${v.immaginiKb} KB more than they need to`, fare: 'An afternoon\'s work: WebP format and sizes made for mobile.' });
    if (v.cls > s.clsGrave) out.push({ area: 'Speed', titolo: 'The page jumps while it loads', fare: 'Ask for fixed sizes on images and banners, so the text stays put.' });
    return out;
  },
};

const C = { crema: '#faf7f4', bianco: '#ffffff', sabbia: '#f3efe9', ink: '#262521', ink2: '#57534c', muted: '#6b665d', line: '#e3ddd4', giallo: '#ffd22e', verde: '#5fd08a', rosso: '#ff5a3c', grigio: '#c9c3b8' };
const NOMI = { messaggio: 'Message', prove: 'Proof and conversion', velocita: 'Speed' };
const ETICHETTE = { rosso: 'Red', giallo: 'Amber', verde: 'Green', grigio: 'Not measured' };
const FONT = "Figtree,'Helvetica Neue',Helvetica,Arial,sans-serif";
const TITOLI = "Outfit,'Helvetica Neue',Helvetica,Arial,sans-serif";
const LINK = {
  analisi: 'https://hotelpositioning.com/en/analysis/?utm_source=tagliando&utm_medium=email&utm_campaign=tagliando-en',
  libro: 'https://www.amazon.it/dp/B0HL3Z4XL7/',
};

export function reportMailEn(rep, email) {
  const pallino = (c) => `<span style="display:inline-block;width:16px;height:16px;border-radius:50%;background:${C[c]};border:2px solid ${C.ink};vertical-align:-3px"></span>`;
  const p = (t, st = '') => `<p style="margin:0 0 14px;font:16px/1.55 ${FONT};color:${C.ink};${st}">${t}</p>`;
  const card = (inner, bg = C.bianco) => `<div style="background:${bg};border:2px solid ${C.ink};border-radius:16px;padding:20px 22px;margin:0 0 18px">${inner}</div>`;
  const h = (t) => `<p style="margin:0 0 10px;font:700 13px/1.3 ${TITOLI};letter-spacing:.04em;text-transform:uppercase;color:${C.muted}">${t}</p>`;
  const btn = (t, u) => `<a href="${u}" style="display:inline-block;background:${C.giallo};color:${C.ink};font:700 16px/1 ${FONT};text-decoration:none;padding:14px 20px;border-radius:999px;border:2px solid ${C.ink}">${t}</a>`;
  const q = (t) => `“${esc(String(t).replace(/^[«"“]|[»"”]$/g, ''))}”`;
  const s = rep.semafori;
  const semafori = ['messaggio', 'prove', 'velocita'].map((k) => `<tr><td style="padding:10px 12px 10px 0;vertical-align:top">${pallino(s[k])}</td><td style="padding:10px 0;border-bottom:1px solid ${C.line}"><b style="font:700 16px/1.3 ${TITOLI};color:${C.ink}">${NOMI[k]}</b> <span style="font:600 13px ${FONT};color:${C.muted}">${ETICHETTE[s[k]]}</span><br><span style="font:15px/1.5 ${FONT};color:${C.ink2}">${esc(rep.frasiSemaforo[k])}</span></td></tr>`).join('');
  const principale = rep.principale ? card(`${h('The main problem')}<p style="margin:0 0 12px;font:800 22px/1.2 ${TITOLI};color:${C.ink}">${esc(rep.principale.titolo)}</p>${rep.principale.frase ? `<p style="margin:0 0 12px;padding:12px 14px;background:${C.sabbia};border-radius:10px;font:italic 16px/1.5 ${FONT};color:${C.ink}">${q(rep.principale.frase)}</p>` : ''}${p(esc(rep.principale.prova))}${p('<b>The substitution test:</b> ' + esc(rep.principale.sostituzione))}${p('<b>What it costs you:</b> ' + esc(rep.principale.cosa_costa), 'margin:0')}`) : '';
  const frasi = rep.frasiFatte.length ? card(`${h(`Stock phrases found: ${rep.frasiFatte.length}`)}${p(rep.frasiFatte.slice(0, 8).map(q).join(' · '))}${p('Almost every hotel uses these phrases: guests read them and move on.', `margin:0;color:${C.muted};font-size:14px`)}`) : '';
  const altri = rep.altri.length ? card(`${h('The other points')}${rep.altri.map((x, i) => `<div style="margin:0 0 ${i === rep.altri.length - 1 ? 0 : 16}px"><p style="margin:0 0 4px;font:700 17px/1.3 ${TITOLI};color:${C.ink}">${esc(x.titolo)}</p><p style="margin:0;font:15px/1.5 ${FONT};color:${C.ink2}"><b>What to do:</b> ${esc(x.fare)}</p></div>`).join('')}`) : '';
  const verde = s.messaggio === 'verde';
  const VC = { no: 'rosso', quasi: 'giallo', si: 'verde' };
  const verdetto = rep.verdetto ? card(`${h('Does your page deserve an ad budget?')}<p style="margin:0 0 10px;font:800 24px/1.2 ${TITOLI};color:${C.ink}">${pallino(VC[rep.verdetto.codice])}&nbsp; ${esc(rep.verdetto.titolo)}</p>${p(esc(rep.verdetto.testo), 'margin:0')}`) : '';
  const AIC = { chiara: 'verde', parziale: 'giallo', confusa: 'rosso' };
  const AIE = { chiara: 'It understands you', parziale: 'It half understands you', confusa: 'It doesn\'t understand you' };
  const a = rep.ai;
  const ai = a ? card(`${h('How artificial intelligence reads you')}<p style="margin:0 0 12px;font:800 20px/1.25 ${TITOLI};color:${C.ink}">${pallino(AIC[a.esito])}&nbsp; ${AIE[a.esito]}</p>${p('Guests and agencies are starting to ask ChatGPT, Gemini or Perplexity where to stay. AI answers with what it finds written. I had an AI read your page and asked it: “Why should a guest choose this hotel?”. This is its answer:')}<p style="margin:0 0 14px;padding:12px 14px;background:${C.sabbia};border-radius:10px;font:italic 16px/1.5 ${FONT};color:${C.ink}">${q(a.risposta)}</p>${p('<b>The benefits it understood:</b> ' + (a.benefici.length ? a.benefici.map(esc).join(' · ') : 'none that are concrete.'))}${p('<b>What it didn\'t understand:</b> ' + esc(a.cosaManca))}${a.segnali.length ? `<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse;margin-top:4px">${a.segnali.map((x) => `<tr><td style="padding:6px 10px 6px 0;vertical-align:top;font:700 15px ${FONT};color:${x.ok ? '#2f8f57' : C.rosso}">${x.ok ? '✓' : '✗'}</td><td style="padding:6px 0;font:15px/1.45 ${FONT};color:${C.ink2}">${esc(x.nome)}${x.ok ? '' : `<br><span style="color:${C.muted}">${esc(x.fare)}</span>`}</td></tr>`).join('')}</table>` : ''}`) : '';
  const libroLink = `<a href="${LINK.libro}" style="color:${C.ink};font-weight:700">Hotel Positioning (Italian edition), on Amazon</a>`;
  const uscite = verde
    ? card(`${p('<b>What now?</b>')}${p('Send this report to your agency: the points above can be fixed with the one-line instructions. Your message holds: that\'s rare, and worth saying.')}${p('If you\'d like to talk it through with me before launching the campaign, reply to this email.')}${p(`The method is in the book, available in Italian: ${libroLink}.`, 'margin:0')}`, C.sabbia)
    : card(`${p('<b>What now?</b>')}${p('Send this report to your agency: speed and proof can be fixed in a few days, following the instructions above.')}${p('The message is a different matter. A button won\'t fix it: you need to find what makes your hotel different, starting from your guests\' reviews. Two routes, your choice:')}${p('<b>If you want me to do it:</b> the positioning analysis, delivered in English.', 'margin:0 0 12px')}<p style="margin:0 0 16px">${btn('Discover the positioning analysis', LINK.analisi)}</p>${p(`<b>If you want the method:</b> the book, available in Italian: ${libroLink}.`)}${p('If you\'d like to talk it through with me, reply to this email: I read it myself.', 'margin:0')}`, C.sabbia);
  const html = `<div style="background:${C.crema};padding:24px 12px"><div style="max-width:600px;margin:0 auto">
<p style="margin:0 0 4px;font:700 13px/1.3 ${TITOLI};letter-spacing:.04em;text-transform:uppercase;color:${C.muted}">Tagliando Hotel · Hotel Positioning</p>
<p style="margin:0 0 6px;font:800 30px/1.1 ${TITOLI};color:${C.ink}">${esc(rep.hotel)}</p>
<p style="margin:0 0 22px;font:14px/1.5 ${FONT};color:${C.muted}"><a href="${esc(rep.url)}" style="color:${C.muted}">${esc(rep.url.replace(/^https?:\/\//, '').replace(/\/$/, ''))}</a> · ${esc(rep.data)} · read on mobile</p>
${verdetto}
${card(`${h('The three traffic lights')}<table role="presentation" cellpadding="0" cellspacing="0" style="width:100%;border-collapse:collapse">${semafori}</table>`)}
${principale}${ai}${frasi}${altri}${uscite}
${p(`Francesco Astolfi<br><span style="color:${C.muted}">Hotel Positioning</span>`, 'margin-top:22px')}
<p style="margin:18px 0 0;font:12px/1.5 ${FONT};color:${C.muted}">You received this report because you requested Tagliando Hotel at hotelpositioning.com/en/tagliando. Speed is measured with Google PageSpeed Insights on mobile; message, proof and the AI reading come from the text of the page, read by an artificial intelligence.</p>
</div></div>`;
  const txt = [
    `Tagliando Hotel · ${rep.hotel}`, `${rep.url} · ${rep.data}`, '',
    ...(rep.verdetto ? ['Does your page deserve an ad budget?', rep.verdetto.titolo, rep.verdetto.testo, ''] : []),
    ...['messaggio', 'prove', 'velocita'].map((k) => `${NOMI[k]}: ${ETICHETTE[s[k]]}. ${rep.frasiSemaforo[k]}`), '',
    ...(rep.principale ? [`The main problem: ${rep.principale.titolo}`, rep.principale.prova, `What it costs you: ${rep.principale.cosa_costa}`, ''] : []),
    ...(a ? ['How AI reads you: ' + AIE[a.esito], `Asked “Why choose this hotel?”, an AI answers: “${a.risposta}”`, `Benefits understood: ${a.benefici.join(' · ') || 'none that are concrete'}`, `What it didn't understand: ${a.cosaManca}`, ...a.segnali.filter((x) => !x.ok).map((x) => `To fix: ${x.nome}. ${x.fare}`), ''] : []),
    ...(rep.frasiFatte.length ? [`Stock phrases found: ${rep.frasiFatte.join(' · ')}`, ''] : []),
    ...rep.altri.flatMap((x) => [x.titolo, `What to do: ${x.fare}`, '']),
    verde ? `What now? Send this report to your agency. Your message holds. If you'd like to talk it through, reply to this email. The method is in the book (Italian edition): ${LINK.libro}` : `What now? Send this report to your agency: speed and proof can be fixed in a few days. The message is a different matter: you need to find what makes your hotel different. Two routes:\nIf you want me to do it: the positioning analysis, in English ${LINK.analisi}\nIf you want the method: the book (Italian edition) ${LINK.libro}\nIf you'd like to talk it through, reply to this email.`,
    '', 'Francesco Astolfi', 'Hotel Positioning',
  ].join('\n');
  return {
    sender: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    to: [{ email }],
    replyTo: { email: process.env.BREVO_SENDER_EMAIL, name: 'Francesco Astolfi' },
    subject: `Tagliando Hotel: does ${rep.hotel}'s page deserve an ad budget?`,
    tags: ['tagliando-report', 'tagliando-en'],
    htmlContent: html, textContent: txt,
  };
}
