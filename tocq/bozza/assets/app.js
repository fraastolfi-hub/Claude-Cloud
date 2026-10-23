// Tocq · bozza. Solo comportamento dimostrativo: nessun dato viene inviato.

// Menu mobile: si apre a tutto schermo, le voci entrano una dopo l'altra; si chiude con Esc o scegliendo una voce
document.querySelectorAll('.nav-toggle').forEach(function (btn) {
  var nav = document.getElementById(btn.getAttribute('aria-controls'));
  var testo = btn.querySelector('.nav-toggle__testo');
  [].forEach.call(nav.children, function (el, i) { el.style.setProperty('--i', i); });
  function imposta(open) {
    nav.classList.toggle('is-open', open);
    document.documentElement.classList.toggle('menu-aperto', open);
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (testo) testo.textContent = btn.getAttribute(open ? 'data-chiudi' : 'data-apri');
    if (open) traccia('menu_aperto', {});
  }
  btn.addEventListener('click', function () { imposta(!nav.classList.contains('is-open')); });
  nav.addEventListener('click', function (e) { var a = e.target.closest('a[href]'); if (a && nav.classList.contains('is-open')) imposta(false); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && nav.classList.contains('is-open')) { imposta(false); btn.focus(); } });
  window.addEventListener('resize', function () { if (window.innerWidth > 920 && nav.classList.contains('is-open')) imposta(false); });
});

// Note di lavoro della bozza ("da confermare"): nascoste per leggere il sito come un ospite,
// si mostrano con il pulsante nel footer o con ?note=1 nell'indirizzo, e la scelta resta ricordata
(function () {
  var mostra = /[?&]note=1/.test(location.search);
  try { mostra = mostra || localStorage.getItem('tocq-note') === '1'; } catch (e) {}
  function imposta(v) {
    document.documentElement.classList.toggle('mostra-note', v);
    document.querySelectorAll('.note-toggle').forEach(function (b) { b.setAttribute('aria-pressed', v ? 'true' : 'false'); b.textContent = v ? 'Nascondi le note di lavoro' : 'Mostra le note di lavoro'; });
    try { localStorage.setItem('tocq-note', v ? '1' : '0'); } catch (e) {}
  }
  imposta(mostra);
  document.addEventListener('click', function (e) { if (e.target.closest('.note-toggle')) imposta(!document.documentElement.classList.contains('mostra-note')); });
})();

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

// Barra mobile: Prenota e Chiama sempre in fondo allo schermo; si toglie solo mentre si scrive in un campo,
// perché la tastiera la spingerebbe sopra il form
var barra = document.querySelector('.sticky-cta');
if (barra) {
  barra.classList.add('is-visible');
  document.addEventListener('focusin', function (e) { if (e.target.matches('input, textarea, select')) barra.classList.remove('is-visible'); });
  document.addEventListener('focusout', function () { barra.classList.add('is-visible'); });
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
  else if (a.hasAttribute('data-chiama')) traccia('clic_chiama', { da: 'barra_mobile' });
  else if (a.hasAttribute('data-prenota') || h.indexOf('#prenota') > -1) traccia('clic_prenota', { da: a.closest('section, header, .sticky-cta') ? (a.closest('section, header, .sticky-cta').id || a.closest('section, header, .sticky-cta').className.split(' ')[0]) : '' });
  else if (h.indexOf('#preventivo') > -1) traccia('clic_preventivo');
  else if (h.indexOf('google.com/maps') > -1) traccia('tragitto_aperto');
});
document.querySelectorAll('form[data-demo]').forEach(function (f) {
  f.addEventListener('submit', function () {
    var fonte = (f.querySelector('input[name="fonte"]') || {}).value || 'prenotazione';
    traccia(fonte.indexOf('preventivo') > -1 ? 'richiesta_preventivo_mice' : fonte.indexOf('download') > -1 ? 'download_presentazione' : 'invio_form', { fonte: fonte });
  });
});

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
      id_albergo: '16496', dc: '6326', id_stile: '21247', language: (document.documentElement.lang || 'it').slice(0, 2), currency: 'EUR',
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

