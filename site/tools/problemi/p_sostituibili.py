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
    title="Come differenziare un hotel che sembra uguale agli altri",
    og_title="Il tuo hotel è bellissimo. Peccato che lo siano tutti.",
    desc="Il tuo hotel è bellissimo. Peccato che lo siano tutti. Fai il test del logo coperto sulla tua homepage, riconosci i dieci segnali dell'hotel sostituibile e trova il motivo per cui l'ospite sceglie te.",
    eyebrow="Sintomo 03 · Bello e sostituibile",
    h1="Gli ospiti ci adorano. Ma non sanno spiegare perché.",
    pull='Il tuo hotel è bellissimo. <span class="hl or in">Peccato che lo siano tutti.</span>',
    lead="Il design si compra. Il fotografo si compra. Il rebranding si compra. E infatti li hanno comprati tutti. Quello che non si compra è un motivo per scegliere te, e non l'altro bellissimo.",
    cta2="Fai il test del logo coperto ↓",
    memo=memo("Homepage · logo coperto", "████████",
              [("«Eleganza. Charme. Esperienza autentica.»", "", ""),
               ("Funziona per il tuo hotel?", "✓ sì", "ok"),
               ("Per quello a venti minuti?", "✓ sì", "ok"),
               ("Per quello su Condé Nast il mese scorso?", "✓ sì", "ok")],
              "Posizionamento", "non pervenuto",
              "Non hai un posizionamento. Hai un arredamento."),
    ag_h2="Facciamo un test. <em>Copri il logo.</em>",
    ag_lead="Prendi la tua homepage. Copri il logo. Leggi il testo. Potrebbe essere il tuo hotel. O quello a venti minuti da te.",
    ag_prose='''        <p>«Ma Francesco, il mio hotel è curato. Abbiamo fatto il rebranding due anni fa.»</p>
        <p>Lo so. Si vede. Il logo è giusto. Le foto sono giuste. I materiali sono giusti.</p>
        <p>È tutto giusto. <strong>Ed è questo il problema.</strong></p>
        <p>Il «giusto», oggi, è lo standard. Ogni boutique hotel ha il logo giusto. Ogni resort ha le foto giuste.</p>
        <p>Il problema non è come appari. È che non sai dire perché esisti.</p>''',
    tool='''      <div class="tool rv d1">
        <div class="tool-head"><span>Il test del logo coperto</span><em>Usa la tua homepage</em></div>
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
            <span class="lab" id="sQ">Regge per tutti e tre?</span>
            <div class="tgl" role="group" aria-labelledby="sQ">
              <button type="button" data-v="si" aria-pressed="false">Sì, per tutti</button>
              <button type="button" data-v="no" aria-pressed="false">No, solo per me</button>
            </div>
          </div>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Parole da vocabolario condiviso</span>
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
    if(choice==='si') sub.innerHTML='Allora non hai un posizionamento. Hai un arredamento. Non è un insulto: è il punto di partenza di quasi tutti.';
    else if(choice==='no') sub.innerHTML=r.n>2?'Sicuro? Ci sono '+w+' che potrebbe usare qualunque hotel. Rileggila come se fossi l’ospite, non il proprietario.':'Bene. Ora la prova del nove: cerca nelle recensioni chi scrive «l’unico posto dove ho trovato…». Se c’è, sei sulla strada giusta.';
    else sub.innerHTML=r.n?'Ci sono '+w+' che potrebbe usare qualunque hotel. Ora rispondi alla domanda qui sopra.':'Nessuna parola da catalogo. Buon segno. Ora rispondi alla domanda qui sopra.';
  }
  bs.forEach(function(b){ b.addEventListener('click',function(){
    choice=b.dataset.v; bs.forEach(function(x){ x.setAttribute('aria-pressed',x===b); }); upd();
  }); });
  ta.addEventListener('input',upd); upd();
})();''',
    sig_h2="I dieci segnali che sei <em>bello e sostituibile.</em>",
    sig_lead="Spunta quelli in cui ti riconosci. Non è un problema di gusto. È un problema di posizione.",
    signals=[
        ("Il test del logo coperto.", "Copri il logo sulla homepage. Il testo funziona per altri cento hotel: «Eleganza. Charme. Esperienza autentica.»", "Non è un'identità. È un vocabolario condiviso con i tuoi concorrenti."),
        ("Recensioni splendide. E intercambiabili.", "«Struttura meravigliosa. Personale impeccabile. Torneremo.» Lo scrivono anche agli altri. Cerca quella che dice: «L'unico posto dove ho trovato X.»", "Non c'è? Allora X non c'è."),
        ("Il tuo design ha 18 mesi di vantaggio. Forse.", "Hai investito nel restyling. Il tuo vicino sta ristrutturando adesso. Con lo stesso architetto di tendenza.", "Il vantaggio estetico è un affitto: scade. L'identità è una proprietà: resta."),
        ("«Boutique hotel» non dice più niente.", "Vent'anni fa era una posizione. Oggi è una categoria. Affollata.", "Dire «siamo un boutique hotel» è come dire «siamo un hotel». Con meno camere."),
        ("Vendi la destinazione, non te stesso.", "Il tuo sito parla della Sardegna. Della Toscana. Del lago. Splendido.", "Stai facendo marketing gratis a tutti i concorrenti della tua zona."),
        ("Il diretto è fermo. Nonostante tutto.", "Sito nuovo, booking engine nuovo, campagne attive. Ma nessuno cerca te per nome: cercano «boutique hotel + zona».", "E lì sei in lista. Con tutti gli altri belli."),
        ("Trenta secondi muti.", "L'ospite chiede: «Cosa vi rende speciali?». Tu rispondi: «Ehm. Cura. Qualità. Attenzione.»", "Se non sai dirlo in trenta secondi, non lo sai."),
        ("Lo staff accetta tutti.", "Purché paghino. Poi vi lamentate: «Gli ospiti non capiscono cosa offriamo.»", "Se accetti tutti, non offri niente di specifico."),
        ("Senza di te, l'hotel perde la voce.", "L'identità sta nella tua testa. Non nei documenti, non nello staff, non nel sito. Se ti fermi un mese, l'hotel torna generico.", "Per un gestore è un problema. Per un proprietario è un rischio patrimoniale."),
        ("Ogni scelta è un dibattito.", "Nuovo ristorante: che concept? Nuova SPA: che filosofia? Nuova campagna: che messaggio? Ogni volta si riparte da zero.", "Chi ha un'identità non dibatte. Deduce."),
    ],
    sig_tail="Non ti serve un altro restyling. Ti serve sapere chi sei. Il bello senza posizione è un costo che si ammortizza.",
    br_h2="Bello è il sintomo. <em>Sostituibile è la malattia.</em>",
    br_lead="Il rebranding decide come appari. Il posizionamento decide perché esisti.",
    br_here=2,
    br_rings=["Quello che sai di essere. Qui è vuoto.", "Quello che dici. Logo, foto, materiali: tutto giusto.", "Quello che incassi. Come gli altri belli."],
    br_prose='''        <p>Logo, foto, sito, materiali: hai lavorato bene sul secondo anello. Ma il primo è vuoto.</p>
        <p>Un rebranding senza posizionamento è un vestito su misura senza nessuno dentro.</p>
        <p><strong>Il design si compra. Il motivo no: va trovato.</strong> E di solito è già scritto, nelle parole dei tuoi ospiti.</p>''',
    br_quote="Il sito è la pelle. Le recensioni sono l'osso.",
    proof_k="Recensioni Booking",
    proof_big="<s>8,6</s> 9",
    offer_lead="L'analisi parte da quello che gli ospiti scrivono di te, non da quello che pensi tu. Lì dentro c'è già il motivo.",
    cand_lead="Sessanta secondi. Guardo la tua homepage, le tue recensioni e i tuoi concorrenti belli. Poi ti dico cosa ti rende diverso, se c'è.",
    faq=[
        ("Ho già fatto un rebranding. Non è la stessa cosa?", "No. Il rebranding decide come appari. Il posizionamento decide perché esisti. Il primo senza il secondo è un vestito su misura senza nessuno dentro."),
        ("E se il mio hotel fosse già posizionato?", "Forse lo è. Il test è qui sopra: copri il logo. Se la homepage regge solo per te, sei posizionato. Se regge per altri cento, no. L'analisi te lo dice senza sconti."),
        ("Funziona anche per un gruppo con più strutture?", "Sì, ed è dove rende di più: ogni struttura distinta dalle altre e dal mercato. Si parte comunque dall'analisi di una."),
        ("Serve rifare il sito?", "Quasi mai da zero. Serve rifare quello che dice. Che costa meno e conta di più."),
    ],
)
