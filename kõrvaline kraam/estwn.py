import xmltodict
import json
import time
t0=time.time()
t1=t0
def b(st):
    global t1
    t2=time.time()
    print(round(t2-t0,2),round(t2-t1,2),st)
    t1=t2
fn='estwn-vaike'
fn='estwn-et-2.1.0.wip'
b('start1')
#jss=xmltodict.parse(open(fn+'.xml',encoding='utf8').read())
b('start1.1')
#json.dump(jss,open(fn+'.json','w',encoding='utf8'),ensure_ascii=False, indent=2, sort_keys=True)
b('start1.2 (Json load)')
jss=json.load(open(fn+'.json',encoding='utf8'))
b('Klassid')
"""
{
"LexicalResource": {
    "@xmlns:dc": "http://purl.org/dc/elements/1.1/",
    "Lexicon": {
        "@confidenceScore": "1.0",
        "@email": "heili.orav@ut.ee",
        "@id": "estwn",
        "@label": "Estonian Wordnet",
        "@language": "et",
        "@license": "https://creativecommons.org/licenses/by-sa/",
        "@note": "Work in progress. Previous name for this dataset was 'koondbaas 74'.",
        "@status": "unchecked",
        "@version": "2.1.0.wip",
        "LexicalEntry": [
{
    "@id": "w526584",
    "Lemma": {
        "@partOfSpeech": "n",
        "@writtenForm": "0-tüüpi grammatika"
    },
    "Sense": {
        "@id": "s-0-tüüpi_grammatika-n1",
        "@status": "unchecked",
        "@synset": "estwn-et-44468-n"
    }
}]}}}
"""
# Näide põhisisust.
LexicalEntry={'@id': 'w526582',
 'Lemma': {'@partOfSpeech': 'n', '@writtenForm': ''},
 'Sense': {'@id': 's--n1',
           '@status': 'unchecked',
           '@synset': 'estwn-et-5275-n'}}
Synset={'@confidenceScore': '0.5',
 '@dc:type': 'C',
 '@id': 'estwn-et-10000-n',
 '@ili': '',
 '@status': 'checked',
 'Definition': {'#text': 'tööriista, eseme vm. lai ja lame osa',
                '@language': 'et',
                '@sourceSense': 's-laba-n1'},
 'SynsetRelation': {'@confidenceScore': '1.0',
                    '@relType': 'hypernym',
                    '@status': 'unchecked',
                    '@target': 'estwn-et-22447-n'}}
class LexicalEntry:
    def __init__(self, lex):
        self.word=lex['Lemma']['@writtenForm']
        self.speech=lex['Lemma']['@partOfSpeech']
        self.id=lex['@id']
        self.syns=[]
        if type(lex['Sense'])!=list:
            lex['Sense']=[lex['Sense']]
        for i in lex['Sense']:
            self.syns.append(i['@synset'])
        return
class Synset:
    def __init__(self, syn):
        self.id=syn['@id']
        self.status=syn['@status']
        self.confidence=syn['@confidenceScore']
        if 'Definition' in syn:
            if type(syn['Definition'])==list:
                self.definition=syn['Definition'][0]['#text']
            else:self.definition=syn['Definition']['#text']
        elif 'ILIDefinition' in syn:
            if type(syn['ILIDefinition'])==list:
                self.definition=syn['ILIDefinition'][0]
            else:self.definition=syn['ILIDefinition']
        else:self.definition='None'
        self.relations=[]
        self.references=[]  # Viide sõnale, mis on seoses
        if 'SynsetRelation' not in syn:return
        if type(syn['SynsetRelation'])!=list:
            syn['SynsetRelation']=[syn['SynsetRelation']]
        for i in syn['SynsetRelation']:
            t=dict()
            t['target']=i['@target']
            t['relType']=i['@relType']
            t['confidence']=i['@confidenceScore']
            self.relations.append(dict(t))
        return

def find(word):
    global words
    if word in words:return words[word]
    fil=list(filter(lambda x:word.lower() in x.lower(),words))
    n=list(sorted(fil,key=lambda x:[x.lower().index(word.lower()),len(x)]))
    if len(n)>0:return words[n[0]]
    for i in range(1,len(word)):
        fil=list(filter(lambda x:word[:-i].lower() in x.lower(),words))
        n=list(sorted(fil,key=lambda x:[x.lower().index(word[:-i].lower()),len(x)]))
        if len(n)>0:return words[n[0]]
def f2(wd):return lexical[find(wd)].word
# Word finder:
# while True:lexical[find(input('Nxt: '))].word

#import pprint
#pprint.pprint(jss)
import pprint
"""
for i in sorted(jss['LexicalResource']['Lexicon']):
    # print(i)
    if type(jss['LexicalResource']['Lexicon'][i])!=list:
        x=list(jss['LexicalResource']['Lexicon'][i])
        if len(x[0])==1:
            x=''.join(x)
        print(i,  '\n  ',x)
    else:
        print(i)
        pprint.pprint(jss['LexicalResource']['Lexicon'][i][0])
"""
lexical=dict()
words=dict()
synset=dict()
b('start syn')
for syn in jss['LexicalResource']['Lexicon']['Synset']:
    synset[syn['@id']]=Synset(syn)
b('start lex')
for lex in jss['LexicalResource']['Lexicon']['LexicalEntry']:
    ide=lex['@id']
    lexical[ide]=LexicalEntry(lex)
    for syn in lexical[ide].syns:
        synset[syn].references.append(ide)
    words[lexical[ide].word]=ide

b('done')
for s in lexical[find('arvelaud')].syns:
    n=synset[s]
    print(', '.join(list(map(lambda x:lexical[x].word,n.references))),'-', n.definition)
