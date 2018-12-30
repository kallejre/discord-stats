# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

Graafi idee. Koostada graaf, kelle sõnum järgneb kellele.


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
import re
for x in range(len(archive['meta']['userindex'])):
    # Viime lokaalse ID vastavusse kasutajanimega
    users[x] = {'n': archive['meta']['users'][archive['meta']['userindex'][x]]['name'],
                'next': dict(), 'prev': dict(),
                'tag_by': dict(),'tag_to': dict()}
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
    prev_msg=-1
    # Regex: \<@!?\d+\>
    for m in sorted(archive['data'][c]):  # m = sõnumi ID
        message = archive['data'][c][m]
        # Nädalapäev: E = 0, P = 6
        # print(time.date(),time.time(),wk,h)
        uid = message['u']
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
        if prev_msg!=-1 and prev_msg!=uid:
            if prev_msg not in users[uid]['next']:
                users[uid]['next'][prev_msg]=0
                users[prev_msg]['prev'][uid]=0
            users[uid]['next'][prev_msg]+=1
            users[prev_msg]['prev'][uid]+=1
        prev_msg=uid
print()
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
"""
with open('disco.tgf', 'w', encoding='utf-8') as f:
    for i in users:
        print(i,users[i]['n'],file=f)
    print('#',file=f)
    for uid in users:
        for nxt in users[uid]['tag_to']:
            count=users[uid]['tag_to'][nxt]
            if count>=1:
                print(uid,nxt,count,file=f)
"""
with open('d_out_tag.txt', 'w', encoding='utf-8') as f:
    for uid in users:
        for nxt in users[uid]['tag_to']:
            count=users[uid]['tag_to'][nxt]
            if count>=1:
                print(users[uid]['n'],users[nxt]['n'],count,file=f,sep='\t')
paarid=set()
key='next'
#key='tag_to'
with open('d_out_msg.txt', 'w', encoding='utf-8') as f:
    for uid in users:
        for nxt in users[uid][key]:
            if ((nxt,uid) not in paarid):  # users[nxt][key][uid]
                paarid.add((uid,nxt))
                if uid in users[nxt][key]:
                    sisse=users[nxt][key][uid]
                    välja=users[uid][key][nxt]
                    count=min([sisse/välja,välja/sisse])*min([sisse, välja])
                    # count= min([users[nxt][key][uid]/users[uid][key][nxt],users[uid][key][nxt]/users[nxt][key][uid]])*\
                    #         min([users[nxt][key][uid], users[uid][key][nxt]])
                    if count>1:
                        l=list(sorted([users[uid]['n'],users[nxt]['n']]))
                        print(*l,välja,sisse,str(count).replace('.',','),file=f,sep='\t')
print('done')
