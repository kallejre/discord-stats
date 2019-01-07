# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

Klassikaline lähenemine statistikale.
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

import colorsys
import datetime
import json
import re
import pickle


class Stats:
    """Statistika."""

    def __init__(self, fname='dht.txt'):
        """
        ###   INIT1   ###.

        Peamiselt muutujate algväärtustamine.
        """
        with open(fname, encoding='utf8') as f:
            file = f.read()
        self.archive = eval(file)
        self.users = dict()
        self.lyhi = dict()
        self.times = list()
        self.times2 = dict()
        # self.ajaformaat = '%a %d %b %Y %H:00'  # 'Thu 15 Nov 2018 14:00'
        self.ajaformaat = '%a %d %b %Y'          # Kasutusel koos times2-ga
        # max(sts.times2,key=lambda x:datetime.datetime.strptime(x,sts.ajaformaat))
        for x1 in range(len(self.archive['meta']['userindex'])):
            self.users[x1] = {'n': self.archive['meta']['users'][self.archive['meta']['userindex'][x1]]['name'],
                              'count': dict(), 'lens': dict(), 'times': dict(), 'next': dict(),
                              'prev': dict(), 'tag_by': dict(), 'tag_to': dict()}
        self.users[-1] = {'n': 'Kõik', 'count': dict(), 'lens': dict(),
                          'times': dict(), 'next': dict(), 'prev': dict(), 'tag_by': dict(), 'tag_to': dict()}
        # Kategooria peaks algama suure tähega
        self.kategooriad = {"dj01": {"Syva", "Kokku", "DJ"}, "dj02": {"Syva", "Kokku", "DJ"},
                            "ettepanekud": {"Yldine", "Kokku"}, "ex01": {"EX", "Kokku"}, "ex02": {"EX", "Kokku"},
                            "ex03": {"EX", "Kokku"}, "ex04": {"EX", "Kokku"}, "ex05": {"EX", "Kokku"},
                            "ex06": {"EX", "Kokku"},
                            "ex07": {"EX", "Kokku"}, "ex08": {"EX", "Kokku"}, "ex09": {"EX", "Kokku"},
                            "ex11": {"EX", "Kokku"},
                            "ex12": {"EX", "Kokku"}, "ex13": {"EX", "Kokku"}, "ex14": {"EX", "Kokku"},
                            "ex15": {"EX", "Kokku"},
                            "food": {"Yldine", "Kokku"}, "general": {"Yldine", "Kokku"}, "git": {"Yldine", "Kokku"},
                            "kaugōpe": {"Yldine", "Kokku"}, "konsult": {"Yldine", "Kokku"}, "meme": {"Yldine", "Kokku"},
                            "mitteniiolulisedagasiiskiolulised-teadaanded": {"Yldine", "Kokku"},
                            "pr03": {"PR", "Kokku"},
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
        channels = list(self.kategooriad)
        for a in list(channels):
            channels += list(self.kategooriad[a])
        self.channels = list(sorted(set(channels)))
        self.header = '\t'.join(['Nimi'] + self.channels + ['Kokku'])
        head = []
        for wk in 'ETKNRLP':
            for hr in range(24):
                head.append(wk + ' ' + str(hr))
        self.header2 = '\t'.join(['Nimi', 'Kanal'] + head)
        self.nimed2 = list(map(lambda uid: self.users[uid]['n'], self.users))
        self.nimed3 = list(map(lambda x: x.lower(), self.nimed2))
        # self.week=["Esmaspäev", "Teisipäev", "Kolmapäev", "Neljapäev", "Reede", "Laupäev", "Pühapäev"]
        self.week = ["Esmasp.", "Teisip.", "Kolmap.", "Neljap.", "Reede", "Laup.", "Pühap."]
        self.init2()

    def init2(self):
        """
        ###   INIT2   ###.

        Siin osas toimub andmete kogumine ja põhiline töötlemine.
        Alumised funktsioonid on vaid vormistamiseks ja kuvamiseks.
        Kunagi võiks teha mingi seadistamisvõimaluse.
        """
        f = open('disc_sõnapilveks.txt', 'w', encoding='utf8')
        for c in sorted(self.archive['data']):  # c = kanali id
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
                    # continue                                      # Lühikese sõnumi saab vahele jätta
                print(self.archive['meta']['userindex'][message['u']],message['m'].lower(), file=f,sep='\t')  # Kopeeri sõnum faili
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
            self.users[x]['count']['total'] = count
            self.users[x]['lens']['total'] = c_len
            if count < 3:
                continue
            out1 = [self.users[x]['n']]
            out2 = [self.users[x]['n']]
            out3 = [self.users[x]['n']]
            for kanal in self.channels:
                if kanal in self.users[x]['count']:
                    out1.append(str(self.users[x]['lens'][kanal]))
                    out2.append(str(self.users[x]['count'][kanal]))
                    out3.append(
                        str(round(self.users[x]['lens'][kanal] / self.users[x]['count'][kanal], 3)).replace('.', ','))
                else:
                    out1.append('0')
                    out2.append('0')
                    out3.append('0')
            out1.append(str(self.users[x]['lens']['total']))
            out2.append(str(self.users[x]['count']['total']))
            out3.append(
                str(round(self.users[x]['lens']['total'] / self.users[x]['count']['total'], 3)).replace('.', ','))
            pikkused.append('\t'.join(out1))
            kogus.append('\t'.join(out2))
            keskmine_pikkus.append('\t'.join(out3))
        with open('d_out1.txt', 'w', encoding='utf-8') as f:
            print('\n'.join([self.header] + pikkused), file=f)
        with open('d_out2.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join([self.header] + kogus))
        with open('d_out3.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join([self.header] + keskmine_pikkus))
        sisukus.append('Jrk.\tNimi\tLühike\tKõik\t%')
        c = 1
        for i1 in sorted(self.lyhi, key=lambda x: self.users[x]['count']['total'], reverse=True):
            out = '\t'.join([str(c), self.users[i1]['n'], str(self.lyhi[i1]), str(self.users[i1]['count']['total']),
                             str(round(self.lyhi[i1] / self.users[i1]['count']['total'] * 100, 2)).replace('.', ',')])
            sisukus.append(out)
            c += 1
        with open('d_out4.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(sisukus))

    def ajatabel_suur(self):
        """Koosta suur tabel iga nime, kanali, kellaaja ja kuupäeva kohta."""
        ajad = [self.header2]
        for x1 in list(self.users):
            total = []
            for c in sorted(self.users[x1]['times']):  # Iga kanaliga
                total.append(self.users[x1]['times'][c])
                ajad.append('\t'.join([self.users[x1]['n'], c] + list(map(str, total[-1]))))
            total = list(map(sum, list(zip(*total))))
            ajad.append('\t'.join([self.users[x1]['n'], 'Kokku'] + list(map(str, total))))
            # print(self.users[x]['times'])
        with open('d_out_ajatabel.txt', 'w', encoding='utf8') as f:
            f.write('\n'.join(ajad))
        print('done')

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

    def graafid_edetabel(self, username, n=5, uid=0):
        """Kuva N populaarseimat suunda ühe kasutaja suhtes."""
        if not uid:
            uid = list(filter(lambda x: username.lower() in self.users[x]['n'].lower(), self.users))[0]
        else:
            uid = username
        # Enne/Peale keda kirjutad
        for i1 in sorted(self.users[uid]['prev'], key=lambda i: self.users[uid]['prev'][i])[-n:]:
            print(self.users[i1]['n'], '->', self.users[uid]['n'], ' \t', self.users[uid]['prev'][i1], 'korda')
        print()
        for i1 in sorted(self.users[uid]['next'], key=lambda i: self.users[uid]['next'][i])[-n:]:
            print(self.users[uid]['n'], '->', self.users[i1]['n'], ' \t', self.users[uid]['next'][i1], 'korda')
        print('\nMärkimised:')
        # Kes keda märgib
        for i1 in sorted(self.users[uid]['tag_by'], key=lambda i: self.users[uid]['tag_by'][i])[-n:]:
            print(self.users[i1]['n'], '->', self.users[uid]['n'], ' \t', self.users[uid]['tag_by'][i1], 'korda')
        print()
        for i1 in sorted(self.users[uid]['tag_to'], key=lambda i: self.users[uid]['tag_to'][i])[-n:]:
            print(self.users[uid]['n'], '->', self.users[i1]['n'], ' \t', self.users[uid]['tag_to'][i1], 'korda')
        print()

    def save(self, fname='d_stats.pkl'):
        """Self -> PKL. Terve objekti salvestamine."""
        with open(fname, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
    def out_users_py(self, fname='users.py'):
        """Self.users -> Python. Kena väljund."""
        with open(fname, 'w', encoding='utf-8') as f:
            f.write('users=' + str(self.users))

    def out_users_json(self, fname='ergo.json'):
        """Self.users -> JSON. Kole väljund."""
        use = json.dumps(self.users)
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(str(use))

    def out_tgf_tag(self, fname='disco_tag.tgf'):
        """Märkimiste põhjal TGF-graaf."""
        with open(fname, 'w', encoding='utf-8') as f:
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
        with open(fname, 'w', encoding='utf-8') as f:
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
        with open('d_out_tag.txt', 'w', encoding='utf-8') as f:
            print('\t'.join('X Y X->Y'.split()), file=f)
            for uid in self.users:
                for nxt in self.users[uid]['tag_to']:
                    count = self.users[uid]['tag_to'][nxt]
                    if count >= 1:
                        print(self.users[uid]['n'], self.users[nxt]['n'], count, file=f, sep='\t')

    def stat_msg(self):
        """Sõnumite statisika, kui palju on X->Y sõnumeid."""
        with open('d_out_msg.txt', 'w', encoding='utf-8') as f:
            print('\t'.join('X Y X->Y'.split()), file=f)
            for uid in self.users:
                for nxt in self.users[uid]['next']:
                    count = self.users[uid]['next'][nxt]
                    if count >= 1:
                        print(self.users[uid]['n'], self.users[nxt]['n'], count, file=f, sep='\t')

    def stat_tag2(self):
        """Kahepoolse märkimise tabel."""
        paarid = set()
        key = 'tag_to'
        with open('d_out_msg2.txt', 'w', encoding='utf-8') as f:
            print('\t'.join('X Y X->Y Y->X Tehe'.split()), file=f)
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
                                print(*lis + [valja, sisse, str(count).replace('.', ',')], file=f, sep='\t')

    def stat_msg2(self):
        """Kahepoolse vestlemise tabel."""
        paarid = set()
        key = 'next'
        with open('d_out_msg2.txt', 'w', encoding='utf-8') as f:
            print('X Y X->Y Y->X Tehe'.split(), file=f, sep='\t')
            for uid in self.users:
                for nxt in self.users[uid][key]:
                    if (nxt, uid) not in paarid:  # self.users[nxt][key][uid]
                        paarid.add((uid, nxt))
                        if uid in self.users[nxt][key]:
                            sisse = self.users[nxt][key][uid]
                            valja = self.users[uid][key][nxt]
                            count = min([sisse / valja, valja / sisse]) * min([sisse, valja])
                            if count > 1:
                                l = list(sorted([self.users[uid]['n'], self.users[nxt]['n']]))
                                print(*l + [valja, sisse, str(count).replace('.', ',')], file=f, sep='\t')
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
        with open('d_out_last24.txt', 'w', encoding='utf-8') as f:
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
        pygame.image.save(lava, "screenshot.jpeg")
        for i1 in sorted(colors):
            print(i1, colors[i1])
        pygame.quit()
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


class Animate:
    ### Kogu soust tuleb nüüd ümber kirjutada
    def __init__(self, sts):
        self.s = 20  # X-telje märgete kirjasuurus                                  # Default: 50
        self.ajatempel = 25  # Ajatempli kõrgus ülal vasakus nurgas                 # Default: 50
        self.legend_size = 30  # Legendi kirjakõrgus                                # Default: 30
        self.name_buffer = self.s * 2 + 5  # Eeldatav nimede ruum koos 5px varuga
        self.colors = dict()
        self.sts = sts
        self.width = (len(sts.channels) + 1) * self.s
        self.graafiku_osa = 250
        self.font_name = 'agencyFB'
        pygame.font.init()
        # self.sts.top_n
        # self.sts.users
        sizes = self.draw_user_legend(simulate=True)
        ls = len(sizes)
        sizes.sort()
        x=0.9
        self.x2 = sizes[round(ls * x)]
        self.y2 = self.legend_size + 3
        x_columns = self.width // self.x2
        y_lines = (len(self.sts.top_n) - 1) // x_columns+1
        self.y_hei = y_lines * self.y2
        self.day0 = datetime.datetime.strptime(min(sts.times2,key=lambda x:datetime.datetime.strptime(x,sts.ajaformaat)),sts.ajaformaat)
        self.day9 = datetime.datetime.strptime(max(sts.times2,key=lambda x:datetime.datetime.strptime(x,sts.ajaformaat)),sts.ajaformaat)
        c = 0
        for i in list(filter(lambda x: x >= 0, sts.top_n)):
            self.colors[i] = tuple(map(lambda x: min([round(255 * x), 255]),
                            colorsys.hsv_to_rgb(0.618033988749895 * c, 1 - i // 5 * 0.01, 1 - i // 3 * 0.005)))
            c += 1
        # """
        self.colors[-1]=(50,50,50)  # Ülejäänud
        self.colors[0]=(200,200,200)  # Rauno?
        self.colors[1]=(255,200,200)  # Kadri
        self.colors[2]=(200,255,200)  # Ago
        self.colors[3]=(200,200,255)  # Test9
        self.colors[4]=(255,255,200)  # Ergo
        self.hei = self.graafiku_osa + self.y_hei + self.name_buffer + self.ajatempel
        maksimumid = set()
        for time in sts.times2:
            for kanal in sts.times2[time]:
                s = 0
                for uid in sts.times2[time][kanal]:
                    s += sts.times2[time][kanal][uid]
                maksimumid.add(s)
        self.vahemiku_max = max(maksimumid)

    def draw_timestamp(self, stamp, pos=(5, 0), color=(200, 000, 000), font='agencyFB'):
        stamp = str(stamp)
        font = pygame.font.SysFont(self.font_name, int(self.ajatempel * 0.8333333))
        text = font.render(stamp, True, color)
        self.lava.blit(text, pos)

    def draw_x_axis(self, channels):
        # X-telje joonistamine
        y_t = self.hei - self.name_buffer - self.y_hei
        color = (200, 000, 000)
        
        font = pygame.font.SysFont(self.font_name, int(self.s * 0.8333333))
        for i in range(len(self.sts.channels)):
            x_t = (i * self.s)
            txt = str(channels[i])
            text = font.render(txt, True, color)
            overflow = pygame.surface.Surface((self.s * 2, int(self.s * 1)))
            overflow.blit(text, (0, 0))
            overflow = pygame.transform.rotate(overflow, 90)
            self.lava.blit(overflow, (x_t, y_t))

    def draw_user_legend(self, simulate=False):

        # Legendi joonistamine:
        if not simulate:
            y = self.hei - self.y_hei
            x = 10
        size = self.legend_size
        font = pygame.font.SysFont(self.font_name, int(size * 0.8333333))
        txt_color = (200, 000, 000)
        out = []
        for i in list(filter(lambda x: x >= 0, self.sts.top_n))+[-1]:

            txt = self.sts.users[i]['n']
            text = font.render(txt, True, txt_color)
            overflow = pygame.surface.Surface((text.get_size()[0] + int(size * 0.8), int(size)))
            if not simulate:
                overflow.blit(text, (int(size * 0.8), 0))
                pygame.draw.rect(overflow, self.colors[i],
                                 (int(size * 0.1), int(size * 0.2), int(size * 0.6), int(size * 0.6)))
                self.lava.blit(overflow, (x, y))

                y += self.y2
                if y + self.y2 > self.hei:
                    y = self.hei - self.y_hei
                    x += self.x2

            out.append(overflow.get_size()[0])
        return out
    def draw_column(self,kanal,data):
        """Koosta standartse laiuse ja kõrgusega tulp, ära joonista."""
        # Ei tulnud hästi välja. Järgmine idee: TOP25 ja ülejäänud
        w,h=self.s,self.graafiku_osa+self.ajatempel*1
        column=pygame.surface.Surface((w,h))
        column_nr = ani.sts.channels.index(kanal)
        s = 0
        for uid in sorted(data[kanal],reverse=True):
            # Joonista kasutaja rect
            y_h=round(log(s+1)/log(self.vahemiku_max+1)*self.graafiku_osa)
            y_h2=round(log(s+data[kanal][uid]+1)/log(self.vahemiku_max+1)*self.graafiku_osa)
            y_h=round((s)/(self.vahemiku_max)*self.graafiku_osa)  # Loobusin logaritmidest
            y_h2=round((s+data[kanal][uid])/(self.vahemiku_max)*self.graafiku_osa)
            pygame.draw.rect(column,self.colors[uid], (0, h-y_h, w,h-y_h2))
            
            s += data[kanal][uid]
        return column
        #y_h=round(log(s+1)/log(self.vahemiku_max+1)*self.graafiku_osa)
        #pygame.draw.rect(self.lava,[220]*3,(self.s*column_nr,self.graafiku_osa+self.ajatempel-y_h,self.s,y_h))
    def draw_columns(self,data=None):
        if not data:
            return
        # Tulpade joonistamine
        # self.vahemiku_max
        
        self.ajatempel  # Ajatempli kõrgus ülal vasakus nurgas
        self.graafiku_osa
        for kanal in data:
            column_nr = self.sts.channels.index(kanal)
            out=self.draw_column(kanal,data)
            self.lava.blit(out,(self.s*column_nr,0))
            """
            column_nr = ani.sts.channels.index(kanal)
            s = 0
            for uid in data[kanal]:
                s += data[kanal][uid]
            y_h=round(log(s+1)/log(self.vahemiku_max+1)*self.graafiku_osa)
            pygame.draw.rect(self.lava,[220]*3,(self.s*column_nr,self.graafiku_osa+self.ajatempel-y_h,self.s,y_h))
            """
    def draw(self,stamp):
        """Ühe kaadri joonistamine."""
        self.lava.fill([0,0,0])
        self.draw_x_axis(sts.channels)        # X-telje joonistamine
        self.draw_user_legend()        # Legendi joonistamine
        self.draw_columns(self.times3[stamp]) # Joonista graafik. Tuleb veel läbi mõelda...
        # list(sorted(sts.times2,key=lambda x:datetime.datetime.strptime(x,sts.ajaformaat)))
        self.draw_timestamp(stamp)        # Lisa ajamärge
        pygame.display.flip()
        pygame.image.save(self.lava, 'gif/screenshot_'+"{:03d}".format(self.counter)+'_'+stamp+'.jpeg')
        self.counter+=1
    def modifyEachValueInDictionary(self,old,new,decay_a,decay_b):
        # max([0,decay_a*old[kanal]-decay_b,new[kanal]])
        # max([0,decay_a*old[kanal]-decay_b])
        out=dict()
        if new:
            for k,v in new.items():
                out[k]=v
        for k,v in old.items():
            if k in out:
                out[k]=max([0,decay_a*v-decay_b,out[k]])
            else:
                out[k]=max([0,decay_a*v-decay_b])
        return out
    def draw_main(self):
        """Ma ei tea, milleks"""
        self.lava = pygame.display.set_mode((self.width, self.hei), 0, 32)
        self.lava.fill([0,0,0])
        self.times3=dict()
        decay_a=0.8
        decay_b=1
        # datetime.datetime(2018, 8, 11, 2, 0)+datetime.timedelta(hours=1)
        if self.day0.hour==0==self.day9.hour and '%H' not in self.sts.ajaformaat:
            delta = datetime.timedelta(days=1)
        else:
            delta = datetime.timedelta(hours=1)
        datum=self.day0
        self.counter=0
        dat_prev=0
        # Esimene kord
        date_text=datetime.datetime.strftime(datum,self.sts.ajaformaat)
        self.times3[date_text]=self.sts.times2[date_text]
        dat_prev=date_text
        self.draw(date_text)
        datum += delta
        while datum<=self.day9:
            date_text=datetime.datetime.strftime(datum,self.sts.ajaformaat)          
            if date_text in self.sts.times2:
                new=self.sts.times2[date_text]
            else:
                new=[]
            old=self.times3[dat_prev]
            dat_prev=date_text
            combined=dict()
            for kanal in set(old).union(set(new)):
                if kanal in new and kanal in old:
                    combined[kanal]=self.modifyEachValueInDictionary(old[kanal],new[kanal],decay_a,decay_b)
                elif kanal in new:
                    combined[kanal]=new[kanal]
                else:
                    combined[kanal]=self.modifyEachValueInDictionary(old[kanal],None,decay_a,decay_b)

            self.times3[date_text]=combined
            self.draw(date_text)
            datum += delta
        pygame.quit()



def stats_load(fname='d_stats.pkl'):
    """PKL -> Self. Terve objekti avamine."""
    with open(fname, 'rb') as f:
        print(f)
        x = pickle.load(f)
    return x

sts = Stats()
sts.times2_cleanup()

sts.ajatabel_suur()
sts.arhiiv()
sts.out_tgf_msg()
sts.out_tgf_tag()
sts.out_users_json()
sts.out_users_py()
sts.stat_last_24()
sts.stat_msg()
sts.stat_msg2()
sts.stat_tag()
sts.stat_tag2()
sts.save()

import pygame
from math import log
# pygame.init()
# ani = Animate(sts)
# ani.draw_main()

"""
for i in list(filter(lambda x: x[0] != '_', dir(sts))):
    if type(eval('sts.' + i)).__name__ == 'type':
        for x in list(filter(lambda x: x[0] != '_', dir(eval('sts.' + i)))):
            print('sts.' + i + '.' + x, str(eval('sts.' + i + '.' + x))[:40], sep='\t')
    else:
        print('sts.' + i, str(eval('sts.' + i))[:35].strip(), sep='\t')
# """
"""
with open('sõnastats.txt',encoding='utf-8') as f:
	a=json.load(f)
# """
