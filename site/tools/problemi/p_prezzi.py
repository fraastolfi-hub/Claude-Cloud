from common import memo, rng, RANGE_JS

P = dict(
    slug="prezzi",
    title="Guerra dei prezzi tra hotel: come smettere di scontare",
    og_title="Il tuo hotel migliora ogni anno. Il tuo prezzo è fermo al 2022.",
    desc="Il tuo hotel migliora ogni anno e il prezzo è fermo al 2022? Il prezzo non premia il prodotto: premia il motivo. Calcola quanto ti costa e riconosci i dieci segnali del prezzo fermo.",
    eyebrow="Sintomo 02 · Il listino",
    h1="Non riesco ad alzare i prezzi senza perdere prenotazioni.",
    pull='Il tuo hotel migliora ogni anno. Il tuo prezzo è fermo al 2022. <span class="hl or in">Uno dei due sta mentendo.</span>',
    lead="A venti chilometri da te c'è uno con un prodotto peggiore del tuo che chiede quaranta euro in più. E li prende. La domanda non è «perché non posso?». È «perché lui sì e io no?».",
    cta2="Quanto ti costa? Fai il conto ↓",
    memo=memo("Tre anni di lavori", "Il tuo hotel",
              [("Camere rinnovate", "✓ fatto", "ok"),
               ("Colazione rifatta", "✓ fatto", "ok"),
               ("Personale formato", "✓ fatto", "ok"),
               ("Recensioni salite", "✓ fatto", "ok")],
              "Il prezzo", "fermo al 2022",
              "Il prodotto è cresciuto. Il prezzo no. Strano, no?"),
    ag_h2="Il prezzo non premia il prodotto. <em>Premia il motivo.</em>",
    ag_lead="In qualunque altro mercato, prodotto migliore vuol dire prezzo maggiore. Nel tuo no. Vediamo perché.",
    ag_prose='''        <p>E non dirmi «il mercato non paga». Il mercato paga quello che gli hai spiegato.</p>
        <p>Quello a venti chilometri un motivo ce l'ha. O almeno l'ha scritto.</p>
        <p>Tu hai il prodotto. Ma il motivo non l'hai mai messo in parole.</p>
        <p><strong>Il premium senza motivo si chiama sovrapprezzo.</strong> E l'ospite lo annusa.</p>
        <p>Allora la domanda giusta è un'altra: quanto ti è costato, quest'anno, il motivo che non hai scritto?</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Il conto del motivo che manca</span><em>Metti i tuoi numeri</em></div>
        <div class="tool-body">
{rng("prR", "Camere", 5, 150, 1, 30)}
{rng("prO", "Occupazione media annua", 20, 95, 1, 60, suf="%")}
{rng("prD", "Euro in più a notte", 5, 100, 5, 40, pre="€", small="Quelli che prende il tuo vicino, a venti chilometri.")}
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Lasciati sul tavolo ogni anno</span>
          <b class="tool-big" id="prOut">€262.800</b>
          <p id="prSub">Senza una camera in più. Solo un prezzo che l'ospite accetta perché ha capito.</p>
        </div>
        <p class="tool-note">Onestà: il conto tiene ferma l'occupazione a prezzo più alto. Succede solo se l'ospite ha un motivo per pagarlo. Senza il motivo, quei soldi li perdi in prenotazioni. I valori di partenza sono d'esempio: metti i tuoi.</p>
      </div>''',
    js='''/* calcolatore prezzo fermo */
(function(){''' + RANGE_JS + '''
  bind(['prR','prO','prD'],function(){
    var out=v('prR')*365*v('prO')/100*v('prD');
    document.getElementById('prOut').textContent=eur(out);
    document.getElementById('prSub').innerHTML='Sono <strong>'+eur(out/12)+'</strong> al mese. Senza una camera in più. Solo un prezzo che l’ospite accetta perché ha capito.';
  });
})();''',
    sig_h2="I dieci segnali del <em>prezzo fermo.</em>",
    sig_lead="Spunta quelli in cui ti riconosci. Non è un problema di listino. È un problema di posizione.",
    signals=[
        ("L'ADR ha un soffitto. E non sai perché.", "Sopra una certa cifra le prenotazioni frenano. Il tuo prodotto varrebbe di più, ma il mercato non ti crede.", "Il premium senza motivo si chiama sovrapprezzo."),
        ("Il prodotto cresce. Il listino no.", "Camere rinnovate, colazione rifatta, recensioni salite. Il prezzo è quello di tre anni fa.", "Hai investito nel prodotto. Non nel motivo per pagarlo."),
        ("Mai alzato i prezzi.", "«Poi la gente non viene.» La gente giusta viene. Quella sbagliata no.", "Tieni i prezzi bassi e avrai solo la gente sbagliata."),
        ("Lo sconto all'ultimo minuto.", "L'ospite chiede lo sconto last minute e glielo dai. «Tanto la camera vuota non rende.»", "Stai allenando il mercato a non pagarti il prezzo pieno."),
        ("Upgrade gratis a settembre.", "«Tanto la camera era vuota.» L'ospite impara una cosa sola: aspettare. E aspetta sempre. Anche a luglio.", "Lo sconto, ripetuto, diventa il prezzo."),
        ("Ti confronti con chi costa meno.", "Guardi i vicini e ti metti un po' sotto. Competi sul prezzo.", "Le catene hanno cinquecento hotel. Indovina chi vince."),
        ("«Buon rapporto qualità-prezzo.»", "È la frase che torna più spesso nelle tue recensioni. Sembra un complimento.", "Vuol dire: costava poco. Nessuno ti sceglie per quello che costa poco."),
        ("Lo yo-yo.", "Bassa stagione: panico, sconti. Alta stagione: pieno, smetti di pensarci. Poi si ricomincia.", "Reagisci. Non costruisci."),
        ("Il senso di colpa al posto sbagliato.", "Alzi i prezzi, l'ospite «budget» se ne va, e tu ti senti in colpa.", "Dovresti festeggiare. Hai appena filtrato."),
        ("Sai l'occupazione. Non quanto guadagni per camera.", "Il pieno ti rassicura. Ma quanto resta per camera e per ospite non lo guardi.", "Stai guidando bendato. I numeri sono lì."),
    ],
    sig_tail="Non ti serve un listino nuovo. Ti serve un motivo per cui l’ospite paga il listino che hai.",
    br_h2="Il prezzo fermo è il sintomo. <em>Non la malattia.</em>",
    br_lead="Il listino sta sul terzo anello. Lo ritocchi da anni. Il problema sta due anelli prima.",
    br_here=3,
    br_rings=["Quello che sai di essere.", "Quello che dici all'ospite.", "Quello che incassi. Allo stesso prezzo del 2022."],
    br_prose='''        <p>Tariffe dinamiche, pacchetti, promozioni: tutto terzo anello. Servono, quando c'è qualcosa da vendere al prezzo giusto.</p>
        <p>Il prezzo sale quando cambia il confronto. Finché l'ospite ti mette accanto agli hotel della zona, vince il più economico.</p>
        <p><strong>Quando ti confronta con un'altra cosa, cambia anche il prezzo che trova giusto.</strong></p>''',
    br_quote="Chi non sa chi è, finisce a vendere sconti.",
    proof_k="Tariffa media",
    proof_big="circa ×2",
    offer_lead="Uno dei cinque documenti dell'analisi completa si chiama «Come vendere senza svendere». Ma si parte dal motivo.",
    cand_lead="Sessanta secondi. Guardo il tuo hotel, i tuoi prezzi e quelli dei vicini. Poi ti dico cosa manca.",
    faq=[
        ("Nella mia zona il mercato non paga.", "Allora spiegami quello a venti chilometri, con un prodotto peggiore, che chiede quaranta euro in più. E li prende. Il mercato paga i motivi. Non le camere."),
        ("Se alzo i prezzi, perdo prenotazioni?", "Se hai un motivo, perdi quelle sbagliate. Senza motivo le perdi e basta. Per questo il posizionamento viene prima del listino, non dopo."),
        ("Non mi basta un revenue manager?", "Il revenue management lavora sul prezzo che il mercato accetta. Il posizionamento cambia quale prezzo il mercato trova giusto. Prima la bussola, poi la regolazione fine."),
        ("Chi implementa? Tu o io?", "Tu, o la tua squadra. Io ti do la direzione, i testi e gli script. Nell'analisi completa c'è anche come gestire l'obiezione sul prezzo. Tu esegui, o deleghi."),
    ],
)
