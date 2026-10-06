from common import memo, rng, RANGE_JS

P = dict(
    slug="valore",
    title="Quanto vale un hotel? Il brand nel calcolo del perito",
    og_title="Quanto vale davvero il tuo hotel? Fai il calcolo del perito.",
    desc="Il perito valuta posizione, metri quadri, stato dell'immobile ed EBITDA. Il tuo nome non c'è in nessuna riga. Fai il calcolo e scopri quanto vale la riga che manca: il brand del tuo hotel.",
    eyebrow="Sintomo 05 · I muri senza nome",
    h1="Il mio hotel vale per l'immobile. Il mio brand non vale niente.",
    pull='Quanto vale davvero il tuo hotel? <span class="hl or in">Fai il calcolo del perito.</span> Cinque minuti.',
    lead="Poi parliamo della riga che manca. È l'unica del calcolo che dipende interamente da te.",
    cta2="Fai il calcolo del perito ↓",
    memo=memo("Perizia · foglio 1", "Il tuo nome?",
              [("Riga 1 · La posizione", "✕ no", "bad"),
               ("Riga 2 · I metri quadri", "✕ no", "bad"),
               ("Riga 3 · Lo stato dell'immobile", "✕ no", "bad"),
               ("Riga 4 · EBITDA × multiplo di zona", "✕ no", "bad")],
              "Il tuo nome", "in nessuna riga",
              "Vent'anni di lavoro. Quattro righe. Nessuna parla di te."),
    ag_h2="Il calcolo che decide <em>vent'anni di lavoro.</em>",
    ag_lead="Carta e penna. Sono quattro righe, e le conosci già.",
    ag_prose='''        <p><strong>Riga 1, la posizione.</strong> Vale quello che vale la zona. Non l'hai decisa tu, non la muovi tu.</p>
        <p><strong>Riga 2, i metri quadri.</strong> Moltiplicati per il valore locale. Matematica, non merito.</p>
        <p><strong>Riga 3, lo stato dell'immobile.</strong> Le tue ristrutturazioni sono qui. Ammortizzate, cioè già scontate.</p>
        <p><strong>Riga 4, l'EBITDA.</strong> Per un multiplo: quello di zona, degli immobili, non delle aziende.</p>
        <p>Gli ospiti che tornano da dieci anni? Il modo in cui lavorate? In nessuna riga. Non perché il perito è cattivo. Il perito valuta quello che si trasferisce. E la tua identità oggi sta nella tua testa. La tua testa non è in vendita.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>La riga che manca</span><em>Foglio del perito</em></div>
        <div class="tool-body">
{rng("vlE", "EBITDA annuo", 100000, 5000000, 50000, 500000, pre="€", small="Valore d'esempio: metti il tuo.")}
{rng("vlM", "Punti di multiplo in più", 0.5, 5, 0.5, 1, pre="+")}
          <div class="tool-row">
            <span class="lab">Riga 5 · Il brand</span>
            <button type="button" class="btn sm" id="vlB" aria-pressed="false" style="justify-self:start">Aggiungi la riga 5 <span class="arr">+</span></button>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k" id="vlK">Riga 5 · Il brand</span>
          <b class="tool-big" id="vlOut">€0</b>
          <p id="vlSub">Senza un'identità documentata, non c'è niente da comprare. Il brand vale zero.</p>
        </div>
        <p class="tool-note">Non ti dico di quanto cambia il multiplo: dipende dalla zona, dal mercato e da chi compra, e chi te lo promette in una pagina web mente. Ti dico quanto vale ogni punto. Il conto è solo EBITDA × punti.</p>
      </div>''',
    js='''/* la riga che manca */
(function(){''' + RANGE_JS + '''
  var on=false, b=document.getElementById('vlB');
  function calc(){
    var e=v('vlE'), m=v('vlM');
    document.getElementById('vlOut').textContent=on?eur(e*m):'€0';
    document.getElementById('vlSub').innerHTML=on
      ? 'Ogni punto di multiplo, sul tuo EBITDA, vale <strong>'+eur(e)+'</strong>. Il brand è la riga che può spostarlo: da multiplo immobiliare a multiplo aziendale.'
      : 'Senza un’identità documentata, non c’è niente da comprare. Il brand vale zero.';
  }
  b.addEventListener('click',function(){
    on=!on; b.setAttribute('aria-pressed',on);
    b.innerHTML=on?'Togli la riga 5 <span class="arr">−</span>':'Aggiungi la riga 5 <span class="arr">+</span>';
    calc();
  });
  bind(['vlE','vlM'],calc);
})();''',
    sig_h2="I dieci segnali che il tuo hotel <em>vale solo per i muri.</em>",
    sig_lead="Spunta quelli in cui ti riconosci. Ognuno è un pezzo di valore che resta nella tua testa invece che nell'hotel.",
    signals=[
        ("La valutazione conta i muri. Non il brand.", "Se domani vendessi, il prezzo sarebbe posizione più metri quadri più EBITDA. Il brand: zero. Perché non c'è niente da comprare.", "Un hotel con identità si vende come un'azienda. Senza, come un immobile."),
        ("Senza di te, l'hotel perde la voce.", "L'identità sta nella tua testa. Non nei documenti, non nello staff, non nel sito. Se ti fermi un mese, l'hotel torna generico.", "Per un gestore è un problema. Per un proprietario è un rischio patrimoniale."),
        ("Il vantaggio estetico è in affitto.", "Hai investito nel restyling. Il vicino ristruttura adesso, con lo stesso architetto. E nel calcolo le tue ristrutturazioni sono già ammortizzate.", "L'estetica scade. L'identità resta."),
        ("Spendi dove si vede.", "Ristrutturazione, mobili, tecnologia. E tagli dove non si vede: strategia, formazione, marketing vero.", "Poi ti chiedi perché sei sempre lì."),
        ("Gli ospiti sono di Booking.", "Buona parte delle prenotazioni passa da lì. Quegli ospiti sono suoi, non tuoi.", "Chi compra non paga ospiti che appartengono a un altro."),
        ("Nessuno ti cerca per nome.", "Il diretto è fermo, nonostante sito nuovo e campagne. Ti trovano come «hotel + zona».", "Una domanda che non porta il tuo nome non si trasferisce."),
        ("Le recensioni non dicono perché.", "«Pulito. Gentile. Torneremo.» Manca quella che dice: «L'unico posto dove ho trovato X.»", "Nessuna prova scritta di cosa ti rende diverso."),
        ("Il personale cambia ogni stagione.", "Lavorano per «un hotel qualsiasi». Il servizio dipende da chi c'è quest'anno.", "L'identità non è solo per l'ospite. È anche per chi lavora con te."),
        ("Ogni scelta è un dibattito.", "Nuovo ristorante: che concept? Nuova SPA: che filosofia? Ogni volta si riparte da zero.", "Chi ha un'identità non dibatte. Deduce."),
        ("Sai l'occupazione. Non quanto guadagni per camera.", "Il pieno ti rassicura. Il margine per camera e per ospite non lo guardi.", "Il perito i numeri li guarda. Tutti."),
    ],
    sig_tail="Il bello senza posizione è un costo che si ammortizza. L’identità è un asset che si rivaluta.",
    br_h2="I muri sono il sintomo. <em>Manca il nome.</em>",
    br_lead="Il perito misura il terzo anello: quello che incassi. Il brand nasce sul primo.",
    br_here=3,
    br_rings=["Quello che sai di essere. Oggi solo nella tua testa.", "Quello che dici all'ospite.", "Quello che incassi. L'unico che il perito vede."],
    br_prose='''        <p>Un hotel con un'identità documentata, cioè scritta, applicata e dimostrabile nei numeri diretti, aggiunge una riga alla formula. Si chiama brand.</p>
        <p>E cambia il multiplo: da multiplo immobiliare a multiplo aziendale.</p>
        <p><strong>È l'unica riga del calcolo che dipende interamente da te.</strong> E puoi iniziare a costruirla questa settimana.</p>''',
    br_quote="L'identità è un asset che si rivaluta.",
    offer_lead="L'analisi è il primo documento della riga 5: il posizionamento del tuo hotel, scritto. Non più solo nella tua testa.",
    cand_lead="Sessanta secondi. Guardo il tuo hotel come lo guarderebbe chi lo vuole comprare: cosa c'è oltre i muri.",
    faq=[
        ("Il perito sbaglia a non contare il brand?", "No. Valuta quello che si trasferisce. Il lavoro è rendere il brand trasferibile: scritto, applicato dallo staff, visibile nelle prenotazioni dirette."),
        ("Cosa vuol dire «identità documentata»?", "Un posizionamento scritto su una pagina, applicato nei testi, negli script e nelle scelte, dimostrabile nei numeri diretti. Finché sta solo nella tua testa, non vale per nessun altro."),
        ("Per me l'hotel è un immobile a reddito. Fa per me?", "No. Se il brand non t'interessa, ti serve un agente, non un posizionamento. Te lo dico prima, così risparmiamo tempo entrambi."),
        ("Ho più strutture. Si può fare?", "Sì, ed è dove rende di più: ogni struttura distinta dalle altre e dal mercato. Si parte comunque dall'analisi di una."),
    ],
)
