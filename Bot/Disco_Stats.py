# -*- coding: UTF-8 -*-
"""
Discordi statistika objekti lugemise moodul.

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

"""

import datetime
import json
import pickle


# OUTPUT_FOLDER-i Lõppu käib kaldkriips
class Stats:
    """Statistika."""

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
            self.excel.write(
                '\t'.join([str(c), self.users[i1]['n'], str(self.lyhi[i1]), str(self.users[i1]['count']['Kokku']),
                           str(round(self.lyhi[i1] / self.users[i1]['count']['Kokku'] * 100, 2))]))
            c += 1

    def ajatabel_suur(self):
        """Koosta suur tabel iga nime, kanali, kellaaja ja kuupäeva kohta."""
        self.excel.ws('Ajatabel')
        self.excel.write(self.header2)
        for x1 in list(self.users):
            for c in sorted(self.users[x1]['times']):  # Iga kanaliga
                print('\t'.join([self.users[x1]['n'], c] + list(map(str, self.users[x1]['times'][c]))), file=self.excel)

    def ajatabel_vaiksem(self, uid, kanal):
        """Ajatabelite sõnede tegemine."""
        out2 = [[self.users[uid]['n'], 'Kell'] + list(map(str, range(24)))]
        week = 'ETKNRLP'
        for i1 in range(7):
            out = ['', week[i1]] + list(map(str, self.users[uid]['times'][kanal][24 * i1:24 * (i1 + 1)]))
            out2.append(out)
        out2 = [''.join(list(map(lambda x: "{0:5}".format(x), i))) for i in zip(*out2)]

        return '\n'.join(out2)

    def render(self, x, mVal):
        if not x.isdigit(): return x
        arr = ['░   ', '░░  ', '░░░ ', '░░░░', '▒░░░', '▒▒░░', '▒▒▒░', '▒▒▒▒', '▓▒▒▒', '▓▓▒▒', '▓▓▓▒', '▓▓▓▓', '█▓▓▓',
               '██▓▓', '███▓', '████']
        return arr[min([(16 * int(x)) // mVal, 15])]

    def ajatabel_vaiksem2(self, uid, kanal):
        """Ajatabelite sõnede tegemine."""
        out2 = [[self.users[uid]['n'], 'Kell'] + list(map(lambda x: str(x) + ' ', range(24)))]
        week = 'ETKNRLP'
        mVal = max(self.users[uid]['times'][kanal])
        for i1 in range(7):
            out = ['', week[i1]] + list(map(str, self.users[uid]['times'][kanal][24 * i1:24 * (i1 + 1)]))
            out2.append(out)
        out2 = [''.join(list(map(lambda x: "{0:5}".format(self.render(x, mVal)), i))) for i in zip(*out2)]

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
        out = ''
        if not uid:
            uid = list(filter(lambda x: username.lower() in self.users[x]['n'].lower(), self.users))[0]
        else:
            uid = username
        out += '\n**Kirjutamised:**\n'
        # Enne/Peale keda kirjutad
        for i1 in sorted(self.users[uid]['prev'], key=lambda i: self.users[uid]['prev'][i])[-n:]:
            x = self.users[i1]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            y = self.users[uid]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            out += ' '.join(list(map(str, [x, '->', y, '\t', self.users[uid]['prev'][i1], 'korda']))) + '\n'
        out += '\n'
        for i1 in sorted(self.users[uid]['next'], key=lambda i: self.users[uid]['next'][i])[-n:]:
            x = self.users[uid]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            y = self.users[i1]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            out += ' '.join(list(map(str, [x, '->', y, ' \t', self.users[uid]['next'][i1], 'korda']))) + '\n'
        out += '\n**Märkimised:**\n'
        # Kes keda märgib
        for i1 in sorted(self.users[uid]['tag_by'], key=lambda i: self.users[uid]['tag_by'][i])[-n:]:
            x = self.users[i1]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            y = self.users[uid]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            out += ' '.join(list(map(str, [x, '->', y, ' \t', self.users[uid]['tag_by'][i1], 'korda']))) + '\n'
        out += '\n'
        for i1 in sorted(self.users[uid]['tag_to'], key=lambda i: self.users[uid]['tag_to'][i])[-n:]:
            x = self.users[uid]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            y = self.users[i1]['n'].encode('iso8859_13', 'replace').decode('iso8859_13')
            out += ' '.join(list(map(str, [x, '->', y, ' \t', self.users[uid]['tag_to'][i1], 'korda']))) + '\n'
        out += '\n'
        return out

    def save(self, fname='d_stats.pkl'):
        """Self -> PKL. Terve objekti salvestamine."""
        temp = self.excel
        self.excel = None
        with open(self.OUTPUT_FOLDER + fname, 'wb') as f:
            pickle.dump(self, f, pickle.HIGHEST_PROTOCOL)
        self.excel = temp

    def out_users_py(self, fname='users.py'):
        """Self.users -> Python. Kena väljund."""
        with open(self.OUTPUT_FOLDER + fname, 'w', encoding='utf-8') as f:
            f.write('users=' + str(self.users))

    def out_users_json(self, fname='ergo.json'):
        """Self.users -> JSON. Kole väljund."""
        use = json.dumps(self.users)
        with open(self.OUTPUT_FOLDER + fname, 'w', encoding='utf-8') as f:
            f.write(str(use))

    def out_tgf_tag(self, fname='disco_tag.tgf'):
        """Märkimiste põhjal TGF-graaf."""
        with open(self.OUTPUT_FOLDER + fname, 'w', encoding='utf-8') as f:
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
        with open(self.OUTPUT_FOLDER + fname, 'w', encoding='utf-8') as f:
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
        f = self.excel
        print('\t'.join('X Y X->Y'.split()), file=f)
        for uid in self.users:
            for nxt in self.users[uid]['tag_to']:
                count = self.users[uid]['tag_to'][nxt]
                if count >= 1:
                    self.excel.write('\t'.join([self.users[uid]['n'], self.users[nxt]['n'], str(count)]))

    def stat_msg(self):
        """Sõnumite statisika, kui palju on X->Y sõnumeid."""
        self.excel.ws('Msg to')
        f = self.excel
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
        f = self.excel
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
                            self.excel.write('\t'.join(lis + list(map(str, [valja, sisse, count]))))

    def stat_msg2(self):
        """Kahepoolse vestlemise tabel."""
        paarid = set()
        key = 'next'
        self.excel.ws('Msg to 2')
        f = self.excel
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
                            l = list(sorted([self.users[uid]['n'], self.users[nxt]['n']])) + list(
                                map(str, [valja, sisse, count]))
                            self.excel.write('\t'.join(l))

    def times2_cleanup(self, n=25):
        ###  ----   Times2/times3 Eri
        # Lugeda kokku enim postituste TOP_N (25) ja ülejäänute statistika liita.
        self.top_n = list(
            filter(lambda x: x >= 0, sorted(self.users, key=lambda x: self.users[x]['count']['Kokku'], reverse=True)))[
                     :n]
        print(self.top_n)
        for date in self.times2:
            for kanal in self.times2[date]:
                counter = 0
                for uid in list(self.times2[date][kanal]):
                    if uid not in self.top_n:
                        counter += self.times2[date][kanal][uid]
                        del self.times2[date][kanal][uid]
                self.times2[date][kanal][-1] = counter
        ###  ----   Times2/times3 Eri läbi

    def stat_last_24(self):
        """Kasutajate aktiivsus viimased 24 tundi või päeva."""
        e = sorted(self.times2, key=lambda x: datetime.datetime.strptime(x, self.ajaformaat))[-24:]
        q = set()
        usrs = set()
        for i in e:
            q = q.union(self.times2[i])
            for x in self.times2[i]:
                usrs = usrs.union(set(self.times2[i][x]))
        usrs = list(sorted(usrs))
        us2 = list(map(lambda x: self.users[x]['n'], usrs))
        q = list(sorted(q))
        self.excel.ws('Last ' + str(24))
        f = self.excel
        print('\t'.join(['Kuupäev', 'Kanal'] + us2), file=f)
        for i in e:
            for kanal in q:
                out = []
                if kanal not in self.times2[i]:
                    continue
                out.append(i)
                out.append(kanal)
                for use in usrs:
                    if use in self.times2[i][kanal]:
                        out.append(self.times2[i][kanal][use])
                    else:
                        out.append(0)
                print('\t'.join(list(map(str, out))), file=f)


def stats_load(fname='d_stats.pkl'):
    """PKL -> Self. Terve objekti avamine."""
    with open(fname, 'rb') as f:
        print(f)
        x = pickle.load(f)
    return x