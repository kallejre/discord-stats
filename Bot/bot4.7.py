# -*- coding: utf-8 -*-
# Bot versioon 4.7.3 otsingutulemused läksid vahepeal katki. 
import asyncio
import os
import pickle, json
import random
import re
import time, datetime#, pytz
import urllib.request
from sys import exit
import funk
import html
from discord.ext import commands
import discord
from bot_funk import *  # Hunnik konstante
from Disco_Stats import Stats  # Spetsiaalne moodul statistika kuvamiseks. Natuke erinev originaalist.
from hangman import hangman
import titato, titato2

"""
Asjad, mida muuta:
    TEHTUD - Wait võiks salvestada asjad vahemällu, et uuel käivitamisel asjad töötaksid.
"""

VERSION = '4.7.3'
bot = commands.Bot(command_prefix=BOT_PREFIX, description='Bot for tests')
# Docs: https://discordpy.readthedocs.io/en/rewrite/
kell = ''
kellad = dict()
games = []
print('Run')


def stats_load2(srv='py2018'):  # Serveri nimi
    """PKL -> Self. Terve objekti avamine."""
    global videod, textid, blacklist
    global kellad
    kell = kellad[srv]
    fname = '../' + srv + '/d_stats.pkl'
    try:
        temp = time.strftime('%d.%m.%Y %H:%M', time.localtime(os.stat(fname).st_mtime))
    except FileNotFoundError:
        return (False, '')
    if kell == temp:
        return (False, '')
    kellad[srv] = temp
    print("Modification time: {}, filename: ".format(temp) + fname)
    with open(fname, 'rb') as f:
        x = pickle.load(f)
    return (True, x)


# data = stats_load()[1]
data = dict()
last_reac = dict()


@bot.event
async def on_ready():
    print('--- Logged in as  ' + bot.user.name + ' --- User ID ' + str(bot.user.id) + ' ---')


def gg(sisu):
    # internetiotsing
    splt = sisu.split()[1:]
    ms = ' '.join(splt)
    regex = re.compile('<div class="g">')
    adr = urllib.request.quote(ms)
    adr = 'https://www.startpage.com/do/search?q=' + adr
    req = urllib.request.Request(adr, None, {'User-Agent': ''})
    response = urllib.request.urlopen(req)
    htm = response.read().decode('utf8')
    try:
        the_page = htm.split('<section class="w-gl w-gl--default">')[1].split('</section>')[0]
    except IndexError:
        return [
            'You did it! [Tulemusi ei leitud.]\nhttps://i.pinimg.com/originals/a0/95/8a/a0958af58be0330979c242038b62e2f1.jpg']
    the_page = re.sub('<a[\s\S]*?>', '<a>', the_page).replace('<a>Anonymous View</a>', '').replace('Web Results', '').split('</div>')
    for m in range(len(the_page)):
        the_page[m] = re.sub('<[\s\S]*?>', ' ', the_page[m].replace('<br>', '\n')).replace('  ', ' ')

    tulem = []
    for m in the_page[:3]:
        m = html.unescape(m).strip()
        m=re.sub('((^\s+)|(\s\n))\s+', '\n',m)
        #tulem.append(m)
        #continue # ((^\s+)|(\s\n))\s+
        out=m.split('\n')
        # print(out)
        if len(out)==2:
            hd,link= out
            desc = '[Kirjeldus puudub]'
        else:
            hd,link,desc= out
        #hd, link = m.split(' \n                 \n                 ')
        #t = li.split(' \n                \n                \n\n                  ')
        if link[:4] != 'http': link = 'http://' + link
        tulem.append([hd, desc, '<' + link + '>'])
    return tulem


def gg_img(sisu):
    # interneti pildiotsing
    splt = sisu.split()[1:]
    ms = ' '.join(splt)
    regex = re.compile('<div class="g">')
    adr = urllib.request.quote(ms)
    adr = 'https://www.startpage.com/do/search?cat=pics&q=' + adr
    req = urllib.request.Request(adr, None, {'User-Agent': ''})
    response = urllib.request.urlopen(req)
    htm = response.read().decode('utf8')
    try:
        the_page = htm.split('<section class="ig-gl__main">')[1].split('</section>')[0]
    except IndexError:
        return [
            'You did it! [Tulemusi ei leitud.]\nhttps://i.pinimg.com/originals/a0/95/8a/a0958af58be0330979c242038b62e2f1.jpg']
    the_page = re.sub('<a[\s\S]*?>', '<a>', the_page).replace('<li><a>Anonymous View</a></li>', '')
    #return the_page
    # '\"clickUrl\": \"[\s\S]*?\"'
    matches = re.finditer(r"\"clickUrl\": \"[\s\S]*?\"", the_page, re.MULTILINE)
    the_page=[]
    for match in matches:
        match2 = match.group()[13:-1]
        mat4=bytes(match2, 'ascii').decode('unicode-escape')
        mat3=urllib.request.unquote(mat4)
        the_page.append(mat3)
    m=min([10, len(the_page)])-1
    the_page = the_page[:m + 1]
    return the_page


bot.remove_command("help")


