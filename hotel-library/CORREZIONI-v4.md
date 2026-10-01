# Registro correzioni: dalla Library online (v2) alla v4

Aggiornato al 1 ottobre 2026.

## 1. La causa principale

Esistono due tassonomie con numerazioni diverse:

- **sito online (v2):** pattern numerati da #1 a #57 in sequenza globale;
- **estratto dati (v3):** codici lettera + numero (A1, C10, D15, L53…), dove il numero **non** coincide con quello del sito.

Gli esempi sono stati collegati ai pattern **per numero**. Il risultato: ogni esempio è finito sul pattern del sito con lo stesso numero, anche quando era un pattern diverso.

| Codice v3 | Esempio | Pattern v3 corretto | Dove è finito sul sito |
|---|---|---|---|
| A1 | citizenM | Mobile Citizens | #1 Anti-OTA |
| A3 | The Hoxton | Anti-Business Hotel | #3 Anti-finto-boutique |
| A6 | Selina | Workation Hub | #6 Solo X camere |
| C10 | Falkensteiner Family | Family-positioned | #10 Solo-travelers obsession |
| C11 | The Hoxton | Business-positioned | #11 Sport-expertise |
| C13 | Hostelle | Gender-specific | #13 Pet-welcomed |
| D15 | Equinox Hotel | Sleep Tourism | #15 Generazionale |
| D16 | Aman | Silence Provider | #16 Vendiamo lo chef |
| D20 | Inn at Little Washington | Dining-destination | #20 Vendiamo la trasformazione |
| G32 | Kimpton | Pet-friendly | #32 N-generazioni |
| L53 | Soho House, Casa Cipriani | Members-Only | #53 Pets Only |
| L54 | Hostelle | Solo-Travelers-Only | #54 Sport Only |
| L55 | D Pet Hotels | Pets-Only | #55 Members Only |
| L56 | La Manga Club | Sport-Only | #56 Solo-travelers Only |
| L57 | Reschio | Wedding-Only | #57 Wedding/Event Only |

Il secondo errore è dello stesso tipo. Alcuni esempi avevano un codice generico ("E", "K", "Nascente", "Boutique Hostel") e sono stati agganciati a **tutti** i pattern della famiglia:

- Monastero Santa Rosa, Borgo Egnazia, Generator, Aman Residences su tutti i pattern dal #22 al #26 (e Santa Rosa ed Egnazia anche su #29);
- Sextantio e "Sober Hospitality (nascente)" su tutti i pattern dal #47 al #50.

**Rimedio strutturale nella v4:**
1. I codici sono lettera + due cifre dentro la famiglia (A01, L05). Non esiste più un numero globale da confondere.
2. Ogni esempio cita i pattern solo con il codice completo. Non sono ammessi codici generici di sola famiglia.
3. Lo script `tools/validate.py` blocca codici inesistenti, duplicati e riferimenti rotti prima di ogni pubblicazione.

## 2. Errori nei dati (estratto v3)

