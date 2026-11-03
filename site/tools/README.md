# Generatori

- `library/`: la pagina /library/ nasce dai dati.
  `python3 parse.py library.md data.json` estrae le schede dal testo della library,
  `python3 gen.py . ../../src/pages/library/index.html` unisce `template.html` e `data.json`.
  Per aggiungere o correggere un pattern basta modificare `data.json` e rilanciare `gen.py`.
- `problemi/`: le sei pagine /problemi/*. Il modello comune è in `common.py`, i contenuti
  di ogni pagina in `p_<slug>.py`. `python3 build_all.py` riscrive tutte e sei le pagine.

Dopo aver rigenerato, lancia `python3 build.py` dalla cartella `site/`.
- `library/en/`: la versione inglese di /en/library/. `python3 gen_en.py . ../../../src/pages/en/library/index.html` (dalla cartella `library/en/`) unisce `template_en.html` e `data_en.json`. Se cambia `data.json` italiano, va aggiornato a mano anche `data_en.json`.
