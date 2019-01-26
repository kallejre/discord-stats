# Bot versioon 4. Eesmärk asjast aru saada.
# Ühildub nüüd ka python 3.7-ga. Discord.py versioon 1.0 (poolik).
import discord
from discord.ext import commands
import asyncio
import re
import funk
import random, time, pickle, os
from discord_class import Stats


# Helin = 392707534764376074
Helin = '<@392707534764376074>'
test='<@482189197671923713>'
ago='<@366546170149076993>'
BOT_PREFIX = ("?", "!")
TOKEN = 'NDg2NDQ1MTA5NjQ3MjQ1MzMy.DnELrQ.WDT1RXBmKt61KbX9MgtoDYGgt8A'
bot = commands.Bot(command_prefix=BOT_PREFIX,
                      description='Bot for tests')
# Link: https://discordapp.com/api/oauth2/authorize?client_id=486445109647245332&permissions=227328&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Fapi%2Foauth2%2Fauthorize&scope=bot
# ATVS: Võimalus teoreetiliselt botti konfida serveri liidesest. KATKI!
atvs=0
kell=''
def stats_load(fname='d_stats.pkl'):
    """PKL -> Self. Terve objekti avamine."""
    global kell
    statbuf = os.stat(fname)
    kell=time.localtime(statbuf.st_mtime)
    kell=time.strftime('%d.%m.%Y %H:%M',kell)
    print("Modification time: {}".format(kell))
    with open(fname, 'rb') as f:
        print(f)
        x = pickle.load(f)
    return x

data=stats_load()

def base36encode(number):
    """Converts an integer to a base36 string."""
    alphabet='0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    base36 = ''
    sign = ''
    if number < 0:
        sign = '-'
        number = -number
    if 0 <= number < 36:
        return sign + alphabet[number]
    while number != 0:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36
    return sign + base36

def atvs_init():
    global atvs
    pin=random.randint(60466176, 2176782330)
    atvs=base36encode(pin)
    print(atvs)

def atvsvc(accessToken):
    """Access Token Verification Service"""
    global atvs
    if accessToken.upper()==atvs:
        atvs_init()
        return True
    else:
        return False

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    atvs_init()
    print('------')

videod=['https://youtu.be/q-q8HUtCM4w',  # Kesköödisko
        'https://youtu.be/YEc19rkkMdg',  # Öö laps
        'https://youtu.be/6iVEH8TIfB4',  # Meeletu öö
        'https://youtu.be/YuBeBjqKSGQ',  # Öökuninganna aaria
        'https://youtu.be/jWFXiBzcDBg',  # Caater Feat. Trinity - The Queen Of Night
        'https://youtu.be/VL7MRMMbmug',  # Ei taha magama jääda
        'https://youtu.be/8DNQRtmIMxk',  # Saturday night
        'https://www.youtube.com/watch?v=dcnd55tLCv8',
        'https://www.youtube.com/watch?v=ADmCFmYLns4',
        'https://www.youtube.com/watch?v=uNSBq6hvU1s',
        'https://www.youtube.com/watch?v=VOrEdIxGPoA',   # Tahan olla öö
        'https://www.youtube.com/watch?v=egX9N8yOgaU',
        
        ]

def find_user(text):
    nimi=text
    if nimi[:2]=='<@':
        print(nimi[2:-1])
        uid=data.archive['meta']['userindex'].index(nimi[2:-1])
    elif nimi=='-1':
        uid=int(nimi)
    elif nimi.isdecimal():
        if len(nimi)>10:
            uid=data.archive['meta']['userindex'].index(nimi)
        else:
            uid=int(nimi)
    else:
        uid = list(filter(lambda x: nimi.lower() in data.users[x]['n'].lower(), data.users))[0]
    return uid
def find_channel(kanal):
    if kanal[:2]=='<#':
        xid=data.archive['meta']['channels'][kanal[2:-1]]
        return data.archive['meta']['channels'][xid]['name']
    else:
        return kanal
blacklist=[]

