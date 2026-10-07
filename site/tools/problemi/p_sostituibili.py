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
    title="Differenziare un hotel che somiglia agli altri",
    og_title="Gli ospiti ti apprezzano, ma non sanno spiegare perché.",
    desc="Molti hotel curati si somigliano. Fai il test del logo coperto sulla tua homepage e scopri il motivo per cui l'ospite sceglie te.",
    eyebrow="Segnale 03 · Riconoscibilità",
    h1="Rendere il tuo hotel riconoscibile.",
    pull='Gli ospiti ti apprezzano, ma non sanno spiegare perché. <span class="hl or in">Spesso non lo spiega nemmeno il sito.</span>',
    lead="Design, foto e rebranding si comprano, e infatti li hanno in tanti. Non si compra un motivo per scegliere te invece di un altro hotel curato.",
    cta2="Fai il test del logo coperto ↓",
    memo=memo("Homepage · logo coperto", "████████",
              [("«Eleganza. Charme. Esperienza autentica.»", "", ""),
               ("Vale per il tuo hotel?", "✓ sì", "ok"),
               ("Per quello a venti minuti?", "✓ sì", "ok"),
               ("Per quello su Condé Nast il mese scorso?", "✓ sì", "ok")],
              "Posizionamento", "non riconoscibile",
              "Le parole sono corrette. Ma valgono per tutte."),
    ag_h2="Un test semplice. <em>Copri il logo.</em>",
    ag_lead="Apri la tua homepage, copri il logo e leggi il testo. Descrive il tuo hotel, o anche quello a venti minuti?",
    ag_prose='''        <p>Logo corretto. Foto corrette. Materiali corretti.</p>
        <p>È tutto corretto. <strong>Ed è proprio questo il punto.</strong></p>
        <p>Oggi il corretto è lo standard: ogni boutique hotel ha un bel logo, ogni resort ha belle foto.</p>
        <p>La differenza non sta in come il tuo hotel appare. Sta nel motivo per cui esiste, detto in modo che l'ospite lo riconosca.</p>''',
    tool='''      <div class="tool rv d1">
        <div class="tool-head"><span>Il test del logo coperto</span><em>Con la tua homepage</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="sTxt">Incolla la prima frase della tua homepage</label>
            <textarea id="sTxt" spellcheck="false">Un'oasi di eleganza e charme a pochi passi dal centro. Un'esperienza autentica e indimenticabile, curata in ogni dettaglio.</textarea>
          </div>
          <div class="logo3" id="sCards" aria-live="polite">
            <div class="lg"><span class="lg-n">Il tuo hotel</span><span class="lg-l" aria-hidden="true"></span><p class="lg-t"></p></div>
            <div class="lg"><span class="lg-n">Quello a venti minuti</span><span class="lg-l" aria-hidden="true"></span><p class="lg-t"></p></div>
            <div class="lg"><span class="lg-n">Quello su Condé Nast</span><span class="lg-l" aria-hidden="true"></span><p class="lg-t"></p></div>
          </div>
          <div class="tool-row">
            <span class="lab" id="sQ">Vale per tutti e tre?</span>
            <div class="tgl" role="group" aria-labelledby="sQ">
              <button type="button" data-v="si" aria-pressed="false">Sì, per tutti</button>
              <button type="button" data-v="no" aria-pressed="false">No, solo per il mio</button>
            </div>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Parole di uso comune nel settore</span>
          <b class="tool-big" id="sOut">9</b>
          <p id="sSub">Rispondi alla domanda qui sopra.</p>
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
    if(choice==='si') sub.innerHTML='Allora il testo descrive la categoria, non il tuo hotel. Succede a molti, e si corregge.';
    else if(choice==='no') sub.innerHTML=r.n>2?'Ci sono però '+w+' che potrebbe usare qualsiasi hotel. Rileggi la frase con gli occhi di un ospite che non ti conosce.':'Bene. Ora cerca nelle tue recensioni chi scrive «l’unico posto dove ho trovato…». Se c’è, è una traccia del tuo posizionamento.';
    else sub.innerHTML=r.n?'Ci sono '+w+' che potrebbe usare qualsiasi hotel. Ora rispondi alla domanda qui sopra.':'Nessuna parola di uso comune. Buon segno. Ora rispondi alla domanda qui sopra.';
  }
  bs.forEach(function(b){ b.addEventListener('click',function(){
    choice=b.dataset.v; bs.forEach(function(x){ x.setAttribute('aria-pressed',x===b); }); upd();
  }); });
  ta.addEventListener('input',upd); upd();
})();''',
    sig_h2="Dieci segnali di un hotel <em>curato ma sostituibile.</em>",
    sig_lead="Seleziona quelli che riconosci nel tuo hotel. Non è una questione di gusto, ma di posizione.",
    signals=[
        ("Il test del logo coperto.", "Senza logo, il testo della tua homepage vale per cento hotel: «Eleganza. Charme. Esperienza autentica.»", "È il vocabolario dei tuoi concorrenti, non un'identità."),
        ("Recensioni ottime, ma intercambiabili.", "«Struttura meravigliosa. Personale impeccabile. Torneremo.» Le stesse parole sono nelle recensioni dei concorrenti. Manca: «L'unico posto dove ho trovato X.»", "Se nessuno lo scrive, X non è ancora percepito."),
        ("Il vantaggio estetico è temporaneo.", "Il tuo restyling è recente. L'hotel vicino sta ristrutturando ora, spesso con lo stesso studio.", "Il vantaggio estetico scade. L'identità resta."),
        ("«Boutique hotel» non distingue più.", "Vent'anni fa era una posizione. Oggi è una categoria, e affollata.", "Dire «boutique hotel» oggi equivale quasi a dire «hotel»."),
        ("Racconti la destinazione, non il tuo hotel.", "Il sito parla della Sardegna, della Toscana, del lago.", "Così promuovi anche tutti i concorrenti della zona."),
        ("Il diretto non cresce.", "Sito nuovo, booking engine nuovo, campagne attive. Ma l'ospite cerca «boutique hotel + zona», non il tuo nome.", "E in quella ricerca sei uno tra molti."),
        ("La risposta a «perché tu?».", "Ti chiedono cosa ti distingue. Rispondi «cura, qualità, attenzione».", "Se la risposta non sta in trenta secondi, non è ancora chiara."),
        ("Nessun filtro sugli ospiti.", "Accetti tutte le richieste. Poi ti accorgi che gli ospiti non capiscono cosa offri.", "Una proposta per tutti non è specifica per nessuno."),
        ("L'identità dipende da una persona.", "Sta nella tua testa: non nei documenti, non nella squadra, non nel sito. Se manchi un mese, la comunicazione torna generica.", "Per la gestione è un limite. Per la proprietà è un rischio patrimoniale."),
        ("Ogni scelta riapre la discussione.", "Nuovo ristorante: quale concept? Nuova SPA: quale filosofia? Ogni volta si riparte da zero.", "Con un'identità definita, le scelte discendono dal posizionamento."),
    ],
    sig_tail="Non ti serve un altro restyling. Ti serve decidere chi sei e per quale ospite. Un’estetica si ammortizza; un’identità resta.",
    br_h2="Curata ma sostituibile. <em>La causa è nel primo passaggio.</em>",
    br_lead="Il rebranding decide come il tuo hotel appare. Il posizionamento decide perché l'ospite lo sceglie.",
    br_here=2,
    br_rings=["Chi sei, e per quale ospite. Qui manca una risposta.", "Cosa dici all'ospite. Logo, foto, materiali: tutto curato.", "Cosa incassi. Come gli altri hotel curati."],
    br_prose='''        <p>Su logo, foto, sito e materiali hai lavorato bene: è il secondo passaggio. Il primo è rimasto senza risposta.</p>
        <p>Un rebranding senza posizionamento dà forma a qualcosa che non è ancora deciso.</p>
        <p><strong>Il design si compra. Il motivo va trovato.</strong> Di solito è già scritto, nelle parole dei tuoi ospiti.</p>''',
    br_quote="Le unicità di un hotel sono già scritte: nelle recensioni degli ospiti.",
    proof_k="Recensioni Booking",
    proof_big="<s>8,6</s> 9",
    offer_lead="L'analisi parte da ciò che gli ospiti scrivono del tuo hotel, non da ciò che ne pensi tu. Il motivo, spesso, è già lì.",
    cand_lead="Un minuto. Guardo la tua homepage, le recensioni e i concorrenti. Poi ti dico cosa ti distingue, se c'è già.",
    faq=[
        ("Ho già fatto un rebranding. Non è la stessa cosa?", "No. Il rebranding decide come il tuo hotel appare. Il posizionamento decide perché l'ospite lo sceglie. Il primo senza il secondo è una forma senza contenuto."),
        ("E se il mio hotel fosse già posizionato?", "Può darsi. Fai il test qui sopra: copri il logo. Se la homepage vale solo per te, la posizione c'è. Se vale per cento hotel, no. L'analisi lo verifica punto per punto."),
        ("Funziona anche per un gruppo con più hotel?", "Sì, ed è dove rende di più: ogni hotel distinto dagli altri del gruppo e dal mercato. Si parte comunque da uno."),
        ("Devo rifare il sito?", "Quasi mai da zero. Va rivisto ciò che dice: costa meno e conta di più."),
    ],
)
