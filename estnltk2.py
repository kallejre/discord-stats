# -*- coding: utf-8 -*-
"""
See kood kasutab estnltk teeki ning töötab linuxil.

Sisendiks on disc_sõnapilveks.txt ja väljundiks out.txt, milles sisaldub JSON
kõigi kasutajate sõnastatistikast.
"""
# https://estnltk.github.io/estnltk/1.4.1/tutorials/installation.html
import estnltk
from estnltk import Text


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

 [{'clitic': '',
   'ending': '0',
   'form': 'sg n',
   'lemma': 'viis',
   'partofspeech': 'N',
   'root': 'viis',
   'root_tokens': ['viis']}],
 [{'clitic': '',
   'ending': 't',
   'form': 'sg p',
   'lemma': 'mitte-täidlane',
   'partofspeech': 'A',
   'root': 'mitte-täidlane',
   'root_tokens': ['mitte', 'täidlane']}],
 [{'clitic': '',
   'ending': 't',
   'form': 'sg p',
   'lemma': 'öötööline',
   'partofspeech': 'S',
   'root': 'öö_tööline',
   'root_tokens': ['öö', 'tööline']}],

 [{'clitic': '',
   'ending': 'sid',
   'form': 'sid',
   'lemma': 'jõudma',
   'partofspeech': 'V',
   'root': 'jõud',
   'root_tokens': ['jõud']}],
 [{'clitic': '',
   'ending': '0',
   'form': 'adt',
   'lemma': 'kodu',
   'partofspeech': 'S',
   'root': 'kodu',
   'root_tokens': ['kodu']}],
 [{'clitic': '',
   'ending': '',
   'form': '',
   'lemma': '.',
   'partofspeech': 'Z',
   'root': '.',
   'root_tokens': ['.']}]
 """
users={'-1':dict()}
c=0
with open('disc_sõnapilveks.txt', encoding='utf-8') as fin:
    for line in fin:
        c+=1
        if c%10000==0:print(c)
        if len(line)>17 and line.split()[0].isdigit() and len(line.split()[0])==18:
            # See on kasutaja sõnumi algus
            uid=line.split()[0]
            line='\t'.join(line.split('\t')[1:])
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
with open('sõnastats.txt', 'w', encoding='utf-8') as f:
    f.write(use)

