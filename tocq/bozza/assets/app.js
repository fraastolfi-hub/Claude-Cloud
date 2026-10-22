// Tocq · bozza. Solo comportamento dimostrativo: nessun dato viene inviato.

// Menu mobile
document.querySelectorAll('.nav-toggle').forEach(function (btn) {
  btn.addEventListener('click', function () {
    var nav = document.getElementById(btn.getAttribute('aria-controls'));
    var open = nav.classList.toggle('is-open');
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
  });
});

// Orologio del tabellone
document.querySelectorAll('[data-clock]').forEach(function (el) {
  function tick() {
    var d = new Date();
    el.textContent = 'MILANO ' + String(d.getHours()).padStart(2, '0') + ':' + String(d.getMinutes()).padStart(2, '0');
  }
  tick();
  setInterval(tick, 30000);
});

// Filtri della tabella destinazioni
document.querySelectorAll('[data-filters]').forEach(function (group) {
  var target = document.getElementById(group.getAttribute('data-filters'));
  group.addEventListener('click', function (e) {
    var btn = e.target.closest('button');
    if (!btn) return;
    group.querySelectorAll('button').forEach(function (b) { b.setAttribute('aria-pressed', b === btn ? 'true' : 'false'); });
    var f = btn.getAttribute('data-filter');
    target.querySelectorAll('tbody tr').forEach(function (tr) {
      tr.hidden = f !== 'tutti' && (tr.getAttribute('data-tags') || '').indexOf(f) === -1;
    });
  });
});

// Configuratore della notte: riepilogo in tempo reale
var config = document.getElementById('configuratore');
if (config) {
  var out = {
    cuscino: document.getElementById('sum-cuscino'),
    materasso: document.getElementById('sum-materasso'),
    lato: document.getElementById('sum-lato'),
    colazione: document.getElementById('sum-colazione'),
    arrivo: document.getElementById('sum-arrivo')
  };
  var partenza = document.getElementById('cfg-partenza-wrap');
  function update() {
    var data = new FormData(config);
    out.cuscino.textContent = data.get('cuscino') || '—';
    out.materasso.textContent = data.get('materasso') || '—';
    out.lato.textContent = data.get('lato') || '—';
    var col = data.get('colazione');
    partenza.hidden = col !== 'Da asporto';
    out.colazione.textContent = col === 'Da asporto'
      ? 'Da asporto, pronta per le ' + (data.get('partenza') || '—')
      : (col || '—');
    out.arrivo.textContent = data.get('arrivo') || 'Standard';
  }
  config.addEventListener('change', update);
  config.addEventListener('input', update);
  update();
}

// Form: nella bozza mostrano solo la conferma
document.querySelectorAll('form[data-demo]').forEach(function (form) {
  form.addEventListener('submit', function (e) {
    e.preventDefault();
    form.classList.add('is-sent');
    var ok = form.querySelector('.form__ok');
    if (ok) ok.scrollIntoView({ behavior: 'smooth', block: 'center' });
  });
});

// ---------------------------------------------------------------------------
// Rifinitura: comportamenti che rendono l'interfaccia "viva" senza effetti gratuiti
// ---------------------------------------------------------------------------
document.documentElement.classList.add('js');
var riduci = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// Header: filetto solo quando la pagina è scorsa
var header = document.querySelector('.header');
function aggiornaHeader() { if (header) header.classList.toggle('is-scrolled', window.scrollY > 8); }
aggiornaHeader();
window.addEventListener('scroll', aggiornaHeader, { passive: true });

// Le ante del simbolo si aprono sulla foto dell'hero, una volta per sessione
document.querySelectorAll('.doors').forEach(function (el) {
  var vista = false;
  try { vista = sessionStorage.getItem('tocq-ante') === '1'; } catch (e) {}
  if (riduci || vista) { el.classList.add('is-done'); return; }
  var img = el.querySelector('img');
  function apri() {
    requestAnimationFrame(function () { el.classList.add('is-open'); });
    setTimeout(function () { el.classList.add('is-done'); }, 1000);
    try { sessionStorage.setItem('tocq-ante', '1'); } catch (e) {}
  }
  if (img && !img.complete) { img.addEventListener('load', apri, { once: true }); setTimeout(apri, 1200); }
  else setTimeout(apri, 150);
});

// Ingresso dei contenuti: solo per ciò che è sotto la piega, così nulla "lampeggia" all'apertura
if ('IntersectionObserver' in window && !riduci) {
  var io = new IntersectionObserver(function (voci) {
    voci.forEach(function (v) {
      if (v.isIntersecting) { v.target.classList.add('is-in'); io.unobserve(v.target); }
    });
  }, { rootMargin: '0px 0px -8% 0px' });
  document.querySelectorAll('main .section > .wrap > *, main .section > .wrap.split > *, main .section > .wrap.grid-3 > *, main .section > .wrap.grid-4 > *, main .board .wrap').forEach(function (el, i) {
    if (el.getBoundingClientRect().top > window.innerHeight) {
      el.classList.add('reveal');
      el.style.transitionDelay = (i % 3) * 60 + 'ms';
      io.observe(el);
    }
  });
}

