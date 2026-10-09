/* Hotel Positioning · strumenti della library (/bonus/<slug>/). Vanilla, nessuna dipendenza.
   Si carica in fondo al <body>, DOPO il markup dello strumento e PRIMA dello <script> inline della pagina.

   window.HPT
   ----------------------------------------------------------------------------------------------
   HPT.unlocked()                 true se localStorage "library_unlocked" === "true" (stessa chiave del vecchio sito).
                                  Il cancello gira da solo al caricamento:
                                  - ?accesso=1 nell'URL: sblocca e toglie il parametro (history.replaceState);
                                  - sbloccato: mostra [data-t-tool] (nel markup ha l'attributo hidden);
                                  - chiuso: lascia [data-t-tool] nascosto e inserisce prima la scheda "Vai alla library",
                                    con numero e nome presi da <body data-tool-n="01" data-tool-name="...">.
   HPT.read(key)                  JSON salvato sotto key, oppure null (anche per leggere un altro strumento,
                                  es. HPT.read("worksheet_state") dal canvas).
   HPT.write(key, obj)            salva obj come JSON; false se lo storage è pieno o bloccato.
   HPT.remove(key)
   HPT.store(key, defaults)       stato persistente di uno strumento:
                                  st.state (oggetto: defaults + salvato), st.set(k, v) (salva subito),
                                  st.patch({..}), st.save(), st.reset() (torna ai defaults e cancella la chiave),
                                  st.on(fn) (fn(state, k) dopo ogni modifica).
   HPT.bind(root, st)             collega i campi [data-k="nome"] dentro root a st.state.nome, ripristina e salva a ogni input:
                                  input/textarea/select -> stringa; checkbox -> booleano;
                                  button[data-k][data-v] -> st.state[k] = data-v, con aria-checked (role=radio)
                                  o aria-pressed (altrimenti) e classe is-selected. Ritorna sync() per riallineare il DOM.
   HPT.screen(name, focus)        mostra [data-screen=name], nasconde gli altri [data-screen], torna in cima;
                                  con focus=true sposta il fuoco sul primo titolo dello schermo (per chi usa la tastiera).
   HPT.download(file, text|righe) scarica un .txt (righe: array unito con \n).
   HPT.print()                    window.print(); prima allunga le textarea perché in stampa si legga tutto.
   HPT.reset(st, domanda)         chiede conferma (domanda opzionale), poi st.reset(). Ritorna true se ha azzerato.
   HPT.$(sel, ctx) / HPT.$$(sel, ctx)
   ---------------------------------------------------------------------------------------------- */
