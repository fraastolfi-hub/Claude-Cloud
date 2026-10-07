from common import memo
from p_sostituibili import WORDS_JS

P = dict(
    slug="agenzie",
    title="Agenzie marketing per hotel: perché cambiarle non basta",
    og_title="Agenzie diverse, risultati simili. La causa è nelle istruzioni.",
    desc="Più agenzie in pochi anni e risultati simili? Quando cambia chi esegue e il risultato resta lo stesso, la causa è nelle istruzioni. Il test del vostro brief e dieci segnali da verificare.",
    eyebrow="Segnale 04 · Comunicazione",
    h1="Dare alle agenzie un brief chiaro.",
    pull='Agenzie diverse, risultati simili. <span class="hl or in">Quando cambia chi esegue e il risultato no, la causa è nelle istruzioni.</span>',
    lead="Non significa che le agenzie fossero tutte inadeguate. Significa che ognuna ha ricevuto lo stesso brief, e ha prodotto ciò che quel brief permetteva.",
    cta2="Il test del brief ↓",
    memo=memo("Fornitori di comunicazione", "5 anni",
              [("Agenzia 1: obiettivi ambiziosi, risultati modesti.", "✕", "bad"),
               ("Agenzia 2: «Serve tempo.» Il tempo è passato.", "✕", "bad"),
               ("Agenzia 3: contenuti curati, poche prenotazioni.", "✕", "bad")],
              "Prenotazioni in più", "invariate",
              "Tre squadre, tre metodi. Lo stesso risultato."),
    ag_h2="Se tre cuochi sbagliano lo stesso piatto, <em>va rivista la ricetta.</em>",
    ag_lead="Un principio che vale in cucina, in sala e nel marketing. Un cuoco che sbaglia un piatto può essere poco preparato. Se lo sbagliano in tre, il problema è la ricetta.",
    ag_prose='''        <p>Nel marketing la ricetta si chiama brief. Spesso dice così:</p>
        <p>«Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità.»</p>
        <p>Con queste istruzioni anche un'ottima agenzia produce charme, eleganza, esperienza autentica. Le stesse parole che usa per le altre strutture che segue.</p>
        <p>Per onestà: a volte l'agenzia è davvero inadeguata. Si riconosce da un segnale preciso: <strong>non fa domande.</strong></p>
        <p>Se invece le domande arrivavano e mancavano le risposte, cambiare agenzia non basta.</p>''',
    tool='''      <div class="tool rv d1">
        <div class="tool-head"><span>Il test del brief</span><em>Con il vostro brief</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="aTxt">Scrivete cosa avete chiesto all'ultima agenzia</label>
            <textarea id="aTxt" spellcheck="false">Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità e sull'esperienza autentica.</textarea>
          </div>
          <p class="brief-prev" id="aPrev" aria-hidden="true"></p>
          <div class="tool-row">
            <span class="lab">Il vostro brief risponde a queste tre domande?</span>
            <div class="bq" role="group" aria-labelledby="q1"><span id="q1">Per quali ospiti siamo, e per quali no?</span><div class="tgl"><button type="button" data-q="0" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="0" data-v="0" aria-pressed="false">No</button></div></div>
            <div class="bq" role="group" aria-labelledby="q2"><span id="q2">Con chi competiamo davvero, anche fuori dal settore alberghiero?</span><div class="tgl"><button type="button" data-q="1" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="1" data-v="0" aria-pressed="false">No</button></div></div>
            <div class="bq" role="group" aria-labelledby="q3"><span id="q3">Perché l'ospite sceglie noi, in una frase verificabile?</span><div class="tgl"><button type="button" data-q="2" data-v="1" aria-pressed="false">Sì</button><button type="button" data-q="2" data-v="0" aria-pressed="false">No</button></div></div>
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
    if(y===3 && r.n<=1){ out.textContent='Brief completo'; sub.innerHTML='Con queste istruzioni un’agenzia può lavorare bene. Se i risultati non arrivano comunque, la causa può essere davvero l’agenzia.'; }
    else if(y>0){ out.textContent='Brief incompleto'; sub.innerHTML='Manca '+(3-y===1?'una risposta':(3-y)+' risposte')+'. Dove mancano risposte, le agenzie tendono a colmare il vuoto con charme ed eleganza.'+gen; }
    else { out.textContent='Brief generico'; sub.innerHTML=(done?'Nessuna delle tre risposte. ':'')+'Con queste istruzioni anche un’ottima agenzia produce charme, eleganza, esperienza autentica.'+gen; }
  }
  bs.forEach(function(b){ b.addEventListener('click',function(){
    var q=+b.dataset.q; ans[q]=+b.dataset.v;
    bs.forEach(function(x){ if(+x.dataset.q===q) x.setAttribute('aria-pressed',x===b); }); upd();
  }); });
  ta.addEventListener('input',upd); upd();
})();''',
    sig_h2="Dieci segnali che la causa <em>non è l'agenzia.</em>",
    sig_lead="Selezionate quelli che riconoscete nella vostra struttura. Se sono molti, un'altra agenzia difficilmente cambierà il risultato.",
    signals=[
        ("Il brief sta in tre righe.", "«Fateci conoscere. Valorizzate la struttura. Puntiamo sulla qualità.»", "Con queste istruzioni, qualsiasi agenzia produce la stessa cosa."),
        ("La risposta a «perché voi?».", "L'agenzia chiede: «Cosa vi distingue?». La risposta è «cura, qualità, attenzione», e l'agenzia scrive esattamente questo.", "Se la risposta non è chiara alla struttura, non può esserlo all'agenzia."),
        ("Nessuna domanda iniziale.", "L'agenzia è partita dal piano editoriale, non dall'identità della struttura. E nessuno l'ha notato.", "Questo è un limite dell'agenzia. Le altre, forse, aspettavano risposte."),
        ("Contenuti curati, poche prenotazioni.", "Il profilo è ordinato, i contenuti sono di qualità. Le prenotazioni arrivano da altri canali.", "La cura formale non sostituisce un messaggio."),
        ("Campagne a basso rendimento.", "Duemila euro di annunci, cinquanta clic, due prenotazioni. Clicca chiunque; prenota chi ha capito cosa offrite.", "La pubblicità amplifica un messaggio. Se il messaggio è generico, amplifica quello."),
        ("«Serve tempo.»", "Sei mesi di contratto, poi altri sei. Il tempo passa, il risultato resta.", "Il tempo non corregge un'istruzione imprecisa: la ripete."),
        ("Ogni tre anni, tutto da capo.", "Sito nuovo, agenzia nuova, campagna nuova. Per qualche mese il segnale si attenua, poi ritorna.", "Si interviene sull'ultimo passaggio, da anni."),
        ("Un sito che elenca servizi.", "«Hotel 4 stelle. SPA. Ristorante. Relax.» Con un altro logo varrebbe per cento strutture.", "L'agenzia ha scritto ciò che ha ricevuto."),
        ("Testi ben scritti, ma uguali.", "Descrizioni e post generati con l'AI. Tutti scrivono meglio, tutti dicono le stesse cose.", "Scrivere bene oggi è il minimo. Non distingue: livella."),
        ("Ogni campagna riparte da zero.", "Nuovo messaggio, nuova idea, nuovo tono. Ogni volta prevalgono le opinioni.", "Con un'identità definita, le scelte discendono dal posizionamento."),
    ],
    sig_tail="Non serve una quarta agenzia. Servono istruzioni chiare: si chiamano posizionamento.",
    br_h2="Il risultato dell'agenzia è un segnale. <em>La causa è nel brief.</em>",
    br_lead="Le agenzie lavorano su promessa e prenotazione. Il primo passaggio spetta alla struttura: nessuno può definirlo dall'esterno senza partire da voi.",
    br_here=2,
    br_rings=["Chi siete, e per quale ospite. Il brief che manca.", "Cosa dite all'ospite. Dove lavorano le agenzie.", "Cosa incassate. Uguale con tutte e tre."],
    br_prose='''        <p>Le istruzioni si possono scrivere. Si chiamano posizionamento.</p>
        <p>Con quelle in mano, l'agenzia successiva, o una di quelle precedenti, lavora in modo diverso.</p>
        <p><strong>Non serve cambiare chi esegue. Serve dargli cosa eseguire.</strong></p>''',
    br_quote="Quando cambia chi esegue e il risultato resta lo stesso, la causa è nelle istruzioni.",
    offer_lead="L'analisi è il brief di cui un'agenzia ha bisogno. Potete condividerla con la vostra il giorno dopo la consegna.",
    cand_lead="Un minuto. Analizzo la struttura come farebbe un'agenzia attenta: con le domande che servono a scrivere il brief.",
    faq=[
        ("Dobbiamo cambiare agenzia?", "Non necessariamente. Serve darle istruzioni chiare. Il posizionamento è il brief di cui un'agenzia ha bisogno, e molte agenzie, con quello in mano, lavorano molto meglio."),
        ("Come si capisce se l'agenzia è davvero inadeguata?", "Da un segnale: non fa domande. Se le fa e mancano le risposte, cambiarla non serve. Servono le risposte."),
        ("Chi si occupa dell'attuazione?", "La vostra squadra o i vostri fornitori, con una direzione chiara. Io fornisco il posizionamento, i testi chiave e gli script; loro eseguono."),
        ("Serve rifare il sito?", "Quasi mai da zero. Serve rivedere ciò che dice: costa meno e conta di più."),
    ],
)
