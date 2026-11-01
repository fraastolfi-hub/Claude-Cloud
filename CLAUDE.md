# Note per Claude

## Pubblicazione del sito (Netlify, piano Pro a crediti)
- Ogni deploy in produzione costa 15 crediti su 3.000 al mese. I deploy dei branch costano 0.
- Lavora e fai push solo sul branch di sviluppo. Porta su `main` solo quando Francesco scrive «pubblica» (o a fine giornata se lo chiede), raggruppando le modifiche in un unico push.
- `netlify.toml` salta la build se il commit non tocca `site/`: i materiali in `materiali/` non generano deploy.
- I file per gli annunci Meta non stanno sul sito: si caricano su Meta e basta (se serve un URL pubblico temporaneo, toglierlo dopo il caricamento).
