"""Discordi sõnapilve statistika."""

import json

with open('sõnastats.txt', encoding='utf-8') as f:
    stats = json.loads(f.read())
with open('users.py',encoding='utf-8') as f:
    exec(f.read())
with open('dht.txt', encoding='utf8') as f:
    file = f.read()
    indexes = eval(file)['meta']['userindex']
c=1
f=open('ergoOnHull.txt', 'w', encoding='utf-8')
for i in sorted(stats['-1'], key=lambda x:stats['-1'][x], reverse=True)[:1500]:
    try:print(c,i, stats['-1'][i], sep='\t', file=f)
    except:pass
    c+=1
f.close()
