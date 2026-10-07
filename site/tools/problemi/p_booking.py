from common import memo, rng, RANGE_JS

P = dict(
    slug="booking",
    title="Ridurre le commissioni OTA e vendere diretto",
    og_title="Commissioni OTA: il calcolo con i numeri del tuo hotel.",
    desc="Un hotel di 80 camere lascia a Booking circa €150.000 l'anno di commissioni. Fai il calcolo con i tuoi numeri e scopri perché l'ospite non prenota diretto.",
    eyebrow="Segnale 01 · Canali di vendita",
    h1="Ridurre la dipendenza dalle OTA.",
    pull='Le commissioni OTA pesano sempre di più sul margine. Per un hotel di 80 camere valgono circa <span class="hl or in">€150.000</span> l\'anno.',
    lead="Booking porta prenotazioni, ma l'ospite resta suo. La causa raramente è il canale: l'ospite non trova un motivo per prenotare da te.",
    cta2="Fai il calcolo con i tuoi numeri ↓",
    memo=memo("Un calcolo d'esempio", "Esempio",
              [("Hotel di 80 camere", "× 80", ""),
               ("Prenotazioni che arrivano da Booking", "× 60%", ""),
               ("Commissione", "× 18%", "bad")],
              "Commissioni annue", "€150.000",
              "Con tariffa media di €95 e occupazione al 50%. In dieci anni, circa €1,5 milioni."),
    ag_h2="Booking resta un canale. <em>Non deve essere il canale.</em>",
    ag_lead="L'obiettivo non è uscire da Booking. È sapere quanto ti costa, e ridurre la quota dove si può.",
    ag_prose='''        <p>Booking porta prenotazioni. <strong>Non porta ospiti tuoi.</strong></p>
        <p>Email, relazione e prossima prenotazione restano al portale. Tu riempi le camere, Booking costruisce il suo marchio.</p>
        <p>Oltre metà delle prenotazioni non è più un canale. È una dipendenza.</p>
        <p>Si riduce quando l'ospite cerca il tuo hotel per nome. E lo cerca quando sa perché sceglierlo.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Il costo delle commissioni</span><em>Con i tuoi numeri</em></div>
        <div class="tool-body">
{rng("bkR", "Camere", 5, 200, 1, 80)}
{rng("bkA", "Tariffa media a notte", 40, 500, 5, 95, pre="€")}
{rng("bkO", "Occupazione media annua", 20, 95, 1, 50, suf="%")}
{rng("bkQ", "Quota di prenotazioni da Booking", 0, 100, 1, 60, suf="%")}
{rng("bkC", "Commissione", 10, 25, 0.5, 18, suf="%")}
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Commissioni annue a Booking</span>
          <b class="tool-big" id="bkOut">€149.796</b>
          <p id="bkSub">In dieci anni, circa un milione e mezzo.</p>
        </div>
        <p class="tool-note">Valori d'esempio: 80 camere, €95 a notte, 50% di occupazione. Metti i tuoi: il calcolo resta nel tuo browser.</p>
      </div>''',
    js='''/* calcolatore commissioni */
(function(){''' + RANGE_JS + '''
  bind(['bkR','bkA','bkO','bkQ','bkC'],function(){
    var rev=v('bkR')*365*v('bkO')/100*v('bkA'), c=v('bkC')/100, out=rev*v('bkQ')/100*c, pt=rev*0.01*c;
    document.getElementById('bkOut').textContent=eur(out);
    document.getElementById('bkSub').innerHTML='In dieci anni: <strong>'+eur(out*10)+'</strong>. Ogni punto di quota che sposti da Booking al diretto vale <strong>'+eur(pt)+'</strong> l’anno.';
  });
})();''',
    sig_h2="Dieci segnali di <em>dipendenza dalle OTA.</em>",
    sig_lead="Seleziona quelli che riconosci nel tuo hotel.",
    signals=[
        ("La risposta a «perché tu?».", "Un ospite ti chiede cosa ti distingue. Rispondi «cura, qualità, attenzione». Ringrazia e prenota un altro hotel su Booking.", "Se la risposta non sta in trenta secondi, non è ancora chiara."),
        ("Nessun filtro sulle richieste.", "Accetti tutte le prenotazioni. Poi ti accorgi che gli ospiti non capiscono cosa offri.", "Essere specifici significa scegliere. E scegliere significa escludere."),
        ("Booking è il primo canale.", "Porta 60 prenotazioni su 100 e ne trattiene il 18%. Con 80 camere sono circa €150.000 l'anno.", "Oltre una certa quota non è più un canale: è una dipendenza."),
        ("Upgrade gratuiti in bassa stagione.", "La camera era libera, l'upgrade non costa nulla. Ma l'ospite impara ad aspettare l'occasione, anche a luglio.", "Lo sconto ripetuto insegna a non pagare il prezzo pieno."),
        ("Tariffe ferme da anni.", "Temi di perdere prenotazioni. Con un aumento perdi soprattutto gli ospiti meno adatti al tuo hotel.", "Tariffe basse attirano chi sceglie per prezzo."),
        ("Un sito che elenca servizi.", "«Hotel 4 stelle. SPA. Ristorante. Relax.» Con un altro logo varrebbe per cento hotel.", "Tra cento hotel simili, l'ospite sceglie il più economico."),
        ("Campagne a basso rendimento.", "€2.000 di annunci, 50 clic, 2 prenotazioni. Clicca chiunque; prenota chi ha capito cosa offri.", "La pubblicità amplifica il messaggio. Anche quando è generico."),
        ("Recensioni intercambiabili.", "«Pulito. Gentile. Buon rapporto qualità-prezzo.» Manca quella che dice: «L'unico posto dove ho trovato…».", "Le recensioni riflettono il posizionamento. Se è generico, lo sono anche loro."),
        ("L'altalena stagionale.", "In bassa stagione sconti e promozioni, in alta il pieno. Poi il ciclo riparte.", "Reagisci alla stagione invece di costruire una domanda tua. È il terreno dove le OTA vincono."),
        ("Gli ospiti persi con l'aumento.", "Alzi la tariffa e chi guarda solo il prezzo sceglie altro. Lo vivi come una perdita.", "Spesso è un filtro: la camera resta per chi ne riconosce il valore."),
    ],
    sig_tail="La causa è una: manca un posizionamento chiaro. Con gli assistenti AI conta ancora di più: Booking mostra una lista, un assistente sceglie due o tre hotel.",
    br_h2="Le commissioni sono un segnale. <em>La causa è più a monte.</em>",
    br_lead="Tra il tuo hotel e il fatturato ci sono tre passaggi. Booking lavora sull'ultimo. Quasi tutti gli interventi sul diretto, pure.",
    br_here=3,
    br_rings=["Chi sei, e per quale ospite.", "Cosa dici all'ospite, e dove.", "Cosa incassi, e quanto resta a Booking."],
    br_prose='''        <p>Booking engine nuovo, campagne sul diretto, tariffa migliore sul sito: tutto terzo passaggio. Utile, ma viene dopo.</p>
        <p>L'ospite prenota diretto quando ha un motivo per cercarti per nome. Quel motivo si decide nel primo passaggio. <strong>Si chiama posizionamento.</strong></p>''',
    br_quote="Booking ti mette in una lista. Un assistente AI sceglie.",
    proof_extra='''    <p class="note-box rv" style="margin-top:26px"><strong>Sulle vendite dirette il caso è un altro.</strong> Veridia Resort, <em>the nature resort of Chia</em>, vende diretto oltre il 60%. Non ho un confronto di fatturato prima e dopo, quindi non lo presento.</p>''',
    offer_lead="Prima di toccare sito e campagne, devi sapere cosa dire all'ospite perché prenoti da te.",
    cand_lead="Un minuto. Bastano il nome del tuo hotel e il sito: il resto lo guardo io, OTA comprese.",
    faq=[
        ("Devo uscire da Booking?", "No. Booking resta un canale, ma smette di essere il principale. Quando l'ospite cerca il tuo hotel per nome, il diretto cresce. Il lavoro è dargli un motivo per farlo."),
        ("Devo rifare il sito?", "No. Si cambiano titolo, presentazione e testi chiave. Un sito nuovo viene dopo, e solo se serve."),
        ("Funziona anche per un hotel più piccolo?", "Sì, spesso meglio. Un hotel di 40 camere può scegliere una nicchia precisa; uno di 200 deve tenere insieme più segmenti."),
        ("Cosa c'entrano gli assistenti AI con le commissioni?", "Booking mostra cento hotel. Un assistente AI ne consiglia due o tre: quelli riconoscibili, specifici e coerenti su ogni canale. Racconta bene solo ciò che è già chiaro."),
    ],
)
