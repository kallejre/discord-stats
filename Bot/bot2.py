# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
import websockets

BOT_PREFIX = ("?", "!")

TOKEN = 'NDg2NDQ1MTA5NjQ3MjQ1MzMy.DnELrQ.WDT1RXBmKt61KbX9MgtoDYGgt8A'

client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command(name='square',
                description="Squares a number.",
                brief="Squares a number.",
                aliases=['sqr', 'Square'],
                pass_context=True)
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)
    await client.say("'ello wr1d!")


@client.command(name='bitcoin',
                description="Uses Coindesk API to get BitCoin price in USD.",
                brief="Returns BTC/USD.",
                pass_context=True)
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

async def troll_task():
    while not client.is_closed:
        tt=10
        try:
            await client.change_presence(game=Game(name="with humanoids"))
            await asyncio.sleep(tt)
            await client.change_presence(game=Game(name="with animals"))
            await asyncio.sleep(tt)
        except websockets.exceptions.ConnectionClosed:
            return

async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("\nCurrent servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(60)#600


client.loop.create_task(list_servers())
client.loop.create_task(troll_task())
client.run(TOKEN)
"""
async def status_task():
    while True:
        await test_bot.change_presence(...)
        await asyncio.sleep(10)
        await test_bot.change_presence(...)
        await asyncio.sleep(10)

@test_bot.event
async def on_ready():
    ...
    bot.loop.create_task(status_task())
"""
