# -*- coding: UTF-8 -*-
"""
Asjandus discordi json-arhiivi töötlemiseks.

Klassikaline lähenemine statistikale.
Edasine arendamine käib siitkaudu

Stats.ajatabel_suur     Koosta suur tabel iga nime, kanali, kellaaja ja kuupäeva kohta.
Stats.ajatabel_vaike    UI ajatabelite kuvamiseks
Stats.ajatabel_vaiksem  Ajatabelite sõnede tegemine.
Stats.arhiiv            Tagastab palju asju. Sõnumite kogupikkus, arv, keskmine pikkus kasutaja/kanali lõikes.
Stats.graafid_edetabel  Kuva N populaarseimat suunda.
Stats.graafik           Pygame joonistamine.
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
                            "videod": {"Yldine", "Kokku"},
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
        for c in self.archive['data']:  # c = kanali id
            cur_name = self.archive['meta']['channels'][c]['name']  # Praeguse kanali nimi
            cur_name = cur_name.split('_')[0]
            prev_msg = -1
            print(cur_name[:1] + cur_name[-2:], end=' ')
            for m in sorted(self.archive['data'][c]):               # m = sõnumi ID
                message = self.archive['data'][c][m]
                if len(message['m'].strip().split()) < 2:           # Ühesõnaliste sõnumitega opereerimine
                    if message['u'] not in self.lyhi:
                        self.lyhi[message['u']] = 0                 # Loendab lühikesi sõnumeid
                    self.lyhi[message['u']] += 1
                    # continue                                      # Lühikese sõnumi saab vahele jätta
                print(message['m'].lower(), file=f)                 # Kopeeri sõnum faili
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

                for sub in [cur_name] + list(self.kategooriad[cur_name]):
                    if sub not in self.users[uid]['count']:         # Kui see sõnum on kasutaja
                        self.users[uid]['count'][sub] = 0           # esimene sõnum antud kanalis
                        self.users[uid]['lens'][sub] = 0            # init loendurid
                        self.users[uid]['times'][sub] = [0] * 168   # Iga tunni jaoks
                    self.users[uid]['count'][sub] += 1
                    self.users[uid]['lens'][sub] += len(message['m'])
                    self.users[uid]['times'][sub][24 * wk + hr] += 1

                uid2 = uid
                uid = -1                                            # Kõigi kasutajate ühisstatistika
                for sub in [cur_name] + list(self.kategooriad[cur_name]):
                    if sub not in self.users[uid]['count']:         # Kui see sõnum on kasutaja
                        self.users[uid]['count'][sub] = 0           # esimene sõnum antud kanalis
                        self.users[uid]['lens'][sub] = 0            # init loendurid
                        self.users[uid]['times'][sub] = [0] * 168   # Iga tunni jaoks
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

        self.times = list(sorted(self.times))
        f.close()
        print()

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
            for c in sorted(self.users[x1]['times']):               # Iga kanaliga
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
        """Kuva N populaarseimat suunda."""
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
                for nxt in self.users[uid]['nxt']:
                    count = self.users[uid]['nxt'][nxt]
                    if count >= 1:
                        print(uid, nxt, count, file=f)

    def stat_tag(self):
        """Tag statisika, kui palju on X->Y märkimisi."""
        with open('d_out_tag.txt', 'w', encoding='utf-8') as f:
            print('X Y X->Y'.split(), file=f, sep='\t')
            for uid in self.users:
                for nxt in self.users[uid]['tag_to']:
                    count = self.users[uid]['tag_to'][nxt]
                    if count >= 1:
                        print(self.users[uid]['n'], self.users[nxt]['n'], count, file=f, sep='\t')

    def stat_msg(self):
        """Sõnumite statisika, kui palju on X->Y sõnumeid."""
        with open('d_out_msg.txt', 'w', encoding='utf-8') as f:
            print('X Y X->Y'.split(), file=f, sep='\t')
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
            print('X Y X->Y Y->X Tehe'.split(), file=f, sep='\t')
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

    def graafik(self):
        """Pygame joonistamine."""
        import pygame
        colors, c = dict(), 0
        for i1 in self.channels:
            colors[i1] = tuple(map(lambda x: 255 * x, colorsys.hsv_to_rgb(0.618033988749895 * c, 1, 1)))
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


sts = Stats()
"""
for i in list(filter(lambda x: x[0] != '_', dir(sts))):
    if type(eval('sts.' + i)).__name__ == 'type':
        for x in list(filter(lambda x: x[0] != '_', dir(eval('sts.' + i)))):
            print('sts.' + i + '.' + x, str(eval('sts.' + i + '.' + x))[:40], sep='\t')
    else:
        print('sts.' + i, str(eval('sts.' + i))[:35].strip(), sep='\t')
#"""