// Hero: quando il video sarà pronto basta indicarne il file in data-video-mp4 / data-video-webm.
// Il video parte muto e in loop solo se l'utente non ha chiesto meno movimento né risparmio dati; la foto resta come poster.
document.querySelectorAll('[data-video-mp4]').forEach(function (box) {
  var mp4 = box.getAttribute('data-video-mp4'), webm = box.getAttribute('data-video-webm');
  var risparmio = navigator.connection && navigator.connection.saveData;
  if (!(mp4 || webm) || riduci || risparmio) return;
  var img = box.querySelector('img');
  var v = document.createElement('video');
  v.className = 'hero-full__video';
  v.muted = true; v.loop = true; v.autoplay = true; v.playsInline = true; v.setAttribute('playsinline', '');
  v.setAttribute('aria-hidden', 'true');
  if (img) v.poster = img.currentSrc || img.src;
  if (webm) { var s1 = document.createElement('source'); s1.src = webm; s1.type = 'video/webm'; v.appendChild(s1); }
  if (mp4) { var s2 = document.createElement('source'); s2.src = mp4; s2.type = 'video/mp4'; v.appendChild(s2); }
  box.appendChild(v);
  var btn = document.createElement('button');
  btn.type = 'button'; btn.className = 'hero-full__pausa'; btn.textContent = 'Pausa';
  btn.addEventListener('click', function () { if (v.paused) { v.play(); btn.textContent = 'Pausa'; } else { v.pause(); btn.textContent = 'Riproduci'; } });
  box.parentNode.appendChild(btn);
});

// Trustindex: il widget si carica solo quando la sezione si avvicina allo schermo, così non pesa sulla prima schermata.
// Uso: data-trustindex="ID_DEL_WIDGET" (il codice che Trustindex dà nello snippet loader.js?ID).
document.querySelectorAll('[data-trustindex]').forEach(function (box) {
  var id = box.getAttribute('data-trustindex');
  if (!id) return;
  function carica() {
    var s = document.createElement('script');
    s.src = 'https://cdn.trustindex.io/loader.js?' + encodeURIComponent(id);
    s.defer = true; s.async = true;
    box.appendChild(s);
    box.classList.add('is-live');
    traccia('recensioni_live_caricate');
  }
  if ('IntersectionObserver' in window) {
    new IntersectionObserver(function (v, o) { if (v[0].isIntersecting) { o.disconnect(); carica(); } }, { rootMargin: '600px 0px' }).observe(box);
  } else carica();
});