// Barra mobile: compare quando i bottoni dell'hero escono dallo schermo, sparisce sopra i form e il footer
var barra = document.querySelector('.sticky-cta');
if (barra && 'IntersectionObserver' in window) {
  var bloccanti = new Set();
  var primoCta = document.querySelector('.hero .btns');
  // i bottoni dell'hero contano finché non sono passati sopra lo schermo (controllo sullo scroll:
  // regge anche i salti diretti alle ancore, che un IntersectionObserver non sempre vede)
  function heroVisibile() { return !!primoCta && primoCta.getBoundingClientRect().bottom > 0; }
  function aggiornaBarra() { barra.classList.toggle('is-visible', !heroVisibile() && bloccanti.size === 0); }
  window.addEventListener('scroll', aggiornaBarra, { passive: true });
  var oss = new IntersectionObserver(function (voci) {
    voci.forEach(function (v) { if (v.isIntersecting) bloccanti.add(v.target); else bloccanti.delete(v.target); });
    aggiornaBarra();
  });
  document.querySelectorAll('main form, .footer').forEach(function (el) { oss.observe(el); });
  aggiornaBarra();
}

// Configuratore: il valore appena cambiato si accende un istante, per dire "ricevuto"
if (config) {
  config.addEventListener('change', function (e) {
    var mappa = { cuscino: 'sum-cuscino', materasso: 'sum-materasso', lato: 'sum-lato', colazione: 'sum-colazione', partenza: 'sum-colazione', arrivo: 'sum-arrivo' };
    var dd = document.getElementById(mappa[e.target.name]);
    if (!dd) return;
    dd.classList.add('is-updated');
    setTimeout(function () { dd.classList.remove('is-updated'); }, 400);
  });
}

// ---------------------------------------------------------------------------
// Percorso (JOURNEY.md)
// ---------------------------------------------------------------------------

// Misura: ogni evento del piano di misurazione finisce nel dataLayer (GA4 / Tag Manager al lancio)
window.dataLayer = window.dataLayer || [];
function traccia(evento, dati) { window.dataLayer.push(Object.assign({ event: evento }, dati || {})); }
document.addEventListener('click', function (e) {
  var a = e.target.closest('a');
  if (!a) return;
  var h = a.getAttribute('href') || '';
  if (h.indexOf('tel:') === 0) traccia('chiamata_reception');
  else if (h.indexOf('#prenota') > -1) traccia('clic_prenota', { da: a.closest('section, header, .sticky-cta') ? (a.closest('section, header, .sticky-cta').id || a.closest('section, header, .sticky-cta').className.split(' ')[0]) : '' });
  else if (h.indexOf('#preventivo') > -1) traccia('clic_preventivo');
  else if (h.indexOf('google.com/maps') > -1) traccia('tragitto_aperto');
});
document.querySelectorAll('form[data-demo]').forEach(function (f) {
  f.addEventListener('submit', function () {
    var fonte = (f.querySelector('input[name="fonte"]') || {}).value || 'prenotazione';
    traccia(fonte.indexOf('preventivo') > -1 ? 'richiesta_preventivo_mice' : fonte.indexOf('download') > -1 ? 'download_presentazione' : 'invio_form', { fonte: fonte });
  });
});

// Il bivio: l'intenzione riordina la home e la barra mobile, e resta ricordata per la visita
var bivio = document.querySelector('.intent');
if (bivio) {
  var sale = document.getElementById('sale');
  var postoEvento = document.getElementById('posto-sale-evento');
  var postoSoggiorno = document.getElementById('posto-sale-soggiorno');
  function applicaIntento(v, daUtente) {
    if (sale && postoEvento && postoSoggiorno) {
      if (v === 'evento') postoEvento.parentNode.insertBefore(sale, postoEvento);
      else postoSoggiorno.parentNode.insertBefore(sale, postoSoggiorno);
    }
    document.querySelectorAll('[data-percorso]').forEach(function (c) { c.setAttribute('data-attivo', c.getAttribute('data-percorso') === v ? 'true' : 'false'); });
    var barraM = document.querySelector('.sticky-cta');
    if (barraM) {
      var prenota = barraM.querySelector('a[href*="#prenota"]');
      var prev = barraM.querySelector('a[href*="#preventivo"]');
      if (v === 'evento') { barraM.insertBefore(prev, prenota); prev.className = 'btn btn--primary'; prenota.className = 'btn'; }
      else { barraM.insertBefore(prenota, prev); prenota.className = 'btn btn--primary'; prev.className = 'btn'; }
    }
    try { localStorage.setItem('tocq-intento', v); } catch (e) {}
    if (daUtente) traccia('intenzione_scelta', { intenzione: v });
  }
  var salvato = null;
  try { salvato = localStorage.getItem('tocq-intento'); } catch (e) {}
  if (salvato === 'evento' || salvato === 'soggiorno') {
    var r = bivio.querySelector('input[value="' + salvato + '"]');
    if (r) r.checked = true;
    applicaIntento(salvato, false);
  } else applicaIntento('soggiorno', false);
  bivio.addEventListener('change', function (e) { applicaIntento(e.target.value, true); });
}

