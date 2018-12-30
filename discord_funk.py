# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

Funktsionaalne lähenemine statistikale.
Siit võiks tulla suur asi.

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
###   INIT   ###
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
                'times': dict(), 'next': dict(), 'prev': dict(), 'tag_by': dict(),'tag_to': dict()}
users[-1] = {'n': 'Kõik', 'count': dict(), 'lens': dict(),
                'times': dict(), 'next': dict(), 'prev': dict(), 'tag_by': dict(),'tag_to': dict()}
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
f = open('disc_sõnapilveks.txt', 'w', encoding='utf8')
###   INIT2   ###
for c in archive['data']:  # c = kanali id
    print(c[0], end='')
    cur_name = archive['meta']['channels'][c]['name']  # Praeguse kanali nimi
    cur_name = cur_name.split('_')[0]
    channels.append(cur_name)
    prev_msg=-1
    for m in sorted(archive['data'][c]):  # m = sõnumi ID
        message = archive['data'][c][m]
        if len(message['m'].strip().split()) < 2:  # Ühesõnaliste sõnumitega opereerimine
            if message['u'] not in lyhi:
                lyhi[message['u']] = 0  # Loendab lühikesi sõnumeid
            lyhi[message['u']] += 1
            # continue         # Lühisõnumi saab vahele jätta
        print(message['m'].lower(), file=f)  # Kopeeri sõnum faili
        time=datetime.datetime.fromtimestamp(message['t'] // 1000)
        wk=time.weekday()
        h=time.hour
        # Nädalapäev: E = 0, P = 6
        # print(time.date(),time.time(),wk,h)
        
        times.add(message['t'] // 10000 - 306788430)  # 10 sekundi täpsusega
        uid = message['u']
        # Siiani korras
        ### REGEX
        matches=re.finditer('\<@!?\d+\>', message['m'])
        tags=[]
        for matchNum, match in enumerate(matches):
            tags.append(match.group()[2:-1].strip('!'))
        if tags:
            # archive['meta']['users']['259709906607800321']
            # archive['meta']['userindex'].index('259709906607800321')
            for tag in tags:
                if tag in archive['meta']['userindex']:
                    teine_uid=archive['meta']['userindex'].index(tag)
                    if teine_uid not in users[uid]['tag_to']:
                        users[uid]['tag_to'][teine_uid]=0
                        users[teine_uid]['tag_by'][uid]=0
                    users[uid]['tag_to'][teine_uid]+=1
                    users[teine_uid]['tag_by'][uid]+=1
                    # print(users[uid]['n'],'->',users[teine_uid]['n'])
                else:
                    pass  # print('ERROR: ',tag)
        ### REGEX läbi
        if prev_msg!=-1 and prev_msg!=uid:
            if prev_msg not in users[uid]['next']:
                users[uid]['next'][prev_msg]=0
                users[prev_msg]['prev'][uid]=0
            users[uid]['next'][prev_msg]+=1
            users[prev_msg]['prev'][uid]+=1
        prev_msg=uid
        # /\ Regexist
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
f.close()
print()
channels=['DJ', 'EX', 'Kokku', 'PR', 'Syva', 'Üldine', 'XP', 'dj01', 'dj02', 'ettepanekud', 'ex01', 'ex02', 'ex03', 'ex04',
          'ex05', 'ex06', 'ex07', 'ex08', 'ex09', 'ex11', 'ex12', 'ex13', 'ex14', 'ex15', 'food', 'general', 'git', 'kaugōpe',
          'konsult', 'meme', 'mitteniiolulisedagasiiskiolulised-teadaanded', 'olulised-teadaanded', 'pr01', 'pr02', 'pr03',
          'pr04', 'pr06', 'pr07', 'pr08', 'pr09', 'pr11', 'pr12', 'pr13', 'pr14', 'pr15', 'random', 'stat', 'syvapy-general',
          'videod', 'wat', 'xp01', 'xp02', 'xp03', 'xp04', 'xp05', 'xp06', 'xp07']
pikkused = list()
times = list(sorted(times))
kogus = list()
keskmine_pikkus = list()
sisukus = list()
header = '\t'.join(['Nimi'] + channels + ['Kokku'])
head=[]
for wk in 'ETKNRLP':
    for hr in range(24):
        head.append(wk+' '+str(hr))
header2 = '\t'.join(['Nimi','Kanal']+head)
del head
ajad = list()
nimed2=list(map(lambda uid:users[uid]['n'], users))
nimed3=list(map(lambda x:x.lower(),nimed2))
nädal=["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede", "Laupäev", "Pühapäev"]
nädal=["Esmasp.", "Teisip.", "Kolmap.", "Neljap.", "Reede", "Laup.", "Pühap."]
class Arhiiv:
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
        sisukus.append(out)
        c += 1
    with open('d_out4.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(sisukus))
class AjatabelSuur:
    ajad.append(header2)
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
class AjatabelVäike:
    print('''
    ****** Interaktiivne "aktiivsusmonitor" ******
Kasutamine:
    Esimesele reale kirjuta üks kategooria (või kanali nimi).
    Teisele reale tühikutega eraldatult kasutajate nimed või "Kõik"
    Kui ei tea (ühe) kasutaja nime, kirjuta nimeosa ja lõppu "?".
    Sulgemiseks Ctrl + C
''')
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
class Graafid:
    if 1:
        username='uudu'
        uid=list(filter(lambda x:username.lower() in users[x]['n'].lower(),users))[0]
        # Enne/Peale keda kirjutad
        for i in sorted(users[uid]['prev'], key=lambda i:users[uid]['prev'][i])[-5:]:
            print(users[i]['n'],'->',users[uid]['n'],' \t',users[uid]['prev'][i],'korda')
        print()
        for i in sorted(users[uid]['next'], key=lambda i:users[uid]['next'][i])[-5:]:
            print(users[uid]['n'],'->',users[i]['n'],' \t',users[uid]['next'][i],'korda')
        print('\nMärkimised:')
        # Kes keda märgib
        for i in sorted(users[uid]['tag_by'], key=lambda i:users[uid]['tag_by'][i])[-5:]:
            print(users[i]['n'],'->',users[uid]['n'],' \t',users[uid]['tag_by'][i],'korda')
        print()
        for i in sorted(users[uid]['tag_to'], key=lambda i:users[uid]['tag_to'][i])[-5:]:
            print(users[uid]['n'],'->',users[i]['n'],' \t',users[uid]['tag_to'][i],'korda')
        print()
    if 0:
        with open('users.py','w',encoding='utf-8') as f:
            f.write('users='+str(users))
        import json
        use=json.dumps(users)
        with open('ergo.json','w',encoding='utf-8') as f:
            f.write(str(use))
            
    with open('disco.tgf', 'w', encoding='utf-8') as f:
        for i in users:
            print(i,users[i]['n'],file=f)
        print('#',file=f)
        for uid in users:
            for nxt in users[uid]['tag_to']:
                count=users[uid]['tag_to'][nxt]
                if count>=1:
                    print(uid,nxt,count,file=f)
                    
    with open('d_out_tag.txt', 'w', encoding='utf-8') as f:
        for uid in users:
            for nxt in users[uid]['tag_to']:
                count=users[uid]['tag_to'][nxt]
                if count>=1:
                    print(users[uid]['n'],users[nxt]['n'],count,file=f,sep='\t')
    paarid=set()
    key='tag_to'
    with open('d_out_msg2.txt', 'w', encoding='utf-8') as f:
        for uid in users:
            for nxt in users[uid][key]:
                if ((nxt,uid) not in paarid):  # users[nxt][key][uid]
                    paarid.add((uid,nxt))
                    if uid in users[nxt][key]:
                        sisse=users[nxt][key][uid]
                        välja=users[uid][key][nxt]
                        count=min([sisse/välja,välja/sisse])*min([sisse, välja])
                        if count>1:
                            l=list(sorted([users[uid]['n'],users[nxt]['n']]))
                            print(*l,välja,sisse,str(count).replace('.',','),file=f,sep='\t')
    paarid=set()
    key='next'
    with open('d_out_msg.txt', 'w', encoding='utf-8') as f:
        for uid in users:
            for nxt in users[uid][key]:
                if ((nxt,uid) not in paarid):  # users[nxt][key][uid]
                    paarid.add((uid,nxt))
                    if uid in users[nxt][key]:
                        sisse=users[nxt][key][uid]
                        välja=users[uid][key][nxt]
                        count=min([sisse/välja,välja/sisse])*min([sisse, välja])
                        if count>1:
                            l=list(sorted([users[uid]['n'],users[nxt]['n']]))
                            print(*l,välja,sisse,str(count).replace('.',','),file=f,sep='\t')
    print('done')
class Graafik:
    """Pygame joonistamine."""
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

    c = 1
    print(len(times))
    print('done')
    pygame.image.save(lava, "screenshot.jpeg")
    for i in sorted(colors):
        print(i,colors[i])
    pygame.quit()
