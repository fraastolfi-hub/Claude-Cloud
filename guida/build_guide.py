# Genera la guida "Come funziona davvero il positioning di un hotel" nello stile della pagina /library.
# Legge nomi, id e soglie dei pattern da src/data/library.json del repository hotelpositioning,
# così i link alla Library restano corretti. Incorpora i font (se disponibili) per un PDF fedele.
# Uso: python3 guida/build_guide.py [cartella_font]
import base64, html, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
LIB_PATH = os.environ.get('LIBRARY_JSON', '/home/user/hotelpositioning/src/data/library.json')
FONT_DIR = sys.argv[1] if len(sys.argv) > 1 else None

LIB = json.load(open(LIB_PATH, encoding='utf-8'))
P = {p['codice']: p for p in LIB['pattern']}
FAM = {f['id']: f['nome'] for f in LIB['famiglie']}
N_PAT = len(LIB['pattern'])
SITE = 'https://hotelpositioning.com'
e = html.escape

# ---------------------------------------------------------------- fonts
FONTS = [
    ('Archivo Black', 400, 'archivo-black/files/archivo-black-latin-400-normal.woff2'),
    ('Space Grotesk', 400, 'space-grotesk/files/space-grotesk-latin-400-normal.woff2'),
    ('Space Grotesk', 500, 'space-grotesk/files/space-grotesk-latin-500-normal.woff2'),
    ('Space Grotesk', 600, 'space-grotesk/files/space-grotesk-latin-600-normal.woff2'),
    ('Space Grotesk', 700, 'space-grotesk/files/space-grotesk-latin-700-normal.woff2'),
    ('Space Mono', 400, 'space-mono/files/space-mono-latin-400-normal.woff2'),
    ('Space Mono', 700, 'space-mono/files/space-mono-latin-700-normal.woff2'),
]
font_css = ''
if FONT_DIR:
    for fam, w, rel in FONTS:
        data = base64.b64encode(open(os.path.join(FONT_DIR, rel), 'rb').read()).decode()
        font_css += (f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;font-display:swap;'
                     f'src:url(data:font/woff2;base64,{data}) format("woff2")}}\n')
font_link = '' if FONT_DIR else (
    '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Space+Grotesk:wght@400;500;600;700&family=Space+Mono:wght@400;700&display=swap" rel="stylesheet">')

# ---------------------------------------------------------------- content helpers
PROFILE_PATTERNS = {
    'location': ['F01', 'F03', 'F05', 'B03', 'B05', 'K07'],
    'capital': ['F04', 'E02', 'E06', 'J01', 'J02', 'K06'],
    'operations': ['H01', 'H03', 'H06', 'D02', 'D06', 'J03'],
    'narrativa': ['G02', 'C03', 'C04', 'C02', 'D01', 'A04', 'I03', 'L07'],
}
MATURITA = {1: ('Consolidato', 'is-t1'), 2: ('Emergente', 'is-t2'), 3: ('Nascente', 'is-nascente')}


def lib_link(codes):
    return f'{SITE}/library?tipo=pattern&amp;ids=' + ','.join(str(P[c]['id']) for c in codes)


def affini(key):
    codes = PROFILE_PATTERNS[key]
    chips = ''.join(
        f'<a class="affine" href="{SITE}/library?tipo=pattern&amp;ids={P[c]["id"]}">'
        f'<span class="affine__id">{c}</span><span class="affine__name">{e(P[c]["nome"])}</span>'
        f'<span class="badge badge--xs">Ops ≥ {P[c]["gestioneMinima"]}</span></a>'
        for c in codes)
    return (f'<div class="sec"><div class="lbl">↳ Pattern coerenti nella Library</div>'
            f'<div class="chips">{chips}</div>'
            f'<a class="btn btn--ink" href="{lib_link(codes)}">Apri questi {len(codes)} pattern →</a></div>')


def card(cid, badges, tag, title, body, foot='', tag_cls='fam'):
    b = ''.join(f'<span class="badge {cls}">{e(t)}</span>' for t, cls in badges)
    return (f'<article class="card"><div class="card__top"><span class="card__id">{cid}</span>'
            f'<div class="card__badges">{b}</div></div>'
            f'<span class="{tag_cls}">{e(tag)}</span><h3 class="card__title">{title}</h3>'
            f'<div class="card__desc">{body}</div>{foot}</article>')


def sheet(bar_id, badges, tag, title, lead, sections, tag_cls='fam'):
    b = ''.join(f'<span class="badge {cls}">{e(t)}</span>' for t, cls in badges)
    secs = ''.join(sections)
    return (f'<article class="sheet"><div class="sheet__keep"><div class="bar"><span class="bar__id">{bar_id}</span><div class="bar__r">{b}</div></div>'
            f'<div class="sheet__intro"><span class="{tag_cls}">{e(tag)}</span><h3 class="sheet__title">{title}</h3>'
            f'<p class="lead">{lead}</p></div></div><div class="sheet__body">{secs}</div></article>')


def sec(label, html_body, cls=''):
    return f'<div class="sec {cls}"><div class="lbl">{label}</div>{html_body}</div>'


# ---------------------------------------------------------------- 01 components
COMPONENTS = [
    ('C1', 'Location', 'Non si cambia', 'is-nascente', 'Dove sei: il flusso di clienti che arriva da solo e il nome che la gente riconosce.'),
    ('C2', 'Capital', 'Anni e investimenti', 'is-t3', 'Cosa hai costruito: la qualità percepita di camere, bagni, spazi, ristorante.'),
    ('C3', 'Operations', 'Mesi di lavoro', 'is-t2', 'Come lavori ogni giorno: accoglienza, pulizia, prezzi, risposta alle recensioni, formazione.'),
    ('C4', 'Narrativa di mercato', 'Settimane · costo basso', 'is-t1', 'Come ti racconti: la promessa, il segmento che scegli, l’identità che ti distingue.'),
]
components_html = ''.join(
    card(cid, [(speed, cls)], 'Componente', e(name), f'<p>{e(desc)}</p>') for cid, name, speed, cls, desc in COMPONENTS)

