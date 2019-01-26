class impo:
    import math
    import os
    import urllib.request
    import json
    import xmltodict
    import time
    import urllib.parse
    import tkinter as tk
    from tkinter import ttk
    from tkinter import filedialog as tk_filedialog
    import inspect
    import gpxpy
from ilmajaamad import cache as cache # Juhuks kui peaks tekkima lisa cache
error_counter=dict()
printer=False
# Üks vana koodijupp
# Allikat ei mäleta.
# Teeb Google mapsi koordinaadipäringu
def coord(address):
    params = {'address' : address, 'sensor' : 'false'}
    url = 'https://maps.google.com/maps/api/geocode/json?key=AIzaSyD7ffhr22Fo8AMiGc0KPYw0L_MrPFftdMI&' + impo.urllib.parse.urlencode(params)
    response = impo.urllib.request.urlopen(url)
    result = impo.json.loads(response.read().decode(response.headers.get_content_charset()))
    return result
    # print(result)
    try:
        return result['results'][0]['geometry']['location']
    except:
        return [None,result]
def elev(coors): # Kõrguspäringu prototüüp, pole kasutuses
    url = 'https://maps.googleapis.com/maps/api/elevation/json?key=AIzaSyD7ffhr22Fo8AMiGc0KPYw0L_MrPFftdMI&locations='
    t=[]
    for i in coors:
        t.append(str(i[0])+','+str(i[1]))
    url+='|'.join(t)
    response = impo.urllib.request.urlopen(url)
    result = impo.json.loads(response.read().decode(response.headers.get_content_charset()))
    try:
        return list(map(lambda x:round(x['elevation'],3),result['results']))
    except:
        return [None,result]
def pun2di(punk):
    return {'lat':punk.lat,'lng':punk.lng}
def dist(loc1, loc2):	# Vahemaa km kahe asukoha vahel
    #Tõlgitud javast
	# https://et.wikipedia.org/wiki/Ortodroom
    l1, g1=impo.math.radians(loc1['lat']),impo.math.radians(loc1['lng'])
    l2, g2=impo.math.radians(loc2['lat']),impo.math.radians(loc2['lng'])
    raadius = 6371.01   # Maa raadius km
    dg=g1-g2            # Pikkuskraadide vahe
    p0 = impo.math.cos(l2) * impo.math.cos(dg)
    p1 = impo.math.cos(l2) * impo.math.sin(dg)
    p2 = impo.math.cos(l1) * impo.math.sin(l2) - impo.math.sin(l1) * p0
    p3 = impo.math.sin(l1) * impo.math.sin(l2) + impo.math.cos(l1) * p0
    return raadius*impo.math.atan2((p1**2+p2**2)**0.5,p3) #Tagastab vahemaa kilomeetrites
def nurk(asi1, asi2):   # Leia nurk kahe asimuudi vahel
    a=min([abs(asi2-asi1),abs(asi1-asi2)])%180 # Nt tuulesuund ja rajasuund
    return min(a,abs(a-180))
