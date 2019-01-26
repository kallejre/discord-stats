# Bot versioon 3. Eesmärk asjast aru saada.
# Ühildub ainult Py3.6-ga (3.5 ja 3.7 ei tööta).
import discord
from discord.ext import commands
import asyncio
import re
import funk
import random

BOT_PREFIX = ("?", "!")
TOKEN = 'NDg2NDQ1MTA5NjQ3MjQ1MzMy.DnELrQ.WDT1RXBmKt61KbX9MgtoDYGgt8A'
bot = commands.Bot(command_prefix=BOT_PREFIX,
                      description='Bot for tests')
blacklist=[]
atvs=0

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

@bot.command()
async def add(ctx, a: int, b: int):
    await ctx.send(a+b)

@bot.command()
async def multiply(ctx, a: int, b: int):
    await ctx.send(a*b)

@bot.command()
async def divide(ctx, a: float, b: float):
    await ctx.send(a/b)

@bot.command()
async def math(ctx, a: str):
    result = re.sub('[^0-9^.^*^+^/^\-^(^)^ ^%]','', a)
    print(result)
    await ctx.send("Understood as "+result)
    await ctx.send("Result: "+str(eval(result)))

@bot.command()
async def ilm(ctx, a: str):
    x=funk.coord(a)
    print(x)
    await ctx.send("Location coordinates: "+str(x))
    asd=funk.ilm.weatherAPI(x['lat'],x['lng'])
    #print(asd)
    msg='Kuupäev: '+asd['vt1dailyForecast']['validDate'][0].split('T')[0]+', '+asd['vt1dailyForecast']['dayOfWeek'][1]+':\n'
    msg+=asd['vt1dailyForecast']['day']['narrative'][1]+'\n'
    msg+=asd['vt1dailyForecast']['night']['dayPartName'][1]+':\n'
    msg+=asd['vt1dailyForecast']['night']['narrative'][1]
    await ctx.send(msg)

@bot.command()
async def greet(ctx):
    await ctx.send(":smiley: :wave: Hello, {0}!".format(ctx.author.mention))

@bot.command()
async def cat(ctx):
    await ctx.send("https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif")

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

@bot.command()
async def test(ctx):
    t=ctx.author
    print(t.name, t.id)
    blacklist.append(ctx)
    await ctx.send('I heard you! {0}'.format(ctx.author.mention))
    # await ctx.send('I heard you! {0} <@{1}>'.format(*str(ctx.author).split('#')))

@bot.command()
async def loop(ctx, key: str, time:int, funk:callable, arg:str='_'):
    t=ctx.author
    print(t.name, t.id)
    blacklist.append(ctx)
    if atvsvc(key):
        await ctx.send('Key updated')
        # Tee midagi tarka
    else:
        await ctx.send(':regional_indicator_w::regional_indicator_r::regional_indicator_o::regional_indicator_n::regional_indicator_g:    :regional_indicator_p::regional_indicator_a::regional_indicator_s::regional_indicator_s::regional_indicator_w::regional_indicator_o::regional_indicator_r::regional_indicator_d:')
    # await ctx.send('I heard you! {0} <@{1}>'.format(*str(ctx.author).split('#')))


async def list_servers():
    await bot.wait_until_ready()
    while not bot.is_closed():
        print("\nCurrent servers:")
        for server in bot.guilds:
            print(server.name)
        await asyncio.sleep(600)#600

bot.remove_command('help')

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

bot.loop.create_task(list_servers())
bot.run(TOKEN)
