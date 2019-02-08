# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

Klassikaline lähenemine statistikale.
See variant proovib kõik tabelid panna ühte exceli tabelisse.
Edasine arendamine käib siitkaudu

Prototüüp animatsiooni tegemiseks.
Ehitatud _classi põhjale
    Kasutan pygame'i, teoreetiliselt saaks ka PIL-ga.
Animatsioon:
    Tulpdiagrammid,
       1 tulp näitab inimeste osalust selles kanalis värviliselt.
    1 tund=1 kaader
       Plaan kasutada vajumist, näiteks postitus sisaldub statistikas 6 tundi.

Stats.ajatabel_suur     Koosta suur tabel iga nime, kanali, kellaaja ja kuupäeva kohta.
Stats.ajatabel_vaike    UI ajatabelite kuvamiseks
Stats.ajatabel_vaiksem  Ajatabelite sõnede tegemine.
Stats.arhiiv            Tagastab palju asju. Sõnumite kogupikkus, arv, keskmine pikkus kasutaja/kanali lõikes.
Stats.graafid_edetabel  Kuva N populaarseimat suunda ühe kasutaja suhtes.
Stats.graafik           Pygame joonistamine. KATKI!
Stats.__init__          Peamiselt muutujate algväärtustamine.
Stats.init2             Aandmete kogumine ja põhiline töötlemine.
Stats.out_tgf_msg       Kirjavahetuse põhjal TGF-graaf.
Stats.out_tgf_tag       Märkimiste põhjal TGF-graaf.
Stats.out_users_json    Self.users -> JSON. Kole väljund.
Stats.out_users_py      Self.users -> Python. Kena väljund.
Stats.stat_msg          Sõnumite statisika, kui palju on X->Y sõnumeid.
Stats.stat_msg2         Kahepoolse vestlemise tabel.
Stats.stat_tag          Tag statisika, kui palju on X->Y märkimisi.
Stats.stat_tag2         Kahepoolse märkimise tabel.
Stats.users             Põhiline muutuja, kus on kasutajate info.

Nädalapäev: E = 0, P = 6
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


import datetime
import json
import re
import pickle
import xlsxwriter
from Animate import Animate
from os import makedirs

class xlsx:
    def __init__(self, fname='stats.xlsx'):
        self.excel=xlsxwriter.Workbook(fname)
        self.sheets=[]
        self.current_sheet=None
        self.row=None
        self.col=None
    def ws(self,name):
        """Lisab uue töölehe ja muudab aktiivseks."""
        self.current_sheet = self.excel.add_worksheet(name)
        self.sheets.append(self.current_sheet)
        self.row=0
        self.col=0
    def write(self,line):
        """Lisa \t-ga eraldatud rida faili nagu kleebiks tavalisse exceli tabelisse."""
        if line=='\n': return
        # print([line])
        lines=line.rstrip('\n').split('\n')
        for line in lines:
            self.col=0
            for cell in line.split('\t'):
                try: self.current_sheet.write(self.row, self.col,float(cell))
                except ValueError: self.current_sheet.write(self.row, self.col,cell)
                self.col+=1
            self.row+=1
    def close(self):
        self.excel.close()

