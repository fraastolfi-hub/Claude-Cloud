from common import memo, rng, RANGE_JS

P = dict(
    slug="booking",
    title="Ridurre le commissioni OTA e vendere diretto",
    og_title="Commissioni OTA: il calcolo con i numeri della vostra struttura.",
    desc="Una struttura di 80 camere lascia a Booking circa €150.000 l'anno di commissioni. Il calcolo con i vostri numeri, dieci segnali di dipendenza dalle OTA e la causa per cui l'ospite non prenota diretto.",
    eyebrow="Segnale 01 · Canali di vendita",
    h1="Ridurre la dipendenza dalle OTA.",
    pull='Le commissioni OTA pesano sempre di più sul margine. Per una struttura di 80 camere valgono circa <span class="hl or in">€150.000</span> l\'anno.',
    lead="Booking porta prenotazioni, ma il rapporto con l'ospite resta al portale. La causa raramente è il canale: è che l'ospite non trova un motivo per prenotare direttamente da voi.",
    cta2="Il calcolo con i vostri numeri ↓",
    memo=memo("Un calcolo d'esempio", "Esempio",
              [("Struttura di 80 camere", "× 80", ""),
               ("Prenotazioni che arrivano da Booking", "× 60%", ""),
               ("Commissione", "× 18%", "bad")],
              "Commissioni annue", "€150.000",
              "Con tariffa media di €95 e occupazione al 50%. In dieci anni, circa €1,5 milioni."),
    ag_h2="Booking resta un canale. <em>Non deve essere il canale.</em>",
    ag_lead="Uscire da Booking non è l'obiettivo. L'obiettivo è sapere quanto costa la quota attuale, e ridurla dove è possibile.",
    ag_prose='''        <p>Booking porta prenotazioni. <strong>Non porta ospiti vostri.</strong></p>
        <p>Dati, relazione e prenotazione successiva restano al portale. La struttura riempie le camere, il portale costruisce il proprio marchio.</p>
        <p>Quando la quota supera la metà delle prenotazioni, non è più un canale tra gli altri. È una dipendenza.</p>
        <p>L'obiettivo è riportarlo al suo ruolo: <strong>un canale, non il canale.</strong></p>
        <p>Succede quando l'ospite cerca la struttura per nome. E la cerca per nome quando sa perché sceglierla.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Il costo delle commissioni</span><em>Con i vostri numeri</em></div>
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
        <p class="tool-note">Tariffa e occupazione sono valori d'esempio: con 80 camere, €95 a notte e il 50% di occupazione il risultato è circa €150.000. Inserite i vostri dati: il calcolo avviene solo nel vostro browser.</p>
      </div>''',
    js='''/* calcolatore commissioni */
(function(){''' + RANGE_JS + '''
  bind(['bkR','bkA','bkO','bkQ','bkC'],function(){
    var rev=v('bkR')*365*v('bkO')/100*v('bkA'), c=v('bkC')/100, out=rev*v('bkQ')/100*c, pt=rev*0.01*c;
    document.getElementById('bkOut').textContent=eur(out);
    document.getElementById('bkSub').innerHTML='In dieci anni: <strong>'+eur(out*10)+'</strong>. Ogni punto di quota spostato da Booking al canale diretto vale <strong>'+eur(pt)+'</strong> l’anno.';
  });
})();''',
    sig_h2="Dieci segnali di <em>dipendenza dalle OTA.</em>",
    sig_lead="Selezionate quelli che riconoscete nella vostra struttura.",
    signals=[
        ("La risposta a «perché voi?».", "Un ospite chiede: «Cosa vi distingue?». La risposta è «cura, qualità, attenzione». L'ospite ringrazia e prenota un'altra struttura su Booking.", "Se la risposta non sta in trenta secondi, non è ancora chiara."),
        ("Nessun filtro sulle richieste.", "Si accettano tutte le prenotazioni. Poi si nota che gli ospiti non colgono cosa offre la struttura.", "Essere specifici significa scegliere. E scegliere significa escludere."),
        ("Booking è il primo canale.", "Porta sessanta prenotazioni su cento e trattiene diciotto euro su cento. Per una struttura di ottanta camere sono circa centocinquantamila euro l'anno.", "Oltre una certa quota non è più un canale: è una dipendenza."),
        ("Upgrade gratuiti in bassa stagione.", "La camera era libera, l'upgrade non costa nulla. Ma l'ospite impara ad aspettare l'occasione, anche a luglio.", "Lo sconto ripetuto insegna al mercato a non pagare il prezzo pieno."),
        ("Tariffe ferme da anni.", "Il timore è perdere prenotazioni. In realtà, con un aumento, si perdono soprattutto gli ospiti meno adatti alla struttura.", "Tariffe basse attirano soprattutto chi sceglie per prezzo."),
        ("Un sito che elenca servizi.", "«Hotel 4 stelle. SPA. Ristorante. Relax.» È un inventario, non un'identità: con un altro logo varrebbe per cento strutture.", "Tra cento strutture simili, l'ospite sceglie la più economica."),
        ("Campagne a basso rendimento.", "Duemila euro di annunci, cinquanta clic, due prenotazioni. Clicca chiunque; prenota chi ha capito cosa offrite.", "La pubblicità amplifica un messaggio. Se il messaggio è generico, amplifica quello."),
        ("Recensioni intercambiabili.", "«Pulito. Gentile. Buon rapporto qualità-prezzo.» Manca la recensione che dice: «L'unico posto dove ho trovato…».", "Le recensioni riflettono il posizionamento. Se è generico, lo sono anche loro."),
        ("L'altalena stagionale.", "In bassa stagione sconti e promozioni. In alta stagione il pieno, e il tema passa in secondo piano. Poi il ciclo riparte.", "Si reagisce alla stagione invece di costruire una domanda propria. È il terreno su cui le OTA lavorano meglio."),
        ("Gli ospiti persi con l'aumento.", "Con un aumento di tariffa, una parte degli ospiti più attenti al prezzo sceglie altro. Viene vissuto come una perdita.", "Spesso è una selezione: la camera resta disponibile per chi ne riconosce il valore."),
    ],
    sig_tail="Segnali così diffusi indicano una causa comune: manca un posizionamento chiaro. Con gli assistenti AI conta ancora di più: Booking mostra una lista, un assistente ne sceglie due o tre.",
    br_h2="Le commissioni sono un segnale. <em>La causa è più a monte.</em>",
    br_lead="Tra la struttura e il fatturato ci sono tre passaggi. Booking lavora sull'ultimo, come la maggior parte degli interventi sul canale diretto.",
    br_here=3,
    br_rings=["Chi siete, e per quale ospite.", "Cosa dite all'ospite, e dove.", "Cosa incassate, e quanto resta a Booking."],
    br_prose='''        <p>Un nuovo booking engine, campagne per il diretto, la tariffa migliore sul sito: tutto terzo passaggio. Utile, ma viene dopo.</p>
        <p>L'ospite prenota diretto quando ha un motivo per cercarvi per nome. Il motivo si definisce nel primo passaggio. <strong>Si chiama posizionamento.</strong></p>
        <p>Con gli assistenti AI conta ancora di più: Booking mostra cento strutture, un assistente ne consiglia due o tre.</p>''',
    br_quote="Booking mette la struttura in una lista. Un assistente AI sceglie.",
    proof_extra='''    <p class="note-box rv" style="margin-top:26px"><strong>Sulle vendite dirette, il caso di riferimento è un altro.</strong> Veridia Resort, <em>the nature resort of Chia</em>, vende diretto oltre il 60%. Per Veridia non ho un confronto di fatturato prima e dopo, quindi non lo presento.</p>''',
    offer_lead="Prima di intervenire su sito e campagne, serve sapere cosa dire all'ospite perché prenoti da voi.",
    cand_lead="Un minuto. Bastano il nome della struttura e il sito: il resto lo analizzo io, compresa la presenza sulle OTA.",
    faq=[
        ("Dobbiamo uscire da Booking?", "No. Booking resta un canale, ma smette di essere quello principale. Quando l'ospite cerca la struttura per nome, la prenotazione diretta cresce: il lavoro consiste nel dargli un motivo per farlo."),
        ("Serve rifare il sito?", "No. Si interviene su titolo, presentazione e testi chiave. Un sito nuovo viene dopo, e solo se serve. Prima il posizionamento."),
        ("Funziona anche per una struttura più piccola?", "Sì, spesso meglio. Una struttura piccola può scegliere una nicchia precisa, una grande deve conciliare più segmenti. E un assistente AI consiglia più facilmente una proposta specifica di una generica."),
        ("Che cosa c'entrano gli assistenti AI con le commissioni?", "Booking mostra una lista di cento strutture. Un assistente AI ne consiglia due o tre, e sceglie quelle riconoscibili, specifiche e coerenti in ogni canale. Un assistente racconta bene solo ciò che è già chiaro."),
    ],
)
