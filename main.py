import discord
import constants
import security
# In order to run the bot, create a file called 'security.py' and emplace a string varible containing the key

client = discord.Client()

@client.event
async def on_ready():
    print("init successful")
    await client.change_presence(game=discord.Game(name="existing - $help (eventually)"))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content == ("$Hello"):
        await client.send_message(message.channel, "World")
    if message.content == ("$help"):
        for i in range(0, len(constants.commands)):
            await client.send_message(message.channel, constants.commands[i])


client.run(security.token)