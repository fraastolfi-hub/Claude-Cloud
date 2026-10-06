# Sito Hotel Positioning

Sito statico, senza framework. Le pagine si scrivono in `src/`, il sito pronto da pubblicare esce in `public/`.

## Comandi

```bash
python3 build.py          # rigenera public/
python3 build.py --serve  # rigenera e apre l'anteprima su http://localhost:8000
```

## Struttura

- `src/pages/` – una cartella per pagina (`libro/index.html` diventa `/libro/`)
- `src/partials/` – pezzi comuni: head, header, footer, form di candidatura
  (in una pagina: `<!-- @include header -->`)
- `src/assets/` – `style.css` (design system) e `site.js` (animazioni, menu, form)
- `ARCHITETTURA.md` – alberatura, tono di voce, fatti canonici, decisioni aperte

## Pubblicazione

Carica il contenuto di `public/` su Netlify, Cloudflare Pages o qualsiasi hosting statico.
Il file `public/_redirects` porta i vecchi indirizzi `/landing-*` sulle nuove pagine `/problemi/*`
(formato Netlify/Cloudflare; su altri hosting va tradotto).

## Prima di andare online

1. Collega i form (candidatura, bonus, smontaggio, quiz) al tuo CRM o servizio email:
   metti l'URL in `action=""` e aggiungi `data-endpoint="1"` al tag `<form>`.
2. Completa i segnaposto evidenziati in giallo tratteggiato (classe `.todo`).
3. Estendi la privacy policy ai nuovi form.