@bot.command(pass_context=True)
async def help(ctx, *args):
    embed = discord.Embed(title="Botten von Bot", description="Enamiku saadaval käskude nimekiri:", color=0x41e510)
    embed.add_field(name="?define <märksõnad>", value="Ei guugelda, vaid ÕS-ib.", inline=False)
    embed.add_field(name="?help", value="Käskude nimekirja kuvamine.", inline=False)
    embed.add_field(name="?ilm [asukoht]",
                    value="""Tagastab eestikeelse ilmateate. Vaikeasukoht Tallinn.
                    Lisavõimalustena saab valida:
                    **?miniilm** (lühike ilmateade)
                    **?ilm_raw** (põhjalik info JSONina)
                    **?ilm_tabel** (vahepealne ilmateade järgneva 48h või 14 päeva kohta)
                    """,
                    inline=False)
    embed.add_field(name="?invite", value="Link boti lisamiseks.", inline=False)
    embed.add_field(name="?math <tehe>", value="Kalkulaator", inline=False)
    embed.add_field(name="?pelmeen", value="Toitvad soovitused.", inline=False)
    embed.add_field(name="?hi", value="Eksperimentaal. Kuvab viimased 5 sõnumit.", inline=False)
    embed.add_field(name="?search <märksõnad>", value="~~Guugeldab~~ StartPage'ib.", inline=False)
    embed.add_field(name="?search_img <märksõnad>",
                    value="Pildiotsing. Tagastab juhusliku pildi esimese kümne tulemuse hulgast.", inline=False)
    embed.add_field(name="?search2 <märksõnad>", value="Sama mis ?search, aga lisab ka esimese pilditulemuse. **Aeglane**.", inline=False)
    embed.add_field(name="?spam", value="Saadab rämpsu.", inline=False)
    embed.add_field(name="?stats [help]", value="Statistika. Lisakäsud on help, edetabel, ajatabel ja top.",
                    inline=False)
    embed.add_field(name="?wait  <aeg> [kanal] <sõnum>",
                    value="Ajastatud toimingute defineerimine.\nAega saab anda sekundites (?wait 10) ja kellaajana (?wait 30.01.19_13:14).",
                    inline=False)
    embed.add_field(name="?g  [new|end|list|<ID>]",
                    value="Hetkel ainult hangman. Lisainfo käsuga `?g help`",
                    inline=False)
    embed.add_field(name="?ping", value="Viisakas viis ühenduse kontrollimiseks.", inline=False)
    embed.add_field(name="?cleanup [sõnumite hulk 1..999]", value="Kustutab kõik boti sõnumid.", inline=False)
    embed.add_field(name="?cleanup2 [sõnumite hulk 2..999]",
                    value="Vaatab läbi viimased sõnumid ja kustutab mänguga seotu.", inline=False)
    embed.add_field(name="?reset", value="Taaskäivitus. ?shutdown enam ei tööta.", inline=False)
    embed.add_field(name="tere", value="Viisakas robot teeb tuju heaks :smiley:", inline=False)
    return await ctx.send(embed=embed)


async def troll_task():
    await bot.wait_until_ready()
    while not bot.is_closed():
        tt = 15
        # Botile ei ole mõtet lisada algus- ja lõpuaega, sest API ei toeta neid bottidel.
        # """
        timestmp = time.strftime('%d %b %H:%M', time.localtime(time.time()))
        # gg = discord.Activity(name='Music', url='aa.eu', application_id=377160)
        gg2 = discord.Game(timestmp)
        # us=bot.get_user(482189197671923713)  # Teise kasutaja staatust ei saa muuta.
        await bot.change_presence(activity=gg2)
        await asyncio.sleep(tt)
        """
        try:
            await bot.change_presence(activity=discord.Game(name="with humanoids"))
            await asyncio.sleep(tt)
            await bot.change_presence(activity=discord.Game(name="with animals"))
            await asyncio.sleep(tt)
        except websockets.exceptions.ConnectionClosed:
            return
        #"""


def alll(ctx): return True


@bot.command(pass_context=True)
async def g(ctx, *args):
    # await ctx.message.delete()
    if args[0] == 'new':
        if 0 in games:
            idd = games.index(0)
        else:
            idd = len(games)
            games.append(0)
        ty = args[1]
        if ty == 'hangman':
            dif = None
            if len(args) > 2:
                if args[2].isnumeric():
                    if 1 <= int(args[2]) <= 5:
                        dif = int(args[2])
            game = hangman(dif)
            games[idd] = game
            await ctx.send('Mängu ID on ' + str(idd + 1) + '\n' + game.startup)
        elif ty == 'ttt':
            # `?game ttt [väljaku suurus] <võidurea pikkus> oselejad...` (tühikutega eraldatud)'
            # print(args)
            try:
                game = titato.game_warp(args)
            except SyntaxError as err:
                game = str(err)
            if type(game) == str:
                # Tagastati veateade
                await ctx.send('Viga, ' + game)
                return
            games[idd] = game
            await ctx.send('Mängu ID on ' + str(idd + 1) + '\n' + game.startup)
        elif ty == 'tt2':
            # `?game tt2 [väljaku suurus] <võidurea pikkus>`
            # print(args)
            try:
                game = titato2.game_warp(args)
            except SyntaxError as err:
                game = str(err)
            if type(game) == str:
                # Tagastati veateade
                await ctx.send('Viga, ' + game)
                return
            games[idd] = game
            await ctx.send('Mängu ID on ' + str(idd + 1) + '\n' + game.startup)
        else:
            await ctx.send('Hetkel on toetatud ainult hangman ja trips-traps-trull (ttt või tt2).')
        return
    elif args[0] == 'help':
        embed = discord.Embed(title='Funktsiooni ?g abi.'.join(args), color=0x443eef, type='rich')
        embed.add_field(name="?g new [Mängu nimi] [Seaded]",
                        value="Alustab uue mänguga ja tagastab mängu ID. Hetkel on olemas vaid hangman (sõnade arvamine) ja ttt (tripstrapstrull)." \
                              "Formaadid:\nHangman: `?g new hangman <raskusaste 1-5>` (viimane on vabatahtlik)\n" \
                              "TTT: `?g new ttt [väljaku suurus] <võidurea pikkus> [Mängijate nimekiri...]` Mängijad eraldatud tühikutega, **kasutada @-märgendeid**!\n" \
                              "Teistmoodi TTT: `?g new tt2 [väljaku suurus] <võidurea pikkus>` Fikseerimata mängijateta. Käikude järjekord ja mängijate arv võib muutuda.",
                        inline=False)
        embed.add_field(name="?g end [Mängu ID]", value="Lõpetab ID põhjal käimasoleva mängu.", inline=False)
        embed.add_field(name="?g list", value="Käimasolevate mängude ja seisude info.", inline=False)
        embed.add_field(name="?g [Mängu ID] <Käik/käsud>",
                        value="Edastab vastava IDga mängule käigu.\nSelleks, et edastada tühikuga käsku, kasuta jutumärke. " \
                              "Formaadid:\nHangman: `?g [ID] [täht]`\nTTT: `?g [ID] [X (1..n)] [Y (1..n)]`",
                        inline=False)
        embed.add_field(name="?cleanup [sõnumite hulk 1..999]",
                        value="Vaatab läbi viimased sõnumid ja kustutab mänguga seotu.", inline=False)
        await ctx.send(embed=embed)
        return
    elif args[0] == 'end':
        t = args[1]
        if not t.isnumeric():
            await ctx.send('ID ei ole nuber.')
            return
        t = int(t) - 1
        if t not in range(len(games)) or games[t] == 0:
            await ctx.send('ID ei ole kehtiv.')
            return
        games[t] = 0

        # input()
        await ctx.send('Mängu ID ' + args[1] + ' on lõpetatud.')
        return await ctx.channel.send('?cleanup')
    elif args[0] == 'list':
        c = 0
        for i in range(len(games)):
            if games[i] == 0: continue
            await ctx.send(str(i + 1) + '    ' + games[i].type)
            c += 1
        if c == 0: await ctx.send('Käimasolevaid mänge ei ole.')
        return
    elif args[0].isnumeric():
        t = int(args[0]) - 1
        if t not in range(len(games)) or games[t] == 0:
            await ctx.send('ID ei ole kehtiv.')
            return
        game = games[t]
        try:
            if type(game) == hangman:
                res, go = game.guess(args[1])
            elif type(game) == titato.game_warp:
                res, go = game.move(ctx.author.mention, int(args[2]), int(args[1]))
            elif type(game) == titato2.game_warp:
                res, go = game.move(ctx.author.mention, int(args[2]), int(args[1]))
        except SyntaxError as err:
            print('SyntaxErr', err)
            res, go = str(err), False
        except Exception as err:
            print('Exception', err)
            res, go = str(err), False
        await ctx.send('**ID: ' + args[0] + '**  ' + res)
        if go:
            games[t] = 0
            await ctx.send(ctx.author.mention + ' oli viimane.')
        return
    await ctx.send('Proovi `?g help`')
    return


