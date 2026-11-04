# Reel del libro (prova 1)

`libro-6passaggi-916.mp4`: 9:16, 43 secondi, senza voce, solo sottotitoli. Struttura «tutorial» (riferimento: video sul montaggio con Claude).

1. Gancio: «Perché l'ospite sceglie te?» con le schede Booking tutte uguali e il prezzo che scende.
2. «6 passaggi.»
3. Passi 01-06, ognuno con l'etichetta PASSO 0X / 06, il titolo evidenziato, una finestra animata e il sottotitolo: bisogno vero, alternative, unicità, persona giusta, categoria, trend.
4. Bonus: Positioning Canvas.
5. Ribaltamento: ~~Abbassare il prezzo~~ → Farti scegliere.
6. CTA: copertina, «Il metodo è nel libro.», 120 pagine · 6 passaggi · 19,90 €, **Link in bio**.

## Musica
Traccia originale generata su Artlist (Lyria 3 Pro, 60 s, strumentale), cartella «Hotel Positioning video libro». Dal cloud non si scarica (host cms-toolkit-artifacts.artlist.io bloccato). Per montarla: copiare il file in `progetto/public/musica.wav` e renderizzare con `--props='{"musica":"musica.wav"}'` (dissolvenza in entrata e in uscita già impostata). Oppure aggiungere la musica direttamente in Instagram.

## Render
    cd progetto && npm i
    npx remotion render Libro-6Passaggi-916 ../libro-6passaggi-916.mp4 --browser-executable=/opt/pw-browsers/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell

Codice delle scene: `progetto/src/video/Libro.tsx` (array `SCENE` con le durate).

# Reel 1 «Le pesche di mio nonno» e Reel 2 «La prima pagina» (da reel-libro-v1.md)

`reel1-pesche-916.mp4` (35") e `reel2-prima-pagina-916.mp4` (34"): versione senza riprese, grafica animata sui tempi dello script. Il testo a schermo è il titolo grande, la voce è il sottotitolo in basso. Il primo fotogramma funziona da copertina (titolo già visibile). Codice: `progetto/src/video/Reels.tsx` (array `REEL1` e `REEL2`: durata, frasi della voce, scena).

Servono anche da storyboard per girare la versione vera (Francesco in camera): stessi tempi e stesso testo a schermo.
Testo sotto il reel e link `?da=reel-pesche` / `?da=reel-prima-pagina`: vedi lo script.
