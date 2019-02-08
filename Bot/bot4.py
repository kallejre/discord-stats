# coding: utf-8
# Bot versioon 4. Eesmärk midagi kasulikku teha.
# Ühildub nüüd ka python 3.7-ga. Discord.py versioon 1.0 (poolik).
import asyncio
import os
import pickle
import random
import re
import time
import urllib.request
from sys import exit
import funk
from discord.ext import commands
import discord
from bot_funk import *
"""
Asjad, mida muuta:
    Wait võiks salvestada asjad vahemällu, et uuel käivitamisel asjad töötaksid (+tugi kellaajale?).
    Customspam võtab nime ära.
    Statistika andmete laadimine.
    Integreerid statistika ja boti koodid.
"""

VERSION='4.0.2.0'
helin = '<@392707534764376074>'
test = '<@482189197671923713>'
ago = '<@366546170149076993>'
BOT_PREFIX = ("?", "!")
võti = 'NDg2NDQ1MTA5NjQ3MjQ1MzMy.DnEL'
rõngas = 'rQ.WDT1RXBmKt61KbX9MgtoDYGgt8A'
bot = commands.Bot(command_prefix=BOT_PREFIX,
                   description='Bot for tests')
# Docs: https://discordpy.readthedocs.io/en/rewrite/
# Link: https://discordapp.com/api/oauth2/authorize?client_id=486445109647245332&permissions=227328&redirect_uri=https%3A%2F%2Fdiscordapp.com%2Fapi%2Foauth2%2Fauthorize&scope=bot
kell = ''

def stats_load(fname='d_stats.pkl'):
    """PKL -> Self. Terve objekti avamine."""
    global kell
    statbuf = os.stat(fname)
    
    temp = time.strftime('%d.%m.%Y %H:%M', time.localtime(statbuf.st_mtime))
    if kell==temp:
        return False
    kell = temp
    print("Modification time: {}".format(kell))
    with open(fname, 'rb') as f:
        print(f)
        x = pickle.load(f)
    return x

from Disco_Stats import Stats
data = stats_load()

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
def gg(sisu):
    sisu='?guugle tallinna linn'
    splt = sisu.split()[1:]
    # try:
    asd = 0
    """if len(splt) >= 2:
        if splt[-1].isdigit():
            asd = int(splt.pop(-1))"""
    ms = ' '.join(splt)
    regex = re.compile('<div class="g">')
    adr = urllib.request.quote(ms)
    adr = 'https://www.startpage.com/do/search?q=' + adr
    print(adr)
    user_agent = ''#'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
    headers={'User-Agent':user_agent,}

    req=urllib.request.Request(adr,None,headers)
    # req = urllib.request.Request(adr)
    response = urllib.request.urlopen(req)
    the_page = response.read().decode('utf8').split('<ol class="list-flat">')[1].split('</ol>')[0]
    the_page = re.sub('<a[\s\S]*?>', '<a>', the_page).replace('<li><a>Anonymous View</a></li>','').split('</li>')
    print(len(the_page))
    #matches = regex.split(the_page)
    #zz=matches.pop(0)
    #del zz
    for m in range(len(the_page)):
        text=the_page[m]
        try:
            text = text.replace('<br>', '\n')
        except Exception:pass
        the_page[m] = re.sub('<[\s\S]*?>', ' ', text)
    if 1:
        for m in the_page[:3]:
            print(len(m))
            m=m.replace('&lt;','<').replace('&nbsp;',' ').replace('&gt;','>')
            hd,li=m.strip().split('  \n \n ')
            link,desc=li.split(' \n \n\n \n \n ')
            print(hd,': ',desc,' - ',link)
    # defin = re.split('\. [A-Z\d]', text2)[0] + '.'
    # print(defin)
    # except Exception as err:
    # print(err)


@bot.command(name='bitcoin',
                description="Uses Coindesk API to get BitCoin price in USD.",
                brief="Returns BTC/USD.",
                pass_context=True)
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await bot.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

async def troll_task():
    while not bot.is_closed:
        tt=10
        try:
            await bot.change_presence(game=Game(name="with humanoids"))
            await asyncio.sleep(tt)
            await bot.change_presence(game=Game(name="with animals"))
            await asyncio.sleep(tt)
        except websockets.exceptions.ConnectionClosed:
            return

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)
async def square(number):
    squared_value = int(number) * int(number)
    await bot.say(str(number) + " squared is " + str(squared_value))

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@bot.command()
async def divide(ctx, a: float, b: float):
    await ctx.send(a/b)