# ---------------------------------------------------------------- 03 profiles
PROFILES = [
    ('location', 'Profilo 01', 'Location-driven', 'Il motore è il luogo',
     'Una componente alta (Location da 8 in su) e le altre più basse. Il cliente paga per vivere Positano, Capri o Ravello attraverso l’hotel: l’hotel è il tramite, non il protagonista.',
     'Esempio tipico: una piccola struttura a Positano con investimenti modesti, gestione familiare e una narrativa ancora da costruire.',
     'Racconta il luogo come identità dell’hotel: “Siamo Positano”, “La vera Capri”. Arredi, colazione, bar ed esperienze raccontano il luogo in modo autentico e specifico, mai generico.',
     'Dipendi del tutto dal flusso turistico del luogo. Se il luogo perde attrattiva, l’hotel non ha alternative: nel tempo conviene costruire anche le altre componenti.'),
    ('capital', 'Profilo 02', 'Capital-driven', 'Il motore è l’esperienza fisica',
     'Capital alto (8 o più) e le altre componenti più basse. Il cliente paga per la bellezza dello spazio e per una qualità materiale che nella zona non trova.',
     'Esempio tipico: un hotel in una località secondaria con un restauro importante o un edificio iconico, gestione ancora in rodaggio, narrativa da costruire.',
     'Racconta l’investimento come promessa: “Il posto più bello della regione”, “Un design che non trovi altrove”, “Lo spazio che vale il viaggio”.',
     'Un capital alto richiede prezzi alti per ripagarsi. Se le operations non sono all’altezza degli spazi, l’ospite si sente ingannato alla prima richiesta gestita male.'),
    ('operations', 'Profilo 03', 'Operations-driven', 'Il motore è la qualità che si ripete',
     'Operations alte (8 o più) e le altre componenti più basse. Il cliente paga per non doverci pensare: sa che tutto funziona.',
     'Esempio tipico: un hotel di città o di mare in una località non iconica, con revenue management attivo, staff formato e stabile, risposte puntuali alle recensioni, pulizia impeccabile.',
     'Racconta l’affidabilità come promessa, ma con meccanismi riconoscibili. citizenM (dal 2025 parte di Marriott) e YOTEL l’hanno trasformata in un prodotto: check-in da soli, camera unica, tutto prevedibile.',
     '“Qualità del servizio” lo dicono tutti. L’eccellenza va trasformata in meccanismi visibili e specifici, non in aggettivi.'),
    ('narrativa', 'Profilo 04', 'Narrativa-driven', 'Il motore è come ti racconti',
     'Narrativa alta (8 o più) e le altre componenti più basse, con le operations almeno a 6-7: sotto quella soglia la narrativa non regge.',
     'Due casi tipici. L’hotel storico di famiglia, dove la storia vera diventa la promessa: “quattro generazioni”, “qui dal 1897”. E l’hotel senza luogo iconico né grandi investimenti che sceglie una promessa radicale e specifica: “l’hotel dei triatleti del circuito di Misano”, non “hotel di charme per famiglie”.'
     '<br><br><strong>Eremito</strong>, in Umbria, è un eremo contemporaneo con cena in silenzio, cucina vegetariana, niente wifi né televisione: il luogo è isolato e la struttura essenziale, è la narrativa a fare il lavoro. <strong>Sextantio</strong> a Santo Stefano di Sessanio, in Abruzzo: Daniele Kihlgren ha costruito il “lusso dell’imperfezione” in un borgo quasi abbandonato, diventato un caso studio della Harvard Business School.',
     'Scegli un segmento molto specifico, fai una promessa radicale e sostienila con scelte operative visibili: menù, orari, servizi, divieti. La narrativa si costruisce con le scelte di ogni giorno, non con gli slogan.',
     'Se la promessa radicale non è mantenuta ogni giorno, è peggio non averla: diventa un contratto che le operations devono onorare.'),
]
profiles_html = ''.join(
    sheet(pid, [(tag, 'is-t1')], 'Profilo di hotel', e(title), lead, [
        sec('Esempio tipico', f'<p>{example}</p>'),
        f'<div class="engine"><div class="lbl">{"Come costruirla" if key == "narrativa" else "Narrativa coerente"}</div><p>{e(engine)}</p></div>',
        sec('Rischio', f'<p>{e(risk)}</p>'),
        affini(key),
    ]) for key, pid, tag, title, lead, example, engine, risk in PROFILES)

# ---------------------------------------------------------------- 04 mixed
MIXED = [
    ('M1', 'Location + Capital', 'Lusso nel luogo iconico', 'Struttura di lusso in un luogo iconico, come l’Hotel Caruso a Ravello (gruppo Belmond). La narrativa coerente è l’esperienza totale del luogo attraverso l’investimento: “il modo più ricco di vivere Ravello”. Il rischio è che le operations diventino il collo di bottiglia di ciò che gli altri due pilastri promettono.'),
    ('M2', 'Location + Narrativa', 'Il luogo, raccontato', 'Casa Cipriani Milano porta in città l’ospitalità veneziana della famiglia Cipriani, attiva dal 1931: la narrativa amplifica la location invece di dipenderne.'),
    ('M3', 'Operations + Narrativa', 'Eccellenza per un segmento', 'The Pig Hotels, nel Regno Unito: il fondatore Robin Hutson ha trasformato l’imperfezione curata in una promessa operativa. Rientra qui anche l’hotel storico di famiglia in una città d’arte minore, con una gestione rigorosa e una storia vera da raccontare.'),
    ('M4', 'Capital + Operations', 'Dove non te l’aspetti', 'Hotel contemporaneo con investimento serio e gestione professionale in una località secondaria. La narrativa coerente è “l’esperienza che non ti aspetti dove non te l’aspetti”: l’hotel può diventare la ragione del viaggio.'),
    ('M5', 'Tutte e quattro alte', 'Amplificazione', 'Il lusso con tutte le componenti eccellenti. Qui la narrativa lavora per amplificazione: estrae valore già presente nelle altre tre. Non salva l’hotel, lo fa rendere di più.'),
]
mixed_html = ''.join(card(mid, [(combo, 'is-t3')], 'Profilo misto', e(t), f'<p>{e(d)}</p>') for mid, combo, t, d in MIXED)

