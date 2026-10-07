from common import memo, rng, RANGE_JS

P = dict(
    slug="prezzi",
    title="Alzare le tariffe senza perdere prenotazioni",
    og_title="Il prodotto migliora ogni anno. La tariffa no.",
    desc="Camere e servizi migliorano, ma la tariffa resta ferma? Il prezzo segue il motivo per cui l'ospite sceglie, non il prodotto. Un calcolo con i vostri numeri e dieci segnali di una tariffa bloccata.",
    eyebrow="Segnale 02 · Prezzo",
    h1="Alzare le tariffe senza perdere prenotazioni.",
    pull='Alzare le tariffe significa perdere prenotazioni. <span class="hl or in">Finché l\'ospite non ha un motivo per pagarle.</span>',
    lead="Capita spesso: a pochi chilometri, una struttura con un prodotto comparabile chiede quaranta euro in più a notte e mantiene l'occupazione. La differenza raramente è nel prodotto. È nel motivo che l'ospite riconosce.",
    cta2="Il calcolo con i vostri numeri ↓",
    memo=memo("Tre anni di investimenti", "La struttura",
              [("Camere rinnovate", "✓ fatto", "ok"),
               ("Colazione rivista", "✓ fatto", "ok"),
               ("Personale formato", "✓ fatto", "ok"),
               ("Recensioni in crescita", "✓ fatto", "ok")],
              "La tariffa", "ferma da tre anni",
              "Il prodotto è cresciuto. La tariffa no."),
    ag_h2="Il prezzo non premia il prodotto. <em>Premia il motivo.</em>",
    ag_lead="In molti mercati un prodotto migliore giustifica un prezzo più alto. Nell'ospitalità succede solo se l'ospite capisce perché.",
    ag_prose='''        <p>Il mercato paga ciò che riesce a capire.</p>
        <p>La struttura vicina che chiede di più, di solito, ha un motivo chiaro. O almeno lo ha scritto.</p>
        <p>Molte strutture hanno il prodotto, ma il motivo non è mai stato messo in parole.</p>
        <p><strong>Un premium senza motivo, per l'ospite, è un sovrapprezzo.</strong></p>
        <p>La domanda utile è un'altra: quanto vale, ogni anno, la differenza di tariffa che oggi non riuscite a sostenere?</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Il valore della differenza</span><em>Con i vostri numeri</em></div>
        <div class="tool-body">
{rng("prR", "Camere", 5, 150, 1, 30)}
{rng("prO", "Occupazione media annua", 20, 95, 1, 60, suf="%")}
{rng("prD", "Euro in più a notte", 5, 100, 5, 40, pre="€", small="La differenza con una struttura comparabile della zona.")}
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Valore annuo della differenza</span>
          <b class="tool-big" id="prOut">€262.800</b>
          <p id="prSub">A parità di camere. Solo con una tariffa che l'ospite accetta perché ne capisce il motivo.</p>
        </div>
        <p class="tool-note">Il calcolo presuppone la stessa occupazione a una tariffa più alta. Accade solo se l'ospite ha un motivo per pagarla: senza, la differenza si perde in prenotazioni. I valori di partenza sono d'esempio: inserite i vostri.</p>
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
    sig_lead="Selezionate quelli che riconoscete nella vostra struttura. Raramente è una questione di listino: più spesso di posizione.",
    signals=[
        ("La tariffa media ha un tetto.", "Oltre una certa cifra le prenotazioni rallentano. Il prodotto varrebbe di più, ma l'ospite non ne vede la ragione.", "Un premium senza motivo, per l'ospite, è un sovrapprezzo."),
        ("Il prodotto cresce, il listino no.", "Camere rinnovate, colazione rivista, recensioni in crescita. La tariffa è quella di tre anni fa.", "Si è investito nel prodotto, non nel motivo per pagarlo."),
        ("Tariffe mai ritoccate.", "Il timore è che gli ospiti smettano di arrivare. In realtà, con un aumento, si perdono soprattutto quelli meno adatti alla struttura.", "Tariffe basse attirano soprattutto chi sceglie per prezzo."),
        ("Lo sconto dell'ultimo minuto.", "L'ospite chiede uno sconto a ridosso della data e lo ottiene: una camera vuota non rende.", "Ripetuto, insegna al mercato ad aspettare."),
        ("Upgrade gratuiti in bassa stagione.", "La camera era libera. Ma l'ospite impara ad aspettare l'occasione, anche a luglio.", "Lo sconto, ripetuto, diventa il prezzo."),
        ("Il riferimento è chi costa meno.", "La tariffa si fissa guardando le strutture vicine, un po' più in basso. Il confronto avviene sul prezzo.", "Sul prezzo vincono le catene: hanno costi e volumi che una struttura indipendente non ha."),
        ("«Buon rapporto qualità-prezzo.»", "È la frase più frequente nelle recensioni. Sembra un complimento.", "Indica che il criterio di scelta è stato il prezzo."),
        ("L'altalena stagionale.", "In bassa stagione sconti, in alta stagione il pieno. Poi il ciclo riparte.", "Si reagisce alla stagione invece di costruire una domanda propria."),
        ("Gli ospiti persi con l'aumento.", "Con un aumento, una parte degli ospiti più attenti al prezzo sceglie altro. Viene vissuto come una perdita.", "Spesso è una selezione: la camera resta disponibile per chi ne riconosce il valore."),
        ("Occupazione nota, margine per camera meno.", "L'occupazione piena rassicura. Quanto resta per camera e per ospite si guarda meno spesso.", "I dati ci sono già: vanno letti insieme."),
    ],
    sig_tail="Non serve un listino nuovo. Serve un motivo per cui l’ospite accetta la tariffa che avete.",
    br_h2="La tariffa ferma è un segnale. <em>La causa è più a monte.</em>",
    br_lead="Il listino sta nel terzo passaggio, e lì si interviene da anni. La causa è due passaggi prima.",
    br_here=3,
    br_rings=["Chi siete, e per quale ospite.", "Cosa dite all'ospite, e dove.", "Cosa incassate. Alla tariffa di tre anni fa."],
    br_prose='''        <p>Tariffe dinamiche, pacchetti, promozioni: tutto terzo passaggio. Servono quando c'è qualcosa da vendere al prezzo giusto.</p>
        <p>La tariffa sale quando cambia il confronto. Se l'ospite vi mette accanto alle altre strutture della zona, vince la più economica.</p>
        <p><strong>Quando vi confronta con un'alternativa diversa, cambia anche il prezzo che considera giusto.</strong></p>''',
    br_quote="Senza un posizionamento chiaro, l'unica leva che resta è il prezzo.",
    proof_k="Tariffa media",
    proof_big="circa ×2",
    offer_lead="Uno dei cinque documenti dell'analisi completa si chiama «Come vendere senza svendere». Il punto di partenza resta il motivo.",
    cand_lead="Un minuto. Analizzo la struttura, le vostre tariffe e quelle delle strutture vicine, poi vi indico cosa manca.",
    faq=[
        ("Nella nostra zona il mercato non accetta tariffe più alte.", "Spesso nella stessa zona c'è una struttura comparabile che applica una tariffa più alta e la mantiene. Il mercato paga i motivi che riconosce, non le camere in sé."),
        ("Se alziamo le tariffe, perdiamo prenotazioni?", "Con un motivo chiaro si perdono soprattutto quelle meno adatte alla struttura. Senza, si perdono e basta. Per questo il posizionamento viene prima del listino."),
        ("Non basta un revenue manager?", "Il revenue management lavora sul prezzo che il mercato accetta. Il posizionamento cambia il prezzo che il mercato considera giusto. Prima la bussola, poi la regolazione fine."),
        ("Chi si occupa dell'attuazione?", "La vostra squadra o i vostri fornitori. Io fornisco la direzione, i testi e gli script; nell'analisi completa c'è anche come gestire l'obiezione sul prezzo."),
    ],
)
