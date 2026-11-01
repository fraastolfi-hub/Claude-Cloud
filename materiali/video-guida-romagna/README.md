# Video Meta · guida Romagna (Remotion)

Video tipografici animati, senza audio (la musica si aggiunge da Meta o da Instagram con la libreria con licenza).

| File | Annuncio | Durata |
|---|---|---|
| R1-Mare_916.mp4 / _45.mp4 | R1 Il mare non è tuo | 9 s |
| R2-TreSecondi_916.mp4 / _45.mp4 | R2 Tre secondi sull'A14 | 9,2 s |
| R3-Regalato_916.mp4 / _45.mp4 | R3 Le sdraio a luglio | 11,6 s |
| R8-Rimini_916.mp4 / _45.mp4 | R8 Le slide da Milano (foto) | 9,4 s |

`_916` = Reels e Stories (1080×1920) · `_45` = feed (1080×1350).

Modificare: `cd progetto && npm i && npx remotion studio`. Testi nei file `src/video/*.tsx`, stile comune in `src/parts.tsx`.

## Reel dal copione (meta-reel-guida-romagna.md)

Cartella `reel/`, tutti 1080×1920 a 30 fps, senza audio, sottotitoli già bruciati.

| File | Reel | Durata | Stato |
|---|---|---|---|
| Reel1-MareNonTuo.mp4 | 1 · Il mare non è tuo | 30 s | **modello**: riquadri "ripresa da girare" dove va il girato |
| Reel2-TreSecondi.mp4 | 2 · Tre secondi | 20 s | pronto |
| Reel3-Tovagliolo.mp4 | 3 · Il tovagliolo | 22 s | pronto |
| Reel4-CopriIlLogo.mp4 | 4 · Copri il logo | 20 s | pronto |
| Reel5-Buttadentro.mp4 | 5 · Il buttadentro | 25 s | **modello**: riquadri "ripresa da girare" |
| Reel6-SiRicordavaIlMare.mp4 | 6 · Si ricordava il mare | 15 s | pronto (muto per scelta) |
| Reel7-FormulaCoperta.mp4 | 7 · La formula coperta | 18 s | pronto |

Reel 1 e 5: girare in verticale, mettere il file in `progetto/public/` e rigenerare:

    cd progetto && npm i
    npx remotion render Reel1-MareNonTuo out.mp4 --props='{"clip":"girato.mp4"}'

Codice dei reel in `progetto/src/reel/`, sottotitoli nell'array `subs` di ogni file.
La voce fuori campo e la musica vanno aggiunte in montaggio o da Instagram.

## Reel con la voce (Reel 2, 3, 4, 7)

File `reel/*-voce.mp4`. Voce di Francesco (originali in `voce-originale/`), tagliata battuta per battuta, velocizzata del 7%, ripulita e portata a −16 LUFS.
La voce detta i tempi: ogni scena parte quando parte la sua battuta (componente `src/reel/Voce.tsx`, tempi in `src/reel/voce.json`).
Per rifare il taglio dopo una nuova registrazione: `python3 voce.py` (richiede le trascrizioni con i tempi delle parole), poi `npx remotion render Reel2-TreSecondi-voce`.
Senza musica: si aggiunge da Ads Manager (libreria suoni di Meta) o con Artlist.
