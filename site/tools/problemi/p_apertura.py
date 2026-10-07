from common import memo

DEC = [
    ("Quante camere, e di che tipo", 0),
    ("Quali servizi: ristorante, SPA, spazi comuni", 0),
    ("Distribuzione degli spazi e materiali", 1),
    ("Arredi, luci, perfino i piatti", 2),
    ("Nome e identità visiva", 2),
    ("Prezzo d'apertura e pacchetti", 3),
    ("Sito, foto e testi", 3),
    ("Cosa sa rispondere la reception a «perché voi?»", 3),
]
dec_html = "\n".join(
    f'            <li data-until="{u}"><span>{t}</span><b class="st">libera</b></li>' for t, u in DEC
)

P = dict(
    slug="apertura",
    title="Aprire un hotel: il posizionamento prima dell'apertura",
    og_title="Il posizionamento si decide prima dell'apertura.",
    desc="State aprendo una struttura? Il posizionamento si decide prima del cantiere: dopo l'apertura ogni correzione costa il triplo. L'esperienza di Francesco Astolfi nei suoi locali, e cosa decidere adesso.",
    eyebrow="Segnale 06 · Nuove aperture",
    h1="Aprire con un'identità chiara.",
    pull='Prima dell\'apertura il posizionamento <span class="hl or in">costa meno e conta di più.</span>',
    lead="Il cantiere procede, i render sono pronti, e la risposta a «perché voi?» spesso viene rimandata a dopo. Al mio primo ristorante l'ho rimandata anch'io.",
    cta2="Cosa potete ancora decidere ↓",
    memo=memo("Il giorno prima dell'apertura", "Ristorante n. 1",
              [("Le luci", "✓ giuste", "ok"),
               ("I tavoli", "✓ giusti", "ok"),
               ("I piatti, proprio la ceramica", "✓ scelti da me", "ok"),
               ("«Perché dovrei venire da voi?»", "?", "bad")],
              "La risposta", "da definire",
              "Soddisfazione, per dieci minuti. Poi una domanda precisa."),
    ag_h2="Un prodotto curato, da solo, <em>non spiega perché sceglierlo.</em>",
    ag_lead="Il giorno prima di aprire il mio primo ristorante ero in mezzo alla sala. Era tutto pronto.",
    ag_prose='''        <p>Avevo scelto personalmente anche i piatti. Non il menu: i piatti, la ceramica.</p>
        <p>Per dieci minuti ho provato soddisfazione. Poi mi sono posto una domanda precisa: se domani un cliente mi chiede «perché dovrei venire da voi?», cosa rispondo?</p>
        <p>Avevo investito tutto, risorse, tempo e firme, su come il locale appariva. Niente su cosa il locale era.</p>
        <p>Il primo anno ha funzionato per curiosità. Il secondo la curiosità è finita, ed è arrivata la domanda vera. L'ho pagata cara.</p>
        <p><strong>Una struttura non entra in difficoltà per le maniglie sbagliate. Ci entra quando nasce uguale alle altre.</strong> E chi nasce uguale ha una sola leva: il prezzo, dal primo giorno.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Cosa potete ancora decidere</span><em>Fase per fase</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="apF">A che punto siete? <output id="apFo" for="apF">Cantiere aperto</output></label>
            <input class="rng" type="range" id="apF" min="0" max="4" step="1" value="1" aria-valuetext="Cantiere aperto">
            <div class="phases" aria-hidden="true"><span>Progetto</span><span>Cantiere</span><span>Finiture</span><span>Pre-apertura</span><span>Aperto</span></div>
          </div>
          <ul class="dec" id="apList">
{dec_html}
          </ul>
        </div>
        <div class="tool-out" aria-live="polite">
          <span class="k">Decisioni ancora libere</span>
          <b class="tool-big" id="apOut">6 su 8</b>
          <p id="apSub">Le fondamenta sono decise. Tutto ciò che l'ospite vedrà, no.</p>
        </div>
        <p class="tool-note">«Libera» significa che si può decidere adesso, senza rifare nulla. Dopo si può ancora cambiare tutto, ma costa il triplo.</p>
      </div>''',
    css='''.phases{display:grid;grid-template-columns:repeat(5,1fr);font:500 12px/1.2 var(--text);color:var(--muted)}
.phases span{text-align:center;overflow-wrap:anywhere}
.phases span:first-child{text-align:left}.phases span:last-child{text-align:right}
.dec{list-style:none;background:var(--white);border-radius:var(--r-sm);padding:4px 16px}
.dec li{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:11px 0;border-bottom:1px solid var(--line);font-size:15.5px;line-height:1.35;transition:color .25s}
.dec li:last-child{border-bottom:0}
.dec .st{flex:none;font:500 12.5px/1 var(--text);border-radius:980px;padding:6px 10px;background:var(--mist);color:var(--ink);transition:background .25s,color .25s}
.dec li.gone{color:var(--muted)}
.dec li.gone span{text-decoration:line-through;text-decoration-color:var(--muted);text-decoration-thickness:1px}
.dec li.gone .st{background:transparent;color:var(--muted);box-shadow:inset 0 0 0 1px var(--line)}''',
    js='''/* cosa potete ancora decidere */
(function(){
  var r=document.getElementById('apF'), o=document.getElementById('apFo'), items=[].slice.call(document.querySelectorAll('#apList li'));
  var N=['Progetto','Cantiere aperto','Finiture e arredi','Pre-apertura','Aperto'];
  var T=['È il momento migliore: il posizionamento può ancora orientare dove e cosa costruire.',
         'Le fondamenta sono decise. Tutto ciò che l’ospite vedrà, no.',
         'State scegliendo finiture e arredi. Conviene avere chiaro prima il motivo per cui l’ospite vi sceglierà.',
         'Restano il prezzo e le parole: sono le prime cose che l’ospite vede.',
         'La struttura è aperta. Il posizionamento si può ancora definire, ma ogni decisione ora è una revisione, e costa il triplo.'];
  function upd(){
    var f=+r.value, free=0;
    items.forEach(function(li){ var ok=f<=+li.dataset.until; if(ok) free++; li.classList.toggle('gone',!ok); li.querySelector('.st').textContent=ok?'libera':'già decisa'; });
    o.textContent=N[f]; r.setAttribute('aria-valuetext',N[f]);
    document.getElementById('apOut').textContent=free+' su '+items.length;
    document.getElementById('apSub').textContent=T[f];
  }
  r.addEventListener('input',upd); upd();
})();''',
    sig_h2="Dieci segnali da verificare <em>prima dell'apertura.</em>",
    sig_lead="Selezionate quelli che riconoscete nel vostro progetto. Prima dell'apertura ognuno si corregge a costo contenuto. Dopo, no.",
    signals=[
        ("Le finiture prima del motivo.", "Luci, tavoli, ceramica, rubinetti: tutto deciso. La risposta a «perché voi?» no.", "Le finiture contano, ma vengono dopo la direzione."),
        ("«Il prodotto si presenterà da solo.»", "Lo pensavo anch'io, il giorno prima di aprire il mio primo ristorante.", "Un prodotto curato non spiega da solo perché sceglierlo."),
        ("«Ci penseremo dopo.»", "Il posizionamento è in fondo alla lista: dopo gli arredi, prima del sito.", "Il «dopo» ha una scadenza: l'apertura."),
        ("I render somigliano a quelli degli altri.", "Il design si acquista, anche quello degli studi più richiesti. E molti lo acquistano.", "Il vantaggio estetico è temporaneo."),
        ("Il concept è «boutique hotel».", "Vent'anni fa era una posizione. Oggi è una categoria, e affollata.", "Dire «boutique hotel» oggi equivale quasi a dire «hotel»."),
        ("Il progetto racconta il luogo, non la struttura.", "Il mare, il lago, le colline.", "Così la comunicazione promuove anche tutte le strutture della zona."),
        ("La tariffa si decide guardando i vicini.", "Un po' più in basso, per partire, con l'idea di alzarla in seguito.", "Chi nasce uguale ha una sola leva: il prezzo, dal primo giorno."),
        ("Il piano vendite si basa sulle OTA.", "Prima ancora di aprire, il canale principale è deciso, ed è di un altro.", "La dipendenza dalle OTA spesso si decide prima dell'apertura."),
        ("L'ospite ideale è «chi apprezza la qualità».", "Una definizione che vale per tutti, quindi per nessuno.", "Essere specifici significa scegliere. E scegliere significa escludere."),
        ("Ogni scelta del cantiere riapre la discussione.", "Quale ristorante, quale SPA, quale stile: ogni riunione riparte dai gusti personali.", "Con un'identità definita, le scelte discendono dal posizionamento."),
    ],
    sig_tail="Siete ancora in tempo. È l’unico momento in cui il posizionamento costa poco e orienta tutto il resto.",
    br_h2="Il cantiere è visibile. <em>Il posizionamento è la fondazione.</em>",
    br_lead="Prima la bussola, poi i muri. Siete ancora al primo passaggio: l'unico momento in cui costa poco.",
    br_here=1,
    br_rings=["Chi sarete, e per quale ospite. Siete ancora in tempo.", "Cosa direte all'ospite, e dove.", "Cosa incasserete. Nascendo uguali agli altri, a prezzo basso."],
    br_prose='''        <p>Prima delle fondamenta si decide dove costruire. Vale anche per l'identità.</p>
        <p>Il posizionamento prima dell'apertura è quello che rende di più: orienta camere, servizi, prezzo e parole prima che diventino definitivi.</p>
        <p><strong>Dopo, costa il triplo.</strong></p>''',
    br_quote="Prima la bussola. Poi i muri. L'ordine conta.",
    proof_extra='''    <article class="card y rv" style="margin-top:20px;box-shadow:none;border-radius:28px">
      <p class="kicker"><b>Caso</b> · Yume Ramen · 5 locali</p>
      <h3 style="margin:12px 0 8px">Una posizione scelta prima di aprire.</h3>
      <p>Un caso da imprenditore, non da consulente: cinque locali costruiti con capitale proprio, partendo da una posizione decisa prima della prima cucina. Da zero a 2,5 milioni di euro di fatturato. Per questo consiglio di decidere la posizione prima dell'apertura.</p>
    </article>''',
    offer_lead="Vale anche per le strutture non ancora aperte: è il momento in cui l'analisi rende di più.",
    cand_lead="Un minuto. Il sito non serve: indicate il nome del progetto e la città. I dettagli li approfondiamo dopo.",
    cand_extra='''      <p class="note-box" style="margin-top:22px">Le candidature sono aperte anche alle strutture non ancora aperte: il posizionamento prima dell'apertura è quello che rende di più.</p>''',
    faq=[
        ("Non abbiamo ancora un sito. Ha senso candidarsi?", "Sì, è il momento migliore. Prima delle fondamenta si decide dove costruire. Vale anche per l'identità."),
        ("Il concept l'ha già definito l'architetto.", "L'architetto decide come la struttura appare. Il posizionamento decide perché l'ospite la sceglie. Se il motivo arriva prima, il progetto ne tiene conto. Se arriva dopo, si rifà."),
        ("Non è troppo presto?", "No. È tardi il giorno dopo l'apertura: da lì ogni correzione costa il triplo."),
        ("Vale anche per una struttura piccola?", "Sì, spesso di più: una struttura piccola può scegliere una nicchia precisa, una grande deve conciliare più segmenti."),
    ],
)
