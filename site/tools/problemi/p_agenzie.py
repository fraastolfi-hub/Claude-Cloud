from common import memo
from p_sostituibili import WORDS_JS

P = dict(
    slug="agenzie",
    title="Agenzia marketing per hotel: perché cambiarla non basta",
    og_title="Tre agenzie, stesso risultato. La statistica ha una sola spiegazione.",
    desc="Hai cambiato tre agenzie marketing in cinque anni e i risultati sono gli stessi? Quando cambi tre volte l'esecutore e il risultato non cambia, il problema è nelle istruzioni. Fai il test del tuo brief.",
    eyebrow="Sintomo 04 · Il valzer delle agenzie",
    h1="Ho cambiato tre agenzie in cinque anni. I risultati sono gli stessi.",
    pull='Tre agenzie, stesso risultato. <span class="hl or in">La statistica ha una sola spiegazione.</span>',
    lead="E non è che sono tutte incapaci. Quando cambi tre volte l'esecutore e il risultato non cambia, il problema è nelle istruzioni.",
    cta2="Fai il test del tuo brief ↓",
    memo=memo("Storico fornitori", "5 anni",
              [("Agenzia 1: prometteva, non portava.", "✕", "bad"),
               ("Agenzia 2: «Ci vuole tempo.» Il tempo è passato.", "✕", "bad"),
               ("Agenzia 3: post bellissimi, like dei parenti.", "✕", "bad")],
              "Prenotazioni in più", "di nessuno",
              "Tre squadre. Tre metodi. Stesso identico risultato."),
    ag_h2="Tre cuochi sbagliano lo stesso piatto? <em>È la ricetta.</em>",
    ag_lead="Un principio che vale in cucina, in sala e nel marketing. Un cuoco che sbaglia il piatto è incapace. Tre cuochi che sbagliano lo stesso piatto: la ricetta è sbagliata.",
    ag_prose='''        <p>Nel marketing la ricetta si chiama brief. Cosa dice il tuo?</p>
        <p>«Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità.»</p>
        <p>Con queste istruzioni anche la migliore agenzia d'Italia produce la stessa cosa: charme, eleganza, esperienza autentica. Come per gli altri dodici hotel che ha in portafoglio.</p>
        <p>Onestà: a volte il principio non vale. Ci sono agenzie davvero scarse. Le riconosci da una cosa: <strong>non ti fanno domande.</strong></p>
        <p>Ma se le domande te le facevano e tu non avevi le risposte, il problema non era loro.</p>''',
    tool='''      <div class="tool rv d1">
        <div class="tool-head"><span>Il test del brief</span><em>Usa il tuo</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="aTxt">Scrivi cosa hai chiesto all'ultima agenzia</label>
            <textarea id="aTxt" spellcheck="false">Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità e sull'esperienza autentica.</textarea>
          </div>
          <p class="brief-prev" id="aPrev" aria-hidden="true"></p>
          <div class="tool-row">
            <span class="lab">Il tuo brief risponde a queste tre domande?</span>
            <div class="bq" role="group" aria-labelledby="q1"><span id="q1">Per chi siamo, e per chi no?</span><div class="tgl"><button type="button" data-q="0" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="0" data-v="0" aria-pressed="false">No</button></div></div>
            <div class="bq" role="group" aria-labelledby="q2"><span id="q2">Contro chi competiamo davvero, anche fuori dagli hotel?</span><div class="tgl"><button type="button" data-q="1" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="1" data-v="0" aria-pressed="false">No</button></div></div>
            <div class="bq" role="group" aria-labelledby="q3"><span id="q3">Perché l'ospite sceglie noi, in una frase che si può verificare?</span><div class="tgl"><button type="button" data-q="2" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="2" data-v="0" aria-pressed="false">No</button></div></div>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Esito</span>
          <b class="tool-big" id="aOut">Brief da catalogo</b>
          <p id="aSub">Con queste istruzioni, chiunque produce charme ed eleganza.</p>
        </div>
      </div>''',
    css='''.brief-prev{font-size:16px;line-height:1.5;background:var(--paper);border:1px dashed var(--line);padding:12px 14px;overflow-wrap:anywhere}
.brief-prev:empty{display:none}
.bq{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 0;border-bottom:1px dashed #A1A1A6;font-size:16px;line-height:1.35}
.bq .tgl{flex:none;box-shadow:none}
.bq .tgl button{padding:8px 12px}
@media (max-width:480px){.bq{flex-direction:column;align-items:flex-start}}''',
    js='''/* test del brief */
(function(){''' + WORDS_JS + '''
  var ta=document.getElementById('aTxt'), prev=document.getElementById('aPrev');
  var out=document.getElementById('aOut'), sub=document.getElementById('aSub'), ans=[null,null,null];
  var bs=[].slice.call(document.querySelectorAll('.bq button'));
  function upd(){
    var r=mark(ta.value.trim()); prev.innerHTML=r.html;
    var y=ans.filter(function(a){return a===1;}).length, done=ans.indexOf(null)===-1;
    var w=r.n===1?'una parola che usano tutti':r.n+' parole che usano tutti';
    var gen=r.n?' E ci sono <strong>'+w+'</strong>, evidenziate qui sopra.':'';
    if(y===3 && r.n<=1){ out.textContent='Brief vero'; sub.innerHTML='Con queste istruzioni un’agenzia può lavorare. Se i risultati non arrivano lo stesso, forse è davvero l’agenzia.'; }
    else if(y>0){ out.textContent='Brief a metà'; sub.innerHTML='Manca '+(3-y===1?'una risposta':(3-y)+' risposte')+'. Le agenzie riempiono i vuoti con charme ed eleganza.'+gen; }
    else { out.textContent='Brief da catalogo'; sub.innerHTML=(done?'Nessuna delle tre risposte. ':'')+'Con queste istruzioni anche la migliore agenzia d’Italia produce charme, eleganza, esperienza autentica.'+gen; }
  }
  bs.forEach(function(b){ b.addEventListener('click',function(){
    var q=+b.dataset.q; ans[q]=+b.dataset.v;
    bs.forEach(function(x){ if(+x.dataset.q===q) x.setAttribute('aria-pressed',x===b); }); upd();
  }); });
  ta.addEventListener('input',upd); upd();
})();''',
    sig_h2="I dieci segnali che il problema <em>non è l'agenzia.</em>",
    sig_lead="Spunta quelli in cui ti riconosci. Se sono tanti, la quarta agenzia non ti salverà.",
    signals=[
        ("Il brief sta in tre righe.", "«Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità.»", "Con queste istruzioni, chiunque produce la stessa cosa."),
        ("Trenta secondi muti.", "L'agenzia chiede: «Cosa vi rende speciali?». Tu rispondi: «Cura. Qualità. Attenzione.» E loro scrivono esattamente quello.", "Se non sai dirlo in trenta secondi, non lo sai. E nemmeno loro."),
        ("Nessuno ti ha fatto domande.", "L'agenzia è partita dal piano editoriale, non da chi sei. E a te è sembrato normale.", "Questa sì che è scarsa. Le altre, forse, aspettavano le tue risposte."),
        ("Post bellissimi, like dei parenti.", "Il profilo è curato, il feed è ordinato. Le prenotazioni arrivano da altre parti.", "Prenotazioni di nessuno."),
        ("Bruci soldi su Google.", "Duemila euro di annunci. Cinquanta clic. Due prenotazioni. Clicca chiunque, prenota solo chi sa.", "Pubblicità senza identità è autocombustione."),
        ("«Ci vuole tempo.»", "Sei mesi di contratto. Poi altri sei. Il tempo è passato. Il risultato no.", "Il tempo non corregge un'istruzione sbagliata. La ripete."),
        ("Ogni tre anni, tutto nuovo.", "Sito nuovo. Agenzia nuova. Campagna nuova. Ogni volta un sintomo in meno per qualche mese. Poi torna.", "Stai riparando l'ultimo pezzo della catena. Da anni."),
        ("Il sito è un inventario.", "«Hotel 4 stelle. SPA. Ristorante. Relax.» Cambi il logo e funziona per altri cento.", "L'agenzia ha scritto quello che le hai dato."),
        ("Tutti scrivono bene. Con l'AI.", "Descrizioni generate, post generati. Scrivono tutti meglio. Dicono tutti le stesse cose.", "Scrivere bene è il nuovo zero. Non differenzia: pareggia."),
        ("Ogni campagna riparte da zero.", "Nuovo messaggio, nuova idea, nuovo tono. Ogni volta opinioni. Ogni volta un dibattito.", "Chi ha un'identità non dibatte. Deduce."),
    ],
    sig_tail="Non ti serve la quarta agenzia. Ti servono istruzioni. Si chiamano posizionamento.",
    br_h2="L'agenzia è il sintomo. <em>Il brief vuoto è la malattia.</em>",
    br_lead="Le agenzie lavorano su promessa e prenotazione. Il primo anello tocca a te: nessuno può scriverlo al posto tuo senza partire da te.",
    br_here=2,
    br_rings=["Quello che sai di essere. Il brief che manca.", "Quello che dici. Dove lavorano le agenzie.", "Quello che incassi. Uguale con tutte e tre."],
    br_prose='''        <p>La buona notizia: le istruzioni si possono scrivere. Si chiamano posizionamento.</p>
        <p>E la quarta agenzia, o la terza richiamata, con quelle in mano diventa improvvisamente brava.</p>
        <p><strong>Non devi cambiare chi esegue. Devi dargli cosa eseguire.</strong></p>''',
    br_quote="Quando cambi l'esecutore e il risultato non cambia, il problema è nelle istruzioni.",
    offer_lead="L'analisi è il brief che le agenzie aspettano da anni. Puoi girarla alla tua il giorno dopo.",
    cand_lead="Sessanta secondi. Guardo il tuo hotel come lo guarderebbe un'agenzia brava: con le domande che non ti hanno fatto.",
    faq=[
        ("Devo licenziare la mia agenzia?", "No. Devi darle finalmente delle istruzioni. Il posizionamento è il brief che le agenzie aspettano da anni. Molte, con quello in mano, diventano ottime."),
        ("Come capisco se l'agenzia è scarsa davvero?", "Da una cosa: non ti fa domande. Se te le fa e tu non hai le risposte, cambiarla non serve. Serve trovare le risposte."),
        ("Chi implementa? Tu o l'agenzia?", "La tua squadra o i tuoi fornitori, con una direzione, finalmente. Io ti do il posizionamento, i testi chiave e gli script. Loro eseguono."),
        ("Serve rifare il sito?", "Quasi mai da zero. Serve rifare quello che dice. Che costa meno e conta di più."),
    ],
)