#Raja vastasasimuut: (x+180)%360
class ilm:
    def hetkeilm(): #Importditav versioon funktsiooniga
        global cache
        cl=list(cache)
        ilm=impo.urllib.request.urlopen('http://www.ilmateenistus.ee/ilma_andmed/xml/observations.php')
        ilm=ilm.read().decode('ISO-8859-1') # Valib õige kodeeringu /proovimise teel

        ilm2=impo.xmltodict.parse(ilm)
        ilm3 = impo.json.loads(impo.json.dumps(ilm2))
        i=0 #Koristamine, eemaldab puuduvad andmed ja jaamad, kus pole tuult
        # precipitations  on sademed
        while i<len(ilm3['observations']['station']):
            nimi=ilm3['observations']['station'][i]['name'] #Ruumi säästmine
            for e in list(ilm3['observations']['station'][i]):# Kui jaamal pole
                if ilm3['observations']['station'][i][e]==None:#mingit tüüpi infot,
                    ilm3['observations']['station'][i].pop(e) # kustutab välja
            if 'winddirection' not in list(ilm3['observations']['station'][i]):
                ilm3['observations']['station'].pop(i) # Tuul on tähtsaim, kustuta,
                                                    # kui tuult ei ole mõõdetud
                i-=1     #Pole mõtet küsida tuule suunda, kui tuult pole...
                continue #...veel vähem internetist asukohta (hüppa edasisest üle)
            if nimi not in cl: # Kui antud jaama pole vahemälus
                coor=loe_coord(nimi.lower()+', eesti') # Otsi googlest
                if type(coor)==list:    # Kui google ka ei tea, siis las ta õpib.
                    print(nimi, i,' '*(30-len(nimi)), coor[1])
                    impo.time.sleep(0.5)     # Liiga palju päringuid, oota
                    coor=loe_coord(nimi.lower()+', eesti') # Otsi uuesti
                ilm3['observations']['station'][i]['loc']=coor
            else:                       # Asukoht on varem salvestatud
                ilm3['observations']['station'][i]['loc']=cache[nimi]
            i+=1
        # 4. ilmamassiiv. Kui varem viitas jaamale jrknr listis, siis nüüd kohanimi
        ilm4=dict()
        for i in ilm3['observations']['station']: # Iga allesjäänud ilmajaamaga
            nim=i['name']
            t=i
            t.pop('name')
            try:
                t['loc']['lat']=round(t['loc']['lat'],4)
                t['loc']['lng']=round(t['loc']['lng'],4)
            except:
                pass
            ilm4[nim]=t
        if False: #Eemalda vanad vahemuutujad, et neid kogemata ei kasutataks
            del ilm, ilm2,ilm3, cache, cl, e,i,t,nim,nimi
        return ilm4

    def lahim_ilm(loc, ilm):
        jaam=(None,20000)
        for i in list(ilm):
            t=round(dist(loc,ilm[i]['loc']),1)
            if t<jaam[1]:
                jaam=(i, t)
        return ilm[jaam[0]], jaam
    def weatherAPI(lat,lng):
        dld=['vt1alerts', 'vt1currentdatetime', 'vt1dailyForecast', 'vt1hourlyForecast', 'vt1observation', 'vt1pollenforecast', 'vt1precipitation', 'vt1wwir']
        key='d522aa97197fd864d36b418f39ebb323'#'c1ea9f47f6a88b9acb43aba7faf389d4'
        adr=''.join(['http://api.weather.com/v2/turbo/',';'.join(dld),'?units=m&language=et-EE&geocode=', str(round(float(lat),2)),',',str(round(float(lng),2)),'&format=json&apiKey=',key])
        #print(adr)
        ilm=impo.urllib.request.urlopen(adr)
        ilm3 = impo.json.loads(impo.json.dumps(ilm.read().decode()))
        ilm2=ilm3.replace('\n\n','\n').replace('\n\n','\n').replace('   ',' ').replace('  ',' ').replace('null','None').replace('true','True').replace('false','False')
        ilm=eval(ilm2)
        return ilm