# Kategooria peaks algama suure tähega
kategooriad_py = {"dj01": {"Syva", "Kokku", "DJ"}, "dj02": {"Syva", "Kokku", "DJ"},
                    "ettepanekud": {"Yldine", "Kokku"}, "ex01": {"EX", "Kokku"}, "ex02": {"EX", "Kokku"},
                    "ex03": {"EX", "Kokku"}, "ex04": {"EX", "Kokku"}, "ex05": {"EX", "Kokku"},
                    "ex06": {"EX", "Kokku"},
                    "ex07": {"EX", "Kokku"}, "ex08": {"EX", "Kokku"}, "ex09": {"EX", "Kokku"},
                    "ex11": {"EX", "Kokku"},
                    "ex12": {"EX", "Kokku"}, "ex13": {"EX", "Kokku"}, "ex14": {"EX", "Kokku"},
                    "ex15": {"EX", "Kokku"},
                    "food": {"Yldine", "Kokku"}, "general": {"Yldine", "Kokku"}, "git": {"Yldine", "Kokku"},
                    "kaugõpe": {"Yldine", "Kokku"}, "konsult": {"Yldine", "Kokku"}, "meme": {"Yldine", "Kokku"},
                    "mitteniiolulisedagasiiskiolulised-teadaanded": {"Yldine", "Kokku"},
                    "pr03": {"PR", "Kokku"}, "java": {"Yldine", "Kokku"},
                    "olulised-teadaanded": {"Yldine", "Kokku"}, "pr01": {"PR", "Kokku"},
                    "pr02": {"PR", "Kokku"},
                    "pr04": {"PR", "Kokku"}, "pr06": {"PR", "Kokku"}, "pr07": {"PR", "Kokku"},
                    "pr08": {"PR", "Kokku"},
                    "pr09": {"PR", "Kokku"}, "pr11": {"PR", "Kokku"}, "pr12": {"PR", "Kokku"},
                    "pr13": {"PR", "Kokku"},
                    "pr14": {"PR", "Kokku"}, "pr15": {"PR", "Kokku"}, "random": {"Yldine", "Kokku"},
                    "wat": {"PR", "Kokku"},
                    "stat": {"Yldine", "Kokku"}, "syvapy-general": {"Yldine", "Kokku"},
                    "videod": {"Yldine", "Kokku"}, "eksam": {"Yldine", "Kokku"},
                    "xp01": {"Syva", "Kokku", "XP"}, "xp02": {"Syva", "Kokku", "XP"},
                    "xp03": {"Syva", "Kokku", "XP"},
                    "xp04": {"Syva", "Kokku", "XP"}, "xp05": {"Syva", "Kokku", "XP"},
                    "xp06": {"Syva", "Kokku", "XP"},
                    "xp07": {"Syva", "Kokku", "XP"}}

kategooriad_java = {"setup": {"Yldine", "Kokku"}, 
                    "ülesanded": {"Kalmo", "Kokku"}, 
                    "codera": {"Yldine", "Kokku"}, 
                    "ex01-id-code": {"EX", "Kokku"}, 
                    "ex02-cpu": {"EX", "Kokku"}, 
                    "food": {"Yldine", "Kokku"}, 
                    "general": {"Yldine", "Kokku"}, 
                    "java": {"Kalmo", "Kokku"}, 
                    "korraldus": {"Kalmo", "Kokku"}, 
                    "meme": {"Yldine", "Kokku"}, 
                    "music": {"Yldine", "Kokku"}, 
                    "pr00-hello": {"PR", "Kokku"}, 
                    "pr01-introduction": {"PR", "Kokku"}, 
                    "pr02-strings": {"PR", "Kokku"}, 
                    "projekt": {"Yldine", "Kokku"}, 
                    "random": {"Yldine", "Kokku"}, 
                    "stat": {"Yldine", "Kokku"}, 
                    "teadaanded": {"Yldine", "Kokku"}, 
                    "teated": {"Yldine", "Kokku"}, 
                    "videod": {"Yldine", "Kokku"},
                    "wat": {"Kalmo", "Kokku"}}

kategooriad_kaug = {"it-eetilised-sotsiaalsed-ja-professionaalsed-aspektid": {"2semester", "Kokku"}, 
                    "statsionaar": {"Yldine", "Kokku"}, 
                    "kaugõpe": {"Yldine", "Kokku"}, 
                    "kasulik-info": {"Yldine", "Kokku"}, 
                    "operatsioonisüsteemid-ja-nende-haldamine": {"2semester", "Kokku"}, 
                    "üld-vestlus": {"Yldine", "Kokku"}, 
                    "arvutivõrgud": {"2semester", "Kokku"}, 
                    "arvutid": {"2semester", "Kokku"}, 
                    "kõrgem_matemaatika": {"2semester", "Kokku"}}