// Il quartiere: mappa vera da trascinare e ingrandire, temi, punti ed elenco evidenziati insieme
var qmap = document.querySelector('.qmap');
if (qmap) {
  var vista = qmap.querySelector('.qmap__vista'), piano = qmap.querySelector('.qmap__piano');
  var LATO = +qmap.getAttribute('data-lato'), HX = +qmap.getAttribute('data-hx'), HY = +qmap.getAttribute('data-hy');
  var puntiQ = [].slice.call(qmap.querySelectorAll('.qmap__punto'));
  var vociQ = [].slice.call(document.querySelectorAll('.poi'));
  var st = { k: 1, x: 0, y: 0 }, MAXK = 2.4;
  function pos(el) { return { x: parseFloat(el.style.left), y: parseFloat(el.style.top) }; }
  function minK() { return Math.max(vista.clientWidth, vista.clientHeight) / LATO; }
  function limita() {
    var w = vista.clientWidth, h = vista.clientHeight;
    st.k = Math.min(MAXK, Math.max(minK(), st.k));
    st.x = Math.min(0, Math.max(w - LATO * st.k, st.x));
    st.y = Math.min(0, Math.max(h - LATO * st.k, st.y));
  }
  function disegna(anima) {
    limita();
    piano.style.transition = anima && !riduci ? 'transform .45s cubic-bezier(.2,.7,.2,1)' : 'none';
    piano.style.transform = 'translate(' + st.x + 'px,' + st.y + 'px) scale(' + st.k + ')';
    piano.style.setProperty('--k', st.k);
    qmap.classList.toggle('is-vicino', st.k > 1.15);
  }
  function zoomIn(f, cx, cy, anima) {
    var k2 = Math.min(MAXK, Math.max(minK(), st.k * f));
    st.x = cx - (cx - st.x) * k2 / st.k; st.y = cy - (cy - st.y) * k2 / st.k; st.k = k2;
    disegna(anima);
  }
  function inquadra(punti, anima) {
    var xs = [HX], ys = [HY];
    punti.forEach(function (p) { var c = pos(p); xs.push(c.x); ys.push(c.y); });
    var x0 = Math.min.apply(null, xs), x1 = Math.max.apply(null, xs), y0 = Math.min.apply(null, ys), y1 = Math.max.apply(null, ys);
    var w = vista.clientWidth, h = vista.clientHeight, pad = 70;
    st.k = Math.min(1.6, (w - pad * 2) / Math.max(x1 - x0, 1), (h - pad * 2) / Math.max(y1 - y0, 1));
    st.k = Math.max(minK(), st.k);
    st.x = w / 2 - (x0 + x1) / 2 * st.k; st.y = h / 2 - (y0 + y1) / 2 * st.k;
    disegna(anima);
  }
  function inVista(el) {
    var c = pos(el), x = st.x + c.x * st.k, y = st.y + c.y * st.k;
    return x > 40 && y > 40 && x < vista.clientWidth - 40 && y < vista.clientHeight - 40;
  }
  function seleziona(id, daMappa) {
    var punto = null;
    puntiQ.forEach(function (p) { var si = p.getAttribute('data-id') === id; p.classList.toggle('is-attivo', si); if (si) punto = p; });
    vociQ.forEach(function (li) {
      var si = li.getAttribute('data-id') === id;
      li.classList.toggle('is-attivo', si);
      if (si && daMappa) { var l = li.parentNode; l.scrollTo({ top: li.offsetTop - l.offsetTop - 40, behavior: riduci ? 'auto' : 'smooth' }); }
    });
    if (punto && !daMappa && !inVista(punto)) {
      var c = pos(punto);
      st.x = vista.clientWidth / 2 - c.x * st.k; st.y = vista.clientHeight / 2 - c.y * st.k; disegna(true);
    }
  }
  // trascinamento con mouse o dito, pizzico con due dita
  var dita = {}, mosso = 0, pizzico = null;
  vista.addEventListener('pointerdown', function (e) {
    dita[e.pointerId] = { x: e.clientX, y: e.clientY }; mosso = 0;
  });
  vista.addEventListener('pointermove', function (e) {
    var d = dita[e.pointerId]; if (!d) return;
    var ids = Object.keys(dita);
    if (ids.length === 2) {
      var a = dita[ids[0]], b = dita[ids[1]];
      d.x = e.clientX; d.y = e.clientY;
      var dist = Math.hypot(a.x - b.x, a.y - b.y), r = vista.getBoundingClientRect();
      if (pizzico) zoomIn(dist / pizzico, (a.x + b.x) / 2 - r.left, (a.y + b.y) / 2 - r.top, false);
      pizzico = dist; mosso = 99; return;
    }
    st.x += e.clientX - d.x; st.y += e.clientY - d.y; mosso += Math.abs(e.clientX - d.x) + Math.abs(e.clientY - d.y);
    // la cattura parte solo quando si trascina davvero, così il tocco su un punto resta un clic
    if (mosso > 4 && !vista.hasPointerCapture(e.pointerId)) { vista.setPointerCapture(e.pointerId); qmap.classList.add('is-trascina'); }
    d.x = e.clientX; d.y = e.clientY; disegna(false);
  });
  function fine(e) { delete dita[e.pointerId]; pizzico = null; if (!Object.keys(dita).length) qmap.classList.remove('is-trascina'); }
  vista.addEventListener('pointerup', fine); vista.addEventListener('pointercancel', fine);
  vista.addEventListener('wheel', function (e) {
    if (!e.ctrlKey && !e.metaKey) { qmap.classList.add('is-suggerisci'); clearTimeout(qmap._t); qmap._t = setTimeout(function () { qmap.classList.remove('is-suggerisci'); }, 1400); return; }
    e.preventDefault(); var r = vista.getBoundingClientRect();
    zoomIn(Math.exp(-e.deltaY * 0.004), e.clientX - r.left, e.clientY - r.top, false);
  }, { passive: false });
  vista.addEventListener('dblclick', function (e) { var r = vista.getBoundingClientRect(); zoomIn(1.6, e.clientX - r.left, e.clientY - r.top, true); });
  vista.tabIndex = 0;
  vista.addEventListener('keydown', function (e) {
    var m = { ArrowLeft: [80, 0], ArrowRight: [-80, 0], ArrowUp: [0, 80], ArrowDown: [0, -80] }[e.key];
    if (m) { e.preventDefault(); st.x += m[0]; st.y += m[1]; disegna(true); }
    if (e.key === '+' || e.key === '=') zoomIn(1.4, vista.clientWidth / 2, vista.clientHeight / 2, true);
    if (e.key === '-') zoomIn(1 / 1.4, vista.clientWidth / 2, vista.clientHeight / 2, true);
  });
  qmap.querySelector('.qmap__comandi').addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var z = +b.getAttribute('data-zoom');
    if (z) zoomIn(z > 0 ? 1.5 : 1 / 1.5, vista.clientWidth / 2, vista.clientHeight / 2, true);
    else inquadra(puntiQ.filter(function (p) { return !p.classList.contains('is-nascosto'); }), true);
  });
  puntiQ.forEach(function (p) {
    var id = p.getAttribute('data-id');
    p.addEventListener('click', function () { if (mosso > 6) return; seleziona(id, true); traccia('mappa_punto', { punto: id }); });
    p.addEventListener('mouseenter', function () { seleziona(id, false); });
  });
  vociQ.forEach(function (li) {
    var id = li.getAttribute('data-id');
    li.addEventListener('mouseenter', function () { seleziona(id, false); });
    li.addEventListener('click', function (e) { if (!e.target.closest('a')) seleziona(id, false); });
  });
  // temi: si vedono i punti del tema, i treni restano come riferimento, la mappa si inquadra da sola
  var gruppo = document.querySelector('.mappa-filtri');
  function tema(f, daUtente) {
    if (gruppo) gruppo.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x.getAttribute('data-filtro') === f ? 'true' : 'false'); });
    qmap.setAttribute('data-tema', f);
    var visibili = [];
    puntiQ.forEach(function (p) {
      var c = p.getAttribute('data-cat'), si = f === 'tutti' || c === f;
      p.classList.toggle('is-nascosto', !si && c !== 'trasporti');
      p.classList.toggle('is-riferimento', !si && c === 'trasporti');
      if (si) visibili.push(p);
    });
    vociQ.forEach(function (li) { li.classList.toggle('is-nascosto', f !== 'tutti' && li.getAttribute('data-cat') !== f); });
    inquadra(f === 'tutti' ? puntiQ.filter(function (p) { return pos(p).x && Math.hypot(pos(p).x - HX, pos(p).y - HY) < 430; }) : visibili, daUtente);
    if (daUtente) traccia('mappa_filtro', { categoria: f });
  }
  if (gruppo) gruppo.addEventListener('click', function (e) { var b = e.target.closest('button'); if (b) tema(b.getAttribute('data-filtro'), true); });
  document.querySelectorAll('[data-tema]').forEach(function (a) {
    if (a === qmap) return;
    a.addEventListener('click', function () { tema(a.getAttribute('data-tema'), true); });
  });
  window.addEventListener('resize', function () { disegna(false); });
  var base = qmap.querySelector('.qmap__base');
  function avvia() { tema('tutti', false); }
  if (base.complete) avvia(); else base.addEventListener('load', avvia);
}

