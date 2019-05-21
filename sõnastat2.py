# Daily top
# Eesmärk teha skript, mis leiab iga päeva populaarseimad märksõnad.
import datetime
import urllib.parse
if not True:
    import estnltk
    from estnltk import Text
# datetime.datetime.fromtimestamp()
# datetime.datetime.fromtimestamp(x-x%(24*3600)-7200)  # Päeva täpsus
OUTPUT_FOLDER='java 2019/'
data=[]
with open(OUTPUT_FOLDER+'disc_sõnapilveks.txt', encoding='utf-8') as f:
    head=f.readline()
    for i in f:
        t=i.split('\t')
        for i in range(4):
            t[i]=int(t[i])
        t[4]=' '.join(urllib.parse.unquote(t[4].strip()).split())
        data.append(t)
data.sort(key=lambda x:x[3])
with open(OUTPUT_FOLDER+'disc_sorted.txt', 'w',encoding='utf-8') as f:
    f.write(head)
    for i in data:
        print(*i, sep='\t', file=f)