@bot.command()
async def hi(ctx):
    t=ctx.author
    his=ctx.history(limit=5)
    out=''
    async for msg in his:
        out+=''.join([msg.author.name,': ',msg.content])+'\n'
        # print(dir(msg))
    out=out.replace('@','(ät)')
    print(out)
    print(t.name, t.id)
    await ctx.send(out)
    await ctx.send('I heard you! {1}, {0}'.format(t.mention,t.name))
    # await ctx.send('I heard you! {0} <@{1}>'.format(*str(ctx.author).split('#')))
          
def find_user(text):
    nimi = text
    if nimi[:2] == '<@':
        print(nimi[2:-1])
        uid = data.archive['meta']['userindex'].index(nimi[2:-1])
    elif nimi == '-1':
        uid = int(nimi)
    elif nimi.isdecimal():
        if len(nimi) > 10:
            uid = data.archive['meta']['userindex'].index(nimi)
        else:
            uid = int(nimi)
    else:
        uid = list(filter(lambda x: nimi.lower() in data.users[x]['n'].lower(), data.users))[0]
    return uid


def find_channel(kanal):
    if kanal[:2] == '<#':
        xid = data.archive['meta']['channels'][kanal[2:-1]]
        return data.archive['meta']['channels'][xid]['name']
    else:
        return kanal


def ilma_output(data, location):
    # Kõigepealt millist infot koguda?
    # id - koordinaadid
    # Hetkeilm: (vt1observation)
    #   Õhuniiskus
    #   Temperatuur
    #   Näiv temp.
    #   Tuule suund, kiirus (kmh)
    #   phrase
    #   Sademed
    # Ilmateade:
    #   data
    #   icon: Url: http://l.yimg.com/a/i/us/we/52/XX.gif
    #   rh - suhteline õhuniiskus
    #   Temperatuur
    #   Näiv temp.
    # vt1alerts - hoiatused
    #   headline

    embed = discord.Embed(title=data['vt1observation']['phrase'], description=location, color=0x2a85ed,
                          type='rich')
    embed.set_thumbnail(url='http://l.yimg.com/a/i/us/we/52/' + str(data['vt1observation']['icon']) + '.gif')
    embed.add_field(name='Temperatuur ' + str(data['vt1observation']['temperature']) + 'C',
                    value='Näiv temperatuur ' + str(data['vt1observation']['feelsLike']) + 'C', inline=False)
    embed.add_field(name='Tuule suund ' + str(data['vt1observation']['windDirCompass']) + '',
                    value='Tuule kiirus ' + str(round(data['vt1observation']['windSpeed'] / 3.6, 1)) + 'm/s',
                    inline=False)
    embed.add_field(name='Õhuniiskus ' + str(data['vt1observation']['humidity']) + '%',
                    value='Kastepunkt ' + str(data['vt1observation']['dewPoint']) + 'C', inline=False)
    
    embed.add_field(name=data['vt1dailyForecast']['dayOfWeek'][1], value=data['vt1dailyForecast']['day']['narrative'][1])
    embed.add_field(name=data['vt1dailyForecast']['night']['dayPartName'][1], value=data['vt1dailyForecast']['night']['narrative'][1])
    
    achtung = []
    if data['vt1alerts']:
        for i in range(len(data['vt1alerts']['headline'])):
            achtung.append(data['vt1alerts']['areaName'][i]+' - '+data['vt1alerts']['headline'][i])
        achtung='\n'.join(achtung)
    else: achtung='Puuduvad'
    embed.add_field(name='Hoiatused:', value=achtung, inline=False)
    
    return embed



