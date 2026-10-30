# Guida «Il tuo hotel paga tutti»

Lead magnet della landing /guida/. Copy v2 (30 ottobre 2026), 26 pagine.

- I testi stanno in `build_guida.py`, lo stile in `base.css`.
- Rigenerare: `python3 build_guida.py && node pdf.mjs` (serve Playwright), poi copiare `che-hotel-sei.pdf` in `site/src/assets/guida/`.