textid=[['Mine magama'],   # 0
 ['Mine magama'],   # 1
 ['Mine magama'],   # 2
 ['Mine magama'],   # 3
 ['Mine magama','Mine prae pelmeene!'],   # 4
 ['Mine magama'],   # 5
 ['Mine magama'],   # 6
 ['Ärka üles'],     # 7
 ['Ärka üles'],     # 8
 ['Ärka üles'],     # 9
 ['Ärka üles'],     # 10
 ['Ärka üles'],     # 11
 ['Ärka üles','Mine prae pelmeene!'],     # 12
 ['Head isu','Mine prae pelmeene!'],      # 13
 ['Head isu','Mine prae pelmeene!'],      # 14
 ['Head isu','Mine prae pelmeene!'],      # 15
 ['Ära istu arvuti taga, mine õue!','Mine prae pelmeene!'],   # 16
 ['Ära istu arvuti taga, mine õue!','Mine prae pelmeene!'],   # 17
 ['Ära istu arvuti taga, mine õue!'],   # 18
 ['Ära istu arvuti taga, mine õue!'],   # 19
 ['Ära istu arvuti taga, mine õue!'],   # 20
 ['Mine varsti magama!'],   # 21
 ['Mine varsti magama!'],   # 22
 ['Mine varsti magama!','Mine varsti pelmeene keetma!']]   # 23

