# Hotel Positioning Library v4

Database di hotel classificati per posizionamento: 12 famiglie, 69 pattern, 19 categorie emergenti, 84 esempi.

| File | Contenuto |
|---|---|
| `library-v4.json` | Fonte unica dei dati: va modificato solo questo |
| `METODOLOGIA-v4.md` | Concetti, scale di valutazione, protocollo di verifica, lettura dei trend |
| `CORREZIONI-v4.md` | Cosa era sbagliato nella versione online e come è stato corretto |
| `export/*.csv` | Pattern, esempi e categorie per sito, Google Sheets e Notion (generati) |
| `tools/validate.py` | Controlla i dati e rigenera i CSV |

Dopo ogni modifica al JSON:

```
python3 hotel-library/tools/validate.py
```

Se lo script riporta errori, i dati non vanno pubblicati.
