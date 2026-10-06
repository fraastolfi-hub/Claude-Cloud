/* Hotel Positioning · comportamenti comuni a tutte le pagine */
(function(){
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  window.HP = { reduce: reduce };
  var $$ = function(s,c){ return Array.prototype.slice.call((c||document).querySelectorAll(s)); };

  // marquee: duplica il contenuto per un loop continuo
  $$('.ticker-track').forEach(function(t){ t.innerHTML = t.innerHTML + t.innerHTML + t.innerHTML + t.innerHTML; });

  // reveal on scroll
  if ('IntersectionObserver' in window) {
    var io = new IntersectionObserver(function(es){
      es.forEach(function(e){ if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
    }, { threshold: .12, rootMargin: '0px 0px -40px 0px' });
    $$('.rv,.sec-head,.tl,[data-reveal]').forEach(function(el){ io.observe(el); });
  } else {
    $$('.rv').forEach(function(el){ el.classList.add('in'); });
  }

  // nav: ombra, menu mobile, barra di lettura, cta fissa su mobile
  var nav = document.querySelector('.nav'), bar = document.querySelector('.readbar');
  var burger = document.querySelector('.burger');
  if (burger) burger.addEventListener('click', function(){
    var open = nav.classList.toggle('open'); burger.setAttribute('aria-expanded', open);
  });
  $$('.mobile-menu a').forEach(function(a){ a.addEventListener('click', function(){ nav.classList.remove('open'); }); });
  function onScroll(){
    // cercati qui e non all'avvio: la CTA fissa e il form arrivano dopo questo script
    var sticky = document.querySelector('.sticky-cta'), stopAt = document.querySelector('[data-sticky-stop], #candidatura');
    var y = window.scrollY, h = document.documentElement.scrollHeight - innerHeight;
    if (nav) nav.classList.toggle('scrolled', y > 10);
    if (bar) bar.style.width = (h > 0 ? y / h * 100 : 0) + '%';
    if (sticky) {
      var past = stopAt ? stopAt.getBoundingClientRect().top < innerHeight : false;
      sticky.classList.toggle('show', y > innerHeight * .8 && !past);
    }
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // contatori: <b data-count="30" data-prefix="€" data-suffix="M">0</b>
  var co = new IntersectionObserver(function(es){
    es.forEach(function(e){
      if (!e.isIntersecting) return; co.unobserve(e.target);
      var el = e.target, to = parseFloat(el.dataset.count), dec = (el.dataset.count.split('.')[1] || '').length;
      var pre = el.dataset.prefix || '', suf = el.dataset.suffix || '', t0 = null;
      function fmt(v){ return pre + v.toFixed(dec).replace('.', ',') + suf; }
      if (reduce) { el.textContent = fmt(to); return; }
      (function f(t){ if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 1200); el.textContent = fmt(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(f); })(performance.now());
    });
  }, { threshold: .6 });
  $$('[data-count]').forEach(function(el){ co.observe(el); });

  // form: validazione, barra di avanzamento, stato inviato.
  // <form class="form" data-hp-form> ... campi [required] dentro .field, privacy in .check
  // Per collegare un endpoint reale: metti l'URL in action="" e data-endpoint="1".
  $$('form[data-hp-form]').forEach(function(f){
    function missing(el){
      if (el.type === 'radio') return !f.querySelector('input[name="' + el.name + '"]:checked');
      return el.type === 'checkbox' ? !el.checked : el.value.trim() === '';
    }
    var req = $$('[required]', f), bar = f.querySelector('.prog i'), txt = f.querySelector('[data-prog-txt]');
    function progress(){
      if (!bar) return;
      var ok = req.filter(function(el){ return !missing(el); }).length;
      var p = Math.round(ok / req.length * 100); bar.style.width = p + '%'; if (txt) txt.textContent = p + '%';
    }
    f.addEventListener('input', function(e){ progress(); var w = e.target.closest('fieldset,.field,.check'); if (w) w.classList.remove('err'); });
    f.addEventListener('change', progress);
    f.addEventListener('submit', function(e){
      var first = null;
      req.forEach(function(el){
        var bad = missing(el) || (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value));
        var w = el.type === 'radio' ? el.closest('fieldset') : el.closest('.field,.check'); if (w) w.classList.toggle('err', bad);
        if (bad && !first) first = el;
      });
      if (first) { e.preventDefault(); first.focus(); if (!reduce) { f.classList.remove('shake'); void f.offsetWidth; f.classList.add('shake'); } return; }
      if (f.dataset.endpoint) return; // invio reale
      e.preventDefault();
      $$('[data-echo]', f).forEach(function(o){ var src = f.querySelector(o.dataset.echo); if (src && src.value.trim()) o.textContent = src.value.trim(); });
      f.classList.add('sent'); f.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
    });
  });
})();
