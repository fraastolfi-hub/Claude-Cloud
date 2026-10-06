# Generatori

- `library/`: la pagina /library/ nasce dai dati.
  `python3 parse.py library.md data.json` estrae le schede dal testo della library,
  `python3 gen.py . ../../src/pages/library/index.html` unisce `template.html` e `data.json`.
  Per aggiungere o correggere un pattern basta modificare `data.json` e rilanciare `gen.py`.
- `problemi/`: le sei pagine /problemi/*. Il modello comune è in `common.py`, i contenuti
  di ogni pagina in `p_<slug>.py`. `python3 build_all.py` riscrive tutte e sei le pagine.

Dopo aver rigenerato, lancia `python3 build.py` dalla cartella `site/`.
