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
  // exit intent: un messaggio per pagina, al massimo una volta per visita, mai per 3 giorni dopo una chiusura
  var EXIT = {
    '/': ['Te ne vai già?', 'Prima fai una prova.', 'Copri il logo della tua homepage e rileggila. Se funziona anche per l’hotel accanto, il problema non è questo sito.', 'Fai il test: 7 domande', '/quiz/', 'No, la mia homepage è perfetta così'],
    '/metodo/': ['Il cassetto ti aspetta', 'Hai letto il metodo. Adesso finisce nel cassetto?', 'È lì che muoiono le buone idee. Ti mando gli otto strumenti per applicarlo: dieci minuti l’uno.', 'Mandami gli strumenti', '/bonus/', 'Lo applico dopo la stagione (come sempre)'],
    '/analisi/': ['Booking ringrazia', 'Chiudi la pagina. Booking incassa lo stesso.', 'Il 18% non va in vacanza. La candidatura chiede sessanta secondi e, se ti scarto, ti spiego perché.', 'Candida il tuo hotel', '/analisi/#candidatura', 'Preferisco pagare la commissione'],
    '/problemi/booking/': ['Un attimo', 'Esci pure. La commissione resta.', 'Ogni prenotazione che ti arriva da Booking mentre ci pensi costa il 18%. Pensarci è gratis. Candidarsi pure.', 'Candida il tuo hotel', '#candidatura', 'Va bene così, Booking è di famiglia'],
    '/problemi/prezzi/': ['Prima di uscire', 'Anche il tuo prezzo resta dove l’hai lasciato.', 'Nel 2022, per la precisione. Ti dico in sette domande se il problema è il mercato o il motivo per sceglierti.', 'Fai il test: 2 minuti', '/quiz/', 'Il mercato non paga, lo so già'],
    '/problemi/sostituibili/': ['Un’ultima cosa', 'Se esci ora, domani sei ancora identico a quello accanto.', 'Mandami la tua homepage. Te la smonto riga per riga, gratis, e ti riscrivo la prima frase.', 'Smonta la mia homepage', '/smontaggio/', 'Preferisco restare uno dei cinquanta'],
    '/problemi/agenzie/': ['Prima della quarta agenzia', 'Il problema non è chi esegue. È cosa gli fai eseguire.', 'Dai all’agenzia un brief che dica chi sei. Ti smonto la homepage gratis: è il primo pezzo di quel brief.', 'Smonta la mia homepage', '/smontaggio/', 'Chiamo la quarta, vediamo'],
    '/problemi/valore/': ['Il perito non aspetta', 'I muri li vede chiunque. Il brand, nessuno.', 'Finché il tuo nome non vale niente, nel calcolo resta la riga vuota. Vediamo se si può riempire.', 'Candida il tuo hotel', '#candidatura', 'Mi tengo i metri quadri'],
    '/problemi/apertura/': ['Le porte si aprono una volta', 'La prima impressione non ha la seconda stagione.', 'Decidi chi sei prima di scegliere le lampade. Dopo costa il triplo, e lo dico con cinque ristoranti alle spalle.', 'Candida la tua struttura', '#candidatura', 'Ci penso dopo l’inaugurazione'],
    '/casi/': ['Il prossimo caso', 'Il prossimo caso potrebbe avere il tuo nome.', 'O quello dell’hotel accanto, se si candida prima. I posti gratuiti sono cinque.', 'Candida il tuo hotel', '#candidatura', 'Lascio il posto all’hotel accanto'],
    '/francesco/': ['Ora sai chi sono', 'Io invece non so ancora chi sei tu.', 'Mandami la tua homepage. In tre giorni ti dico cosa racconta di te, e cosa no.', 'Smonta la mia homepage', '/smontaggio/', 'Preferisco restare un mistero'],
    '/libro/': ['19,90 € sono troppi?', 'Meno di una commissione su una camera, per una notte.', 'Se non ti fidi ancora, prenditi il primo capitolo gratis insieme agli otto strumenti.', 'Mandami il primo capitolo', '/bonus/', 'Preferisco continuare a pagare commissioni'],
    '/library/': ['88 posizionamenti dopo', 'E il tuo, qual è?', 'Sette domande per capire se sei invisibile, sostituibile o posizionato. Due minuti.', 'Fai il test', '/quiz/', 'Lo so già (credo)'],
    '/risorse/': ['Indeciso?', 'L’indecisione è il primo sintomo.', 'Parti dal gradino più basso: sette domande, due minuti, nessuna email obbligatoria.', 'Fai il test', '/quiz/', 'Ci penso, come al solito'],
    '/quiz/': ['Mancano due minuti', 'Meno di una telefonata con il call center di Booking.', 'Finisci il test: la risposta scomoda arriva alla fine.', 'Ok, finisco', '#close', 'Meglio non saperlo'],
    '/smontaggio/': ['Tre secondi', 'La tua homepage ha tre secondi. Tu qui ne hai già spesi trenta.', 'Quattro campi, nessuna call. Te la smonto io, riga per riga.', 'Smonta la mia homepage', '#form', 'La mia homepage va benissimo così']
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
