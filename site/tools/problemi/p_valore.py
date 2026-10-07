from common import memo, rng, RANGE_JS

P = dict(
    slug="valore",
    title="Quanto vale un hotel? Il brand nella valutazione",
    og_title="Il valore del tuo hotel oltre l'immobile: la riga che manca nella perizia.",
    desc="Il perito valuta posizione, metri quadri, stato dell'immobile ed EBITDA. Il nome del tuo hotel non compare. Calcola quanto vale la riga che manca: il brand.",
    eyebrow="Segnale 05 · Valore del brand",
    h1="Un brand che valga oltre l'immobile.",
    pull='Il valore del tuo hotel coincide con quello dell\'immobile. <span class="hl or in">Il calcolo del perito lo mostra in quattro righe.</span>',
    lead="Poi c'è una quinta riga, che oggi manca. È l'unica che dipende solo dalle tue scelte.",
    cta2="Fai il calcolo del perito ↓",
    memo=memo("Perizia · foglio 1", "Il nome?",
              [("Riga 1 · La posizione", "✕ no", "bad"),
               ("Riga 2 · I metri quadri", "✕ no", "bad"),
               ("Riga 3 · Lo stato dell'immobile", "✕ no", "bad"),
               ("Riga 4 · EBITDA × multiplo di zona", "✕ no", "bad")],
              "Il nome del tuo hotel", "in nessuna riga",
              "Vent'anni di lavoro, quattro righe. Nessuna riguarda l'identità."),
    ag_h2="Il calcolo che riassume <em>vent'anni di lavoro.</em>",
    ag_lead="Sono quattro righe, e probabilmente le conosci già.",
    ag_prose='''        <p><strong>Riga 1, la posizione.</strong> Vale quanto la zona. Non dipende da te.</p>
        <p><strong>Riga 2, i metri quadri.</strong> Per il valore locale. È un calcolo, non un merito.</p>
        <p><strong>Riga 3, lo stato dell'immobile.</strong> Qui entrano le ristrutturazioni, già ammortizzate.</p>
        <p><strong>Riga 4, l'EBITDA.</strong> Per un multiplo di zona: quello degli immobili, non delle aziende.</p>
        <p>Gli ospiti che tornano da dieci anni, il modo di lavorare della tua squadra: non sono in nessuna riga. Il perito valuta ciò che si può trasferire. Un'identità che sta solo nella tua testa non si trasferisce.</p>''',
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
          <p id="vlSub">Senza un'identità scritta non c'è nulla da comprare: il brand vale zero.</p>
        </div>
        <p class="tool-note">Di quanto cambi il multiplo dipende da zona, mercato e acquirente: nessuna pagina web può prometterlo. Qui vedi quanto vale ogni punto: EBITDA × punti.</p>
      </div>''',
    js='''/* la riga che manca */
(function(){''' + RANGE_JS + '''
  var on=false, b=document.getElementById('vlB');
  function calc(){
    var e=v('vlE'), m=v('vlM');
    document.getElementById('vlOut').textContent=on?eur(e*m):'€0';
    document.getElementById('vlSub').innerHTML=on
      ? 'Ogni punto di multiplo, sul tuo EBITDA, vale <strong>'+eur(e)+'</strong>. Il brand è la riga che può spostarlo: da multiplo immobiliare a multiplo aziendale.'
      : 'Senza un’identità scritta non c’è nulla da comprare: il brand vale zero.';
  }
  b.addEventListener('click',function(){
    on=!on; b.setAttribute('aria-pressed',on);
    b.innerHTML=on?'Togli la riga 5 <span class="arr">−</span>':'Aggiungi la riga 5 <span class="arr">+</span>';
    calc();
  });
  bind(['vlE','vlM'],calc);
})();''',
    sig_h2="Dieci segnali di un valore <em>legato solo all'immobile.</em>",
    sig_lead="Seleziona quelli che riconosci nel tuo hotel. Ognuno è valore che resta nelle persone invece che nell'hotel.",
    signals=[
        ("La valutazione considera l'immobile, non il brand.", "Se vendi, il prezzo è posizione più metri quadri più EBITDA. Il brand vale zero: non c'è nulla da trasferire.", "Un hotel con un'identità si valuta come un'azienda. Senza, come un immobile."),
        ("L'identità dipende da una persona.", "Sta nella tua testa: non nei documenti, non nella squadra, non nel sito. Se manchi un mese, la comunicazione torna generica.", "Per la gestione è un limite. Per la proprietà è un rischio patrimoniale."),
        ("Il vantaggio estetico è temporaneo.", "Il tuo restyling è recente, ma l'hotel vicino ristruttura ora, con lo stesso studio. E nel calcolo le ristrutturazioni sono già ammortizzate.", "L'estetica scade. L'identità resta."),
        ("Gli investimenti vanno dove si vedono.", "Ristrutturazione, arredi, tecnologia. Meno spesso strategia, formazione e marketing.", "Sono proprio le voci che costruiscono il valore che il perito oggi non vede."),
        ("Gli ospiti arrivano dalle OTA.", "Buona parte delle prenotazioni passa dai portali, e quegli ospiti restano loro.", "Un acquirente non paga ospiti che appartengono a un altro."),
        ("Poche ricerche per nome.", "Il diretto non cresce, nonostante sito nuovo e campagne. Ti trovano come «hotel + zona».", "Una domanda che non porta il tuo nome non si trasferisce."),
        ("Le recensioni non dicono perché.", "«Pulito. Gentile. Torneremo.» Manca quella che dice: «L'unico posto dove ho trovato X.»", "Non c'è una prova scritta di ciò che ti distingue."),
        ("La squadra cambia ogni stagione.", "Si lavora per «un hotel come tanti». Il servizio dipende da chi c'è quell'anno.", "L'identità serve all'ospite, ma anche a chi lavora con te."),
        ("Ogni scelta riapre la discussione.", "Nuovo ristorante: quale concept? Nuova SPA: quale filosofia? Ogni volta si riparte da zero.", "Con un'identità definita, le scelte discendono dal posizionamento."),
        ("Occupazione nota, margine per camera meno.", "L'occupazione piena rassicura. Il margine per camera e per ospite lo guardi meno spesso.", "Chi valuta il tuo hotel guarda tutti i numeri."),
    ],
    sig_tail="Il valore dipende dall’immobile e dalle persone. La quinta riga si costruisce mettendo per iscritto il posizionamento.",
    br_h2="Un valore legato all'immobile è un segnale. <em>Manca il nome.</em>",
    br_lead="Il perito misura il terzo passaggio: ciò che incassi. Il brand nasce nel primo.",
    br_here=3,
    br_rings=["Chi sei, e per quale ospite. Oggi non è scritto.", "Cosa dici all'ospite, e dove.", "Cosa incassi. L'unico passaggio che il perito vede."],
    br_prose='''        <p>Un'identità scritta, applicata e visibile nelle vendite dirette aggiunge una riga al calcolo. Si chiama brand.</p>
        <p>E può cambiare il multiplo: da immobiliare ad aziendale.</p>
        <p><strong>È l'unica riga che dipende solo da te.</strong> E puoi iniziare a costruirla subito.</p>''',
    br_quote="Un'estetica si ammortizza. Un'identità si rivaluta.",
    offer_lead="L'analisi è il primo documento della riga 5: il posizionamento del tuo hotel, messo per iscritto.",
    cand_lead="Un minuto. Guardo il tuo hotel come farebbe un acquirente: cosa c'è oltre l'immobile.",
    faq=[
        ("Il perito sbaglia a non considerare il brand?", "No. Valuta ciò che si può trasferire. Il lavoro è rendere il brand trasferibile: scritto, applicato dalla squadra, visibile nelle prenotazioni dirette."),
        ("Cosa vuol dire «identità scritta»?", "Un posizionamento messo su una pagina, applicato nei testi, negli script e nelle scelte, verificabile nei numeri del diretto. Finché sta nella testa di una persona, non vale nulla per nessun altro."),
        ("Per me l'hotel è un immobile a reddito. Fa per me?", "Probabilmente no. Se il brand non è una priorità, ti serve un consulente immobiliare, non un posizionamento. Meglio dirlo subito."),
        ("Ho più hotel. Si può fare?", "Sì, ed è dove rende di più: ogni hotel distinto dagli altri del gruppo e dal mercato. Si parte comunque da uno."),
    ],
)