@bot.event
async def on_message(message):
    channel = message.channel
    sisu = message.content
    # if str(message.channel) not in ['botnet', 'random']:
    #    return
    uid = int(message.author.id)
    user = message.author.name
    if len(sisu) > 2 and sisu[0] == '?':
        print(str(message.created_at)[:-10], sisu, user, sep='\t')
    if user.lower().startswith('kadri'): await message.add_reaction(u"\U0001F916")
    if sisu.startswith('?math'):
        if user in blacklist:
            return await channel.send('blacklisted')
        a = ' '.join(sisu.split()[1:])
        if a == '':
            await channel.send("ERROR: Tehe on puudu.")
            return
        result = re.sub('[^0-9^.^*^+^/^\-^(^)^ ^%]', '', a)
        print(result)
        try:
            await channel.send("Understood as " + result)
            await channel.send("Result: " + str(eval(result)))
        except Exception as err:
            await channel.send(err)
        return
    elif sisu.startswith('?ilm'):
        if user in blacklist:
            return await channel.send('blacklisted')
        a = ' '.join(sisu.split()[1:])
        if a == '':
            x = {'lat': 59.43696079999999, 'lng': 24.7535747}
            loc='Tallinn'
        else:
            x2 = funk.coord(a)
            if len(x2['results']) == 0:
                await channel.send("ERROR: Asukohta ei leitud.")
                return
            x = x2['results'][0]['geometry']['location']
            loc=x2['results'][0]['formatted_address']
        asd = funk.ilm.weatherAPI(x['lat'], x['lng'])
        msg = ilma_output(asd, loc)
        await channel.send(embed=msg)
        return
    elif sisu.startswith('?help'):
        embed = discord.Embed(title="Not a nice bot", description="A Very un-Nice bot. List of commands are:",
                              color=0x41e510)

        # embed.add_field(name="?add X Y", value="Gives the addition of **X** and **Y**", inline=False)
        # embed.add_field(name="?multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
        embed.add_field(name="?math <tehe>", value="Resolves math problems", inline=False)
        embed.add_field(name="?ilm [asukoht]", value="Tagastab eestikeelse ilmateate. Vaikeasukoht Tallinn.", inline=False)
        # embed.add_field(name="?cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
        embed.add_field(name="?spam", value="Mine magama", inline=False)
        embed.add_field(name="?wait", value="Spämmib rohkem", inline=False)
        embed.add_field(name="?stats", value="Statistika", inline=False)
        embed.add_field(name="?define", value="Ei guugelda, vaid ÕS-ib", inline=False)
        embed.add_field(name="?pelmeen", value="Söö pelmeene", inline=False)
        # embed.add_field(name="?loop", value="Args: key, time, funk, args (ainult ilm ja math)", inline=False)
        embed.add_field(name="?help", value="Gives this message", inline=False)
        embed.add_field(name="tere", value="Teeb tuju heaks :)", inline=False)

        await channel.send(embed=embed)
    elif sisu.startswith('?pelmeen'):
        return await channel.send('https://nami-nami.ee/retsept/2442/pelmeenid_lihaga')
    elif sisu.startswith('?wait'):
        if user in blacklist:
            return await channel.send('blacklisted')
        try:
            x = ' '.join(sisu.split()[2:])
            a = int(sisu.split()[1])
            if a > 120:
                await channel.send('Vastu võetud ' + str(x) + ', esitamisel ' + time.strftime('%d.%m %H:%M',
                                                                                              time.localtime(
                                                                                                  time.time() + a)))
            await asyncio.sleep(a)
            # await channel.send('- '+str(x))
            await channel.send('' + str(x))
        except Exception as err:
            await channel.send(str(err))
    elif sisu.startswith('?customspam'):
        # bot.get_channel(537315188039221301)
        if user in blacklist:
            return await channel.send('blacklisted')
        try:
            x = ' '.join(sisu.split()[2:])
            a = int(sisu.split()[1])
            kanal2 = channel
            print(x)
            print(sisu.split()[2])
            if sisu.split()[2].startswith('<#') and sisu.split()[2].endswith('>'):
                idd = int(sisu.split()[2][2:-1])
                kanal2 = bot.get_channel(idd)
                x = ' '.join(sisu.split()[3:])
            if a > 120:
                await channel.send('Vastu võetud ' + str(x) + ', esitamisel ' + time.strftime('%d.%m %H:%M',
                                                                                              time.localtime(
                                                                                                  time.time() + a)))
            await asyncio.sleep(a)
            # await channel.send('- '+str(x))
            iad = '<@' + str(abs(uid)) + '> '
            # iad=''
            await kanal2.send(iad + str(x))
        except Exception as err:
            await channel.send(str(err))
    elif sisu.startswith('?spam'):
        """
        juutuub = '://www.youtube.com/watch' in sisu or 'yt.be' in sisu
        if juutuub or 1:
            if message.author.mention in [Helin, ago] or 1:
                a=time.localtime()
                if a.tm_hour in range(6):#1,6):
                    # await channel.send(random.choice(videod))
                    await channel.send('Kell on '+str(a.tm_hour)+':'+str(a.tm_min)+', mine magama!')
        """
        a = time.localtime()
        await channel.send('Kell on ' + time.strftime('%H:%M', a) + ', ' + random.choice(textid[a.tm_hour]))

    elif sisu.startswith('?stats'):
        commands = sisu.split()[1:]
        print(commands)
        if len(commands) == 0:
            await channel.send('No! Katkine asi. Proovi **stats help**')
            return
        if commands[0] == 'help':
            await channel.send('No! Katkine asi. \n**Docs:**\n?stats edetabel <kasutajanimi> *<n>*\n'
                               '?stats ajatabel <kanal>')
        elif commands[0] == 'edetabel':
            print(commands[1])
            if len(commands) < 3:
                if len(commands) == 1:
                    await channel.send('Viga, kasutajatunnus on puudu')
                    return
                if len(commands) == 2:
                    num = 5
            else:
                num = int(commands[2])
            nimi = commands[1]
            try:
                uid = find_user(nimi)
            except IndexError:
                await channel.send('Kasutajat ei leitud.')
                return
            print(nimi, uid)
            await channel.send('Statistika ' + kell + ' seisuga.')
            await channel.send(data.graafid_edetabel(uid, uid=True, n=num))
        elif commands[0] == 'ajatabel':
            # ajatabel_vaiksem
            if len(commands) < 3:
                await channel.send('Vaja on kasutajat ja kanalit')
                return
            try:
                uid = find_user(commands[1])
            except IndexError:
                await channel.send('Kasutajat ei leitud.')
                return
            kanal = find_channel(commands[2])
            await channel.send('Statistika ' + kell + ' seisuga.')
            try:
                await channel.send('```' + data.ajatabel_vaiksem(uid, kanal) + '```')
            except KeyError:
                await channel.send(
                    """Tundmatu kanal. Vt alla.\n Ühendatud kanalid:\n`    Kokku`\n`    ├───EX`\n`    ├───PR`\n`    ├───Syva`\n`    │   ├───DJ`\n`    │   └───XP`\n`    └───Üldine`""")
        else:
            await channel.send('No! Katkine asi. Proovi **stats help**')
        # await channel.send('No! Katkine asi.')
    elif sisu.startswith('?define'):
        splt = sisu.split()[1:]
        try:
            asd = 0
            if len(splt) >= 2:
                if splt[-1].isdigit():
                    asd = int(splt.pop(-1))
            ms = ' '.join(splt)
            regex = r"<div class=\"tervikart\">[.\s\S\d\D]*?<\/div>"
            adr = urllib.request.quote(ms)
            adr = 'https://www.eki.ee/dict/ekss/index.cgi?Q=' + adr
            req = urllib.request.Request(adr)
            response = urllib.request.urlopen(req)
            the_page = response.read().decode('utf8')
            matches = re.finditer(regex, the_page, re.MULTILINE)

            for matchNum, match in enumerate(matches, start=1):
                text = match.group()
                break
            try:
                text = text.replace('<br>', '\n')
            except Exception:
                await channel.send('Tulemusi ei leitud.')
                return
            text2 = re.sub('<[\s\S]*?>', '', text)
            if asd:
                if len(text2) < 1300:
                    return await channel.send(text2)
                else:
                    return await channel.send('Liiga pikk vastus\n' + text2[:1300])
            defin = re.split('\. [A-Z\d]', text2)[0] + '.'
            await channel.send(defin)
            return
        except Exception as err:
            await channel.send(err)
            return
    elif sisu.startswith('shutdown'):
        print(uid, type(uid))
        if int(uid) == 482189197671923713:
            await channel.send('shutdown...')
            exit()
            return
        else:
            await channel.send('no')
    elif sisu.lower().startswith('tere'):
        print(str(message.created_at)[:-10], sisu, user, sep='\t')
        if user.lower().startswith('tere'):
            return
        elif user.lower().startswith('kadri'):
            return await channel.send('<@' + str(abs(uid)) + '>' + ', **pelmeen!**')
        await channel.send('<@' + str(abs(uid)) + '>' + ', **tere!**')


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
    global data
    while not bot.is_closed():
        print("\nCurrent servers: ", end='')
        for server in bot.guilds:
            print(server.name, end=', ')
        print()
        data=stats_load()
        await asyncio.sleep(600)  # 600
    await ctx.send(embed=embed)

"""
@bot.command()
async def help(ctx):
    embed = discord.Embed(title="nice bot", description="A Very Nice bot. List of commands are:", color=0xeee657)

    embed.add_field(name="$add X Y", value="Gives the addition of **X** and **Y**", inline=False)
    embed.add_field(name="$multiply X Y", value="Gives the multiplication of **X** and **Y**", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    embed.add_field(name="$math", value="Resolves maath problems", inline=False)
    embed.add_field(name="$ilm", value="Tagastab estikeelse ilmateate homseks", inline=False)
    embed.add_field(name="$cat", value="Gives a cute cat gif to lighten up the mood.", inline=False)
    embed.add_field(name="$info", value="Gives a little info about the bot", inline=False)
    embed.add_field(name="$loop", value="Args: key, time, funk, args (ainult ilm ja math)", inline=False)
    embed.add_field(name="$help", value="Gives this message", inline=False)
    await ctx.send(embed=embed)
    """
bot.loop.create_task(list_servers())
# client.loop.create_task(list_servers())
# client.loop.create_task(troll_task())
bot.run(võti + rõngas)