class gui: #Klass graafilise kasutajaliideste rühmitamiseks
    class setup(impo.tk.Tk):
        def __init__(self, *args, **kwargs):
            impo.tk.Tk.__init__(self, *args, **kwargs)
            self.kontr=[0,0,0]
            self.tm=False
            self.otsir=impo.ttk.Label(text='Punktide otsingu raadius')
            self.raad=impo.ttk.Entry(width=4)
            self.otsir.grid(row=0, column=0,sticky=impo.tk.W)
            self.raad.grid(row=0, column=2)
            self.raad.insert(0, "35")

            self.otsik=impo.ttk.Label(text='Esimese raadiuse kordaja')
            self.korda=impo.ttk.Entry(width=4)
            self.otsik.grid(row=1, column=0,sticky=impo.tk.W)
            self.korda.grid(row=1, column=2)
            self.korda.insert(0, "1.0")

            self.nurk=impo.tk.IntVar()
            self.nurkl=impo.ttk.Label(text='Nurkade liitmine (BETA)')
            self.nurkv=impo.ttk.Checkbutton(variable=self.nurk)
            self.nurkl.grid(row=2, column=0,sticky=impo.tk.W)
            self.nurkv.grid(row=2, column=2)

            self.dirl=impo.ttk.Label(text='Sisendandmete kaust')
            self.dirb=impo.ttk.Button(text='Ava...', command=self.kaust)
            self.dirl.grid(row=3, column=0,sticky=impo.tk.W)
            self.dirb.grid(row=3, column=2)
            self.ka=impo.ttk.Label(text='')

            self.savl=impo.ttk.Label(text='Väljundfaili nimi')
            self.savb=impo.ttk.Button(text='Vali...', command=self.kmlf)
            self.savl.grid(row=5, column=0,sticky=impo.tk.W)
            self.savb.grid(row=5, column=2)
            self.fa=impo.ttk.Label(text='')

            self.json=impo.tk.IntVar()
            self.jsl=impo.ttk.Label(text='JSON formaadis koopia')
            self.jsv=impo.ttk.Checkbutton(variable=self.json)
            self.jsl.grid(row=7, column=0)
            self.jsv.grid(row=7, column=2)

            self.tt=impo.tk.IntVar()
            impo.ttk.Label(text='Lihtsustatud rajad').grid(row=8, column=0, columnspan=3)
            impo.ttk.Label(text='Ära lihtsusta radu\n(Mittesoovitatav)').grid(row=9, column=0,sticky=impo.tk.W)
            self.l2=impo.ttk.Label(text='Kasuta olemas radu',state='disabled')
            self.l2.grid(row=10, column=0,sticky=impo.tk.W)
            impo.ttk.Label(text='Lihtsusta radu').grid(row=11, column=0,sticky=impo.tk.W)
            impo.ttk.Radiobutton(variable=self.tt, value=1, command=self.radi).grid(row=9, column=2)
            self.o2=impo.ttk.Radiobutton(variable=self.tt, value=2,state='disabled', command=self.radi)
            self.o2.grid(row=10, column=2)
            impo.ttk.Radiobutton(variable=self.tt, value=3, command=self.radi).grid(row=11, column=2)

            self.button = impo.ttk.Button(text="start", command=self.start, state='disabled')
            self.button.grid(row=12,column=0,columnspan=3)
            self.ret=0
        def radi(self):
            self.kontr[2]=1
            if 3==sum(self.kontr):
                self.button.config(state='normal')
            else:
                self.button.config(state='disabled')
        def kaust(self):
            self.dirr=impo.tk_filedialog.askdirectory(mustexist=True)
            self.kontr[0]=1
            if impo.os.path.exists(self.dirr+'\\tmp'):
                self.o2.config(state='normal')
                self.l2.config(state='normal')
                self.tm=True
            else:
                self.l2.config(state='disabled')
                self.o2.config(state='disabled')
                if self.tt.get()==2:
                    self.kontr[2]=0
                self.tm=False
                if not impo.os.path.exists(self.dirr):
                    self.kontr[0]=0
                print(self.dirr)
            self.ka.config(text=self.dirr)
            self.ka.grid(row=4, column=0, columnspan=3,sticky=impo.tk.W)
            if 3==sum(self.kontr):
                self.button.config(state='normal')
            else:
                self.button.config(state='disabled')
        def kmlf(self):
            self.ouf=impo.tk_filedialog.asksaveasfilename(defaultextension='.kml', filetypes = [('Keyhole Markup Language', '.kml'), ('Kõik failid', '*.*')])
            self.kontr[1]=1
            if self.ouf=='':
                self.kontr[1]=0
            
            t=self.ouf[:-4]
            if t[-4:]=='.kml':
                t=t[:-4]
            if t[-4]=='.':
                t=t[:-4]
            self.ouf=t
            print(self.ouf)
            self.fa.config(text=self.ouf+'.kml')
            self.fa.grid(row=6, column=0, columnspan=3,sticky=impo.tk.W)
            if 3==sum(self.kontr):
                self.button.config(state='normal')
            else:
                self.button.config(state='disabled')
        def start(self):
            self.ret=dict()
            self.err=[False]*2
            try:
                self.ret['r']=float(self.raad.get())
            except ValueError:
                self.err[0]=True
            try:
                self.ret['fp']=float(self.korda.get())
            except ValueError:
                self.err[1]=True
            self.ret['nurk']=bool(self.nurk.get())
            self.ret['sis']=self.dirr
            self.ret['val']=self.ouf
            self.ret['json']=bool(self.json.get())
            self.ret['tmp']=int(self.tt.get())
            self.ret['mkt']=not self.tm
            if sum(self.err)==0:
                self.destroy()
            else:
                o='Leiti järgmised vead:\n'
                if self.err[0]:
                    o+='Vale raadiuse formaat'
                if self.err[1]:
                    o+='\nVale raadiuse kordaja formaat'
                self.ret=0
                impo.tk.messagebox.showerror(str(sum(self.err))+' viga!',o)
        def read_bytes(self): #Kasuta seda kui allikat
            '''simulate reading 500 bytes; update progress bar'''
            self.bytes += 5
            self.progress["value"] = self.bytes
            if self.bytes < self.maxbytes:
                # read more bytes after 100 ms
                self.after(100, self.read_bytes)
            else:
                self.destroy()
    class info(impo.tk.Tk):
        def __init__(self, *args, **kwargs):
            impo.tk.Tk.__init__(self, *args, **kwargs)
            self.geometry("400x123")
            self.resizable(width=False, height=False)
            self.infotxt=[0]*3
            self.progress=[0]*3
            self.infotxt[0]  = impo.ttk.Label(self,text='t')
            self.infotxt[0].pack(fill='x')
            self.progress[0] = impo.ttk.Progressbar(self, orient="horizontal", mode="determinate", value=0, maximum=11)
            self.progress[0].pack(fill='x')
            self.infotxt[1]  = impo.ttk.Label(self,text='t')
            self.infotxt[1].pack(fill='x')
            self.progress[1] = impo.ttk.Progressbar(self, orient="horizontal", mode="determinate", value=15, maximum=76)
            self.progress[1].pack(fill='x')
            self.infotxt[2]  = impo.ttk.Label(self,text='t')
            self.infotxt[2].pack(fill='x')
            self.progress[2] = impo.ttk.Progressbar(self, orient="horizontal", mode="determinate", value=40, maximum=78)
            self.progress[2].pack(fill='x')
            self.title('Programm töötab')
            self.prog_val=[0]*3
            self.t_start=0
            self.tect=['']*3
        def infow(self,lvl=2, label='', bar=1):
            lvl-=1
            #global prog_val,tect,t_start
            if lvl!=0:
                if label=='':
                    self.prog_val[lvl]+=bar
                    self.progress[lvl].config(value=self.prog_val[lvl])
                    m=self.progress[lvl].cget('maximum')
                    if lvl==1:
                        t_cur=impo.time.time()
                        eta=round(self.t_start-t_cur+((t_cur-self.t_start)/self.prog_val[1]*m))
                        self.infotxt[lvl].config(text='{0} {1}/{2}  {3}s veel'.format(self.tect[1],self.prog_val[1],m,eta))
                    else:
                        self.infotxt[lvl].config(text='{0} {1}/{2}'.format(self.tect[lvl],self.prog_val[lvl],m))
                else:
                    if lvl==1:
                        self.t_start=impo.time.time()
                    self.prog_val[lvl]=0
                    self.progress[lvl].config(maximum=bar,value=0)
                    self.tect[lvl]=label
                    self.infotxt[lvl].config(text='{0} {1}/{2}'.format(self.tect[lvl],self.prog_val[lvl],self.progress[lvl].cget('maximum')))
            else:
                self.prog_val[lvl]+=1
                self.tect[lvl]=label
                self.progress[lvl].config(value=self.prog_val[lvl])
                self.infotxt[lvl].config(text='{0} {1}/{2}'.format(self.tect[lvl],self.prog_val[lvl],self.progress[lvl].cget('maximum')))
            
            self.update()
        def sulg(self):
            s=impo.ttk.Button(self,command=self.destroy, text='Sulge')
            s.pack()
            self.geometry("400x150")
            self.mainloop()