@bot.command()
async def hi(ctx):
    # Väike demo ajaloo vaatamisest.
    # Koosolekute ID: 499629361713119264
    t = ctx.author
    his = ctx.history(limit=5)
    out = ''
    async for msg in his:
        out += ''.join([msg.author.name, ': ', msg.content]) + '\n'
    out = out.replace('@', '(ät)')
    await ctx.send(out)
    await ctx.send('I heard you! {1}, {0}'.format(t.mention, t.name))


@bot.command()
async def ping(ctx, wait='5'):
    # Pingimine. Vastab sõnumile ja kustutab 10 sekundi pärast.
    # Koosolekute ID: 499629361713119264
    t = ctx.author
    rdr1, rdr2 = 'Ping ping, {0}; {1}ms! Kustub '.format(t.mention, str(round(bot.latency, 3))), ' sekundi pärast.'
    print(wait, [wait], wait.isdigit())
    if wait.isdigit():
        wait = int(wait)
    else:
        wait = 5
    msg = await ctx.send(rdr1 + str(wait) + rdr2)
    for i in range(wait - 1, -1, -1):
        await asyncio.sleep(1)
        await msg.edit(content=rdr1 + str(i) + rdr2)
    await msg.delete()
    await ctx.message.delete()


def find_user(text, server):
    nimi = text
    if nimi[:2] == '<@':
        uid = data[server].archive['meta']['userindex'].index(nimi[2:-1])
    elif nimi == '-1':
        return -1
    elif nimi.isdecimal():
        if len(nimi) > 10:
            uid = data[server].archive['meta']['userindex'].index(nimi)
        else:
            return int(nimi)
    else:
        uid = list(filter(lambda x: nimi.lower() in data[server].users[x]['n'].lower(), data[server].users))[0]
    return uid


def find_channel(kanal, server):
    if kanal[:2] == '<#':
        xid = data[server].archive['meta']['channels'][kanal[2:-1]]
        return xid['name']
    else:
        return kanal


@bot.command()
async def define_old(ctx, *args):
    print(args)
    splt = list(args)
    await ctx.send(define_wrap(splt))


def define_wrap(splt):
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
            return 'Tulemusi ei leitud.'
        text2 = re.sub('<[\s\S]*?>', '', text)
        if asd:
            if len(text2) < 1300:
                return text2
            else:
                return 'Liiga pikk vastus\n' + text2[:1300]
        defin = re.split('\. [A-Z\d]', text2)[0] + '.'
        return defin
    except Exception as err:
        return err


@bot.command()
async def define(ctx, *args):
    results = define2(' '.join(args))  # Tagastab listi tulemustest.
    embed = discord.Embed(title=' '.join(args), color=0xc904e2, type='rich')
    c = 0
    for res in results:
        c += len(res)
        temp = res.strip().split('\n')
        if len(temp) == 1:
            field = res.strip().split(' ')[0].strip()
            defi = res.strip()
        else:
            field = temp[0].strip()
            defi = '\n'.join(temp[1:]).strip()
        if c < 5900:
            embed.add_field(name=field, value=defi, inline=False)
        else:
            embed.add_field(name='Liiga palju tulemusi', value='Rohkem vastuseid ei saa kuvada', inline=False)
            break
    if not results:
        embed.add_field(name='. . .', value='Tulemusi ei leitud', inline=False)
    await ctx.send(embed=embed)


def is_me(m):
    # print([m.content])
    if m.content.startswith('? g'): return True
    if m.content.startswith('?g '): return True
    if m.content.startswith('?cleanup'): return True
    # if m.author == bot.user: return True
    return (m.content.startswith('**ID')) or \
           (m.content.startswith('ID')) or m.content.startswith('?wait') or \
           ('hangman' in m.content.lower()) or \
           ('> oli viimane.' in m.content.lower()) or \
           (m.content.startswith('Mängu ID'))


