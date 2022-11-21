from itertools import cycle
import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv
import sys

import VacChecker

intents = discord.Intents.all()
client = commands.Bot(command_prefix = ".", intents=intents)

status = cycle(["your steam accounts!", "to see who gets banned!"])

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

@client.event
async def on_ready():
    change_status.start()
    print("Bot is ready!")

@client.event
async def on_message(message):
    if isinstance(message.channel, discord.channel.DMChannel) and message.author != client.user:
        await message.channel.send("This is a DM")
        await message.channel.send(VacChecker.VacChecker())

@tasks.loop(seconds=1)
async def change_status():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name = (next(status))))
    

client.run(TOKEN)

