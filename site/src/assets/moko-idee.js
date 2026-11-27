/* App delle idee Moko (/clienti/moko/idee/).
   Il contenuto (le idee) è cifrato con la password dell'area (PBKDF2-SHA256 + AES-GCM), come le altre pagine.
   Le decisioni stanno su Netlify (funzione /api/moko-idee), con lo stesso token del registro.
   In locale, senza la funzione, l'app va in «prova»: le decisioni restano solo in questo browser. */
(function () {
  "use strict";
  var KEY_S = "mk-moko-key", KEY_L = "mk-idee-key", PROVA = "mk-idee-prova", PROVA_RG = "mk-idee-prova-rg";
  var API = "/api/moko-idee", RG_API = "/api/moko-registro";
  var MAX_CODA = 10, SHOOTING = 8;
  var MOTIVI = { "non-moko": ["Non è Moko", "il tono o l'idea non ci somigliano"], "aggressiva": ["Troppo aggressiva", "punge troppo, anche se è vera"],
    "non-si-gira": ["Non si può fare", "mancano persone, spazi o permessi"], "gia-vista": ["Già vista", "l'abbiamo fatta o la fanno tutti"] };
  var TIPI = { telefono: "Col telefono", shooting: "Giornata di shooting", grafica: "Solo grafica" };
  var meta = JSON.parse(document.getElementById("mk-payload").textContent);
  var app = document.getElementById("ia");
  var lock = document.getElementById("lock");

  /* ---------- cifratura ---------- */
  function b64(s) { return Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); }); }
  function toB64(u8) { var s = ""; for (var i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]); return btoa(s); }
  function get(st, k) { try { var v = st.getItem(k); return v ? b64(v) : null; } catch (e) { return null; } }
  function put(st, k, raw) { try { st.setItem(k, toB64(raw)); } catch (e) {} }
  function del(st, k) { try { st.removeItem(k); } catch (e) {} }
  async function derive(pw) {
    var base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
    return new Uint8Array(await crypto.subtle.deriveBits({ name: "PBKDF2", salt: b64(meta.salt), iterations: meta.iter, hash: "SHA-256" }, base, 256));
  }
  async function decrypt(raw, dataB64) {
    var key = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
    var buf = b64(dataB64);
    return crypto.subtle.decrypt({ name: "AES-GCM", iv: buf.slice(0, 12) }, key, buf.slice(12));
  }

  /* ---------- stato ---------- */
  var RAW, D, IDX = {}, PIDX = {}, FIL = {}, stati = {}, rgStati = {}, rgInviate = false, H = {}, prova = false, online = true;
  var view = "oggi", coda = [], pos = 0, dettaglio = null, back = "oggi", lista = null;
  function esc(v) { return String(v == null ? "" : v).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function minu(t) { return t.charAt(0).toLowerCase() + t.slice(1); }
  function oggi() { return new Date().toLocaleDateString("sv-SE", { timeZone: "Europe/Rome" }); }
  function tra(giorni) { var d = new Date(); d.setDate(d.getDate() + giorni); return d.toLocaleDateString("sv-SE", { timeZone: "Europe/Rome" }); }
  function meseOra() {
    var p = oggi().split("-"), i = (+p[0] - 2026) * 12 + (+p[1] - 12);
    return Math.max(0, Math.min(D.mesi.length - 1, i));
  }
  function pst(id) { return stati[id] ? stati[id].s : ""; }
  function postDaFare() { var m = meseOra(); return D.post.filter(function (x) { return x.mese <= m && pst(x.id) === ""; }); }
  function rgs(id) { return rgStati[id] ? rgStati[id].s : ""; }
  function st(id) { var s = stati[id]; if (!s) return ""; if (s.s === "dopo" && s.f <= oggi()) return ""; return s.s; }
  function di(s) { return D.i.filter(function (x) { return st(x.id) === s; }); }

  // in fila: una per filone a giro, prima quelle da girare e poi la grafica
  function inFila() {
    var per = D.f.map(function (f) {
      return D.i.filter(function (x) { return x.f === f.k && st(x.id) === ""; })
        .sort(function (a, b) { return (a.k === "grafica") - (b.k === "grafica") || a.o - b.o; });
    });
    var out = [], giro = 0, any = true;
    while (any) { any = false; per.forEach(function (l) { if (l[giro]) { out.push(l[giro]); any = true; } }); giro++; }
    return out;
  }

  async function carica() {
    if (prova) {
      try { stati = JSON.parse(localStorage.getItem(PROVA) || "{}"); rgStati = JSON.parse(localStorage.getItem(PROVA_RG) || "{}"); } catch (e) { stati = {}; rgStati = {}; }
      return;
    }
    var r = await fetch(API, { headers: H, cache: "no-store" });
    if (r.status === 404 && /^(localhost|127\.0\.0\.1|\[::1\])$/.test(location.hostname)) { prova = true; return carica(); }
    if (!r.ok) throw new Error(r.status);
    stati = (await r.json()).stati || {};
    var g = await fetch(RG_API, { headers: H, cache: "no-store" });
    if (!g.ok) throw new Error(g.status);
    var gj = await g.json(); rgStati = gj.stati || {}; rgInviate = gj.voci >= D.rg.length;
  }
  async function salvaRg(id, s) {
    var prima = rgStati[id];
    if (s) rgStati[id] = { s: s, chi: "Giulia", quando: new Date().toISOString() }; else delete rgStati[id];
    if (prova) { try { localStorage.setItem(PROVA_RG, JSON.stringify(rgStati)); } catch (e) {} return true; }
    try {
      var body = { id: id, s: s, chi: "Giulia" };
      if (!rgInviate) body.voci = D.rg;
      var r = await fetch(RG_API, { method: "POST", headers: Object.assign({ "content-type": "application/json" }, H), body: JSON.stringify(body) });
      if (!r.ok) throw new Error(r.status);
      rgInviate = true; setOnline(true); return true;
    } catch (e) {
      if (prima) rgStati[id] = prima; else delete rgStati[id];
      setOnline(false); toast("Non salvata: controlla la connessione e riprova"); return false;
    }
  }
  async function salva(id, s, extra) {
    var prima = stati[id], v = s ? Object.assign({ s: s, t: new Date().toISOString() }, extra || {}) : null;
    if (v) stati[id] = v; else delete stati[id];
    if (prova) { try { localStorage.setItem(PROVA, JSON.stringify(stati)); } catch (e) {} return true; }
    try {
      var r = await fetch(API, { method: "POST", headers: Object.assign({ "content-type": "application/json" }, H), body: JSON.stringify(Object.assign({ id: id, s: s }, extra || {})) });
      if (!r.ok) throw new Error(r.status);
      var j = await r.json(); if (j.stato) stati[id] = j.stato;
      setOnline(true); return true;
    } catch (e) {
      if (prima) stati[id] = prima; else delete stati[id];
      setOnline(false); toast("Non salvata: controlla la connessione e riprova"); return false;
    }
  }

  /* ---------- immagini cifrate ---------- */
  var cache = {}, io = "IntersectionObserver" in window ? new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); carImg(e.target); } });
  }, { rootMargin: "300px" }) : null;
  function carImg(im) {
    var u = im.dataset.enc; if (!u) return;
    var p = cache[u] || (cache[u] = fetch(u).then(function (r) { return r.text(); }).then(function (t) { return decrypt(RAW, t.trim()); })
      .then(function (b) { return URL.createObjectURL(new Blob([b], { type: "image/jpeg" })); }));
    p.then(function (src) { im.src = src; }).catch(function () { delete cache[u]; });
  }
  function immagini() { app.querySelectorAll("img[data-enc]").forEach(function (im) { if (io) io.observe(im); else carImg(im); }); }
  function prefetch(x) { if (x && !cache[x.img]) { var im = new Image(); im.dataset.enc = x.img; carImg(im); } }

  /* ---------- pezzi ---------- */
  var tt;
  function toast(t) {
    var e = document.getElementById("toast"); e.textContent = t; e.hidden = false;
    clearTimeout(tt); tt = setTimeout(function () { e.hidden = true; }, 2200);
  }
  function setOnline(v) { online = v; var b = document.getElementById("off"); if (b) b.hidden = v; }
  function chips(x, conStato) {
    var s = st(x.id), lab = { si: "Da fare", fatta: "Fatta", pubblicata: "Pubblicata", no: "Scartata", dopo: "Messa da parte" }[stati[x.id] && stati[x.id].s] || "";
    return '<div class="chips"><span class="chip">' + esc(FIL[x.f].n) + '</span><span class="chip k-' + x.k + '">' + TIPI[x.k] + "</span>"
      + (conStato && lab ? '<span class="chip st">' + lab + (s === "no" && stati[x.id].m ? ": " + minu(MOTIVI[stati[x.id].m][0]) : "") + "</span>" : "") + "</div>";
  }
  function scheda(x) {
    return '<img class="shot" data-enc="' + esc(x.img) + '" alt="Prova dell\'idea: ' + esc(x.t) + '">' + chips(x, true)
      + '<h1 class="idea-t" tabindex="-1">' + esc(x.t) + '</h1><p class="idea-d">' + esc(x.d) + "</p>"
      + '<dl class="rows"><div class="row"><dt>Perché funziona</dt><dd>' + esc(x.p) + "</dd></div>"
      + '<div class="row"><dt>Cosa serve</dt><dd>' + esc(x.s) + "</dd></div>"
      + '<div class="row"><dt>Dove può uscire</dt><dd>' + esc(x.e) + "</dd></div>"
      + (x.n ? '<div class="row warn"><dt>Da confermare</dt><dd>' + esc(x.n) + "</dd></div>" : "") + "</dl>";
  }
  function item(x, azione) {
    var sub = x.k === "grafica" ? "dal modello, 5 minuti" : x.s;
    return '<div class="it"><button class="open" data-apri="' + x.id + '"><img data-enc="' + esc(x.img) + '" alt=""><span><b>' + esc(x.t) + "</b><small>" + esc(sub) + "</small></span></button>"
      + (azione ? '<button class="ck" data-azione="' + azione[0] + '" data-id="' + x.id + '">' + azione[1] + "</button>" : "") + "</div>";
  }
  function itemPost(x, azione) {
    return '<div class="it"><button class="open" data-post="' + x.id + '">' + (x.img ? '<img data-enc="' + esc(x.img) + '" alt="">' : '<span class="ph"></span>')
      + "<span><b>" + esc(x.t) + "</b><small>" + esc(x.fmt) + " · " + esc(x.c) + (x.mese < meseOra() ? " · da " + esc(D.mesi[x.mese].split(" ")[0].toLowerCase()) : "") + "</small></span></button>"
      + (azione ? '<button class="ck" data-azione="' + azione[0] + '" data-id="' + x.id + '">' + azione[1] + "</button>" : "") + "</div>";
  }
  function schedaPost(x) {
    var s = pst(x.id), lab = { fatta: "Fatto", pubblicata: "Pubblicato" }[s];
    return (x.img ? '<img class="shot sq" data-enc="' + esc(x.img) + '" alt="Foto per il post: ' + esc(x.t) + '">' : "")
      + '<div class="chips"><span class="chip">' + esc(x.c) + '</span><span class="chip k-grafica">' + esc(x.fmt) + '</span><span class="chip k-telefono">' + esc(D.mesi[x.mese]) + "</span>"
      + (lab ? '<span class="chip st">' + lab + "</span>" : "") + "</div>"
      + '<h1 class="idea-t" tabindex="-1">' + esc(x.t) + "</h1>"
      + (x.bis ? '<p class="idea-d">Per chi vuole: ' + esc(x.bis.charAt(0).toLowerCase() + x.bis.slice(1)) + "</p>" : "")
      + '<dl class="rows">' + (x.ov ? '<div class="row"><dt>Scritta sulla foto</dt><dd>' + esc(x.ov) + "</dd></div>" : "")
      + '<div class="row"><dt>Testo del post</dt><dd class="cap">' + esc(x.testo) + "</dd>"
      + '<button type="button" class="copia" data-copia="' + x.id + '">Copia il testo</button>'
      + (/\[/.test(x.testo) ? '<p class="note">Le parti tra parentesi quadre vanno completate prima di pubblicare.</p>' : "") + "</div>"
      + '<div class="row"><dt>Codice nel manuale</dt><dd>' + esc(x.cod) + "</dd></div></dl>";
  }
  function elenco(xs, azione, vuoto) { return xs.length ? xs.map(function (x) { return item(x, azione); }).join("") : '<p class="empty-l">' + vuoto + "</p>"; }

  /* ---------- schermate ---------- */
  function render(focus) {
    var main = document.getElementById("main"), dock = document.getElementById("dock"), tabs = document.getElementById("tabs");
    var fila = inFila(), da = di("si"), fatte = di("fatta");
    tabs.querySelectorAll("[data-tab]").forEach(function (b) { b.setAttribute("aria-current", b.dataset.tab === view || ((view === "dett" || view === "post") && b.dataset.tab === back) ? "page" : "false"); });
    var nb = da.length + postDaFare().length;
    tabs.querySelector('[data-tab="fare"] .bd').textContent = nb || "";
    tabs.querySelector('[data-tab="fare"] .bd').hidden = !nb;
    dock.hidden = true; tabs.hidden = false; dock.className = "dock";
    var h = "";

    if (view === "oggi") {
      var n = Math.min(MAX_CODA, fila.length), pub = di("pubblicata").length, no = di("no").length, dopo = D.i.filter(function (x) { return stati[x.id] && stati[x.id].s === "dopo" && st(x.id) === "dopo"; }).length;
      var tel = da.filter(function (x) { return x.k === "telefono"; }).length, sho = da.filter(function (x) { return x.k === "shooting"; }).length, gra = da.length - tel - sho;
      h = '<h1 class="t" tabindex="-1">Ciao Giulia</h1><p class="lead">Le idee per i social di Moko: scegli quelle che ti piacciono, falle, pubblicale.</p>'
        + '<h2 class="s">Oggi</h2>'
        + (n ? '<button class="stat hot" data-go="guarda"><span><b>Da guardare</b><small>sì, no o non ora' + (fila.length > n ? " · altre " + (fila.length - n) + " in fila" : "") + '</small></span><span class="n">' + n + "</span></button>"
             : '<div class="stat quiet"><span><b>Niente da guardare</b><small>le idee nuove arrivano con la mail del lunedì</small></span></div>')
        + '<button class="stat" data-tab="fare"><span><b>Le tue idee da fare</b><small>' + tel + " col telefono · " + sho + " da shooting · " + gra + ' di grafica</small></span><span class="n">' + da.length + "</span></button>"
        + (function () { var pd = postDaFare().length, m = meseOra(), cl = D.rg.filter(function (v) { return v.mese <= m && rgs(v.id) === ""; }).length;
            return '<button class="stat" data-tab="fare"><span><b>Post del piano</b><small>quelli di ' + esc(D.mesi[m].split(" ")[0].toLowerCase()) + ' e quelli rimasti indietro</small></span><span class="n">' + pd + "</span></button>"
              + '<button class="stat" data-tab="mese"><span><b>La checklist del mese</b><small>cosa va online, cosa preparare, cosa decidere</small></span><span class="n">' + cl + "</span></button>"; })()
        + '<button class="stat" data-tab="fare"><span><b>Fatte, da pubblicare</b><small>pronte per uscire</small></span><span class="n">' + (fatte.length + D.post.filter(function (x) { return pst(x.id) === "fatta"; }).length) + "</span></button>"
        + '<h2 class="s">Finora</h2>'
        + '<button class="stat" data-lista="pubblicata"><span><b>Pubblicate</b></span><span class="n">' + pub + "</span></button>"
        + '<button class="stat" data-lista="no"><span><b>Scartate</b><small>puoi sempre riguardarle</small></span><span class="n">' + no + "</span></button>"
        + (dopo ? '<button class="stat" data-lista="dopo"><span><b>Messe da parte</b><small>tornano da sole tra quattro settimane</small></span><span class="n">' + dopo + "</span></button>" : "")
        + '<div class="foot"><a href="' + esc(D.manuale) + '">Il manuale completo</a><button data-esci>Esci</button></div>';
    }

    if (view === "guarda") {
      tabs.hidden = true;
      if (pos >= coda.length) {
        var resto = inFila().length;
        h = '<div class="bar-top"><span></span><button data-tab="oggi">Chiudi</button></div><div class="fine"><b tabindex="-1">Fatto</b><p class="lead">'
          + (resto ? "Ce ne sono altre " + resto + " in fila. Puoi guardarle adesso o un altro giorno." : "Non ci sono altre idee da guardare. Le nuove arrivano con la mail del lunedì.")
          + "</p>" + (resto ? '<button class="btn pri" data-go="guarda">Guarda le prossime</button>' : "")
          + '<button class="btn ' + (resto ? "sec" : "pri") + '" data-tab="fare">Vedi cosa fare</button></div>';
      } else {
        var x = coda[pos];
        h = '<div class="bar-top"><span>' + (pos + 1) + " di " + coda.length + '</span><button data-tab="oggi">Chiudi</button></div>' + scheda(x);
        dock.hidden = false;
        dock.innerHTML = '<button class="btn sec" data-dec="no">No</button><button class="btn sec" data-dec="dopo">Non ora</button><button class="btn pri" data-dec="si">Sì, la faccio</button>';
        prefetch(coda[pos + 1]);
      }
    }

    if (view === "dett") {
      var y = IDX[dettaglio], s = stati[y.id] ? stati[y.id].s : "";
      tabs.hidden = true;
      h = '<div class="bar-top"><span></span><button data-indietro>Indietro</button></div>' + scheda(y);
      var az = s === "si" ? [["fatta", "Fatta", "pri"], ["", "Rimetti tra le idee", "sec"]]
        : s === "fatta" ? [["pubblicata", "Pubblicata", "pri"], ["si", "Non è ancora fatta", "sec"]]
        : s === "pubblicata" ? [["fatta", "Non è ancora uscita", "sec"]]
        : s === "no" || s === "dopo" ? [["", "Riguardala", "pri"]] : [["si", "Sì, la faccio", "pri"]];
      dock.hidden = false; dock.className = "dock " + (az.length === 2 ? "two" : "one");
      if (az.length === 2) az.reverse();
      dock.innerHTML = az.map(function (a) { return '<button class="btn ' + a[2] + '" data-set="' + a[0] + '">' + a[1] + "</button>"; }).join("");
    }

    if (view === "post") {
      var z = PIDX[dettaglio], zs = pst(z.id);
      tabs.hidden = true;
      h = '<div class="bar-top"><span></span><button data-indietro>Indietro</button></div>' + schedaPost(z);
      var pa = zs === "fatta" ? [["", "Non è ancora fatto", "sec"], ["pubblicata", "Pubblicato", "pri"]]
        : zs === "pubblicata" ? [["fatta", "Non è ancora uscito", "sec"]] : [["fatta", "Fatto", "pri"]];
      dock.hidden = false; dock.className = "dock " + (pa.length === 2 ? "two" : "one");
      dock.innerHTML = pa.map(function (a) { return '<button class="btn ' + a[2] + '" data-set="' + a[0] + '">' + a[1] + "</button>"; }).join("");
    }

    if (view === "mese") {
      var mi = meseOra(), TIPI_RG = [["online", "Va online"], ["prepara", "Da preparare"], ["decide", "Da decidere"], ["controlla", "Da controllare"]];
      var voce = function (v, conMese) {
        var s = rgs(v.id), info = [v.entro ? "entro il " + v.entro : "", v.chi, conMese ? D.mesi[v.mese] : ""].filter(Boolean).join(" · ");
        return '<div class="rg' + (s ? " chiusa" : "") + '"><p>' + esc(v.testo) + (info ? "<small>" + esc(info) + "</small>" : "")
          + (s ? '<small class="ok">' + (s === "fatto" ? "Fatto" : "Non serve") + (rgStati[v.id].chi ? " · " + esc(rgStati[v.id].chi) : "") + "</small>" : "") + "</p>"
          + '<div class="rg-b">' + (s ? '<button class="ck" data-rg="' + v.id + '" data-rgs="">Annulla</button>'
            : '<button class="ck" data-rg="' + v.id + '" data-rgs="saltato">Non serve</button><button class="ck pri" data-rg="' + v.id + '" data-rgs="fatto">Fatto</button>') + "</div></div>";
      };
      var del = D.rg.filter(function (v) { return v.mese === mi; }), ind = D.rg.filter(function (v) { return v.mese < mi && rgs(v.id) === ""; });
      var fatte_n = del.filter(function (v) { return rgs(v.id); }).length;
      h = '<h1 class="t" tabindex="-1">' + esc(D.mesi[mi]) + '</h1><p class="lead">' + esc(D.fasi[mi]) + ". " + fatte_n + " su " + del.length + " chiuse.</p>"
        + (ind.length ? '<h2 class="s">Rimasto indietro</h2>' + ind.map(function (v) { return voce(v, true); }).join("") : "")
        + TIPI_RG.map(function (tp) { var g = del.filter(function (v) { return v.tipo === tp[0]; }); return g.length ? '<h2 class="s">' + tp[1] + "</h2>" + g.map(function (v) { return voce(v, false); }).join("") : ""; }).join("")
        + '<p class="note" style="margin-top:18px">È la stessa checklist dell\'area: quello che segni qui lo vedono tutti, e il primo del mese arriva il promemoria con quello che manca.</p>';
    }

    if (view === "fare") {
      var pd = postDaFare(), pf = D.post.filter(function (x) { return pst(x.id) === "fatta"; });
      var t = da.filter(function (x) { return x.k === "telefono"; }), sh = da.filter(function (x) { return x.k === "shooting"; }), g = da.filter(function (x) { return x.k === "grafica"; });
      h = '<h1 class="t" tabindex="-1">Da fare</h1>'
        + '<h2 class="s">Post del piano · ' + esc(D.mesi[meseOra()]) + '</h2><p class="note">Già decisi: hanno il testo pronto e un mese. Tocca «Fatto» quando è pronto, «Pubblicato» quando è uscito.</p>'
        + (pd.length ? pd.map(function (x) { return itemPost(x, ["fatta", "Fatto"]); }).join("") : '<p class="empty-l">Nessuno, per questo mese.</p>')
        + (pf.length ? '<h2 class="s">Post fatti, da pubblicare</h2>' + pf.map(function (x) { return itemPost(x, ["pubblicata", "Pubblicato"]); }).join("") : "")
        + '<h2 class="s">Le tue idee · col telefono</h2><p class="note">Dieci o quindici minuti, quando sei in hotel. Tocca «Fatta» quando l\'hai girata.</p>'
        + elenco(t, ["fatta", "Fatta"], "Nessuna, per ora.")
        + '<h2 class="s">Le tue idee · giornata di shooting</h2><div class="meter"><i style="width:' + Math.min(100, sh.length / SHOOTING * 100) + '%"></i></div>'
        + '<p class="note">' + sh.length + " di " + SHOOTING + ". Quando sono " + SHOOTING + " si fissa la giornata e si decide se chiamare un fotografo.</p>"
        + elenco(sh, ["fatta", "Fatta"], "Nessuna, per ora.")
        + '<h2 class="s">Le tue idee · solo grafica</h2><p class="note">Niente da girare: si preparano dal modello.</p>'
        + elenco(g, ["fatta", "Fatta"], "Nessuna, per ora.")
        + '<h2 class="s">Idee fatte, da pubblicare</h2>' + elenco(fatte, ["pubblicata", "Pubblicata"], "Nessuna, per ora.");
    }

    if (view === "lista") {
      var L = { pubblicata: ["Pubblicate", di("pubblicata")], no: ["Scartate", di("no")],
        dopo: ["Messe da parte", D.i.filter(function (x) { return st(x.id) === "dopo"; })] }[lista];
      h = '<div class="bar-top"><span></span><button data-tab="oggi">Indietro</button></div><h1 class="t" tabindex="-1">' + L[0] + "</h1>"
        + elenco(L[1], lista === "pubblicata" ? null : ["", "Riguardala"], "Nessuna.");
    }

    if (view === "filoni") {
      var rows = D.f.map(function (f) {
        var xs = D.i.filter(function (x) { return x.f === f.k; }), si = 0, no = 0, mot = {};
        xs.forEach(function (x) { var s = stati[x.id] && stati[x.id].s; if (s === "si" || s === "fatta" || s === "pubblicata") si++; else if (s === "no") { no++; mot[stati[x.id].m] = (mot[stati[x.id].m] || 0) + 1; } });
        return { f: f, n: xs.length, si: si, no: no, mot: mot };
      }).sort(function (a, b) { return b.si - a.si || a.no - b.no; });
      h = '<h1 class="t" tabindex="-1">I tuoi filoni</h1><p class="lead">Ogni idea appartiene a un filone. Quelli che prendono più sì diventano la strategia di Moko per il 2027.</p>'
        + rows.map(function (r) {
          var m = Object.keys(r.mot).map(function (k) { return minu(MOTIVI[k][0]) + (r.mot[k] > 1 ? " (" + r.mot[k] + ")" : ""); }).join(", ");
          return '<div class="fil"><div class="h">' + esc(r.f.n) + "<span>" + r.si + " sì · " + r.no + " no</span></div>"
            + '<div class="pips" aria-hidden="true">' + "<i></i>".repeat(r.si) + '<i class="no"></i>'.repeat(r.no) + '<i class="wait"></i>'.repeat(r.n - r.si - r.no) + "</div>"
            + "<small>" + esc(r.f.d) + (m ? " · No: " + esc(m) : "") + "</small></div>";
        }).join("")
        + '<p class="note" style="margin-top:18px">Francesco e Nicola vedono i motivi dei no, così le idee nuove arrivano più vicine a quello che cerchi.</p>';
    }

    main.innerHTML = h;
    main.parentElement.scrollTop = 0; window.scrollTo(0, 0);
    immagini();
    if (focus) { var f = main.querySelector("[tabindex='-1']"); if (f) f.focus({ preventScroll: true }); }
  }

  function vai(v, focus) {
    if (v === "guarda") { coda = inFila().slice(0, MAX_CODA); pos = 0; }
    view = v; render(focus !== false);
  }

  /* ---------- azioni ---------- */
  async function decidi(d, motivo) {
    var x = coda[pos]; if (!x) return;
    var extra = d === "no" ? { m: motivo } : d === "dopo" ? { f: tra(28) } : null;
    if (!(await salva(x.id, d, extra))) return;
    toast(d === "si" ? (x.k === "shooting" ? "Aggiunta alla giornata di shooting" : x.k === "telefono" ? "Aggiunta a «Col telefono»" : "Aggiunta alla grafica da fare")
      : d === "no" ? "Scartata: " + minu(MOTIVI[motivo][0]) : "Torna tra quattro settimane");
    pos++; render(true);
  }
  var veil = document.getElementById("veil");
  function chiediMotivo() { veil.hidden = false; veil.querySelector(".opt").focus(); }
  function chiudiMotivo() { veil.hidden = true; var b = document.querySelector('[data-dec="no"]'); if (b) b.focus(); }

  document.addEventListener("click", async function (e) {
    var t = e.target.closest("button,a"); if (!t || !RAW) return;
    if (t.dataset.tab) { dettaglio = null; vai(t.dataset.tab); }
    else if (t.dataset.go) vai(t.dataset.go);
    else if (t.dataset.lista) { lista = t.dataset.lista; vai("lista"); }
    else if (t.dataset.dec) { if (t.dataset.dec === "no") chiediMotivo(); else decidi(t.dataset.dec); }
    else if (t.dataset.motivo) { veil.hidden = true; decidi("no", t.dataset.motivo); }
    else if (t.hasAttribute("data-annulla")) chiudiMotivo();
    else if (t.dataset.post) { back = view; dettaglio = t.dataset.post; view = "post"; render(true); }
    else if (t.dataset.rg) { if (await salvaRg(t.dataset.rg, t.dataset.rgs)) { toast({ "": "Riaperta", fatto: "Segnata come fatta", saltato: "Segnata: non serve" }[t.dataset.rgs]); render(false); } }
    else if (t.dataset.copia) {
      var tx = PIDX[t.dataset.copia].testo, gaps = (tx.match(/\[[^\]]*\]/g) || []).length;
      try { await navigator.clipboard.writeText(tx); toast(gaps ? "Copiato · " + gaps + (gaps > 1 ? " parti" : " parte") + " da completare" : "Copiato"); }
      catch (x) { toast("Non riesco a copiare: tieni premuto sul testo"); }
    }
    else if (t.dataset.apri) { back = view === "lista" ? "lista" : view; dettaglio = t.dataset.apri; view = "dett"; render(true); }
    else if (t.hasAttribute("data-indietro")) { view = back; render(true); }
    else if (t.dataset.set !== undefined) {
      var s = t.dataset.set;
      var isPost = view === "post";
      if (await salva(dettaglio, s)) { toast(isPost ? { "": "Di nuovo da fare", fatta: "Segnato come fatto", pubblicata: "Segnato come pubblicato" }[s]
        : { "": "Di nuovo tra le idee da guardare", si: "Di nuovo da fare", fatta: "Segnata come fatta", pubblicata: "Segnata come pubblicata" }[s]); view = back; render(true); }
    }
    else if (t.dataset.azione !== undefined) {
      var a = t.dataset.azione;
      if (await salva(t.dataset.id, a)) { toast({ "": "Di nuovo tra le idee da guardare", fatta: "Passa tra quelle da pubblicare", pubblicata: "Segnata come pubblicata" }[a]); render(false); }
    }
    else if (t.hasAttribute("data-esci")) { del(localStorage, KEY_L); del(sessionStorage, KEY_S); location.reload(); }
    else if (t.hasAttribute("data-riprova")) { try { await carica(); setOnline(true); render(false); } catch (x) { setOnline(false); } }
  });
  veil.addEventListener("click", function (e) { if (e.target === veil) chiudiMotivo(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape" && !veil.hidden) chiudiMotivo(); });

  /* ---------- apertura ---------- */
  async function apri(raw) {
    D = JSON.parse(new TextDecoder().decode(await decrypt(raw, meta.data)));
    RAW = raw;
    D.f.forEach(function (f) { FIL[f.k] = f; });
    D.i.forEach(function (x, i) { x.o = i; IDX[x.id] = x; });
    D.post.forEach(function (x) { PIDX[x.id] = x; });
    var pre = new TextEncoder().encode("moko-registro:"), buf = new Uint8Array(pre.length + raw.length);
    buf.set(pre); buf.set(raw, pre.length);
    H = { "x-registro": Array.prototype.map.call(new Uint8Array(await crypto.subtle.digest("SHA-256", buf)), function (b) { return b.toString(16).padStart(2, "0"); }).join("") };
    lock.hidden = true; app.querySelector(".shell").hidden = false;
    try { await carica(); } catch (e) { setOnline(false); }
    document.getElementById("prova").hidden = !prova;
    var q = location.hash.slice(1);
    vai(q === "guarda" || q === "fare" || q === "mese" || q === "filoni" ? q : "oggi", false);
  }

  lock.addEventListener("submit", async function (e) {
    e.preventDefault();
    var err = lock.querySelector(".err"); err.hidden = true; lock.classList.add("busy");
    try {
      var raw = await derive(lock.password.value);
      await apri(raw);
      put(sessionStorage, KEY_S, raw);
      if (lock.ricorda.checked) put(localStorage, KEY_L, raw);
    } catch (x) { err.hidden = false; lock.classList.remove("busy"); lock.password.select(); }
  });

  var saved = get(localStorage, KEY_L) || get(sessionStorage, KEY_S);
  if (saved) apri(saved).catch(function () { del(localStorage, KEY_L); del(sessionStorage, KEY_S); lock.hidden = false; });
  else lock.hidden = false;
})();