# ---------------------------------------------------------------- 05 hotels
HOTELS = [
    ('A', '4 stelle · Positano · 25 camere · stagionale', '“Siamo a Positano, siamo accoglienti”', (10, 6, 6, 3), '€3,0M'),
    ('B', '4 stelle · Positano · 25 camere · stagionale', '“La vera casa positanese”', (10, 6, 6, 8), '€4,5M'),
    ('C', '4 stelle · Cattolica · 50 camere', '“Famiglia e divertimento”', (6, 6, 6, 3), '€1,3M'),
    ('D', '4 stelle · Cattolica · 50 camere · +30 giorni', '“L’hotel dei triatleti del circuito di Misano”', (6, 6, 6, 9), '€2,0M'),
    ('E', '4 stelle business · Milano Linate · 80 camere · tutto l’anno', 'Operations eccellenti, promessa chiara', (5, 6, 9, 7), '€5,2M'),
    ('F', '4 stelle storico · Mantova · 30 camere', '“Quattro generazioni di famiglia”', (5, 5, 7, 9), '€1,8M'),
    ('G', '3 stelle al mare · Riviera del Conero · 22 camere · stagionale', '“Hotel di famiglia da sempre”', (6, 4, 5, 2), '€440K'),
    ('H', 'Agriturismo · Monferrato · 10 camere', '“Esperienza enogastronomica piemontese”', (4, 5, 5, 3), '€490K'),
    ('I', 'Lo stesso agriturismo · 10 camere', '“La residenza del vignaiolo per enologi professionisti”', (4, 5, 5, 9), '€800K'),
]
LABELS = ('Location', 'Capital', 'Operations', 'Narrativa')


def hotel_card(h):
    hid, sub, story, scores, rev = h
    tot = sum(scores)
    cls = 'is-t1' if tot >= 27 else ('is-t2' if tot >= 21 else 'is-nascente')
    bars = ''.join(
        f'<div class="meter{" is-n" if i == 3 else ""}"><span class="meter__l">{LABELS[i]}</span>'
        f'<span class="meter__t"><span class="meter__f" style="width:{s * 10}%"></span></span><span class="meter__v">{s}</span></div>'
        for i, s in enumerate(scores))
    foot = (f'<div class="rule"></div><div class="hfoot"><div><div class="lbl">Fatturato stimato</div>'
            f'<div class="hfoot__v">{rev}</div></div><div class="hfoot__r"><div class="lbl">Posizionamento</div>'
            f'<div class="hfoot__v">{tot}<small>/40</small></div></div></div>')
    return card(f'Hotel {hid}', [(f'{tot}/40', cls)], sub, e(story), f'<div class="meters">{bars}</div>', foot)


hotels_html = ''.join(hotel_card(h) for h in HOTELS)

VS = [
    ('A', 'B', 'Stesso albergo a Positano, stesse camere e stesse operations: cambia solo la narrativa. A dice “siamo a Positano, siamo accoglienti” (3). B ha costruito “la vera casa positanese”: oggetti del paese, menù solo con prodotti locali, arredi che raccontano la storia del borgo, esperienze con i pescatori del porto (8). Il posizionamento passa da 25 a 30 e il fatturato stimato cresce di €1,5M. La narrativa ha amplificato la location.', '+50%'),
    ('C', 'D', 'Stesso albergo a Cattolica. C è un 4 stelle “famiglia e divertimento” come altri cinquanta sulla costa (3). D è diventato “l’hotel dei triatleti del circuito di Misano”: deposito bici, nutrizionista sportivo, convenzioni con il circuito, pacchetti allenamento e apertura prolungata per le gare d’autunno (9). Il posizionamento passa da 21 a 27 e il fatturato stimato cresce di €700K, con trenta giorni di apertura in più. Da commodity a specialista.', '+54%'),
    ('A', 'E', 'Positano ha una location straordinaria ma apre solo d’estate (posizionamento 25). Il business hotel di Linate ha una location meno iconica ma apre tutto l’anno, con operations eccellenti e una promessa chiara (27). E fattura quasi il doppio perché ha più camere (80 contro 25) e apre il doppio dei giorni. Il posizionamento dice quanto è forte l’hotel; il fatturato dipende anche da dimensione e stagionalità.', 'Dimensione'),
    ('F', None, 'L’hotel storico di Mantova non vince su location e capital, ma ha buone operations e una narrativa altissima fondata sulla storia vera della famiglia (9). La storia non è una componente a parte: è il materiale con cui la narrativa costruisce la promessa. Posizionamento 26 e un segmento di appassionati di storia disposti a pagare l’autenticità.', 'Storia'),
    ('G', None, 'Il 3 stelle delle Marche apre quasi solo d’estate e sopravvive sul flusso turistico generale (posizionamento 17, narrativa 2). Non sbaglia nulla di grave, ma non ha leve. Una narrativa specifica, come “l’hotel degli appassionati di immersioni del Parco del Conero” o “la casa degli escursionisti del Monte Conero”, porterebbe la narrativa a 8 e il posizionamento a 23, intercettando segmenti che oggi scelgono altrove.', 'Potenziale'),
    ('H', 'I', 'Stesso agriturismo nel Monferrato, stesse dieci camere, stessa cantina. H vende la generica “esperienza enogastronomica piemontese” (3, posizionamento 17). I è diventato “la residenza del vignaiolo per enologi professionisti”: un workshop tecnico all’anno ospitato da una cantina diversa, visite tecniche per gruppi di enologi stranieri, settimane dedicate a un singolo produttore (9, posizionamento 23). Il fatturato stimato cresce di €310K. La leva della narrativa funziona anche nel piccolissimo, se è abbastanza specifica.', '+63%'),
]
vs_html = ''.join(
    card(f'Confronto {i + 1:02d}', [(delta, 'is-t1' if delta.startswith('+') else 'is-t3')], 'Confronto',
         (f'Hotel {a} <span class="x">vs</span> Hotel {b}' if b else f'Hotel {a}'), f'<p>{e(t)}</p>', tag_cls='catag')
    for i, (a, b, t, delta) in enumerate(VS))

