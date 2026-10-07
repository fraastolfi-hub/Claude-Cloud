from common import memo, rng, RANGE_JS

P = dict(
    slug="prezzi",
    title="Alzare le tariffe senza perdere prenotazioni",
    og_title="Il prodotto migliora ogni anno. La tariffa no.",
    desc="Il tuo hotel migliora, ma la tariffa resta ferma? Il prezzo segue il motivo per cui l'ospite sceglie, non il prodotto. Fai il calcolo con i tuoi numeri.",
    eyebrow="Il problema · Tariffe che non salgono",
    h1="Alzare le tariffe senza perdere prenotazioni.",
    pull='Alzare le tariffe significa perdere prenotazioni. <span class="hl or in">Finché l\'ospite non ha un motivo per pagarle.</span>',
    lead="A pochi chilometri, un hotel simile al tuo chiede €40 in più a notte e resta pieno. La differenza raramente è nel prodotto. È nel motivo che l'ospite riconosce.",
    cta2="Fai il calcolo con i tuoi numeri ↓",
    memo=memo("Tre anni di investimenti", "Il tuo hotel",
              [("Camere rinnovate", "✓ fatto", "ok"),
               ("Colazione rivista", "✓ fatto", "ok"),
               ("Personale formato", "✓ fatto", "ok"),
               ("Recensioni in crescita", "✓ fatto", "ok")],
              "La tariffa", "ferma da tre anni",
              "Il prodotto è cresciuto. La tariffa no."),
    ag_h2="Il prezzo non premia il prodotto. <em>Premia il motivo.</em>",
    ag_lead="Un prodotto migliore giustifica un prezzo più alto solo se l'ospite capisce perché.",
    ag_prose='''        <p>Il mercato paga ciò che capisce.</p>
        <p>L'hotel vicino che chiede di più, di solito, ha un motivo chiaro. O almeno l'ha scritto.</p>
        <p>Tu hai il prodotto. Il motivo, forse, non l'hai mai messo in parole.</p>
        <p><strong>Un premium senza motivo, per l'ospite, è un sovrapprezzo.</strong></p>
        <p>La domanda utile: quanto vale ogni anno la differenza che oggi non riesci a chiedere?</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Il valore della differenza</span><em>Con i tuoi numeri</em></div>
        <div class="tool-body">
{rng("prR", "Camere", 5, 150, 1, 30)}
{rng("prO", "Occupazione media annua", 20, 95, 1, 60, suf="%")}
{rng("prD", "Euro in più a notte", 5, 100, 5, 40, pre="€", small="La differenza con un hotel simile della tua zona.")}
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Valore annuo della differenza</span>
          <b class="tool-big" id="prOut">€262.800</b>
          <p id="prSub">A parità di camere. Solo con una tariffa che l'ospite accetta perché ne capisce il motivo.</p>
        </div>
        <p class="tool-note">Il calcolo tiene ferma l'occupazione. Succede solo se l'ospite ha un motivo per pagare di più: senza, perdi prenotazioni. Valori d'esempio: metti i tuoi.</p>
      </div>''',
    js='''/* calcolatore prezzo fermo */
(function(){''' + RANGE_JS + '''
  bind(['prR','prO','prD'],function(){
    var out=v('prR')*365*v('prO')/100*v('prD');
    document.getElementById('prOut').textContent=eur(out);
    document.getElementById('prSub').innerHTML='Sono <strong>'+eur(out/12)+'</strong> al mese, a parità di camere. Solo con una tariffa che l’ospite accetta perché ne capisce il motivo.';
  });
})();''',
    sig_h2="Dieci segnali di <em>una tariffa bloccata.</em>",
    sig_lead="Seleziona quelli che riconosci nel tuo hotel. Raramente è una questione di listino.",
    signals=[
        ("La tariffa media ha un tetto.", "Oltre una certa cifra le prenotazioni rallentano. Il prodotto varrebbe di più, ma l'ospite non vede perché.", "Un premium senza motivo, per l'ospite, è un sovrapprezzo."),
        ("Il prodotto cresce, il listino no.", "Camere rinnovate, colazione rivista, recensioni in crescita. La tariffa è quella di tre anni fa.", "Hai investito nel prodotto, non nel motivo per pagarlo."),
        ("Tariffe mai ritoccate.", "Temi che gli ospiti smettano di arrivare. Con un aumento perdi soprattutto quelli meno adatti al tuo hotel.", "Tariffe basse attirano chi sceglie per prezzo."),
        ("Lo sconto dell'ultimo minuto.", "L'ospite chiede uno sconto a ridosso della data e lo ottiene: una camera vuota non rende.", "Ripetuto, insegna al mercato ad aspettare."),
        ("Upgrade gratuiti in bassa stagione.", "La camera era libera. Ma l'ospite impara ad aspettare l'occasione, anche a luglio.", "Lo sconto, ripetuto, diventa il prezzo."),
        ("Il riferimento è chi costa meno.", "Guardi gli hotel vicini e ti metti un po' sotto. Il confronto diventa il prezzo.", "Sul prezzo vincono le catene: hanno costi e volumi che un indipendente non ha."),
        ("«Buon rapporto qualità-prezzo.»", "È la frase più frequente nelle recensioni. Sembra un complimento.", "Indica che il criterio di scelta è stato il prezzo."),
        ("L'altalena stagionale.", "In bassa stagione sconti, in alta stagione il pieno. Poi il ciclo riparte.", "Si reagisce alla stagione invece di costruire una domanda propria."),
        ("Gli ospiti persi con l'aumento.", "Alzi la tariffa e chi guarda solo il prezzo sceglie altro. Lo vivi come una perdita.", "Spesso è un filtro: la camera resta per chi ne riconosce il valore."),
        ("Occupazione nota, margine per camera meno.", "L'occupazione piena rassicura. Quanto resta per camera e per ospite si guarda meno spesso.", "I dati ci sono già: vanno letti insieme."),
    ],
    sig_tail="Non ti serve un listino nuovo. Ti serve un motivo per cui l’ospite accetta la tua tariffa.",
    br_h2="La tariffa ferma è un segnale. <em>La causa è più a monte.</em>",
    br_lead="Il listino sta nel terzo passaggio, e lì intervieni da anni. La causa è due passaggi prima.",
    br_here=3,
    br_rings=["Chi sei, e per quale ospite.", "Cosa dici all'ospite, e dove.", "Cosa incassi. Alla tariffa di tre anni fa."],
    br_prose='''        <p>Tariffe dinamiche, pacchetti, promozioni: tutto terzo passaggio. Servono quando hai qualcosa da vendere al prezzo giusto.</p>
        <p>La tariffa sale quando cambia il confronto. Se l'ospite ti mette accanto agli hotel della zona, vince il più economico.</p>
        <p><strong>Se ti confronta con un'alternativa diversa, cambia anche il prezzo che considera giusto.</strong></p>''',
    br_quote="Il mercato paga i motivi che riconosce. Non le camere.",
    proof_k="Tariffa media",
    proof_big="circa ×2",
    offer_lead="Uno dei cinque documenti dell'analisi completa si chiama «Come vendere senza svendere». Si parte sempre dal motivo.",
    cand_lead="Un minuto. Guardo il tuo hotel, le tue tariffe e quelle dei vicini. Poi ti dico cosa manca.",
    faq=[
        ("Nella mia zona il mercato non accetta tariffe più alte.", "Spesso nella stessa zona c'è un hotel simile che chiede di più e resta pieno. Il prezzo che regge dipende dal motivo che l'ospite riconosce, più che dalle camere."),
        ("Se alzo le tariffe, perdo prenotazioni?", "Con un motivo chiaro perdi soprattutto quelle meno adatte al tuo hotel. Senza, le perdi e basta. Per questo il posizionamento viene prima del listino."),
        ("Non basta un revenue manager?", "Il revenue manager lavora sul prezzo che il mercato accetta. Il posizionamento cambia il prezzo che il mercato considera giusto. Prima la bussola, poi la regolazione fine."),
        ("Chi mette in pratica?", "La tua squadra o i tuoi fornitori. Io do la direzione, i testi e gli script. Nell'analisi completa c'è anche come gestire l'obiezione sul prezzo."),
    ],
)
