#!/bin/sh
# Lancia la diagnosi su tutte le estrazioni salvate e stampa voto e parametri (per misurare la variabilità del modello).
cd "$(dirname "$0")/.."
for f in veridia-landing olympic veridia club-family moko hoxton; do
  NODE_USE_ENV_PROXY=1 node diagnosi.js --estrazione prove/estrazioni/$f.json --salva prove/estrazioni/$f.risultato.json 2>/dev/null \
    | awk -v n="$f" 'NR==3{v=$1} /^Posizionamento/{p=$0} /^Hook/{h=$0} END{printf "%-16s %-8s %s | %s\n", n, v, p, h}'
done