def is_me2(m):
    return m.author == bot.user or m.content.startswith('?')


@bot.command()
@commands.check(alll)
async def cleanup2(ctx, n=15):
    if n > 1000: n = 500
    if n < 2: n = 2
    t = ctx.author
    # his = ctx.history(limit=5)
    deleted = await ctx.channel.purge(limit=n, check=is_me)
    await ctx.send('deleted ' + str(len(deleted)))


@bot.command()
@commands.check(alll)
async def cleanup(ctx, n=15):
    if n < 2: n = 2
    t = ctx.author
    deleted = await ctx.channel.purge(limit=n, check=is_me2)
    await ctx.send('deleted ' + str(len(deleted)))


def define2(msg):
    try:
        asd = 1
        ms = msg
        regex = r"<div class=\"tervikart\">[.\s\S\d\D]*?<\/div>"
        regex2 = r"<span class=\"leitud_ss\">([.\s\S\d\D]*?)<\/span>"
        adr = urllib.request.quote(ms)
        adr = 'https://www.eki.ee/dict/ekss/index.cgi?Q=' + adr
        req = urllib.request.Request(adr)
        response = urllib.request.urlopen(req)
        the_page = response.read().decode('utf8')
        matches = re.finditer(regex, the_page, re.MULTILINE)
        results = []
        for matchNum, match in enumerate(matches, start=1):
            text = match.group()
            try:
                text = text.replace('<br/>', '\n').replace('\n\n', '\n')
            except Exception as err:
                return [err]
            for matchNum, match in enumerate(re.finditer(regex2, text, re.MULTILINE)):
                title = match.group(1)
                break
            text2 = re.sub('<[\s\S]*?>', '', text)
            if len(text2) < 1020:
                results.append(text2)
            else:
                results.append(
                    text2.split('\n')[0] + '\n**Liiga pikk vastus**\n' + '\n'.join(text2.split('\n')[1:])[:1000])
        return results
    except Exception as err:
        return [err]


def stats(message):
    global data
    stat_col = 0xf27e54
    sisu = message.content
    # srv=str(message.guild)
    #    if srv=='java 2019':
    server = str(message.guild)
    if server not in data:
        server = 'java 2019'
        # return 'Selles serveris statisika ei tööta' # str(list(data))
    commands = sisu.split()[1:]
    kanalid = '**Võimalikud ühendatud kanalid:**\n`    Kokku`\n`    ├───EX`\n`    ├───PR`\n`    ├───Syva`\n`    │   ├───DJ`\n`    │   └───XP`\n`    └───Üldine`'
    help_msg = '**Docs:**\n?stats edetabel <kasutajanimi> *<n>*\n?stats ajatabel <kasutajanimi> <kanal>\n?stats ajatabel2 <kasutajanimi> <kanal> *- Graafik*\n?stats top <n>\n\n' + kanalid
    if len(commands) == 0: return ('Viga, katkine asi. \n' + help_msg)
    if commands[0] == 'help':
        return (help_msg)
    elif commands[0] == 'edetabel':
        embed = discord.Embed(title='Statistika', description=kellad[server] + ' seisuga.', color=stat_col)
        if len(commands) < 3:
            if len(commands) == 1: return ('Viga, kasutajatunnus on puudu.')
            if len(commands) == 2: num = 5
        else:
            num = int(commands[2])
        nimi = commands[1]
        try:
            uid = find_user(nimi, server)
        except IndexError:
            return ('Viga, kasutajat ei leitud.')
        stri = data[server].graafid_edetabel(uid, uid=True, n=num)
        for part in stri.strip().split('\n\n**'):
            part = part.strip()
            hdr = part.split('\n')[0].strip('*')
            part = '\n'.join(part.strip().split('\n')[1:])
            embed.add_field(name=hdr, value=part, inline=False)
        return embed  # ('Statistika ' + kellad[server] + ' seisuga.' +stri)
    elif commands[0] == 'ajatabel':
        if len(commands) < 3:
            return ('Viga, vaja on kasutajat ja kanalit.')
        try:
            uid = find_user(commands[1], server)
        except IndexError:
            return ('Viga, kasutajat ei leitud.')
        kanal = find_channel(commands[2], server)
        try:
            return ('Statistika ' + kellad[server] + ' seisuga.\n' + '```' +
                    data[server].ajatabel_vaiksem(uid, kanal) + '```')
        except KeyError:
            return ('Viga, tundmatu kanal.\n ' + kanalid)
    elif commands[0] == 'ajatabel2':
        if len(commands) < 3:
            return ('Viga, vaja on kasutajat ja kanalit.')
        try:
            uid = find_user(commands[1], server)
        except IndexError:
            return ('Viga, kasutajat ei leitud.')
        kanal = find_channel(commands[2], server)
        try:
            return ('Statistika ' + kellad[server] + ' seisuga.\n' + '```' +
                    data[server].ajatabel_vaiksem2(uid, kanal) + '```')
        except KeyError:
            return ('Viga, tundmatu kanal.\n ' + kanalid)
    elif commands[0] == 'top':
        n = int(commands[1])
        embed = discord.Embed(title='Statistika' + kellad[server] + ' seisuga.',
                              description=message.author.name + ': ' + ' '.join(commands), color=stat_col)

        # Esitab top N praeguses kanalis ja kokku.
        # data['java 2019'].users[uid]['count']
        def helper(x, cha):
            if cha in data[server].users[x]['count']:
                return data[server].users[x]['count'][cha]
            else:
                return 0

        out = ''
        ch = str(message.channel)
        kokku = list(sorted(data[server].users, key=lambda x: data[server].users[x]['count']['Kokku']))[-abs(n) - 1:]
        kanalis = list(sorted(filter(lambda x: helper(x, ch), data[server].users), key=lambda x: helper(x, ch)))[
                  -abs(n) - 1:]
        # print(kokku, kanalis)
        for i in kokku:
            out += data[server].users[i]['n'] + '\t' + str(data[server].users[i]['count']['Kokku']) + '\n'
        if len(out) == 0: out = '<tühi>'
        embed.add_field(name='Kogu serveris:', value=out)
        out = ''
        for i in kanalis:
            out += data[server].users[i]['n'] + '\t' + str(data[server].users[i]['count'][ch]) + '\n'
        if len(out) == 0: out = '<tühi>'
        embed.add_field(name='Siin kanalis:', value=out)
        return embed
    elif commands[0] == 'update':
        # d=stats_load()
        d = stats_load2(server)
        if d[0]:
            data[server] = d[1]
        return 'Uuendatud ' + kellad[server]
    else:
        return ('Viga, katkine asi.\n' + help_msg)


