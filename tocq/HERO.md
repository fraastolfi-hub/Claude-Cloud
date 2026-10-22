# Tocq · l'hero del nuovo sito

Tre proposte per la prima schermata, tutte costruite sull'origine del marchio nel brand book: il simbolo è **"una porta che si apre"** e **"una finestra su Milano"**. Tutte e tre funzionano oggi con una foto e sono pronte per un video.

| | A · La finestra su Milano | B · Dal binario alla camera | C · Le ante |
|---|---|---|---|
| Dove vederla | `bozza/index.html` (già in home) | `bozza/proposte-hero/hero-b.html` | `bozza/proposte-hero/hero-c.html` |
| Cosa si vede | Foto o video a schermo intero. Le ante del simbolo si aprono sull'immagine; titolo grande in bianco; barra con 4 numeri in basso | Un contatore va da 00:00 a 03:00 mentre scorrono stazione, hall e camera: il tragitto reale dal treno al letto | Il simbolo del marchio grande, con foto o video visibile solo dentro le due ante |
| Cosa dice | Il prodotto: la camera con le torri di Porta Nuova | La promessa: tre minuti dal binario | Il marchio: una porta aperta su Milano |
| Forza | Massimo impatto visivo, standard dei siti di hotel di fascia alta | La più specifica: nessun altro hotel di Milano può dirlo così | La più riconoscibile e proprietaria |
| Rischio | Dipende tutto dalla qualità del video o della foto | Il contatore va tarato sul tempo vero (da cronometrare) | Su mobile l'immagine dentro le ante è piccola |

## Raccomandazione

**A come hero, con il video del tragitto di B dentro.** La prima schermata è a tutto schermo (A), e il video racconta i 3 minuti dal binario alla camera (B). Le ante del simbolo si aprono all'inizio, una sola volta. C resta come motivo grafico per la call to action finale, dove c'è già.

Così l'hero tiene insieme le tre cose che contano: impatto visivo, la promessa vera ("Scendi a Garibaldi. Sei arrivato.") e il marchio.

## Brief per il video dell'hero

**Idea:** "Tre minuti." Un unico movimento continuo, dal binario di Porta Garibaldi al cuscino sul letto, montato in 15 secondi. Niente persone in primo piano: l'ospite è chi guarda.

**Storyboard (15 secondi, in loop):**

| Tempo | Inquadratura | Note |
|---|---|---|
| 0–2 s | Binario di Porta Garibaldi all'alba o al tramonto, un treno che si ferma. Camera ad altezza occhi, avanza | Luce calda, poche persone sfocate |
| 2–5 s | Uscita dalla stazione: le torri di Porta Nuova si aprono davanti, la camera gira verso Via Tocqueville | Il momento "finestra su Milano" |
| 5–7 s | Il portone del Tocq che si apre (due ante, come il simbolo) | Ripresa frontale, simmetrica: è il raccordo con le ante animate del sito |
| 7–10 s | La hall: velluto verde, lamelle dorate, la reception con qualcuno che alza lo sguardo e sorride | Unico volto, di passaggio, con liberatoria |
| 10–13 s | Corridoio, porta della camera che si apre, finestra con le torri | Tende che si aprono da sole (movimento lento) |
| 13–15 s | Il cuscino scelto sul letto, una mano che lo sistema. Dissolvenza al nero per il loop | Chiude sul servizio, non sulla stanza vuota |

**Specifiche tecniche:**
- Due tagli dallo stesso girato: **16:9 orizzontale** (1920×1080) e **9:16 verticale** (1080×1920) per mobile e social.
- 12–15 secondi, loop pulito (primo e ultimo fotogramma compatibili), **senza audio**.
- Esportazione web: MP4 H.264 e WebM, **sotto i 4 MB** per il 16:9 e sotto i 3 MB per il 9:16; più un fotogramma di copertina in WebP per chi non vede il video.
- Spazio libero a sinistra (circa 40% dell'inquadratura) nel 16:9 e in basso nel 9:16, dove sta il testo.
- Colore: neri profondi e toni caldi vicini al corallo del brand book (Pantone 472); evitare il blu freddo.
- Girato con gimbal; dove serve, un drone indoor solo per l'uscita dalla stazione.
- Liberatorie per ogni persona riconoscibile; permesso RFI/Grandi Stazioni per riprendere in stazione (oppure partire dall'uscita, in strada).

**Come si inserisce nel sito:** basta copiare i file in `bozza/assets/video/` e scrivere il nome in `data-video-mp4` e `data-video-webm` nell'hero (`src/pages/index.html`). Il codice c'è già:
- il video parte muto e in loop, con la foto come copertina;
- non parte con l'impostazione "riduci movimento" del sistema né con il risparmio dati attivo;
- ha un bottone "Pausa" sempre visibile.

**Foto di riserva per lo shooting:** se il video non si fa subito, servono almeno due foto orizzontali ad alta risoluzione (3000 px): la camera con le torri all'alba, e il portone di Via Tocqueville con le ante aperte.

## Recensioni Trustindex

Sì, hanno senso, ma non nell'hero: un widget esterno rallenterebbe la prima schermata, che è quella che conta di più per Google (LCP). Sono quindi nel capitolo **"Il ritorno"**, dopo i voti:
- il widget si carica solo quando la sezione si avvicina allo schermo;
- finché non c'è l'ID, mostra tre recensioni vere scelte a mano, che restano anche come riserva se il servizio non risponde;
- per attivarlo basta l'ID del widget (lo snippet di Trustindex `loader.js?ID`) in `data-trustindex`, nella home.

Da decidere quando si configura il widget su Trustindex:
1. **Filtro:** solo recensioni da 4 stelle in su, e preferibilmente in italiano e inglese.
2. **Piattaforme:** Google, Booking, TripAdvisor ed Expedia insieme; Expedia (8,8) alza la media.
3. **Stile:** fondo chiaro, carattere ereditato dal sito, niente stelline colorate fuori palette.
4. **Dati strutturati:** disattivare quelli di Trustindex per le recensioni sul proprio sito, perché Google non li accetta per un hotel che pubblica le sue recensioni.
5. **Privacy:** aggiungere Trustindex all'informativa e al banner dei cookie, se il widget ne imposta.
