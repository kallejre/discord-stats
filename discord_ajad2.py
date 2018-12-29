# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

See variant võiks olla interaktiivne lähenemine probleemile.


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
import datetime
for x in range(len(archive['meta']['userindex'])):
    # Viime lokaalse ID vastavusse kasutajanimega
    users[x] = {'n': archive['meta']['users'][archive['meta']['userindex'][x]]['name'], 'count': dict(), 'lens': dict(),
                'times': dict()}
users[-1] = {'n': 'Kõik', 'count': dict(), 'lens': dict(),
                'times': dict()}
channels = []
# Kategooria peaks algama suure tähega
kategooriad = { "dj01": {"Syva", "Kokku", "DJ"},
                "dj02": {"Syva", "Kokku", "DJ"},
                "ettepanekud": {"Üldine", "Kokku"},
                "ex01": {"EX", "Kokku"},
                "ex02": {"EX", "Kokku"},
                "ex03": {"EX", "Kokku"},
                "ex04": {"EX", "Kokku"},
                "ex05": {"EX", "Kokku"},
                "ex06": {"EX", "Kokku"},
                "ex07": {"EX", "Kokku"},
                "ex08": {"EX", "Kokku"},
                "ex09": {"EX", "Kokku"},
                "ex11": {"EX", "Kokku"},
                "ex12": {"EX", "Kokku"},
                "ex13": {"EX", "Kokku"},
                "ex14": {"EX", "Kokku"},
                "ex15": {"EX", "Kokku"},
                "food": {"Üldine", "Kokku"},
                "general": {"Üldine", "Kokku"},
                "git": {"Üldine", "Kokku"},
                "kaugōpe": {"Üldine", "Kokku"},
                "konsult": {"Üldine", "Kokku"},
                "meme": {"Üldine", "Kokku"},
                "mitteniiolulisedagasiiskiolulised-teadaanded": {"Üldine", "Kokku"},
                "olulised-teadaanded": {"Üldine", "Kokku"},
                "pr01": {"PR", "Kokku"},
                "pr02": {"PR", "Kokku"},
                "pr03": {"PR", "Kokku"},
                "pr04": {"PR", "Kokku"},
                "pr06": {"PR", "Kokku"},
                "pr07": {"PR", "Kokku"},
                "pr08": {"PR", "Kokku"},
                "pr09": {"PR", "Kokku"},
                "pr11": {"PR", "Kokku"},
                "pr12": {"PR", "Kokku"},
                "pr13": {"PR", "Kokku"},
                "pr14": {"PR", "Kokku"},
                "pr15": {"PR", "Kokku"},
                "random": {"Üldine", "Kokku"},
                "stat": {"Üldine", "Kokku"},
                "syvapy-general": {"Üldine", "Kokku"},
                "videod": {"Üldine", "Kokku"},
                "wat": {"PR", "Kokku"},
                "xp01": {"Syva", "Kokku", "XP"},
                "xp02": {"Syva", "Kokku", "XP"},
                "xp03": {"Syva", "Kokku", "XP"},
                "xp04": {"Syva", "Kokku", "XP"},
                "xp05": {"Syva", "Kokku", "XP"},
                "xp06": {"Syva", "Kokku", "XP"},
                "xp07": {"Syva", "Kokku", "XP"}}

