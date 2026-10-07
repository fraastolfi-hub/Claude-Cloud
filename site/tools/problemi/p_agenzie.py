from common import memo
from p_sostituibili import WORDS_JS

P = dict(
    slug="agenzie",
    title="Agenzie marketing per hotel: perché cambiarle non basta",
    og_title="Agenzie diverse, risultati simili. La causa è nelle istruzioni.",
    desc="Hai cambiato più agenzie e i risultati sono simili? Quando cambia chi esegue e il risultato no, la causa è nelle istruzioni. Fai il test del tuo brief.",
    eyebrow="Il problema · Agenzie che non bastano",
    h1="Dare alle agenzie un brief chiaro.",
    pull='Agenzie diverse, risultati simili. <span class="hl or in">Quando cambia chi esegue e il risultato no, la causa è nelle istruzioni.</span>',
    lead="Non vuol dire che le agenzie fossero tutte scarse. Ognuna ha ricevuto lo stesso brief, e ha fatto ciò che quel brief permetteva.",
    cta2="Fai il test del tuo brief ↓",
    memo=memo("Fornitori di comunicazione", "5 anni",
              [("Agenzia 1: obiettivi ambiziosi, risultati modesti.", "✕", "bad"),
               ("Agenzia 2: «Serve tempo.» Il tempo è passato.", "✕", "bad"),
               ("Agenzia 3: contenuti curati, poche prenotazioni.", "✕", "bad")],
              "Prenotazioni in più", "invariate",
              "Tre squadre, tre metodi. Lo stesso risultato."),
    ag_h2="Se tre cuochi sbagliano lo stesso piatto, <em>va rivista la ricetta.</em>",
    ag_lead="Un cuoco che sbaglia un piatto può essere poco preparato. Se lo sbagliano in tre, il problema è la ricetta.",
    ag_prose='''        <p>Nel marketing la ricetta si chiama brief. Spesso dice così:</p>
        <p>«Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità.»</p>
        <p>Con queste istruzioni anche un'ottima agenzia scrive charme, eleganza, esperienza autentica. Le stesse parole che usa per gli altri hotel che segue.</p>
        <p>A volte l'agenzia è davvero inadeguata. Lo riconosci da un segnale: <strong>non fa domande.</strong></p>
        <p>Se le domande arrivavano e mancavano le risposte, cambiare agenzia non basta.</p>''',
    tool='''      <div class="tool rv d1">
        <div class="tool-head"><span>Il test del brief</span><em>Con il tuo brief</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="aTxt">Scrivi cosa hai chiesto all'ultima agenzia</label>
            <textarea id="aTxt" spellcheck="false">Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità e sull'esperienza autentica.</textarea>
          </div>
          <p class="brief-prev" id="aPrev" aria-hidden="true"></p>
          <div class="tool-row">
            <span class="lab">Il tuo brief risponde a queste tre domande?</span>
            <div class="bq" role="group" aria-labelledby="q1"><span id="q1">Per quali ospiti è il mio hotel, e per quali no?</span><div class="tgl"><button type="button" data-q="0" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="0" data-v="0" aria-pressed="false">No</button></div></div>
            <div class="bq" role="group" aria-labelledby="q2"><span id="q2">Con chi compete davvero, anche fuori dagli hotel?</span><div class="tgl"><button type="button" data-q="1" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="1" data-v="0" aria-pressed="false">No</button></div></div>
            <div class="bq" role="group" aria-labelledby="q3"><span id="q3">Perché l'ospite sceglie il mio hotel, in una frase verificabile?</span><div class="tgl"><button type="button" data-q="2" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="2" data-v="0" aria-pressed="false">No</button></div></div>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Esito</span>
          <b class="tool-big" id="aOut">Brief generico</b>
          <p id="aSub">Con queste istruzioni, qualsiasi agenzia produce charme ed eleganza.</p>
        </div>
      </div>''',
    css='''.brief-prev{font-size:16px;line-height:1.5;color:var(--ink-2);background:var(--white);border-radius:var(--r-sm);padding:14px 16px;overflow-wrap:anywhere}
.brief-prev:empty{display:none}
.bq{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:12px 0;border-bottom:1px solid var(--line);font-size:16px;line-height:1.35;color:var(--ink)}
.bq:last-child{border-bottom:0}
.bq .tgl{flex:none}
.bq .tgl button{padding:7px 14px}
@media (max-width:480px){.bq{flex-direction:column;align-items:flex-start}}''',
    js='''/* test del brief */
(function(){''' + WORDS_JS + '''
  var ta=document.getElementById('aTxt'), prev=document.getElementById('aPrev');
  var out=document.getElementById('aOut'), sub=document.getElementById('aSub'), ans=[null,null,null];
  var bs=[].slice.call(document.querySelectorAll('.bq button'));
  function upd(){
    var r=mark(ta.value.trim()); prev.innerHTML=r.html;
    var y=ans.filter(function(a){return a===1;}).length, done=ans.indexOf(null)===-1;
    var w=r.n===1?'una parola di uso comune':r.n+' parole di uso comune';
    var gen=r.n?' Il testo contiene <strong>'+w+'</strong>, evidenziate qui sopra.':'';
    if(y===3 && r.n<=1){ out.textContent='Brief completo'; sub.innerHTML='Con queste istruzioni un’agenzia può lavorare bene. Se i risultati non arrivano lo stesso, la causa può essere davvero l’agenzia.'; }
    else if(y>0){ out.textContent='Brief incompleto'; sub.innerHTML='Manca '+(3-y===1?'una risposta':(3-y)+' risposte')+'. Dove mancano risposte, l’agenzia riempie il vuoto con charme ed eleganza.'+gen; }
    else { out.textContent='Brief generico'; sub.innerHTML=(done?'Nessuna delle tre risposte. ':'')+'Con queste istruzioni anche un’ottima agenzia produce charme, eleganza, esperienza autentica.'+gen; }
  }
  bs.forEach(function(b){ b.addEventListener('click',function(){
    var q=+b.dataset.q; ans[q]=+b.dataset.v;
    bs.forEach(function(x){ if(+x.dataset.q===q) x.setAttribute('aria-pressed',x===b); }); upd();
  }); });
  ta.addEventListener('input',upd); upd();
})();''',
    sig_h2="Dieci segnali che la causa <em>non è l'agenzia.</em>",
    sig_lead="Seleziona quelli che riconosci nel tuo hotel. Se sono molti, un'altra agenzia difficilmente cambierà il risultato.",
    signals=[
        ("Il brief sta in tre righe.", "«Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità.»", "Con queste istruzioni, qualsiasi agenzia produce la stessa cosa."),
        ("La risposta a «perché voi?».", "L'agenzia chiede: «Cosa vi distingue?». Rispondi «cura, qualità, attenzione», e l'agenzia scrive esattamente questo.", "Se la risposta non è chiara a te, non può esserlo all'agenzia."),
        ("Nessuna domanda iniziale.", "L'agenzia è partita dal piano editoriale, non dall'identità del tuo hotel. E nessuno l'ha notato.", "Questo è un limite dell'agenzia. Le altre, forse, aspettavano risposte."),
        ("Contenuti curati, poche prenotazioni.", "Il profilo è ordinato, i contenuti sono di qualità. Le prenotazioni arrivano da altri canali.", "La cura formale non sostituisce un messaggio."),
        ("Campagne a basso rendimento.", "€2.000 di annunci, 50 clic, 2 prenotazioni. Clicca chiunque; prenota chi ha capito cosa offri.", "La pubblicità amplifica il messaggio. Anche quando è generico."),
        ("«Serve tempo.»", "Sei mesi di contratto, poi altri sei. Il tempo passa, il risultato resta.", "Il tempo non corregge un'istruzione imprecisa: la ripete."),
        ("Ogni tre anni, tutto da capo.", "Sito nuovo, agenzia nuova, campagna nuova. Per qualche mese va meglio, poi si torna lì.", "Intervieni sull'ultimo passaggio, da anni."),
        ("Un sito che elenca servizi.", "«Hotel 4 stelle. SPA. Ristorante. Relax.» Con un altro logo varrebbe per cento hotel.", "L'agenzia ha scritto ciò che ha ricevuto."),
        ("Testi ben scritti, ma uguali.", "Descrizioni e post generati con l'AI. Tutti scrivono meglio, tutti dicono le stesse cose.", "Scrivere bene oggi è il minimo. Non distingue: livella."),
        ("Ogni campagna riparte da zero.", "Nuovo messaggio, nuova idea, nuovo tono. Ogni volta vincono le opinioni.", "Con un'identità definita, le scelte discendono dal posizionamento."),
    ],
    sig_tail="Non ti serve una quarta agenzia. Ti servono istruzioni chiare: si chiamano posizionamento.",
    br_h2="Il risultato dell'agenzia è un segnale. <em>La causa è nel brief.</em>",
    br_lead="Le agenzie lavorano su promessa e prenotazione. Il primo passaggio spetta a te: nessuno può definirlo da fuori senza partire da te.",
    br_here=2,
    br_rings=["Chi sei, e per quale ospite. Il brief che manca.", "Cosa dici all'ospite. Dove lavorano le agenzie.", "Cosa incassi. Uguale con tutte e tre."],
    br_prose='''        <p>Le istruzioni si possono scrivere. Si chiamano posizionamento.</p>
        <p>Con quelle in mano, la prossima agenzia, o una delle precedenti, lavora in modo diverso.</p>
        <p><strong>Non serve cambiare chi esegue. Serve dargli cosa eseguire.</strong></p>''',
    br_quote="Quando cambia chi esegue e il risultato resta lo stesso, la causa è nelle istruzioni.",
    offer_lead="L'analisi è il brief che serve a un'agenzia. Puoi girarla alla tua il giorno dopo la consegna.",
    cand_lead="Un minuto. Guardo il tuo hotel come farebbe un'agenzia attenta: con le domande che servono a scrivere il brief.",
    faq=[
        ("Devo cambiare agenzia?", "Non per forza. Devi darle istruzioni chiare. Il posizionamento è il brief che le serve, e molte agenzie, con quello in mano, lavorano molto meglio."),
        ("Come capisco se l'agenzia è davvero inadeguata?", "Da un segnale: non fa domande. Se le fa e mancano le risposte, cambiarla non serve. Servono le risposte."),
        ("Chi mette in pratica?", "La tua squadra o i tuoi fornitori, con una direzione chiara. Io do il posizionamento, i testi chiave e gli script; loro eseguono."),
        ("Devo rifare il sito?", "Quasi mai da zero. Va rivisto ciò che dice: costa meno e conta di più."),
    ],
)