QUESTIONS = [
    ('Domanda 01', 'Le operations tengono?',
     '<p>Guarda le recensioni degli ultimi 24 mesi su Google, Booking e TripAdvisor. La media è sopra 4,3? Lo staff è formato e stabile? Il revenue management è attivo? Rispondi in fretta a recensioni e segnalazioni?</p>',
     [('Se no', 'La narrativa non è la tua priorità. Prima raggiungi la soglia operativa: una narrativa forte adesso ti farebbe più male che bene.'),
      ('Se sì', 'Passa alla domanda 2.')]),
    ('Domanda 02', 'Qual è il tuo profilo?',
     '<p>Dai un voto da 0 a 10 a ciascuna componente, senza barare, e sommali: è il tuo Posizionamento di Mercato di oggi. Poi conta quante componenti hanno 8 o più.</p>',
     [('Nessuna ≥ 8', 'La leva da costruire è la narrativa: è l’unica che puoi alzare in fretta senza grandi investimenti. Se più componenti sono sotto 5, prima vanno sistemate capital e operations.'),
      ('Una ≥ 8', 'Hai un profilo puro: Location, Capital, Operations o Narrativa-driven. La narrativa deve raccontare e amplificare quella componente.'),
      ('Due o più ≥ 8', 'Hai un profilo misto: la narrativa deve raccontare l’incrocio specifico, non una sola componente.')]),
    ('Domanda 03', 'Il mercato raggiungibile regge il business?',
     '<p>Con la narrativa che stai pensando, i clienti raggiungibili per distanza e capacità di spesa bastano a garantire il fatturato minimo? Il calcolo: <strong>camere × occupazione obiettivo × giorni di apertura × prezzo medio obiettivo</strong>. I clienti potenziali per quella narrativa sono abbastanza per raggiungerlo?</p>',
     [('Se sì', 'Procedi.'), ('Se no', 'Sposta la narrativa su un asse con un mercato più ampio prima di investire.')]),
]
q_html = ''.join(
    f'<article class="panel"><div class="panel__head"><span class="panel__title">{qid}</span></div><div class="panel__body">'
    f'<h3 class="sheet__title sheet__title--sm">{e(title)}</h3>{body}'
    f'<div class="answers">' + ''.join(f'<div class="answer"><span class="badge is-t1">{e(k)}</span><p>{e(v)}</p></div>' for k, v in answers) +
    f'</div></div></article>' for qid, title, body, answers in QUESTIONS)

LOGO = ('<svg class="logo__mark" viewBox="0 0 30 30" aria-hidden="true"><g fill="currentColor">'
        '<rect x="0" y="0" width="8" height="8"/><rect x="11" y="0" width="8" height="8"/><rect x="22" y="0" width="8" height="8"/>'
        '<rect x="0" y="11" width="8" height="8"/><rect x="11" y="11" width="8" height="8"/><rect x="22" y="11" width="8" height="8"/>'
        '<rect x="0" y="22" width="8" height="8"/><rect x="11" y="22" width="8" height="8"/></g>'
        '<circle cx="26" cy="26" r="4.4" fill="#F9535F"/></svg>')

CHAPTERS = [('cap1', '01 · Le 4 componenti'), ('cap2', '02 · Narrative diverse'), ('cap3', '03 · I 4 profili'),
            ('cap4', '04 · Profili misti'), ('cap5', '05 · 9 hotel'), ('cap6', '06 · Le 2 regole'), ('cap7', '07 · Le 3 domande')]
pills = ''.join(f'<a class="pill" href="#{a}">{e(t)}</a>' for a, t in CHAPTERS)


def h2(n, anchor, title, lead=''):
    lead_html = f'<p class="h2__lead">{lead}</p>' if lead else ''
    return f'<header class="h2" id="{anchor}"><span class="h2__n">Capitolo {n}</span><h2>{title}</h2>{lead_html}</header>'


