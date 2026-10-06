"""Template comune per le sei pagine /problemi/*. Genera HTML statico completo."""
from pathlib import Path

OUT = Path(__file__).resolve().parents[2] / "src" / "pages" / "problemi"
STRIPE = "https://buy.stripe.com/aFa8wI5uaduM6LM3fr3AY00"


def memo(head_l, head_r, rows, tot_l, tot_r, foot, plain=False, stamp=None):
    lis = "\n".join(
        f'        <li><span>{a}</span><span class="v {c}">{b}</span></li>' for a, b, c in rows
    )
    st = f'<span class="stamp-tag">{stamp}</span>' if stamp else ""
    return f'''    <div class="memo{' plain' if plain else ''} rv d1" aria-label="{head_l}">
      {st}<div class="memo-h"><span>{head_l}</span><span>{head_r}</span></div>
      <ul>
{lis}
      </ul>
      <div class="tot"><span>{tot_l}</span><b>{tot_r}</b></div>
      <p class="memo-f">{foot}</p>
    </div>'''


def signals(items):
    out = []
    for i, (h, p, pk) in enumerate(items, 1):
        d = ["", " d1"][i % 2 == 0]
        out.append(f'''        <article class="sig rv{d}">
          <span class="n">{i:02d}</span>
          <h3>{h}</h3>
          <p>{p}</p>
          <p class="pk">{pk}</p>
          <button type="button" class="sig-btn" aria-pressed="false">Mi riconosco</button>
        </article>''')
    return "\n".join(out)


def rings(here, texts):
    names = [("Anello 1", "Posizionamento"), ("Anello 2", "Promessa"), ("Anello 3", "Prenotazione")]
    parts = []
    for i, ((k, h), t) in enumerate(zip(names, texts), 1):
        cls = " here" if i == here else ""
        parts.append(f'<div class="ring3{cls}"><span class="k">{k}</span><h3>{h}</h3><p>{t}</p></div>')
    return '\n      <div class="lk" aria-hidden="true">→</div>\n      '.join(parts)


def faq(items):
    return "\n".join(
        f'''      <details class="rv"><summary>{q}</summary><div class="ans"><p>{a}</p></div></details>'''
        for q, a in items
    )


SIG_JS = r'''
/* i dieci segnali: contatore "Mi riconosco" */
(function(){
  var btns=[].slice.call(document.querySelectorAll('.sig-btn')), meter=document.getElementById('sigMeter');
  var out=document.getElementById('sigScore'), msg=document.getElementById('sigMsg'), bar=document.getElementById('sigBar');
  var M=[
    'Spunta i segnali in cui ti riconosci. Con onestà: qui siamo solo tu e me.',
    '<b>Uno o due.</b> Forse sei messo meglio di tanti. O forse stai leggendo troppo in fretta.',
    '<b>Tre o quattro.</b> Il sintomo c’è. Non è ancora cronico: è il momento migliore per guardarlo.',
    '<b>Cinque o più?</b> Fermati. Respira. Non è colpa tua: nessuno te l’ha mai insegnato.',
    '<b>Otto o più.</b> %TAIL%'
  ];
  bar.innerHTML=new Array(11).join('<i></i>');
  var cells=bar.children;
  function upd(){
    var n=btns.filter(function(b){return b.getAttribute('aria-pressed')==='true';}).length;
    out.textContent=n;
    for(var i=0;i<cells.length;i++) cells[i].classList.toggle('on',i<n);
    msg.innerHTML=M[n===0?0:n<3?1:n<5?2:n<8?3:4];
    meter.classList.toggle('hot',n>=5);
  }
  btns.forEach(function(b){
    b.addEventListener('click',function(){
      var on=b.getAttribute('aria-pressed')!=='true';
      b.setAttribute('aria-pressed',on);
      b.closest('.sig').classList.toggle('on',on);
      upd();
    });
  });
  upd();
})();'''

RANGE_JS = r'''
  var nf=new Intl.NumberFormat('it-IT',{maximumFractionDigits:1});
  function eur(x){ return '€'+new Intl.NumberFormat('it-IT',{maximumFractionDigits:0}).format(Math.round(x)); }
  function bind(ids,cb){
    ids.forEach(function(id){
      var i=document.getElementById(id), o=document.getElementById(id+'o');
      function u(){ o.textContent=(i.dataset.pre||'')+nf.format(+i.value)+(i.dataset.suf||''); }
      i.addEventListener('input',function(){ u(); cb(); }); u();
    });
    cb();
  }
  function v(id){ return parseFloat(document.getElementById(id).value); }'''


def rng(id_, label, mn, mx, step, val, pre="", suf="", small=""):
    sm = f"<small>{small}</small>" if small else ""
    num = f"{val:,}".replace(",", ".") if isinstance(val, int) and val >= 10000 else str(val).replace(".", ",")
    shown = f"{pre}{num}{suf}"
    return f'''          <div class="tool-row">
            <label for="{id_}">{label} <output id="{id_}o" for="{id_}">{shown}</output></label>
            <input class="rng" type="range" id="{id_}" min="{mn}" max="{mx}" step="{step}" value="{val}" data-pre="{pre}" data-suf="{suf}">
            {sm}
          </div>'''


