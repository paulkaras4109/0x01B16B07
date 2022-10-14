import discord
from discord.ext import commands
from discord.utils import get
import constants
import yt_dlp
import ffmpeg

import time
import random
import os
import asyncio
import sys
import threading

from mcstatus import JavaServer

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = "$", description=constants.description, intents=intents)
lock = threading.Event()

@bot.event
async def on_ready():
    print("init successful")
    await bot.change_presence(activity=discord.Activity(name='existence - $help', type=discord.ActivityType.watching))

async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

@bot.command(pass_context=True, aliases=['bye'])
async def leave(ctx):
    '''
    Causes the bot to leave its current voice channel
    '''
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()


def unlock(err):
    lock.set()


@bot.command()
async def checkme(ctx):
    '''
    Checks your message
    Usage: $checkme
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
    '''
    Rolls a dice in NdN format.
    '''
    
    args = ctx.message.content.split(" ")
    if (len(args) < 2):
        await ctx.send('Not enough arguments!')
        return
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

@bot.command(aliases=['mc'])
async def mcss(ctx):
    '''
    Gets the status of a Java Minecraft server
    Usage: $mcss 'ip'
    ip: an IPv4 address, including port (if not default 25565).
    If none is specified, defaults to "b1gb055.xyz" (7h3 b1g 53rv3r)
    '''
    args = ctx.message.content.split(" ")

    ip = "192.168.1.172"

    if len(args) == 2:
        ip = args[1]
    
    try:
        mcserver = JavaServer.lookup(ip)

        status = mcserver.status()

        desc = status.description

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
async def ytplay(ctx, url: str):
    '''
    Play audio from a youtube video link, and stream it to your current channel.
    Usage: $ytplay 'url'
    url: the URL to a YouTube video
    '''
    ytdl = yt_dlp.YoutubeDL(constants.ytdl_format_options)
    loop = loop or asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
    if 'entries' in data:
        data = data['entries'][0]
    filename = data['title'] if stream else ytdl.prepare_filename(data)

    await join(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    voice.play(discord.FFmpegPCMAudio(filename))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.5

    nname = filename.rsplit('-', 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")


token = os.environ.get("BOT_TOKEN")
bot.run(token)
