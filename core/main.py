import discord
from discord.ext import commands
from discord.utils import get
import constants
import os
import asyncio
import sys
import youtube_dl
import ffmpeg

import time
import random

from mcstatus import MinecraftServer

bot = commands.Bot(command_prefix = "$", description=constants.description)

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

@bot.command(pass_context=True, aliases=['yt'])
async def playyt(ctx, url: str):
    '''
    Plays a YouTube video in your current channel
    Usage: $playyt url
    url: the URL to a YouTube Video
    '''
    os.chdir('/Music/.tmp')
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music playing")
        return

    await join(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/Music/.tmp/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("/Music/.tmp"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    await ctx.send(f"Playing: {nname[0]}")
    print("playing\n")

@bot.command(pass_context=True, aliases=['lplay'])
async def localplay(ctx, num: int):
    '''
    Plays a song from the local library
    Usage: $localplay num
    num: int index of local song
    '''
    await join(ctx)
    voice = get(bot.voice_clients, guild=ctx.guild)
    
    songs = [x for x in os.listdir("/Music") if x.endswith('.flac') or x.endswith('mp3')]
    songname = songs[num]
    songname = "/Music/" + songname 


    voice.play(discord.FFmpegPCMAudio(songname))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    await ctx.send(f"Playing: {songname}")
    print("playing\n")

@bot.command(aliases=['llist'])
async def locallist(ctx):
    '''
    Lists the songs in the local library
    Usage: $locallist
    '''

    songs = [x for x in os.listdir("/Music") if x.endswith('.flac') or x.endswith('mp3')]

    for idx, s in enumerate(songs):
        songs[idx] = str(idx) + ': ' + s
    
    await ctx.send(songs)

@bot.command(aliases=['ladd'])
async def localadd(ctx, url: str):
    '''
    Adds a song from YouTube into the local song library
    Usage: $localadd url
    url: YouTube URL
    '''

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '/Music/%(title)s.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])
    
    await ctx.send("Downloaded link")

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
    Gets the status of a Minecraft server
    Usage: $mcss 'ip'
    ip: an IPv4 address, including port (if not default 25565).
    If none is specified, defaults to "b1gb055.xyz" (7h3 b1g 53rv3r)
    '''
    args = ctx.message.content.split(" ")

    ip = "b1gb055.xyz"

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
