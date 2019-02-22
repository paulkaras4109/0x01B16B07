import discord
from discord.ext import commands
from discord.utils import get
import constants
import os
import asyncio
import sys

import time
import random

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

    validpaths = ["google", "anime", "comfy", "homework"]

    path = ""
    if len(args) == 2:
        if args[1] in validpaths:
            path = "/" + args[1] + "/"
        else:
            path = "/" + random.choice(validpaths) + "/"
    else:
        path = "/" + random.choice(validpaths) + "/"
    
    if (path == "/homework/") and (ctx.message.channel.is_nsfw() == False):
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
    await ctx.send_file(ctx.message.channel, f)

@bot.command()
async def checknsfw(ctx):
    if (ctx.channel.is_nsfw()):
        await ctx.send("This is an NSFW channel")
    else:
        await ctx.send("This isn't an NSFW channel")


token = os.environ.get("BOT_TOKEN")
bot.run(token)