CSS = r"""
:root{--paper:#FFFDF5;--paper-2:#F6F1E4;--ink:#111;--ink-soft:rgba(17,17,17,.68);--yellow:#FFD23F;--yellow-soft:#FFF6CF;--rust:#D85A30;--coral:#F9535F;
--line:2px solid var(--ink);--line-thick:3px solid var(--ink);--shadow:6px 6px 0 var(--ink);--shadow-sm:4px 4px 0 var(--ink);--shadow-lg:10px 10px 0 var(--ink);
--display:"Archivo Black","Arial Black",sans-serif;--sans:"Space Grotesk",system-ui,sans-serif;--mono:"Space Mono",ui-monospace,monospace;
--gutter:clamp(16px,4vw,40px);color-scheme:light}
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
html{-webkit-text-size-adjust:100%;-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{font-family:var(--sans);font-size:16px;line-height:1.5;color:var(--ink);background-color:var(--paper);
background-image:repeating-linear-gradient(0deg,transparent 0 47px,rgba(17,17,17,.055) 47px 48px),repeating-linear-gradient(90deg,transparent 0 47px,rgba(17,17,17,.055) 47px 48px)}
a{color:inherit;text-decoration:none}
strong{font-weight:700}
.wrap{max-width:1180px;margin:0 auto;padding:0 var(--gutter)}
.narrow{max-width:760px}
.lbl{font-family:var(--mono);font-size:11px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;line-height:1.4}
.rule{height:2px;background:var(--ink);margin:18px 0}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.hl{background:var(--yellow);padding:0 .12em;box-decoration-break:clone;-webkit-box-decoration-break:clone}
/* badges / tags */
.badge{display:inline-flex;align-items:center;justify-content:center;white-space:nowrap;font-family:var(--mono);font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;line-height:1.3;border:var(--line);padding:3px 8px;background:var(--paper)}
.badge--xs{font-size:9px;padding:1px 5px}
.badge.is-t1{background:var(--yellow)}.badge.is-t2{background:var(--rust);color:#fff}.badge.is-t3{background:var(--paper)}.badge.is-nascente{background:var(--ink);color:var(--yellow)}
.fam{display:inline-block;align-self:flex-start;font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;line-height:1.3;background:var(--ink);color:var(--paper);padding:4px 8px}
.catag{display:inline-block;align-self:flex-start;font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;line-height:1.3;background:var(--rust);color:#fff;border:var(--line);padding:3px 8px}
.pill{display:inline-flex;align-items:center;font-family:var(--mono);font-size:11px;font-weight:700;letter-spacing:.05em;text-transform:uppercase;line-height:1.3;border:var(--line);padding:7px 10px;background:var(--paper)}
.pill:hover{background:var(--yellow)}
.btn{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:13px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;border:var(--line);background:var(--yellow);color:var(--ink);padding:12px 18px;box-shadow:var(--shadow-sm);transition:transform .12s,box-shadow .12s}
.btn:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 var(--ink)}
.btn--ink{background:var(--ink);color:var(--paper);align-self:flex-start;box-shadow:4px 4px 0 var(--rust);margin-top:6px}
.btn--paper{background:var(--paper)}
/* header */
.header{position:sticky;top:0;z-index:40;background:var(--paper);border-bottom:var(--line-thick)}
.header__in{display:flex;align-items:center;justify-content:space-between;gap:16px;height:72px}
.brand{display:flex;align-items:center;gap:18px;min-width:0}
.logo{display:inline-flex;align-items:center;gap:12px;line-height:1}
.logo__mark{width:44px;height:44px;flex:none}
.logo__word{display:flex;flex-direction:column;font-family:var(--display);text-transform:uppercase;font-size:20px;line-height:.98}
.logo__o{display:inline-block;width:.74em;height:.74em;border-radius:50%;background:var(--coral);margin:0 .03em;vertical-align:-.02em}
.brand__lib{border-left:var(--line);padding-left:18px}
.brand__title{font-family:var(--display);font-size:24px;line-height:1;text-transform:uppercase;letter-spacing:-.01em}
.brand__ver{margin-top:6px;font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--ink-soft)}
.header__r{display:flex;align-items:center;gap:18px}
.back{font-family:var(--mono);font-size:11px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.back:hover{text-decoration:underline}
.count{white-space:nowrap;font-family:var(--mono);font-size:12px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;background:var(--yellow);border:var(--line);padding:7px 12px;box-shadow:var(--shadow-sm);transform:rotate(-2deg)}
/* hero */
.hero{border-bottom:var(--line-thick)}
.hero__in{padding-top:clamp(40px,6vw,88px);padding-bottom:clamp(36px,5vw,64px)}
.hero__title{font-family:var(--display);text-transform:uppercase;font-size:clamp(34px,5.8vw,80px);line-height:.95;letter-spacing:-.02em;max-width:18ch}
.hero__lead{margin-top:28px;font-size:clamp(16px,1.6vw,19px);max-width:68ch;font-weight:500}
.hero__pills{margin-top:32px;display:flex;flex-wrap:wrap;gap:8px}
.hero__actions{margin-top:28px;display:flex;flex-wrap:wrap;gap:14px;align-items:center}
/* chapters */
.chapter{padding:clamp(48px,6vw,80px) 0 0}
.h2{margin-bottom:28px}
.h2__n{display:inline-block;font-family:var(--mono);font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;background:var(--ink);color:var(--yellow);padding:4px 10px;margin-bottom:14px}
.h2 h2{font-family:var(--display);text-transform:uppercase;font-size:clamp(28px,4.4vw,52px);line-height:.95;letter-spacing:-.02em;max-width:22ch;padding-bottom:16px;border-bottom:var(--line-thick)}
.h2__lead{margin-top:18px;font-size:clamp(16px,1.6vw,18px);font-weight:500;max-width:68ch}
.prose p{font-size:17px;line-height:1.6;max-width:68ch;margin-bottom:16px;font-weight:500}
.prose h3{font-family:var(--display);text-transform:uppercase;font-size:clamp(19px,2.2vw,24px);line-height:1.05;margin:30px 0 10px}
/* grid + cards */
.grid{display:grid;gap:28px;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));margin:28px 0}
.grid--2{grid-template-columns:repeat(auto-fill,minmax(420px,1fr))}
.card{display:flex;flex-direction:column;background:var(--paper);border:var(--line);box-shadow:var(--shadow);padding:clamp(18px,2vw,24px)}
.card__top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:12px}
.card__id{font-family:var(--mono);font-size:12px;font-weight:700;letter-spacing:.05em;text-transform:uppercase}
.card__badges{display:flex;flex-direction:column;align-items:flex-end;gap:8px}
.card__title{margin-top:14px;font-family:var(--display);text-transform:uppercase;font-size:clamp(20px,1.9vw,26px);line-height:1;letter-spacing:-.01em}
.card__title .x{display:inline-block;background:var(--coral);padding:0 6px;font-size:.75em;vertical-align:.1em}
.card__desc{margin-top:10px;font-size:15px;line-height:1.45;font-weight:500}
.card__desc p+p{margin-top:8px}
/* meters (hotel scores) */
.meters{display:grid;gap:7px;margin-top:6px}
.meter{display:grid;grid-template-columns:92px 1fr 24px;gap:10px;align-items:center}
.meter__l{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.06em;text-transform:uppercase}
.meter__t{height:14px;border:var(--line);background:var(--paper-2);position:relative}
.meter__f{position:absolute;inset:0 auto 0 0;background:var(--ink)}
.meter.is-n .meter__f{background:var(--rust)}
.meter__v{font-family:var(--display);font-size:15px;text-align:right}
.hfoot{display:flex;justify-content:space-between;gap:12px;align-items:flex-end}
.hfoot__r{text-align:right}
.hfoot__v{font-family:var(--display);font-size:30px;line-height:1;margin-top:4px}
.hfoot__v small{font-size:14px;color:var(--ink-soft)}
/* sheet (profile) */
.sheet{background:var(--paper);border:var(--line-thick);box-shadow:var(--shadow-lg);margin:36px 0}
.bar{display:flex;align-items:center;justify-content:space-between;gap:12px;min-height:56px;background:var(--ink);color:var(--paper);padding:12px clamp(18px,3vw,28px)}
.bar__id{font-family:var(--mono);font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--yellow)}
.bar__r{display:flex;gap:8px;flex-wrap:wrap}
.sheet__intro{padding:clamp(20px,3vw,32px) clamp(20px,3vw,32px) 0;display:flex;flex-direction:column;gap:18px}
.sheet__body{padding:18px clamp(20px,3vw,32px) clamp(20px,3vw,32px);display:flex;flex-direction:column;gap:18px}
.sheet__title{font-family:var(--display);text-transform:uppercase;font-size:clamp(28px,4vw,44px);line-height:.95;letter-spacing:-.02em;max-width:20ch}
.sheet__title--sm{font-size:clamp(22px,3vw,32px)}
.lead{font-size:18px;line-height:1.5;font-weight:500;max-width:68ch}
.sec{border-top:var(--line);padding-top:16px;display:flex;flex-direction:column;gap:8px}
.sec p{font-weight:500;max-width:72ch}
.engine{background:var(--yellow);border:var(--line);box-shadow:var(--shadow-sm);padding:14px 16px;display:flex;flex-direction:column;gap:6px}
.engine p{font-weight:600}
.affine{display:inline-flex;align-items:center;gap:8px;padding:8px 12px;border:var(--line);background:var(--paper);box-shadow:var(--shadow-sm);transition:transform .12s,box-shadow .12s,background .12s}
.affine:hover{transform:translate(-2px,-2px);box-shadow:6px 6px 0 var(--ink);background:var(--yellow)}
.affine__id{font-family:var(--mono);font-size:11px;font-weight:700;letter-spacing:.05em;background:var(--ink);color:var(--yellow);padding:1px 6px}
.affine__name{font-family:var(--display);font-size:14px;line-height:1.2;text-transform:uppercase;letter-spacing:-.01em}
/* formula + big boxes */
.formula{background:var(--ink);color:var(--paper);border:var(--line-thick);box-shadow:var(--shadow-lg);padding:clamp(24px,4vw,40px);margin:32px 0;text-align:center}
.formula__f{font-family:var(--display);text-transform:uppercase;font-size:clamp(18px,3vw,30px);line-height:1.3;display:flex;flex-wrap:wrap;justify-content:center;gap:.05em .3em}
.formula__f .op{color:var(--yellow)}
.formula__res{display:inline-block;margin-top:14px;background:var(--yellow);color:var(--ink);font-family:var(--display);text-transform:uppercase;font-size:clamp(18px,3vw,30px);padding:4px 14px}
.formula .lbl{color:rgba(255,253,245,.7);margin-top:16px}
.ybox{background:var(--yellow);border:var(--line-thick);box-shadow:var(--shadow-lg);padding:clamp(22px,3.5vw,36px);margin:32px 0}
.ybox .lbl{margin-bottom:10px}
.ybox p{font-size:18px;font-weight:600;line-height:1.45;max-width:64ch}
.note{display:flex;gap:12px;align-items:flex-start;background:var(--yellow-soft);border:var(--line);padding:14px 16px;margin:20px 0;font-size:15px;font-weight:500}
.note .badge{flex:none}
.scale{border:var(--line);background:var(--paper);box-shadow:var(--shadow-sm);margin:18px 0 8px}
.scale__row{display:grid;grid-template-columns:72px 1fr;border-top:var(--line)}
.scale__row:first-child{border-top:0}
.scale__v{font-family:var(--display);font-size:22px;display:flex;align-items:center;justify-content:center;background:var(--ink);color:var(--yellow)}
.scale__t{padding:12px 14px;font-size:15px;font-weight:500}
ol.take{list-style:none;counter-reset:t;display:grid;gap:14px;margin-top:6px}
ol.take li{counter-increment:t;position:relative;padding-left:46px;font-size:17px;font-weight:600;line-height:1.45}
ol.take li::before{content:counter(t);position:absolute;left:0;top:0;width:32px;height:32px;display:flex;align-items:center;justify-content:center;background:var(--ink);color:var(--yellow);font-family:var(--display)}
/* panels (questions) */
.panel{background:var(--paper);border:var(--line-thick);box-shadow:var(--shadow);margin:28px 0}
.panel__head{background:var(--ink);padding:12px 18px;min-height:56px;display:flex;align-items:center}
.panel__title{font-family:var(--display);font-size:20px;text-transform:uppercase;color:var(--yellow)}
.panel__body{padding:clamp(18px,3vw,28px);display:flex;flex-direction:column;gap:12px}
.panel__body p{font-weight:500;max-width:72ch}
.answers{border-top:var(--line);padding-top:14px;display:grid;gap:12px}
.answer{display:grid;grid-template-columns:130px 1fr;gap:14px;align-items:start}
.answer .badge{justify-self:start;white-space:normal;text-align:left}
/* cta + footer */
.cta{background:var(--ink);color:var(--paper);border-top:var(--line-thick);margin-top:clamp(56px,7vw,96px);padding:clamp(48px,6vw,80px) 0}
.cta .h2__n{background:var(--yellow);color:var(--ink)}
.cta h2{font-family:var(--display);text-transform:uppercase;font-size:clamp(28px,4.4vw,52px);line-height:.95;max-width:20ch;padding-bottom:16px;border-bottom:3px solid rgba(255,253,245,.3);margin-bottom:22px}
.cta p{color:rgba(255,253,245,.88);max-width:68ch;margin-bottom:14px;font-size:17px;font-weight:500}
.cta__btns{display:flex;flex-wrap:wrap;gap:14px;margin-top:26px}
.cta .btn{box-shadow:4px 4px 0 var(--coral)}
footer{background:var(--ink);color:rgba(255,253,245,.65);border-top:2px solid rgba(255,253,245,.2);padding:22px 0 36px;font-family:var(--mono);font-size:11px;letter-spacing:.12em;text-transform:uppercase}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
@media (max-width:760px){
 .header__in{height:60px}
 .logo__mark{width:32px;height:32px}.logo__word{font-size:14px}
 .brand{gap:12px}.brand__lib{padding-left:12px}.brand__title{font-size:18px}.brand__ver{display:none}
 .back{display:none}
 .grid,.grid--2{grid-template-columns:1fr}
 .answer{grid-template-columns:1fr;gap:6px}
 .meter{grid-template-columns:80px 1fr 22px}
}
/* ---------------------------------------------------------- print / PDF */
@page{size:A4;margin:14mm 13mm 16mm}
@media print{
 :root{--paper:#fff}
 body{background:#fff;font-size:10.5pt}
 .header{position:static;border-bottom:var(--line-thick)}
 .header__in{height:auto;padding:2px 0 12px}
 .wrap{max-width:none;padding:0}
 .hero{break-after:page;border-bottom:0}
 .hero__in{padding:70mm 0 0}
 .hero__title{font-size:54pt;max-width:none}
 .hero__lead{font-size:14pt;max-width:none}
 .hero__actions{display:none}
 .chapter{padding-top:24px}
 .chapter{break-before:page;padding-top:0}
 .chapter--first,.chapter--flow{break-before:auto;padding-top:24px}
 .sheet__keep{break-inside:avoid}
 .grid{grid-template-columns:repeat(2,1fr);gap:16px;margin:18px 0}
 .card,.panel,.formula,.ybox,.scale,.engine,.note,.sec,.answer,.prose p{break-inside:avoid}
 .sheet{box-shadow:6px 6px 0 var(--ink);margin:20px 0;break-inside:auto}
 .bar,.sheet__title,.h2,.prose h3,.panel__head{break-after:avoid}
 .card{box-shadow:4px 4px 0 var(--ink)}
 .h2 h2{font-size:30pt}
 .affine{box-shadow:none}
 .btn--ink{display:none}
 .cta{break-before:page;margin-top:0}
}
"""

