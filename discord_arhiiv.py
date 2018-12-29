# -*- coding: UTF-8 -*-
"""Asjandus discordi json-arhiivi töötlemiseks."""

"""
Andmete kogumiseks: https://dht.chylex.com/
Andmeformaat:
data:
    kanali kood
        postituse kood.
            m - sõnum
            t - sõnumi id?
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
f = open('disc_sõnapilveks.txt', 'w', encoding='utf8')
for x in range(len(archive['meta']['userindex'])):
    # Viime lokaalse ID vastavusse kasutajanimega
    users[x] = {'n': archive['meta']['users'][archive['meta']['userindex'][x]]['name'], 'count': dict(), 'lens': dict()}
channels = []
for c in archive['data']:  # c = kanali id
    print(c)
    cur_name = archive['meta']['channels'][c]['name']  # Praeguse kanali nimi
    cur_name = cur_name.split('_')[0]
    channels.append(cur_name)
    for m in sorted(archive['data'][c]):  # m = sõnumi ID
        message = archive['data'][c][m]
        if len(message['m'].strip().split()) < 2:  # Ühesõnaliste sõnumitega opereerimine
            if message['u'] not in lyhi:
                lyhi[message['u']] = 0  # Loendab lühikesi sõnumeid
            lyhi[message['u']] += 1
            # continue                                  # Lühisõnumi saab vahele jätta
        print(message['m'].lower(), file=f)  # Kopeeri sõnum faili
        uid = message['u']
        if cur_name not in users[uid]['count']:  # Kui see sõnum on kasutaja
            users[uid]['count'][cur_name] = 0  # esimene sõnum antud kanalis
            users[uid]['lens'][cur_name] = 0  # init loendurid
        users[uid]['count'][cur_name] += 1
        users[uid]['lens'][cur_name] += len(message['m'])
f.close()
channels.sort()
pikkused = list()
kogus = list()
keskmine_pikkus = list()
sisukus = list()
header = '\t'.join(['Nimi'] + channels + ['Kokku'])
for x in list(users):
    count = 0
    c_len = 0
    for c in users[x]['count']:
        count += users[x]['count'][c]
        c_len += users[x]['lens'][c]
    users[x]['count']['total'] = count
    users[x]['lens']['total'] = c_len
    if count < 3:
        continue
    out1 = [users[x]['n']]
    out2 = [users[x]['n']]
    out3 = [users[x]['n']]
    for kanal in channels:
        if kanal in users[x]['count']:
            out1.append(str(users[x]['lens'][kanal]))
            out2.append(str(users[x]['count'][kanal]))
            out3.append(str(round(users[x]['lens'][kanal] / users[x]['count'][kanal], 3)).replace('.', ','))
        else:
            out1.append('0')
            out2.append('0')
            out3.append('0')
    out1.append(str(users[x]['lens']['total']))
    out2.append(str(users[x]['count']['total']))
    out3.append(str(round(users[x]['lens']['total'] / users[x]['count']['total'], 3)).replace('.', ','))
    pikkused.append('\t'.join(out1))
    kogus.append('\t'.join(out2))
    keskmine_pikkus.append('\t'.join(out3))
with open('d_out1.txt', 'w', encoding='utf-8') as f:
    print('\n'.join([header] + pikkused), file=f)
with open('d_out2.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join([header] + kogus))
with open('d_out3.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join([header] + keskmine_pikkus))
sisukus.append('Jrk.\tNimi\tLühike\tKõik\t%')
c = 1
for i in sorted(lyhi, key=lambda x: users[x]['count']['total'], reverse=True):
    out = '\t'.join([str(c), users[i]['n'], str(lyhi[i]), str(users[i]['count']['total']),
                     str(round(lyhi[i] / users[i]['count']['total'] * 100, 2)).replace('.', ',')])
    # print(out)
    sisukus.append(out)
    c += 1

with open('d_out4.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(sisukus))
