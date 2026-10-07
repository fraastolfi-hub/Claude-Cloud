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
    og_title="Ho aperto cinque ristoranti. Al primo ho fatto il tuo stesso errore.",
    desc="Stai aprendo un hotel? Il posizionamento si decide prima delle fondamenta: dopo l'apertura costa il triplo. L'errore che Francesco Astolfi ha fatto al suo primo ristorante, perché tu non lo rifaccia.",
    eyebrow="Sintomo 06 · Il cantiere senza risposta",
    h1="Sto aprendo una struttura. Non voglio nascere commodity.",
    pull='Ho aperto cinque ristoranti. <span class="hl or in">Al primo ho fatto il tuo stesso errore.</span>',
    lead="Te lo racconto prima che lo firmi anche tu. Il cantiere corre, i render sono bellissimi, e la risposta a «perché voi?» è ferma al «poi vediamo».",
    cta2="Cosa puoi ancora decidere? ↓",
    memo=memo("Il giorno prima dell'apertura", "Ristorante n. 1",
              [("Le luci", "✓ giuste", "ok"),
               ("I tavoli", "✓ giusti", "ok"),
               ("I piatti, proprio la ceramica", "✓ scelti da me", "ok"),
               ("«Perché dovrei venire da voi?»", "?", "bad")],
              "La risposta", "poi vediamo",
              "Orgoglio, per dieci minuti. Poi una paura precisa."),
    ag_h2="Il prodotto non parla. <em>Sta zitto ed è bello.</em>",
    ag_lead="Il giorno prima dell'apertura del primo ristorante ero in mezzo alla sala. Tutto perfetto.",
    ag_prose='''        <p>Avevo scelto personalmente anche i piatti. Non il menu: proprio i piatti. La ceramica.</p>
        <p>Orgoglio, per dieci minuti. Poi una paura precisa, che non ho detto a nessuno: se domani uno mi chiede «perché dovrei venire da voi?», io cosa rispondo?</p>
        <p>Avevo speso tutto, soldi, notti, firme fatte tremando, su come il posto appariva. Zero su cosa il posto era.</p>
        <p>Il primo anno è girato, per curiosità. Il secondo la curiosità è finita ed è cominciata la domanda vera. L'ho pagata cara.</p>
        <p><strong>Gli hotel e i ristoranti non falliscono per le maniglie sbagliate. Falliscono perché nascono uguali.</strong> E chi nasce uguale ha una sola leva: il prezzo. Dal giorno uno.</p>''',
    tool=f'''      <div class="tool rv d1">
        <div class="tool-head"><span>Cosa puoi ancora decidere</span><em>Sposta il cantiere</em></div>
        <div class="tool-body">
          <div class="tool-row">
            <label for="apF">A che punto sei? <output id="apFo" for="apF">Cantiere aperto</output></label>
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
          <p id="apSub">Le fondamenta sono decise. Tutto quello che l'ospite vedrà, no.</p>
        </div>
        <p class="tool-note">Libera vuol dire: la decidi adesso, senza rifare niente. Dopo si può ancora cambiare tutto. Ma costa il triplo.</p>
      </div>''',
    css='''.phases{display:grid;grid-template-columns:repeat(5,1fr);font:700 10.5px/1.2 var(--mono);letter-spacing:.02em;text-transform:uppercase;color:var(--muted)}
.phases span{text-align:center;overflow-wrap:anywhere}
.phases span:first-child{text-align:left}.phases span:last-child{text-align:right}
.dec{list-style:none;border:2px solid var(--ink)}
.dec li{display:flex;justify-content:space-between;align-items:center;gap:12px;padding:10px 12px;border-bottom:1.5px dashed #b9b0a0;font-size:15.5px;line-height:1.35;transition:background .25s,color .25s}
.dec li:last-child{border-bottom:0}
.dec .st{flex:none;font:700 11.5px var(--mono);letter-spacing:.06em;text-transform:uppercase;border:2px solid var(--ink);padding:4px 7px;background:var(--mint)}
.dec li.gone{background:var(--paper-2);color:var(--muted)}
.dec li.gone span{text-decoration:line-through;text-decoration-color:var(--orange-dk);text-decoration-thickness:2px}
.dec li.gone .st{background:var(--ink);color:var(--paper)}''',
    js='''/* cosa puoi ancora decidere */
(function(){
  var r=document.getElementById('apF'), o=document.getElementById('apFo'), items=[].slice.call(document.querySelectorAll('#apList li'));
  var N=['Progetto','Cantiere aperto','Finiture e arredi','Pre-apertura','Aperto'];
  var T=['Sei nel momento migliore. Il posizionamento può ancora decidere dove e cosa costruire.',
         'Le fondamenta sono decise. Tutto quello che l’ospite vedrà, no.',
         'Stai scegliendo le maniglie. Assicurati di sapere prima il motivo.',
         'Restano il prezzo e le parole. Sono le prime cose che l’ospite vede.',
         'Il «poi» è scaduto. Si può ancora fare, ma ogni decisione adesso è un rifacimento. Costa il triplo.'];
  function upd(){
    var f=+r.value, free=0;
    items.forEach(function(li){ var ok=f<=+li.dataset.until; if(ok) free++; li.classList.toggle('gone',!ok); li.querySelector('.st').textContent=ok?'libera':'già decisa'; });
    o.textContent=N[f]; r.setAttribute('aria-valuetext',N[f]);
    document.getElementById('apOut').textContent=free+' su '+items.length;
    document.getElementById('apSub').textContent=T[f];
  }
  r.addEventListener('input',upd); upd();
})();''',
    sig_h2="I dieci segnali che stai per <em>nascere commodity.</em>",
    sig_lead="Spunta quelli in cui ti riconosci. Qui ogni segnale è ancora gratis da correggere. Dopo l'apertura, no.",
    signals=[
        ("Hai scelto le maniglie prima del motivo.", "Luci, tavoli, ceramica, rubinetti: tutto deciso. La risposta a «perché voi?» no.", "Gli hotel non falliscono per le maniglie sbagliate."),
        ("«Il prodotto parlerà da solo.»", "Lo pensavo anch'io. Il giorno prima dell'apertura del mio primo ristorante.", "Il prodotto non parla. Sta zitto ed è bello."),
        ("«Poi vediamo.»", "Il posizionamento è in fondo alla lista. Dopo gli arredi, prima del sito.", "Il «poi» ha una scadenza. Si chiama apertura."),
        ("I render somigliano a quelli degli altri.", "Il design si compra. L'architetto di tendenza pure. E infatti li comprano tutti.", "Il vantaggio estetico è un affitto. Scade."),
        ("Il concept è «boutique hotel».", "Vent'anni fa era una posizione. Oggi è una categoria. Affollata.", "È come dire «siamo un hotel». Con meno camere."),
        ("Il progetto racconta il posto, non te.", "Il mare, il lago, le colline. Splendido.", "Stai facendo marketing gratis a tutti gli hotel della zona."),
        ("Il prezzo lo decidi guardando i vicini.", "Ti metti un po' sotto, per partire. Poi lo alzi. Poi.", "Chi nasce uguale ha una sola leva: il prezzo. Dal giorno uno."),
        ("Il piano vendite è Booking.", "Prima ancora di aprire, il canale principale è deciso. Ed è di un altro.", "Si chiama dipendenza. E la firmi prima di aprire."),
        ("L'ospite ideale è «chi apprezza la qualità».", "Cioè tutti. Cioè nessuno.", "Specifico è scegliere. E scegliere è escludere."),
        ("Ogni scelta del cantiere è un dibattito.", "Che ristorante? Che SPA? Che stile? Ogni riunione riparte da zero, a colpi di gusti personali.", "Chi ha un'identità non dibatte. Deduce."),
    ],
    sig_tail="Sei ancora in tempo. È l’unico momento in cui il posizionamento costa poco e decide tutto.",
    br_h2="Il cantiere è il sintomo. <em>Il motivo è la fondazione.</em>",
    br_lead="Prima la bussola, poi i muri. Tu sei ancora al primo anello: l'unico momento in cui costa poco.",
    br_here=1,
    br_rings=["Quello che sai di essere. Sei ancora in tempo.", "Quello che dirai all'ospite.", "Quello che incasserai. Se nasci uguale, a prezzo basso."],
    br_prose='''        <p>Prima delle fondamenta si decide dove costruire. Vale anche per l'identità.</p>
        <p>Il posizionamento prima dell'apertura è quello che rende di più: decide camere, servizi, prezzo e parole prima che diventino cemento.</p>
        <p><strong>Dopo, costa il triplo.</strong></p>''',
    br_quote="Prima la bussola. Poi i muri. L'ordine conta.",
    proof_extra='''    <article class="card y rv" style="margin-top:22px">
      <p class="kicker" style="color:var(--ink)"><b>Caso</b> · Yume Ramen · 5 locali</p>
      <h3 style="margin:12px 0 8px">Questo non l'ho consigliato. L'ho inventato.</h3>
      <p>La posizione l'ho decisa prima di accendere la prima cucina. Con soldi miei. Da zero a 2,5 milioni di euro di fatturato. È il motivo per cui, oggi, a te lo dico prima.</p>
    </article>''',
    offer_lead="Vale anche per le strutture non ancora aperte. Anzi: è il momento in cui l'analisi rende di più.",
    cand_lead="Sessanta secondi. Il sito non serve: mettimi il nome del progetto e la città. Il resto me lo racconti dopo.",
    cand_extra='''      <p class="note-box" style="margin-top:22px">Anche strutture non ancora aperte: il posizionamento pre-apertura è quello che rende di più.</p>''',
    faq=[
        ("Non ho ancora un sito. Ha senso candidarsi?", "È il momento migliore. Prima delle fondamenta si decide dove costruire. Vale anche per l'identità."),
        ("Il concept ce l'ha già l'architetto.", "L'architetto decide come appare. Il posizionamento decide perché esiste. Se gli dai il motivo prima, progetta meglio. Se glielo dai dopo, rifate."),
        ("Non è troppo presto?", "No. È troppo tardi il giorno dopo l'apertura. Il «poi» ha una scadenza, e dopo costa il triplo."),
        ("Funziona anche per una struttura piccola?", "Funziona meglio. Una struttura piccola può permettersi una nicchia stretta. Una grande vive di compromessi."),
    ],
)
