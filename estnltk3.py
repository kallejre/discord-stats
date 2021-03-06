# -*- coding: utf-8 -*-
"""
See kood kasutab estnltk teeki ning töötab linuxil.

Sisendiks on disc_sõnapilveks.txt ja väljundiks out.txt, milles sisaldub JSON
kõigi kasutajate sõnastatistikast.
"""
# https://estnltk.github.io/estnltk/1.4.1/tutorials/installation.html
import estnltk
import urllib.parse
from estnltk import Text
from discord_class import xlsx
"""
    A - adjective
    C - comparative adjective
    D - adverb
    G - non declinable adjective
    H - real name
    I - interjection
    J - conjunction  		<- Tuleks eemaldada statistikast.
    K - co-expression
    N - cardinal numeral
    O - ordinal numeral
    P - pronoun
    S - noun
    U - superlative adjective
    V - verb
    X - other type of word belonging together with a verb
    Y - abbreviation
    Z - sign
"""
def main(sts):
    users={'-1':dict()}
    c=0
    with open(sts.OUTPUT_FOLDER+'disc_sõnapilveks.txt', encoding='utf-8') as fin:
        for line in fin:
            c+=1
            if c==1: continue
            if c%10000==0:print(c)
            uid=line.split()[2]
            line=urllib.parse.unquote('\t'.join(line.split('\t')[4:]))
            lause=Text(line)
            if uid not in users:
                users[uid]=dict()
            s=lause.analysis
            for sona in s:
                lemmad=[sona[0]['lemma']]
                if sona[0]['partofspeech'] in 'Z':#'ZJP':
                    continue  # Jäta vahele sidesõnad ja üksikud tähemärgid.
                else:
                    lemmad=sona[0]['root_tokens']  # Tugi liitsõnadele
                    for lemma in lemmad:
                        if lemma not in users[uid]:
                            users[uid][lemma]=0
                        if lemma not in users['-1']:
                            users['-1'][lemma]=0
                        users[uid][lemma]+=1
                        users['-1'][lemma]+=1
    import json
    use = json.dumps(users, ensure_ascii=False)
    with open(sts.OUTPUT_FOLDER+'sõnastats.txt', 'w', encoding='utf-8') as f:
        f.write(use)
    c=1
    # Kuna peafunktsiooni exceli töövihik on veel lahti, siis saab sinna asju lisada.
    sts.excel.ws('Sõnade top 1500')
    sts.excel.write('Sõna\tKogus')
    #f=open(sts.OUTPUT_FOLDER+'sõnastats2.txt', 'w', encoding='utf-8')
    sonastik=list(sorted(users['-1'], key=lambda x:users['-1'][x], reverse=True))
    # print(len(sonastik))  # -> 33110.
    for i in sonastik[:1500]:
        i2=i
        try:
            int(i)
            i2='\''+i
        except:pass
        try:sts.excel.write(i2+'\t'+str(users['-1'][i]))
        except:print(i)
        c+=1
    #f.close()