// Galleria: filtri per area e foto a schermo intero, con frecce, tastiera e scorrimento del dito
var galleria = document.getElementById('galleria');
if (galleria) {
  var voci = [].slice.call(galleria.querySelectorAll('.galleria__voce'));
  var gf = document.querySelector('.galleria-filtri');
  if (gf) gf.addEventListener('click', function (e) {
    var b = e.target.closest('button'); if (!b) return;
    var f = b.getAttribute('data-filtro');
    gf.querySelectorAll('button').forEach(function (x) { x.setAttribute('aria-pressed', x === b ? 'true' : 'false'); });
    voci.forEach(function (v) { v.classList.toggle('is-nascosto', f !== 'tutte' && v.getAttribute('data-cat') !== f); });
    traccia('galleria_filtro', { categoria: f });
  });
  var lb = document.createElement('div');
  lb.className = 'lightbox'; lb.setAttribute('role', 'dialog'); lb.setAttribute('aria-modal', 'true'); lb.setAttribute('aria-label', 'Foto');
  lb.innerHTML = '<img alt=""><p></p><button type="button" class="lightbox__chiudi" aria-label="Chiudi">×</button><button type="button" class="lightbox__prec" aria-label="Foto precedente">‹</button><button type="button" class="lightbox__succ" aria-label="Foto successiva">›</button>';
  document.body.appendChild(lb);
  var lbImg = lb.querySelector('img'), lbTxt = lb.querySelector('p'), corrente = 0, origine = null;
  function visibili() { return voci.filter(function (v) { return !v.classList.contains('is-nascosto'); }); }
  function mostra(i) {
    var vv = visibili(); corrente = (i + vv.length) % vv.length;
    var a = vv[corrente].querySelector('a');
    lbImg.src = a.getAttribute('href'); lbImg.alt = a.querySelector('img').alt; lbTxt.textContent = a.getAttribute('data-didascalia');
  }
  function apri(i) { origine = document.activeElement; mostra(i); lb.classList.add('is-open'); document.documentElement.classList.add('lightbox-aperta'); lb.querySelector('.lightbox__chiudi').focus(); }
  function chiudi() { lb.classList.remove('is-open'); document.documentElement.classList.remove('lightbox-aperta'); if (origine) origine.focus(); }
  galleria.addEventListener('click', function (e) {
    var a = e.target.closest('a'); if (!a) return; e.preventDefault();
    apri(visibili().indexOf(a.parentNode)); traccia('galleria_foto', { foto: a.getAttribute('data-didascalia') });
  });
  lb.addEventListener('click', function (e) {
    if (e.target.closest('.lightbox__prec')) mostra(corrente - 1);
    else if (e.target.closest('.lightbox__succ')) mostra(corrente + 1);
    else if (e.target.closest('.lightbox__chiudi') || e.target === lb) chiudi();
  });
  document.addEventListener('keydown', function (e) {
    if (!lb.classList.contains('is-open')) return;
    if (e.key === 'Escape') chiudi(); if (e.key === 'ArrowLeft') mostra(corrente - 1); if (e.key === 'ArrowRight') mostra(corrente + 1);
  });
  var x0 = null;
  lb.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  lb.addEventListener('touchend', function (e) { if (x0 === null) return; var d = e.changedTouches[0].clientX - x0; if (Math.abs(d) > 50) mostra(corrente + (d < 0 ? 1 : -1)); x0 = null; });
}