class funs:
    class punkt:
        def __init__(self,lo,la,idd,edge=set(),ele=0, wei=1, v=1):
                self.lng=lo
                self.lat=la
                self.uid=idd
                self.edges=edge
                self.att=ele
                self.weight=wei
                self.speed=v
        def out(self):
                edge2=set()
                selve={'lat':self.lat,'lng':self.lng}
                for i in self.edges:
                    ss=impo.math.degrees(funs.nurk_coor(punktid[self.uid],punktid[i]))
                    edge2.add((i,round(dist(selve,{'lat':punktid[i].lat,'lng':punktid[i].lng})*1000,2),
                            round(ss+0,1)%360))
                return {'"Latitude"':self.lat,
                        '"Longtitude"':self.lng,
                        '"Unique ID"':self.uid,
                        '"Neighbours"':edge2,
                        '"Elevation"':round(self.att,3),
                        '"Weight"':self.weight,
                        '"Speed"':self.speed}
    def merg(adr,out): #Import full tracks
        gpx_file = open(adr, 'r')
        try:
            gpx = impo.gpxpy.parse(gpx_file)
        except UnicodeDecodeError:
            return
        if len(gpx.tracks)==0:
            return
        gpx.tracks[0].description=' '#avoid errors with html description
        gpx.tracks[0].simplify()
        f=open(out,'w')
        f.write(gpx.to_xml())
        f.close()
    def merg2(adr,inf):
        global ui, punktid
        try:
            gpx_file = open(adr, 'r')
        except FileNotFoundError:
            return
        try:
            gpx = impo.gpxpy.parse(gpx_file) #Raises error and returns
        except impo.gpxpy.parser.mod_gpx.GPXXMLSyntaxException:
            return
        first=True
        if len(gpx.tracks)==0:
            return
        for segment in gpx.tracks[0].segments:
            ################################
            #  ERROR  ERROR  ERROR  ERROR  # Tegelikult viga enam ei ole
            ################################
            inf.infow(3,'Punkt',len(segment.points))
            ################################
            #  ERROR  ERROR  ERROR  ERROR  #
            ################################
            for point in segment.points:# Points are added continuosly,
                inf.infow(3)
                if first:               # each has edge to next and previous
                    punktid[ui]=funs.punkt(point.longitude,point.latitude,ui,{ui+1},point.elevation)
                    first=False         # Except for 1st...
                else:
                    punktid[ui]=funs.punkt(point.longitude,point.latitude,ui,{ui-1,ui+1},point.elevation)
                ui+=1
        punktid[ui-1].edges.remove(ui)  # ...and last, those have 1 edge.
    def nurk_coor(p1, p2):              # Leia asimuut 2 punkti vahel
        #http://www.igismap.com/formula-to-find-bearing-or-heading-angle-between-two-points-latitude-longitude/
        X=impo.math.cos(impo.math.radians(p2.lat))*impo.math.sin(impo.math.radians(p2.lng-p1.lng))# It's 'copipasta', I hope it works
        Y=impo.math.cos(impo.math.radians(p1.lat))*impo.math.sin(impo.math.radians(p2.lat))-impo.math.sin(impo.math.radians(p1.lat))*impo.math.cos(impo.math.radians(p2.lat))*impo.math.cos(impo.math.radians(p2.lng-p1.lng))
        return impo.math.atan2(X,Y)
    def nurk_3(p0,p1,p2):               # Find angle (p1,p0,p2)
        as1=impo.math.degrees(funs.nurk_coor(p0,p1))
        as2=impo.math.degrees(funs.nurk_coor(p0,p2))
        a=round(abs(as1-as2),1)        # (as1-as2) can be from -360 to 360 degrees
        if a>180:
            a=180-a%180                 # Shortest true angle is 0..180 deg
        return a
    def raadius(x,t): #For lambda. check if point is close to other
        global r #Searches from square 2rX2r m. Designed for N60 deg latitude
        return (x.lat<t.lat+0.0001*(r/5) and x.lat>t.lat-0.0001*(r/5) and 
               x.lng<t.lng+0.00005*(r/5) and x.lng>t.lng-0.00005*(r/5))
    def tabel(*args):#For debugging formats arguments to columns
        print('\t'.join(list(map(lambda x:str(x).strip(),args))))
    def printf(s, ex=''):
        if printer:
            print(ex, s)
    def bug():
        ln=impo.inspect.currentframe().f_back.f_lineno
        try:
            error_counter[ln]+=1
        except KeyError:
            error_counter[ln]=1
    def dist(a,b):
        return ((a.lat-b.lat)**2+(a.lng-b.lng)**2)**0.5
