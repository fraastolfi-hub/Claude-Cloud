# Tocq · regole di marca per il sito

Fonte: *Tocq Hotel Milano Brand Guidelines, Brand Book v1.0, novembre 2018* (`BRANDGUIDELINES_TOCQ.pdf`, cartella Drive del cliente).
Qui sotto c'è come ogni regola è applicata nella bozza, e cosa manca per applicarla del tutto.

## Marchio

| Regola del brand book | Nel sito |
|---|---|
| Simbolo (porta che si apre, finestra su Milano, linee dell'edificio) + logotipo TOCQ + HOTEL MILANO | Tracciati vettoriali ricavati dal file `logo-TOCQ_neg.pdf`, senza ridisegnare nulla |
| Versione verticale = principale | Footer e materiali; `assets/img/logo-verticale.svg` (nero) e `logo-verticale-neg.svg` (bianco) |
| Versione orizzontale solo dove lo spazio in verticale è ridotto (pag. 14) | Solo nell'header (barra alta 80 px): `logo-orizzontale.svg` |
| Area di rispetto = 1/3 dell'altezza del simbolo (pag. 16) | Header: marchio alto 44 px dentro 80 px, quindi 18 px liberi sopra e sotto; nessun elemento entro 15 px a destra |
| Dimensione minima di stampa 20 mm, consigliata 30 mm (pag. 18) | Sul web: marchio orizzontale mai sotto 36 px di altezza, verticale mai sotto 80 px |
| Negativo bianco su fondi scuri; nero o bianco sui fondi colorati secondo la leggibilità (pag. 17, 21) | Bianco su nero nel footer; mai il marchio in corallo o verde |
| Su foto solo con contrasto sufficiente (pag. 20) | Regola da rispettare quando entrano le foto vere |
| Simbolo da solo | `assets/img/simbolo.svg`, per favicon e icona app |

## Colori (pag. 19)

Valori campionati dal PDF del brand book.

| Colore | Riferimento | 100% | 80% | 50% | 20% |
|---|---|---|---|---|---|
| **Nero** (primario) | C60 M40 Y40 K100 · Pantone Process Black C | `#000000` | `#484848` | `#939393` | `#d6d6d6` |
| **Corallo** (secondario) | C0 M40 Y50 K10 · Pantone 472 C | `#d2a275` | `#dbb38e` | `#e9cfb4` | `#f7ebe0` |
| **Verde** (secondario) | C65 M35 Y60 K25 · Pantone 5615 C | `#5d6f5d` | `#798674` | `#a7ada0` | `#dadbd5` |

Uso nel sito: bianco e nero per testo, fondi e bottoni principali (come in tutta la corporate identity del brand book); corallo per i dati in evidenza su nero (tabellone, riepilogo del configuratore, bottoni su fondo nero) e per i fondi chiari al 20%; verde per le etichette e le frecce sui fondi bianchi.

Nota: il campione chiamato "Corallo" nel brand book è un salmone/cuoio, non un rosso corallo. Il pattern lo chiama infatti "Salmone".

## Carattere (pag. 29)

- **Futura Std** per tutte le parti verbali: Light per il testo, Medium per etichette e bottoni (maiuscolo spaziato), Bold per i titoli.
- Futura Std è un carattere a licenza. In produzione va servito con licenza web (Adobe Fonts "Futura PT" o licenza webfont di Futura Std). La bozza usa **Jost**, sostituto libero dallo stesso disegno geometrico, solo come segnaposto: il CSS chiama già Futura per prima, quindi sui computer che l'hanno installata si vede quella vera.

## Lettering (pag. 25–28)

Il brand book prevede un lettering proprietario, nato dal simbolo, per "le aree più significative" (RESTAURANT, BAR, RECEPTION, SALA DUOMO…). **Non è nei file ricevuti**: serve il font o i tracciati vettoriali. Nel sito andrebbe usato con parsimonia, come nel brand book: nomi delle sale nella pagina Meeting, titoli di sezione brevi. Finché manca, la bozza non lo imita.

## Pattern (pag. 31–34)

- Ricostruito dal vettoriale del brand book come tessera ripetibile senza giunture: `assets/img/pattern-*.svg`.
- Combinazioni previste dal brand book e preparate: nero/bianco, nero 80/nero 50, salmone/salmone 80, salmone 20/salmone 50, verde/verde 80, verde 20/verde 50, bianco/nero.
- Nel sito: solo fasce decorative (oggi la fascia salmone sopra il footer), mai sotto il testo corrente.

## Pittogrammi (pag. 36–37)

Disabili, uomini, donne, guardaroba, ascensore, bagagli, scale, frecce direzionali, vietato fumare. Sono pensati per la segnaletica interna. Nella bozza ne riprende il segno solo la freccia degli elenchi. Per usarli nel sito (servizi della camera, deposito bagagli) servono i file vettoriali.

## Cosa manca

1. File vettoriale originale del **marchio in positivo** (in cartella c'è solo il negativo: il positivo della bozza è ricavato da lì).
2. File del **lettering** proprietario.
3. **Licenza web** di Futura Std, o decisione di usare Futura PT da Adobe Fonts.
4. **Pittogrammi** in vettoriale.
5. **Foto approvate** per il web: l'archivio in Drive ha oltre cento scatti con nomi di file non descrittivi.