HTML = f"""<!doctype html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Positioning di un hotel</title>
<meta name="description" content="Una guida pratica per capire qual è il motore del tuo hotel (location, capital, operations o narrativa di mercato) e quale narrativa scegliere di conseguenza, con i pattern della Hotel Positioning Library.">
{font_link}
<style>{font_css}{CSS}</style>
</head>
<body>

<header class="header"><div class="wrap header__in">
 <div class="brand">
  <a class="logo" href="{SITE}/" aria-label="Hotel Positioning">{LOGO}<span class="logo__word"><span>Hotel</span><span>P<i class="logo__o"></i>sitioning</span></span></a>
  <a class="brand__lib" href="{SITE}/library"><div class="brand__title">Guida</div><div class="brand__ver">v1.0 · Francesco Astolfi</div></a>
 </div>
 <div class="header__r"><a class="back" href="{SITE}/library">← Library</a><span class="count">7 capitoli</span></div>
</div></header>

<main>
<section class="hero"><div class="wrap hero__in">
 <h1 class="hero__title"><span class="hl">Come funziona davvero</span> il positioning di un hotel</h1>
 <p class="hero__lead">Una guida pratica per capire che tipo di hotel hai, quale leva fa davvero il tuo fatturato e come costruire una narrativa di mercato coerente con la tua realtà, invece che con la moda del momento. Alla fine di ogni profilo trovi i pattern della Library che funzionano per te.</p>
 <nav class="hero__pills" aria-label="Capitoli">{pills}</nav>
 <div class="hero__actions"><a class="btn" href="#cap7">Fai l’autodiagnosi →</a><a class="btn btn--paper" href="{SITE}/library">Apri la Library</a></div>
</div></section>

<div class="wrap">

<section class="chapter chapter--first">
 {h2('01', 'cap1', 'Un hotel non è una cosa sola', 'Quello che il mercato percepisce del tuo hotel, il suo <strong>Posizionamento di Mercato</strong>, è la somma di quattro componenti. Il lavoro vero è capire quale delle quattro è la tua leva principale e investire di conseguenza.')}
 <div class="formula">
  <div class="formula__f"><span>Location</span><span class="op">+</span><span>Capital</span><span class="op">+</span><span>Operations</span><span class="op">+</span><span>Narrativa di mercato</span></div>
  <div class="formula__res">= Posizionamento di Mercato</div>
  <div class="lbl">Ogni componente da 0 a 10 · totale da 0 a 40 · percepito dal cliente</div>
 </div>
 <div class="grid">{components_html}</div>
 <div class="prose">
  <p>Puoi vincere spingendo su una sola componente con le altre nella media, oppure con due o tre alte. Tutte e quattro alte è ovvio ma raro. Tutte e quattro basse è l’hotel commodity che sopravvive a fatica.</p>
  <p>Non confondere due cose. Il <strong>Posizionamento di Mercato</strong> è il risultato percepito dal cliente. La <strong>Narrativa di mercato</strong> è una delle quattro componenti che lo determinano: la scelta deliberata di come racconti il tuo hotel. Delle quattro, è l’unica su cui puoi lavorare in fretta, con un costo contenuto e senza toccare i muri.</p>
  <h3>Dove sei: la location</h3>
  <p>La location non è solo un indirizzo. È il flusso di clienti che arriva da solo e la ragione per cui un turista sceglie una zona invece di un’altra.</p>
 </div>
 <div class="scale">
  <div class="scale__row"><div class="scale__v">10</div><div class="scale__t">Portofino, Capri, Ravello, Positano, il centro storico di Venezia e di Firenze, Taormina: l’hotel vende prima ancora che il proprietario parli.</div></div>
  <div class="scale__row"><div class="scale__v">6-7</div><div class="scale__t">Rimini, Jesolo, Senigallia, Grado, Caorle: flussi stabili ed estate forte, ma la tua fetta te la devi conquistare.</div></div>
  <div class="scale__row"><div class="scale__v">5</div><div class="scale__t">Un 4 stelle a Modena, Padova, Verona, Brescia: flussi business e culturali, nessuna iconicità automatica.</div></div>
  <div class="scale__row"><div class="scale__v">3-4</div><div class="scale__t">Un piccolo paese dell’entroterra abruzzese o del Monferrato: la location non aiuta, ostacola. Chi viene lo fa per una ragione precisa.</div></div>
 </div>
 <div class="prose">
  <h3>Cosa hai costruito: il capital</h3>
  <p>Il capital è quanto hai investito nella struttura fisica: non il valore immobiliare, ma la qualità che il cliente percepisce in camera, in bagno, al ristorante, al bar. Camere rifatte nel 2024 con un investimento serio comunicano una cosa; moquette del 2003 e materassi stanchi ne comunicano un’altra, qualunque cosa dica la brochure.</p>
 </div>
 <div class="ybox"><div class="lbl">Regola</div><p>Il capital pesa moltissimo nei primi tre minuti dell’esperienza. Nessuna narrativa salva un bagno brutto.</p></div>
 <div class="prose">
  <h3>Come lavori ogni giorno: le operations</h3>
  <p>Accoglienza al check-in, pulizia costante, puntualità del ristorante, risposta alle recensioni, revenue management che adatta i prezzi, formazione del personale, gestione dei fornitori. Un hotel con componenti nella media ma operations eccellenti sopravvive e cresce. Uno con componenti alte ma operations scadenti brucia la reputazione in un anno e mezzo. Sono la componente più sottovalutata dai proprietari e la più decisiva nel lungo periodo.</p>
  <h3>Come ti racconti: la narrativa di mercato</h3>
  <p>È la promessa che fai, il segmento che decidi di servire, l’identità che costruisci: la ragione precisa per cui un cliente deve scegliere te e pagare il prezzo che chiedi. Senza narrativa esisti come hotel generico, al prezzo che decidono le OTA. Una narrativa forte può poggiare sulla storia della famiglia, su un meccanismo operativo distintivo, su un segmento molto specifico, sull’opposizione a un format dominante, su una visione del mondo.</p>
  <p>Non è un’etichetta di marketing. È una scelta strategica che decide cosa offri, chi servi, come ti organizzi e come comunichi. E, una volta scelta, va mantenuta ogni giorno.</p>
 </div>
</section>

<section class="chapter chapter--flow">
 {h2('02', 'cap2', 'Due hotel uguali, narrative diverse')}
 <div class="prose"><p>Due hotel con la stessa location, lo stesso capital e le stesse operations possono raccontarsi in modi opposti. Un 4 stelle di dieci camere su una collina umbra può diventare “boutique romantico per coppie”, “ritiro silenzioso per professionisti in burnout” o “casa di campagna per matrimoni intimi”. Stesse camere, stesso staff. Clienti diversi, prezzi diversi, posizionamento diverso.</p></div>
 <div class="ybox"><div class="lbl">Il punto</div><p>La domanda giusta non è “qual è la narrativa più bella”, ma “qual è la narrativa coerente con le altre tre componenti che ho”. La narrativa deve amplificare quello che hai, oppure creare valore dove le altre componenti non arrivano.</p></div>
</section>

<section class="chapter chapter--flow">
 {h2('03', 'cap3', 'Qual è il motore del tuo hotel', f'Esistono quattro profili, uno per componente. Riconoscere il tuo cambia la risposta su dove investire e su quale narrativa costruire. Per ogni profilo trovi i pattern della Hotel Positioning Library più coerenti, con il livello minimo di operations che ciascuno richiede.')}
 {profiles_html}
</section>

<section class="chapter">
 {h2('04', 'cap4', 'I profili misti sono la norma', 'Nella realtà i profili puri sono rari: la maggior parte degli hotel ha due o tre componenti alte. La narrativa deve allora raccontare l’incrocio, non un elemento solo.')}
 <div class="grid">{mixed_html}</div>
</section>

<section class="chapter chapter--flow">
 {h2('05', 'cap5', 'Nove hotel a confronto', 'La teoria diventa concreta guardando dei casi: nove hotel <strong>ipotetici</strong> con componenti diverse, il loro Posizionamento di Mercato e un fatturato annuo plausibile.')}
 <div class="note"><span class="badge is-nascente">Attenzione</span><span>Hotel e fatturati sono esempi costruiti per spiegare il metodo, non dati di mercato. Il fatturato dipende dal posizionamento ma anche da numero di camere, giorni di apertura e prezzo medio raggiungibile: un posizionamento alto non garantisce da solo un fatturato alto.</span></div>
 <div class="grid grid--hotels">{hotels_html}</div>
 <div class="prose"><h3>I confronti che contano</h3></div>
 <div class="grid grid--2">{vs_html}</div>
 <div class="ybox">
  <div class="lbl">Le quattro letture da portare via</div>
  <ol class="take">
   <li>Il Posizionamento di Mercato è la somma delle quattro componenti. La narrativa è una delle quattro: può essere la leva principale oppure amplificare le altre.</li>
   <li>Un posizionamento alto non significa automaticamente un fatturato alto: contano anche dimensione, giorni di apertura e prezzo raggiungibile (Positano contro Linate).</li>
   <li>La location iconica da sola non garantisce il fatturato più alto. Spesso chi si lamenta della location ha un problema altrove: una narrativa mai costruita.</li>
   <li>Negli esempi di questa guida, a parità delle altre tre componenti, la sola narrativa sposta il fatturato stimato tra il 50% e il 65%. Sono stime illustrative, ma mostrano perché è la leva più accessibile: non richiede grandi investimenti strutturali.</li>
  </ol>
 </div>
</section>

<section class="chapter">
 {h2('06', 'cap6', 'Due regole valide per tutti')}
 {sheet('Regola 01', [('Operations', 'is-t2')], 'Regola', 'Le operations devono mantenere la promessa',
        'La narrativa crea aspettative che la gestione deve soddisfare ogni giorno. La narrativa è una promessa; le operations sono il pagamento quotidiano di quella promessa.', [
        sec('Tre modi di tradire la promessa', '<p>Prometti silenzio e il wifi “che non c’è” funziona al bar. Prometti cucina del territorio e il cuoco cambia ogni tre mesi. Prometti un servizio personale e rispondi alle recensioni negative con un messaggio automatico.</p>'),
        sec('Cosa succede', '<p>Se non la mantieni, la narrativa amplifica il danno: i clienti attirati dalla promessa se ne vanno delusi e scrivono recensioni proprio su ciò che avevi promesso.</p>'),
        '<div class="engine"><div class="lbl">Soglia operativa</div><p>Se le recensioni non superano in media 4,3 su 5, lo staff non è formato e stabile, il revenue management non è attivo e le criticità non trovano risposta rapida, una narrativa radicale non è la mossa giusta. Prima si sistemano le operations, poi si lavora sulla narrativa.</p></div>'])}
 {sheet('Regola 02', [('Mercato', 'is-t2')], 'Regola', 'La narrativa deve stare dentro un business che regge',
        'Esiste anche la trappola opposta: una narrativa troppo stretta per il mercato che location e capital ti permettono di raggiungere.', [
        sec('Troppo stretta', '<p>Un hotel 100% vegano di undici camere in una valle remota, con prezzi alti, ha una promessa perfetta sulla carta ma un bacino di clienti che rischia di non bastare.</p>'),
        sec('Il caso Selina', '<p>Un posizionamento forte non salva un modello di business sbagliato. Selina, la catena globale di hub per nomadi digitali, aveva una narrativa chiarissima ma è cresciuta in fretta grazie al debito: a luglio 2024 la società è entrata in amministrazione controllata nel Regno Unito e ad agosto il business è stato venduto.</p>'),
        '<div class="engine"><div class="lbl">Come uscirne</div><p>La narrativa deve restringere abbastanza da creare identità, non così tanto da chiudere il mercato. Spesso la soluzione non è radicalizzare meno, ma scegliere un asse altrettanto radicale con un mercato più ampio.</p></div>'])}
</section>

<section class="chapter">
 {h2('07', 'cap7', 'Tre domande per capire che hotel sei', 'Prima di investire un euro nella narrativa, rispondi onestamente a tre domande.')}
 {q_html}
</section>

</div>

<section class="cta"><div class="wrap">
 <span class="h2__n">Cosa fare adesso</span>
 <h2>Dalla diagnosi al pattern giusto</h2>
 <p>Location, capital, operations e narrativa di mercato contribuiscono tutte al posizionamento. La narrativa giusta dipende dal tuo profilo: un hotel Location-driven racconta il luogo, uno Operations-driven racconta l’affidabilità con meccanismi visibili, uno Narrativa-driven costruisce valore dove le altre componenti non arrivano.</p>
 <p>Se dopo le tre domande la narrativa è la tua leva, il passo successivo è scegliere il pattern giusto. La Hotel Positioning Library ne raccoglie {N_PAT}, osservati in hotel reali in Italia e nel mondo, ognuno con il profilo per cui funziona e il livello di operations che richiede. Se invece la risposta alla prima domanda è stata no, la narrativa può aspettare: lavora prima su quello che serve davvero.</p>
 <div class="cta__btns"><a class="btn" href="{SITE}/library">Apri la Library · hotelpositioning.com/library</a><a class="btn btn--paper" href="{SITE}/">Candidati per l’analisi</a></div>
</div></section>
</main>

<footer><div class="wrap"><span>Francesco Astolfi · Hotel Positioning</span><span>hotelpositioning.com · Rimini 2026</span></div></footer>
</body>
</html>
"""

name = 'positioning-hotel-guida.html'
out = os.path.join(HERE, name)
open(out, 'w', encoding='utf-8').write(HTML)
print('written', out, len(HTML))