def page(p):
    slug = p["slug"]
    url = f"https://hotelpositioning.com/problemi/{slug}/"
    proof_extra = p.get("proof_extra", "")
    cand_extra = p.get("cand_extra", "")
    html = f'''<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{p["title"]} · Hotel Positioning</title>
<meta name="description" content="{p["desc"]}">
<link rel="canonical" href="{url}">
<meta property="og:title" content="{p["og_title"]}"><meta property="og:description" content="{p["desc"]}"><meta property="og:type" content="website">
<!-- @include head -->
<link rel="stylesheet" href="/assets/problemi.css">
<style>
{p.get("css","").strip()}
</style>
</head>
<body>
<!-- @include header -->

<main id="main">

<!-- ================= HERO: il sintomo ================= -->
<section class="ph-hero">
  <div class="wrap split">
    <div>
      <span class="eyebrow"><span class="dot"></span>{p["eyebrow"]}</span>
      <h1><q>{p["h1"]}</q></h1>
      <p class="pull">{p["pull"]}</p>
      <p class="lead">{p["lead"]}</p>
      <div class="btn-row">
        <a href="#candidatura" class="btn">Candida il tuo hotel <span class="arr">→</span></a>
        <a href="#conto" class="btn ghost">{p["cta2"]}</a>
      </div>
      <p class="micro"><b>Analisi gratuita per 5 hotel.</b> Una alla settimana, la faccio io. Poi torna a €697.</p>
    </div>
{p["memo"]}
  </div>
</section>

<!-- ================= N°01 AGITAZIONE ================= -->
<section class="sec white" id="conto">
  <div class="wrap">
    <div class="sec-head">
      <span class="num-tag">N°01</span>
      <h2>{p["ag_h2"]}</h2>
      <p class="lead">{p["ag_lead"]}</p>
    </div>
    <div class="grid-2">
      <div class="prose rv">
{p["ag_prose"]}
      </div>
{p["tool"]}
    </div>
  </div>
</section>

<!-- ================= N°02 I DIECI SEGNALI ================= -->
<section class="sec alt" id="segnali">
  <div class="wrap">
    <div class="sec-head">
      <span class="num-tag">N°02</span>
      <h2>{p["sig_h2"]}</h2>
      <p class="lead">{p["sig_lead"]}</p>
    </div>
    <div class="sig-wrap">
      <aside class="sig-meter" id="sigMeter" aria-label="Segnali riconosciuti">
        <span class="k">Ti riconosci in</span>
        <span class="score" aria-live="polite"><span id="sigScore">0</span><small>/10</small></span>
        <div class="sig-bar" id="sigBar" aria-hidden="true"></div>
        <p class="sig-msg" id="sigMsg" aria-live="polite">Spunta i segnali in cui ti riconosci. Con onestà: qui siamo solo tu e me.</p>
        <a href="#candidatura" class="btn sm">Candida il tuo hotel <span class="arr">→</span></a>
      </aside>
      <div class="sig-grid">
{signals(p["signals"])}
      </div>
    </div>
  </div>
</section>

<!-- ================= N°03 PONTE: il sintomo non è la malattia ================= -->
<section class="sec dark">
  <div class="wrap">
    <div class="sec-head">
      <span class="num-tag">N°03</span>
      <h2>{p["br_h2"]}</h2>
      <p class="lead">{p["br_lead"]}</p>
    </div>
    <div class="chain3 rv">
      {rings(p["br_here"], p["br_rings"])}
    </div>
    <div class="grid-2" style="align-items:end">
      <div class="prose rv">
{p["br_prose"]}
      </div>
      <div class="rv d1">
        <p class="big-quote" style="font-size:clamp(26px,2.8vw,38px);margin-bottom:30px">{p["br_quote"]}</p>
        <a href="/metodo/" class="btn ghost">Il metodo in sei passaggi <span class="arr">→</span></a>
      </div>
    </div>
  </div>
</section>

<!-- ================= N°04 LA PROVA ================= -->
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <span class="num-tag">N°04</span>
      <h2>{p.get("proof_h2","Prima la bussola. <em>Poi i muri.</em>")}</h2>
    </div>
    <article class="proof rv">
      <div class="l">
        <p class="kicker"><b>Caso</b> · Silva Splendid · Fiuggi</p>
        <h3>Da «hotel 4 stelle con SPA» a <span class="hl in">L’Hotel Benessere di Fiuggi</span>.</h3>
        <ol>
          <li>118 camere e la SPA più grande del Lazio. Invisibile lo stesso: diceva tutto a tutti.</li>
          <li>{p.get("proof_move","La mossa: un fatto al posto di un aggettivo, una categoria con l’articolo determinativo, e l’uscita quasi totale dal mercato delle famiglie.")}</li>
          <li>In cinque anni il fatturato passa da 3,5 a oltre 7 milioni di euro. La tariffa media circa raddoppia.</li>
        </ol>
      </div>
      <div class="r">
        <span class="kicker">{p.get("proof_k","Fatturato annuo")}</span>
        <b>{p.get("proof_big","<s>€3,5M</s> €7M+")}</b>
        <p class="case-honest">Non da solo: posizionamento più ristrutturazione. Il posizionamento ha dato la direzione, gli investimenti l’hanno resa credibile. In quest’ordine.</p>
      </div>
    </article>
{proof_extra}
    <div class="btn-row rv" style="margin-top:30px"><a href="/casi/" class="btn ghost">Leggi i casi per intero <span class="arr">→</span></a></div>
  </div>
</section>

<!-- ================= N°05 L'OFFERTA ================= -->
<section class="sec alt">
  <div class="wrap">
    <div class="sec-head">
      <span class="num-tag">N°05</span>
      <h2>Due modi per partire. <em>Lo stesso metodo.</em></h2>
      <p class="lead">{p["offer_lead"]}</p>
    </div>
    <div class="offer">
      <div class="card rv">
        <p class="kicker"><b>Candidatura</b> · 5 posti</p>
        <p class="price">Gratis</p>
        <p>Cinque hotel selezionati. Un’analisi alla settimana, e la faccio io. Non un junior, non un tool.</p>
        <ul class="check-list">
          <li>Diagnosi del posizionamento attuale e mappa dei concorrenti.</li>
          <li>Tre profili di ospite ideale.</li>
          <li>Il posizionamento proposto e cinque azioni da fare subito.</li>
          <li>20-25 pagine. Risposta alla candidatura entro 48 ore.</li>
        </ul>
        <a href="#candidatura" class="btn">Candida il tuo hotel <span class="arr">→</span></a>
      </div>
      <div class="card ink rv d1">
        <p class="kicker" style="color:#B9B0A0"><b>Analisi completa</b> · subito</p>
        <p class="price">€697<small>+ IVA</small></p>
        <p>Per chi non vuole aspettare la selezione. O non è stato scelto.</p>
        <ul class="check-list">
          <li>5 documenti operativi, 39 pagine.</li>
          <li>Consegna in 48 ore dal questionario.</li>
          <li>3 call di controllo: mese 1, 3 e 6.</li>
          <li>Garanzia: se non ti serve, rimborso più €500 entro 30 giorni.</li>
        </ul>
        <a href="{STRIPE}" class="btn" rel="noopener">Acquista l’analisi · €697 + IVA <span class="arr">→</span></a>
      </div>
    </div>
    <p class="offer-more rv"><a href="/analisi/">Tutti i dettagli dell’offerta →</a><span class="muted" style="font-weight:400">Garanzia, i cinque documenti, come lavoro.</span></p>
  </div>
</section>

<!-- ================= CANDIDATURA ================= -->
<section class="sec orange" id="candidatura" data-sticky-stop>
  <div class="wrap cand">
    <div>
      <div class="sec-head" style="margin-bottom:0">
        <span class="sticker">5 posti · 1 a settimana</span>
        <h2>Candida il tuo hotel.</h2>
        <p class="lead">{p["cand_lead"]}</p>
      </div>
      <ul class="check-list">
        <li>Hotel indipendenti. Non catene in franchising.</li>
        <li>Proprietari e gestori disposti a cambiare qualcosa. E a rinunciare a certi ospiti.</li>
        <li>Anche se ti scarto, ti spiego perché.</li>
      </ul>
      <ul class="check-list no" style="margin-top:14px">
        <li>Non candidarti se cerchi una soluzione magica, o se pensi che il posizionamento sia «scrivere meglio».</li>
      </ul>
{cand_extra}
    </div>
    <!-- @include form-candidatura -->
  </div>
</section>

<!-- ================= FAQ ================= -->
<section class="sec">
  <div class="wrap">
    <div class="sec-head">
      <span class="num-tag">FAQ</span>
      <h2>{p.get("faq_h2","Le domande che non mi fai <em>ad alta voce.</em>")}</h2>
    </div>
    <div class="faq">
{faq(p["faq"])}
    </div>
    <div class="btn-row rv" style="margin-top:36px">
      <a href="#candidatura" class="btn dark">Candida il tuo hotel <span class="arr">→</span></a>
      <a href="/analisi/" class="btn ghost">Tutti i dettagli dell’offerta</a>
    </div>
  </div>
</section>

</main>

<!-- @include footer -->
<!-- @include sticky-candidatura -->
<script>
{p["js"].strip()}
{SIG_JS.replace("%TAIL%", p["sig_tail"])}
</script>
</body>
</html>
'''
    dest = OUT / slug / "index.html"
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(html)
    return dest