// Pagina FAQ: ricerca immediata fra le domande e le risposte
var cerca = document.getElementById('faq-cerca');
if (cerca) {
  var voci = document.querySelectorAll('.faq-pagina .faq__item');
  var gruppi = document.querySelectorAll('.faq-gruppo');
  var esito = document.getElementById('faq-esito');
  function normalizza(t) { return t.toLowerCase().normalize('NFD').replace(/[̀-ͯ]/g, ''); }
  var testi = [].map.call(voci, function (d) { return normalizza(d.textContent); });
  var timer;
  cerca.addEventListener('input', function () {
    var q = normalizza(cerca.value.trim());
    var trovate = 0;
    voci.forEach(function (d, i) {
      var ok = !q || q.split(/\s+/).every(function (w) { return testi[i].indexOf(w) > -1; });
      d.classList.toggle('is-nascosta', !ok);
      if (q && ok && trovate < 1) d.open = true;
      if (ok) trovate++;
    });
    gruppi.forEach(function (g) { g.classList.toggle('is-vuoto', !g.querySelector('.faq__item:not(.is-nascosta)')); });
    esito.textContent = q ? (trovate ? trovate + (trovate === 1 ? ' risposta' : ' risposte') : 'Nessuna risposta: chiama la reception, +39 02 62071') : '';
    clearTimeout(timer);
    if (q) timer = setTimeout(function () { traccia('faq_ricerca', { testo: q, risultati: trovate }); }, 800);
  });
}

/* Selettore lingue: si chiude cliccando fuori o con Esc */
(function () {
  var l = document.querySelector('.lingue');
  if (!l) return;
  document.addEventListener('click', function (e) { if (l.open && !l.contains(e.target)) l.open = false; });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && l.open) { l.open = false; l.querySelector('summary').focus(); } });
})();

