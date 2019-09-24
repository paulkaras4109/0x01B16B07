import discord
from discord.ext import commands
from discord.utils import get
import constants
import os
import asyncio
import sys

import time
import random

from mcstatus import MinecraftServer

bot = commands.Bot(command_prefix = "$", description=constants.description)

@bot.event
async def on_ready():
    print("init successful")
    await bot.change_presence(activity=discord.Game(name='existence - $help', type=2))

@bot.command()
async def hello(ctx):
    '''
    Says "World"
    Usage: $world
    '''
    await ctx.send("World")

@bot.command()
async def checkme(ctx):
    '''
    Checks your message
    Usage: $checkme3
    '''
    checked = bot.get_emoji(408868557078921216)

    await ctx.message.add_reaction(checked)

@bot.command()
async def joined(ctx, member : discord.Member):
    '''
    Says when a member joined the server.
    '''
    await ctx.send('{0.name} joined in {0.joined_at}'.format(member))
    
@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)

@bot.command()
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
    
    await ctx.send(pasta)

@bot.command()
async def pic(ctx):
    '''
    Outputs an image into the channel
    Usage: $pic 'source'
    Avalibe Sources: google, anime, comfy, homework
    If a key is not specified, a random one is chosen.
    'homework' is an NSFW key and can only be used in NSFW channels.
    '''
    
    args = ctx.message.content.split(" ")

    validpaths = ["google", "anime", "comfy", "homework", "art"]
    #We don't want to choose NSFW content as a random valid path
    vp_skinny = ["google", "anime", "comfy"]

    path = ""
    if len(args) == 2:
        if args[1] in validpaths:
            path = "/" + args[1] + "/"
        else:
            path = "/" + random.choice(vp_skinny) + "/"
    else:
        path = "/" + random.choice(vp_skinny) + "/"
    
    if (path == "/homework/" or path == "/art/") and (ctx.message.channel.is_nsfw() == False):
        await ctx.send("Calling NSFW command in non-NSFW channel. This incident will be reported.")
        return
    
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
    img = discord.File(f)
    await ctx.send(file=img)

@bot.command()
async def mcss(ctx):
    '''
    Gets the status of a Minecraft server
    Usage: $mcss 'ip'
    ip: an IPv4 address, including port (if not default 25565).
    If none is specified, defaults to "172.87.22.155:25565" (7h3 b1g 53rv3r)
    '''
    args = ctx.message.content.split(" ")

    ip = "172.87.22.155"

    if len(args) == 2:
        ip = args[1]
    
    try:
        mcserver = MinecraftServer.lookup(ip)

        status = mcserver.status()

        desc = status.description['text']

        vers = status.version.name
        serverinfo = "v" + vers

        if status.players.sample is not None:
            playernames = [x.name for x in status.players.sample]
        else:
            playernames = []

        playerlist = "{0} players online: {1}".format(status.players.online, ", ".join(playernames))


        msg = "```" + desc + "\n" + serverinfo + "\n" + playerlist + "```"
        await ctx.send(msg)

    except:
        await ctx.send("Error: could not contact MC server")

@bot.command()
async def selfie(ctx):
    '''
    Posts a selfie of the bot.
    '''
    
    path = "/selfies/"
    
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
    img = discord.File(f)
    await ctx.send(file=img)
    

token = os.environ.get("BOT_TOKEN")
bot.run(token)
