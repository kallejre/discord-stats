class impo:
    import math
    import urllib.request
    import json
    import xmltodict
    import time
    import urllib.parse
from ilmajaamad import cache as cache # Juhuks kui peaks tekkima lisa cache
error_counter=dict()
printer=False
# Üks vana koodijupp
# Allikat ei mäleta.
# Teeb Google mapsi koordinaadipäringu
def coord(address):
    params = {'address' : address, 'sensor' : 'false'}
    hmm='zaSyD7ffhr22Fo8AMiGc0KPYw0L_MrPFft'
    url = 'https://maps.googleapis.com/maps/api/elevation/json?key=AI'+hmm+'dMI&' + impo.urllib.parse.urlencode(params)
    response = impo.urllib.request.urlopen(url)
    result = impo.json.loads(response.read().decode(response.headers.get_content_charset()))
    return result
def elev(coors): # Kõrguspäringu prototüüp, pole kasutuses
    hmm='zaSyD7ffhr22Fo8AMiGc0KPYw0L_MrPFft'
    url = 'https://maps.googleapis.com/maps/api/elevation/json?key=AI'+hmm+'dMI&locations='
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
    def hetkeilm():
        """Ma ei tea mis siin toimub, aga tahaks kunagi kasutusele võtta."""
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
        vot='d522aa97197fd864d36b418f39ebb323'#'c1ea9f47f6a88b9acb43aba7faf389d4'
        adr=''.join(['http://api.weather.com/v2/turbo/',';'.join(dld),'?units=m&language=et-EE&geocode=', str(round(float(lat),2)),',',str(round(float(lng),2)),'&format=json&apiKey=',vot])
        ilm=impo.urllib.request.urlopen(adr)
        ilm3 = impo.json.loads(impo.json.dumps(ilm.read().decode()))
        ilm2=ilm3.replace('\n\n','\n').replace('\n\n','\n').replace('   ',' ').replace('  ',' ').replace('null','None').replace('true','True').replace('false','False')
        ilm=eval(ilm2)
        return ilm


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
            return {'"Latitude"':self.lat, '"Longtitude"':self.lng,
                    '"Unique ID"':self.uid, '"Neighbours"':edge2,
            '"Elevation"':round(self.att,3), '"Weight"':self.weight, '"Speed"':self.speed}

    def dist(a,b):
        return ((a.lat-b.lat)**2+(a.lng-b.lng)**2)**0.5
