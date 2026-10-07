/* Hotel Positioning · consenso ai cookie (GDPR, linee guida del Garante 2021)
   - nessuno script di terze parti prima del consenso;
   - "Rifiuta" e la X valgono quanto "Accetta tutti";
   - la scelta dura 6 mesi, poi il banner ricompare;
   - gli ID si impostano in window.HP_TRACKING (partial head.html): vuoti = disattivati.
   Eventi: window.HPtrack('lead', { form: 'candidatura' }) li manda a GA4 e Meta, solo se attivi. */
(function(){
  var KEY = 'hp-consent', TTL = 182 * 864e5, cfg = window.HP_TRACKING || {};
  var el = document.getElementById('cc'); if (!el) return;
  var opts = document.getElementById('cc-opts'), stats = document.getElementById('cc-stats'), mkt = document.getElementById('cc-mkt');
  var save = document.getElementById('cc-save'), custom = document.getElementById('cc-custom');
  var loaded = { ga: false, meta: false };

  function read(){ try { var c = JSON.parse(localStorage.getItem(KEY)); return c && Date.now() - c.ts < TTL ? c : null; } catch (e) { return null; } }
  function write(c){ c.ts = Date.now(); c.v = 1; try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) {} }

  function loadGA(){
    if (loaded.ga || !cfg.ga4) return; loaded.ga = true;
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(cfg.ga4);
    document.head.appendChild(s);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function(){ dataLayer.push(arguments); };
    gtag('js', new Date());
    gtag('config', cfg.ga4, { anonymize_ip: true });
  }
  function loadMeta(){
    if (loaded.meta || !cfg.metaPixel) return; loaded.meta = true;
    !function(f,b,e,v,n,t,s){if(f.fbq)return;n=f.fbq=function(){n.callMethod?n.callMethod.apply(n,arguments):n.queue.push(arguments)};
    if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';n.queue=[];t=b.createElement(e);t.async=!0;
    t.src=v;s=b.getElementsByTagName(e)[0];s.parentNode.insertBefore(t,s)}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
    fbq('init', cfg.metaPixel); fbq('track', 'PageView');
  }
  function apply(c){ if (c.stats) loadGA(); if (c.mkt) loadMeta(); }

  window.HPtrack = function(name, params){
    params = params || {};
    if (loaded.ga && window.gtag) gtag('event', name === 'lead' ? 'generate_lead' : name, params);
    if (loaded.meta && window.fbq) fbq(name === 'lead' ? 'track' : 'trackCustom', name === 'lead' ? 'Lead' : name, params);
  };

  function open(customize){
    var c = read() || {};
    stats.checked = !!c.stats; mkt.checked = !!c.mkt;
    opts.hidden = !customize; save.hidden = !customize; custom.hidden = !!customize;
    el.hidden = false;
  }
  function close(c){
    var had = read(); write(c); el.hidden = true;
    // consenso revocato dopo che gli script sono partiti: si ricarica la pagina per fermarli
    if ((had && had.stats && !c.stats && loaded.ga) || (had && had.mkt && !c.mkt && loaded.meta)) { location.reload(); return; }
    apply(c);
  }

  el.addEventListener('click', function(e){
    var b = e.target.closest('[data-cc]'); if (!b) return;
    var a = b.getAttribute('data-cc');
    if (a === 'accept') close({ stats: true, mkt: true });
    else if (a === 'reject') close({ stats: false, mkt: false });
    else if (a === 'custom') open(true);
    else if (a === 'save') close({ stats: stats.checked, mkt: mkt.checked });
  });
  document.addEventListener('click', function(e){ if (e.target.closest('[data-cookie-prefs]')) { e.preventDefault(); open(true); } });

  var c = read();
  if (c) apply(c); else open(false);
})();
