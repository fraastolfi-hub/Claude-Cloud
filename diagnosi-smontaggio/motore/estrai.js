// Estrazione della prima schermata di una homepage (SPEC.md, "Estrazione della prima schermata").
// leggiSchermata gira dentro il browser: non può usare nulla definito fuori dalla funzione.

export const VIEWPORT = {
  desktop: { width: 1366, height: 768 },
  mobile: { width: 390, height: 844 },
};

export function leggiSchermata(vh) {
  const pulisci = t => (t || '').replace(/\s+/g, ' ').trim();
  const parole = t => pulisci(t).split(' ').filter(Boolean).length;

  // I banner cookie li nasconde estraiDaPagina prima della lettura: li chiude ogni visitatore.
  // Popup, newsletter e finestre modali restano: coprono davvero il hero.
  const OVERLAY = '[id*=cookie i],[class*=cookie i],[id*=iubenda i],[class*=iubenda i],[id*=onetrust i],[class*=onetrust i],' +
    '[class*=consent i],[id*=consent i],[role=dialog],[aria-modal=true],[class*=modal i],[class*=popup i],[class*=newsletter i]';
  const ESCLUSI = OVERLAY + ',nav,[role=navigation],form,button,[role=button],select,input,textarea,label,footer';
  // Elementi fissi sullo schermo: barre, chat, notifiche, pannelli laterali. Non sono testo del hero.
  const fisso = el => {
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const pos = getComputedStyle(e).position;
      if (pos === 'fixed' || pos === 'sticky') return true;
    }
    return false;
  };
  const lettere = t => (t.match(/\p{L}/gu) || []).length;

  const nascosto = el => {
    for (let e = el; e && e !== document.body; e = e.parentElement) {
      const s = getComputedStyle(e);
      if (s.display === 'none' || s.visibility === 'hidden' || parseFloat(s.opacity) < 0.05) return true;
    }
    return false;
  };
  const inSchermata = el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0 && r.top < vh && r.bottom > 0 && r.left < innerWidth && r.right > 0;
  };
  const visibile = el => inSchermata(el) && !nascosto(el);
  const pieno = colore => {
    const m = (colore || '').match(/rgba?\(([^)]+)\)/);
    if (!m) return false;
    const p = m[1].split(',').map(Number);
    return p.length < 4 || p[3] > 0.3;
  };

  // Testi del hero: elementi senza figli a blocco, fuori da menu, moduli, pulsanti e popup.
  // I testi dentro un link contano solo se lunghi (un link corto è un pulsante o una voce di menu).
  const BLOCCHI = ['DIV', 'P', 'H1', 'H2', 'H3', 'H4', 'H5', 'H6', 'UL', 'OL', 'SECTION', 'ARTICLE'];
  const blocchi = [];
  const visti = new Set();
  document.querySelectorAll('h1,h2,h3,h4,h5,h6,p,div,span,li,strong,em,small,a').forEach(e => {
    if (e.tagName !== 'H1' && (e.closest(ESCLUSI) || fisso(e))) return;
    if ([...e.children].some(c => BLOCCHI.includes(c.tagName))) return;
    const testo = pulisci(e.innerText);
    if (testo.length < 3 || visti.has(testo)) return;
    // Il testo dentro un link è un pulsante o una voce di menu, salvo che sia un titolo (slide cliccabili).
    if (e.tagName !== 'H1' && e.closest('a') && !e.closest('h1,h2,h3') && !e.querySelector('h1,h2,h3')) return;
    // Contenitori fatti solo di link o pulsanti (es. una riga con due CTA) non sono testo del hero.
    const testoLink = [...e.querySelectorAll('a,button')].map(x => pulisci(x.innerText)).join(' ');
    if (testoLink && testo.replace(/\s/g, '').length - testoLink.replace(/\s/g, '').length < 3) return;
    if (!visibile(e)) return;
    visti.add(testo);
    const r = e.getBoundingClientRect();
    blocchi.push({ testo: testo.slice(0, 300), fs: parseFloat(getComputedStyle(e).fontSize), top: Math.round(r.top), el: e });
  });
  blocchi.sort((a, b) => a.top - b.top);

  // Headline: h1 visibile, altrimenti il blocco di almeno 3 parole con il font più grande.
  const h1s = [...document.querySelectorAll('h1')];
  const h1Vis = h1s.find(h => visibile(h) && !h.closest(OVERLAY) && pulisci(h.innerText).length > 2);
  let headline = null;
  if (h1Vis) {
    headline = { testo: pulisci(h1Vis.innerText), fs: parseFloat(getComputedStyle(h1Vis).fontSize), top: Math.round(h1Vis.getBoundingClientRect().top), el: h1Vis };
  } else {
    const candidati = blocchi.filter(b => parole(b.testo) >= 3 && parole(b.testo) <= 20);
    headline = candidati.sort((a, b) => b.fs - a.fs || a.top - b.top)[0] || null;
  }

  const dentroHeadline = b => headline && (headline.el.contains(b.el) || b.el.contains(headline.el) ||
    headline.testo.includes(b.testo) || b.testo === headline.testo);
  const altri = blocchi.filter(b => !dentroHeadline(b) && parole(b.testo) >= 2);
  const sotto = headline ? altri.filter(b => b.top > headline.top && parole(b.testo) >= 3) : [];
  const sottotitolo = sotto.length ? sotto[0] : null;
  const supporto = altri.filter(b => b !== sottotitolo && b.fs >= 11).map(b => b.testo)
    .filter(t => !(sottotitolo && (sottotitolo.testo.includes(t) || t.includes(sottotitolo.testo)))).slice(0, 8);

  let fraseVisibile = false;
  if (headline) {
    const r = headline.el.getBoundingClientRect();
    const x = Math.min(innerWidth - 1, Math.max(0, r.left + r.width / 2));
    const y = Math.min(vh - 1, Math.max(0, r.top + Math.min(r.height, 40) / 2));
    const colpito = document.elementFromPoint(x, y);
    const coperta = colpito && !headline.el.contains(colpito) && !colpito.contains(headline.el) && colpito.closest(OVERLAY);
    fraseVisibile = !coperta;
  }
  const fsMax = Math.max(0, ...altri.map(b => b.fs));
  const headlinePiuGrande = !!headline && headline.fs >= fsMax;

  // Pulsanti: principali se hanno uno sfondo pieno (sull'elemento o sul primo figlio).
  // Bordo senza sfondo o link testuale = secondario. Telefono, email e lingue non contano.
  const pulsanti = [];
  const testiPulsanti = new Set();
  document.querySelectorAll('a,button,input[type=submit]').forEach(e => {
    if (e.closest(OVERLAY) || e.closest('nav,[role=navigation]')) return;
    if (!visibile(e)) return;
    const testo = pulisci(e.innerText || e.value);
    const href = e.getAttribute('href') || '';
    if (!testo || lettere(testo) < 2 || parole(testo) > 7 || /^(tel|mailto):/.test(href)) return;
    // Un link grande quanto una slide non è un pulsante; uno di pochi pixel è un link nascosto per l'accessibilità.
    const box = e.getBoundingClientRect();
    if (box.height > 0.3 * vh || box.width < 10 || box.height < 10) return;
    const chiave = testo.toLowerCase();
    if (testiPulsanti.has(chiave)) return;
    testiPulsanti.add(chiave);
    const figlio = e.firstElementChild;
    const principale = pieno(getComputedStyle(e).backgroundColor) || (figlio && pieno(getComputedStyle(figlio).backgroundColor));
    const r = e.getBoundingClientRect();
    pulsanti.push({ testo, principale: !!principale, top: Math.round(r.top), left: Math.round(r.left), inModulo: !!e.closest('form') });
  });

  const campoData = [...document.querySelectorAll('input,select')].find(i => visibile(i) && !i.closest(OVERLAY) &&
    (i.type === 'date' || /date|data|arriv|check.?in|partenz|dates/i.test([i.name, i.placeholder, i.getAttribute('aria-label'), i.id].join(' '))));
  const moduloDate = !!campoData;
  const moduloEl = campoData ? campoData.closest('form') : null;
  // Il pulsante accanto al campo date fa parte del modulo di prenotazione.
  const rigaDate = campoData ? campoData.getBoundingClientRect().top : null;
  const principali = pulsanti.filter(p => p.principale && !(moduloEl && p.inModulo) && !(rigaDate !== null && Math.abs(p.top - rigaDate) < 150));
  const ordinati = principali.sort((a, b) => a.top - b.top || a.left - b.left);

  const testoSchermata = blocchi.map(b => b.testo).join(' \n ');
  const fuoriH1 = h1s.filter(h => h !== h1Vis).map(h => pulisci(h.innerText)).filter(Boolean);

  return {
    headline: headline ? headline.testo : '',
    sottotitolo: sottotitolo ? sottotitolo.testo : '',
    supporto,
    frase_visibile: fraseVisibile && !!headline,
    headline_piu_grande: headlinePiuGrande,
    pulsanti: pulsanti.map(({ testo, principale }) => ({ testo, principale })),
    cta_primari: principali.length + (moduloDate ? 1 : 0),
    cta_testo: ordinati.length ? ordinati[0].testo : '',
    modulo_date: moduloDate,
    testo_schermata: testoSchermata,
    h1_fuori: fuoriH1,
  };
}