def ilma_output(data, location):
    embed = discord.Embed(title=data['vt1observation']['phrase'], description=location, color=0x2a85ed, type='rich')
    embed.set_thumbnail(url='http://l.yimg.com/a/i/us/we/52/' + str(data['vt1observation']['icon']) + '.gif')
    embed.add_field(name='Temperatuur ' + str(data['vt1observation']['temperature']) + 'C',
                    value='Näiv temperatuur ' + str(data['vt1observation']['feelsLike']) + 'C', inline=False)
    embed.add_field(name='Tuule suund ' + str(data['vt1observation']['windDirCompass']) + '',
                    value='Tuule kiirus ' + str(round(data['vt1observation']['windSpeed'] / 3.6, 1)) + 'm/s',
                    inline=False)
    embed.add_field(name='Õhuniiskus ' + str(data['vt1observation']['humidity']) + '%',
                    value='Kastepunkt ' + str(data['vt1observation']['dewPoint']) + 'C', inline=False)
    embed.add_field(name=data['vt1dailyForecast']['dayOfWeek'][1],
                    value=data['vt1dailyForecast']['day']['narrative'][1])
    embed.add_field(name=data['vt1dailyForecast']['night']['dayPartName'][1],
                    value=data['vt1dailyForecast']['night']['narrative'][1])
    achtung = []
    if data['vt1alerts']:
        for i in range(len(data['vt1alerts']['headline'])):
            achtung.append(data['vt1alerts']['areaName'][i] + ' - ' + data['vt1alerts']['headline'][i])
        achtung = '\n'.join(achtung)
    else:
        achtung = 'Puuduvad'
    embed.add_field(name='Hoiatused:', value=achtung, inline=False)
    return embed


def ilma_output2(data, location):
    embed = discord.Embed(title=data['vt1observation']['phrase'], description=location, color=0x2a85ed, type='rich')
    embed.set_thumbnail(url='http://l.yimg.com/a/i/us/we/52/' + str(data['vt1observation']['icon']) + '.gif')
    embed.add_field(name='Temperatuur ' + str(data['vt1observation']['temperature']) + 'C',
                    value='Näiv temperatuur ' + str(data['vt1observation']['feelsLike']) + 'C', inline=False)
    embed.add_field(name='Tuule suund ' + str(data['vt1observation']['windDirCompass']) + '',
                    value='Tuule kiirus ' + str(round(data['vt1observation']['windSpeed'] / 3.6, 1)) + 'm/s',
                    inline=False)
    return embed


def ilm_output_table(data, location):
    ilm = dict(data)
    sep = ';'
    fn = ['ilm_daily.csv', 'ilm_hourly.csv']
    daily = True
    hourly = True
    encoding = 'cp1252'
    if daily:
        header = ['dayPartName', 'phrase', 'cloudPct', 'humidityPct', 'precipType', 'precipAmt',
                  'precipPct', 'qualifier', 'snowRange', 'temperature', 'thunderEnumPhrase',
                  'thunderEnum', 'uvIndex', 'uvDescription', 'windDirCompass', 'windDirDegrees',
                  'windSpeed', 'icon', 'iconExtended', 'narrative']
        output = [header]
        for x in range(15):
            output.append([])
            for i in header:
                output[-1].append(ilm['vt1dailyForecast']['day'][i][x])
            output.append([])
            for i in header:
                output[-1].append(ilm['vt1dailyForecast']['night'][i][x])
        f = open(fn[0], 'w', encoding=encoding)
        for i in output:
            if set(i) == {None}: continue
            txt = sep.join(list(map(str, i[:-1]))).replace('.', ',') + sep + i[-1]
            f.write(txt + '\n')
        f.close()
    if hourly:
        header = ['processTime', 'dayInd', 'phrase', 'rh', 'precipPct', 'precipType',
                  'severity', 'temperature', 'feelsLike', 'uvIndex', 'windDirCompass',
                  'windDirDegrees', 'windSpeed', 'icon', 'iconExtended']
        output = [header]
        for x in range(len(ilm['vt1hourlyForecast']['processTime'])):
            output.append([])
            for i in header:
                output[-1].append(ilm['vt1hourlyForecast'][i][x])
        f = open(fn[1], 'w', encoding=encoding)
        for i in output:
            txt = sep.join(list(map(str, i))).replace('.', ',')
            f.write(txt + '\n')
        f.close()
    return fn


def ilm_getData(a):
    if a == '':
        x = {'lat': 59.43696079999999, 'lng': 24.7535747}
        loc = 'Tallinn'
    else:
        x2 = funk.coord(a)
        if len(x2['results']) == 0:
            return channel.send("ERROR: Asukohta ei leitud.")
        x = x2['results'][0]['geometry']['location']
        loc = x2['results'][0]['formatted_address']
    return funk.ilm.weatherAPI(x['lat'], x['lng']), loc


@bot.event  # type: ignore
async def on_raw_reaction_add(payload) -> None:
    # Probably needs testing. It should maybe remove bot's own message, 
    # if someone reacts with wastebasket emoji
    # For safety reasons, it should also authenticate reacting user 
    waste_basket=b'\xf0\x9f\x97\x91\xef\xb8\x8f'
    if (payload.emoji.name.encode('utf8')!=waste_basket):
        return
    # Fetch message is rather slow operation, that's why it only takes place if user reacts with wastebasket
    msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    # Safety checks
    if (msg.author!=bot.user and msg.author!=payload.member):
        return
    await msg.delete()


