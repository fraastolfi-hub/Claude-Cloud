# Come Gmail decide la scheda: cosa sappiamo e cosa no

Leggi questo file quando devi spiegare un segnale, pesare un caso dubbio o rispondere a "perché finisce in Promozioni?".

## Cosa è documentato

- Gmail smista le email nelle schede (Principale, Promozioni, Social, Aggiornamenti, Forum) con un **classificatore di machine learning**, non con liste di parole. Google cita tre famiglie di segnali: **chi invia**, **cosa contiene** il messaggio e **come il singolo destinatario ha interagito** in passato con quel mittente.
- La classificazione è **per destinatario**. La stessa email può arrivare in Principale a un ospite che risponde sempre e in Promozioni a uno che non apre mai. Se un utente sposta un'email in Principale, Gmail tende a ricordarselo per quel mittente.
- Dal 2024 Google chiede a chi invia in massa (oltre 5.000 messaggi al giorno verso Gmail) **SPF, DKIM e DMARC** allineati, **disiscrizione con un clic** (intestazioni List-Unsubscribe e List-Unsubscribe-Post) e un tasso di segnalazioni spam **sotto lo 0,3%**. Questi requisiti decidono se l'email arriva o va nello spam, non la scheda. Restano comunque un prerequisito.
- Promozioni non è lo spam. Gmail supporta le **annotazioni Promozioni** (markup schema.org nell'HTML) per mostrare badge offerta, codice sconto, scadenza e immagine in anteprima. Per una DEM che vende davvero, presidiare bene Promozioni può valere più che forzare l'arrivo in Principale.

## Cosa è osservato (euristiche, non regole)

Queste correlazioni vengono dai test sul campo (seed test, strumenti come ByeByePromo e GlockApps). Usale come probabilità, non come certezze.

| Segnale | Spinge verso Promozioni | Spinge verso Principale |
|---|---|---|
| Tono | "Noi a voi", annuncio, linguaggio da volantino | Una persona che scrive a una persona |
| Lessico | sconto, %, offerta, prezzo in evidenza, gratis, codice | Racconto, informazione, domanda |
| Urgenza | scade, ultimi posti, solo oggi, countdown | Date come informazione ("la notte del 25 dura un'ora in più") |
| CTA | Bottoni colorati, "Prenota ora", più CTA ripetute | Un link nel testo, oppure "rispondi a questa mail" |
| Immagini | Hero grande, griglie di immagini, immagini cliccabili, poco testo | Nessuna immagine o una sola, molto testo |
| Link | Molti link, molti domini, redirect del tracciamento ESP | 1–3 link verso il proprio dominio |
| Layout | Multi-colonna, blocchi a tessere, footer con icone social | Una colonna, aspetto da email "scritta a mano" |
| Mittente | noreply@, nome del brand, invio da piattaforma condivisa | Nome di persona ("Giulia di Hotel X"), indirizzo a cui si può rispondere |
| Oggetto | Maiuscole, !, emoji, prezzo, % | Frase normale, curiosità, nome proprio |
| Interazione | Nessuna risposta, nessuno spostamento | Risposte, salvataggi, spostamenti in Principale |

Il segnale più forte, e l'unico che il copy non controlla, è il **comportamento storico del destinatario**. Per questo la revisione del testo riduce il rischio ma non lo azzera.

## Leve per hotel e ristoranti, dalla più forte alla più debole

1. **Far rispondere.** "Rispondi a questa mail e ti tengo il tavolo" genera risposte, il segnale di interazione migliore.
2. **Mittente-persona.** "Marco, direttore del Silva Splendid", con reply-to reale.
3. **Prezzo fuori dall'email.** Il prezzo resta sulla landing; nell'email si racconta il motivo per partire.
4. **Un solo link nel testo** al posto dei bottoni.
5. **Meno immagini:** al massimo una, non cliccabile o con un solo link.
6. **Niente blocchi "altre offerte"** in fondo.
7. **Footer minimo:** indirizzo e disiscrizione, senza fila di icone social.

## Cosa fare per verificare davvero

Nessuna revisione testuale può dire "arriva in Principale". Per saperlo serve un **seed test**:

- 2–3 caselle Gmail: almeno una nuova e una che ha già interagito con il mittente;
- invio dall'ESP reale, con il template reale;
- controllo della scheda in cui arriva.

Gli strumenti automatici (ByeByePromo, GlockApps, Litmus Inbox Preview) fanno la stessa cosa in scala.