// Indicatore dell'ora: segue il capitolo più presente nello schermo
var ora = document.querySelector('.ora-capitolo');
if (ora && 'IntersectionObserver' in window) {
  var attivi = new Map();
  var oraTxt = ora.querySelector('.ora-capitolo__ora');
  var nomeTxt = ora.querySelector('.ora-capitolo__nome');
  var ossOra = new IntersectionObserver(function (voci) {
    voci.forEach(function (v) { if (v.isIntersecting) attivi.set(v.target, v.intersectionRatio); else attivi.delete(v.target); });
    var migliore = null, max = 0;
    attivi.forEach(function (r, el) { if (r > max) { max = r; migliore = el; } });
    if (migliore) {
      oraTxt.textContent = migliore.getAttribute('data-ora');
      nomeTxt.textContent = migliore.getAttribute('data-capitolo');
      ora.classList.toggle('is-notte', migliore.classList.contains('section--dark'));
    }
    ora.classList.toggle('is-visible', !!migliore);
  }, { threshold: [0, .25, .5, .75] });
  document.querySelectorAll('[data-ora]').forEach(function (c) { ossOra.observe(c); });
}

// Configuratore breve: riepilogo e passaggio delle scelte alla pagina camere
var mini = document.getElementById('mini-config');
if (mini) {
  var riep = document.getElementById('mini-riepilogo');
  var vai = document.getElementById('mini-vai');
  function aggiornaMini() {
    var d = new FormData(mini);
    var lato = d.get('lato') === 'Corte interna, silenziosa' ? 'Corte, silenziosa' : d.get('lato');
    riep.textContent = [d.get('cuscino'), lato, d.get('colazione')].join(' · ');
    var q = new URLSearchParams({ cuscino: d.get('cuscino'), lato: d.get('lato'), colazione: d.get('colazione') });
    vai.href = 'camere.html?' + q.toString() + '#configura';
  }
  mini.addEventListener('change', function () { aggiornaMini(); traccia('uso_configuratore', { dove: 'home' }); });
  aggiornaMini();
}

