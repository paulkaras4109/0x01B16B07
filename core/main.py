import discord
from discord.ext import commands
from discord.utils import get
import constants
import os
import asyncio
import sys

import time
import random
import urllib
from urllib import request
from bs4 import BeautifulSoup

bot = commands.Bot(command_prefix = "$", description=constants.description)
cli = discord.Client()
cli.login('NTQ4MDMyNzMyMDAxNzMwNTYx.D0_bOQ.5Pc_NtdFC0ox0Whn3v8embti_ac')

@bot.event
async def on_ready():
    print("init successful")
    await bot.change_presence(game=discord.Game(name="existing - $help"))

@bot.command()
async def hello():
    '''
    Says "World"
    Usage: $world
    '''
    await bot.say("World")

@bot.command(pass_context=True)
async def checkme(ctx):
    '''
    Checks your message
    Usage: $checkme
    '''
    checked = get(bot.get_all_emojis(), name = 'checked')
    await bot.add_reaction(ctx.message, checked)

@bot.command()
async def joined(member : discord.Member):
    '''
    Says when a member joined the server.
    '''
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.command(pass_context=True)
async def pasta(ctx):
    '''
    Prints a specified or random copypasta.
    Usage: $pasta 'key'
    Avalibe keys: enter 'list' as the key
    If key is not specified, a random one is chosen.
    '''
    keys = list(constants.pastas)
    args = ctx.message.content.split(" ")
    
    if (len(args) == 1):
        ps = random.choice(keys)
    else:
        ps = args[1].lower()

    try:
        pasta = constants.pastas[ps]
    except:
        pasta = "pasta not found"
    
    if ps == "list":
        pasta = keys
    
    await bot.say(pasta)

@bot.command(pass_context=True)
async def pic(ctx):
    args = ctx.message.content.split(" ")

    validpaths = ["google", "anime", "comfy", "homework"]

    path = ""
    if len(args) == 2:
        if args[1] in validpaths:
            path = "/" + args[1] + "/"
        else:
            path = "/" + random.choice(validpaths) + "/"
    else:
        path = "/" + random.choice(validpaths) + "/"
    
    pic = random.choice([
        x for x in os.listdir(path)
        if os.path.isfile(os.path.join(path, x))
    ])
    ext = os.path.splitext(pic)[1]
    while True:
        pic = random.choice([
            x for x in os.listdir(path)
            if os.path.isfile(os.path.join(path, x))
        ])
        ext = os.path.splitext(pic)[1]
        if (ext == '.png') or (ext == '.jpg') or (ext == '.gif') or (ext == '.webm'):
            break
    
    f = path + pic
    await bot.send_file(ctx.message.channel, f)


token = os.environ.get("BOT_TOKEN")
bot.run('token')