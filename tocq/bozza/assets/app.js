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