for c in sorted(archive['data']):  # c = kanali id
    cur_name = archive['meta']['channels'][c]['name']  # Praeguse kanali nimi
    cur_name = cur_name.split('_')[0]
    channels.append(cur_name)
    print(cur_name[:1]+cur_name[-2:],end=' ')
    for m in archive['data'][c]:  # m = sõnumi ID
        message = archive['data'][c][m]
        time=datetime.datetime.fromtimestamp(message['t'] // 1000)
        wk=time.weekday()
        h=time.hour
        # Nädalapäev: E = 0, P = 6
        # print(time.date(),time.time(),wk,h)
        uid = message['u']
        for sub in [cur_name]+list(kategooriad[cur_name]):
            if sub not in users[uid]['count']:# Kui see sõnum on kasutaja
                users[uid]['count'][sub] = 0  # esimene sõnum antud kanalis
                users[uid]['lens'][sub] = 0  # init loendurid
                users[uid]['times'][sub] = [0]*168  # Iga tunni jaoks
            users[uid]['count'][sub] += 1
            users[uid]['lens'][sub] += len(message['m'])
            users[uid]['times'][sub][24*wk+h]+=1
        
        uid = -1  # Kõigi kasutajate peale kokku
        for sub in [cur_name]+list(kategooriad[cur_name]):
            if sub not in users[uid]['count']:# Kui see sõnum on kasutaja
                users[uid]['count'][sub] = 0  # esimene sõnum antud kanalis
                users[uid]['lens'][sub] = 0  # init loendurid
                users[uid]['times'][sub] = [0]*168  # Iga tunni jaoks
            users[uid]['count'][sub] += 1
            users[uid]['lens'][sub] += len(message['m'])
            users[uid]['times'][sub][24*wk+h]+=1
print()
channels=['DJ', 'EX', 'Kokku', 'PR', 'Syva', 'Üldine', 'XP', 'dj01', 'dj02', 'ettepanekud', 'ex01', 'ex02', 'ex03', 'ex04',
          'ex05', 'ex06', 'ex07', 'ex08', 'ex09', 'ex11', 'ex12', 'ex13', 'ex14', 'ex15', 'food', 'general', 'git', 'kaugōpe',
          'konsult', 'meme', 'mitteniiolulisedagasiiskiolulised-teadaanded', 'olulised-teadaanded', 'pr01', 'pr02', 'pr03',
          'pr04', 'pr06', 'pr07', 'pr08', 'pr09', 'pr11', 'pr12', 'pr13', 'pr14', 'pr15', 'random', 'stat', 'syvapy-general',
          'videod', 'wat', 'xp01', 'xp02', 'xp03', 'xp04', 'xp05', 'xp06', 'xp07']
nimed2=list(map(lambda uid:users[uid]['n'], users))
nimed3=list(map(lambda x:x.lower(),nimed2))
print('''
    ****** Interaktiivne "aktiivsusmonitor" ******
Kasutamine:
    Esimesele reale kirjuta üks kategooria (või kanali nimi).
    Teisele reale tühikutega eraldatult kasutajate nimed või "Kõik"
    Kui ei tea (ühe) kasutaja nime, kirjuta nimeosa ja lõppu "?".
    Sulgemiseks Ctrl + C
''')
nädal=["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede", "Laupäev", "Pühapäev"]
nädal=["Esmasp.", "Teisip.", "Kolmap.", "Neljap.", "Reede", "Laup.", "Pühap."]
try:
    while True:
        kanal=input('\nSisesta kanal: ')
        if kanal not in channels:
            print('Tundmatu kanal. Vt alla.')
            print('''Ühendatud kanalid:
    Kokku
    ├───EX
    ├───PR
    ├───Syva
    │   ├───DJ
    │   └───XP
    └───Üldine''')
            print(*channels)
            continue
        while True:
            nimed=input('Sisesta nimed: ')
            if nimed[-1]=='?':
                nimed=nimed[:-1].strip()
                # print(nimed2)
                out=list(sorted(filter(lambda x:nimed in x.lower(),nimed2)))
                print(*out)
                continue
            nimed4=[]
            for nimi in nimed.split():
                if nimi.lower()=='kõik':
                    nimed4.append(-1)
                elif nimi.lower() in nimed3:
                    nimed4.append(nimed3.index(nimi.lower()))
                else:
                    print(nimi+' ei leitud.')
            if nimed4!=[]:
                break
        for uid in nimed4:
            print('\t'.join([users[uid]['n'],'Päev']+list(map(str,range(24)))))
            for i in range(7):
                out=['',nädal[i]]+list(map(str,users[uid]['times'][kanal][24*i:24*(i+1)]))
                print('\t'.join(out))
            print('\n')
except KeyboardInterrupt:
    pass
##ajad = list()
##header=['Nimi','Kanal']
##for wk in 'ETKNRLP':
##    for hr in range(24):
##        header.append(wk+' '+str(hr))
##header = '\t'.join(header)
##ajad.append(header)
##for x in list(users):
##    for c in sorted(users[x]['times']):  # Iga kanaliga
##        ajad.append('\t'.join([users[x]['n'],c]+list(map(str,users[x]['times'][c]))))
##with open('d_out_ajatabel2.txt','w',encoding='utf8') as f:
##    f.write('\n'.join(ajad))
print('done')
