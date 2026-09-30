# Estrazioni del 30/09/2026 prodotte da estrai.js (girato su Apify con la pageFunction generata da apify-pagefunction.mjs).
# Copiate qui perché da questo ambiente i siti degli hotel non sono raggiungibili direttamente.
# Per il mobile si riportano i campi che cambiano il voto (frase visibile, pulsanti, modulo date, prove).
import json, pathlib
def s(headline="", sottotitolo="", supporto=(), frase=True, grande=True, cta=0, cta_testo="", date=False, h1_fuori=(), seconda=(), prove=(), testo=None):
    return {"headline": headline, "sottotitolo": sottotitolo, "supporto": list(supporto), "frase_visibile": frase,
            "headline_piu_grande": grande, "cta_primari": cta, "cta_testo": cta_testo, "modulo_date": date,
            "testo_schermata": testo if testo is not None else " \n ".join([headline, sottotitolo, *supporto]),
            "h1_fuori": list(h1_fuori), "seconda_schermata": list(seconda), "prove": [dict(tipo=t, testo=x, schermate=n) for t, x, n in prove]}
casi = {}
casi["olympic"] = {"url": "https://www.olympicspahotel.it/", "title": "Olympic SPA Hotel 4*S Val di Fassa | Adults-Only Wellness",
  "meta": "Olympic 4*S in Val di Fassa: rifugio adults-only 14+. Scopri la Te Jaga SPA, l'iconica Sauna nel Bosco e l'autentica cucina Ladina in Trentino.",
  "desktop": s("Cuore Ladino e Tradizioni", "", ["SPA e Benessere"], testo="Camere \n Cuore Ladino e Tradizioni \n SPA e Benessere \n Esperienze",
    h1_fuori=["Olympic SPA Hotel - Hotel Adults Only nel cuore del Trentino"],
    seconda=["L'Olympic propone durante l'anno tante offerte speciali e promozioni per la tua vacanza in Trentino. Scegli quella più adatta a te!",
             "Ritmi lenti e colori autunnali Boschi dorati A PARTIRE DA € 1954 A PERSONA SCOPRI L'OFFERTA Dal 1° settembre all'8 novembre 2026",
             "Colazione in baita o Forest experience mindfulness Soggiorno a inizio settimana A PARTIRE DA € 927 A CAMERA",
             "Ladin soul Sentirsi parte della montagna. Esperienze e profumi sulle Dolomiti."],
    prove=[("riconoscimento", "TripAdvisor", 3.68)])}
casi["olympic"]["mobile"] = {**casi["olympic"]["desktop"], "prove": [dict(tipo="riconoscimento", testo="TripAdvisor", schermate=4.28)]}
casi["veridia"] = {"url": "https://www.veridiaresort.com/it", "title": "Il Nature Resort di Chia, Sud Sardegna - Veridia Resort",
  "meta": "Un rifugio naturale sulla costa incontaminata di Chia, Sardegna. Cinque ettari di giardini mediterranei, spiaggia privata a Su Portu e silenzio autentico. Aperto maggio–ottobre.",
  "desktop": s("Il Nature Resort della Riserva di Chia", "Un rifugio sul mare tra silenzio,natura e bellezza", cta=2, cta_testo="RICHIESTA",
    seconda=["Nascosto lungo la costa incontaminata di Chia, Veridia Resort è un luogo dove la natura e la tranquillità si prendono la scena.",
             "Immerso in cinque ettari di giardini mediterranei, Veridia non punta all’eccesso né al lusso: celebra il silenzio, lo spazio e la semplicità.",
             "QUI, TRA L’ARIA PROFUMATA DI MIRTO E IL SUONO LIEVE DEL VENTO E DEL MARE, OGNI OSPITE PUÒ ALLONTANARSI DALLA FRENESIA QUOTIDIANA E RISCOPRIRE IL VALORE DEL TEMPO CHE SCORRE LENTO."])}
