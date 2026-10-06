import json, sys, html
from collections import OrderedDict
here = sys.argv[1]; out = sys.argv[2]
D = json.load(open(here + '/data.json', encoding='utf-8'))
T = open(here + '/template.html', encoding='utf-8').read()
e = lambda s: html.escape(str(s), quote=True)
P = [d for d in D if d['type'] == 'pattern']; C = [d for d in D if d['type'] == 'categoria']
fams = OrderedDict()
for d in P: fams.setdefault(d['fam'], d['family'])
FLAG = {'DA VERIFICARE': ('warn', 'Da verificare'), 'ACQUISITO': ('gone', 'Acquisito'), 'VENDUTO': ('gone', 'Venduto')}
def card(d):
    pin = ('<button type="button" class="pin" data-pin="{id}" aria-pressed="false"><span class="off">Fissa +</span>'
           '<span class="on">Fissato ✓</span><span class="sr"> {lab}</span></button>')
    if d['type'] == 'pattern':
        h = ['<article class="lc" id="%s" data-type="pattern" data-fam="%s" data-stage="%s">' % (d['id'], d['fam'], d['stage'])]
        h.append('<div class="lc-top"><span class="lc-code">%s</span>%s</div>' % (d['id'], pin.format(id=d['id'], lab=e(d['id'] + ' ' + d['title']))))
        h.append('<p class="lc-fam">%s</p><h3>%s</h3><p class="lc-desc">%s</p>' % (e(d['family']), e(d['title']), e(d['desc'])))
        b = '<span class="mat s-%s">Pattern %s</span>' % (d['stage'].lower(), d['stage'].lower())
        if d['ita']: b += '<span class="mat ita">🇮🇹 Caso italiano</span>'
        h.append('<div class="badges">%s</div>' % b)
        if d['pioneer']:
            h.append('<p class="pioneer"><b>Spazio libero</b>%s</p>' % e(d['note']))
        else:
            lis = []
            for x in d['examples']:
                s = '<li><b>%s</b><span class="tg t" title="Livello di verifica %s">%s</span>' % (e(x['name']), x['tier'], x['tier'])
                if x['ita']: s += '<span class="tg it">🇮🇹 ITA</span>'
                if x.get('flag'): c, l = FLAG[x['flag']]; s += '<span class="tg %s">%s</span>' % (c, l)
                if x.get('more'): s += '<span class="more" title="Compare anche in altri %d pattern">+%d pattern</span>' % (x['more'], x['more'])
                lis.append(s + '</li>')
            h.append('<div class="ex"><p class="ex-h">Esempi verificati · %d</p><ul>%s</ul></div>' % (len(lis), ''.join(lis)))
    else:
        x = d['example']
        h = ['<article class="lc cat" id="%s" data-type="categoria" data-stage="%s">' % (d['id'], d['stage'])]
        h.append('<div class="lc-top"><span class="lc-code"><small>CAT</small>#%d</span>%s</div>' % (d['num'], pin.format(id=d['id'], lab=e('categoria ' + d['title']))))
        h.append('<p class="lc-fam">Categoria emergente</p><h3>%s</h3><p class="lc-desc">%s</p>' % (e(d['title']), e(d['desc'])))
        b = '<span class="mat s-%s">Stadio: %s</span>' % (d['stage'].lower(), d['stage'].lower())
        if d['ita']: b += '<span class="mat ita">🇮🇹 Caso italiano</span>'
        h.append('<div class="badges">%s</div>' % b)
        rel = ''.join('<button type="button" data-goto="%s" aria-label="Vai al pattern %s">%s</button>' % (r, r, r) for r in d['related'])
        h.append('<div class="cex"><p class="ex-h">Esempio</p><a href="%s" target="_blank" rel="noopener">%s ↗</a><span class="place">%s</span><p>%s</p></div>'
                 % (e(x['url']), e(x['name']), e(x['place']), e(x['note'])))
        h.append('<div class="rel"><span>Pattern affini</span>%s</div>' % rel)
    h.append('</article>')
    return ''.join(h)
cards = '\n'.join(card(d) for d in D)
stage_chips = '\n'.join('<button type="button" class="fchip" data-f="stage" data-v="%s" aria-pressed="false">%s</button>' % (v, l) for v, l in
    [('Nascente', 'Nascente · %d' % sum(d['stage']=='Nascente' for d in D)), ('Emergente', 'Emergente · %d' % sum(d['stage']=='Emergente' for d in D)),
     ('Consolidato', 'Consolidato · %d' % sum(d['stage']=='Consolidato' for d in D)), ('Maturo', 'Maturo · %d' % sum(d['stage']=='Maturo' for d in D))])
fam_chips = '\n'.join('<button type="button" class="fchip" data-f="fam" data-v="%s" aria-pressed="false">%s</button>' % (k, e(v)) for k, v in fams.items())
ld = {"@context": "https://schema.org", "@type": "CollectionPage",
      "name": "La library dei posizionamenti per hotel indipendenti",
      "description": "69 pattern e 19 categorie emergenti per differenziare un hotel indipendente, con esempi reali verificati.",
      "url": "https://hotelpositioning.com/library/", "inLanguage": "it", "version": "4.0",
      "isPartOf": {"@type": "WebSite", "name": "Hotel Positioning", "url": "https://hotelpositioning.com/"},
      "author": {"@type": "Person", "name": "Francesco Astolfi", "url": "https://hotelpositioning.com/francesco/"},
      "about": "Brand positioning per hotel indipendenti",
      "mainEntity": {"@type": "ItemList", "numberOfItems": len(D), "itemListElement": [
          {"@type": "ListItem", "position": i + 1, "url": "https://hotelpositioning.com/library/#" + d['id'],
           "name": (d['id'] if d['type']=='pattern' else 'Categoria #%d' % d['num']) + ' · ' + d['title']} for i, d in enumerate(D)]}}
keep = ['id','type','stage','fam','family','title','desc','examples','pioneer','note','num','example','related','ita']
data = [{k: d[k] for k in keep if k in d} for d in D]
js = json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')
rep = {'%%LDJSON%%': json.dumps(ld, ensure_ascii=False), '%%CARDS%%': cards, '%%DATA%%': js,
       '%%STAGE_CHIPS%%': stage_chips, '%%FAM_CHIPS%%': fam_chips,
       '%%N_ALL%%': str(len(D)), '%%N_PAT%%': str(len(P)), '%%N_CAT%%': str(len(C)), '%%N_FAM%%': str(len(fams)),
       '%%N_ITA%%': str(sum(d['ita'] for d in D)), '%%N_PIONEER%%': str(sum(d['pioneer'] for d in P))}
for k, v in rep.items(): T = T.replace(k, v)
assert '%%' not in T
import os; os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(T)
print('ok', len(T))