@bot.event
async def on_message(message):
    channel = message.channel
    sisu=message.content
    #if str(message.channel) not in ['botnet', 'random']:
    #    return
    uid=-int(message.author.id )
    user=message.author.name
    if sisu.startswith('?math'):
        print('math by ',user)
        if user in blacklist:
            return await channel.send('blacklisted')
        a=' '.join(sisu.split()[1:])
        if a=='':
            await channel.send("ERROR: Tehe on puudu.")
            return
        result = re.sub('[^0-9^.^*^+^/^\-^(^)^ ^%]','', a)
        print(result)
        try:
            await channel.send("Understood as "+result)
            await channel.send("Result: "+str(eval(result)))
        except Exception as err:await channel.send(err)
        return
    if sisu.startswith('?ilm2'):  # {'lat': 59.43696079999999, 'lng': 24.7535747}
        print('ilm2 by ',user)
        x={'lat': 59.43696079999999, 'lng': 24.7535747}
        asd=funk.ilm.weatherAPI(x['lat'],x['lng'])
        msg='Kuupäev:\n'+asd['vt1dailyForecast']['validDate'][0].split('T')[0]+', '+asd['vt1dailyForecast']['dayOfWeek'][1]+':\n'
        msg+=asd['vt1dailyForecast']['day']['narrative'][1]+'\n'
        msg+=asd['vt1dailyForecast']['night']['dayPartName'][1]+':\n'
        msg+=asd['vt1dailyForecast']['night']['narrative'][1]
        await channel.send(msg)
        return
    if sisu.startswith('?ilm'):
        print('ilm by ',user)
        if user in blacklist:
            return await channel.send('blacklisted')
        a=' '.join(sisu.split()[1:])
        if a=='':
            await channel.send("ERROR: Asukoht on puudu.")
            return
        x2=funk.coord(a)
        if len(x2['results'])==0:
            await channel.send("ERROR: Asukohta ei leitud.")
            return
        x= x2['results'][0]['geometry']['location']
        stri="Asukoht: {0}\nLat: {1}, Lng: {2}".format(x2['results'][0]['formatted_address'],x['lat'],x['lng'])
        await channel.send(stri)
        asd=funk.ilm.weatherAPI(x['lat'],x['lng'])
        print(a)
        msg='Kuupäev: '+asd['vt1dailyForecast']['validDate'][0].split('T')[0]+', \n'+asd['vt1dailyForecast']['dayOfWeek'][1]+':\n'
        msg+=asd['vt1dailyForecast']['day']['narrative'][1]+'\n'
        msg+=asd['vt1dailyForecast']['night']['dayPartName'][1]+':\n'
        msg+=asd['vt1dailyForecast']['night']['narrative'][1]
        await channel.send(msg)
        return
    if sisu.startswith('?help'):
        print('help by ',user)
        embed = discord.Embed(title="Not a nice bot", description="A Very un-Nice bot. List of commands are:", color=0x41e510)

        # embed.add_field(name="?add X Y", value="Gives the addition of **X** and **Y**", inline=False)
        # embed.add_field(name="?multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
        embed.add_field(name="?math <tehe>", value="Resolves math problems", inline=False)
        embed.add_field(name="?ilm <asukoht>", value="Tagastab eestikeelse ilmateate homseks", inline=False)
        embed.add_field(name="?ilm2", value="Tagastab homse ilmateate tallinna kohta", inline=False)
        # embed.add_field(name="?cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
        embed.add_field(name="?spam", value="Mine magama", inline=False)
        embed.add_field(name="?wait", value="Spämmib rohkem", inline=False)
        embed.add_field(name="?stats", value="Ei tööta", inline=False)
        # embed.add_field(name="?loop", value="Args: key, time, funk, args (ainult ilm ja math)", inline=False)
        embed.add_field(name="?help", value="Gives this message", inline=False)

        await channel.send(embed=embed)
    if sisu.startswith('?wait'):
        print('wait by ',user)
        if user in blacklist:
            return await channel.send('blacklisted')
        try:
            x=' '.join(sisu.split()[2:])
            a=int(sisu.split()[1])
            if a>120:
                await channel.send('Vastu võetud '+str(x)+', esitamisel '+time.strftime('%d.%m %H:%M',time.localtime(time.time()+a)))
            await asyncio.sleep(a)
            # await channel.send('- '+str(x))
            await channel.send(''+str(x))
        except Exception as err:
            await channel.send(str(err))
    if sisu.startswith('?spam'):
        """
        juutuub = '://www.youtube.com/watch' in sisu or 'yt.be' in sisu
        if juutuub or 1:
            if message.author.mention in [Helin, ago] or 1:
                a=time.localtime()
                if a.tm_hour in range(6):#1,6):
                    # await channel.send(random.choice(videod))
                    await channel.send('Kell on '+str(a.tm_hour)+':'+str(a.tm_min)+', mine magama!')
        """
        print('spam by ',user)
        a=time.localtime()
        await channel.send('Kell on '+time.strftime('%H:%M',a)+', '+random.choice(textid[a.tm_hour]))
        
    
    if sisu.startswith('?stats'):
        print('stats by ',user)
        commands=sisu.split()[1:]
        print(commands)
        if len(commands)==0:
            await channel.send('No! Katkine asi. Proovi **stats help**')
            return
        if commands[0]=='help':
            await channel.send('No! Katkine asi. \n**Docs:**\n?stats edetabel <kasutajanimi> *<n>*\n'
                               '?stats ajatabel <kanal>')
        elif commands[0]=='edetabel':
            print(commands[1])
            if len(commands)<3:
                if len(commands)==1:
                    await channel.send('Viga, kasutajatunnus on puudu')
                    return
                if len(commands)==2:
                    num=5
            else:
                num=int(commands[2])
            nimi=commands[1]
            try:uid=find_user(nimi)
            except IndexError:
                await channel.send('Kasutajat ei leitud.')
                return
            print(nimi, uid)
            await channel.send('Statistika '+kell+' seisuga.')
            await channel.send(data.graafid_edetabel(uid,uid=True,n=num))
        elif commands[0]=='ajatabel':
            # ajatabel_vaiksem
            if len(commands)<3:
                await channel.send('Vaja on kasutajat ja kanalit')
                return
            try:uid=find_user(commands[1])
            except IndexError:
                await channel.send('Kasutajat ei leitud.')
                return
            kanal=find_channel(commands[2])
            await channel.send('Statistika '+kell+' seisuga.')
            try: await channel.send('```'+data.ajatabel_vaiksem(uid,kanal)+'```')
            except KeyError:
                await channel.send("""Tundmatu kanal. Vt alla.\n Ühendatud kanalid:\n`    Kokku`\n`    ├───EX`\n`    ├───PR`\n`    ├───Syva`\n`    │   ├───DJ`\n`    │   └───XP`\n`    └───Üldine`""")
        else:
            await channel.send('No! Katkine asi. Proovi **stats help**')
        #await channel.send('No! Katkine asi.')
    if sisu.lower().startswith('tere'):
        print('tere by ',user)
        if user.lower().startswith('tere'):return
        elif user.lower().startswith('kadri'):return await channel.send('<@'+str(abs(uid))+'>'+', **pelmeen!**')
        await channel.send('<@'+str(abs(uid))+'>'+', **tere!**')
@bot.event
async def on_command_error(ctx, error):
    print(str(error))
@bot.command()
async def info(ctx):
    embed = discord.Embed(title="nice bot", description="Nicest bot there is ever.", color=0xeee657)
    # give info about you here
    embed.add_field(name="Author", value="#3355")
    # Shows the number of servers the bot is member of.
    embed.add_field(name="Server count", value=f"{len(bot.guilds)}")
    # give users a link to invite thsi bot to their server
    embed.add_field(name="Invite", value="[Invite link](<insert your OAuth invitation link here>)")
    await ctx.send(embed=embed)

async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("\nCurrent servers:")
        for server in bot.guilds:
            print(server.name)
        await asyncio.sleep(600)#600
    await ctx.send(embed=embed)

bot.loop.create_task(list_servers())
bot.run(TOKEN)