casi["veridia"]["mobile"] = casi["veridia"]["desktop"]
casi["club-family"] = {"url": "https://www.clubfamilyhotelriccione.com/", "title": "Club Family Hotel Riccione per famiglie sul mare con piscina - Club Family Hotel Riccione",
  "meta": "Vacanze All Inclusive a Riccione in hotel 3 stelle sul mare con piscina riscaldata, animazione e servizi per famiglie.",
  "desktop": s(frase=False, grande=False, h1_fuori=["Club Family Hotel Riccione 3 Stelle sul mare"],
    seconda=["Scopri il nostro hotel All Inclusive a Riccione, direttamente sulla spiaggia",
             "Siamo un hotel 3 stelle sul mare di Riccione, premiato dalla community di TripAdvisor come miglior hotel per famiglie in Italia: qui ti aspettano il sorriso dello staff, la comodità di avere la spiaggia proprio davanti e tutti i servizi pensati per chi viaggia con i più piccoli.",
             "Grazie alla formula esclusiva Club Family All Inclusive® Open Bar H24 & Spiaggia, puoi goderti il mare senza pensieri: nel tuo soggiorno sono inclusi 2 lettini e 1 ombrellone per tutta la vacanza, oltre a bevande illimitate e tanti servizi dedicati a tutta la famiglia.",
             "Animazione, le Tate per i piccoli, le feste a tema, i gonfiabili di Gommoland Park, l'arena di gioco all'aperto e i giochi interattivi nell'area multimediale, gli acquascivoli in piscina"],
    prove=[("riconoscimento", "banner tripadvisor header-banner-it.png", 0.8),
           ("riconoscimento", "Siamo un hotel 3 stelle sul mare di Riccione, premiato dalla community di TripAdvisor come miglior hotel per famiglie in Italia", 1.59)])}
casi["club-family"]["mobile"] = {**casi["club-family"]["desktop"], "cta_primari": 1, "cta_testo": "Chiedi il tuo preventivo MIGLIOR TARIFFA GARANTITA",
  "prove": [dict(tipo="riconoscimento", testo="banner tripadvisor header-banner-it.png", schermate=0.85)]}
casi["hoxton"] = {"url": "https://thehoxton.com/london/shoreditch/", "title": "Book Our Boutique Hotel in Shoreditch, East London | The Hoxton",
  "meta": "Stay at The Hoxton Hotel, Shoreditch in the heart of East London and experience comfortable rooms, all-day dining with a rooftop! Book now.",
  "desktop": s("Hello, Shoreditch!", cta=1, date=True,
    seconda=["Stay 2 nights and get £50/$50/€50 credit, 3 nights gets you £100/$100/€100, and 4 nights gets you £150/$150/€150!"])}
casi["hoxton"]["mobile"] = casi["hoxton"]["desktop"]
casi["moko"] = {"url": "https://www.hotelmoko.it/", "title": "Hotel 3 Stelle Superior a Milano Marittima | Moko Boutique Hotel", "meta": "",
  "desktop": s("Your stay. Your story. Your mark.", cta=1, cta_testo="Prenota", h1_fuori=["L’Hotel 3 stelle superior che non ti aspetti, a Milano Marittima"],
    seconda=["MOKO Milano Marittima", "Un lifestyle hotel a Milano Marittima, a due minuti a piedi dal mare e dal Papeete Beach. Abbiamo un tattoo studio, colazione fino a mezzogiorno", "tattoo studio", "colazione"])}
casi["moko"]["mobile"] = casi["moko"]["desktop"]
casi["veridia-landing"] = {"url": "https://stay.veridiaresort.com/", "title": "Veridia Resort — Where Nature Becomes Your Luxury",
  "meta": "Veridia Resort in Chia, Sardinia. The only elegant retreat set within a protected Mediterranean nature reserve. Silence, wild nature, and the cleanest sea in Italy.",
  "desktop": s("Silence, Wild Nature, and the Cleanest Sea in Italy.",
    "The only elegant retreat set within a protected Mediterranean nature reserve — where true luxury means being completely surrounded by wild nature.",
    ["CHIA, SARDINIA · PROTECTED NATURE RESERVE"], cta=1, cta_testo="PLAN MY ESCAPE →",
    prove=[("voto", "B. Booking.com Superb 8.5 /10", 1.15), ("voto", "tripadvisor ★★★★½ 4.5 /5", 1.15), ("riconoscimento", "Legambiente Guida Blu 5 Vele award", 4.84)])}
casi["veridia-landing"]["mobile"] = {**casi["veridia-landing"]["desktop"], "prove": [dict(tipo="voto", testo="B. Booking.com Superb 8.5 /10", schermate=1.15)]}
cartella = pathlib.Path(__file__).parent / "estrazioni"
for nome, c in casi.items():
    (cartella / f"{nome}.json").write_text(json.dumps(c, ensure_ascii=False, indent=1))
print(sorted(casi))
