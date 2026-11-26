/* Area riservata Moko: decifra il contenuto della pagina con la password (PBKDF2-SHA256 + AES-GCM).
   La chiave derivata resta in sessionStorage fino alla chiusura della scheda o a «Esci». */
(function () {
  var KEY = "mk-moko-key";
  var meta = JSON.parse(document.getElementById("mk-payload").textContent);
  var main = document.getElementById("mk-main");
  var form = main.querySelector(".mk-lock");
  var err = main.querySelector(".mk-err");
  var out = document.querySelector(".mk-out");

  function b64(s) { return Uint8Array.from(atob(s), function (c) { return c.charCodeAt(0); }); }
  function toB64(u8) { var s = ""; for (var i = 0; i < u8.length; i++) s += String.fromCharCode(u8[i]); return btoa(s); }
  function storeGet() { try { var s = sessionStorage.getItem(KEY); return s ? b64(s) : null; } catch (e) { return null; } }
  function storeSet(raw) { try { sessionStorage.setItem(KEY, toB64(raw)); } catch (e) {} }
  function storeDel() { try { sessionStorage.removeItem(KEY); } catch (e) {} }

  async function derive(pw) {
    var base = await crypto.subtle.importKey("raw", new TextEncoder().encode(pw), "PBKDF2", false, ["deriveBits"]);
    var bits = await crypto.subtle.deriveBits({ name: "PBKDF2", salt: b64(meta.salt), iterations: meta.iter, hash: "SHA-256" }, base, 256);
    return new Uint8Array(bits);
  }
  async function decrypt(raw, dataB64) {
    var key = await crypto.subtle.importKey("raw", raw, "AES-GCM", false, ["decrypt"]);
    var buf = b64(dataB64);
    return crypto.subtle.decrypt({ name: "AES-GCM", iv: buf.slice(0, 12) }, key, buf.slice(12));
  }


  /* Registro di marcia: stato condiviso su Netlify (funzione /api/moko-registro), accesso con un token tratto dalla chiave */
  async function registro(raw) {
    var bar = main.querySelector("[data-registro]");
    var status = bar.querySelector(".rg-status"), sel = bar.querySelector(".rg-chi");
    var items = Array.prototype.slice.call(main.querySelectorAll("[data-rg]"));
    var API = "/api/moko-registro";
    var pre = new TextEncoder().encode("moko-registro:"), buf = new Uint8Array(pre.length + raw.length);
    buf.set(pre); buf.set(raw, pre.length);
    var tok = Array.prototype.map.call(new Uint8Array(await crypto.subtle.digest("SHA-256", buf)), function (b) { return b.toString(16).padStart(2, "0"); }).join("");
    var H = { "x-registro": tok };
    var stati = {}, online = false, vociInviate = false;
    try { var c = localStorage.getItem("mk-rg-chi"); if (c) sel.value = c; } catch (e) {}
    sel.addEventListener("change", function () { try { localStorage.setItem("mk-rg-chi", sel.value); } catch (e) {} });
    var d = new Date(), adesso = (d.getFullYear() - 2026) * 12 + (d.getMonth() + 1 - 12);
    var cur = main.querySelector("#rg-" + Math.max(0, Math.min(12, adesso)));
    bar.querySelector(".rg-now").addEventListener("click", function (e) { e.preventDefault(); if (cur) cur.scrollIntoView({ behavior: "smooth" }); });
    function voci() {
      return items.map(function (li) {
        return { id: li.dataset.rg, mese: +li.dataset.mese, tipo: li.dataset.tipo, testo: li.querySelector(".rg-t").textContent, chi: li.dataset.chi, entro: li.dataset.entro };
      });
    }
    function quando(iso) { try { return new Date(iso).toLocaleDateString("it-IT", { day: "numeric", month: "long" }); } catch (e) { return ""; } }
    function draw() {
      var fatte = 0, late = 0, perMese = {};
      items.forEach(function (li) {
        var st = stati[li.dataset.rg] || {}, s = st.s || "", m = +li.dataset.mese;
        li.querySelectorAll("[data-s]").forEach(function (b) { b.setAttribute("aria-pressed", b.dataset.s === s ? "true" : "false"); });
        li.dataset.state = s;
        var isLate = !s && m < adesso;
        li.classList.toggle("rg-late", isLate);
        li.querySelector(".rg-who").textContent = s ? (s === "fatto" ? "Fatto" : "Non serve") + (st.chi ? " · " + st.chi : "") + (st.quando ? " · " + quando(st.quando) : "") : (isLate ? "Rimasta indietro" : "");
        if (s === "fatto") fatte++;
        if (isLate) late++;
        var pm = perMese[m] || (perMese[m] = [0, 0]); pm[1]++; if (s) pm[0]++;
      });
      bar.querySelector(".rg-n-done").textContent = fatte + " su " + items.length;
      bar.querySelector(".rg-n-late").textContent = late; bar.querySelector(".rg-sum-late").classList.toggle("on", late > 0);
      main.querySelectorAll("[data-cnt]").forEach(function (el) { var pm = perMese[el.dataset.cnt] || [0, 0]; el.textContent = pm[0] + " su " + pm[1] + " chiuse."; });
    }
    async function load() {
      try {
        var r = await fetch(API, { headers: H, cache: "no-store" });
        if (!r.ok) throw new Error(r.status);
        var j = await r.json(); stati = j.stati || {}; online = true;
        vociInviate = j.voci === items.length;
        status.textContent = "Collegato: quello che segni lo vedono tutti." + (j.aggiornato ? " Ultima modifica il " + quando(j.aggiornato) + "." : "");
      } catch (e) {
        online = false;
        status.textContent = "Checklist non raggiungibile: quello che segni ora non viene salvato.";
      }
      bar.classList.toggle("rg-off", !online);
      draw();
    }
    items.forEach(function (li) {
      li.querySelectorAll("[data-s]").forEach(function (b) {
        b.addEventListener("click", async function () {
          var id = li.dataset.rg, prima = stati[id], s = b.dataset.s;
          if (s) stati[id] = { s: s, chi: sel.value, quando: new Date().toISOString() }; else delete stati[id];
          draw();
          if (!online) return;
          try {
            var body = { id: id, s: s, chi: sel.value };
            if (!vociInviate) body.voci = voci();
            var r = await fetch(API, { method: "POST", headers: Object.assign({ "content-type": "application/json" }, H), body: JSON.stringify(body) });
            if (!r.ok) throw new Error(r.status);
            vociInviate = true;
            status.textContent = "Salvato.";
          } catch (e) {
            if (prima) stati[id] = prima; else delete stati[id];
            draw();
            status.textContent = "Non salvato: riprova tra poco.";
          }
        });
      });
    });
    var pb = main.querySelector(".rg-prev"), po = main.querySelector(".rg-prev-out");
    if (pb) pb.addEventListener("click", async function () {
      po.hidden = false; po.textContent = "Preparo l'anteprima…";
      try {
        if (!vociInviate) {
          var first = items[0];
          await fetch(API, { method: "POST", headers: Object.assign({ "content-type": "application/json" }, H), body: JSON.stringify({ id: first.dataset.rg, s: (stati[first.dataset.rg] || {}).s || "", chi: sel.value, voci: voci() }) });
          vociInviate = true;
        }
        var r = await fetch(API + "?anteprima=1", { headers: H, cache: "no-store" });
        var j = await r.json();
        if (!j.email) { po.textContent = "Questo mese non c'è niente da mandare."; return; }
        po.innerHTML = "";
        var h = document.createElement("p"); h.className = "rg-subj"; h.textContent = "Oggetto: " + j.email.subject; po.appendChild(h);
        var f = document.createElement("iframe"); f.className = "rg-frame"; f.title = "Anteprima dell'email"; f.setAttribute("sandbox", ""); f.srcdoc = j.email.html; po.appendChild(f);
      } catch (e) { po.textContent = "Anteprima non disponibile: la checklist non è raggiungibile."; }
    });
    draw();
    load();
  }
  function wire(raw) {
    if (main.querySelector("[data-registro]")) registro(raw).catch(function () {});
    main.querySelectorAll(".copy").forEach(function (el, i) {
      if (!el.id) el.id = "cp-" + i;
      var btn = document.createElement("button");
      btn.type = "button"; btn.className = "mk-btn"; btn.textContent = "Copia"; btn.dataset.copy = el.id;
      el.classList.add("has-btn"); el.appendChild(btn);
    });
    main.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var src = document.getElementById(btn.dataset.copy);
        var text = src.innerText.replace(/\s*Copia(to)?\s*$/, "").trim();
        function done() {
          btn.textContent = "Copiato"; btn.classList.add("ok");
          setTimeout(function () { btn.textContent = "Copia"; btn.classList.remove("ok"); }, 1600);
        }
        function fallback() {
          var r = document.createRange(); r.selectNodeContents(src);
          var sel = window.getSelection(); sel.removeAllRanges(); sel.addRange(r);
          try { if (document.execCommand("copy")) done(); } catch (e) {}
        }
        if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done, fallback);
        else fallback();
      });
    });
    main.querySelectorAll("img[data-src-enc]").forEach(function (im) {
      fetch(im.dataset.srcEnc).then(function (r) { return r.text(); }).then(function (t) { return decrypt(raw, t.trim()); })
        .then(function (buf) { im.src = URL.createObjectURL(new Blob([buf], { type: "image/jpeg" })); im.classList.add("ok"); })
        .catch(function () {});
    });
    main.querySelectorAll("[data-tabs]").forEach(function (bar) {
      var btns = bar.querySelectorAll("[data-tab]");
      function show(id, push) {
        btns.forEach(function (b) { b.setAttribute("aria-selected", b.dataset.tab === id ? "true" : "false"); });
        main.querySelectorAll("[data-panel]").forEach(function (p) { p.hidden = p.dataset.panel !== id; });
        if (push) history.replaceState(null, "", "#" + id);
      }
      btns.forEach(function (b) { b.addEventListener("click", function () { show(b.dataset.tab, true); }); });
      var h = location.hash.slice(1);
      if (h && main.querySelector('[data-panel="' + h + '"]')) show(h, false);
    });
    main.querySelectorAll("[data-filter-group]").forEach(function (g) {
      g._apply = function (f) { apply(f, g.querySelector('[data-filter="4"]')); };
      function apply(f, b) {
          g.querySelectorAll("[data-filter]").forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
          main.querySelectorAll("[data-cat]").forEach(function (it) { it.hidden = f !== "*" && it.dataset.cat !== f && it.dataset.camp !== f; });
          main.querySelectorAll(".mt-group").forEach(function (gr) {
            var vis = gr.querySelectorAll(".mt-item:not([hidden])").length;
            gr.hidden = vis === 0; var n = gr.querySelector(".mt-n"); if (n) n.textContent = vis;
          });
      }
      g.querySelectorAll("[data-filter]").forEach(function (b) {
        b.addEventListener("click", function () { apply(b.dataset.filter, b);
        });
      });
    });
    (function () {
      var c = new URLSearchParams(location.search).get("c");
      if (!c) return;
      var b = main.querySelector('[data-filter="' + c + '"]');
      if (b) { b.click(); return; }
      var g = main.querySelector("[data-filter-group]");
      if (g) g._apply && g._apply(c);
    })();
    main.querySelectorAll("[data-check]").forEach(function (box) {
      var out = box.querySelector(".ck-out"), all = box.querySelectorAll("input");
      box.addEventListener("change", function () {
        var n = 0; all.forEach(function (i) { if (i.checked) n++; });
        out.textContent = n === all.length ? "10 su 10: si può pubblicare." : n + " su " + all.length;
        box.classList.toggle("done", n === all.length);
      });
    });
    var still = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    function grow(el) {
      el.querySelectorAll("[data-w]").forEach(function (b) { b.style.width = b.dataset.w + "%"; });
      el.querySelectorAll("[data-dash]").forEach(function (c) { c.style.strokeDasharray = c.dataset.dash; });
      el.querySelectorAll(".cnt").forEach(function (c) {
        var to = parseFloat(c.dataset.to), dec = +c.dataset.dec || 0, pre = c.dataset.pre || "", suf = c.dataset.suf || "";
        function fmt(v) { return pre + v.toFixed(dec).replace(".", ",").replace(/\B(?=(\d{3})+(?!\d))/g, ".") + suf; }
        if (still) { c.textContent = fmt(to); return; }
        var t0 = null;
        function step(t) { if (!t0) t0 = t; var k = Math.min(1, (t - t0) / 900); c.textContent = fmt(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); }
        requestAnimationFrame(step);
      });
    }
    var anim = main.querySelectorAll(".kt-grid, figure.ch, .stk");
    if ("IntersectionObserver" in window && !still) {
      var io = new IntersectionObserver(function (es) { es.forEach(function (e) { if (e.isIntersecting) { grow(e.target); io.unobserve(e.target); } }); }, { threshold: 0.25 });
      anim.forEach(function (el) { io.observe(el); });
    } else { anim.forEach(grow); }
    // Analisi: livelli di lettura
    main.querySelectorAll("[data-lv-set]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        main.dataset.level = btn.dataset.lvSet;
        main.querySelectorAll("[data-lv-set]").forEach(function (x) { x.setAttribute("aria-selected", x === btn ? "true" : "false"); });
        var first = main.querySelector('[data-lv="' + btn.dataset.lvSet + '"]') || main.querySelector("[data-lv]");
        if (first && btn.dataset.lvSet !== "3") first.scrollIntoView({ block: "start" });
      });
    });
    // Analisi: tutto quello che è «da confermare»
    main.querySelectorAll("[data-confirm]").forEach(function (box) {
      var list = box.querySelector(".conf-list"), n = 0;
      main.querySelectorAll(".acx .p-c").forEach(function (tag) {
        var blk = tag.closest("p, li, tr, .kpi, div"), sec = tag.closest(".acx");
        if (!blk || !sec) return;
        var t = blk.innerText.replace(/\s+/g, " ").trim();
        if (t.length > 220) t = t.slice(0, 217) + "…";
        var li = document.createElement("li");
        li.innerHTML = '<a href="#' + sec.id + '"></a>';
        li.firstChild.textContent = sec.dataset.title + " — " + t;
        list.appendChild(li); n++;
      });
      box.querySelector(".conf-n").textContent = "(" + n + ")";
    });
    // Analisi: indice laterale, capitolo attivo, avanzamento
    var side = main.querySelector(".an-side"), grid = main.querySelector(".an-grid"), prog = main.querySelector(".an-prog span");
    if (side && grid) {
      var links = side.querySelectorAll("[data-sec]");
      if ("IntersectionObserver" in window) {
        var so = new IntersectionObserver(function (es) {
          es.forEach(function (e) {
            if (e.isIntersecting) links.forEach(function (l) { l.classList.toggle("on", l.dataset.sec === e.target.id); });
          });
        }, { rootMargin: "-40% 0px -55% 0px" });
        main.querySelectorAll("section.acx").forEach(function (sx) { so.observe(sx); });
      }
      function onScroll() {
        var r = grid.getBoundingClientRect(), h = window.innerHeight;
        var p = Math.min(1, Math.max(0, (h * 0.4 - r.top) / (r.height)));
        if (prog) { prog.style.width = (p * 100).toFixed(1) + "%"; prog.parentNode.classList.toggle("show", r.top < h * 0.5 && r.bottom > 0); }
      }
      window.addEventListener("scroll", onScroll, { passive: true }); onScroll();
      var fab = main.querySelector(".an-fab");
      if (fab) {
        fab.addEventListener("click", function () { var o = document.body.classList.toggle("side-open"); fab.setAttribute("aria-expanded", o ? "true" : "false"); });
        side.addEventListener("click", function (e) { if (e.target.closest("a")) { document.body.classList.remove("side-open"); fab.setAttribute("aria-expanded", "false"); } });
      }
    }
    main.querySelectorAll("a[data-enc]").forEach(function (a) {
      a.addEventListener("click", async function (e) {
        e.preventDefault();
        a.classList.add("mk-busy");
        try {
          var txt = await (await fetch(a.dataset.enc)).text();
          var blob = new Blob([await decrypt(raw, txt.trim())], { type: a.dataset.type || "application/octet-stream" });
          var url = URL.createObjectURL(blob);
          var l = document.createElement("a"); l.href = url; l.download = a.dataset.name;
          document.body.appendChild(l); l.click(); l.remove();
          setTimeout(function () { URL.revokeObjectURL(url); }, 10000);
        } finally { a.classList.remove("mk-busy"); }
      });
    });
  }

  async function open(raw) {
    var html = new TextDecoder().decode(await decrypt(raw, meta.data));
    main.innerHTML = html;
    document.body.classList.add("mk-open");
    if (out) out.hidden = false;
    wire(raw);
    if (location.hash) { var el = document.getElementById(location.hash.slice(1)); if (el) el.scrollIntoView(); }
  }

  if (out) out.addEventListener("click", function () { storeDel(); location.reload(); });

  form.addEventListener("submit", async function (e) {
    e.preventDefault();
    err.hidden = true; form.classList.add("mk-busy");
    try {
      var raw = await derive(form.password.value);
      await open(raw);
      storeSet(raw);
    } catch (x) {
      err.hidden = false; form.classList.remove("mk-busy"); form.password.select();
    }
  });

  var saved = storeGet();
  if (saved) open(saved).catch(function () { storeDel(); });
})();