(function(){
  var UNLOCK = 'library_unlocked';
  var $ = function(s, c){ return (c || document).querySelector(s); };
  var $$ = function(s, c){ return Array.prototype.slice.call((c || document).querySelectorAll(s)); };

  function get(k){ try { return localStorage.getItem(k); } catch (e) { return null; } }
  function set(k, v){ try { localStorage.setItem(k, v); return true; } catch (e) { return false; } }
  function remove(k){ try { localStorage.removeItem(k); } catch (e) {} }
  function read(k){ var raw = get(k); if (!raw) return null; try { return JSON.parse(raw); } catch (e) { return null; } }
  function write(k, o){ try { return set(k, JSON.stringify(o)); } catch (e) { return false; } }
  function unlocked(){ return get(UNLOCK) === 'true'; }

  // ?accesso=1 -> sblocca e pulisce l'URL
  try {
    var u = new URL(location.href);
    if (u.searchParams.get('accesso') === '1') {
      set(UNLOCK, 'true');
      u.searchParams.delete('accesso');
      history.replaceState(history.state, '', u.pathname + u.search + u.hash);
    }
  } catch (e) {}

  function esc(s){ return String(s).replace(/[&<>"]/g, function(c){ return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]; }); }

  function gate(){
    var tool = $('[data-t-tool]');
    if (!tool) return;
    if (unlocked()) { tool.hidden = false; document.body.classList.remove('t-locked'); return; }
    document.body.classList.add('t-locked');
    if ($('.t-gate')) return;
    var b = document.body.dataset;
    var box = document.createElement('section');
    box.className = 't-gate';
    box.setAttribute('aria-labelledby', 't-gate-title');
    box.innerHTML = '<div class="t-gate__card">'
      + '<span class="t-gate__n" aria-hidden="true">' + esc(b.toolN || '') + '</span>'
      + '<h1 class="t-title t-gate__title" id="t-gate-title">' + esc(b.toolName || 'Strumento') + '</h1>'
      + '<p class="t-lead">Questo strumento sta dentro la library. Entra una volta, resti dentro per sempre.</p>'
      + '<a class="t-btn t-btn--lg t-gate__cta" href="/bonus/#strumenti">Vai alla library →</a>'
      + '</div>';
    tool.parentNode.insertBefore(box, tool);
  }

  function store(key, defaults){
    var base = defaults || {};
    var s = {}, fns = [];
    function fill(src){ for (var k in base) s[k] = base[k]; if (src) for (var j in src) s[j] = src[j]; }
    fill(read(key));
    function emit(k){ fns.forEach(function(f){ try { f(s, k); } catch (e) { if (window.console) console.error(e); } }); }
    var st = {
      key: key, state: s,
      save: function(){ return write(key, s); },
      set: function(k, v){ s[k] = v; write(key, s); emit(k); },
      patch: function(o){ for (var k in o) s[k] = o[k]; write(key, s); emit(null); },
      reset: function(){ for (var k in s) delete s[k]; fill(null); remove(key); emit(null); },
      on: function(f){ fns.push(f); }
    };
    return st;
  }

  function bind(root, st){
    var els = $$('[data-k]', root || document);
    function sync(){
      els.forEach(function(el){
        var k = el.getAttribute('data-k'), v = st.state[k];
        if (el.hasAttribute('data-v')) {
          var on = String(v) === el.getAttribute('data-v');
          el.setAttribute(el.getAttribute('role') === 'radio' ? 'aria-checked' : 'aria-pressed', on ? 'true' : 'false');
          el.classList.toggle('is-selected', on);
        } else if (el.type === 'checkbox') {
          el.checked = !!v;
        } else {
          var str = v == null ? '' : String(v);
          if (el.value !== str) el.value = str;
        }
      });
    }
    els.forEach(function(el){
      var k = el.getAttribute('data-k');
      if (el.hasAttribute('data-v')) el.addEventListener('click', function(){ st.set(k, el.getAttribute('data-v')); });
      else if (el.type === 'checkbox') el.addEventListener('change', function(){ st.set(k, el.checked); });
      else el.addEventListener('input', function(){ st.set(k, el.value); });
    });
    st.on(function(s, k){ if (k === null || k === undefined) sync(); else els.forEach(function(el){ if (el.hasAttribute('data-v') && el.getAttribute('data-k') === k) sync(); }); });
    sync();
    return sync;
  }

  function screen(name, focus){
    var shown = null;
    $$('[data-screen]').forEach(function(el){
      var on = el.getAttribute('data-screen') === name;
      el.hidden = !on;
      if (on) shown = el;
    });
    try { window.scrollTo(0, 0); } catch (e) {}
    if (focus && shown) {
      var h = $('h1, h2', shown);
      if (h) { h.setAttribute('tabindex', '-1'); h.focus({ preventScroll: true }); }
    }
    return shown;
  }

  function download(name, text){
    if (Array.isArray(text)) text = text.join('\n');
    var a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([text], { type: 'text/plain;charset=utf-8' }));
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function(){ URL.revokeObjectURL(a.href); }, 1000);
  }

  // in stampa le textarea mostrano tutto il testo, non solo le prime righe
  function grow(){ $$('.t-page textarea').forEach(function(t){ t.dataset.h = t.style.height; t.style.height = 'auto'; t.style.height = (t.scrollHeight + 4) + 'px'; }); }
  function shrink(){ $$('.t-page textarea').forEach(function(t){ t.style.height = t.dataset.h || ''; }); }
  window.addEventListener('beforeprint', grow);
  window.addEventListener('afterprint', shrink);
  function print(){ grow(); window.print(); }

  function reset(st, q){
    if (q && !window.confirm(q)) return false;
    st.reset();
    return true;
  }

  window.HPT = {
    unlocked: unlocked, read: read, write: write, remove: remove,
    store: store, bind: bind, screen: screen, download: download, print: print, reset: reset,
    $: $, $$: $$
  };
  gate();
})();