| Esempio | Prima | Ora | Fonte |
|---|---|---|---|
| Selina | "Fallita 2024, Chapter 11" | In administration nel Regno Unito dal 22/07/2024; business venduto a Collective Hospitality il 27/08/2024 | [Hospitality Investor](https://www.hospitalityinvestor.com/hotels/selina-hospitality-falls-administration), [Skift](https://skift.com/2024/07/22/selina-collapses-in-liquidity-crisis-seeks-buyers/) |
| citizenM | Esempio di indipendente anti-catena | Acquisito da Marriott (chiusura luglio 2025, 37 hotel) | [Marriott](https://marriott.gcs-web.com/node/36046) |
| Saorsa 1875 | "Venduta 2025, rebrand Birchwood con prodotti animali" | Confermata solo la messa in vendita (~£950k) per altri progetti dei proprietari. Rebrand ed esito: da verificare | [The Caterer](https://www.thecaterer.com/news/vegan-hotel-in-perthshire-on-the-market-for-nearly-1m) |
| Beaches | Family-Only | Family-designed: accoglie anche coppie, single e amici | [Sandals UK](https://www.sandals.co.uk/blog/the-best-caribbean-breaks-grandparents/) |
| Reschio | Wedding-only | Hotel da 36 camere aperto nel 2021 | [Dezeen](https://www.dezeen.com/2021/07/05/hotel-castello-di-reschio-umbria-italy/amp/) |
| Eremito | "Ex monastero XIV" | Eremo contemporaneo ricostruito da un rudere, aperto nel 2013 | [Gambero Rosso](https://gamberorossointernational.com/?p=523204) |
| Equinox | "Equinox Hotels", catena | Un solo hotel (Hudson Yards, 2019, 212 camere) con programma sonno | [Hospitality Net](https://www.hospitalitynet.org/news/4119262.html) |
| Hostelle | Solo-Travelers-Only | Women-Only (fondato 2012, black-owned) | [Travel Noire](https://travelnoire.com/hostelle-black-owned-women-only-hostel-in-amsterdam) |
| Sober Hospitality | Esempio "Camp Recovery" (centro di riabilitazione) | Jill Hotel Bruxelles (verificato), The Stromness Orkney (da verificare) | [Travel Tomorrow](https://traveltomorrow.com/brussels-based-jill-hotel-becomes-belgiums-first-to-ban-alcoholic-drinks-from-its-menu/) |
| Kimpton | Founder-persona, N-generazioni | Brand IHG, solo Pet-Welcomed | — |
| Casa Wabi | Hotel, "prenotazione solo via email" | Fondazione con residenze d'artista, T3 come riferimento di categoria | — |
| Aurelio Lech | Stagione invertita | Rimosso: aprire d'inverno in una località sciistica non è un'inversione | — |
| Six Senses | "42% fatturato wellness, 5,2 notti" | Dati senza fonte: sospesi. Brand IHG dal 2019 | — |
| Bambu Indah | Carbon trasparente | Materiale-manifesto. Carbon trasparente è Bucuti & Tara | — |
| Sextantio | "HBS Case" senza riferimento | HBS, caso "Sextantio" (E. Cantillon, 2006) | ricerca catalogo |

## 3. Incoerenze di tassonomia risolte

- **Doppioni eliminati:** Anti-Lusso-Patinato (A2 = J43) resta solo in J01. Workation (A6 = D19) diventa C08 (pubblico) + D04 (connessione). Silenzio (D16 = D18) diventa D03. Chef (D20 = G30) diventa D01.
- **Pattern spostati:** Albergo Diffuso e Ambasciata Regionale passano da E a F (il luogo è l'identità). Luxury Glamping esce dai pattern e resta solo categoria (CAT03).
- **Pattern accorpati:** Anti-Catena + Anti-Finto-Boutique in A02. Hotel-Museo + Hotel-Collezione in E02.
- **Pattern nuovi:** B05 Accesso Difficile / Car-Free, F05 Cultura Locale come Prodotto, L06 Women Only.
- **Tier e caveat separati:** "T1-Caveat" non esiste più. Il tier misura quanto il caso rappresenta il pattern; `caveat` segnala se il business ha retto.
- **Conteggi allineati:** il sito diceva 57+16, l'estratto 54 (dichiarati 56) e 49 esempi (dichiarati 51). Ora i numeri li calcola lo script: 65 pattern, 16 categorie, 59 esempi.

## 4. Ancora da verificare prima di pubblicare

Esempi con `verifica: da_verificare` (11) e `proposto` (8): l'elenco completo è in `export/esempi.csv` (colonne `verifica` e `note`). In ordine di priorità:

1. Saorsa 1875: esito della vendita. Decide se resta un caso caveat.
2. Six Senses: trovare una fonte per i dati economici o eliminarli.
3. Soho House: in quali sedi le camere sono solo per soci (decide il tier su L05).
4. The Connaught: fonte per il "maggiordomo da 40 anni".
5. I nuovi casi italiani: Casa Maria Luigia, Casadonna-Reale, Atelier sul Mare, Vigilius, Lefay, Italy Family Hotels, Italy Bike Hotels, Palazzo Margherita.