// Riprova sociale in tutta la pagina, con la posizione in schermate dall'inizio.
export function cercaProve(vh) {
  const pulisci = t => (t || '').replace(/\s+/g, ' ').trim();
  const VOTO = /\d[.,]\d\s*(\/\s*(10|5)|su 10|su 5|★)|\b\d{2,}\s+(recensioni|reviews|valutazioni)|superb\s+\d|eccellente\s+\d/i;
  const RICON = /travellers.?\s*choice|michelin|gambero rosso|guida blu|5 vele|bandiera blu|award|premio|premiat|miglior hotel|best hotel/i;
  const PIATTAFORMA = /^(tripadvisor|booking(\.com)?|holidaycheck|trustyou)$/i;
  const RUMORE = /recaptcha|privacy|cookie|termini|terms/i;
  const salta = e => !!e.closest('[id*=cookie i],[class*=cookie i],[id*=iubenda i],[class*=iubenda i],[id*=onetrust i],[class*=consent i],[role=dialog],[aria-modal=true]');
  const prove = [];
  document.querySelectorAll('body *').forEach(e => {
    if (salta(e)) return;
    const proprio = pulisci([...e.childNodes].filter(n => n.nodeType === 3).map(n => n.textContent).join(' '));
    const img = e.tagName === 'IMG' ? pulisci(e.alt + ' ' + e.src) : '';
    const testo = proprio || img;
    if (!testo) return;
    const r = e.getBoundingClientRect();
    if (r.height === 0) return;
    const s = getComputedStyle(e);
    if (s.display === 'none' || s.visibility === 'hidden') return;
    if (RUMORE.test(testo)) return;
    // Il voto spesso è spezzato in più elementi: si legge il testo dei contenitori fino a tre livelli sopra.
    let contesto = testo;
    for (let x = e.parentElement, i = 0; x && i < 3; x = x.parentElement, i++) {
      const t = pulisci(x.innerText);
      if (t.length > 300) break;
      contesto = t;
    }
    // Loghi delle piattaforme di recensioni; le icone del sito (es. "Booking" sul pulsante prenota) non contano.
    const piattaforma = PIATTAFORMA.test(proprio) || (/tripadvisor|booking\.com|holidaycheck/i.test(img) && !/icons?\//i.test(img));
    const tipo = VOTO.test(testo) || ((piattaforma || RICON.test(contesto)) && VOTO.test(contesto)) ? 'voto'
      : RICON.test(testo) || piattaforma ? 'riconoscimento' : null;
    if (!tipo) return;
    const vicino = pulisci((e.parentElement || e).innerText).slice(0, 160) || testo;
    const schermate = +((r.top + scrollY) / vh).toFixed(2);
    if (schermate < 0) return;
    prove.push({ tipo, testo: vicino, schermate });
  });
  return prove.sort((a, b) => a.schermate - b.schermate).slice(0, 12);
}

export async function estraiDaPagina(page) {
  const title = await page.title();
  const meta = await page.evaluate(() => (document.querySelector('meta[name=description]') || {}).content || '');
  const risultato = { title, meta };
  await page.addStyleTag({ content: '[id*=cookie i],[class*=cookie i],[id*=iubenda i],[class*=iubenda i],[id*=onetrust i],[class*=onetrust i],[class*=consent i],[id*=consent i],[id*=cmp i]{display:none!important}' }).catch(() => {});
  for (const [nome, vp] of Object.entries(VIEWPORT)) {
    await page.setViewportSize(vp);
    // Scorre la pagina per far caricare i contenuti pigri, poi torna in cima.
    for (let y = 0; y < 8000; y += 700) {
      await page.evaluate(yy => window.scrollTo(0, yy), y);
      await page.waitForTimeout(120);
    }
    const prove = await page.evaluate(cercaProve, vp.height);
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.waitForTimeout(2500);
    const schermata = await page.evaluate(leggiSchermata, vp.height);
    const seconda = await page.evaluate(vh => {
      const pulisci = t => (t || '').replace(/\s+/g, ' ').trim();
      const testi = [];
      document.querySelectorAll('h1,h2,h3,p,li,strong').forEach(e => {
        const r = e.getBoundingClientRect();
        if (r.top >= vh && r.top < 2 * vh && r.height > 0) testi.push(pulisci(e.innerText));
      });
      return [...new Set(testi)].filter(t => t.length > 3).slice(0, 20);
    }, vp.height);
    risultato[nome] = { ...schermata, prove, seconda_schermata: seconda };
  }
  return risultato;
}

export async function estrai(url) {
  const { chromium } = await import('playwright');
  const browser = await chromium.launch();
  try {
    const context = await browser.newContext({ locale: 'it-IT' });
    const page = await context.newPage();
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    await page.waitForTimeout(3000);
    return { url, ...(await estraiDaPagina(page)) };
  } finally {
    await browser.close();
  }
}
