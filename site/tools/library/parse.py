import re, json, sys
src = open(sys.argv[1], encoding='utf-8').read()
lines = [l.strip() for l in src.split('\n')]
lines = [l for l in lines if l]
start = lines.index('Rimescola') + 1
L = lines[start:]
items = []
i = 0
code_re = re.compile(r'^([A-L]\d\d)$')
cat_re = re.compile(r'^CAT #(\d+)$')
ex_re = re.compile(r'^(.*?)(T[123])(🇮🇹 ITA)?(.*)$')
def stage(s):
    m = re.match(r'^PIN \+(\w+)$', s); return m.group(1).capitalize()
while i < len(L):
    s = L[i]
    m = code_re.match(s); mc = cat_re.match(s)
    if m:
        it = {'id': s, 'type': 'pattern', 'stage': stage(L[i+1]), 'family': L[i+2],
              'title': L[i+3].lstrip('# ').strip(), 'desc': L[i+4], 'examples': [], 'pioneer': False}
        it['fam'] = it['family'][0]
        i += 5
        if L[i] == 'PATTERN NASCENTE':
            it['pioneer'] = True; it['note'] = L[i+1]; i += 2
        else:
            n = int(re.match(r'ESEMPI VERIFICATI \((\d+)\)', L[i]).group(1)); i += 1
            for _ in range(n):
                e = ex_re.match(L[i]); i += 1
                ex = {'name': e.group(1).strip(), 'tier': e.group(2), 'ita': bool(e.group(3))}
                flag = e.group(4).replace('⚠', '').strip()
                if flag: ex['flag'] = flag
                if i < len(L) and re.match(r'^\+(\d+) pattern$', L[i]):
                    ex['more'] = int(L[i][1:].split()[0]); i += 1
                it['examples'].append(ex)
            assert len(it['examples']) == n
        items.append(it)
    elif mc:
        it = {'id': 'CAT' + mc.group(1).zfill(2), 'num': int(mc.group(1)), 'type': 'categoria', 'stage': stage(L[i+1]),
              'family': L[i+2], 'title': L[i+3].lstrip('# ').strip(), 'desc': L[i+4]}
        assert L[i+5] == 'Esempio:'
        lm = re.match(r'^\[(.*?) ↗\]\((.*?)\)\s*—\s*(.*)$', L[i+6])
        it['example'] = {'name': lm.group(1), 'url': lm.group(2), 'place': lm.group(3), 'note': L[i+7]}
        assert L[i+8].startswith('↳')
        it['related'] = re.findall(r'[A-L]\d\d', L[i+9])
        i += 10
        items.append(it)
    else:
        raise SystemExit('unexpected: %r at %d' % (s, i))
# mark italian category examples by name match with flagged pattern examples
ita_names = {e['name'] for it in items if it['type']=='pattern' for e in it['examples'] if e['ita']}
for it in items:
    if it['type']=='categoria':
        it['example']['ita'] = it['example']['name'] in ita_names
        it['ita'] = it['example']['ita']
    else:
        it['ita'] = any(e['ita'] for e in it['examples'])
json.dump(items, open(sys.argv[2],'w',encoding='utf-8'), ensure_ascii=False, indent=1)
P=[x for x in items if x['type']=='pattern']; C=[x for x in items if x['type']=='categoria']
print(len(items), len(P), len(C))
from collections import Counter
print(Counter(x['stage'] for x in P), Counter(x['stage'] for x in C))
print('ita', sum(x['ita'] for x in P), sum(x['ita'] for x in C), 'pioneer', sum(x['pioneer'] for x in P))
print(Counter(f for x in P for f in [x['family']]))
print(Counter(e.get('flag') for x in P for e in x['examples']), Counter(e['tier'] for x in P for e in x['examples']))
print(sorted(ita_names)); print(len({e['name'] for x in P for e in x['examples']}))
print([ (x['id'],x['example']['name'],x['ita']) for x in C if x['ita']])
