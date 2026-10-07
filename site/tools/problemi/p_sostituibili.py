from common import memo

WORDS_JS = r'''
  /* parole da vocabolario condiviso: radici che compaiono in quasi tutti i siti di hotel */
  var STEMS=['eleganz','elegant','charme','autentic','esperienz','indimenticabil','unic','eccellen','accogl','relax','luss','raffinat','curat','qualità','qualita','cuore','oasi','immers','comfort','confortevol','emozion','magic','perfett','ideal','tranquill','esclusiv','ospitalità','attenzion','dettagl','valorizz','conoscere','stile','boutique','meraviglios','impeccabil','incantevol','suggestiv','prestigios','benvenut','straordinar','speciale','cornice','passi','incanto','sogno'];
  function esc(s){ return s.replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c];}); }
  function mark(txt){
    var n=0, html=esc(txt).replace(/[A-Za-zÀ-ÖØ-öø-ÿ]+/g,function(w){
      var l=w.toLowerCase();
      for(var i=0;i<STEMS.length;i++){ if(l.indexOf(STEMS[i])===0){ n++; return '<mark class="gen">'+w+'</mark>'; } }
      return w;
    });
    return {html:html,n:n};
  }'''

P = dict(
    slug="sostituibili",
    title="Differenziare una struttura che somiglia alle altre",
    og_title="Gli ospiti vi apprezzano, ma non sanno spiegare perché.",
    desc="Molte strutture curate si somigliano. Il test del logo coperto sulla vostra homepage, dieci segnali di una struttura sostituibile e il motivo per cui l'ospite sceglie voi.",
    eyebrow="Segnale 03 · Riconoscibilità",
    h1="Rendere la struttura riconoscibile.",
    pull='Gli ospiti vi apprezzano, ma non sanno spiegare perché. <span class="hl or in">Spesso non lo spiega nemmeno il sito.</span>',
    lead="Design, fotografia e rebranding si acquistano, e infatti molte strutture li hanno. Non si acquista un motivo per scegliere voi invece di un'altra struttura curata.",
    cta2="Il test del logo coperto ↓",
    memo=memo("Homepage · logo coperto", "████████",
              [("«Eleganza. Charme. Esperienza autentica.»", "", ""),
               ("Vale per la vostra struttura?", "✓ sì", "ok"),
               ("Per quella a venti minuti?", "✓ sì", "ok"),
               ("Per quella su Condé Nast il mese scorso?", "✓ sì", "ok")],
              "Posizionamento", "non riconoscibile",
              "Le parole sono corrette. Ma valgono per tutte."),
    ag_h2="Un test semplice. <em>Coprite il logo.</em>",
    ag_lead="Aprite la vostra homepage, coprite il logo e leggete il testo. Descrive la vostra struttura, o anche quella a venti minuti?",
    ag_prose='''        <p>Molte strutture hanno fatto un rebranding negli ultimi anni, e si vede.</p>
        <p>Il logo è corretto. Le fotografie sono corrette. I materiali sono corretti.</p>
        <p>È tutto corretto. <strong>Ed è proprio questo il punto.</strong></p>
        <p>Oggi il «corretto» è lo standard. Ogni boutique hotel ha un logo curato, ogni resort ha belle fotografie.</p>
        <p>La differenza non sta in come la struttura appare. Sta nel motivo per cui esiste, detto in modo che l'ospite lo riconosca.</p>''',
    tool='''      <div class="tool rv d1">
        <div class="tool-head"><span>Il test del logo coperto</span><em>Con la vostra homepage</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="sTxt">Incollate la prima frase della vostra homepage</label>
            <textarea id="sTxt" spellcheck="false">Un'oasi di eleganza e charme a pochi passi dal centro. Un'esperienza autentica e indimenticabile, curata in ogni dettaglio.</textarea>
          </div>
          <div class="logo3" id="sCards" aria-live="polite">
            <div class="lg"><span class="lg-n">La vostra struttura</span><span class="lg-l" aria-hidden="true"></span><p class="lg-t"></p></div>
            <div class="lg"><span class="lg-n">Quella a venti minuti</span><span class="lg-l" aria-hidden="true"></span><p class="lg-t"></p></div>
            <div class="lg"><span class="lg-n">Quella su Condé Nast</span><span class="lg-l" aria-hidden="true"></span><p class="lg-t"></p></div>
          </div>
          <div class="tool-row">
            <span class="lab" id="sQ">Vale per tutte e tre?</span>
            <div class="tgl" role="group" aria-labelledby="sQ">
              <button type="button" data-v="si" aria-pressed="false">Sì, per tutte</button>
              <button type="button" data-v="no" aria-pressed="false">No, solo per noi</button>
            </div>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Parole di uso comune nel settore</span>
          <b class="tool-big" id="sOut">9</b>
          <p id="sSub">Rispondete alla domanda qui sopra.</p>
        </div>
      </div>''',
    css='''.logo3{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.lg{background:var(--white);border-radius:var(--r-sm);padding:14px;display:grid;gap:10px;align-content:start;min-width:0}
.lg-n{font:500 12.5px/1.25 var(--text);color:var(--muted)}
.lg-l{height:12px;border-radius:6px;background:var(--ink);width:70%}
.lg:nth-child(2) .lg-l{width:50%}.lg:nth-child(3) .lg-l{width:85%}
.lg-t{font-size:14px;line-height:1.45;color:var(--ink-2);overflow-wrap:anywhere}
@media (max-width:560px){.logo3{grid-template-columns:1fr}}''',
    js='''/* test del logo coperto */
(function(){''' + WORDS_JS + '''
  var ta=document.getElementById('sTxt'), cards=[].slice.call(document.querySelectorAll('#sCards .lg-t'));
  var out=document.getElementById('sOut'), sub=document.getElementById('sSub'), choice=null;
  var bs=[].slice.call(document.querySelectorAll('.tgl button[data-v]'));
  function upd(){
    var t=ta.value.trim(), r=mark(t||'…');
    cards.forEach(function(c){ c.innerHTML=r.html; });
    out.textContent=t?r.n:'0';
    var w=r.n===1?'una parola':r.n+' parole';
    if(choice==='si') sub.innerHTML='Allora il testo descrive la categoria, non la struttura. È il punto di partenza di molte strutture, e si può correggere.';
    else if(choice==='no') sub.innerHTML=r.n>2?'Ci sono però '+w+' che potrebbe usare qualsiasi struttura. Provate a rileggere la frase con gli occhi di un ospite che non vi conosce.':'Bene. Una verifica ulteriore: cercate nelle recensioni chi scrive «l’unico posto dove ho trovato…». Se c’è, è una traccia del vostro posizionamento.';
    else sub.innerHTML=r.n?'Ci sono '+w+' che potrebbe usare qualsiasi struttura. Ora rispondete alla domanda qui sopra.':'Nessuna parola di uso comune. Buon segno. Ora rispondete alla domanda qui sopra.';
  }
  bs.forEach(function(b){ b.addEventListener('click',function(){
    choice=b.dataset.v; bs.forEach(function(x){ x.setAttribute('aria-pressed',x===b); }); upd();
  }); });
  ta.addEventListener('input',upd); upd();
})();''',
    sig_h2="Dieci segnali di una struttura <em>curata ma sostituibile.</em>",
    sig_lead="Selezionate quelli che riconoscete nella vostra struttura. Non è una questione di gusto, ma di posizione.",
    signals=[
        ("Il test del logo coperto.", "Coperto il logo, il testo della homepage vale per cento strutture: «Eleganza. Charme. Esperienza autentica.»", "È un vocabolario condiviso con i concorrenti, non un'identità."),
        ("Recensioni ottime, ma intercambiabili.", "«Struttura meravigliosa. Personale impeccabile. Torneremo.» Le stesse parole compaiono nelle recensioni dei concorrenti. Manca quella che dice: «L'unico posto dove ho trovato X.»", "Se nessuno lo scrive, X non è ancora percepito."),
        ("Il vantaggio estetico è temporaneo.", "Il restyling è recente. Una struttura vicina sta ristrutturando ora, spesso con lo stesso studio di architettura.", "Il vantaggio estetico scade. L'identità resta."),
        ("«Boutique hotel» non distingue più.", "Vent'anni fa era una posizione. Oggi è una categoria, e affollata.", "Dire «boutique hotel» oggi equivale quasi a dire «hotel»."),
        ("Si racconta la destinazione, non la struttura.", "Il sito parla della Sardegna, della Toscana, del lago.", "Così la comunicazione promuove anche tutti i concorrenti della zona."),
        ("Il diretto non cresce.", "Sito nuovo, booking engine nuovo, campagne attive. Ma l'ospite cerca «boutique hotel + zona», non il vostro nome.", "E in quella ricerca la struttura è una tra molte."),
        ("La risposta a «perché voi?».", "Alla domanda «Cosa vi distingue?» la risposta è «cura, qualità, attenzione».", "Se la risposta non sta in trenta secondi, non è ancora chiara."),
        ("Nessun filtro sugli ospiti.", "Si accettano tutte le richieste. Poi si nota che gli ospiti non colgono cosa offre la struttura.", "Una proposta per tutti non è specifica per nessuno."),
        ("L'identità dipende da una persona.", "Sta nella testa della proprietà o della direzione: non nei documenti, non nella squadra, non nel sito. Con un mese di assenza, la comunicazione torna generica.", "Per la gestione è un limite. Per la proprietà è un rischio patrimoniale."),
        ("Ogni scelta riapre la discussione.", "Nuovo ristorante: quale concept? Nuova SPA: quale filosofia? Nuova campagna: quale messaggio? Ogni volta si riparte da zero.", "Con un'identità definita, le scelte discendono dal posizionamento."),
    ],
    sig_tail="Non serve un altro restyling. Serve definire chi siete e per quale ospite. Un’estetica senza posizione si ammortizza; un’identità resta.",
    br_h2="Curata ma sostituibile. <em>La causa è nel primo passaggio.</em>",
    br_lead="Il rebranding decide come la struttura appare. Il posizionamento decide perché l'ospite la sceglie.",
    br_here=2,
    br_rings=["Chi siete, e per quale ospite. Qui manca una risposta.", "Cosa dite all'ospite. Logo, fotografie, materiali: tutto curato.", "Cosa incassate. Come le altre strutture curate."],
    br_prose='''        <p>Su logo, fotografie, sito e materiali avete lavorato bene: è il secondo passaggio. Ma il primo è rimasto senza risposta.</p>
        <p>Un rebranding senza posizionamento dà forma a qualcosa che non è ancora stato definito.</p>
        <p><strong>Il design si acquista. Il motivo va trovato.</strong> E di solito è già scritto, nelle parole dei vostri ospiti.</p>''',
    br_quote="Le unicità di una struttura sono già scritte: nelle recensioni degli ospiti.",
    proof_k="Recensioni Booking",
    proof_big="<s>8,6</s> 9",
    offer_lead="L'analisi parte da ciò che gli ospiti scrivono della struttura, non da ciò che ne pensa la proprietà. Il motivo, spesso, è già lì.",
    cand_lead="Un minuto. Analizzo la vostra homepage, le recensioni e le strutture concorrenti, poi vi indico cosa vi distingue, se c'è già.",
    faq=[
        ("Abbiamo già fatto un rebranding. Non è la stessa cosa?", "No. Il rebranding decide come la struttura appare. Il posizionamento decide perché l'ospite la sceglie. Il primo senza il secondo resta una forma senza contenuto."),
        ("E se la struttura fosse già posizionata?", "È possibile. Il test è qui sopra: coprite il logo. Se la homepage vale solo per voi, la posizione c'è. Se vale per cento strutture, no. L'analisi lo verifica punto per punto."),
        ("Funziona anche per un gruppo con più strutture?", "Sì, ed è dove rende di più: ogni struttura distinta dalle altre del gruppo e dal mercato. Si parte comunque dall'analisi di una."),
        ("Serve rifare il sito?", "Quasi mai da zero. Serve rivedere ciò che dice: costa meno e conta di più."),
    ],
)