# OUTPUT_FOLDER-i Lõppu käib kaldkriips
class Stats:
    """Statistika."""

    def __init__(self, fname='dht.txt',OUTPUT_FOLDER='Python/',  sname='stats.xlsx', kategooria=kategooriad_py):
        """
        ###   INIT1   ###.

        Peamiselt muutujate algväärtustamine.
        """
        with open(fname, encoding='utf8') as f:
            file = f.read()
        self.archive = eval(file)
        self.users = dict()
        self.lyhi = {-1: 0}
        self.times = list()
        self.times2 = dict()
        self.OUTPUT_FOLDER = OUTPUT_FOLDER
        try:makedirs(OUTPUT_FOLDER)
        except FileExistsError: pass
        self.excel=xlsx(OUTPUT_FOLDER+sname)
        # self.ajaformaat = '%a %d %b %Y %H:00'  # 'Thu 15 Nov 2018 14:00'
        self.ajaformaat = '%a %d %b %Y'          # Kasutusel koos times2-ga
                    # Koodinäide: max(sts.times2,key=lambda x:datetime.datetime.strptime(x,sts.ajaformaat))
        # Kategooria peaks algama suure tähega
        self.kategooriad = kategooria
        
        for x1 in range(len(self.archive['meta']['userindex'])):
            self.users[x1] = {'n': self.archive['meta']['users'][self.archive['meta']['userindex'][x1]]['name'],
                              'count': dict(), 'lens': dict(), 'times': dict(), 'next': dict(),
                              'prev': dict(), 'tag_by': dict(), 'tag_to': dict()}
        self.users[-1] = {'n': 'Kõik', 'count': dict(), 'lens': dict(),
                          'times': dict(), 'next': dict(), 'prev': dict(), 'tag_by': dict(), 'tag_to': dict()}
        channels = list(self.kategooriad)
        for a in list(channels):
            channels += list(self.kategooriad[a])
        self.channels = list(sorted(set(channels)))
        self.header = '\t'.join(['Nimi'] + self.channels)
        head = []
        for wk in 'ETKNRLP':
            for hr in range(24):
                head.append(wk + ' ' + str(hr))
        self.header2 = '\t'.join(['Nimi', 'Kanal'] + head)
        self.nimed2 = list(map(lambda uid: self.users[uid]['n'], self.users))
        self.nimed3 = list(map(lambda x: x.lower(), self.nimed2))
        # self.week=["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede", "Laupäev", "Pühapäev"]
        self.week = ["Esmasp.", "Teisip.", "Kolmap.", "Neljap.", "Reede", "Laup.", "Pühap."]
        self.__init2()

    def __init2(self):
        """
        ###   INIT2   ###.

        Siin osas toimub andmete kogumine ja põhiline töötlemine.
        Alumised funktsioonid on vaid vormistamiseks ja kuvamiseks.
        Kunagi võiks teha mingi seadistamisvõimaluse.

        Init-funktsioon on jagatud kaheks, sest teoreetiliselt võiks andmete lugemine ja enetav töötlemine olla eraldi.
        """
        f = open(self.OUTPUT_FOLDER+'disc_sõnapilveks.txt', 'w', encoding='utf8')
        # print(self.archive['meta']['channels'])
        print('Server','Channel','User','Timestamp','Message', file=f,sep='\t')
        for c in sorted(self.archive['data'], key=lambda x:(self.archive['meta']['channels'][x]['server'],x)):  # c = kanali id
            server_id=self.archive['meta']['channels'][c]['server']
            server_name=self.archive['meta']['servers'][server_id]['name']
            cur_name = self.archive['meta']['channels'][c]['name']  # Praeguse kanali nimi
            cur_name = cur_name.split('_')[0]
            prev_msg = -1
            print(cur_name[:1] + cur_name[-2:], end=' ')
            for m in sorted(self.archive['data'][c]):  # m = sõnumi ID
                message = self.archive['data'][c][m]
                if len(message['m'].strip().split()) < 2:  # Ühesõnaliste sõnumitega opereerimine
                    if message['u'] not in self.lyhi:
                        self.lyhi[message['u']] = 0  # Loendab lühikesi sõnumeid
                    self.lyhi[message['u']] += 1
                    self.lyhi[-1] += 1
                    # continue                                      # Lühikese sõnumi saab vahele jätta
                print(server_id,c,self.archive['meta']['userindex'][message['u']],message['t'] // 1000,message['m'].lower(), file=f,sep='\t')  # Kopeeri sõnum faili
                time = datetime.datetime.fromtimestamp(message['t'] // 1000)  # 1 sekundi täpsusega
                wk = time.weekday()
                hr = time.hour
                self.times.append(time)
                uid = message['u']
                # REGEX start
                matches = re.finditer('\<@!?\d+\>', message['m'])
                tags = []
                for matchNum, match in enumerate(matches):
                    tags.append(match.group()[2:-1].strip('!'))
                if tags:
                    # self.archive['meta']['userindex'].index(yld_id)
                    for tag in tags:
                        if tag in self.archive['meta']['userindex']:
                            teine_uid = self.archive['meta']['userindex'].index(tag)
                            if teine_uid not in self.users[uid]['tag_to']:
                                self.users[uid]['tag_to'][teine_uid] = 0
                                self.users[teine_uid]['tag_by'][uid] = 0
                            self.users[uid]['tag_to'][teine_uid] += 1
                            self.users[teine_uid]['tag_by'][uid] += 1

                if prev_msg != -1 and prev_msg != uid:
                    if prev_msg not in self.users[uid]['next']:
                        self.users[uid]['next'][prev_msg] = 0
                        self.users[prev_msg]['prev'][uid] = 0
                    self.users[uid]['next'][prev_msg] += 1
                    self.users[prev_msg]['prev'][uid] += 1
                # REGEX läbi
                # self.times2 töötlemine
                time_str = time.strftime(self.ajaformaat)
                if time_str not in self.times2:
                    self.times2[time_str] = dict()
                if cur_name not in self.times2[time_str]:
                    self.times2[time_str][cur_name] = dict()
                if uid not in self.times2[time_str][cur_name]:
                    self.times2[time_str][cur_name][uid] = 0
                self.times2[time_str][cur_name][uid] += 1
                # self.times2 töötlemine läbi
                for sub in [cur_name] + list(self.kategooriad[cur_name]):
                    if sub not in self.users[uid]['count']:  # Kui see sõnum on kasutaja
                        self.users[uid]['count'][sub] = 0  # esimene sõnum antud kanalis
                        self.users[uid]['lens'][sub] = 0  # init loendurid
                        self.users[uid]['times'][sub] = [0] * 168  # Iga tunni jaoks
                    self.users[uid]['count'][sub] += 1
                    self.users[uid]['lens'][sub] += len(message['m'])
                    self.users[uid]['times'][sub][24 * wk + hr] += 1

                uid2 = uid
                uid = -1  # Kõigi kasutajate ühisstatistika
                for sub in [cur_name] + list(self.kategooriad[cur_name]):
                    if sub not in self.users[uid]['count']:  # Kui see sõnum on kasutaja
                        self.users[uid]['count'][sub] = 0  # esimene sõnum antud kanalis
                        self.users[uid]['lens'][sub] = 0  # init loendurid
                        self.users[uid]['times'][sub] = [0] * 168  # Iga tunni jaoks
                    self.users[uid]['count'][sub] += 1
                    self.users[uid]['lens'][sub] += len(message['m'])
                    self.users[uid]['times'][sub][24 * wk + hr] += 1
                if tags:
                    for tag in tags:
                        if tag in self.archive['meta']['userindex']:
                            teine_uid = self.archive['meta']['userindex'].index(tag)
                            if teine_uid not in self.users[uid]['tag_to']:
                                self.users[uid]['tag_to'][teine_uid] = 0
                            if uid2 not in self.users[uid]['tag_by']:
                                self.users[uid]['tag_by'][uid2] = 0
                            self.users[uid]['tag_to'][teine_uid] += 1
                            self.users[uid]['tag_by'][uid2] += 1
                if prev_msg != -1 and prev_msg != uid2:
                    if prev_msg not in self.users[uid]['next']:
                        self.users[uid]['next'][prev_msg] = 0
                    if uid2 not in self.users[uid]['prev']:
                        self.users[uid]['prev'][uid2] = 0
                    self.users[uid]['next'][prev_msg] += 1
                    self.users[uid]['prev'][uid2] += 1
                prev_msg = uid2
        print()
        # del self.archive
        self.times = list(sorted(self.times))
        f.close()

    def arhiiv(self):
        """
        Tagastab palju asju.

        d_out1 - Sõnumite kogupikkus kasutaja/kanali lõikes.
        d_out2 - Sõnumite arv kasutaja/kanali lõikes.
        d_out3 - Sõnumite keskmine pikkus kasutaja/kanali lõikes.
        d_out4 - Pikkade ja lühikeste sõnumite suhe.
        """
        pikkused = list()
        kogus = list()
        keskmine_pikkus = list()
        sisukus = list()
        for x in list(self.users):
            count = 0
            c_len = 0
            for c in self.users[x]['count']:
                count += self.users[x]['count'][c]
                c_len += self.users[x]['lens'][c]
            if count < 1:
                continue
            out1 = [self.users[x]['n']]
            out2 = [self.users[x]['n']]
            out3 = [self.users[x]['n']]
            for kanal in self.channels:
                if kanal in self.users[x]['count']:
                    out1.append(str(self.users[x]['lens'][kanal]))
                    out2.append(str(self.users[x]['count'][kanal]))
                    out3.append(
                        str(round(self.users[x]['lens'][kanal] / self.users[x]['count'][kanal], 3)))
                else:
                    out1.append('0')
                    out2.append('0')
                    out3.append('0')
            pikkused.append('\t'.join(out1))
            kogus.append('\t'.join(out2))
            keskmine_pikkus.append('\t'.join(out3))
        
        self.excel.ws('Pikkused')
        self.excel.write('\n'.join([self.header] + pikkused))
        self.excel.ws('Kogused')
        self.excel.write('\n'.join([self.header] + kogus))
        self.excel.ws('Keskmised pikkused')
        self.excel.write('\n'.join([self.header] + keskmine_pikkus))
        self.excel.ws('Lühikeste osa')
        self.excel.write('Jrk.\tNimi\tLühike\tKõik\t%')
        c = 1
        for i1 in sorted(self.lyhi, key=lambda x: self.users[x]['count']['Kokku'], reverse=True):
            self.excel.write('\t'.join([str(c), self.users[i1]['n'], str(self.lyhi[i1]), str(self.users[i1]['count']['Kokku']),
                             str(round(self.lyhi[i1] / self.users[i1]['count']['Kokku'] * 100, 2))]))
            c += 1

    def ajatabel_suur(self):
        """Koosta suur tabel iga nime, kanali, kellaaja ja kuupäeva kohta."""
        self.excel.ws('Ajatabel')
        self.excel.write(self.header2)
        for x1 in list(self.users):
            for c in sorted(self.users[x1]['times']):  # Iga kanaliga
                print('\t'.join([self.users[x1]['n'], c] + list(map(str, self.users[x1]['times'][c]))),file=self.excel)


    def ajatabel_vaiksem(self, uid, kanal):
        """Ajatabelite sõnede tegemine."""
        out2 = ['\t'.join([self.users[uid]['n'], 'Päev'] + list(map(str, range(24))))]
        for i1 in range(7):
            out = ['', self.week[i1]] + list(map(str, self.users[uid]['times'][kanal][24 * i1:24 * (i1 + 1)]))
            out2.append('\t'.join(out))
        return '\n'.join(out2)

    def ajatabel_vaike(self):
        """UI ajatabelite kuvamiseks."""
        print('''
        ****** Interaktiivne "aktiivsusmonitor" ******
    Kasutamine:
        Esimesele reale kirjuta üks kategooria (või kanali nimi).
        Teisele reale tühikutega eraldatult kasutajate nimed või "Kõik"
        Kui ei tea (ühe) kasutaja nime, kirjuta nimeosa ja lõppu "?".
        Sulgemiseks Ctrl + C ''')
        try:
            while True:
                kanal = input('\nSisesta kanal: ')
                if kanal not in self.channels:
                    print('Tundmatu kanal. Vt alla.')
                    print('Ühendatud kanalid:\n    Kokku\n    ├───EX\n    ├───PR\n    ├───Syva\n'
                          '    │   ├───DJ\n    │   └───XP\n    └───Üldine')
                    print(*self.channels)
                    continue
                while True:
                    nimed = input('Sisesta nimed: ')
                    if nimed[-1] == '?':
                        nimed = nimed[:-1].strip()
                        print(nimed)
                        out = list(sorted(filter(lambda x: nimed.lower() in x.lower(), self.nimed2)))  # ;nimed.lower()
                        print(*out)
                        continue
                    nimed4 = []
                    for nimi in nimed.split():
                        if nimi.lower() == 'kõik':
                            nimed4.append(-1)
                        elif nimi.lower() in self.nimed3:
                            nimed4.append(self.nimed3.index(nimi.lower()))
                        else:
                            print(nimi + ' ei leitud.')
                    if nimed4:
                        break
                for uid in nimed4:
                    print(self.ajatabel_vaiksem(uid, kanal))
        except KeyboardInterrupt:
            pass

    def graafid_edetabel(self, username, n=5, uid=False):
        """Kuva N populaarseimat suunda ühe kasutaja suhtes."""
        out=''
        if not uid:
            uid = list(filter(lambda x: username.lower() in self.users[x]['n'].lower(), self.users))[0]
        else:
            uid = username
        out+='\nKirjutamised:\n'
        # Enne/Peale keda kirjutad
        for i1 in sorted(self.users[uid]['prev'], key=lambda i: self.users[uid]['prev'][i])[-n:]:
            x=self.users[i1]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            y=self.users[uid]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            out+=' '.join(list(map(str,[x, '->', y, '\t', self.users[uid]['prev'][i1], 'korda'])))+'\n'
        out+='\n'
        for i1 in sorted(self.users[uid]['next'], key=lambda i: self.users[uid]['next'][i])[-n:]:
            x=self.users[uid]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            y=self.users[i1]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            out+=' '.join(list(map(str,[x, '->', y, ' \t', self.users[uid]['next'][i1], 'korda'])))+'\n'
        out+='\nMärkimised:\n'
        # Kes keda märgib
        for i1 in sorted(self.users[uid]['tag_by'], key=lambda i: self.users[uid]['tag_by'][i])[-n:]:
            x=self.users[i1]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            y=self.users[uid]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            out+=' '.join(list(map(str,[x, '->', y, ' \t', self.users[uid]['tag_by'][i1], 'korda'])))+'\n'
        out+='\n'
        for i1 in sorted(self.users[uid]['tag_to'], key=lambda i: self.users[uid]['tag_to'][i])[-n:]:
            x=self.users[uid]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            y=self.users[i1]['n'].encode('iso8859_13','replace').decode('iso8859_13')
            out+=' '.join(list(map(str,[x, '->', y, ' \t', self.users[uid]['tag_to'][i1], 'korda'])))+'\n'
        out+='\n'
        return out

    def save(self, fname='d_stats.pkl'):
        """Self -> PKL. Terve objekti salvestamine."""
        temp = self.excel
        self.excel = None
        with open(self.OUTPUT_FOLDER+fname, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        self.excel = temp
    def out_users_py(self, fname='users.py'):
        """Self.users -> Python. Kena väljund."""
        with open(self.OUTPUT_FOLDER+fname, 'w', encoding='utf-8') as f:
            f.write('users=' + str(self.users))

    def out_users_json(self, fname='ergo.json'):
        """Self.users -> JSON. Kole väljund."""
        use = json.dumps(self.users)
        with open(self.OUTPUT_FOLDER+fname, 'w', encoding='utf-8') as f:
            f.write(str(use))

    def out_tgf_tag(self, fname='disco_tag.tgf'):
        """Märkimiste põhjal TGF-graaf."""
        with open(self.OUTPUT_FOLDER+fname, 'w', encoding='utf-8') as f:
            for i1 in filter(lambda x: x > -1, self.users):
                print(i1, self.users[i1]['n'], file=f)
            print('#', file=f)
            for uid in filter(lambda x: x > -1, self.users):
                for nxt in self.users[uid]['tag_to']:
                    count = self.users[uid]['tag_to'][nxt]
                    if count >= 1:
                        print(uid, nxt, count, file=f)

    def out_tgf_msg(self, fname='disco_msg.tgf'):
        """Kirjavahetuse põhjal TGF-graaf."""
        with open(self.OUTPUT_FOLDER+fname, 'w', encoding='utf-8') as f:
            for i1 in filter(lambda x: x > -1, self.users):
                print(i1, self.users[i1]['n'], file=f)
            print('#', file=f)
            for uid in filter(lambda x: x > -1, self.users):
                for nxt in self.users[uid]['next']:
                    count = self.users[uid]['next'][nxt]
                    if count >= 1:
                        print(uid, nxt, count, file=f)

    def stat_tag(self):
        """Tag statisika, kui palju on X->Y märkimisi."""
        self.excel.ws('Tag to')
        f=self.excel
        print('\t'.join('X Y X->Y'.split()), file=f)
        for uid in self.users:
            for nxt in self.users[uid]['tag_to']:
                count = self.users[uid]['tag_to'][nxt]
                if count >= 1:
                    self.excel.write('\t'.join([self.users[uid]['n'], self.users[nxt]['n'], str(count)]))

    def stat_msg(self):
        """Sõnumite statisika, kui palju on X->Y sõnumeid."""
        self.excel.ws('Msg to')
        f=self.excel
        print('\t'.join('X Y X->Y'.split()), file=f)
        for uid in self.users:
            for nxt in self.users[uid]['next']:
                count = self.users[uid]['next'][nxt]
                if count >= 1:
                    self.excel.write('\t'.join([self.users[uid]['n'], self.users[nxt]['n'], str(count)]))

    def stat_tag2(self):
        """Kahepoolse märkimise tabel."""
        paarid = set()
        key = 'tag_to'
        self.excel.ws('Tag to 2')
        f=self.excel
        print('X\tY\tX->Y\tY->X\tTehe', file=f)
        for uid in self.users:
            for nxt in self.users[uid][key]:
                if (nxt, uid) not in paarid:
                    paarid.add((uid, nxt))
                    if uid in self.users[nxt][key]:
                        sisse = self.users[nxt][key][uid]
                        valja = self.users[uid][key][nxt]
                        count = min([sisse / valja, valja / sisse]) * min([sisse, valja])
                        if count > 1:
                            lis = list(sorted([self.users[uid]['n'], self.users[nxt]['n']]))
                            self.excel.write('\t'.join(lis + list(map(str,[valja, sisse, count]))))

    def stat_msg2(self):
        """Kahepoolse vestlemise tabel."""
        paarid = set()
        key = 'next'
        self.excel.ws('Msg to 2')
        f=self.excel
        print('X\tY\tX->Y\tY->X\tTehe', file=f)
        for uid in self.users:
            for nxt in self.users[uid][key]:
                if (nxt, uid) not in paarid:  # self.users[nxt][key][uid]
                    paarid.add((uid, nxt))
                    if uid in self.users[nxt][key]:
                        sisse = self.users[nxt][key][uid]
                        valja = self.users[uid][key][nxt]
                        count = min([sisse / valja, valja / sisse]) * min([sisse, valja])
                        if count > 1:
                            l = list(sorted([self.users[uid]['n'], self.users[nxt]['n']])) + list(map(str,[valja, sisse, count]))
                            self.excel.write('\t'.join(l))

    def stat_weeks(self):  # Kutsuda välja enne cleanup-i
        weeks=dict()
        self.ajaformaat
        """
        # Idee: stat nädalanumbritega, aktiivsed nädalad.
        >>> import datetime
        >>> datetime.date(2010, 6, 16).isocalendar()[1]
        """
        # Times2 on halb, sest seal on ainulttop25 ja kõik ülejäänud.
        for aeg in self.times2:
            #print(aeg)
            asd=datetime.datetime.strptime(aeg,self.ajaformaat).isocalendar()
            week=datetime.datetime.strptime(aeg,self.ajaformaat).isocalendar()[:2]
            if week not in weeks:
                weeks[week]=dict()
            for kanal in self.times2[aeg]:
                #print(kanal)
                for uid in self.times2[aeg][kanal]:
                    #print(uid)
                    if uid not in weeks[week]:
                        weeks[week][uid]=0
                    weeks[week][uid]+=self.times2[aeg][kanal][uid]
        self.weeks=weeks
        ########  Start tabeli tegemine
        
        self.excel.ws('Nädalad')
        head=['Aasta','Nädal']+ list(map(lambda x:self.users[x]['n'], sorted(self.users)))
        self.excel.write('\t'.join(head))
        for week in sorted(weeks):
            out=[str(week[0]),str(week[1])]
            for uid in sorted(self.users):
                if uid in weeks[week]:
                    out.append(str(weeks[week][uid]))
                else:out.append('')
            self.excel.write('\t'.join(out))
            # print(week, weeks[week])
    def times2_cleanup(self,n=25):
        ###  ----   Times2/times3 Eri
        # Lugeda kokku enim postituste TOP_N (25) ja ülejäänute statistika liita.
        self.top_n=list(filter(lambda x:x>=0,sorted(self.users,key=lambda x:self.users[x]['count']['Kokku'],reverse=True)))[:n]
        print(self.top_n)
        for date in self.times2:
            for kanal in self.times2[date]:
                counter=0
                for uid in list(self.times2[date][kanal]):
                    if uid not in self.top_n:
                        counter+=self.times2[date][kanal][uid]
                        del self.times2[date][kanal][uid]
                self.times2[date][kanal][-1]=counter
        ###  ----   Times2/times3 Eri läbi
    
    def stat_last_24(self):
        """Kasutajate aktiivsus viimased 24 tundi või päeva."""
        e=sorted(self.times2,key=lambda x:datetime.datetime.strptime(x,self.ajaformaat))[-24:]
        q=set()
        usrs=set()
        for i in e:
            q=q.union(self.times2[i])
            for x in self.times2[i]:
                usrs=usrs.union(set(self.times2[i][x]))
        usrs=list(sorted(usrs))
        us2=list(map(lambda x: self.users[x]['n'],usrs))
        q=list(sorted(q))
        self.excel.ws('Last '+str(24))
        f=self.excel
        print('\t'.join(['Kuupäev','Kanal']+us2), file=f)
        for i in e:
            for kanal in q:
                out=[]
                if kanal not in self.times2[i]:
                    continue
                out.append(i)
                out.append(kanal)
                for use in usrs:
                    if use in self.times2[i][kanal]:
                        out.append(self.times2[i][kanal][use])
                    else:
                        out.append(0)
                print('\t'.join(list(map(str,out))), file=f)

    def graafik(self):
        """Pygame joonistamine. Väga KATKI!"""
        import pygame
        colors, c = dict(), 0
        for i1 in self.channels:
            colors[i1] = tuple(map(lambda x: round(255 * x), colorsys.hsv_to_rgb(0.618033988749895 * c, 1, 1)))
            c += 1
        pygame.init()
        lava = pygame.display.set_mode((min(len(self.times), 10000), len(self.users)), 0, 32)
        # pygame.draw.rect(lava, (255,255,255),(5,5,10,10))
        pygame.display.update()
        for x1 in list(self.users):
            count, c_len = 0, 0
            for c in self.users[x1]['times']:  # Iga kanaliga
                for stamp in self.users[x1]['times'][c]:  # Iga ajatempel
                    pygame.draw.rect(lava, colors[c], (self.times.index(stamp) % 10000, x1, 2, 3))
            self.users[x1]['count']['total'] = count
            self.users[x1]['lens']['total'] = c_len
            pygame.display.update()
        pygame.image.save(lava, self.OUTPUT_FOLDER+"screenshot.jpeg")
        for i1 in sorted(colors):
            print(i1, colors[i1])
        pygame.quit()

def stats_load(fname='d_stats.pkl'):
    """PKL -> Self. Terve objekti avamine."""
    with open(fname, 'rb') as f:
        print(f)
        x = pickle.load(f)
    return x

def stat_full(*args, **kwargs):
    print('Algus', end=' ')
    sts = Stats(*args, **kwargs)
    print('1', end=' ')
    sts.stat_weeks()
    sts.times2_cleanup()
    sts.ajatabel_suur()
    print('2', end=' ')
    sts.arhiiv()
    print('3', end=' ')
    sts.out_tgf_msg()
    sts.out_tgf_tag()
    sts.out_users_json()
    sts.out_users_py()
    print('4', end=' ')
    sts.stat_last_24()
    sts.stat_msg()
    sts.stat_msg2()
    sts.stat_tag()
    sts.stat_tag2()
    print('5', end=' ')
    sts.graafid_edetabel(-1,n=5,uid=True)
    sts.graafid_edetabel('ago',n=5,uid=False)
    sts.graafid_edetabel(-1,n=10,uid=True)
    sts.graafid_edetabel('ago',n=5,uid=False)
    print('6', end=' ')
    sts.excel.close()
    sts.save()
    """
    print('7',end=' ')
    ani = Animate(sts)
    ani.draw_main()"""
    print('done')
    return sts



# def __init__(self, fname='dht.txt',OUTPUT_FOLDER='Python/',  sname='stats.xlsx', kategooria=kategooriad_py):
print('Pyyton')
# sts = stat_full('dht.txt', 'Python/', kategooria=kategooriad_py)  # Python
print('Java')
sts = stat_full('dht_java.txt', 'Java/', kategooria=kategooriad_java)  # Java
print('Kaug')
sts = stat_full('dht_kaug.txt', 'Kaug/', kategooria=kategooriad_kaug)  # Kaug



"""
# Kirjutab välja Stats-objekti lapsed.
for i in list(filter(lambda x: x[0] != '_', dir(sts))):
    if type(eval('sts.' + i)).__name__ == 'type':
        for x in list(filter(lambda x: x[0] != '_', dir(eval('sts.' + i)))):
            print('sts.' + i + '.' + x, str(eval('sts.' + i + '.' + x))[:40], sep='\t')
    else:
        print('sts.' + i, str(eval('sts.' + i))[:35].strip(), sep='\t')
# """
"""
# JSON iga kasutaja sõnakasutusest.
with open('sõnastats.txt',encoding='utf-8') as f:
	a=json.load(f)
# """
