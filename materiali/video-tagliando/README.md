# Video Meta · Tagliando Hotel · il calcolo del punteggio (Remotion)

Tre video animati, senza audio (la musica si aggiunge da Meta o da Instagram con la libreria con licenza). Stesso stile degli annunci statici T1-T8 (`materiali/ads-tagliando`). I risultati mostrati sono un **esempio**, e lo dicono a schermo: non un hotel reale.

| File | Video | Durata | Cosa si vede |
|---|---|---|---|
| V1-Calcolo_916.mp4 / _45.mp4 | Il calcolo | 14,4 s | «Il tuo sito merita un budget?» → contatore 0/21 → i 21 controlli si spuntano area per area (Messaggio, Prove, Velocità, Come ti legge l'AI) e ogni semaforo si accende → timbro «Non ancora. Prima va sistemato il messaggio.» → chiusura con la foto del meccanico |
| V2-Lancetta_916.mp4 / _45.mp4 | La lancetta | 9,4 s | «Quanto è efficace il tuo sito?» → un indicatore Non ancora / Quasi / Sì con la lancetta che cerca mentre scorrono i controlli («Controllo 9/21 · Prove · Domande frequenti») → si ferma su «Quasi. Qualche modifica prima di investire.» → chiusura |
| V3-Diagnosi_916.mp4 / _45.mp4 | La centralina | 10,6 s | «Fai il tagliando al tuo sito.» con la foto del meccanico → sotto, la diagnosi si stampa riga per riga con la barra 0→100% (prima schermata ✗, test di sostituzione ✗, recensioni ✓, pulsante prenota ✓, velocità 74/100, AI a metà) → «Verdetto: quasi.» → chiusura |

`_916` = Reels e Stories (1080×1920) · `_45` = feed (1080×1350).

Le etichette dei controlli sono i 21 controlli veri dell'algoritmo (`progetto/src/controlli.ts`, presi da `site/netlify/lib/tagliando.mjs`); gli esiti ✓/✗ sono quelli dell'esempio.

## Testi per Meta (pulsante «Scopri di più», stessa destinazione degli statici)

**V1 · Il calcolo** · `utm_content=v1`
> Il tuo sito merita un budget pubblicitario?
> 21 controlli su messaggio, prove, velocità e su come ti legge l'AI.
> Alla fine, un verdetto: sì, quasi, o non ancora.
> Gratis. Due minuti.
>
> Titolo: Il tuo sito merita un budget? · Descrizione: Il tagliando gratuito per hotel

**V2 · La lancetta** · `utm_content=v2`
> Quanto è efficace il tuo sito?
> Non «bello» o «brutto». Efficace: se chi arriva da un annuncio capisce perché scegliere te.
> Il tagliando lo misura in 21 controlli e ti dice dove si ferma la lancetta.
> Gratis. Due minuti.
>
> Titolo: Quanto è efficace il tuo sito? · Descrizione: 21 controlli, un verdetto

**V3 · La centralina** · `utm_content=v3`
> Dal meccanico, la centralina ti dice cosa non va prima che si rompa.
> Il tagliando fa lo stesso con il sito del tuo hotel: prima schermata, test di sostituzione, recensioni, pulsante, velocità, come ti legge l'AI.
> Prima della campagna. Non dopo.
> Gratis. Due minuti.
>
> Titolo: Fai il tagliando al tuo sito · Descrizione: Prima della campagna, gratis

URL: `https://hotelpositioning.com/tagliando/?utm_source=meta&utm_medium=paid&utm_campaign=tagliando&utm_content=vN`

## Modificare

    cd progetto && npm i && npx remotion studio

Testi e tempi in `src/video/*.tsx`, pezzi comuni (etichetta, titoli, chiusura con la foto) in `src/parts.tsx`, i 21 controlli in `src/controlli.ts`.
Nel workspace cloud il render usa il browser preinstallato:

    npx remotion render V1-Calcolo-916 out.mp4 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