async def reactor(message):
    global last_reac
    user = message.author.name.lower()
    srv = str(message.guild)
    if user not in last_reac:
        last_reac[user] = dict()
    if srv not in last_reac[user]:
        last_reac[user][srv] = 0
    if time.time() - last_reac[user][srv] < 600:
        return False
    last_reac[user][srv] = int(time.time())
    if user.startswith('kadri'):
        if srv == 'java 2019':
            await message.add_reaction(bot.get_emoji(547512864252887041))
        else:
            await message.add_reaction(u"\U0001F916")
    if user.startswith('ago'):
        if srv == 'java 2019':
            await message.add_reaction(bot.get_emoji(535201597131849768))
        if srv == 'py2018':
            await message.add_reaction(bot.get_emoji(507250218484629524))
    if user.startswith('test9'):
        if srv == 'py2018':
            await message.add_reaction(bot.get_emoji(506934160250765323))
        elif False:
            for i in range(18):
                await message.add_reaction('\U0001f50d')
    print(srv,srv=='bot test', message.content,  'test' in message.content)
    # print(dir(bot.user))
    print(message.author.bot)
    if  not message.author.bot:  # srv=='bot test' and
        async with message.channel.typing():
            reaction_string='\U0001f50e'  # :mag_right:
            await message.add_reaction(reaction_string)
            def check(reaction, user_obj):
                return user_obj == message.author and str(reaction.emoji) == reaction_string

            try:
                reaction, user_obj = await bot.wait_for('reaction_add', timeout=15.0, check=check)
            except asyncio.TimeoutError:
                # User didn't respond
                await message.clear_reaction(reaction_string)
            else:
                # User responded
                await message.clear_reaction(reaction_string)
                # Run queries
        print(0)
    if user.startswith('rauno'):
        last_reac[user][srv] = int(time.time()) + 30
        for i in range(1):
            try:
                await message.add_reaction(random.choice(all_emojis))
            except discord.errors.HTTPException:
                try:
                    await message.add_reaction(random.choice(all_emojis))
                except:
                    pass
    if user.startswith('sebastian'):
        pass
        #await message.add_reaction(u"\U0001F34D")
        #await message.add_reaction(u"\U0001F355")
    if user.startswith('elvar'):
        await message.add_reaction(u"\U0001F37A")


async def wait(channel, sisu, user, uid):
    try:
        x = ' '.join(sisu.split()[2:])
        # Ajatempli lugemine
        a = sisu.split()[1]
        if a.isdecimal():
            a = int(a)
            stamp = time.strftime('%d.%m.%y_%H:%M', time.localtime(time.time() + a))
        else:
            stamp = str(a)
            a = time.mktime(datetime.datetime.strptime(stamp, '%d.%m.%y_%H:%M').timetuple()) - int(time.time())
        # Kanali olemasolu kontroll.
        kanal2 = channel
        idd = channel.id
        isuser = False
        # Kontrollib, kas mainitud inimene on sama inimene kes saatis sõnumi
        SAMA_INIMENE = lambda sisu, uid: sisu.split()[2] == '<@!' + str(uid) + '>'
        TEINE_INIMENE = lambda sisu, uid: len(sisu.split()[2]) == len('<@!' + str(uid) + '>') and  sisu.split()[2].startswith('<@')
        KANAL = lambda sisu, uid: sisu.split()[2].startswith('<#') and sisu.split()[2].endswith('>')
        print('debug',sisu,'\n', uid, sisu.split()[2])
        print(KANAL(sisu, uid), SAMA_INIMENE(sisu, uid), TEINE_INIMENE(sisu, uid))
        if KANAL(sisu, uid):
            idd = int(sisu.split()[2][2:-1])
            kanal2 = bot.get_channel(idd)
            x = ' '.join(sisu.split()[3:])
        # Juhul, kui teade algab selle isiku tagiga, kes on autor, 
        # siis me ei hakka kanalit reostama, vaid kirjutame talle otse.
        # Teoreetiliselt võime saata teate ka teisele inimesele.
        elif TEINE_INIMENE(sisu, uid):  # DM/PM
            print("Oli vist sama inimene")
            print(sisu.split()[2])
            idd = int(sisu.split()[2][3:-1])  # UID juhul, kui märgitakse keegi kolmas.
            print(idd)
            kanal2 = await bot.fetch_user(idd)
            x = ' '.join(sisu.split()[3:])
            isuser = True
        if a > 120:
            await channel.send('Vastu võetud ' + str(x) + ', esitamisel ' + stamp)
        # Ma tahaks kuskile siia panna süsteemi, mis salvestab edastatavad teated vahepeal tekstifaili.
        # Salvestada: usch - kasutaja või kanal; idd - kanali ID, kuhu sõnum saata.; stamp - ajatempel, millest tuletada ooteaeg.
        iad = ['<@' + str(abs(uid)) + '> ', '', '- '][1]  # Võimalik spämmiennetus.
        msg = iad + str(x)
        to_save = [stamp, isuser, idd, msg]
        f = open('wait_queue.txt', 'a')
        print(*to_save, sep=';\'', file=f)
        f.close()
        await asyncio.sleep(a)
        await kanal2.send(msg)
    except Exception as err:
        await channel.send(str(err))


@bot.command(pass_context=True)
async def spam(ctx, *args):
    chance = random.random()
    if ctx.author.name.lower().startswith('elvar'):
        chance += 0.5
    if chance < 0.75:
        a = time.localtime()
        await ctx.send('Kell on ' + time.strftime('%H:%M', a) + ', ' + random.choice(textid[a.tm_hour]))
    else:
        reso = gg_img('asd spam canned pork')
        e = discord.Embed(title='Juhuslik otsingutulemus', color=0x0c9c6c)
        e.set_image(url=reso[random.randint(0, len(reso) - 1)])
        await ctx.send(embed=e)


