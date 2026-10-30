/* Hotel Positioning · consenso ai cookie (GDPR, linee guida del Garante 2021)
   - nessuno script di terze parti prima del consenso;
   - "Rifiuta" e la X valgono quanto "Accetta tutti";
   - la scelta dura 6 mesi, poi il banner ricompare;
   - gli ID si impostano in window.HP_TRACKING (partial head.html): vuoti = disattivati. Con GTM, GA4 e pixel
     si configurano dentro il contenitore: lasciare vuoti ga4 e metaPixel qui, per non contare due volte.
   Eventi: window.HPtrack('lead', { form: 'candidatura' }, { eventID: '...' }) li manda a GA4 e Meta, solo se attivi.
   Se la scelta sui cookie non è ancora fatta, l'evento aspetta: parte appena l'utente accetta, si perde se rifiuta. */
(function(){
  var KEY = 'hp-consent', TTL = 182 * 864e5, cfg = window.HP_TRACKING || {};
  var el = document.getElementById('cc'); if (!el) return;
  var opts = document.getElementById('cc-opts'), stats = document.getElementById('cc-stats'), mkt = document.getElementById('cc-mkt');
  var save = document.getElementById('cc-save'), custom = document.getElementById('cc-custom');
  var loaded = { ga: false, meta: false, gtm: false };

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
  // Google Tag Manager: parte solo dopo un consenso (statistiche o marketing) e riceve lo stato del consenso
  // (Consent Mode v2), così i tag dentro GTM rispettano la scelta. Gli eventi del sito arrivano nel dataLayer.
  function consentState(c){ var a = c.stats ? 'granted' : 'denied', m = c.mkt ? 'granted' : 'denied';
    return { analytics_storage: a, ad_storage: m, ad_user_data: m, ad_personalization: m }; }
  function loadGTM(c){
    if (!cfg.gtm) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = window.gtag || function(){ dataLayer.push(arguments); };
    if (loaded.gtm) { gtag('consent', 'update', consentState(c)); return; }
    loaded.gtm = true;
    gtag('consent', 'default', consentState(c));
    gtag('js', new Date());
    dataLayer.push({ 'gtm.start': new Date().getTime(), event: 'gtm.js' });
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtm.js?id=' + encodeURIComponent(cfg.gtm);
    document.head.appendChild(s);
  }
  function apply(c){ if (c.stats || c.mkt) loadGTM(c); if (c.stats) loadGA(); if (c.mkt) loadMeta(); }

  var pending = [];
  function send(name, params, opts){
    params = params || {};
    if (loaded.gtm) dataLayer.push(Object.assign({ event: name === 'lead' ? 'generate_lead' : name }, params, opts && opts.eventID ? { event_id: opts.eventID } : {}));
    if (loaded.ga && window.gtag) gtag('event', name === 'lead' ? 'generate_lead' : name, params);
    if (loaded.meta && window.fbq) fbq(name === 'lead' ? 'track' : 'trackCustom', name === 'lead' ? 'Lead' : name, params, opts && opts.eventID ? { eventID: opts.eventID } : undefined);
  }
  window.HPtrack = function(name, params, opts){
    if (!read()) { pending.push([name, params, opts]); return; }
    send(name, params, opts);
  };
  // consenso ai cookie di marketing già dato? (serve al form per la Conversions API)
  window.HPconsent = function(){ var c = read(); return { stats: !!(c && c.stats), mkt: !!(c && c.mkt) }; };

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
    var q = pending; pending = []; q.forEach(function(a){ send(a[0], a[1], a[2]); });
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
