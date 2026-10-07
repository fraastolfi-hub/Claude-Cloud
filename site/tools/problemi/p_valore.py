from common import memo, rng, RANGE_JS

P = dict(
    slug="valore",
    title="Quanto vale un hotel? Il brand nella valutazione",
    og_title="Il valore della struttura oltre l'immobile: la riga che manca nella perizia.",
    desc="Il perito valuta posizione, metri quadri, stato dell'immobile ed EBITDA. Il nome della struttura non compare in nessuna riga. Un calcolo per capire quanto vale la riga che manca: il brand.",
    eyebrow="Segnale 05 · Valore del brand",
    h1="Un brand che valga oltre l'immobile.",
    pull='Il valore della struttura coincide con quello dell\'immobile. <span class="hl or in">Il calcolo del perito lo mostra in quattro righe.</span>',
    lead="Poi c'è una quinta riga, che oggi manca. È l'unica del calcolo che dipende interamente dalle scelte della struttura.",
    cta2="Il calcolo del perito ↓",
    memo=memo("Perizia · foglio 1", "Il nome?",
              [("Riga 1 · La posizione", "✕ no", "bad"),
               ("Riga 2 · I metri quadri", "✕ no", "bad"),
               ("Riga 3 · Lo stato dell'immobile", "✕ no", "bad"),
               ("Riga 4 · EBITDA × multiplo di zona", "✕ no", "bad")],
              "Il nome della struttura", "in nessuna riga",
              "Vent'anni di lavoro, quattro righe. Nessuna riguarda l'identità."),
    ag_h2="Il calcolo che riassume <em>vent'anni di lavoro.</em>",
    ag_lead="Sono quattro righe, e chi gestisce una struttura le conosce già.",
    ag_prose='''        <p><strong>Riga 1, la posizione.</strong> Vale quanto vale la zona. Non dipende dalla gestione.</p>
        <p><strong>Riga 2, i metri quadri.</strong> Moltiplicati per il valore locale. È un calcolo, non un merito.</p>
        <p><strong>Riga 3, lo stato dell'immobile.</strong> Qui entrano le ristrutturazioni, già ammortizzate.</p>
        <p><strong>Riga 4, l'EBITDA.</strong> Per un multiplo di zona: quello degli immobili, non delle aziende.</p>
        <p>Gli ospiti che tornano da dieci anni, il modo di lavorare della squadra: non compaiono in nessuna riga. Non per una scelta del perito. Il perito valuta ciò che si può trasferire, e un'identità che esiste solo nella testa della proprietà non si trasferisce.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>La riga che manca</span><em>Foglio del perito</em></div>
        <div class="tool-body">
{rng("vlE", "EBITDA annuo", 100000, 5000000, 50000, 500000, pre="€", small="Valore d'esempio: inserite il vostro.")}
{rng("vlM", "Punti di multiplo in più", 0.5, 5, 0.5, 1, pre="+")}
          <div class="tool-row">
            <span class="lab">Riga 5 · Il brand</span>
            <button type="button" class="btn sm" id="vlB" aria-pressed="false" style="justify-self:start">Aggiungi la riga 5 <span class="arr">+</span></button>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k" id="vlK">Riga 5 · Il brand</span>
          <b class="tool-big" id="vlOut">€0</b>
          <p id="vlSub">Senza un'identità documentata, non c'è nulla da acquistare: il brand vale zero.</p>
        </div>
        <p class="tool-note">Di quanto cambi il multiplo dipende dalla zona, dal mercato e dall'acquirente: non è un dato che si possa promettere in una pagina web. Qui trovate quanto vale ogni punto. Il calcolo è EBITDA × punti.</p>
      </div>''',
    js='''/* la riga che manca */
(function(){''' + RANGE_JS + '''
  var on=false, b=document.getElementById('vlB');
  function calc(){
    var e=v('vlE'), m=v('vlM');
    document.getElementById('vlOut').textContent=on?eur(e*m):'€0';
    document.getElementById('vlSub').innerHTML=on
      ? 'Ogni punto di multiplo, sul vostro EBITDA, vale <strong>'+eur(e)+'</strong>. Il brand è la riga che può spostarlo: da multiplo immobiliare a multiplo aziendale.'
      : 'Senza un’identità documentata, non c’è nulla da acquistare: il brand vale zero.';
  }
  b.addEventListener('click',function(){
    on=!on; b.setAttribute('aria-pressed',on);
    b.innerHTML=on?'Togli la riga 5 <span class="arr">−</span>':'Aggiungi la riga 5 <span class="arr">+</span>';
    calc();
  });
  bind(['vlE','vlM'],calc);
})();''',
    sig_h2="Dieci segnali di un valore <em>legato solo all'immobile.</em>",
    sig_lead="Selezionate quelli che riconoscete nella vostra struttura. Ognuno indica una parte di valore che resta nelle persone invece che nella struttura.",
    signals=[
        ("La valutazione considera l'immobile, non il brand.", "In caso di vendita, il prezzo sarebbe posizione più metri quadri più EBITDA. Il brand varrebbe zero, perché non c'è nulla di trasferibile.", "Una struttura con un'identità si valuta come un'azienda. Senza, come un immobile."),
        ("L'identità dipende da una persona.", "Sta nella testa della proprietà o della direzione: non nei documenti, non nella squadra, non nel sito. Con un mese di assenza, la comunicazione torna generica.", "Per la gestione è un limite. Per la proprietà è un rischio patrimoniale."),
        ("Il vantaggio estetico è temporaneo.", "Il restyling è recente, ma una struttura vicina ristruttura ora, con lo stesso studio. E nel calcolo le ristrutturazioni sono già ammortizzate.", "L'estetica scade. L'identità resta."),
        ("Gli investimenti vanno dove si vedono.", "Ristrutturazione, arredi, tecnologia. Meno spesso strategia, formazione e marketing.", "Sono proprio le voci che costruiscono la parte di valore che il perito oggi non vede."),
        ("Gli ospiti arrivano dalle OTA.", "Buona parte delle prenotazioni passa dai portali, e il rapporto con quegli ospiti resta a loro.", "Un acquirente non paga ospiti che appartengono a un altro."),
        ("Poche ricerche per nome.", "Il diretto non cresce, nonostante sito nuovo e campagne. La struttura viene trovata come «hotel + zona».", "Una domanda che non porta il vostro nome non si trasferisce."),
        ("Le recensioni non dicono perché.", "«Pulito. Gentile. Torneremo.» Manca quella che dice: «L'unico posto dove ho trovato X.»", "Non esiste una prova scritta di ciò che vi distingue."),
        ("La squadra cambia ogni stagione.", "Si lavora per «una struttura come tante». Il servizio dipende da chi c'è quell'anno.", "L'identità serve all'ospite, ma anche a chi lavora con voi."),
        ("Ogni scelta riapre la discussione.", "Nuovo ristorante: quale concept? Nuova SPA: quale filosofia? Ogni volta si riparte da zero.", "Con un'identità definita, le scelte discendono dal posizionamento."),
        ("Occupazione nota, margine per camera meno.", "L'occupazione piena rassicura. Il margine per camera e per ospite si guarda meno spesso.", "Chi valuta la struttura guarda tutti i numeri."),
    ],
    sig_tail="Molti segnali insieme indicano che il valore dipende dall’immobile e dalle persone. La quinta riga si costruisce mettendo per iscritto il posizionamento.",
    br_h2="Un valore legato all'immobile è un segnale. <em>Manca il nome.</em>",
    br_lead="Il perito misura il terzo passaggio: ciò che la struttura incassa. Il brand nasce nel primo.",
    br_here=3,
    br_rings=["Chi siete, e per quale ospite. Oggi non è scritto.", "Cosa dite all'ospite, e dove.", "Cosa incassate. L'unico passaggio che il perito vede."],
    br_prose='''        <p>Una struttura con un'identità documentata, cioè scritta, applicata e visibile nelle vendite dirette, aggiunge una riga al calcolo. Si chiama brand.</p>
        <p>E può cambiare il multiplo: da immobiliare ad aziendale.</p>
        <p><strong>È l'unica riga del calcolo che dipende interamente dalla struttura.</strong> E si può iniziare a costruirla subito.</p>''',
    br_quote="Un'estetica si ammortizza. Un'identità si rivaluta.",
    offer_lead="L'analisi è il primo documento della riga 5: il posizionamento della struttura, messo per iscritto.",
    cand_lead="Un minuto. Analizzo la struttura come farebbe un acquirente: cosa c'è oltre l'immobile.",
    faq=[
        ("Il perito sbaglia a non considerare il brand?", "No. Valuta ciò che si può trasferire. Il lavoro consiste nel rendere il brand trasferibile: scritto, applicato dalla squadra, visibile nelle prenotazioni dirette."),
        ("Che cosa significa «identità documentata»?", "Un posizionamento scritto su una pagina, applicato nei testi, negli script e nelle scelte, verificabile nei numeri delle vendite dirette. Finché resta nella testa di una persona, non ha valore per nessun altro."),
        ("Consideriamo la struttura un immobile a reddito. È adatto a noi?", "Probabilmente no. Se il brand non è una priorità, serve un consulente immobiliare, non un posizionamento. Meglio chiarirlo subito."),
        ("Abbiamo più strutture. Si può fare?", "Sì, ed è dove rende di più: ogni struttura distinta dalle altre del gruppo e dal mercato. Si parte comunque dall'analisi di una."),
    ],
)