@bot.command(pass_context=True)
async def miami(ctx, tz='America/New_York', *args):
    # https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568
    chance = random.random()+0.0
    if ctx.author.name.lower().startswith('elvar'):
        chance += 0.5
    if chance < 0.05:  # 0.75
        if tz in pytz.all_timezones:
            miami = pytz.timezone(tz)
        elif tz.title in pytz.all_timezones:
            miami = pytz.timezone(tz.title())
        elif tz.upper in pytz.all_timezones:
            miami = pytz.timezone(tz.upper())
        else:
            await ctx.send('Tundmatu ajavöönd. Vaata "https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568"')
            return
        a = pytz.timezone('UTC').localize(datetime.datetime.utcnow()).astimezone(miami)
        await ctx.send('Seal on kell ' + datetime.datetime.strftime(a,'%H:%M'))
    else:
        reso = gg_img(('asd '+tz.replace('/',' ').replace('_',' ')+' '+' '.join(args)).strip())
        e = discord.Embed(title='Juhuslik otsingutulemus', color=0xb2bf1d)
        e.set_image(url=reso[random.randint(0, len(reso) - 1)])
        await ctx.send(embed=e)


@bot.command(pass_context=True)
async def pelmeen(ctx, *args):
    return await ctx.send('https://nami-nami.ee/retsept/2442/pelmeenid_lihaga')


@bot.command(pass_context=True)
async def unread2(ctx, *args):
    msg=ctx.author.mention+' '+' '.join(args)+' readme!'
    kanalid=ctx.guild.channels

    
    for ch in sorted(list(filter(lambda x:type(x)==discord.channel.TextChannel,ctx.guild.channels)), key=lambda x:(x.category_id,x.id)):
        if type(ch)==discord.channel.TextChannel:
            #await ch.edit(name='asdasd_'+ch.name)
            print(ch.name)
            try:
                await ch.send(msg)
                await asyncio.sleep(0.1)
                await ch.purge(limit=1, check=lambda x:is_me2)
                await asyncio.sleep(0.4)
            except discord.errors.Forbidden:
                pass
    return 0#await ctx.send(':)')

@bot.command(pass_context=True)
async def unread(ctx, *args):
    msg=ctx.author.mention+' '+' '.join(args)+' readme!'
    kanalid=ctx.guild.channels
    kanalid=[ctx.channel]
    
    for ch in sorted(list(filter(lambda x:type(x)==discord.channel.TextChannel,ctx.guild.channels)), key=lambda x:(x.category_id,x.id)):
        if type(ch)==discord.channel.TextChannel:
            #await ch.edit(name='asdasd_'+ch.name)
            print(ch.name)
            try:
                await ch.send(msg)
                await asyncio.sleep(0.1)
                await ch.purge(limit=1, check=lambda x:is_me2)
                await asyncio.sleep(0.4)
            except discord.errors.Forbidden:
                pass
    return 0#await ctx.send(':)')

"""

def is_me2(m):
    return m.author == bot.user or m.content.startswith('?')


@bot.command()
@commands.check(alll)
async def cleanup2(ctx, n=15):
    if n > 1000: n = 500
    if n < 2: n = 2
    t = ctx.author
    # his = ctx.history(limit=5)
    deleted = await ctx.channel.purge(limit=n, check=is_me)
    await ctx.send('deleted ' + str(len(deleted)))


@bot.command()
@commands.check(alll)
async def cleanup(ctx, n=15):
    if n < 2: n = 2
    t = ctx.author
    deleted = await ctx.channel.purge(limit=n, check=is_me2)
    await ctx.send('deleted ' + str(len(deleted)))
"""
def is_me3(m):
    x=m.reactions
    print(len(x))
    global reaktsioon
    if len(x)!=0:
        y=x[0]
        reaktsioon=y
        counts = {react.emoji: react.count for react in m.reactions}
        print(type(x[0]))
        print(dir(y))
        print(counts)
    return False


@bot.command(pass_context=True)
async def c(ctx, *args):
    n=2
    t = ctx.author
    deleted = await ctx.channel.purge(limit=n, check=is_me3)
    print('deleted ' + str(len(deleted)))



@bot.command(pass_context=True)
async def invite(ctx, *args):
    return await ctx.send('Call me maybe:\n' + Link)


@bot.command(pass_context=True)
async def week(ctx, *args):
    if datetime.datetime.utcnow().isocalendar()[1] - 35>-1:
        wk=datetime.datetime.utcnow().isocalendar()[1] - 35
    elif datetime.datetime.utcnow().isocalendar()[1] - 4>-1:
        wk=datetime.datetime.utcnow().isocalendar()[1] - 4
    else:
        wk=datetime.datetime.utcnow().isocalendar()[1] - 35+52
    if wk<20:
        await ctx.send(str(wk) + '. nädal.')
    else:
        await ctx.send('Vaheaeg ('+str(wk)+'. nädal?)')


@bot.command(pass_context=True)
async def hallo(ctx, *args):
    # Args tuple sõnedega, mis tulid argumentidena.
    await ctx.send(str(args))


"""
channel = message.channel 
sisu = message.content
uid = int(message.author.id)
user = message.author.name
"""


