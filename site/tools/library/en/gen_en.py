import json, sys, html
from collections import OrderedDict
here = sys.argv[1]; out = sys.argv[2]
D = json.load(open(here + '/data_en.json', encoding='utf-8'))
T = open(here + '/template_en.html', encoding='utf-8').read()
e = lambda s: html.escape(str(s), quote=True)
P = [d for d in D if d['type'] == 'pattern']; C = [d for d in D if d['type'] == 'categoria']
fams = OrderedDict()
for d in P: fams.setdefault(d['fam'], d['family'])
FLAG = {'DA VERIFICARE': ('warn', 'To be verified'), 'ACQUISITO': ('gone', 'Acquired'), 'VENDUTO': ('gone', 'Sold')}
IT = {'Nascent': 'nascente', 'Emerging': 'emergente', 'Established': 'consolidato', 'Mature': 'maturo'}
plural = lambda n: 'pattern' if n == 1 else 'patterns'
def card(d):
    pin = ('<button type="button" class="pin" data-pin="{id}" aria-pressed="false"><span class="off">Pin +</span>'
           '<span class="on">Pinned ✓</span><span class="sr"> {lab}</span></button>')
    if d['type'] == 'pattern':
        h = ['<article class="lc" id="%s" data-type="pattern" data-fam="%s" data-stage="%s">' % (d['id'], d['fam'], d['stage'])]
        h.append('<div class="lc-top"><span class="lc-code">%s</span>%s</div>' % (d['id'], pin.format(id=d['id'], lab=e(d['id'] + ' ' + d['title']))))
        h.append('<p class="lc-fam">%s</p><h3>%s</h3><p class="lc-desc">%s</p>' % (e(d['family']), e(d['title']), e(d['desc'])))
        b = '<span class="mat s-%s">%s pattern</span>' % (IT[d['stage']], d['stage'])
        if d['ita']: b += '<span class="mat ita">🇮🇹 Italian case</span>'
        h.append('<div class="badges">%s</div>' % b)
        if d['pioneer']:
            h.append('<p class="pioneer"><b>Open space</b>%s</p>' % e(d['note']))
        else:
            lis = []
            for x in d['examples']:
                s = '<li><b>%s</b><span class="tg t" title="Verification level %s">%s</span>' % (e(x['name']), x['tier'], x['tier'])
                if x['ita']: s += '<span class="tg it">🇮🇹 ITA</span>'
                if x.get('flag'): c, l = FLAG[x['flag']]; s += '<span class="tg %s">%s</span>' % (c, l)
                if x.get('more'): s += '<span class="more" title="Also appears in %d other %s">+%d %s</span>' % (x['more'], plural(x['more']), x['more'], plural(x['more']))
                lis.append(s + '</li>')
            h.append('<div class="ex"><p class="ex-h">Verified examples · %d</p><ul>%s</ul></div>' % (len(lis), ''.join(lis)))
    else:
        x = d['example']
        h = ['<article class="lc cat" id="%s" data-type="categoria" data-stage="%s">' % (d['id'], d['stage'])]
        h.append('<div class="lc-top"><span class="lc-code"><small>CAT</small>#%d</span>%s</div>' % (d['num'], pin.format(id=d['id'], lab=e('category ' + d['title']))))
        h.append('<p class="lc-fam">Emerging category</p><h3>%s</h3><p class="lc-desc">%s</p>' % (e(d['title']), e(d['desc'])))
        b = '<span class="mat s-%s">Stage: %s</span>' % (IT[d['stage']], d['stage'].lower())
        if d['ita']: b += '<span class="mat ita">🇮🇹 Italian case</span>'
        h.append('<div class="badges">%s</div>' % b)
        rel = ''.join('<button type="button" data-goto="%s" aria-label="Go to pattern %s">%s</button>' % (r, r, r) for r in d['related'])
        h.append('<div class="cex"><p class="ex-h">Example</p><a href="%s" target="_blank" rel="noopener">%s ↗</a><span class="place">%s</span><p>%s</p></div>'
                 % (e(x['url']), e(x['name']), e(x['place']), e(x['note'])))
        h.append('<div class="rel"><span>Related patterns</span>%s</div>' % rel)
    h.append('</article>')
    return ''.join(h)
cards = '\n'.join(card(d) for d in D)
stage_chips = '\n'.join('<button type="button" class="fchip" data-f="stage" data-v="%s" aria-pressed="false">%s</button>' % (v, l) for v, l in
    [(v, '%s · %d' % (v, sum(d['stage']==v for d in D))) for v in ('Nascent', 'Emerging', 'Established', 'Mature')])
fam_chips = '\n'.join('<button type="button" class="fchip" data-f="fam" data-v="%s" aria-pressed="false">%s</button>' % (k, e(v)) for k, v in fams.items())
ld = {"@context": "https://schema.org", "@type": "CollectionPage",
      "name": "The positioning library for independent hotels",
      "description": "69 patterns and 19 emerging categories to differentiate an independent hotel, with verified real examples.",
      "url": "https://hotelpositioning.com/en/library/", "inLanguage": "en", "version": "4.0",
      "isPartOf": {"@type": "WebSite", "name": "Hotel Positioning", "url": "https://hotelpositioning.com/en/"},
      "author": {"@type": "Person", "name": "Francesco Astolfi", "url": "https://hotelpositioning.com/en/francesco/"},
      "about": "Brand positioning for independent hotels",
      "mainEntity": {"@type": "ItemList", "numberOfItems": len(D), "itemListElement": [
          {"@type": "ListItem", "position": i + 1, "url": "https://hotelpositioning.com/en/library/#" + d['id'],
           "name": (d['id'] if d['type']=='pattern' else 'Category #%d' % d['num']) + ' · ' + d['title']} for i, d in enumerate(D)]}}
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
