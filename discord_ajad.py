# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

See variant genereerib tabeli kasutajate postituste sõltumise kellaajast.

Andmete kogumiseks: https://dht.chylex.com/
Andmeformaat:
data:
    kanali kood
        postituse kood.
            m - sõnum
            t - ajatempel millisekundites
            u - kasutaja kohalik id
            a - lisad
                <index 0..>
                url - veebiaadress faili, pildi, lingini
            e - ka lisa
                type - video, link, article, gifv, rich, image
                url
meta:
    channels (dict)
        kanali id
            name
            server
    servers - serveri(te) info
        name
        type
    userindex - list kasutajate ID-ga
    users - dict kasutaja globaalse ID ja nime sidumine.
        name - kasutaja kuvatav nimi
"""

with open('dht.txt', encoding='utf8') as f:
    file = f.read()
archive = eval(file)
users = dict()
lyhi = dict()
times = set()
import datetime
for x in range(len(archive['meta']['userindex'])):
    # Viime lokaalse ID vastavusse kasutajanimega
    users[x] = {'n': archive['meta']['users'][archive['meta']['userindex'][x]]['name'], 'count': dict(), 'lens': dict(),
                'times': dict()}
channels = []
for c in archive['data']:  # c = kanali id
    print(c[0], end='')
    cur_name = archive['meta']['channels'][c]['name']  # Praeguse kanali nimi
    cur_name = cur_name.split('_')[0]
    channels.append(cur_name)
    for m in sorted(archive['data'][c]):  # m = sõnumi ID
        message = archive['data'][c][m]
        if len(message['m'].strip().split()) < 2:  # Ühesõnaliste sõnumitega opereerimine
            if message['u'] not in lyhi:
                lyhi[message['u']] = 0  # Loendab lühikesi sõnumeid
            lyhi[message['u']] += 1
        time=datetime.datetime.fromtimestamp(message['t'] // 1000)
        wk=time.weekday()
        h=time.hour
        # Nädalapäev: E = 0, P = 6
        # print(time.date(),time.time(),wk,h)
        uid = message['u']
        if cur_name not in users[uid]['count']:  # Kui see sõnum on kasutaja
            users[uid]['count'][cur_name] = 0  # esimene sõnum antud kanalis
            users[uid]['lens'][cur_name] = 0  # init loendurid
            users[uid]['times'][cur_name] = [0]*168  # Iga tunni jaoks
        users[uid]['count'][cur_name] += 1
        users[uid]['lens'][cur_name] += len(message['m'])
        users[uid]['times'][cur_name][24*wk+h]+=1
print()
channels.sort()
ajad = list()
head=[]
for wk in 'ETKNRLP':
    for hr in range(24):
        head.append(wk+' '+str(hr))
header = '\t'.join(['Nimi','Kanal']+head)
ajad.append(header)
for x in list(users):
    total=[]
    for c in sorted(users[x]['times']):  # Iga kanaliga
        total.append(users[x]['times'][c])
        ajad.append('\t'.join([users[x]['n'],c]+list(map(str,total[-1]))))
    total=list(map(sum,list(zip(*total))))
    ajad.append('\t'.join([users[x]['n'],'Kokku']+list(map(str,total))))
    # print(users[x]['times'])
with open('d_out_ajatabel.txt','w',encoding='utf8') as f:
    f.write('\n'.join(ajad))
c = 1
print('done')
