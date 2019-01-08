import pygame
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
