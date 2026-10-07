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
      var r = stopAt ? stopAt.getBoundingClientRect() : null;
      var onForm = r ? (r.top < innerHeight && r.bottom > 0) : false; // nascosta solo mentre il form è a schermo
      sticky.classList.toggle('show', y > innerHeight * .8 && !onForm);
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
  // Invio: Netlify Forms (attributo data-netlify) solo sul dominio pubblicato; in anteprima mostra solo la conferma.
  // Dopo l'invio, la funzione netlify/functions/submission-created.js salva il contatto su Brevo e manda la notifica.
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
      e.preventDefault();
      var done = function(){
        $$('[data-echo]', f).forEach(function(o){ var src = f.querySelector(o.dataset.echo); if (src && src.value.trim()) o.textContent = src.value.trim(); });
        f.classList.add('sent'); f.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
        if (window.HPtrack) HPtrack('lead', { form: f.getAttribute('name') || f.id });
      };
      // Netlify Forms: invio in background; la funzione submission-created salva su Brevo e manda la notifica
      if (f.hasAttribute('data-netlify') && /(^|\.)(hotelpositioning\.com|netlify\.app)$/.test(location.hostname)) {
        var pg = f.querySelector('input[name="pagina"]'); if (pg) pg.value = location.pathname;
        var btn = f.querySelector('[type=submit]'); if (btn) btn.disabled = true;
        var fail = f.querySelector('.send-err');
        fetch('/', { method: 'POST', headers: { 'Content-Type': 'application/x-www-form-urlencoded' }, body: new URLSearchParams(new FormData(f)).toString() })
          .then(function(r){ if (!r.ok) throw new Error(r.status); done(); })
          .catch(function(){
            if (btn) btn.disabled = false;
            if (!fail) { fail = document.createElement('p'); fail.className = 'form-foot send-err'; fail.setAttribute('role', 'alert'); btn.insertAdjacentElement('afterend', fail); }
            fail.textContent = 'Invio non riuscito. Riprovate tra un momento oppure scrivete a privacy@hotelpositioning.com.';
          });
        return;
      }
      done();
    });
  });
  // exit intent: un messaggio per pagina, al massimo una volta per visita, mai per 3 giorni dopo una chiusura
  var EXIT = {
    '/': ['Prima di andare', 'Sette domande sulla vostra struttura.', 'Due minuti per capire quanto è riconoscibile oggi rispetto alle strutture della vostra zona.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/metodo/': ['Per applicare il metodo', 'Gli otto strumenti del libro, gratuiti.', 'Schede pratiche per lavorare sui sei passaggi con la vostra squadra. Dieci minuti ciascuna.', 'Ricevi gli strumenti', '/bonus/', 'No, grazie'],
    '/analisi/': ['Prima di andare', 'La candidatura richiede un minuto.', 'Rispondo entro 48 ore, anche quando la candidatura non è adatta.', 'Candida la struttura', '/analisi/#candidatura', 'Ci penserò'],
    '/analisi-gratuita.html': ['Prima di andare', 'La candidatura richiede un minuto.', 'Rispondo entro 48 ore, anche quando la candidatura non è adatta.', 'Candida la struttura', '/analisi/#candidatura', 'Ci penserò'],
    '/problemi/booking/': ['Prima di andare', 'Ridurre la dipendenza dalle OTA parte dal posizionamento.', 'Inviate la candidatura: valuto la struttura e rispondo entro 48 ore.', 'Candida la struttura', '#candidatura', 'Ci penserò'],
    '/problemi/prezzi/': ['Prima di andare', 'Sette domande sul vostro posizionamento.', 'Due minuti per capire se il limite al prezzo dipende dal mercato o dalla riconoscibilità della struttura.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/problemi/sostituibili/': ['Prima di andare', 'Una revisione gratuita della vostra homepage.', 'Titolo e sottotitolo analizzati riga per riga, con tre alternative pronte. Sei revisioni al mese.', 'Richiedi la revisione', '/smontaggio/', 'No, grazie'],
    '/problemi/agenzie/': ['Prima di andare', 'Un brief chiaro parte dalla homepage.', 'Una revisione gratuita di titolo e sottotitolo: il primo elemento di un brief efficace per qualsiasi agenzia.', 'Richiedi la revisione', '/smontaggio/', 'No, grazie'],
    '/problemi/valore/': ['Prima di andare', 'Il valore del brand si può costruire.', 'Inviate la candidatura: valuto la struttura e rispondo entro 48 ore.', 'Candida la struttura', '#candidatura', 'Ci penserò'],
    '/problemi/apertura/': ['Prima di andare', 'Il posizionamento si decide prima dell’apertura.', 'Dopo, cambiarlo costa molto di più. Inviate la candidatura e rispondo entro 48 ore.', 'Candida la struttura', '#candidatura', 'Ci penserò'],
    '/casi/': ['Prima di andare', 'Il prossimo caso può essere la vostra struttura.', 'Le candidature sono valutate una per una. Rispondo entro 48 ore.', 'Candida la struttura', '#candidatura', 'Ci penserò'],
    '/francesco/': ['Prima di andare', 'Una revisione gratuita della vostra homepage.', 'In tre giorni lavorativi vi dico cosa comunica oggi la vostra homepage, e cosa no.', 'Richiedi la revisione', '/smontaggio/', 'No, grazie'],
    '/libro/': ['Prima di andare', 'Il primo capitolo, gratuito.', 'Otto pagine in PDF, insieme agli otto strumenti del libro.', 'Ricevi il primo capitolo', '/bonus/', 'No, grazie'],
    '/library/': ['Prima di andare', 'E il posizionamento della vostra struttura?', 'Sette domande per capire se oggi è invisibile, sostituibile o posizionata. Due minuti.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/risorse/': ['Prima di andare', 'Il punto di partenza più semplice.', 'Sette domande, due minuti, nessuna email obbligatoria.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/quiz/': ['Mancano due minuti', 'Il risultato arriva alla fine del test.', 'Completate le domande per vedere il profilo della vostra struttura.', 'Completa il test', '#close', 'Esci'],
    '/smontaggio/': ['Prima di andare', 'La richiesta richiede quattro campi.', 'Nessuna call. Ricevete la revisione entro tre giorni lavorativi.', 'Richiedi la revisione', '#form', 'No, grazie']
  };
  var exitEl = document.getElementById('exit'), path = location.pathname.replace(/index\.html$/, '');
  // confronto sulla parte finale dell'indirizzo: funziona anche se il sito sta in una sottocartella
  var key = Object.keys(EXIT).filter(function(k){ return k !== '/' && path.slice(-k.length) === k; })
    .sort(function(x, y){ return y.length - x.length; })[0];
  if (!key && document.getElementById('sintomi')) key = '/';
  var cfg = EXIT[key];
  function store(k, v){ try { if (v === undefined) return localStorage.getItem(k); localStorage.setItem(k, v); } catch (e) { return null; } }
  function sstore(k, v){ try { if (v === undefined) return sessionStorage.getItem(k); sessionStorage.setItem(k, v); } catch (e) { return null; } }
  if (exitEl && cfg) {
    var lastFocus = null, armedAt = Date.now() + 6000;
    ['k','t','p'].forEach(function(id, i){ document.getElementById('exit-' + id).textContent = cfg[i]; });
    var cta = document.getElementById('exit-cta');
    cta.innerHTML = cfg[3] + ' <span class="arr">→</span>'; cta.href = cfg[4] === '#close' ? '#' : cfg[4];
    document.getElementById('exit-no').textContent = cfg[5];
    var blocked = function(){
      if (Date.now() < armedAt || sstore('hp-exit') || $$('form.sent').length) return true;
      var snooze = parseInt(store('hp-exit-snooze') || '0', 10); if (snooze > Date.now()) return true;
      // non disturbare chi sta compilando un form
      var a = document.activeElement; if (a && a.closest && a.closest('form')) return true;
      return false;
    };
    var open = function(){
      if (blocked()) return;
      sstore('hp-exit', '1'); lastFocus = document.activeElement;
      exitEl.hidden = false; cta.focus();
    };
    var close = function(snooze){
      exitEl.hidden = true;
      if (snooze) store('hp-exit-snooze', String(Date.now() + 3 * 864e5));
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    };
    $$('[data-exit-close]', exitEl).forEach(function(b){ b.addEventListener('click', function(){ close(true); }); });
    exitEl.addEventListener('click', function(e){ if (e.target === exitEl) close(true); });
    cta.addEventListener('click', function(e){ if (cfg[4] === '#close') { e.preventDefault(); } close(false); });
    document.addEventListener('keydown', function(e){
      if (exitEl.hidden) return;
      if (e.key === 'Escape') close(true);
      if (e.key === 'Tab') { // tieni il focus dentro il pop-up
        var f = $$('a,button', exitEl), first = f[0], last = f[f.length - 1];
        if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
        else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      }
    });
    // desktop: il mouse esce verso la barra del browser
    document.addEventListener('mouseout', function(e){ if (!e.relatedTarget && e.clientY <= 0) open(); });
    // mobile: dopo metà pagina, una risalita veloce verso l'alto
    var lastY = scrollY, lastT = Date.now(), deep = false;
    addEventListener('scroll', function(){
      var y = scrollY, t = Date.now(), h = document.documentElement.scrollHeight - innerHeight;
      if (h > 0 && y / h > .5) deep = true;
      if (deep && innerWidth < 900 && (lastY - y) / Math.max(t - lastT, 1) > 1.6 && lastY - y > 120) open();
      lastY = y; lastT = t;
    }, { passive: true });
  }
})();