@bot.event
async def on_message(message):
    channel = message.channel
    sisu = message.content
    # if str(message.channel) not in ['botnet', 'random']:
    #    return
    uid = int(message.author.id)
    user = message.author.name
    tag = message.author.mention.replace('!', '')
    if len(sisu) > 2 and sisu[0] == '?':
        print(str(message.created_at)[:-10] + '    ' + sisu, user, sep='\t')
    if str(message.channel) in yldkanalid:
        await reactor(message)
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
            await channel.send("Tuvastatud kui " + result)
            await channel.send("Tulem: " + str(eval(result)))
        except Exception as err:
            await channel.send(err)
        return
    elif sisu.startswith('?ilm_raw'):
        asd, loc = ilm_getData(' '.join(sisu.split()[1:]))
        fn = 'ilm.json'
        json.dump(asd, open(fn, 'w', encoding='utf8'), ensure_ascii=False, indent=2)
        await channel.send('ilmast', file=discord.File(fn))
        return
    elif sisu.startswith('?ilm_tabel'):
        asd, loc = ilm_getData(' '.join(sisu.split()[1:]))
        fn1, fn2 = ilm_output_table(asd, loc)
        await channel.send('ilm 2 nädalat', file=discord.File(fn1))
        await channel.send('ilm 2 päeva', file=discord.File(fn2))
        return
    elif sisu.startswith('?miniilm'):
        asd, loc = ilm_getData(' '.join(sisu.split()[1:]))
        msg = ilma_output2(asd, loc)
        await channel.send(embed=msg)
        return
    elif sisu.startswith('?ilm'):
        asd, loc = ilm_getData(' '.join(sisu.split()[1:]))
        msg = ilma_output(asd, loc)
        await channel.send(embed=msg)
        return
    elif sisu.startswith('?wait'):
        if user in blacklist:
            return await channel.send('blacklisted')
        return await wait(channel, sisu, user, uid)
    elif sisu.startswith('?stats'):
        x = stats(message)
        if type(x) == discord.Embed:
            return await channel.send(embed=x)
        else:
            return await channel.send(x)
    elif sisu.startswith('?search_img'):
        reso = gg_img(sisu)
        if len(reso) == 1 and reso[0].startswith('You did it!'):
            return await channel.send('Tulemusi ei leitud.')
        e = discord.Embed(title='Juhuslik otsingutulemus', color=0xd81c0f)
        e.set_image(url=reso[random.randint(0, 9)])
        await channel.send(embed=e)
        return
    elif sisu.startswith('?search2'):
        reso = gg(sisu)
        if len(reso) == 1 and reso[0].startswith('You did it!'):
            return await channel.send(reso[0])  # Tulemusi ei leitud.
        embed = discord.Embed(title='Otsingutulemused', description=sisu[8:], color=0xd81c0f, type='rich')
        for res in reso:  # Kuvab 3 tulemust.
            embed.add_field(name=res[0], value=res[1] + '\n' + res[2], inline=False)
        
        reso = gg_img(sisu)
        if not (len(reso) == 1 and reso[0].startswith('You did it!')):
            embed.set_thumbnail(url=reso[0])
        
        return await channel.send(embed=embed)
    elif sisu.startswith('?search'):
        reso = gg(sisu)
        if len(reso) == 1 and reso[0].startswith('You did it!'):
            return await channel.send(reso[0])  # Tulemusi ei leitud.
        embed = discord.Embed(title='Otsingutulemused', description=sisu[8:], color=0xd81c0f, type='rich')
        for res in reso:  # Kuvab 3 tulemust.
            embed.add_field(name=res[0], value=res[1] + '\n' + res[2], inline=False)
        return await channel.send(embed=embed)
    elif sisu.strip() == '?reset':
        print('RESET')
        print(tag, '\n', test)
        print('-----------------')
        if tag == test:
            await channel.send('Restarting...')
            #exit()
            print(discord.Status.dnd)
            await bot.change_presence(status=discord.Status.dnd, activity=discord.Game('None'))
            
            #
            return
        else:
            await channel.send('no')
    elif list(re.finditer(r"\bhmm\b", sisu, re.IGNORECASE)) and not sisu.startswith(
            '?') and tag != bvb and user != 'anubis':
        await channel.send('Mitte hmm, vaid hm või hmh!')
    elif sisu.lower().startswith('tere'):
        if tag == bvb: return
        if '<@' in sisu and bvb not in sisu: return
        for n in ['kadri', 'piret', 'sebastian', 'elvar', 'anubis', 'test', 'ago']:
            if n in sisu.lower() and 'bot' not in sisu.lower(): return
        print(str(message.created_at)[:-10] + '    ' + sisu, user, sep='\t')  # Logimine tere jaoks.
        if user.lower().startswith('kadri'):
            return await channel.send('<@' + str(abs(uid)) + '>' + ', **pelmeen!**')
        await channel.send('<@' + str(abs(uid)) + '>' + ', **tere!**')
    elif bvb in sisu.lower():
        if tag != bvb:
            await channel.send('I heard you! {1}, {0}'.format(tag, user))
    await bot.process_commands(message)


async def list_servers():
    await bot.wait_until_ready()
    global data
    while not bot.is_closed():
        print("Current servers: " + ', '.join(list(map(lambda x: x.name, bot.guilds))))
        for srv in list(map(lambda x: x.name, bot.guilds)):
            if srv not in kellad:
                kellad[srv] = ''
            tmp = stats_load2(srv)
            if tmp[0]: data[srv] = tmp[1]
        await asyncio.sleep(600)  # 600
        # Lisada kontroll, kas kood on muutunud?
        # Pole vajalik, sest niikuinii saaks teha käsitsi taaskäivituse.


async def import_wait_tasks():
    await asyncio.sleep(15)
    f = open('wait_queue.txt')
    tmp = f.readlines()
    f.close()
    # print(tmp)
    # kasutame koha peal ootamise genereerimist?
    f = open('wait_queue.txt', 'w')
    loop = asyncio.get_event_loop()
    for i in tmp:
        x = i.strip().split(';\'')
        a = time.mktime(datetime.datetime.strptime(x[0], '%d.%m.%y_%H:%M').timetuple()) - int(time.time())
        if a > -20:
            a = max([a, 0])
            print(*x, sep=';\'', file=f)

            async def bg_wait_task(a=a, x=x):
                if x[1] == 'True':  # DM/PM
                    kanal2 = bot.fetch_user(int(x[2]))
                else:
                    kanal2 = bot.get_channel(int(x[2]))
                await asyncio.sleep(a)
                await kanal2.send(x[3])

            loop.create_task(bg_wait_task())
    f.close()


bot.loop.create_task(import_wait_tasks())
bot.loop.create_task(list_servers())
bot.loop.create_task(troll_task())
bot.run(võti + rõngas)
