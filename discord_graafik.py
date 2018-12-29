# -*- coding: UTF-8 -*-
"""Asjandus discordi json-arhiivi töötlemiseks."""

"""
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
        print(datetime.datetime.fromtimestamp(message['t'] // 1000))
        times.add(message['t'] // 10000 - 306788430)  # 10 sekundi täpsusega
        uid = message['u']
        if cur_name not in users[uid]['count']:  # Kui see sõnum on kasutaja
            users[uid]['count'][cur_name] = 0  # esimene sõnum antud kanalis
            users[uid]['lens'][cur_name] = 0  # init loendurid
            users[uid]['times'][cur_name] = set()
        users[uid]['count'][cur_name] += 1
        users[uid]['lens'][cur_name] += len(message['m'])
        users[uid]['times'][cur_name].add(message['t'] // 10000 - 306788430)
print()
times = list(sorted(times))
channels.sort()
pikkused = list()
kogus = list()
keskmine_pikkus = list()
sisukus = list()
header = '\t'.join(['Nimi'] + channels + ['Kokku'])

print(len(times))
import pygame,colorsys
colors=dict()
c=0
for i in channels:
    colors[i]=tuple(map(lambda x:255*x,colorsys.hsv_to_rgb(0.618033988749895*c,1,1)))
    c+=1
pygame.init()
lava = pygame.display.set_mode((min(len(times),10000), len(users)), 0, 32)
#pygame.draw.rect(lava, (255,255,255),(5,5,10,10))
pygame.display.update()
for x in list(users):
    count = 0
    c_len = 0
    for c in users[x]['times']:  # Iga kanaliga
        for stamp in users[x]['times'][c]:  # Iga ajatempel 
            pygame.draw.rect(lava, colors[c],(times.index(stamp)%10000,x,2,3))
    users[x]['count']['total'] = count
    users[x]['lens']['total'] = c_len
    print(x)
    pygame.display.update()

sisukus.append('Jrk.\tNimi\tLühike\tKõik\t%')
c = 1
print(len(times))
print('done')
pygame.image.save(lava, "screenshot.jpeg")
for i in sorted(colors):
    print(i,colors[i])
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
