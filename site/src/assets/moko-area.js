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

  function wire(raw) {
    main.querySelectorAll("[data-copy]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var src = document.getElementById(btn.dataset.copy);
        var text = src.innerText.trim();
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
    main.querySelectorAll("[data-enc]").forEach(function (a) {
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
