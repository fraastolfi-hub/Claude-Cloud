from common import memo, rng, RANGE_JS

P = dict(
    slug="booking",
    title="Ridurre le commissioni Booking e vendere diretto",
    og_title="Ogni anno regali €150.000 a Booking. Fai il conto con i tuoi numeri.",
    desc="Un hotel di 80 camere lascia a Booking circa €150.000 l'anno. Fai il conto con i tuoi numeri, riconosci i dieci segnali della dipendenza e scopri perché l'ospite non prenota diretto.",
    eyebrow="Sintomo 01 · Le commissioni",
    h1="Le commissioni a Booking mi costano un rene.",
    pull='Ogni anno regali <span class="hl or in">€150.000</span> a Booking. Ti mandano almeno il panettone a Natale?',
    lead="Booking ti porta prenotazioni. Non ospiti: quelli restano suoi. Il problema non è Booking. È che non sai spiegare perché uno dovrebbe prenotare direttamente da te.",
    cta2="Fai il conto con i tuoi numeri ↓",
    memo=memo("Facciamo due conti", "Esempio",
              [("Hotel di 80 camere", "× 80", ""),
               ("Prenotazioni che arrivano da Booking", "× 60%", ""),
               ("Commissione", "× 18%", "bad")],
              "Ogni anno, a Booking", "€150.000",
              "Natale. Il panettone. Tuo.", stamp="ZERO PANETTONI"),
    ag_h2="Ma Francesco, <em>senza Booking chiudo!</em>",
    ag_lead="No. Nessuno ti chiede di chiudere Booking. Ti chiedo di guardare quanto ti costa restarci dentro così.",
    ag_prose='''        <p>Booking ti porta prenotazioni. <strong>Non ospiti.</strong></p>
        <p>L'ospite è di Booking, non tuo. Tu riempi le camere con i suoi clienti. E lui difende il suo marchio con i tuoi soldi.</p>
        <p>Si chiama dipendenza. Non partnership.</p>
        <p>L'obiettivo non è uscire da Booking. È rimetterlo al suo posto: <strong>un canale, non il canale.</strong></p>
        <p>Succede quando l'ospite ti cerca per nome. E ti cerca per nome solo se sa perché dovrebbe scegliere te.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Il conto del panettone</span><em>Metti i tuoi numeri</em></div>
        <div class="tool-body">
{rng("bkR", "Camere", 5, 200, 1, 80)}
{rng("bkA", "Tariffa media a notte", 40, 500, 5, 95, pre="€")}
{rng("bkO", "Occupazione media annua", 20, 95, 1, 50, suf="%")}
{rng("bkQ", "Quota di prenotazioni da Booking", 0, 100, 1, 60, suf="%")}
{rng("bkC", "Commissione", 10, 25, 0.5, 18, suf="%")}
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Ogni anno, nelle tasche di Booking</span>
          <b class="tool-big" id="bkOut">€149.796</b>
          <p id="bkSub">In dieci anni fanno circa un milione e mezzo.</p>
        </div>
        <p class="tool-note">Tariffa e occupazione sono valori d'esempio: con 80 camere, €95 a notte e il 50% di occupazione esce il conto di partenza, circa €150.000. Metti i tuoi. Il calcolo resta nel tuo browser.</p>
      </div>''',
    js='''/* calcolatore commissioni */
(function(){''' + RANGE_JS + '''
  bind(['bkR','bkA','bkO','bkQ','bkC'],function(){
    var rev=v('bkR')*365*v('bkO')/100*v('bkA'), c=v('bkC')/100, out=rev*v('bkQ')/100*c, pt=rev*0.01*c;
    document.getElementById('bkOut').textContent=eur(out);
    document.getElementById('bkSub').innerHTML='In dieci anni: <strong>'+eur(out*10)+'</strong>. Ogni punto di quota che sposti da Booking al diretto vale <strong>'+eur(pt)+'</strong> l’anno.';
  });
})();''',
    sig_h2="I dieci segnali che lavori <em>per Booking.</em>",
    sig_lead="E non lui per te. Spunta quelli in cui ti riconosci.",
    signals=[
        ("Trenta secondi muti.", "L'ospite chiede: «Cosa vi rende speciali?». Tu rispondi: «Ehm. Cura. Qualità. Attenzione.» Lui ringrazia. E prenota su Booking. Un altro hotel.", "Se non sai dirlo in trenta secondi, non lo sai."),
        ("Lo staff non sa filtrare.", "Accettate tutti, purché paghino. Poi vi lamentate: «Gli ospiti non capiscono cosa offriamo.»", "Specifico è scegliere. E scegliere è escludere."),
        ("Booking è il tuo socio.", "Ti porta sessanta prenotazioni su cento e si tiene diciotto euro su cento. Per un hotel di ottanta camere fanno centocinquantamila euro l'anno. Tutti gli anni.", "Si chiama dipendenza. Non partnership."),
        ("Upgrade gratis a settembre.", "«Tanto la camera era vuota.» Intanto insegni una cosa all'ospite: aspetta lo sconto. E lui lo aspetta sempre. Anche a luglio.", "Hai allenato il mercato a non pagarti il prezzo pieno."),
        ("Mai alzato i prezzi.", "«La gente non paga.» Falso. La gente giusta paga. Quella sbagliata no.", "Tieni i prezzi bassi e avrai solo la gente sbagliata."),
        ("Il sito è anonimo.", "«Hotel 4 stelle. SPA. Ristorante. Relax.» Questo è un inventario, non un'identità. Cambi il logo e funziona per altri cento.", "Cento hotel uguali. Tu sei uno dei cento."),
        ("Bruci soldi su Google.", "Duemila euro di annunci. Cinquanta clic. Due prenotazioni. Clicca chiunque, prenota solo chi sa. E tu non gli hai detto cosa sei.", "Pubblicità senza identità è autocombustione."),
        ("Recensioni intercambiabili.", "«Pulito. Gentile. Buon rapporto qualità-prezzo.» Nessuno scrive: «L'unico posto dove ho trovato…».", "Le recensioni riflettono il posizionamento. Generico tu, generiche loro."),
        ("Lo yo-yo.", "Bassa stagione: panico, sconti. Alta stagione: pieno, smetti di pensarci. Poi di nuovo bassa. Di nuovo panico.", "Questo non è gestire. È sopravvivere. E Booking adora chi sopravvive."),
        ("Il senso di colpa al posto sbagliato.", "Alzi i prezzi e l'ospite «budget» se ne va. Tu ti senti in colpa. Dovresti festeggiare: hai liberato una camera per chi paga il giusto.", "Non hai perso un ospite. Hai filtrato."),
    ],
    sig_tail="Non ti serve più marketing. Ti serve sapere chi sei. Booking ti ha tenuto in vita finora: l’AI non ti farà lo stesso favore.",
    br_h2="Le commissioni sono il sintomo. <em>Non la malattia.</em>",
    br_lead="Tra il tuo hotel e l'incasso ci sono tre anelli. Booking lavora sull'ultimo. E tu, da anni, anche.",
    br_here=3,
    br_rings=["Quello che sai di essere.", "Quello che dici all'ospite.", "Quello che incassi. E che dividi con Booking."],
    br_prose='''        <p>Booking engine nuovo, campagne per il diretto, la tariffa più bassa sul sito. Tutto terzo anello. Utile, ma arriva dopo.</p>
        <p>L'ospite prenota diretto quando ha un motivo per cercarti per nome. Il motivo sta nel primo anello. <strong>Si chiama posizionamento.</strong></p>
        <p>E adesso conta il doppio: Booking ti metteva in una lista di cento. L'AI ne consiglia uno o due.</p>''',
    br_quote="Booking ti metteva in una lista. L'AI ti lascia fuori.",
    proof_extra='''    <p class="note-box rv" style="margin-top:26px"><strong>Sul diretto, il caso è un altro.</strong> Veridia Resort, <em>the nature resort of Chia</em>, vende diretto oltre il 60%. Lì non ho un prima e dopo di fatturato da mostrarti. Quindi non te lo mostro.</p>''',
    offer_lead="Prima di toccare il sito o le campagne, scopri cosa dire all'ospite perché prenoti da te.",
    cand_lead="Sessanta secondi. Mi servono il nome dell'hotel e il sito: il resto lo guardo io, Booking compreso.",
    faq=[
        ("Devo uscire da Booking?", "No. Booking resta un canale. Smette di essere il canale. Quando l'ospite ti cerca per nome, la prenotazione diretta arriva da sola: il lavoro è dargli un motivo per cercarti."),
        ("Serve rifare il sito?", "No. Cambi headline, bio e testi chiave. Il sito nuovo viene dopo, solo se serve. Prima il posizionamento. Sempre."),
        ("Funziona anche per un hotel piccolo?", "Funziona meglio. Un hotel piccolo può permettersi una nicchia stretta. Uno grande vive di compromessi. E con l'AI lo specifico batte il generico."),
        ("E l'AI cosa c'entra con le commissioni?", "Booking ti metteva in una lista di cento. L'AI ne consiglia uno o due, e sceglie chi è riconoscibile, specifico, diverso dagli altri. L'AI è uno specchio: se sei vuoto, riflette vuoto."),
    ],
)
