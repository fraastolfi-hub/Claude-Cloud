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
    var sticky = document.querySelector('.sticky-cta'), stopAt = document.querySelector('[data-sticky-stop], #richiedi');
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
    // gruppi di caselle che finiscono in un solo campo (es. canali di prenotazione)
    $$('[data-join]', f).forEach(function(g){
      var out = f.querySelector('#' + g.dataset.join);
      g.addEventListener('change', function(){ out.value = $$('input[type=checkbox]:checked', g).map(function(c){ return c.value; }).join(', '); g.classList.remove('err'); progress(); });
    });
    function bad(el){
      if (missing(el)) return true;
      if (el.type === 'email' && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(el.value)) return true;
      if (el.type === 'number') { var n = parseFloat(el.value); if (isNaN(n) || (el.min !== '' && n < +el.min) || (el.max !== '' && n > +el.max)) return true; }
      return false;
    }
    // gruppi «almeno uno»: <div data-any="id-del-campo-nascosto"> con più campi; il campo nascosto (required) si riempie se almeno uno è compilato
    $$('[data-any]', f).forEach(function(g){
      var out = f.querySelector('#' + g.dataset.any);
      function upd(){ out.value = $$('input:not([type=hidden]),textarea', g).some(function(i){ return i.value.trim(); }) ? '1' : ''; if (out.value) g.classList.remove('err'); }
      g.addEventListener('input', upd); upd();
    });
    // salvataggio nel browser: <form data-save="chiave"> ricorda risposte e passo finché non si invia
    var SAVE = f.dataset.save, saveReady = false;
    function save(){ if (!SAVE) return; try { var o = { step: cur, v: {} }; $$('[name]', f).forEach(function(el){ if (el.type === 'hidden' || el.name === 'bot-field') return; o.v[el.name] = (el.type === 'checkbox' || el.type === 'radio') ? (el.checked ? el.value || 'on' : (o.v[el.name] || '')) : el.value; }); localStorage.setItem(SAVE, JSON.stringify(o)); } catch (e) {} }
    function wrap(el){ return el.type === 'radio' ? el.closest('fieldset') : el.closest('.field,.check'); }
    function check(list){
      var first = null;
      list.forEach(function(el){ var b = bad(el), w = wrap(el); if (w) w.classList.toggle('err', b); if (b && !first) first = el; });
      return first;
    }
    // passi: <div class="fstep"> uno alla volta, «Avanti» controlla solo il passo corrente
    var steps = $$('.fstep', f), cur = 0, stxt = f.querySelector('[data-step-txt]');
    function show(n){
      cur = n;
      steps.forEach(function(s, i){ s.hidden = i !== n; });
      if (stxt) stxt.textContent = 'Passo ' + (n + 1) + ' di ' + steps.length;
      if (bar) bar.style.width = Math.round(n / steps.length * 100) + '%';
      var sq = f.parentElement.querySelectorAll('.q-steps i');
      for (var i = 0; i < sq.length; i++) { sq[i].className = i < n ? 'done' : (i === n ? 'cur' : ''); }
      if (SAVE && saveReady) save();
    }
    function shake(){ if (!reduce) { f.classList.remove('shake'); void f.offsetWidth; f.classList.add('shake'); } }
    function next(){
      var first = check($$('[required]', steps[cur]));
      if (first) { if (first.type !== 'hidden') first.focus(); shake(); return; }
      show(cur + 1);
      var foc = steps[cur].querySelector('input:not([type=hidden]),select,textarea'); if (foc) foc.focus({ preventScroll: true });
      f.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'start' });
    }
    if (steps.length) {
      show(0);
      if (SAVE) { try { var sv = JSON.parse(localStorage.getItem(SAVE) || 'null'); if (sv && sv.v) {
        $$('[name]', f).forEach(function(el){ var v = sv.v[el.name]; if (v == null || el.type === 'hidden') return; if (el.type === 'checkbox' || el.type === 'radio') el.checked = (el.value || 'on') === v; else el.value = v; });
        $$('[data-any]', f).forEach(function(g){ g.dispatchEvent(new Event('input')); });
        if (typeof sv.step === 'number') show(Math.min(Math.max(sv.step, 0), steps.length - 1));
      } } catch (e) {} }
      saveReady = true; f.addEventListener('input', save); f.addEventListener('change', save);
      f.addEventListener('click', function(e){
        if (e.target.closest('[data-next]')) { e.preventDefault(); next(); }
        else if (e.target.closest('[data-prev]')) { e.preventDefault(); show(Math.max(0, cur - 1)); }
      });
      // Invio da tastiera nei passi intermedi: va avanti invece di inviare
      f.addEventListener('keydown', function(e){ if (e.key === 'Enter' && e.target.tagName !== 'TEXTAREA' && cur < steps.length - 1) { e.preventDefault(); next(); } });
    }
    function progress(){
      if (!bar || steps.length) return;
      var ok = req.filter(function(el){ return !missing(el); }).length;
      var p = Math.round(ok / req.length * 100); bar.style.width = p + '%'; if (txt) txt.textContent = p + '%';
    }
    f.addEventListener('input', function(e){ progress(); var w = e.target.closest('fieldset,.field,.check'); if (w) w.classList.remove('err'); });
    f.addEventListener('change', progress);
    f.addEventListener('submit', function(e){
      if (steps.length && cur < steps.length - 1) { e.preventDefault(); next(); return; }
      var first = check(req);
      if (first) {
        e.preventDefault();
        if (steps.length) { var i = steps.findIndex(function(st){ return st.contains(first); }); if (i > -1 && i !== cur) show(i); }
        if (first.type !== 'hidden') first.focus(); shake(); return;
      }
      e.preventDefault();
      var done = function(){
        $$('[data-echo]', f).forEach(function(o){ var src = f.querySelector(o.dataset.echo); if (src && src.value.trim()) o.textContent = src.value.trim(); });
        if (bar) bar.style.width = '100%'; if (f.dataset.save) { try { localStorage.removeItem(f.dataset.save); } catch (e) {} } f.classList.add('sent'); f.scrollIntoView({ behavior: reduce ? 'auto' : 'smooth', block: 'center' });
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
            fail.textContent = 'Invio non riuscito. Riprova tra un momento oppure scrivimi a consulting@francescoastolfi.net.';
          });
        return;
      }
      done();
    });
  });
  // exit intent: un messaggio per pagina, al massimo una volta per visita, mai per 3 giorni dopo una chiusura
  var EXIT = {
    '/': ['Prima di andare', 'Ti basta un minuto per richiederlo.', 'Lo smontaggio gratuito della tua homepage, accanto ai concorrenti. Fatto a mano da me, massimo 6 al mese.', 'Richiedi lo smontaggio', '#richiedi', 'No, grazie'],
    '/metodo/': ['Prima di andare', 'Il primo passo è sulla tua homepage.', 'Lo smontaggio gratuito: la tua prima riga accanto ai concorrenti, con il logo coperto. In 3 giorni lavorativi.', 'Richiedi lo smontaggio', '/#richiedi', 'No, grazie'],
    '/analisi/': ['Prima di andare', 'Comincia dallo smontaggio, gratis.', 'La tua homepage accanto ai concorrenti, un verdetto e dove cercare il motivo. In 3 giorni lavorativi.', 'Richiedi lo smontaggio', '/#richiedi', 'Ci penso'],
    '/problemi/booking/': ['Prima di andare', 'Meno OTA parte dal posizionamento.', 'Smontaggio gratuito della tua homepage, accanto ai concorrenti. In 3 giorni lavorativi.', 'Richiedi lo smontaggio', '#richiedi', 'Ci penso'],
    '/problemi/prezzi/': ['Prima di andare', 'Sette domande sul tuo posizionamento.', 'Due minuti per capire se il limite al prezzo è il mercato o il tuo hotel.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/problemi/sostituibili/': ['Prima di andare', 'Copri il logo: si capisce chi sei?', 'Lo smontaggio gratuito mette la tua prima riga accanto ai concorrenti. In 3 giorni lavorativi.', 'Richiedi lo smontaggio', '/smontaggio/', 'No, grazie'],
    '/problemi/agenzie/': ['Prima di andare', 'Un brief chiaro parte dalla homepage.', 'Lo smontaggio gratuito ti dice se la tua prima riga si distingue dai concorrenti: il primo pezzo di un buon brief.', 'Richiedi lo smontaggio', '/smontaggio/', 'No, grazie'],
    '/problemi/valore/': ['Prima di andare', 'Il valore del brand si costruisce.', 'Comincia dallo smontaggio gratuito della tua homepage. In 3 giorni lavorativi.', 'Richiedi lo smontaggio', '#richiedi', 'Ci penso'],
    '/problemi/apertura/': ['Prima di andare', 'Il posizionamento si decide prima di aprire.', 'Dopo, cambiarlo costa molto di più. Comincia dallo smontaggio gratuito.', 'Richiedi lo smontaggio', '#richiedi', 'Ci penso'],
    '/casi/': ['Prima di andare', 'Il prossimo caso può essere il tuo hotel.', 'Comincia dallo smontaggio gratuito della homepage. Massimo 6 al mese.', 'Richiedi lo smontaggio', '/#richiedi', 'Ci penso'],
    '/francesco/': ['Prima di andare', 'Lo smontaggio gratuito della tua homepage.', 'In tre giorni lavorativi ti dico se l\'ospite riesce a distinguerti dai concorrenti.', 'Richiedi lo smontaggio', '/smontaggio/', 'No, grazie'],
    '/libro/': ['Prima di andare', 'I bonus del libro, gratis.', 'Gli otto fogli di lavoro che uso con gli hotel che seguo, via email.', 'Scarica i bonus', '/bonus/', 'No, grazie'],
    '/library/': ['Prima di andare', 'E il tuo hotel, dove si trova?', 'Sette domande per capire se oggi è invisibile, sostituibile o posizionato. Due minuti.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/risorse/': ['Prima di andare', 'Il punto di partenza più semplice.', 'Sette domande, due minuti, nessuna email obbligatoria.', 'Fai il test', '/quiz/', 'No, grazie'],
    '/quiz/': ['Mancano due minuti', 'Il risultato arriva alla fine del test.', 'Rispondi alle domande per vedere il profilo del tuo hotel.', 'Completa il test', '#close', 'Esci'],
    '/smontaggio/': ['Prima di andare', 'Bastano pochi campi.', 'Nessuna chiamata. Ricevi lo smontaggio entro tre giorni lavorativi.', 'Richiedi lo smontaggio', '#form', 'No, grazie']
  };
  var exitEl = document.getElementById('exit'), path = location.pathname.replace(/index\.html$/, '');
  // confronto sulla parte finale dell'indirizzo: funziona anche se il sito sta in una sottocartella
  var key = Object.keys(EXIT).filter(function(k){ return k !== '/' && path.slice(-k.length) === k; })
    .sort(function(x, y){ return y.length - x.length; })[0];
  if (!key && document.querySelector('.hero-c') && document.getElementById('richiedi')) key = '/';
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

/* Titoli: le parole non si spezzano mai. Se una parola non sta nella riga, il titolo si rimpicciolisce quanto basta. */
(function(){
  var SEL = 'h1,h2,h3,.pull,.big-quote,.exit-t,.foot .big';
  function over(h){
    if (h.scrollWidth > h.clientWidth + 1) return true;
    if (h.getBoundingClientRect().right > document.documentElement.clientWidth + 1) return true;
    var l = h.querySelectorAll('.line');
    for (var i = 0; i < l.length; i++) if (l[i].scrollWidth > l[i].clientWidth + 1) return true;
    return false;
  }
  function fit(){
    document.querySelectorAll(SEL).forEach(function(h){
      h.style.removeProperty('font-size');
      if (!h.clientWidth || !over(h)) return;
      var fs = parseFloat(getComputedStyle(h).fontSize), n = 0;
      while (over(h) && n++ < 40 && fs > 14) { fs *= 0.96; h.style.setProperty('font-size', fs.toFixed(1) + 'px', 'important'); }
    });
  }
  var t; function later(){ clearTimeout(t); t = setTimeout(fit, 120); }
  fit();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fit);
  window.addEventListener('load', fit);
  window.addEventListener('resize', later);
})();
