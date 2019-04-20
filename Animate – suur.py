import pygame
import datetime, colorsys, os
from math import log

import inspect
def lineno(): return inspect.currentframe().f_back.f_lineno

ajaformaat = '%a %d %b %Y %H:00'  # 'Thu 15 Nov 2018 14:00'
ajaformaat = '%a %d %b %Y'          # Kasutusel koos times2-ga
class Animate:
    ### Kogu soust tuleb nüüd ümber kirjutada
    def __init__(self, data, ushmm, channels):
        try: pygame.init()
        except:pass
        self.s = 20  # X-telje märgete kirjasuurus                                  # Default: 50
        self.ajatempel = 25  # Ajatempli kõrgus ülal vasakus nurgas                 # Default: 50
        self.legend_size = 30  # Legendi kirjakõrgus                                # Default: 30
        self.name_buffer = self.s * 2 + 5  # Eeldatav nimede ruum koos 5px varuga
        self.colors = dict()
        self.data = data
        self.users = ushmm[0]
        self.hmm=ushmm[1]
        self.channels=channels
        self.width = (len(channels) + 1) * self.s
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
        y_lines = (len(self.hmm) - 1) // x_columns+1
        self.y_hei = y_lines * self.y2
        self.day0 = min(data)
        self.day9 = max(data)
        c = 0
        # for i in list(filter(lambda x: x >= 0, sts.top_n)):
        for i in sorted(self.hmm):
            self.colors[i] = tuple(map(lambda x: min([round(255 * x), 255]),
                            colorsys.hsv_to_rgb(0.618033988749895 * c, 1 - c // 5 * 0.01, 1 - c // 3 * 0.005)))
            c += 1
        # """
        self.colors['-1']=(50,50,50)  # Ülejäänud
        self.colors[0]=(200,200,200)  # Rauno?
        self.colors[1]=(255,200,200)  # Kadri
        self.colors[2]=(200,255,200)  # Ago
        self.colors[3]=(200,200,255)  # Test9
        self.colors[4]=(255,255,200)  # Ergo
        self.hei = self.graafiku_osa + self.y_hei + self.name_buffer + self.ajatempel
        maks_vals=list()
        for time in self.data:
            for ch in self.data[time]['chs']:
                maks_vals.append(0)
                for u in self.data[time]['chs'][ch]:
                    maks_vals[-1]+=self.data[time]['chs'][ch][u]
        mx=max(maks_vals)
        col_h=log(mx+1)
        self.vahemiku_max = mx  # col_h

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
        for i in range(len(channels)):
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
        for i in hmm+['-1']:

            txt = users[i][0]
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
        column=pygame.surface.Surface((w,h), pygame.SRCALPHA)
        column_nr = self.channels.index(kanal)
        s = 0
        #    Midagi tuleb ette võtta recalc-funktsiooniga.
        #print(lineno(), data[kanal])
        
        for uid in sorted(data[kanal],reverse=True):
            # Joonista kasutaja rect
            #print(uid, data[kanal][uid], users[uid][0], self.colors[uid])
            s += data[kanal][uid]
        total=s
        if s!=0:
            y=0
            for uid in sorted(data[kanal],reverse=False):
                hei=data[kanal][uid]/s*h  # ühe kasutaja suhtelise ulatuse kõrgus
                pygame.draw.rect(column,self.colors[uid], (0, y, w,hei))
                y+=hei
        # self.graafiku_osa - veeru kõrgus-ajatempli kõrgus.
        y_h=round(log(total+1)/log(self.vahemiku_max+1) * self.graafiku_osa)  # Ülemine serv (kaugus alt)
        y_h2=round(log(total+1)/log(self.vahemiku_max+1)*self.graafiku_osa)  # Alumine serv
        y_h2=0
        
        #pygame.draw.rect(column,[255]*3, (0, h-y_h, w,h-y_h2))
        trans_overlay=pygame.surface.Surface((w*1.0,h-y_h), pygame.SRCALPHA).convert()
        trans_overlay.fill([0, 0, 0])
        #pygame.draw.rect(trans_overlay,[255,0,0], (0, 0, w*0.6,y_h*1.3))
        trans_overlay.set_alpha(round(0.65*255)) # 60%
        column.blit(trans_overlay, (0,0))
        """
            y_h=round(log(s+1)/log(self.vahemiku_max+1)*self.graafiku_osa)
            y_h2=round(log(s+data[kanal][uid]+1)/log(self.vahemiku_max+1)*self.graafiku_osa)
            y_h=round((s)/(self.vahemiku_max)*self.graafiku_osa)  # Loobusin logaritmidest
            y_h2=round((s+data[kanal][uid])/(self.vahemiku_max)*self.graafiku_osa)
            pygame.draw.rect(column,self.colors[uid], (0, h-y_h, w,h-y_h2))
            
            s += data[kanal][uid]
        """
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
        # print(lineno(), data)
        for kanal in data:
            column_nr = self.channels.index(kanal)
            out=self.draw_column(kanal,data)
            self.lava.blit(out,(self.s*column_nr,0))
            # pygame.display.flip()
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
        self.draw_x_axis(self.channels)        # X-telje joonistamine
        self.draw_user_legend()        # Legendi joonistamine
        self.draw_columns(self.times3[stamp]) # Joonista graafik. Tuleb veel läbi mõelda...
        # list(sorted(sts.times2,key=lambda x:datetime.datetime.strptime(x,sts.ajaformaat)))
        self.draw_timestamp(stamp)        # Lisa ajamärge
        pygame.display.flip()
        path='gif_suur/screenshot_'+"{:03d}".format(self.counter)+'_'+stamp+'.jpg'
        os.makedirs(os.path.dirname(path), exist_ok=True)
        pygame.image.save(self.lava, path)
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
                out[k]=max([0,round(decay_a*v-decay_b, 1),out[k]])
            else:
                out[k]=max([0,round(decay_a*v-decay_b, 1)])
                if out[k]==0:
                    del out[k]
        return out
    def draw_main(self):
        """Ma ei tea, milleks"""
        self.lava = pygame.display.set_mode((self.width, self.hei),1, 16)
        
        self.lava.fill([0,0,0])
        self.times3=dict()
        decay_a=0.8
        decay_b=5
        # datetime.datetime(2018, 8, 11, 2, 0)+datetime.timedelta(hours=1)
        if self.day0.hour==0==self.day9.hour and '%H' not in ajaformaat:
            delta = datetime.timedelta(days=1)
        else:
            delta = datetime.timedelta(hours=1)
        datum=self.day0
        self.counter=0
        dat_prev=0
        # Esimene kord
        date_text=datetime.datetime.strftime(datum,ajaformaat)
        self.times3[date_text]=data[datum]['chs']
        dat_prev=date_text
        self.draw(date_text)
        datum += delta
        while datum<=self.day9:
            date_text=datetime.datetime.strftime(datum,ajaformaat)
            if datum in self.data:
                new=self.data[datum]['chs']
                # print(lineno(), 'NEW: ',new)
            else:
                new=[]
            old=self.times3[dat_prev]#['chs']
            # print(lineno(), 'OLD:',old)
            dat_prev=date_text
            combined=dict()
            for kanal in set(old).union(set(new)):
                if kanal in new and kanal in old:
                    combined[kanal]=self.modifyEachValueInDictionary(old[kanal],new[kanal],decay_a,decay_b)
                elif kanal in new:
                    combined[kanal]=new[kanal]
                else:
                    # print(lineno(), old[kanal],None,decay_a,decay_b)
                    combined[kanal]=self.modifyEachValueInDictionary(old[kanal],None,decay_a,decay_b)
            self.times3[date_text]=combined
            self.draw(date_text)
            datum += delta
        pygame.quit()

####
# Tegevusplaan: PKL-failist võtame ainult kasutajate ja kanalite IDd. Edasine toimub raw-andmetega.
####
# Mida meil on vaja?
# data.archive['meta']['users']
# data.archive['meta']['channels']
import discord_class
from discord_class import Stats
server_dirs=['TTÜ IT 2018/', 'java 2019/','py2018/']
server_dirs.pop(0)
dirr=server_dirs[0]
channels=dict()  # ID: pikk_nimi
users=dict()
data=dict()  # kuupäev->kanal->kasutaja+kokku
for dirr in server_dirs:
    stat=discord_class.stats_load(dirr+'d_stats.pkl')
    us=stat.archive['meta']['users']
    ch=stat.archive['meta']['channels']
    for u in us:
        if u not in users:
            users[u]=[us[u]['name'], 0]
    for c in ch:
        channels[c]=ch[c]['name']
    f=open(dirr+'disc_sõnapilveks.txt', encoding='utf-8')
    f.readline()  # header
    for l in f: # Server	Channel	User	Timestamp	Message
        if l.count('\t')<4:
            continue
        srv,chn,user,time,*msg=l.split('\t')
        time2 = datetime.datetime.fromtimestamp(float(time))  # 1 sekundi täpsusega
        time_str = time2.strftime(ajaformaat)
        time_round=datetime.datetime.strptime(time_str, ajaformaat)
        if time_str not in data:
            data[time_round] = {'time':time_str, 'chs':dict()}
        #if chn not in data:
        #    data[time_str][chn] = dict()
        users[user][1]+=1
        ########## SIIT EDASI !!!
    f.close()
# Sorteeritud nimekiri ID-dega, kellel on enim sõnumeid.
users['-1']=['Ülejäänud', 0]
hmm=list(reversed(sorted(users, key=lambda x:users[x][1])[-30:]))
# Kanalite nimekiri
import re
pattern = re.compile(r"(ex|hw|pr|xp|dj)\d\d")
chs=dict()  # Channels kosolideeritult.,   ID: lyhike_nimi
for ch in channels:
    n=channels[ch]
    if pattern.match(n):
        n=n[:4]
    chs[ch]=n
# Hetkeseis: olemas sõnastik, kus jälgime ühendatavaid kanaleid.
# Samuti on teada, kõige aktiivsemad kasutajad (hmm).
def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)
times=list(data)
for i in daterange(min(data), max(data)):
    if i not in data:
        time_str = i.strftime(ajaformaat)
        print(time_str)
        data[i] = {'time':time_str, 'chs':dict()}

for dirr in server_dirs:
    f=open(dirr+'disc_sõnapilveks.txt', encoding='utf-8')
    f.readline()  # header
    for l in f: # Server	Channel	User	Timestamp	Message
        if l.count('\t')<4:
            continue
        srv,chn,user,time,*msg=l.split('\t')
        time2 = datetime.datetime.fromtimestamp(float(time))
        time_str = time2.strftime(ajaformaat)
        time_round=datetime.datetime.strptime(time_str, ajaformaat)
        kanal=chs[chn]
        if user not in hmm: user='-1'
        if kanal not in data[time_round]['chs']:
            data[time_round]['chs'][kanal] = dict()
        if user not in data[time_round]['chs'][kanal]:
            data[time_round]['chs'][kanal][user]=1
        else: data[time_round]['chs'][kanal][user]+=1
    print(time_str,list(data[time_round]))
    f.close()
# Järgmine, leida kanalite maksimum
maks_vals=list()
for time in data:
    for ch in data[time]['chs']:
        maks_vals.append(0)
        for u in data[time]['chs'][ch]:
            maks_vals[-1]+=data[time]['chs'][ch][u]
mx=max(maks_vals)
col_h=log(mx+1)
channels2=list(sorted(set(map(lambda x:chs[x],chs))))  # List lühinimedega

ani=Animate(data, [users, hmm], channels2)
ani.draw_main()