// Pagina camere: le scelte arrivate dalla home precompilano il configuratore
if (config && location.search) {
  var p = new URLSearchParams(location.search);
  ['cuscino', 'lato', 'colazione'].forEach(function (k) {
    var v = p.get(k);
    if (!v) return;
    var r = config.querySelector('input[name="' + k + '"][value="' + v.replace(/"/g, '') + '"]');
    if (r) r.checked = true;
  });
  config.dispatchEvent(new Event('change'));
}
if (config) config.addEventListener('change', function (e) { if (e.isTrusted) traccia('uso_configuratore', { dove: 'camere' }); });

// Squadra: un nome apre la citazione che lo riguarda
var nomi = document.querySelectorAll('.names--interattivi button');
nomi.forEach(function (b, i) {
  b.setAttribute('aria-pressed', i === 0 ? 'true' : 'false');
  b.addEventListener('click', function () {
    nomi.forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    document.querySelectorAll('.citazioni .quote').forEach(function (q) { q.classList.toggle('is-attiva', q.getAttribute('data-id') === b.getAttribute('data-citazione')); });
  });
});

// La porta aperta: le ante si aprono quando la call to action finale entra nello schermo
var finale = document.querySelector('.finale');
if (finale) {
  if ('IntersectionObserver' in window && !riduci) {
    new IntersectionObserver(function (v, o) { if (v[0].isIntersecting) { finale.classList.add('is-aperta'); o.disconnect(); } }, { threshold: .35 }).observe(finale);
  } else finale.classList.add('is-aperta');
}

// Meeting: "Quante persone siete?" accende le sale giuste e precompila il preventivo
var range = document.getElementById('persone-range');
if (range) {
  var out = document.getElementById('persone-out');
  var esito = document.getElementById('persone-esito');
  var cta = document.getElementById('persone-cta');
  var nomiAll = { platea: 'platea', scuola: 'banchi di scuola', ferro: 'ferro di cavallo', tavolo: 'tavolo unico', cabaret: 'cabaret', cocktail: 'in piedi' };
  var colonne = { platea: 3, scuola: 4, ferro: 5, tavolo: 6, cabaret: 7, cocktail: 8 };
  function aggiornaPersone() {
    var n = +range.value;
    out.textContent = n;
    var adatte = [];
    document.querySelectorAll('tr[data-sala]').forEach(function (tr) {
      var ok = [];
      Object.keys(nomiAll).forEach(function (k) {
        var cella = tr.children[colonne[k]];
        var cap = +tr.getAttribute('data-' + k);
        var va = cap >= n;
        if (cella) cella.classList.toggle('is-ok', va);
        if (va) ok.push(nomiAll[k]);
      });
      tr.classList.toggle('is-adatta', ok.length > 0);
      tr.classList.toggle('is-esclusa', ok.length === 0);
      if (ok.length) adatte.push('<b>' + tr.getAttribute('data-sala') + '</b> (' + ok.join(', ') + ')');
    });
    esito.innerHTML = adatte.length
      ? 'Per ' + n + ' persone: ' + adatte.join(' · ') + '.'
      : 'Per ' + n + ' persone in un allestimento solo serve unire più spazi: scrivici e ti proponiamo la soluzione.';
    // la sala proposta è la più piccola che basta, non la più grande
    var prima = [].slice.call(document.querySelectorAll('tr.is-adatta')).sort(function (x, y) { return (+x.getAttribute('data-platea')) - (+y.getAttribute('data-platea')); })[0];
    cta.textContent = prima ? 'Preventivo per ' + n + ' persone in Sala ' + prima.getAttribute('data-sala') : 'Preventivo per ' + n + ' persone';
  }
  range.addEventListener('input', aggiornaPersone);
  range.addEventListener('change', function () { traccia('selettore_persone', { persone: +range.value }); });
  cta.addEventListener('click', function () {
    var campo = document.getElementById('p-persone');
    if (campo) campo.value = range.value;
  });
  aggiornaPersone();
}

// Posizione: "Dove devi andare domani?" risponde con mezzo e tempo presi dalla tabella
var dove = document.getElementById('dove');
if (dove) {
  var righe = document.querySelectorAll('#dest tbody tr');
  righe.forEach(function (tr, i) {
    var o = document.createElement('option');
    o.value = i;
    o.textContent = tr.children[0].textContent.trim();
    dove.appendChild(o);
  });
  var box = document.getElementById('finder-esito');
  dove.addEventListener('change', function () {
    if (dove.value === '') { box.hidden = true; return; }
    var tr = righe[+dove.value];
    var nome = tr.children[0].textContent.trim();
    var come = tr.children[2].textContent.trim();
    var tempo = tr.children[3].textContent.trim();
    box.querySelector('.finder__risposta').innerHTML = '<b>' + nome + '</b><br>' + come + ' · ' + tempo + ' dal Tocq.';
    box.hidden = false;
    traccia('destinazione_cercata', { destinazione: nome });
  });
}

// Prenotazione: apre il motore ufficiale Blastness con le date scelte (stesso collegamento della pagina concerti del Tocq)
var prenotaForm = document.getElementById('prenota-form');
if (prenotaForm) {
  var oggi = new Date();
  function isoData(d) { return d.toISOString().slice(0, 10); }
  var arrivo = document.getElementById('b-in'), partenza = document.getElementById('b-out');
  if (arrivo && !arrivo.value) { arrivo.value = isoData(oggi); arrivo.min = isoData(oggi); }
  if (partenza && !partenza.value) { var dom = new Date(oggi); dom.setDate(dom.getDate() + 1); partenza.value = isoData(dom); }
  if (arrivo && partenza) arrivo.addEventListener('change', function () {
    if (partenza.value <= arrivo.value) { var d = new Date(arrivo.value); d.setDate(d.getDate() + 1); partenza.value = isoData(d); }
    partenza.min = arrivo.value;
  });
  var vai = document.getElementById('b-vai');
  function aggiornaLink() {
    var q = new URLSearchParams({
      id_albergo: '16496', dc: '6326', language: 'it', currency: 'EUR',
      checkin_date: arrivo.value, checkout_date: partenza.value,
      rooms: '1', adults_1: document.getElementById('b-ad').value, children_1: '0'
    });
    var codice = (document.getElementById('b-code') || {}).value;
    if (codice) q.set('promo_code', codice); // nome del parametro da verificare con Blastness
    vai.href = 'https://book.blastness.com/results?' + q.toString();
  }
  prenotaForm.addEventListener('input', aggiornaLink);
  prenotaForm.addEventListener('change', aggiornaLink);
  prenotaForm.addEventListener('submit', function (e) { e.preventDefault(); });
  vai.addEventListener('click', function () { traccia('prenotazione_avviata', { checkin: arrivo.value, checkout: partenza.value }); });
  aggiornaLink();
}
