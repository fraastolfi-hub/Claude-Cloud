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
